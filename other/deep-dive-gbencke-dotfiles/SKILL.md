---
name: deep-dive
description: >
  Generate a deep-dive technical document from meeting transcripts and
  summaries in the Obsidian vault. Follows a strict 16-section structure with
  attribution rules, table preference, verbatim-only quotes, and blocker
  flagging. Output is written to 01.Technical/product/deep dives/.
  Use when asked to "create a deep dive", "write a deep dive on X", "generate
  deep dive report", "deep dive into X", or invokes /deep-dive.
argument-hint: "<topic>"
---

# Deep Dive Skill

Reads all files in `02.Meetings/transcripts/` and `02.Meetings/summaries/`
and produces a structured deep-dive document on the requested topic.

The argument is the topic. Example: `/deep-dive Insurance and Payor Definitions at Provider Level`

---

## Output Location

```
01.Technical/product/deep dives/deep-dive-<topic-slug>.md
```

Use `01.Technical/product/deep dives/deep-dive-non-patient-events.md` as the
structural template. Match its 16-section layout exactly.

---

## 16-Section Structure

| # | Section | Content |
|---|---|---|
| 1 | **Core Problem** | 2–3 sentences: the fundamental gap or tension |
| 2 | **What [TOPIC] Is** | Scope, definition, why it matters |
| 3 | **Classic vs. NewGen** | Comparison table (Aspect \| Classic \| NewGen/IQ) |
| 4 | **Key Architectural Decisions** | One subsection per decision, dated, with owner and context quote where available |
| 5 | **[Topic-Specific]** | 1–3 sections for sub-topics unique to this domain (see guide below) |
| 6 | **Impact on Downstream** | How this topic affects rules engine, scheduling, chatbot, or other systems |
| 7 | **Synchronization Gaps** | Table: Gap \| Impact \| Status/Owner |
| 8 | **Feature Flag Behavior** | Table if flags apply; omit section if none |
| 9 | **Open Questions** | Numbered list of unresolved items only |
| 10 | **Blockers & Dependencies** | Table: Blocker \| Owner \| Target date |
| 11 | **Concerns Flagged** | Table: Concern \| Who \| Date \| Impact |
| 12 | **Stakeholders & Positions** | Table: Person \| Role \| Position on this topic |
| 13 | **Key Quotes** | Blockquote format with attribution and date |
| 14 | **Confluence Documentation** | Links found in transcripts/summaries: Space \| Page Title \| 3–5 bullet summary |
| 15 | **Timeline** | Table: Date \| Milestone (oldest to newest) |
| 16 | *(omit any section where no evidence exists)* | — |

---

## Topic-Specific Section Guide (Section 5)

Pick 1–3 sub-section names that fit the domain:

| Topic | Topic-Specific Sections |
|---|---|
| Non-Patient Events | Deletion & Cancellation · Recurring Event Handling |
| Plan of Care | Hydration Strategy · Visit Counting Logic |
| Payer/Financial | Payer Data Hydration · Insurance & Financial Class Integration |
| Provider Insurance | Allowed Insurance per Provider · Referential Integrity Rules |

For any topic not listed, derive 1–3 sub-sections from the most recurring
sub-themes in the source material.

---

## Authoring Rules

- **Every factual claim** must trace to a specific meeting date and speaker
  name. Format: *(Feb 5 — Firstname Lastname)*
- **Prefer tables** over prose for comparisons, gaps, blockers, and
  stakeholders.
- **Verbatim quotes only** — use blockquote syntax (`>`) with `— Name (Date)`
  attribution. Never paraphrase as a quote.
- **Mark genuine blockers** as `**blocker**` in bold where they block a
  milestone.
- **Open questions only** — list items with no confirmed answer in any source.
  If a decision is partially resolved, note the remaining gap explicitly.
- **Valid Obsidian Markdown** — no HTML, no LaTeX.
- **No extra structure** — do not add sections, preamble, or commentary outside
  the 16-section layout.
- **Omit empty sections** — never write "no information available"; drop the
  section entirely.

---

## Verification Checklist

After writing the output file, confirm:

- [ ] Output exists at `01.Technical/product/deep dives/deep-dive-<slug>.md`
- [ ] All sections present, numbered, in order (16 or fewer)
- [ ] Every decision in Section 4 has a date and owner
- [ ] Section 12 (Stakeholders) covers all named people from the transcripts
- [ ] Section 13 (Key Quotes) uses `>` blockquote syntax with `— Name (Date)` attribution
- [ ] No section contains "no information available" — omit instead
