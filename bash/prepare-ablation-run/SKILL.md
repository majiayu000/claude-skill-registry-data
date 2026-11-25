---
name: prepare-ablation-run
description: 'Mint run repositories under ~/Developer/ablation-runs, each stamped with a variant, the frozen spec, and the acceptance kit.'
disable-model-invocation: true
---

# Prepare a run

Mints one repository per run, because a run is a single interactive harness session, and each
repository is a snapshot rather than a link back here — spec and context frozen as they stood at
mint time.

## 1. Interview

Ask these questions.

1. **Which variants?** `bare`, `checks-only`, `governed`, or any combination.
2. **Which models?** Each answer becomes the last field of a run id, e.g. `sonnet-5`,
   `gemini-3-8-flash-high`. Lowercase kebab-case, no dots — the id reaches a `sed`
   expression where a `.` matches any character.
3. **Which host harness?** Required, not optional. `claude-code`, `antigravity`, or another
   name in the same charset. The whole metrics path forks on this answer: Claude Code's
   figures come out of a transcript afterwards, Antigravity persists no token count
   anywhere on disk. Recorded as `unknown`, a missing token table is unreadable — it could
   mean either.
4. **How many of each?** One repository is minted per variant × model × repeat, so two of each
   across three variants on one model is six repositories.
5. **Which spec/md file?** State default `docs/evals/ablation/implementation-spec.md`

### Summarize

1. Read the spec and **create a slug naming the task the run performs, no abbreviations** using this format `YYYYMMDD-<slug>-<variant>-<run-number>-<model>`, for example `20260904-build-initial-cli-bare-1-sonnet-5`
2. If multiple runs are to be created, list every cell you are about to mint — variant, model,
   repeat — and say how many repositories that is in total. A matrix is easy to misread by a
   factor of two, and every cell is a session someone has to sit through.

**Wait for user confirmation before proceeding**

## 2. Refuse a drifted kit

```sh
bash scripts/preflight.sh --spec <path>
```

This checks that this repository is clean at the declared source commit, that the acceptance
kit still reproduces its frozen verdict — `governedFiles: 24`, `invalidFiles: 15`,
`totalViolations: 22`, all 18 codes reached — that the stamped assets match
`assets/assets.sha256`, and that the edit register's three cuts are still absent from the
vendored skills.

A drifted kit or a drifted asset silently changes what **every** run minted from it received,
and runs minted either side of the drift are then not comparable. A failure here is a
**refusal**: report exactly what drifted, and mint nothing.

Two of the register's cuts are invisible to the per-run leak sweep, which waives record
vocabulary for the governed variant — so a restored "respect ADRs in the area you're touching"
would pass there in silence while manufacturing the exact behaviour the bare arm exists to
measure the absence of. That is why they are asserted by name here rather than left to the pin.

## 3. Mint

One run:

```sh
bash scripts/prepare-run.sh --variant <variant> --model <model> --slug <slug> --spec <path>
```

A matrix:

```sh
bash scripts/prepare-batch.sh --slug <slug> --models <a,b> --variants <x,y,z> --repeat <n> --spec <path>
```

`prepare-run.sh` is the only script that writes; the batch delegates every cell to it, so a batched
and a hand mint produce identical repositories. The batch mints repeat-major, so an abort partway
leaves whole balanced blocks rather than every repeat of one variant and none of another. It
reports each cell as `ok` or `FAIL` and exits non-zero if any cell failed — read that table, since
a batch that minted five of six still prints five successes.

## 4. Check every mint

```sh
bash scripts/verify-run.sh <run-directory>
```

Report its output verbatim, including anything it flags. Run it on **each** repository a batch
produced. The checks that matter most are the ones whose failure is silent: that `.claude/rules/`
entries are real symlinks rather than the copies `rsync -aL` would leave, that no symlink resolves
outside the run directory, that the leak sweep covers the whole tree rather than one file, that
the vendored skills still hash equal to `assets/skills/`, that the scaffold reproduces its own
cohort hash, and that every gate except the acceptance suite opens green — the suite is red by
design until the run builds the thing.

The skills check is hashed rather than diffed because `diff -rq` cannot do it: it follows
`.claude/skills` into `.agents/skills`, reports `Directory loop detected`, skips the comparison
and still exits clean. The obvious tool prints a green tree it never read.

Do **not** expect a non-zero dependency count here. `src/` is empty at mint, so cruising zero is
correct and proves nothing either way; what is checkable now is that `tsPreCompilationDeps: true`
is set, without which the tool erases every `import type` and prints a green checkmark over an
empty graph. The non-zero assertion belongs to scoring, over an output tree.

## 5. Hand over

Print what `prepare-run.sh` reported: the launch command, the flags, and `start`. The flags are
protocol, not convenience — `--setting-sources project,local` shuts off the user-level hooks that
would otherwise rewrite `Read` into `cat` and hide the record channel from the transcript.

The variant is in the directory name by decision, so the operator reads the runs root at a glance.
What stays out of the name and out of the tree is the study around the run: that it is one of
several, and that anything is being compared.

The hand-over also prints a **cohort** hash (`scaffold_sha`). Runs are comparable only within one
cohort, and this is the only field that says so — `source_sha` cannot, because a commit can be
amended out of existence, and the checks and governed layers are derived from the source repo at
mint time rather than stored. Two governed runs minted eight hours apart on 2026-09-03 differed by
74 insertions and 188 deletions across four records; both reported a clean mint and nothing in
either tree distinguished them. Check the hash against the siblings you intend to compare before
launching.

## 6. After the session

```sh
bash scripts/collect-metrics.sh <run-directory>
```

Reports tokens, the record channel (which records the run opened, by which tool, and how far into
the session), skills invoked, test placement, and the floor. Claude Code's figures are recoverable
from its transcript at any later time and need no logging switched on. Antigravity's are not
recoverable at all, so an interactive Antigravity run reports the floor by design, not by failure.

The floor — duration, churn, inventory, entry point — is recomputed here, from the run tree, after
the fact. It used to be a `metrics.sh` stamped into the run and appended to `RESULTS.md` by the
agent as its own last act. That path is closed on both counts: it told the run it was being
measured, and it reported a knowingly partial reading. Taken from inside the session, it excluded
the commits and the report text written after it, so every churn figure it printed undercounted
its own run — `RESULTS.md` appears in one run's numstat at 138 lines against a file of 278.

Duration is `started` to the **last commit**, not to the clock now: this script runs whenever the
operator gets to it, and "now" would bill every idle hour to the run. The in-run `AGENTS.md` tells
the run to commit its report as its final act precisely so that stamp exists.

This output is **operator-side**. Never write it back into the run: telling a run that its record
reads are being counted is the one measurement that would change what it measures.
