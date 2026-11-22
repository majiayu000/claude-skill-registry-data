---
name: split
description: Presentation/Core/Engine split control plane — the canonical entry point for any work decomposing the Yuzu server into three binaries (presentation · core · engine) per ADR-0031-presentation-core-engine-decomposition / ADR-0032 (the admission interlock) / ADR-0033 (access-control spine). Use when the user says "/split", "/pce-split", "/decomposition", asks to plan or implement a split workstream (WS-A*, WS-B*, WS-X*), asks "what's our gap to the presentation/core split" or "is it safe to extract presentation/the engine yet", asks to audit split readiness, or starts work touching the seam (handlers calling stores directly, the INV-31-4 contract test, the Drogon port, `server/presentation` or `server/engine`, the `uce` DB grants, component service identity, or the ADR-0032 admission/grant/audit substrate — `use_case_run_id`, the release log, the capability-declaration registry).
---

# Presentation / Core / Engine split skill

The single entry point for decomposition work. Bundles three things:

1. **The model** — the two axes + the cross-cutting lane, the ADR-0032 interlock
   **standing merge-gate**, and the per-cutover **safe-to-extract gate** (get this
   wrong and a "boundary" ships with a renderer still holding a `Store*`, or an
   engine composes facts core never confined).
2. **The delivery matrix** — every workstream WS-0…WS-X5: what it delivers, which
   axis, owner, dependencies, whether it gates an extraction, routed reviewers, status.
3. **Gap/priority + workflow** — what to build next and the standard procedure.

This skill does NOT replace the ADRs or the matrix. **On any conflict, the ADRs
govern the model and `docs/presentation-core-split-delivery-matrix.md` governs
delivery** — this file is a pointer and loses to both.

⚠️ **Cite ADR-0031 by filename** — the number hosts *two* accepted ADRs
(`0031-presentation-core-engine-decomposition.md` is the split;
`0031-engine-principal-store.md` is the engine RBAC identity). See `docs/adr/README.md`.

⚠️ **Current-state comes from the tree, not the ADR status columns** — the docs go
stale (the first draft of this matrix asserted `authorize_list_read` had "zero
occurrences"; it has 66). Grep before you claim anything is unbuilt.

---

## Usage

```
/split                    # default: print the model + both gates + the matrix, ask which WS to work on
/split audit              # snapshot: which WS are done, is presentation/engine extraction safe yet
/split plan <WS>          # plan-only walk-through for a single workstream (e.g. WS-A4, WS-B11)
/split implement <WS>     # full workflow: plan → governance → implement → test → docs for one WS slice
```

Without a subcommand, default to printing **the model + the two gates + the matrix**
and asking which workstream to work on.

---

## 1. The model — read before sequencing anything

Authoritative: `docs/adr/0031-presentation-core-engine-decomposition.md` (INV-31-1..6,
the 5-step migration) + `docs/adr/0032-use-case-admission-protocol.md` (the interlock)
+ `docs/presentation-core-split-delivery-matrix.md` (delivery). Read them before this
skill claims anything is "done."

### 1a. Two axes + a cross-cutting lane

- **Axis A — logical seam / authority (monolith-OK).** Public versioned API as sole
  authority; every handler/renderer calls the API, never a store pointer; INV-31-4
  contract test; the ADR-0032/0033 confinement + admission + audit substrate. *Makes
  the split correct.* Almost all buildable while one binary.
- **Axis B — physical decomposition.** Drogon + G10, strangler cutover, extract
  presentation, extract engine, state relocation, event spine, component service
  identity, `uce` DB decomposition, supervision, per-binary `/readyz`. *Makes it real.*
- **Lane X — cross-cutting/continuous.** Fan-out measurement, compat contract,
  topology config, split observability, validation harness, credential hardening.

### 1b. ⚠️ The standing merge-gate (ADR-0032 interlock — binds immediately)

**No engine-path code — admits a run, mints a grant, serves a use-case result, or
composes released facts — merges into ANY binary until the unconditional interlock set
(a)–(d)+(h) lands complete** (incl. (h)'s admitting-credential id + frozen grant
snapshot + requesting-credential id). Reference-and-defer is safe for *ownership*,
never for *whether it gates a merge*. Today only (a) is shipped; (c)/(d)/(h) and the
`evaluate_as_operator` seam are absent, and (b) is blocked on **#2665** (the shipped
#1715 confinement is *additive*; interlock (b) needs *deny-precedence*).

### 1c. ⚠️ The safe-to-extract gate (the load-bearing constraint)

The strangler's **first live family cutover** is the extraction moment — not a late
"extract" row. All boundary prerequisites gate *that* cutover, and each subsequent
family. The full clause tables (presentation and engine) live in the matrix doc's
"safe-to-extract gate" section. In one line each:

- **Extract presentation** needs, per family: seam enforced + INV-31-4 test green
  (WS-A4) · that family's public caps (WS-A3) · sessions+replay durable (WS-B3) ·
  event spine on the HA WS-2a outbox (WS-B4) · component service identity (WS-B6) ·
  presentation `/readyz` (WS-B7) · Drogon canary (WS-B1) · K-fanout measured (WS-X1) ·
  compat enforced (WS-X2) · 6a break-glass (WS-X4) · presentation owns no DB (WS-B11) ·
  per-family rollback (WS-B2).
- **Extract engine** additionally needs: presentation already extracted (engine is
  *fifth*) · interlock (a)–(d)+(h) closed + #2665 resolved · (i)(k)(l)(m) · `uce` DB
  isolation (WS-B11) · engine-side grant/input-hash verification.

Miss any and the failure is structural: a `Store*` surviving the boundary, a `/readyz`
green while core is down (INV-31-6), or an engine enlarging authority core never confined.

### 1d. Non-obvious model decisions (survived a three-model adversarial panel)

- **Split ⇎ HA are decoupled, but the split *consumes* HA.** Not a prerequisite for a 2nd replica
  (HA §1c decoupled — ratified by the ADR-1005 owner Dave Rae, 2026-09-07; the agent `Subscribe`
  blocker is gateway-fronting, HA WS-4, not the split). But it *inherits* HA WS-1 (sessions, done),
  rides HA WS-2a's `event_outbox` for the spine, and takes MCP replay durability from HA WS-2b —
  one-way dependencies.
- **Inherit ADR-2002's event spine wholesale** — never a parallel non-durable transport.
  MCP replay durabilizes (ADR-2002 §4/§5 supersedes exec-plan D15d).
- **Capability parity is THIS-owned per-family** (ADR-0031 §3), not deferred to M3
  (M3 is the NVD matcher-parity gate, a different thing).

---

## 2. The delivery matrix — pointer

Source of truth: **`docs/presentation-core-split-delivery-matrix.md`**. Read it before
this skill claims a status. WS-0 (reconciliation + interlock certification) is the
predecessor of everything; Axis A = WS-A1..A6; Axis B = WS-B1..B11; Lane X = WS-X1..X5.
The matrix carries the per-row Owner (THIS vs /auth vs HA vs exec-plan), the
`Gates cutover?` column (P/E), routed reviewers, and a re-stampable "Verified <date>" line.

> **⚠️ Standing instruction — update on close.** Every PR that closes or materially changes a
> workstream's status MUST update that row in `docs/presentation-core-split-delivery-matrix.md`
> **and** re-stamp its Verified line in the SAME PR. A matrix from a stale checkout is worse than
> none — treat status drift as a review-blocking defect.

**Hard invariants that must not regress:** INV-31-1..6 (credential pipe · confine-then-
compose · no cross-component DB · no private core API · service-identity-not-people ·
store-in-readyz), on-behalf-of rejected on every ingress, isolation as-if-remote from
day one, no UI-only capability, the standing merge-gate, and the safe-to-extract gate.

---

## 3. Gap / priority — what to build next

Delivery phases (dependency-ordered):

1. **Phase 0 — Reconcile:** WS-0 + arm the merge-gate. Blocks everything.
2. **Phase A — Seam & authority (monolith):** WS-A1 → WS-A2r, WS-A3 (per-family),
   **WS-A4** (net-new heart), WS-B1 (Drogon canary, parallel), WS-B11 (DB decomposition,
   early), WS-X2, WS-X5 (continuous). WS-A2a + WS-A6 proceed under the merge-gate.
3. **Phase B — Extract presentation:** WS-B2 cutover plane + WS-B3/B4/B6/B7 + WS-X1/X4 +
   WS-B11 → first cutover behind the gate → WS-B8 progressive cutover + httplib
   retirement → WS-B10, WS-X3.
4. **Phase C — Extract engine:** WS-B9 behind the engine gate → WS-B11(engine half) → finalize.

**Highest-leverage first slices after WS-0:** WS-A4's *remaining* work and WS-B1
(Drogon canary) — both monolith-buildable and parallel; WS-B11 is a third early start.
None waits on an external programme now that WS-A3 is THIS-owned per-family.
**⚠️ WS-A4's GLOBAL INV-31-4 drift test already shipped** (out-of-band, #842/#3991/#3992 —
`scripts/ci/check-api-parity.py` + `test_openapi_spec_completeness.cpp`; `/api/vN` drift-zero). It's a
**lexical** tripwire, not a proof (scans `server/core/src/*.cpp` only) — a literal registration absent from
OpenAPI fails the build; a non-literal *direct* verb call warns (exit 0); a helper- or header-defined
registration escapes SILENTLY (#2572). Do NOT rebuild it. WS-A4's remaining slices are the **per-family** seam+contract enforcement (gates
WS-B2), the handler→API seam refactor, and the PII-audit relocation — grep the tree before scoping.

## 4. Landing a WS slice (workflow)

Read the routed doc first (the matrix row names the reviewers and the owning module) →
smallest coherent patch → its tests → `/test` → `/governance <range>` with the named
reviewers. A WS is done only when its safe-to-extract clause (if any) has a passing
WS-X5 validation-harness scenario. WS-0 re-verifies every "pulled" status **against the
tree**, never the ADR status column.
