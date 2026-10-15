---
name: tauri-app-opener
description: Guidance for Tauri v2 opener plugin with safe external links and file handling.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Opening external links or files / 打开外部链接或文件
- Allowlisted protocols or paths / 协议或路径白名单
- Safe opener wrapper / 安全打开封装

**Trigger phrases include:**
- "opener", "open link", "protocol allowlist", "open file"
- "打开链接", "打开文件", "协议白名单", "安全打开"

## How to use this skill

1. Define allowed protocols and target paths
2. Configure opener plugin capabilities and scope
3. Implement a safe open API with strict validation
4. Validate behavior across platforms and error cases

## Outputs

- Opener policy and allowlist plan / 打开策略与白名单方案
- Cross-platform behavior checklist / 跨平台行为清单

## Scope

- Boundary: Opener plugin usage only
- Key points: Protocol and path allowlisting

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/opener/
- https://v2.tauri.app/zh-cn/plugin/opener/

## Keywords

tauri opener, external links, allowlist, security

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
