---
name: run-validation-until-no-failure
description: |
  Use when the user wants to run the IDA validation pipeline (`uv run ida_analyze_bin.py -debug`)
  repeatedly until it reports zero failures. For each failing skill, diagnose the failure, ask the
  user how to proceed, and offer several viable solutions. Only when the user explicitly says the
  failure cannot be solved now and asks to temporarily disable the skill, comment it out in
  configs/<GAMEVER>.yaml and record it in docs/ida_validation_failure-<GAMEVER>.md. Use after a
  game-version bump or a large batch of new skills when several skills may fail and you want a
  guided triage-and-quarantine pass.
  Triggers: run validation until no failure, validate until green, get validation passing,
  disable failing skills, quarantine failing skills, loop ida_analyze_bin until no failures
disable-model-invocation: true
---

# Run Validation Until No Failure

Loop the analysis/validation pipeline until it reports **`Failed: 0`**. Each iteration: run
`ida_analyze_bin.py -debug`; if a skill failed (the pipeline is fail-fast, so it's exactly one),
diagnose *why*, present several concrete resolution options, and ask the user which option to take.
Do not disable or record the skill before the user answers. If the user explicitly answers that it
cannot be solved now and asks to temporarily disable the skill, append the failure to
`docs/ida_validation_failure-<GAMEVER>.md`, comment that skill out of `configs/<GAMEVER>.yaml`, and
run the `unit` and `repository-contract` unittest suites before resuming validation. If the config
dependency test reports consumers whose `expected_input` can no longer be produced, apply the same
ask-before-action rule to each dependent skill. Environment / infrastructure failures are **not**
skill bugs — STOP and surface those instead of quarantining a skill.

Resolve `GAMEVER` from the user's explicit request or `CS2VIBE_GAMEVER`; use only
`configs/$GAMEVER.yaml` for the validation run and all quarantine edits.

## When to Use

- The user asks to "run validation until it passes / until no failures", "get validation green", or
  "disable the failing skills and keep going".
- After bumping to a new game version or landing many new skills, to triage a wave of failures — each
  gets quarantined with its reason for later fixing.

## Why the loop works (pipeline facts)

- `uv run ida_analyze_bin.py -debug` ends with a summary and exits non-zero when `Failed > 0`:
  ```
  ============================================================
  Summary
  ============================================================
    Successful: N
    Failed: N
    Skipped: N
  ```
- It is **fully fail-fast**: the first failing skill aborts the remaining skills, the remaining
  platforms, **and** the remaining modules. So each run surfaces **exactly one** actionable failing
  skill — handle at most one validation-failing skill per iteration.
- Skills whose `expected_output` YAML already exist on disk are **skipped** on re-runs, so each
  iteration advances quickly to the next unresolved skill.

## Safety Rules — STOP conditions (never loop forever)

For every STOP condition, stop the automatic loop, report the evidence, offer concrete next-step
options, and ask the user how to proceed. Do not resume until the user answers.

- **Infra / environment failure → STOP and ask.** If the failure is not attributable to a specific
  skill's logic, do **not** comment out a skill. Signals:
  - `Failed: IDB lock file detected (...)`
  - `Failed: opened binary verification failed` / `Aborting current binary after opened binary verification failure`
  - `Failed to restore MCP connection ...`
  - `Error: Binary file not found` or any `idalib-mcp` startup error
  These mean the toolchain / binary / IDB is broken, not the skill. Offer relevant recovery options
  such as clearing a confirmed stale lock, correcting the binary path, or restarting the MCP/IDA
  session, then ask the user which action to take.
- **`-gamever` required error → STOP and ask.** The command relies on `$CS2VIBE_GAMEVER`. If the run
  errors, offer to use the user's explicit version, read `CS2VIBE_GAMEVER` from `.env`, or inspect
  available `configs/*.yaml` files with the user; do not guess the game version.
- **No progress → STOP and ask.** If a run's failing skill is the *same* one you just commented (the
  config edit didn't take), or the `Failed` count did not go down, report the evidence and offer
  investigation options. Never re-comment the same block or force past it.
- **Unrelated unittest failure → STOP and ask.** Only dependency gaps reported by
  `TestConfigSkillDependencyGraph.test_config_module_skills_have_no_expected_input_order_gaps` may
  lead to asking whether to quarantine more skills. Do not hide failures from any other test,
  exception, import error, or test infrastructure problem by commenting out config entries. Offer
  repair or investigation options and ask the user how to proceed.
- **User decision is required before skill edits.** Present several viable, failure-specific repair
  options and wait for the user's answer. If the user selects a repair, make only the edits authorized
  by that choice and run the relevant tests before resuming validation. Quarantine only after an
  explicit answer such as `解决不了，先屏蔽该skill` (or an unambiguous equivalent); do not interpret
  silence, a generic approval, or uncertainty as permission to quarantine.
- **Quarantine edits are comment-only.** After explicit quarantine approval, append to
  `docs/ida_validation_failure-<GAMEVER>.md` and comment (prefix `#`) the validation-failing skill or
  dependency-broken descendant's block in `configs/<GAMEVER>.yaml`. Comment one skill block at a
  time, re-run the relevant gate, do not delete config entries, do not touch unrelated skills, and
  do not uncomment anything unless the user separately requests it.

## Method

### Step 1 — Run validation; capture full log + summary

```bash
uv run ida_analyze_bin.py -gamever "$GAMEVER" -configyaml "configs/$GAMEVER.yaml" -debug > /tmp/ida_validation_output.txt 2>&1; tail -15 /tmp/ida_validation_output.txt
```

The full log goes to `/tmp/ida_validation_output.txt`; `tail -15` is only for the pass/fail verdict.

### Step 2 — Read the verdict from the summary

From the `tail` output, read `  Failed: N`.

- `Failed: 0` → **DONE.** Report success and stop the loop.
- `Failed: N` (N ≥ 1) → continue. (Fail-fast means one actionable skill; `N` counts the pending work
  items that one failure aborted.)

### Step 3 — Identify the failing skill + its module + platform (from the FULL log)

The per-skill failure detail is not reliably in the last 15 lines — parse the whole file. Find the
last real failure signal (the pattern excludes the `Failed: N` summary line):

```bash
grep -nE "^  (Failed: [^0-9]|Pre-processed but missing expected_output:|Preprocess failed:)" /tmp/ida_validation_output.txt | tail -5
```

The failing skill is named on that line (or, on the agent-fallback path, on the last
`  Processing skill: <skill>` immediately followed by a bare `    Failed`). Then read upward for
context:

- **Module** = nearest preceding `Module: <module_name>` header.
- **Platform** = nearest preceding `  Platform: <platform>` line.
- **Reason** = the indented lines of that skill's block (e.g. `missing expected_input: ...`,
  `Skill file not found: ...`, preprocess diagnostics).

Now apply the **Safety Rules**: if this is an infra failure, stop the loop, offer recovery options,
and ask the user how to proceed. Do not continue to the skill-quarantine steps.

### Step 4 — Ask the user how to resolve the failure

Report the skill name, module, platform, verbatim failure block, and a one-line diagnosis. Then offer
2-4 concrete, viable options tailored to the failure and ask the user which one to take. Prefer
specific options such as:

1. Fix the failing skill or preprocessor logic, then run its targeted tests and validation again.
2. Repair a missing or invalid dependency, config entry, or generated artifact, then re-run the
   dependency test and validation.
3. Investigate ambiguous environment or toolchain evidence before changing any skill.
4. If it cannot be solved now, temporarily disable the failing skill.

Do not present irrelevant boilerplate options. **Stop and wait for the user's answer.** Then:

- If the user selects a repair or investigation option, carry it out within the user's chosen scope,
  run the relevant tests, and return to Step 1. Do not write a quarantine record.
- If the user explicitly answers `解决不了，先屏蔽该skill` or gives an unambiguous equivalent that
  both defers the fix and requests temporary disabling, continue to Step 5.
- If the answer is ambiguous, ask a concise follow-up. Do not quarantine by inference.

### Step 5 — Record the approved quarantine in the game-version doc

File: `docs/ida_validation_failure-<GAMEVER>.md`, using the resolved `GAMEVER` verbatim in the
filename. Create it if missing; otherwise **append** a new section. Record: skill name, module,
platform, the verbatim failure block from the log, a one-line diagnosis, and that the user chose to
temporarily disable the skill.

```markdown
## find-ConnectInterfaces  (module: engine2, platform: windows/linux)

Failure (from `ida_analyze_bin.py -debug`):

    Start skill: find-ConnectInterfaces
      Preprocess: no old YAML for ConnectInterfaces.windows.yaml
      Preprocess: trying func_xrefs fallback for ConnectInterfaces
      Preprocess: exclude_func YAML missing or invalid: CNetSupportImpl_Connect.windows.yaml
      Preprocess: failed to locate ConnectInterfaces
    Preprocess failed: find-ConnectInterfaces; falling back to AGENT SKILL
    Processing skill: find-ConnectInterfaces
      Falling back to: .claude\skills\find-ConnectInterfaces\SKILL.md
      Error: Skill file not found: .claude\skills\find-ConnectInterfaces\SKILL.md
      Failed

Diagnosis: preprocessor could not locate ConnectInterfaces and no agent SKILL.md exists to fall back
to. Needs a preprocessor fix or a find-ConnectInterfaces SKILL.md.

Decision: user chose to temporarily disable this skill because it could not be resolved now.
```

### Step 6 — Comment the failing skill out of configs/<GAMEVER>.yaml

Comment the skill's entire list-item block **under the correct module**, and add one `Awaiting fix`
line above it that points at the game-version failure doc. The rule: insert a `#` right after the
6-space base indent on every line of the block, keeping `{platform}` placeholders verbatim (this
disables it for all platforms).

Before:

```yaml
      - name: find-ConnectInterfaces
        expected_output:
          - ConnectInterfaces.{platform}.yaml
        expected_input:
          - CNetSupportImpl_Connect.{platform}.yaml
```

After:

```yaml
      #  Awaiting fix, failure reason has been written into "docs/ida_validation_failure-13990.md"
      #- name: find-ConnectInterfaces
      #  expected_output:
      #    - ConnectInterfaces.{platform}.yaml
      #  expected_input:
      #    - CNetSupportImpl_Connect.{platform}.yaml
```

The block runs from its `- name:` line (6-space indent) through every more-indented line until the
next `- name:` at the same level, or a dedent.

**Disambiguation (important):** the same skill name can appear under several modules (e.g.
`find-ConnectInterfaces` exists in 3 modules). Comment **only** the one under the `Module:` you found
in Step 3. Use the Edit tool with an `old_string` that includes the *preceding sibling skill entry*
(which differs per module) so the match is unique — a bare block match would silently hit the wrong
module.

### Step 7 — Run unit and repository-contract tests after every configs/<GAMEVER>.yaml quarantine

Immediately after commenting out any skill block, run both explicit unittest suites:

```bash
uv run python tests/run_test_suite.py unit -b --durations 30
uv run python tests/run_test_suite.py repository-contract -b --durations 30
```

The suite runner audits that every discovered test is assigned exactly once. The `unit` suite covers
the implementation-level analysis, config, snapshot, and candidate behavior; the
`repository-contract` suite covers checked-in configuration and dependency-graph invariants. Redis
and release integration suites are outside this quarantine gate.

- **Both suites pass** → the active `configs/<GAMEVER>.yaml` dependency chain is intact; continue to
  Step 8.
- **Only**
  `TestConfigSkillDependencyGraph.test_config_module_skills_have_no_expected_input_order_gaps`
  fails → inspect its dependency-gap list. Each entry identifies a consumer whose `expected_input`
  is no longer produced, for example:

  ```text
  windows module[2] server/find-ChildSkill missing: _artifacts/server/Parent.windows.yaml
  ```

  Here `server/find-ChildSkill` is the affected child skill. Report the gap, provide viable options
  such as repairing/restoring the producer, changing the consumer dependency when semantically
  correct, or temporarily disabling the child, and ask the user how to proceed. Stop and wait for the
  answer. If the user selects a repair, implement it and re-run both unittest suites. Only if the
  user explicitly says it cannot be solved now and asks to temporarily disable that child, append
  its unittest failure, dependency diagnosis, and decision to
  `docs/ida_validation_failure-<GAMEVER>.md`; then comment that child's full block under the named
  module using the Step 6 rules and re-run both unittest suites immediately.
- **Any other unittest failure** → STOP and ask. It is not evidence that another skill should be
  quarantined.

Handle one unique child skill per unittest iteration. A child may be listed once per platform;
comment its all-platform `{platform}` block only once after explicit approval. Ask again for each
newly exposed descendant; a previous quarantine decision does not authorize later descendants. Keep
re-running both suites until they pass. Do not return to IDA validation while either suite is red.

### Step 8 — Resume the validation loop

Go back to Step 1. The just-disabled skill is now skipped, and previously-successful skills are
skipped (their outputs exist), so the next run reaches the next failure quickly. Repeat until
`Failed: 0` (DONE) or a STOP condition trips.

> **Cascading is expected and must be resolved before validation resumes.** Disabling a producer can
> break a consumer whose `expected_input` names the disabled output. The unittest dependency graph
> catches this immediately, even when stale YAML artifacts would otherwise let the validation run
> skip past the broken config chain. Ask the user how to resolve each descendant, apply the selected
> repair or explicitly approved quarantine, and call the full dependency chain out in the report.

## Quick reference — failure signal lines

| Log line (2-space indent) | Meaning | Action |
|---|---|---|
| `Failed: <skill> (missing expected_input: ...)` | dependency YAML absent | diagnose, offer solutions, ask user |
| `Failed: <skill> (invalid expected_input ...)` | dependency YAML malformed | diagnose, offer solutions, ask user |
| `Pre-processed but missing expected_output: <skill> (...)` | preprocess ran, output not written | diagnose, offer solutions, ask user |
| `Preprocess failed: <skill>; falling back to AGENT SKILL` → `    Failed` | preprocess AND agent fallback failed | diagnose, offer solutions, ask user |
| `Failed: <skill> (<exception>)` | skill raised | diagnose, offer solutions, ask user |
| `Failed: IDB lock file detected ...` | stale lock / another IDA instance | **STOP** (infra) |
| `Failed: opened binary verification failed` | wrong/broken binary open | **STOP** (infra) |
| `Failed to restore MCP connection ...` | idalib-mcp died | **STOP** (infra) |
| unittest dependency gap: `<module>/<skill> missing: <artifact>` | active consumer has no active producer | offer repair/quarantine options, ask user |
| any other unittest failure | unrelated code/test/infrastructure failure | **STOP** |

## Notes

- `tail -15` is only for the verdict; always parse the **full** `/tmp/ida_validation_output.txt` to
  identify the failing skill and its reason.
- IDA validation surfaces one actionable skill per iteration (fail-fast). The mandatory `unit` and
  `repository-contract` loop may surface several dependency descendants; ask about and handle one
  block per unittest iteration.
- Never run the next IDA validation iteration until both suite-runner commands above pass with zero
  failures.
- On the quarantine path, edit `configs/<GAMEVER>.yaml` by commenting only. Re-enabling a skill once
  it's fixed is a separate manual step — the commented blocks plus
  `docs/ida_validation_failure-<GAMEVER>.md` are the resulting to-do list.
- This skill does not `git commit`; leave staging/committing to the user unless they ask.
