---
name: gz-adr-audit
persona: pipeline-orchestrator
description: Use for an ADR's Gate-5 audit; provides the audit templates and procedure.
category: adr-audit
compatibility: GovZero v6 framework; provides audit procedure for COMPLETED→VALIDATED ADR transition
metadata:
  skill-version: "6.15.1"
  govzero-framework-version: "v6"
  govzero-author: "GovZero governance team"
  govzero-spec-references: "docs/governance/GovZero/charter.md, docs/governance/GovZero/audit-protocol.md"
  govzero-gates-covered: "Gate 5 (Human Attestation)"
  govzero_layer: "Layer 2 - Ledger Consumption"
  trust_model: "Trusts Layer 1 ledger proof for mechanical checks; re-verifies the ADR thesis via the bound fidelity gate (ADR-0.0.73) — gz adr fidelity RUNS the Decision's assertions against the running system"
gz_command: audit
invocation: uv run gz audit <adr-id>
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: opus
---

# gz-adr-audit

Execute reproducible ADR verification to move from COMPLETED → VALIDATED.

## Persona

**Active driver:** `pipeline-orchestrator` — read `.gzkit/personas/pipeline-orchestrator.md` and adopt its behavioral identity before executing this skill. The audit is a sequenced ceremony (verify proof → reproduce → run the fidelity gate); step-discipline and ceremony-completion are not rules to follow — they are who you are while running it.

## Persona Dispatch

The audit is read-only judgment work — a single driver scoring its own findings is the optimistic-bias failure mode `spec-reviewer`'s anti-traits literally name. Dispatch the following personas as independent subagents to produce the evidence the driver synthesizes:

| Persona | Function in this ceremony | Invoked at |
|---|---|---|
| `spec-reviewer` | Independent requirement-tracing against ledger proof; verifies each OBPI's claimed REQ coverage holds against a fresh read of brief and tests | Steps 1–2 (Verify Ledger Proof, Reproduce Key Evidence) |
| `quality-reviewer` | Independent assessment of the ADR package's structural coherence: do the OBPIs cohere into the ADR's claimed capability, or is the integration brittle? | After Step 2, before Step 3 |
| `narrator` | Frames the Step 4 audit documentation (AUDIT.md) in operator-value terms; the Step 3 fidelity gate is now bound and runs itself — no prose value-demonstration to compose | Step 4 (Document) |

Personas not dispatched: `implementer` (no code written in this ceremony — if audit reveals a defect requiring code, file a GHI via `/ghi-author` and route to a fresh OBPI brief, never spawn an implementer inside the audit).

**This ceremony has no artifact channel for these dispatches** — they are unattested and undisclosed (GHI #770's named residual), and the receipt machinery that would record them is not yet authored (GHI #846; `ADR-pool.obpi-pipeline-dispatch-attestation` is Superseded into ADR-0.0.73, which delivered no receipts). Treat the mandate as binding on you, not as something a gate will catch.

Persona doctrine reference: ADR-0.0.11-persona-driven-agent-identity-frames (Validated).

### Common Rationalizations

| Thought | Reality |
|---------|---------|
| "All OBPIs passed individually, the ADR is obviously complete" | Individual OBPI completion doesn't prove ADR-level integration. The audit verifies the whole. |
| "Tests pass and coverage is met, the audit is done" | That's verification, not fidelity. Step 3 (Fidelity Gate) runs the ADR's thesis against the running system, not just its tests. |
| "The closeout ceremony already covered this" | Audit and closeout invoke the same bound fidelity gate; running one satisfies the other's fidelity step. Mechanical checks (Step 1-2) are still independent. |
| "Ledger entries exist from a previous audit, I can skip re-verification" | Check staleness. Entries older than 7 days or predating code changes require fresh verification. |
| "This is a Foundation ADR, the audit can be lighter" | Foundation ADRs run the same fidelity gate. The thesis is held against the running system. |

### Red Flags

- AUDIT.md contains only mechanical checkmarks without a Fidelity Gate section
- Agent marks ADR as VALIDATED without running `uv run gz adr report` to confirm lifecycle change
- Audit proofs directory is empty or contains only pass/fail text without actual command output
- Fidelity assertions so generic they could apply to any ADR
- Validation receipt emitted before all shortfalls are resolved

---

## Layer 2 Trust Model

This is a **Layer 2** tool — it consumes proof from the ledger rather than re-running verification commands.

**Trust Chain:**

1. **Layer 1 tools** (`gz-obpi-sync`, the OBPI pipeline) run tests, check coverage, validate evidence
2. **Layer 1 writes proof** to the ledger as OBPI completion and receipt events
3. **This tool reads proof** (`gz adr audit-check`) — if all briefs show PASS/Completed, skip re-verification
4. **Gate 5 attests** to the presence of proof, not re-execution

**Why trust the ledger?**

- Re-running tests in Layer 2 duplicates Layer 1 work
- Gate 5's job is to verify *proof exists*, not regenerate proof
- Human attestation observes artifacts, not re-executes them

**When to force re-verification:**

- If ledger entries are older than 7 days (staleness threshold)
- If you suspect ledger corruption or tampering
- If Layer 1 tools have been updated since last audit

In these cases, run `uv run gz audit <adr-id>` first to regenerate ledger proof.

---

## Assets

- `assets/AUDIT_PLAN.template.md` — Plan scaffold (scope, checks, risk focus)
- `assets/AUDIT.template.md` — Annotation shell (✓/✗/⚠, summary, attestation)

---

## Audit Procedure

**Prerequisite:** ADR is COMPLETED (all briefs done, tests/coverage/docs pass).

### 1. Plan

Each Bash invocation starts a fresh shell, so do NOT export shell
variables across calls. Inline the full ADR directory path in every
command so each Bash call is self-contained. Substitute the real ADR
directory (e.g. `docs/design/adr/foundation/ADR-0.0.16-foo-slug`) for the
placeholder below.

```bash
mkdir -p docs/design/adr/<kind>/ADR-x.y.z-slug/audit/proofs
```

- Read ADR prose, extract all claims
- Create `audit/AUDIT_PLAN.md` with checks for each claim
- Run `uv run gz cli audit` for governance issues
- Legacy note: `docs/design/audit/**` remains historical only; new audits live under the ADR folder.

### 2. Verify Ledger Completeness

Before running any commands, check ledger proof:

```bash
uv run gz adr audit-check <adr-id>
```

**If ledger is complete (all briefs PASS):**

- Skip to Step 3 (Fidelity Gate) — no re-verification needed
- Trust the Layer 1 proof the ledger carries
- Record "Ledger proof verified" in audit notes

**If ledger is incomplete or missing:**

Audit-check failure has two causes that look identical at the CLI but require
opposite remediation. Diagnose before editing:

- **(a) Genuinely missing coverage** — no test asserts the flagged REQ's
  semantics. Remediation: author a REQ-derived test (per the Red→Green→Refactor
  rhythm in `.gzkit/rules/tests.md` § Red-Green-Refactor), then decorate it with
  `@covers(REQ-X.Y.Z-NN-MM)`. Re-run `uv run gz audit <adr-id>` to write fresh
  ledger entries, then return to Step 2.
- **(b) Coverage-shape drift** — a test exists but pins an obsolete output
  string or asserts a shape the REQ did not mandate. Remediation: re-derive the
  assertion from the OBPI brief's REQ semantics per `.gzkit/rules/tests.md`
  § Red-Green-Refactor (**Tests assert semantics, not strings**).
  **Backfilling a cosmetic `@covers` decorator without re-deriving the
  assertion is the forbidden anti-pattern** — it silences `gz adr audit-check`
  while leaving the semantic gap intact.

After remediation, re-run `uv run gz audit <adr-id>` to write fresh ledger
entries, then return to Step 2.

**Force re-verification (optional):**

If you need to regenerate proof (staleness, suspicion, etc.), run the validation commands:

Inline the full ADR directory path, as in Step 1:

```bash
uv run gz test > docs/design/adr/<kind>/ADR-x.y.z-slug/audit/proofs/unittest.txt 2>&1
uv run mkdocs build --strict > docs/design/adr/<kind>/ADR-x.y.z-slug/audit/proofs/mkdocs.txt 2>&1
uv run gz closeout <adr-id> --dry-run > docs/design/adr/<kind>/ADR-x.y.z-slug/audit/proofs/gates.txt 2>&1
```

Record ✓/✗/⚠ outcomes for each check.

### 3. Fidelity Gate (MANDATORY — bound, replaces prose Demonstrate Value)

**An audit that only verifies mechanical checks (tests pass, coverage met) without holding the ADR's thesis against the running system is incomplete.**

This step is a **bound, runnable gate**, not prose: the audit ceremony invokes the SAME standalone fidelity gate the closeout ceremony invokes (one gate, two consumers — `gzkit.fidelity.assert_fidelity_for_ceremony`). `gz audit` runs it automatically; you do not narrate it.

**What the gate does:**

```bash
uv run gz adr fidelity <ADR-ID>
```

It parses the ADR Decision's `## Fidelity Assertions` block and RUNS each assertion's command against the committed tree — a detached worktree at HEAD, so uncommitted files cannot satisfy it and its commands cannot write to the live checkout; no buildable worktree fails closed (GHI #1156) — comparing observed vs expected exit. A failed assertion **blocks the audit** (exit 3) before any validation receipt is written — a red thesis cannot record a false `validated`.

**Absence policy (graceful migration, OBPI-0.0.73-04):** an ADR that carries no `## Fidelity Assertions` block is **flagged with a warning** (the prose 'Demonstrate Value' step is gone — absence is surfaced, not papered over with agent prose) but does not hard-block the in-flight audit. Hard presence-enforcement lives at ADR closeout (ADR-0.0.73 Boundary Invariant #4) and the new-ADR template. The back-fill of fidelity blocks onto already-VALIDATED ADRs is a separate forced sweep.

**Authoring duty:** if the ADR under audit has no block yet, author a `## Fidelity Assertions` table (claim / command / expected-exit rows that exercise the ADR's thesis) before closeout — do not substitute prose.

**Relationship to closeout ceremony:** both ceremonies invoke the identical gate, so running one satisfies the other's fidelity step. There is no separate prose demonstration to write in either path.

### 4. Document

Populate `audit/AUDIT.md` with:

- **Fidelity Gate** section (from Step 3 — each assertion's claim, command, expected vs observed exit, pass/fail)
- Execution log (✓/✗/⚠ per check)
- Evidence index (links to proof files)
- Summary table (completeness, integrity, alignment)

### 5. Identify Shortfalls

Review for:

- Incomplete implementations (claimed features not shipped)
- Misalignments (code ≠ docs ≠ tests)
- Missing or failing fidelity assertions (the thesis never held against the running system)
- Unexplained anomalies

### 6. Remediate

For each shortfall:

- Severity (blocking/non-blocking)
- Proposed fix
- Effort estimate

Implement fixes, re-validate, update `AUDIT.md`.

### 7. Mark VALIDATED

When all shortfalls resolved:

- Complete `AUDIT.md`; the operator's acceptance in Step 8 is the attestation — the agent does not sign for them
- The ADR's lifecycle moves through the Step 8 receipt, never by hand-editing its status

### 8. Emit Validation Receipt (agent-relayed via audit-begin/audit-end)

After a successful audit the agent emits the validated receipt. The
operator's verbatim audit acceptance, relayed via the `--evidence-json`
`attestation_text` field, IS the Gate-5 attestation — there is no TTY
`ATTEST` gate. The `gz adr audit-begin` / `gz adr audit-end` pair brackets
the audit ceremony as a distinct operator moment. Steps:

1. **Open the ceremony.** `uv run gz adr audit-begin <adr-id>` — writes
   the per-ADR co-presence marker at
   `.claude/plans/.pipeline-active-<adr-id>.json`. The marker is
   written by the gzkit CLI itself, not by hand; the slash-command
   entry-point chain (operator typed `/gz-adr-audit` → skill ran
   `audit-begin`) is the legitimate co-presence proof the runtime
   accepts.
2. **Operator verbal attestation.** Wait for the operator's verbal
   ack — `accept audit` or `verify audit`. This is the ADR
   audit-validation acceptance, **not** OBPI Gate-5 closeout (which
   already happened on each linked OBPI; by the time `/gz-adr-audit`
   runs, every linked OBPI is `attested_completed` in the ledger).
   The audit ceremony is a distinct operator moment — accepting the
   audit's verification of the integrated ADR (ledger proof complete,
   fidelity gate ran, no shortfalls remain) — and wants its
   own phrasing so the ledger's `attestation_text` field is
   self-documenting. The verbal ack IS the Gate-5 human-attestation
   event; the agent relays it into the ledger receipt.
3. **Emit the receipt.**

   ```bash
   uv run gz adr emit-receipt <adr-id> --event validated \
     --attestor "g0" \
     --evidence-json '{"gate":5,"tests_passed":true,"tests_count":...,
                       "scope":"<adr-id>","date":"<YYYY-MM-DD>",
                       "attestation_text":"<operator verbatim ack> — <agent enrichment>"}'
   ```

   The receipt records `evidence.attestation_type=operator-verbatim-conversational`
   from the `attestation_text` field — the operator's verbatim acceptance is
   the Gate-5 attestation.

4. **Close the ceremony.** `uv run gz adr audit-end <adr-id>` —
   removes the marker. Marker hygiene matters: leaving it behind
   would let a second emit succeed without a fresh operator
   invocation, defeating the co-presence proof.

**Rules:**

- **Audit fails → no receipt.** Only emit after all shortfalls are
  resolved.
- **Attestor field is `g0`** — never the operator's real name and never
  their personal email (`AGENTS.md` § Execution Rules, Operator PII). Do
  not use `agent:<model-id>` — `validated`/`attested`/
  `accepted` are human-attestation events and the ledger receipt
  records the operator on whose behalf the agent is relaying.
- **Marker hygiene.** Always pair `audit-begin` with `audit-end`.
  If the emit fails for any reason, still run `audit-end` so the
  next ceremony starts clean.
- **Do not hand-write the marker.** Use the `gz adr audit-begin` CLI
  verb — hand-fabricating the marker file bypasses the ceremony
  entry-point.
- **Idempotent:** Running twice produces two ledger entries (audit
  trail preserved).

### 9. Verify Lifecycle Update

**MANDATORY.** After emitting the receipt, confirm the lifecycle change took
effect before declaring success:

```bash
uv run gz adr report <adr-id>
```

The Lifecycle column MUST show `Validated`. If it still shows `Completed`,
the audit is not done — investigate why the state did not propagate. Do not
report success to the operator until the report command confirms the change.

**Recommended evidence fields:**

| Field | Type | Description |
|-------|------|-------------|
| `gate` | int | Gate number (e.g., 5) |
| `tests_passed` | bool | Whether unit tests passed |
| `coverage_pct` | float | Coverage percentage |
| `briefs_completed` | int | Number of briefs completed |
| `shortfalls_resolved` | int | Number of shortfalls fixed |

---

## Validation Commands

| Type | Command | Layer |
|------|---------|-------|
| **Ledger check** | `uv run gz adr audit-check <adr-id>` | L2 |
| **Ledger check (JSON)** | `uv run gz adr audit-check <adr-id> --json` | L2 |
| ADR lifecycle summary | `uv run gz adr status <adr-id> --json` | L1 |
| Unit tests | `uv run gz test` | L1 |
| Docs build | `uv run mkdocs build --strict` | L1 |
| Governance | `uv run gz cli audit` | L1 |
| Config paths | `uv run gz check-config-paths` | L1 |
| Heavy gates | `uv run gz closeout <adr-id> --dry-run` | L1 |
| OBPI reconcile | `uv run gz audit <adr-id>` | L1+L2 |
| Coverage discovery | `uv run gz covers <adr-id>` | L1 |
| **Open audit ceremony** | `uv run gz adr audit-begin <adr-id>` — writes per-ADR co-presence marker. | L1 |
| **Emit receipt** | `uv run gz adr emit-receipt <adr-id> --event validated --attestor "g0" --evidence-json '{...,"attestation_text":"<operator verbatim ack>"}'` after operator's verbal `accept audit` / `verify audit` (NOT OBPI-closeout `attest completed`). | L2 |
| **Close audit ceremony** | `uv run gz adr audit-end <adr-id>` — removes marker. | L1 |

**Layer key:** L1 = runs verification, L2 = reads ledger proof

**When to run evidence checks:**

- Before marking an ADR Completed/Validated
- During CI checks for a target ADR
- Before `gz closeout`, `gz attest`, or `gz audit`
- Before the closeout ceremony (`/gz-adr-closeout-ceremony`)

---

## Gate Checklist

**COMPLETED (Phase 1):**

- [ ] All features shipped
- [ ] Unit tests pass, coverage ≥40%
- [ ] Docs complete, mkdocs builds clean
- [ ] Linting/formatting/type checks pass

**VALIDATED (Phase 2):**

- [ ] Audit plan created
- [ ] All checks executed with proofs
- [ ] **Fidelity gate passed** — the ADR's assertions ran against the running system
- [ ] No unresolved ✗ failures
- [ ] Code matches documentation
- [ ] Examples are executable
- [ ] Validation receipt emitted to ledger
- [ ] Operator's audit acceptance relayed verbatim in the receipt
- [ ] **Lifecycle verified** — `uv run gz adr report <adr-id>` shows Validated

---

## Failure Modes

- **Mechanical-only audit** — tests pass and coverage met but the ADR's thesis is never held against the running system. The human cannot assess value from a checklist of green checkmarks alone.
- Audits drift from template structure
- No proof artifacts captured
- Shortfalls not remediated before marking VALIDATED
- Audit skips Step 3 (Fidelity Gate) and jumps straight to documentation

---

## Relationship to Closeout Ceremony

`gz-adr-audit` and `gz-adr-closeout-ceremony` are **complementary but independent**:

| Concern | gz-adr-audit | gz-adr-closeout-ceremony |
|---------|-------------|--------------------------|
| **Focus** | Evidence verification + bound fidelity gate | Human-witnessed runbook walkthrough + bound fidelity gate |
| **Mode** | Agent-driven with human attestation | Human-driven with agent presenting |
| **Outputs** | AUDIT.md + proofs/ + ledger entries | Closeout form + attestation record |
| **Fidelity gate** | Step 3 (`gz adr fidelity`, bound) | EXECUTE→ATTESTATION edge (same gate, bound) |

**Both invoke the same bound gate** (`assert_fidelity_for_ceremony`) — one gate, two consumers. Running either ceremony exercises the ADR's `## Fidelity Assertions` against the running system; there is no separate prose value-demonstration to write or duplicate.
