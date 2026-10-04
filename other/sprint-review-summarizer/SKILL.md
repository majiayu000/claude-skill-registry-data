---
name: sprint-review-summarizer
description: "Transform sprint notes into a structured stakeholder doc: delivered, deferred, risks, next focus. No Jira needed. Use when preparing sprint review or stakeholder updates from free-form PM notes. Triggers: 'sprint review summary', 'summarize sprint results', 'итоги спринта', 'оформи итоги спринта'."
version: 1.0.0
---

# Sprint Review Summarizer

This skill transforms plain-language sprint summary notes into a structured stakeholder document covering delivered items, deferred work, risks, and next sprint focus. It works from any free-form text or markdown file — no integrations, no YAML, no Jira required.

**Input:**
- Sprint notes as pasted text or markdown file (any format accepted)
- Optional: sprint number, team name, sprint goal (for metadata enrichment)

**Output:**
- Markdown stakeholder document with sections: Executive Summary, Delivered, Deferred, Risks & Issues, Next Sprint Focus, Key Decisions (if detected)

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate and Parse Input

1. Check that sprint notes content is provided (pasted text or file reference)
   - If input is empty or whitespace only: Stop. Return: "No sprint notes provided. Paste your sprint summary or provide a file path."

2. Check input format
   - If input resembles a structured Jira/CSV export (column headers, ID fields, etc.): Inform the user — "This looks like a structured export, not plain-language notes. This skill works best with free-form sprint notes." Offer to attempt processing if user confirms.
   - Otherwise: proceed with parsing

3. Extract optional sprint metadata if present in notes:
   - Sprint name or number (e.g., "Sprint 24", "Q2 Sprint 3")
   - Dates (e.g., "May 5–19")
   - Team name
   - Sprint goal
   - If metadata is missing: use placeholder "Sprint [YYYY-MM-DD]" for the heading and continue without blocking

### Step 2: Classify Items into Four Categories

1. Read all content and identify discrete items (sentences, bullet points, paragraphs describing work)

2. Map each item to one of four categories using semantic heuristics:

   **Delivered** — signals: "shipped", "done", "released", "completed", "launched", "finished", "delivered", "closed", "fixed", "resolved"

   **Deferred** — signals: "pushed", "moved", "postponed", "deferred", "not completed", "carried over", "slipped", "didn't make it", "won't be done this sprint"

   **Risks & Issues** — signals: "blocked", "blocker", "risk", "concern", "dependency", "issue", "problem", "delay", "at risk", "needs attention", "escalate"

   **Next Sprint Focus** — signals: "next sprint", "next", "plan", "priority", "upcoming", "focus for", "will start", "goal for next"

3. Handle items that span multiple categories:
   - Place under the primary category
   - Add a cross-reference note if secondary category is relevant (e.g., item in Delivered that also carries a risk)

**Edge Cases:**
- If notes contain only delivered items: generate document with empty sections marked "None noted this sprint" — do not omit sections
- If notes are very short (1–3 sentences): extract what's possible; append note: "Source notes were minimal — document may be incomplete. Consider adding detail before sharing."

### Step 3: Detect Key Decisions

1. Scan for decision language: "decided", "agreed", "approved", "confirmed", "resolved to", "we will", "going with", "chose", "selected"
2. If any decisions are detected: compile a Key Decisions list
3. If no decisions detected: omit the Key Decisions section from output

### Step 4: Calculate Completion Metric

1. Count items in Delivered vs. total items (Delivered + Deferred)
2. If quantifiable: include in Executive Summary as "N of M items delivered"
3. If items cannot be counted (prose-only notes): use qualitative phrasing (e.g., "Core sprint goal achieved; 2 items deferred")

### Step 5: Handle Multi-Sprint Input

1. Check if notes reference multiple sprints (e.g., "Sprint 24", "Sprint 25" headers appear)
2. If distinct sprint boundaries are detectable: generate separate sections per sprint
3. If indistinguishable: process as one sprint and append note: "Notes may cover multiple sprints — review sections for accuracy."

### Step 6: Format and Output Document

1. Generate markdown document following the Output Format below
2. Ensure all four core sections appear even if empty
3. Validate no placeholder text is visible to the end user

---

## Output Format

```markdown
## Sprint Review: [Sprint Name or Date]

**Team:** [team name or "—"]
**Sprint dates:** [dates or "—"]
**Summary:** [1-sentence executive summary, e.g., "8 of 10 planned items delivered; 2 deferred to next sprint due to dependency blockers."]

---

### ✅ Delivered
- [Item 1]
- [Item 2]

### ⏩ Deferred
- [Item 1 — reason if mentioned]
- *(None noted this sprint)*

### ⚠️ Risks & Issues
- [Risk or issue 1]
- *(None noted this sprint)*

### 🎯 Next Sprint Focus
- [Priority 1]
- [Priority 2]

### 📋 Key Decisions
- [Decision 1]
*(Section omitted if no decisions detected)*
```

**Field rules:**
- Executive Summary: one sentence, includes completion metric if quantifiable
- All four core sections always present, even if empty (use "None noted this sprint")
- Key Decisions section: only included when decisions are detected
- Output is copy-paste ready for email, Slack, or stakeholder update

---

## Negative Cases

- **Empty input:** Stop before processing. Return: "No sprint notes provided. Paste your sprint summary or provide a file path."
- **Jira/CSV structured export:** Detect column-header patterns; warn user and offer to attempt anyway with confirmation
- **Non-EN/RU language detected:** Process in the detected language; generate output in same language
