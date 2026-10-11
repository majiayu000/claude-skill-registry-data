---
name: short-video-abstract
description: Produce a fast, decision-oriented abstract grounded in a video transcript.
version: 1.0.0
---

# Short video abstract

## Goal

Help the reader decide in under a minute whether the full study notes or source video
are worth their time.

## Rules

1. Write in the transcript's primary language unless the source metadata strongly
   indicates another language.
2. Stay grounded in the transcript. Do not add background facts or infer claims that
   the speaker did not make.
3. Keep the entire response concise: roughly 120–200 Chinese characters or 80–140
   English words.
4. Do not reproduce the transcript or create a detailed chapter list.
5. If the transcript is incomplete or low quality, say so in one short warning.

## Output

Produce exactly these sections:

1. `# 一句话摘要` / `# One-sentence abstract` — the topic and central conclusion.
2. `## 你会得到什么` / `## What you will learn` — 2–4 concrete bullets.
3. `## 是否值得深入` / `## Is it worth going deeper?` — who benefits, what prior
   interest is assumed, and the strongest reason to continue or skip.

