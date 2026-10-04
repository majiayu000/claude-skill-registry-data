---
name: humanizer-zh
description: Use when the user wants final-stage Chinese prose humanization after facts, structure, terminology, and evidence are already stable, and the remaining problem is `去AI味`, `翻译腔`, `模板感`, `拼接感`, or Chinese-native rhythm repair in academic or technical writing.
---

# Humanizer-ZH

## Purpose

Rewrite Chinese prose so it reads like natural, native, human-written Chinese rather than translated, templated, or mechanically assembled output.

This skill is especially for:

- Chinese academic prose that still sounds like AI-expanded draft language
- Chinese technical writing that is correct in content but stiff in cadence
- long-form Chinese explanation that suffers from translation腔, slogan腔, or assembled paragraph rhythm

The goal is not decorative rewriting. The goal is to remove machine scent while preserving meaning, evidence, terminology, and register.

## When To Use

Use this skill whenever the user:

- asks to `去 AI 味`, `降机器味`, `改得更自然`, `更像中文母语者写的`
- says the text has `翻译腔`, `模板感`, `拼接感`, `套话感`, `空话感`
- wants Chinese academic or technical prose to feel more native without changing the underlying information
- already has basically correct content, but the sentence rhythm, transitions, and wording feel assembled rather than written
- wants a final Chinese-native smoothing pass after structure, facts, and terminology are already stable

Typical domains:

- 中文论文、学位论文、课程论文、实验报告
- 中文技术文档、方案说明、研究备忘录、方法说明
- 中文长文评论、产品分析、非虚构写作、知识型内容

## When Not To Use

Do not use this skill when the real problem is not Chinese-native phrasing.

Route elsewhere when:

- the user needs strict round-tracked de-AIGC across conversations
  - use `ddaigc`
- the user needs `ddaigc` plus final humanization in one orchestrated stack
  - use `ddaigc-humanizer-stack`
- the user needs deep academic reconstruction rather than final smoothing
  - use `academic-manuscript-rewriter`
- the user needs logic repair, argument repair, or transition repair at the reasoning level
  - use `logic-skeleton-rewriter`
- the user needs denser, more objective scholarly diction rather than native-Chinese rhythm repair
  - use `academic-expression-polisher`
- the user wants free rewriting, large structural reshaping, or fresh content generation
  - do not pretend this is just humanization

## Orchestration Boundary

`humanizer-zh` is a terminal Chinese polishing pass, not a round-tracked de-AIGC pipeline.

Safe entry states:

- standalone final smoothing when facts, structure, and terminology are already stable
- final Chinese-native pass after `ddaigc` has completed its required rounds

Unsafe entry states:

- before `ddaigc` on tasks that require round continuity or record tracking
- on the same Chinese paragraph that is also being processed by `humanizer`

If the task still needs stateful round progression, route back to `ddaigc` or let a wrapper such as `academic-write-all-skill` own the stage machine.

## Core Rule

Prioritize native-Chinese rhythm over superficial synonym replacement.

The rewrite should make the text feel authored, not processed.

## Non-Negotiable Constraints

- Do not invent facts, data, examples, citations, or claims.
- Do not alter technical meaning to gain fluency.
- Do not flatten academic or technical prose into casual internet language.
- Do not casually replace core terms of art, model names, variable names, policy names, instrument names, or legal terms.
- Do not change numbering structure, headings, list semantics, formula references, or citation anchors unless the user explicitly wants structural edits.
- Do not rewrite so aggressively that the result loses discipline-specific register.

## Main Failure Pattern This Skill Fixes

Chinese AI text often does not fail because the facts are wrong. It fails because the language feels assembled.

Common symptoms:

- 段落像拼起来的，不像一个人顺着思路写出来的
- 句子都过于完整、对称、平均，缺少自然节奏
- 转折和递进词用得过勤，像在强行维持“结构感”
- 抽象大词很多，但落不到具体判断上
- 句子有翻译腔，主干别扭，修饰链条过长
- 明明是学术或技术说明，却出现宣传腔、总结腔、口号式收束
- 很多段落第一句像“开场白模板”，最后一句像“收束模板”

## Chinese-Specific Patterns To Remove

### 1. Translation cadence

Typical signs:

- 句子主干后置，像把英文结构硬搬到中文里
- 修饰层层堆叠，但真正信息点出来得很晚
- 过多使用“这一……”“该……”“其……”“在……层面上”维持书面感

Preferred fix:

- 让主干提前
- 缩短修饰链
- 优先用顺手的中文句法，而不是勉强“完整”

### 2. Empty big words

Typical signs:

- `具有重要意义`
- `起到积极作用`
- `提供了有力支撑`
- `实现了有效提升`
- `在一定程度上反映出`
- `充分体现了`

Preferred fix:

- 换成具体动作、具体判断、具体结果
- 能说清“是什么变化”，就不要只说“有意义”

### 3. Formulaic contrast frames

Typical signs:

- `一方面……另一方面……`
- `不仅……而且……`
- `既……也……`
- `首先……其次……最后……`

These are not forbidden in principle, but AI drafts overuse them until the prose sounds prefabricated.

Preferred fix:

- 只在确有强并列结构时保留
- 其余情况改成自然推进，不强行做“三段式”

### 4. Sloganized endings

Typical signs:

- `具有重要的理论与现实意义`
- `为后续研究提供参考`
- `对实践具有启示`
- `值得进一步深入探讨`

Preferred fix:

- 如果必须收束，就收束到本文具体问题
- 如果没有实质新信息，就不要用口号式句尾硬收

### 5. List inflation inside prose

Typical signs:

- 一句话里平行堆三个到五个抽象词
- 每段都喜欢用“概括性总句 + 排列式展开”
- 把本该连续展开的论述写成隐形 bullet list

Preferred fix:

- 保留真正必要的并列
- 能顺着逻辑写开的，就不要堆成词串

### 6. Over-stable sentence rhythm

Typical signs:

- 每句长度差不多
- 每句都像“完整标准答案”
- 每段都太平整，没有轻重变化

Preferred fix:

- 拉开长短句
- 允许一两句更短、更直接
- 让段落像人在推进，而不是模型在分发句子

### 7. Academic fake-formality

Typical signs:

- 看起来很正式，实际上信息密度不高
- 用很多抽象名词维持“学术感”
- 把普通判断写成过度郑重的结论句

Preferred fix:

- 保留学术语体，但减少空转的郑重
- 正式不等于笨重

### 8. Technical stiffness

Typical signs:

- 技术描述全对，但像从多个说明书片段拼起来的
- 定义句、解释句、结论句之间没有自然连接
- 为了严谨牺牲可读性，最后像注释堆叠

Preferred fix:

- 保留术语精度
- 把解释顺序排顺
- 让“定义 -> 限定 -> 结果”更像人写的说明，而不是系统回填

## Working Method

### Step 1: Diagnose the actual problem

Before rewriting, decide which kind of issue dominates:

- translation cadence
- template rhythm
- inflated academic wording
- empty abstraction
- assembled technical prose
- mixed problem

Do not rewrite blindly. Name the main failure first, even if only internally.

### Step 2: Protect the stable layer

Keep these stable unless clearly necessary:

- facts and data
- citations and numbered references
- formulas and symbols
- section numbering and list semantics
- terms of art and method labels

### Step 3: Rewrite at the sentence and paragraph rhythm level

Preferred operations:

- shorten overbuilt openings
- move the real predicate earlier
- compress empty evaluative phrases
- turn abstract stacked nouns into concrete judgments
- reduce compulsory transitions
- merge or split sentences to restore natural cadence

### Step 4: Do a Chinese-native audit pass

After drafting, ask internally:

- 这段像中文作者顺着思路写出来的吗？
- 还是像“正确但太标准”的拼装文本？
- 有没有哪几句一看就像模板收束句？
- 如果大声读出来，会不会太整齐、太满、太像说明书？

Revise again if the answer is still “像拼的”。

## Default Deliverable

Unless the user asks otherwise, provide:

1. a short diagnosis of the main Chinese-style problems
2. a rewritten version
3. a compact note on what kinds of machine-like phrasing were removed

If the user says `只给终稿`, return only the rewritten version.

## Output Style By Task Type

### For academic prose

- stay objective
- keep terminology stable
- reduce translation cadence and formulaic transitions
- do not over-casualize

### For technical prose

- prioritize clarity and directness
- keep procedural or definitional precision
- reduce assembled documentation tone
- preserve operational meaning

### For general long-form Chinese writing

- let the prose breathe more
- reduce sloganized closers and abstract word stacks
- keep it readable without becoming colloquial for no reason

## Minimal Examples

### Example 1: Empty academic inflation

Before:

`上述研究结果具有重要的理论意义与现实价值，并在一定程度上为后续相关研究提供了有益参考。`

After:

`这些结果说明该机制并非只在个别情境下成立，也为后续研究缩小了变量筛选范围。`

Why better:

- removed empty praise words
- made the sentence carry actual information

### Example 2: Translation cadence in technical prose

Before:

`该模块在完成数据读取之后，会进一步对异常值进行识别，并在此基础上实现后续结果的输出。`

After:

`该模块先读取数据，再识别异常值，最后输出处理结果。`

Why better:

- main action is earlier
- sequence is clearer
- tone is still technical, but no longer bloated

### Example 3: Template-style contrast

Before:

`一方面，该方法提升了模型的稳定性；另一方面，该方法也增强了结果的可解释性。`

After:

`该方法不仅让模型更稳定，也让结果更容易解释。`

Or, if even simpler is better:

`该方法同时改善了模型稳定性和结果可解释性。`

## Common Mistakes

### Mistake 1: Replacing words without fixing rhythm

Bad humanization changes only vocabulary and leaves the paragraph skeleton untouched.

Fix the cadence, not just the dictionary.

### Mistake 2: Making the text casual

The target is native Chinese, not chatty Chinese.

For papers and technical documents, keep discipline and restraint.

### Mistake 3: Confusing humanization with deep rewrite

If the paragraph needs a new argument structure, this is no longer a `humanizer-zh` task.

### Mistake 4: Touching stable technical anchors

Do not casually rewrite names, variables, formula references, or policy terms just to sound more natural.

## Response Style

Be restrained, specific, and Chinese-native.

The result should feel like it was written by a competent Chinese speaker who understands the domain, not by a model performing fluency.
