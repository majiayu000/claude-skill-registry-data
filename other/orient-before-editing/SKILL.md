---
name: orient-before-editing
description: Use at the start of any task in a large or unfamiliar codebase, before writing or editing code. Builds an accurate mental model first — read structure over full files, confirm the real current state instead of assuming it, time-box investigation, and carry the project's cross-module invariants — so the changes that follow are incremental and architecture-consistent instead of guess-driven rewrites.
---

# Orient Before Editing

The most expensive mistakes in a mature codebase happen before a single line is typed — an agent skims one file, assumes how the rest works, and rewrites something that was quietly encoding constraints it never saw. This skill is the orientation pass that comes *first*: build a correct mental model of the project, then change it. Four chapters, each a short list of tool-flow and hard constraints.

## Chapter 1 — Read the map before the territory

- **Read the head first.** Imports/exports, the function list, the switch-case router at the top of a file usually tell you what's inside. Read the full body only when the head doesn't answer your question.
- **Don't reflex-read long files end to end.** Reading a 600-line file to learn what a 15-line header would have told you is tokens spent for nothing.
- **Prefer structural search to blind opening.** One targeted `grep`/`glob` for a symbol, route, or call site often replaces three speculative file reads.
- **Map top-down.** Entry point → routing/dispatch → the module that owns the behavior. Start from the entry and follow the flow, not from a random leaf working upward.

## Chapter 2 — Confirm the current state before you change it

- **Observe, don't assume.** Read the actual current file (or ask for it) before proposing an edit. "The current state" is something you look at, never something you guess.
- **"Seems like" / "should be" means go read, not go type.** Those words are the signal that you don't actually know yet — resolve them with a read, not with a rewrite.
- **Prefer the smallest diff over a rewrite.** A rewrite silently discards the invisible constraints the existing code was encoding. Change incrementally so those constraints survive.
- **Surface contradictions.** If the file contradicts how it was described to you, say so before proceeding — don't quietly paper over the mismatch.

## Chapter 3 — Time-box your investigation

- **Two calls to decide "exists or new?"** To answer "does this already exist / do I need to build it," cap yourself at ~2 tool calls — one structural search plus one confirming read — then decide.
- **Stop once you have the answer.** Don't spider out into "who else references this," "what's the blast radius," "how do other pages use it" unless the task actually needs it.
- **Widening scope is the user's call, not a drift.** When it's ambiguous whether to look wider, state what you found and ask — don't burn ten more searches on a guess.

## Chapter 4 — Hold the project's invariants in your head

- **Every mature project has cross-module invariants** — a canonical format for time, for money, for identity/permission derivation, for API return shape. New code must conform, or it breaks coordination between modules that never see each other's source.
- **Find the one source of truth before writing.** Grep for the canonical helper (the shared time-normalizer, the money-conversion util, the auth-derivation function) and reuse it. Re-implementing it locally is how two modules drift apart.
- **New code obeys the standard; legacy is reconciled at the boundary.** Don't retro-fit existing data to a new invariant unless asked — normalize at the read/export layer instead of rewriting stored data in place.
- **These invariants are exactly what one file can't tell you** — which is the whole reason you read the map (Ch. 1) before touching anything.

## The principle

Orientation is not overhead you skip to move faster — it *is* the fast path. The rewrite you avoid because you read the header, and the module you didn't break because you knew its invariant, cost less than any investigation that surfaced them.

---

> Adapt, don't copy-paste. This is the shape of the idea, not a config to drop in verbatim — the concrete invariants (which formats are canonical, how deep your investigation should go) come from your own project's actual conventions and failure patterns.

---

<details>
<summary><b>中文版</b>(点击展开)</summary>

# 进场:先建完整心智模型

成熟代码库里最贵的错误,往往在敲下第一行代码之前就已经犯了——扫了一个文件,就假设其余部分怎么运作,然后重写了一段其实在默默承载着它根本没看到的约束的代码。这个 skill 就是**排在最前面**的那一步进场:先建立起对项目正确的心智模型,再去改它。四个 chapter,每个都是一小串工具流程 + 硬约束。

## 第一章:先读地图,再读地形

- **先读文件头。** 顶部的 require/exports、函数列表、switch-case 路由,通常就告诉你里面有什么。头部答不上你的问题,再去读全文。
- **别反射式地全文读长文件。** 为了搞清一个 15 行头部就能告诉你的事去读 600 行,是纯浪费 token。
- **结构性搜索优先于盲目打开。** 对某个符号/路由/调用点做一次精准 `grep`/`glob`,往往顶得上三次靠猜的文件读取。
- **自顶向下建图。** 入口 → 路由/分发 → 拥有该行为的模块。从入口顺着流程走,别从某个随机的叶子往上倒推。

## 第二章:先搞清现状,再动手改

- **要观察,别假设。** 提议改动前,先读到真实的当前文件(或索要它)。"现状"是拿来看的,永远不是拿来猜的。
- **"好像"/"应该"意味着去读,不是去敲。** 这两个词就是你其实还不知道的信号——用一次读取去消除它,而不是用一次重写。
- **最小 diff 优先于重写。** 重写会悄悄丢掉现有代码承载着的、看不见的约束。增量地改,让这些约束存活下来。
- **把矛盾摆出来。** 如果文件跟别人给你的描述对不上,先说出来再往下走,别默默把这个不一致糊过去。

## 第三章:给调研设边界

- **判断"已存在还是新建"最多 2 次调用。** 要回答"这个是不是已经有了/要不要新建",给自己封顶 ~2 次工具调用——一次结构性搜索 + 一次确认读取——然后就下结论。
- **拿到答案就停。** 除非任务真的需要,别继续铺开去查"还有谁引用它""影响面多大""别的页面怎么用它"。
- **扩大范围是用户的决定,不是你的漂移。** 当"要不要查更宽"本身模糊时,把你查到的摆出来问一句——别靠猜再烧十次搜索。

## 第四章:心里装着项目级不变量

- **每个成熟项目都有跨模块不变量**——时间的统一格式、金额的统一格式、身份/权限的派生方式、接口返回的口径。新代码必须遵守,否则就会打断那些彼此看不到对方源码的模块之间的协同。
- **动手前先找到唯一真源。** grep 出那个金标准 helper(统一的时间归一函数、金额换算工具、身份派生函数)并复用它。在本地重新实现一份,正是两个模块开始漂移的起点。
- **新代码遵守标准;存量在边界层兜。** 除非有要求,别把存量数据回迁到新不变量上——在读取/导出层归一,而不是就地重写已落库的数据。
- **这些不变量恰恰是单个文件告诉不了你的**——这正是你为什么要先读地图(第一章)再动任何东西的原因。

## 核心原则

进场理解不是为了跑得更快而砍掉的额外开销——它**本身**就是那条快路。因为读了头部而避开的那次重写、因为知道了不变量而没被你打断的那个模块,省下的都比任何把它们暴露出来的调研更值。

---

> 别照搬,自己微调。这里给的是思路的骨架,不是一份可以直接粘贴进项目的配置——具体的不变量(哪些格式是金标准、调研该查到多深)来自你自己项目里真实的约定和踩过的坑。

</details>
