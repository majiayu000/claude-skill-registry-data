---
name: thread-analysis
description: Analyze Twitter/X threads to extract insights from viral and educational content. Use when the user mentions Twitter, X, thread, tweets, viral thread, or provides a twitter.com or x.com URL.
---

# Twitter/X Thread Analysis

Analyze Twitter/X threads to generate structured reports with summaries, key points, and insights from conversational content.

## When to Use

Activate this skill when the user:
- Mentions "Twitter", "X", "thread", "tweets", "tweet thread"
- Provides a twitter.com or x.com URL
- Asks to summarize a viral thread
- Wants to analyze a thread they copied
- References a thought-leader's thread

## Instructions

1. **Get the thread content**:
   - If URL: Fetch using WebFetch (try nitter mirror if needed)
   - If text: Use directly
   - Ask for URL or content if not provided
2. If fetch fails:
   - Inform user: "Could not fetch thread content"
   - Suggest copying thread text manually
   - Stop here
3. **Read the analysis prompt** from `prompts/thread.md`
4. **Extract thread metadata**:
   - Author handle and name
   - Thread topic/title
   - Number of tweets
5. **Generate analysis** following the prompt structure exactly
6. **Create output directory** `reports/threads/` if needed
7. **Save the report** to `reports/threads/YYYY-MM-DD_sanitized-title.md`
8. **Update the activity log** at `logs/YYYY-MM-DD.md`:
   - Add entry under "## Threads Read" section
   - Format: `- [Title](../reports/threads/filename.md) - HH:MM`
9. **Confirm to user** what was saved and where

## Report Format

```markdown
# [Thread Topic/Title]

**Source**: [URL or "Manual Input"]
**Author**: [@handle]
**Date**: YYYY-MM-DD
**Type**: Twitter/X Thread

---

[Analysis content following prompts/thread.md structure]

---

## My Notes

[Empty space for user notes]
```

## Error Handling

- If URL invalid: Ask for correct URL or suggest copy
- If thread too short: Analyze but note limited content
- If prompts/thread.md missing: Use prompts/default.md

## Related

- Slash command: `/thread <url-or-content>`
- Prompt file: `prompts/thread.md`
- Output: `reports/threads/`
