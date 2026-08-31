**English** | [简体中文](https://github.com/Seyud/device_faker_config/blob/main/docs/README.md)

# Device Faker Configuration Contribution Guide

Welcome to contribute device configurations for the Device Faker project! By contributing configurations, you can help more users achieve better device spoofing results.

## Contribution Methods

### 1. Choose the Appropriate Template Category

Select the appropriate folder in the `templates` directory to place your configuration file:

- **common** - General device configurations (suitable for most daily applications)
- **gaming** - Gaming device configurations (optimized for gaming applications)
- **transcend** - Unlock device configurations (for bypassing specific restrictions)

**Note: Please create a subfolder for the device brand (e.g., `Xiaomi`, `Samsung`, `OnePlus`) under the corresponding category directory, and place the configuration file inside the brand folder.**

### 2. Create a Configuration File

Create a `.toml` file named after the **device model** in the corresponding brand folder:

For example:
- `Xiaomi/xiaomi_15_pro.toml`
- `Samsung/samsung_s24_ultra.toml`
- `Google/pixel_8_pro.toml`

### 3. Configuration Format

Configuration files use [TOML](https://toml.io/) format, with the basic structure as follows:

```toml
# Template configuration
[templates.your_device_template]
# Optional fields
version = "v1.0.0"          # Optional, template version (for display only, does not affect spoofing)
version_code = 20251212            # Optional, template version code (for display only)
author = "your_name"       # Optional, author (for display only)
description = "Device highlights description"  # Optional, description (for display only)
packages = [
    "com.example.app1",
    "com.example.app2",
]
manufacturer = "Device manufacturer"
brand = "Brand"
model = "Device model"
device = "Device code name"
product = "Product code name"
fingerprint = "Complete device fingerprint"
hardware = "Hardware code name"   # Optional
build_id = "Build ID"             # Optional
name = "Internal product name"    # Optional
marketname = "Market model name"  # Optional
```

**Important Field Descriptions:**

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `packages` | No | Target application package name list | `["com.google.android.apps.photos"]` |
| `manufacturer` | Yes | Device manufacturer | `"Google"` |
| `brand` | Yes | Brand | `"Google"` |
| `model` | Yes | Device model | `"marlin"` |
| `device` | No | Device code name | `"Pixel XL"` |
| `fingerprint` | No | Complete device fingerprint | `"google/marlin/marlin:10/...:user/release-keys"` |
| `hardware` | No | Hardware code name (maps to Build.HARDWARE / ro.hardware) | `"qcom"` |
| `build_id` | No | Build ID (maps to Build.ID / ro.build.id) | `"UKQ1.230917.001"` |
| `name` | No | Internal product name | `"marlin"` |
| `marketname` | No | Market model name | `"Pixel XL"` |
| `version` | No | Template version (for display only, does not affect spoofing) | `"1.0.0"` |
| `version_code` | No | Template version code (for display only, does not affect spoofing) | `1` |
| `author` | No | Template author (for display only) | `"Coolapk@Seyud"` |
| `description` | No | Template description (for display only) | `"Feature: 120Hz support"` |

## Obtaining Device Information

You can obtain device information from the following sources:

1. **Official Documentation** - Device manufacturer website
2. **Developer Tools** - Command-line acquisition
3. **Existing Devices** - Obtain from real devices
4. **Open Source Projects** - Reference other device fingerprints

Command to obtain complete device fingerprint:
```bash
su -c getprop ro.build.fingerprint
```

## Submission Process

1. Fork this project
2. Add your `.toml` configuration file to the corresponding directory
3. Ensure the configuration format is correct and fields are complete
4. Create a Pull Request describing your device configuration
5. Wait for code review

## Notes

- Use English and underscores for file names, avoid special characters
- Ensure configuration names have no spaces
- Test if the configuration works correctly
- Keep configuration files concise and readable
- Follow existing code style and format

## Additional References

For detailed configuration instructions, please refer to:
- [Device Faker Official Configuration Documentation](https://github.com/Seyud/device_faker/blob/main/docs/CONFIG.md)

## Contribution Incentives

Your contribution will help more users achieve a better device spoofing experience! Thank you for your contribution to the open-source community.

---

If you encounter problems during contribution, feel free to create an Issue or participate in discussions.
