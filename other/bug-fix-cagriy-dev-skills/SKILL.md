---
name: bug-fix
description: Diagnose and fix an open bug tracked under bugs/ in the current repo, the test-driven way, then close it. Use when the user wants to fix a bug, resolve or close an open issue, "work the next bug", or address a defect previously filed via /bug-submit. Accepts a bug number from $ARGUMENTS; with none, takes the lowest-numbered open bug (a folder directly in bugs/), and stops with a handover to /bug-submit when there are no open bugs. Grounds in the codebase + the last feature, clarifies the report with the user (AskUserQuestion with options + a recommendation where possible), confirms a fact-driven root cause before touching code, explains the fix for approval, implements it test-first (TDD), and asks the user to verify when it can't test automatically (UI etc.). On confirmed resolution it appends resolution notes + lessons to the bug report, archives the bug folder into bugs/archive/, regenerates the tracker via bug-tracker-render, and makes one commit (never pushes). Step 1 confirms before doing any work when invoked proactively; the confirmation is skipped when the user explicitly typed /bug-fix. Because this skill modifies code and commits, the proactive-invocation confirmation is non-negotiable.
user-invocable: true
disable-model-invocation: false
argument-hint: "[bug number, or omit to take the lowest-numbered open bug]"
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion, Skill, Bash
---

# bug-fix — Diagnose, fix (TDD), and close a tracked bug

You are running the `bug-fix` skill. The user may have arrived here by typing `/bug-fix` (with an optional bug number in `$ARGUMENTS`) or because the model proactively invoked the skill. Your job is to take one open bug from `bugs/`, find its **root cause with evidence**, fix it test-first, get the fix confirmed, then close the bug (archive it + regenerate the tracker) and commit.

This skill works on the **current branch**: it never creates a branch and never pushes. It makes exactly **one commit** once the fix is confirmed.

This skill has eleven steps (Steps 0–10). Execute them in order. Do not skip Step 1 (proactive-invocation confirmation), Step 3 (clarification), Step 4 (root-cause gate), Step 5 (approval), or Step 9 (close + commit). The root-cause discipline in Step 4 and the TDD discipline in Step 6 are the whole point of this skill — do not shortcut them.

## Step 0 — Locate the repo and select the target bug

This step is read-only; do it before the confirmation so the confirmation can name the bug.

- `git rev-parse --show-toplevel` → `repo_root`. If it fails (not a git work tree), stop and tell the user to `cd` into the target repo first.
- Parse `$ARGUMENTS` for a bug number: accept `3`, `#3`, or `bug-3` → `N = 3`.
- List open bugs (folders directly in `bugs/`, which are by definition the *open* ones — closed bugs live in `bugs/archive/`):

  ```bash
  find "<repo_root>/bugs" -maxdepth 1 -type d -name 'bug-*' 2>/dev/null
  ```

  Parse `N` and `slug` from each `bug-<N>-<slug>` folder name (integers only, numeric compare so `bug-10` > `bug-9`).

**Selection:**

- **A number was given.** If `bugs/bug-<N>-*` exists → that is the target. If instead `bugs/archive/bug-<N>-*` exists → tell the user "Bug #<N> is already resolved (in `bugs/archive/`)." and stop. If neither exists → tell the user "No bug #<N> found under `bugs/` or `bugs/archive/`." and stop.
- **No number given.** If there are open bugs → the target is the **lowest-numbered** open bug. If there are **no** open bugs → report it and offer the handover, then stop:

  > No open bugs under `bugs/`. Nothing to fix. If you've hit something new, run `/bug-submit` to file it first.

Read the target bug's `bug-<N>-<slug>.md` fully into context (description, expected behaviour, repro steps, severity, screenshots, triage). Record `bug_number`, `slug`, `bug_folder` (`<repo_root>/bugs/bug-<N>-<slug>/`), and `report_file`.

## Step 1 — Confirm before proceeding (when invoked proactively)

This skill modifies code and creates a commit — proactive invocation without a clear opt-in is high cost. This check is strictly enforced (as it is for `feature-implement`).

Check the most recent user message for the literal tag `<command-name>/bug-fix</command-name>` (or a leading `/bug-fix` the user typed). If present, the user explicitly opted in — skip this step and continue with Step 2.

Also treat as opt-in (and skip this step) if the user, earlier in **this** conversation, explicitly approved fixing **this** bug — for example by choosing an `AskUserQuestion` option that named the bug and said to fix it, or by affirming a proposal of yours that did. Note the prior approval in one line of chat instead of re-asking; a fresh confirmation seconds after the user asked for exactly this is friction, not safety. **This does not extend to Step 5.** An approval given before the root cause was known cannot be approval of a fix nobody had seen yet, so Step 5's fix approval still happens on its own terms.

Otherwise (proactive invocation), call `AskUserQuestion` once, naming the selected bug:

- Question: "Fix bug #<N>: <title>? This will diagnose the root cause, modify code test-first, and on confirmation archive the bug and make one commit (no push)."
- Options: **Proceed** (recommended) / **Pick a different bug** / **Cancel**.

If the user picks Cancel (or anything non-affirmative), stop with no changes. If they pick a different bug, return to Step 0 with their choice.

## Step 2 — Ground yourself in the codebase

Build an accurate mental model before forming any theory. Read, don't skim:

- The code paths the bug's triage points at — and read them **end to end**, following the actual control flow, not just the named function. (Per the debugging discipline: understand the path fully before hypothesising.)
- Project orientation: `README`, `CLAUDE.md`, and any `docs/` relevant to the affected area.
- **The last feature.** Check `features/` for the highest-version `feature-v<N>-*` folder and skim its design / plan / implement notes — a freshly shipped feature is a common source of new bugs, and its docs explain intended behaviour.
- **The intent document, whenever the report questions whether the behaviour is a defect at all.** If it reads as "is this broken, or is this how it's meant to work?" — or borders on a feature request — go to whatever states intent for *that* area (the original design or goals doc, that feature's own design under `features/`, a product spec), not just the most recent feature. Explicit documented intent is what turns Step 4's works-as-intended disposition into an evidence-backed close rather than an opinion.
- Recent history around the affected files: `git log --oneline -10 -- <path>` and `git log -p -1 -- <path>` where useful, to see what changed and why.

Detect the project's tooling so you can run tests later — language-agnostic, read it from manifests + CI config (e.g. `package.json` scripts, `Makefile`, `pyproject.toml`, `cargo`, CI workflow files). Record the commands you'll reuse: `TEST`, and where they exist `LINT`, `TYPE_CHECK`, `BUILD`.

Establish a **baseline**: run `TEST` (and `LINT` if quick) and record what already passes/fails. Pre-existing unrelated failures are not yours to fix and must not later be mistaken for a regression caused by your change. **Start that run in the background before the reading above, not after it.** None of the grounding depends on its result, so a slow suite otherwise stalls the run for minutes doing nothing; collect the result before you start diagnosing in Step 4. Its role as the regression reference is unchanged.

## Step 3 — Review the bug and clarify with the user

**This step is mandatory even in auto / non-interactive mode.** If the harness told you to "work without stopping" or "skip clarifying questions", that does not apply here — fixing the wrong thing wastes far more time than one round of questions.

Decide whether the report leaves material ambiguity: unclear expected behaviour, fuzzy repro steps, multiple plausible interpretations of "broken", missing environment/version, or a symptom that could map to more than one feature.

- If there is no material ambiguity, say so in one line and continue to Step 4.
- Otherwise ask. **Prefer `AskUserQuestion`** with concrete, mutually-exclusive options and a **recommendation** (put the recommended option first, label it "(Recommended)"), because you can usually frame the ambiguity as a choice ("Which is the expected behaviour when X?", "Which environment did you see this on?"). Fall back to a plain chat question only for genuinely free-form input (e.g. "paste the exact error"). Keep it to one focused round where possible.

Fold the answers into your understanding of the bug before diagnosing.

## Step 4 — Diagnose the root cause (fact-driven — no guessing)

This is the gate the whole skill turns on. **Find the root cause, supported by evidence, before you change a single line of production code.**

- Do not assume and do not invent hypotheses you can't test. Every claim about the cause must be backed by something you observed: a reproduction, a failing assertion, a log line, a value you printed, a code path you traced.
- **Don't anchor on the triage.** The report's triage is a quick first read and may name a plausible-but-wrong cause or differentiator. When it asserts a specific factor, confirm or refute it empirically before theorising about mechanism — build a minimal controlled matrix (the suspected factor × an orthogonal control) and observe which cell actually reproduces, rather than reasoning forward from the triage's hypothesis.
- Reproduce the bug if at all possible — run the failing command, write a throwaway probe or a (soon-to-be-permanent) failing test, add temporary instrumentation. Capture the exact observed-vs-expected behaviour.
- If you cannot reach a confident root cause: run more tests/experiments, widen the trace, or **ask the user for help** (logs, exact repro, environment, a screen recording). Asking is correct; guessing is not.
- Remove any temporary instrumentation you added once you have your answer.

Only proceed to Step 5 when you can state the root cause concretely — citing `path/to/file.ext:line` and the evidence. If after honest effort you still can't, tell the user what you found, what you ruled out, and what you'd need from them; do **not** proceed to a speculative fix.

**No-fix disposition.** If the evidence-backed conclusion is that the bug should *not* be fixed — works-as-intended, a duplicate, or cost unjustified by measured impact (record the measurement) — there is a parallel close path. Skip Step 5's fix approval and Step 6's TDD; confirm the disposition with the user via `AskUserQuestion` (**Close as <disposition>** / **Fix it anyway** / **Cancel**), then close as in Step 9 but with an evidence-backed `## Resolution` recording the disposition in place of a code fix, and commit with `chore(bug #<N>): <disposition> — <short title>` instead of `fix(...)`. Archiving and tracker regeneration are unchanged.

## Step 5 — Explain the fix and get approval

Tell the user, at whatever length the fix needs to be judged:

- **Root cause** — one or two sentences, with the evidence.
- **Proposed fix** — what you'll change and in which file(s), and why it addresses the root cause (not just the symptom).
- **How you'll verify** — the regression test you'll add, and any manual check needed.

Then ask for approval via `AskUserQuestion`: **Proceed** (recommended) / **Adjust approach** / **Cancel**. If they want adjustments, incorporate them and re-confirm. If they cancel, stop with no code changes. Keep the fix scoped to the root cause — do not bundle refactors, cleanups, or unrelated improvements (raise those separately if they matter).

## Step 6 — Implement the fix, test-first (TDD)

Follow the standard TDD cycle without exception:

1. **Red.** Write a test that encodes the correct behaviour the bug violates (a regression test). Run it and confirm it **fails** for the expected reason — this proves the test actually captures the bug. If the fix introduces a not-yet-existing symbol (a new type, function, or module the test references), a bare "symbol not found" compile/import error is **not** a meaningful Red — first add a minimal stub that compiles and returns a trivially-wrong value, so the failing test is a real assertion failure that proves the test captures the behaviour.
2. **Green.** Make the **minimal** change at the root cause to make that test pass. No scope creep, no speculative hardening.
3. **Refactor (only if needed).** Tidy strictly what you just touched, keeping tests green.
4. **No regressions.** Run the full `TEST` suite plus `LINT` / `TYPE_CHECK` / `BUILD` where they exist. Compare against the Step 2 baseline — anything green before must still be green. Pre-existing unrelated failures stay as they were (don't fix-and-bundle them here).

When the obvious assertion for a bug is unreliable, ground the regression test in an observed, deterministic signal instead of a guessed or flaky one. For visual / layout / geometry bugs, first run a throwaway probe that dumps the framework's *measured* values and assert against those, rather than against guessed pixel thresholds (which are usually wrong and cause red-green-red churn). For performance / scaling bugs, assert on a proxy for the work done — items processed, regions invalidated, calls made — and that it stays bounded as input grows, rather than on wall-clock time.

If the bug genuinely has no automatable layer (pure visual/UI, external-only behaviour), still add a test at whatever layer *is* testable; Step 7 covers the human check for the rest. Never skip writing the test just because the top layer is hard to reach.

## Step 7 — Verify the resolution

- If automated tests fully exercise the fixed behaviour and they pass, the resolution is verified — note which tests cover it.
- For UI / frontend changes, where you can, run the app (start the dev server, exercise the feature, watch for regressions) before declaring success.
- If you **cannot** verify automatically (UI rendering you can't drive, an external system, a visual judgement), ask the user to test. Give precise steps to reproduce and what "fixed" looks like, then confirm via `AskUserQuestion`: **Confirmed fixed** / **Still broken** / **Partially fixed**. Wait for their answer — do not assume success.

## Step 8 — If unresolved, loop back to diagnosis

If the regression test still fails after your change, or the user reports the bug remains (or only partially resolved), **return to Step 4** — re-diagnose with the new evidence in hand (what the failed attempt ruled out is itself a fact). Do not pile speculative patch on speculative patch.

Bound the loop: if repeated honest attempts don't converge, stop and tell the user plainly what you've tried, what each attempt ruled out, and what you need from them. Thrashing helps no one.

## Step 9 — Close the bug and commit

Only reach this step once the resolution is **confirmed** (Step 7).

**9a — Append the resolution to the report.** Add a `## Resolution` section to the end of `report_file` (just before, or replacing, the trailing "Filed via …" footer is fine — keep the footer line):

```markdown
## Resolution

- **Resolved:** <YYYY-MM-DD>
- **Root cause:** <evidence-backed, one or two lines, cite path/to/file.ext:line>
- **Fix:** <what changed, and the file(s) touched>
- **Verification:** <the regression test(s) by name, and/or "user confirmed">

**Lessons learned:** <anything worth remembering — a fragile pattern, a missing test, a surprising interaction. One to three bullets, or "none.">
```

**9b — Archive the bug folder.** Move it from open to closed:

```bash
mkdir -p "<repo_root>/bugs/archive"
mv "<repo_root>/bugs/bug-<N>-<slug>" "<repo_root>/bugs/archive/bug-<N>-<slug>"
```

(Plain `mv` — the folder may contain not-yet-tracked images; staging happens at commit. No symlinks.)

**9c — Regenerate the tracker.** Invoke the `bug-tracker-render` skill via the `Skill` tool (no arguments). The bug now renders under **Closed**. If it returns a `skipped — …` status, surface that one-line note and continue.

**9d — Commit (one commit, no push).** Stage the fix and the bug-tracking changes, then commit:

```bash
git add <changed source + test files>
git add "<repo_root>/bugs"        # captures the archive move + regenerated tracker
git commit -m "fix(bug #<N>): <short bug title>"
```

Keep the first commit line under 72 characters. Do **not** stage unrelated modified/untracked files, and do **not** push. If a pre-commit hook fails, fix the underlying issue and create a new commit (never `--no-verify`). Record the commit short-sha.

## Step 10 — Capture lessons

Invoke the `lessons-capture` skill in this plugin via the `Skill` tool with the single argument `bug-fix`. It runs the reflection protocol, appends a dated entry to `~/.claude/dev-skills/lessons/bug-fix.md`, and returns the entry body for the highlights below. Do not run the reflection inline — `lessons-capture` is the single source of that protocol.

Then output a short, scannable summary in chat (under ~20 lines):

```
Fixed bug #<N>: <title>  →  archived to bugs/archive/bug-<N>-<slug>/
Commit: <short-sha>  (not pushed — run /push when ready)

**Root cause:** <one line>
**Fix:** <one line, file(s)>
**Verified by:** <test name(s) or "user confirmed">

**Skill-improvement recommendations**
- <single item from Step 10, or "No skill-improvement recommendations from this run.">
```

## Constraints (non-negotiable)

- **Root cause before fix.** Step 4 is a hard gate: no production-code change until the cause is established with evidence. Never ship a speculative fix; if unsure, run more tests or ask the user.
- **Test-first, always.** Step 6 writes a failing test before the fix and confirms it goes green after. The fix is the **minimal** change at the root cause — no bundled refactors or unrelated changes.
- **Mandatory clarification.** Step 3 runs even under autonomous instructions. Prefer `AskUserQuestion` with options + a recommendation; fall back to chat only for free-form input.
- **One bug per invocation.** Fix exactly the selected bug. If you discover adjacent bugs, note them for the user (suggest `/bug-submit`) rather than fixing them in the same run.
- **Current branch only; one commit; no push.** Never create a branch, never push. Exactly one commit, made only after the resolution is confirmed. Never use `--no-verify` or bypass signing.
- **No regressions.** Honour the Step 2 baseline — anything passing before must still pass. Don't silently "fix" pre-existing unrelated failures inside this run.
- **The tracker is rendered, not hand-written.** Closing a bug means moving its folder to `bugs/archive/` and invoking `bug-tracker-render` — never hand-edit `bugs/bugs-tracker.html`.
- **No open bug ⇒ clean stop.** If there's nothing to fix, report it and hand over to `/bug-submit`. Don't invent work.
- **Language-agnostic.** Detect and reuse the project's own tooling; don't assume a specific stack.
- **Lessons capture runs every time.** Step 10 always invokes `lessons-capture`; whether it yields a recommendation or "none this run" is that skill's call.
