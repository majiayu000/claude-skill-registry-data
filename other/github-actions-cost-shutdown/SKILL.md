---
name: github-actions-cost-shutdown
description: "Use when an owner reports a surprise GitHub Actions bill, asks which repo is spending the minutes, wants CI replaced by tests run locally, or bans automatic git actions and Dependabot PRs. Also when the billing API returns HTTP 410 (endpoint moved), a local gate prints PASS while skipping phases because CI is set in the shell, or a trigger change must land on a remote far ahead of a dirty clone."
---

# GitHub Actions cost shutdown

Goal: zero automatic Actions spend, one local gate that covers every CI job, and a
number-backed answer to "why was my bill $N".

## 1. Measure before touching anything

Never accept the owner's attribution of the cost, and report whatever part of the
bill the measurement does not explain. Public repos on standard runners are free, so
first confirm the repo is private
(`gh repo view OWNER/REPO --json name,visibility,owner`). Private repos draw on the
plan's included minutes (2,000 a month on Free, 3,000 on Pro) and bill the overage
(GitHub docs, verified 2026-09-24).

The per-user endpoint `users/<user>/settings/billing/actions` is **gone**
(`HTTP 410 {"message":"This endpoint has been moved."}`). Use the per-repo, per-SKU
billing usage endpoint:

```bash
for m in 8 9; do echo "== month $m =="; gh api "users/<user>/settings/billing/usage?year=2026&month=$m" \
  --jq '.usageItems[] | select(.repositoryName=="<repo>") | [.sku, .quantity, .grossAmount, .netAmount] | @tsv' \
  | awk -F'\t' '{q[$1]+=$2; g[$1]+=$3; n[$1]+=$4} END {for (k in q) printf "%-22s qty=%10.2f gross=$%7.2f net=$%7.2f\n", k, q[k], g[k], n[k]}'; done
```

- Read `netAmount`, not `grossAmount`: the included allowance absorbs a chunk, so a
  gross estimate overstates the bill. `Actions storage` is usually `$0.00` net even
  with artifacts uploaded on every run; the money is nearly always `Actions Windows`,
  at ~1.7x the Linux per-minute rate ($0.010 vs $0.006 for 2-core, verified
  2026-09-24).
- Then attribute by trigger, the thing you are about to change:

  ```bash
  gh api "repos/<owner>/<repo>/actions/runs?per_page=100&created=>YYYY-MM-DD" --paginate \
    --jq '.workflow_runs[] | [.name, .event, .conclusion] | @tsv' | sort | uniq -c | sort -rn
  ```

  `276 CI push success / 235 CI push failure / 3 workflow_dispatch` is the whole
  finding: hundreds of billed runs, a third of them failures a local run would have
  caught in minutes.
- `dynamic` runs named `npm_and_yarn in /x ...` or `Graph Update: pip ...` are
  **Dependabot**, not any workflow file. Its own runs are free, but each
  security-update PR is an automatic git action that also triggers CI. Check with
  `gh api repos/O/R/automated-security-fixes`, disable with
  `gh api -X DELETE repos/O/R/automated-security-fixes`; alerts stay on
  (`gh api repos/O/R/vulnerability-alerts -i` returns 204). Check
  `.github/dependabot.yml` too.

`gh` shell traps on this box (verified 2026-09-24):

- git-bash rewrites a leading-slash endpoint with no query string into a path
  (`invalid API endpoint: "C:/Program Files/Git/repos/..."`). Drop the leading slash,
  as above.
- Windows PowerShell 5.1 strips the double quotes inside `-q '<jq>'` (e.g.
  `gh run view --json jobs -q '...'`); the filter then fails on stderr, which looks
  like no output when stderr is hidden. git-bash and
  pwsh 7 pass it intact. If a `-q` filter prints nothing, parse the `--json` output
  in Python.

## 2. Disable: remove triggers, never delete the workflow

Change `on:` to `workflow_dispatch:` only (delete `push`, `pull_request`,
`push: tags`). Keep the jobs so a clean-machine or Linux run can still be started by
hand; deleting the file throws away release packaging and any check that lives only
there.

- Header comment: the measured numbers and "do not re-add push:". Rewrite any comment
  that contradicts the new trigger, and drop dead `concurrency` comments about
  push/PR cost trade-offs.
- Verify with PyYAML. Bare `on` parses as boolean `True`, so read
  `d.get('on', d.get(True))`.
- A tag-triggered release still works when dispatched **with the tag as the ref**
  (`gh workflow run <release>.yml --ref vX`): `github.ref` is `refs/tags/vX`, so
  version resolution and an `if: startsWith(github.ref, 'refs/tags/v')` publish gate
  still fire. Say so in the header: `git push origin vX` muscle memory now publishes
  nothing.
- **Make the remaining workflow correct.** A step that could never pass is often why
  most runs failed. E.g. bare `ruff check` where lint is a *ratchet test* (a baseline
  count that may fall but must not rise, like `tests/test_lint_is_clean.py` with
  `RUFF_BASELINE = 29`) fails every run and stops the job before the tests start.
  Run the ratchet test instead.
- **The push that removes the trigger does not fire a run**: `push` events evaluate
  the workflow file *in the pushed commit*. Confirm the newest run's `head_sha` is
  still the previous commit:
  `gh api "repos/<o>/<r>/actions/runs?per_page=5" --jq '.workflow_runs[] | [.name,.event,.head_sha[0:8],.created_at] | @tsv'`
- Check other branches only for triggers without a branch filter. An old
  `push: branches: [master]` on a side branch never matched that branch anyway, and a
  PR from it evaluates the *merged* file, i.e. the fixed one.

## 3. Replace with ONE local gate that is a true superset

The critical failure is **silent coverage loss**. Enumerate every CI job and cover
each one, including checks that lived only in CI (architecture guards, lint,
backend/schema assertions) and suites CI never ran (such as vitest in package.json).
Run fast checks as an early phase: they fail in seconds, not after a build.

- **A missing dependency fails the phase.** With no `rg` on PATH the check must refuse
  to run, not pass on zero matches; an uninstalled linter is a failure, not a skip.
- **Resolve the interpreter the way the project's launchers do**, e.g.
  `$env:X_PYTHON`, then `.venv\Scripts\python.exe`, then `python`. System python
  often lacks ruff and pytest.
- **Lint = the project's real standard.** Run the ratchet test, not the bare linter.
- **Print parsed counts, not exit codes.** pytest: `--junitxml=<temp>`, read
  `testsuites.testsuite.{tests,failures,errors,skipped}`, then delete the file; no XML
  means collection crashed. Playwright: join the
  `^\s+\d+ (passed|failed|flaky|skipped|did not run)` lines. oxlint: count lines
  containing `: error `.
- **No `$env:CI` sniffing in the gate: the trap worth the whole skill.** Gate scripts
  commonly auto-enable a reduced "CI mode" from `$env:CI`, and agent shells, task
  runners and terminals set `CI` too, so a local "full" run silently skips the
  expensive phases (GPU/display smokes, integration) and still prints
  `GAUNTLET PASSED`. Make the flag explicit, pass it from the workflow, and comment
  why, or someone re-adds the sniff.
- **But set `CI=1` for the Playwright child only**, restoring it afterwards. Configs
  key `forbidOnly`/`reuseExistingServer` on it; without it a stray `test.only`
  shrinks the suite and a stale server on the port gets tested.
- In PowerShell 7, set `$PSNativeCommandUseErrorActionPreference = $false`. Wrap
  native calls with EAP=Continue while piping `2>&1 | Tee-Object`, then check
  `$LASTEXITCODE` yourself.
- **Reproduce what the Linux runner caught for free**: case-only filename collisions
  (`git ls-files | Group-Object { $_.ToLowerInvariant() }`).
- Service containers such as Postgres: `docker run`, poll until ready, tear down in
  `finally`.
- Android device suites: pin `ANDROID_SERIAL` and refuse a physical device unless one
  is named. `--no-device` should still compile the instrumented sources.
- Keep each file's existing EOL. Write new files in the house style (CRLF here).

## 4. Prove it: run the whole gate, no skip flags

Paste the phase table: a run that skipped the very phases the fix was about proves
nothing. A full gate (about 1,960 pytest tests plus Playwright) outruns the agent
bash tool's default timeout (omp: 300 s), so run it async, redirect to a log, and
read the report table from the end of the log.

Pre-existing failures are findings to report, not to fix unasked. Rule out two false
alarms first:

- A **stale test binary** fails against newer source/data: it asserts an old
  expectation (`REQUIRE( 2 == 1 )`) while the source at that line asserts the new
  one. Rebuild the test target before calling anything a repo regression.
- A build tree configured by an **older CMake** that has since been replaced fails at
  re-generate with mixed module dirs (`share/cmake-4.3/...` missing under 4.4).
  `cmake --preset <name>` reconfigures in place; objects survive, so the rebuild is
  incremental.

## 5. Sweep the claims CI used to back

Grep the docs for `CI`, `workflow`, `badge.svg` and "on every push". A workflow badge
freezes on its last status once runs stop, so swap in static badges. Fix release
instructions that say "push a tag" and stale notes about what the test runner does,
and add a short README "Checks" section giving the gate command.

## 6. Write the policy down

Add it to the repo's `AGENTS.md`/`CLAUDE.md`, or the next agent re-adds a trigger:
workflows stay `workflow_dispatch`-only, no automatic triggers, the gate command to
run instead, and no git hooks (a pre-push hook that runs a multi-minute gate gets
`--no-verify`'d, a fast variant that skips the build tests a stale binary, and any
pre-push hook blocks the owner's own pushes).

If the owner also **bans automatic git actions**, add: no commit, push, tag, branch,
merge, rebase or PR on their behalf (read-only inspection is fine), and Dependabot
security fixes stay off. Skip step 7: leave everything uncommitted and print the
exact command for the owner to run.

## 7. Land it

Commit only the files you touched, by explicit path; these repos usually have
unrelated dirty files.

If the clone is far behind the remote, do **not** rebase the checkout to land a
config change: that drags the tree through every upstream commit on top of dirty
files. Rebuild the commit onto the remote tip through a temporary index and push that
SHA; the worktree never moves:

```bash
( set -e
  export GIT_INDEX_FILE="$PWD/.git/tmp-push-index"; rm -f "$GIT_INDEX_FILE"
  git read-tree origin/master
  git diff HEAD~1 HEAD | git apply --cached --whitespace=nowarn -
  TREE=$(git write-tree)
  COMMIT=$(git log -1 --format=%B HEAD | git commit-tree "$TREE" -p origin/master)
  git diff --stat origin/master "$COMMIT"      # same files, same counts, or stop
  git push origin "$COMMIT":master
  rm -f "$GIT_INDEX_FILE" )
```

First check the remote has not itself changed the files you are rewriting
(`git diff --stat $(git merge-base HEAD origin/master) origin/master -- <paths>`).
Afterwards tell the owner their local branch still carries a redundant copy of the
commit: `git pull --rebase` drops it by patch-id; `reset --hard` would destroy their
dirty files.
