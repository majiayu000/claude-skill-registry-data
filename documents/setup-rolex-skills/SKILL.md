---
name: setup-rolex-skills
description: 配置本仓库的工程 skill：设置 issue tracker、triage 标签词汇和领域文档布局。每个仓库在首次使用其他工程 skill 之前运行一次。
disable-model-invocation: true
---

# Setup Rolex Skills

搭建工程 skill 所需的每个仓库配置：

- **Issue tracker**：issue 存放位置（默认 GitHub；也原生支持本地 markdown）
- **Triage 标签**：五个标准 triage 角色使用的标签字符串
- **领域文档**：`GLOSSARY.md` 和 ADR 的位置，以及消费规则
- **Implementation notes**：实现决策与因果记录存放位置（固定为 `.agents/notes/`）

这是一个 prompt 驱动的 skill，不是确定性脚本。探索、展示发现、与用户确认、然后写入。

## Process

### 1. 探索

查看当前仓库，理解初始状态。读取已有内容，不要假设：

- `git remote -v` 和 `.git/config`：是 GitHub 仓库吗？是哪个？
- `AGENTS.md` 和 `CLAUDE.md`：是否存在？是否已有 `## Agent skills` 区块？
- `GLOSSARY.md` 和 `GLOSSARY-MAP.md`
- `docs/adr/` 和任何 `src/*/docs/adr/` 目录
- `docs/agents/`：本 skill 之前的输出是否已存在？
- `.scratch/`：本地 markdown issue tracker 惯例是否已在使用
- `triage` skill 是否已安装？（旁边是否有 `triage` skill 目录，或 `triage` 在可用 skill 列表中。）决定 Section B 是否运行。
- Monorepo 信号：`pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 字段，或有自己 `src/` 的 `packages/*`。只在真正的大型多包仓库中才呈现；没有这些信号就意味着单上下文，绝大多数仓库都是如此。

### 2. 展示发现并询问

总结已存在什么、缺少什么。然后按顺序处理各部分。一个问题，一个回答，然后下一个。

每个部分以推荐答案开头，让用户一个字就能接受。只在选择确实有分支时给一行解释；当探索已经确定了答案时跳过该部分（`triage` 未安装时跳过 Section B，没有 monorepo 时跳过 Section C）。

**Section A：Issue tracker。**

> 解释："Issue tracker" 是本仓库 issue 的存放位置。`to-tickets`、`triage`、`to-spec` 等 skill 从中读写。它们需要知道是调用 `gh issue create`、在 `.scratch/` 下写 markdown 文件，还是遵循你描述的其他工作流。选择你实际跟踪工作的位置。

默认姿态：这些 skill 为 GitHub 设计。如果 `git remote` 指向 GitHub，提议 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自托管），提议 GitLab。否则（或用户偏好），提供：

- **GitHub**：issue 在仓库的 GitHub Issues 中（使用 `gh` CLI）
- **GitLab**：issue 在仓库的 GitLab Issues 中（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 markdown**：issue 作为文件存放在 `.scratch/<feature>/` 下（适合个人项目或没有 remote 的仓库）
- **其他**（Jira、Linear 等）：请用户用一段话描述工作流；skill 将其记录为自由文本

将选择记录在 `docs/agents/issue-tracker.md`。GitHub 和 GitLab 模板带有 "PRs as a request surface" 标志，默认 **off**。保持关闭，不要提出：如果用户希望外部 PR 进入 triage 队列，他们可以稍后在文件中修改。

**Section B：Triage 标签词汇。** 如果 `triage` skill 未安装则整体跳过。

如果已安装，只问一个问题：

> 是否保留默认 triage 标签？（推荐：**是**）

默认是五个标准角色，每个标签字符串等于其名称：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。选**是**则原样写入。只有当用户说否（通常因为他们的 tracker 已使用其他名称，如用 `bug:triage` 代替 `needs-triage`），才收集覆盖值，让 `triage` 使用已有标签而非创建重复。

**Section C：领域文档。** 默认 **单上下文**（仓库根目录下一个 `GLOSSARY.md` + `docs/adr/`）。这适合几乎所有仓库，无需询问直接写入。

仅当探索发现 monorepo 信号时才提供 **多上下文**（根目录 `GLOSSARY-MAP.md` 指向每个上下文的 `GLOSSARY.md`）。然后确认他们想要哪种布局。

### 3. 确认并编辑

向用户展示草稿：

- 要添加到 `CLAUDE.md` / `AGENTS.md` 的 `## Agent skills` 区块（选择规则见步骤 4）
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 和 `docs/agents/triage-labels.md` 的内容（最后一个仅当 `triage` 已安装时）

让他们在写入前编辑。

### 4. 写入

**选择要编辑的文件：**

- 如果 `CLAUDE.md` 存在，编辑它。
- 否则如果 `AGENTS.md` 存在，编辑它。
- 如果都不存在，询问用户要创建哪一个；不要替他们选。

当 `CLAUDE.md` 已存在时永远不要创建 `AGENTS.md`（反之亦然）；始终编辑已存在的那个。

如果所选文件中已有 `## Agent skills` 区块，原地更新其内容而非追加重复。不要覆盖用户对周围章节的编辑。

区块内容：

```markdown
## Agent skills

### Issue tracker

[一句话摘要 issue 跟踪位置]。详见 `docs/agents/issue-tracker.md`。

### Triage labels

[一句话摘要标签词汇]。详见 `docs/agents/triage-labels.md`。

### Domain docs

[一句话摘要布局："单上下文" 或 "多上下文"]。详见 `docs/agents/domain.md`。

### Implementation notes

实现决策与因果记录存放在 `.agents/notes/`，记录决策、取舍与偏离，供下一次尝试学习。
```

仅当 `triage` 已安装且 Section B 运行时才包含 `### Triage labels` 子区块并写入 `docs/agents/triage-labels.md`。

然后使用本 skill 目录中的种子模板写入文档文件：

- [issue-tracker-github.md](./issue-tracker-github.md)：GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)：GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md)：本地 markdown issue tracker
- [triage-labels.md](./triage-labels.md)：标签映射（仅当 `triage` 已安装）
- [domain.md](./domain.md)：领域文档消费规则 + 布局

对于"其他" issue tracker，使用用户描述从零编写 `docs/agents/issue-tracker.md`。

### 5. 完成

告诉用户设置完成，哪些工程 skill 现在会读取这些文件。提醒他们可以稍后直接编辑 `docs/agents/*.md`；只有想切换 issue tracker 或从头开始时才需要重新运行本 skill。
