---
name: critical-echo
description: Generate constructive criticism reviews for popular tech articles. Use when asked to review, critique, or analyze trending tech articles from platforms like Qiita, Zenn, Hacker News, or Dev.to. (user)
---

This file defines the procedure for AI to generate Critical Echo review articles.

---

## Motivation

When an article goes viral and everyone nods along — "Yes, exactly!" — that's often the moment thinking stops. Good criticism doesn't tear down. It adds dimension — a "perspective line" (補助線) that helps readers see relationships that weren't visible before.

AI criticism has no motive to suspect: no tribal affiliations, no past statements to defend, no personal stakes. This lets readers focus on the argument itself.

**We only critique strong articles.** Being selected for review is recognition, not attack.

---

## Overview

Generate constructive criticism reviews for popular tech articles.

**Principles:**
- Not criticism for its own sake
- Add perspective to the original article, expanding reader thinking
- Only review articles worth critiquing

---

## Workflow

### 1. Collect

Fetch trending/popular articles from target platforms.

**Target platforms:**
- Qiita (Weekly Trend)
- Zenn (Trending)
- Hacker News (Front page)
- Dev.to (Top posts)

### 2. Select

Select "articles worth critiquing" from collected articles.

**Selection criteria:**

| Include | Exclude |
|---------|---------|
| Articles with clear arguments | Mere information roundups |
| Allows structural discussion | Fact reports or experience logs only |
| Readers are nodding "yes, exactly!" | Clickbait / rage-bait titles |
| Author wrote sincerely | Entertainment / meme posts |
| Room to add perspective | Already self-critical content |

**Decision examples:**
- ◎ "You should do X" / "The value of Y" — Has argument, easy to critique
- △ Technical tutorials — Limited room for perspective
- × Failure stories / retrospectives — Already reflective, criticism feels rude
- × Rankings / roundups — No argument to engage with

**Log all decisions** in `selection-logs/YYYY-MM-DD.md` with rationale.

### 3. Write

Generate review for selected articles.

**Prompt:**

```
Provide constructive criticism for this article.

Principles:
- Acknowledge the article's value, then add overlooked perspectives
- Don't list "missing things" — focus deeply on one point
- Maintain respect for the author; end by handing a question to readers

Then self-critique your review and output a revised version.

Self-critique checklist:
- Did I criticize beyond the article's scope?
- Am I asking for things unreasonable to expect?
- Is the tone attacking rather than constructive?
- Did I sufficiently acknowledge the article's value?

Output only the revised version.
Follow the format in templates/review.md.
```

### 4. Verify

Check the generated review.

**Checklist:**
- [ ] Article's value is clearly stated
- [ ] Criticism focuses on one point
- [ ] Tone is not aggressive
- [ ] Pros/Cons balance is appropriate
- [ ] "One thought" section is not preachy
- [ ] Score section includes both article score and self-score with brief rationale

### 5. Publish

Save the review and update related files:

1. **Save review file** to `docs/reviews/YYYY-MM-DD-[slug].md`
   - Example: `docs/reviews/2025-12-19-value-of-upstream.md`

2. **Update reviews.yml** - Prepend a new entry to `docs/_data/reviews.yml`:
   ```yaml
   - title: 'On "Article Title"'
     slug: YYYY-MM-DD-[slug]
     date: YYYY-MM-DD
     original: https://original-url
   ```

3. **Update url_list.md** - Append the URL to `url_list.md` to prevent duplicate reviews

4. **Commit** all changes with message: `Add review: [article title]`

---

## Templates

See `templates/review.md` in the repository root.

---

## Operational notes

- Target 1-3 articles per day
- Don't feature the same author consecutively
- Avoid articles currently in controversy (allow cooling period)
- If responses come to reviews, consider a follow-up article
- **Write reviews in the same language as the original article**
