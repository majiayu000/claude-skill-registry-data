---
name: quality-check-scoped
description: Diff-bounded single-pass quality evaluation for PR review. Classifies every changed path by ARTIFACT TYPE first (runtime code / deployable config / tests / docs-planning / garura prose / ProductOS model / STM evidence / wireframes — pure globs, first match wins), then evaluates standard-ID checks against the diff using mechanical match rules from the PR severity taxonomy — grep-based rules fire only on runtime-code/deployable-config/tests (a keyword in prose is not a security defect, #438); pure path rules respect the same prose guard on prose artifacts unless the matched glob is docs-targeting (#454). Matching runs in a bundled deterministic script (scan_taxonomy.py) — real glob/regex, no inference. Every finding carries artifact_type. Emits findings.yaml. Reuses /quality-check KB data — NOT its 11-subagent execution model. Use only from review-change play; never invoke standalone for full-repo audits.
user-invocable: false
---

# Quality Check (Scoped)

Single-pass diff-bounded evaluation. Reuses the KB used by `/quality-check` but evaluates only standards relevant to files in `changed_paths`. **Diff scope invariant: NEVER reads files outside `changed_paths`.**

## Purpose vs `/quality-check`

| | `/quality-check` | `quality-check-scoped` |
|---|---|---|
| Scope | Full repo | Diff only |
| Execution | 11 parallel subagents | Single deterministic script (`scan_taxonomy.py`) |
| Output | Spider chart + scored audit | `findings.yaml` |
| Invocable | User | Play only (review-pr) |
| KB usage | All standards in all domains | Only standards whose taxonomy match rule fires on the diff |

## Input Contract

The skill is invoked with a JSON payload from `quality-auditor`:

```yaml
diff_path: "{stm_base}/{issue}/evidence/review-pr/diff.patch"   # unified diff
changed_paths:                                                    # array; absolute repo-relative paths
  - src/api/users.ts
  - src/db/migrations/0042_add_email.sql
standards_set:                                                    # resolved from config standards_order
  kb: ~/.garura/core/memory/knowledge/quality/
  ltm: ./.garura/core/memory/knowledge/quality/
  stm: .garura/project/issues/{issue}/specs/quality/
severity_taxonomy_path: ./core/components/memory/standards/rules/pr.md
intent_summary: "Add email verification flow"                     # 1–3 sentences from spec/intent.yaml or PR body
output_path: "{stm_base}/{issue}/evidence/review-pr/findings.yaml"
```

**Pre-flight (hard halts):**

| Check | Action on Failure |
|---|---|
| `severity_taxonomy_path` exists | HALT — "PR severity taxonomy missing at {path}" |
| `diff_path` exists and non-empty | HALT — "Empty or missing diff" |
| `changed_paths` non-empty | HALT — "No changed paths supplied" |
| At least one of `standards_set.{kb,ltm,stm}` resolves | HALT — "No standards source resolvable" |

## Execution

The whole mechanical scan is one deterministic script — `scripts/scan_taxonomy.py` (#454).
It is a real glob/regex engine, **not inference**: the agent runs it and returns its output,
and never hand-matches rules against files. Hand-matching an 800-file diff against a 330-row
table was the old slow path AND the source of loose-substring false positives (a name-glob
`**/schema*` "matching" `finding-schema.md`); a real glob engine makes both problems
structurally impossible.

### Step 1 — Run the scan
Write the contract's `changed_paths` (one path per line) to a file and pass it as `--paths`,
so the scan is bounded by the contract's authoritative list — the Diff Scope Invariant, not a
list the script re-derives:
```
printf '%s\n' "${changed_paths[@]}" > "{working}/changed-paths.txt"
python3 <skill-dir>/scripts/scan_taxonomy.py \
    --taxonomy "{severity_taxonomy_path}" \
    --diff "{diff_path}" \
    --paths "{working}/changed-paths.txt" \
    --out "{output_path}"
```
`--paths` is authoritative when supplied; only when the caller omits it does the script fall
back to deriving `changed_paths` from the diff's own file headers. The added lines used for
`grep:` rules always come from the diff. In one pass the script:

1. **Classifies** every changed path by artifact type — the taxonomy's Artifact-Type
   Scoping table, first-match glob (`garura-prose`, `productos-model`, `stm-evidence`,
   `wireframe`, `tests`, `deployable-config`, `docs-planning`, `runtime-code` default).
2. **Evaluates** every severity row's match rule with real glob/regex:
   - `grep:` / `grep+path:` grep-half — eligible only on the CODE artifact types
     (`runtime-code`, `deployable-config`, `tests`); dropped on any prose type (#438).
   - `path:` / `grep+path:` path-half — on a prose artifact type it fires only when the
     matched glob is docs-targeting; otherwise the match is dropped (#454 prose guard).
   - `CODE-20` `**/*` catch-all — rolled into `meta.catchall.CODE-20` as a single count,
     never per-file findings (#454).
3. **Emits** `findings.yaml` (schema below), stable-sorted, byte-identical across runs.

### Step 2 — Verify and return
Confirm the script exited `0` and `{output_path}` exists. If `meta.errors` is non-empty a
taxonomy row failed to compile (FS-5) — surface it; do not work around it. Return the
`findings.yaml` path to the caller. Do **not** re-derive, re-classify, or "double-check" any
finding by inference — the script's output is authoritative and complete. KB description
files are consulted (via `standards_order`) only when a human reads a finding back, not to
gate emission — the taxonomy row IS the standard.

### Output ordering
`findings.yaml` is written with a stable sort (`severity → file → line → standard_id`), so
two invocations on the same `(diff, taxonomy)` produce byte-identical output bar
`meta.generated_at`.

```yaml
meta:
  generated_at: "{ISO-8601}"
  diff_path: "{diff_path}"
  taxonomy_path: "{severity_taxonomy_path}"
  changed_paths_count: {N}
  scan_coverage: {0.0–1.0}
  standards_relevant: {count}
  catchall:
    CODE-20: {count of files the **/*​ catch-all covered}   # count, not findings (#454)
findings:
  - standard_id: SEC-19
    severity: P1
    file: src/config/secrets.ts
    line: 14
    evidence: 'const apiKey = "sk_live_abc..."'
    artifact_type: runtime-code
    taxonomy_rule_id: SEC-19
  - ...
counts:
  P1: {n}
  P2: {n}
  P3: {n}
  P4: {n}
```

## Output Schema (`findings.yaml`)

| Field | Type | Required | Notes |
|---|---|---|---|
| `meta.generated_at` | string | yes | ISO-8601 |
| `meta.diff_path` | string | yes | echoed from input |
| `meta.scan_coverage` | float | yes | 0.0–1.0 |
| `meta.standards_relevant` | int | yes | count of taxonomy rows whose match rule fired |
| `meta.catchall.CODE-20` | int | yes | count of files the `**/*` catch-all covered — a count, never per-file findings (#454) |
| `meta.errors[]` | list | no | taxonomy rows that failed to compile (FS-5); empty/absent when clean |
| `findings[].standard_id` | string | yes | MUST exist in taxonomy |
| `findings[].severity` | enum P1\|P2\|P3\|P4 | yes | sourced from taxonomy, never inferred |
| `findings[].file` | string | yes | repo-relative path from `changed_paths` |
| `findings[].line` | int | yes | line in the diff hunk |
| `findings[].evidence` | string | yes | matched substring or path |
| `findings[].artifact_type` | enum | yes | from the Artifact-Type Scoping table; grep findings only on `runtime-code`/`deployable-config`/`tests` |
| `findings[].taxonomy_rule_id` | string | yes | same as `standard_id` |
| `counts.P1`–`P4` | int | yes | counts by severity |

## Diff Scope Invariant

The skill MUST NOT:
- Read files outside `changed_paths`.
- Walk the full repository tree.
- Invoke `/quality-check` or any of its subagents.
- Use heuristic/LLM reasoning to classify severity — severity is read from the taxonomy table, not inferred.

## Determinism

Two back-to-back invocations on the same `(diff_path, changed_paths, taxonomy_path)` MUST produce a byte-identical `findings.yaml` (after stripping `meta.generated_at`). Stable sort order: `severity asc → file asc → line asc → standard_id asc`. This is guaranteed by `scan_taxonomy.py` being pure glob/regex — there is no inference step to vary between runs.

## Failure Modes

| Code | Condition | Action |
|---|---|---|
| FS-1 | Taxonomy missing | HALT + structured failure |
| FS-2 | Diff empty/missing | HALT |
| FS-3 | A finding lacks `standard_id` | DROP finding + log error to evidence |
| FS-4 | Standards source unresolvable | HALT |
| FS-5 | Match rule regex invalid | HALT — taxonomy is malformed |

## Reference

- Scanner: `scripts/scan_taxonomy.py` (the deterministic match engine — #454)
- Input contract: `reference/input-contract.md`
- Output schema: `reference/finding-schema.md`
- Taxonomy: `core/components/memory/standards/rules/pr.md`
