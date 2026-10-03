---
name: social-text-websense-gate
description: Use when drafting, reviewing, or revising Xiaohongshu/Douyin/social-platform Chinese text so it has real internet-native judgment instead of README tone, technical-briefing tone, or mechanical meme-word stuffing.
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  trigger: 小红书/抖音/社交平台标题、正文、图文文案、caption、评论引导的网感闸门
  source: local
---

# Social Text Websense Gate

## Purpose

This skill is a **text taste gate** for social-platform Chinese copy. It does not publish, scrape, score, or render visuals. It helps the content role decide whether a draft sounds like a real internet-native person reacting to a concrete situation, or like an editor packaging a methodology.

The core rule:

```text
网感来自荒谬点识别，不来自网络词密度。
```

Words like `疑似`、`绷不住`、`抽象`、`这娃` can appear naturally, but they are not the goal. If the copy mechanically stuffs those words without finding the actual absurdity, it still fails this gate.

## When To Use

Use this skill when working on:

- Xiaohongshu / Rednote titles, body copy, carousel text, captions, or comment prompts.
- Douyin titles, captions,图文正文,口播开头, or short social text.
- Tech-social posts about AI coding, Agents, Codex, Skills, workflow, GitHub repos, tool failures, non-CS product building, or automation.
- A user says the copy is `太正经`, `像编辑`, `像 README`, `没网感`, `像 AI`, `像发布会`, or `不是经常冲浪的人`.
- A draft is factually right but scroll-stopping power is weak.

Do **not** use it as a replacement for:

- `humanizer-zh`: general anti-AI-writing cleanup.
- `cheat-on-content`: scoring, blind prediction, publishing registration, and retro.
- `xhs-publish-assistant`: final copy-ready publish bundle.
- Fact checking. This skill can make copy sharper, but cannot invent facts.

## Default Sequence

For social-platform tech copy, default to this order:

```text
处境 / 情绪 / 自嘲
→ 真实事故感
→ 技术锚点
→ 仓库 / 方法 / 试用 / 反驳入口
```

Do not open with macro claims like:

```text
AI Agent 工作流正在成为新的生产力范式。
提示词不够用了，Skill 才是资产。
普通人必须掌握 AI 时代的底层逻辑。
```

Those may be true, but on Xiaohongshu/Douyin they often feel like a technical briefing. Start with the human friction instead.

## The Websense Test

Before editing, answer these questions:

1. **What is the concrete situation?** Who is tired, annoyed, tempted, confused, or being made responsible?
2. **What is the absurd point?** What exactly is funny, annoying, or screenshot-worthy?
3. **What is the technical anchor?** Which real tool, behavior, script, workflow, boundary, or failure mode keeps the joke grounded?
4. **What is the human relationship?** Is the tool helping, over-helping, replacing, exposing, embarrassing, or dumping responsibility back on the person?
5. **What action should the reader take?** Save, comment, try the repo, ask for the script, argue, or go test it.

If you cannot answer #2, do not add internet words. Find the absurdity first.

## Rewrite Patterns

### 1. Absurd action + plausible annoying excuse

Good social copy often shows an AI/tool doing something over-free, then gives it a painfully reasonable excuse.

Weak:

```text
Codex 有时候会乱改项目。
```

Stronger:

```text
你让它修一个按钮，它把半个项目翻新，然后跟你说遵循一致性设计。
```

Transfer pattern:

```text
你让它做 A，它反手做 B，然后给一个听起来很合理但很欠揍的理由。
```

More examples:

```text
你让它删一段废代码，它顺手整理了整个目录结构，然后说这是降低复杂度。
你让它看一眼报错，它开始讲技术选型的历史沿革。
你让它写个测试，它把测试写成了对业务逻辑的哲学批判。
```

### 2. Do not describe the persona; show what the tool did to that person

Weak:

```text
我是一个有很多想法但很累的程序员。
```

Stronger:

```text
轻松干翻我这种有无数想法、但被上班榨到一行代码都不想写的技术中登。
```

The second line works because it defines a relationship: the tool has more energy than the person who is supposed to control it.

### 3. Translate technical mechanics into human situations

Weak:

```text
我们需要为 Agent 增加边界和校验机制。
```

Stronger:

```text
自由到我想给它办入职、配工牌、安排直属领导。直属领导不是我，是那个校验脚本。
```

Use the human scene to carry the technical anchor. Do not hide the anchor; bury it in the joke.

### 4. Keep the repo/method call-to-action dirty enough to feel real

Weak:

```text
欢迎体验我的开源工作流项目。
```

Stronger:

```text
请大家的大 Codex 狠狠抽打我的小 skill。有用就 star，没用就来骂，我正好修。
```

The call-to-action should feel like a real builder asking for stress, not a brand account asking for engagement.

## Bad Patterns

### README tone

```text
本项目基于角色化 Agent 工作流，提供可复用的任务拆解与质量控制能力。
```

Why it fails: technically clear, socially dead. Move the technical claim after a concrete situation.

### Technical launch-event tone

```text
我们正在从 prompt 时代走向 skill 时代。
```

Why it fails: it starts from trend commentary instead of reader friction.

### Meme-word stuffing

```text
Codex 疑似抽象，绷不住了，这娃太离谱。
```

Why it fails: the words gesture at internet culture but do not reveal a specific absurdity.

### Sterilized safety rewrite

```text
需要注意的是，不同工具在不同项目中的表现存在差异，建议结合自身情况谨慎使用。
```

Why it fails: it may be safe, but it kills the social post. Keep factual boundaries in the background; do not open like a production announcement unless the topic requires it.

## Review Checklist

Before returning social-platform text, check:

- [ ] The first screen has a human situation, not a macro trend.
- [ ] The draft identifies a specific absurdity.
- [ ] At least one line could plausibly be screenshot and sent to a group chat.
- [ ] The technical anchor is real and not blurred by the joke.
- [ ] Internet words are not used as a checklist.
- [ ] The copy does not sound like README, launch notes, or a platform announcement.
- [ ] The self-mockery lands on a concrete group or state, not generic `我很累`.
- [ ] The ending gives a clear reader action: try, save, comment, argue, test, or visit the repo.

## Output Modes

When asked to revise a draft, use one of these modes:

### Gate report

```md
## 结论
通过 / 需要重写 / 只需小修

## 最大问题

## 最该保留

## 重写方向

## 可直接替换句
```

### Rewrite only

If the user asks for direct copy, return only the revised copy. Do not add title pools, hashtags, visual notes, or publishing advice unless asked.

## Common Pitfalls

1. **Turning websense into a word list.** If a prompt says `多用疑似/绷不住/抽象`, correct it: those words are optional byproducts, not the target.
2. **Polishing away the weirdness.** Some roughness is the asset. Do not upgrade every line into a clean methodology sentence.
3. **Forgetting the technical anchor.** A funny line without the real tool behavior becomes generic meme content.
4. **Over-explaining before the hook lands.** Social copy earns explanation after it creates recognition.
5. **Pretending platform taste is universal.** This gate is for social text. Long-form WeChat, docs, README, and investor/legal/medical copy need different tone.
