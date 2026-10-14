---
name: rem-review-ux
description: UX/UI review — Nielsen heuristics, accessibility, visual hierarchy, mobile UX, conversion flow, state coverage, dark patterns. Review UI, review UX, review design, review usability, review this page, check accessibility, a11y review, WCAG audit, UX audit, design review, usability review, UI review, heuristic evaluation. Runs automated a11y audit script (alt text, labels, heading hierarchy, touch targets, landmarks, duplicate IDs, viewport) via Chrome DevTools, then manual review of what the script cannot catch (contrast, focus, keyboard traps, ARIA correctness, cognitive load, dark patterns). Convention-aware — reads CLAUDE.md and learnings first so it never flags intentional design decisions. Distinct from rem-qa (visual/interactive browser testing across many pages; rem-review-ux is heuristic evaluation of a specific page), rem-audit (repo-wide code quality; rem-review-ux is UX-only), rem-cro (conversion optimization strategy; rem-review-ux audits without experimentation), rem-seo (discoverability markup; rem-review-ux is user-experience). Pairs with rem-qa for visual regression across pages, rem-cro for conversion experiments on issues found.
user-invocable: true
allowed-tools: Read, Grep, Glob, Task, Bash, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__list_console_messages, mcp__chrome-devtools__list_network_requests, mcp__chrome-devtools__emulate, mcp__chrome-devtools__resize_page, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__click, mcp__chrome-devtools__hover, mcp__chrome-devtools__fill, mcp__chrome-devtools__press_key, mcp__chrome-devtools__performance_start_trace, mcp__chrome-devtools__performance_stop_trace, mcp__chrome-devtools__performance_analyze_insight
argument-hint: '[files-or-url]'
---

# rem-review-ux — UX/UI Review

Senior UX/UI designer + accessibility expert + front-end performance specialist. Convention-aware — never flag intentional design decisions as issues.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file. When the fan-out runs, say it plainly ("I captured the page, now several independent reviewers look at it through different lenses, then a separate reviewer double-checks each issue"). Never surface "lens / finder / UL1 / Context Packet / score ≥80" — translate.

## Core Principles

- **Convention-first** — read CLAUDE.md and learnings BEFORE reviewing. If a pattern is established by project convention (design system, brand, component library), don't flag it
- **History-aware** — check learnings.md for known UX decisions. If intentionally chosen ("we use hamburger menu because..."), don't re-flag
- **Find wide, verify independently** — UX is subjective, which is exactly why precision can't come from the reviewer self-censoring. Lens finders surface every clear-problem candidate (each with an honest "could be preference" note); a *separate* verifier then scores each ≥80 and drops taste-not-problem findings. The reviewer never talks itself out of a finding at generation. Engine: `_references/fanout-review-protocol.md`
- **Acknowledge what works** — don't only report problems. Note strong patterns worth preserving
- **Scale to project** — micro-SaaS priorities differ from enterprise. Prioritize what affects real users now

## How this review runs

NOT one pass walking 12 evaluation areas in sequence and then self-dropping anything under 80% confidence — that single-context generate-and-self-judge shape is what makes a reviewer quietly discard real problems as "probably just my preference." Instead: capture the page once, fan out independent heuristic lens finders over the captures, then an independent verifier enforces precision. Lens map: `_references/ux-lenses.md`.

## Target

Review `$ARGUMENTS`. If a URL or running app, the Capture Pass takes screenshots at multiple viewports and a snapshot. If files, read component code and trace the user flow.

---

## Step 0: Load Project Context + Build the Context Packet (MANDATORY)

1. **Read project CLAUDE.md** — design system, component library, brand guidelines, established UI patterns, styling approach (Tailwind config, theme tokens)
2. **Read `memory/learnings*`** — known UX decisions, intentional trade-offs, previously reviewed and accepted patterns
3. **Read `memory/feedback_*.md`** — user corrections on design approach

**Assemble the Context Packet** (`fanout-review-protocol.md` § Stage 0) and inline it into every lens finder AND the verifier — Task sub-agents start fresh and will flag intentional design as a problem without it:
- **DO NOT FLAG**: design patterns CLAUDE.md establishes, UX decisions documented as intentional, UI patterns consistent with the rest of the app (internal consistency > external convention)
- **Page context**: interface type + target user + primary goal + device context (from Step 1)
- The verifier scores anything matching DO NOT FLAG as 0.

---

## Step 1: Context Gathering

Before reviewing, understand:
- What type of interface? (marketing, app, admin, checkout, content)
- Who is the target user? (tech-savvy, general public, professionals)
- What is the primary user goal on this page/screen?
- What device context matters most? (mobile-first? desktop-heavy?)

---

## Capture Pass (Steps 2-5, orchestrator-run ONCE)

The live-browser work happens here and ONLY here. The Chrome DevTools MCP is a single session, so the orchestrator captures the page once and the lens finders (Step 6) reason over these artifacts — no finder drives the browser. Skip the live steps for a code-only review (read components instead) and mark un-capturable states "unverified," don't fabricate them.

**Targeted re-capture (closes the coverage gap):** if a lens flags a high-value interaction the fixed battery didn't cover (a specific widget's focus trap, an unreached error state, an invalid-submit path), the orchestrator runs ONE sequential follow-up capture for it before Step 8, then feeds the result to verification. The single-session rule only bars *parallel finder-driven* browser calls — a sequential orchestrator re-capture is fine. Don't leave a checkable interaction at "unverified" when one targeted capture would settle it.

### Step 2: Multi-Viewport & Multi-Mode Capture (live URLs)
Capture at multiple breakpoints — **Mobile** 375×667 (primary for most users) · **Tablet** 768×1024 (often forgotten) · **Desktop** 1440×900 (full). For each: screenshot + snapshot. Then alternate modes: **Dark** (`emulate({ colorScheme: "dark" })`, screenshot, reset to `"auto"`) and **Light** — compare for contrast issues, missing theme tokens, broken visuals.

### Step 3: Performance & Network Impact on UX
Speed IS a feature: run a performance trace (`reload: true, autoStop: true`); analyze insights for LCP/CLS/INP; check network for render-blocking resources; check console for errors/warnings indicating broken UX; test degraded network (`emulate({ networkConditions: "Slow 3G" })`, screenshot loading states, reset).

### Step 4: Automated Accessibility Audit
Run the a11y script via `evaluate_script`. Full script + interpretation in `_references/a11y-audit-script.md`. Captures: images (alt), buttons/links (empty), heading hierarchy, form labels, touch targets <44×44, landmarks, `<html lang>`, skip link, duplicate IDs, viewport meta. **These results are reported once and passed to the UL3 finder so it does NOT re-flag what the script caught.**

### Step 5: Interactive Testing (live URLs)
Test interactions and log the results for the finders: Tab through the page (`press_key({ key: "Tab" })`, check focus visibility), click primary CTA (feedback + state change), hover interactive elements, fill + submit a form (validation behavior), Escape on modals/overlays, keyboard nav of dropdowns/carousels/accordions.

---

## Step 6: Lens Fan-Out (the finders)

Parallel independent `Task` lens-finders, each evaluating the captured page through one heuristic lens, each blind to the others. Mechanics: `fanout-review-protocol.md` § Stage 1. Lens definitions: `_references/ux-lenses.md`.

1. **Select lenses.** One page is a bounded surface, so the default runs all 5 in parallel (UL1 Nielsen · UL2 visual/interaction/mobile · UL3 manual WCAG · UL4 content/trust/conversion/state · UL5 i18n/dark-patterns/psychology). A quick review runs UL1+UL2+UL3.
2. **Dispatch finders in parallel** — one `Task` per lens, single message. Each prompt = the **Context Packet** (Step 0) + the Capture-Pass artifacts (screenshots, snapshot, perf insights, a11y-script results, interaction log) + the lens mandate from `ux-lenses.md` + the "liberal finder" rule + required return shape. Finders reason over the captures — they do NOT call the browser.
3. **Finders are liberal.** Each surfaces every clear-problem candidate with its location (element / screenshot region), a `why_real`, and an honest `why_maybe` ("could be preference because..."). They do NOT self-suppress on "this might just be my taste" — that's the verifier's job (Step 8). Only the DO NOT FLAG list is out of scope. Cite named principles (Nielsen # · WCAG SC · Fitts/Hick/etc.).

---

## Step 7: Dedupe + Cross-Lens Synthesis

Plain orchestrator work, no agent (protocol § Stage 2):
1. **Dedupe** candidates by element + issue; agreement across lenses is a confidence signal.
2. **Cross-lens synthesis** — the seams: a Nielsen consistency issue (UL1) that's also a visual-hierarchy break (UL2) · a dark pattern (UL5) that's also a conversion-flow leak (UL4) · a contrast failure (UL3) that's also a color-system problem (UL2) · a state (UL4) with no accessible status announcement (UL3). Promote as `cross-cutting` — often the highest-value because they recur across the page.

---

## Step 8: Independent Verification (where precision lives)

UX findings are subjective, so precision MUST come from a fresh judge, not the finder second-guessing itself. A **separate verifier that did not generate the findings** scores each candidate. Full spec: `fanout-review-protocol.md` § Stage 3.

1. **Dispatch the verifier** (cheap / Haiku-class) with the **Context Packet** + candidates, in small batches (~5-8) with a one-line justification per score. One page is usually one or two batches.
2. **Score each candidate 0-100** (0 = preference / false positive · 25 = unverifiable · 50 = real but minor · 75 = clear UX problem · 100 = blocks the user). The verifier applies the drops the finders did NOT:
   - DO NOT FLAG / convention-required / consistent-with-the-app (internal consistency > external convention) → score 0
   - **taste, not a problem** (a different design choice, not a usability defect) → score low. This is the gate UX most needs: weigh each finder's `why_maybe` honestly — if it reads as preference, drop it.
   - already caught by the automated a11y script (Step 4) → score 0 (reported once, not re-flagged)
3. **Filter: keep only ≥ 80.** Record everything dropped (with its score) for the "Findings NOT Reported" section.

If no separate agent is available, self-verify in a deliberately fresh frame (judge each as "real problem vs my preference" as if it were someone else's finding) and note that verification was not independent. The ≥80 threshold is non-negotiable.

---

## Output Format

### Finding Format (shared contract)

Every finding reported in this skill MUST use the **Explainable Finding** format — full spec at `_references/finding-format.md`. Required fields per item:

- **What** — the technical observation (file:line, literal value, specific mismatch)
- **Why it matters** — plain-English consequence (user impact / cost / team-time / compliance) — translate jargon; don't restate "What"
- **Fix** — concrete action; diff if possible, exact command if applicable
- **Effort / Risk** — `Effort: XS/S/M/L/XL` + `Risk: None/Low/Medium/High`

Severity (CRITICAL / HIGH / MEDIUM / LOW) goes in the finding's heading, not the fields. Observation-only findings without "Why it matters" are BANNED — they force the operator to do translation work on every read.

### Next Steps (shared contract)

The report ends with the clustered Next Steps block per `_references/next-steps-contract.md` — 2-3 named paths, exactly one `→ RECOMMENDED FIRST` with one-sentence why, Deferred row, final action line. A flat list of recommendations is banned.

Full report template (18 sections with tables, score card, flow analysis, fix sequencing) in `_references/output-format.md`.

**Section order summary:**

1. Convention Context Loaded · 2. Executive Summary · 3. UX Score Card (9 dimensions, 🟢/🟡/🔴) · 4. Automated Audit Results · 5. Findings Report (ID-tagged, priority-sorted) · 6. Findings NOT Reported (incl. verifier-dropped <80, with scores) · 7. UX Strengths · 8. Quick Wins · 9. Mobile-Specific Issues · 10. Accessibility Gaps · 11. State Coverage Gaps · 12. User Flow Analysis · 13. Design Recommendations · 14. Competitive Context · 15. Cross-Lens Findings · 16. Fix Sequencing Plan · 17. Completion Status · 18. Next Steps — Choose Your Path

**MANDATORY Section 18 structure** — follow the shared Next Steps contract (2-3 named paths like "A11y Critical", "Mobile UX Sweep", "Conversion Polish" — each with Findings/Effort/Impact/Handoff, exactly one `→ RECOMMENDED FIRST` with a one-sentence why, plus Deferred row and final action line). Flat handoff lists FAIL this contract. Load the ref before producing the report.

---

## Handoffs

**← Upstream** (who hands work here)
- `rem-qa` — cross-page sweep flags a specific page → deep heuristic evaluation here
- `rem-cro` — CRO audit surfaces UX issues needing heuristic framing
- `rem-execute` / `rem-branch` — post-ship UX validation of new flows

**→ Downstream** (conditional on output)
- IF cross-page visual regression needed after UX fixes → `/rem-qa`
- IF conversion experiments justified by findings → `/rem-cro`
- IF microcopy / error message rewrites needed → `/rem-copy`
- IF a11y violations need code-level fixes → `/rem-review-code`
- IF metadata / structured-data issues surface → `/rem-seo`
- IF findings reveal systemic a11y issues → `/rem-audit`
- IF UX pattern worth capturing → `/rem-learn`

**∥ Parallel** (runs alongside)
- `rem-seo` — same page, different concern (UX for users, SEO for discoverability)

**✗ Abort signals**
- IF page is auth-gated AND no test credentials available → report BLOCKED (partial review only)
- IF CLAUDE.md establishes an unconventional pattern as intentional design → DO NOT FLAG it (per convention-first rule)

See `_references/skill-routing.md` for full workflow chains and confusion pairs.

---

## Rules

1. **Read conventions BEFORE reviewing + build the Context Packet.** Step 0 is mandatory. A finder dispatched without the packet hasn't read CLAUDE.md and will flag the project's intentional design (an unconventional-but-deliberate nav, a brand color) as a problem. Inline the packet into every finder AND the verifier.

2. **Separate problems from preferences — in the verifier, not the finder.** A missing loading state is a problem; preferring a different blue is a preference. Finders surface clear-problem candidates with an honest "might be preference" note; the Step 8 verifier (a separate agent) drops taste-not-problem findings. Never self-suppress at generation — that's exactly how real UX problems get discarded as "probably just my preference."

3. **Internal consistency trumps external convention.** If the app consistently uses pattern X (even if unusual), don't flag it. Flag only if some pages use X and others use Y — that's inconsistency.

4. **Don't flag what the automated a11y script catches.** Report script results once in Automated Audit Results, then the UL3 finder focuses manual review on what the script cannot see.

5. **Be specific with fixes.** "Improve the contrast" is not actionable. "Change `text-gray-400` to `text-gray-600` on `.card-subtitle` for 4.5:1 contrast ratio" is actionable.

6. **Acknowledge good UX.** If a flow works well, say so. If a component is well-designed, note it. This gives the user confidence about what NOT to change.

7. **Cite named principles.** Nielsen heuristic number, WCAG SC, Fitts's Law — named citations are more credible than vague concerns.

8. **Next Steps MUST be a decision, not a list.** Cluster findings into 2-3 named paths (e.g., "A11y Critical Fixes", "Mobile UX Sweep", "Conversion Polish"), mark exactly one `→ RECOMMENDED FIRST` with a one-sentence why. See `_references/next-steps-contract.md`.

9. **Scale to the project.** Micro-SaaS projects don't need enterprise i18n readiness. Prioritize what affects real users now.

10. **Handoff explicitly.** Surface code-quality issues → rem-review-code. Discoverability → rem-seo. Cross-page visual regression → rem-qa. Microcopy rewrites → rem-copy. Conversion experiments → rem-cro.

11. **Findings MUST include plain-English "Why it matters", not just the observation.** Every finding follows `_references/finding-format.md` — What / Why it matters / Fix / Effort+Risk. Reports end with the `next-steps-contract.md` cluster, not a flat list.

12. **Capture once, fan out over the captures.** The MCP browser is single-session — the orchestrator runs the Capture Pass (Steps 2-5) once; lens finders reason over the artifacts and never touch the live browser. Dispatching finders that each drive the browser will conflict or hang.

13. **Narrate in plain language, never lens/UL-IDs/Context-Packet jargon.** Phase labels and lens IDs are internal anchors; the user hears "I captured the page, then several independent reviewers looked at it, then a separate double-check." Publication gate per `_references/output-voice.md`.
