---
name: laws-of-ux-review
description: >
  Audit existing UI code against all 30 Laws of UX, scoring compliance 0-60 with prioritized code fixes.
  Use when user says "review UX", "UX audit", "audit this page", "check UX compliance", "score this UI",
  "how good is the UX", or "laws-of-ux review".
---

# Laws of UX — Review & Audit

Score existing UI code against all 30 Laws of UX and deliver prioritized, code-level fixes.

## Process

### Step 1: Read the Target

Read the component/page file(s) the user wants audited. If no file specified, ask which file or component to review.

### Step 2: Score Each Law

Load `references/ux-laws-complete.md` from the parent `laws-of-ux` skill.

For each of the 30 laws, score:

| Score | Meaning |
|-------|---------|
| **2** | Compliant — law is properly applied |
| **1** | Partial — some application but incomplete or inconsistent |
| **0** | Violation — law is broken or not addressed where it should be |
| **—** | N/A — law doesn't apply to this component type |

**Maximum score: 60** (all 30 laws fully compliant)

### Step 3: Classify Findings

Group all non-compliant laws into severity tiers:

**CRITICAL (score 0, high-impact laws):**
Laws that directly cause usability failures:
- Fitts's Law (unreachable/tiny targets)
- Doherty Threshold (no loading feedback)
- Hick's Law (overwhelming choices)
- Cognitive Load (too much at once)
- Jakob's Law (breaks conventions)

**WARNING (score 0-1, medium-impact laws):**
Laws that degrade experience:
- Proximity, Common Region, Similarity (grouping issues)
- Miller's Law, Chunking (information overload)
- Goal-Gradient, Zeigarnik (missing progress)
- Von Restorff (nothing stands out)

**SUGGESTION (score 1, polish laws):**
Laws that improve quality:
- Aesthetic-Usability (visual polish)
- Peak-End Rule (celebration states)
- Flow (minor interruptions)
- Parkinson's Law (time cues)

### Step 4: Generate Report

Output this exact format:

```markdown
# UX Audit: [Component/Page Name]

**Score: [X]/60** | **Grade: [A/B/C/D/F]**

| Grade | Range |
|-------|-------|
| A | 50-60 |
| B | 40-49 |
| C | 30-39 |
| D | 20-29 |
| F | 0-19 |

## Critical Issues ([count])

### [Law Name] — Score: 0/2
**Problem:** [What's wrong, referencing specific lines]
**Fix:**
```[language]
// Before (line XX)
[current code]

// After
[fixed code]
```

## Warnings ([count])

### [Law Name] — Score: [0-1]/2
**Problem:** [description]
**Fix:** [code change]

## Suggestions ([count])

### [Law Name] — Score: 1/2
**Improve:** [description]
**Code:** [enhancement]

## Compliant ([count])
[List of laws scoring 2/2 — no action needed]

## N/A ([count])
[List of laws not applicable to this component]
```

### Step 5: Prioritized Action Plan

After the report, provide a numbered action plan:

```markdown
## Action Plan (do in this order)

1. **[Critical fix]** — [1-line description] → [file:line]
2. **[Critical fix]** — [1-line description] → [file:line]
3. **[Warning fix]** — [1-line description] → [file:line]
...
```

## Rules

1. **Always read the actual code** — never score based on assumptions
2. **Every violation needs a code fix** — no fix = not a real finding
3. **Be honest about N/A** — don't force-apply laws that don't fit
4. **Reference specific lines** — `file.tsx:42` not "somewhere in the component"
5. **Score consistently** — same violation in two components gets same score
