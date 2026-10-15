---
name: tauri-app-stronghold
description: Guidance for Tauri v2 stronghold plugin with encrypted storage and sensitive data handling.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Encrypted storage for secrets or credentials / 机密或凭据加密存储
- Stronghold snapshots or clients / Stronghold 快照或客户端
- Securely storing sensitive data on disk / 敏感数据安全落盘

**Trigger phrases include:**
- "stronghold", "encrypted storage", "snapshot", "secrets"
- "Stronghold", "加密存储", "快照", "密钥"

## How to use this skill

1. Define secure storage requirements and data classification
2. Configure Stronghold snapshot and client management
3. Restrict plugin access with capabilities and scope
4. Validate encryption lifecycle and recovery procedures

## Outputs

- Secure storage plan / 安全存储方案
- Snapshot and recovery checklist / 快照与恢复清单

## Scope

- Boundary: Stronghold plugin usage only
- Key points: Encrypted storage and snapshot management

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/stronghold/
- https://v2.tauri.app/zh-cn/plugin/stronghold/

## Keywords

tauri stronghold, encrypted storage, secrets, snapshot

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
