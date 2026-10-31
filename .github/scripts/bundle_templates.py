#!/usr/bin/env python3
"""把 templates/**/*.toml 机械拼接成 dist/templates.toml（WebUI 在线模板库一次性拉取）。

设计约束（都为「零耦合」服务）：
- 输出结构与单个模板文件、与 config.toml 完全一致：只有 `[templates."<键>"]` 表；
- **不改写任何字段**——每个表的表体逐字来自源文件，只把表头换成文件名（stem）；
- 不写时间戳等易变内容 → 同样输入必得同样字节，`--check` 可做逐字节比对，
  版本识别交给 git blob sha（WebUI 从 git tree 接口免费拿到）；
- 不新增任何字段语义：WebUI 用现有 `sanitizeTemplate` 即可消费。

同时把两条隐含不变式变成硬检查（fail 而不是静默降级）：
- 每个模板文件必须是「恰好一个 [templates."<名字>"] 表、无其它顶层键、无子表」；
- stem 必须全局唯一——WebUI 用 stem 作为导入键，同名会让两条模板互相覆盖。

**dist/templates.toml 是 CI 产物，PR 不需要提交它**：push 到 main 后由
`.github/workflows/bundle.yml` 运行本脚本并自动提交（见该 workflow 的说明）。
PR 侧只用 `--stdout` 验证「模板能否被聚合成 bundle」，不比对文件。

用法：
    python .github/scripts/bundle_templates.py            # 本机手动生成 dist/templates.toml
    python .github/scripts/bundle_templates.py --check     # 校验工作区文件是否与源文件一致
    python .github/scripts/bundle_templates.py --stdout    # 只把聚合结果打到 stdout（PR CI 用）
"""

from __future__ import annotations

import os
import sys
import tomllib
from dataclasses import dataclass

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(REPO_ROOT, "templates")
OUTPUT_PATH = os.path.join(REPO_ROOT, "dist", "templates.toml")
CATEGORIES = {"common", "gaming", "transcend"}
SCHEMA_VERSION = 1


@dataclass
class Entry:
    stem: str
    rel_path: str
    inner_name: str
    body: str


def normalize(text: str) -> str:
    """CRLF → LF（跨平台确定性），并去掉行尾多余空白行。"""
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")


def collect() -> list[Entry]:
    entries: list[Entry] = []
    errors: list[str] = []

    for root, _dirs, files in os.walk(TEMPLATES_DIR):
        for filename in sorted(files):
            if not filename.endswith(".toml"):
                continue

            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, REPO_ROOT).replace(os.sep, "/")
            parts = rel_path.split("/")
            if len(parts) < 4 or parts[0] != "templates" or parts[1] not in CATEGORIES:
                continue
            if filename == ".gitkeep":
                continue

            stem = filename[: -len(".toml")]
            if '"' in stem or "\\" in stem:
                errors.append(f"{rel_path}: 文件名含引号或反斜杠，无法作为 TOML 键")
                continue

            raw = open(full_path, "rb").read().decode("utf-8")
            text = normalize(raw)

            # 结构校验（用解析器判定，避免被多行数组里的 '[' 骗到）
            try:
                parsed = tomllib.loads(text)
            except Exception as exc:  # noqa: BLE001 - 报错信息直接给维护者
                errors.append(f"{rel_path}: TOML 解析失败: {exc}")
                continue

            extra_top = [key for key in parsed if key != "templates"]
            if extra_top:
                errors.append(f"{rel_path}: 除 [templates.*] 外还有顶层键 {extra_top}")
                continue

            templates = parsed.get("templates")
            if not isinstance(templates, dict) or len(templates) != 1:
                errors.append(f"{rel_path}: 必须恰好包含一个 [templates.\"...\"] 表")
                continue

            inner_name = next(iter(templates))
            body_value = templates[inner_name]
            nested = [
                key
                for key, value in body_value.items()
                if isinstance(value, dict) or (isinstance(value, list) and any(isinstance(v, dict) for v in value))
            ]
            if nested:
                errors.append(f"{rel_path}: 模板内出现子表/子表数组 {nested}，bundle 只支持扁平字段")
                continue

            # 表头不一定是第一行：仓库里有文件以空行/缩进开头（如 huawei_matepad.toml），
            # 因此定位「第一行以 [ 开头的行」作为表头，其后的内容整体作为表体（逐字保留）。
            lines = text.split("\n")
            header_index = next((i for i, line in enumerate(lines) if line.lstrip().startswith("[")), None)
            if header_index is None or not lines[header_index].lstrip().startswith("[templates"):
                actual = lines[header_index][:60] if header_index is not None else "<无表头>"
                errors.append(f"{rel_path}: 找不到 [templates...] 表头（实际: {actual!r}）")
                continue

            entries.append(
                Entry(
                    stem=stem,
                    rel_path=rel_path,
                    inner_name=inner_name,
                    body="\n".join(lines[header_index + 1 :]).rstrip("\n"),
                )
            )

    seen: dict[str, str] = {}
    for entry in entries:
        if entry.stem in seen:
            errors.append(
                f"stem 重复: {entry.stem} ({seen[entry.stem]} 与 {entry.rel_path})；"
                "WebUI 用 stem 作为导入键，必须唯一（请按真值合并或改名）"
            )
        else:
            seen[entry.stem] = entry.rel_path

    if errors:
        print("❌ bundle 生成前置校验失败：")
        for message in errors:
            print("  -", message)
        sys.exit(1)

    entries.sort(key=lambda item: item.rel_path)
    return entries


def render(entries: list[Entry]) -> bytes:
    lines = [
        "# 本文件由 .github/scripts/bundle_templates.py 生成，请勿手工编辑。",
        "# 内容 = templates/**/*.toml 按路径排序后的机械拼接（表头换成文件名，字段逐字保留）。",
        "# WebUI 在线模板库拉这一个文件即可拿到全部模板（替代逐文件 700+ 次请求）。",
        f"schema_version = {SCHEMA_VERSION}",
        f"count = {len(entries)}",
        "",
    ]
    for entry in entries:
        lines.append(f"# {entry.rel_path} · {entry.inner_name}")
        lines.append(f'[templates."{entry.stem}"]')
        lines.append(entry.body)
        lines.append("")
    return ("\n".join(lines) + "\n").encode("utf-8")


def main() -> int:
    args = sys.argv[1:]
    check_only = "--check" in args
    emit_stdout = "--stdout" in args
    if check_only and emit_stdout:
        print("--check 与 --stdout 不能同时使用")
        return 2

    entries = collect()
    payload = render(entries)

    # 只做结构校验（PR CI）：不落盘、不比对，仅证明「模板能被聚合成 bundle」。
    # 用 buffer 写，避免 Windows 的 sys.stdout 把 \n 翻成 \r\n。
    if emit_stdout:
        sys.stdout.buffer.write(payload)
        sys.stdout.buffer.flush()
        print(
            f"✅ 聚合结构校验通过：{len(entries)} 个模板，{len(payload) / 1024:.1f} KB",
            file=sys.stderr,
        )
        return 0

    if check_only:
        if not os.path.exists(OUTPUT_PATH):
            print("❌ dist/templates.toml 不存在，请运行: python .github/scripts/bundle_templates.py")
            return 1
        current = open(OUTPUT_PATH, "rb").read()
        if current != payload:
            # Windows + core.autocrlf=true 会把工作区文件翻成 CRLF；那种情况下内容其实一致，
            # 而且 git 里存的仍是 LF（见 .gitattributes），不要误报成「需要重新生成」。
            if current.replace(b"\r\n", b"\n") == payload:
                print(
                    "⚠️ dist/templates.toml 工作区是 CRLF（core.autocrlf），已按 LF 归一后一致，无需处理。"
                )
                return 0
            print("❌ dist/templates.toml 与 templates/ 不一致，请重新生成:")
            print("   python .github/scripts/bundle_templates.py")
            return 1
        print(f"✅ dist/templates.toml 已是最新（{len(entries)} 个模板，{len(payload) / 1024:.1f} KB）")
        return 0

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(payload)

    # 自检：生成物必须能被解析，且模板数与源文件一致
    parsed = tomllib.loads(payload.decode("utf-8"))
    assert len(parsed["templates"]) == len(entries), "生成物模板数不一致"

    print(f"✅ 已生成 dist/templates.toml：{len(entries)} 个模板，{len(payload) / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
