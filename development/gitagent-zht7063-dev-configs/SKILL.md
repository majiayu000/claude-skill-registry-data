---
name: gitAgent
description: Use this skill in the scenario of writing git commit messages.
---

# 1. 适用范围

- 适用于所有 Git 提交（包括合并前的普通提交）。
- 不要求额外脚本/工具；仅规范输出内容。
- 与 Conventional Commits 类似，但增加 Emoji 前缀，并对主题、正文、脚注给出更严格的可读性约束。

# 2. 输出目标

你的输出结果需要符合以下目标：

1. 一眼可读：从提交列表即可判断改动性质与影响范围。
2. 可追溯：需要时可在正文/脚注补充动机、影响与关联 Issue。
3. 可检索：类型与 scope 统一，便于按模块聚合。
4. 低噪声：一次提交尽量只解决一类问题；避免“杂烩提交”。

# 3. Commit Message 格式

## 3.1 标准格式（推荐）

一个标准的 Commit Message 格式应该是：

```
<emoji> <type>(<scope>): <subject>

<body>

<footer>
```

其中：

- emoji：见下方映射表，只能选 1 个。
- type：小写固定集合（见映射表）。
- scope：可选，但强烈建议在中大型仓库中填写。
- subject：必须为祈使句/动词开头，简洁描述“做了什么”。
- body：可选，用于解释“为什么/怎么做/影响”。
- footer：可选，用于 BREAKING CHANGE:、Refs:、Closes: 等。

## 3.2 最短格式

当变更很小且无需解释时使用最短格式：

```
<emoji> <type>: <subject>
```

# 4. 主题行规则（Subject Rules）

Subject 部分的要求为：

- 长度：建议 ≤ 72 字符（英文）/ ≤ 40 中文字符（尽量短）。
- 语气：使用祈使句（Add/Fix/Refactor/Update/Remove/Improve…）。
- 不加句号：结尾不要 ./。。
- 不写废话：禁止 update stuff、fix bug 这类无信息密度表达。
- 不混合多件事：如果涉及多模块多类型，拆分提交。

示例：

✅ ✨ feat(api): add token refresh endpoint
✅ 🐛 fix(train): handle empty batch in dataloader
❌ ✨ feat: add something
❌ fix: bug

# 5. Scope 规则（建议统一）

## 5.1 何时需要 scope

- 项目有多个子系统/包/模块/服务时，必须写。
- 单模块小仓库可省略，但推荐保留以利未来扩展。

## 5.2 Scope 命名规范

- 全小写，使用 - 连接：data-loader、auth、ui、docs。
- Scope 的来源优先级：
  - 顶层目录（src/xxx、packages/xxx）
  - 服务名/包名
  - 明确功能域（training、metrics、infra）

# 6. Emoji x Type 映射表

> 选择原则：根据“主要意图”选 1 个 emoji + type。不要为了好看堆 emoji。

| Emoji | Type     | 适用场景                       | 主题动词示例                   |
| ----- | -------- | ------------------------------ | ------------------------------ |
| 🎉    | init     | 初始化仓库/项目脚手架/首次提交 | init, scaffold, bootstrap      |
| ✨    | feat     | 新功能/新能力                  | add, implement, support        |
| 🐛    | fix      | 修复 bug                       | fix, correct, handle           |
| ♻️    | refactor | 重构（不改功能）               | refactor, simplify, reorganize |
| ⚡️   | perf     | 性能优化                       | speed up, optimize             |
| 🧪    | test     | 测试相关                       | add, update, stabilize         |
| 📝    | docs     | 文档/注释/README               | document, update, clarify      |
| 🎨    | style    | 代码风格（不影响语义）         | format, lint, style            |
| 🔥    | remove   | 删除代码/资源                  | remove, delete, drop           |
| 🚑    | hotfix   | 紧急修复（生产事故）           | hotfix, patch                  |
| 🚀    | build    | 构建/打包/发布相关             | build, release, bump           |
| 👷    | ci       | CI 配置/流水线                 | configure, fix                 |
| 🔧    | chore    | 杂项维护（不属于以上）         | update, maintain               |
| 🔒    | security | 安全修复/加固                  | harden, patch                  |
| ⏪    | revert   | 回滚提交                       | revert                         |

**补充约束**：

- `chore` 仅在确实无法归类时使用，优先用更具体类型。
- `hotfix` 只用于“线上紧急修复”；一般 bug 修复用 `fix`。

# 7. Body Rules （正文写法，可选但推荐）

当满足任一条件时必须写 body：

- 变更 **非直观**（看 diff 不容易明白动机）。
- 影响面较大（接口、训练流程、数据格式、配置等）。
- 修复了边界条件/历史遗留问题，需要解释原因。

## 7.1 Body 模板（推荐使用要点列表）

```text
Why:
- ...

What:
- ...

Impact:
- ...
```

- 每行建议 ≤ 80 字符（英文）/ ≤ 50 中文字符。
- 只写关键信息，不写“我做了很多工作”。

# 8. Footer（脚注）规则（可选）

## 8.1 关联 Issue/任务

```text
Refs: #123
Closes: #456
```

## 8.2 破坏性变更（必须声明）

```text
BREAKING CHANGE: <说明破坏点与迁移方式>
```

- 当 API、配置、数据格式不兼容时必须添加。

# 9. 典型场景示例

## 9.1 新功能

```text
✨ feat(cli): add `--dry-run` option for evaluation

Why:
- Allow checking configuration without launching training

What:
- Parse and validate flags
- Skip side effects when enabled
```

## 9.2 Bug 修复

```text
🐛 fix(data-loader): handle empty mask when computing loss

Why:
- Some samples contain no valid foreground pixels

Impact:
- Prevent NaN loss and training crash
```

## 9.3 重构

```text
♻️ refactor(model): split encoder init from forward path

What:
- Extract encoder construction into dedicated factory
- Keep behavior identical
```

## 9.4 性能优化

```text
⚡️ perf(inference): cache text embeddings for repeated prompts
```

## 9.5 文档

```text
📝 docs(readme): clarify installation steps for CUDA builds
```

## 9.6 测试

```text
🧪 test(metrics): add unit tests for mIoU edge cases
```

## 9.7 CI

```text
👷 ci(github): fix caching key for pip dependencies
```

## 9.8 回滚

```text
⏪ revert(train): revert mixed precision change causing overflow

Refs: <commit-hash>
```

---

# 10. 禁止项（Claude Code 不得输出）

- ❌ 不要写 `WIP`、`tmp`、`try`、`update` 这类无意义提交（除非仓库明确允许临时分支）。
- ❌ 不要在 subject 里写文件列表、路径堆砌。
- ❌ 不要在同一个提交里混合 `feat` 与 `fix` 等多个主类型。
- ❌ 不要省略关键信息：例如“修复 bug”但未说明修复点。
- ❌ 不要把正文写成大段流水账。

---

# 11. 自检清单（提交前 10 秒）

Claude Code 生成提交信息前，请自检：

- emoji 与 type 是否匹配主要意图？
- subject 是否动词开头、足够具体、无句号？
- scope 是否正确反映主要改动模块？
- 是否只做了一件事（或一个主题）？
- 若有破坏性变更，是否写了 `BREAKING CHANGE:`？
- 若修复/实现对应 Issue，是否写了 `Refs/Closes`？

---

# 12. 快速决策指南（选 type 的最短路径）

- 初始化仓库/项目脚手架/首次提交 → `🎉 init`
- 新能力/新接口/新行为 → `✨ feat`
- 修 bug/修异常/修逻辑错误 → `🐛 fix`
- 结构调整但行为不变 → `♻️ refactor`
- 仅加速/降显存/提升吞吐 → `⚡️ perf`
- 只改文档/注释 → `📝 docs`
- 只改测试 → `🧪 test`
- 只改 CI → `👷 ci`
- 构建、依赖、发布版本 → `🚀 build`
- 删除代码/资源 → `🔥 remove`
- 线上紧急修复 → `🚑 hotfix`
- 其他维护杂项 → `🔧 chore`

---

# 13. 额外约定（可选但推荐）

- 同一仓库内尽量固定 scope 集合（长期维护可以在 README/CONTRIBUTING 中列出允许的 scope）。
- 若团队使用 PR 标题生成 changelog，可直接复用本规范作为 PR 标题格式。/
