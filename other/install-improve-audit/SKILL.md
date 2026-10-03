---
name: install-improve-audit
description: >-
  Get an unfamiliar repo installing and building locally, fix only what blocks it, and open a PR carrying the fixes plus an append-only change log. The deliverable is a working build and a PR — never a findings report. Trigger when the user says "install this repo", "get this building", "clone and set this up", "make this run locally", "why won't this build", "docker compose build fails", "/install-improve-audit", or hands over a repo path or URL and asks for it working. Container-native repos are first-class: the container build is a real install path, not a disqualification, and a repo that builds in its own image reaches INSTALLED. Improvements are a bounded bonus tier that opens only after the build passes, is capped at 3 items, and is always droppable. Do NOT use for repo analysis, architecture review, code-quality assessment, deliberate security scanning, or dependency-hygiene audits — this skill refuses those and names the right tool instead.
---

# Install Improve Audit

Get the target repo building locally, fix what blocks it, and open a PR. The name is
the priority order, and the order is strict:

- **Install** — the only thing that counts as success. Non-negotiable.
- **Improve** — a bonus tier, opened only after the build passes, hard-capped, always droppable.
- **Audit** — the append-only log of what you changed and why. A change log, not a code audit.

**Three outputs and no others: a working build, a committed fix set, an open PR.**

## Input

The target is the repo path or URL the user named, or the current working directory if
they named none. If they stated a `<slug>`, use it for the branch and doc names;
otherwise derive it from the repo directory name. Honor a docs-path override and a
GitHub issue number if given. Ask for nothing else — if the target resolves, start.

## Acceptance gate — read first

Your final message is invalid unless it contains all four:

1. a verdict: `INSTALLED`, `INSTALLED-DEGRADED (<what is off>)`, or
   `BLOCKED (first blocker: <reason>)`
2. the commands that now work, or the exact command that failed
3. the last 15 lines of install-check output — from the passing run if DONE was
   reached, from the failing run if it was not. If those lines are a
   dependency-resolver package wall, keep the lines that prove pass/fail and
   elide the package list mid-line, saying so — the requirement is evidence,
   not bulk
4. the PR URL — or, if you lack push access, the branch name and the exact push
   command in its place. That is the only permitted substitute.

**When more than one degradation applies**, semicolon-join every one of them in this
fixed order — do not pick a winner, and never drop one to keep the line short:

1. excluded components, with the count (`2 of 10 workspace members excluded`)
2. `scripts disabled — untested at runtime`
3. relaxed version, with what it was relaxed from
4. `no build command`
5. `container build only; native install documented but not verified`
6. `tests failing, build clean`
7. start-check failure, with the reason

So: `INSTALLED-DEGRADED (2 of 10 workspace members excluded; scripts disabled —
untested at runtime)`. A most-severe-wins rule would hide a partial install behind a
lesser reason, which is the exact thing the verdict exists to surface.

An issues list is not a deliverable. A code-quality assessment is not a
deliverable. A repo-is-bad summary is not a deliverable. If the repo cannot be
installed, ship `BLOCKED` with the first blocking error and the smallest next
action — not a broad assessment.

If the caller asks for a repo analysis, say this skill installs first, and that a
code-review or repo-health tool is the right one for analysis. The "Audit" in the
name is the change log, not a code audit.

## DONE — binary, nothing else counts

From a clean tree, all three of these exit 0:

1. the repo's dependency install command
2. the repo's build command
3. a minimal load check of what was installed — `python -c "import <package>"`,
   `node -e "require('<entry>')"`, or the ecosystem's equivalent, appended to
   `install-check.sh`. Loading only: no app start, no config, no network. This
   is the cheapest proof that the resolver's exit 0 produced something that
   executes — a pin that installs clean but cannot import fails here instead
   of in the first user's session.

Write all three into `install-check.sh` at the repo root at step 4 of the order of
operations — right after branching, so the file is born on the install branch. If
that file exists or the root is not writable, use `.install-audit/install-check.sh`
and name that path in your final output.

**The first two lines are `#!/usr/bin/env bash` and `set -euo pipefail`.** Without
`set -e` the script's exit status is the *last* command's, so a failed build followed
by a passing load check exits 0 and the gate certifies a broken install. This is not
optional and not a style preference.

You are not finished until the check exits 0 and you have pasted its last 15
lines verbatim. "It builds now" is not acceptance.

Edge cases, decided in advance — do not deliberate:

- **No build command exists or can be inferred:** dependency install plus the
  load check is DONE. Verdict `INSTALLED-DEGRADED (no build command)`.
- **The repo's install path is containerized:** see the `## Containers` section below.
  A container-native repo reaches plain `INSTALLED`.
- **The documented build command also runs tests, lint, or e2e:** narrow it to the
  compile/build step only. Tests are not part of DONE. If it cannot be narrowed and
  only the test phase fails, verdict `INSTALLED-DEGRADED (tests failing, build clean)`.
- **The target moves mid-run** (upstream commits land, or the operator calls for
  a fresh tree): commit whatever has landed, reset to a clean tree at the new state,
  then cherry-pick back only the commits whose errors still recur. Keep the audit-log
  rows already earned and restart the loop at step 7. The budget does not reset.
  Because every fix is committed as it lands (step 7), a reset costs you nothing that
  was already earned.
- **Optional, after DONE:** start the app for about 10 seconds, then kill it. Start it
  in the background and `kill` it by PID — do **not** reach for `timeout`, which is not
  present on macOS/BSD by default. Do not `source` an example env file blindly either;
  unquoted values with spaces word-split and the failure looks like a repo bug when it
  is your harness. If the app dies, verdict is `INSTALLED-DEGRADED` with the reason.
  Do not fix runtime config unless it is a one-liner.

  Worth doing rather than skipping: the one real run found a repo that documents no
  build command but whose run command silently compiled a production build. The
  start-check is where an implicit build shows itself.

## Containers — a first-class install path

Some repos are built on containers. For those, the container path **is** the install,
and this skill's job is to get it working — not to refuse it and report that the repo
has no build command. A container-native repo that builds reaches plain `INSTALLED`.

**Build is not run.** `docker build` and `docker compose build` start nothing: no
services, no ports, no long-running process. They exit 0 or non-zero, and that is
exactly what the gate needs. `docker compose up` starts services and is **not** a gate
command — if the documented command is `docker compose up --build`, narrow it to
`docker compose build`.

**When to use the container path.** Use it when the repo documents no native install,
when the native path is explicitly unsupported, or when the container build is the
README's primary route and the native path fails. Prefer native when both work — it is
faster to re-run and proves more about the dependency situation.

**The gate, substituted.** The three-part native gate collapses to two commands, both
in `install-check.sh`:

1. `docker compose build` (or `docker build -t <tag> .`) — dependency install and
   build are fused inside the image; there is no separate install step to assert.
2. The load check, run **inside** the image:
   `docker compose run --rm <service> python -c "import <package>"`, or
   `docker run --rm <tag> node -e "require('<entry>')"`. Same rule as native: loading
   only, no app start, no network.

**Verdicts.** No new verdict vocabulary — the existing grammar already covers it:

- Container build and load check pass, and the repo is container-native → `INSTALLED`.
- Repo documents both paths and only the container one was verified →
  `INSTALLED-DEGRADED (container build only; native install documented but not verified)`.
- Docker is not installed, or the daemon is not running → `BLOCKED (first blocker:
  docker unavailable)`. That is a genuine blocker, not a degradation — say so plainly
  rather than falling back to a native path the repo does not support.

**Cost.** A cold image build is slow, but the budget excludes unattended waiting and
layer caching makes re-runs fast — which is what you want from a repeatable gate. Image
build time is never a reason to refuse the container path.

## Budget — counted in attempts, not minutes

**8 failed fix attempts, total, for the whole install.** One attempt is one pass of the
step-7 loop: one first-error, one smallest change, one re-run. A pass that clears its
error does not count against the 8 — only failures do.

Attempts, not minutes, because you have no clock. A wall-clock budget requires stamping
a start time and subtracting subprocess duration from it, and in the one real run of
this skill none of that happened: the session ran roughly three times its stated budget
and no status line was ever emitted. An attempt counter is something you can actually
hold. Note you cannot buy headroom by batching several changes into one attempt — the
loop takes the **first** error and makes the **smallest** change that clears it, so a
batched attempt breaks a rule that is already there.

- After attempt **4**, print one line: `STATUS 4/8 | last error | next move`.
- After attempt **8**, if the check has never passed, all fixing stops. From that point
  the only permitted actions are:
  1. commit anything not yet committed
  2. finish the audit log
  3. write `## Blocked` and `## Recommendations`
  4. open the draft PR
  5. produce the final output

  No further source reading. No alternate-architecture research. No issue list. No
  improvements — a repo that never built has nothing to improve.

Unattended waiting — dependency downloads, cold image builds — is free and always was.
The Improve box and the PR steps sit outside this count and have their own limits.

## Order of operations — do not reorder

1. **Environment, one line each, no prose:** OS/arch; the runtime version the repo
   declares (`.nvmrc`, `.python-version`, `engines`, `rust-toolchain.toml`,
   `go.mod`); the version actually installed; which version manager is available;
   package manager and version; whether Docker is installed and its daemon is
   running (`docker info`). Docker is a gate input, not trivia — a container-native
   repo cannot be installed without it.
2. **Recon — one pass, delegated.** Launch the Explore subagent, read-only,
   with this exact return contract: *"Return the documented dependency-install
   command and build command from README, INSTALL, Makefile, and CI workflow files.
   Return the declared runtime version. Return nothing else. Do not read source
   files. Do not assess the code."* If Explore is unavailable, do the same recon
   yourself, limited to those same files. The file list is the bound, not a clock.
3. **Branch** `install/<YYYY-MM-DD>-<slug>`.
4. **Write `install-check.sh`** with all three parts DONE requires (or the two-command
   container substitute), `set -euo pipefail` at the top, then prove the gate can fail
   before trusting it:

   Replace the **first** command with an unmistakable marker — a command that cannot
   exist, e.g. `zzz_gate_marker_zzz` — run the script, and confirm two things
   together: it exits non-zero, **and** the error names your marker. Then restore the
   command. Do not run the unmodified gate here; step 6 does that.

   Both halves matter. A non-zero exit alone proves nothing at this point, because the
   install has not run yet and is presumed failing — that is the premise of this whole
   skill. Only the marker appearing in the output proves the script actually reaches
   and reports the command you think it does. Breaking the first command keeps this to
   seconds instead of a cold dependency resolve.

   The gate is self-authored under time pressure — exactly the condition this skill
   says produces polarity inversions in `fix_probes` — and an inverted gate reads every
   install as done, including through the pasted output lines.
5. **Create the audit doc:** frontmatter and an empty log table only. Nothing else
   goes in it yet.
6. **Run the gate's install path** — the same command `install-check.sh` holds, not
   whatever the README says verbatim. Native repo: the documented dependency-install
   command. Container repo: the narrowed build from `## Containers`
   (`docker compose build` / `docker build`), **never** `docker compose up`, even when
   `up --build` is exactly what the README documents. Do not pre-diagnose. Let it fail.
7. **Loop until DONE or budget:** take the **first** error → smallest change that
   clears it → re-run → append one log row → **commit that fix on the spot**, one
   commit per logical fix, message naming the error it cleared. Repeat.

   Committing inside the loop is what makes "one commit per logical fix" real instead
   of reconstructed at the end, and it is what lets a mid-run reset cost nothing. Every
   repo file you change gets a log row and a commit — including a change you made and
   then decided was unnecessary, which gets a row saying so.
8. **On DONE:** open the Improve box, if anything on its list qualifies.
9. **Write** the audit doc's status table, `## Blocked`, `## Improvements`, and
   `## Recommendations`, then open the PR.

## What you may read during the fix loop

Only files directly implicated by the error in front of you: build scripts, config
files, env templates, manifests, lockfiles, version pins, and the file the failing
command names. Do not browse the codebase looking for problems.

## Improve — the bonus tier

Opens only after `install-check.sh` exits 0. Everything in it is droppable, and
dropping all of it costs the run nothing.

**Box: 3 items maximum, and at most 2 failed attempts across the whole box.** Separate
from the install attempt budget, and it runs before the PR steps. When either cap is
hit, stop mid-item, revert anything unfinished, and move what is left to
`## Recommendations`.

**Eligible — only these, and only when the install itself put it in front of you:**

1. Record a runtime version the repo needs but does not declare (`.nvmrc`,
   `.python-version`, `engines`) — the version you had to discover the hard way.
2. Correct an install or build command in the repo's own docs that you proved wrong.
3. Add the step you had to work out yourself to the existing install docs.
4. Add a key you had to guess to an existing `.env.example`.
5. Wire `install-check.sh` into a CI workflow that already runs on push — one line,
   and only if such a workflow already exists. This is the one item the local re-run
   rule cannot verify; the reviewer sees the result on the PR, which is what CI is
   for. On a run with no push access it goes to `## Recommendations` instead.

**Not eligible, however tempting:** dependency upgrades the build did not need,
refactors, formatting or lint sweeps, new tests, new CI files, new doc files, renaming
or restructuring anything, or an improvement to code you never had to open. If it is
not on the list above, it is a recommendation, not an improvement.

**Rules that keep this skippable:**

- Each improvement is its own commit, prefixed `improve:`. A reviewer must be able to
  drop every one of them and still merge a working build.
- Re-run `install-check.sh` after each one. If an improvement breaks it, `git revert`
  that commit and move on — never debug an improvement.
- Improvements never change the verdict, never appear in `## Blocked`, and never delay
  the PR.
- `BLOCKED` runs skip this tier entirely.
- **Zero improvements is a normal, complete run.** Do not manufacture one to fill the
  section; an empty `## Improvements` is omitted, not apologized for.

## PDDA compliance — deliberately partial

Full PDDA compliance is **not a goal of this run** and is not achievable inside the
budget. Produce exactly what is listed below and nothing more. Do not open PDDA.md
or ROUTER.md to check whether more is required — the answer is no.

**Location:** `PROJECT/2-WORKING/INSTALL-<slug>.md`. Override with the docs path if
one was given. If the repo has no `PROJECT/` tree, fall back to
`docs/install/INSTALL-<slug>.md`, or repo root. Do not create a PDDA lifecycle
structure in a repo that lacks one.

**Frontmatter — exactly these keys:**

```
title, status, created, updated, owner, doc_type: install-audit
ratings_provisional: true
gh_issue          # only if an issue number was given
```

**Body — exactly these sections:**

```
Status table (what was completed | what's next)
the append-only fix log table
## Blocked
## Improvements     # omit if none landed
## Recommendations
```

**Deliberately omitted — do not add:** Swarm Preflight Contract, `fix_probes`,
phases, `complexity` / `risk` / `effort`, `non_goals`, `roadmap_exempt`,
MARATHON.yaml stanzas, lifecycle folder transitions.

`fix_probes` specifically: `install-check.sh` **is** the gate for this work. A probe
set authored under time pressure is where polarity inversions come from, and an
inverted probe reads as already-done. A later pass adds probes if this graduates.

`ratings_provisional: true` is load-bearing — a single-pass run's ratings are guesses,
and the flag keeps this doc out of automated selection until a human reviews it.

**Never move the doc to `3-COMPLETED`.** That transition belongs to the closeout
chain after the PR merges, not to this run.

Two rules hold regardless of location:

- **Append-only during the run.** Each row is written **after** the fix is applied.
  No narrative sections until step 9.
- The log is a table: `| time | step | error (first line only) | change made | file | result |`

## Blocker ladder — in this order

Two fix attempts per distinct error, then move down. Every failed attempt counts
against the 8:

1. Honor the lockfile exactly (`npm ci`, `pip install -r` with hashes,
   `poetry install`, `cargo build --locked`) before touching any version.
2. Switch to the runtime version the repo **declares**, via the version manager.
   Do not edit the declaration.
3. If a postinstall script is the blocker, retry with scripts disabled
   (`--ignore-scripts` or equivalent). The log row names the skipped scripts
   and what they were supposed to produce, and the verdict reason says
   `scripts disabled — untested at runtime`. If a skipped script builds the
   package's own native component, disabling it is a broken install wearing a
   green exit code — that is not a degradation; keep moving down the ladder.
4. Relax the declared version. Log it as a degradation with the reason.
5. Exclude the failing optional component, workspace member, or extra; build the
   rest. Log what is excluded, and carry it into the verdict parenthetical with
   the count — `INSTALLED-DEGRADED (2 of 10 workspace members excluded)` — and
   into the PR title. The log table alone is not enough visibility for a
   partial install; a reader of the verdict must see the hole without opening
   the log.
6. `BLOCKED`. Append to `## Blocked`: the error, what was tried, and the single
   smallest thing that would unblock it. The verdict names it as the *first*
   blocker — serial fixing means later blockers are unknown, and the reader
   must not assume the named one is the only one.

Before rung 6, if the repo has a container path you have not tried, try it — see
`## Containers`. A repo that builds in its own container is installed, not blocked.

## Scope fence

During the fix loop this fence is absolute. The Improve tier widens it by exactly five
listed items, and only after DONE.

**May edit freely:** dependency manifests and lockfiles, config and env files,
build and run scripts, `install-check.sh`, install docs, version-manager pins.

**May patch minimally** — only when the error is clearly build-shaped: a bad import
path, a missing shim, a syntax break from a version bump, a hardcoded absolute
path. Smallest possible diff. Log every one.

**May NOT:** refactor logic, bump majors to chase a nicer API, change public APIs,
reformat, fix lint or type errors that do not block the build, edit tests except to
make them runnable, or repair broken business logic. If the application genuinely
does not compile against its own declared runtime, that is `BLOCKED` with a
recommendation for a separate code-fixing run — not this skill's job.

Anything outside the fence is logged as a recommendation. You do not do it.

If the repo is not owned by your organization: use no credentials it did not ship
with, no internal registries, and run nothing beyond its documented install and
build commands.

## The PR — the run is not finished at DONE

1. **Commit what is left** — the audit doc, and anything not already committed. The
   fixes themselves were committed inside the loop at step 7, one per logical fix, so
   the history already shows which change cleared which error; do not squash it now.
   Improvement commits stay separate and keep their `improve:` prefix, so they can be
   dropped independently.
2. **CHANGELOG.md** — if the repo already has one, add **one** entry summarizing the
   landed fixes. If the repo has no CHANGELOG, do not create one.
3. **Push the branch.** If you lack push access to origin, stop here and hand back the
   branch name and the exact push command. That pair substitutes for the PR URL in the
   acceptance gate and in Final output — it is the one case where a run is complete
   without a URL. Everything else in the final output is still required.
4. **Open the PR.** Title: `install: <verdict> — <slug>`. Body: your final output,
   **verbatim**. It is already exactly what a reviewer needs; do not author a
   second description.
5. **Do not merge.** No auto-merge, no reviewer assignment, no labels.
6. **`BLOCKED` still ships a PR** — as a draft. `install-check.sh`, the fixes that
   did land, and the blocked doc are what let the next attempt resume rather than
   restart. A blocked run with no PR wastes the whole session.

## Final output — exactly this, nothing more

- **Verdict:** `INSTALLED` | `INSTALLED-DEGRADED (<what is off>)` | `BLOCKED (first blocker: <reason>)`
- **PR:** URL, and `draft` if drafted. With no push access: the branch name and the
  exact push command instead — the only permitted substitute for a URL
- Last 15 lines of install-check output, verbatim — the passing run on DONE, the
  failing run on `BLOCKED`. Never omitted: a run with no output is not a report.
  Package-wall lines may be elided mid-line with the elision marked; the status
  lines that prove the exit are the part that must survive.
- The copy-pasteable commands that now work, or the command that failed
- `git diff --stat` for the branch
- `## Improvements` — one line each, with the commit that carries it (omit if none)
- `## Blocked` and `## Recommendations` — ranked. **Recommendations: maximum 3**, plus
  a `+N more not listed` line if more qualify — never drop one silently. Each must be
  something you actually saw during recon or the run, not something you inferred about
  a repo you did not read. The fence limits where you look, never what you may say
  about what you saw. The **cap** is what keeps this from becoming the findings report
  this skill exists to prevent; a provenance test does not, and would delete the
  recon-sourced observations that are often the most useful lines in the report
- `### Security — incidental findings only` (below; omit entirely if empty)

### Security — incidental findings only

Written after DONE, at the bottom. Not an audit. Never changes the verdict.

**Only what the install put in front of you** — no scanning, no grepping for
secrets, no extra tool calls, no time spent looking. Typical qualifying finds: a
credential or private key in a tracked file you opened; a committed `.env` with
real values; an install script fetching and executing remote code; a dependency
pulled over plain HTTP or from an unpinned source; no lockfile at all.

**Maximum 3 items, one line each:** what it is, the path, why it matters. No
severity ratings, no remediation plans, no CVE lookups. If you find yourself
investigating, stop — write the line and move on. If more than 3 qualify, write
the 3 that matter most and state the count of the rest in one line — never drop
a qualifying find silently.

An empty security section is the expected outcome, not a gap.

## Not wanted

Architecture review, code quality assessment, deliberate security scanning,
coverage analysis, dependency hygiene review, or any finding you did not encounter
while making the build pass.

Do not deliver a static-analysis report. A final message containing findings but no
verdict and no PR is incomplete work.
