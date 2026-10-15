---
name: tauri-setup
description: Guidance for Tauri v2 prerequisites and environment setup across macOS, Windows, Linux, and mobile Android iOS targets.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Tauri v2 prerequisites or environment setup / Tauri v2 前置环境或安装配置
- Rust toolchain, Node.js, build tools, Xcode, Android SDK/NDK / Rust 工具链、Node.js、构建工具、Xcode、Android SDK/NDK
- Desktop and mobile environment checks / 桌面与移动端环境检查

**Trigger phrases include:**
- "prerequisites", "toolchain", "Xcode", "Android SDK", "NDK"
- "前置环境", "工具链", "Xcode", "Android Studio", "NDK"

## How to use this skill

1. Identify the target platforms and OS (macOS, Windows, Linux, Android, iOS)
2. Provide OS-specific prerequisite installation steps
3. Include mobile development checks for Android Studio/NDK and Xcode
4. Verify toolchains with minimal commands and version checks

## Outputs

- Prerequisite checklist by platform / 按平台的前置环境清单
- Verification commands and pass criteria / 验证命令与通过标准

## Scope

- Boundary: Operating-system level dependencies only
- v2 focus: Mobile development prerequisites must be covered

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/start/prerequisites/
- https://v2.tauri.app/mobile/development/#prerequisites

## Keywords

tauri v2, prerequisites, rust, node.js, build tools, xcode, android studio, ndk, sdk

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
