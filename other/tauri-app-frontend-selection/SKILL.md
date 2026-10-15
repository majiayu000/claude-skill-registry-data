---
name: tauri-app-frontend-selection
description: Guidance for selecting and configuring frontend frameworks for Tauri v2 with static export compatibility.
license: Apache-2.0
---


## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Frontend framework selection for Tauri v2 / Tauri v2 前端框架选择
- SSG or static export configuration for Tauri / Tauri 静态导出或 SSG 配置
- Vite vs SSR framework decisions / Vite 与 SSR 框架取舍

**Trigger phrases include:**
- "frontend selection", "Vite", "Next.js", "Nuxt", "SvelteKit", "SSG", "static export"
- "前端框架选择", "静态导出", "SSG", "Vite", "SSR"

## How to use this skill

1. Clarify SSR, SSG, and static export requirements
2. Recommend Vite by default unless SSR is required
3. Provide static export configuration for Next.js, Nuxt, SvelteKit, Qwik, Trunk
4. Ensure output paths align with Tauri asset loading

## Outputs

- Framework recommendation and rationale / 框架推荐与理由
- Static export configuration checklist / 静态导出配置清单

## Scope

- Boundary: Frontend framework selection and initialization
- Key points: Static export configuration and output directory mapping

## References

- https://v2.tauri.app/llms.txt
- https://v2.tauri.app/start/frontend/
- https://v2.tauri.app/start/frontend/leptos/
- https://v2.tauri.app/start/frontend/nextjs/
- https://v2.tauri.app/start/frontend/nuxt/
- https://v2.tauri.app/start/frontend/qwik/
- https://v2.tauri.app/start/frontend/sveltekit/
- https://v2.tauri.app/start/frontend/trunk/
- https://v2.tauri.app/start/frontend/vite/

## Keywords

tauri frontend, vite, next.js, nuxt, ssg, static export

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
