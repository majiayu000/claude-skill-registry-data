---
name: jade-core-change-collector
description: >-
  Collects Java version breaking-change rules from user-supplied sources. Uses
  LLM reading comprehension to extract rules from fetched text — never regex.
  A schema-validating write_manifest.py enforces evidence, confidence, and
  format. If all sources fail, halts with AWAITING_SOURCE_INPUT.
when_to_use: >-
  Use when the orchestrator reaches MANIFEST_READY phase, or when the user says
  "collect breaking changes", "produce change manifest", "gather java version
  diffs". Requires user-supplied source list (URLs, file paths, or local KB files).
arguments: [artifacts_dir]
argument-hint: "[path to artifacts directory]"
allowed-tools: Bash(python *) Read Write
---

# JADE Change Collector — LLM-as-Extractor

## Objective

Produce `artifacts/01-breaking-changes-manifest.json` where every rule is extracted
by the agent's reading comprehension from actual fetched source text. Never regex.
Never fabricate.

## Strict-mode constraint

**It is forbidden to emit a rule unless the agent read it directly from a fetched
source file.** Every rule must cite a `source_label` and `evidence_ref` that the
agent just read. Confidence scores below `0.7` MUST NOT appear in the manifest.

---

## Required input

- `artifacts/00-run-config.json`
- User-supplied source list (URLs, file paths, or local `.md` KB files)

---

## Produced artifacts

| Artifact | Purpose |
|----------|---------|
| `artifacts/01-source-index.json` | Every source with fetch status, snippet, hash |
| `artifacts/01-source-content-{label}.txt` | **Clean, readable text** extracted from each source — the LLM reads THIS |
| `artifacts/01-source-fetch-errors.json` | Written only when **all** sources fail |
| `artifacts/01-breaking-changes-manifest.json` | Final rule list, schema-validated |
| `artifacts/01-evidence-map.json` | Rejected candidates, extraction notes |
| `artifacts/01.5-precision-sample-{rule_id}.json` | Deterministic rank-ordered pattern-hit sample (precision gate, opt-in) |
| `artifacts/01.5-precision-verdicts-{rule_id}.json` | Agent's TRUE/FALSE_POSITIVE/UNDECIDABLE judgments — the only hand-written file in the precision gate |
| `artifacts/01.5-precision-report.json` | Scored precision per rule, with Wilson interval and counterexamples |
| `artifacts/PRECISION_ACTION_REQUIRED.md` | Written only when a rule needs a pattern rewrite, a larger sample, or a human decision |

---

## Workflow

### Phase A — Source Ingestion

1. Read `artifacts/00-run-config.json` to obtain `run_id` and `artifacts_path`.
2. Accept the user's source list. Sources are URLs, local files, or KB paths.
3. For each source, invoke `scripts/fetch_source.py`:

```
python scripts/fetch_source.py \
  --run-config artifacts/00-run-config.json \
  --source-url "<URL_OR_PATH>" \
  --source-label "<HUMAN_READABLE_LABEL>"
```

The script:
- Fetches URL content (handles 200, 404, timeout, paywall detection)
- Strips HTML tags to produce **clean readable text**
- Writes `artifacts/01-source-content-{label}.txt`
- Updates `artifacts/01-source-index.json`

**If zero sources succeed** (all 404/timeout/paywall): write `01-source-fetch-errors.json`,
set `AWAITING_SOURCE_INPUT` in `00-run-state.json`, and halt.

### Phase B — LLM Extraction (the agent does this)

**The agent MUST NOT invent rules from prior knowledge.** Every rule MUST come from
text the agent explicitly read.

1. **Read each source file** with the `Read` tool:
   - Read `artifacts/01-source-content-{label}.txt`
   - Scan for breaking changes between `source_version` and `target_version`
   - Identify rule candidates: new language features, deprecated APIs, removed components, behavioral changes

2. **For each candidate rule, cite evidence:**
   - `evidence_ref` — `source-label::line-range` (e.g., `mock-sources::lines 15-28`)
   - `evidence_hash` — SHA-256 from `01-source-index.json` for that source

3. **Build a JSON array of rules.** Each rule MUST have:
   - `id` — unique ID, e.g., `GENERICS_UPGRADE`, `LOOP_MODERNIZATION`
   - `name` — human-readable name
   - `fix_strategy` — `"recipe:jade-recipe-{version}-{id}"` format
   - `severity` — `HIGH`, `MEDIUM`, `LOW`, `WARNING`, `INFO`
   - `category` — `LANGUAGE_CHANGE`, `API_REMOVAL`, `DEPRECATION`, `BEHAVIOR_CHANGE`, etc.
   - `match_pattern` — valid regex to find instances in source
   - `patterns[]` — array with `{type: "regex", pattern, target_extensions, reason, confidence}`
   - `evidence_ref`, `evidence_hash`, `confidence` (0.7–1.0)
   - `verification_hint` — how to confirm the fix was applied correctly

4. **Save the rules to a temp JSON file:**
```bash
python -c "
import json
rules = [...]  # your extracted rules
json.dump(rules, open('artifacts/01-extracted-rules.tmp.json', 'w'), indent=2)
"
```

### Phase C — Validate and Write

1. Invoke `write_manifest.py` with the temp file:

```
python scripts/write_manifest.py \
  --input artifacts/01-extracted-rules.tmp.json \
  --artifacts-dir artifacts/ \
  --run-id <run_id> \
  --source-version <source_version> \
  --target-version <target_version>
```

2. `write_manifest.py` validates:
   - Every rule has required fields (`id`, `name`, `severity`, `patterns`)
   - Every rule has `evidence_ref` and `evidence_hash` (Anti-Hallucination gate)
   - `confidence >= 0.7`
   - `fix_strategy` starts with `"recipe:"`
   - `match_pattern` compiles as valid regex
   - No duplicate `rule_id` values
   - `severity` and `category` are valid values

3. If validation fails → print errors, exit 2. DO NOT proceed with invalid manifest.
4. If validation passes → `01-breaking-changes-manifest.json` is written atomically.

---

### Phase D — Pattern-Precision Sampling (only when `precision_gate.enabled` is true)

When `00-run-config.json` carries an enabled `precision_gate` block, the manifest is
not final at the end of Phase C — a garbage pattern (one that matches the right
syntax shape but almost never the actual construct the rule describes) must be
caught **before** the knowledge graph is built and the scanner injects
`// JADE-FLAG:` comments into the workspace, not after. This phase runs entirely
inside the same `MANIFEST_READY` agent pause as Phases A-C; there is no separate
pipeline stop for it.

For **each** rule in the just-written manifest:

1. Sample the rule's population of regex hits:
```
python scripts/sample_pattern_hits.py \
  --run-config artifacts/00-run-config.json \
  --rule-id <rule_id>
```
   This writes `artifacts/01.5-precision-sample-<rule_id>.json` — a deterministic,
   rank-ordered sample computed via the scanner's own file-collection logic (never
   re-implemented), so the sample's population is provably identical to what
   `scan_and_tag.py` would flag. The script never touches the workspace.

2. **Read every hit** in the sample artifact and judge it against one question only:

   > For each hit, answer one question: is what the pattern caught on this line the
   > construct that `rule_description` describes? You are not judging whether it
   > needs fixing, or whether the change is risky. You are judging only whether the
   > pattern caught what it claims to catch.

   Record one verdict per `hit_id` — `TRUE_POSITIVE`, `FALSE_POSITIVE`, or
   `UNDECIDABLE` — each with a `reason` (>= 20 characters). A `FALSE_POSITIVE`
   verdict additionally requires a `false_positive_class`: `NOT_THE_CONSTRUCT`,
   `RIGHT_CONSTRUCT_WRONG_CONTEXT`, `ALREADY_COMPLIANT`, `COMMENT_OR_STRING`,
   `TEST_ONLY`, `GENERATED_CODE`, or `OTHER`.

3. Save the verdicts to `artifacts/01.5-precision-verdicts-<rule_id>.json` — the
   **only** artifact in this phase the agent writes by hand:
```json
{
  "schema_version": 1,
  "rule_id": "<rule_id>",
  "sample_artifact": "01.5-precision-sample-<rule_id>.json",
  "sample_hash": "<sha256 of the sample artifact file>",
  "verdicts": [
    {"hit_id": "...", "verdict": "TRUE_POSITIVE", "reason": "..."},
    {"hit_id": "...", "verdict": "FALSE_POSITIVE", "false_positive_class": "NOT_THE_CONSTRUCT", "reason": "..."}
  ]
}
```

### Phase E — Scoring and Manifest Injection

1. Score every rule that has both a sample and a verdicts artifact:
```
python scripts/score_pattern_precision.py --run-config artifacts/00-run-config.json
```
   This writes `artifacts/01.5-precision-report.json`. There is deliberately no
   `--min-precision` or `--sample-size` flag — the threshold and sample floor come
   only from `00-run-config.json#precision_gate`, so the agent cannot dodge a low
   score by passing a laxer flag. Exit code `1` means at least one rule needs
   attention (see `artifacts/PRECISION_ACTION_REQUIRED.md`, written only when that
   happens); exit `2` means the verdicts violated the contract in step D2/D3 and
   **no report was written** — fix the verdicts file and re-run.

2. If a rule comes back `REJECTED`, `INCONCLUSIVE`, or `ABANDONED`, read
   `PRECISION_ACTION_REQUIRED.md` and act on `next_action`:
   - `REWRITE_PATTERN` — rewrite `pattern`/`patterns[]` in
     `01-extracted-rules.tmp.json` using the report's `counterexamples` and
     `false_positive_classes`, increment `pattern_revision`, and repeat from
     Phase C (`write_manifest.py`) → step D1 → step D2 → step D3 → step E1. Each
     pattern rewrite draws an independent new sample (the seed mixes in the
     pattern text), so previous verdicts are never silently carried over to a
     changed pattern.
   - `ENLARGE_SAMPLE` — re-run step D1 with the larger `--sample-size` the report
     suggests; nested sampling means already-judged hits keep their `hit_id`, so
     only the newly-added hits need fresh verdicts.
   - `REJUDGE_WITH_MORE_CONTEXT` — re-run step D1 with a larger `--context-lines`,
     then re-judge.
   - `HUMAN_DECISION` (rule hit `max_revisions`) — this is not the agent's call:
     either drop the rule from the manifest or ask the user for an explicit
     `precision_gate.overrides` entry (`reason` + `approved_by`).

3. Re-run `write_manifest.py`, now pointed at the report, to fold the score into
   the final manifest:
```
python scripts/write_manifest.py \
  --input artifacts/01-extracted-rules.tmp.json \
  --artifacts-dir artifacts/ \
  --run-id <run_id> \
  --source-version <source_version> \
  --target-version <target_version> \
  --precision-report artifacts/01.5-precision-report.json
```
   `01-extracted-rules.tmp.json` itself must **never** contain a `pattern_precision`
   or `queue_eligible` key — those are script-computed only and get rejected as
   `FORGED_PRECISION` if present. The resulting manifest carries
   `pattern_precision` (value, status, judged/true_positive/false_positive/
   undecidable, Wilson interval, counterexamples) and `queue_eligible` per rule,
   sourced only from the validated report.

4. Resume the orchestrator exactly as in Phase C — it re-validates the manifest at
   `MANIFEST_READY`, then walks the (now non-pass-through) `PRECISION_GATE_READY`
   gate, which re-checks the report against the manifest before sealing it and
   moving on to `TOOLING_SCOUT_READY`.

---

## Halt conditions

| Condition | Action |
|-----------|--------|
| All sources failed | Write `01-source-fetch-errors.json`, set `AWAITING_SOURCE_INPUT`, halt |
| Agent cannot extract any rule from sources | Write empty manifest (rules: []), note in evidence map |
| `write_manifest.py` validation fails | Fix extracted JSON, re-run Phase C |

---

## Constraints

1. Never fabricate a rule from model priors — evidence MUST be in the read text.
2. `confidence` rated by the agent based on source quality:
   - Official JLS/Oracle docs → 0.90–1.0
   - Secondary sources → 0.75–0.85
   - Ambiguous wording → DON'T extract (reject it)
3. `fix_strategy` always uses `recipe:` prefix to enable the dispatcher.
4. `evidence_hash` must match a hash from `01-source-index.json`.
5. The agent writes the extracted rules to a temp file, then `write_manifest.py`
   validates and saves — the agent never directly writes the manifest.
