---
name: tauri-app-file-system
description: Guidance for Tauri v2 file-system plugin with scoped access and safe file operations.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Reading or writing local files / 读写本地文件
- Safe directory scope configuration / 安全目录 Scope 配置
- Import or export file workflows / 文件导入导出流程

**Trigger phrases include:**
- "file system", "file access", "scope", "read", "write"
- "文件系统", "文件访问", "Scope", "读写"

## How to use this skill

1. Define the minimal directories and file patterns to access
2. Configure file-system plugin scope and capabilities
3. Implement file selection, read, and write flows
4. Validate access boundaries and error handling

## Outputs

- File access scope plan / 文件访问 Scope 方案
- Import/export flow checklist / 导入导出流程清单

## Scope

- Boundary: File-system plugin usage only
- Key points: Scope restrictions for safe access

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/file-system/
- https://v2.tauri.app/zh-cn/plugin/file-system/

## Keywords

tauri file system, scope, read write, file access

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
