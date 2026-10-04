---
name: arch
description: Use this skill for any decision about how an app's code and files are structured — the architecture, folder layout, and where things live. Trigger it when starting a new codebase's structure, adding a feature or large chunk of code, creating new files that must land in the right place, reviewing or auditing an existing structure ("how's my architecture", "is this a mess", "red flags"), when an app has grown too big and needs restructuring, or before any refactor of a live app's structure so it doesn't break. Strongly prefer arch over improvising folder placement or restructuring by feel, even when the user doesn't say the word "architecture". Arch reads what's already there before recommending, fits the structure to the project's scope (it does NOT default to any one architecture like FSD), and treats restructuring of a running app as a verified, reversible migration.
---

# Arch

Arch decides **how code and files are structured** — and keeps that decision consistent across sessions. It sits between `thinker` (decides *what* to build) and `qa-tester` (verifies it *works*): thinker hands off an approved plan, arch decides the structure, qa-tester confirms nothing broke.

**Cardinal rule — read before you recommend, and fit structure to scope.** Arch never prescribes an architecture blind. It reads what is already there (or, greenfield, what the scope demands) and recommends the *lightest structure that fits*. Over-architecting is as much a failure as under-architecting — FSD on a landing page is a mistake. **There is no default architecture; there is only the right rung for this scope.**

**Second rule — never change structure and behavior at once, and never touch what you can't verify.** Any restructuring of a live app runs as a verified migration with a test baseline and reversible steps, never a big-bang rewrite.

---

## Phases

```
0. ROUTE      → pick the mode; default entry on any existing codebase is ASSESS
1. ASSESS     → read what's there: file axis + code axis, red/yellow flags (tooling-backed)
2. RECOMMEND  → classify scope → pick the lowest structure rung that fits
3. BLUEPRINT  → greenfield only: establish structure + skeleton + enforcement + ledger
4. INTEGRATE  → new feature / big chunk: where it goes + no-break integration
5. PLACE      → single new file (fast path): apply the ledger's conventions
6. EVOLVE     → app got too big/messy: verified safe migration to a new structure
```

ASSESS is the front door. Almost every real invocation on an existing app starts there — you cannot advise a structure you have not read. Greenfield (BLUEPRINT) is the rare path. Move one phase at a time; do not skip to EVOLVE without ASSESS.

---

## Phase 0 — ROUTE

Read `ARCHITECTURE.md` at the repo root first if it exists — it is the ledger, the source of truth. Then dispatch on the request and repo state:

- Existing code + "review my structure / is this a mess / it's getting big" → **ASSESS**, then usually RECOMMEND or EVOLVE
- Existing code + "add feature X / a big new module" → **INTEGRATE**
- Existing code + "new file / new component" → **PLACE** (fast path, no ceremony)
- Existing code + "restructure / migrate / refactor the architecture" → **ASSESS → EVOLVE**
- No codebase yet + an approved plan (often a `thinker` spec) → **BLUEPRINT**
- Ambiguous → run **ASSESS** first; it is read-only and always safe.

Every phase reads the ledger before acting and writes back after.

---

## Phase 1 — ASSESS (the default entry point)

You cannot recommend a structure you have not read. Read `references/assessment.md` and evaluate **two independent axes** — they fail separately:

- **File structure** — organizing principle, naming consistency, colocation, nesting depth, barrel usage, whether folders reflect *enforced* boundaries or are decorative.
- **Code structure** — dependency direction and cycles, component design, where state lives, data-fetching consistency, cross-cutting handling (error/auth/i18n), abstraction health.

Back every finding with **real tooling, not vibes** (`madge`/`dependency-cruiser` for the dep graph and cycles, `knip` for dead exports, boundary linters, complexity/size metrics), then layer LLM judgment on what tools can't see. Grade findings 🔴 red / 🟡 yellow, each with evidence (the file/folder), *why* it's a problem, and a fix ranked by effort×impact. Snapshot the result into the ledger.

---

## Phase 2 — RECOMMEND (scope → the right rung)

Read `references/structure-ladder.md`. Classify the project's scope (app type, domain complexity, feature count, team parallelism, lifespan, rendering model), then recommend the **lowest rung on the ladder that fits** — climbing later is cheap, unwinding over-structure is expensive. Name the rung above and the concrete trigger for climbing to it. Flag over-architecture (e.g. "you're running FSD but only need feature-first") as loudly as under-architecture.

---

## Phase 3 — BLUEPRINT (greenfield only)

Take the approved plan (a `thinker` Technical Spec if present). Run RECOMMEND to pick the rung, then establish:

1. the folder skeleton for the chosen rung,
2. naming/placement conventions,
3. **enforcement config** (boundary linter, and `components.json` if shadcn is used),
4. an ADR recording the choice and its *why*,
5. the `ARCHITECTURE.md` ledger.

If FSD is the selected rung, read `references/fsd-shadcn-kit.md` for the canonical FSD + shadcn + Next.js setup (this is the one case that kit applies).

---

## Phase 4 — INTEGRATE (new feature / big chunk)

Read the ledger for the established conventions. Decide placement per the existing structure, then produce a **no-break integration plan**: what it touches, boundary compliance, required error/loading states, and a scaffold of the correct folders and files. For non-trivial integrations, apply the verify gates (typecheck → lint boundaries → build). Update the ledger; write an ADR if the integration made a real structural decision.

---

## Phase 5 — PLACE (single new file, fast path)

Read the ledger, apply the conventions (correct folder, naming, imports through the right public API), done. No ceremony — this lightweight path is what makes "strict file rules" automatic rather than manual discipline. If the file doesn't fit any existing convention cleanly, that's a signal — surface it and consider RECOMMEND.

---

## Phase 6 — EVOLVE (verified safe migration)

The app got too big or too messy and the structure must change. Read `references/safe-migration.md`. **Never big-bang.** Run the protocol:

```
UNDERSTAND → map the blast radius (dep graph, what imports what, what could break)
BASELINE   → qa-tester captures current behavior as a golden master + characterization tests
PLAN       → strangler: small reversible steps; mechanical moves before semantic ones
MIGRATE    → apply ONE step
VERIFY     → typecheck → lint boundaries → build → qa-tester vs baseline; auto-revert on red
RECORD     → update ledger + write an ADR for the migration
```

You cannot safely refactor code you cannot verify — the BASELINE step is not optional.

---

## Orchestration

Arch is the conductor, not the whole orchestra. It owns the plan and the structure; it delegates execution through the installed skill set. Route selection through **`decider`** (this repo's standard router — pass it the situation, stage, and tasks; it returns the picks), then hand off:

- Skill selection / routing → **`decider`**
- Behavior baseline + per-step verification → **`qa-tester`** (full pass) or **`verify`** (quick confirm one change works)
- What to characterize / test strategy → **`test-driven-development`** (design the characterization tests) or **`qa-automation-engineer`** (standing test architecture)
- Per-step structural sanity → **`code-review`**; quality-only cleanup → **`simplify`**
- A migration step that fails VERIFY for a non-obvious reason → **`systematic-debugging`** (root-cause first), or **`debugging-and-error-recovery`** for triage
- Writing the ADR / decision record → **`documentation-and-adrs`**
- Visualizing the resulting structure → **`sys-design`** (generates the architecture graph suite from the codebase — offer it after BLUEPRINT and after every EVOLVE so the new structure is documented visually)

This aligns with the repo's default pipeline (`PLAN → EXECUTE → [SECURE/A11Y/PERF] → REVIEW → TEST → VERIFY`): arch owns PLAN/EXECUTE for *structure*, then feeds REVIEW→TEST→VERIFY to the skills above. Read a chosen skill's own SKILL.md before running it. A handoff from `thinker` (an approved spec) is the input to BLUEPRINT.

---

## Enforcement over vibes

Instructions drift and models drift; what actually holds an architecture is machine enforcement. Whenever arch establishes or changes a structure, it emits the config that makes violations **fail**, not merely be discouraged: boundary/layer rules (`eslint-plugin-boundaries`, `Steiger` for FSD, `dependency-cruiser`), import-path conventions (tsconfig/vite aliases, `components.json` for shadcn), and a CI or pre-commit gate that runs them. An architecture without enforcement is a suggestion — emit the enforcement.

---

## The ledger

Read `references/ledger-and-adr.md`. Arch maintains `ARCHITECTURE.md` at the repo root as the single source of truth — chosen structure, conventions, boundaries, thresholds, known flags — plus `docs/adr/` for decisions with their *why*. Every phase reads the ledger first and writes back after. Without it, arch gives contradictory advice across sessions. Same discipline as qa-tester's persistent ledger.

---

## Operating principles

- **Read before you recommend.** ASSESS is the default; never prescribe blind.
- **Fit structure to scope.** Lightest rung that fits. Over-architecture is a red flag, not a virtue.
- **No default architecture.** Flat, feature-first, layered, FSD, hexagonal — each is right for a scope. Pick per project.
- **Never break the running app.** Structural change on a live app = verified migration, reversible steps, test baseline. No big-bang.
- **Enforce, don't advise.** Emit lint/CI config so the structure holds after arch leaves.
- **Evidence, not opinion.** Back flags with tooling output; cite the file or folder.
- **Delegate execution.** Arch plans and structures; `decider` routes; `qa-tester`/`code-review`/`systematic-debugging` execute; `sys-design` visualizes the result.
- **Match the user's language** (Russian, Uzbek, English).
- **Web-first, stack-aware.** Defaults tuned to Next.js 15 App Router + React Server Components + shadcn/ui (the repo's house stack); Flutter, Go, and others handled via the ladder's per-stack guidance and their own dependency tooling (see `references/assessment.md`).

---

## Worked examples (abbreviated)

**"My Next.js dispatcher app is getting huge and messy, help."**
ROUTE → ASSESS (read-only). Run `madge --circular` and `knip`; find 🔴 three circular deps between `features/orders` and `features/tracking`, a 900-line `Dashboard.tsx` with data-fetching inline, and 🟡 by-type folders straining at 40+ components. RECOMMEND: you're past feature-first — climb to FSD to get *enforced* isolation; here's the target rung and why. Then offer EVOLVE to get there safely. Nothing edited yet.

**"Add a live-chat feature to the app."**
ROUTE → INTEGRATE. Ledger says structure is FSD. Chat is a user interaction with business value → `features/chat` slice with `ui/model/api` segments; the WebSocket client goes in `shared/api`; it composes `Button`/`Input` from `shared/ui`. Scaffold the folders, list the boundary rules it must obey, note the error/reconnect states, run typecheck+lint gate.

**"Restructure the whole thing to FSD."**
ROUTE → ASSESS → EVOLVE. Refuse the big-bang. BASELINE current behavior via qa-tester first, then a strangler plan: step 1 is the mechanical move of `shared` (codemod + import rewrite, zero behavior change), verified, before any semantic reshaping. Each step reversible.

---

## Testing this skill

Arch's output is judgment-based, so validate live rather than with automated assertions. Run it on a real repo and check: does ASSESS surface *real* flags with tooling evidence (not generic advice)? Does RECOMMEND pick the right rung and actively resist over-structuring a small app? Does EVOLVE produce a plan that is genuinely reversible and baseline-first? A messy mid-size Next.js app is the ideal test case.
