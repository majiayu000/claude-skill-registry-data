---
name: grilling
description: 对 plan、decision 或 idea 进行无休止的追问。当用户想要压力测试他们的思考，或使用任何 'grill' 触发短语时使用。
---

无休止地访谈用户，直到达成 shared understanding。把它映射为一棵 **design tree**：每个 decision 都分支为挂在它下面的 decisions。

以 **rounds**（轮次）来推进这棵树。**frontier** 是每个前提都已确定、你可以*现在*就问的 decision：不需要猜测你还没听到的答案。一轮里问整个 frontier：给每个问题编号并给出你的 recommended answer。然后等待用户回答，再进入下一轮。

一轮的格式如下：

```
❓ **Q1** - **<问题标题>**: <问题正文，可能是多段，包括多个选项>

➡️ <你的推荐答案>

---

❓ **Q2** - **<问题标题>**: <问题正文，可能是多段，包括多个选项>

➡️ <你的推荐答案>
```

每轮用户的回答都会重塑这棵树：已确定的 decisions 把 frontier 向外推，解锁依赖它们的后续问题。重新计算 frontier，再问下一轮。一个问题的答案依赖本轮内另一个仍开放的问题，它属于*更晚*的一轮，而不是这一轮。

查找 _facts_ 是你的工作，永远不是用户的。当 frontier 问题需要来自环境（filesystem、tools 等）的事实时，派一个 sub-agent 去找；不要向用户询问任何你自己能查到的东西。不要阻塞等待它：一个运行中的探索是一个尚未确定的前提，所以只有它下游的问题才等待 sub-agent 报告；现在就把 frontier 其余的问题问完。_decisions_ 是用户的：把每个 decision 摆到用户面前，等待回答。

当 frontier 为空时 session 结束：design tree 的每个分支都被访问过，没有任何东西被默默假设。在用户确认你们已达成 shared understanding 之前，不要执行它。
