---
name: ui-path-radar
description: 'UI path tracer for SwiftUI/UIKit apps. 5-layer audit with 34 issue categories and 19 automated checks: discover entry points, trace flows, detect dead ends and broken promises, evaluate UX impact, verify data wiring. Supports targeted trace, diff against previous audits, and handoff to planning skills. Triggers: "trace UI paths", "find dead ends", "/ui-path-radar".'
version: 2.2.0  # orphan feature detection (was 2.1.0)
author: Terry Nyberg
license: Apache-2.0
allowed-tools: [Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion]
inherits: radar-suite-core.md
metadata:
  tier: execution
  category: analysis
---

# UI Path Radar

> **Quick Ref:** 5-layer UI path audit: discover entry points → trace flows → detect issues → evaluate UX → verify data wiring. Output: `.ui-path-radar/` in project root.

You are performing a systematic UI path audit on this SwiftUI application.

**Required output:** Every finding MUST include Urgency, Risk, ROI, and Blast Radius ratings using the Issue Rating Table format. Do not omit these ratings.

## Quick Commands

| Command | Description |
|---------|-------------|
| `/ui-path-radar` | Full 5-layer audit |
| `/ui-path-radar layer1` | Discovery only — find all entry points |
| `/ui-path-radar layer2` | Trace — trace critical paths |
| `/ui-path-radar layer3` | Issues — detect problems across codebase |
| `/ui-path-radar layer4` | Evaluate — assess user impact |
| `/ui-path-radar layer5` | Data wiring — verify real data usage |
| `/ui-path-radar trace "A → B → C"` | Trace a specific user flow path |
| `/ui-path-radar diff` | Compare current findings against previous audit |
| `/ui-path-radar fix` | Generate fixes for found issues |
| `/ui-path-radar status` | Show audit progress and remaining issues |
| `--show-suppressed` | Show findings suppressed by known-intentional entries |
| `--accept-intentional` | Mark current finding as known-intentional (not a bug) |

## Overview

UI Path Radar uses a 5-layer approach:

| Layer | Purpose | Est. Time (small / large codebase) | Output |
|-------|---------|-------------------------------------|--------|
| **Layer 1** | Pattern Discovery — Find all UI entry points | ~1-2 min / ~3-5 min | Entry point inventory |
| **Layer 2** | Flow Tracing — Trace critical paths in depth | ~2-3 min / ~5-8 min | Detailed flow traces |
| **Layer 3** | Issue Detection — Categorize issues across codebase | ~2-4 min / ~5-10 min | Issue catalog |
| **Layer 4** | Semantic Evaluation — Evaluate from user perspective | ~1-2 min / ~3-5 min | UX impact analysis |
| **Layer 5** | Data Wiring — Verify features use real data | ~2-4 min / ~5-10 min | Data integrity report |

> **Codebase size guide:** Small = <200 files, Large = 500+ files. Estimate from `find Sources -name "*.swift" | wc -l`.

## Issue Categories

Each category maps to a **default axis** (see `skills/radar-suite-axis-classification/SKILL.md` for the framework). The default axis may be overridden by the verification checklist (see "Axis Classification Protocol" section below) — e.g., a "Dead End" finding whose branch is unreachable from any production call site gets reclassified from `axis_1_bug` to `axis_3_dead_code` by the reachability trace.

| Category | Severity | Default Axis | Description |
|----------|----------|--------------|-------------|
| Dead End | 🔴 CRITICAL | axis_1_bug (→ axis_3_dead_code if unreachable) | Entry point leads nowhere |
| Wrong Destination | 🔴 CRITICAL | axis_1_bug | Entry point leads to wrong place |
| Mock Data | 🔴 CRITICAL | axis_1_bug | Feature shows fabricated data when real data exists |
| Destructive Without Confirmation | 🔴 CRITICAL | axis_1_bug | Delete/clear happens immediately without confirmation dialog |
| Silent State Reset | 🔴 CRITICAL | axis_1_bug | In-progress work lost when navigating away and back (form clears, selections lost) |
| Incomplete Navigation | 🟡 HIGH | axis_1_bug | User must scroll/search after landing |
| Missing Auto-Activation | 🟡 HIGH | axis_1_bug | Expected mode/state not set |
| Unwired Data | 🟡 HIGH | axis_1_bug (→ axis_3_smelly if model field has no read/write sites) | Model data exists but feature ignores it |
| Platform Parity Gap | 🟡 HIGH | axis_1_bug | Feature works on one platform, broken on another |
| Promise-Scope Mismatch | 🟡 HIGH | axis_1_bug | Specific CTA opens generic/broad destination |
| Buried Primary Action | 🟡 HIGH | axis_1_bug | Primary button hidden below scroll fold |
| Dismiss Trap | 🟡 HIGH | axis_1_bug | Only visible action is Cancel/back, no forward path |
| macOS Dismiss Trap | 🔴 CRITICAL | axis_1_bug | Sheet/modal relies ONLY on `.presentationDragIndicator` / `.presentationDetents` (iOS-only) with NO macOS-visible dismiss control (Done/Cancel/Close button, `SheetContainer`, or `@Environment(\.dismiss)` button). macOS has NO swipe-to-dismiss → user is TRAPPED. Heuristic: a presented View that uses drag-indicator/detents but the file has no cancellationAction/confirmationAction/Button("Done"\|"Cancel"\|"Close")/xmark/SheetContainer/dismiss(). Beware false positives where the presented view delegates to a wrapper that provides the dismiss — trace through to the wrapped view. (Real instances 2026-06: MaintenanceTaskListView, LegacyShareSheet.) Detect mechanically with a build-script grep: flag any file using drag-indicator/detents that lacks a dismiss signal, bypassable via a `// dismiss-parity: ok` comment. |
| Context Dropping | 🟡 HIGH | axis_1_bug | Navigation path loses item context between platforms or via notifications |
| Notification Nav Fragility | 🟡 HIGH | axis_1_bug | Untyped NotificationCenter dict used for navigation context |
| Sheet Presentation Asymmetry | 🟡 HIGH | axis_2_scatter (→ axis_1_bug if only one platform works) | Different presentation mechanisms per platform for same feature |
| Empty State Missing | 🟡 HIGH | axis_1_bug (→ axis_3_dead_code if empty case unreachable) | No guidance when list/view is empty — users think app is broken |
| Error Recovery Missing | 🟡 HIGH | axis_1_bug | Error displayed but no retry button or recovery path |
| Keyboard Obscures Input | 🟡 HIGH | axis_1_bug | Text field covered by keyboard with no scroll adjustment (iOS) |
| Permission Denied Dead End | 🟡 HIGH | axis_1_bug | Permission denied but no explanation or path to Settings |
| Modal Stacking | 🟡 HIGH | axis_1_bug | Multiple sheets/alerts open on top of each other |
| Navigation Container Mismatch | 🟡 HIGH | axis_1_bug | selectedSection value not a valid tag in current TabView/sidebar |
| Two-Step Flow | 🟢 MEDIUM | axis_1_bug | Intermediate selection required |
| Missing Feedback | 🟢 MEDIUM | axis_1_bug | No confirmation of success |
| Gesture-Only Action | 🟢 MEDIUM | axis_1_bug | Feature only accessible via swipe/long-press |
| Loading State Trap | 🟢 MEDIUM | axis_1_bug | Spinner with no cancel/timeout/escape |
| Stale Navigation Context | 🟢 MEDIUM | axis_2_scatter (→ axis_1_bug if user observes stale data) | Cached context with no clearing/validation mechanism |
| Phantom Touch Target | 🟢 MEDIUM | axis_1_bug | Visual element looks tappable but isn't (icon without action, card without nav) |
| Race Condition UX | 🟢 MEDIUM | axis_1_bug | User can trigger conflicting operations simultaneously (double-tap, edit while sync) |
| Invisible Selection | 🟢 MEDIUM | axis_1_bug | Item is selected/active but visual indicator missing or too subtle |
| Inconsistent Pattern | ⚪ LOW | axis_2_scatter | Same feature accessed differently |
| Orphaned Code | ⚪ LOW | axis_3_dead_code (if unreachable) or axis_3_smelly (if reachable but unjustified) | Feature exists but no entry point |
| Command-Palette-Only Feature | 🟡 HIGH | axis_1_bug | Feature reachable only via command palette (QuickFind/Go To), no visible UI entry point |
| Deeply Buried Feature | 🟡 HIGH | axis_1_bug | User-facing feature requires 4+ taps from nearest tab bar item |
| Double-Nested Navigation | ⚪ LOW | axis_2_scatter | NavigationStack inside NavigationStack causing doubled nav bars |

### Axis Classification Protocol (MANDATORY — before emitting any finding)

Every finding must be classified on the 3-axis framework and pass the schema gate in `radar-suite-core.md` before emission. The protocol:

1. **Assign default axis** from the table above based on the issue category.

2. **Run required verification checks:**
   - **Reachability trace** (MANDATORY for Dead End, Empty State Missing, Orphaned Code) — walk upstream from the flagged branch at least 2 call-site levels. If no production call site reaches it, RECLASSIFY to `axis_3_dead_code`.
   - **Whole-file scan** (MANDATORY for "missing handler" categories: Empty State Missing, Error Recovery Missing, Missing Feedback) — read the ENTIRE file (not just the flagged region) for handlers elsewhere. If found, RECLASSIFY to `axis_2_scatter`.
   - **Branch enumeration** (MANDATORY for Platform Parity Gap, Sheet Presentation Asymmetry) — read BOTH sides of every `#if os(iOS)` / `#else` block before claiming platform-broken. Stuffolio has 266 such blocks; dropping the `#else` branch is the #1 false-positive source.
   - **Pattern citation lookup** (MANDATORY for every finding, regardless of category) — grep the audited codebase for a similar pattern shape. Cite by file:line in the `better_approach` field. A finding without this citation is REJECTED.

3. **Write coaching fields.** Populate `current_approach`, `suggested_fix`, `better_approach` (with citation), `better_approach_tradeoffs` — all mandatory. Load coaching examples via `.radar-suite/project.yaml` `coaching_examples` array.

4. **Validate against schema gate.** Run the gate checks from `radar-suite-core.md`. If any mandatory field is missing, either fix the finding or downgrade confidence to `possible` and increment `rejected_no_citation` in the handoff.

5. **Write the finding** to the handoff YAML with full axis + coaching fields.

**Reclassification logging:** When the verification checklist reclassifies a finding's axis (e.g., "Dead End" → `axis_3_dead_code` via reachability trace), log the reclassification in the finding's `verification_log` so capstone and the user can see the framework caught a would-be false positive:

```yaml
verification_log:
  - check: reachability_trace
    result: "no production call site found; reclassified from axis_1_bug (Dead End) to axis_3_dead_code"
```

**Axis summary block.** At the end of the handoff, include:
```yaml
axis_summary:
  axis_1_bug: [count]
  axis_2_scatter: [count]
  axis_3_dead_code: [count]
  axis_3_smelly: [count]
  rejected_no_citation: [count]
```

## Design Principles

### 1. Honor the Promise
> When a button/card says "Do X", tapping it should DO X.
> Not "go somewhere you might find X."

### 2. Context-Aware Shortcuts
> If user's context implies a specific item, skip pickers.

### 3. State Preservation
> When navigating to a feature, set up the expected state.

### 4. Consistent Access Patterns
> Same feature should be accessed the same way everywhere.

### 5. Data Integrity
> If the app tracks data relevant to a feature, the feature must use it.
> Never show mock/hardcoded data when real user data exists.
> Never ignore model relationships that would improve decisions.

### 6. Primary Action Visibility
> The primary action must be visible without scrolling after the user completes the key interaction.
> Pin Save/Continue/Done buttons outside ScrollView or in toolbar. Never bury them below tall content.

### 7. Escape Hatch
> Every view must have a visible way to go forward OR back. Cancel alone is not enough after user completes a step.

### 8. Gesture Discoverability
> Every action available via gesture (swipe, long-press) should also be accessible via a visible button or menu.

### Freshness

Base all findings on current source code only. Do not read or reference
files in `.agents/`, `scratch/`, or prior audit reports. Ignore cached
findings from auto-memory or previous sessions. Every finding must come
from scanning the actual codebase as it exists now.

---

## Before Starting

All setup questions were captured during the Skill Introduction call below (`USER_EXPERIENCE`, `FIX_MODE`, `DELIVERY`, `PRESENCE_MODE`). Do NOT re-ask them here. Show the one-line settings reminder from § Skill Introduction and proceed to the audit.

If any of the four variables is missing for some reason (e.g., session-prefs file deleted mid-session), re-run the full Skill Introduction call before continuing — never partially re-ask, since the questions are interdependent (Question 4 overrides Question 1 — see Hands-Free Mode below).

### Permission Modes

#### Normal Mode
- Read any file without asking.
- Edit files only if user chose auto-fix and the fix is isolated to the audited flow.
- Build and run tests without asking.
- If a fix breaks the build, restore the original code and document as "Documented."

#### Hands-Free Mode
**Guarantees no blocking prompts.** Only uses: `Read`, `Grep`, `Glob`.
Does NOT use: `Bash`, `Edit`, `Write`, `AskUserQuestion`.

**Precedence rules (load-bearing — Hands-Free wins all ties):**

1. **Hands-Free overrides `FIX_MODE`.** Even if Question 2 was answered `Auto-fix safe items` or `Batch mode`, no fixes are applied in Hands-Free mode. All findings are emitted with `Status: Deferred (hands-free)` in the Issue Rating table. The Fix Plan is still produced (so the user can act on it on return), but no Wave 1-4 fix application runs.
2. **Hands-Free suppresses the next-wave `AskUserQuestion`.** The "CRITICAL — BLOCKING requirement" rule under § Progress Banner applies in Normal and Pre-Approved modes only. In Hands-Free mode, the progress banner still prints, but the `AskUserQuestion` call is omitted and replaced by the completion message below.
3. **Hands-Free defers all write-tool layer steps.** The following steps require Edit/Write and are deferred until the user returns: writing `.ui-path-radar/layer3-results.yaml`, `.ui-path-radar/layer5-data-wiring.yaml`, `.ui-path-radar/canaries.yaml`, `.ui-path-radar/handoff.yaml`, `.agents/ui-audit/ui-path-radar-handoff.yaml`, and `.radar-suite/ledger.yaml`. To resolve: in Hands-Free mode, the skill emits these YAML files **inline in the conversation as fenced YAML blocks** so the user can persist them on return. Inline emission does not count as a write.
4. **Hands-Free covers all 5 layers, not just 1-4.** Layer 5 step 7 (write `layer5-data-wiring.yaml`) and Layer 3's cross-layer verification table edits both fall under rule 3 above — emitted inline rather than written to disk.

When complete:
```
⏱ Hands-free audit complete through Layer [N] of 5: [plain description].
  Layers requiring write access: [list]
  Findings deferred: [count] (no fixes applied — Hands-Free mode)
  Handoff YAML + ledger entries: emitted inline above; copy to .ui-path-radar/, .agents/ui-audit/, and .radar-suite/ when you return
  Reply to continue with supervised steps.
```

#### Pre-Approved Mode
Full speed, no restrictions. Assumes you've set up permissions.

### Permission Setup (for unattended runs)

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

> **Tip:** If you frequently run audit-only layers (1-4), the Hands-free mode eliminates permission prompts entirely without changing any settings.

### Context Budget

If context is running low, prioritize in this order:
1. Finish the current phase
2. Emit findings for what you've audited so far
3. Skip remaining unaudited flows

Never start auditing a new flow you can't finish.

### Experience-Level Adaptation

Adjust ALL output based on the user's experience level:

#### Beginner
- Use plain language with real-world analogies.
- Define technical terms on first use in parentheses.
- Explain flags/categories and why they matter.
- Include file context: "DashboardView.swift (the main home screen) line 118"
- Explain the "why" behind each suggestion.
- Use compact 4-column table format.

#### Intermediate
- Use standard SwiftUI terminology without defining basics.
- Explain non-obvious patterns.
- Standard file:line format.
- Full 9-column format with brief finding descriptions.

#### Experienced (default)
- Concise findings. No definitions or explanations of standard patterns.
- Recommendations: what to fix, where.
- Full 9-column format, terse findings.

#### Senior/Expert
- Minimal findings text. No prose between tables.
- File:line + one-line fix description only.
- Skip: progress explanations, design principle citations, category definitions.
- Full 9-column format, maximally compressed.

#### Enforcement Rule
At the **start of each layer**, silently check: "Am I writing at the selected experience level?" Do NOT drift toward "Experienced" as a default.

---

## Execution Instructions

### Skill Introduction (MANDATORY — run before anything else)

**This section replaces `radar-suite-core.md § Session Setup` for the ui-path-radar entry point.** Do NOT also run core's 4-question Session Setup — its questions are consolidated below. On first invocation, ask all four setup questions in a single `AskUserQuestion` call. The "Before Starting" section above reuses these answers and never re-asks.

**Question 1: "What's your experience level with Swift/SwiftUI?"**
- **Beginner** — New to Swift. Plain language, analogies, define terms on first use.
- **Intermediate** — Comfortable with SwiftUI basics. Standard terms, explain non-obvious patterns.
- **Experienced (Recommended)** — Fluent with SwiftUI. Concise findings, no definitions.
- **Senior/Expert** — Deep expertise. Terse, file:line only, skip explanations.

**Question 2: "How should fixes be handled?"**
- **Auto-fix safe items (Recommended)** — Apply isolated, low-blast-radius fixes automatically. Present cross-cutting fixes and design decisions for approval first.
- **Review first** — Present all findings with ratings, then ask before making any changes. Fixes still happen — you just approve each wave first.
- **Batch mode** — Approve all fixes in each wave at once.

**IMPORTANT:** All three modes lead to fixes. "Review first" means the user sees the plan before code changes — it does NOT mean "skip fixes and jump to handoff." After presenting findings, ALWAYS offer to fix them regardless of which mode was selected. (Exception: Hands-Free mode overrides this — see Question 4.)

**Question 3: "How should results be delivered?"**
- **Display only (Recommended)** — Show findings in the conversation. No file written.
- **Report only** — Write findings to `.ui-path-radar/[DATE]-audit.md`. Minimal conversation output. **Before writing**, per Artifact Lifecycle (Class 3) in `radar-suite-core.md`, archive any existing `.ui-path-radar/*-audit.md` to `.ui-path-radar/archive/superseded/`.
- **Display and report** — Show findings in the conversation AND write to file.

**Question 4: "Will you be stepping away during the audit?"**
- **I'll be here (Recommended)** — Normal mode. Permission prompts may appear for writes/edits.
- **Hands-Free (walk away safe)** — Read-only tools (Read, Grep, Glob) only. No Bash, no Edit, no Write, no AskUserQuestion. **Hands-Free overrides Question 2:** all fixes are deferred regardless of `FIX_MODE`. The progress banner still prints, but the `AskUserQuestion` next-wave prompt is suppressed; the skill emits the "audit complete through Layer N" completion message instead (see Hands-Free Mode below).
- **Pre-Approved** — You have already configured Claude Code permissions. Run at full speed.

Store as: `USER_EXPERIENCE`, `FIX_MODE`, `DELIVERY`, `PRESENCE_MODE`. Apply to ALL output for the session, per `radar-suite-core.md § Experience-Level Output Rules`. Also persist to `.radar-suite/session-prefs.yaml` per `radar-suite-core.md § Session Persistence`.

**Question 5 (optional follow-up): "Would you like a brief explanation of what this skill does?"**
- **No, let's go (Recommended)** — Skip explanation, proceed to audit.
- **Yes, explain it** — Show one of the explanations below adapted to experience level, then proceed.

**Experience-adapted explanations:**

- **Beginner**: "UI Path Radar checks every button, link, and menu item in your app to make sure they actually work. Think of it like walking through every door in a building to verify none are locked, lead nowhere, or open to the wrong room. It finds 'dead ends' (buttons that do nothing), 'broken promises' (a button says 'Export PDF' but opens the wrong screen), and missing features. It runs in 5 layers, each going deeper — from finding all the buttons, to tracing what happens when you tap them, to checking if the data behind them is real."

- **Intermediate**: "UI Path Radar systematically audits all UI entry points (sheets, navigation links, toolbar buttons, deep links, notifications) across your SwiftUI app. It traces user flows end-to-end, flags dead ends, promise-scope mismatches, platform gaps, and orphaned state. Five layers: discovery → flow tracing → issue detection → UX evaluation → data wiring verification."

- **Experienced**: "5-layer UI path audit across 34 issue categories and 19 automated checks: entry point discovery, flow tracing, issue detection, semantic UX evaluation, and data wiring verification. Outputs issue rating tables with fix plans."

- **Senior/Expert**: "Entry point → flow trace → issue scan → UX eval → data wiring. 34 categories, 19 checks. Rating tables + fix plans."

**User impact explanations:** Can be toggled at any time with `--explain` / `--no-explain`. When enabled, each finding gets a 3-line companion explanation (what's wrong, fix, user experience before/after). See `radar-suite-core.md` for format and rules. Store as `EXPLAIN_FINDINGS` (default: false).

**Experience-level auto-apply (ui-path-radar local):** If `USER_EXPERIENCE` = Beginner, auto-set `EXPLAIN_FINDINGS = true` and default sort to `impact`. If Senior/Expert, default sort to `effort`. Apply all output rules from `radar-suite-core.md § Experience-Level Output Rules`.

---

## Shared Patterns

See `radar-suite-core.md` for: Tier System, Pipeline UX Enhancements, Table Format, Plain Language Communication, Work Receipts, Contradiction Detection, Finding Classification, Audit Methodology, Context Exhaustion, Progress Banner, Issue Rating Tables, Handoff YAML schema, Known-Intentional Suppression, Pattern Reintroduction Detection, Experience-Level Output Rules, Implementation Sort Algorithm, short_title requirement.

## Pre-Scan Startup (MANDATORY — before any layer scan)

1. **Known-intentional suppression:** Run the protocol in `radar-suite-core.md § Known-Intentional Suppression`. Core owns this — do not restate the steps here.

2. **Pattern reintroduction detection:** Run the protocol in `radar-suite-core.md § Pattern Reintroduction Detection`. Core owns this.

---

When invoked, perform the audit:

### If no arguments or "full":

**Before starting, print:**
```
Full Audit: 5 layers — estimated total: ~10-30 min depending on codebase size
  Layer 1: Find all entry points → Layer 2: Trace how users navigate → Layer 3: Detect issues → Layer 4: Evaluate user impact → Layer 5: Verify data wiring
```

Run all 5 layers sequentially, outputting findings to `.ui-path-radar/` in the project root.
**Between layers, print:** `✓ Layer [N] of 5 complete: [plain description] — starting Layer [N+1]: [plain description]`

### If "layer1" or "discovery": `enumerate-required`

**Before starting**, count Swift files and print an estimate:
```
Layer 1: Discovery — scanning [N] Swift files
  Estimated time: ~[1-2 min for <200 files / 3-5 min for 500+ files]
  Progress will be shown after each tier completes.
```

**Scan in 3 tiers, from top-level down. After completing each tier, print a progress line:**

#### Tier 1: Top-Level Structure
1. Find the app's navigation skeleton: `TabView`, `NavigationSplitView`, sidebar sections
2. For each top-level destination, identify the view file
3. Scan for sheet routing enums: `grep -r "enum.*Sheet\|enum.*SheetType" Sources/`
4. Scan for navigation state: `grep -r "selectedSection\|selectedTab\|activeSheet" Sources/`

**After Tier 1, print:** `Layer 1: ✓ Tier 1 Structure (1/3) — found [N] tabs, [N] sidebar items, [N] sheet enums`

#### Tier 2: Entry Point Patterns
Scan for these patterns across ALL source files:

| Pattern | Search | Priority |
|---------|--------|----------|
| Sheets | `.sheet(`, `.fullScreenCover(` | HIGH — primary feature access |
| Navigation | `NavigationLink(`, `.navigationDestination(` | HIGH — screen transitions |
| Tab views | `TabView`, `.tabItem(` | HIGH — top-level entry points |
| Buttons with state | `Button(.*{` near `showing` or `activeSheet` or `selected` | HIGH — action triggers |
| Deep links | `onOpenURL`, `DeepLinkRouter`, URL scheme handlers | HIGH — external entry points |
| Notification nav | `.onReceive(NotificationCenter`, `NotificationCenter.default` near navigation/sheet state | HIGH — invisible triggers |
| Spotlight/Handoff | `onContinueUserActivity`, `CSSearchableItemActionType` | HIGH — system search entry |
| MenuBarExtra / CommandGroup | `MenuBarExtra`, `CommandGroup`, `.commands {` | HIGH — macOS app menu commands |
| File operations | `.fileImporter`, `.fileExporter`, `PhotosPicker` | MEDIUM — data entry paths |
| Context menus | `.contextMenu {` | MEDIUM — long-press actions |
| Swipe actions | `.swipeActions` | MEDIUM — list row shortcuts |
| Toolbars | `.toolbar {` with `Button` | MEDIUM — persistent actions |
| Keyboard shortcuts | `.keyboardShortcut` | MEDIUM — power user entry |
| Promotion cards | `PromotionCard`, `CompactPromotionCard`, dismissable feature cards | MEDIUM — conditional entry |
| Confirmation dialogs | `.confirmationDialog(`, `.alert(` | LOW — exit gates, not entry points |

**Zero-match handling:** When a scanned pattern returns 0 results, do NOT silently skip it. Report: `"<PatternName>: 0 matches — pattern not present in codebase"`. This prevents confusion where a category appears "clean" when it was never scanned.

**After Tier 2, print:** `Layer 1: ✓ Tier 2 Patterns (2/3) — found [N] entry points across [N] patterns`

#### Tier 3: Container View Enumeration
For views that are **feature hubs** (tools, settings, reports, dashboards), don't just log the hub as one entry point — enumerate each actionable card/row inside it as a sub-entry-point. These hubs often contain 10-20+ features that the Tier 2 scan misses because they're wired through enum-based routing, not direct `.sheet()` modifiers.

Also identify the **primary detail view** (the view users spend the most time in) and audit its sheet/action surface separately — it often has the largest entry point count.

**After Tier 3, print:** `Layer 1: ✓ Tier 3 Containers (3/3) — enumerated [N] hub views, [N] sub-entry-points added`

#### Catalog Rules

**For each entry point found:**

| Field | Description |
|-------|-------------|
| Label | What the user sees (button text, card title, menu item) |
| Location | File and line where the trigger lives |
| Action type | Sheet, navigation, state change, deep link, notification, keyboard shortcut |
| Destination | What view/screen opens |
| Depth | Hierarchy level: L0 (tab/sidebar) → L1 (section view) → L2 (detail/sheet) → L3 (sub-sheet) |
| Condition | When is this entry point visible? (e.g., "only if items exist", "after dismissal: never") |
| Flags | Suspicious patterns (see below) |

**Flags to apply during discovery:**

| Flag | Description |
|------|-------------|
| `dead_end` | Trigger exists but destination is missing or broken |
| `promise_mismatch` | Specific label opens generic/broad destination |
| `incomplete_nav` | Lands on section top, not the specific feature |
| `missing_state` | Navigation without setting up expected mode/state |
| `two_step` | Requires intermediate picker before reaching feature |
| `no_feedback` | Action completes without confirmation |
| `orphaned` | View exists but has no entry point |
| `platform_gap` | Works on one platform, broken on another |
| `alias` | Entry point mirrors another entry point's destination. Group aliases separately — they confirm redundancy, not new paths |
| `conditional` | Entry point disappears after user action. **Scan for:** `@AppStorage` keys containing `hasDismissed`, `hasUsed`, `hasScanned`, `hasSeen`; `if !settings.someFlag` guards around UI elements; `.onboardingComplete` checks. |
| `invisible` | Entry point triggered by notification, deep link, or Spotlight — not visible in the UI hierarchy |
| `callback_wiring` | View takes an `onComplete`, `onItemSelected`, or similar closure — trace what the closure does |
| `container_mismatch` | Navigation sets `selectedSection` to a value that may not be a valid tag in the current container |

#### De-duplication Rules

- **Context menus repeated on identical UI elements** (e.g., same menu on product/receipt/nameplate photos): catalog once, note multiplier (e.g., "×3 photo types")
- **QuickFind / Spotlight / Siri Shortcuts** that mirror other entry points: tag as `alias`, group in a separate "Meta-Entry-Points" section at the end
- **Confirmation dialogs**: list separately as "Exit Gates" — they guard destructive actions, not open features

#### Discovery Output

Group the table by hierarchy level, not flat:

```
## L0: Top-Level Navigation (tabs, sidebar)
| # | Label | Location | Action | Destination | Flags |

## L1: Section Views (dashboard, tools, settings, detail)
| # | Label | Location | Action | Destination | Flags |

## L2: Feature Sheets & Sub-Navigation
| # | Label | Location | Action | Destination | Flags |

## Meta-Entry-Points (QuickFind, Spotlight, Deep Links, Keyboard Shortcuts)
| # | Label | Location | Action | Mirrors # | Flags |

## Exit Gates (Confirmation Dialogs)
| # | Label | Location | Guards |
```

After the tables, list:
- Total entry points found (primary + aliases)
- Count by flag type
- Count by depth level
- Recommended flows to audit in Layer 2 (flagged entries first, deepest paths second)

### If "layer2" or "trace" (no path argument): `enumerate-required`

**Before starting, print:**
```
Layer 2: Flow Tracing — [N] flagged entry points to trace
  Estimated time: ~[2-3 min for <5 flows / 5-8 min for 10+ flows]
```

1. Read flagged entry points from Layer 1
2. For each flagged entry point, trace the complete user journey. **After each flow, print:** `Layer 2: ✓ Flow [N]/[total] — "[flow name]"`
3. Document in `layer2-traces/flow-XXX.yaml`
4. Identify gaps between expected and actual journeys

**IMPORTANT — Trace into callbacks and closures:**
When tracing a flow, do NOT stop at the view presentation. If a sheet presents a view that takes an `onComplete`, `onItemSelected`, or similar closure, trace what that closure does. An empty closure `{ }` or unimplemented handler is a dead end.

**IMPORTANT — Verify navigation container constraints:**
At each navigation step, if `selectedSection = .X` is set:
1. Check whether `.X` is a valid tag in the current navigation container (TabView tags on iPhone, sidebar items on iPad/macOS)
2. If it's not a valid tag, the assignment is a no-op — flag as dead end
3. Different platforms may have different valid tags — check both

**Check both pre-action AND post-action feedback:**
- Pre-action: Is there a confirmation dialog before destructive operations?
- Post-action: Is there a toast, haptic, or visual confirmation after non-destructive actions (save, duplicate, archive)?

#### Flow Trace Template

```yaml
flow_trace:
  id: "flow-001"
  name: "Feature Name from Entry Point"
  entry_point: "entry-point-id"

  steps:
    - step: 1
      action: "User taps [button/card/menu item]"
      file: "SourceFile.swift:78"
      code: "selectedSection = .tools"
      issues: []

    - step: 2
      action: "App navigates to [destination]"
      file: "DestinationView.swift"
      result: "[what user sees]"
      issues:
        - category: "incomplete_navigation"
          detail: "User must scroll to find feature"

  expected_journey:
    - "[step 1]"
    - "[step 2]"

  actual_journey:
    - "[step 1]"
    - "[extra step]"
    - "[step 2]"

  gap_analysis:
    type: "[issue category]"
    extra_steps: 2
    user_confusion_risk: "medium"
```

### If "trace" with path argument (e.g., `trace "Dashboard → Add Item → Photo → Save"`):
Targeted flow trace — trace a specific user journey described in natural language:
1. Parse the path description into discrete steps (split on `→`, `->`, or `,`)
2. For each step, identify the SwiftUI view, button, or action that triggers it
3. Trace the complete code path step by step (file, line, state changes, view transitions)
4. At each step, check for issues (Buried Primary Action, Dismiss Trap, Promise-Scope Mismatch, Missing Feedback, Callback Wiring)
5. Document the trace and any issues found
6. Output: Issue Rating Table for any findings, plus the step-by-step trace

### If "layer3" or "issues": `mixed`

**Before starting, print:**
```
Layer 3: Issue Detection — scanning [N] entry points for issues
  Estimated time: ~[2-4 min for <100 entries / 5-10 min for 200+]
```

> **CRITICAL: Do NOT delegate Layer 3 checks to Explore subagents.** Run each check directly using Grep/Glob/Read tools against the full codebase. Subagent sampling causes false negatives — a previous audit checked 1 of 7 list views for gesture-only actions and concluded "all clear," missing 6 findings.

**Step 0 — Cross-layer verification (MANDATORY):**
Before scanning for new issues, re-verify ALL flagged findings from Layer 1 and Layer 2. For each:
- Check whether the flag still holds when you look at extension files (`+Sections.swift`, `+Actions.swift`, etc.) and ViewModel bindings (`@Bindable`, `Binding<Bool>` parameters)
- If a finding was based on "this @State var is never set to true" — also check if it's passed as a `$binding` to a ViewModel method or child view that sets `.wrappedValue = true`
- **Retract** false positives explicitly: `~~#N — [original finding]~~ RETRACTED: [reason]`
- Print: `Layer 3: ✓ Cross-layer verification — [N] confirmed, [N] retracted`

**Then proceed with automated checks 1-18 below.**

After each check, print: `Layer 3: ✓ Check [N] [check name] ([N]/19) — [N] findings so far`

> **Numbering note:** Checks 1-10, 10b, 11-18 = 19 total. Check 10b ("Notification Type-Safety") was added in v2.0 as a strict sub-case of Check 10. Rather than renumber 11-18 (which would invalidate every external reference to "Check 11" etc.), 10b is kept as a suffix and counted in the `/19` denominator. When printing progress for Check 10b, use the literal token `10b`: `Layer 3: ✓ Check 10b Notification Type-Safety (11/19) — N findings so far`.

---

### Automated Check 1: Sheet Case Coverage

**What it detects:** Enum cases defined in a sheet routing enum (e.g., `DashboardSheetType`) that have no corresponding handler in the `sheetContent(for:)` switch — the case exists but presenting it shows nothing or crashes.

**How to detect:**
```bash
# Step 1: Find all sheet enum cases
grep -n "case " <SheetEnumFile>.swift | grep -v "//"

# Step 2: Find all handled cases in sheet content switch
grep -n "case \." <SheetContentFile>.swift

# Step 3: Compare — any cases in Step 1 without a handler in Step 2?
```

**Also check the reverse:** handlers that reference cases no longer in the enum (dead handlers).

**Safe patterns (do NOT flag):**
- Cases with a `default:` handler that provides meaningful content
- Deprecated cases with explicit comments

**Severity:** 🔴 CRITICAL (sheet opens blank or crashes)

---

### Automated Check 2: Orphaned Views

**What it detects:** View structs defined (`struct XxxView: View`) but never instantiated anywhere outside of `#Preview` blocks.

**How to detect:**
```bash
# Step 1: Find all View struct definitions
grep -rn "struct.*: View" Sources/ --include="*.swift" | grep -v "Preview\|test\|Test"

# Step 2: For each view name, search for instantiation
# A view is "used" if its name appears as `ViewName(` somewhere outside its own file and outside #Preview
grep -rn "ViewName(" Sources/ --include="*.swift" | grep -v "#Preview\|Preview {"
```

**Also check for orphaned modifiers:** Structs conforming to `ViewModifier` that are defined but `.modifier()` is never called with them, and no `.xxxModifier()` extension applies them.

**Safe patterns (do NOT flag):**
- Views used only in previews if explicitly marked as preview-only
- Views instantiated dynamically via reflection or factory patterns
- Views referenced in `@ViewBuilder` results

**Severity:** ⚪ LOW (dead code, no user impact — but may indicate ~hundreds of lines of wasted code)

---

### Automated Check 3: Promise-Scope Mismatch

**What it detects:** A specific-sounding CTA ("Track AppleCare+", "Set Warranty") that opens a generic/overly-broad destination. The user expects a focused action but gets a container with the action buried among unrelated content.

**How to detect:**
```bash
# Step 1: Find sheet presentations that use generic wrappers
grep -rn "EditItemSheetWrapper\|FullEditView\|SettingsView" Sources/ --include="*.swift" \
  | grep -i "sheet\|present"

# Step 2: Find onItemSelected callbacks — trace what they open
grep -A5 "onItemSelected" Sources/ --include="*.swift" \
  | grep "showing\|activeSheet\|EditItem"

# Step 3: Cross-reference specific CTA labels vs destination scope
grep -B5 "EditItemSheetWrapper" Sources/ --include="*.swift" \
  | grep "Track\|Set\|Add\|Manage\|Configure"
```

**Programmatic detection logic:**
1. Find CTA labels with specific verbs ("Track X", "Set Y", "Add Z", "Manage W")
2. Trace to the destination view
3. Count distinct sections/concerns in that destination
4. If CTA specificity = 1 concern but destination has 3+ unrelated sections → flag

**Safe patterns (do NOT flag):**
- General CTAs ("Edit Product", "Settings") opening broad views — this is expected
- CTAs that open a pre-scrolled or pre-filtered version of a broad view

**Severity:** 🟡 HIGH (user confusion, broken trust in CTAs)

---

### Automated Check 4: Entry Point Coverage (Orphan Feature Detection)

**What it detects:** Features defined in routing enums (sheet types, navigation sections, command palette items) that lack a visible UI entry point outside the command palette. Users who don't use the command palette will never discover these features.

**Three-tier detection:**

**Tier 1: Enumerate all feature destinations**
```bash
# Find all sheet/routing enum cases (adapt patterns to the project)
grep -n "case " Sources/ --include="*.swift" -r | grep -i "Sheet\|SheetType\|Section\|Destination"

# Find all command palette / QuickFind items
grep -rn "QuickFindItem\|QuickFindSheet" Sources/ --include="*.swift" | grep "case "
```

For each case found, record it in a feature inventory table:
| Feature | Enum | Has Primary UI Entry? | Has Command Palette Entry? | Tap Depth |

**Tier 2: Cross-reference against visible UI triggers**
```bash
# Find all places each enum case is triggered from visible UI
# (buttons, navigation links, list rows — NOT command palette)
grep -rn "activeSheet = \.featureName" Sources/ --include="*.swift" | grep -v "QuickFind\|CommandPalette"
grep -rn "selectedSection = \.featureName" Sources/ --include="*.swift"

# Count tap depth: how many taps from a tab bar item to reach each trigger?
# Tab bar = 0, view on tab = 1, button on that view = 2, sheet from button = 3, etc.
```

**Tier 3: Classify each feature**

| Classification | Criteria | Severity |
|---|---|---|
| **Orphan** | No UI trigger at all (only in code, never presented) | 🔴 CRITICAL |
| **Command-palette-only** | Trigger exists only in QuickFind/Go To/Spotlight | 🟡 HIGH |
| **Deeply buried** | Primary UI trigger exists but requires 4+ taps | 🟡 HIGH |
| **Adequately surfaced** | Reachable in 1-3 taps from a tab | No finding |

**What to flag:**
- Features with zero visible UI entry points (command-palette-only or orphan)
- Features requiring 4+ taps when they serve a primary user need (not a power-user utility)
- Features whose only entry point is a gesture (swipe, long-press) with no visual hint

**Safe patterns (do NOT flag):**
- Power-user/maintenance utilities (photo optimizer, data cleanup) at 3+ taps — these are correctly placed as secondary tools
- Features intentionally gated behind settings (e.g., Legacy Wishes behind `legacyWishesEnabled`)
- Debug/developer-only features
- Command palette entries that mirror an existing primary UI entry point (aliases)

**Severity:** 🔴 CRITICAL if feature is user-facing with no entry point, 🟡 HIGH if command-palette-only or 4+ taps for a primary feature, ⚪ LOW if internal/utility

---

### Automated Check 5: Buried Primary Action

**What it detects:** Primary action button (Save, Continue, Done, Submit) placed inside a ScrollView after tall content, making it invisible without scrolling. Users see only "Cancel" and feel trapped.

**How to detect:**
```bash
# Step 1: Find files with primary action buttons
grep -rn "\.borderedProminent\|\.controlSize(.large)" Sources/ --include="*.swift" \
  | cut -d: -f1 | sort -u > /tmp/primary_buttons.txt

# Step 2: Find files with ScrollView
grep -rn "ScrollView" Sources/ --include="*.swift" \
  | cut -d: -f1 | sort -u > /tmp/scrollviews.txt

# Step 3: Cross-reference — files with BOTH are candidates
comm -12 /tmp/primary_buttons.txt /tmp/scrollviews.txt

# Step 4: For each candidate, manually check:
# - Is the button INSIDE the ScrollView? (not pinned outside)
# - Is it the last child of a VStack inside ScrollView?
# - Are there 4+ tall elements above it?
# - Exclude: .toolbar buttons, buttons outside ScrollView, Form-based layouts
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Button pinned OUTSIDE ScrollView
VStack(spacing: 0) {
    ScrollView { content }
    Divider()
    actionButtons.padding()  // pinned below scroll
}

// ✅ Button in .toolbar
.toolbar {
    ToolbarItem(placement: .confirmationAction) {
        Button("Done") { ... }
    }
}

// ✅ Standard Form sections
Form {
    Section { ... }
    Section { Button("Save") { ... } }
}

// ✅ Bottom action bar outside ScrollView
VStack(spacing: 0) {
    ScrollView { photoGrid }
    bottomActionBar
}
```

**Severity:** 🟡 HIGH (user feels trapped, only sees Cancel)

---

### Automated Check 6: Dismiss Traps

**What it detects:** A view where the only visible action is Cancel/Dismiss/back with no forward path shown.

**How to detect:**
```bash
# Step 1: Find views with only cancellationAction in toolbar
grep -rn "cancellationAction" Sources/ --include="*.swift" \
  | cut -d: -f1 | sort -u > /tmp/cancel_views.txt

# Step 2: Find views with confirmationAction or primaryAction
grep -rn "confirmationAction\|primaryAction" Sources/ --include="*.swift" \
  | cut -d: -f1 | sort -u > /tmp/forward_views.txt

# Step 3: Files with cancel but no forward action in toolbar
comm -23 /tmp/cancel_views.txt /tmp/forward_views.txt

# Step 4: For each candidate, check if body has visible .borderedProminent button
# Exclude: HelpView, WhatsNewSheet, info/about views (dismiss is expected)
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Cancel + Done/Save in toolbar
.toolbar {
    ToolbarItem(placement: .cancellationAction) { Button("Cancel") { ... } }
    ToolbarItem(placement: .confirmationAction) { Button("Done") { ... } }
}

// ✅ Cancel in toolbar + primary action in body (visible without scroll)

// ✅ Read-only/info sheets (dismiss is the only expected action)
```

**Severity:** 🟡 HIGH (user feels stuck after completing a step)

---

### Automated Check 7: Gesture-Only Actions

**What it detects:** Feature or action accessible only via gesture (swipe, long-press, context menu) with no visible button or menu alternative.

**How to detect:**
```bash
# Step 1: Find swipeActions and contextMenu usage
grep -rn "\.swipeActions\|\.contextMenu" Sources/ --include="*.swift"

# Step 2: For each file with gesture actions, extract action labels
grep -A10 "\.swipeActions\|\.contextMenu" Sources/ --include="*.swift" \
  | grep 'Button("'

# Step 3: Check if those same action labels appear as visible buttons
# in the same view (outside gesture blocks)
```

**IMPORTANT — Check ALL list views, not just a sample.** A previous audit checked 1 of 7 list views and concluded "all clear," missing 6 findings.

**Safe patterns (do NOT flag):**
```swift
// ✅ Swipe action + toolbar/menu equivalent
.swipeActions { Button("Delete") { ... } }
.toolbar {
    ToolbarItem { Menu { Button("Delete") { ... } } }
}

// ✅ Standard list delete (.onDelete) — well-known iOS convention

// ✅ Context menu duplicating a visible button (convenience)
```

**Severity:** 🟢 MEDIUM (feature undiscoverable for some users; 🟡 HIGH on macOS where swipe is rare)

---

### Automated Check 8: Loading State Traps

**What it detects:** A view that shows a loading indicator with no way for the user to cancel, go back, or timeout.

**How to detect:**
```bash
# Step 1: Find ProgressView paired with interactiveDismissDisabled
grep -rn "interactiveDismissDisabled" Sources/ --include="*.swift"

# Step 2: Find full-screen loading overlays
grep -B5 -A5 "ProgressView" Sources/ --include="*.swift" \
  | grep -l "ignoresSafeArea\|ZStack"

# Step 3: For each, check if cancel button exists during loading state
# Check if async operation has timeout/cancellation
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Loading with cancel button
// ✅ Loading with timeout
// ✅ Inline progress indicator (doesn't block interaction)
// ✅ Brief loading (< 2 sec typical) for local operations
```

**Severity:** 🟢 MEDIUM (user trapped if operation hangs)

---

### Automated Check 9: Context Dropping

**What it detects:** Navigation path has item/context available at the source but drops it before reaching the destination. The right destination is opened but without the context the user expects.

**How to detect:**
```bash
# Step 1: Find platform-split presentations
grep -rn "#if os(iOS)" Sources/ --include="*.swift" \
  | xargs -I{} grep -l "\.sheet\|\.fullScreenCover" {} 2>/dev/null

# Step 2: Compare parameters in iOS sheet vs macOS notification
grep -B2 -A15 "NotificationCenter.default.post" Sources/ --include="*.swift" \
  | grep -E "userInfo|let context"

# Step 3: Find NavigationContext structs and their properties
grep -rn "NavigationContext\|NavigationInfo" Sources/ --include="*.swift"

# Step 4: Compare context struct properties with destination view init params

# Step 5: Find show* flags set from item-context closures where destination
# uses parameterless init
grep -B10 "show.*= true" Sources/ --include="*.swift" \
  | grep -E "item\.|onItemSelected"
```

**Safe patterns (do NOT flag):**
```swift
// ✅ All destination parameters passed on all platforms
// ✅ Parameterless init is intentional (fresh/empty state)
// ✅ Context struct matches notification sender 1:1
```

**Severity:** 🟡 HIGH (user loses context; may cause data loss)

---

### Automated Check 10: Notification Navigation Fragility

**What it detects:** Navigation between views using `NotificationCenter` with untyped `[String: Any]` dictionaries instead of typed function calls or bindings. Key typos, type mismatches, or omitted fields are silent at compile time.

**How to detect:**
```bash
# Step 1: Find NotificationCenter posts with userInfo (navigation-related)
grep -rn "NotificationCenter.default.post" Sources/ --include="*.swift" \
  | grep -v "object: nil)" \
  | grep -i "userInfo"

# Step 2: Find the notification names used for navigation
grep -rn "\.requestNavigate\|\.navigateTo\|\.showFeature\|\.openSection" Sources/ --include="*.swift"

# Step 3: Find corresponding receivers
grep -rn "\.onReceive\|publisher(for:" Sources/ --include="*.swift" \
  | grep -i "navigate\|show\|open"

# Step 4: For each sender/receiver pair, compare key counts and key names
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Typed callback/closure
// ✅ Environment-based navigation
// ✅ Binding-based state change
// ✅ Notification used for non-navigation purposes (sync events, refresh triggers)
```

**Severity:** 🟡 HIGH (silent bugs, no compiler safety)

---

### Automated Check 10b: Notification Type-Safety

**What it detects:** Same userInfo key sent with one type (e.g., `PersistentIdentifier`) but cast to a different type on receive (e.g., `as? String`). Compiles silently, fails at runtime with silent nil.

**How to detect:**
```bash
# Step 1: Extract all userInfo key-value pairs from senders
grep -B2 -A20 "NotificationCenter.default.post" Sources/ --include="*.swift" -rn \
  | grep -E '"[a-zA-Z]+":' > /tmp/sender_keys.txt

# Step 2: Extract all userInfo key casts from receivers
grep -B2 -A10 "userInfo\?" Sources/ --include="*.swift" -rn \
  | grep -E '"[a-zA-Z]+".*as\?' > /tmp/receiver_casts.txt

# Step 3: For each key in BOTH sender and receiver:
# Compare the type being sent vs the type being cast
# Mismatch example:
#   Sender:   "itemID": item.persistentModelID    (PersistentIdentifier)
#   Receiver: info["itemID"] as? String            (String)
#   → CRITICAL: silent nil, navigation silently broken

# Step 4: Flag mismatches:
# - Sender PersistentIdentifier, receiver String (or vice versa)
# - Sender uses `as Any` type erasure
# - Orphaned keys sent but never read
# - Missing keys expected by receiver but never sent
```

**Severity:** 🔴 CRITICAL (type mismatches cause silent navigation failures)

---

### Automated Check 11: Sheet Presentation Asymmetry

**What it detects:** Same feature uses fundamentally different presentation mechanisms on different platforms — e.g., iOS uses `.sheet` with direct view init, macOS uses NotificationCenter → navigation. Both work, but different mechanisms drift apart.

**How to detect:**
```bash
# Step 1: Find files with platform-conditional sheet presentations
grep -rn "#if os(iOS)" Sources/ --include="*.swift" \
  | cut -d: -f1 | sort -u > /tmp/platform_split.txt

# Step 2: For each, check if iOS uses .sheet and macOS uses a different mechanism
for f in $(cat /tmp/platform_split.txt); do
  ios_sheet=$(grep -c "\.sheet\|\.fullScreenCover" "$f" 2>/dev/null || echo 0)
  notification=$(grep -c "NotificationCenter.default.post" "$f" 2>/dev/null || echo 0)
  if [ "$ios_sheet" -gt 0 ] && [ "$notification" -gt 0 ]; then
    echo "ASYMMETRY: $f"
  fi
done

# Step 3: For asymmetric files, count parameters in each path
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Same mechanism, minor platform differences (styling, frame size)
// ✅ Platform-specific STYLING, not mechanism
```

**Severity:** 🟡 HIGH (maintenance burden, drift risk, enables context dropping)

---

### Automated Check 12: Stale Navigation Context

**What it detects:** A view stores navigation context in `@State` for later use, but the context is never cleared — can become stale if source item is deleted or user navigates away.

**How to detect:**
```bash
# Step 1: Find @State properties with Context/Info types
grep -rn "@State.*private.*var.*[Cc]ontext\|@State.*private.*var.*[Ii]nfo\|@State.*private.*var.*[Nn]avigation" \
  Sources/ --include="*.swift"

# Step 2: For each, check if it's ever set to nil
# Extract variable name, search for "varName = nil"

# Step 3: If no clearing mechanism exists → flag as stale context risk

# Step 4: Check if context references PersistentIdentifier without validation
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Context cleared after use (.onDisappear, .onChange)
// ✅ Context is a computed property (always fresh)
// ✅ Context validated before use (modelContext.model(for:) != nil check)
```

**Severity:** 🟢 MEDIUM (edge case but can cause crashes or stale data display)

---

### Automated Check 13: Simulated Delay

**What it detects:** `Task.sleep` or `asyncAfter` followed by hardcoded data assignment — simulating a network fetch or AI computation with fake data.

**How to detect:**
```bash
# Step 1: Find Task.sleep or asyncAfter in feature views (not tests/previews)
grep -rn "Task\.sleep\|asyncAfter" Sources/ --include="*.swift" \
  | grep -v "Test\|Preview\|#Preview" \
  | grep -v "// animation\|// dismiss\|// sheet" > /tmp/delay_sites.txt

# Step 2: For each delay site, check if the next 10 lines set a hardcoded value
while IFS=: read -r file line _; do
  sed -n "$((line+1)),$((line+10))p" "$file" \
    | grep -q "= \[.*\]\|= .*(\|= \".*\"\|= true\|= false\|\.result =\|\.suggestion" \
    && echo "SIMULATED: $file:$line"
done < /tmp/delay_sites.txt

# Step 3: Exclude legitimate uses:
# - Task.sleep for animation timing (< 0.5s, near dismiss/animation code)
# - asyncAfter for sheet presentation sequencing
# - Delays before real async/API calls
# Flag: delay + hardcoded data WITHOUT any network/API call between them
```

**Severity:** 🟢 MEDIUM to 🔴 CRITICAL (depends on whether users see fake data as real)

---

### Automated Check 14: Navigation Container Constraints

**What it detects:** `selectedSection = .X` assignments where `.X` is not a valid tag in the current navigation container. On iPhone (TabView), only tab tags are valid. On iPad/macOS (sidebar), sidebar items are valid. Setting a non-existent tag is a silent no-op — the user taps and nothing happens.

**How to detect:**
```bash
# Step 1: Find all selectedSection assignments
grep -rn "selectedSection = \." Sources/ --include="*.swift"

# Step 2: Find valid TabView tags (iPhone)
grep -rn "\.tag(\." Sources/ --include="*.swift" | grep -i "tab"

# Step 3: Find valid sidebar items
grep -rn "\.tag(\." Sources/ --include="*.swift" | grep -i "sidebar\|NavigationSplitView"

# Step 4: For each assignment in Step 1, check if the value is valid for both platforms
# If assigned value is not a valid tag on either platform → flag
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Assigned value matches a .tag() in both TabView and sidebar
// ✅ Assignment is inside a platform check (#if os(iOS)) using platform-specific tags
```

**Severity:** 🟡 HIGH (user taps, nothing happens — silent dead end)

---

### Automated Check 15: Notification Lifecycle

**What it detects:** Notification names that are posted but never received (dead posts), or declared but never posted or received (dead declarations). Also catches receivers without corresponding posters.

**How to detect:**
```bash
# Step 1: Find all notification name declarations
grep -rn "static let\|static var" Sources/ --include="*.swift" \
  | grep "Notification.Name\|NSNotification.Name"

# Step 2: For each notification name, count posts and receivers
# Posts: grep for ".post(name: .notificationName"
# Receivers: grep for ".onReceive" or "publisher(for: .notificationName"

# Step 3: Flag:
# - Declared + posted but never received → dead post
# - Declared but never posted or received → dead declaration
# - Received but never posted → will never fire
```

**Safe patterns (do NOT flag):**
```swift
// ✅ System notifications received but not posted (e.g., .willResignActive)
// ✅ Notifications used in extension targets (may be posted/received in a different target)
```

**Severity:** ⚪ LOW for dead declarations, 🟢 MEDIUM for dead posts (code that runs but has no effect), 🟡 HIGH for receivers without posters (code waiting for something that never happens)

---

### Automated Check 16: Success Feedback

**What it detects:** Non-destructive actions (save, duplicate, archive, bookmark, export) that complete without any user-visible confirmation — no toast, haptic, banner, or navigation change.

**How to detect:**
```bash
# Step 1: Find action completion points
grep -rn "modelContext\.save\|dismiss()\|\.delete\|duplicate\|archive\|export\|\.insert" \
  Sources/ --include="*.swift"

# Step 2: For each, check surrounding 10 lines for feedback:
# - ToastManager, toast, showToast
# - UINotificationFeedbackGenerator, haptic
# - banner, alert, confirmationDialog
# - Navigation change (dismiss + new sheet)

# Step 3: Flag actions with no feedback within 10 lines of the completion point
# Exclude: destructive actions (delete) — those should have pre-confirmation, not post-feedback
```

**Safe patterns (do NOT flag):**
```swift
// ✅ Toast shown after save
// ✅ Haptic played on completion
// ✅ View dismisses with completion callback that shows feedback
// ✅ Destructive actions with pre-confirmation dialog (feedback is the confirmation)
```

**Severity:** 🟢 MEDIUM (user unsure if action succeeded)

---

### Automated Check 17: Empty State Coverage

**What it detects:** List or collection views that show nothing when empty — no `ContentUnavailableView`, no placeholder text, no onboarding prompt. Users see a blank screen and think the app is broken.

**How to detect:**
```bash
# Step 1: Find list/collection views
grep -rn "List {\|ForEach\|LazyVGrid\|LazyHGrid\|LazyVStack" Sources/ --include="*.swift" \
  | cut -d: -f1 | sort -u

# Step 2: For each, check if there's an empty state handler:
# - ContentUnavailableView
# - .overlay { if items.isEmpty { ... } }
# - if items.isEmpty { emptyView } else { List { ... } }

# Step 3: Flag lists with no empty state handling
# Exclude: lists that are always populated (e.g., settings sections, static menus)
```

**Severity:** 🟡 HIGH (users think app is broken when they first open it)

---

### Automated Check 18: Error Recovery

**What it detects:** Error states displayed to the user with no retry button, no "Open Settings" link, or no other recovery path. The user sees an error and has no way forward.

**How to detect:**
```bash
# Step 1: Find error display patterns
grep -rn "\.alert\|errorMessage\|showError\|isError" Sources/ --include="*.swift"

# Step 2: For each error display, check if there's a retry or recovery action:
# - Button("Retry"), Button("Try Again")
# - Link to Settings (openURL with app-settings:)
# - Alternative action offered

# Step 3: Flag errors with no recovery path
# Exclude: fatal errors that genuinely can't be retried, informational alerts with "OK"
```

**Severity:** 🟡 HIGH (user stuck at error with no path forward)

---

### Verification Template (MANDATORY for Layer 3)

Before grading issues, produce this table for each flagged entry point from Layer 1:

```
| # | Entry Point | Flag | Verified? | Receipt | Status |
|---|-------------|------|-----------|---------|--------|
| 1 | [label] | [flag] | ? | (file:line checked) | confirmed / retracted / needs-runtime |
```

Rules:
- Every flagged entry point from Layer 1 must appear in this table
- `?` in the Verified column means the finding hasn't been checked in Layer 3 yet
- Layer 3 cannot produce a grade while any flagged entry has `?` in Verified
- Retracted findings stay in the table with strikethrough — they prove you checked, not just confirmed

---

### If "layer4" or "evaluate": `enumerate-required`

**Before starting, print:**
```
Layer 4: Semantic Evaluation — [N] issues to evaluate
  Estimated time: ~[1-2 min for <10 issues / 3-5 min for 20+]
```

1. For each issue, assess user impact using these **4 criteria** (score each 1-5):

| Criterion | 1 (no impact) | 3 (moderate) | 5 (severe) |
|-----------|--------------|--------------|------------|
| **Discoverability** | Feature is obvious, multiple entry points | Requires learning but findable | Hidden, gesture-only, or buried 4+ taps deep |
| **Efficiency** | One tap from context | 2-3 taps, minor detour | 4+ taps, navigation required, context lost |
| **Feedback** | Clear confirmation + undo | Confirmation but no undo | No feedback, user unsure if action completed |
| **Recovery** | Easy undo, no data loss | Partial undo, minor data loss possible | No undo, data loss, or must recreate from scratch |

2. For each finding, assign a **confidence level**:
   - `verified` — confirmed by grep, file read, or code trace. The issue definitely exists.
   - `probable` — code suggests the issue but not fully traced through all code paths.
   - `needs-runtime` — static analysis can't determine; requires running the app to confirm.

3. Map violations to design principles (#1-#8)
4. **After each evaluation, print:** `Layer 4: ✓ Issue [N]/[total] — [confidence] — [D/E/F/R scores]`
5. Output to `layer4-semantic-evaluation.md`

### If "layer5" or "data-wiring" or "wiring": `enumerate-required`

**Before starting, print:**
```
Layer 5: Data Wiring — inventorying models and cross-referencing features
  Estimated time: ~[2-4 min for <20 features / 5-10 min for 40+]
```

1. **Model inventory.** Catalog what data the app tracks:
```bash
# Find all @Model classes and their properties
grep -rn "@Model" Sources/Models/ --include="*.swift" -l

# Find relationships
grep -rn "var.*:.*\[.*\]?" Sources/Models/ --include="*.swift" | grep -v "//"

# Find computed properties that aggregate data
grep -rn "var.*:.*{" Sources/Models/ --include="*.swift" | grep -i "total\|average\|count\|cost\|price"
```
**Print:** `Layer 5: ✓ Model inventory (1/7) — [N] models, [N] properties`

2. **Select features to cross-reference.** Don't check every feature — select the **top 5-8** using these criteria:
   - Features that **make decisions** based on model data (advisors, calculators, suggestion engines)
   - Features with the **most model properties available** but unclear how many they use
   - Features flagged in earlier layers
   - The **primary detail view** (reads the most model data)

   For each, check what model data it reads vs what's available. **Print:** `Layer 5: ✓ Feature scan (2/7) — [N] features checked`

3. **Mock data detection:**
```bash
# Fake fetch pattern
grep -rn "asyncAfter" Sources/Features/ --include="*.swift" -A 10 | grep -B 5 "=.*[0-9]\|\".*\$"

# Static arrays pretending to be fetched data
grep -rn "let.*=.*\[" Sources/Features/ --include="*.swift" | grep -i "alternative\|suggestion\|recommendation"

# Hardcoded scores/ratings in non-test code
grep -rn "Score.*=.*[0-9]\|rating.*=.*[0-9]" Sources/Features/ --include="*.swift" | grep -v "test\|Test\|preview\|Preview"

# Functions that simulate work
grep -rn "func fetch\|func load\|func compute" Sources/Features/ --include="*.swift" -A 15 | grep "asyncAfter\|sleep\|\.random"
```
**Print:** `Layer 5: ✓ Mock data scan (3/7)`

4. **Cross-reference matrix:**

| Feature | Data Available | Data Used | Data Ignored |
|---------|---------------|-----------|--------------|
| [name] | [model properties] | [what it reads] | [gap] |

**Print:** `Layer 5: ✓ Cross-reference matrix (4/7) — [N] features cross-referenced, [N] gaps found`

5. **Form-to-detail parity check (MANDATORY):**

   For every model that has BOTH a form/edit view AND a detail/read-only view, verify that every user-editable field in the form has a corresponding display in the detail view.

   **Method:**
   a. Identify form/detail view pairs (e.g., `ExtendedWarrantyFormView` + `EnhancedItemDetailView+Sections` extended warranty section; `RMAFormView` + `RMAListView`).
   b. In each form, enumerate fields bound to TextFields, Pickers, Toggles, DatePickers, Steppers.
   c. For each editable field, grep the detail view for a display consumer. Classify:
      - `displayed`: Field appears in a DetailKeyValueRow, Text(), or equivalent read-only rendering.
      - `form-only`: Field is only read by the form to populate edit state. User enters data that vanishes after save.
      - `computed`: Field feeds a computed property that IS displayed (indirect display -- acceptable).
      - `serialization-only`: Field is backed up/exported but never shown to the user in any view.

   d. Report `form-only` fields as findings with `pattern_fingerprint: form_editable_but_no_detail_display`.

   **Why this matters:** Users who enter data and can't see it after saving perceive it as data loss, even when the data is correctly persisted. This is the most common "vanishing field" UX bug pattern and is invisible to data-integrity audits (the data round-trips perfectly).

   **Handoff input:** If data-model-radar ran first, check `.agents/ui-audit/data-model-radar-handoff.yaml` for `form_only_fields[]`. These are pre-identified suspects -- verify each against the actual detail view rather than re-scanning from scratch.

   **Print:** `Layer 5: ✓ Form-to-detail parity (5/7) — [N] form-only fields found`

6. **Integration gap detection:**
```bash
# Find Manager/Service classes
grep -rn "class.*Manager\|class.*Service" Sources/ --include="*.swift" | grep -v "test\|Test"

# Check if feature views reference them
```

**Print:** `Layer 5: ✓ Integration gap detection (6/7) — [N] manager/service references checked`

7. **Platform parity check:**
```bash
# Find iOS-only dismiss buttons
grep -rn "#if os(iOS)" Sources/ --include="*.swift" -A 3 | grep -i "dismiss\|toolbar\|done"

# Find extension files with platform-specific computed properties
grep -rl "extension.*View" Sources/ --include="*.swift" | grep "+"
```
**Print:** `Layer 5: ✓ Platform parity (7/7)`

8. Output to `layer5-data-wiring.yaml`

### If "diff":

**Compare findings against the previous ui-path-radar audit** — surface what regressed, what got fixed, and what's new since the last run.

#### Usage

```
/ui-path-radar diff
/ui-path-radar diff --since 2026-04-01
/ui-path-radar diff --layer 3        # restrict to one layer's findings
```

#### Source of Truth

The diff reads from `.radar-suite/ledger.yaml` — the only authoritative cross-session store of ui-path-radar findings. Per-layer YAML files (`.ui-path-radar/layer3-results.yaml`, `.ui-path-radar/layer5-data-wiring.yaml`) and per-run handoff files are overwritten each run, so they cannot serve as a diff baseline.

The "previous audit" is defined as **the most recent ledger session entry with `skill: ui-path-radar`** that is strictly older than the current session. If no prior session exists, the diff command MUST refuse with:

> "No prior ui-path-radar audit found in `.radar-suite/ledger.yaml`. Run a full audit (`/ui-path-radar`) first to establish a baseline."

Do not invent a baseline. Do not fall back to memory or stale `.ui-path-radar/*-audit.md` reports.

#### How It Works

1. **Identify the baseline session** — read `.radar-suite/ledger.yaml`, find the most recent prior session entry with `skill: ui-path-radar`. With `--since YYYY-MM-DD`, use the latest entry on or after that date instead.
2. **Identify the current session** — either the in-progress session (if the user just ran an audit) or the most recent completed session.
3. **Run a quick re-verification scan** on the current codebase for each previously-reported issue's file:line — has the problem been fixed in place?
4. **Bucket every finding** from the union of baseline + current into one of four categories by RS-NNN ID:
   - **Fixed** — present in baseline with `status: open`, present in current with `status: fixed`, OR the file:line no longer matches the pattern fingerprint
   - **Regressed** — present in baseline with `status: fixed`, but `file_hash` changed AND the pattern fingerprint matches at the same file:line again
   - **New** — RS-NNN ID is in current but not baseline
   - **Persistent** — present in both with the same status
5. **Apply optional filters:** `--layer [1-5]` restricts to findings whose `layer` field matches.

#### Output Format

```
Audit Diff: <previous date> → <current date> (<days> days)

✅ Fixed (<count>)
| RS-NNN | short_title | Category | Fixed in |

🔴 Regressed (<count>)
| RS-NNN | short_title | Category | Was fixed | file_hash changed? |

🆕 New (<count>)
| RS-NNN | short_title | Category | Urgency |

📌 Persistent (<count>)
[collapsed by default; pass --verbose to expand]

📁 Changed files since baseline: <count> (may need re-verification)
```

#### Refusal cases

- No prior ledger session: refuse with the message above
- `--since` date is in the future: refuse with "Date is in the future; no audits to compare"
- `--layer [N]` outside 1-5: refuse with "Layer N is not a valid ui-path-radar layer (must be 1-5)"
- `--layer [N]` matches no findings in either baseline or current: print "No findings in Layer N across either session" (not a refusal — a legitimate empty result)

### If "fix" or "fixes":
1. Read `layer3-results.yaml` and `layer5-data-wiring.yaml` for unfixed issues
2. Generate specific code fixes
3. Prioritize by severity (critical first)
4. Group into:
   - **Safe fixes** — isolated, low blast radius
   - **Cross-cutting fixes** — touch shared code
   - **Requires design decision** — multiple valid approaches
   - **Deferred** — no action needed now
   - **Out of scope** — belongs to a different audit type

### If "status":
1. Read existing audit files
2. Report: issues found, fixed, remaining
3. Show priority queue for unfixed issues

---

## Output Format

> **CRITICAL FORMATTING RULE:** The Issue Rating Table below IS the output. Do NOT create separate sections for "Critical Issues", "Data Wiring Issues", "Recommendations", or any other vertical breakdown of findings. Every finding — navigation issues, data wiring issues, orphaned code, missing feedback, design violations — goes into ONE table as ONE row. Context goes in the Finding column. No exceptions.

### Layer Transition Summary (between each layer)

When completing a layer and moving to the next, print:
```
✓ Layer [N] of 5 complete: [plain description] — [M] findings ([X] verified, [Y] probable, [Z] needs-runtime)
  Retracted from prior layers: [count or "none"]
  Cumulative: [total] findings ([C] critical, [H] high, [M] medium, [L] low)
  Next: Layer [N+1] — [plain description of what it does and why it matters given current findings].
  → "proceed" | "explain #[N]" | "stop here"
```

### Final Output (after all layers or after a single layer run)

After completing the audit, provide these **6 items in order**:

1. **One-line summary** — entry point count, issue count by severity (one sentence, not a section)
2. **Issue Rating Table** — every finding in a single table. Each finding MUST include a confidence tag (`verified` / `probable` / `needs-runtime`) in the Finding column.
3. **Proactive risk callout** — Auto-identify the top 3 riskiest findings:
```
Before proceeding, these findings have elevated risk profiles:
  #[N] — [short description] (Risk:Fix [indicator], Blast [count] files)
  #[N] — [short description] (Risk:No Fix [indicator], [consequence])
  → Say "explain #[N]" for a detailed risk breakdown before deciding.
```
4. **Cross-skill handoff notes** (if applicable):
```
Related areas to check next:
  #[N] → Check whether saved data survives editing round-trips (data safety audit)
  #[N] → Check visual layout and spacing for this screen (visual quality audit)
```
5. **Limitations disclaimer:**
```
Limitations: Static analysis only. Not checked: animation smoothness,
   real-device timing, race conditions under memory pressure, subjective
   UX feel, accessibility with VoiceOver. Consider runtime testing for
   findings marked "needs-runtime."
```
6. **One-line next step** — suggest next action

Items 3-5 may be omitted if not applicable.

### Issue Rating Table

**Hard formatting rule — Table, not list:** ALL findings MUST be in a single markdown table. Each finding is ONE ROW. Never expand into individual sections or bullet-pointed ratings. ALL categories go in the same table.

**Full table:**
```markdown
| #   | Finding                   | Conf     | Urgency      | Risk:Fix | Risk:NoFix | ROI      | Blast    | Effort  | Status |
|-----|---------------------------|----------|--------------|----------|------------|----------|----------|---------|--------|
| 1   | Dead end: ".warranty"     | verified | 🔴 Critical | ⚪ Low  | 🔴 Crit   | 🟠 Exc  | 🟢 2f   | Trivial | Open   |
|     | unhandled                 |          |              |          |            |          |          |         |
```

**Compact table (narrow terminal):**
```markdown
| #   | Finding                   | Conf     | Urgency      | Effort  |
|-----|---------------------------|----------|--------------|---------|
| 1   | Dead end: ".warranty"     | verified | 🔴 Critical | Trivial |
```

### Indicator Scale

| Indicator | General meaning | ROI meaning |
|-----------|----------------|-------------|
| 🔴 | Critical / high concern | Poor return — reconsider |
| 🟡 | High / notable | Marginal return |
| 🟢 | Medium / moderate | Good return |
| ⚪ | Low / negligible | — |
| 🟠 | Pass / positive | Excellent return |

- **Urgency:** 🔴 CRITICAL (dead end, wrong destination, mock data) · 🟡 HIGH (broken promise, missing activation, unwired data) · 🟢 MEDIUM (two-step flow, missing feedback) · ⚪ LOW (inconsistency, orphaned code)
- **Risk: Fix:** Risk of the fix introducing regressions
- **Risk: No Fix:** User-facing consequence of leaving the issue
- **ROI:** 🟠 Excellent · 🟢 Good · 🟡 Marginal · 🔴 Poor
- **Blast Radius:** Number of files the fix touches. Do not use `<br>` tags. Count by grepping for callers/references before rating.
- **Fix Effort:** Trivial / Small / Medium / Large

### Finding Dependencies and Fingerprints

When creating findings, populate these optional fields where relationships are obvious:

- **`depends_on`/`enables`:** UI path findings often chain -- a dead-end fix enables a flow that was previously untestable. If one fix must come before another, populate with finding IDs.
- **`pattern_fingerprint`/`grep_pattern`/`exclusion_pattern`:** Assign fingerprints for generalizable UI anti-patterns (e.g., `dead_end_sheet`, `unhandled_navigation_case`, `mock_data_in_production`, `missing_platform_parity`).

---

## Fix Application Workflow

After presenting findings, apply fixes in **waves**. After each wave (including commits), **always** print the progress banner and auto-prompt for the next wave. Never leave the user with a blank prompt.

### Waves

| Wave | Section | Est. Time | Description |
|------|---------|-----------|-------------|
| 1 | Safe fixes + tests | ~10-15 min | Isolated, low blast radius. Auto-apply. Write tests. |
| 2 | Cross-cutting fixes + tests | ~15-25 min | Touch shared code. Present for review. Write tests. |
| 3 | Design decisions | ~5-15 min | Multiple options. Requires user input per item. |
| 4 | Build + Test + Commit | ~5 min | Build both platforms, run tests, stage, commit. |

**Every fix must have a test.** Do not move to the next wave until tests for the current wave's fixes are written and compiling.

Skip empty waves.

### Progress Banner (MANDATORY after every wave)

**CRITICAL — BLOCKING requirement in Normal and Pre-Approved modes.** After EVERY wave and EVERY commit, your NEXT output MUST be the progress banner followed by the next-wave `AskUserQuestion`.

**Hands-Free mode exception:** In Hands-Free mode, the progress banner still prints, but the next-wave `AskUserQuestion` call is suppressed (per the Hands-Free Mode precedence rules above). Replace the AskUserQuestion with the Hands-Free completion message instead.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Wave [N] of [total] complete: [wave name]
   [X] findings fixed, [Y] remaining, [Z] deferred

⏱  Next: Wave [N+1] — [wave name] (~[time estimate])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately ask: "Ready for Wave [N+1]?" with options:
- **Proceed (Recommended)** — Start the next wave
- **Commit first** — Commit current changes before continuing
- **Stop here** — End for now, resume later

---

### Pipeline Mode Behavior (Tier 2/3)

When running inside a Tier 2 or Tier 3 pipeline (detected via `tier` field in `.radar-suite/session-prefs.yaml`):

1. **On skill start:** Emit the pipeline-level progress banner (see `radar-suite-core.md` Pipeline UX Enhancements #1). If this is the first skill in the pipeline OR `experience_level` is Beginner/Intermediate, also emit the audit-only statement.
2. **On skill completion:** Emit a per-skill mini rating table marked "PRELIMINARY" (see Pipeline UX Enhancements #2). Then emit the pipeline-level progress banner showing this skill as complete.
3. **Within-skill wave banners** (above) are still emitted normally in addition to the pipeline-level banners.

### short_title Requirement (v2.1)

Every finding MUST include a `short_title` field (max 8 words). This is the human-scannable label used in pipeline banners, pre-capstone summaries, and ledger output.

Example: `short_title: "Delete button missing on edit sheet"`

All finding ID references in output (tables, banners, summaries) use the format: `RS-NNN (short_title)`.

---

## Regression Canaries

After fixing a workflow issue, generate a "canary" — a specific check that detects if the issue recurs. Canaries are stored in `.ui-path-radar/canaries.yaml` and can be run as a quick regression check before release.

### Canary Format

```yaml
canaries:
  - id: "canary-001"
    issue_ref: "issue-017"
    description: "NavigationContext must include existingItemID"
    check_type: "grep_match"
    file: "Sources/Views/Navigation/AppNavigationView.swift"
    pattern: "existingItemID.*PersistentIdentifier"
    expect: "match"  # fail if pattern NOT found
    added: "2026-03-08"

  - id: "canary-002"
    issue_ref: "issue-013"
    description: "Continue button must appear before tall content in flow"
    check_type: "line_order"
    file: "Sources/Features/ItemManagement/Views/UnifiedPhotoFlow.swift"
    first_pattern: "Continue with AI Analysis"
    second_pattern: "sourcePickerContent"
    expect: "first_before_second"
    added: "2026-03-08"
```

### Canary Check Types

| Type | Description | Pass condition |
|------|-------------|----------------|
| `grep_match` | Pattern must exist in file | Pattern found |
| `grep_absent` | Pattern must NOT exist in file | Pattern not found |
| `line_order` | Two patterns must appear in specific order | First before second |
| `param_count` | Count params in a function/dict | Count matches expected |
| `platform_parity` | Same pattern must exist in both iOS and macOS blocks | Found in both |

### Running Canaries

```bash
for canary in $(yq '.canaries[].id' .ui-path-radar/canaries.yaml); do
  file=$(yq ".canaries[] | select(.id == \"$canary\") | .file" .ui-path-radar/canaries.yaml)
  pattern=$(yq ".canaries[] | select(.id == \"$canary\") | .pattern" .ui-path-radar/canaries.yaml)
  expect=$(yq ".canaries[] | select(.id == \"$canary\") | .expect" .ui-path-radar/canaries.yaml)

  if [ "$expect" = "match" ]; then
    grep -q "$pattern" "$file" && echo "✅ $canary" || echo "❌ $canary REGRESSION"
  elif [ "$expect" = "absent" ]; then
    grep -q "$pattern" "$file" && echo "❌ $canary REGRESSION" || echo "✅ $canary"
  fi
done
```

### When to Generate Canaries

After each fix in fix mode, generate a canary:
1. After fixing Context Dropping → canary verifying the field exists in both paths
2. After fixing Buried Primary Action → canary verifying button order
3. After fixing Platform Parity Gap → canary verifying pattern on both platforms
4. After fixing Dismiss Trap → canary verifying forward action exists

Canaries are **additive** — they accumulate over time as a regression safety net.

---

## Handoff Brief Generation

After completing all layers (full audit) or `fix` mode, generate `.ui-path-radar/handoff.yaml`.

### When to Generate
- After a full 5-layer audit completes
- After `fix` mode completes (refreshes with current state)
- NOT after individual layer runs

### Format

```yaml
# Handoff Brief — generated by ui-path-radar
project: <project name from directory>
audit_date: <ISO 8601 date>
source_files_scanned: <count>

summary:
  total_issues: <count>
  critical: <count>
  high: <count>
  medium: <count>
  low: <count>

file_timestamps:
  <file path>: "<ISO 8601 mod date>"

issues:
  - id: <sequential number>
    finding: "<description>"
    category: <dead_end|wrong_destination|mock_data|incomplete_navigation|missing_activation|unwired_data|platform_gap|promise_scope_mismatch|buried_primary_action|dismiss_trap|two_step_flow|missing_feedback|gesture_only_action|loading_state_trap|context_dropping|notification_nav_fragility|sheet_presentation_asymmetry|stale_navigation_context|navigation_container_mismatch|empty_state_missing|error_recovery_missing|inconsistent_pattern|orphaned_code|command_palette_only|deeply_buried_feature|double_nested_navigation>
    urgency: <critical|high|medium|low>
    risk_fix: <critical|high|medium|low>
    risk_no_fix: <critical|high|medium|low>
    roi: <excellent|good|marginal|poor>
    blast_radius: "<description, e.g. '1 file' or '4 files'>"
    fix_effort: <trivial|small|medium|large>
    files:
      - <file path>
    suggested_fix: "<what to do, not how>"
    group_hint: "<optional grouping suggestion>"
```

### File Timestamps

```bash
stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%SZ" "<file path>"
```

### Group Hints

Common hints: `missing_confirmations`, `missing_feedback`, `orphaned_features`, `dead_code`, `platform_parity`, `dead_notifications`, `navigation_container`

---

## Cross-Skill Handoff

UI Path Radar complements **data-model-radar** (model layer), **roundtrip-radar** (data safety), **ui-enhancer-radar** (visual quality), and **capstone-radar** (ship readiness).

### On Completion — Write Handoff

After completing an audit, write `.agents/ui-audit/ui-path-radar-handoff.yaml`:

```yaml
source: ui-path-radar
date: <ISO 8601>
project: <project name>

file_timestamps:
  <file path>: "<ISO 8601 mod date>"

for_roundtrip_radar:
  suspects:
    - workflow: "<affected workflow>"
      finding: "<what was found>"
      file: "<file:line>"
      question: "<specific question for roundtrip-radar to verify>"
      group_hint: "<optional>"

for_ui_enhancer_radar:
  suspects:
    - view: "<view file>"
      finding: "<what was found>"
      action: "remove or wire up before visual audit"
      group_hint: "<optional>"

for_capstone_radar:
  blockers:
    - finding: "<description>"
      urgency: "<CRITICAL|HIGH>"
      group_hint: "<optional>"

checks_performed:
  # automated_checks: 19 = Checks 1-10, 10b, 11-18 (Check 10b kept as suffix to preserve external references — see § Layer 3 Numbering Note)
  automated_checks: 19
  # categories_scanned MUST match the Issue Categories table at SKILL.md:57-92 (34 categories) — keep in sync when adding categories
  categories_scanned:
    - dead_end
    - wrong_destination
    - mock_data
    - destructive_no_confirm
    - silent_state_reset
    - incomplete_navigation
    - missing_activation
    - unwired_data
    - platform_gap
    - promise_scope_mismatch
    - buried_primary_action
    - dismiss_trap
    - context_dropping
    - notif_nav_fragility
    - sheet_asymmetry
    - empty_state_missing
    - error_recovery_missing
    - keyboard_obscures_input
    - permission_denied_dead_end
    - modal_stacking
    - nav_container_mismatch
    - two_step_flow
    - missing_feedback
    - gesture_only_action
    - loading_state_trap
    - stale_nav_context
    - phantom_touch_target
    - race_condition_ux
    - invisible_selection
    - inconsistent_pattern
    - orphaned_code
    - command_palette_only
    - deeply_buried_feature
    - double_nested_nav
  persona_evaluation: false
  confidence_scoring: true
```

### End-of-Run Directory Cleanup (MANDATORY)

Per the Artifact Lifecycle rules in `radar-suite-core.md`, before returning from this skill:
1. List files in `.radar-suite/` (and `.ui-path-radar/` if used).
2. Move any stale single-use handoffs (`RESUME_PHASE_*.md`, `RESUME_*.md` except `NEXT_STEPS.md`, `*-v[0-9]*.md`) to `.radar-suite/archive/superseded/`.
3. Confirm Class 1 persistent-state files (`ledger.yaml`, `session-prefs.yaml`) are in-place rewrites — not dated or versioned.
4. Confirm Class 2 handoff files are overwrites, not appends.

This prevents `.radar-suite/` from accumulating stale prose artifacts across runs.

### Write to Unified Ledger (MANDATORY)

After writing the handoff YAML, also write findings to `.radar-suite/ledger.yaml` following the Ledger Write Rules in `radar-suite-core.md`:

1. Read existing ledger (or initialize if missing)
2. Record this session (timestamp, skill name, build)
3. For each finding: check for duplicates, assign RS-NNN ID if new, set `impact_category`, compute `file_hash`
4. Write updated ledger

**Impact category mapping for ui-path-radar findings:**
- Dead-end screen (no way forward or back) → `ux-broken`
- Broken navigation (button does nothing, link goes nowhere) → `ux-broken`
- Missing empty state or loading state → `ux-degraded`
- Buried CTA or hard-to-find feature → `ux-degraded`
- Accessibility dead end → `ux-broken`
- Visual-only issues → `polish`

### On Startup — Read Ledger & Handoffs (MANDATORY)

Before starting the audit, read the unified ledger and ALL companion handoff YAMLs:

```
Read .radar-suite/ledger.yaml (if exists) — check for existing findings to avoid duplicates
Read .agents/ui-audit/data-model-radar-handoff.yaml (if exists)
Read .agents/ui-audit/roundtrip-radar-handoff.yaml (if exists)
Read .agents/ui-audit/ui-enhancer-radar-handoff.yaml (if exists)
Read .agents/ui-audit/capstone-radar-handoff.yaml (if exists)
Read .workflow-audit/persona-handoff.yaml (if exists)
Read .workflow-audit/handoff.yaml (if exists)
```

### Workflow-Audit Persona Integration

When `.workflow-audit/persona-handoff.yaml` exists:

1. Display: "Persona evaluation from workflow-audit available -- incorporating."
2. **Layer 4 enrichment:** Use persona D/E/F/R ratings to weight your own Layer 4 scoring. If workflow-audit rated a workflow's Feedback as 2/5, weight Feedback-related issues higher for that workflow.
3. **Skip persona derivation:** Use workflow-audit's personas instead of re-deriving them. They were built from semantic analysis you don't replicate.
4. **Category overlap:** Read `checks_performed.categories_scanned`. For categories both skills check, still run your own automated checks but note "Also flagged by workflow-audit" for duplicate findings in the same file.

When `.workflow-audit/handoff.yaml` exists (without persona handoff):
- Import CRITICAL/HIGH findings as companion findings tagged `[via workflow-audit]`
- Note which categories workflow-audit checked

When neither exists: proceed normally. No change to audit behavior.

**Ledger check:** If the ledger contains findings for views you're about to audit, note their RS-NNN IDs. When you find the same issue, update the existing finding instead of creating a new one.

**Regression check:** For any `fixed` findings in the ledger whose `file_hash` no longer matches the current file, flag for re-verification per the Regression Detection protocol in `radar-suite-core.md`.

Parse `for_ui_path_radar` sections. Incorporate as **priority targets** — verify each independently.

If not found, proceed normally.

---

## Cautionary Note

**This skill is a tool, not an oracle.**

It systematically scans using pattern matching and heuristics. It surfaces real issues you'd miss manually — but it has inherent limitations:

**Good at:** Structural inconsistencies, patterns that compile but fail silently, cross-platform parity, repeatable checklists.

**Can miss:** Business logic correctness, UX nuance, false positives (intentionally retained code), novel bug patterns.

**Use responsibly:** Treat findings as leads to investigate, not verdicts. Verify critical findings manually. Don't assume clean = zero issues — it means zero *known-pattern* issues.

---

## End Reminder

After every layer/wave/commit: print progress banner → `AskUserQuestion` → never blank prompt.
