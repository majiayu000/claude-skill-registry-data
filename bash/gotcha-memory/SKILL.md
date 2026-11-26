---
name: gotcha-memory
description: Operational learning loop — records command failures, detects recurrence and injects the lesson as a preamble before the next execution of the same task. Use to query/seed/debug the project's gotcha memory.
---

> **Auto-Trigger:** When the user asks "why does this always fail?", "what have we already learned about this task?", wants to seed curated rules, or wants to inspect/clean the project's failure memory.
> **Keywords:** "gotcha", "gotchas", "recurring failure", "recurring error", "lesson learned", "failure memory", "preamble", "curated", "rule seed", "operational learning"
> **Priority:** MEDIUM
> **Tools:** Bash, Read

## When NOT to Activate
- Debugging ONE new, one-off failure — this module handles RECURRENCE (>= N identical failures within a window); for the first occurrence, debug normally.
- Managing conversational/semantic memory (session context, RAG) — this module is memory of EXECUTION FAILURES, not of knowledge.

## Contract

**INPUT:** Bash failure events (recorded automatically by the `gotcha_postflight.py` hook) + your curated lessons (YAML/JSONL seed). Config in `gotchas.*`/`paths.gotcha_store` of `operator-profile.yaml`.

**OUTPUT:** `failures.jsonl` + `curated.jsonl` in the store (default `.claude/gotchas/`) and a "⚠️ GOTCHAS" preamble on the preflight's stderr when a lesson matches the task. On `--export-unknown` (step 5), one `hpp.decision-suite/v1` file.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | always (hooks and CLI, except the `--export-unknown` refusal below) — the learning loop never breaks the caller's flow |
| 1 | only in `--self-test` when an assertion fails |
| 2 | only in `--export-unknown` when the output file already exists (it may hold your labels): nothing is written |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `operator-profile.yaml` (`gotchas.*`, `paths.gotcha_store`) | Reads | config (window, min_count, top, store) |
| `<store>/failures.jsonl` | Writes (append) | failure events classified by family |
| `<store>/curated.jsonl` | Reads/Writes (idempotent append) | your always-on rules |
| `<store>/failures*.jsonl` → your suite file | Reads / Writes once (exclusive create; `--export-unknown` only) | offline relabel of `unknown` (step 5) |

## Process
1. **Install the hooks** (via plugin or manual wire — see README): `PreToolUse Bash → gotcha_preflight.py` and `PostToolUse` + `PostToolUseFailure Bash → gotcha_postflight.py`, all `timeout: 30`, WARN-only. The two exit events point to the same script because the host emits `PostToolUseFailure` when Bash fails — the case this memory exists to record.
2. **Seed your rules** (optional, idempotent):
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/_lib/gotchas_memory.py" --seed curated.seed.example.yaml
   ```
3. **Query what the system has learned** about a task:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/_lib/gotchas_memory.py" --preamble "run the site deploy"
   ```
4. **See the whole loop working** (demo with a temporary store, zero effect on the project):
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/_lib/gotchas_memory.py"
   ```
5. **Relabel `unknown` — offline, run by a person** (optional; requires the HPP core, `python -m hpp`).
   A message no family matched stays `unknown`: the hooks never relabel it and never call a decider.
   To find a family worth adding, export the store's `unknown` messages as an `hpp.decision-suite/v1`
   (redacted, secret-shaped ones left out, repeats merged into `count`; the options are the families
   without `unknown`, so an abstention maps back to it), label every case, measure your decider (a
   command that reads `{"question", "state"}` JSON on stdin and prints one `hpp.decision/v1`
   record), and keep its per-message records beside the store:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/_lib/gotchas_memory.py" --export-unknown unknown-suite.json
   # label every case: "expected": "<family>" or "abstain" (an unlabelled case is refused, exit 2)
   python -m hpp decide eval unknown-suite.json --decider-command '["python", "my_decider.py"]'
   STORE=.claude/gotchas                  # or your paths.gotcha_store
   python - unknown-suite.json "$STORE/decisions" '["python", "my_decider.py"]' <<'PY'
   import json, pathlib, subprocess, sys
   suite = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
   out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
   failed = []
   for case in suite["cases"]:
       request = json.dumps({"question": suite["question"], "state": case["state"]}, ensure_ascii=True)
       answer = subprocess.run(json.loads(sys.argv[3]), input=request, capture_output=True, text=True)
       if answer.returncode != 0:  # a failed decider leaves no record behind
           failed.append(case["id"]); print(f"decider failed on {case['id']} (exit {answer.returncode})", file=sys.stderr)
           continue
       (out / (case["id"] + ".json")).write_text(answer.stdout, encoding="utf-8")
   sys.exit(1 if failed else 0)
   PY
   for r in "$STORE"/decisions/*.json; do [ -e "$r" ] || continue; python -m hpp decide validate "$r"; done
   ```
   The export never overwrites its output. The records are advisory: nothing in the kit reads them.
   Trust a decider only after `decide eval` passes on your own labels (selective accuracy, zero
   confident errors, instrument failures counted apart). A new signal enters the family table in
   `${CLAUDE_PLUGIN_ROOT}/_lib/error_strategy.py` only as a code change made by a person, with the
   incident cited in that family's `why` — never from a record.

## Executed examples

The three below were genuinely run (2026-09-19) against a temporary store via
`GOTCHA_STORE_DIR` — zero effect on the project. The output is the real one, with the store
path abbreviated to `<store>`.

**1 · Seed the curated rules (first time):**

```
$ GOTCHA_STORE_DIR=<store> python "${CLAUDE_PLUGIN_ROOT}/_lib/gotchas_memory.py" --seed curated.seed.example.yaml
Seeded 5 curated gotchas into <store>/curated.jsonl
$ echo $?
0
```
<!-- executed: 2026-09-22 · exit=0 -->

**2 · Seed the SAME file again — the idempotency proof:**

```
$ GOTCHA_STORE_DIR=<store> python "${CLAUDE_PLUGIN_ROOT}/_lib/gotchas_memory.py" --seed curated.seed.example.yaml
Seeded 0 curated gotchas into <store>/curated.jsonl
```
<!-- executed: 2026-09-22 · exit=0 -->

Zero, not five again: re-seeding does not duplicate. That is what allows leaving the seed in a
project's setup and running it in every session.

**3 · Query what the system knows about a task:**

```
$ GOTCHA_STORE_DIR=<store> python "${CLAUDE_PLUGIN_ROOT}/_lib/gotchas_memory.py" --preamble "run the site deploy"
⚠️ GOTCHAS (do not repeat these — learned from earlier failures):
  • [rule] Deploy/routing: prove the BACKEND changed (a route exclusive to the new version + a build marker), not just the auth gate or the process status.
$ echo $?
0
```
<!-- executed: 2026-09-22 · exit=0 -->

The rule that appeared is a **curated** one (seeded in example 1) — it matched by substring
on "deploy". A **learned** lesson (from recurring failures) would appear in the same list
with the `[Nx]` counter in front.

## Proof

```bash
python "${CLAUDE_PLUGIN_ROOT}/_lib/gotchas_memory.py" --self-test     # -> self-test OK ✓  · exit 0
python "${CLAUDE_PLUGIN_ROOT}/_lib/error_strategy.py" --self-test     # -> self-test OK    · exit 0
python "${CLAUDE_PLUGIN_ROOT}/hooks/gotcha_preflight.py" --self-test  # -> self-test OK
python "${CLAUDE_PLUGIN_ROOT}/hooks/gotcha_postflight.py" --self-test # -> self-test OK
```

The four self-tests cover: classification by family (with word boundary —
an isolated `ENOTFOUND` is network, `ModuleNotFoundError` is dependency), recurrence that becomes a
gotcha after `min_count` failures within the window, seed idempotency, the hooks'
conservative detection (ambiguous = not a failure), and the relabel export (only `unknown`,
secret-shaped left out, an existing output never overwritten).

**Operational success criterion:** after 3 identical failures recorded in < 24h,
`--preamble "<same task>"` returns a non-empty preamble with `[3x]`.

## Known failures / limits
- Failure detection is CONSERVATIVE: only exit code != 0, `is_error: true` or a non-empty `error` field count. A "silent" failure (exit 0 with wrong output) is not captured — by design (it does not invent failures).
- Covers only the Bash tool (the hooks' matcher). Other tools would require new matchers.
- YAML seed requires PyYAML; without PyYAML, use a `.jsonl` seed (stdlib).
