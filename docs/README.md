**简体中文** | [English](https://github.com/Seyud/device_faker_config/blob/main/docs/en/README.md)

# Device Faker 配置贡献指南

欢迎为 Device Faker 项目贡献设备配置！通过贡献配置，您可以帮助更多用户获得更好的机型伪装效果。

## 贡献方式

### 1. 选择合适的模板分类

在 `templates` 目录下选择合适的文件夹放置您的配置文件：

- **common** - 通用设备配置（适合大部分日常应用）
- **gaming** - 游戏设备配置（专为游戏应用优化）
- **transcend** - 破限设备配置（用于破除特定限制）

**注意：请在对应分类目录下，根据设备品牌创建子文件夹（如 `Xiaomi`, `Samsung`, `OnePlus` 等），并将配置文件放入品牌文件夹中。**

### 2. 创建配置文件

在对应品牌文件夹中创建以**设备型号**命名的 `.toml` 文件：

例如：
- `Xiaomi/xiaomi_15_pro.toml`
- `Samsung/samsung_s24_ultra.toml`
- `Google/pixel_8_pro.toml`

### 3. 配置格式

配置文件使用 [TOML](https://toml.io/) 格式，基本结构如下：

```toml
# 模板配置
[templates.your_device_template]
# 可选字段
version = "v1.0.0"          # 可选，模板版本（仅用于显示，不影响伪装）
version_code = 20251212            # 可选，模板版本码（仅用于显示）
author = "your_name"       # 可选，作者（仅用于显示）
description = "设备亮点描述"  # 可选，描述（仅用于显示）
packages = [
    "com.example.app1",
    "com.example.app2",
]
manufacturer = "设备厂商"
brand = "品牌"
model = "设备型号"
device = "设备代号"
product = "产品代号"
fingerprint = "完整设备指纹"
hardware = "硬件代号"    # 可选
board = "主板代号"      # 可选
build_id = "构建版本号"  # 可选
name = "内部产品名称"  # 可选
marketname = "市场型号名称"  # 可选
```

**重要字段说明：**

| 字段 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `packages` | 否 | 目标应用包名列表 | `["com.google.android.apps.photos"]` |
| `manufacturer` | 是 | 设备制造商 | `"Google"` |
| `brand` | 是 | 品牌 | `"Google"` |
| `model` | 是 | 设备型号 | `"marlin"` |
| `device` | 否 | 设备代号 | `"Pixel XL"` |
| `fingerprint` | 否 | 完整设备指纹 | `"google/marlin/marlin:10/...:user/release-keys"` |
| `hardware` | 否 | 硬件代号（对应 Build.HARDWARE / ro.hardware） | `"qcom"` |
| `board` | 否 | 主板代号（对应 Build.BOARD / ro.product.board） | `"kalama"` |
| `build_id` | 否 | 构建版本号（对应 Build.ID / ro.build.id） | `"UKQ1.230917.001"` |
| `name` | 否 | 内部产品名称 | `"marlin"` |
| `marketname` | 否 | 市场型号名称 | `"Pixel XL"` |
| `version` | 否 | 模板版本（仅用于显示，不影响伪装） | `"1.0.0"` |
| `version_code` | 否 | 模板版本码（仅用于显示，不影响伪装） | `1` |
| `author` | 否 | 模板作者（仅用于显示） | `"Coolapk@Seyud"` |
| `description` | 否 | 模板描述（仅用于显示） | `"特点：支持120Hz"` |

## 设备信息获取

您可以从以下方式获取设备信息：

1. **官方文档** - 设备制造商官网
2. **开发者工具** - 命令获取
3. **现有设备** - 从真实设备上获取
4. **开源项目** - 参考其他设备的指纹

获取完整设备指纹的命令：
```bash
su -c getprop ro.build.fingerprint
```

## 提交流程

1. Fork 本项目
2. 在相应目录添加您的 `.toml` 配置文件
3. 确保配置格式正确，字段完整
4. 创建 Pull Request，描述您添加的设备配置
5. 等待代码审查

## 注意事项

- 配置文件名使用英文和下划线，避免特殊字符
- 确保配置名称没有空格
- 测试配置是否正常工作
- 保持配置文件的简洁和可读性
- 遵循现有的代码风格和格式

## 更多参考

详细的配置说明请参考：
- [Device Faker 官方配置文档](https://github.com/Seyud/device_faker/blob/main/docs/CONFIG.md)

## 贡献激励

您的贡献将帮助更多用户获得更好的机型伪装体验！感谢您为开源社区的贡献。

---

如果您在贡献过程中遇到问题，欢迎创建 Issue 或参与讨论。