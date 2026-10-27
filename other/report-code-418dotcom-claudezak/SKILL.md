---
description: Generate a professional report from data or findings - audience-aware
argument-hint: "[topic and audience]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Grep
  - Bash(date:*)
---

Turn raw data, findings, or research into a polished narrative report. Adapts tone and depth for the target audience.

## Steps

### Step 1: Clarify inputs

Identify:
- **Topic:** What is this report about?
- **Data sources:** What files, findings, or data should feed into it?
- **Audience:** Who is reading this? (executive, technical team, client, board, general)
- **Format preference:** Brief (1-2 pages), standard (3-5 pages), or comprehensive (5+ pages)

If the user didn't specify an audience, default to "professional — clear, direct, no jargon."

### Step 2: Gather source material

Read all relevant files and data. Scan for:
- Key findings and metrics
- Patterns and trends
- Comparisons (before/after, vs. benchmark, vs. competitor)
- Anomalies or concerns
- Recommendations that emerge from the data

### Step 3: Structure for the audience

**Executive audience:**
- Lead with the bottom line (recommendation or key finding)
- Use bullet points over paragraphs
- Include only metrics that drive decisions
- Keep under 2 pages
- End with clear next steps

**Technical audience:**
- Lead with methodology
- Include detailed data and analysis
- Show your work (how you reached conclusions)
- Include caveats and limitations
- Reference source files

**Client audience:**
- Lead with what matters to them (results, ROI, impact)
- Use their language, not yours
- Contextualise numbers ("+15% vs industry average of +3%")
- Include visual formatting (tables, bold key numbers)
- End with what happens next

### Step 4: Write the report

```markdown
# [Report Title]

**Date:** [date]
**Prepared for:** [audience]

---

## Summary

[2-3 sentences: key finding, core recommendation, bottom line]

## Key Findings

### [Finding 1]
[Data, context, significance]

### [Finding 2]
[Data, context, significance]

### [Finding 3]
[Data, context, significance]

## Analysis

[Deeper interpretation — what the findings mean, patterns, comparisons]

## Recommendations

1. **[Action]** — [rationale and expected impact]
2. **[Action]** — [rationale and expected impact]
3. **[Action]** — [rationale and expected impact]

## Next Steps

- [ ] [Specific action with owner/timeline]

---
Sources: [list data sources used]
```

### Step 5: Quality check

Before delivering, verify:
- [ ] Every claim has supporting data
- [ ] No jargon the audience wouldn't understand
- [ ] Recommendations are actionable (not vague)
- [ ] Numbers are consistent throughout
- [ ] Report answers "so what?" — not just "what"

Save to `reports/[topic]-report.md` and output a summary.
