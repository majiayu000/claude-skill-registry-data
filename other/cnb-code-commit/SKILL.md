---
name: cnb-code-commit
description: 编写代码、提交并创建 PR。
---

# 自动编码并提交推送

根据用户需求选择：
1. 新建分支 -> 编写代码 -> 推送代码 -> 并创建 PR
2. 切换到 PR 源分支 -> 编写代码 -> 推送代码更新 PR

## 步骤

### 1. 理解需求

分析用户输入，明确要修改的文件、功能/Bug 描述、目标分支（PR 的 base）。
如需了解项目结构，直接在当前工作区读取代码。如需了解 PR 变更，可使用 cnb-pr-diff Skill。

### 2. 判断场景并准备分支

根据触发场景切换到正确的工作分支：

- **PR 评论触发**（`CNB_PULL_REQUEST_IID` 存在）：在此分支上继续修改
  ```bash
  git checkout "$CNB_PULL_REQUEST_BRANCH"
  git pull origin "$CNB_PULL_REQUEST_BRANCH"
  ```
- **ISSUE 评论触发** PR 已存在，则切换到 PR 源分支继续开发
  ```bash
  git checkout <PR 源分支名> && git pull
  ```
- **ISSUE 评论触发** PR 不存在，则基于目标分支创建新分支 `auto/{关键词1}-{关键词2}-{4位随机后缀}`
  ```bash
  git checkout -b auto/{关键词1}-{关键词2}-$(openssl rand -hex 2)
  ```
  > ⚠️ **分支命名精简规则**：
  > - `{关键词}`：从 ISSUE 标题/描述中提取 **2 个核心关键词**（名词或动词），用短横线连接，每个关键词不超过 2 个英文单词
  > - `{随机后缀}`：固定 4 位十六进制，用 `$(openssl rand -hex 2)` 生成
  > - **总长度控制**：分支名 `auto/` 之后的部分不超过 20 个字符
  > - **示例**：`auto/optimize-skill-3a7f`、`auto/login-error-b2c1`

### 3. 编写代码

直接在工作区中读取和修改文件，实现代码变更。遵循项目已有的代码风格，确保 import/依赖完整。

**生成/修改 `.cnb.yml` 时的特殊处理**：
- 优先加载 `cnb-pipeline` skill 的 SKILL.md，参照其中的语法文档和校验方式生成并验证配置
- 生成完成后需通过 cnb-pipeline skill 提供的校验方式验证，校验通过后才能提交；校验失败则修复后重新校验

### 4. 验证与提交

```bash
# 查看变更概览
git diff --stat
# 如有构建/lint 命令则执行验证
# 暂存并提交
git add -A
git commit -m "{类型}: {简短描述}"
```

类型：`feat`(新功能) / `fix`(修复) / `refactor`(重构) / `docs`(文档) / `chore`(其他)

### 5. 推送变更并判断是否需要创建 PR

```bash
# 推送当前分支
git push origin HEAD
```

根据推送输出判断是否已有 PR：

- **已有 PR**（输出包含 `There is already has pull request`）：跳过创建 PR，直接在评论中告知用户
- **无 PR**（输出包含 `Create a pull request` 或 `new branch`）：走第 6 步创建 PR

> ⚠️ 只有新建分支且推送后确认无 PR 时，才执行第 6 步。

**示例 1 — 已有 PR，跳过创建：**
```
$ git push origin HEAD
remote:
remote: There is already has pull request for 'fix/optimize-cnb-code-commit-skill' by visiting:
remote:
remote: 	https://cnb.cool/cnb/skills/cnb-skill/-/pulls/140
remote:
To https://cnb.cool/cnb/skills/cnb-skill.git
   e3d8f95..639bd55  HEAD -> fix/optimize-cnb-code-commit-skill

# 输出包含 "There is already has pull request" → 已有 PR，不再创建
# 在评论中告知用户：PR 已存在，代码已推送到 PR #140
```

**示例 2 — 无 PR，需要创建：**
```
$ git push origin HEAD
remote:
remote: Create a pull request for 'fix/optimize-cnb-code-commit-skill' to 'main' by visiting:
remote:
remote: 	https://cnb.cool/cnb/skills/cnb-skill/-/compare/main...fix/optimize-cnb-code-commit-skill
remote:
To https://cnb.cool/cnb/skills/cnb-skill.git
 * [new branch]      fix/optimize-cnb-code-commit-skill -> fix/optimize-cnb-code-commit-skill

# 输出包含 "Create a pull request" → 无 PR，需要走第 6 步创建
```

### 6. 创建 PR（仅推送后确认无 PR 时执行）

```bash
cnb pulls post-pull --repo "$CNB_REPO_SLUG" \
  --base "$CNB_DEFAULT_BRANCH" \
  --head "$(git branch --show-current)" \
  --title "{类型}: {简短描述}" \
  --body '{变更目的与主要改动，支持 Markdown 真换行}

Ref #'"$CNB_ISSUE_IID"
```

> ⚠️ `--body` 用**单引号包真换行**，不要用 `\n`；非 ISSUE 触发时去掉末尾 `Ref #...` 行。

## 注意事项

- 编码前先理解项目结构和代码风格
- 需求不明确或范围过大时，先在评论中确认再执行
- 不修改无关文件，推送前确认变更正确
- 生成/修改 `.cnb.yml` 文件时需使用 cnb-pipeline skill 技能
- **推送后不要轮询 CI 状态**：代码推送后会自动触发 CI，无需主动调用 `cnb pulls check-status` 等命令反复轮询。如果 CI 失败，平台会自动唤起 NPC 继续处理，NPC 只需在评论中说明已完成的修复即可结束当前会话

## 禁止的操作

- ❌ PR 不存在时，禁止在默认分支上修改代码，需新建分支并创建 PR
- ❌ `git push --force`（不要强制推送，除非用户明确要求；如需覆盖可用 `--force-with-lease`）
- ❌ 推送代码后轮询/等待 CI 状态（CI 失败会自动唤起 NPC，无需主动等待）
