---
name: daily-en-review
description: Review and improve English in daily journal entries. Use when the user wants to review their daily English practice with Japanese originals in `::ja` and `::en` sections.
---

# Daily English Review Skill

This skill reviews English translations in daily journal entries for English learning purposes.

## Daily Format

Daily entries use this structure:
```markdown
---
date: YYYY-MM-DD
publish: true
---

::ja

[Japanese content - what they want to say]

::en

<!-- draft:
[User's English attempt - needs review]
-->

<!-- review:
[Review notes go here]
-->

[Final English version goes here]
```

## Review Process

### Step 1: Read and Understand
1. Read the `::ja` section to understand what the user wants to express
2. Read the `<!-- draft: -->` to see their English attempt
3. Identify errors and areas for improvement
4. Note any image embeds (`![[image.jpg]]`) in the `::ja` section

### Step 2: Provide Review Notes
Add corrections to the `<!-- review: -->` section in this format:
```
- "original phrase" → "improved phrase" (reason in Japanese)
```

### Step 3: Generate Final Version
Write the polished English version after the review comments.

### Step 4: Include Images
Copy any image embeds from the `::ja` section to the end of the `::en` section to maintain visual consistency.

## Review Priorities

1. **Grammar correctness**: Fix basic errors first
2. **Natural expression**: Make it sound natural
3. **Meaning preservation**: Keep the original intent
4. **Brevity**: Daily entries are short, keep reviews focused

## Example Review

### Input:
```markdown
::ja

今日はvaultの整理をした。
古い日報を消して、英語練習用の仕組みを作った。

::en

<!-- draft:
Today I cleaned up vault.
I deleted old daily and made new system for English.
-->
```

### Output:
```markdown
::ja

今日はvaultの整理をした。
古い日報を消して、英語練習用の仕組みを作った。

::en

<!-- draft:
Today I cleaned up vault.
I deleted old daily and made new system for English.
-->

<!-- review:
- "cleaned up vault" → "cleaned up my vault" (冠詞追加)
- "deleted old daily" → "deleted the old daily files" (冠詞追加、filesで明確に)
- "made new system" → "set up a new system" (より自然な表現)
- "for English" → "for English practice" (目的を明確に)
-->

Today I cleaned up my vault.
I deleted the old daily files and set up a new system for English practice.
```

## Commands

When the user invokes this skill:
1. Find today's daily entry (or the one they specify)
2. Read both `::ja` and `::en` sections
3. Add review notes to `<!-- review: -->` section
4. Write the corrected English after the review comments
5. Update the file

## File Locations

- Vault source: `/Users/orangekame3/src/github.com/orangekame3/vault/daily/`
- Blog content: `/Users/orangekame3/src/github.com/orangekame3/orangekame3.github.io/src/content/daily/`
