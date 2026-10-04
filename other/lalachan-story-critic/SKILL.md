---
name: lalachan-story-critic
description: Use when writing, revising, criticizing, or preparing LALACHAN/RaraXia/AyaChan/SasaKun stories, Xiaoyunque prompts, dialogue, scripts, or video story drafts, especially when the user says the story sounds strange, AI-like, unsmooth, too abstract, overpatched, hard to understand, or asks for a critic/quality pass before video generation.
---

# LALACHAN Story Critic

Use this skill before a story becomes a Xiaoyunque prompt, and whenever the user
says the writing feels strange or unnatural.

## Core Standard

The story should feel like a tiny cartoon scene, not a prompt or moral essay.

For 15s:

```text
setup -> small problem -> visible joke/payoff
```

For 30s:

```text
setup -> problem -> cooperation/twist -> payoff
```

Dialogue must sound speakable in normal Chinese. If a line sounds like a report,
translation, slogan, or AI explanation, rewrite it.

## Repeated Critique Loop

Never accept the first draft for a LALACHAN story. Run a critique loop before
showing or saving the final story:

1. Draft the scene in plain language.
2. Read every line of dialogue out loud mentally.
3. Mark anything that sounds like a slogan, report, translation, prompt, or
   forced-cute phrase.
4. Check that every event has a clear cause. Avoid using `突然` to glue unrelated
   events together.
5. Rewrite the weak lines and re-check.
6. Stop only when the story is easy to understand, characters sound distinct,
   and the joke/payoff is visible without explanation.

If the user asks for a story only, do this loop internally and return only the
polished story. If the user asks what is wrong, show the critique with exact
lines.

## Normal Language Rules

Use everyday phrasing first, then add one small cartoon exaggeration. Avoid
trying to make every sentence cute.

Bad patterns to reject:

- Forced-cute abstract phrases, such as `睡前勇气`, when a normal line like
  `我就吃了一小口饼干` works better.
- Pests, props, or background objects shouting slogans unless the whole scene
  clearly supports that joke.
- Sudden gadget magic with no setup. A character should pick up or use the prop.
- Fake anime battle lines for small daily-life problems unless the action is
  clearly slapstick.
- Robot lines that sound like system logs, status reports, or app messages.
- Decorative final text or props that do not pay off the story.

Use the simple test: would a normal person or a cute cartoon character actually
say this line out loud? If not, rewrite it.

## Critic Workflow

1. Read the draft story and prompt if available.
2. Separate story problems from Xiaoyunque technical prompt problems.
3. Quote the exact weak lines or phrases.
4. Name the failure mode.
5. Rewrite the line in a natural character voice.
6. Repeat the critique after rewriting if any line still sounds strange.
7. Only after the critique passes, produce a clean revised story or prompt.

Do not just say "make it warmer" or "more vivid". Point to the exact wording
that fails.

## Failure Modes To Check

- **Report voice**: words like `结论`, `本质`, `版本`, `意义`, `真正的`, `系统提示`
  used as dialogue.
- **Translated wording**: phrases that sound mechanically translated.
- **Prompt leakage**: visual/style instructions mixed into the story itself.
- **Weak causality**: events happen by `突然` with no action causing them.
- **Overloaded story**: too many props, concepts, or plot turns for the duration.
- **Theme lecture**: characters explain the lesson instead of showing it.
- **Voice blur**: 啦啦侠、阿芽酱、飒飒君、庄子 sound interchangeable.
- **Forced prop**: LightMind, notebook, words card, or robot appears with no job.
- **Unsafe lab action**: dancing or comedy touches sterile tools, culture dishes,
  pipettes, fume hoods, liquid nitrogen, or samples carelessly.
- **Overpatched prompt**: the prompt repeats constraints so much that the scene
  becomes buried.

## Character Voice Rules

- 啦啦侠: warm, brave after a silly misunderstanding, food-minded but not random.
- 阿芽酱: practical, observant, gentle correction, light teasing.
- 飒飒君: curious, impulsive, physical comedy, quick reaction.
- 庄子: precise, dry, cute, safety-minded; avoid long reports or slogans.

Bad:

```text
庄子：「结论：实验需要冷静，也需要一点点节奏。」
```

Better:

```text
庄子：「看来，做实验要静得下来，也要踩得准拍子。」
```

Bad:

```text
庄子：「我的手很稳，但跳舞的版本可能不太稳。」
```

Better:

```text
庄子：「我的手很稳，但跳舞嘛……不太行。」
```

## Prop Rules

Each visible prop should have one job:

- LightMind: notices a detail or warns about a small problem.
- Notebook: records a map, recipe, protocol, score, or clue.
- Words card: sits physically in the scene with one new word.
- 庄子 robot: precise hands, safety check, deadpan joke.

If a prop has no job, leave it as background or remove it from the story.

## Words Card Rule

Default reference image:

```text
$LALACHAN_ROOT/words-card.jpg
```

For each new story, choose a fresh word connected to the story. Include:

```text
English:
Japanese:
Furigana:
Chinese meaning:
```

The card is a physical desk prop, not a subtitle overlay.

## Lab Story Rule

For biological lab scenes:

- Keep the lab clean and credible.
- Use gloves, incubator, microscope, pipette, petri dish, and careful movement.
- Comedy can happen at the safe edge of the scene.
- Dancing should be tiny and away from samples or instruments.
- Do not imply careless contamination.

## Output Shape

When asked to critique:

```markdown
## Problems
- Exact line:
  Problem:
  Better:

## Revised Story
...

## Prompt Notes
...
```

When asked only for a final story, still run the critic pass internally and
produce the polished result.
