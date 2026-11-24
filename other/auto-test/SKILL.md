---
name: auto-test
description: 'Run an automated, sandboxed test of the Senzing Bootcamp plugin. Probes the live Senzing MCP server for drift and for inaccurate or misleading information, checks every MCP call the plugin makes against what the server actually accepts, and optionally walks the bootcamp with a simulated Bootcamper and lints the transcript against the interaction invariants. Each run gets its own sandbox, so it is safe to run many times a day and concurrently. Use when the maintainer wants to auto-test, smoke-test on a schedule, watch for MCP server drift, or check the plugin without sitting through a dry run. Maintainer tool — not part of the bootcamper experience.'
argument-hint: "[walk] [persona: terse|verbose|confused|impatient|offscript] [turns]"
---

# Auto Test

A **maintainer** tool for developing the Senzing Bootcamp Claude Plugin (SBCP).
Never invoked during a bootcamp. It is the unattended counterpart to
[`dry-run`](../dry-run/SKILL.md): dry-run is a careful session with a human,
auto-test is a cheap one you can run three times a day.

## What it is for, and what it cannot do

Two questions, and they deserve different amounts of trust.

**"Has the MCP server changed under us?"** — answered completely and for free. The
server is the plugin's hard dependency (INV-080 routes every Senzing fact through
it) and it changes with no notice. `mcp_probe.py` talks JSON-RPC straight to
`https://mcp.senzing.com/mcp` with **no Claude process and no tokens**, so this half
runs in seconds. This is the part that actually justifies a schedule.

**"Does the bootcamp still behave?"** — answered partially, and the limit is
structural. `phase3-conversational.md` forbids self-play for two reasons; the walk
here answers one and a half:

1. *ground-rules.md forbids fabricating the Bootcamper's response* — **answered.**
   Two OS processes: A runs the bootcamp, B answers as the Bootcamper. A fabricates
   nothing.
2. *an assistant that knows it is graded will comply* — **answered only by
   discipline.** A is never told it is under test, and grading happens afterwards on
   the saved transcript. Put an invariant in A's prompt and you are measuring the
   model's carefulness instead of the plugin's files.

⛔ **What stays unanswered:** a simulated Bootcamper is more cooperative than a real
one — it answers in format, never gets confused, never asks "wait, why?". So this
inherits phase 3's asymmetry rather than fixing it:

> **Findings are trustworthy. A clean run is weak evidence.**

Report a clean auto-test as "no regression detected", never as "the bootcamp works".
Phase 3 with a human still has to happen.

⛔ **(INV-369) A clean run that included the walk is reported only as "no regression detected
(simulated Bootcamper, persona `<p>`)"**, never as "phase 3 passed" or "the bootcamp works",
and the report lists phase 3 with the maintainer as not yet done. The persona is the part the
disclosure exists to carry: a clean run under `confused` and a clean run under `offscript` are
different evidence, and a reader handed "no regression detected" alone cannot tell which one
they have. A probe-only run names no persona, because no walk ran.

## Running it

```console
.claude/skills/auto-test/autotest.py                  # MCP only — seconds, free
.claude/skills/auto-test/autotest.py --walk           # + a simulated walk
.claude/skills/auto-test/autotest.py --walk --persona confused --turns 16
.claude/skills/auto-test/autotest.py --walk --keep    # keep the sandbox to inspect
```

**Starting mid-bootcamp, at a fixed model and effort (#870).** `--seed mid` builds dry-run's
mid-bootcamp project, at Module 5 step 11, and the lint then defaults to `--phase content`;
an explicit `--phase` still wins. `--effort <level>` sets the guide's effort from the first
turn, as `--model` sets its model, and both hold for the whole walk: the bootcamp asks the
Bootcamper to change neither (#4), so no Bootcamper reply is read as a `/model` or `/effort`
command. A reply that starts with `/` is sent to the guide as text (#656):

```console
.claude/skills/auto-test/autotest.py --walk --seed mid --model claude-haiku-5-5 --effort low
```

The scripts are stored executable (mode `100755`, #843, INV-419). Windows ignores that bit, so there
run each one through the interpreter, `python3 .claude/skills/auto-test/autotest.py`, with
the same arguments; the same holds for `mcp_probe.py` below.

**The argument chooses the runs** (`[walk] [persona] [turns]`):

- **No argument: present the two halves and ask which to run.** They cost very different
  things and answer different questions, so the choice is the maintainer's:
  1. **MCP probe** — zero tokens, seconds. Drift, conformance, server quality, and the
     static-contract audit against `tests/test_mcp_call_contracts.py`.
  2. **+ simulated walk** — spends tokens. Two OS processes run the bootcamp and answer as
     the Bootcamper, then `transcript_lint.py` grades the saved transcript.
- **An argument naming a walk** is the answer: run both. A trailing persona and turn count
  answer the walk's own parameters (`--persona`, `--turns`); otherwise the defaults
  (`terse`, 12) stand.
- **The probe runs either way, and it runs first.** A walk against a server that has
  drifted underneath it produces findings no one can attribute.

⛔ **The walk is never inferred from silence.** (INV-333) It is asked about, not assumed.

Exit code is 1 if anything BREAKING was found, 0 otherwise, so it drops into cron or
CI unchanged. `--json` prints the machine-readable report; every run also writes
`report.json` into its sandbox.

To refresh the baseline after deliberately accepting a server change:

```console
.claude/skills/auto-test/mcp_probe.py update
```

Commit the resulting `baseline/mcp-snapshot.json` — the offline suite reads it.

## The sandbox, and why each layer is there

Each run builds a fresh private directory under the system temp directory, named
`senzing-autotest-<timestamp>-<persona>-<random>` (`tempfile.mkdtemp`, mode 0700,
resolved), holding `project/` and the Bootcamper's empty `bootcamper/`. Reports stay in
`~/senzing-autotest/reports/`. `project/` is built by dry-run's `scaffold_project.py` in the
mode `--seed` names, with `--run-root` vouching for the run root, the one place under the
temp directory the scaffold builds in. If the scaffold fails, the walk is not run: the report
carries a BREAKING `scaffold-failed` finding with the scaffold's error and the run exits 1,
as a failed walk does, and the probe's findings are still reported. There is no fallback
project (#840).

| Layer | Why |
|---|---|
| Run root under the system temp directory, never `$HOME` | Claude Code loads `.claude/CLAUDE.md`, `CLAUDE.md`, `CLAUDE.local.md` and `.claude/rules/*.md` from a child's cwd and every ancestor even under `--setting-sources project,local` (CLI 2.1.310, #794), so a run under `$HOME` hands the guide `~/.claude/CLAUDE.md` (#834). `write-gate.py` exempts the project directory first, so a project under the temp directory is gated only at its own boundary. The root is resolved because the gate compares targets with `os.getcwd()`, and macOS reaches its temp directory through a symlink. On Windows the temp directory is under the user profile; the report then names any instruction file found there |
| Bootcamper runs from `bootcamper/` beside the project | never `$HOME` and never inside the project; `walk.py` creates it |
| **git worktree pinned to a SHA** | you will edit the repo while runs execute; an unpinned run tests half-saved files and its findings are unattributable |
| Per-run `mcp.json` + `--strict-mcp-config` | the run sees Senzing and nothing else — none of your authenticated claude.ai connectors |
| Distinct `--session-id` | concurrent runs never share history |
| **Instruction isolation** (always) | `--setting-sources project,local` on every `claude` call, so the walk reads the sandbox's instruction files and none of the host user's — a `~/.claude/CLAUDE.md` rule is otherwise obeyed by the guide and then scored as the plugin's behavior (#733). It leaves `CLAUDE_CONFIG_DIR` alone, so it costs no credentials; where the CLI cannot take the flag, the report names every host instruction file the run could read |
| `--isolate-config` (opt-in) | own `CLAUDE_CONFIG_DIR` for session state; isolates state but **not credentials**, so it needs `ANTHROPIC_API_KEY`. ⚠️ Not what isolates instructions: the user instruction file is `$CLAUDE_CONFIG_DIR/CLAUDE.md`, so moving that directory takes the credentials with it |

The sandbox is removed at the end unless `--keep`.

## The pieces

| File | Does | Costs |
|---|---|---|
| [`mcp_probe.py`](mcp_probe.py) | drift, conformance, server-quality, static-contract audit | zero tokens |
| [`transcript_lint.py`](transcript_lint.py) | interaction invariants over a recorded walk | zero tokens |
| [`walk.py`](walk.py) | drives the two-process bootcamp walk | tokens |
| [`autotest.py`](autotest.py) | sandbox + orchestration + report | — |
| `baseline/mcp-snapshot.json` | the committed contract the offline suite checks against | — |

## What made this hard, and what you must preserve

**Most closed value sets live in description prose, not in JSON-Schema enums.** When
the harness was built (2026-07-27) all 13 tools had zero `enum` keys. On server 1.39.0
(2026-10-15) four parameters declare one: `sdk_guide.topic`, `mapping_workflow.action`
(whose enum includes `null`), `reporting_guide.topic` and `get_sdk_reference.topic`.
The rest — the languages `generate_scaffold` and `sdk_guide` take, `search_docs`'s
categories, the sample datasets — live only in description prose. A checker that reads
only `inputSchema.enum` misses most of the contract. `accepted_values` unions a declared
enum into the accepted set with `null` dropped, so an enum can clear a suspicion but
never replaces the probed or prose sets and never adds a rejection.

**So the accepted set is discovered by probing, not by reading.** Sending
`sdk_guide(topic='zzz_probe_invalid')` comes back *"Valid topics: install, configure,
load, …"*. `PROBE_MATRIX` does that once per parameter. Every entry must stay
side-effect free — `mapping_workflow` qualifies only because an unknown action fails
deserialization before the handler runs.

⛔ **Never infer a rejection. Send the value.** This rule cost three false positives
while the tool was being built, each one a confident BREAKING finding against
correct plugin text:

- `get_sample_data(dataset='list')` is absent from every list the server publishes
  and works perfectly — an undocumented discovery sentinel.
- `sdk_guide(language='c#')` is absent from the rejection message and works — the
  rejection list is a *display* list, not the acceptance set.
- `generate_scaffold(language='typescript')` works despite a description naming only
  four languages.

`verify_literal()` settles a suspicion with an actual call; `record_verified_extras()`
persists the verdict into the baseline so the offline suite inherits it.

⛔ **`submit_feedback` and `download_resource` are blocked by flag, not by
instruction.** `NEVER_CALL` in the probe, `--disallowedTools` in the walk. An
unattended run cannot be trusted to remember a rule.

## Reading the output

Severities mean specific things:

- **BREAKING** — a documented path is broken now. A tool vanished, a parameter
  became required, a value the plugin uses is rejected, or the static contract in
  `tests/test_mcp_call_contracts.py` no longer holds.
- **WATCH** — the server changed in a way that needs a human to re-read it, or it
  carries misleading information (`doc-incomplete`, `silent-accept`).
- **INFO** — context, not action.

Report the findings in that order — BREAKING, WATCH, INFO — naming the sandbox the run used
and whether the walk was included, and, where it was, the persona the clean-run line above
requires (INV-369).

Two WATCH findings were live as of 2026-07-27 and are about the **server**, not the
plugin: `generate_scaffold.language` accepts `typescript` while documenting four
languages, and `search_docs.category` accepts any string without error, so a typo
returns plausible but wrongly-scoped results.

## Scheduling

The MCP half is the part worth running often — your plugin only changes when you
change it, and 515 tests already cover that, while the server moves on its own.

```console
0 */4 * * *  cd /path/to/repo && .claude/skills/auto-test/autotest.py --json >> ~/autotest.log 2>&1
0 3 * * *    cd /path/to/repo && .claude/skills/auto-test/autotest.py --walk --persona confused --turns 20
```

Rotate `--persona` across runs (`terse`, `verbose`, `confused`, `impatient`,
`offscript`). A single cooperative persona is the main reason an automated walk is
weaker than a human one, and rotation is the cheapest partial mitigation. If the maintainer
names no persona on a walk they have run recently, say which one the last run used.

## What to do with a finding

Follow [`dry-run`](../dry-run/SKILL.md)'s rules. They apply unchanged, and in dry-run's
order: the finding is recorded first and fixed after.

⛔ **(INV-317) Record each finding as you find it, before fixing anything:** in the run's
dated `specs/IMPLEMENTED.md` entry, marked not yet filed, or as a GitHub issue filed after
the maintainer's yes (INV-314), or one yes for the whole list shown in one message (INV-314,
2026-10-13 note), under the conditions in `.claude/skills/feedback-to-issues/drafts.py` →
"The batch yes". Never put it in a new file under `specs/` (INV-307). A fixed
finding no longer reproduces, so a run that fixes first leaves no evidence the finding existed.

⛔ **(INV-318) Never apply the `unattended-ok` label to an issue this run files.** A probe that
labels its own findings lets `/unattended-issue-loop` *(user level)* work them with nobody in
between. Choosing what runs unattended is the maintainer's decision alone.

Only after the record, in dry-run's order (its steps 2 to 6): fix the class
not the instance, write a repo-level test, ⛔ **negative-control it**, record it in
the same `specs/IMPLEMENTED.md` entry (what was done, and the issue the finding became),
and either queue the invariant it establishes or explicitly state that it establishes none.
⛔ **(INV-365) Route it through `/review-invariants`; never edit `specs/INVARIANTS.md` here:** write a
`DEFERRED INVARIANT` block for a new rule, or a `PROPOSED AMENDMENT` block for a correction,
in the run's `specs/IMPLEMENTED.md` entry, as
[`review-invariants` → "Writing one"](../review-invariants/SKILL.md#writing-one) shows
(INV-300), then tell the maintainer to run `/review-invariants`.

⛔ **(INV-317) A scheduled run's `report.json` or log is raw output, not a recorded finding.**
An `autotest.py` run on a schedule writes its report and nothing else. Its lines become
findings when the maintainer triages the report, and that triage records each one, as above,
before fixing it.

For a **server-side** finding (`doc-incomplete`, `silent-accept`, `doc-wrong`) the
fix is not in this repo. Record it first, as above. Then work around it in the plugin if it can mislead a
bootcamper, and consider reporting it upstream — but ⛔ **not** via `submit_feedback`
from an automated run.

## Guardrails

- **Never send anything outside the machine.** No `submit_feedback`, no
  `download_resource`. Enforced by flag in both the probe and the walk. Let the flags do
  the enforcing: do not hand-run the pieces around `autotest.py`.
- **Never tell process A it is under test.** It destroys the only thing the walk
  measures.
- **Never report a clean run as a passed audit.** State the coverage limits; the
  report carries them for you.
- **Never put the sandbox under `$HOME` or at a fixed shared path.** Each run gets its own
  `mkdtemp` directory under the system temp directory.
- **Keep `baseline/mcp-snapshot.json` committed.** Without it the offline
  conformance test silently covers nothing — `tests/test_auto_test_harness.py`
  asserts it is present for exactly that reason.

## Scope note

`.claude/` is **not** propagated to the public repo (`python3 -m tools.bootcamp_build promote`
publishes the built packages, each assistant's catalog, `site/` and `public/` only), so this
skill never ships to bootcampers.
