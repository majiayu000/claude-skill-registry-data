---
name: tauri-app-positioner
description: Guidance for Tauri v2 positioner plugin with multi-display alignment strategies.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Aligned popup or tray windows / 对齐弹窗或托盘窗口
- Multi-monitor positioning / 多显示器定位
- Consistent placement across platforms / 跨平台一致位置

**Trigger phrases include:**
- "positioner", "align", "multi-monitor", "tray window"
- "定位", "对齐", "多显示器", "托盘窗口"

## How to use this skill

1. Define window alignment and anchor points
2. Configure positioner plugin capabilities
3. Handle multi-display coordinates and scaling factors
4. Validate behavior on macOS, Windows, and Linux

## Outputs

- Window positioning plan / 窗口定位方案
- Multi-display scaling checklist / 多显示器缩放清单

## Scope

- Boundary: Positioner plugin usage only
- Key points: Multi-display and scaling differences

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/positioner/
- https://v2.tauri.app/zh-cn/plugin/positioner/

## Keywords

tauri positioner, window alignment, multi-display, scaling

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
