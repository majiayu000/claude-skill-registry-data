---
name: trace
description: Use when the user runs /trace [topic] or wants to see how an idea evolved over time across the vault. Tracks the arc of thinking on a specific topic.
---

# Trace — Idea Evolution Tracker

Show how a specific idea or topic has evolved across King's vault over time.

## Input

The user provides a topic after the command: `/trace [topic]`
If no topic given, ask: "What idea do you want to trace?"

## Process

1. **Search broadly** — grep all `.md` files in the vault for the topic (and synonyms/related terms)
   ```bash
   grep -ril "[topic]" ~/Documents/Obsidian/personalOS/ --include="*.md"
   ```

2. **Collect matches** — read each matching file, extract:
   - The file path and folder (tells you context: daily note vs knowledge vs project)
   - The frontmatter `date` or `created` field
   - The surrounding paragraph(s) where the topic appears

3. **Sort chronologically** — by `date`/`created` frontmatter, or by filename for daily notes (`YYYY-MM-DD.md`)

4. **Trace the arc** — look for:
   - First mention: what was the original framing?
   - How did the language/framing shift over time?
   - What other concepts got linked to it?
   - Where does it sit now — active project, knowledge note, daily thought?

## Output Format

---

**Tracing: [topic]**
*Found in [N] notes across [date range]*

**First appearance** — [date], [file]
> [quote or paraphrase]

**Evolution**
- [date] — [file type] — [how the idea shifted]
- [date] — [file type] — [new angle or connection]
- ...

**Current state** — [where it lives now, how it's framed]

**Connected to**
- [[note]] — [why it's connected]

**Observation** — [one insight about how this idea has grown or changed]

---

## Rules

- Pull direct quotes where possible — King's own words, not summaries
- Chinese content in daily notes: include it, translate inline
- If topic appears in only 1-2 notes, say so — the trace may be short
- Don't force connections that aren't there
