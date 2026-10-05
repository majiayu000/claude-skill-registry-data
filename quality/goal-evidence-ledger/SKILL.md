---
name: goal-evidence-ledger
description: "Maintain the append-only evidence ledger: `.flow/runs/<run-id>/evidence/*.evidence.yaml` sidecars plus matching `.txt` raw captures, written only via `bin/flow-record-evidence.sh`. Use when goal-evaluator runs a verification command, when /flow:start or /flow:address captures verification evidence on a FlowRun, or when /flow:goal evaluate produces a judge report. Evidence that lives only in the transcript dies with the session; only file-backed, schema-validated sidecars prove ACs durably and satisfy the judge's Independence Protocol."
allowed-tools: Bash, Read, Write
context: fork
agent: general-purpose
---

# Goal Evidence Ledger

## Contract

Iron law: no AC transitions to `pass` without a FlowEvidence sidecar whose `proves: [<AC.id>]` names it, and every non-trivial sidecar declares what it does NOT prove. Invoked by `goal-evaluator` (Step 2, once per verification command), by `/flow:start` Phase 4 and `/flow:address` (verification-evidence sidecars on the FlowRun), and by `/flow:goal evaluate` for judge reports. Inputs: evidence id, type, proves list, and optional command, exit code, raw-output path, limitations, negative cases. Returns the sidecar path, which the caller sets as the AC's `evidence_ref`. Permitted skips: `limitations` on `holdout_validation` and `verdict` types; the raw `.txt` when nothing was captured. The helper is never skipped.

## Inputs

1. **Evidence id** — `evidence-<AC.id>-<descriptor>-<turn>`; lowercase, digits, `_-`.
2. **Evidence type** — one of `evidence.schema.json`'s enum: command_result, test_result, lint_result, runtime_smoke_result, visual_result, git_diff, holdout_validation, verdict, human_approval, review_comment_snapshot, ci_status, llm_judge_report, artifact_check, path_boundary_check.
3. **Proves** — AC ids this evidence supports.
4. Optional: `command`, `exit_code`, raw output path, `limitations`, `negative_cases`.

## Outputs

1. `.flow/runs/<run-id>/evidence/<evidence-id>.evidence.yaml` (schema `plugins/flow/schemas/v1/evidence.schema.json`).
2. `.flow/runs/<run-id>/evidence/<evidence-id>.txt` — raw stdout/stderr when captured, beside the sidecar. Both files are named from the id lower-cased, with any character other than a-z, 0-9, `_` and `-` made `-`; an id is at most 200 characters.
3. An `evidence-captured` journal artifact.
4. One line appended to `.flow/runs/<run-id>/events.jsonl`.

## Workflow

### Step 1: Compose

```yaml
apiVersion: flow.synapti.ai/v1
kind: FlowEvidence
metadata:
  id: <evidence-id>
  goal: <goal-id>
  run_id: <run-id>
  activity_id: <activity-id, if any>
  created_at: <ISO-8601 UTC>
evidence:
  type: <enum-value>
  command: <bash command, if applicable>
  exit_code: <captured, if command type>
  # output_ref: leave it out; with --raw-output, flow-record-evidence.sh sets it to the copy's name, relative to this sidecar's directory (evidence-ac1-test.txt for the id evidence-ac1-test)
  proves:
    - <AC.id>
  limitations:
    - <what this evidence does NOT prove>
  negative_cases:
    - <adversarial or boundary cases exercised>
```

### Step 2: Negative space

| Evidence type | Required |
|---|---|
| `command_result`, `test_result`, `lint_result`, `visual_result`, `llm_judge_report` | `limitations` |
| `runtime_smoke_result` | `limitations` + `negative_cases` |
| `holdout_validation`, `verdict` | none — the verdict format owns its negative space |

The schema rejects a `command_result` without `limitations` at write time.

### Step 3: Write

```bash
bin/flow-record-evidence.sh --run-id <run-id> --evidence-file <composed.yaml> [--raw-output <stdout-capture>]
```

The helper writes atomically (tempfile + rename via `_journal_atomic.py`), refuses symlinked targets and lockfiles, validates the schema when `jsonschema` is installed, and copies the raw output next to the sidecar, setting the sidecar's `output_ref` to the copy's name; it refuses a sidecar whose `output_ref` names another file, and an id already recorded (a correction is a new id). It copies the raw output whole and synced before it writes the sidecar, so a refused or short copy leaves neither, and a sidecar that cannot be written takes its copy away again; once the sidecar is written, the copy stays; of two overlapping records of one id, the second is refused (exit 2). Surface any non-zero exit with its stderr: exit 1 is the arguments or the evidence (fix them and record again), exit 2 the repository, the run, an existing record or the system (too many open files, an I/O error).

### Step 4: Journal

```bash
bin/journal-record.sh --issue {N} --type evidence-captured --metadata evidence_id=<id> --metadata goal_id=<goal-id> --metadata proves=<comma-list of AC ids>
```

### Step 5: Link

The caller updates the AC in `.flow/goals/<id>.goal.yaml`: `status: evidence_collected`, `evidence_ref: .flow/runs/<run-id>/evidence/<evidence-id>.evidence.yaml`, `last_evaluated_at: <now>`.

## Rules

- Evidence is append-only: a correction is a new sidecar (`evidence-AC1-retest-turn2`) and the AC's `evidence_ref` moves to it; the old sidecar stays as audit trail.
- One run proving two ACs is one sidecar with `proves: [AC1, AC2]`.
- Capture evidence before the verdict; never after the goal is `achieved`.
- Never write a sidecar with `echo >`; the helper is the only writer.

## References

- `plugins/flow/skills/evidence-based-development/SKILL.md` — the ASSERTION/EVIDENCE/VERIFIED discipline this ledger materializes.
- `plugins/flow/references/evidence-bundle-format.md` — the bundle layout the judge consumes.
