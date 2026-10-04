---
name: site-phase-7b
description: >-
  Phase 7b — Dedicated visual review with fresh context. Evaluates screenshots
  against blueprint, applies 34 criteria, produces structured diagnosis for loopback.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
effort: high
context: fork
user-invocable: false
---

# Phase 7b — Visual Review

## Objective

With fresh context, perform a thorough visual review of the built site. Compare screenshots against the enchantment map, evaluate manual criteria 32-34, check image quality, and assess anti-similarity. Produce a structured diagnosis that either approves the site or provides an actionable fix list for the loopback correction agent.

This phase is SEPARATE from Phase 7 (automated scoring). Phase 7 ensures technical quality (score >= 9.0). This phase ensures VISUAL quality and ENCHANTMENT — what makes someone want to buy the site.

---

## Input (provided by orchestrator)

- `$LEAD_ID` — the lead being built
- Phase 7 automated scores (from report)
- Screenshots at `sites/$LEAD_ID/screenshots/`
- Blueprint at `sites/$LEAD_ID/mapa-encantamento.md`

## Step 1 — Load the 34 criteria

```
Read: sites/_templates/visual-review-criteria.md
```

This file contains ALL 34 criteria with IDs, categories, severities, penalties, and pass conditions. You must know every criterion to evaluate properly.

## Step 2 — Load the quality rubric

```
Read: sites/_templates/quality-rubric.md
```

This contains: criteria 32-34 scoring rubrics, Gate 2 visual analysis questions, visual-analysis.md format template, classic error patterns.

## Step 3 — Read the enchantment map

```
Read: sites/$LEAD_ID/mapa-encantamento.md
```

Extract and memorize:
- Every section's planned LAYOUT, ANIMATION, VISUAL TECHNIQUE
- The signature element and where it should appear
- The aesthetic direction committed
- The animation budget (showstopper, supporting, baseline)

## Step 4 — Read Phase 7 automated results

```
Read: data/reports/site-$LEAD_ID/phase7-quality.md
```

Note: which automated criteria passed/failed, the final score, any fixes already applied.

## Step 5 — Visual inspection of screenshots

Read ALL screenshots with full visual attention:

```
Read: sites/$LEAD_ID/screenshots/fullpage-desktop.png
Read: sites/$LEAD_ID/screenshots/fullpage-mobile.png
Read: sites/$LEAD_ID/screenshots/viewport-desktop.png
Read: sites/$LEAD_ID/screenshots/viewport-mobile.png
```

For EACH screenshot, analyze pixel by pixel:
- **Proportions:** Elements with wrong size, distorted images, disproportionate cards
- **Positioning:** Overlapping elements, misaligned, outside container
- **Spacing:** Excessive gaps, inconsistent margins, missing padding
- **Text:** Breaking into too many lines on mobile, overflow, truncation
- **Responsiveness:** Layout working on desktop but broken on mobile (or vice-versa)
- **Enchantment:** Wow moments from the blueprint that were NOT implemented

## Step 6 — Evaluate manual criteria 32-34

### Criterion 32: Visual Originality

Open screenshots of the last 2 built sites:
```bash
LAST_TWO=$(ls -td sites/*/screenshots/fullpage-desktop.png 2>/dev/null | grep -v "$LEAD_ID" | head -2)
for f in $LAST_TWO; do echo "Compare with: $f"; done
```

Read each and compare. Score 0-10 using the rubric from visual-review-criteria.md.

### Criterion 33: Desktop Professionalism

Score from fullpage-desktop.png using rubric.

### Criterion 34: Mobile Professionalism

Score from fullpage-mobile.png using rubric. SEPARATE evaluation from desktop.

## Step 6.5 — Comparative Framework (MANDATORY before verdicts)

**Why this step exists:** Without a comparison framework, "Looks like $50K site?" defaults to YES. You need external reference points to honestly evaluate distinctiveness.

### 6.5a — Load the 5 most recent sites' screenshots

```bash
RECENT_SITES=$(ls -td sites/*/screenshots/fullpage-desktop.png 2>/dev/null | grep -v "$LEAD_ID" | head -5)
for f in $RECENT_SITES; do echo "Read: $f"; done
```

Read each screenshot. Compare structurally against the current site.

### 6.5b — Fill the Comparison Table (MANDATORY in visual-analysis.md)

For each of the 3 most recent other sites, score similarity 0-10 where 0 = completely different and 10 = identical structure:

```markdown
## Comparative Framework

### Comparison A — [site name]
- Hero similarity: X/10 — [what specifically is similar or different]
- Navbar similarity: X/10
- Section order similarity: X/10
- Color palette similarity: X/10
- Typography pairing similarity: X/10
- Animation character similarity: X/10
- "Could be confused with" overall: X/10

### Comparison B — [site name]
[same structure]

### Comparison C — [site name]
[same structure]

### Overall Assessment
- **Most dangerous overlap:** [which site + which dimension]
- **Distinguishing features:** List 3 concrete things that make the current site impossible to confuse with any of the 3 comparisons
  1. [Concrete thing #1]
  2. [Concrete thing #2]
  3. [Concrete thing #3]
```

### 6.5c — Verdict gate (applies before Step 9 verdicts)

You may ONLY answer SIM/YES to the 3 verdicts in Step 9 if:

1. ALL 3 "could be confused with" overall scores are <= 5
2. At least 3 distinguishing features are concrete (not abstract words like "refined", "elegant", "premium")
3. You can describe the site in 10 concrete words that would NOT describe any of the 3 comparison sites

If any of these conditions fail, the verdicts MUST be NO and you write a Loopback Diagnosis with specific divergence instructions.

## Step 7 — Blueprint adherence check

For EACH section in the blueprint, verify:
1. Was the specified LAYOUT implemented?
2. Does the specified ANIMATION exist in the component?
3. Was the VISUAL TECHNIQUE applied?
4. Is the signature element present where specified?

List every deviation.

## Step 8 — Image review

Load the image analysis guide:
```
Read: sites/_templates/image-analysis-guide.md
```

Run the image gate:
```bash
.claude/scripts/gate-images.sh $LEAD_ID --full
```

Then perform visual checks from the guide:
1. **Visual inspection** in screenshots — overflow, stretch, crop, whitespace
2. **CSS containment** in code — object-fit, dimensions, overflow-hidden
3. **Image-context coherence** — does image content match section topic?
4. **Contribution** — does each image help or hurt?

## Step 9 — Answer quality questions + verdicts

Follow the Gate 2 Questions section from quality-rubric.md. Answer ALL questions IN WRITING:

**Wow moments, Visual quality, Mobile-specific, Desktop-specific** — every question answered.

**Three verdicts (answer HONESTLY):**
- "Looks like a $50K site?" → YES or NO with justification
- "Would someone share this link saying 'look how amazing'?" → YES or NO
- "If I were the business OWNER, would I be PROUD?" → YES or NO

## Step 10 — Produce structured output

### If ALL criteria pass (every criterion >= 8, average >= 9.0, all 3 verdicts YES):

Write `sites/$LEAD_ID/visual-analysis.md` following the format from quality-rubric.md. Mark status as PASS.

### If ANY criterion fails:

Write `sites/$LEAD_ID/visual-analysis.md` with the full analysis AND a Loopback Diagnosis section:

```markdown
## Loopback Diagnosis

### Status: FAIL
### Loopback Count: {N}/2

### Failing Criteria
| # | Criterion | Score | Required | Category |
|---|-----------|-------|----------|----------|
| {n} | {name} | {score} | >= 8 | {category} |

### Visual Problems Found
1. **[Section: {name}]** {description}
   - File: {file_path}:{line}
   - Fix: {specific fix instruction}

### Blueprint Deviations
- {section}: Blueprint says "{spec}" but implementation uses "{actual}"

### Verdicts
- "Looks like $50K site?" → {YES/NO} — {justification}
- "Would someone share?" → {YES/NO} — {justification}
- "Owner proud?" → {YES/NO} — {justification}

### Suggested Action
{Prioritized list of what to fix first}
```

**CRITICAL:** The diagnosis must include specific file paths and line numbers for every problem. The Correction Agent will use this to apply targeted fixes — vague descriptions like "fix the layout" are useless.

---

## Anti-Shortcut Rules

- If you find "everything perfect" on first look, you are prioritizing speed. STOP and look again.
- visual-analysis.md MUST have >= 1000 characters of real analysis (not checkboxes)
- You MUST mention EACH section by name in your analysis
- Score 9.0+ from Phase 7 does NOT mean visual review passes — a generic site can score perfectly

## Exit Gate

```bash
# 1. Visual analysis completeness
.claude/scripts/gate-quality-loop.sh $LEAD_ID --post

# 2. Comparative framework + memorability
.claude/scripts/gate-memorability.sh $LEAD_ID
```

Both gates must pass. If either fails, return to the corresponding step and fix.

## Constraints

| Constraint | Enforced by |
|---|---|
| All 34 criteria >= 8, average >= 9.0 | Criteria check |
| All 3 verdicts = YES | Honest visual assessment |
| visual-analysis.md >= 1000 chars | gate-quality-loop.sh --post |
| Every section mentioned by name | Anti-shortcut rule |
| Diagnosis includes file:line for every problem | Loopback contract |
| Images coherent and well-contained | gate-images.sh --full + visual check |

## Exit Criteria

- [ ] All 34 criteria evaluated (31 automated reviewed + 3 manual scored)
- [ ] Blueprint adherence checked for every section
- [ ] Image review complete (gate + visual + coherence)
- [ ] All quality questions answered in writing
- [ ] All 3 verdicts answered honestly
- [ ] visual-analysis.md saved with >= 1000 chars
- [ ] Status determined: PASS (all clear) or FAIL (with structured diagnosis)
- [ ] gate-quality-loop.sh --post exits 0
