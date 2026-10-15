---
name: tauri-app-notification
description: Guidance for Tauri v2 notification plugin with permission flow and click handling.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- System notifications / 系统通知
- Notification permissions or callbacks / 通知权限或回调
- Deep-linking from notifications / 通知触发深链

**Trigger phrases include:**
- "notification", "system alerts", "permission", "callback"
- "通知", "系统提醒", "权限", "回调"

## How to use this skill

1. Define notification types and user flows
2. Configure notification plugin capabilities
3. Handle permission requests and click callbacks
4. Map notification clicks to app routes safely

## Outputs

- Notification flow plan / 通知流程方案
- Permission and click handling checklist / 权限与点击处理清单

## Scope

- Boundary: Notification plugin usage only
- Key points: Permissions and click handling

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/notification/
- https://v2.tauri.app/zh-cn/plugin/notification/

## Keywords

tauri notification, system alerts, permissions, callbacks

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
