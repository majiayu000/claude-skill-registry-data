---
name: policy-news-search
description: Search and collect policy/current-affairs source materials before analysis. Use when input is fragmented (keywords, fuzzy title, retell, or URL), when weekly/manual inspection is requested, or when analysis workflow reports critical knowledge gaps. Separates retrieval from analysis and controls agent-browser usage by priority.
---

# Policy & News Search Skill

Use this skill to turn fragmented user input into complete, verifiable source materials.

## Hard boundary

- Retrieval only. Do **not** output analysis conclusions in this skill.
- Report three things only after retrieval:
  1) what was found,
  2) whether material is complete,
  3) whether to enter full analysis.

## Modes

1. User-triggered retrieval
   - Read and follow: `references/openclaw_search_vol1_triggered.md`
2. Inspection mode (manual/cron-triggered)
   - Read and follow: `references/openclaw_search_vol2_autonomous.md`

## Tool priority

1. Built-in search/fetch first to decide whether content is worth deep fetch.
2. Use `agent-browser-clawdbot` only after trigger conditions are met and full text is needed.
3. Avoid agent-browser for bulk title scanning.

## Integration contract with analysis skill

When handing off to `policy-news-analysis`, provide:
- audience hint (if known)
- source URL(s)
- publisher/date
- completeness checklist result
- unresolved missing fields (if any)

## Output checklist

- Input type recognized (keyword/fuzzy title/retell/URL)
- Retrieval path executed (policy path or event path)
- Completeness check done
- Trigger decision made (enter analysis or not)
- Missing fields explicitly listed if incomplete
