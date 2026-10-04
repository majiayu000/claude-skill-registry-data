---
name: qa-css-analysis
description: Generate focused QA test plans (300 lines max) for customer CSS deployments
---

## ⚠️ OUTPUT RULES - READ FIRST

Generate EXACTLY these 3 sections in this order:
1. **Predicted Breakages** (3-7 issues max)
2. **Risk Assessment** (single table)
3. **Manual Test Plan** (test sessions with checkboxes)

**Total length: 300 lines maximum**

All other sections are FORBIDDEN unless explicitly valuable for THIS deployment.

---

## When to Use This Skill
- User mentions: "QA test plan", "CSS conflicts", "analyze CSS for [customer]"
- Customer CSS deployment scenarios
- Pre-deployment risk assessment

---

## Analysis Workflow

### Step 1: Read Customer CSS
- Location: `src/customers/[customer]/custom.css`
- Flag: Global selectors, !important, element selectors

### Step 2: Read Application Styles
- Core: `src/app/@core/components/`
- Theme: `src/app/@theme/`
- Pages: `src/app/pages/`

### Step 3: Detect Conflicts
- Compare selectors
- Check specificity + !important
- Predict cascade issues

### Step 4: Check Git History
- Search: "CSS", "style", "[customer name]"
- Find patterns from past bugs

### Step 5: Generate Report
Follow exact format below.

---

## REQUIRED OUTPUT FORMAT

**File:** `risk reports/qa_test_report_[customer].md`

**Structure (STRICT):**
````markdown
# QA Test Report - [Customer] CSS Deployment

## 🔍 Predicted Breakages

### Issue #1: [Short Title]
**Severity:** 🔴 CRITICAL
**Priority:** P1
**Confidence:** 95%

**What Breaks:**
- Component: [name]
- Expected: [normal behavior]
- After deploy: [broken behavior]

**Root Cause:**
```css
/* problematic CSS */
```

**Impact:**
- User: [how affected]
- Business: [consequences]

**Where to Test:**
- Page 1
- Page 2

**Test Steps:**
1. Navigate to [page]
2. Check [element]
3. Expected: [result]
4. If broken: [what happens]

[Repeat for issues #2-7 max]

---

## 📊 Risk Assessment

| Issue | Severity | Priority | Confidence | Impact |
|-------|----------|----------|------------|--------|
| [Issue 1] | 🔴 CRITICAL | P1 | 95% | [desc] |
| [Issue 2] | 🟡 HIGH | P2 | 90% | [desc] |

**Severity Key:**
- 🔴 CRITICAL: App unusable, blocks deployment
- 🟡 HIGH: Major visual/functional issue
- 🟢 MEDIUM: Minor issue, workarounds exist
- ⚪ LOW: Negligible impact

---

## 📋 Manual Test Plan

### Test Session 1: Critical Issues (XX min)

**Setup:**
- Browser: Chrome (latest)
- Environment: Test

#### Test 1.1: [Test Name]
- [ ] Step 1: [action]
- [ ] Step 2: [action]
- [ ] Expected: [result]
- [ ] If broken: [report what]
- [ ] Stop condition: Yes/No

[Repeat for sessions 2-3 max]

---
**END OF REPORT**
````

---

## Optional Sections (Use Sparingly)

Include ONLY if critically valuable:

- **Executive Summary** (2-3 lines) - Deploy yes/no at top
- **Stop Conditions** - When to halt testing
- **Time Estimates** - Per session only

Do NOT add:
- Screenshots checklists
- Bug templates
- Historical context
- Reference info
- Success criteria
- Contact info
- Execution logs
- ASCII diagrams

---

## Severity Guidelines

**Confidence:**
- 100%: Same selector + !important
- 90-95%: Global selector
- 80-90%: Similar selectors
- 70-80%: Potential conflict
- <70%: Low risk

**Priority:**
- P1: Blocks deployment
- P2: Test before deploy
- P3: Document only

---

## Best Practices

1. Check git history for patterns
2. Focus on: `button`, `input`, `div`, element selectors
3. Any `!important` = red flag
4. Global selectors = dangerous
5. Keep report under 300 lines

---

## Output Checklist

Before saving, verify:
- [ ] Only 3 main sections
- [ ] 3-7 issues max
- [ ] Under 300 lines
- [ ] No forbidden sections
- [ ] Saved to: `risk reports/qa_test_report_[customer].md`

---

## Example Output Length
````
# QA Test Report - CustomerB CSS
## Predicted Breakages (7 issues × 20 lines = 140 lines)
## Risk Assessment (table = 15 lines)
## Manual Test Plan (3 sessions × 30 lines = 90 lines)
---
Total: ~250 lines ✅
````

---