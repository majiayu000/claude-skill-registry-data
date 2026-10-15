---
name: tauri-scaffold
description: Guidance for Tauri v2 project scaffolding with create-tauri-app, project structure, and frontend static export configuration.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Scaffolding a Tauri v2 project / 搭建 Tauri v2 项目脚手架
- Project structure or initial configuration / 项目结构或初始化配置
- Static export or SSG for framework integration / 框架静态导出或 SSG

**Trigger phrases include:**
- "create-tauri-app", "scaffold", "project structure", "static export", "SSG"
- "脚手架", "项目结构", "静态导出", "SSG"

## How to use this skill

1. Gather target platforms and frontend framework choice
2. Use create-tauri-app with appropriate options
3. Apply SSG or static export configuration for the chosen framework
4. Verify the project builds and loads local assets correctly

## Outputs

- Scaffold commands and options / 脚手架命令与选项
- Project structure and config checklist / 项目结构与配置清单

## Scope

- Boundary: create-tauri-app decisions and initial configuration
- Key points: SSG/export configuration for frameworks like Next.js

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/start/create-project/
- https://v2.tauri.app/start/project-structure/
- https://v2.tauri.app/start/frontend/

## Keywords

tauri scaffold, create-tauri-app, project structure, static export, ssg

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
