---
name: content-style-calibration-loop
description: Use when a user edits or criticizes generated copy and you need to extract durable writing-style rules instead of merely remembering surface words.
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  trigger: 用户手改文案、说不像我、太正经、太编辑、没网感、太 AI、需要把风格反馈沉淀成 skill/reference
  source: local
---

# Content Style Calibration Loop

## Purpose

This skill turns user edits into reusable style rules. It prevents the agent from doing the shallow version of learning:

```text
用户用了几个词 → 下次多塞这几个词
```

The correct goal is:

```text
用户改了什么关系、视角、节奏、风险边界或人群钉子 → 下次按这个写作判断工作
```

Use this skill after the user edits generated text, rejects a tone, or says a draft does not sound like them.

## When To Use

Use it when the user:

- edits a model-written paragraph and asks you to learn the style;
- says `不像我`, `太编辑`, `太 AI`, `太正经`, `太抽象`, `没网感`, `像 README`, or `像发布会`;
- distinguishes between a surface feature and the real rule, e.g. `不是多用这些词，是要有网感`;
- wants the lesson added to a skill, reference, README, or workflow;
- is calibrating a recurring content voice for Xiaohongshu, Douyin, WeChat, scripts, captions, or other public copy.

Do not use it to preserve raw private conversations. Extract rules, not transcripts.

## Calibration Workflow

### 1. Capture the before/after pair

Get the model draft and the user-edited version. If the original is not available, still analyze the user edit, but mark the missing comparison.

Completion criterion: you can point to at least one changed phrase, deleted structure, or added line.

### 2. Diff meaning, not just wording

Classify each important change:

| Change type | Question |
| --- | --- |
| Voice | Did the user make it rougher, sharper, calmer, more local, more personal? |
| Viewpoint | Did the user move from expert explanation to participant experience? |
| Relationship | Did the user show what the tool/project does to a person? |
| Specificity | Did the user replace generic terms with an incident, object, role, or scene? |
| Rhythm | Did the user shorten, fragment, add breath, or keep a deliberate rough edge? |
| Risk boundary | Did the user remove over-cautious disclaimers or add factual anchors? |
| Platform fit | Did the user make it more suitable for XHS/Douyin/WeChat/etc.? |

Completion criterion: every accepted user edit is mapped to at least one reason.

### 3. Extract rules, not word lists

Bad extraction:

```text
User likes 疑似、绷不住、抽象.
```

Better extraction:

```text
User wants high-intensity internet-native judgment: identify the absurd point in a real situation, then say it with half-joke/half-accurate technical self-mockery. Internet words may appear, but should not be forced.
```

Completion criterion: the rule would still work if none of the original words were reused.

### 4. Keep the strongest examples

Store 1-3 compact before/after examples or pattern examples. Do not store entire chat logs, platform metrics, credentials, personal directories, or private context.

Completion criterion: each example demonstrates a rule and is safe to publish or share.

### 5. Decide the destination

Use the smallest durable destination that will affect future behavior:

| Lesson type | Destination |
| --- | --- |
| User preference that should follow all sessions | memory / user profile |
| Account-specific writing style | account style guide or content repo reference |
| Reusable agent procedure | skill |
| One-off task state | session notes or current repo files, not memory |
| Raw operational data | operations repo only, not public skills |

Completion criterion: the lesson is stored where the next relevant agent/tool can read it.

### 6. Verify the next prompt can use it

Write a tiny future-use prompt fragment, for example:

```text
Use the calibrated style rule: websense comes from identifying the absurd point, not stuffing meme words. Keep technical anchors real, but open with the human friction.
```

Completion criterion: the prompt fragment is specific enough to change a future draft.

## Output Format

When reporting a calibration result, use:

```md
# 风格校准结论

## 1. 用户改动

## 2. 改动背后的规则

## 3. 下次写作要做

## 4. 下次写作不要做

## 5. 可沉淀位置

## 6. 已沉淀 / 待用户确认
```

Keep it short. The goal is not literary analysis; the goal is future behavior change.

## Example

User changes:

```text
我就是那个有无数想法、但被上班榨到一行代码都不想写的技术中登。
```

into:

```text
轻松干翻我这种有无数想法、但被上班榨到一行代码都不想写的技术中登。
```

Do not extract:

```text
Use the phrase 技术中登 more.
```

Extract:

```text
Do not merely introduce the persona. Show the power relationship: the tool/AI/project has so much energy that it embarrasses, replaces, overwhelms, or exposes the person who was supposed to control it.
```

## Public-Skill Hygiene

When turning a private calibration into a public skill:

- Keep general rules and safe examples.
- Remove platform backend data, engagement metrics, account IDs, session IDs, local paths, cron IDs, cookies, screenshots, and raw comments.
- Do not quote large private conversation chunks.
- Do not publish a user's personal biography unless they explicitly made it part of the public account voice.
- Prefer `user-edited sample` / `confirmed style sample` wording over private chat provenance.

## Common Pitfalls

1. **Learning the vocabulary instead of the judgment.** If the user says `不是这些词，是网感`, immediately rewrite the rule around judgment.
2. **Overfitting one post.** A high-performing post gives a hypothesis, not universal law. Record it as a style pattern to test.
3. **Saving too much.** Skills should contain compact rules and examples, not raw drafts, raw chats, or platform data dumps.
4. **Skipping verification.** A calibration is not complete until it produces a prompt fragment, checklist item, or skill/reference update that future agents can actually use.
5. **Letting the editor override the user.** The agent may explain why an edit works, but the user's taste is the final style signal for their own account.
