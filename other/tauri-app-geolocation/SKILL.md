---
name: tauri-app-geolocation
description: Guidance for Tauri v2 geolocation plugin with permission handling and privacy controls.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Location access or tracking features / 位置访问或轨迹功能
- Permission flow and privacy constraints / 权限流程与隐私约束
- Accuracy and frequency tuning / 精度与频率调优

**Trigger phrases include:**
- "geolocation", "location", "tracking", "privacy"
- "定位", "位置", "轨迹", "隐私"

## How to use this skill

1. Define location accuracy and update frequency
2. Configure geolocation plugin capabilities
3. Handle permission requests and denial cases
4. Provide opt-out and privacy-safe defaults

## Outputs

- Location access and privacy plan / 位置访问与隐私方案
- Opt-out defaults and denial handling checklist / 退出默认与拒绝处理清单

## Scope

- Boundary: Geolocation plugin usage only
- Key points: Permission handling and privacy compliance

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/geolocation/
- https://v2.tauri.app/zh-cn/plugin/geolocation/

## Keywords

tauri geolocation, location, privacy, permissions

## 常见陷阱 (Gotchas)

1. **版本兼容性**：注意框架版本与依赖库的兼容性，不同版本 API 可能有差异
2. **配置文件格式**：配置文件格式错误是最常见的问题，建议使用编辑器的语法检查
3. **环境变量**：确保所有必要的环境变量已正确设置，敏感信息不要硬编码
4. **依赖冲突**：多版本共存时注意依赖冲突，使用 lock 文件锁定版本
5. **性能陷阱**：大数据量场景下注意性能优化，避免 N+1 查询等常见问题

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
