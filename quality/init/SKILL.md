---
name: init
description: Initialises the current repository for the Meegle plus GitLab flow by injecting the AGENTS.md block, MR and work item templates, and the docs/intent directory. Use when onboarding an existing repo to this flow, when the user says /init, or when asked to set up ai-native-workflow in a project.
---

# /init —— 把当前仓库接入这套流程

装的是**约定**，不是能力。skills 已经在机器上（`~/.ai-native-workflow`），这一步只往仓库里放
需要被 review、被版本固定、被队友 clone 到的东西。

## 做五件事

源目录 `${AI_NATIVE_WORKFLOW_HOME:-$HOME/.ai-native-workflow}`（不存在就告诉用户先跑 `install.sh`，不要自己造内容）。

### 1. 注入 `AGENTS.md`

把源目录的 `AGENTS.block.md` 内容写进仓库根 `AGENTS.md`：

- 没有 `AGENTS.md` → 新建，写入该块
- 有 → 找 `<!-- ai-native-workflow:start -->` … `<!-- ai-native-workflow:end -->`：
  - 找到 → **只替换这两行之间的内容**（升级路径），项目自己写的部分一个字不动
  - 没找到 → 追加到文件末尾

`CLAUDE.md` 若不存在，建一个指向 `AGENTS.md` 的软链（Claude Code 读它）。已存在就别动。

### 2. 放模板

```
docs/templates/meegle-work-item.md          ← 源目录 templates/meegle-work-item.md
docs/templates/merge-request.md             ← 源目录 templates/merge-request.md
docs/templates/technical-design.md          ← 源目录 templates/technical-design.md
docs/templates/test-cases.md                ← 源目录 templates/test-cases.md
docs/templates/quality-report.html          ← 源目录 templates/quality-report.html
.gitlab/merge_request_templates/default.md  ← 同 merge-request.md（GitLab 开 MR 时自动带出）
```

已存在的文件**不覆盖**，报告「已存在，跳过」，让用户自己决定要不要合并。

### 3. 建 `docs/intent/`

放一个 `README.md` 说明它装什么：每次 `/p` 的选型理由、每次 `/b` 踩的坑和留的债，
文件名按主题（`docs/intent/order-state.md`）。这是 MR 里 Why 段唯一的原料来源。

同时建 `docs/intent/GOTCHAS.md`（空表即可）：踩了会疼、但从代码看不出来的地方。

### 3.5 提醒项目补占位

注入的块里有四处需要项目自己填，**列出来提醒用户**，不要替他猜：

- 「本项目的事实来源」第 5 条起 —— 架构文档 / 设计系统 / ADR 在哪
- 「项目结构」的源码根目录与测试根目录
- 「合并前本地验证」表 —— 真实的 lint / typecheck / 单元+接口 / 集成命令
- 已知的坑 —— 老项目通常一抓一大把，先记三条最疼的

能从 `package.json` / `Makefile` / CI 配置 / 现有目录结构里**读到**的可以直接填进去，
读不到的留占位，别编。

同时核对「共同上下文文档」五份（核心业务流程、技术架构、API 与调用链、系统约束、外部依赖）
在 `docs/` 下有没有，**只报缺口，不建空文件** —— 空壳文档比没有更坏，它让人以为已经有了。

### 4. 项目专属 skill 的位置

建 `.agents/skills/`（Codex 与 pi 原生读），并建两条软链让另外两个工具也看得到：

```bash
mkdir -p .agents/skills .claude .qoder
ln -sfn ../.agents/skills .claude/skills
ln -sfn ../.agents/skills .qoder/skills
```

这里放**这个项目专有**的 skill（部署流程、领域词汇表、内部服务约定），
不放 `/pd /bl /s /p /b /t` —— 那些在机器级，升级一次全项目生效。

先检查 `.claude/skills` / `.qoder/skills` 是否已存在且不是软链；是就跳过并报告，不覆盖。

### 4.5 CI 兜底（问过再做）

**先问用户要不要**，同意了再动 `.gitlab-ci.yml`：

> 要不要加一个 MR 约定检查 job？它检查：标题带工作项号、六段齐全非空、
> Why 段引用的 `docs/intent/*.md` 真实存在。不齐则 MR 变红。

同意 → 复制 `templates/mr-contract-check.sh` 到 `.gitlab/mr-contract-check.sh`，
把 `templates/gitlab-ci-mr-contract.yml` 里的 job **合并**进项目的 `.gitlab-ci.yml`
（读一遍现有 stage 结构再插，**不要整份覆盖**）。没有 `.gitlab-ci.yml` 就新建。

不管做不做，都提醒一句：**「未 resolve 的讨论不能合入」在 GitLab 项目设置里有原生开关**
（Settings → Merge requests → Merge checks → All threads must be resolved），
打开它比写 CI 可靠，一分钟的事。

### 5. 报告

列出：写了哪些文件、跳过了哪些（为什么）、建了哪些软链。
提醒用户 **把这些改动 commit 进仓库** —— 约定要随仓库走，队友 clone 即得。

## 规则

- **不覆盖用户已有内容。** 只有 `ai-native-workflow` 标记块之间的内容可以被替换。
- 不生成 `.gitignore` 条目：这些文件本来就该进 git。
- 不改 CI 配置、不装依赖、不碰源码。
- 仓库不是 git 仓库时先停下来问。
