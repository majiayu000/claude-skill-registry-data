---
name: tauri-app-localhost
description: Guidance for Tauri v2 localhost plugin with local service access and minimal exposure.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Accessing localhost services from the app / 应用访问本地服务
- Local server exposure and safety / 本地服务暴露与安全
- Dev vs production localhost behavior / 开发与生产本地行为

**Trigger phrases include:**
- "localhost", "local service", "dev server", "ports"
- "本地服务", "localhost", "端口", "开发服务器"

## How to use this skill

1. Identify local services and their access requirements
2. Configure localhost plugin capabilities and allowed ports
3. Separate dev-mode access from production constraints
4. Validate minimal exposure and audit access patterns

## Outputs

- Localhost access policy / 本地服务访问策略
- Dev/prod separation checklist / 开发生产分离清单

## Scope

- Boundary: Localhost plugin usage only
- Key points: Controlled access and environment separation

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/localhost/
- https://v2.tauri.app/zh-cn/plugin/localhost/

## Keywords

tauri localhost, local service, dev server, security

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
