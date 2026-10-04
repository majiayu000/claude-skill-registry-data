---
name: ci-review
description: |
  Install a CI-triggered LLM code reviewer into the current repo: on every push to a PR/MR, Claude Code runs headless, reproduces every claim the change makes, hunts correctness bugs with concrete failure scenarios, and posts a machine-readable execution verdict. For configured bot branches (do/* by default), it also requires a separate value verdict before auto-merge, rejecting bookkeeping-only work and incomplete outcomes. Detects GitHub vs GitLab, installs a deterministic verdict gate, and supports review-only or auto-merge tiers. Use when the user says /ci-review, 装一个 CI 代码审查, CI 里自动 code review, 给 PR/MR 加 AI review, 让机器人验证 PR, 审查通过自动合并.
trigger: /ci-review
compatibility: Claude Code
license: MIT
---

# ci-review

给仓库装一个审查机器人：所有 PR 都回答**这次改动宣称做到的事，真的做到了吗？**；
对配置的机器人分支再回答**这件事值得自动进入默认分支吗？**

它不替人类评价普通 PR 的方向；但 `do/*` 没有人实时把关，必须额外通过价值门，
避免验证账本、重复 sweep 和未完成产物仅因"技术上没错"就自动合入。
配合 do-something 的 MR 模式即成飞轮：do-something 提出方向并实践，ci-review 验证实践质量，
do-something 下一轮先回应它的评论。开"通过即合并"档后，机器人分支的收割也由机器完成，人类只在想否决时出现。

## 触发条件

- `/ci-review`：装进当前仓库（幂等，已存在的文件不覆盖；`/ci-review --force` 覆盖）。
- `/ci-review status`：检查文件、合并档位、secrets/variables、最近运行。
- `/ci-review merge on|off`：改合并档位。

## 安装流程

脚本只做确定性的事（识别平台、写文件、改档位、报状态）；问用户、设变量由你做。

### 1. 依赖检查

当前目录是 git 仓库且有 origin，否则停下说明。GitHub 需要 `gh auth status` 通过，GitLab 需要 `glab auth status` 通过；
未登录就只装文件，变量留给用户手设。

### 2. 装文件

```bash
bash <本 SKILL.md 所在目录>/scripts/install.sh [仓库路径] [--force] [--platform github|gitlab] [--merge on|off]
```

脚本按 origin 主机名判平台：含 `github.com` → GitHub；含 `gitlab` → GitLab（自建实例也算）；
判不出退出码 2。此时用 AskUserQuestion 问"这个仓库托管在哪"（GitHub / GitLab），带 `--platform` 重跑。

| 平台 | CI 配置 | 审查规范 |
|---|---|---|
| GitHub | `.github/workflows/ci-review.yml`（官方 `anthropics/claude-code-action@v1`） | `.github/ci-review.md` + `.github/scripts/ci-review-verdict.sh` |
| GitLab | `.gitlab/ci-review.yml`（`claude -p` 头less，需 `include:`） | `.gitlab/ci-review.md` + `.gitlab/ci-review-verdict.sh` |

审查规范是 `prompts/review.md` 的副本，落在仓库里供按口味修改；CI 里的 Claude 读它执行。

### 3. 问合并档位（仅首次写入 CI 文件时问）

CI 文件已存在 → 档位以文件里 `CI_REVIEW_MERGE` 为准，不再问，这就是"记住上次选择"。
首次安装 → 用 AskUserQuestion 问一次，两档：

| 档位 | 行为 | 选后执行 |
|---|---|---|
| 仅审查 | 发评论 + 结论，合不合人定 | `install.sh merge off`（默认，可不跑） |
| 通过即合并 | 结论 pass 且无未解决线程 → 自动合并，**仅限 `do/*` 分支** | `install.sh merge on` |

选"通过即合并"前，用一句话向用户复述后果：机器人分支每次 push 通过审查后几分钟内进默认分支，
人类的收割闸门消失，否决手段变成 revert、关掉档位、或在 PR 里留一条不 resolve 的线程。

### 4. 问模型接入（仅缺变量时问）

先跑 `install.sh status` 看哪些没设。认证 secret 和网关变量都已有 → 跳过本节。
缺网关变量 → 用 AskUserQuestion 问"模型走哪里"：

| 选项 | BASE_URL |
|---|---|
| 官方 Anthropic | 留空 |
| 智谱 GLM | `https://open.bigmodel.cn/api/anthropic` |
| MiniMax | `https://api.minimaxi.com/anthropic` |
| DeepSeek | `https://api.deepseek.com/anthropic` |
| 其他 Anthropic 兼容网关 | 用户填 |

再问模型名（网关上的名字，留空 = CLI 默认）。审查是工具调用密集型任务，提醒用户选支持 tool use、上下文够大的模型。
问完直接设：

```bash
# GitHub
gh variable set CI_REVIEW_BASE_URL --body "<url>"     # 官方 Anthropic 则跳过
gh variable set CI_REVIEW_MODEL --body "<model>"
# GitLab
glab variable set ANTHROPIC_BASE_URL "<url>"
glab variable set ANTHROPIC_MODEL "<model>"
```

**API key 不经对话传递**：对话记录明文落盘。让用户在自己的终端里交互式设置，设完你再跑 `status` 确认：

```bash
gh secret set CI_REVIEW_API_KEY                          # GitHub，粘贴后回车
glab variable set ANTHROPIC_AUTH_TOKEN --masked          # GitLab
glab variable set GITLAB_TOKEN --masked                  # GitLab 还要项目访问令牌，api scope；仅审查 Reporter 以上，自动合并 Developer 以上
```

想烧 Pro/Max 订阅额度而不是 API key：`claude setup-token` 生成 `CLAUDE_CODE_OAUTH_TOKEN`，按 CI 文件顶部注释改认证字段。

### 5. 提交并告知

只提交生成的三个文件（CI 配置 + 审查规范 + verdict gate），GitLab 还要在 `.gitlab-ci.yml` 里加 `include: - local: .gitlab/ci-review.yml` 并确认 stages 有 `test`。
最后跑 `install.sh status`，把仍缺的项原样告诉用户，并说明：push 后开一个 PR/MR 才能看到第一次运行。

## 合并档位怎么工作

合并**不经模型**。模型只在 sticky 第一行写
`<!-- ci-review last=<sha> execution=pass|fail value=pass|fail|na -->`，
确定性 gate 把失败 verdict 变成红 check，并核对以下条件：

1. 来源分支匹配 `CI_REVIEW_MERGE_BRANCHES`（默认 `do/*`，空格分隔的 glob；想覆盖所有 PR 改成 `*`）。
2. sticky 的 sha 等于本次 HEAD，且 `execution=pass`。
3. 匹配机器人分支时 `value=pass`；普通分支必须是 `value=na`。
4. 无未解决的评审线程（人和机器人的都算）。do-something 与机器人来回 5 轮后会回"留人裁决"停手，那条线程留着就挡住合并。
5. 合并方式 `CI_REVIEW_MERGE_METHOD`（默认 squash）是仓库允许的。

`execution=pass` 的定义写死在审查规范里：结论"做成了"、本轮 inline 为 0、且至少验证过一条声明；
**没有可验证声明就是 fail**。不按扩展名免审：`SKILL.md` 和 references 会改变 Agent 行为，本来就是产品代码。
机器人分支的 `value=pass` 还要求有具体证据、直接推进项目目的、留下持久成果并真正闭环；只改 DO.md、重复 sweep 或关键路径未验证均 fail。

模型的 allowedTools 里没有合并权限，PR 正文里的注入最多骗它写个 `pass`，还得过分支和线程两关。
所有档位设置都在 CI 文件顶部，改档位 = 一次 commit，历史可查。

## `status` 检查

```bash
bash <本 SKILL.md 所在目录>/scripts/install.sh status
```

输出平台、两个文件是否在、合并档位与范围、secrets/variables 是否设、最近三次运行（GitHub）。

## 审查行为（写在 prompts/review.md，此处只列不变量）

- 范围增量：sticky 里记 `last=<sha>`，下次只审这个 sha 之后的 diff，不重复评论。
- 先验证声明再找缺陷：正文、commit message、DO.md 里的"验证过了"逐条亲自复现。
- 匹配 `CI_REVIEW_MERGE_BRANCHES` 的机器人分支额外审价值；普通分支固定 `value=na`。
- Markdown 不豁免；按文件是否改变行为判断审查深度。
- 每条发现必须有失败场景，否则不发；风格、命名、"可以考虑"一律不报。
- 只发评论和双 verdict，不改代码、不 approve、不 request changes、不合并。
- 评论正文以 `<!-- ci-review -->` 开头，do-something 据此识别机器人线程并对回合数设上限。

## 调口味

- 改审查规范：直接编辑仓库里的 `.github/ci-review.md` 或 `.gitlab/ci-review.md`，下次 push 生效。
- 换模型或换网关：改仓库变量 `CI_REVIEW_MODEL` / `CI_REVIEW_BASE_URL`（GitLab 改 CI 变量），不用动 CI 文件。
- 改合并范围或方式：改 CI 文件顶部的 `CI_REVIEW_MERGE_BRANCHES` / `CI_REVIEW_MERGE_METHOD`。
- 降成本：`concurrency.cancel-in-progress` 已开，连续 push 只审最后一次。

## 错误处理

- Action 报认证失败 → secret 名与 workflow 里 `with:` 字段不匹配，二选一改齐。
- 网关返回 401 → 该网关只认 Bearer 头或只认 x-api-key；模板两种都发，检查 key 是否属于该网关。
- 网关返回 model not found → `CI_REVIEW_MODEL` 写的是官方 ID 而非网关上的名字。
- 报 "Claude Code is not installed on this repository" → workflow 里的 `github_token` 行被删了却没装 Claude GitHub App，二者留一个。
- 评论没出现但 job 成功 → 看 job 日志里 Claude 的输出；常见是 `--allowedTools` 缺 `mcp__github_inline_comment__create_inline_comment`。
- 合并步骤报 "Resource not accessible by integration" → 仓库 Settings → Actions → Workflow permissions 改成 Read and write。
- 合并步骤两次都失败、提示 required status checks / auto-merge not allowed → 分支保护把本 workflow 设成了必需检查，仓库要开 "Allow auto-merge"，脚本会退回 `--auto`。
- 合并后默认分支上的 `on: push` workflow 没跑 → GITHUB_TOKEN 触发的事件不会再触发 workflow，这是 GitHub 的防递归规则；需要的话把合并 token 换成 PAT。
- 通过了却没合并、日志说"未解决线程" → 有人或机器人留了线程没 resolve，这是设计：留人裁决。
- GitLab 发评论 401/403 → `GITLAB_TOKEN` 权限不够，需要 api scope 且 Reporter 以上；合并 405 → 令牌不到 Developer，或目标分支受保护。
