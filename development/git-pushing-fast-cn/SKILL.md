---
name: git-pushing-fast-cn
description: 当用户需要在当前单分支提交并推送改动，并生成 Conventional Commit 信息时使用。支持基于 diff 自动判断 type/scope/summary、处理已暂存或用户要求的改动范围、为非简单改动生成分段提交正文，并安全处理单分支推送。
---

# Git 快速提交推送

## Overview

在当前仓库的当前分支上，快速、安全地提交并推送本地改动。

默认结果是一个聚焦的 Conventional Commit，再推送到当前分支跟踪的远端。需要分析实际 diff，暂存用户要求的改动范围，根据改动内容生成提交信息；对于非简单改动，需要写分段提交正文，让评审者能按主题快速理解改动内容。

这个流程适用于普通单分支交付，例如把当前工作保存到远端；不处理分支合并、历史改写或 PR 创建。

## Conventional Commit 规则

基础格式：

```text
<type>[可选 scope]: <description>

[正文：仅简单改动可省略；非简单改动必须写分段正文]

[footer：破坏性变更必须填写；相关 issue 引用可按需填写]
```

在本技能中，正文只对简单提交可选。非简单改动必须写分段正文；如果运行了测试、校验、hook 或手动验证，必须包含“测试：”或“验证：”等价分段。

类型：

| Type | 用途 |
| --- | --- |
| `feat` | 新增用户可见或产品能力 |
| `fix` | 修复 bug |
| `docs` | 仅文档变更 |
| `style` | 不影响逻辑的格式或样式变更 |
| `refactor` | 不新增功能、不修 bug 的代码重构 |
| `perf` | 性能优化 |
| `test` | 测试或覆盖率变更 |
| `build` | 构建系统、依赖或打包变更 |
| `ci` | CI 或自动化配置变更 |
| `chore` | 维护或杂项变更 |
| `revert` | 回滚历史提交 |

破坏性变更：
- 在 type 或 scope 后使用 `!`，例如 `feat(api)!: 移除旧字段`。
- 行为契约发生变化时，在 footer 中加入 `BREAKING CHANGE:`。

提交信息风格：
- 使用仓库既有的提交语言。
- 标题使用现在时和祈使语气，例如 `fix login redirect` 或 `修复登录跳转`。
- 标题尽量控制在 72 个字符以内。
- 相关时在正文或 footer 中引用 issue，例如 `Closes #123` 或 `Refs #456`。

## 何时使用

当用户要求执行以下操作时使用本技能：
- 提交并推送当前工作
- “推上去”、“保存到远端”或完成普通单分支交付
- 将 staged 和 unstaged 改动整理为一个 Conventional Commit
- 提交正文需要按功能区、界面区、测试、文档或校验结果分段说明

## 不要使用

以下场景不要使用本技能：
- 需要将工作分支合并到主分支的双分支流程
- 强制推送、rebase、squash、amend 或改写历史
- 创建 Pull Request，除非用户在推送后明确要求
- 代码评审、发布说明、周报或 changelog 生成
- `git reset --hard`、`git checkout -- <file>` 等破坏性命令

## 使用说明

按以下流程顺序执行。目标仓库、分支或推送目的地不明确时，停止并说明阻塞原因，不要猜测执行。

1. 检查仓库状态。
   - 运行 `git status --short`、`git branch --show-current` 和 `git remote -v`。
   - 可用时通过 `git rev-parse --abbrev-ref --symbolic-full-name @{u}` 检查 upstream。
   - 先看暂存区统计和实际内容：`git diff --cached --stat` 与 `git diff --cached`；如果没有暂存改动，再看 `git diff --stat` 与 `git diff`。
   - 需要脚本友好地解析状态时，使用 `git status --porcelain`。
   - 不得丢弃或回滚用户改动。

2. 暂存改动。
   - 用户要求提交全部改动时，执行 `git add -A`。
   - 用户指定更小范围时，只暂存指定范围。
   - 仅当用户要求的范围需要逻辑分组时，使用指定文件、路径模式或 `git add -p`。
   - 重新运行 `git status --short`，确认目标文件已经暂存。
   - 禁止让已知密钥文件留在待提交暂存区，包括 `.env`、凭证文件、私钥或 token。

3. 生成提交信息。
   - 使用 Conventional Commits：`type(scope): 中文摘要`。
   - 根据实际 diff 选择 type 和 scope，不得只根据文件名判断。
   - 对非简单改动，提交正文必须包含 2-5 个简短分段。
   - 分段标题命名受影响区域，下面用列表说明具体变化。
   - 如果运行了测试、校验、hook 或手动验证，需要加入“测试：”或“验证：”分段。

分段正文示例：

```text
fix(module): 调整组件行为

行为：
- 调整受影响组件的默认状态。
- 对不支持的输入保持原有行为不变。

实现：
- 将重复逻辑移动到小型辅助函数。
- 更新相关配置以使用新的辅助函数。

测试：
- 补充更新行为的覆盖用例。
- 推送前运行相关校验。
```

4. 提交。
   - 使用多个 `-m` 参数或其他无交互方式执行 `git commit`，确保正文被完整保留。
   - 禁止使用 `--no-verify`。
   - hook 或校验失败时，先修复失败原因，再重新提交。

5. 推送。
   - 当前分支已有 upstream 时，执行 `git push`。
   - 当前分支没有 upstream 时，执行 `git push -u origin <current_branch>`，除非仓库或用户指定其他远端。
   - 推送因远端更新被拒绝时，先 `git fetch` 并检查差异再决定下一步。
   - 除非用户明确要求强推并确认风险，否则不得 force-push。
   - 禁止向 `main` 或 `master` 强推。

6. 汇报。
   - 最终回复保持简洁。
   - 说明提交哈希、分支、远端推送结果和已运行的校验。
   - 如果宿主应用支持 Git 指令，仅在对应 Git 动作成功后再发出相关指令。

## 安全协议

- 禁止修改 global 或 system Git config。
- 除非用户明确要求，禁止运行 `git reset --hard` 或 `git checkout -- <file>` 等破坏性命令。
- 禁止跳过 hooks。
- 禁止提交密钥。
