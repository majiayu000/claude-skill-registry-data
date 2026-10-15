---
name: tauri-build
description: Guidance for Tauri v2 production builds, signing, and distribution artifacts.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Production builds or packaging / 生产构建或打包
- Signing or release artifacts / 签名或发布产物
- CI pipelines for distribution / 分发相关 CI 流水线

**Trigger phrases include:**
- "build", "release", "signing", "distribution", "pipeline"
- "构建", "发布", "签名", "分发", "流水线"

## How to use this skill

1. Identify target platforms and packaging formats
2. Configure release build and signing requirements
3. Produce installers or app bundles per platform
4. Validate release artifacts and update channels

## Outputs

- Release build checklist / 发布构建清单
- Signing and distribution plan / 签名与分发方案

## Scope

- Boundary: Build, signing, and distribution only
- Key points: Debug vs release and platform packaging

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/distribute/
- https://v2.tauri.app/distribute/app-store/
- https://v2.tauri.app/distribute/appimage/
- https://v2.tauri.app/distribute/aur/
- https://v2.tauri.app/distribute/crabnebula-cloud/
- https://v2.tauri.app/distribute/debian/
- https://v2.tauri.app/distribute/dmg/
- https://v2.tauri.app/distribute/flatpak/
- https://v2.tauri.app/distribute/google-play/
- https://v2.tauri.app/distribute/macos-application-bundle/
- https://v2.tauri.app/distribute/microsoft-store/
- https://v2.tauri.app/distribute/rpm/
- https://v2.tauri.app/distribute/snapcraft/
- https://v2.tauri.app/distribute/windows-installer/
- https://v2.tauri.app/distribute/sign/macos/
- https://v2.tauri.app/distribute/sign/windows/
- https://v2.tauri.app/distribute/sign/linux/
- https://v2.tauri.app/distribute/sign/ios/
- https://v2.tauri.app/distribute/sign/android/
- https://v2.tauri.app/distribute/pipelines/crabnebula-cloud/
- https://v2.tauri.app/distribute/pipelines/github/

## Keywords

tauri build, release, signing, packaging, distribution

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
