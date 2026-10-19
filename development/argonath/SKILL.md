---
name: argonath
description: Use when the user runs /argonath [project] [--quick]. Default mode weighs the about-to-be-pushed diff; the `project` verb weighs the standing project tree instead. Runs the project's lint/format/build/test toolchain, scans for secrets, dry-runs the merge against the resolved target branch and probes it for semantic-drift risk the textual merge cannot see — escalating to a real test run on the merged tree, in a throwaway worktree, when that probe fires (all three diff mode only) — then invokes /nazgul and /mithrandir as advisory rows. Aggregates everything into one Pass / Hold verdict. Report only — never runs `git push`.
purpose: Weighs a diff or the project tree against lint, build, test, secrets, and advisory checks before a push.
user_invocable: true
stage: weigh
composes: nazgul:dispatch, mithrandir:dispatch
---

# Argonath — Pre-Push Analysis

The twin pillars at the river-gate. Before code crosses, render a verdict on whether it should pass. Report only — the skill never invokes `git push` itself.

## Argument Parsing

Arguments: `/argonath [project] [--quick]`

- No verb → diff mode. Weighs the about-to-be-pushed diff (`@{upstream}..HEAD`). Full run includes artefacts + secret scan + merge check + advisory rows.
- `project` verb → project mode. Weighs the standing project tree, not a diff. Useful on master/main, on a fully pushed branch, or when no commits have been made yet.
- `--quick` → skip the two sub-skill advisory rows (Rubric, Verdict) and the merged-tests escalation. Faster; only artefact commands, the secret scan, and (diff mode) the merge check and the drift probe. The drift probe survives `--quick` because it costs a `rev-list` and two name-only diffs, not a sub-skill dispatch — it still reports the risk, it just does not act on it.

## Workflow

### 1. Verify a git repo

```bash
git rev-parse --show-toplevel
```

If it errors, stop:
> Not in a git repo — nothing to analyse.

Capture branch and upstream:

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
git rev-list --count '@{upstream}..HEAD'
```

If no upstream is configured, mark the header `· no upstream`.

### 2. Resolve commands

```bash
~/.claude/hooks/argonath-detect.sh
```

Returns JSON: `{stack, lint, format, build, test, install, test_scope, source}`. If `stack` is `unknown` and every command is empty, render every artefact row as `⚪ skipped — no command`, run the secret scan and advisory rows, and finish.

`install` is not an artefact row and is never run here — this tree is already installed. It belongs to step 7, which materialises a fresh checkout that carries none of the project's dependencies.

When `source` is `override` or `merged`, append `(via .skadi/argonath.yaml)` after the stack name in the header.

### 3. Run artefact steps

For each non-empty command (`lint`, `format`, `build`, `test`), call:

```bash
~/.claude/hooks/argonath-run.sh <label> <command...>
```

Labels: `Lint`, `Format`, `Build`, `Tests`. Capture each JSON result. The hook always exits 0; read `ok` from the JSON.

The `format` command is a **check**, not a fix — it carries `--set-exit-if-changed`, so it exits non-zero when files are unformatted and the row fails. Argonath never rewrites the tree it grades.

Empty command → render the row as `⚪ skipped — no command`.

If `test_scope` is `changed`, the project's test command runs as configured — Argonath does not transform it. The override file is the place to express scope.

**Test secrets.** A suite that needs credentials names them as `{{NAME}}` placeholders in its override command — e.g. `test: fvm flutter test --dart-define=testAccount={{TEST_ACCOUNT}}` — and declares each one in the repo's `test_env.md` in Skadi state (`~/.claude/hooks/skadi-state.sh path "${SKADI_PROFILE:-default}" "$PWD" test_env.md`), one `NAME=secret:<item>:<field>` line apiece. `argonath-run.sh` resolves them through `secret.sh`; the row's `command` keeps the placeholder and the log masks the value. When the file or a name is missing, the row fails before the suite runs and its summary names the path to write — render that summary as it stands, never as failing tests. A mass failure confined to one directory whose test config calls `fail(…)` for missing credentials is the same missing secret: say so, rather than calling the suite broken.

### 4. Secret scan

Diff mode — resolve the target here, by step 5's order: run that `rev-parse` chain and pass the **name** that resolved (`master`, `main`, or `origin/HEAD`), not the SHA it prints. If none resolves, call the hook with no argument:

```bash
~/.claude/hooks/argonath-secrets.sh <target>
```

Project mode:

```bash
~/.claude/hooks/argonath-secrets.sh --project
```

Returns JSON `{ok, count, hits, note}`. In diff mode the scanned range is everything the branch brings to its target — `<merge-base>..HEAD` — whether pushed or not. Standing on the target itself, or with no target resolved, it falls back to `@{upstream}..HEAD`, and with no upstream either, to everything `HEAD` carries; the `note` names the range read. A branch with no commits beyond its target and no upstream thus scans the whole tree, so an old committed secret can raise a Hold there; in project mode every tracked file is scanned, untracked / `.gitignore`d paths excluded.

`ok: false` with `count: 0` means the scan could not run at all — a root it could not enter, or a `git diff` (diff mode) or `git grep` (project mode) that failed. Render the row `🚫` with the hook's `note` as its detail, never as a clean pass and never as "0 hits".

### 5. Merge check (diff mode only)

Project mode has no other branch to merge into — render the row `⚪ skipped — no project mode`, the same shape as the Verdict row, and skip the rest of this section.

Diff mode resolves the target the same way `/mithrandir` already does — the first of `master`, `main`, `origin/HEAD` that exists locally:

```bash
git rev-parse --verify --quiet master \
  || git rev-parse --verify --quiet main \
  || git rev-parse --verify --quiet origin/HEAD
```

If none resolves, or the current branch **is** the resolved target, render the row `⚪ skipped — no target` — there is nothing to probe.

Otherwise:

```bash
~/.claude/hooks/argonath-merge-check.sh <target>
```

Returns JSON `{ok, conflicted_paths, note}`. The probe runs `git merge-tree --write-tree` — a purely in-memory computation that never touches the working tree or the index, so it is safe to run regardless of what else this step has checked out. `ok: false` names a genuine textual conflict against the target's current tip; render the conflicting paths (comma-joined, capped at 3 with a `+N more` tail) in the detail column.

The hook can also return `ok: true` with a `note` ending in `— skipped` or `unavailable or errored` — its own internal degrade for a git too old to carry `--write-tree`, or any other `merge-tree` failure that never produced a `CONFLICT` line. Render that case as `⚪ skipped — <note>`, not `✅` — only a `note` of `"clean merge against <target>"` is a genuine pass.

On that genuine pass, the detail column reads `no textual conflict` — not `clean`. The probe compared hunks and found none overlapping; it did not build the merged tree, run its tests, or otherwise establish that the merge is sound. `clean` invites the reader to conclude the second thing from the first. Step 6 exists for exactly the gap that phrasing used to hide.

### 6. Drift probe (diff mode only)

The merge check reads hunks: it answers whether the two sides collide *textually*. A merge can be textually clean and still break — the branch swaps the test framework while the target adds tests in the old one; the branch bumps a dependency while the target adds code against the old API; both sides add a migration bearing the same version. Neither side touched the other's lines, so `merge-tree` sees nothing. The drift probe names that risk without merging anything.

Project mode has no target to drift from — render the row `⚪ skipped — no project mode` and skip the rest of this section. Reuse the target resolved in step 5; when none resolved, or the current branch **is** the target, render `⚪ skipped — no target`.

Otherwise:

```bash
~/.claude/hooks/argonath-drift.sh <target>
```

Returns JSON `{ok, moved, signals, note}`. The probe is two-layered, cheapest first: it asks whether the target has moved at all since the branch point (a target standing still carries no risk — there is nothing new to collide with), and only then whether either side's changes land on one of three surfaces where a silent collision is known to hide — `dependency` (a manifest or lockfile, either side), `test-config` (a test-runner config, either side), `migration` (a migrations directory, *both* sides, since a version collision needs two). Each signal carries its `kind`, its `path`, and the `side` that moved it (`branch`, `target`, or `both`).

Render by outcome:

- `moved: 0` → `⚪ skipped` with the detail `target unmoved since branch point`
- `ok: true` with `moved > 0` → `✅` with the detail `target moved <N> commits, no risk signal`
- `ok: false` → `⚠ ` with the signal paths and the tail `— escalated`. Each path carries its side in parentheses — `pubspec.yaml (both sides)`, `vitest.config.ts (target)` — because which side moved a shared surface is half of what makes it worth reading. Comma-join them, capped at 3 with a `+N more` tail, the same cap the merge row's conflicting paths use

A fired signal is a **risk, not a proven failure** — the probe never ran a test. It is advisory: it never holds the verdict, whatever it found. What it does is decide whether step 7 runs at all. A quiet drift is the common case, and it is the reason the expensive probe stays unpaid for: nothing is merged, nothing is checked out, nothing is installed.

### 7. Merged tests (diff mode only, and only when drift fired)

Steps 5 and 6 both read and neither runs. This step is the escalation, and the only one that actually settles the question: it materialises the merge result and puts the project's own tests to it.

It runs **only** when step 6 returned `ok: false`. There is no flag to reach for and none to remember — a quiet drift means there is nothing to verify, and the merge is never performed. Render the row:

- project mode → `⚪ skipped — no project mode`
- no target resolved, or the current branch **is** the target → `⚪ skipped — no target`
- drift returned `moved: 0` or `ok: true` → `⚪ skipped — no drift risk`
- `--quick` → `⚪ skipped — --quick`

Otherwise:

```bash
~/.claude/hooks/argonath-merged-test.sh <target>
```

Returns JSON `{ok, ran, stage, stack, command, summary, log, note}`. The hook computes the merged tree in memory, wraps it in an unreferenced commit, and checks that out in a throwaway `git worktree` — the caller's working tree and index are never touched. Inside that worktree it **re-detects the toolchain**, installs, then tests. The re-detection is the point: when the merge is what changes the test framework, the old framework's command would prove nothing. Dependencies are installed there rather than copied from this tree, because a manifest that changed in the merge is exactly the case being tested.

Render by outcome:

- `ran: false` → `⚪ skipped — <note>` (no test command on the merged tree, a textual conflict the merge row already owns, or a materialisation that failed)
- `ok: true` → `✅` with the detail `<command> on the merged tree — all green`
- `ok: false` → `🚫` with the detail `<command> on the merged tree — <summary>`, and name the failing `stage` when it is `install`

Unlike drift, this row **is a gate**. It ran the tests; a failure here is proven, not suspected, and it holds the verdict.

A run costs an install and a full test pass on a cold checkout — often slower than every other row combined. That cost is why step 6 stands in front of it.

### 8. Advisory rows (skip when `--quick`)

Invoke the two existing skills as sub-skills via the Skill tool, but fold each into a single row only.

- **Rubric** —
  - Diff mode → invoke `/nazgul` (default verb, scope=diff). Read its pass/fail tally; render `<P> pass · <F> fail`.
  - Project mode → invoke `/nazgul project`. Same row shape.
- **Verdict** —
  - Diff mode → invoke `/mithrandir branch`. Read the tier (`sound` / `wavering` / `off`) and the one-line reasoning paragraph; render `<tier> — <≤60-char excerpt>`.
  - Project mode → `/mithrandir` has no project verb, so render the row as `⚪ skipped — no project mode`.

If either errors out, render its row as `⚠  unavailable — <short reason>` and continue.

### 9. Aggregate

- **Pass** — every artefact step `ok` or `skipped`, secret scan returned `ok: true`, **and** the merge check and merged tests (where they ran) returned `ok: true` or were skipped.
- **Hold** — any artefact step `ok: false`, secret scan returned `ok: false`, the merge check returned `ok: false`, **or** merged tests returned `ok: false`.

Advisory rows (drift, rubric, mithrandir) **never** push the verdict off `Pass`. A skipped merge check (project mode, or no target resolved) never holds the verdict either — it is a skip, not a finding. The drift probe never holds it under any outcome: it reports a risk it has not tested, and an untested risk is not a failing gate.

### 10. Render

Lead with a blockquote summary line, then the table. The blockquote echoes the verdict so the reader gets the conclusion in one breath.

Diff mode:

```
> Hold — tests must pass before crossing.

Argonath  master · 3 commits ahead of origin/master · stack: flutter
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Lint            fvm flutter analyze                          0 issues
  ✅ Format          fvm dart format --set-exit-if-changed .      clean
  ✅ Build           fvm flutter build apk --debug                ok
  🚫 Tests           fvm flutter test                             4 failing in test/dos_step3_test.dart
  ✅ Secret scan     no tokens / .env values in diff
  ✅ Merge           dry-run vs master                            no textual conflict
  ⚠  Drift          pubspec.yaml (both sides)                    — escalated
  🚫 Merged tests    fvm flutter test on the merged tree          2 failing in test/api_client_test.dart
  ✅ Rubric          /nazgul: 9 pass · 0 fail
  ⚠  Verdict        /mithrandir: wavering — proportion drifts wide
───────────────────────────────────────
  5 of 7 gates clear · 2 advisory notes
```

Project mode:

```
> Pass — project tree clear, no obstacles found.

Argonath  master · up to date with origin/master · stack: flutter · mode: project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Lint            fvm flutter analyze                          0 issues
  ✅ Format          fvm dart format --set-exit-if-changed .      clean
  ✅ Build           fvm flutter build apk --debug                ok
  ✅ Tests           fvm flutter test                             all green
  ✅ Secret scan     no tokens / .env values in tracked files
  ⚪ Merge           skipped — no project mode
  ⚪ Drift           skipped — no project mode
  ⚪ Merged tests    skipped — no project mode
  ✅ Rubric          /nazgul project: 9 pass · 0 fail
  ⚪ Verdict         skipped — no project mode
───────────────────────────────────────
  7 of 7 gates clear · 0 advisory notes
```

Symbols:

- `✅` — passed (`ok: true`)
- `🚫` — failed (`ok: false`)
- `⚪` — skipped (no command, no project-mode counterpart, no resolvable merge target, or `--quick` mode for advisory rows)
- `⚠ ` — advisory tier below `sound` / unavailable, or a drift risk signal

Header line carries: `<branch> · <ahead-state> · stack: <stack>` and `(via .skadi/argonath.yaml)` when relevant. In project mode, append ` · mode: project` after the stack name so the scope is plain.

`<ahead-state>`:
- `<N> commits ahead of <upstream>` when `N > 0`
- `up to date with <upstream>` when `N == 0`
- `no upstream` when not tracking

Footer line: `<P> of <T> gates clear · <A> advisory note(s)` — counts the artefact + secret + merge + merged-tests rows toward the gate count, a skipped row counting as clear; advisory rows (drift, rubric, verdict) are tallied separately, and only those that actually flagged count toward `<A>`.

Verdict-summary line in the blockquote follows /mithrandir's spirit:

- Diff mode:
  - `> Pass — every gate clear, the road is open.`
  - `> Hold — <plain reason: tests must pass / secrets removed / both>.`
- Project mode:
  - `> Pass — project tree clear, no obstacles found.`
  - `> Hold — <plain reason>.`

When `stack: unknown` and every artefact row was skipped, the verdict still resolves on the secret scan alone. If clean: `> Pass — toolchain unknown, but no obstacles found.`

## Rules

- Read-only — never runs `git push`, `git commit`, `git tag`, `git push --tags`, or any state-mutating tool beyond the artefact commands themselves
- Artefact commands are taken at the user's word — if `.skadi/argonath.yaml` configures something destructive as the test command, the skill runs it; the override file is the user's responsibility
- The full step log lives in the tempfile path emitted by `argonath-run.sh`. Do not read it unless the user asks for the failure detail
- Sub-skills (`/nazgul`, `/mithrandir`) are advisory — never block the Pass/Hold verdict on their findings
- Sort the body rows in the order: Lint → Format → Build → Tests → Secret scan → Merge → Drift → Merged tests → Rubric → Verdict. Hide a row only if it is `--quick`-suppressed
- Project mode scans tracked files only — untracked / `.gitignore`d paths stay out of the secret scan, and the verdict row is always `⚪ skipped` (no `/mithrandir` project verb exists)
- Project mode has no target tree to probe either — the merge, drift, and merged-tests rows are always `⚪ skipped — no project mode`
- The merge check never mutates the tree — `git merge-tree --write-tree` computes entirely in memory. If it ever needs a fallback for a git older than 2.38, that fallback must preserve the same guarantee; a real `git merge --no-commit` against the working tree is not an acceptable substitute inside a read-only skill
- The merge row proves only that the two sides do not collide *textually*. Its detail column reads `no textual conflict`, never a bare `clean` — a reader who takes it for "the merge is fine" has been misled by the skill, and the drift row exists because that reading was too easy to make
- The drift probe merges nothing and checks nothing out — it reads refs and name-only diffs, the same read-only guarantee the merge check carries. A signal it raises is a risk it has *not* tested; never render it as a proven failure, and never let it hold the verdict
- The drift probe survives `--quick` while the two sub-skill advisory rows do not. It costs one `rev-list` and two name-only diffs, so the reason `--quick` exists does not apply to it
- Merged tests run only on a fired drift signal, and never under `--quick`. There is no flag to force them: a flag would have to be remembered, and the run it guards is expensive enough that nobody would reach for it on the day it mattered. The drift signal is the trigger precisely so the decision is not the user's to make twice
- Merged tests are a **gate**, not an advisory row — alone among the merge-adjacent rows they actually executed something, so alone among them they may hold the verdict. Drift's own signal never holds it, however loud
- The merged-tree probe never mutates the caller's tree either: it computes the tree in memory, wraps it in an unreferenced commit, and checks that out in a throwaway `git worktree` it tears down on every exit path. A real `git merge` or `git checkout` against the working tree is not an acceptable substitute, the same rule the merge check carries
- The merged tree's toolchain is re-detected inside that worktree, never inherited from this one. A merge that swaps the test framework is the case the probe exists for, and the old framework's command would prove nothing about it
