---
name: tauri-app-develop
description: Guidance for Tauri v2 daily development workflow, debugging, resources, sidecar usage, and testing strategies.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Day-to-day Tauri v2 development workflow / Tauri v2 日常开发流程
- Dev server vs static assets / 开发服务器与静态资源切换
- Debugging Rust + WebView / Rust 与 WebView 联合调试
- Sidecar or resources management / sidecar 与资源管理
- Testing strategies for Tauri apps / Tauri 测试策略

**Trigger phrases include:**
- "dev workflow", "debug", "sidecar", "resources", "icons"
- "开发流程", "调试", "sidecar", "资源管理", "图标"

## How to use this skill

1. Choose dev server or static asset mode / 选择开发模式
2. Configure resources, sidecar, and icons / 配置资源与 sidecar
3. Set up Rust + WebView debugging flow / 建立双端调试流程
4. Recommend testing strategy (mocking, WebDriver, CI) / 推荐测试策略

## Outputs

- Development checklist / 开发清单
- Debugging workflow guide / 调试流程指南
- Testing recommendations / 测试建议

## Scope

- Boundary: Development workflow only / 仅限开发流程
- Key points: Dev server vs static assets and dual-side debugging / 模式切换与调试
- Out of scope: release builds or distribution / 不涉及发布与分发

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/develop/
- https://v2.tauri.app/develop/configuration-files/
- https://v2.tauri.app/develop/calling-rust/
- https://v2.tauri.app/develop/calling-frontend/
- https://v2.tauri.app/develop/resources/
- https://v2.tauri.app/develop/sidecar/
- https://v2.tauri.app/develop/state-management/
- https://v2.tauri.app/develop/updating-dependencies/
- https://v2.tauri.app/develop/icons/
- https://v2.tauri.app/develop/debug/
- https://v2.tauri.app/develop/debug/crabnebula-devtools/
- https://v2.tauri.app/develop/debug/neovim/
- https://v2.tauri.app/develop/debug/rustrover/
- https://v2.tauri.app/develop/debug/vscode/
- https://v2.tauri.app/develop/plugins/
- https://v2.tauri.app/develop/plugins/develop-mobile/
- https://v2.tauri.app/develop/tests/
- https://v2.tauri.app/develop/tests/mocking/
- https://v2.tauri.app/develop/tests/webdriver/
- https://v2.tauri.app/develop/tests/webdriver/ci/
- https://v2.tauri.app/develop/tests/webdriver/example/selenium/
- https://v2.tauri.app/develop/tests/webdriver/example/webdriverio/

## Keywords

tauri develop, dev server, static assets, sidecar, debugging, tests, 开发流程, 调试, 资源管理

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
