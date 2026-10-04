---
name: distill-test-set
description: >
  Turn a large dataset (an existing oversized Coval test set, an export of past
  conversations, or a CSV/JSON of cases) into a small, high-signal Coval test set by
  removing duplicates, identifying unique scenarios, and selecting a representative,
  failure-weighted subset — then bulk-loading it with no row cap. Use when the user
  says "I have thousands of cases", "dedupe my test set", "my test set is too big",
  "turn this dataset into a test set", "pick representative scenarios", or "my CSV
  import only kept 10 / uploaded everything".
argument-hint: "[source-dataset-or-coval-test-set-id]"
---

# Distill Test Set

Turn a large, noisy dataset into a small, high-signal Coval test set. Big datasets are
the wrong input for simulation: running thousands of sims is slow, expensive, and likely
to overwhelm the agent under test, and most rows are duplicates, paraphrases, or
boilerplate. The goal is a **representative 10–50 case suite** that covers the agent's
real scenarios once each, weighted toward known failures.

Drive everything through the `coval` CLI and the bundled `scripts/distill.py`. Follow the
phases in order. Present a summary and get confirmation before creating anything.

If `$ARGUMENTS` is a Coval test set id (8 chars) or a file path, use it as the source in
Phase 1.

> **Why this skill instead of a plain import?** Coval has two loaders, and neither dedupes:
> the CSV/XLSX importer and `coval test-cases create --stdin` load **every** row 1:1
> (great once you've chosen your rows), while "Create test set → attach a file" runs an
> **LLM** that synthesizes only ~10–15 scenarios (a generation cap, not a representative
> sample). This skill does the dedup + representative selection itself, then loads the
> result with the uncapped path.

## Phase 0: Preflight + Inventory

### Step 1: Check authentication
```bash
coval whoami
```
If not authenticated: `coval login` (get a key at https://app.coval.dev/settings → Organization → Manage → API Keys). No account? https://coval.dev.

> **Before you start:** this skill needs only the `coval` CLI and `python3` (used by the
> bundled script and a couple of small JSON reads) — no `jq` or other tools. If `coval` is a
> shell alias on your machine, run the commands with `coval-cli` instead (`which coval` to check).

### Step 2: Inventory existing test sets (so we don't clobber one)
```bash
coval test-sets list --format json
```
Note the ids/sizes. If the user wants to distill an existing Coval test set, confirm its id here.

## Phase 1: Locate + Profile the Source Dataset

Determine where the large dataset lives. Two common cases:

1. **An existing, oversized Coval test set** — use `--source coval:<TEST_SET_ID>` (the script
   pulls every case via the API, paginated). Confirm the id and its size:
   ```bash
   coval test-sets get <TEST_SET_ID> --format json | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('display_name'), d.get('test_case_count') or '(size shown in app)')"
   ```
2. **A local file** — CSV, JSON, or NDJSON of past conversations / SME-reviewed rows / logs.

Then identify the **field mapping** by inspecting a few rows:
- the **user utterance / scenario** field (`--input-field`, default `input_str`)
- the **expected answer / behavior** field (`--expected-field`, default `expected_behaviors`)
- a **label** to stratify by — the intent or route or category (`--label-field`)
- a **pass/fail** field if the data is review-graded (`--pass-fail-field`; values starting with `Pass`/`Fail`)

If the source is a Coval test set whose metadata is packed into a pipe-delimited
`description` (e.g. `journey=… | sub_topic=… | next_agent_status=… | sme_result=…`), add
`--parse-coval-description` so those become usable labels.

Load `references/distillation-method.md` if you need help choosing the field mapping or
understanding what the script does.

## Phase 2: Distill

Run the distiller. It (1) drops rows with no checkable answer, (2) removes exact +
paraphrase duplicates, (3) caps boilerplate-convergence clusters (many different asks
that all hit one generic fallback/greeting) to a small quota, and (4) selects a
stratified, **failure-weighted** subset across your labels and languages.

```bash
python3 scripts/distill.py \
  --source <coval:TEST_SET_ID | path> \
  --parse-coval-description \          # only if labels are in a pipe-delimited description
  --label-field <intent/route field> \
  --pass-fail-field <pass/fail field> \
  --target-size 30 \                   # start small: 10–50
  --min-minority-ratio 0.3 \           # keep ~1/3 of a minority language (e.g. non-English); 0 to disable
  --out distilled.ndjson
```

The script prints a report to stderr — show it to the user:
```
dropped_low_info / boilerplate_groups / scenario_rows_after_dedup /
selected / selected_fail / selected_cjk / selected_by_label
```

- No third-party packages are needed; paraphrase clustering uses a character n-gram
  heuristic by default.
- For higher-quality clustering on multilingual data, set `OPENAI_API_KEY` and add
  `--embeddings on` (it falls back to the heuristic automatically if anything fails).
- Tuning knobs: `--target-size`, `--fail-weight` (default 0.45), `--boilerplate-quota`
  (default 4), `--jaccard-threshold` / `--embed-threshold`. See `references/distillation-method.md`.

## Phase 3: Review + Adjust

Show the user a sample of the distilled set and the label/pass-fail/language breakdown:
```bash
python3 -c "import json;[print('IN :',json.loads(l)['input_str'][:70],'| EXP:',json.loads(l)['expected_output_str'][:60]) for l in open('distilled.ndjson')]"
wc -l distilled.ndjson
```
Ask: "Does this coverage look right? (yes / re-run with different size or weighting / edit the file)"

- Too many fallback/greeting rows → lower `--boilerplate-quota`.
- Want more failure coverage → raise `--fail-weight` or `--target-size`.
- Want to hand-curate → edit `distilled.ndjson` directly (one JSON object per line:
  `{"input_str", "expected_output_str", "description"}`). Keep every line valid JSON — the
  bulk loader stops at the first malformed line, so a stray typo can silently drop the rest.
- Sanity-check coherence → confirm each `expected_output_str` actually answers its
  `input_str`. The distiller preserves whatever input/answer pairing your source had, so any
  misalignment already in the source data carries through (garbage in, garbage out).

**Start small.** A 20–30 case suite you can run and trust beats a 2,000 case suite you
can't. Get the agent passing these, then add a new test set for the next workflow.

## Phase 4: Create the Test Set + Bulk-Load (uncapped)

Create a `SCENARIO` test set and load the distilled cases with `--stdin` — the **uncapped**
path that loads exactly the rows you chose (no 10-case generation limit):

```bash
TS=$(coval test-sets create --name "<Agent> — Representative Suite" --type SCENARIO \
  --description "Distilled from <source>: deduped, failure-weighted representative scenarios" \
  --format json | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")

cat distilled.ndjson | coval test-cases create --test-set-id "$TS" --stdin
```

> `--stdin` reads one JSON object per line (`input_str` required; `expected_output_str`,
> `description` optional) and POSTs one test case per line with **no row cap**. This is the
> fix for "the importer only kept ~10 cases".

> **Note:** `SCENARIO` is the right type for persona-driven eval and is also the CLI default.
> If an older CLI build rejects `--type`, just omit it (you still get SCENARIO).

## Phase 5: Verify + Next Steps

```bash
coval test-cases list --test-set-id "$TS" --page-size 100 --format json | python3 -c "import json,sys;print(len(json.load(sys.stdin)))"
```
Confirm the count matches the distilled file, then show the app link:
`https://app.coval.dev/test-sets/<TS>`

```
What's next?

  Create personas to drive these scenarios:   /design-persona  or  /personas-from-artifacts
  Add expected behaviors / refine cases:       /build-test-suite
  Configure evaluation metrics:                /configure-metrics
  Launch an evaluation on the small set first: /quick-eval

  Iterate: once the agent passes this suite, distill a NEW test set for the next workflow
  rather than growing this one — narrow, branch-covering suites beat one giant set.
```
