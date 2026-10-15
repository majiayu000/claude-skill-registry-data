---
name: ship-polished-ui
description: >-
  Create or improve premium, production-grade web UI (site, landing page, app screen, component). Triggers: "crée un site", "make this premium", "améliore l'UI", "polish the page", UI bugs, "vérifie que ça marche". Always runs real-browser QA and a Verification Ledger. Documents: use design-elevation.
---

# ship-polished-ui — Premium frontend craft, browser-verified

Pair the in-house design doctrine (**[references/design-direction.md](references/design-direction.md)** — the taste authority) with a disciplined visual QA loop. The doctrine handles taste. This skill handles craft — actually verifying in a real browser that the change shipped without regressions, hidden bugs, or the half-finished feeling of "looks fine on the bit I happened to screenshot." Why this discipline exists, with the real bugs behind it: [references/why-and-anti-patterns.md](references/why-and-anti-patterns.md).

## Step 0 — Route before you build

Before Phase 1, decide which lane you are in:

- **New site / greenfield, no `design-intent.md` present** → the taste-and-direction contract is missing. Offer to run **design-forge BRIEF** first (it turns the brief + brand-package into a `design-intent.md` with art direction, testable criteria, and a motion stance). If the user wants to proceed without it, you own the direction yourself via the Design Spec (Phase 1) — but say so explicitly.
- **Retouche / improving an existing UI** → skip the brief, go straight into the two-phase loop below.
- **Purely documentary request** (a plan HTML, a report, a slide deck, a dashboard read but not shipped) → this is **not** a ship-polished-ui job. Hand off to **design-elevation**, which owns documentary artifacts.

This routing keeps ship-polished-ui the single entry point for client websites and app UIs, while documentary work and up-front art direction live in their own skills.

## The two-phase loop

For any request that triggers this skill, run the loop:

```
┌──────────────────────────────────┐
│  Phase 1 — Design                │
│  In-house doctrine (design-      │
│  direction.md) for direction     │
└──────────────┬───────────────────┘
               │ apply edits
               ▼
┌──────────────────────────────────┐
│  Phase 2 — Verify                │
│  Browser-based visual QA loop    │
│  (see references/visual-qa-      │
│  checklist.md)                   │
└──────────────┬───────────────────┘
               │ found a bug?
       ┌───────┴───────┐
       │ yes           │ no
       ▼               ▼
   loop back       declare done
```

Repeat until **every cell of the Verification Ledger is PASS with evidence** (see Phase 2). The exit condition is objective, not a feeling: not "zero issues at the scope the user cares about," but a posted ledger in which no cell is left `not-evidenced` and any scope reduction was explicitly approved by the user and recorded. **Do not declare a UI change "done" without posting a completed Verification Ledger** — the ledger *is* the definition of done.

## Phase 1 — Design

Full procedure: **[references/phase1-design.md](references/phase1-design.md)** (contracts to load, visual direction, motion inventory, Design Spec block and its eight rubrics). The binding rules:

- **Load the contracts first.** `Glob` for `**/design-intent.md`, `docs/branding/brand-package.md`, `docs/branding/brand-tokens.css`, `**/tokens.css`. A brand-package makes palette and typography `brand-fixed` (import the tokens, never retype a hex). A `design-intent.md` binds Phase 1 and its TESTABLE CRITERIA become Verification Ledger rows. On a greenfield site with neither, declare it and offer design-forge BRIEF first.
- **Read `references/design-direction.md` before posting the Design Spec.** Mandatory.
- **Animated surface, showcase site or landing page: read `references/motion-craft.md` before coding** and post a motion inventory (hover/press, hero entrance, scroll reveals, exactly one signature moment, reduced-motion behavior). A page that ships 100% static does not pass this skill.
- **You may not write a line of CSS before you have posted the Design Spec**, all eight rubrics filled: typography, named palette, one layout primitive, signature moment, 1-3 real references (Match/Change), motion inventory, media strategy, persona + art-direction seed + real data. Bare adjectives ("clean", "modern", "premium") are forbidden unless attached to a named reference. On an ambitious request, sketch 3 directions first and choose one with justification.
- Define any new color, shadow or z-index as a token before using it. Move to Phase 2 right after the first edits; do not batch.

## Phase 2 — Verify (the non-negotiable loop)

The output of this phase is one artifact: the **Verification Ledger** — an accountable table posted in the chat, not a prose "looks good." It replaces self-attestation. The full format, the two families of rows, the honesty rule, and the objective exit condition live in **[references/visual-qa-checklist.md](references/visual-qa-checklist.md)** Sections 1 (build the matrix → ledger) and 12 (post the completed ledger). The essentials:

- **Post the scope matrix as a table in the chat *before* the first screenshot.** A matrix "in your head" does not exist. On a **full-site build**, the matrix is the inventory pages × sections × viewports (there is no "changed CSS" scope on greenfield).
- **Seed the matrix deterministically when the codebase is accessible.** Run `node scripts/scan-surfaces.mjs <project-root>` (in `scripts/` next to this SKILL.md; installed as a plugin: `${CLAUDE_PLUGIN_ROOT}/skills/ship-polished-ui/scripts/`) and save its JSON manifest — **the manifest is the surfaces axis of the matrix**. You may add surfaces beyond it; any manifest surface you drop must be declared out of scope in the ledger, never silently omitted. If the script cannot run in this environment, write that as a declared gap in the ledger — a failed script is a gap, not a permission to skip.
- **Viewports include 320/360 (small-mobile).** The verdict is **invalid** if a device class was never actually rendered — a binary gate, not a nicety.
- **A cell that was not rendered is `not-evidenced`, never PASS.** A PASS requires a real proof: every check row names a screenshot file path (`qa-shots/<name>.png`) that exists on disk, plus the measured value where applicable (`scrollWidth/clientWidth`, contrast ratio, touch-target px).
- **Objective exit condition:** every ledger cell is PASS with evidence; any scope reduction is explicitly approved by the user and recorded in the ledger. There is no subjective "scope the user cares about." **Machine gate:** before declaring done, save the ledger turn to a file and run `node scripts/check-ledger.mjs <ledger-file> [manifest.json]` — it must exit `0`. Each `MANQUE :` line on stderr is a correction to make; loop until clean.

### The VERIFICATION LEDGER marker (mandatory, machine-checkable)

Post the ledger under a heading that contains the **exact** string `VERIFICATION LEDGER` (e.g. `## VERIFICATION LEDGER — {project} — {date}`). This exact marker is how tooling (and the user) locate the ledger; do not paraphrase it ("verification table", "QA ledger", etc. do not count). `scripts/check-ledger.mjs` enforces exactly this contract: marker present (or a motivated `LEDGER-EXEMPT:` line), no `not-evidenced` cell counted PASS, mandatory viewports (320/360/375/768/desktop) present, and — when given the scan-surfaces manifest — every scanned surface covered or declared out of scope.

**Auditable escape hatch — never silent.** If a turn that runs after this skill was invoked is legitimately **not** a UI turn (e.g. the user pivoted to an unrelated question, or the work was a pure non-visual refactor with nothing to render), you may skip the ledger — but only by writing, in that turn, the exact line `LEDGER-EXEMPT: <reason>` stating why no ledger applies. This is an explicit, logged exception, never an implicit omission: either a `VERIFICATION LEDGER` heading or a `LEDGER-EXEMPT:` line must appear on any turn that would otherwise declare UI work done.

**Consume the design-intent contract.** If Phase 1 loaded a `design-intent.md`, its **TESTABLE CRITERIA become additional lines of the Verification Ledger** — one ledger row per criterion, each demanding a real measured proof, never a declarative PASS. The design-intent's motion stance and art direction are checked here the same way.

**Verify the Design Spec, decision by decision.** The Design Spec posted in Phase 1 (§1.3) is a contract with Phase 2: the ledger carries **one `conformité Design Spec` transverse row per Spec decision**, each backed by a real proof, never a declarative PASS. Concretely — the **named typography** is actually loaded (`@font-face`/grep on the served CSS), the **named palette** is present as tokens (not a stray hex), the **layout primitive** repeats where the Spec said, the **signature moment** exists and works (see Motion QA), and the **media** respects the perf rules of motion-craft §⑨. A Spec decision with no matching ledger row was declared, not verified.

Tooling correspondence, the eleven headline checks (scope matrix, open the running app, multi-position screenshots, element zoom, interactive states, adjacent elements, label/value pairs, responsive sweep and data states, reading ergonomics, premium-craft and component-intent, loop until clean): **[references/phase2-verify.md](references/phase2-verify.md)**. The operational core is **[references/visual-qa-checklist.md](references/visual-qa-checklist.md)** — read it on every invocation. Every fallback tool actually used is recorded in the ledger.

## Before client delivery, and delegation

- Before anything ships to a client, run **design-forge AUDIT** (or **TEST** when a live-driving tool is available) against the `design-intent.md`. ship-polished-ui runs the incremental visual-QA loop during the build; design-forge runs the independent pre-delivery audit. Neither replaces the other.
- Dispatch the `visual-qa-inspector` agent (`subagent_type: visual-qa-inspector`; its output is the Verification Ledger itself) when the change touches more than 3 components (blocking, not optional), under heavy context pressure, or when you think "I'll just take one screenshot". Skip it for trivial changes (one CSS file, ~10 lines). If the agent is absent, run the full checklist inline at no reduced coverage and note that in the ledger. Briefing and placement: [references/agent-dispatch.md](references/agent-dispatch.md), [references/packaging-as-plugin.md](references/packaging-as-plugin.md).

## Read these references when relevant

- **[references/design-direction.md](references/design-direction.md)** — design doctrine; mandatory before the Design Spec.
- **[references/motion-craft.md](references/motion-craft.md)** — motion and 3D playbook; mandatory before coding any animated surface.
- **[references/visual-qa-checklist.md](references/visual-qa-checklist.md)** — Phase 2 operational checklist (14 sections), including the slop and swap-brand gate (`slop-lint.mjs`).
- **[references/css-side-effects.md](references/css-side-effects.md)** — read when touching `overflow`, `position`, `z-index`, `isolation`, `clip-path`, `filter`, `transform`, `backdrop-filter`, `background-attachment`, or container sizing.
- **[references/iframe-and-host-shells.md](references/iframe-and-host-shells.md)** — read whenever the app is hosted inside another shell (Power Apps, Salesforce, embeds).
- **[references/why-and-anti-patterns.md](references/why-and-anti-patterns.md)** — the bugs behind the discipline, the anti-patterns table (always-wrong moves), reporting tone. Read before declaring done.
- **session-lessons-2026-05-04 / 05-21 / 05-31** (`references/`) — concrete bugs caught in real sessions: looking harder, the viewport matrix, and the correct / comfortable / premium axes.
- **[references/phase1-design.md](references/phase1-design.md)**, **[references/phase2-verify.md](references/phase2-verify.md)** — the full Phase 1 and Phase 2 procedures.
