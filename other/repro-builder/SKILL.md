---
name: repro-builder
description: "Turns a vague bug report into a minimal, runnable reproduction: extracts hypotheses from the report text, snapshots the environment, generates a repro test/script, EXECUTES it and iterates (max 5 attempts) until the bug demonstrably reproduces - or documents precisely which information is missing. The repro lives outside the target project. Trigger: /repro"
trigger: /repro
---
# /repro

Turns a vague bug report into a minimal, actually EXECUTED
repro test - or a precise list of which information is missing to reproduce.

## PROTECTION RULE - never modify target project or ~/.claude/

This skill writes repro artifacts to a `repro/` subfolder in the **working
directory**, never inside the target project. It also never touches
`~/.claude/`. If `$ProjectDir` resolves to a path under `~/.claude/`, the
collector rejects it with an error.

## What this is for

- "Doesn't work" is the most expensive sentence in the industry. Instead of guessing, this
  skill extracts hypotheses from the report, generates a repro candidate, EXECUTES IT
  and iterates based on the result.
- **No fix** - repro is the product, a fix is a follow-up task. No
  UI/browser reproduction (code level only). No production databases -
  only local/synthetic data.
- Repro artifacts always live **in the working directory** (`repro/` subfolder),
  **never in the target project**.

## What You Must Do When Invoked

If `/repro -help` or `/repro -h` (without further arguments) is invoked:
output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target and bug report

Clarify `-ProjectDir` and the bug report (paste free text or file path).
Get confirmation.

### Step 3 - Environment snapshot

```powershell
& "<SKILL_DIR>/scripts/env-snapshot.ps1" -ProjectDir "<path>"
```

The result (stack, runtimes, test runner, git state, entry points) flows
into the protocol later - it records AGAINST which state reproduction was done.

### Step 4 - Dissect report

Symptom (what happens), expectation (what should happen), trigger candidates
(inputs, sequence, state), environment hints. Missing core information NOTE
IMMEDIATELY as "missing info" - but continue with hypotheses anyway, do not
give up prematurely.

### Step 5 - Localize suspicious code

From symptom terms + stacktrace (if present) find the relevant files
(Grep) and read them completely (Read). Form hypotheses: under which conditions
does this code produce the symptom? Order by likelihood.

No usable hint in the report: make ONE hypothesis attempt from pure
code reading, then abort early with a list of questions - do not burn 5
blind attempts.

### Step 6 - Repro loop (max 5 attempts)

Per attempt:

1. Generate repro artifact in the working directory under `repro/` (never in the
   target project): preferably a test in the style of the detected test runner that
   imports/invokes the target project; otherwise a standalone script. Minimal: one
   scenario, one hard assertion on EXPECTED behavior - the test MUST fail when the
   bug is present (that is the proof logic).
2. Execute (Bash/PowerShell depending on stack), interpret result:
   - Assertion fails with the reported symptom -> **reproduced**.
     Minimize artifact (remove unnecessary parts, run again - must stay red).
   - Test green or different symptom -> discard/refine hypothesis, next
     attempt.
3. Record each attempt in the protocol (hypothesis, artifact version, result
   including verbatim output).
4. External services (DB, API) needed: use stubs/fakes in the artifact; if
   impossible, document as missing info instead of guessing.
5. Heisenbug suspicion (timing/race): artifact with retry loop (N runs,
   measure failure rate); "reproduced" from demonstrable rate, rate in protocol.
6. Test runner not installed in target project: standalone script instead of test,
   do not install anything in the target project.

### Step 7 - Finalize

`repro/` folder in the working directory with repro artifact + `repro-protocol.md`:

- **Reproduced**: environment snapshot, final artifact, exact output of the red
  run (verbatim), classification (which hypothesis was correct, `proven` by
  run output). Note: artifact is suitable as regression test.
- **Not reproduced** (after up to 5 attempts): all attempts in the protocol +
  precise list of missing info as copy-ready follow-up questions for the reporter
  ("Which locale?", "What data volume?"). Never "cannot reproduce" WITHOUT this
  list.

Evidence requirement: "reproduced" only with verbatim error output of the run in
the protocol. Hypotheses without a run are at most `suspected`.

### Step 8 - Summarize

Briefly: reproduced yes/no, how, what (if not reproduced) is missing.

## Usage

```
/repro                          # interactive
/repro <repo>                   # report will be prompted
/repro <repo> <report-file>     # report from file
/repro -help
```


