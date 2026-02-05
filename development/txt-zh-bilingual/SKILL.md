---
name: txt-zh-bilingual
description: Translate English .txt files into Chinese and produce sentence-aligned bilingual JSON with merging of short English sentences. Use when asked to batch-convert text files into [{"en","zh"}] arrays, split/merge sentences, or generate JSON alongside original .txt files.
---

# Txt Zh Bilingual

## Overview

Convert English `.txt` files into bilingual JSON arrays, with sentence splitting, merging of short English sentences, and Chinese translation for each aligned segment.

## Workflow

### 1. Translate the full text first (AI-guided)

Read the entire `.txt` file and produce a coherent, natural Chinese translation of the full content. Fix line breaks, captions, or fragmentary lines in Chinese so the narrative flows.

Guidelines:
- Preserve tone, pacing, and speaker intent.
- Keep technical terms and product names consistent.
- Do not force sentence-by-sentence alignment at this stage.

### 2. Build English sentence segments

Reconstruct complete English sentences from the raw lines. Merge broken fragments and normalize punctuation.

Guidelines:
- Merge fragments split by newlines into complete sentences when they belong together.
- Preserve intentional short lines only when they are standalone utterances (e.g., sound cues, one-word reactions, quoted asides).
- If a line is obviously a continuation (starts with conjunctions like "and", "but", "so", or lowercase), merge it into the previous segment.
- If punctuation is missing but the meaning clearly continues, merge until the thought completes.
- Keep each `en` segment concise; split long sentences if they become unwieldy for listening practice.

### 3. Align Chinese to English segments

Split the full Chinese translation from Step 1 into segments that align with the English sentences from Step 2. Each `zh` entry should map cleanly to the corresponding `en` entry for listen-then-translate practice.

Alignment rules:
- One `en` sentence maps to one `zh` sentence/segment.
- If one English sentence requires multiple Chinese clauses, keep them within the same `zh` entry.
- Avoid mixing content from different English sentences into one `zh` entry.
- Prefer natural Chinese phrasing over word-for-word mapping, but keep information coverage aligned.

### 4. Validate output format

Ensure the JSON is an array of objects like:

```json
[
  {"en": "Example sentence.", "zh": "示例句子。"}
]
```
