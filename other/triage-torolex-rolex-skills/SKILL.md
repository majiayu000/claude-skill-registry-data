---
name: triage
description: 将 issue 和外部 PR 通过一个分类角色 state machine 进行 triage 流转：分类、验证、如有需要，grill（追问澄清），并编写 agent-ready brief。
disable-model-invocation: true
---

# Triage（分类）

将项目 issue tracker 上的 issue 通过一个小型 state machine 进行 triage 流转。

如果本仓库将外部 PR 作为请求面处理（见 issue-tracker 配置），triage 同样覆盖它们：**PR 是带有代码的 issue**，相同的 role、相同的状态、相同的机器，只是下面标注了一些"针对 PR"的差异。将裸 `#42` 解析为 issue 或 PR，按 tracker 配置处理。

Triage 期间发布到 issue tracker 的每条评论**必须**以如下声明开头：

```
> *本文由 AI 在 triage 期间生成。*
```

## 参考文档

- [AGENT-BRIEF.md](AGENT-BRIEF.md)：如何编写持久的 agent brief
- [OUT-OF-SCOPE.md](OUT-OF-SCOPE.md)：`.out-of-scope/` 知识库的工作原理

## 角色

两个**分类** role：

- `bug`：有东西坏了
- `enhancement`：新功能或改进

五个**状态** role：

- `needs-triage`：maintainer 需要评估
- `needs-info`：等待 reporter 提供更多信息
- `ready-for-agent`：完全明确，准备好让 AFK agent 接取
- `ready-for-human`：需要人类实现
- `wontfix`：不会处理

对于 PR，相同的状态适用于附带的代码：`ready-for-agent` 表示已附加 brief，agent 应该在 diff 上执行下一步；`ready-for-human` 表示准备好让人合并。

每个 triage 后的 issue 应恰好携带一个分类 role 和一个状态 role。如果状态 role 冲突，标注出来并在做任何其他事情前询问 maintainer。

这些是规范的 role 名称。issue tracker 中实际使用的标签字符串可能不同。映射关系应该已经提供给你。如果没有，让用户运行 `/setup-rolex-skills`。

状态转换：未标注的 issue 通常先进入 `needs-triage`；然后可以转到 `needs-info`、`ready-for-agent`、`ready-for-human` 或 `wontfix`。`needs-info` 在 reporter 回复后回到 `needs-triage`。maintainer 可以随时覆盖；标记看起来不寻常的转换并在继续前询问。

## 调用

maintainer 调用 `/triage` 并用自然语言描述他们想要什么。解读请求并执行。示例：

- "显示所有需要我关注的内容"
- "我们来看 #42"（issue 或 PR）
- "把 #42 移到 ready-for-agent"
- "哪些准备好了让 agent 接取？"

## 显示需要关注的内容

查询 issue tracker 并按三个桶展示，最早的在最前面：

1. **未标注**：从未被 triage 过
2. **`needs-triage`**：评估进行中
3. **`needs-info` 且 reporter 在上次 triage 后有活动**：需要重新评估

当 PR 在范围内时，将外部 PR 包含在这些桶中，并在每行标注 `[PR]` 或 `[issue]`。发现阶段只暴露*外部* PR（tracker 配置定义了谁算外部），所以协作者进行中的 PR 不是 triage 工作。此过滤器仅适用于发现阶段；明确指定的 PR 无论作者如何都会进行 triage。

显示计数和每项的简要摘要。让 maintainer 选择。

## Triage 特定 issue 或 PR

1. **收集上下文。** 阅读完整的 issue 或 PR（正文、评论、标签、作者、日期；对于 PR，还有 diff）。解析任何先前的 triage 记录，以免重复提问已解决的问题。使用项目的领域词汇浏览代码库，尊重你正在接触区域的 ADR。针对代码库运行两项检查：（a）**冗余**：按领域概念搜索请求行为的现有实现（不仅仅是请求的措辞），并报告搜索位置。如果找到，则是已实现的 `wontfix`（步骤 5）。（b）**之前的拒绝**：阅读 `.out-of-scope/*.md`，找出任何与本次请求相似的内容。

2. **推荐。** 告诉 maintainer 你的分类和状态建议及其理由，加上与请求相关的简短代码库摘要（包括它是否已实现）。等待指示。

3. **验证声明。** 在进一步 grilling 之前，检查声明是否成立。对于 bug，按 reporter 的步骤复现。对于 PR，确认 diff 做了它声称的事情：检出它，运行相关测试或命令。报告发生了什么：验证通过（附代码路径）、失败、或细节不足（强烈的 `needs-info` 信号）。经过验证的确认能生成更强的 agent brief。

4. **Grill（如果需要）。** 如果请求需要细化，调用 Skill 工具两次，分别传入 "grilling" 和 "domain-modeling"，一轮问题一轮问题地将其追问成形，同时锐化领域术语，并随着决策落地就地更新 `GLOSSARY.md`/ADR。

5. **应用结果：**
   - `ready-for-agent`：发布 agent brief 评论（[AGENT-BRIEF.md](AGENT-BRIEF.md)）。
   - `ready-for-human`：结构与 agent brief 相同，但注明为什么不能委托给 agent（需要判断、外部访问、设计决策、手动测试）。
   - `needs-info`：发布 triage 记录（模板见下）。
   - `wontfix`：关闭 issue，根据*原因*选择不同评论：
     - **已实现**：更改已存在于代码库中。指向所在位置；**不要**写入 `.out-of-scope/`（该知识库只针对*已拒绝*的请求，不是已构建的）。
     - **已拒绝（bug）**：礼貌解释，然后关闭。
     - **已拒绝（enhancement）**：写入 `.out-of-scope/`，在评论中链接，然后关闭（[OUT-OF-SCOPE.md](OUT-OF-SCOPE.md)）。
   - `needs-triage`：应用 role。如果已有部分进展可加可选评论。

## 快速状态覆盖

如果 maintainer 说"把 #42 移到 ready-for-agent"，信任他们并直接应用 role。确认你将要做什么（role 更改、评论、关闭），然后执行。跳过 grilling。如果移到 `ready-for-agent` 但没有 grilling 会话，询问他们是否要写 agent brief。

## Needs-info 模板

```markdown
## Triage Notes

**目前已经确认的情况：**

- 要点 1
- 要点 2

**我们仍然需要你提供的信息（@报告人）：**

- 问题 1
- 问题 2
```

在"已确认的情况"下捕获 grilling 期间解决的所有内容，以免工作丢失。问题必须具体且可操作，而非"请提供更多信息"。

## 恢复之前的会话

如果 issue 或 PR 上存在先前的 triage 记录，阅读它们，检查 reporter 是否已回复任何未解决的问题，然后在继续之前呈现更新的画面。不要重复已解决的问题。
