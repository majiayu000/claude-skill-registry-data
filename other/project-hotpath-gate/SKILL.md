---
name: project-hotpath-gate
description: "Use when a project needs its hot-path gate configuration established or updated - the canonical config at .thrum/hotpath-gate.json defining trigger directories, per-concept detection patterns, and incident prose for the coordinator-hotpath-merge-gate skill. Detects every language present in the repo and drives detection off the shared reliability-class library, so the generated config is real for Go, Python, JS/TS, Rust, or any mix. First invocation generates from project inspection; subsequent invocations reconcile against current project state and propose diffs."
---

# Project Hot-Path Gate

## Canonical path

`.thrum/hotpath-gate.json` — the single authoritative location.
`coordinator-hotpath-merge-gate` reads from this path only.

## Run modes and dispatch order

On every invocation, dispatch in this order. Earlier branches short-circuit
later ones.

1. **First-run** (config absent) — generate a new `.thrum/hotpath-gate.json`
   from project inspection. Optionally accept seeded prose context (incident
   descriptions, fix patterns) from the invoker.
2. **Re-run-unchanged** (config present, matches current project state) — report
   "hotpath-gate.json is current; no changes needed" and exit without writing.
3. **Re-run-evolved** (config present, project has drifted) — compute a
   sectional diff, present for approval, write only on confirmation.

Load the /thrum:generator-idempotency-protocol skill and follow it.

> **Note: human-in-the-loop required.** This skill uses interactive prompts for
> first-run incident-prose seeding and re-run-evolved diff approval. It cannot
> run unattended in CI.

## First-run mode

Triggered when `.thrum/hotpath-gate.json` does not exist.

### Step 1: Census the repo's languages

Detect every language present — a repo can carry more than one:

- Manifest files at the repo root or in each workspace: `go.mod` (Go),
  `package.json` (JS/TS), `pyproject.toml`/`requirements.txt`/`setup.py`
  (Python), `Cargo.toml` (Rust).
- `git ls-files` extension histogram, as a cross-check and as the sole signal
  where no manifest exists in a subtree.
- A language is detected when it has a manifest, or its tracked-file share
  clears 5%.

Record every detected language as `languages_detected`. A repo clearing the
threshold for more than one language is polyglot: every detected language's
probe pack runs in Step 3, not just the largest one.

### Step 2: Detect trigger directories

Scan for hot-path code using each detected language's own route/handler/RPC
idiom:

```bash
# Go
grep -rlE 'func Handle|func.*Handler|http\.Handle|rpc\.' --include='*.go'
# Python
grep -rlE '@app\.(route|get|post|put|delete|patch)|@router\.' --include='*.py'
# JS/TS
grep -rlE "app\.(get|post|put|delete|patch)\(|router\.(get|post|put|delete|patch)\(" --include='*.ts' --include='*.js'
```

Also scan for projection/writer, storage/DB, sync, and listener/boot
directories, using each language's own idiom for those shapes (a database
open call, a background sync loop, a process-boot entrypoint). Collapse
subdirectories under their parent when the parent already matches. Record the
deduplicated list as `trigger_directories`.

### Step 3: Walk the reliability class library

Read `../project-philosophy/resources/reliability-class-library.md`, shared
with `project-philosophy`. Walk every class tagged `Consumers: ... hotpath` —
each names the lens it feeds and, where relevant, a hot-path facet within that
lens.

For each such class and each language recorded in `languages_detected`, run
the probe the library gives that class for that language, scoped to that
language's own files within `trigger_directories` from Step 2 — a language
with no hot-path directories of its own contributes no findings, even if it
clears the repo-wide detection threshold. Where the library marks a language
"none" or "open gap" for a class — this includes Go for some classes, such
as the security concepts that don't apply to a perimeter-protected daemon —
that language contributes no finding for that class and the walk moves to
the next one.

A class whose `**Consumers:**` line names hotpath with no facet parenthetical
IS its lens — e.g. Class 8 is the `silent_fail_open` lens. Record its matches
into that lens's primary pattern field (the array of distinct
patterns/identifiers actually found in the repo). A class with zero matches
for a given language is not an error — record it as walked-and-not-found, and
continue.

A class whose `**Consumers:**` line names a hot-path facet in parentheses
enriches the named lens's `context` field with the adapted finding. Where
that class's own probe is the only detection the lens has for its primary
pattern field, also record matches there (Class 1 into `subprocess_hot_path`,
Class 5 into `dispatch_blocking` and `peer_dial_circuit_breaker`). The one
exception is Class 2: `async_io_decoupling` carries its own independent,
incident-derived detection for its primary fields, so Class 2 enriches
`context` only and never touches a primary field.

A lens's secondary refinement fields (pre-flight guard patterns, native
alternatives, and similar) populate only where a class gives a probe for
them; a field with no probe for the detected language is left absent rather
than guessed at.

`async_io_decoupling`'s own primary fields (goroutine/boot-stage/cancellation
patterns and dropped-context params) come from a Go-only detection pass
independent of the class library, scoped to `trigger_directories`:

```bash
grep -rnE 'go func|go bootstage\.Run' --include='*.go'
grep -rnE 'bootstage\.Run|OnReady|SetOnReady|DependsOn|Await\(' --include='*.go'
grep -rnE 'CompactAll|MergeGroup|filepath\.Walk|os\.ReadDir|io\.Copy' --include='*.go'
grep -rnE 'ctx\.Done\(\)|ctx\.Err\(\)|r\.Beat\(|context\.WithoutCancel' --include='*.go'
grep -rn '_ context\.Context' --include='*.go'
```

Record these as `io_work_patterns`, `boot_and_coupling_patterns`,
`async_discipline_patterns`, and `dropped_ctx_pattern` respectively. No
equivalent probe exists yet for other languages; the fields are absent there
rather than guessed at.

### Step 4: Accept seeded prose context

Use `AskUserQuestion` for per-lens prose seeding. Prefer sequential
category→item questions (one prompt per lens, ≤4 options each) over packing
every lens into a single prompt.

Prompt the invoker for incident descriptions, fix patterns, and
project-specific nuances for each lens. These become the `context` prose
fields in the config.

If the invoker has no incident prose to seed (first-time setup on a new
project), leave the `context` fields as empty strings with a
`<!-- TODO: seed with incident history -->` comment. The gate skill still
functions without prose context — it just provides less guidance to the
reviewer.

### Step 5: Generate `.thrum/hotpath-gate.json`

Assemble all discovered values into the JSON structure and write to
`.thrum/hotpath-gate.json`. Ensure the file is not gitignored (add a `!`
exception in `.gitignore` if needed, following the `.thrum/philosophy.md`
pattern).

Only emit `embed_aware_skip` for a language with a compiled-in-bundle concept
and a derivable reachability command (Go's `go:embed` is the current
example). Omit the field for a language with no such concept rather than
writing a placeholder.

If Step 3 found zero matching lenses across every detected language, do not
write an empty-but-valid config — see the scaffold/refuse behavior in
`## Zero-match handling` below.

Announce the path and summarize what was discovered per language, including
which reliability classes were found vs. walked-and-not-found.

## Zero-match handling

The generator never writes a config with an empty `lenses` object. When Step
3 finds no matching lens across every detected language:

- **Default:** write a scaffold marked at the top level with
  `_UNAUTHORED_SCAFFOLD: true`. Populate `trigger_directories` from a
  language-neutral serving heuristic — route decorators, files matching
  `*proxy*`/`*server*`/`*api*`, a `Dockerfile` with `EXPOSE`/`CMD`, and
  detected entrypoints. Add a commented TODO stub per reliability-library
  concept, keyed to the files the heuristic found.
- **Alternative, offered interactively:** refuse to write the file, with a
  message naming which languages were detected and why no lens matched.

No downstream consumer relies on a zero-lens config meaning "clean" — a
generator run either produces real findings, an explicit scaffold, or a
refusal.

## Re-run-unchanged mode

Triggered when `.thrum/hotpath-gate.json` exists.

### Step 1: Read the existing config

Read `.thrum/hotpath-gate.json` in full. Parse all lens sections.

### Step 2: Sanity-check against current project state

Re-run the detection steps from first-run mode, but compare rather than write:

- Are the `languages_detected` still correct? Any new language crossing the
  threshold?
- Are the `trigger_directories` still correct? Any new directories with
  hot-path code?
- Does each lens's primary pattern field still match what Step 3 finds? Any
  new patterns per language?
- Are the `reference_patterns` still accurate? Any new established patterns?

Each check is a boolean "matches" vs. "differs".

### Step 3: If nothing differs — no-op exit

Print: `.thrum/hotpath-gate.json` is current; no changes needed.

### Step 4: If anything differs — hand off to evolved mode

## Re-run-evolved mode

Triggered when the config exists AND the unchanged-mode sanity check flagged
drift.

> **Never silently overwrite.** The config may contain hand-seeded incident
> prose that must survive every re-run. A write without explicit confirmation is
> a bug.

### Step 1: Detect drift

Four drift categories:

- **New or removed languages** — a language crossing or falling below the
  detection threshold
- **New trigger directories** — new directories with hot-path code not in the
  config
- **New patterns** — new matches for an existing lens, per language
- **New reference patterns** — new established working patterns or tripwire
  tests

### Step 2: Compute a proposed diff

Present drift as a readable sectional diff. Each item should have:

- The detected change in plain language
- A proposed edit (addition / removal / update to a config field)
- A one-line rationale

### Step 3: Present for approval

Present the diff. On approval, apply edits in-place, preserving surrounding
content. Append a provenance comment:
`// updated YYYY-MM-DD via project-hotpath-gate re-run-evolved`.

On decline — do NOT write. Record the skipped proposal for future runs.

## Test impact selection plan (per-merge gate)

Owner ruling, verbatim: "default ON as soon as it lands, no side-by-side; safety net = daily full gate + a load/regression test before deploy".

Run the per-merge test lanes through the repository's test-impact-selection plan wrapper (the gate role's documented
command, taking `--base`, `--head` and `--lane`), not the bare full-lane runner. It runs the plan, prints the `TIS_PLAN` line, and passes `--producer-rc` to the runner. Quote the `TIS_PLAN` line in the
verdict. FULL (`decision=FULL RUN`) is the normal fallback: a plan error or any fail-closed reason runs the whole lane.
For a per-landing gate, a FULL RUN fallback means the full NON-race lane, never race-all.

## Reference

- `.thrum/hotpath-gate.json` — the config file this skill generates
- `../project-philosophy/resources/reliability-class-library.md` — the shared
  reliability class library; every `Consumers: ... hotpath` class and its
  per-language probes drive Step 3
- `coordinator-hotpath-merge-gate` — the gate skill that reads this config
- `project-philosophy` — the sibling skill that generates `.thrum/philosophy.md`
  (this skill follows the same generate-first / reconcile-on-reinvoke pattern;
  run both at the same onboarding moment)
