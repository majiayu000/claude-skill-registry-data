---
name: lalachan-story-improvement-loop
description: Use when a LALACHAN story needs repeated critique and revision cycles, especially 10-round polish, shareability repair, natural Chinese dialogue, Xiaoyunque story readiness, or running a Codex exec loop with gpt-5.5 xhigh.
---

# LALACHAN Story Improvement Loop

Use this skill when a story still feels strange, hard to understand, too
AI-like, not shareable, or not ready for video generation.

This skill extends the `lalachan-story-critic` rules. It is for repeated
improvement, not a single rewrite.

## Core Loop

Run the story through explicit rounds:

```text
draft -> exact problem list -> revised story -> next focus
```

Default to 10 rounds for important stories. Use fewer rounds only for tiny
repairs.

## Round Checklist

Use one main focus per round:

1. Story promise: what the audience expects to see.
2. Duration fit: 15s needs one joke; 30s can support setup, twist, payoff.
3. Causality: every event should be caused by an action or visible rule.
4. Character voice: each line must sound speakable by that character.
5. Dialogue read-aloud: remove translated, slogan-like, report-like lines.
6. Visual comedy: one memorable image people can retell.
7. Safety and credibility: dangerous actions need cartoon framing or setup.
8. Prop function: every prop gets one job or stays background.
9. Share hook: end with payoff or a clear next question.
10. Final compression: remove repeated explanations and prompt leakage.

## Failure Modes

Reject:

- abstract morals that characters would not say
- events connected only by `突然`
- too many props for the duration
- fake epic battle language for small jokes
- system-log robot dialogue
- prompt instructions inside the story text
- unclear physical actions that may render as unsafe

## Output Shape

For a documented loop:

```markdown
## Round N
Problem:
Change:
Result:
```

For a final deliverable:

```markdown
## Final Story
...

## Prompt Notes
...
```

Keep `Prompt Notes` separate from the story.

## Codex Exec Script

In the LALACHAN repo, use:

```bash
scripts/lalachan_story_improve_loop_codex.sh STORY.md --rounds 10
```

The script uses:

```text
model: gpt-5.5
reasoning effort: xhigh
```

It saves every prompt and result under:

```text
references/story-improvement-runs/
```

Use `--dry-run` to inspect prompts without spending model credits.
