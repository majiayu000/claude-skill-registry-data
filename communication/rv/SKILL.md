---
name: rv
description: Reviews a branch or merge request for semantic defects and posts each finding as its own resolvable GitLab thread. Use before opening an MR as a final self-check, when assigned to review someone's MR, when the user says /rv, or when asked to review code or a diff.
---

# /rv —— 五轴之外的语义 review

## 两种模式

先判模式，再进 review 步骤。**方法论两边完全相同**，只有 diff 从哪来、findings 发到哪不同。

**本地模式**（无参数，或参数是 `local`）—— 开 MR 前的最后一道关：

```bash
BASE=$(git merge-base ${2:-main} HEAD); git diff "$BASE"   # 含未提交改动
```
findings **只打到 chat**，不碰 GitLab。

**MR 模式**（参数是 MR 号或 URL）：

```bash
glab mr diff <id>
glab mr view <id> --json  # 或不带 --json 读描述
```
findings 先打到 chat，**再**作为 discussion 发到 MR（见末尾）。

**什么时候不该跑**：每次提交后、每轮改动成型后。它是整条分支的全量高成本 pass，
fresh-context 的价值一次性兑现，反复重扫只是拖慢循环，不多抓 bug。

## Step 1 · 找到这次改动的核心语义

不要从 diff 第一行开始扫。先回答：**这次改动引入或修改了什么概念？这个概念的定义是什么？**

读 MR 描述 + commit message + 核心文件，提炼 thesis：

> 本次改动新增/修改了 X 概念，X 表达的语义是 Y，它在系统中的位置是 Z。

提炼不出来，这本身就是第一个 finding —— 这个改动没有清晰的核心。

## Step 2 · 围绕核心概念延伸（review 的脊柱）

按关注度排序，不是平等并列：

**A. 概念语义** —— 它封装/表达了什么？一句话说得清吗？有没有暴露**超出**语义的能力（漏），
或**缺失**语义应有的能力（不完整）？

**B. 命名** —— 命名错 = 语义错，不是格式问题。名字不对的概念，使用方会被字面意思误导。

**C. 边界** —— 这个属性/方法是否**非放在这里不可**？问「放在这里是必然的还是顺手的」，
不是「放在这里行不行」。

**D. 概念关系** —— 耦合是否破坏了任一方的语义？代码里的概念关系是否 mirror 业务里的关系？

**E. 分层** —— IO / 数据 / 渲染（或 传输 / 业务 / IO）是否互不知晓对方实现？
边界处校验，内部信任。

**F. 错误处理**（语义性最强，最常被错当成「加 try-catch」）——
本质是**责任分配**：抛错的人想过谁来处理吗？处理的人想过该不该由自己处理吗？
责任链终点是用户：这个错误用户能处理（提示 + 重试/改输入），还是用户处理不了、
软件要兜底（降级/重试/带诊断地失败）？

吞错误、泛化 catch-all、`catch { return null }`、空 catch、把系统错误当用户错误报 ——
全部是**责任分配失败**。

## Step 3 · Review 测试

不看覆盖率，看每个测试**有没有语义**：

1. 这个测试验证什么情况？说不清 = 它是个仪式。测试名就是 spec：
   `test_user_creation` 没 spec，`test_user_creation_fails_when_email_already_registered` 才是。
   显式检查：有没有失败/边界 case，还是只有 happy path。
2. 它真的在验证预期，还是把实现重写一遍（实现错测试跟着错 = 等于没测）？
   **Mock 是责任声明** —— mock 掉 X = 「我信任 X 的行为」。mock 掉 DB 然后「验证」事务回滚，
   测的是 mock，不是事务。粒度错位的测试，它的 passed 不提供它声称的保护。
3. 删掉它会丢失什么保护？答不上来就该删或重写。

## Step 4 · 过程性担忧

- **静默决策**：diff 里有没有未在 MR 描述 / `docs/intent/` 里说明的选择？挖出来。
- **顺手改动**：没人要求但顺带做的，列出来让作者确认动机。
- **本该出现却没出现的改动**：改了 schema 没改 migration、改了接口没改全部调用方、
  改了行为没更新 `AGENTS.md` / 文档 / 测试 —— **漏改比错改更难发现**。
- **不可逆变更**：迁移、删除、协议/数据格式破坏 —— 有回滚路径吗？

## 输出

只输出**实际发现**的问题。每条写：位置（file:line 或概念名）、问题（具体哪里语义不对）、
建议方向（改成什么）。

禁止：打 P0/P1/严重度标签、按 Step/维度分节、写「X 部分未发现问题」、写整体评价/综合结论、
用「建议优化 / 可以考虑 / 或许」软化、把 nit 升级成 issue 凑数。

**空报告是合法且常见的输出。** 不要为了显得在做事而注水。

## 写回 MR（仅 MR 模式）

一条 finding = **一条独立 discussion**，这样才能逐条 resolve。

```bash
# 取 diff refs（inline 定位需要）
glab api "projects/:fullpath/merge_requests/<iid>" | jq .diff_refs

# 能落到 diff 内某一行的 finding → 带 position 的 discussion
glab api "projects/:fullpath/merge_requests/<iid>/discussions" -X POST \
  -f body="<问题 + 建议方向>" \
  -f position[position_type]=text \
  -f position[new_path]=<file> -f position[new_line]=<line> \
  -f position[base_sha]=<base> -f position[head_sha]=<head> -f position[start_sha]=<start>

# 落不到 diff 内的 finding（跨文件 / 漏改 / 本该有却没有的改动）→ 不带 position 的 discussion
glab mr note create <id> -m "<问题 + 建议方向>"
```

- 位置对不上时**不要硬塞 inline**，退回不带 position 的 discussion。
- 没发现问题也发一条 `No findings.`，让 `/fb` 有明确信号。
- 发完报告：MR 链接 + 发了几条带位置 / 几条不带位置。
- **review session 永远不改代码。**
