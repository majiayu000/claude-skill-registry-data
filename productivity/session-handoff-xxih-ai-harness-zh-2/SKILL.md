---
name: session-handoff
description: 当用户明确要求做 session 收尾、生成 handoff、为新窗口续跑保存上下文，或在上下文将满时准备交接材料时使用。
---

# Session Handoff

这个 skill 解决的是“这一窗口先收住，下一个窗口怎么无缝接上”。它不是默认行为，也不是普通总结；它要求先把值得沉淀的 learning 收口到明确出口，再把可继续执行的 handoff 文档写进本地 `.session/`。

## 何时使用

- 用户明确要求做 session 收尾、handoff、save session、换窗口续跑、上下文接力
- 当前 section 已告一段落，但不准备现在结束整条工作流
- 上下文窗口接近极限，需要把当前状态压缩成交接文档

不适用：

- 用户只是让你普通总结一下，而不是为后续 session 交接
- 当前仍在主要实现中段，既没有阶段性结论，也没有可交接的下一步
- 只是要做长期规则沉淀，不需要生成本地 handoff 文档
- 用户没有明确触发 session 交接意图时，不要主动启用

## 产物

每次使用本 skill，默认产出以下最小集合：

1. learning 出口结果
   - 先按 `learning-evolution` 的规则判断信号该去 `drop`、`keep-task-local`、`queue-support` 还是 `codify-now`
   - 落点继续使用当前任务容器、`.learned/rules.md`、`.learned/support.md` 或正式资产
2. handoff 文档
   - 写入 `.session/<YYYYMMDD-HHMMSS>-session-handoff.md`
   - 文件名中的时间必须是本次 session 实际结束时间，不能写相对时间
3. 续跑入口
   - 向用户明确 handoff 文件路径
   - 说明它只是可选入口，不假设下个窗口一定会使用它

## 工作流

1. 先确认这是显式触发
   - 只有用户明确要求 session 收尾、handoff、save / resume 类动作时才继续
   - 若只是“顺手总结一下”，不要擅自写 `.session/`
2. 收集当前 session 证据
   - 当前目标、已做改动、验证结果、失败尝试、关键决策、剩余阻碍、下一步
   - 若当前工作已有任务容器、研究记录或验证记录，优先复用
3. 先做 learning 出口判断
   - 先运行 `Observation -> Selection -> Representation`
   - 已经足够明确且用户允许演化时，直接 `codify-now`
   - 不要跳过这一步直接写 handoff；否则交接文档只会变成散乱摘要
4. 准备 `.session/`
   - 若目录不存在则创建
   - 该目录默认应已被 `.gitignore` 忽略；若未忽略，先补 ignore 再继续
5. 生成 handoff 文档
   - 使用当前 session 的实际结束时间命名文件
   - 按模板完整填写，不要只写几条松散 bullet
   - 没有内容的部分也要诚实写明 `无`、`尚未确认` 或 `未发生`
6. 向用户交付
   - 报告写入路径和本次 learning 落点
   - 提醒这是给下个窗口使用的可选入口，不自动恢复，不替用户决定何时读取

## handoff 文档要求

- 必须写明 `结束时间`，并与文件名中的时间一致
- 必须区分：
  - 已确认有效
  - 已完成但未验证
  - 明确失败或不该重试
  - 下一窗口的精确起点
- 必须记录本次 learning 的落点，而不是只说“做了 learning”
- 若本次没有代码改动，也要说明是研究、整理还是决策性 session
- 若工作区有未提交改动或已知风险，要直接写明，不要让下个窗口重新猜

## 输出模板

需要模板时，读取 [references/templates.md](references/templates.md)。

## 纪律约束

- 这是显式 skill；没有用户主动触发，不要自动执行
- handoff 文档是交接材料，不是把整段对话原样倾倒到文件
- 不要把 task-local、长期规则、资产候选混写成一团；先按 `learning-evolution` 分流
- 文件名必须包含本次 session 结束时间，且使用绝对时间，不写“today”“just now”
- 不要假设用户下个窗口一定会读取这个文件；它是备选入口，不是强依赖
