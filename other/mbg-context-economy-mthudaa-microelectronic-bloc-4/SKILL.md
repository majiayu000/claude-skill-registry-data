---
name: mbg-context-economy
description: How to work in this repository without burning the context window - resolve the repo from $MBG_ROOT instead of searching $HOME, read a file once at the right granularity, never poll git state, and climb the verification ladder cheapest-first instead of re-running the whole flow. Use at the start of any multi-step task in this repo, and whenever a session starts feeling slow or repetitive. Do not use it to decide what a design should be - it governs how you gather information, not what you conclude.
metadata:
  short-description: How to work in this repository without burning the context window - resolve the repo from $MBG_ROOT instead of searching $HOME, read a file once at the right…
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-context-economy/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG Context Economy

## Purpose

This repository is large — `src/mbg/router.py` is 1437 lines, `checks.py` is
1210, `README.md` is 1958 — and the design flow prints a lot. An agent that
reads whole files, re-reads them, and polls state between every step will
exhaust its context before it finishes the task, and the user pays for all of
it.

This is not hypothetical. A real Codex session in this repository was
measured, and the numbers are the reason this skill exists:

```text
1,065 KB of conversation
  87%  tool OUTPUT, not reasoning
 357 KB  ONE 1000-line script, re-read 22 times   (~89,000 tokens)
  78 KB  src/mbg/checks.py, re-read 9 times
  70 KB  git status / git log / git diff, polled 27+ times
  33 KB  searching $HOME to find the repository it was already inside
```

Just under half the session was spent re-acquiring information the agent
already had. The task did complete — but most of the budget went to
re-reading, not to designing, and the user's own summary of it was that the
agent looked confused.

## When to Use

- At the start of any multi-step task in this repository.
- Before reading a source file over ~300 lines.
- Before running the design flow or the test suite.
- When a session starts feeling repetitive, slow, or expensive.

## When Not to Use

- To decide *what* a circuit should be, or whether a result is good. This
  skill governs how you gather information, never what you conclude from it.
- As a reason to skip verification. Reading less is the goal; **checking
  less is not**. If the cheap path cannot answer the question, pay for the
  expensive one and say why.

## Required Inputs

None. This applies to every session.

## Preconditions

- `source $MBG_HOME/activate.sh` (or an equivalent) has run, so `$MBG_ROOT`
  points at the checkout. If it has not, set it once — do not search for it.

## Workflow

### 1. Resolve the repository once — never search for it

The measured session spent **33 KB across 10 commands** running
`rg --files "$HOME"`, `find "$HOME" -path '*/.ai/knowledge/...'` and `ls -la`
over the home directory, hunting for a repo whose path was already in the
environment. Codex is especially exposed here: its plugin cache lives
under `$CODEX_HOME/plugins/cache/`, which is **not** the repository, so a skill
loaded from the cache tells you nothing about where the code is.

```bash
REPO="${MBG_ROOT:?run: source \"$MBG_HOME/activate.sh\"}"
cd "$REPO"
```

Resolve it once, at the top, and keep using it. `$MBG_ROOT`, `$MBG_HOME`,
`$MBG_VENV`, `$PDKPATH` and the pinned tool paths (`$MBG_MAGIC`,
`$MBG_NETGEN`, `$MBG_KLAYOUT`) are all exported by `activate.sh` — see
`mbg-setup`. If a variable is missing, that is a setup problem to report,
not a filesystem to crawl.

### 2. Index before you read

Reading a whole file to find one function is the single most expensive habit
in the measured session. Ask the structural question first:

| Question | Cheap | Expensive |
| :--- | :--- | :--- |
| What is in this module? | `grep -n '^def \|^class ' src/mbg/checks.py` — **~280 tokens** | reading `checks.py` — **~12,500 tokens** |
| Where is X defined? | `grep -rn 'def spice_to_gds_with_checks' src/mbg/` | reading `pipeline.py` — ~7,600 tokens |
| What does the flow return? | `grep -n 'return {' -A 12 src/mbg/pipeline.py` | reading `pipeline.py` |
| How big is this before I open it? | `wc -l <file>` | finding out by reading it |

The index is roughly **45× cheaper** than the file. Read the index, pick the
span, then read *that span only*.

### 3. Read a span once, and remember it

Two idioms from the measured session, both to be avoided:

```bash
# BAD — overlapping windows of a file already read, with line numbers
nl -ba examples/run_clocked_comparator.py | sed -n '420,620p'
nl -ba examples/run_clocked_comparator.py | sed -n '540,660p'
nl -ba examples/run_clocked_comparator.py | sed -n '730,850p'
nl -ba examples/run_clocked_comparator.py | sed -n '760,1030p'
```

`nl -ba` doubles the cost of every line for information you rarely use, and
overlapping windows re-pay for the overlap. If you need line numbers, `grep
-n` already gives them for the lines that matter.

**A file you have read is in your context. Re-reading it does not refresh
your memory — it duplicates it.** Re-read only when you have edited the file
since, or when a tool reports something that contradicts what you have.
"Let me just check that again" is the thought to catch.

### 4. Do not poll state

`git status --short`, `git log --oneline -5` and `git diff --stat` were run
**27+ times** in the measured session, several of them prepended to unrelated
commands, for **70 KB**. State does not change unless you change it.

- Check `git status` **once** before you start editing and **once** before
  you commit — that is the project's own rule in `AGENTS.md`, and it is two
  calls, not twenty.
- After a successful `Edit`/`Write`, the change landed. The tool would have
  errored otherwise. Do not read the file back to confirm it.
- Do not re-run a passing test to see whether it still passes.

### 5. Climb the verification ladder, cheapest first

The design flow has a natural cost order. Run the cheapest check that can
answer the question, and stop as soon as you have an answer:

```text
  parse + build_design_context      < 1 s    topology, nets, degree, sizes
  test_complexity_ladder.py         ~ 4 s    structural metrics, no layout
  test_router_synthetic.py          ~ 27 s   router logic, no PDK tools
  spice_to_gds_ctx()                ~ 40 s   layout + internal connectivity
  Magic DRC                         ~ 1 s    after layout exists
  KLayout DRC                       ~ 13 s   dominated by deck load, not size
  netgen LVS                        ~ 5 s
  PEX extraction + simulation       slowest
  test_all_designs.py               ~ 4 min  all 8 designs, all four legs
  pytest tests/ -q                  ~ 5 min  209 tests
```

Two rules that follow from that shape:

- **Internal connectivity gates the expensive tools.** `opens`, `shorts`
  and `missing_access` must all be zero before Magic, KLayout and netgen are
  worth running. If the internal check already knows the layout is wrong,
  report that — do not spend a DRC/LVS cycle rediscovering it.
- **Do not re-run the whole flow to inspect one stage.** The run already
  wrote its artifacts. Read `<outdir>/verification/drc_summary.json`,
  `<cell>.lvs.out`, `<cell>_extracted.spice` from disk instead of
  regenerating them.

### 6. Ask a command for the answer, not for its output

Shell output is the largest single cost in a design session, and most of it
is never used. Shape the command so it returns the answer:

```bash
# BAD  — 200 lines of report to find one number
cat outputs/x/verification/drc_summary.json

# GOOD — the verdict, in one line
python3 -c "import json;d=json.load(open('outputs/x/verification/drc_summary.json'));\
print(d['verdict'], [(r['engine'],r['status'],r['violations']) for r in d['results']])"

# BAD  — the whole LVS report
cat outputs/x/x.lvs.out

# GOOD — the four lines that decide it
grep -E 'Number of (nets|devices)|Final result|Property err' outputs/x/x.lvs.out
```

Cap anything that can run long: `| head -40`, `| tail -30`,
`| grep -c`, `2>&1 | tail -5`. A `find` or `rg` across a large tree without
a cap is how a single command costs thousands of tokens.

### 7. Put bulk reading somewhere other than your own context

When the platform offers sub-agents, a survey that would cost tens of
thousands of tokens inline — "audit this module", "find every call site of
X", "profile this run" — belongs in one. The sub-agent reads the files; you
receive the conclusion. Ask it for findings, not for transcripts.

This applies to *bulk reading*, not to everything: spawning an agent to
answer a question you could `grep` costs more than the grep.

### 8. Write intermediate results to disk, not into the conversation

Long logs, profiles, and generated data belong in a scratch file you can
query later, not pasted into context. Run the flow with its output
redirected, then extract what you need:

```bash
python tests/test_all_designs.py > /tmp/run.log 2>&1
sed -n '/FINAL SUMMARY/,$p' /tmp/run.log       # 12 lines, not 4,000
```

## Outputs

- The same conclusions, reached with a fraction of the context.
- Every claim still backed by a command that was actually run — economy is
  about not re-reading, never about not checking.

## Failure Modes

- **Searching for the repository.** `$MBG_ROOT` is exported by
  `activate.sh`. If it is unset, say so; do not crawl `$HOME`.
- **Reading a file to find a symbol.** Index first, then read the span.
- **`nl -ba file | sed -n 'a,b'` in overlapping windows.** Re-pays for the
  overlap and doubles the cost of every line.
- **Re-reading a file to "make sure".** It is already in context. Re-read
  only after you have edited it, or after a tool contradicted it.
- **`git status` prepended to unrelated commands.** Twice per task, not
  twenty times.
- **Re-running the full flow to inspect one stage.** The artifacts are on
  disk.
- **`cat`-ing a report to find one field.** Query it.
- **Skipping a check to save context.** This is the one failure mode that is
  worse than the waste. Reading less is the goal; verifying less is not. If
  budget is genuinely short, say what you did not run rather than implying
  it passed.

## Dependencies

- `mbg-setup` owns `$MBG_ROOT` / `$MBG_HOME` / `activate.sh`.
- `mbg-repo-analysis` is the read-only map to consult *before* opening
  modules; it exists precisely so nobody has to read `src/mbg` to orient.
- `mbg-ic-verify` owns the DRC/LVS cost model referenced in §5.
