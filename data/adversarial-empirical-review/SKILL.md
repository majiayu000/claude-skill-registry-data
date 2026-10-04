---
name: adversarial-empirical-review
description: "N-round adversarial review pipeline for empirical research output — the chain from data to LaTeX tables to a manuscript that cites them. A Claude drafter proposes minimal diffs, a deterministic mechanical battery gates every diff from a clean state with a regression gate, a Codex reviewer files check-backed critiques, and a blind judge panel decides residual disputes. Manual-invoke ONLY: trigger when the user explicitly runs /adversarial-empirical-review or names 'adversarial-empirical-review' / 'adversarial empirical review'. Do NOT auto-trigger on generic 'review my results', 'check my tables', or manuscript-editing requests. For prose-style refinement use style-emulation instead; this skill AUDITS WHETHER THE TABLES ARE CORRECT — that each number in the tables is what the analysis code computes, reproduces from the data, and is internally consistent. It is an empirical + code review: the manuscript is read only to resolve table numbering, and prose is not examined."
---

# Adversarial Empirical Review

Runs a regression-gated, N-round adversarial loop over a project's empirical output. The
design is in `docs/2026-06-08-adversarial-empirical-review-design.md` (v2) and the module API
in `docs/CONTRACTS.md`. Read the design before operating the skill.

The costly error here is corrupting a result that was already correct, so the whole pipeline is
incumbent-preserving: a hard failure-set regression gate, "no clear difference keeps the
incumbent" for residuals, and minimization of LLM judgment in favour of mechanical checks.

**The crux is whether the tables are correct.** Auditing an empirical manuscript means verifying
that the numbers in its tables are what the analysis code actually computes — that each
coefficient, standard error, p-value, N, and R² reproduces from the data and the code and is
internally consistent. This is an empirical + code review: the battery, the reviewer, and the
drafter are all scoped to **table-number correctness**, the manuscript is consulted only as the
spine that maps paper Table numbers to fragment files, and prose is not examined (the
prose-scanning catalog checks default to off; research-design and interpretation critique are out
of scope, with the consequential-category machinery retained as a fail-safe). The mechanical anchor for this is
`builtin.table_source_agreement` (every estout-fragment cell is audited against a `numbers.json` of
computed values) together with the reproduction tier and the coef/SE/t, star/p, bounds, and
sample-size checks. The crux is **fail-closed**: a manuscript table with no `numbers.json` spec is a
`FAIL` and a missing artifact a `CHECK_ERROR`, and the driver will not converge unless every
`required_checks` entry (default the crux) is present and passing — otherwise it stops with
`crux_unverified`. A manuscript whose tables are hand-transcribed estout fragments decoupled from
the regressions (the common case) is reviewed by recomputing the regressions and diffing the cells
— supply a `numbers.json` of computed values so the audit is mechanical rather than left to the
reviewer's eye.

**Generation-based certification (the path past the parse-and-compare ceiling).** Parse-and-compare
has a structural limit: a second numeric token inside one cell, a number in a spanning descriptor
row, or content behind an exotic macro is invisible to any LaTeX parser. The durable fix is to
GENERATE the fragments from the computed source so displayed == computed by construction:
`scripts/tablegen.py` renders estout-style fragments deterministically from `layouts` entries in
the same `numbers.json` (the project's pipeline calls `python tablegen.py --numbers ...
--tables-dir ...` after the analysis writes the artifact), and `builtin.fragment_regeneration`
certifies each laid-out table by re-rendering it and comparing **byte-for-byte** with the on-disk
fragment — any drift at all is a `FAIL`, so the parser gaps disappear for generated tables. The
parse-and-compare crux keeps running on the same artifact as defense in depth. Mixed mode is
supported (generated and hand-written tables side by side; the PASS message names the uncovered
tables); `require_all: true` under `battery.builtin["builtin.fragment_regeneration"]` demands a
layout for every manuscript table, and projects that adopt generation should add the check to
`required_checks` so an unevaluated state blocks convergence exactly like the crux. Keys under
`tables` starting with `_` are auxiliary value rows (placeholder sources for composite cells),
exempt from the crux's missing-row rule.

**From-raw mode (`snapshot_from_raw: true`).** The strongest re-execution tier: the driver copies
the project, **deletes every committed intermediate** (snapshot-partition files, output-partition
files, `protected_paths` caches, the numbers artifact — directory globs expanded, deletions
confined to the copy), runs the full raw inputs → cleaning → analysis → tables pipeline
(`rebuild.from_raw_command`, or `rebuild.from_raw_argv` as an exact argv list — preferred on
Windows) twice, and certifies three checks: `builtin.raw_table_identity` (the regenerated LaTeX
table files are IDENTICAL to the committed ones, modulo line endings/trailing whitespace),
`builtin.raw_numbers_agreement` (numbers artifact within tolerance), and `builtin.raw_determinism`
(the two runs agree). Activation is fail-closed: `partitions.raw` plus a from-raw command are
required, the raw partition is read-only and provenance-hashed like the snapshot, the identity
check is auto-added to `required_checks` so the run cannot converge while the from-raw chain is
unverified, and `driver init` halts if any project file matches no partition glob (an unclassified
file is a purge-coverage hole). The driver runs all of this inline — no orchestrator action is
needed beyond stepping — but expect long battery phases: the full pipeline executes twice per
re-execution, bounded by `rebuild.from_raw_timeout` (default 7200 s per run).

## Orchestration contract (read this first)

When invoked from Claude Code, **you are the orchestrator**, but you do **not** improvise the
control flow. A deterministic Python state machine — `scripts/driver.py` — owns every transition,
enforces the invariants (regression gate, ratchet, mapping disposal, termination), and persists
state to `progress.json` after each step. You step it and fulfil the agent dispatches it asks for.

**The Claude-vs-Codex split.** Python can launch Codex (subprocess) but cannot launch Claude
subagents. So the driver runs Codex roles (reviewer, `all_codex` judges) inline, and **pauses for
you** whenever it needs a Claude role (the drafter, and the Claude member of a `cross_family`
panel). Each pause is a typed `AgentRequest`.

## How to run it

1. **Preflight + setup.**
   ```bash
   cd skills/adversarial-empirical-review/scripts
   python driver.py init --config <path/to/aer.config.json>
   ```
   This validates config, runs the partition linter, builds the run workspace in a local temp
   dir (off Dropbox), establishes the incumbent baseline battery, records the baseline green-set
   and the state-0 fingerprint, and writes `progress.json`. It prints a JSON **action**.

2. **Step loop.** Repeatedly:
   ```bash
   python driver.py step
   ```
   The driver advances as far as it can on its own — running the battery, the failure-set
   regression gate, the Codex reviewer, the blind Codex judges, the resolution checks, the
   classifier, oscillation, and termination — and then prints one JSON action:

   - `{"action": "dispatch", "request": {role, family, prompt_path, input_paths, output_path, inline, no_network, cwd}}`
     — **only for Claude roles.** Dispatch it:
       - `role: "drafter"` → launch a Claude subagent (Agent tool, `model: "opus"`) with the
         instructions at `prompt_path` and the files in `input_paths`; the subagent edits the
         candidate and writes its JSON summary to `output_path`. Never use `claude -p`.
       - `role: "judge", family: "claude"` (cross-family panels only) → launch a fresh, isolated
         Claude subagent whose entire input is the `inline` payload; it must not read any file;
         it writes its `{choice, rationale}` vote to `output_path`.
     After the agent finishes, run `python driver.py step` again.

   - `{"action": "continue"}` → just step again.

   - `{"action": "done", "stop_reason": "...", "reports": {...}}` → the run terminated
     (converged / oscillation / round_cap / budget / halted). Read `artifacts/escalations.md`,
     `battery_report.md`, `cost_report.md`, and `run_summary.json`, then present the escalations
     to the user and copy results back.

3. **NO PASSIVE WAITING.** Between steps, proceed immediately. Pause only for a genuine error or
   a `halted` stop reason (an infrastructure error needing the user).

## Folding human decisions back (re-run)

Escalated identification/specification/causal-overclaim items land in `artifacts/escalations.md`.
The user records resolutions in `decisions.json` (content-hash-scoped). Re-running the pipeline
consumes them and suppresses re-litigation of settled matters.

## Key constraints (inherited + skill-specific)

1. **No `claude -p`.** All Claude work runs via the Agent tool (subagents). It is the only Claude
   channel that works on Windows and the credential-isolation mechanism (no `ANTHROPIC_API_KEY`
   is ever materialized; subagents use the session).
2. **Codex flags (Windows).** Codex subprocesses use `-m gpt-5.5 --skip-git-repo-check
   --dangerously-bypass-approvals-and-sandbox -c model_reasoning_effort=xhigh`, UTF-8 with
   `errors="replace"`. Judges additionally run with network denied and an isolated cwd.
3. **Blinding.** Judges receive the disputed claim and both versions **inline** as Version 1 /
   Version 2; they may not read files; the version→incumbent mapping is sealed outside any
   judge-reachable path. On Windows the sandbox bypass means isolation is defense-in-depth, not
   OS-enforced (see design §6, §10).
4. **Secrets.** Subprocess environments are scrubbed; reviewer/judge workspaces are
   secret-scanned and redacted; the audit never records a credential or a live mapping.
5. **Snapshot is read-only to the drafter.** The drafter edits code/tables/prose within each
   issue's allowed partitions, under a diff budget; promotion requires resolving ≥1 open issue.
6. **Dropbox temp.** The run executes in a local temp dir off any Dropbox-synced path; results
   are copied back at the end with one-level `.bak`.
7. **Resume.** `python driver.py step` resumes from the last checkpoint; `init --fresh` restarts.

## Invocation

Manual-invoke only: `/adversarial-empirical-review` or an explicit by-name request. It is
token-intensive (multi-round, re-execution, judge panels), so it never auto-triggers.

## File structure

```
adversarial-empirical-review/
├── SKILL.md                 # this file
├── README.md                # usage + config reference + limitations
├── docs/                    # design spec (v2), CONTRACTS.md, the Codex review
├── schemas/                 # JSON Schemas for the structured artifacts
├── prompts/                 # drafter · reviewer · classifier · judge
└── scripts/
    ├── contracts.py         # shared types (source of truth)
    ├── driver.py            # the state machine (you step this)
    ├── ledger.py · fingerprint.py
    ├── config.py · battery.py · regression.py
    ├── workspace.py · reexec.py
    ├── blinding.py · classify.py · dispatch.py
    ├── cost.py · audit.py
    ├── tablegen.py          # fragment generator (numbers.json layouts → .tex) + CLI
    └── checks_builtin/      # consistency · generation · bounds · reproduction
```

See `docs/CONTRACTS.md` for the exact module APIs and `README.md` for the config reference and
the deferred-feature list (from-raw mode, OS-container judge isolation, GUI, free-form reviewer
code, domain check packs).
