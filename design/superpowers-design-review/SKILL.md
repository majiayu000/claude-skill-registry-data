---
name: superpowers-design-review
description: >
  Design audit tool that crawls a live site, screenshots every page, runs a 10-category
  checklist (including AI slop detection), and iteratively fixes issues with atomic commits.
  For reviewing plans before implementation, use /superpowers-plan-design-review instead.
  Use when asked to "audit this site", "design review", "check the UI", or "visual QA".
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
  - WebSearch
---

> **DEPRECATED** — use `/design-review` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Design Review — Live Site Visual Audit

**Purpose:** Systematically audit a deployed website. Screenshot every page, run a
10-category checklist including AI slop detection, and fix issues iteratively with
atomic commits.

**NOTE:** This skill requires a running browse daemon. If not available, use
`/superpowers-plan-design-review` for plan-stage reviews instead.

---

## Modes

| Mode | When to use | Scope |
|------|-------------|-------|
| **Full** | Default when URL provided | All pages, all categories |
| **Quick** (`--quick`) | 30-second smoke test | Key pages, critical categories only |
| **Diff-aware** | On feature branch | Only changed pages/routes |

---

## Phase 0: Setup

### Detect browse daemon
```bash
~/.claude/skills/agent-browser/browse --version 2>/dev/null || \
  ~/.claude/skills/agent-browser/setup 2>/dev/null || \
  echo "BROWSE_NOT_FOUND"
```

If `BROWSE_NOT_FOUND`: AskUserQuestion:
> "The browse daemon isn't available. Options:
> - A) Run `~/.claude/skills/agent-browser/setup` to install it (recommended)
> - B) Use /superpowers-plan-design-review instead (plan-stage, no live site needed)"

### Parse args
- URL: provided or ask via AskUserQuestion
- Mode: full / quick / diff-aware
- Branch: auto-detect via `git rev-parse --abbrev-ref HEAD`

### Create output dirs
```bash
SLUG=$(echo "$URL" | sed 's|https\?://||' | cut -d'/' -f1 | cut -d':' -f1)
DATE=$(date +%Y%m%d-%H%M%S)
OUTDIR=~/.claude/.context/design-reviews/$SLUG-$DATE
mkdir -p $OUTDIR/screenshots $OUTDIR/evidence
echo "OUTDIR: $OUTDIR"
```

---

## Phase 1: First Impression

Open the site. Screenshot the hero/first viewport.

Assess (no checklist yet — just gut reaction):
1. What does this site DO? Can you tell in 5 seconds?
2. What does it FEEL like? (professional, playful, corporate, startup, etc.)
3. What's the single strongest visual element?
4. What's the first thing that feels off?

Log first impressions to `$OUTDIR/first-impressions.md`.

---

## Phase 2: Design System Extraction

Screenshot key pages. Extract the design system from what's built:

1. **Color:** Screenshot and describe primary, accent, background, text colors. Identify CSS custom properties if visible.
2. **Typography:** What fonts? (heading, body, mono) What sizes? What weights?
3. **Spacing:** What spacing scale is used? (4px, 8px, etc.)
4. **Borders/radius:** What corner radius? Border width?
5. **Shadows:** What shadow style?
6. **Motion:** Any animations observed? (entrance, hover, transition)
7. **Iconography:** Style of icons? (outline, filled, brand-specific)

Document findings in `$OUTDIR/design-system.md`.

---

## Phase 3: Visual Audit

Screenshot every page. For each page, evaluate:

### 10-Category Audit Checklist

| # | Category | What to check |
|---|----------|---------------|
| 1 | First Impression | Hero composition, brand clarity, visual anchor |
| 2 | Typography | Font choices, hierarchy, readability, no default stacks |
| 3 | Color | Consistency, contrast, CSS variables, no generic AI palettes |
| 4 | Layout | Intentional structure, not just stacked cards |
| 5 | Imagery | Photos/images feel authentic vs stock/AI-generated |
| 6 | Spacing | Consistent rhythm, no random padding |
| 7 | Interactions | Hover states, transitions, loading states |
| 8 | Responsive | Mobile/tablet intentional, not just stacked |
| 9 | Accessibility | Keyboard nav, focus states, contrast |
| 10 | AI Slop Detection | Hard rejection patterns (see below) |

### AI Slop Detection — Hard Rejections
Flag if ANY apply:
1. Generic SaaS card grid as first impression
2. Beautiful image with weak brand
3. Strong headline with no clear action
4. Busy imagery behind text
5. Sections repeating same mood statement
6. Carousel with no narrative purpose
7. App UI made of stacked cards instead of layout
8. Purple/violet gradient backgrounds
9. 3-column icon-in-circle feature grid
10. Centered everything (`text-align: center` on all headings)

### AI Slop Scoring
Rate the site 0-10 on "how AI-generated does this feel":
- 0-3: Intentionally designed, feels handcrafted
- 4-6: Mix of intentional and generic patterns
- 7-10: Obviously template-generated

---

## Phase 4: Interaction Flows

Test the primary user journeys. For each flow:
1. Start-to-end screenshot the happy path
2. Test: empty state, error state, loading state
3. Note: what does the user see at each step?
4. Time: how long does each step take visually?

Document flows in `$OUTDIR/interaction-flows.md`.

---

## Phase 5: Cross-Page Consistency

Compare screenshots across pages:
- Are fonts consistent?
- Are colors used the same way?
- Do buttons behave the same?
- Is spacing consistent?
- Are empty states handled consistently?

Flag inconsistencies in `$OUTDIR/consistency-report.md`.

---

## Phase 6: Triage

After all evidence is collected, triage findings:

**Categorize each finding:**
- **CRITICAL:** Breaks the experience or causes data loss risk
- **HIGH:** Significant UX or visual quality issue
- **MEDIUM:** Improvement opportunity
- **LOW:** Polish item

**Format:**
```
FINDING: [description]
Page: [URL]
Category: [CRITICAL/HIGH/MEDIUM/LOW]
AI Slop: [yes/no]
Fix: [what needs to change]
```

Sort by priority. Flag AI slop findings separately.

---

## Phase 7: Fix Loop

For each CRITICAL and HIGH finding:

1. **Screenshot before** → save to `$OUTDIR/evidence/`
2. **Fix the issue** — make the smallest possible change that resolves it
3. **Screenshot after** → save to `$OUTDIR/evidence/`
4. **Commit** with message: `[design-fix] {one-line description}`

### Fix Loop Rules
- One commit per fix (atomic)
- Before/after screenshots for every fix
- Risk cap: if a fix requires structural changes (3+ files, new components), ask via AskUserQuestion before proceeding
- If git state is dirty at start, ask to stash or abort — no work on dirty state
- If git state becomes dirty mid-loop with uncommitted changes, pause and ask

---

## Phase 8: Final Report

Generate `$OUTDIR/REPORT.md`:

```
DESIGN REVIEW REPORT
====================
Site: {URL}
Date: {date}
Mode: {full/quick/diff-aware}
Branch: {branch}

SCORES
======
Overall Design Quality: __/10
AI Slop Risk: __/10
First Impression: __/10

CATEGORIES
==========
1. First Impression:  __/10
2. Typography:        __/10
3. Color:             __/10
4. Layout:            __/10
5. Imagery:           __/10
6. Spacing:           __/10
7. Interactions:       __/10
8. Responsive:         __/10
9. Accessibility:     __/10
10. AI Slop Detection: __/10

FINDINGS SUMMARY
================
Critical: N
High: N
Medium: N
Low: N
Fixed: N (during review)

TOP ISSUES
==========
1. [issue] — [status: fixed/not fixed]
2. [issue] — [status: fixed/not fixed]

RECOMMENDATIONS
===============
[Priority list of remaining issues to address]

VERDICT: [CLEAR / NEEDS_WORK / CRITICAL]
```

---

## Review Log

```bash
mkdir -p ~/.claude/.context
echo '{"skill":"design-review","timestamp":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","status":"STATUS","site":"'"$SLUG"'","score":N,"critical":N,"high":N,"fixed":N}' >> ~/.claude/.context/reviews.jsonl
```

STATUS: "clean" if 0 critical and 0 high; "issues_found" otherwise

---

## Cleanup

After all fixes committed:
```bash
echo "Design review complete. $N issues found, $M fixed."
echo "Report: $OUTDIR/REPORT.md"
echo "Screenshots: $OUTDIR/screenshots/"
```

---

## Completion Status

- **DONE** — Full audit complete, all critical/high issues fixed, report generated
- **DONE_WITH_CONCERNS** — Audit complete but some issues deferred
- **BLOCKED** — Browse daemon not available
- **NEEDS_CONTEXT** — Missing URL or cannot access the site
