---
name: tauri-app-creator
description: Guidance for creating Tauri v2 projects using official create-tauri-app workflows and minimal run verification.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Creating a new Tauri v2 app from scratch / 新建 Tauri v2 应用
- Choosing a create-tauri-app installation method / 选择 create-tauri-app 安装方式
- Minimal run verification for first boot / 最小启动验证流程

**Trigger phrases include:**
- "create-tauri-app", "new tauri app", "bootstrap", "dev mode"
- "创建 Tauri", "新建项目", "初始化", "启动验证"

## How to use this skill

1. Pick the create-tauri-app installation method based on environment
2. Run the creation command and select frontend template
3. Install dependencies and start the Tauri dev mode
4. Confirm the app boots with a minimal verification checklist

## Outputs

- Creation commands by package manager / 按包管理器的创建命令
- Minimal boot verification checklist / 最小启动验证清单

## Scope

- Boundary: Using create-tauri-app to create a Tauri v2 project
- Key points: Explain method trade-offs (npm, pnpm, bun, cargo, curl)

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/
- https://v2.tauri.app/start/
- https://v2.tauri.app/start/prerequisites/
- https://v2.tauri.app/start/create-project/
- https://v2.tauri.app/start/project-structure/

## Keywords

create-tauri-app, tauri v2, new project, scaffold, dev mode

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
