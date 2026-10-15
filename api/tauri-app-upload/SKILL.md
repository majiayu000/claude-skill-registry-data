---
name: tauri-app-upload
description: Guidance for Tauri v2 upload plugin with file transfer, progress reporting, and headers.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Uploading large files from desktop or mobile / 桌面或移动端的大文件上传
- Progress callbacks or custom headers / 进度回调或自定义头
- Reliable file transfer from local disk / 本地磁盘可靠文件传输

**Trigger phrases include:**
- "upload", "progress", "headers", "retry"
- "上传", "进度", "请求头", "重试"

## How to use this skill

1. Define upload endpoints and file selection flow
2. Configure upload plugin capabilities and scope
3. Implement progress callbacks and error handling
4. Validate performance and retries for large files

## Outputs

- Upload flow and retry plan / 上传流程与重试方案
- Permission and performance checklist / 权限与性能清单

## Scope

- Boundary: Upload plugin usage only
- Key points: Progress handling and custom headers

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/plugin/upload/
- https://v2.tauri.app/zh-cn/plugin/upload/

## Keywords

tauri upload, file transfer, progress, headers

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
