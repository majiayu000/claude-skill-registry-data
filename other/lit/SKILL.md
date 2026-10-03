---
name: lit
description: "文献调研入库：检索论文、产出 notes/papers/<citekey>.md 结构化笔记并追加 lit/literature-log.md 索引。引用必须来自真实检索结果并附 DOI 或 arXiv ID。查文献、读某篇论文、找相关工作时用。"
argument-hint: "[主题，或论文 URL / DOI / arXiv ID]"
context: fork
background: false
allowed-tools: Read, Write, Edit, Glob, Grep, Task, WebSearch, WebFetch
---

# 文献调研入库

对象：$ARGUMENTS

本 skill 在隔离子上下文中运行：检索过程产生的大量原文不会污染主 context，
只有最终的笔记路径和几行摘要会回到主线程。

> 为什么显式写 `background: false`：Claude Code 2.1.x 起 `context: fork` 的 skill **默认后台运行**。
> 本 skill 的产出是给用户当场看的结构化摘要（入没入库、哪几篇、为什么不入），
> 后台跑会让这份摘要变成一条事后通知，用户当下拿不到判断依据，也就没法接着决定要不要读原文。
> 隔离 context 要保留，后台不要——所以 fork 保留、background 显式关掉。

## 第 1 步 检索

按顺序选工具，能用前面的就别用后面的：

1. **已配置的 MCP** —— `zotero`（本地库里可能已经有了，先查重）、
   `paper-search`、`semantic-scholar`。先看当前会话有哪些 MCP 工具可用。
2. **WebSearch / WebFetch** —— 没有 MCP 时用。搜到之后必须实际打开页面确认，
   不能只凭搜索结果摘要。

主题较宽（要一次覆盖 5 篇以上）时，派 `lit-reviewer` subagent 并行检索，
每个 subagent 负责一个子问题，回报「标题 + 年份 + DOI/arXiv ID + 三行摘要」。

传入的是 URL / DOI / arXiv ID 时跳过检索，直接取那一篇。

先在 `lit/literature-log.md` 和 `notes/papers/` 里查一遍，已经入过库的直接说明并停止，
不要重复写一遍笔记。

## 第 2 步 写笔记

路径 `notes/papers/<citekey>.md`。citekey 用 `作者姓+年份+首个实词`，全小写，如 `chen2024diffusion`。

````markdown
---
citekey: chen2024diffusion
title: <论文完整标题>
authors: [Chen Wei, Li Ming]
year: 2024
venue: NeurIPS 2024
doi: 10.48550/arXiv.2405.12345
tags: [diffusion-policy, manipulation]
status: read
read_date: 2026-07-22
---

## 核心问题
作者要解决什么。一句话说清，不要抄摘要。

## 方法
怎么做的。够我以后不重读原文也能复述的程度，但不要抄公式堆砌。

## 关键结论
- 论文报告的主要结果（带数字和数据集名）
- 消融里真正有信息量的那一两条

## 与本项目的关系
为什么把它入库。它支持 / 反对 / 补充了我们的哪个判断。
无关就不该入库——直接说不相关然后停。

## 可复用的点
- 具体到「哪个 trick 可以直接拿来用在哪个模块」
- 有官方代码就写仓库地址

## 存疑
- 实验设置里可疑的地方、结论外推得太远的地方
- 我没看懂、需要再确认的部分
````

`status` 取 `read` / `skimmed` / `queued`。只扫了摘要就写 `skimmed`，不要写 `read`。

## 第 3 步 更新索引

往 `lit/literature-log.md` 的表格追加一行。**列顺序是固定契约，照抄，不要自己排**：

```text
| citekey | 标题 | 年份 | 状态 | 与本项目的关系 | 笔记路径 |
| --- | --- | --- | --- | --- | --- |
| chen2024diffusion | <短标题> | 2024 | 精读 | <半句话，实质关联> | notes/papers/chen2024diffusion.md |
```

「状态」列用中文取值 `待读` / `略读` / `精读` / `已复现` / `已弃`，与笔记 frontmatter 的
`status` 对应：`queued`→待读，`skimmed`→略读，`read`→精读。**两边必须一致。**

一篇一行，只 append。文件不存在才新建（带表头）；已存在就只在表格末尾加行，不要重排既有行。

## 硬约束

1. **引用必须来自本次真实检索结果**，并且带 DOI 或 arXiv ID。没有标识符的条目不入库。
2. **严禁凭记忆生成 BibTeX、标题、作者、年份或页码。** 训练数据里的文献信息足够
   似是而非到骗过 review，这是本模板最不能容忍的一类错误。
3. 找不到就明说找不到：「检索了 <关键词>，在 <工具> 里没有找到匹配的论文」。
   不要给一个「大概是这篇」的猜测，也不要给凑出来的标题。
4. 数字（论文报告的指标）必须能指到原文的表/图编号，写进笔记时注明出处，如
   `(Table 3)`。记不清就不写。
5. 笔记里区分「论文说的」和「我的判断」。后者写在「存疑」和「与本项目的关系」里，
   并标 `[AI-DRAFT]`。

## 回到主线程时输出

只回报三样，别把检索原文带回去：

1. 新建/更新了哪些 `notes/papers/*.md`
2. 每篇一行：citekey + 与本项目的关系
3. 明确列出「检索了但没入库」的和原因（不相关 / 找不到全文 / 已存在）
