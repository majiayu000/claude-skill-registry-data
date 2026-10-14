---
name: rem-qa
description: Visual QA testing across real browser — Playwright (primary) or Chrome DevTools MCP (fallback). QA this, QA the site, test the site, check for visual bugs, run QA, browser test, visual test, smoke test, screenshot test, cross-page testing, mobile testing, desktop testing, diff-aware QA, Playwright testing, Lighthouse audit, health score, visual regression, find broken layouts, find dead clicks, find console errors. Crawls multiple pages, tests interactions at mobile + desktop viewports, captures screenshots to `tmp-screenshots/`, monitors console errors + network failures, detects layout shift (CLS) + touch-target violations + horizontal overflow, runs Lighthouse, produces 8-dimension health score (Visual / Interactivity / Mobile UX / Performance / Error-Free / Accessibility / Consistency / Content). Diff-aware mode (`/rem-qa diff`) tests only pages affected by recent git changes. Convention-aware — reads CLAUDE.md so it doesn't flag intentional z-index / overlay / mobile-nav patterns. Distinct from rem-review-ux (deep heuristic evaluation of a single page with Nielsen + WCAG + dark patterns; rem-qa is broader cross-page functional sweep with real clicks), rem-seo (markup + discoverability audit; rem-qa is visual + interactive), rem-verify (build + test + typecheck; rem-qa is browser-based user perspective), rem-audit (repo-wide code health; rem-qa is live-browser bugs). Pairs with rem-review-ux for deep UX follow-up on pages rem-qa flags, rem-test to generate regression tests from bugs found, rem-seo to handoff metadata issues.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Task, Agent, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__list_console_messages, mcp__chrome-devtools__list_network_requests, mcp__chrome-devtools__get_network_request, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__click, mcp__chrome-devtools__hover, mcp__chrome-devtools__fill, mcp__chrome-devtools__fill_form, mcp__chrome-devtools__press_key, mcp__chrome-devtools__emulate, mcp__chrome-devtools__resize_page, mcp__chrome-devtools__lighthouse_audit, mcp__chrome-devtools__performance_start_trace, mcp__chrome-devtools__performance_stop_trace, mcp__chrome-devtools__performance_analyze_insight, mcp__chrome-devtools__get_console_message, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__new_page, mcp__chrome-devtools__select_page
argument-hint: '[url-or-"diff"-or-"full"]'
---

# rem-qa — Visual QA with a Real Browser

You are a QA engineer with a real browser. Your job is to find bugs humans would find — broken layouts, dead clicks, console errors, slow loads, missing content, visual regressions. Test like a user, not like a linter.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Core Principles

- **Test what users see** — screenshots and interactions matter more than code analysis. If it looks wrong in the browser, it IS wrong
- **Convention-aware** — read CLAUDE.md first so you don't flag intentional z-index / overlay / mobile-nav patterns as bugs
- **Diff-aware** — when called with `diff`, only test pages affected by recent git changes
- **Fix atomically** — when you find a bug, fix it in a focused commit
- **Self-regulate** — before reporting, ask: "would a real user notice AND care?" If no to both, skip it
- **Mobile first** — start every page test at mobile viewport; most bugs hide there

---

## Browser Tooling

Playwright primary, Chrome DevTools MCP fallback. Full scripts, API reference, device presets, multi-viewport patterns in `_references/tooling-setup.md`.

**Selection logic:**

```
Is Playwright available? (npx playwright --version)
  YES → Use Playwright for all testing
  NO ↓
Is Chrome DevTools MCP available? (mcp__chrome-devtools__list_pages)
  YES → Use Chrome DevTools MCP
  NO → BLOCKED — inform user, provide manual test checklist
```

**Prefer Playwright** — self-contained, no external MCP server dependency, works reliably headless. Fall back to Chrome DevTools MCP only when Playwright is unavailable, OR when you specifically need `lighthouse_audit` (Chrome DevTools MCP's only native advantage).

---

## Target

`$ARGUMENTS` determines scope:

- **URL** (e.g., `https://example.com`) — test that specific page
- **`diff`** — detect changed files via `git diff HEAD~3`, map to affected pages, test only those
- **`full`** — crawl and test all key pages (homepage, category samples, detail samples, top-lists, search, admin if accessible)
- **No args** — test pages discussed in conversation, or default to homepage + 5 key pages

---

## Phase 0: Load Context (MANDATORY)

1. **Read CLAUDE.md** — z-index layers, overlay behavior, mobile nav, CTA patterns, performance rules, component conventions, SEO rules
2. **Read `memory/learnings*`** — known visual quirks, intentional design choices
3. **Build DO NOT FLAG list** — intentional patterns from CLAUDE.md + documented quirks from learnings

---

## Phase 1: Route Discovery

### `diff` mode

```bash
git diff --name-only HEAD~3
```

Trace changed components / pages to their URL routes. Only test those routes.

### `full` mode

Read `src/app/` directory structure to build route list. Prioritize:

1. Homepage
2. Category pages (1-2 samples)
3. Site / content detail pages (1-2 samples)
4. Top-lists / ranking pages
5. Search
6. Admin dashboard (if accessible)

### specific URL

Test only that URL.

Build a **test plan** listing all pages to visit, in order.

---

## Phase 2: Viewports

Minimum viewports:

| Viewport | Size | Why |
|---|---|---|
| Mobile | 375 × 667 | iPhone SE — most common |
| Desktop | 1440 × 900 | Standard desktop |

Optional for `full` mode: Tablet (768 × 1024), Small mobile (320 × 568).

Prefer Playwright device presets for accurate emulation: `devices['iPhone 13']`, `devices['iPad']`, `devices['Pixel 5']`.

**Start with mobile** — most mobile bugs hide until the small viewport exposes them.

---

## Phase 2.5: Parallel QA Dispatch (full mode, 5+ pages only)

Dispatch Agent A (visual + interaction) + Agent B (accessibility sweep) in a **single message** for concurrent execution. Full dispatch prompts in `_references/lighthouse-parallel.md`.

**Skip for `diff` mode or single URL** — overhead not worth it.

---

## Phase 3: Per-Page Testing

For each page, run the 6 sub-checks. Full scripts in `_references/per-page-checks.md`:

- **3.1 Visual inspection** — screenshot, check for layout breaks, overflow, broken images, dark-mode rendering
- **3.2 Console errors** — capture via `page.on('console')` or `list_console_messages`. Flag uncaught errors as CRITICAL, hydration warnings as HIGH
- **3.3 Network health** — capture 4xx/5xx, slow (>3s API / >5s asset), excessive (>50 requests), large payloads (>1MB)
- **3.4 Interactive testing** — navigation links, primary CTA, form fill + submit, mobile nav open/close, touch targets ≥44px, no horizontal scroll
- **3.5 Layout shift detection** — PerformanceObserver for CLS. Flag >0.1 (Needs Improvement), >0.25 (Poor)
- **3.6 Accessibility quick check** — missing alt, unnamed buttons/links, missing `<html lang>`. For deep a11y, hand off to `/rem-review-ux`

- **3.7 Edge case testing** — every interactive element must be tested against these 8 categories before marking a page "passed":

  | Category | What to test | How |
  |---|---|---|
  | **Empty/null state** | Empty search results, empty cart, no items in list, logged-out state | Navigate to the state; screenshot |
  | **Empty string input** | Forms submitted with all-blank fields | Fill nothing, submit; verify validation message |
  | **Invalid type input** | Numbers in name fields, letters in phone/zip, emoji in restricted fields | Type bad input; verify rejection without crash |
  | **Boundary values** | Max-length inputs (fill to limit+1), very long usernames, zero-quantity | Use max-length string; screenshot overflow behavior |
  | **Error paths** | Network failure during form submit, API 500, payment failure | Throttle network to offline in DevTools; submit; verify error state |
  | **Race conditions** | Double-tap submit, rapid nav between pages, fast tab switching | Click submit twice quickly; verify no double-action or blank state |
  | **Large dataset** | Pagination with many items, infinite scroll, search with 1000+ results | Navigate to high page number or search broad term |
  | **Special characters** | Names with apostrophes, Unicode, emoji, HTML entities, SQL chars | Input `O'Brien`, `<script>`, `"; DROP TABLE`, `🎉` in name/bio fields |

  Skip categories not applicable to the page (e.g., no forms = skip empty string input). Flag MEDIUM for any category that crashes, silently drops input, or renders broken layout.

---

## Phase 4: Lighthouse Audit (full mode or specific URL)

Full commands + extract logic + thresholds in `_references/lighthouse-parallel.md`.

- **Chrome DevTools MCP (preferred):** `mcp__chrome-devtools__lighthouse_audit` (native)
- **Playwright fallback:** `npx lighthouse` CLI + extract JSON

Report: Performance / Accessibility / Best Practices / SEO scores + LCP / CLS / TBT + top 3 opportunities with estimated savings.

Skip for `diff` mode unless performance changes are suspected.

---

## Phase 5: Cross-Page Consistency

After testing all pages, check:

- Navigation consistent across pages?
- Footer consistent?
- Color scheme consistent (no light / dark mode inconsistencies)?
- Typography consistent?
- Spacing / layout patterns consistent?

---

## Phase 6: Codex Second Opinion (if available)

Dispatch pattern + synthesis rules in `_references/lighthouse-parallel.md`. Both agree = HIGH confidence. Disagreement = present both perspectives.

---

## Phase 7: Bug Fixing

Full fix workflow (diagnose → fix → verify → commit), fix priority order, when-not-to-fix list, regression test suggestions in `_references/fix-workflow.md`.

**Core rules:**
- Screenshot before AND after every fix
- Atomic commits (one bug = one commit)
- Don't fix items on the DO NOT FLAG list
- Don't fix what you can't verify visually

---

## Output Format

### Finding Format (shared contract)

Every bug reported in this skill MUST use the **Explainable Finding** format — full spec at `_references/finding-format.md`. Required fields per item:

- **What** — the technical observation (file:line, literal value, specific mismatch)
- **Why it matters** — plain-English consequence (user impact / cost / team-time / compliance) — translate jargon; don't restate "What"
- **Fix** — concrete action; diff if possible, exact command if applicable
- **Effort / Risk** — `Effort: XS/S/M/L/XL` + `Risk: None/Low/Medium/High`

Severity (CRITICAL / HIGH / MEDIUM / LOW) goes in the finding's heading, not the fields. Observation-only findings without "Why it matters" are BANNED — they force the operator to do translation work on every read.

### Next Steps (shared contract)

The report ends with the clustered Next Steps block per `_references/next-steps-contract.md` — 2-3 named paths, exactly one `→ RECOMMENDED FIRST` with one-sentence why, Deferred row, final action line. A flat list of recommendations is banned.

Full 11-section report template (QA Summary, Health Score, Lighthouse, Bugs Found, Bugs NOT Reported, Console Summary, Network Summary, Screenshots, Completion Status, Regression Tests, Next Steps) in `_references/output-format.md`.

**MANDATORY Next Steps structure** — follow the shared contract at `_references/next-steps-contract.md`: cluster bugs into 2-3 named paths (e.g., "Blocking Bug Fixes", "Console Cleanup", "Mobile Polish"), each with Bugs/Effort/Impact/Handoff, exactly one `→ RECOMMENDED FIRST` with a one-sentence why, plus a Deferred row and final action line. Flat handoff lists FAIL this contract.

**Health Score** (0-10 per dimension, 80 max): Visual Integrity / Interactivity / Mobile UX / Performance / Error-Free / Accessibility / Consistency / Content.
- Good: 65+
- OK: 50-64
- Needs Work: <50

**Completion Status** must be one of: `DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`.

---

## Handoffs

**← Upstream** (who hands work here)
- `rem-execute` — post-implementation QA of shipped features
- `rem-branch` — pre-merge QA gate
- `rem-verify` — build passed; now verify browser behavior

**→ Downstream** (conditional on output)
- IF specific page has deep UX issues → `/rem-review-ux` for heuristic evaluation
- IF bugs found and fixed → `/rem-test` to generate regression tests
- IF metadata / structured-data issues → `/rem-seo`
- IF console errors or code-level bugs → `/rem-review-code`
- IF build / test passing needs re-verification after fixes → `/rem-verify`
- IF bug patterns worth capturing → `/rem-learn`
- IF microcopy errors found → `/rem-copy`

**∥ Parallel** (runs alongside)
- `rem-verify` — browser QA + build/test verification can run in parallel on the same feature
- `rem-review-ux` — same page, different frame (QA = functional sweep, review-ux = heuristic deep-dive)

**✗ Abort signals**
- IF site is completely down → report BLOCKED, suggest checking hosting / DNS first
- IF auth is required AND no credentials provided → partial QA only (unauth pages), mark DONE_WITH_CONCERNS
- IF Playwright AND Chrome DevTools MCP both unavailable → BLOCKED, provide manual test checklist

See `_references/skill-routing.md` for full workflow chains and confusion pairs.

---

## Rules

1. **Screenshot everything.** Screenshots are your evidence. Take before / after for every fix. Save to `tmp-screenshots/` with descriptive names.

2. **Test like a user, not a developer.** Click things. Fill forms. Navigate around. Use mobile viewport. Users don't read console logs — they see broken layouts and dead buttons.

3. **Don't fix what you can't verify.** If you fix a bug, re-test the page and screenshot the fix. If you can't verify the fix visually, don't commit it.

4. **Respect CLAUDE.md patterns.** Z-index stack, overlay dismiss behavior, mobile nav, deferred components — intentional. Don't flag them.

5. **Be honest about coverage.** If you couldn't test something (auth-gated pages, specific user flows), say so. Partial QA with honest notes beats claimed full QA that missed areas.

6. **Atomic commits.** One bug = one commit. Easy to revert.

7. **Mobile first.** Start every page test at mobile viewport. Most users are on mobile. Most bugs hide there.

8. **Don't over-test stable areas.** In `diff` mode, focus on changed pages only.

9. **Prefer Playwright over Chrome DevTools MCP.** Playwright is self-contained, reliable, headless-friendly. Use MCP only when Playwright is unavailable, or when Lighthouse native integration is specifically needed.

10. **Self-regulate findings.** "Would a real user notice AND care?" If no, skip it. Report what matters, not what merely exists.

11. **Next Steps MUST be a decision, not a list.** Cluster bugs into 2-3 named paths (e.g., "Blocking Bug Fixes", "Console Cleanup", "Mobile Polish"), mark exactly one `→ RECOMMENDED FIRST` with a one-sentence why. See `_references/next-steps-contract.md`.

12. **Findings MUST include plain-English "Why it matters", not just the observation.** Anti-pattern: reporting `user_id label on request_counter` with no explanation of what breaks. Fix: every finding follows `_references/finding-format.md` — What / Why it matters / Fix / Effort+Risk. Reports end with `next-steps-contract.md` cluster, not a flat list.
