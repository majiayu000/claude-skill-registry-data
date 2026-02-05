---
name: blog-en-review
description: Review and improve English translations in bilingual blog posts. Use when the user wants to review, edit, or polish English text in blog posts that have Japanese originals with `::ja` and `::en` sections.
---

# Blog English Review Skill

This skill reviews English translations in bilingual blog posts to ensure the Japanese nuance is correctly conveyed.

## Blog Format

The blog uses this structure:
```markdown
---
title_ja: 日本語タイトル
title_en: English Title
desc_ja: 日本語の説明
desc_en: English description
date: YYYY-MM-DD
publish: false
---

::ja

[Japanese content - the source of truth]

::en

<!-- draft:
[User's English draft - needs review]
-->

<!-- review:
[Review notes go here]
-->

[Final English version goes here]
```

## Review Process

### Step 1: Read and Understand
1. Read the `::ja` section carefully to understand the original intent
2. Read the `<!-- draft: -->` section to see the user's English attempt
3. Identify nuance gaps between Japanese and English

### Step 2: Provide Review Notes
Add corrections to the `<!-- review: -->` section in this format:
```
- "original phrase" → "improved phrase" (reason)
- Added: [what was added and why]
- Removed: [what was removed and why]
- Nuance: [explanation of Japanese nuance that was missing]
```

### Step 3: Generate Final Version
Write the polished English version after the review comments, preserving:
- The author's voice and style
- All links and markdown formatting
- The same paragraph structure as Japanese when possible

## Review Priorities

1. **Nuance accuracy**: Does it convey the Japanese meaning correctly?
2. **Natural English**: Does it read naturally to native speakers?
3. **Tone matching**: Does it match the casual/formal tone of the Japanese?
4. **Cultural context**: Are cultural references explained if needed?

## Example Review

### Input (draft):
```
<!-- draft:
At the Tama city, there is Coffee shop, Kuroko.
The Rei-ryu, is selected at the coffee shop, is delicious.
-->
```

### Output (review + final):
```
<!-- review:
- "At the Tama city" → "In Tama" (more natural preposition, no "city")
- "there is Coffee shop, Kuroko" → "there's a coffee shop called Kuroko" (article, word order)
- "The Rei-ryu, is selected" → "Reiryuu, a coffee they sell there" (clearer structure)
- "is at most for me" → "is the best I've ever had" (captures 断言できる nuance)
-->

In Tama, there's a coffee shop called Kuroko.

Reiryuu, a coffee they sell there, is absolutely exquisite—I highly recommend giving it a try.
```

## Commands

When the user invokes this skill:
1. Ask which blog post to review (or use the one they specify)
2. Read both `::ja` and `::en` sections
3. Fill in `<!-- review: -->` with corrections
4. Write the final English version after the review section
5. Offer to update the file with the changes

## File Locations

- Vault source: `/Users/orangekame3/src/github.com/orangekame3/vault/blog/`
- Blog content: `/Users/orangekame3/src/github.com/orangekame3/orangekame3.github.io/src/content/blog/`
