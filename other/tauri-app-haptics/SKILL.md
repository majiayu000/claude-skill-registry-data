---
name: tauri-app-haptics
description: Guidance for Tauri v2 haptics plugin with feedback patterns and graceful fallback.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Tactile feedback on mobile devices / 移动端触觉反馈
- Haptic patterns or device support / 触感模式或设备支持
- Fallback on unsupported devices / 不支持设备的回退

**Trigger phrases include:**
- "haptics", "vibration", "feedback", "mobile"
- "震动", "触感", "反馈", "移动端"

## How to use this skill

1. Identify interactions requiring haptic feedback
2. Configure haptics plugin capabilities
3. Implement feedback patterns with sensible defaults
4. Handle unsupported devices with silent fallback

## Outputs

- Haptic feedback plan / 触觉反馈方案
- Fallback behavior checklist / 回退行为清单

## Scope

- Boundary: Haptics plugin usage only
- Key points: Feedback patterns and fallback strategy

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/haptics/
- https://v2.tauri.app/zh-cn/plugin/haptics/

## Keywords

tauri haptics, vibration, mobile feedback, fallback

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
