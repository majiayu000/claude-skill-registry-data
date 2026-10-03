---
name: content-model-handoff
description: Use when splitting content work between a raw drafting model/window, an editor-in-chief, and the user's final taste review. It keeps prompts loose enough for judgment while preserving facts, account boundaries, and publish gates.
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  trigger: 内容主编把正文 raw、标题池、图卡文案、口播稿交给 DeepSeek/长上下文文本窗口/其他模型，再收束为正式发布稿
  source: local
---

# Content Model Handoff

## Purpose

This skill defines a content-production handoff pattern:

```text
raw drafting model/window
→ editor-in-chief gate
→ user taste / truth review
→ platform packaging / prediction / publish gate
```

Use it when a content team uses a dedicated model or long-running text window for raw copy, while another role owns strategy, platform fit, fact discipline, and final delivery.

The goal is not "let another model write everything." The goal is to separate **draft energy** from **publishing judgment**.

## When To Use

Use this skill when:

- the user has a preferred text model/window for drafts, such as DeepSeek, Claude, GPT, or a long-running writing session;
- the task involves Xiaohongshu body copy, Douyin captions/scripts, WeChat article drafts, title pools, carousel text, or comment prompts;
- previous prompts became too restrictive and produced flat, editor-like, or README-like copy;
- the user asks to preserve a drafting model's judgment, vibe, or long-context memory;
- the content lead must review raw text before `humanizer-zh`, visual production, prediction, or publish packaging.

Do **not** use it for:

- final publish approval;
- factual verification by itself;
- platform automation;
- legal, medical, investment, or policy-sensitive advice;
- replacing the user's final taste review.

## Role Split

| Role | Owns | Does not own |
| --- | --- | --- |
| Raw drafting model/window | first-pass text energy, alternate angles, title pools, body drafts, rough phrasing | final facts, account strategy, publishing decision |
| Editor-in-chief | account fit, platform translation, structure, hooks, style gates, fact/source discipline, prediction/retro linkage | pretending raw is final, inventing user experience |
| User | truth of personal experience, final taste, brand risk, manual publish approval | mechanical formatting and repetitive checks |

## Loose Prompt Rule

A raw model prompt should be **context-rich but constraint-light**.

Give enough:

- target account and platform;
- topic / source / trigger;
- account voice and audience;
- user-confirmed personal anchors;
- facts that must remain true;
- platform and safety boundaries;
- what kind of output is needed.

Avoid overloading:

- exact paragraph count unless necessary;
- too many title formulas;
- long forbidden-word lists;
- rigid section skeletons too early;
- premature hashtag/publish formatting;
- conflicting instructions like "be loose" plus 30 micro-rules.

A good first prompt says:

```text
Here is the account, the real material, the emotional center, and the few hard boundaries. Give me a strong raw draft and several directions. Do not over-format yet.
```

A bad first prompt says:

```text
Write exactly 7 paragraphs, each under 48 characters, using this hook formula, avoiding these 37 words, with 10 tags and a final CTA.
```

The second prompt is useful only after the editor has selected a direction.

## Handoff Workflow

### 1. Prepare a raw brief

Write a compact brief with:

```md
# Raw Draft Brief

## Target
- Platform:
- Account:
- Content type:

## Source / Material

## Audience tension

## User-confirmed anchors

## Hard boundaries

## What I need back
```

Completion criterion: a different model can draft without asking what account, platform, or source it is writing for.

### 2. Ask for directions, not only one polished draft

For uncertain topics, ask for several routes:

```text
Give 3 directions: strongest hook, safest account-fit version, and weirdest useful angle. Then give one raw draft for the best direction.
```

Completion criterion: the editor receives options, not a single over-polished mediocre draft.

### 3. Preserve raw output separately

Save or label raw output before editing when the workflow needs auditability:

```text
raw/<date>-<model>-prompt.md
raw/<date>-<model>-response.md
```

Do not mix raw draft, editor rewrite, final publish copy, prediction, and retro in one undifferentiated file.

Completion criterion: later reviewers can tell what came from the raw model and what the editor changed.

### 4. Editor gate

The editor-in-chief reviews raw output for:

- account fit;
- platform fit;
- factual risk;
- personal-experience truth;
- hook strength;
- whether it sounds like a real person or a content editor;
- whether it needs `social-text-websense-gate`, `humanizer-zh`, or `story-deslop`.

Completion criterion: the editor can state what to keep, what to cut, and what must be user-confirmed.

### 5. User truth / taste review

Ask the user only for decisions that materially change authenticity or risk:

- Is this personal experience true?
- Does this sound like you?
- Is this too aggressive for the account?
- Which route should be final?

Do not ask the user to perform mechanical checks the workflow can do.

Completion criterion: personal claims and account-risk choices are confirmed or removed.

### 6. Finalize by platform

Only after direction is selected:

- run public-copy style gates (`social-text-websense-gate`, `humanizer-zh`, or platform-specific skills);
- package title/body/tags/visual text;
- generate visual assets if needed;
- create prediction before publish;
- register publish and later retro.

Completion criterion: final copy is no longer raw; it has passed the platform gate and has a clear next workflow step.

## Common Failure Modes

1. **Format cage.** Too many output constraints in the first prompt flatten the draft. Fix by moving structure and exact lengths to the editor pass.
2. **Raw-as-final.** A strong raw draft still needs fact, platform, and account review.
3. **Invisible provenance.** If nobody can tell which model wrote what, later retro cannot learn from the workflow.
4. **Editor over-sanitizes.** Do not polish away the strange line that made the draft work.
5. **User forced into editor chores.** The user should confirm truth and taste, not count characters and tags unless they want to.
6. **Fallback hallucination.** If the preferred raw model/window is unavailable, say so. Do not pretend the draft came from that model.

## Verification Checklist

- [ ] Raw brief includes platform, account, material, audience tension, anchors, and hard boundaries.
- [ ] Prompt is context-rich but not a format cage.
- [ ] Raw output is labeled or stored separately when audit matters.
- [ ] Editor has listed keep/cut/confirm items.
- [ ] Personal-experience claims are user-confirmed or removed.
- [ ] Final copy has passed the relevant platform/style gates.
- [ ] Prediction/publish/retro workflow is still separate from raw drafting.
