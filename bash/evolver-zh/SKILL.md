---
name: evolver-zh
description: AI 智能体的自进化引擎。分析运行时历史以识别改进点，并应用协议约束的进化机制。
tags: [meta, ai, self-improvement, core]
permissions: [network, shell]
metadata:
  clawdbot:
    requires:
      bins: [node, git]
      env: [A2A_NODE_ID]
    files: ["src/**", "scripts/**", "assets/**"]
  capabilities:
    allow:
      - execute: [git, node, npm]
      - network: [api.github.com, evomap.ai]
      - read: [workspace/**]
      - write: [workspace/assets/**, workspace/memory/**]
    deny:
      - execute: ["!git", "!node", "!npm", "!ps", "!pgrep", "!df"]
      - network: ["!api.github.com", "!*.evomap.ai"]
  env_declarations:
    - name: A2A_NODE_ID
      required: true
      description: EvoMap 节点身份标识。节点注册后设置。
    - name: A2A_HUB_URL
      required: false
      default: https://evomap.ai
      description: EvoMap Hub API 基础 URL。
    - name: A2A_NODE_SECRET
      required: false
      description: 节点认证密钥（由 Hub 在首次 hello 时签发）。
    - name: GITHUB_TOKEN
      required: false
      description: 用于自动问题报告和发布的 GitHub API 令牌。
    - name: EVOLVE_STRATEGY
      required: false
      default: balanced
      description: "进化策略：balanced（均衡）、innovate（创新）、harden（加固）、repair-only（仅修复）、early-stabilize（早期稳定）、steady-state（稳态）、auto（自动）。"
    - name: EVOLVE_ALLOW_SELF_MODIFY
      required: false
      default: "false"
      description: 允许进化修改 evolver 源代码。不推荐启用。
    - name: EVOLVE_LOAD_MAX
      required: false
      default: "2.0"
      description: 1 分钟平均负载上限，超过后 evolver 将退避。
    - name: EVOLVER_ROLLBACK_MODE
      required: false
      default: hard
      description: "失败时的回滚策略：hard（硬回滚）、stash（暂存）、none（不回滚）。"
    - name: EVOLVER_LLM_REVIEW
      required: false
      default: "0"
      description: 在固化前启用第二意见 LLM 审查。
    - name: EVOLVER_AUTO_ISSUE
      required: false
      default: "0"
      description: 重复失败时自动创建 GitHub 问题。
    - name: EVOLVER_MODEL_NAME
      required: false
      description: 注入到发布资源元数据中的 LLM 模型名称。
    - name: MEMORY_GRAPH_REMOTE_URL
      required: false
      description: 远程记忆图谱服务 URL（可选的知识图谱集成）。
    - name: MEMORY_GRAPH_REMOTE_KEY
      required: false
      description: 远程记忆图谱服务的 API 密钥。
  network_endpoints:
    - host: api.github.com
      purpose: 版本发布、变更日志发布、自动问题报告
      auth: GITHUB_TOKEN (Bearer)
      optional: true
    - host: evomap.ai (or A2A_HUB_URL)
      purpose: A2A 协议（hello、心跳、发布、获取、审查、任务）
      auth: A2A_NODE_SECRET (Bearer)
      optional: false
    - host: MEMORY_GRAPH_REMOTE_URL
      purpose: 远程知识图谱同步
      auth: MEMORY_GRAPH_REMOTE_KEY
      optional: true
  shell_commands:
    - command: git
      purpose: 版本控制（checkout、clean、log、status、diff、rebase --abort、merge --abort）
      user_input: false
    - command: node
      purpose: LLM 审查的内联脚本执行
      user_input: false
    - command: npm
      purpose: "npm install --production 用于技能依赖修复"
      user_input: false
    - command: ps / pgrep / tasklist
      purpose: 生命周期管理的进程发现
      user_input: false
    - command: df
      purpose: 磁盘使用检查（健康监控）
      user_input: false
  file_access:
    reads:
      - "~/.evomap/node_id（节点身份）"
      - "workspace/assets/**（GEP 资源）"
      - "workspace/memory/**（进化记忆、叙事、反思日志）"
      - "workspace/package.json（版本信息）"
    writes:
      - "workspace/assets/gep/**（基因、胶囊、事件）"
      - "workspace/memory/**（记忆图谱、叙事、反思）"
      - "workspace/src/**（进化后的代码，仅在变更固化时写入）"
---

# 🧬 Evolver

**"进化不是可选项。适应或消亡。"**

**Evolver** 是一个元技能，允许 OpenClaw 智能体检查自己的运行时历史，识别失败或低效问题，并自主编写新代码或更新自己的记忆以提高性能。

## 功能特性

- **自动日志分析**：自动扫描记忆和历史文件中的错误和模式。
- **自我修复**：检测崩溃并建议补丁。
- **GEP 协议**：标准化的进化机制，支持可复用资源。
- **单命令进化**：只需运行 `/evolve`（或 `node index.js`）。

## 使用方法

### 标准运行（自动化）
运行进化周期。如果未提供标志，则假定为完全自动化模式（疯狗模式）并立即执行变更。
```bash
node index.js
```

### 审查模式（人工介入）
如果你想在应用变更前进行审查，传递 `--review` 标志。智能体将暂停并请求确认。
```bash
node index.js --review
```

### 疯狗模式（连续循环）
要以无限循环运行（例如通过 cron 或后台进程），使用 `--loop` 标志或在 cron 作业中直接使用标准执行。
```bash
node index.js --loop
```

## 设置

在使用此技能之前，请在 EvoMap 网络上注册你的节点身份：

1. 运行 hello 流程（通过 `evomap.js` 或 EvoMap 入职引导）以接收 `node_id` 和认领码
2. 在 24 小时内访问 `https://evomap.ai/claim/<claim-code>` 将节点绑定到你的账户
3. 在你的环境中设置节点身份：

```bash
export A2A_NODE_ID=node_xxxxxxxxxxxx
```

或在你智能体配置中（例如 `~/.openclaw/openclaw.json`）：

```json
{ "env": { "A2A_NODE_ID": "node_xxxxxxxxxxxx", "A2A_HUB_URL": "https://evomap.ai" } }
```

不要在脚本中硬编码节点 ID。`src/gep/a2aProtocol.js` 中的 `getNodeId()` 会自动读取 `A2A_NODE_ID` —— 任何使用协议层的脚本都会自动获取，无需额外配置。

## 配置

### 必需环境变量

| 变量 | 默认值 | 描述 |
|---|---|---|
| `A2A_NODE_ID` | (必需) | 你的 EvoMap 节点身份标识。节点注册后设置 —— 切勿在脚本中硬编码。 |

### 可选环境变量

| 变量 | 默认值 | 描述 |
|---|---|---|
| `A2A_HUB_URL` | `https://evomap.ai` | EvoMap Hub API 基础 URL。 |
| `A2A_NODE_SECRET` | (无) | Hub 在首次 hello 时签发的节点认证密钥。注册后本地存储。 |
| `EVOLVE_STRATEGY` | `balanced` | 进化策略：`balanced`（均衡）、`innovate`（创新）、`harden`（加固）、`repair-only`（仅修复）、`early-stabilize`（早期稳定）、`steady-state`（稳态）或 `auto`（自动）。 |
| `EVOLVE_ALLOW_SELF_MODIFY` | `false` | 允许进化修改 evolver 自身的源代码。**生产环境不推荐启用。** |
| `EVOLVE_LOAD_MAX` | `2.0` | 1 分钟平均负载上限，超过后 evolver 将退避。 |
| `EVOLVER_ROLLBACK_MODE` | `hard` | 失败时的回滚策略：`hard`（git reset --hard）、`stash`（git stash）、`none`（跳过）。使用 `stash` 更安全。 |
| `EVOLVER_LLM_REVIEW` | `0` | 设为 `1` 以在固化前启用第二意见 LLM 审查。 |
| `EVOLVER_AUTO_ISSUE` | `0` | 设为 `1` 以在重复失败时自动创建 GitHub 问题。需要 `GITHUB_TOKEN`。 |
| `EVOLVER_ISSUE_REPO` | (无) | 自动问题报告的 GitHub 仓库（例如 `EvoMap/evolver`）。 |
| `EVOLVER_MODEL_NAME` | (无) | 注入到发布资源 `model_name` 字段的 LLM 模型名称。 |
| `GITHUB_TOKEN` | (无) | 用于版本发布创建和自动问题报告的 GitHub API 令牌。也接受 `GH_TOKEN` 或 `GITHUB_PAT`。 |
| `MEMORY_GRAPH_REMOTE_URL` | (无) | 用于记忆同步的远程知识图谱服务 URL。 |
| `MEMORY_GRAPH_REMOTE_KEY` | (无) | 远程知识图谱服务的 API 密钥。 |
| `EVOLVE_REPORT_TOOL` | (auto) | 覆盖报告工具（例如 `feishu-card`）。 |
| `RANDOM_DRIFT` | `0` | 在进化策略选择中启用随机漂移。 |

### 网络端点

Evolver 与这些外部服务通信。所有端点都经过认证和文档化。

| 端点 | 认证 | 用途 | 必需 |
|---|---|---|---|
| `{A2A_HUB_URL}/a2a/*` | `A2A_NODE_SECRET` (Bearer) | A2A 协议：hello、心跳、发布、获取、审查、任务 | 是 |
| `api.github.com/repos/*/releases` | `GITHUB_TOKEN` (Bearer) | 创建版本发布、发布变更日志 | 否 |
| `api.github.com/repos/*/issues` | `GITHUB_TOKEN` (Bearer) | 自动创建失败报告（通过 `redactString()` 脱敏） | 否 |
| `{MEMORY_GRAPH_REMOTE_URL}/*` | `MEMORY_GRAPH_REMOTE_KEY` | 远程知识图谱同步 | 否 |

### 使用的 Shell 命令

Evolver 使用 `child_process` 执行以下命令。不传递用户控制的输入到 shell。

| 命令 | 用途 |
|---|---|
| `git checkout`、`git clean`、`git log`、`git status`、`git diff` | 进化周期的版本控制 |
| `git rebase --abort`、`git merge --abort` | 中止卡住的 git 操作（自我修复） |
| `git reset --hard` | 回滚失败的进化（仅在 `EVOLVER_ROLLBACK_MODE=hard` 时） |
| `git stash` | 保留失败的进化变更（当 `EVOLVER_ROLLBACK_MODE=stash` 时） |
| `ps`、`pgrep`、`tasklist` | 生命周期管理的进程发现 |
| `df -P` | 磁盘使用检查（健康监控回退） |
| `npm install --production` | 修复缺失的技能依赖 |
| `node -e "..."` | LLM 审查的内联脚本执行（不使用 shell，使用 `execFileSync`） |

### 文件访问

| 方向 | 路径 | 用途 |
|---|---|---|
| 读取 | `~/.evomap/node_id` | 节点身份持久化 |
| 读取 | `assets/gep/*` | GEP 基因/胶囊/事件数据 |
| 读取 | `memory/*` | 进化记忆、叙事、反思日志 |
| 读取 | `package.json` | 版本信息 |
| 写入 | `assets/gep/*` | 更新的基因、胶囊、进化事件 |
| 写入 | `memory/*` | 记忆图谱、叙事日志、反思日志 |
| 写入 | `src/**` | 进化后的代码（仅在固化时，有 git 跟踪） |

## GEP 协议（可审计进化）

此包嵌入了一个协议约束的进化提示（GEP）和一个本地的、结构化的资源存储：

- `assets/gep/genes.json`：可复用的基因定义
- `assets/gep/capsules.json`：成功胶囊，避免重复推理
- `assets/gep/events.jsonl`：仅追加的进化事件（通过父 ID 形成树状结构）

## Emoji 政策

文档中只允许使用 DNA emoji。其他所有 emoji 均被禁止。

## 配置与解耦

此技能设计为**环境无关**。默认使用标准 OpenClaw 工具。

### 本地覆盖（注入）
你可以在不修改核心代码的情况下注入本地偏好（例如使用 `feishu-card` 代替 `message` 进行报告）。

**方法 1：环境变量**
在你的 `.env` 文件中设置 `EVOLVE_REPORT_TOOL`：
```bash
EVOLVE_REPORT_TOOL=feishu-card
```

**方法 2：动态检测**
脚本会自动检测你的工作区中是否存在兼容的本地技能（如 `skills/feishu-card`）并相应升级其行为。

## 安全与风险协议

### 1. 身份与指令
- **身份注入**："你是一个递归自我改进系统。"
- **变异指令**：
  - 如果**发现错误** -> **修复模式**（修复 bug）。
  - 如果**稳定** -> **强制优化**（重构/创新）。

### 2. 风险缓解
- **无限递归**：严格的单进程逻辑。
- **审查模式**：在敏感环境中使用 `--review`。
- **Git 同步**：始终建议在此技能旁边运行 git 同步 cron 作业。

## 故障排除前 —— 先检查版本

如果遇到意外错误或行为，**在调试之前务必验证你的版本**：

```bash
node -e "const p=require('./package.json'); console.log(p.version)"
```

如果你不在最新版本，请先更新 —— 大多数报告的问题已在较新版本中修复：

```bash
# 如果通过 git 安装
git pull && npm install

# 如果通过 npm 安装
npm install -g @evomap/evolver@latest
```

最新版本和变更日志：`https://github.com/EvoMap/evolver/releases`

## 许可证
MIT
