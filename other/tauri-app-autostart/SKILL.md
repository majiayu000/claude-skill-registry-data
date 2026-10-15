---
name: tauri-app-autostart
description: Guidance for Tauri v2 autostart setup with platform differences and rollback.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Enabling or disabling app autostart / 启用或关闭应用自启动
- Platform-specific autostart behavior / 平台自启动行为差异
- User-controlled autostart toggle / 用户可控自启动开关

**Trigger phrases include:**
- "autostart", "startup", "login items", "boot launch"
- "自启动", "开机启动", "登录项"

## How to use this skill

1. Decide autostart defaults and user controls
2. Configure autostart plugin and permissions
3. Handle platform differences for startup registration
4. Provide rollback and verification steps

## Outputs

- Autostart policy and toggle plan / 自启动策略与开关方案
- Rollback and verification checklist / 回滚与验证清单

## Scope

- Boundary: Autostart configuration and control only
- Key points: Platform-specific startup behavior

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/autostart/
- https://v2.tauri.app/zh-cn/plugin/autostart/

## Keywords

tauri autostart, startup, enable disable, platform

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
