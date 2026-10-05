---
name: project-structure
description: Understand the agent-ebpf-filter repository structure through layered references, and choose the right files, commands, and docs when developing agents or features in this project.
---

# Agent eBPF Filter 项目结构导航

本 skill 是 `agent-ebpf-filter` 仓库的项目结构入口。它采用“入口索引 + 分层 references”的方式：先用本文件判断任务属于哪一层，再按需读取 `references/` 下的详细文档，避免一次性加载过多上下文。

## 使用原则

1. 先判断任务影响域：backend / frontend / proto / eBPF / wrapper / adapters / hooks / AgentSight / TLS capture / ML / sandbox / docs。
2. 先读 `references/00-layered-map.md` 获取全局层级图。
3. 根据任务读取对应层级文档。
4. 修改前确认是否牵涉跨层同步：proto ↔ backend ↔ frontend ↔ docs ↔ generated files。
5. 修改后运行最小充分验证，并如实说明成功、失败或跳过原因。

## References 分层索引

### 0. 全局层级与导航

- `references/00-layered-map.md`：项目的多层架构、目录职责、数据流、跨层依赖、选择文档的路线图。

### 1. 根目录、构建与运行层

- `references/01-root-build-runtime.md`：根目录文件、Make targets、devcontainer、安装、运行时端口、权限、环境变量、验证命令。

### 2. 后端层

- `references/02-backend-layers.md`：Go backend 的路由层、handler 层、runtime state、event/envelope、network、TLS、AgentSight、ML、sandbox、plugins、shell sessions、OTLP/Prometheus 等详细入口。

### 3. 前端层

- `references/03-frontend-layers.md`：Vue 3 前端目录、路由、views/components/composables/types/data/utils/pb 的分层规则与各页面入口。

### 4. 协议、eBPF 与生成层

- `references/04-proto-ebpf-generated.md`：proto 文件分工、生成文件、eBPF C 程序、Go 绑定、事件字段跨层同步、禁止手改清单。

### 5. Agent 集成与安全运行层

- `references/05-agent-integrations-security.md`：wrapper、Python/Node adapters、native hooks、MCP、AgentSight、runtime feature gates、auth、OS enforcement、危险操作边界。

### 6. 功能域索引层

- `references/06-feature-domain-index.md`：按功能域（Dashboard、Monitor、Network、TLSCapture、ExecutionGraph、Explorer、Executor、Hooks、ML、Plugins、Config 等）列出前后端文件与验证建议。

### 7. Agent 工作流与检查清单层

- `references/07-agent-workflows-checklists.md`：新功能、Bug 修复、代码审查、Vue 改动、API 改动、proto/eBPF 改动、文档同步、验证策略的操作清单。

## 快速选择

| 你要做什么 | 优先读 |
| --- | --- |
| 只是想快速理解项目 | `00-layered-map.md` |
| 找 build/run/test 命令 | `01-root-build-runtime.md` |
| 改 Go API、事件、ML、sandbox、TLS、AgentSight | `02-backend-layers.md` |
| 改 Vue 页面、组件、composable、路由 | `03-frontend-layers.md` |
| 改 proto 或 eBPF | `04-proto-ebpf-generated.md` |
| 改 wrapper、hooks、adapters、MCP、安全开关 | `05-agent-integrations-security.md` |
| 按页面/功能找文件 | `06-feature-domain-index.md` |
| 不确定如何规划、验证和同步文档 | `07-agent-workflows-checklists.md` |

## 关键约束速记

- Vue 改动遵守 Composition API 与 `<script setup lang="ts">`。
- `tracked_comms` 是 16-byte command exact match。
- `tracked_paths` 是 256-byte path exact match，不是递归路径树。
- cgroup destination blocking 使用 exact IPv4 / IPv6 / port map，不是 CIDR/range。
- LSM 文件名策略是 basename-based；exec 策略按 exact path 或 executable basename。
- Release mode 中敏感 API 受 runtime access token 保护；dev mode 默认关闭 auth。
- Shell sessions、`/system/run`、hook 安装、policy mutation、TLS capture 等能力受 runtime feature gate 控制。
- 不要手改生成文件：`backend/pb/*.pb.go`、`frontend/src/pb/*`、`adapters/*/tracker_*`、`backend/ebpf/*_bpf*.go`、`backend/ebpf/*.o`。
