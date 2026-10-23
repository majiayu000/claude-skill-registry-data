---
name: analyzer-review
description: Review analyzer changes against this project's product rules (say what it means, findings lead to an action, answer first, forgiving input, honest about limits and cost, no tracebacks, discoverable) and its hard constraints (no imports between analyzers, shared code in _kit, boto3 + stdlib at import, read-only, Python 3.10 floor, pandas 2 and 3). Use before committing or opening a PR, or to audit one existing command.
argument-hint: "[base ref (default: uncommitted changes) | View command name, e.g. dynamodb.schema]"
---

# Analyzer review

Target: `$ARGUMENTS`.

## 1. Scope

- **Empty.** Review the uncommitted changes: `git diff HEAD` plus untracked files under `src/aws_analyzer/`, `tests/`,
  `docs/` and `README.md` (`git status --short`).
- **A git ref** (`main`, `HEAD~3`, a SHA). Review `git diff <ref>...HEAD` plus the uncommitted changes.
- **`<service>.<command>`** (`s3.what_if`, `dynamodb.schema`). Review that command end to end: its View method,
  its analyzer method, the pure functions and findings it uses, its tests, and its README and docs entries.

List the View commands the scope adds or changes. Those get the output review in step 3.

## 2. Mechanical checks

```bash
.venv/bin/python .claude/skills/check/rules.py --apis
```

`rules.py` covers read-only calls, lazy imports, imports between analyzers, copies of `_kit` helpers (and, in the
Bedrock pair, of `_bedrock/`'s), banners,
View decoration and docstrings, and
IAM permissions missing from the README. Report its errors, and any warnings the change caused. It can't see a
helper copied from one service into another: when the change adds a function another service has too, say whether
it's the same code (it goes in `_kit/`, or `_bedrock/` for the Bedrock pair) or a different thing under the name.

Don't run the whole test suite here. That's `/check`'s job. Suggest it at the end if it hasn't been run since
the change.

## 3. Read the output as the user

For each added or changed command, run the one-argument call and one call with options through the demo:

```bash
.venv/bin/python .claude/skills/demo/demo.py <service> 'ui.<command>(...)'
```

Read the output as a data scientist in a notebook who is not an AWS expert. Check each rule in CLAUDE.md's
"Product goal" against the actual output and the code behind it:

- **Say what it means.** Is it plain-English sentences, or raw codes, ARNs, JSON or DynamoDB types? Is jargon
  explained where it first appears? Is the raw form still reachable as a secondary view?
- **Findings lead to an action.** Is every finding a `(level, message)` pair that says what's wrong, why it
  matters, the monthly price where one can be computed, and a next step: a command, a setting, or the exact
  call to copy? Is `warn` reserved for things worth acting on? Are they shown as one `_Findings` panel, and does
  the report end with a `_Next` block whose calls are filled in from the result and run as written?
- **Answer first.** Is there a title with a subtitle that says what was read, then three to six cards with the
  deciding number, then the tables? Are the units ones people know (`human_size`, `human_money` per month,
  `human_age`, commas)? Watch for raw bytes, epoch times, `Decimal` or `{"S": ...}`.
- **Forgiving input.** Does it accept `s3://b/p` and `b/p`, `"10MB"`, `"7d"` / `"2024-05-01"`, `"10k"`, and
  wrong-typed key values? Is the one-argument call useful on its own?
- **Honest about limits and cost.** Are estimates labelled, with the price basis shown? Are partial results
  labelled ("stopped at limit=...")? Do expensive scans stop early by default? Does the command show what it
  read or cost?
- **No tracebacks.** Is the View method `@_friendly_errors`? Is a config section the caller can't read recorded
  in `errors`, so it shows as a note that names the missing permission? Does a missing optional package go
  through `_require`? Is there a readable error for bad input (`ValueError` with a hint)?
- **Discoverable.** Does the docstring's first paragraph read well in `ui.help()`, and is the command in the right
  `_GROUPS` entry? Is the name what a user would guess, and consistent with the neighbouring commands?

## 4. Constraints rules.py can't see

- **Python 3.10.** Look for stdlib that is newer than 3.10: `datetime.UTC`, `tomllib`, `typing.Self`,
  `enum.StrEnum`, `ExceptionGroup` / `except*` (3.11), `itertools.batched`, `Path.walk` (3.12), and
  `compression.zstd` (3.14) unless it's guarded.
- **pandas 2 and 3.** pandas 3 turns on copy-on-write (chained assignment silently does nothing) and makes `str`
  the default string dtype (so `dtype == object` checks and `.astype(object)` assumptions break). Look for
  `inplace=True` on slices and for anything else that behaves differently between the two.
- **IPython 8 and 9.** Only `IPython.display` and `get_ipython` are used. Flag anything else.
- **Read-only.** Look beyond API calls too: no local side effects either (no files written outside a path the
  user passed, and no environment changes).
- **Blocks.** A new block type registers both drawings, `@_draws(_Block, "html")` and `@_draws(_Block, "text")`,
  and shows in a text-mode test: one without a text drawing becomes a "Part of this report isn't shown" note.
- **Windows.** A change to an explorer or the chat window goes through `_kit/window.py` (CLAUDE.md, "The windows'
  kit"): callbacks through `_safely`, its commands through `@_window_errors`, AWS read off the loop with `_later`
  (a stale result dropped by its key), HTML widgets set with `_set`, and nothing copied from another window. Its
  tests click and type through it, and drive any background path inside `asyncio.run`.
- **Tests.** Pure logic is tested without moto. There's a text-mode UI test, and a failure-path test where one
  exists. Tests don't depend on the real clock or on network access.
- **Docs.** Check the README command table, "Getting the data", the pure-function list and the IAM paragraph;
  `docs/<service>.md` (the command reference and permissions); and CLAUDE.md if a convention changed.

## 5. Report

Group the findings:

1. **Must fix.** Constraint violations, anything that writes, tracebacks a user can hit, wrong numbers, and
   Python 3.10 or pandas-2/3 breakage.
2. **Should fix.** Gaps in the product rules: missing next steps, raw units, an unlabelled estimate, an unhelpful
   default.
3. **Nits.** Wording and naming.

For each finding, give the `file:line`, what the user would actually see (quote the demo output), and the
concrete fix. End with anything reviewed that is fine but worth knowing. Don't edit files unless the user asks.
Then offer to fix the must-fix and should-fix items.
