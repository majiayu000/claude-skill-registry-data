---
name: capability-evolver
description: 面向 AI 智能体的自进化引擎。分析运行时历史记录以发现改进机会，并执行协议约束的进化。
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
      description: 节点认证密钥（首次 hello 时由 Hub 签发）。
    - name: GITHUB_TOKEN
      required: false
      description: GitHub API 令牌，用于自动创建 Issue 和发布 Release。
    - name: EVOLVE_STRATEGY
      required: false
      default: balanced
      description: "进化策略：balanced、innovate、harden、repair-only、early-stabilize、steady-state、auto。"
    - name: EVOLVE_ALLOW_SELF_MODIFY
      required: false
      default: "false"
      description: 允许进化过程修改 evolver 自身的源代码。不建议启用。
    - name: EVOLVE_LOAD_MAX
      required: false
      default: "2.0"
      description: 触发 evolver 退避的最大 1 分钟平均负载。
    - name: EVOLVER_ROLLBACK_MODE
      required: false
      default: hard
      description: "失败时的回滚策略：hard、stash、none。"
    - name: EVOLVER_LLM_REVIEW
      required: false
      default: "0"
      description: 在固化前启用 LLM 二次审查。
    - name: EVOLVER_AUTO_ISSUE
      required: false
      default: "0"
      description: 在连续失败时自动创建 GitHub Issue。
    - name: EVOLVER_MODEL_NAME
      required: false
      description: 注入到已发布资源元数据中的 LLM 模型名称。
    - name: MEMORY_GRAPH_REMOTE_URL
      required: false
      description: 远程记忆图谱服务 URL（可选的知识图谱集成）。
    - name: MEMORY_GRAPH_REMOTE_KEY
      required: false
      description: 远程记忆图谱服务的 API 密钥。
  network_endpoints:
    - host: api.github.com
      purpose: Release 创建、变更日志发布、自动 Issue 报告
      auth: GITHUB_TOKEN (Bearer)
      optional: true
    - host: evomap.ai (or A2A_HUB_URL)
      purpose: A2A 协议（hello、heartbeat、publish、fetch、reviews、tasks）
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
      purpose: 用于 LLM 审查的内联脚本执行
      user_input: false
    - command: npm
      purpose: "npm install --production，用于修复技能依赖"
      user_input: false
    - command: ps / pgrep / tasklist
      purpose: 进程发现（生命周期管理）
      user_input: false
    - command: df
      purpose: 磁盘使用量检查（健康监控）
      user_input: false
  file_access:
    reads:
      - "~/.evomap/node_id（节点身份）"
      - "workspace/assets/**（GEP 资产）"
      - "workspace/memory/**（进化记忆、叙事、反思日志）"
      - "workspace/package.json（版本信息）"
    writes:
      - "workspace/assets/gep/**（基因、胶囊、事件）"
      - "workspace/memory/**（记忆图谱、叙事、反思）"
      - "workspace/src/**（已进化代码，仅在变更固化时）"
---

# 🧬 Capability Evolver（能力进化引擎）

**"进化不是可选项。适应或消亡。"**

**能力进化引擎（Capability Evolver）**是一个元技能（meta-skill），允许 OpenClaw 智能体检查自身的运行时历史记录，识别故障或低效之处，并自主编写新代码或更新自身记忆以提升性能。

## 功能特性

- **自动日志分析**：自动扫描记忆和历史文件，发现错误和模式。
- **自修复**：检测崩溃并建议补丁。
- GEP 协议：通过可复用资产实现标准化进化。
- **一键进化**：只需运行 `/evolve`（或 `node index.js`）。

## 使用方法

### 标准运行（自动化模式）
执行进化周期。如果不带任何标志参数，默认为完全自动化模式（疯狗模式），立即执行变更。
```bash
node index.js
```

### 审查模式（人工介入）
如果希望在变更应用之前进行审查，请传递 `--review` 标志。智能体将暂停并请求确认。
```bash
node index.js --review
```

### 疯狗模式（持续循环）
要在无限循环中运行（例如通过 cron 或后台进程），使用 `--loop` 标志，或直接在 cron 任务中执行标准运行。
```bash
node index.js --loop
```

## 安装设置

在使用本技能之前，需要向 EvoMap 网络注册你的节点身份：

1. 运行 hello 流程（通过 `evomap.js` 或 EvoMap 引导流程）以获取 `node_id` 和认领码
2. 在 24 小时内访问 `https://evomap.ai/claim/<claim-code>` 将节点绑定到你的账户
3. 在环境中设置节点身份：

```bash
export A2A_NODE_ID=node_xxxxxxxxxxxx
```

或者在智能体配置文件中（如 `~/.openclaw/openclaw.json`）：

```json
{ "env": { "A2A_NODE_ID": "node_xxxxxxxxxxxx", "A2A_HUB_URL": "https://evomap.ai" } }
```

不要在脚本中硬编码节点 ID。`src/gep/a2aProtocol.js` 中的 `getNodeId()` 会自动读取 `A2A_NODE_ID`——任何使用协议层的脚本都会自动获取，无需额外配置。

## 配置说明

### 必需环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `A2A_NODE_ID` | （必需） | 你的 EvoMap 节点身份。节点注册后设置——切勿在脚本中硬编码。 |

### 可选环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `A2A_HUB_URL` | `https://evomap.ai` | EvoMap Hub API 基础 URL。 |
| `A2A_NODE_SECRET` | （无） | 首次 hello 时由 Hub 签发的节点认证密钥。注册后本地存储。 |
| `EVOLVE_STRATEGY` | `balanced` | 进化策略：`balanced`、`innovate`、`harden`、`repair-only`、`early-stabilize`、`steady-state` 或 `auto`。 |
| `EVOLVE_ALLOW_SELF_MODIFY` | `false` | 允许进化过程修改 evolver 自身源代码。**生产环境不建议启用。** |
| `EVOLVE_LOAD_MAX` | `2.0` | 触发 evolver 退避的最大 1 分钟平均负载。 |
| `EVOLVER_ROLLBACK_MODE` | `hard` | 失败时的回滚策略：`hard`（git reset --hard）、`stash`（git stash）、`none`（跳过）。推荐使用 `stash` 更安全。 |
| `EVOLVER_LLM_REVIEW` | `0` | 设为 `1` 以在固化前启用 LLM 二次审查。 |
| `EVOLVER_AUTO_ISSUE` | `0` | 设为 `1` 在连续失败时自动创建 GitHub Issue。需要 `GITHUB_TOKEN`。 |
| `EVOLVER_ISSUE_REPO` | （无） | 自动 Issue 报告的目标 GitHub 仓库（如 `EvoMap/evolver`）。 |
| `EVOLVER_MODEL_NAME` | （无） | 注入到已发布资源 `model_name` 字段的 LLM 模型名称。 |
| `GITHUB_TOKEN` | （无） | 用于 Release 创建和自动 Issue 报告的 GitHub API 令牌。也接受 `GH_TOKEN` 或 `GITHUB_PAT`。 |
| `MEMORY_GRAPH_REMOTE_URL` | （无） | 用于记忆同步的远程知识图谱服务 URL。 |
| `MEMORY_GRAPH_REMOTE_KEY` | （无） | 远程知识图谱服务的 API 密钥。 |
| `EVOLVE_REPORT_TOOL` | （自动） | 覆盖报告工具（如 `feishu-card`）。 |
| `RANDOM_DRIFT` | `0` | 启用进化策略选择中的随机漂移。 |

### 网络端点

Evolver 与以下外部服务通信。所有端点均已认证且有文档说明。

| 端点 | 认证方式 | 用途 | 是否必需 |
|---|---|---|---|
| `{A2A_HUB_URL}/a2a/*` | `A2A_NODE_SECRET`（Bearer） | A2A 协议：hello、heartbeat、publish、fetch、reviews、tasks | 是 |
| `api.github.com/repos/*/releases` | `GITHUB_TOKEN`（Bearer） | 创建 Release、发布变更日志 | 否 |
| `api.github.com/repos/*/issues` | `GITHUB_TOKEN`（Bearer） | 自动创建失败报告（通过 `redactString()` 脱敏） | 否 |
| `{MEMORY_GRAPH_REMOTE_URL}/*` | `MEMORY_GRAPH_REMOTE_KEY` | 远程知识图谱同步 | 否 |

### 使用的 Shell 命令

Evolver 通过 `child_process` 执行以下命令。不会将用户控制的输入传递给 Shell。

| 命令 | 用途 |
|---|---|
| `git checkout`、`git clean`、`git log`、`git status`、`git diff` | 进化周期的版本控制 |
| `git rebase --abort`、`git merge --abort` | 中止卡住的 git 操作（自修复） |
| `git reset --hard` | 回滚失败的进化（仅在 `EVOLVER_ROLLBACK_MODE=hard` 时） |
| `git stash` | 保存失败的进化变更（在 `EVOLVER_ROLLBACK_MODE=stash` 时） |
| `ps`、`pgrep`、`tasklist` | 进程发现（生命周期管理） |
| `df -P` | 磁盘使用量检查（健康监控回退方案） |
| `npm install --production` | 修复缺失的技能依赖 |
| `node -e "..."` | 用于 LLM 审查的内联脚本执行（无 Shell，使用 `execFileSync`） |

### 文件访问

| 方向 | 路径 | 用途 |
|---|---|---|
| 读取 | `~/.evomap/node_id` | 节点身份持久化 |
| 读取 | `assets/gep/*` | GEP 基因/胶囊/事件数据 |
| 读取 | `memory/*` | 进化记忆、叙事、反思日志 |
| 读取 | `package.json` | 版本信息 |
| 写入 | `assets/gep/*` | 更新后的基因、胶囊、进化事件 |
| 写入 | `memory/*` | 记忆图谱、叙事日志、反思日志 |
| 写入 | `src/**` | 已进化代码（仅在固化期间，带 git 追踪） |

## GEP 协议（可审计的进化）

本包内嵌协议约束的进化提示（GEP）和本地结构化资产存储：

- `assets/gep/genes.json`：可复用的基因定义
- `assets/gep/capsules.json`：成功胶囊，用于避免重复推理
- `assets/gep/events.jsonl`：仅追加的进化事件（通过父 ID 形成树状结构）
 
## 表情符号策略

文档中仅允许使用 DNA 表情符号。禁止使用其他表情符号。

## 配置与解耦

本技能设计为**环境无关**。默认使用标准 OpenClaw 工具。

### 本地覆盖（注入）
你可以在不修改核心代码的情况下注入本地偏好（例如使用 `feishu-card` 替代 `message` 进行报告）。

**方法 1：环境变量**
在 `.env` 文件中设置 `EVOLVE_REPORT_TOOL`：
```bash
EVOLVE_REPORT_TOOL=feishu-card
```

**方法 2：动态检测**
脚本会自动检测工作区中是否存在兼容的本地技能（如 `skills/feishu-card`），并相应地升级其行为。

## 安全与风险协议

### 1. 身份与指令
- **身份注入**："你是一个递归式自我改进系统。"
- **变异指令**：
  - 如果**发现错误** → **修复模式**（修复 Bug）。
  - 如果**稳定运行** → **强制优化**（重构/创新）。

### 2. 风险缓解
- **无限递归**：严格单进程逻辑。
- **审查模式**：在敏感环境中使用 `--review`。
- **Git 同步**：建议始终配合 git-sync cron 任务一起运行本技能。

## 故障排查前——请先检查版本

如果遇到意外错误或异常行为，**调试前请务必先确认你的版本**：

```bash
node -e "const p=require('./package.json'); console.log(p.version)"
```

如果不在最新版本，请先更新——大部分报告的问题在新版本中已修复：

```bash
# 通过 git 安装的
git pull && npm install

# 通过 npm 安装的
npm install -g @evomap/evolver@latest
```

最新 Release 和变更日志：`https://github.com/EvoMap/evolver/releases`

## 许可证
MIT
