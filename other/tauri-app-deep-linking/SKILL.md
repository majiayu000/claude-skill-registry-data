---
name: tauri-app-deep-linking
description: Guidance for Tauri v2 deep-linking plugin with URL schemes and safe routing.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Deep links or custom URL schemes / 深链或自定义 URL Scheme
- Routing external URLs to the app / 外部 URL 路由到应用
- Secure handling for external input / 外部输入安全处理

**Trigger phrases include:**
- "deep link", "url scheme", "app link", "routing"
- "深链", "URL Scheme", "应用链接", "路由"

## How to use this skill

1. Define supported schemes and link patterns
2. Configure deep-linking plugin and OS registration
3. Validate and sanitize all external link payloads
4. Route parameters to frontend with single-instance support

## Outputs

- Deep-linking registration and routing plan / 深链注册与路由方案
- Input validation checklist / 输入校验清单

## Scope

- Boundary: Deep-linking registration and handling
- Key points: Input validation and single-instance integration

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/deep-linking/
- https://v2.tauri.app/zh-cn/plugin/deep-linking/

## Keywords

tauri deep linking, url scheme, routing, security

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
