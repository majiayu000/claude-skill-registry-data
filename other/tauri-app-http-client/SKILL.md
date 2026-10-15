---
name: tauri-app-http-client
description: Guidance for Tauri v2 http-client plugin with allowlisted requests and secure transport.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- HTTP requests from Rust side / Rust 侧发起 HTTP 请求
- Bypassing WebView restrictions / 绕过 WebView 限制
- Domain allowlists and secure request handling / 域名白名单与安全请求处理

**Trigger phrases include:**
- "http client", "allowlist", "requests", "WebView"
- "HTTP 请求", "白名单", "WebView"

## How to use this skill

1. Define allowed domains, methods, and headers
2. Configure http-client plugin capabilities and scope
3. Implement request timeouts, retries, and error handling
4. Validate sensitive data handling and logging hygiene

## Outputs

- Request policy and allowlist plan / 请求策略与白名单方案
- Security and logging checklist / 安全与日志清单

## Scope

- Boundary: HTTP client plugin usage only
- Key points: Domain allowlists and transport security

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/http-client/
- https://v2.tauri.app/zh-cn/plugin/http-client/

## Keywords

tauri http client, requests, allowlist, security

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
