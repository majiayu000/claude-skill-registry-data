---
name: ljg-word-flow
description: "Word flow: deep-dive word analysis + infograph card in one go. Takes one or more English words, runs ljg-word (generates deep semantics analysis) then ljg-card -i (generates infograph PNG). Use when user says '词卡', 'word card', 'word flow', or provides English words wanting both analysis and visual card."
user_invocable: true
version: "1.0.1"
---

# ljg-word-flow: 词卡

一条命令完成：解词 → 铸信息图。支持多词并行。

## 模式

**强制 NATIVE 模式。** 本 workflow 是纯 skill 管道（ljg-word → ljg-card -i），不需要 Algorithm 的七步流程。直接按下方执行步骤调用 skill，不走 OBSERVE/THINK/PLAN/BUILD/EXECUTE/VERIFY/LEARN。

## 参数

直接传入一个或多个英文单词，空格分隔。

```
/ljg-word-flow Obstacle
/ljg-word-flow Serendipity Resilience Entropy
```

## 执行

### 1. 收集单词列表

从用户消息中提取所有英文单词。

### 2. 处理每个单词

对每个单词，串行执行两步：

**步骤 A — 解词（ljg-word）：**

调用 Skill tool 执行 `ljg-word`，传入单词。在对话中输出 Markdown 解析结果。

**步骤 B — 铸信息图（ljg-card -i）：**

以步骤 A 的解析内容为输入，调用 Skill tool 执行 `ljg-card -i`。生成 PNG 文件到 `~/Downloads/`。

### 3. 多词并行

多个单词时，每个单词启动一个 Agent subagent 并行处理（每个 subagent 内部 A→B 串行）。

### 4. 汇总报告

```
════ 词卡完成 ═══════════════════════
📖 {Word1}
   🖼️ ~/Downloads/{Word1}.png

📖 {Word2}
   🖼️ ~/Downloads/{Word2}.png
...
```

## 关键约束

- 先解词后铸卡，顺序不可逆
- ljg-word 和 ljg-card -i 各自的质量标准不变
- 信息图内容来自解词结果，不是字典释义
