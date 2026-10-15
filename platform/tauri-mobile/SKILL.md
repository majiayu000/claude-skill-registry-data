---
name: tauri-mobile
description: Guidance for Tauri v2 mobile development setup, debugging, and bundle identifiers.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Android or iOS builds / Android 或 iOS 构建
- Mobile debugging or run flows / 移动端调试与运行流程
- Bundle identifier configuration / 包名与 Bundle ID 配置

**Trigger phrases include:**
- "mobile", "android", "ios", "bundle id", "debugging"
- "移动端", "Android", "iOS", "包名", "调试"

## How to use this skill

1. Confirm mobile prerequisites and target platforms
2. Configure bundle identifiers and platform settings
3. Set up mobile debugging workflow
4. Validate responsive UI behavior and platform constraints

## Outputs

- Mobile development checklist / 移动端开发清单
- Bundle ID and platform settings plan / 包名与平台配置方案

## Scope

- Boundary: Mobile-specific setup and workflow only
- Key points: Bundle ID and mobile debugging

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/mobile/
- https://v2.tauri.app/mobile/development/
- https://v2.tauri.app/learn/mobile-file-associations/
- https://v2.tauri.app/learn/mobile-multiwindow/

## Keywords

tauri mobile, android, ios, bundle id, debugging

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
