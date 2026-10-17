---
name: retro
description: "对一次 coding session 做复盘。"
disable-model-invocation: true
---

用户要求做一次 **retrospective**。你的任务是针对 coding agent 的**环境**提出改进建议，让未来的运行更好。

## Steps

1. 调用 Skill tool 的 `writing-for-agents`，获取写作风格指南。

2. 阅读用户所指那次 session 的 primary sources。这可能需要在本机上搜索 session 日志。如果用户没有指定 session，默认用当前这一次。

3. 在以下类别中寻找改进候选。

- **Navigation**：agent 找到正确文件有多容易？文件之间是否存在隐藏依赖？加一条 **navigation pointer** 会不会更容易？_Use when_ session 花了很久才找到某条信息。
- **Automated checks**：是否存在能捕获 agent 所犯错误的 automated checks？Linting、typing、测试、filesystem linters？先读仓库自己的 check 命令（它的 `package.json`/build-tool 的 `lint`/`check` scripts、它的 CI workflow），这样"检查已存在但没有接线或悄悄失效"本身就是一个发现，而不是重复发明。一个没有任何 **guardrail** 的仓库（没有 pre-commit hook，也没有跑 lint/typecheck/test 命令的 CI job）本身就是发现：没有 lint 的仓库是一个长期错失的机会，而不是中性默认。_Use when_ agent 犯了某个 automated check 本可以捕获的错误，或仓库完全没有 guardrail。
- **Coding standards**：是否应给 **reviewer agent** 增加一条新规则去执行？是否应删除或澄清某条既有规则？先给违规分类：**mechanical** 违规（固定的句法模式、被禁 API、import 形态、文件位置规则）一律上确定性检查：在仓库自己的 linter 里加自定义规则、新的 pre-commit hook 或新的 CI job，取仓库语言与现有 guardrail 下最便宜的那种。默认构建检查而不是写规则。`CODING_STANDARDS.md` 只保留真正的 **judgement calls**（跨文件一致性、"与周围风格匹配"、任何 guardrail 都无法替代的东西）。_Use when_ reviewer agent 未能捕获某个错误。
- **Global AGENTS.md**：是否有 steering 指令应该移到 coding standards（或 automated checks）里去？_Use when_ AGENTS.md 文件特别大——无论在仓库还是用户的 global scope。
- **Tool economy**：agent 是否做了本可以精简的昂贵 tool calls？是否有特别 token 低效的自定义工具（CLI、MCP）？_Use when_ agent 做了昂贵的 tool call。
- **No-ops**：在 steering 文件里寻找并不改变 agent 行为的指令。_Use when_ steering 文件庞大且臃肿。
- **Information access**：寻找提升 agent 信息获取能力的机会。将 dev server logs 同时输出到另一处、对第三方服务的只读访问。_Use when_ agent 无法获取某条关键信息。

4. 按严重程度排序，把这些候选呈现给用户。

## Reference

### Implementation vs Review

记住所有工作都经过两个阶段：implementation 和 review。implementation agent 承受最大的 **context pressure**。它负责探索、写代码、调试失败。

review agent 的 context pressure 最小——它拿到的是一个 diff，不需要探索。它通常也不需要写代码或调试。

这意味着应该由 review agent 负责执行 coding standards，而不是 implementation agent。

### Files

你可以访问仓库中的若干文件：

- `CLAUDE.md`/`AGENTS.md`：这些文件会被推入任何在本仓库工作的 agent 的 context window。必须极其节制地使用，通常只用于指向其他文件的 **navigation pointers**。
- `CODING_STANDARDS.md`：这个文件在 review 时读取，而不是 implementation 时。如果 standards 文件超过 1,000 行，就添加指向 docs 文件夹的 **navigation pointers**。
- Docs：把 docs 用作参考文件，由其他文件指向。写新 docs 之前先找现成的。
- Skills：把 skills 用作文档（因为它们的 description 会进入 agent 的 context window），或用作 user-invoked commands。遵循 `writing-for-agents` skill 中的建议。
