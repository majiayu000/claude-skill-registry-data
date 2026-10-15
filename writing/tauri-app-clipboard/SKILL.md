---
name: tauri-app-clipboard
description: Guidance for Tauri v2 clipboard plugin with safe copy, paste, and monitoring flows.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Reading or writing clipboard content / 读写剪贴板内容
- Clipboard monitoring or images / 剪贴板监听或图像
- Reducing clipboard abuse risk / 降低剪贴板滥用风险

**Trigger phrases include:**
- "clipboard", "copy", "paste", "monitoring"
- "剪贴板", "复制", "粘贴", "监听"

## How to use this skill

1. Identify clipboard content types and user flows
2. Configure clipboard plugin capabilities and scope
3. Implement copy, paste, and change listeners carefully
4. Restrict access to user-initiated actions only

## Outputs

- Clipboard access policy / 剪贴板访问策略
- User-initiated flow checklist / 用户触发流程清单

## Scope

- Boundary: Clipboard plugin usage only
- Key points: Permission control and user-initiated access

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/clipboard/
- https://v2.tauri.app/zh-cn/plugin/clipboard/

## Keywords

tauri clipboard, copy, paste, permissions

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
