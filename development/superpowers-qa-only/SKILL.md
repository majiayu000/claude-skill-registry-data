---
name: superpowers-qa-only
description: >
  Report-only QA testing. Systematically tests a web application and produces a
  structured report with health score, screenshots, and repro steps — but never
  fixes anything. Use when asked to "just report bugs", "qa report only", or
  "run QA without making changes".
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
  - WebSearch
---

> **DEPRECATED** — use `/qa-only` instead. This skill is a legacy alias and will be removed in a future cleanup.
# QA Only — Report Without Fixing

**Purpose:** Test a web application and produce a structured report. Screenshots,
repro steps, health score. **Never makes any code changes.**

**Key rule:** This skill is read-only. No fixes. No test framework detection. No
attempt to write tests. Just observe and report.

---

## Modes

| Mode | Trigger | Scope |
|------|---------|-------|
| **Full** | URL provided, no flags | All pages, all categories |
| **Quick** | `--quick` flag | Key pages, critical categories only (30s) |
| **Diff-aware** | On feature branch, no URL | Only changed files/routes from git diff |
| **Regression** | `--regression <baseline>` | Compare against prior baseline.json |

---

## Phase 1: Initialize

### Detect browse daemon
```bash
~/.claude/skills/agent-browser/browse --version 2>/dev/null || \
  ~/.claude/skills/agent-browser/setup 2>/dev/null || \
  echo "BROWSE_NOT_FOUND"
```

If `BROWSE_NOT_FOUND`: Offer to install or exit.

### Parse inputs
- URL: provided, or from git diff (diff-aware mode), or ask via AskUserQuestion
- Mode: full / quick / diff-aware / regression
- Branch: `git rev-parse --abbrev-ref HEAD`

### Create output dirs
```bash
SLUG=$(echo "$URL" | sed 's|https\?://||' | cut -d'/' -f1 | cut -d':' -f1)
DATE=$(date +%Y%m%d-%H%M%S)
MODE_DIR=$(echo "$MODE" | tr '[:upper:]' '[:lower:]')
OUTDIR=~/.claude/.context/qa-reports/$SLUG-$MODE_DIR-$DATE
mkdir -p $OUTDIR/screenshots $OUTDIR/evidence
echo "OUTDIR: $OUTDIR"
```

### Diff-aware mode
If on a feature branch with no URL:
```bash
git diff --name-only $(git merge-base HEAD main 2>/dev/null || git rev-parse --abbrev-ref HEAD^) | head -20
```
Identify changed routes/pages. Ask via AskUserQuestion: "Found N changed files. Which pages should I test?" Options: test all / specify pages.

### Regression mode
```bash
BASELINE="$1"
if [ -f "$BASELINE" ]; then
  echo "Loading baseline from $BASELINE"
else
  echo "Baseline not found: $BASELINE"
fi
```

---

## Phase 2: Authenticate (if needed)

Check if login is required:
```bash
~/.claude/skills/agent-browser/browse --navigate "$URL" 2>/dev/null | head -5
```

If auth form detected:
AskUserQuestion:
> "The site requires authentication. Options:
> - A) Provide credentials (I will use them to log in, then discard)
> - B) Provide a session cookie/token
> - C) Skip auth-required pages
> - D) Cancel QA run"

Handle 2FA and CAPTCHA honestly: note if present, do not attempt to bypass.

---

## Phase 3: Orient

Before testing, understand what you're looking at:

1. **Snapshot:** Screenshot the homepage and primary entry point
2. **Framework detection:** Check for Next.js, React, Vue, Rails, WordPress indicators
3. **Links inventory:** Discover primary navigation and key pages
4. **Console errors:** Check for JavaScript errors at load
5. **Performance baseline:** Initial load time estimate

Document in `$OUTDIR/orient.md`.

### Framework-specific guidance
- **Next.js:** Check `/admin`, `/dashboard`, `/settings` routes; test ISR/SSR behavior
- **Rails:** Check `/admin`, Devise auth flows; test ActiveRecord error pages
- **WordPress:** Check `/wp-admin` exposure; test Gutenberg editor states
- **General SPA:** Test client-side routing, deep links, 404 handling

---

## Phase 4: Explore

For each page discovered:

### Per-page checklist:

**Visual:**
- Does the page render correctly?
- Are images/fonts loading?
- Is layout consistent across viewports?

**Interactive:**
- Do buttons respond to click?
- Do forms accept input?
- Do dropdowns/menus open/close?
- Do modals open/close?
- Does navigation work?

**Forms:**
- Validation messages appear?
- Required fields enforced?
- Submit works?
- Error states render?

**States:**
- Loading states exist?
- Empty states handled?
- Error states user-friendly?

**Console:**
- Any JavaScript errors?
- Any console warnings?

**Responsive:**
- Usable on mobile?
- Keyboard nav works?
- Touch targets >= 44px?

---

## Phase 5: Document

For each bug found, create evidence:

**Tier 1 — Interactive bugs (screenshot before + after):**
```
BUG: [title]
Page: [URL]
Severity: [CRITICAL/HIGH/MEDIUM/LOW]

STEPS TO REPRODUCE:
1. [step]
2. [step]
3. [step]

EXPECTED: [what should happen]
ACTUAL: [what happens instead]

Evidence:
- Before: screenshots/bug-N-before.png
- After: screenshots/bug-N-after.png
```

**Tier 2 — Static bugs (annotated screenshot):**
```
BUG: [title]
Page: [URL]
Severity: [CRITICAL/HIGH/MEDIUM/LOW]

DESCRIPTION: [one paragraph]

Evidence:
- Annotated: evidence/bug-N-annotated.png
```

---

## Phase 6: Health Score

Calculate weighted health score:

```
HEALTH SCORE RUBRIC
===================
Console Errors:     15% — JS errors, warnings, failed requests
Functional:         20% — broken buttons, forms, navigation
Accessibility:      15% — keyboard nav, ARIA, contrast, touch targets
UX Quality:         15% — loading states, empty states, error messages
Visual Quality:     10% — layout, typography, imagery consistency
Links:              10% — broken links, 404s, dead navigation
Performance:        10% — load time, render blocking
Content:             5% — copy errors, missing text, placeholder content
```

Rate each category 0-10. Calculate weighted average.

---

## Phase 7: Wrap Up

### Generate report `$OUTDIR/qa-report.md`
```
QA REPORT
=========
Site: {URL}
Date: {date}
Mode: {full/quick/diff-aware/regression}
Branch: {branch}

HEALTH SCORE: {N}/100
  Console:    {N}/10 (15%)
  Functional: {N}/10 (20%)
  A11y:       {N}/10 (15%)
  UX:         {N}/10 (15%)
  Visual:     {N}/10 (10%)
  Links:      {N}/10 (10%)
  Performance:{N}/10 (10%)
  Content:     {N}/10 (5%)

TOP 3 ISSUES
=============
1. [title] — [severity] — [page]
2. [title] — [severity] — [page]
3. [title] — [severity] — [page]

CONSOLE SUMMARY
===============
[JS errors found] errors, [warnings] warnings

ALL FINDINGS
============
[Full bug list, sorted by severity]

REGRESSION COMPARISON (if --regression mode)
=============================================
New issues: N
Fixed issues: N
Regression issues: N

VERDICT: [CLEAR / NEEDS_WORK / CRITICAL]
```

### Save baseline
```bash
cp $OUTDIR/qa-report.md $OUTDIR/baseline.json 2>/dev/null || true
```

---

## Review Log

```bash
mkdir -p ~/.claude/.context
echo '{"skill":"qa-only","timestamp":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","status":"STATUS","site":"'"$SLUG"'","mode":"'"$MODE"'","health_score":N,"critical":N,"high":N,"medium":N,"low":N}' >> ~/.claude/.context/reviews.jsonl
```

STATUS: "clean" if 0 critical AND 0 high; "issues_found" otherwise

---

## QA-Only Rules

1. **Never fix bugs.** Observe and document only.
2. **Never write tests.** Don't detect test frameworks or suggest test cases.
3. **Never change code.** No edits, no commits, no automated fixes.
4. **Screenshots are evidence.** Every finding needs visual proof.
5. **Repro steps must work.** If you can't reproduce it consistently, note uncertainty.

---

## Completion Status

- **DONE** — Full QA complete, report generated with all evidence
- **DONE_WITH_CONCERNS** — QA complete but some areas couldn't be tested (auth blocked, etc.)
- **BLOCKED** — Cannot access the site
- **NEEDS_CONTEXT** — Missing URL and no git diff available
