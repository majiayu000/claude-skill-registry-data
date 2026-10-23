---
name: gz-obpi-sync
persona: main-session
description: Use to reconcile OBPI briefs and the ADR table against the ledger and report what only the operator can resolve.
category: obpi-pipeline
compatibility: GovZero v6 framework with OBPI briefs
metadata:
  skill-version: "3.4.1"
  govzero-framework-version: "v6"
  govzero-author: "GovZero governance team"
  skill-type: "orchestrator"
  govzero_layer: "Layer 1 - Evidence Gathering"
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: sonnet
---

# gz-obpi-sync

## Purpose

**OBPI reconciliation for one ADR** — audit each brief against actual evidence,
reconcile each brief and the ADR table **from the ledger**, and report the
drift that reconciliation cannot and must not fix.

This skill is the unified OBPI verification surface. It consolidates two skills
retired at ADR-0.0.36 closeout: a Layer 1 evidence-gathering skill and a Layer 3
ADR-table-sync skill. Both were deleted per the delete-on-retire policy in
`.gzkit/rules/skill-surface-sync.md`; the table-sync predecessor happened to
carry this skill's present slug, which is why the pre-consolidation names are
described here rather than cited. The `gz obpi sync` verb absorbed the same two
(GHI #641) and is this skill's reconciliation step.

**The direction is ledger → brief, never evidence → brief.** Completion evidence
is the ledger (`AGENTS.md` § Behavior Rules); a brief's `status:` is a derived
view. Passing tests do not complete an OBPI: completion is `gz obpi complete`
with the operator's Gate 5 attestation, in every lane (ADR-0.0.36), and only the
operator initiates it. This skill never marks a brief Completed by hand and
never edits a brief's body.

This skill ensures:

1. Each brief is audited against actual evidence (tests, coverage, `@covers` tags)
2. An audit log entry records each audit
3. Each brief's frontmatter and the ADR OBPI table agree with the ledger
4. Evidence-complete OBPIs the ledger does not show as completed are reported
   to the operator, not "fixed"

**Use when:** Before closeout ceremony, after completing work, periodic housekeeping,
or any time brief status might have drifted from reality.

### Common Rationalizations

These thoughts mean STOP — you are about to skip evidence-backed verification:

| Thought | Reality |
|---------|---------|
| "The briefs look correct, reconciliation is unnecessary" | Brief status drifts silently. Only evidence-backed auditing reveals the actual state. |
| "Tests pass so the OBPI is complete — I'll set the brief to Completed" | Tests verify code behavior. Completion is a ledger event carrying the operator's attestation; report the OBPI as ready and stop. |
| "I'll update the ADR table manually instead" | Manual table updates bypass the ledger. `gz obpi sync` derives the row from it. |
| "One brief is still in progress, I'll reconcile the rest later" | Partial reconciliation creates inconsistent snapshots. Run for the full ADR. |
| "The audit log already has entries from a previous audit" | Stale entries do not reflect current evidence. Each reconciliation writes fresh ones. |
| "Coverage is close to 40%, I'll round up" | The threshold is fail-closed. 39.9% is FAIL, not "close enough." |

### Red Flags

- A brief's `status:` edited by hand, in either direction
- ADR OBPI table shows "Completed" for an OBPI the ledger does not show completed
- Audit entries are older than the most recent code changes to OBPI-scoped files
- Agent updates the ADR table directly instead of running `gz obpi sync`
- A `completed` or `validated` receipt emitted by the agent on audit evidence alone

---

## Trust Model

**Layer 1+2+3 — Full Stack:** This tool verifies evidence (L1), reads the ledger (L2), and reconciles derived state from it (L3).

- **Reads:** Code, tests, coverage reports, brief files, ledger
- **Writes:** Audit log entries (`{adr-dir}/logs/obpi-audit.jsonl`, through `gz obpi audit`); brief frontmatter and the ADR OBPI table (through `gz obpi sync`, from ledger-derived state)
- **Verifies:** Tests pass, coverage meets threshold, `@covers` tags present
- **Does NOT write:** completion or validation receipts; brief bodies

---

## Invocation

```text
/gz-obpi-sync ADR-0.0.19
/gz-obpi-sync 0.0.19
```

---

## Workflow Phases

```text
╔══════════════════════════════════════════════════════════════════════╗
║  PHASE 1: AUDIT (Layer 1 — Evidence Gathering)                       ║
║  gz obpi audit --adr ADR-X.Y.Z                                       ║
║  Locates tests, runs them, measures coverage, evaluates criteria,    ║
║  appends one audit log entry per brief.                              ║
╠══════════════════════════════════════════════════════════════════════╣
║  PHASE 2: RECONCILE (Layer 2 → Layer 3)                              ║
║  gz obpi sync OBPI-X.Y.Z-NN   (once per brief)                       ║
║  Brief frontmatter and ADR table row follow ledger-derived state.    ║
╠══════════════════════════════════════════════════════════════════════╣
║  PHASE 3: REPORT                                                     ║
║  What was reconciled, what blocked, and which OBPIs are evidence-    ║
║  complete but not completed in the ledger (operator's to initiate).  ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## Procedure

### Phase 1: Audit Each Brief

**Goal:** Establish what the evidence shows, independent of any status field.

Use `gz obpi audit` as the deterministic evidence step — it locates tests,
runs them, measures coverage, evaluates criteria, and appends the
`obpi-audit` entry in one call (`obpi_audit_cmd._build_entry`).

```bash
# Audit all OBPIs for an ADR in one pass
uv run gz obpi audit --adr ADR-X.Y.Z

# Audit a single OBPI
uv run gz obpi audit OBPI-X.Y.Z-NN

# JSON output for programmatic consumption
uv run gz obpi audit OBPI-X.Y.Z-NN --json
```

**Phantom OBPI remediation:** If Phase 1 surfaces an OBPI that exists in
the ledger graph (via `obpi_created` event) but has no on-disk brief file,
`gz obpi withdraw` cleans it from the graph. Both withdraw and supersede are
witnessed transitions (a `human_attested` witness per the OBPI-01 state
machine): surface the case and run the verb on the operator's word, recording
the operator as `g0` (`AGENTS.md` § Execution Rules):

```bash
uv run gz obpi withdraw OBPI-X.Y.Z-NN --reason "phantom entry from promotion" --attestor "g0"
```

**Superseded-OBPI remediation:** When a reconciled OBPI has been replaced by
another that carries its intent forward (not merely retired), record the
replacement lineage with `gz obpi supersede` rather than a bare withdraw —
the superseding OBPI id is preserved on the graph node:

```bash
uv run gz obpi supersede OBPI-X.Y.Z-NN --by OBPI-X.Y.Z-MM --rationale "replaced by redesigned brief" --attestor "g0"
```

**Output:** Each brief audited; one audit log entry per brief.

### Phase 2: Reconcile from the Ledger

**Goal:** Brief frontmatter and the ADR OBPI table agree with the ledger.

```bash
uv run gz obpi sync OBPI-X.Y.Z-NN
```

Run it once per brief. It is fail-closed: it rewrites the brief's frontmatter
status to the ledger-derived runtime state, reconciles the receipt and the ADR
table row, and exits non-zero with its blockers when they cannot be made to
agree. Do not hand-edit what it reports; read the blocker, and surface it.

**Output:** Derived state matches the ledger, or a named blocker per OBPI.

**Receipts are the operator's.** A reconcile never emits a receipt on audit
evidence. `completed` and `validated` are human-attestation events: relay one
only when the operator has attested that OBPI in words, recording them as `g0`:

```bash
uv run gz obpi emit-receipt OBPI-X.Y.Z-NN --event validated --attestor "g0" --evidence-json '<evidence>'
```

### Phase 3: Report

**Goal:** Provide a human-readable summary, including what is the operator's.

```markdown
## ADR-X.Y.Z Reconciliation Report

**Timestamp:** <ISO-8601>

### Ledger state

| State | Count | Briefs |
|-------|-------|--------|
| Completed | 5 | 01, 02, 03, 04, 05 |
| Not completed | 4 | 06, 07, 08, 09 |

### Reconciled

| Brief | Before | After | Source |
|-------|--------|-------|--------|
| OBPI-03 | Draft | Completed | ledger (`gz obpi sync`) |

### Evidence-complete, not completed in the ledger

| Brief | Audit | Next (operator's) |
|-------|-------|-------------------|
| OBPI-06 | 5/5 PASS | initiate completion through `gz-obpi-pipeline` |

### Blockers

| Brief | `gz obpi sync` blocker |
|-------|------------------------|
| (none) | |

### Audit log

Location: `{adr-dir}/logs/obpi-audit.jsonl`
Entries written: 9
```

---

## Agent Execution Contract

When this skill is invoked, the agent MUST:

1. **Execute phases sequentially** — no skipping
2. **Audit before reconciling** — evidence is read before derived state moves
3. **Run tests before claiming PASS** — no assumptions
4. **Reconcile only through `gz obpi sync`** — never hand-edit a brief's status or the ADR table
5. **Report all findings** — even if no changes made
6. **Stop on blocking errors** — don't proceed if tests fail

### Error Handling

| Error | Action |
|-------|--------|
| Brief not found | Skip, report as missing (see Phantom OBPI remediation) |
| Tests fail | Log failure; report, change nothing |
| Coverage < 40% | Log gap; report, change nothing |
| `gz obpi sync` exits non-zero | Stop on that OBPI, report its blockers verbatim |

---

## Lane-Aware Audit

| Lane | Criteria to Verify |
|------|-------------------|
| **Lite** | Tests pass, coverage ≥40% |
| **Heavy** | Lite + BDD scenarios + docs/manpage updated |

Read the lane from the brief's `lane:` frontmatter. Gate 5 attestation applies
to completion in both lanes; it is not something an audit can supply.

---

## Audit Log Aggregation

```bash
# Count audited briefs (substitute the ADR directory)
wc -l docs/design/adr/<kind-dir>/ADR-X.Y.Z-slug/logs/obpi-audit.jsonl

# Summary by result
jq -r '.criteria_evaluated[].result' docs/design/adr/<kind-dir>/ADR-X.Y.Z-slug/logs/obpi-audit.jsonl | sort | uniq -c
```

---

## Related Skills

| Skill | Role in Workflow |
|-------|------------------|
| `gz-obpi-specify` | Creates the briefs this skill audits |
| `gz-obpi-pipeline` | Runs `gz obpi sync` at Stage 5; owns completion |
| `gz-obpi-lock` | Coordinates multi-agent access to briefs |
| `gz-adr-audit` | Gate 5 closeout (uses reconcile for evidence) |
| `gz-adr-sync` | ADR-level reconciliation and full governance sync (Layers 1-3) |

---

## Audit Log Schema (v1)

**Location:** `{adr-dir}/logs/obpi-audit.jsonl` — an audit log beside the ADR,
not the project ledger (`.gzkit/ledger.jsonl`).

`gz obpi audit` appends one JSON line per brief (`obpi_audit_cmd._build_entry`
is the authority for the fields):

```json
{
  "type": "obpi-audit",
  "timestamp": "ISO-8601",
  "obpi_id": "OBPI-X.Y.Z-NN",
  "adr_id": "ADR-X.Y.Z",
  "brief_status_before": "<brief status>",
  "brief_status_after": "<brief status>",
  "lane": "Lite|Heavy",
  "evidence": {
    "tests_found": ["path/to/test.py"],
    "tests_passed": true,
    "test_count": 10,
    "coverage_percent": 46.05,
    "coverage_threshold": 40,
    "covers_tags": ["@covers ADR-X.Y.Z"]
  },
  "criteria_evaluated": [
    {"criterion": "text", "result": "PASS|FAIL", "evidence": "location"}
  ],
  "action_taken": "none",
  "agent": "cli",
  "session_id": null
}
```

**Guarantees:** Append-only, one line per audit, machine-readable.

---

## When to Run

| Trigger | Reason |
|---------|--------|
| Starting work on ADR | Baseline current state |
| Before closeout ceremony | Ensure all briefs accurate |
| After multi-agent session | Catch paperwork drift |
| Weekly housekeeping | Periodic hygiene |
| CI pre-merge | Governance gate (optional) |
| Pipeline Stage 5 | Post-implementation verification |
