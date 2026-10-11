---
name: default-video-digest
description: Turn a transcript into grounded, structured notes for deep study.
version: 1.0.0
---

# Deep study notes

## Goal

Create a self-contained learning guide that helps the reader understand, question,
retain, and apply the video's content without replacing the source evidence.

## Rules

1. Preserve the raw transcript separately; never reproduce or overwrite it here.
2. Write in the transcript's primary language unless the source metadata strongly
   indicates another language.
3. Do not invent claims, speakers, evidence, chapters, or timestamps.
4. Link chapters and important claims to the nearest available source timestamp. If
   the transcript has no useful segment timing, omit timestamp links rather than
   inventing them.
5. Clearly distinguish the speaker's claims from your synthesis or questions.
6. Explain important concepts and reasoning chains instead of merely listing topics.
7. If the transcript is incomplete or low quality, state the limitation prominently.

## Output

Produce these sections, omitting only sections for which the transcript has no basis:

1. `# 核心结论` / `# Core thesis` — the purpose, conclusion, and argument in context.
2. `## 知识地图` / `## Knowledge map` — how the major concepts relate.
3. `## 分段精读` / `## Guided walkthrough` — structured chapters with grounded
   timestamps and detailed explanations.
4. `## 关键论点与证据` / `## Claims and evidence` — pair each important claim with
   the support actually offered, and flag unsupported assertions.
5. `## 概念与术语` / `## Concepts and terminology` — concise definitions in context.
6. `## 反思与待验证问题` / `## Questions and checks` — assumptions, uncertainties,
   counterarguments, and facts worth independently verifying.
7. `## 学习与行动清单` / `## Study and action list` — review prompts, exercises, or
   next actions that follow from the material.

