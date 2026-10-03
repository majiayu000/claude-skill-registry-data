---
name: graduate
layer: stack
description: Turn a proven POC into a real, crouton-native, documented package(s) + a consuming app — the deliberate "step back and rebuild" checkpoint. SPEC-DRIVEN — the POC discovers a behaviour spec (captured at each sign-off), graduation freezes it as authoritative, the app is rebuilt the crouton way to satisfy it, and nothing is done until it's checked + signed off against two gates (experience + crouton-conformance). Use when a `pocs/*` app is proven and "done", or asked to "graduate this poc", "make it a real app", "extract the package".
allowed-tools: Read, Grep, Glob, Bash, mcp__github__issue_read, mcp__github__issue_write, mcp__github__sub_issue_write, mcp__github__add_issue_comment, mcp__github__list_issues, mcp__github__search_issues, mcp__github__get_label
---

# Graduate — turn a proven POC into real, crouton-native packages + an app

A POC (`pocs/*`) is an **incubator**: messy, heavily-iterated, safe-to-fail code built to
*discover the right shape* against a real use case (`pocs/CLAUDE.md`). Graduation is the
deliberate moment that proven shape becomes a real product. The output is **an app AND one
or more packages** — the app is the proving consumer; the **packages are the durable value**.

**Order matters: `incubator → launched → shared` (`AGENTS.md` *Stages*).** The **app is a
first-class milestone, signed off *before* extraction** — you rebuild the proven behaviour as a real
app and get both acceptance axes (C1 experience + C2 conformance) signed off, and *then* extract the
settled parts into packages as a deliberate later move. The package is **extracted from the proven
app**, never written first and never a prerequisite for the app. (If the spike already *grew* a
shared package instead of just *consuming* one — as the layout engine did during the builder spike,
#1175 — that's stage-inversion debt: note it, don't repeat it. A spike consumes shared packages; it
does not add shared surface. New capability is built in the app, then extracted.)

## The model — spec-driven graduation

> **The POC *discovers* the spec → graduation *freezes* it as authoritative → the app is
> rebuilt *the crouton way* to *satisfy* it → two gates (experience + conformance) → not done
> until checked + signed off.**

This inverts textbook spec-driven on purpose: you build a POC precisely *because you don't know
the spec yet*. So in the POC the code leads and the spec is **emergent**, captured one entry at a
time at each "ok this works" (the `/spec` ledger — see `pocs/CLAUDE.md`). **Graduation is the moment
the spec flips from discovered to authoritative**: now the spec leads and the code is the
regenerable output, rebuilt clean to serve it.

**A POC is a floor, not a ceiling — graduation is not a 1:1 port.** A POC *proves the core exists*;
it deliberately leaves directions, options and additions open, and it *fakes* whatever wasn't the
point (data, persistence, auth). So the graduated app is a **superset** of the POC, sorted into three
buckets — only the first is governed by the side-by-side comparison:

| Bucket | What it is | Signed off by |
|---|---|---|
| **Preserve** | the proven, signed-off POC experience — the contract | **C1 side-by-side** vs the live POC |
| **Replace** | a POC stopgap/fake → the real crouton thing (demo blocks → real collections · ephemeral state → persistence) | C1 (same behaviour) + conformance (real impl) |
| **Add** | completeness the POC left open that a *real* app needs (collections + CRUD, persistence, auth/team scope, empty/error/loading states, edge cases) | the **normal new-behaviour gates** (`/schema-review`, `/ui-proposal`, `/test-review`) — **not C1**, there's no POC to compare |

The trap is treating graduation as "make the app equal the POC": that under-builds (skips the
**Add** bucket a real app needs) *or* over-preserves (ports the **Replace** fakes forward). Name each
behaviour's bucket up front (the revision plan, A2) so the right gate governs it.

**Three invariants (read these before touching anything):**

1. **Preserve experience · revise architecture · clean code.** The POC is the *baseline*.
   - **Experience** (the signed-off behaviour/feel) is the **contract** — study the POC closely and
     reproduce it. *"Don't port" means don't copy the CODE — it never meant build a different UX.*
     Building fresh-from-imagination and losing the signed-off feel is the #1 failure (#988).
   - **Architecture** (how it's built) is **deliberately revised** — that revision *is the work of
     graduating*. Copying the spike forward = zero architecture revision = none of the actual work.
   - Every **divergence** in either layer is a *deliberate, recorded, re-signed* decision (the
     revision plan, stage A2) — **never silent drift.** Drift dressed up as "improvement" after the
     fact is the trap; the legitimacy comes from deciding + signing off *up front*.
2. **The comparison is the gate, not the list.** A written spec can't be certified exhaustive (gaps
   are invisible on a list). The real verdict comes from **POC and app open side-by-side, the same
   inventory walked on both** — the spec is the *walk script*, the live POC is the *expected result*.
3. **Done = a spec entry checked + concretely signed off.** No proxy is "done" — not a green build,
   not a deploy URL, not the agent's own confidence (every one of those lied during #988). Status is
   *derived* from a recorded `lgtm <id>`, never self-asserted.

**Two acceptance axes — a graduated app needs BOTH, both signed off:**

- **Experience** — matches the signed-off spec (the side-by-side comparison, stage C1).
- **Crouton-conformance** — it's a *real crouton app*: CLI-scaffolded · real collections · consumes
  the correct packages (**doesn't reinvent what a package provides**) · passes `frontend-review` +
  `a11y` + `typecheck` + `e2e-smoke` · docs updated (stage C2).

This skill does **not** auto-merge or auto-deploy. It drives the rebuild under the existing gates.

## When to run

- A `pocs/<name>` is proven and the owner calls it "done" (the shape has settled, worth reusing).
- The code has accreted across many iterations — the worst outcome would be copying it into `apps/`.

If the POC is still being explored, it's **too early** — say so and stop.

---

## Stage A — Freeze the spec (before handoff)

### A0. The spec ledger is the experience contract
**If the POC captured specs at sign-off** (the `/spec` ledger convention, `pocs/CLAUDE.md`), that
ledger **is the frozen spec** — no reconstruction needed; go straight to A1 to reconcile it once.

**If the POC predates the convention (retrofit, one-time tax):** reconstruct the spec from
`HANDOFF.md` + `changelog.json` + the spike code + the planted `data-handoff` hooks. This is *lossy*
— a reconstructed list can't be certified exhaustive — so lean harder on the comparison gate (C1) and
the live POC as ground truth. **Draft every reconstructed entry as `status: proposed`** — proven in
the POC but not yet reconciled in graduation, so it has an honest home that isn't the frozen contract
(and the sign-off hook won't let it pose as `settled` yet). The **human verifies it against the running
POC and signs off** (you usually can't reach the live POC from a sandbox — draft, they own the check).

### A1. Reconcile the spec against the running POC (gate)
Drive the running POC and sort behaviour into three buckets — **confirmed** (works as the spec says
✅) · **contradicted** (spec says X, app does Y → fix until they agree) · **undocumented** (the app
does it, the spec doesn't mention it → add or consciously drop — the unknown-unknowns a checklist
misses). Drive what's drivable; code-confirm gesture states honestly. Wherever a state is hard to
locate, plant a stable `data-handoff` hook and name it on the spec entry — that hook is the shared
vocabulary the rebuild reproduces, so the same walk runs on POC *and* app. **Each confirmed entry
flips `proposed` → `settled` with the recorded `signedOff`** (the retrofit drafts; A1 is where the
human sign-off makes them the contract). Entries you'll deliberately change become `stopgap`/`new`.

> Needs an environment that can actually run the POC. A sandbox that kills dev servers / blocks the
> preview URL can't do A1 — the human drives; you draft and reconcile from artifacts.

### A2. Revision plan — bucket every behaviour + record every divergence (sign-off)
Three short plans, all signed off *before* building. First **bucket each behaviour** (Preserve /
Replace / Add) so the right gate governs it, then:
- **Architecture revision** — per spec entry (or globally) the clean crouton-native HOW, naming the
  POC shortcut it replaces (demo blocks → real collections · overlay-measured handles → the package's
  renderer · ephemeral state → real persistence). This is the **Replace** bucket.
- **Experience revision** — which `settled` spec entries we'll *deliberately do differently* and why
  (a `stopgap` entry is *expected* to change; a `settled` entry is the contract). These become the
  *expected* diffs in C1; everything else unexpected there is a bug.
- **Additions** — what the real app must **Add** that the POC left open (a POC is a floor, not a
  ceiling): real collections + CRUD, persistence, auth/team scope, empty/error/loading states, the
  edge cases a demo skips. Each lands as a `status: new` spec entry and is signed off through its
  **own** new-behaviour gate (`/schema-review`, `/ui-proposal`, `/test-review`) — *not* C1, since
  there's no POC expected-result to compare. Don't let "preserve the POC" quietly cap the app here.

### A3. Data model — real collections (sign-off)
Decide the real **collections** (`crouton config` → `/schema-review` #314 → generate). The collections
ARE the data model the app exists to compose — backend-free demo blocks are a POC crutch, not the app.

### A4. Walking skeleton — boot it first (checkpoint)
`crouton init` the app the crouton way + the real collections, **deploy, and confirm it boots** before
building any behaviour. A CLI scaffold is correct-by-construction — this kills the green-build/runtime
-500 class (missing `server/db/schema.ts` etc., #988) on something tiny instead of after building
everything. **Tag a checkpoint** here.

### Open the graduation epic
Per `github-tasks`: a hypothesis-framed **epic** + a **sub-issue per package + the app**, labelled by
target. The POC's epic is the *input*; this is the *output*. Reference the spec ledger/brief.

---

## Stage B — Build the crouton way, to satisfy the spec (handoff)

**Build the app as a real crouton app — CLI-scaffolded, never hand-assembled, never a copy of the
POC.** Hand-assembly silently omits standard scaffold (and 500s at runtime on a green build, #988);
copying `spike-*` re-imports the POC's workarounds and skips the architecture revision. If you catch
yourself `cp`-ing POC files into the app, **stop.**

For each `packages/*` unit:

0. **Survey the target package FIRST.** Read what it already provides (types · validators · utils ·
   storage · tested helpers) so you build *on* it, not *over* it — re-scope to the **genuine gap**,
   reuse the rest, record the re-scope on the issue. (#983 WS4: serialisation was narrower than
   briefed because the sanitiser + bridge + storage already existed.)
1. **Hand-written package logic → test-first** (`/test-review`, the #774 gate): the spec entry's
   behaviour becomes the failing test, signed off, built to green. The app **consumes** the package —
   it must not reinvent what the package provides (DRY; a conformance check, C2).
2. Reproduce the **`data-handoff` hooks** from the spec so the C1 walk runs identically on both apps.
3. Respect the `packages/` edit gate, `pnpm typecheck`, and the data-model / UI gates
   (`/schema-review` #314, `/ui-proposal` #307).

---

## Stage C — Verify against both gates, then promote (after handoff)

### C1. Experience gate — side-by-side comparison (Preserve + Replace only)
Open the **POC and the rebuilt app together** and walk the **Preserve + Replace** entries (`status:
settled` / `stopgap`) **entry by entry** on both: same inventory (palette · gestures · the
`data-handoff` hooks · each entry's how-to-test). Every difference is triaged — **same** (preserved
✅) · **intentionally different** = a logged A2 decision (✨ ✅) · **unexplained** = drift/regression
(🐛 fix). The gate passes at **zero unexplained differences**, and each entry is **checked + signed
off** (`lgtm <id>`). The spec is the walk; the live POC is the expected.

> **Add** entries (`status: new`) are **not** walked here — there's no POC to compare. They were signed
> off through their own new-behaviour gate at A2/B (`/schema-review`, `/ui-proposal`, `/test-review`).
> C1 certifies the app didn't *lose* the POC; the new-behaviour gates certify what it *added*.

### C2. Crouton-conformance gate (sign-off) → run `/conformance`
Run the **`/conformance`** skill against the app — it owns the full checklist (the single source of
truth) and renders it as a required, signed-off gate. It certifies the app is a *real crouton app*:
- **CLI-scaffolded** (`crouton init`), not hand-built — `server/db/schema.ts` present (the #988 500)
- **Real collections** (`crouton config` → generate), not stub blocks
- **Consumes the correct packages** without reimplementing what they provide (DRY — the key check)
- passes **`/frontend-review`** + **`/a11y`** + **`pnpm typecheck`** + **`/e2e-smoke`**
- **docs updated** — package/app `CLAUDE.md`; new package ⇒ `node scripts/gen-package-catalog.mjs` + `pkg:*` label

`/conformance` composes the existing probes and holds on `status:blocked` until a human signs off this
axis. (C1 above is the *experience* axis — the side-by-side; C2 here is the *conformance* axis.)

### Done, checkpoints, promote
**Done = both axes signed off** — never one, never a proxy. **Tag a checkpoint** at every signed-off
state (skeleton boots · each spec group passes C1 · conformance green) so any step rewinds in one
command. Then promote `pocs/<name>` → `apps/<name>` (or a fresh app) under the `apps/` rules + `/deploy`;
retire the POC (`/remove-app`) once it supersedes; run `/postmortem` at epic close.

---

## What you hand back

- The **frozen, signed-off spec** (the `/spec` ledger, or the reconstructed-and-signed retrofit) +
  `writeups/briefings/<name>-graduation-brief.md`.
- A graduation epic + sub-issues (one per package + the app), hypothesis-framed.
- The **revision plan** (architecture + experience divergences, signed off).
- Both gates green and signed off (experience C1 + conformance C2), with checkpoint tags.

## Conventions

Defers to the **root `CLAUDE.md`** / `AGENTS.md` for workflow/commit/issue conventions (ISSUE-FIRST,
`/commit`, no-squash, the `packages/` edit gate, test-first #774, **done = a checked + signed-off
spec entry**). Reuses `/conformance` (the C2 gate), `/postmortem`, `/test-review`, `/schema-review`,
`/ui-proposal`, `/frontend-review`, `/a11y`, `/e2e-smoke`, `/deploy`, `/remove-app`, and the `/spec`
capture (`pocs/CLAUDE.md`). This skill *orchestrates* that checkpoint — it doesn't replace any of them.
