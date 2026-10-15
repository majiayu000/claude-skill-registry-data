---
name: tauri-app-updater
description: Guidance for Tauri v2 updater plugin with OTA updates and signing keys.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- OTA updates for the app / 应用 OTA 更新
- Signing keys or update servers / 签名密钥或更新服务器
- Automatic update checks / 自动更新检查

**Trigger phrases include:**
- "updater", "OTA", "signing key", "update server"
- "更新", "OTA", "签名", "更新服务器"

## How to use this skill

1. Generate and manage updater signing keys
2. Configure update server URLs and metadata
3. Implement update checks and user prompts
4. Validate update flow across platforms

## Outputs

- Update flow plan / 更新流程方案
- Signing and metadata checklist / 签名与元数据清单

## Scope

- Boundary: Updater plugin setup and usage only
- Key points: Signing keys and update metadata

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/updater/
- https://v2.tauri.app/zh-cn/plugin/updater/

## Keywords

tauri updater, ota updates, signing, update server

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
