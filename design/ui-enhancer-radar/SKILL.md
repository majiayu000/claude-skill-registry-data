---
name: ui-enhancer-radar
description: 'Systematic iOS/SwiftUI UI audit with design intent interview, 14-domain analysis (including Color Audit with adaptive Color Profile, iPad Sheet Sizing caller-side audit, Button Hit Region three-factor interaction audit, and Silent Picker menu-presentation audit), element compaction, cross-view consistency checks, layout reorganization, design-aware push-back, App Store guardrails, and incremental apply with revert safety. Run /ui-enhancer-radar help for all commands. Triggers: "enhance this UI", "ui enhancer radar", "improve this view", "screen review", "ux audit", "ipad sheet truncation", "button not tappable on iPad", "picker does nothing".'
version: 3.6.0  # Domain 9 externalized to reference/ (proof-of-pattern for inline-domain migration) + Color Audit (11) + iPad sheet sizing (12) + button hit region (13) + silent picker (14) + visual inspection gate + App Store guardrails + view profile + refinement loop + cross-view consistency
author: Terry Nyberg
license: Apache-2.0
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion]
inherits: radar-suite-core.md
metadata:
  tier: execution
  category: ux
---

# UI Enhancer Radar

> **Quick Ref:** Screenshot + code analysis of any iOS/SwiftUI view. Design intent interview (sacred elements, aggressiveness), 14-domain analysis with layout reorganization, Color Audit (adaptive Color Profile), iPad Sheet Sizing caller-side audit, Button Hit Region three-factor audit, and Silent Picker menu-presentation audit, element compaction (compact vs remove vs keep), cross-view consistency checks, design-aware refinement with push-back and App Store guardrails, incremental apply with revert safety (git or file backup), visual verification guidance, and files-changed summary.

<ui-enhancer-radar>

You are performing a systematic UI enhancement on a specific iOS/SwiftUI view, analyzing both the visual screenshot and the underlying code, then implementing improvements with tests.

**Required output:** Every finding MUST include a severity rating (Critical / High / Medium / Low) and estimated implementation effort (Trivial / Small / Medium / Large).

## Quick Commands

| Command | Description |
|---------|-------------|
| `/ui-enhancer-radar` | Full audit with interview |
| `/ui-enhancer-radar space` | Space efficiency analysis only |
| `/ui-enhancer-radar hierarchy` | Visual hierarchy analysis only |
| `/ui-enhancer-radar density` | Information density analysis only |
| `/ui-enhancer-radar interaction` | Interaction patterns analysis only |
| `/ui-enhancer-radar accessibility` | Accessibility audit only |
| `/ui-enhancer-radar hig` | HIG compliance check only |
| `/ui-enhancer-radar dark-mode` | Dark mode audit only |
| `/ui-enhancer-radar performance` | Performance impact analysis only |
| `/ui-enhancer-radar design-system` | Design system compliance only |
| `/ui-enhancer-radar color` | Color audit only (inventory, flatness, consistency) |
| `/ui-enhancer-radar ipad-sheets` | iPad sheet sizing audit only (caller-side `.sheet()` check) |
| `/ui-enhancer-radar hit-region` | Button hit region audit only (three-factor: .plain + Form/List + trailing chevron) |
| `/ui-enhancer-radar silent-picker` | Silent Picker audit only (menu Picker, no .pickerStyle, custom non-Form container) |
| `/ui-enhancer-radar compare` | Compare before/after screenshots for progress |
| `/ui-enhancer-radar revert` | Undo all changes back to last checkpoint |
| `/ui-enhancer-radar batch [path]` | Audit all views in a directory, rank by severity |
| `--show-suppressed` | Show findings suppressed by known-intentional entries |
| `--accept-intentional` | Mark current finding as known-intentional (not a bug) |
| `/ui-enhancer-radar --capture` | Capture screenshot from running simulator (optional) |
| `/ui-enhancer-radar --devices` | Analyze layout across device sizes (optional) |
| `/ui-enhancer-radar fix-deferred` | Resolve items deferred from a previous run |
| `/ui-enhancer-radar verify` | Re-check previous findings without full re-audit (~5 min) |

---

## Help Command

**If the user runs `/ui-enhancer-radar help`**, display this command reference and stop (do not start an audit):

```
UI Enhancer — Available Commands

FULL AUDIT
  /ui-enhancer-radar              Full 14-domain audit with interview

SINGLE DOMAIN (skip interview, run one domain)
  /ui-enhancer-radar space        Space efficiency analysis
  /ui-enhancer-radar hierarchy    Visual hierarchy analysis
  /ui-enhancer-radar density      Information density analysis
  /ui-enhancer-radar interaction  Interaction patterns analysis
  /ui-enhancer-radar accessibility  Accessibility audit
  /ui-enhancer-radar hig          HIG compliance check
  /ui-enhancer-radar dark-mode    Dark mode audit
  /ui-enhancer-radar performance  Performance impact analysis
  /ui-enhancer-radar design-system  Design system compliance
  /ui-enhancer-radar color        Color audit (inventory, flatness, consistency)
  /ui-enhancer-radar ipad-sheets  iPad sheet sizing audit (caller-side `.sheet()` check)
  /ui-enhancer-radar hit-region   Button hit region audit (.plain + chevron + Form/List)

UTILITIES
  /ui-enhancer-radar compare      Compare before/after screenshots
  /ui-enhancer-radar revert       Undo all changes back to checkpoint
  /ui-enhancer-radar batch [path] Audit all views in a directory
  /ui-enhancer-radar help         Show this command list

OPTIONS (combine with any command)
  --capture                 Capture screenshot from running simulator
  --devices                 Analyze layout across device sizes
```

---

## First-Run Hint

When `/ui-enhancer-radar` is invoked with no subcommand, display this hint **once** before the Phase 1 interview (not on subsequent runs in the same session):

> Tip: Run `/ui-enhancer-radar help` to see all available commands, or continue for a full audit.

Then proceed directly to Phase 1.

---

## Skill Introduction (MANDATORY — run before anything else)

**This section replaces `radar-suite-core.md § Session Setup` for the ui-enhancer-radar entry point.** Do NOT also run core's 4-question Session Setup — its questions are consolidated below. Phase 1 ("Interview") below reuses the answers captured here and does NOT re-ask experience level, fix mode, or attendance.

On first invocation, ask all setup questions in a single `AskUserQuestion` call:

**Question 1: "What's your experience level with Swift/SwiftUI?"**
- **Beginner** — New to Swift. Plain language, analogies, define terms on first use.
- **Intermediate** — Comfortable with SwiftUI basics. Standard terms, explain non-obvious patterns.
- **Experienced (Recommended)** — Fluent with SwiftUI. Concise findings, no definitions.
- **Senior/Expert** — Deep expertise. Terse, file:line only, skip explanations.

**Question 2: "How should fixes be handled?"**
- **Auto-fix safe items (Recommended)** — Apply isolated, low-blast-radius fixes automatically. Present cross-cutting fixes and design decisions for approval first.
- **Review first** — Present all findings with ratings, then ask before making any changes. Fixes still happen — you just approve each wave first.
- **Batch mode** — Approve all fixes in each wave at once.

**IMPORTANT:** All three modes lead to fixes. "Review first" means the user sees the plan before code changes — it does NOT mean "skip fixes and jump to handoff." After presenting findings, ALWAYS offer to fix them regardless of which mode was selected. (Exception: Hands-Free mode overrides this — see Question 3.)

**Question 3: "Will you be stepping away during the audit?"**
- **I'll be here (Recommended)** — Normal mode. Permission prompts may appear for writes/edits.
- **Hands-Free (walk away safe)** — Read-only analysis only (Read, Grep, Glob). No edits, no Bash, no prompts. **Hands-Free overrides Question 2:** all fixes are deferred regardless of `FIX_MODE`. Phase 7b (Visual Inspection Gate) is skipped — no code changes will be applied. The skill emits the saved playbook and Hands-Free completion message instead of the next-phase `AskUserQuestion` (see § Hands-Free Mode below for full precedence rules).
- **Pre-Approved** — You have already configured Claude Code permissions for this session. Run at full speed without restriction.

Store as: `USER_EXPERIENCE`, `FIX_MODE`, `PRESENCE_MODE`. Apply to ALL output for the session, per `radar-suite-core.md § Experience-Level Output Rules`. Also persist to `.radar-suite/session-prefs.yaml` per `radar-suite-core.md § Session Persistence`.

**Question 4 (optional follow-up): "Would you like a brief explanation of what this skill does?"**
- **No, let's go (Recommended)** — Skip explanation, proceed to Phase 1 (Interview).
- **Yes, explain it** — Show one of the explanations below adapted to experience level, then proceed.

**Experience-adapted explanations for UI Enhancer:**

- **Beginner**: "UI Enhancer is like having a professional designer review every screen in your app. It checks 14 different things — spacing, colors, accessibility, layout efficiency, iPad sheet sizing, button hit regions, and more — then suggests specific improvements. It won't just say 'this looks wrong'; it'll show you exactly what to change and why. It works one view at a time, applying changes incrementally so you can undo anything."

- **Intermediate**: "UI Enhancer performs a 14-domain analysis of SwiftUI views: layout, spacing, color accessibility, typography, element compaction, cross-view consistency, iPad sheet sizing, button hit regions, and more. It interviews you about design intent first, then audits against Apple HIG and your app's design system. Changes are applied incrementally with revert safety."

- **Experienced**: "14-domain SwiftUI UI audit with design intent interview, adaptive color profiles, element compaction, cross-view consistency checks, iPad sheet sizing caller-side audit, button hit region three-factor audit, silent picker menu-presentation audit, layout reorganization, App Store guardrails, and incremental apply with revert safety. Run `/ui-enhancer-radar help` for the full command list."

- **Senior/Expert**: "14-domain view audit: layout, color, typography, spacing, compaction, consistency, accessibility, iPad sheet sizing, button hit region, silent picker. Interview → analyze → apply incrementally."

Store the experience level as `USER_EXPERIENCE` and apply to ALL output for the session.

**User impact explanations:** Can be toggled at any time with `--explain` / `--no-explain`. When enabled, each finding gets a 3-line companion explanation (what's wrong, fix, user experience before/after). See the shared rating system doc for format and rules. Store as `EXPLAIN_FINDINGS` (default: false).

**Experience-level auto-apply:** If `USER_EXPERIENCE` = Beginner, auto-set `EXPLAIN_FINDINGS = true` and default sort to `impact`. If Senior/Expert, default sort to `effort`. Apply all output rules from Experience-Level Output Rules table in `radar-suite-core.md`.

---

## Shared Patterns

See `radar-suite-core.md` for: Tier System, Pipeline UX Enhancements, Table Format, Plain Language Communication, Work Receipts, Contradiction Detection, Finding Classification, Audit Methodology, Context Exhaustion, Progress Banner, Issue Rating Tables, Handoff YAML schema, Known-Intentional Suppression, Pattern Reintroduction Detection, Experience-Level Output Rules, Implementation Sort Algorithm, short_title requirement.

## Pre-Scan Startup (MANDATORY — before any domain scan)

1. **Known-intentional suppression:** Run the protocol in `radar-suite-core.md § Known-Intentional Suppression`. Core owns this — do not restate the steps here.

2. **Pattern reintroduction detection:** Run the protocol in `radar-suite-core.md § Pattern Reintroduction Detection`. Core owns this.

---

## Phase 1: Interview

Before analyzing, run a brief intake to focus the audit on what matters most.

**Experience level was already captured in § Skill Introduction (Question 1). Do NOT re-ask it here. The questions below are content-specific to ui-enhancer-radar's audit shape — focus, priority, design intent, aggressiveness.**

**Display this instruction before the first set of questions:**

> To answer, type the option labels (e.g., "General polish, All domains, Moderate") or use numbers (e.g., "1, 1, 1"). You can answer all questions at once or one at a time.

```
questions:
[
  {
    "question": "What's the main reason for this review?",
    "header": "Focus",
    "options": [
      {"label": "General polish (Recommended)", "description": "No specific complaint \u2014 just want it to be better"},
      {"label": "Specific problem", "description": "Users or I have noticed something wrong"},
      {"label": "Pre-release review", "description": "Final check before shipping"},
      {"label": "Competitive parity", "description": "Want to match or exceed a competitor's UX"}
    ],
    "multiSelect": false
  },
  {
    "question": "Which aspects matter most right now?",
    "header": "Priority",
    "options": [
      {"label": "All domains (Recommended)", "description": "Full 14-domain analysis"},
      {"label": "Visual \u2014 layout and hierarchy", "description": "Space, visual weight, information density"},
      {"label": "Interaction \u2014 usability", "description": "Touch targets, discoverability, feedback"},
      {"label": "Technical \u2014 performance and compliance", "description": "Dark mode, perf, HIG, design system"}
    ],
    "multiSelect": false
  }
]
```

**If "Specific problem"**, follow up:

```
questions:
[
  {
    "question": "What's the specific issue?",
    "header": "Issue",
    "options": [
      {"label": "Too much wasted space (most common)", "description": "Content doesn't start until halfway down the screen"},
      {"label": "Hard to find things", "description": "Users can't discover features or actions"},
      {"label": "Looks cluttered or confusing", "description": "Too much competing for attention"},
      {"label": "I'll describe it", "description": "Let me explain the problem"}
    ],
    "multiSelect": false
  }
]
```

**If "Competitive parity"**, ask for a competitor screenshot to enable Domain 10 (Competitive Comparison).

### Design Intent (always ask)

After the focus/priority questions, always ask about design intent and change aggressiveness:

```
questions:
[
  {
    "question": "Are there elements on this screen you consider essential to its identity — things that should be preserved even if they use extra space?",
    "header": "Identity",
    "options": [
      {"label": "No sacred elements (Recommended)", "description": "Everything is fair game for optimization"},
      {"label": "Yes, I'll point them out", "description": "I'll identify specific elements to preserve"},
      {"label": "Keep all branding/headers", "description": "Preserve illustrated headers, icons, and branded sections"},
      {"label": "Not sure — show me options", "description": "Offer compact vs remove for each visual element"}
    ],
    "multiSelect": false
  },
  {
    "question": "How aggressive should changes be?",
    "header": "Aggressiveness",
    "options": [
      {"label": "Moderate (Recommended)", "description": "Compact where possible, remove only clear redundancies"},
      {"label": "Conservative", "description": "Tighten spacing and compact only — never remove elements"},
      {"label": "Aggressive", "description": "Maximize space — remove anything non-essential"}
    ],
    "multiSelect": false
  }
]
```

### Attendance

Attendance mode (`PRESENCE_MODE`) was already captured in § Skill Introduction (Question 3). Do NOT re-ask here. The Hands-Free Mode section below documents precedence rules for write-tool deferral and `AskUserQuestion` suppression.

### Hands-Free Mode (precedence rules — load-bearing)

When `PRESENCE_MODE = Hands-Free`:

1. **Hands-Free overrides `FIX_MODE`.** Even if Question 2 was answered `Auto-fix safe items`, `Review first`, or `Batch mode`, no fixes are applied in Hands-Free mode. All findings are emitted with `Status: Deferred (hands-free)` in the Issue Rating table. The Fix Plan, Report (Phase 6), and Playbook (Phase 7) are still produced — they're held in the conversation for the user to act on when they return.
2. **Phase 7b (Visual Inspection Gate) is skipped.** Since no code changes will be applied, the gate has nothing to protect. The skill emits the saved playbook to `.agents/ui-enhancer-radar/[date]-[view]-playbook.md` and prints the completion message below.
3. **Phase 7c-7f are deferred.** Guided Visual Review, Apply Approved Changes, Pattern Sweep, and Refinement Loop all require interactive user prompts (`AskUserQuestion`) and/or write tools. None of these run in Hands-Free.
4. **BLOCKING progress banner exception.** The "CRITICAL — BLOCKING requirement" for the next-phase `AskUserQuestion` (§ Phase Progress Banner) applies in Normal and Pre-Approved modes only. In Hands-Free, the progress banner still prints after each completed phase, but the `AskUserQuestion` is suppressed in favor of the completion message.
5. **Handoff YAML emitted inline.** Writing `.agents/ui-audit/ui-enhancer-radar-handoff.yaml` and `.radar-suite/ledger.yaml` requires Edit/Write — forbidden in Hands-Free. The skill emits these as fenced YAML blocks inline in the conversation so the user can persist them on return.

Hands-Free completion message:
```
⏱ Hands-free audit complete through Phase 5 (Domain Analysis) + Phase 6 (Report).
  Phases skipped (deferred until you return): 7a-7f (apply), 8 (tests), 9 (summary).
  Findings deferred: [count] (no fixes applied — Hands-Free mode)
  Playbook saved: .agents/ui-enhancer-radar/[date]-[view]-playbook.md
  Handoff YAML + ledger entries: emitted inline above; copy to .agents/ui-audit/ and .radar-suite/ when you return
  Reply to continue with supervised phases.
```

When `PRESENCE_MODE = Pre-Approved`: full speed, no restrictions. Assumes permissions are configured per the Permission Setup guide below. All phases run normally.

### Permission Setup (for unattended runs)

To avoid permission prompts during audits, pre-allow these read-only patterns in Claude Code settings. Safe to auto-approve — they cannot modify your codebase:

```
# Already safe by default (no setup needed):
Read, Grep, Glob — always auto-approved

# Add these for unattended Bash scans:
Bash(find:*)
Bash(wc:*)
Bash(stat:*)
```

**Do NOT auto-approve** (keep prompted — they modify state):
```
Edit, Write — file modifications
Bash(rm:*), Bash(git:*) — destructive operations
```

**After all questions, always offer:**

> Anything else I should know? (design preferences, constraints, specific elements to preserve — or press Enter to skip)

Record any free-text input as additional constraints that apply throughout the audit. For example: "Preserve saturation and hue of card backgrounds" becomes a constraint checked during every finding.

**If "Yes, I'll point them out"** — ask the user to describe or screenshot the sacred elements. Tag them as `[PRESERVE]` in the findings table and default to compaction (Phase 6c) rather than removal.

**If "Keep all branding/headers"** — mark all illustrated headers, SheetHeaders, ContentIllustratedHeaders, and branded sections as `[PRESERVE]`. Only recommend compaction for these, never removal.

**If "Not sure — show me options"** — for every visual element, present the full Phase 6c compaction menu (compact / remove / keep).

### Aggressiveness calibration

The aggressiveness setting affects all findings throughout the audit:

| Setting | Spacing | Headers | Decorative elements | Redundant info |
|---|---|---|---|---|
| **Conservative** | Tighten 10-20% | Compact only | Keep, reduce size | Merge, don't remove |
| **Moderate** | Tighten 20-40% | Compact (default), remove if redundant | Compact or remove | Remove if truly duplicate |
| **Aggressive** | Minimize to HIG minimum | Remove unless `[PRESERVE]` | Remove | Remove |

The interview determines:
- Which domains to run (all 14, or a focused subset)
- Severity weighting (user-reported problems get Critical minimum)
- Whether to include competitive comparison
- Which elements are sacred (`[PRESERVE]` tag)
- How aggressive to be with changes (Conservative / Moderate / Aggressive)
- How to pitch explanations (experience level)

### Experience-Level Adaptation

Adjust ALL output (findings, questions, recommendations, compaction options) based on the user's experience level:

- **Beginner**: Plain language, real-world analogies. "This header takes up 120 points of space — that's about a third of the visible screen on an iPhone. Compacting it would let users see their content sooner." Define SwiftUI terms on first use. When presenting compaction options, explain what each choice means visually.
- **Intermediate**: Standard SwiftUI terminology, explain non-obvious tradeoffs. "The `SheetHeader` uses 120pt — compacting to inline icon+title saves 80pt and keeps the visual identity. The `.stuffolioCard()` modifier handles the styling." Explain architectural choices but not basic concepts.
- **Experienced** (default): Concise findings. "SheetHeader: 120pt → 40pt inline. Saves 80pt above fold." No definitions, focus on measurements and tradeoffs.
- **Senior/Expert**: Minimal. "SheetHeader 120→40pt. `.stuffolioCard()` handles styling. 3 files touched." Skip design rationale — just the change, the impact, and the blast radius.

---

## Phase 2: Gather Input

```
questions:
[
  {
    "question": "How would you like to provide the view to analyze?",
    "header": "Input",
    "options": [
      {"label": "Screenshot + file path (Recommended)", "description": "Deepest analysis \u2014 visual + structural"},
      {"label": "Screenshot only", "description": "Visual analysis, recommendations without code changes"},
      {"label": "File path only", "description": "Code analysis, structural improvements"},
      {"label": "Capture from simulator", "description": "I'll capture the screenshot automatically (optional)"}
    ],
    "multiSelect": false
  }
]
```

**If "Capture from simulator"** (optional feature):
```bash
xcrun simctl io booted screenshot /tmp/ui-enhancer-radar-capture.png
```
Then read the captured screenshot.

---

## Phase 2b: View Type Classification

**Before analyzing, classify the view type.** This determines severity weighting, compensation strategies, and domain-specific heuristics throughout the audit.

Classify by reading the code and/or screenshot. Do NOT ask the user — infer from evidence:

| View Type | How to Identify | Implications |
|-----------|----------------|--------------|
| **Dashboard / overview** | Aggregates data from multiple sources, cards/widgets, summary stats | Space efficiency is Critical; visual variety matters most |
| **Detail / inspector** | Shows one item's full data, sections of attributes | Information density is Critical; hierarchy matters most |
| **Form / input** | Text fields, pickers, toggles for data entry | Interaction patterns are Critical; keep chrome minimal |
| **List / table** | Repeating rows of similar items, search/filter | Density and performance are Critical; row height matters |
| **Help / reference** | Static instructional text, tips, guides | Space is Medium priority; visual richness prevents boredom |
| **Sheet / modal** | Presented modally for a focused task | Check for duplicate headers (SheetContainer + SheetHeader) |
| **Settings / config** | Toggles, preferences, grouped sections | HIG compliance is Critical; follow system patterns |

**Record the classification** at the top of the report (e.g., "View type: Help / reference (sheet)"). Reference it when:
- Choosing severity levels (Domain 1-11)
- Offering compaction alternatives (Phase 6c)
- Recommending compensation techniques (Phase 6d)
- Deciding whether a finding is worth fixing
- Applying platform-specific design heuristics (see below)

#### Platform-Specific Design Heuristics

When the view runs on multiple platforms, apply platform-appropriate design expectations:

| View Type | macOS (with sidebar) | iPhone (no sidebar) |
|---|---|---|
| **Dashboard** | Should be a *summary* — show stats, alerts, and insights. Navigation lives in sidebar. Feature cards that duplicate sidebar items are redundant. | Should be a *hub* — provide entry points to all features. No sidebar means the dashboard IS the navigation. |
| **Settings / config** | Settings items accessible via sidebar don't need dashboard cards. Theme toggle in header is optional if Settings is 1 click away. | Settings behind a tab or gear icon — header controls add convenience. |
| **Form / input** | Wider layout allows side-by-side fields. Keyboard toolbar not needed (Tab key navigation). | Keyboard Done toolbar is essential. Single-column layout. |
| **List / table** | Can show more columns, denser rows. Hover effects for interactivity. | Swipe actions, pull-to-refresh. Touch-optimized row height (44pt min). |

**How to apply:** After classifying the view type, check which platform the screenshot/code targets. If macOS with sidebar, apply the "summary" heuristic for dashboards. If iPhone, apply the "hub" heuristic. Flag findings that are platform-specific (e.g., "This redundancy only applies on macOS where the sidebar provides the same navigation").

---

## Phase 3: Screenshot Analysis

When a screenshot is provided, analyze it visually:

### 3a. First Impression (3-Second Test)
- What does the user see first? Is it what matters most?
- Can the user tell what this screen does within 3 seconds?
- Is the primary action obvious?

### 3b. Visual Scan Pattern
- Does the layout follow natural eye flow (F-pattern or Z-pattern)?
- Are related elements grouped visually?
- Is there a clear visual hierarchy (primary > secondary > tertiary)?

### 3c. Content-to-Chrome Ratio
- Measure: What percentage of the viewport is actual content vs. navigation chrome?
- **Target:** >60% content on iPhone, >70% on iPad
- Flag any view where content ratio falls below 50%

---

## Phase 4: Code Analysis

When a SwiftUI file is provided, read it and analyze:

### 4a. View Structure
- Total nesting depth (VStack chains)
- Number of distinct visual sections
- Spacing and padding accumulation
- Bottom padding for floating elements

### 4b. Component Audit
- Redundant UI elements (same info shown twice)
- Elements that could be merged (separate rows that should be one)
- Hidden/conditional elements wasting space when collapsed
- Action button sizing and placement

### 4c. Text and Typography
- Font hierarchy clarity (is there a clear primary > secondary > tertiary?)
- Line limit truncation (important text cut off while less important text has room)
- Dynamic Type support (`.system(size:)` vs semantic fonts)

### 4d. Color Usage
- Meaningful vs. decorative color
- Competing colors
- Contrast sufficiency
- Information redundancy (color + icon + text)

---

## Phase 5: Domain Analysis

Run the applicable domains based on the interview:

### Verification Template (MANDATORY per view audit)

Before grading a view, produce this checklist showing what was actually inspected:

```
| Domain | Checked? | Receipt | Findings |
|--------|----------|---------|----------|
| 1. Space Efficiency | ? | (file:line) | |
| 2. Visual Hierarchy | ? | (file:line) | |
| 3. Information Density | ? | (file:line) | |
| 4. Interaction Patterns | ? | (file:line) | |
| 5. Accessibility | ? | (file:line) | |
| 6. HIG Compliance | ? | (file:line) | |
| 7. Dark Mode | ? | (file:line) | |
| 8. Performance Impact | ? | (file:line) | |
| 9. Design System Compliance | ? | (file:line) | |
| 10. Competitive Comparison | ? | (file:line) | (only if competitor screenshot provided; otherwise skip with reason) |
| 11. Color Audit | ? | (file:line) | |
| 12. iPad Sheet Sizing | ? | (file:line) | |
| 13. Button Hit Region | ? | (file:line) | |
| 14. Silent Picker | ? | (file:line) | (candidates — verify on device) |
```

Rules:
- Every domain must be marked checked (yes) or skipped (no — with reason)
- Skipped domains cannot contribute to the grade (positive or negative)
- A grade cannot be produced while any domain has `?`
- Domain 10 is conditionally applicable — only runs when the user supplies a competitor screenshot during Phase 1. If no screenshot, mark it `skipped (no competitor screenshot provided)` and do not include in scoring.

### Domain 1: Space Efficiency `enumerate-required`

**Goal:** Maximize content-to-chrome ratio; minimize wasted vertical space.

| Check | What to Look For | Common Fix |
|-------|-----------------|------------|
| Header overhead | Custom headers stacking on nav bar | Collapse or merge headers |
| Dual button rows | Action buttons on separate line from navigation | Merge into one row |
| Section headers | Oversized section titles with icons | Reduce font size, remove decorative icons |
| Bottom padding | Excessive padding for floating elements | Reduce to actual element height + margin |
| Hints/tips | Permanent hints that should dismiss after first use | Use coach marks or remove after learning |
| Photo sections | Separate photo rows when thumbnail could be inline | Merge photo into title/header row |
| Dividers/spacers | Excessive VStack spacing or explicit Spacer() | Reduce spacing values |
| **Mergeable sections** | Small sections (1-2 items) with their own header overhead | Merge into adjacent related section |
| **Relocatable controls** | Buttons/toggles in separate rows that could fit in an existing header or toolbar | Move into header, nav bar, or existing row |
| **Redundant entry points** | Same action accessible from both a toolbar button AND a content card/row | Remove the duplicate; keep the more discoverable one |

**Layout reorganization analysis (run for every view):**

Before recommending individual element changes, check whether **reorganizing the layout** would save more space than tweaking individual elements:

1. **Count items per section** — sections with 1-2 items are candidates for merging with adjacent sections
2. **Check for orphaned controls** — buttons, toggles, or status indicators in their own row that could be absorbed into an existing element (e.g., theme toggle → header)
3. **Identify duplicate entry points** — the same action accessible from both a toolbar/action bar AND a content card below; remove the less discoverable one
4. **Measure section header overhead** — each section header costs ~40pt; merging 2 sections saves ~40pt without touching content

**Metrics:**
- Content starts at: [Y position in points from top]
- First interactive element at: [Y position]
- Content-to-chrome ratio: [percentage]
- Target: Content should start within 120pt of safe area top on iPhone

---

### Domain 2: Visual Hierarchy `enumerate-required`

**Goal:** The most important information should be the most prominent.

| Check | What to Look For | Common Fix |
|-------|-----------------|------------|
| Title prominence | Is the item/screen title the dominant element? | Ensure title is largest text |
| Competing elements | Multiple elements fighting for attention | Differentiate with size/weight/color |
| Status overload | Status indicators louder than content | Reduce to subtle badges |
| Date/number sizing | Dates or numbers displayed too large | Use caption/footnote for secondary data |
| Action vs. content | Action buttons more prominent than content | Tone down button styling |
| Truncation | Important text truncated while less important text has room | Allow wrapping or reprioritize |
| Color dominance | Bright colors on secondary elements | Reserve bright colors for primary actions |

**Analysis technique:**
1. Squint at the screenshot — what stands out?
2. That should be the primary content, not navigation chrome
3. If navigation or status draws the eye first, hierarchy is wrong

---

### Domain 3: Information Density `enumerate-required`

**Goal:** Show the right amount of information — not too sparse, not too cluttered.

| Check | What to Look For | Common Fix |
|-------|-----------------|------------|
| Sparse rows | List rows with too much whitespace | Reduce padding, show more per row |
| Dense rows | Too much crammed into one row | Progressive disclosure |
| Redundant info | Same data shown in multiple places | Remove duplicates |
| Hidden useful info | Important data behind taps/scrolling | Surface in primary view |
| Badge overload | Too many status badges on one element | Prioritize, hide secondary |
| Empty states | Large empty areas when data is missing | Collapse section |
| Nonsense values | Negative numbers, meaningless dates | Use human labels or hide |

**Density targets:**
- List row: 2-3 lines max (title + subtitle + trailing status)
- Card: 4-6 data points visible without scrolling
- Form section: 3-5 fields visible without scrolling

---

### Domain 4: Interaction Patterns `mixed`

**Goal:** Every interactive element should be discoverable, predictable, and satisfying.

| Check | What to Look For | Common Fix |
|-------|-----------------|------------|
| Touch targets | Elements smaller than 44x44pt | Increase frame/padding |
| Ambiguous buttons | Buttons that look like labels | Add clear button styling |
| Combined buttons | Two features sharing one button | Separate into distinct buttons |
| Gesture-only actions | Actions only via swipe/long-press | Add visible button alternative |
| Dead ends | Screens with no clear next action | Add CTA or navigation hint |
| Feedback gaps | Actions with no visual/haptic response | Add animation or haptic |
| Scroll discovery | Content below fold with no indicator | Add hint or gradient |
| Menu depth | Important actions buried in menus | Surface frequently-used actions |

---

### Domain 5: Accessibility `mixed`

**Goal:** Every user, regardless of ability, can use the view effectively.

| Check | What to Look For | Common Fix |
|-------|-----------------|------------|
| Color-only info | Information conveyed only by color | Add icon + text (triple redundancy) |
| Fixed fonts | `.system(size:)` instead of semantic | Use Dynamic Type |
| Missing labels | Images/icons without accessibility labels | Add `.accessibilityLabel()` |
| Small text | Text below 11pt that doesn't scale | Use `.caption` minimum |
| Contrast ratio | Low contrast text on backgrounds | Ensure 4.5:1 (WCAG AA) |
| VoiceOver order | Reading order doesn't match visual | Reorder or group |
| Motion | Animations without Reduce Motion check | Check accessibility setting |

---

### Domain 6: HIG Compliance `mixed`

**Goal:** Follow Apple Human Interface Guidelines for platform consistency.

| Check | What to Look For | Common Fix |
|-------|-----------------|------------|
| Navigation | Custom back buttons, non-standard patterns | Use system NavigationStack |
| Tab bar | Incorrect icons or labels | Follow SF Symbol + short label |
| Sheet presentation | Missing drag indicator or dismiss | Add `.presentationDragIndicator(.visible)` |
| System colors | Hard-coded colors | Use `.primary`, `.secondary` |
| Platform differences | iOS-only patterns on macOS | Use `#if os(iOS)` |
| Safe areas | Content under notch or home indicator | Respect safe area insets |
| Standard controls | Custom controls duplicating system | Use SwiftUI standard controls |

---

### Domain 7: Dark Mode `grep-sufficient`

**Goal:** The view should look correct and intentional in both light and dark mode.

| Check | What to Look For | Common Fix |
|-------|-----------------|------------|
| Hardcoded colors | `Color.white`, `Color.black`, hex values | Use semantic colors (`.primary`, `.background`) |
| Background assumptions | `.background(Color.white)` | Use `.background(Color(.systemBackground))` |
| Shadow visibility | Shadows invisible in dark mode | Use `.shadow` with adaptive opacity |
| Image contrast | Images with white/transparent backgrounds | Add dark mode variants or tinted backgrounds |
| Separator visibility | Light separators disappearing | Use `.separator` system color |
| Accent consistency | Accent colors that clash in dark mode | Test all accent colors in both modes |
| Material usage | Solid backgrounds where materials work better | Use `.ultraThinMaterial` for overlays |

**Analysis:** If screenshot provided, check if the view uses light or dark mode. If code available, run the automated checks below.

> **CRITICAL: Do NOT delegate Domain 7 checks to Explore subagents.** Run each check directly using Grep/Read tools against the target view file(s). Subagent sampling causes false negatives.

#### Automated Detection

**Check 7a: Hardcoded colors**
```bash
# Find hardcoded Color.white, Color.black, Color(red:green:blue:), hex colors
grep -n "Color\.white\|Color\.black\|Color(red:\|Color(hex:\|UIColor(red:\|NSColor(red:" <view_file>.swift

# Find .foregroundColor(.white) / .foregroundStyle(.white)
grep -n "foregroundColor(\.white)\|foregroundStyle(\.white)\|foregroundColor(\.black)\|foregroundStyle(\.black)" <view_file>.swift
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Semantic colors
.foregroundStyle(.primary)
.background(Color(.systemBackground))

// ✅ White text on intentionally colored backgrounds (e.g., Insights card pattern)
// Check: if the background is a solid accent color, .white text is correct

// ✅ Color.white/black in Color(light:dark:) adaptive initializers
```

**Check 7b: Background assumptions**
```bash
# Find non-adaptive backgrounds
grep -n "\.background(Color\.white)\|\.background(\.white)\|\.background(Color\.black)" <view_file>.swift

# Find hardcoded RGB backgrounds
grep -n "\.background(Color(red:" <view_file>.swift
```

**Check 7c: Shadow visibility in dark mode**
```bash
# Find shadows with low opacity black (invisible in dark mode)
grep -n "\.shadow(color:.*\.black.*opacity.*0\.[0-1]" <view_file>.swift

# Find shadows without color parameter (default is black, may be invisible)
grep -n "\.shadow(radius:" <view_file>.swift | grep -v "color:"
```

**Check 7d: Material opportunities**
```bash
# Find solid background overlays that could use materials
grep -n "\.background(Color.*opacity\|\.background(\.ultraThin\|\.background(\.thin\|\.background(\.regular" <view_file>.swift

# Find ZStack overlays with solid semi-transparent backgrounds
grep -B3 -A3 "ZStack" <view_file>.swift | grep "opacity"
```

---

### Domain 8: Performance Impact `grep-sufficient`

**Goal:** UI patterns should not cause frame drops, excessive redraws, or memory issues.

| Check | What to Look For | Common Fix |
|-------|-----------------|------------|
| Heavy body | Complex expressions in view body | Extract to computed properties |
| Inline images | Image decoding in body | Use `AsyncCachedImage` or background decoding |
| Missing lazy | Large lists without `LazyVStack` | Switch to lazy containers |
| Excessive state | Too many `@State` vars causing redraws | Consolidate or use `@Observable` |
| Geometry readers | GeometryReader in scroll views | Use `.onGeometryChange` or remove |
| Conditional complexity | Deep if/else chains in body | Extract to `@ViewBuilder` functions |
| Animation cost | Heavy animations on low-end devices | Reduce or check Reduce Motion |

**Analysis:** Read the SwiftUI file and run the automated checks below. Flag files over 500 lines that could benefit from extraction.

> **CRITICAL: Do NOT delegate Domain 8 checks to Explore subagents.** Run each check directly.

#### Automated Detection

**Check 8a: Missing lazy containers**
```bash
# Find non-lazy VStack/HStack inside ScrollView with ForEach
grep -n "ScrollView" <view_file>.swift
# Then check: is the ForEach inside a VStack (not LazyVStack)?
grep -B5 "ForEach" <view_file>.swift | grep "VStack\b" | grep -v "LazyVStack"
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Small static lists (< 20 items) — lazy containers add overhead for small lists
// ✅ VStack with fixed content (no ForEach)
// ✅ LazyVStack already used
```

**Check 8b: GeometryReader in scroll contexts**
```bash
# Find GeometryReader usage
grep -n "GeometryReader" <view_file>.swift

# Check if it's inside a ScrollView or List (causes layout thrashing)
grep -B10 "GeometryReader" <view_file>.swift | grep "ScrollView\|List {"
```

**Safe patterns (do NOT flag):**
```swift
// ✅ GeometryReader at the top level (not inside scroll)
// ✅ .onGeometryChange modifier (proper replacement)
// ✅ GeometryReader used only for initial measurement (cached in @State)
```

**Check 8c: Excessive @State count**
```bash
# Count @State variables in the view
grep -c "@State " <view_file>.swift

# Flag if > 8 @State vars in a single view (suggests consolidation needed)
```

**Check 8d: Heavy view body**
```bash
# Count lines in the body property (approximate)
# Find "var body:" and count lines until next "var " or "func " at same indent
grep -n "var body:" <view_file>.swift

# Flag if body exceeds ~100 lines — extract to computed properties or subviews
wc -l <view_file>.swift
# Flag if total file > 500 lines
```

**Check 8e: Image decoding in body**
```bash
# Find UIImage/NSImage initialization in view body (should be async)
grep -n "UIImage(data:\|UIImage(contentsOf\|NSImage(data:\|NSImage(contentsOf" <view_file>.swift

# Find synchronous image loading
grep -n "Data(contentsOf:" <view_file>.swift
```

**Check 8f: Animation without Reduce Motion check**
```bash
# Find .animation or withAnimation
grep -n "\.animation(\|withAnimation" <view_file>.swift

# Check if @Environment(\.accessibilityReduceMotion) is declared
grep -n "accessibilityReduceMotion" <view_file>.swift

# Flag: animations present but no reduce motion check
```

**Safe patterns (do NOT flag):**
```swift
// ✅ .animation(.default, value:) — implicit animations with value binding (low cost)
// ✅ System animations (sheet presentation, navigation transitions)
// ✅ Reduce Motion already checked
```

---

### Domain 9: Design System Compliance `enumerate-required`

**Goal:** The view should follow the project's established design system. Compare it against the project's documented rules and flag both off-pattern usage (custom UI where a standard component/modifier exists, off-palette colors, non-`@ScaledMetric` icons, sheets not using `SheetContainer`) AND missing-for-consistency gaps (a feature most sibling views enable but this one doesn't).

**Why this is project-specific:** Domain 9 has no fixed ruleset — its rules ARE the project's design system. With no design-system source (`conventions.yaml` / `CLAUDE.md` rules / `DESIGN_SYSTEM.md` / style guide), it skips entirely and recommends establishing one. It never invents rules.

**Reference:** `references/domain-9-design-system-compliance.md` — full checks 9a–9e, unused-capability check, cross-view consistency pass, finding format, exclusions, acceptance criteria, synthetic fixture.

**Detection steps (summary — full bodies in the reference):**

1. Read the design-system source (config → docs). If none exists, skip with a single "no design system found" note.
2. **9a** color palette — flag colors outside the approved palette.
3. **9b** component usage — custom header/container UI where a shared component exists.
4. **9c** modifier usage — card-like UI without `.stuffolioCard()` / `.actionCard()`.
5. **9d** sheet pattern — sheets not using `SheetContainer` + `SheetHeader`.
6. **9e** icon sizing — fixed icon frames without `@ScaledMetric`.
7. **Unused-capability check** — view builds custom UI for a feature a shared component already exposes via a parameter → enable the parameter, delete the custom UI.
8. **Cross-view consistency** — using the Adaptive View Profile, flag features most sibling views enable that this view lacks; always framed as a recommendation with a skip option.

**Project-convention awareness:** sources rules from `.radar-suite/conventions.yaml` (`approved_palette`, `spacing_namespace`, `card_modifiers`, `sheet_container`, `shared_components`) if present, else greps `CLAUDE.md` / `DESIGN_SYSTEM.md` / `Sources/Views/Components/`. No source → skip the domain.

**Severity default:** 🟢 MEDIUM (drift, not breakage). Elevates to 🟡 HIGH when the violation breaks a load-bearing accessibility rule the design system encodes (colorblind-palette rule, Dynamic Type via `@ScaledMetric`), when 5+ views share the off-pattern shape (systemic), or when a missing empty/loading/error state leaves a real flow with no feedback. Never CRITICAL on its own.

**Exclusions (skip without flagging):** no design-system source exists; dev-only harness / `#Preview` / fixture; a documented, sanctioned exception; platform-guarded chrome correct for its platform. Full list in the reference.

> **CRITICAL: Do NOT delegate Domain 9 to Explore subagents.** The conformance comparison needs the project docs and the view file held together; a subagent that reads only the view loses the baseline and produces false positives.

---

### Domain 10: Competitive Comparison (On Request) `enumerate-required`

Only runs when user provides a competitor screenshot during interview.

| Analysis | What to Compare |
|----------|----------------|
| Information density | How much data is visible without scrolling? |
| Visual hierarchy | What does each app emphasize first? |
| Interaction patterns | How many taps to accomplish the same task? |
| Space efficiency | Content-to-chrome ratio comparison |
| Unique strengths | What does each app do better? |

Output as a side-by-side comparison table.

---

### Domain 11: Color Audit `mixed`

**Goal:** Ensure intentional, consistent, and effective use of color throughout the view. Detect monochromatic flatness, semantic drift, opacity inconsistencies, and missing visual differentiation.

**Adaptive Color Profile:** On first run, this domain reads CLAUDE.md and design system files to learn the project's palette rules. Findings are saved to `.agents/ui-enhancer-radar/color-profile.md` so subsequent audits can compare views against established patterns.

> **CRITICAL: Do NOT delegate Domain 11 checks to Explore subagents.** Run each check directly using Grep/Read tools against the target view file(s).

#### 11a. Color Inventory Table

**Build a table of every colored element in the view:**

| Element | Color | Opacity | Role | Category |
|---|---|---|---|---|
| Header bg | `.blue` | 100% | Branding | Chrome |
| Section icon | `.secondary` | 100% | Decoration | Chrome |
| Toggle (on) | `.blue` | 100% | Interactive | System |
| Row text | `.primary` | 100% | Content | Text |

**Categories:** Chrome (navigation, headers, borders), Content (user data, labels), Interactive (buttons, toggles, pickers), Status (badges, indicators), Decoration (icons, backgrounds, separators)

#### Automated Detection for Color Inventory

```bash
# Step 1: Extract all color references from the view file
grep -n "\.foregroundStyle(\|\.foregroundColor(\|\.fill(\|\.background(\|\.tint(\|Color\.\|Color(\|\.opacity(\|\.shadow(" <view_file>.swift

# Step 2: Extract specific named colors
grep -on "\.\(blue\|red\|green\|yellow\|orange\|purple\|pink\|cyan\|teal\|indigo\|gray\|mint\|brown\|primary\|secondary\|tertiary\|white\|black\|clear\|accentColor\)" <view_file>.swift

# Step 3: Extract custom color references
grep -n "AccessibleColor\|sf3aYellow\|Color(red:\|Color(hex:\|Color(\"" <view_file>.swift

# Step 4: Extract opacity modifiers
grep -n "\.opacity(" <view_file>.swift
```

Build the inventory table from these results. Each grep match becomes a row.

#### 11b. Color Distribution

Count unique colors and how many elements use each:

```
Color Distribution:
  .secondary / .gray:  14 elements  ████████████████  (58%)  ⚠️ DOMINANT
  .blue:                4 elements  ████              (17%)
  .primary:             3 elements  ███               (12%)
  .red:                 2 elements  ██                 (8%)
  .tertiary:            1 element   █                  (4%)
```

**Flag:** Any color family used by >50% of elements → "Monochromatic risk"
**Flag:** Any color used only once → "Orphan color — is it intentional?"

#### 11c. Monochromatic Detection (Form Flatness)

**This is the most critical check for form/settings views.** When a view is visually flat — same background, same text color, same icon color everywhere — users cannot scan it effectively.

#### Automated Detection for Monochromatic Risk

```bash
# Count distinct color families in the view file (excluding opacity variants)
# Extract unique color names from all color references
grep -oh "\.\(blue\|red\|yellow\|orange\|purple\|pink\|cyan\|teal\|indigo\|gray\|mint\|brown\|primary\|secondary\|tertiary\|accentColor\)" <view_file>.swift \
  | sort -u | wc -l

# Count how many elements use each color family
grep -oh "\.\(blue\|red\|yellow\|orange\|purple\|pink\|cyan\|teal\|indigo\|gray\|mint\|brown\|primary\|secondary\|tertiary\)" <view_file>.swift \
  | sort | uniq -c | sort -rn

# Flag: if .secondary or .gray accounts for >50% of color references → monochromatic risk
# Flag: if total distinct color families ≤ 2 → critical monochromatic
```

**Color Variance Score:** Count distinct color *families* (not counting opacity variants) visible in the view, excluding system chrome (status bar, nav bar).

| Score | Distinct Colors | Assessment |
|---|---|---|
| 1-2 | Monochromatic | **Critical** — view appears as a flat, undifferentiated wall |
| 3-4 | Low variety | **High** — sections blend together, hard to scan |
| 5-6 | Adequate | **Medium** — functional but could benefit from more differentiation |
| 7+ | Good variety | **Pass** — clear visual zones |

**When monochromatic is detected, recommend (in order):**

1. **Colored section header icons** — Each section gets a semantically colored icon circle (e.g., Network = blue cloud, Privacy = red shield, Data = purple database). This alone breaks the monochrome wall into scannable zones.
2. **Section background tints** — Subtle colored backgrounds (5-8% opacity) behind each section group, using the section's accent color.
3. **Icon colorization** — Replace `.secondary` gray icons with semantically meaningful colors from the project palette (shield = red, cloud = blue, sparkles = yellow).
4. **Interactive row highlighting** — Rows with pickers, navigation chevrons, or buttons get a subtle accent indicator to distinguish from static display rows.

#### 11d. Section Distinguishability

**Can you tell where one section ends and another begins without reading the text?**

| Check | What to Look For | Fix |
|---|---|---|
| Section headers same style as row labels | Headers use same font/color as content | Make headers bolder, colored, or add accent bar |
| No visual boundary between sections | Sections separated only by thin dividers | Add section background tints or spacing |
| All icons same color | Every icon is `.secondary` gray | Assign semantic colors per section |
| Sections run together visually | No color or weight change at section boundaries | Add colored section headers or dividers |

#### 11e. Interactive vs. Static Contrast

**Can users instantly identify which elements are tappable?**

| Check | What to Look For | Fix |
|---|---|---|
| Buttons look like labels | Navigation rows with no chevron/color distinction | Add `.blue` text or chevron indicator |
| Pickers look like static text | Picker values in same color as labels | Use accent color for picker values |
| Destructive actions blend in | "Clear History" looks like "Activity History" | Use `.red` for destructive, accent for navigation |
| Toggle rows vs info rows | Both look identical except for the toggle | Add subtle leading tint or icon color |

#### 11f. Opacity Consistency

**Group elements by role and check if similar elements use matching opacities:**

| Role | Elements | Opacities Found | Consistent? |
|---|---|---|---|
| Subtitles | Row descriptions, section footers | 70%, 85%, `.secondary` | No — standardize to `.secondary` |
| Backgrounds | Section tints, hover states | 6%, 8%, 45% | Check if intentional variation |
| Shadows | Card shadows, text shadows | 10%, 20%, 30%, 35% | Acceptable range |
| Borders | Card borders, row separators | 15%, 20%, 30% | Narrow to 2 values |

**Flag:** Same-role elements with >20% opacity variance → "Inconsistent opacity"

#### 11g. Semantic Drift

**Does the same color mean different things in different parts of the view?**

| Color | Location A | Meaning A | Location B | Meaning B | Drift? |
|---|---|---|---|---|---|
| `.blue` | Sidebar | "Own" phase | Dashboard | Primary action | Minor |
| `.orange` | Sidebar | "Dispose Of" phase | Dashboard | Import/Export | Yes — different semantic |

**Flag:** Same color with clearly different meanings in adjacent or related areas.

#### 11h. Light/Dark Mode Delta

For each element, note whether color/opacity changes between modes:

| Check | What to Look For | Fix |
|---|---|---|
| Hardcoded `.white` or `.black` | Won't adapt to mode switch | Use `.primary`, `.background`, semantic colors |
| Hex colors without dark variant | `Color(hex: "#FFFFFF")` in both modes | Use `Color(.systemBackground)` or asset catalog |
| Shadows invisible in dark mode | `Color.black.opacity(0.1)` disappears | Use adaptive opacity or colored shadows |
| Tints that wash out | Light tints (5% opacity) invisible on dark backgrounds | Increase dark mode opacity (e.g., 3% light → 8% dark) |

#### Automated Detection for Light/Dark Mode Delta

```bash
# Reuses Domain 7 checks — cross-reference here
# Find hardcoded white/black
grep -n "Color\.white\|Color\.black\|\.white)\|\.black)" <view_file>.swift | grep -v "//.*white\|//.*black"

# Find hex colors without dark variant
grep -n 'Color(hex:\|Color("#\|Color(red:' <view_file>.swift

# Find shadows using black with low opacity
grep -n "shadow.*\.black.*opacity.*0\.[0-1]" <view_file>.swift

# Find low-opacity tints that may wash out in dark mode
grep -n "\.opacity(0\.0[1-8])" <view_file>.swift
```

#### 11i. Contrast Pairs (WCAG AA)

Check text-on-background combinations:

| Pair | Ratio Needed | Common Failures |
|---|---|---|
| Body text on background | 4.5:1 | `.secondary` on `.systemGroupedBackground` in light mode |
| White text on colored cards | 4.5:1 | White on `.yellow` or `.cyan` (low contrast) |
| Caption text on tinted backgrounds | 4.5:1 | `.tertiary` on subtle tints |
| Interactive text on background | 3:1 (large text) | `.blue` on dark backgrounds can be low |

#### 11j. Design System Compliance

**Compare actual color usage against project rules:**

1. Read CLAUDE.md for palette restrictions (e.g., "never use green", "use AccessibleColor.sf3aYellow instead of .yellow")
2. Read design system files for approved colors
3. Flag any color not in the approved palette
4. Flag any use of restricted colors

#### Automated Detection for Design System Color Compliance

```bash
# Step 1: Find restricted colors (project-specific — read CLAUDE.md first)
# Example: if green is forbidden:
grep -n "\.green\|Color\.green\|foregroundStyle(\.green)\|foregroundColor(\.green)" <view_file>.swift

# Example: if system .yellow should be sf3aYellow:
grep -n "\.yellow\b" <view_file>.swift | grep -v "sf3aYellow\|AccessibleColor\|semantic.*warning"

# Step 2: Find colors not in approved palette
# Extract all color names, compare against approved list from CLAUDE.md
grep -oh "\.\(blue\|red\|green\|yellow\|orange\|purple\|pink\|cyan\|teal\|indigo\|gray\|mint\|brown\)" <view_file>.swift \
  | sort -u

# Step 3: Find custom hex/RGB colors (may not be in palette)
grep -n "Color(red:\|Color(hex:\|Color(\"" <view_file>.swift
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Colors used in conditional semantic contexts (status indicators per CLAUDE.md)
// ✅ .yellow used for semantic warning status (explicitly allowed per CLAUDE.md)
// ✅ sf3aYellow / AccessibleColor.sf3aYellow (approved replacement)
```

### Adaptive View Profile

The View Profile is a persistent file that grows with each audit, enabling cross-view consistency checks for both color (Domain 11) and component usage (Domain 9). Stored at `.agents/ui-enhancer-radar/view-profile.md`.

**On first audit of a project:**

1. Check for `.agents/ui-enhancer-radar/view-profile.md` — if it doesn't exist, create it
2. Record the Color Inventory Table, opacity conventions, and semantic color map from this audit
3. Record which shared components the view uses and which optional parameters it enables
4. Note the project's palette rules from CLAUDE.md

**On subsequent audits:**

1. Load the View Profile
2. **Color comparison:** Flag views that deviate from established color/opacity conventions
3. **Component comparison:** Flag views that don't enable features most sibling views use
4. Update the profile with any new patterns discovered
5. If a previously recorded convention has changed in the majority of views, update the convention (not the outlier)

**View Profile format (`.agents/ui-enhancer-radar/view-profile.md`):**

```markdown
# UI Enhancer View Profile
*Last updated: [date] | Views audited: [count]*

## Project Palette
[Colors from CLAUDE.md or design system]

## Color Conventions
| Role | Standard Color | Standard Opacity | Views Using |
|---|---|---|---|
| Section header icon | Semantic per section | 100% | DashboardView, ToolsView |
| Row subtitle | .secondary | 100% | SettingsView, ItemDetailView |
| Card shadow | sectionColor | 20% resting | DashboardView |

## Semantic Color Map
| Color | Meaning | Consistent Across Views? |
|---|---|---|
| .blue | Primary actions, Own phase | Yes |
| .orange | Dispose Of, data flow | Yes |

## Component Usage
| Component | Parameter | Enabled In | Not Enabled In | Adoption |
|---|---|---|---|---|
| ContentIllustratedHeader | showThemeToggle | Dashboard, Tools, Reports, MyProducts, StuffScout, LegacyWishes | Settings, Archive | 75% |
| ContentIllustratedHeader | showHelp | Dashboard, Tools, Reports | Settings, Archive, MyProducts | 50% |
| ContentIllustratedHeader | solidBackground | Dashboard | All others | 12% (intentional — dashboard only) |
| SheetContainer | showHelp | AddItem, StuffScout, Backup | Restore, Export | 60% |

## Detected Patterns
| Pattern | Views Using | Views Missing | Notes |
|---|---|---|---|
| Keyboard Done toolbar | All form views | — | Universal |
| Pull-to-refresh | Dashboard, MyProducts | Reports, Archive | Data views only |
| Empty state handling | MyProducts, Dashboard | Loans, Locations | Gap — should add |

## Refinement History
| Date | View | Change | Kept? | Notes |
|---|---|---|---|---|
| 2026-03-22 | DashboardView | VStack spacing 24→16→12pt | Kept 12pt | User wanted tighter |
| 2026-03-22 | DashboardView | Solid header background | Kept | More punch in light mode |
| 2026-03-22 | DashboardView | Quick Stats collapsed padding -8pt | Kept | Closer to MY STUFF |
```

**Refinement History** records what was tried during the refinement loop (Phase 7f) — both kept and reverted changes. This serves two purposes:
1. If the user returns and says "I liked the spacing we tried last time," the history shows what values were used
2. It reveals patterns — if the user consistently asks for tighter spacing, future audits should start with tighter recommendations

---

### Domain 12: iPad Sheet Sizing `enumerate-required`

**Goal:** For every `.sheet(isPresented:)` and `.sheet(item:)` call in the codebase, verify that tall presented content (Form / List / ScrollView) has been given an iPad sizing mechanism. Catches the caller-side blind spot that Domain 9's "Sheet pattern" check leaves — a sheet can use no house-style container AND no Apple sizing API, and still compile, pass all other domains, and quietly truncate to a floating ~540×620pt form sheet on iPad.

**Why this is cross-file:** the defect is a relationship between the caller (a `.sheet { ... }` closure somewhere) and the callee (the presented view's `body`). Neither file is wrong in isolation. Single-file grep cannot detect it; the domain needs to enumerate call sites, classify presented-view bodies, and check for any of four sizing mechanisms.

**Reference:** `references/domain-12-ipad-sheet-sizing.md` — full heuristic, exclusions list, finding format, acceptance criteria.

**Recognized sizing mechanisms (any one of these satisfies the check):**

1. House-style container (`SheetContainer` or project equivalent) that applies sizing internally
2. `.presentationSizing(.page)` on the sheet closure (iOS 18+)
3. `.presentationDetents([.large])` on the sheet closure (iOS 17 fallback)
4. Project convenience modifier (e.g., `.iPadPageSheet()`) that wraps one of the above

**Detection steps:**

1. Enumerate every `.sheet(isPresented:|item:)` call: `grep -rn --include="*.swift" -E "\.sheet\(isPresented:|\.sheet\(item:" Sources/`
2. For each, identify the presented view's type (top-level expression in the closure)
3. Read that view's `body` — skip if it starts with a recognized sizing container; skip if exclusions match (pickers, scanners, share sheets — see reference)
4. Check if the sheet closure has any sizing modifier (`.presentationSizing`, `.presentationDetents`, project modifier)
5. If the body is tall (Form / List / ScrollView at the top, or `NavigationStack` wrapping one of those) AND no sizing mechanism is present → flag

**Project-convention awareness:** learns house-style container + modifier names from `.radar-suite/conventions.yaml` if present, or from grepping CLAUDE.md / `Sources/Views/Components/` for a `View` extension that applies `presentationSizing(.page)` or `presentationDetents([.large])`. Falls back to Apple-API-only checks if no convention is found.

**Severity default:** 🟢 MEDIUM (user-visible iPad UX regression, not a crash). Elevates to 🟡 HIGH when any of: app is actively iPad-facing, 5+ sites share the issue (systemic), or the presented view is a critical flow (add-item, settings root, legal/compliance sheet).

**Borderline cases** (`NavigationStack { VStack { Header; mainContent } }` where `mainContent` is a conditional tree) are flagged as medium-confidence with a one-line synopsis of the tallest branch — not batched into the high-confidence fix set by default.

**Output row format** (per finding):

| File:line | State binding | Presented view (body shape) | Why flagged | Confidence | Suggested fix |
|---|---|---|---|---|---|
| `Sources/Views/Lists/RMAListView.swift:210` | `$showingAddRMA` | `RMAFormView` (`NavigationStack { Form }`) | Tall content, no sizing container, no sizing modifier | High | Append `.iPadPageSheet()` (project convention) or `.presentationSizing(.page)` (Apple default) inside the sheet closure |

**Exclusions (skip without flagging):** Photos/document pickers, scanners, share sheets, confirmation dialogs, splash screens, chooser views, single-action confirmations. Full list in the reference file.

**Do NOT delegate Domain 12 to Explore subagents.** Run the grep + Read passes directly. Enumeration is the point; a subagent can silently drop findings.

---

### Domain 13: Button Hit Region `enumerate-required`

**Goal:** For every `Button { } label: { }` call site, detect the three-factor interaction bug where `.buttonStyle(.plain)` + a manually drawn trailing `chevron.right` + Form/List context collapses the iPad hit region to the chevron alone. The rest of the row becomes visually tappable but functionally dead — users tap and nothing happens.

**Why this is three-factor:** no single factor is wrong. `.buttonStyle(.plain)` is legal. Manual chevrons are legal. Buttons inside Forms are legal. The *interaction* of the three — on iPad specifically — is what breaks. Single-file pattern matchers can't detect interactions.

**Reference:** `references/domain-13-button-hit-region.md` — full heuristic, exclusions, both fix options, acceptance criteria.

**Detection steps:**

1. Enumerate every `Button { } label: { }` in `Sources/` (skip `Button("Text", action:)` form — no custom label, no bug)
2. Check label closure for manually drawn trailing chevron: `Image(systemName: "chevron.right")` or `"chevron.forward"` (ignore DisclosureGroup custom implementations)
3. Check Button's modifier chain for `.buttonStyle(.plain)` or `.buttonStyle(.borderless)` — other styles don't have this bug
4. Check for Form/List context: structural walk for `Form { ... }` / `List { ... }` ancestor, OR modifier indicators on the Button or its parent Section (`.listRowBackground`, `.listRowInsets`, `.listRowSeparator`)
5. Check label closure for `.contentShape(Rectangle())` or `.contentShape(.rect)` — if present, author explicitly fixed the hit region; skip
6. When all four trigger and no content-shape escape, flag

**Recommended fixes (offer both):**

- **Fix A (preferred per HIG):** remove the decorative chevron. Card modifiers (`.actionCard()`, `.destructiveCard()`, colored row backgrounds) already read as tappable. HIG says chevrons are for NavigationLinks, not Buttons.
- **Fix B:** keep the chevron, add `.contentShape(Rectangle())` on the label's outer HStack. Preserves visual treatment but guarantees hit region.

**Severity:** 🟡 HIGH default (user-visible interaction failure — button looks broken). Elevates to 🔴 CRITICAL for buttons on critical paths (add-item, save, export, payment), systemic cases (5+ sites in same view hierarchy), or accessibility failures confirmed via VoiceOver.

**Exclusions:**
- `NavigationLink { } label:` — chevrons here are system-managed
- `DisclosureGroup` — chevron is a control, intentional
- `.buttonStyle(.bordered)`, `.borderedProminent`, or any system style other than `.plain` / `.borderless`
- Toolbar item Buttons
- macOS-only views (`#if os(macOS)` wrapping the whole body)
- Animated expand/collapse chevrons (`.rotationEffect(.degrees(isExpanded ? 90 : 0))`)

**Output row format:**

| File:line | Button action | Label synopsis | Button style | Context | Fix A (preferred) | Fix B |
|---|---|---|---|---|---|---|
| `Sources/Features/Settings/Views/BackupDataSheet.swift:193` | `createBackup()` | icon + 2-line text + chevron | `.plain` | Section in Form via SheetContainer | Remove chevron | Add `.contentShape(Rectangle())` |

**Pattern sweep follow-up:** this bug is rarely isolated. After a first fix, grep the full codebase for the same shape (same card modifier + same chevron + same button style). Offer batch application to consistent patterns.

**Do NOT delegate Domain 13 to Explore subagents.** Three-factor reasoning requires holding the full label closure, the modifier chain, and the Form/List context simultaneously. A subagent can lose one of the three factors and produce either false positives or false negatives.

---

### Domain 14: Silent Picker `enumerate-required`

**Goal:** For every `Picker(...)` call site, detect the two-factor interaction bug where a menu-style `Picker` with **no explicit `.pickerStyle(...)`** sits in a **custom (non-`Form`/`List`) container** — a `DisclosureGroup` body, a `ScrollView`+`VStack` screen, or a card with cleared row chrome. The picker renders as an enabled pop-up button but its menu **never presents on tap**. The user taps and nothing happens; the accessibility tree reports a healthy `AXPopUpButton`. No crash, no warning, no anti-pattern token.

**Why this is two-factor:** a style-less `Picker` is idiomatic. Custom containers are legal. The *interaction* — automatic menu presentation inside cleared-row-chrome / non-Form containers — is what fails, at runtime only.

**Cousin of Domain 13, not a duplicate:** both yield a control that's visually present and accessibility-enabled but dead on tap. But Domain 13 is `Button` + chevron + `.buttonStyle(.plain)` collapsing the *hit region* (tap misses); Domain 14 is `Picker` + no `.pickerStyle` + custom container failing to *present the menu* (tap lands, nothing opens). Domain 13's detector greps `Button`/`chevron`/`buttonStyle` and walks straight past `Picker` — which is exactly why this shipped with Domain 13 already in place.

**Reference:** `references/domain-14-silent-picker.md` — full heuristic, container classification, false-positive list, on-device verify protocol, acceptance criteria.

**Detection steps:**

1. Enumerate every `Picker(...)` in `Sources/` (both `Picker("Title", selection:)` and `Picker(selection:) { } label: { }` forms)
2. Skip any Picker with an explicit `.pickerStyle(...)` of any kind — the style is the fix
3. Reject `DatePicker` / `ColorPicker` / `PhotosPicker` false positives (the bare `Picker(` grep matches them)
4. Classify the container: genuine `Form`/`List` row with intact chrome → **skip**; `DisclosureGroup` body, `ScrollView`+`VStack` screen, or cleared-row-chrome / custom-card context → **candidate**
5. Emit as a ⚠️ **candidate**, NOT a confirmed bug — static analysis proves the risk, not the deadness

**Candidates require on-device verification.** Build, run, tap each flagged picker. Menu opens → false positive (some custom containers do present correctly), note and leave. Menu does not open → confirmed, apply Fix A.

**Recommended fixes (offer both):**

- **Fix A (preferred):** add `.pickerStyle(.menu)` — one line, lowest risk, verified to restore presentation.
- **Fix B (only for nested tiers):** rebuild on `Menu { Button… } label: { … }` — needed only when a picker reveals a sub-picker (two-tier), which `Picker` can't express cleanly.

**Severity:** 🟡 HIGH default (control ignores taps — reads as broken). Elevates to 🔴 CRITICAL on critical paths (add-item, edit-item, save, payment) — a dead control in the primary add/edit flow is a textbook **App Store Guideline 2.1** rejection ("a control that does nothing") — or when 3+ pickers in one view hierarchy share the pattern.

**Exclusions:**
- Any explicit `.pickerStyle(...)` (`.menu`, `.segmented`, `.wheel`, `.inline`, `.radioGroup`, custom)
- `Picker` in a genuine `Form`/`List` row with intact chrome
- `DatePicker`, `ColorPicker`, `PhotosPicker`
- Already rebuilt on `Menu { }`

**Output row format:**

| File:line | Picker | Style | Container | Status | Fix A | Fix B |
|---|---|---|---|---|---|---|
| `Sources/Views/Forms/WarrantyFormView+BasicSections.swift:193` | `"Acquired From"` | none (menu) | DisclosureGroup/VStack, cleared chrome | ⚠️ verify on device | `+ .pickerStyle(.menu)` | `Menu { }` rebuild |

**Pattern sweep follow-up:** this bug travels in packs (origin case: 7 sites across 4 files). After the first confirmed fix, sweep for the same shape: `Picker` + no `.pickerStyle` + (cleared-chrome modifier OR `DisclosureGroup` body OR `ScrollView`/`VStack` screen).

**Do NOT delegate Domain 14's candidate confirmation to static reasoning.** The container classification can be delegated, but "is the menu actually dead?" requires a real tap on a real device/sim. Emit candidates; verify on-device before asserting any picker is broken.

---

## Phase 6: Generate Report

### Report Structure

```
## UI Enhancer Report: [ViewName]
*UI Enhancer v[version] | [date]*

### Focus: [from interview — e.g., "General polish" or "Specific: too much wasted space"]

### Screenshot Analysis
- Content-to-chrome ratio: X%
- First content element at: Ypt from top
- Primary action visibility: [Obvious / Hidden / Ambiguous]
- 3-second test: [Pass / Fail — what draws the eye]

### Findings

| # | Domain | Finding | Severity | Effort | Recommendation |
|---|--------|---------|----------|--------|---------------|
| 1 | Space | 45% of screen is header chrome | Critical | Medium | Merge photo into title row |
| 2 | Hierarchy | Date text dominates over item title | High | Small | Replace with status circle |
| 3 | Dark Mode | 3 hardcoded Color.white references | Medium | Trivial | Replace with semantic colors |
| ... | ... | ... | ... | ... | ... |

### UX Score

| Domain | Score | Notes |
|--------|-------|-------|
| 1. Space Efficiency | 4/10 | Content starts at 410pt |
| 2. Visual Hierarchy | 6/10 | Date text too dominant |
| 3. Information Density | 7/10 | Good density, some redundancy |
| 4. Interaction Patterns | 5/10 | Combined buttons, gesture-only deletes |
| 5. Accessibility | 8/10 | Good labels, some fixed fonts |
| 6. HIG Compliance | 7/10 | Minor deviations |
| 7. Dark Mode | 6/10 | Some hardcoded colors |
| 8. Performance Impact | 8/10 | Clean structure |
| 9. Design System Compliance | 7/10 | Mostly compliant |
| 10. Competitive Comparison | N/A | (skipped — no competitor screenshot provided) |
| 11. Color Audit | 5/10 | Monochromatic sections, inconsistent opacities |
| 12. iPad Sheet Sizing | 9/10 | Uses .iPadPageSheet() convention |
| 13. Button Hit Region | 6/10 | One .plain + chevron in Form section needs .contentShape(Rectangle()) |
| 14. Silent Picker | 7/10 | One menu Picker in a DisclosureGroup card lacks .pickerStyle(.menu) — verify on device |
| **Overall** | **6.4/10** | (Domain 10 excluded from average when N/A) |

### Before/After ASCII Mockup

BEFORE:
┌─────────────────────────┐
│ [Nav Bar]               │
│ [Photo Row - 56pt]      │
│ [Title Row - 64pt]      │
│ [Tab Chips - 40pt]      │
│ [Action Buttons - 32pt] │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│ [Content starts here]   │
│ ...                     │
└─────────────────────────┘
Content ratio: 39%

AFTER:
┌─────────────────────────┐
│ [Nav Bar]               │
│ [Photo+Title - 64pt]    │
│ [Chips + Buttons - 40pt]│
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│ [Content starts here]   │
│ ...                     │
│ ...                     │
│ ...                     │
└─────────────────────────┘
Content ratio: 63%

### Space Budget (Before/After)

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Header chrome | [N]pt | [N]pt | -[N]pt |
| Search/filters | [N]pt | [N]pt | -[N]pt |
| Section headers (×[count]) | [N]pt | [N]pt | -[N]pt |
| Content starts at | [Y]pt | [Y]pt | -[N]pt |
| Content-to-chrome ratio | [X]% | [X]% | +[N]% |
| Sections | [N] | [N] | -[N] |
| Feature cards/buttons | [N] | [N] | -[N] |

**Net space recovered:** ~[N]pt

### Implementation Priority

**Quick Wins (do first):**
1. [Finding] — [exact code change]

**Medium Effort:**
2. [Finding] — [approach]

**Nice-to-Have:**
3. [Finding] — [approach]
```

---

## Phase 6b: Content & Identity Preservation Check (MANDATORY before removing UI)

**When any finding recommends removing or replacing a UI element, check whether it contained informational text OR visual identity elements that serve a purpose beyond decoration.**

### What to check

For each element being removed, ask:
- Does it contain **explanatory text** (descriptions, subtitles, instructions)?
- Does it contain **status information** (counts, states, labels)?
- Would a **first-time user** lose context about what this screen does?
- Does it contain **branding elements** (app icon, section icon, colored backgrounds) that establish visual identity?
- Does it contribute to **visual consistency** across the app (same component used in multiple views)?
- Is it tagged `[PRESERVE]` from the Design Intent interview?

**If text content would be lost**, the text must be **relocated, not deleted**. Propose one of these options to the user:

**If visual identity would be lost** (icons, colors, branded backgrounds), route to **Phase 6c (Element Compaction)** instead of removing — compaction preserves identity at reduced size.

### Relocation options

| Option | When to use | Example |
|--------|------------|---------|
| **Help button (`?`)** | Descriptive text that experienced users don't need | Toolbar `?` button → popover with description |
| **Info icon (`i`)** | Context that's useful but not essential to scan | Small `ℹ️` next to a title, expands on tap |
| **First-visit only** | Onboarding text that should disappear after learning | Show once via `@AppStorage`, hide after first visit |
| **Nav bar subtitle** | Short taglines (< 40 chars) | `.navigationSubtitle("Identify & Appraise")` |
| **Tooltip / help text** | Secondary info on macOS | `.help("Identify and value antiques...")` |
| **Keep as-is** | The text is truly decorative and losing it is fine | Marketing copy repeated elsewhere |

### How to present

After listing findings but before implementation, flag any content at risk:

```
questions:
[
  {
    "question": "Removing [element] would also remove the text '[text]'. Where should this information go?",
    "header": "Content",
    "options": [
      {"label": "Drop it (Recommended)", "description": "The text isn't needed — users understand from context"},
      {"label": "Help button (?)", "description": "Add a toolbar help button that shows this on tap"},
      {"label": "First-visit only", "description": "Show on first use, hide after"},
      {"label": "Keep the element", "description": "Don't remove this element after all"}
    ],
    "multiSelect": false
  }
]
```

**If "Keep the element"** — remove that finding from the playbook and adjust space savings estimates.

### Skip this check when

- The removed element contained only a **title that's already in the nav bar**
- The removed element contained only **color/icon decoration** with no text
- The text is **displayed elsewhere on the same screen** (e.g., in a banner below)

---

## Phase 6c: Element Compaction (MANDATORY when recommending removal of visual elements)

**When a finding recommends removing a decorative or branding element for space efficiency, the user may want to preserve the element's visual identity at a smaller footprint. Always offer compaction as an alternative to removal.**

### Cross-View Consistency Check (run before compaction decisions)

Before recommending removal or compaction of any visual element, check whether it's part of a cross-view pattern:

1. **Grep the codebase** for the component name (e.g., `ContentIllustratedHeader`, `SheetHeader`, custom component names)
2. **Count how many views** use the same component
3. **If used in 3+ views**, flag it as a **consistency pattern**:

```
⚠️ Cross-view pattern detected: [ComponentName] is used in [N] views:
  - ViewA.swift (line X)
  - ViewB.swift (line Y)
  - ViewC.swift (line Z)

Removing it from this view would break visual consistency.
Recommendation: Compact (not remove), or apply the change across all [N] views.
```

**If a consistency pattern is detected:**
- Default to **Compact** instead of Remove
- If the user chooses Remove, warn: "This will make [ViewName] visually inconsistent with [N] other views that use [ComponentName]. Apply the same change to all, or just this one?"
- Offer: "Apply to all [N] views" / "Just this view" / "Cancel"

### When to trigger

This check runs when ANY finding recommends removing:
- Illustrated headers (ContentIllustratedHeader, custom banners)
- Branded sections with icons, backgrounds, or imagery
- Photo rows, hero images, or visual feature cards
- Any element the user may consider part of the view's visual identity
- Any element tagged `[PRESERVE]` during the Design Intent interview

### What to ask

For each element recommended for removal, present compaction as the default:

```
questions:
[
  {
    "question": "The [element] uses ~[N]pt. How would you like to handle it?",
    "header": "Element",
    "options": [
      {"label": "Compact (Recommended)", "description": "Preserve visual identity at reduced size (~[M]pt savings)"},
      {"label": "Remove entirely", "description": "Maximum space savings (~[N]pt recovered)"},
      {"label": "Keep as-is", "description": "No change to this element"}
    ],
    "multiSelect": false
  }
]
```

### Compaction techniques by element type

| Element Type | Full Size | Compaction Techniques | Target Size |
|---|---|---|---|
| **Illustrated header** (icon + title + subtitle + background) | ~100-140pt | Inline icon (28pt) + title only, reduce background height, drop subtitle | ~44-56pt |
| **Section header** (decorative circle + title) | ~40-48pt | Smaller circle (18pt), reduce font, tighten padding | ~28-32pt |
| **Photo/hero row** | ~80-120pt | Thumbnail (40pt) inline with title instead of full-width | ~44pt |
| **Status banner/card** | ~60-80pt | Compact badge or chip instead of card | ~28-36pt |
| **Tip/hint section** | ~60-100pt | Collapsible disclosure, or single-line with `(i)` | ~20-44pt |
| **Feature card** | ~80-120pt | Reduce padding, smaller icon, tighter text | ~48-64pt |

### How to generate compact code

When "Compact" is selected, apply these reductions in order until target height is reached:

1. **Reduce icon size** — e.g., 48pt → 28pt, 32pt → 20pt
2. **Inline layout** — switch from VStack to HStack where possible
3. **Drop secondary text** — remove subtitles, taglines, descriptions (relocate per Phase 6b if needed)
4. **Tighten spacing** — reduce padding and VStack/HStack spacing by 30-50%
5. **Reduce background** — shrink or remove decorative backgrounds, keep accent color as border or tint
6. **Simplify** — remove shadows, reduce corner radius, flatten visual layers

### Playbook format for compaction

When compaction is chosen, the playbook entry should show the before/after with measurements:

```
### Fix #N: Compact [element name]

**File:** `Sources/Views/[file].swift`
**Lines:** [range]

**Before:** (~[N]pt height)
[exact code block]

**After:** (~[M]pt height, [savings]pt saved)
[exact replacement code — compacted version]

**Why:** Preserves visual identity while reclaiming [savings]pt of vertical space

**Test:** Verify element is visually recognizable at smaller size on iPhone SE and Pro Max
```

### When NOT to compact

- The element is **purely redundant** (same title shown in nav bar AND header AND banner) — removal is better
- The element **cannot be meaningfully reduced** (already near minimum viable size)
- The user explicitly chose "Remove entirely"

---

## Phase 6d: Visual Compensation Check (MANDATORY when removing visual elements)

**When findings remove headers, icons, colored elements, or decorative components, the result may look visually flat. Before implementing, check whether the remaining UI needs visual enrichment to compensate.**

### When to trigger

This check runs when ANY finding:
- Removes a header component (SheetHeader, ContentIllustratedHeader, custom headers)
- Removes colored backgrounds, accent bars, or decorative elements
- Consolidates multiple visual sections into fewer elements
- Strips icons or imagery from the view

### What to ask

```
questions:
[
  {
    "question": "Removing [element] will reduce visual richness. How would you like to compensate?",
    "header": "Visual",
    "options": [
      {"label": "Colored section headers (Recommended)", "description": "Add colored icon circles to section headers for visual anchoring"},
      {"label": "Per-section accent colors", "description": "Use project palette to differentiate sections (icons, borders, or backgrounds)"},
      {"label": "Both \u2014 headers + accents", "description": "Full treatment: colored header icons + per-section accent colors from project palette"},
      {"label": "No compensation needed", "description": "The view looks fine without it"}
    ],
    "multiSelect": false
  }
]
```

### Compensation techniques (by view type)

| View Type | Best Compensation | Why |
|-----------|------------------|-----|
| **Help / reference** | Colored icon circles in section headers | Provides visual anchoring without distracting from linear reading |
| **Dashboard / overview** | Colored card backgrounds + accent bars | Scanning views benefit from strong visual differentiation |
| **Form / input** | Subtle section tints or header icons | Keep focus on inputs, use color sparingly |
| **Detail / inspector** | Accent bars on cards + status colors | Help users scan for specific information |
| **List / table** | Alternating row tints or leading color indicators | Help distinguish items at a glance |

### Color palette for compensation

**Always check the project's design system first.** Before applying any colors:

1. Read `CLAUDE.md` for documented color rules or palette restrictions
2. Search for design system files (`DESIGN_SYSTEM.md`, `StyleGuide.swift`, `Colors.swift`, `Theme.swift`)
3. Check for existing color constants or enums in the codebase (`grep` for `static let`, `Color(`, `UIColor(`)

**If a project palette exists:** Use only colors from that palette. Follow any restrictions (e.g., "never use green", "use semantic colors only"). Reference the project's color constants in code, not raw SwiftUI colors.

**If no project palette exists:** Use this default set, which provides good contrast and variety across common forms of color vision:

| Color | Use for |
|-------|---------|
| Blue | Primary, required, actions |
| Purple | Secondary, optional, analysis |
| Teal/Cyan | Tools, utilities, coverage |
| Orange | Media, images, discovery |
| Pink | Support, resources, special |
| Yellow | Tips, highlights, warnings |
| Gray | Notes, neutral, settings |

### When to skip

- The view is already visually rich after removal (e.g., content itself has color/imagery)
- Only minor chrome was removed (a single label or small spacer)
- The user explicitly chose "No compensation needed"

---

## Phase 7: Implementation Playbook

**MANDATORY: Before ANY code edits, complete Phase 7a (User Commit Offer), Phase 7b (Visual Inspection Gate), and Phase 7c (Guided Visual Review). These are NOT optional. Skipping them means making blind changes to visual UI.**

For each finding, generate the exact code change — not just a description.

### Playbook Entry Format

```
### Fix #1: [Finding title]

**File:** `Sources/Views/Detail/EnhancedItemDetailView.swift`
**Lines:** 180-265

**Before:**
[exact code block to replace]

**After:**
[exact replacement code]

**Why:** [one sentence explaining the UX improvement]

**Test:** [what to verify after applying]
```

Offer to apply changes:

```
questions:
[
  {
    "question": "How would you like to apply these changes?",
    "header": "Implement",
    "options": [
      {"label": "Apply all (Recommended)", "description": "Implement all fixes with keep/revert after each"},
      {"label": "Quick wins only", "description": "Only Trivial/Small effort changes"},
      {"label": "One at a time", "description": "Apply and verify each fix individually"},
      {"label": "Save playbook", "description": "Save to file, implement later"}
    ],
    "multiSelect": false
  }
]
```

---

## Phase 7a: User Commit Offer (MANDATORY — execute before ANY edits)

**This phase is NOT optional. Do NOT skip it. Do NOT silently create checkpoints. ASK the user.**

**First, check if git is available** by running `git rev-parse --is-inside-work-tree`. If git is available, offer the git-based options. If not, offer file-based alternatives.

### If git IS available:

```
questions:
[
  {
    "question": "Before making changes, would you like to commit your current work? This creates a clean revert point.",
    "header": "Safety",
    "options": [
      {"label": "Commit first (Recommended)", "description": "Commit uncommitted changes so you can revert cleanly"},
      {"label": "Skip — working tree is clean", "description": "No uncommitted work to protect"},
      {"label": "Skip — I'll manage git myself", "description": "Proceed without committing"}
    ],
    "multiSelect": false
  }
]
```

**If "Commit first":**
1. Run `git status` to show what will be committed
2. Stage and commit with message: `chore: checkpoint before ui-enhancer-radar changes`
3. Confirm the commit hash to the user

**If "Skip — working tree is clean":**
Verify with `git status --porcelain`. If there ARE uncommitted changes, warn and re-ask.

**If "Skip — I'll manage git myself":**
Proceed without committing.

### If git is NOT available:

```
questions:
[
  {
    "question": "No git repository detected. Before making changes, would you like to back up the files that will be modified?",
    "header": "Safety",
    "options": [
      {"label": "Back up files (Recommended)", "description": "Copy each file to a .backup before editing"},
      {"label": "Skip — I have my own backups", "description": "Proceed without backup"},
      {"label": "Save playbook only", "description": "Show the changes but don't apply — I'll do it manually"}
    ],
    "multiSelect": false
  }
]
```

**If "Back up files":**
For each file that will be modified, create a copy: `cp file.swift file.swift.backup`
List the backup files created so the user can find them.

**If "Save playbook only":**
Generate the full playbook with before/after code blocks, but do not apply any edits. The user applies changes manually in Xcode.

**Revert behavior without git:**
- "Revert this fix" → restore from `.backup` file
- "Revert all" → restore all `.backup` files
- After the audit completes successfully, offer to clean up `.backup` files

---

## Phase 7b: Visual Inspection Gate (MANDATORY — blocks ALL code changes)

> **⚠️ CRITICAL WARNING: NEVER modify UI code based solely on code analysis.**
>
> Code analysis can count colors, measure spacing values, and detect structural patterns — but it CANNOT tell you whether a view actually *looks* wrong. A view with 3/5 blue icons might look perfectly fine because the form layout separates them visually. A view with "excessive" padding might feel exactly right on a real device.
>
> **Every UI change must be validated by a human looking at the actual view.** This is non-negotiable. The user must visually inspect the view before ANY finding is approved or rejected.

### Why This Gate Exists

Without visual inspection, the skill will:
- Fix "problems" that aren't actually visible to users
- Make changes that look worse than the original
- Waste time on micro-optimizations that don't matter on a real screen
- Create a "revert everything" scenario because changes were made blind

### How It Works

**Before applying ANY code changes from the playbook, block on user visual inspection.**

Present this prompt (do NOT skip, do NOT auto-proceed):

```
questions:
[
  {
    "question": "Before making changes, you need to see the actual view. How are you viewing it?",
    "header": "Inspect",
    "options": [
      {"label": "Xcode Canvas (Recommended)", "description": "Open the file in Xcode — Canvas shows the view live. Fastest feedback loop."},
      {"label": "Running in Simulator", "description": "App is running in Simulator — I can navigate to the view"},
      {"label": "Running on device", "description": "App is running on a physical device"},
      {"label": "I'll view it later", "description": "Save the findings as a playbook — I'll apply changes when I can see the view"},
      {"label": "Explain pros/cons", "description": "Why does visual inspection matter for this?"}
    ],
    "multiSelect": false
  }
]
```

**If "Xcode Canvas":**
Confirm: "Open `[FileName].swift` in Xcode. The Canvas panel (right side) should show the view. If Canvas isn't visible, press Opt+Cmd+Return. Reply when you can see it."

**If "Running in Simulator" or "Running on device":**
Confirm: "Navigate to [ViewName] in the app. Reply when you can see it."

**If "I'll view it later":**
Save the full playbook to `.agents/ui-enhancer-radar/[date]-[view]-playbook.md`. Do NOT apply any code changes. Print:
```
📋 Playbook saved. Run `/ui-enhancer-radar` on this view again when you can see it.
   No code changes were made.
```
**Then skip Phases 7c-7e entirely and go to Phase 9 (Summary).**

**If "Explain pros/cons":**
Explain briefly, then re-prompt with the same options (minus Explain).

### Gate Rule

**Do NOT proceed to Phase 7c until the user confirms they can see the view.** There is no bypass. There is no "trust the code analysis" option. If the user cannot view the screen right now, the correct action is to save the playbook for later.

---

## Phase 7c: Guided Visual Review (MANDATORY — with user looking at the view)

**This is the core of the visual audit. The user is looking at the actual view. Walk through each finding collaboratively, then collect any additional issues the user spots.**

### Part 1: Walk Through Recommended Changes

For each finding in the playbook, present it as a question while the user is looking at the view:

```
Finding #[N]: [description]

Look at [specific element] on your screen.
[Describe what to look for — e.g., "Notice the three blue icons in a row: Appearance, Privacy, and iCloud. Do they blend together?"]

What do you think?
1. **Fix this** — [brief description of the change]
2. **Compact instead** — [if applicable: preserve visual identity at smaller size]
3. **Skip** — it looks fine on screen, leave it
4. **Explain pros/cons** — walk through the tradeoff before deciding
```

**Key behavioral rules:**
- **Describe what to LOOK FOR, not what's "wrong."** Let the user's eyes decide if it's actually a problem.
- **Accept "Skip" gracefully.** Code analysis flagged it, but the user's eyes override. Mark as Accepted with reason "Looks fine on screen per user inspection."
- **Never argue** if the user says it looks fine. They are literally looking at it. You are not.
- **Be specific** about which element to examine — don't say "check the colors"; say "look at the three icons next to Appearance, Privacy, and iCloud."

### Part 2: User-Spotted Issues (MANDATORY — always ask)

After walking through all recommended findings, **always** ask:

```
questions:
[
  {
    "question": "Now that you're looking at [ViewName], do you see anything else you'd like to change? Things code analysis might miss — alignment, spacing feel, visual weight, element sizing, color choices.",
    "header": "Your eyes",
    "options": [
      {"label": "Yes, I see some things", "description": "I'll describe what I'd like to change"},
      {"label": "No, looks good", "description": "The recommended changes cover everything"},
      {"label": "Actually, let me look at dark mode too", "description": "Toggle to dark mode before deciding"}
    ],
    "multiSelect": false
  }
]
```

**If "Yes, I see some things":**
Let the user describe in free text. For each item they mention:
1. Evaluate against design rules (push-back if needed — see Push-back guidance below)
2. Add to the approved changes list
3. Generate the playbook entry

**If "Actually, let me look at dark mode too":**
Wait for user to toggle. Then re-ask about both light and dark mode issues.

### What This Phase Produces

A **final approved list** of changes — combining:
- Recommended findings the user confirmed (from Part 1)
- User-spotted issues (from Part 2)
- With all "Skip" items removed

This list is the input to Phase 7d.

---

## Phase 7d: Apply Approved Changes (execute after visual review)

**Apply ONLY the changes approved in Phase 7c. One at a time, with keep/revert after each.**

### Per-Change Flow

For each approved change:

1. **Apply the fix** (Edit tool)
2. **If testable** (accessibility fix, dead code removal, component wiring change) — write a test. If purely visual (spacing, color, layout reorder) — skip the test.
3. **Show what changed** (brief description + files modified)
4. **Direct user to check the view:**

> "Check [ViewName] in [Canvas/Simulator/device]. The [element] should now [description of visible change]."

5. **Ask:**

```
questions:
[
  {
    "question": "Fix #N applied: [description]. How does it look?",
    "header": "Review",
    "options": [
      {"label": "Keep", "description": "Looks good, move to next fix"},
      {"label": "Compact instead", "description": "Revert removal, apply compacted version preserving visual identity"},
      {"label": "Revert this fix", "description": "Doesn't look right — undo this change, continue with others"},
      {"label": "Revert all", "description": "Undo everything back to checkpoint"},
      {"label": "Stop here", "description": "Keep changes so far, skip remaining fixes"}
    ],
    "multiSelect": false
  }
]
```

**If "Keep":**
After each kept fix that removes a reference to a component/property/array, check for dead code:
1. Grep the codebase for the removed reference
2. If the definition is now unreferenced, flag it: "The definition of `[name]` at [file:line] is now unused. Clean up?"
3. If the user confirms, remove the dead definition

**If "Compact instead":**
1. Revert: `git checkout -- [files modified by this fix]`
2. Apply compaction (Phase 6c techniques)
3. Direct user to check the view again
4. Re-ask with Keep / Revert

**If "Revert this fix":**
```bash
git checkout -- [files modified by this fix]
```
Continue to next fix.

**If "Revert all":**
```bash
git checkout -- [all files modified by ui-enhancer-radar in this session]
```
Report: "All UI Enhancer changes reverted."

**If "Stop here":**
Skip remaining fixes. Offer to save remaining playbook entries.

### Batch Revert Command

Available anytime: `/ui-enhancer-radar revert`

1. Shows files changed during the session
2. Asks for confirmation (Revert all / Show diff first / Cancel)

### Safety Rules

1. **Never force-push** — revert only affects local changes
2. **Never revert past user commits** — only revert ui-enhancer-radar edits
3. **No revert if already pushed** — warn and suggest `git revert` instead

---

## Phase 7e: Pattern Sweep — Similar View Queue (after applying changes to one view)

**After all approved changes are applied to a view, check if similar patterns exist in other views. Pre-generate tailored recommendations for each similar view, but require visual inspection before presenting or applying them.**

### Why pre-generate but gate on visual inspection

Code analysis CAN reliably detect structural similarity (same component, same color pattern, same layout issue). What it CANNOT do is tell you whether the fix from View A makes sense in View B — the context may be different. So:

- **Pre-generate:** Read each similar view's code, adapt the original fix to its specific structure, and prepare tailored recommendations. This is "thinking" work — safe to do without seeing the view.
- **Gate on viewing:** Present the tailored recommendations ONLY after the user can see the view. The user validates whether the recommendations make visual sense in this context.

This means the skill does the work upfront, and the user just validates — efficient without being blind.

### When to trigger

After Phase 7d completes (all approved changes applied or stopped), and at least one change was kept.

### Step 1: Find similar views and pre-generate recommendations

For each type of change that was applied:

1. **Build a grep query** from the change (e.g., if you changed `.blue` to `.purple` on a Privacy icon, search for other views with the same component/pattern)
2. **Search all view files** in Sources/
3. **For each matching view, read the code** and generate specific recommendations adapted to that view's structure. Don't just copy the original fix — account for differences:
   - Different number of sections/icons
   - Different semantic meanings (Privacy in one view vs. Network in another)
   - Different component parameters enabled
   - Different layout structure that may not need the same change

4. **Present the queue** with the full rating table:

```
Pattern: [description — e.g., "monochromatic blue icons in settings-style views"]

I found [N] views with the same pattern. I've read each one and prepared
specific recommendations based on what we changed in [original view]:

| # | View | Pattern Match | Tailored Recommendation | Severity |
|---|------|--------------|------------------------|----------|
| 1 | PrivacyNetworkView | 5/7 icons .blue | Change Network→cyan, VPN→purple, Cache→orange, keeping Privacy→blue | HIGH |
| 2 | CloudSyncView | 3/4 icons .blue | Change Zones→purple, Status→cyan, keeping Sync→blue | MEDIUM |
| 3 | NotificationSettingsView | 2/4 icons .blue | Minor — only 2 adjacent blues. Change Schedule→orange | LOW |
```

Then ask:

```
questions:
[
  {
    "question": "[N] similar views found. Walk through them one at a time? You'll view each before any changes.",
    "header": "Queue",
    "options": [
      {"label": "Start the queue (Recommended)", "description": "Open each view, review tailored recommendations, apply what looks right"},
      {"label": "Defer all", "description": "Add to DEFERRED.md for a future visual inspection session"},
      {"label": "Accept as-is", "description": "These views are fine — the pattern doesn't bother me elsewhere"},
      {"label": "Explain pros/cons", "description": "Walk through why consistency matters across views"}
    ],
    "multiSelect": false
  }
]
```

**There is no "Fix all now" option.** Every view requires visual inspection. Batch-applying visual changes across multiple views without looking at them is exactly what this skill is designed to prevent.

### Step 2: Walk through the queue (one view at a time)

For each view in the queue:

**2a. Direct user to open the view:**

> "Open **[ViewName]** in [Canvas / Simulator / device]. [Brief description of what the view shows — e.g., 'This is the privacy settings form with network, VPN, and cache sections.']"

Wait for user to confirm they can see it.

**2b. Present tailored recommendations:**

Once the user confirms, present the pre-generated recommendations for THIS specific view:

```
Based on what we changed in [original view], here's what I'd recommend for [this view]:

1. [Specific change — e.g., "Change Network section icon from .blue to .cyan"]
   Look at [specific element]. Does the blue blend with adjacent sections?

2. [Specific change — e.g., "Change VPN section icon from .blue to .purple"]
   Look at [specific element]. Would purple better distinguish this section?

Do you see the same issues here?
```

Then ask:

```
questions:
[
  {
    "question": "[ViewName]: [N] recommendations. How does it look?",
    "header": "Review",
    "options": [
      {"label": "Apply all", "description": "All recommendations look right for this view"},
      {"label": "Apply some", "description": "I'll tell you which ones to apply and which to skip"},
      {"label": "Skip this view", "description": "It looks fine as-is — move to next view"},
      {"label": "I see other things too", "description": "Apply recommendations + I'll add my own changes"},
      {"label": "Stop the queue", "description": "Done with similar views — keep remaining as-is or defer"}
    ],
    "multiSelect": false
  }
]
```

**If "Apply all":** Apply changes, direct user to verify visually, then Keep/Revert per Phase 7d flow.

**If "Apply some":** User specifies which. Apply only those.

**If "I see other things too":** Apply recommendations, then collect user-spotted issues (same as Phase 7c Part 2). This is valuable — the user is already looking at the view, so capture everything.

**If "Skip this view":** Mark as Accepted ("Looks fine on screen per user inspection"). Move to next view in queue.

**If "Stop the queue":** Ask whether remaining views should be Deferred (tracked) or Accepted (closed).

### Step 3: Queue progress

After each view in the queue, print a mini progress banner:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Similar views: [completed]/[total]
   [ViewA] ✅ Fixed | [ViewB] ✅ Skipped | [ViewC] ⏳ Next
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### What NOT to sweep

- Changes that were specific to one view's unique layout (not a pattern)
- Refactoring changes (sheet router enum) — these are per-view architectural decisions
- Changes the user "Skip"ped during visual review — if they said it looks fine in the original view, don't flag the same thing elsewhere
- Views the user already audited in this session — don't re-queue them

---

## Phase 7f: Refinement Loop (after all changes applied)

**After all findings are applied (or stopped early), offer the user a chance to refine the result. This is where users request tweaks like "add a background tint," "make the icon bigger," or "change the color."**

### When to trigger

After the last change in Phase 7d is resolved (Keep / Stop here), ask:

```
questions:
[
  {
    "question": "All changes applied. Would you like to refine anything?",
    "header": "Refine",
    "options": [
      {"label": "Done (Recommended)", "description": "Changes look good, move to tests"},
      {"label": "Refine an element", "description": "Tweak a specific element (color, size, spacing, background)"},
      {"label": "Compare before/after", "description": "See what changed before deciding"},
      {"label": "Question or new direction", "description": "Ask about the changes, suggest a different approach, or redirect"}
    ],
    "multiSelect": false
  }
]
```

### Refinement flow

**If "Refine an element":**
1. Ask the user what they want to change (free-form or screenshot)
2. **Evaluate the request** against the project's design system and CLAUDE.md before implementing
3. Apply the refinement
4. Show the result and re-ask with Keep / Revert / Refine again

### Push-back guidance (MANDATORY)

**Before implementing any refinement, check it against design rules. Push back when a refinement would:**

| Violation | Example | Push-back response |
|---|---|---|
| **Break colorblind safety** | "Make it green" | "Green isn't in the colorblind-safe palette — it's confused with red by ~8% of users. How about cyan or blue instead?" |
| **Break color palette** | "Use hot pink" | "That color isn't in the project's design system. The closest approved colors are pink (.pink) or purple (.purple). Which works?" |
| **Violate Dynamic Type** | "Use .system(size: 11)" | "Fixed font sizes don't scale with Dynamic Type. Use .caption or .footnote instead for the same visual size with accessibility support." |
| **Break visual consistency** | "Remove the icon circle" | "[ComponentName] uses icon circles in [N] other views. Removing it here would break consistency. Resize instead?" |
| **Undo the audit's improvement** | "Put the header back to full size" | "That would restore ~[N]pt of the space we just recovered. If you want the branding back, compact is the middle ground — it preserves identity at half the height." |
| **Break HIG compliance** | "Make the touch target 30pt" | "Apple HIG requires 44pt minimum touch targets. I can make it visually 30pt with a 44pt tap area using .contentShape()." |
| **Exceed space budget** | "Add a subtitle and description" | "Adding that text would push content below the fold. Consider putting it behind a disclosure or (?) button instead." |
| **App Store rejection risk** | See table below | Flag with "App Store risk" and cite the specific guideline |

### App Store Review guardrails

**UI changes that are known to trigger App Store rejections. Flag these BEFORE implementing:**

| Risk | Guideline | What triggers it | Push-back response |
|---|---|---|---|
| **Missing accessibility** | 2.1 (Performance) | Removing `.accessibilityLabel()`, VoiceOver support, or Dynamic Type | "Removing this accessibility label could trigger rejection under guideline 2.1. VoiceOver users won't be able to interact with this element." |
| **Non-functional UI** | 2.1 (Performance) | Adding buttons/links that do nothing, placeholder UI, "coming soon" labels | "Empty buttons or 'coming soon' UI can trigger rejection. Either wire it up or remove it." |
| **iPad layout broken** | 2.4.1 (Multitasking) | Hardcoding widths that break iPad split view, removing landscape support | "This layout would break on iPad multitasking. Use adaptive layout (ViewThatFits, size classes) instead of fixed widths." |
| **Missing back/dismiss** | 4.0 (Design) | Removing dismiss buttons from sheets, creating navigation dead ends | "Removing this dismiss button would create a dead end — users can't escape. App Review flags this under guideline 4.0." |
| **Misleading UI** | 2.3.1 (Accurate) | Icons/labels that suggest functionality the app doesn't have | "This icon implies [feature] but the app doesn't support it. App Review flags misleading UI under guideline 2.3.1." |
| **Minimum font size** | 2.1 (Performance) | Text below 11pt that doesn't scale | "Text this small may be flagged as unreadable. Use `.caption2` (11pt) as the minimum, and ensure it scales with Dynamic Type." |
| **Privacy UI** | 5.1.1 (Data Collection) | Removing permission explanations, hiding privacy controls | "Removing this explanation could violate guideline 5.1.1. Users must understand why data is collected before granting permission." |

### How to push back

1. **Explain why** — cite the specific rule (CLAUDE.md, HIG, colorblind palette, cross-view pattern)
2. **Offer an alternative** — never just say "no," always suggest what WOULD work
3. **Defer to the user** — if they insist after hearing the tradeoff, implement it with a note: "Applied as requested. Note: this deviates from [rule]."

### Diminishing returns guardrail

Track refinement count per element. After **3 refinements on the same element**:

> "This element has been refined 3 times. Further tweaks may not be visible to users. Suggest moving on — you can always revisit later. Continue refining or move on?"

This prevents infinite micro-adjustment loops while respecting the user's autonomy.

### When to skip refinement

- User chose "Done" — proceed to Phase 8 (Tests)
- Single-domain audit (e.g., `/ui-enhancer-radar space`) — refinement is less relevant for focused checks
- No visual changes were made (e.g., only performance or accessibility fixes)

---

## Phase 8: Tests

**Before asking, analyze the changes and make a recommendation.** State whether tests are needed and why, then ask.

**How to decide:**
- **No tests needed:** Pure styling (color, font, padding), layout reordering, section merging, spacing changes, renaming labels, enabling existing component parameters — recommend skipping
- **Tests recommended:** New reusable component extracted, new interaction behavior added, conditional logic changed, accessibility labels modified — recommend adding

```
questions:
[
  {
    "question": "[Recommendation: Skip/Add] — [brief reason]. Would you like to add tests?",
    "header": "Tests",
    "options": [
      {"label": "Skip tests", "description": "Verify visually by running the app"},
      {"label": "Add tests for new components", "description": "Generate tests for any extracted or new components"},
      {"label": "Add preview coverage", "description": "Ensure #Preview blocks cover all states"},
      {"label": "Full test suite", "description": "Unit tests + previews + accessibility checks"}
    ],
    "multiSelect": false
  }
]
```

**If "Skip tests"** — proceed to Phase 9. Most UI enhancer changes (spacing, color, layout reordering, compaction) are verified visually, not via tests.

### How to verify changes visually

**After applying changes, suggest a verification method:**

| Method | Best for | How |
|--------|----------|-----|
| **Xcode Canvas preview (Recommended)** | Quick visual check after each change | Open the modified file in Xcode, Canvas auto-refreshes as code changes. No build required. |
| **Run on simulator** | Full interaction testing, navigation flows | Cmd+R in Xcode. Verify the view looks right in context with real data. |
| **Run on device** | Final validation, touch targets, real-world sizing | Build to physical device for accurate colors, text sizes, and haptics. |
| **Screenshot comparison** | Before/after side-by-side | Capture simulator screenshots before and after; compare in Preview.app or Finder. |
| **Dark mode toggle** | Dark mode verification | Toggle Appearance in Xcode Canvas or Settings > Developer > Dark Appearance on device. |
| **Dynamic Type** | Accessibility text scaling | Change text size in Canvas controls or Settings > Accessibility > Display & Text Size. |

**Always mention Canvas as the recommended method** — it gives immediate feedback without building, and the user can see changes as they're applied.

### What Gets Tests

| Change Type | Test Type | Example |
|-------------|-----------|---------|
| New component extracted | Unit test (Swift Testing) | `WarrantyStatusCircle` properties and states |
| Layout change | Preview verification | `#Preview` with all states |
| Accessibility change | Accessibility audit test | VoiceOver label coverage |
| Interaction change | UI test (if warranted) | Button tap triggers expected action |
| Performance change | No test needed | Verified by profiling |

### Test Template

```swift
import Testing
@testable import [AppModule]

@Suite("[ComponentName] Tests")
struct [ComponentName]Tests {
    @Test("Renders correct state for [condition]")
    func [testName]() {
        // Arrange
        // Act
        // Assert with #expect
    }
}
```

### When to Skip Tests
- Pure styling changes (color, font, padding) — verify visually
- Layout reordering — verify via preview/screenshot
- Removing unused code — no behavior to test

---

## Phase 9: Summary & Progress Tracking

### Files Changed Summary (MANDATORY)

**Before asking about progress, always list every file modified during this audit:**

```
## Files Modified

| File | Changes |
|------|---------|
| `Sources/Views/Tools/ToolsView.swift` | Removed action bar, enabled showThemeToggle, full-width single-tool grid |
| `Sources/Views/Tools/ToolCategory.swift` | Merged input+output → importExport, renamed CSV Import → Spreadsheet Import |
| `Documentation/Development/FUTURE_FEATURES.md` | Added XLSX import item |

Total files: 3 | Lines added: X | Lines removed: Y
```

**This helps users who return to the project later know exactly what was touched.**

### Progress Question

```
questions:
[
  {
    "question": "Changes applied. Want to measure the improvement?",
    "header": "Progress",
    "options": [
      {"label": "Done for now (Recommended)", "description": "Save the report and move on"},
      {"label": "Re-audit now", "description": "Run the audit again and compare scores"},
      {"label": "Capture new screenshot", "description": "Take a fresh screenshot and compare side-by-side"}
    ],
    "multiSelect": false
  }
]
```

### Progress Report Format

```
## Progress: [ViewName]

UI Enhancer v[version]

| Domain | Before | After | Change |
|--------|--------|-------|--------|
| Space Efficiency | 4/10 | 7/10 | +3 |
| Visual Hierarchy | 6/10 | 8/10 | +2 |
| Overall | 6.4/10 | 8.1/10 | +1.7 |

Content-to-chrome ratio: 39% → 63% (+24%)
Findings resolved: 8/12
Tests added: 5
```

### Phase Progress Banner (CRITICAL — BLOCKING requirement in Normal and Pre-Approved modes)

**After EVERY phase and EVERY commit, your NEXT output MUST be the progress banner followed by the next-phase `AskUserQuestion`. Do not output anything else first. Do not leave a blank prompt.**

**Hands-Free mode exception:** In Hands-Free mode, the progress banner still prints, but the next-phase `AskUserQuestion` is suppressed (per the Hands-Free Mode precedence rules in § Skill Introduction). Replace the AskUserQuestion with the Hands-Free completion message instead.

The skill has **9 numbered top-level phases** (the user-facing structure). Several phases have lettered sub-phases (2b, 6b/6c/6d, 7a/7b/7c/7d/7e/7f) — these are implementation steps within a parent phase and print as substeps, not as standalone phases.

**Banner template (top-level phase completion):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Phase [N] of 9 complete: [phase name]

⏱  Next: Phase [N+1] — [phase name] (~[time estimate])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Banner template (sub-phase completion within a top-level phase):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Phase [N] (substep [letter]) of 9 complete: [substep name]

⏱  Next: Phase [N] (substep [next-letter]) — [substep name] (~[time estimate])
   or → Phase [N+1] if this was the last substep
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

This keeps the denominator stable at 9 while still announcing fine-grained progress through Phase 7's six substeps (7a-7f).

Phase time estimates:
| Phase | Name | Est. Time |
|-------|------|-----------|
| 1 | Interview | ~2 min |
| 2 (with substep 2b) | Gather Input + View Type Classification | ~3 min |
| 3 | Screenshot Analysis | ~2 min |
| 4 | Code Analysis | ~3-5 min |
| 5 | Domain Analysis | ~5-10 min |
| 6 (with substeps 6b/6c/6d) | Report + Content Preservation + Compaction + Compensation | ~3-5 min |
| 7 (with substeps 7a/7b/7c/7d/7e/7f) | Implementation Playbook through Refinement Loop | ~25-50 min total |
| 8 | Tests | ~5-10 min |
| 9 | Summary | ~2 min |

Then immediately prompt for the next phase (or substep, where applicable). **After a commit**, reprint the banner and auto-prompt. Never leave a blank prompt.

---

### Pipeline Mode Behavior (Tier 2/3)

When running inside a Tier 2 or Tier 3 pipeline (detected via `tier` field in `.radar-suite/session-prefs.yaml`):

1. **On skill start:** Emit the pipeline-level progress banner (see `radar-suite-core.md` Pipeline UX Enhancements #1). If this is the first skill in the pipeline OR `experience_level` is Beginner/Intermediate, also emit the audit-only statement.
2. **On skill completion:** Emit a per-skill mini rating table marked "PRELIMINARY" (see Pipeline UX Enhancements #2). Then emit the pipeline-level progress banner showing this skill as complete.
3. **Within-skill phase banners** (above) are still emitted normally in addition to the pipeline-level banners.

### short_title Requirement (v2.1)

Every finding MUST include a `short_title` field (max 8 words). This is the human-scannable label used in pipeline banners, pre-capstone summaries, and ledger output.

Example: `short_title: "Low contrast on dark mode card"`

All finding ID references in output (tables, banners, summaries) use the format: `RS-NNN (short_title)`.

---

## Optional Features

These features are available but not run by default. User must explicitly request them.

### Device Size Simulation (Optional)

Analyze how the view behaves across device sizes by examining spacing, padding, and layout constraints in code.

```
/ui-enhancer-radar --devices
```

| Device | Width | Check |
|--------|-------|-------|
| iPhone SE | 375pt | Does content fit? Truncation? |
| iPhone 16 | 393pt | Standard layout |
| iPhone 16 Pro Max | 430pt | Extra space utilized? |
| iPad 11" | 820pt | Split view behavior? |

### Simulator Screenshot Capture (Optional)

Automatically capture a screenshot from a running simulator.

```
/ui-enhancer-radar --capture
```

```bash
# List available simulators
xcrun simctl list devices booted

# Capture screenshot
xcrun simctl io booted screenshot /tmp/ui-enhancer-radar-capture.png
```

### Before/After Screenshot Comparison

When `/ui-enhancer-radar compare` is used, or when the user wants to see visual progress:

**Automated workflow (if simulator is running):**
```bash
# Capture "after" screenshot
xcrun simctl io booted screenshot /tmp/ui-enhancer-radar-after.png
```
Then read both the original screenshot (provided at start) and the new capture, comparing side by side.

**Manual workflow (guide the user):**
1. "Take a screenshot now (Cmd+Shift+4 on macOS, or Cmd+S in Simulator)"
2. "Apply the changes"
3. "Take another screenshot"
4. "Open both in Preview.app — Window > Tile All to Left/Right for side-by-side"

**What to compare:**
- Content-to-chrome ratio: did it improve?
- Visual hierarchy: is the primary content more prominent?
- Color variety: did monochromatic sections gain differentiation?
- Space recovery: is content visible that was previously below the fold?
- Consistency: do the changes match the app's existing patterns?

### Batch Mode (`/ui-enhancer-radar batch [path]`)

Audit all views in a directory, build the View Profile in one pass, then rank views by severity.

**How it works:**
1. Glob for `*.swift` files in the specified path
2. For each file, classify the view type (Phase 2b) and run a lightweight analysis (skip interview — use default "General polish, All domains, Moderate")
3. Build the View Profile from all views simultaneously — this gives the strongest baseline for cross-view consistency
4. Rank views by overall severity score
5. Present the ranked list with top findings per view

**Output format:**
```
## Batch Audit: [path]
*[N] views analyzed | [date]*

| # | View | Type | Score | Top Finding |
|---|------|------|-------|-------------|
| 1 | PrivacyNetworkView | Settings/form | 3/10 | Monochromatic — 14/18 elements gray |
| 2 | ArchiveView | List | 5/10 | Section headers undifferentiated |
| 3 | DashboardView | Dashboard | 6/10 | Sidebar-content redundancy (macOS) |
| ... | ... | ... | ... | ... |

Run `/ui-enhancer-radar` on any view above for a full audit.
```

**After presenting the ranked list, offer a seamless transition:**

```
questions:
[
  {
    "question": "[ViewName] scored lowest ([score]/10). Start a deep audit on it now?",
    "header": "Next",
    "options": [
      {"label": "Deep audit worst view (Recommended)", "description": "Open [ViewName] in Canvas/simulator, then walk through findings visually"},
      {"label": "Pick a different view", "description": "Choose which view to audit from the ranked list"},
      {"label": "Done for now", "description": "Save batch results to handoff, audit views later"},
      {"label": "Explain more", "description": "What does a deep audit do that batch scan doesn't?"}
    ],
    "multiSelect": false
  }
]
```

**If user selects a view:** Transition directly into the full audit flow (Phase 1 interview → Phase 7 implementation). Do NOT require the user to re-invoke the skill — continue in the same session. The batch scan findings for that view become the starting point for Phase 5 (Domain Analysis), pre-populated with what the batch already found.

**Batch mode limitations:**
- No interview — uses defaults. Run individual audits for design-intent-aware analysis.
- No screenshot analysis — code-only. Provide screenshots for visual domains.
- No implementation — findings only. Run individual audits to apply fixes.
- **Transition to individual audit is seamless** — no need to re-invoke the skill.

---

## Analysis Heuristics Reference

### Content-to-Chrome Ratio

```
Chrome = status bar + nav bar + tab bar + custom headers + toolbars + search + pickers
Content = everything else

Targets:   iPhone >60% | iPad >70% | macOS >75%
Flags:     <50% Critical | 50-60% High | 60-70% Medium | >70% Good
```

### Vertical Space Budget (iPhone)

```
Viewport: ~667pt (SE) to ~852pt (Pro Max)
Status bar: 54pt (Dynamic Island) / 44pt (notch) / 20pt (none)
Nav bar: 44pt | Tab bar: 49pt + 34pt safe area

Budget: Header max 80pt | Actions max 44pt (one row) | Content >60% of remaining
```

### Visual Hierarchy Scoring

```
For each element, assign visual weight:
  Size: Large=3, Medium=2, Small=1
  Weight: Bold=2, Regular=1, Light=0
  Color: Bright=2, Standard=1, Muted=0
  Position: Top-left=3, Center=2, Bottom-right=1

Highest weight should be primary content.
If chrome/status/badge scores highest → hierarchy issue.
```

### Common Anti-Patterns

| Anti-Pattern | Example | Fix |
|-------------|---------|-----|
| Date Dominance | "Sep 1982" in title3.bold | Caption or status circle |
| Header Stack | Logo+title+subtitle+search+picker+buttons | Collapse to essentials |
| Badge Overload | 5 status badges on one row | Prioritize, hide secondary |
| Combined Controls | Two functions in one button | Separate into distinct controls |
| Permanent Hints | "Tap any field to edit" on every visit | Show once, then remove |
| Negative Numbers | "-15,892 days" for expired items | "Expired" label or icon |
| Orphaned Chrome | Parent header visible on child view | Ensure child replaces parent |
| Giant Padding | 100pt padding for 44pt floating button | Match to actual element size |
| Hardcoded Colors | `Color.white` in dark mode | Use semantic `.background` |
| Heavy View Body | 200-line body with inline logic | Extract computed properties |

---

## Edge Case Guardrails

**Known situations where the skill can cause problems if not handled carefully:**

| Edge Case | Risk | Guardrail |
|---|---|---|
| **No `#Preview` block** | Canvas verification recommended but impossible | Check for `#Preview` before recommending Canvas. If missing, offer to add one or suggest simulator instead. |
| **Shared component modification** | Changing a shared component (e.g., `ContentIllustratedHeader`) breaks all views that use it | NEVER modify shared components directly. Always apply changes at the call site. If a component needs changing, flag it as a cross-cutting change and confirm scope. |
| **Multiplatform views** | Platform-specific heuristics applied to the wrong platform; changes on one side break the other | See multiplatform guardrail below. |

### Multiplatform guardrail (MANDATORY for any view with `#if os()` blocks)

**Before making any changes to a multiplatform view:**

1. **Detect platform blocks** — grep the file for `#if os(iOS)`, `#if os(macOS)`, `#else`. If found, the view is multiplatform.
2. **Analyze each platform separately** — don't apply iPhone heuristics (44pt touch targets, 852pt viewport) to macOS code, or macOS heuristics (menu bar, sidebar, window chrome) to iOS code.
3. **After every change, check the other platform:**
   - If editing iOS-specific code: does macOS still have equivalent functionality? (e.g., dismiss buttons, theme toggle, toolbar actions)
   - If editing macOS-specific code: does iOS still have equivalent functionality?
   - If editing shared code (outside `#if` blocks): does it work on BOTH platforms?
4. **Watch for duplicate controls** — adding something to shared code that already exists in a platform-specific block creates duplicates on that platform (e.g., theme toggle in both header AND macOS toolbar).
5. **Platform-specific metrics:**

| Metric | iOS | macOS |
|---|---|---|
| Min touch/click target | 44pt | 24pt (but 44pt preferred) |
| Viewport height | 667-932pt | Variable (window) |
| Navigation | TabView, NavigationStack | NavigationSplitView, sidebar |
| Dismiss mechanism | Swipe down, X button | Close button, Esc key |
| Typography baseline | San Francisco, Dynamic Type | San Francisco, fixed sizes acceptable |
| **Large files (1000+ lines)** | Partial file reads may miss context, leading to incomplete findings | Read the full file in sections before generating findings. If the file exceeds 1000 lines, note it and focus on the visible sections. |
| **Rename cascades** | Renaming an enum case (e.g., `ToolCategory.input` → `.importExport`) requires updating every `switch` statement | After any rename, grep the codebase for the old name to verify no references remain. Build before moving to the next fix. |

---

## Decision Prompt Rules (MANDATORY — all user-facing decisions)

Every `AskUserQuestion` that presents a design decision, implementation choice, or finding resolution MUST include an **"Explain pros/cons"** option:

- **[Recommended option] (Recommended)** — [one-line description]
- **[Alternative(s)]** — [one-line description each]
- **Accept as-is** — [why this is safe to leave] (where applicable)
- **Explain pros/cons** — Walk through the tradeoffs before deciding

If the user selects "Explain pros/cons": present a brief analysis (3-5 bullets), then re-prompt with the same options (minus "Explain pros/cons").

**Never silently note findings "for future."** Every finding discovered during the audit must be presented with the full Issue Rating Table and a decision prompt (Fix / Defer / Accept / Explain pros/cons).

### Finding Dependencies and Fingerprints

When creating findings, populate these optional fields where relationships are obvious:

- **`depends_on`/`enables`:** Visual fixes sometimes depend on each other -- e.g., a color system change enables contrast fixes across multiple views. If one fix must come before another, populate with finding IDs.
- **`pattern_fingerprint`/`grep_pattern`/`exclusion_pattern`:** Assign fingerprints for generalizable UI anti-patterns (e.g., `hardcoded_color`, `missing_dynamic_type`, `insufficient_contrast`, `missing_dark_mode_adaptive`).

---

## Finding Resolution (MANDATORY — end of every run)

**Principle:** Every finding must reach a terminal state. "Deferred" is not terminal — it's temporary.

### Terminal States

| State | Meaning | How |
|-------|---------|-----|
| **Fixed** | Code changed, test written, committed | Phase 7 apply workflow |
| **Planned** | Added to `DEFERRED.md` with severity, effort, reason, release gate | User chose "save for later" |
| **Accepted** | User explicitly said "this is fine" | User chose "accept as-is" |

### Self-Resolution (end of every run)

After Phase 9 completes (or if the user chose "plan only"), check for unresolved findings in this session. If any exist, present:

```
You have [N] unresolved findings from this audit:

| # | Finding | Severity | Effort |
|---|---------|----------|--------|
| 1 | ... | ... | ... |

Every finding needs a decision:
1. **Fix now** — enter apply workflow for these items
2. **Plan it** — add to DEFERRED.md (tracked, reviewed before release)
3. **Accept as-is** — explicitly sign off (removed from tracking)
4. **Explain more** — walk through what each finding means
```

For each finding, the user chooses Fix / Plan / Accept. Update the handoff YAML accordingly:
- Fix → move to `findings_fixed` after apply completes
- Plan → move to `findings_planned`, write to `DEFERRED.md`
- Accept → move to `findings_accepted`

### `fix-deferred` Subcommand

When invoked via `/ui-enhancer-radar fix-deferred`:

1. Read own handoff YAML (`.agents/ui-audit/ui-enhancer-radar-handoff.yaml`)
2. Extract findings that were not applied in previous runs
3. If empty → "No deferred findings from previous ui-enhancer-radar runs."
4. If non-empty → present findings table (already rated from original run)
5. For each finding, ask: Fix now / Plan it / Accept as-is
6. Fix items enter Phase 7 apply workflow. Plan items go to DEFERRED.md. Accept items go to `findings_accepted`.
7. Update handoff YAML with resolved statuses

### `verify` Subcommand (lightweight re-check)

When invoked via `/ui-enhancer-radar verify`: Read own handoff YAML, grep for each finding's pattern in the codebase, classify as Still present / Resolved / Changed, update handoff accordingly. Print summary. Much faster than a full re-audit. See data-model-radar SKILL.md for full verify logic.

### Startup Check

On every invocation, check for `DEFERRED.md` at the project root. If it exists and contains ui-enhancer-radar items:

```
📋 You have [N] planned items from previous ui-enhancer-radar audits in DEFERRED.md.
   [M] are pre-release priority. Run `/ui-enhancer-radar fix-deferred` to resolve them.
```

### DEFERRED.md Format

If DEFERRED.md doesn't exist, create it when the first item is planned. Format:

```markdown
# Deferred Findings

Items intentionally deferred from radar audits. Review before each release.

| # | Finding | Source | Severity | Release Gate | Effort | Reason | Date | Review By |
|---|---------|--------|----------|-------------|--------|--------|------|-----------|
```

**Release Gate values:** Pre-release / Post-release / Next major

**Review By:** Default 90 days from deferral date. Capstone flags overdue items.

---

## Cross-Skill Handoff

UI Enhancer Radar complements **data-model-radar** (model layer), **ui-path-radar** (navigation paths), **roundtrip-radar** (data safety), and **capstone-radar** (ship readiness). Findings from one skill inform the others.

### Cross-Skill Resolution (after fixing any finding)

When a fix resolves a finding that originated from ANOTHER skill's handoff, update that skill's handoff YAML. Read the other skill's handoff, find the matching finding in `findings_deferred[]` or `for_capstone_radar.blockers[]`, move it to `findings_fixed[]` (or `resolved[]`) with the fix commit hash and `resolved_by: "ui-enhancer-radar"`. This prevents stale handoffs from blocking capstone's ship recommendation.

### On Completion — Write Handoff

After completing a view audit, write/update `.agents/ui-audit/ui-enhancer-radar-handoff.yaml`:

```yaml
source: ui-enhancer-radar
date: <ISO 8601>
project: <project name>
views_audited: <count>

# File timestamps — enables staleness detection by consuming skills
file_timestamps:
  <file path>: "<ISO 8601 mod date>"
  # one entry per unique file referenced in issues

findings_fixed:
  - finding: "<description>"
    severity: "<CRITICAL|HIGH|MEDIUM|LOW>"
    fix_commit: "<git hash>"

findings_deferred:
  - finding: "<description>"
    severity: "<CRITICAL|HIGH|MEDIUM|LOW>"
    reason: "<why deferred>"
    group_hint: "<optional batching suggestion>"

findings_planned:
  - finding: "<description>"
    severity: "<CRITICAL|HIGH|MEDIUM|LOW>"
    release_gate: "<Pre-release|Post-release|Next major>"
    reason: "<why deferred>"
    deferred_md_row: true
    group_hint: "<optional batching suggestion>"

findings_accepted:
  - finding: "<description>"
    severity: "<CRITICAL|HIGH|MEDIUM|LOW>"
    reason: "<why accepted>"
    accepted_date: "<ISO 8601>"

for_ui_path_radar:
  # Visual issues that suggest structural navigation problems
  suspects:
    - view: "<view file>"
      finding: "<e.g., button with no visible action>"
      question: "<is this button wired to a destination?>"
      group_hint: "<optional batching suggestion>"

for_roundtrip_radar:
  # Views with data binding concerns found during visual audit
  suspects:
    - workflow: "<affected workflow>"
      finding: "<e.g., form field not reflected in saved data>"
      file: "<file:line>"
      question: "<does this field round-trip correctly?>"
      group_hint: "<optional batching suggestion>"

for_capstone_radar:
  # Visual/UX issues that affect ship readiness
  blockers:
    - finding: "<description>"
      urgency: "<CRITICAL|HIGH>"
      group_hint: "<optional batching suggestion>"
```

### File Timestamps

For each unique file path referenced across all issues, record its modification date:

```bash
stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%SZ" "<file path>"
```

Enables consuming skills to detect **staleness** — if a view file changed after the audit, visual findings may be stale.

### Group Hints

Optional field for batching related issues. Common hints:
- `spacing_issues` — padding, margins, layout
- `color_accessibility` — contrast, colorblind safety
- `hierarchy_issues` — visual prominence problems
- `hig_violations` — Apple HIG non-compliance
- `dark_mode` — light/dark mode issues

**Automatic:** This file is always written so other audit skills can pick up where this one left off. No user action needed.

### End-of-Run Directory Cleanup (MANDATORY)

Per the Artifact Lifecycle rules in `radar-suite-core.md`, before returning from this skill:
1. List files in `.radar-suite/`.
2. Move any stale single-use handoffs (`RESUME_PHASE_*.md`, `RESUME_*.md` except `NEXT_STEPS.md`, `*-v[0-9]*.md`) to `.radar-suite/archive/superseded/`.
3. Confirm Class 1 persistent-state files (`ledger.yaml`, `session-prefs.yaml`, `DEFERRED.md`) are in-place rewrites — not dated or versioned.
4. Confirm Class 2 handoff files are overwrites, not appends.

This prevents `.radar-suite/` from accumulating stale prose artifacts across runs.

### Write to Unified Ledger (MANDATORY)

After writing the handoff YAML, also write findings to `.radar-suite/ledger.yaml` following the Ledger Write Rules in `radar-suite-core.md`:

1. Read existing ledger (or initialize if missing)
2. Record this session (timestamp, skill name, build)
3. For each finding: check for duplicates, assign RS-NNN ID if new, set `impact_category`, compute `file_hash`
4. Write updated ledger

**Impact category mapping for ui-enhancer-radar findings:**
- Color contrast failure (WCAG) → `ux-broken` (accessibility violation)
- Missing dark mode support → `ux-degraded`
- Spacing/alignment issues → `polish`
- HIG violations → `polish`
- Visual hierarchy problems → `ux-degraded`
- Colorblind safety violations → `ux-broken`

### On Startup — Read Ledger & Handoffs (MANDATORY)

Before Phase 1 (Interview), read the unified ledger and ALL companion handoff YAMLs:

```
Read .radar-suite/ledger.yaml (if exists) — check for existing findings to avoid duplicates
Read .agents/ui-audit/data-model-radar-handoff.yaml (if exists)
Read .agents/ui-audit/ui-path-radar-handoff.yaml (if exists)
Read .agents/ui-audit/roundtrip-radar-handoff.yaml (if exists)
Read .agents/ui-audit/capstone-radar-handoff.yaml (if exists)
```

**Ledger check:** If the ledger contains findings for views you're about to audit, note their RS-NNN IDs. When you find the same issue, update the existing finding instead of creating a new one.

**Regression check:** For any `fixed` findings in the ledger whose `file_hash` no longer matches the current file, flag for re-verification per the Regression Detection protocol in `radar-suite-core.md`.

**Parse `for_ui_enhancer_radar` sections.** Each companion can direct findings to this skill. Look for:
- `for_ui_enhancer_radar.suspects[]` — views another skill flagged as having visual issues
- `for_ui_enhancer_radar.priority_views[]` — views another skill wants audited first

If found, incorporate as context during the interview phase (e.g., "capstone-radar wants ToolsHelpView audited first — monochromatic icons flagged"). These are not pre-confirmed findings — verify each one independently.

**What each companion provides:**
- data-model-radar — model fields that should be displayed but aren't (missing UI for data)
- ui-path-radar — dead buttons to remove before visual audit
- roundtrip-radar — data issues that affect view correctness, computed data never displayed
- capstone-radar — priority views from ship readiness grading

If not found, proceed normally.

---

## Compliance Self-Check (MANDATORY — run before final summary)

**Before writing the final summary, handoff YAML, or session wrap-up, execute this mechanical checklist. Do NOT skip it. Do NOT summarize without running it first.**

Review your own output from this session and fill in each row:

```
| # | Gate | Check | Pass? | Gaps |
|---|------|-------|-------|------|
| 1 | Table Format | Every findings table has 9 columns (Finding, Confidence, Urgency, Risk:Fix, Risk:NoFix, ROI, Blast Radius, Fix Effort, Status) | ? | |
| 2 | Test Gate | Every committed fix has a test — or a documented exemption (visual, dead code, singleton) | ? | |
| 3 | Visual Inspection | User confirmed they could see every view BEFORE any code changes were applied | ? | |
| 4 | Pattern Sweep | Every similar-view finding was presented with full table + decision prompt (no silent "noted for future") | ? | |
| 5 | Decision Prompts | Every design decision included "Explain pros/cons" option | ? | |
| 6 | Finding Resolution | Every finding reached terminal state (Fixed, Planned, Accepted) — no orphaned "deferred" items | ? | |
```

**If ANY gate fails**, print the gap, fix it, then proceed:
- **Visual Inspection fail:** If code was changed without user viewing the screen, flag it: "Changes to [view] were applied without visual confirmation. Verify in Canvas/simulator now, or revert."
- **Other gates:** See data-model-radar SKILL.md for full gate-checking instructions.

---

## End Reminder

After every phase/commit: print progress banner → `AskUserQuestion` → never blank prompt.

**Gates (all mandatory):**

| Gate | Rule |
|------|------|
| **Visual Inspection** | NEVER modify UI without user viewing it first. Phase 7b is non-negotiable. If user can't see view, save playbook and stop. |
| **Context Exhaustion** | After 50 tool calls, downgrade findings to `probable (long context)`. Add `context_exhaustion_after: [N]` to handoff. |
| **Table Format** | ALL findings tables need 9 columns. Count before output. No exceptions. |
| **Test Gate** | Test with each fix. Pure visual/dead code exempt (document why). |

**Phase 7 order:** 7a (Commit) → 7b (Visual Gate) → 7c (Guided Review) → 7d (Apply) → 7e (Pattern Sweep) → 7f (Refinement). Never skip 7b or 7c.

</ui-enhancer-radar>
