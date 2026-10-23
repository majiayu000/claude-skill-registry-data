---
name: wikicommit-merge
description: Run WikiCommit's quality gates over the uncommitted changes under .wikicommit/, then branch, open a PR, merge it into the repository's default branch, and file one review tracking Issue per page. Use this only to land WikiCommit's own output — the uncommitted changes under .wikicommit/, including your own edits to its policy files — including inside an unattended run that works through sources in batches. It squash-merges to the default branch and publishes, so do not use it as a general way to commit, push or open a PR for ordinary repository changes — use git and gh directly for those.
metadata:
  requires: "wikicommit-init"
---

# wikicommit-merge

> **Paths in this file.** `references/…`, `scripts/…`, `workflow.yaml` and `../<other-skill>/…` are relative to this Skill's directory — the one holding this `SKILL.md`, which the runtime names when it loads the Skill — not to the repository root, because the Skills may be installed under `.claude/skills/` or `.agents/skills/`. Commands still run from the repository root, so spell the path out from there (`python <this Skill's directory>/scripts/…`). Paths starting with `.wikicommit/` are repository-root paths as before.

Runs quality checks against the uncommitted changes under `.wikicommit/` (wiki pages, source management files), then performs branch creation, PR creation, merge (without relying on GitHub's auto-merge feature — see Step 7 in `references/merge-pr.md`), merge confirmation, and post-review tracking Issue generation end-to-end.

## Usage

```
/wikicommit-merge
```

## Processing Flow — the workflow engine holds the order

The order of this Skill's steps is kept by `.wikicommit/scripts/skill_workflow.py`, not by you. It returns **one step at a time**, checks on disk (and, for the merge itself, on GitHub) that the step was really done before moving on, and keeps its place in this run's record — so after a compaction or a new session you pick up exactly where the run stopped instead of re-deciding whether the branch, the PR or the merge already happened.

**Start the run** (add `--non-interactive` when no person can answer questions in this run — a subagent, a scheduled or unattended run; the workflow engine then answers the warnings question itself with "proceed", and the warnings still go into the PR body):

```bash
python .wikicommit/scripts/skill_workflow.py start --workflow workflow.yaml \
    --model "<the model ID this runtime reports for you>"
```

(Spell `workflow.yaml` out from the repository root, as the note at the top says.)

Then **loop**:

1. Read the JSON it printed. **Keep the `run` path** — every later call names it.
2. If `notes` is present, report every line of it to the user. The workflow engine's own steps speak through it: the version-skew check of `.wikicommit/scripts/` (`OUTDATED:`, `MISSING:`, `ORPHAN:`, `WARNING:` — report all four; a skew warning does not stop the run, but a quality gate older than the rule it enforces passes what the current one would block, and this is the last check before the default branch), the default branch (`DEFAULT_BRANCH:`, with a `WARNING:` when it could not be read from GitHub and `main` is assumed), a PR an earlier run left for a person (`AWAITING_MERGE:` while it is still open, `AWAITED_MERGED:` once a person merged it and this run files its Issues), pages held back because no AI review judges them (`UNREVIEWED_PAGE:`, `HELD_SOURCE:`, `HELD_BACK:` — say which, and that they stay uncommitted), and another run's unfinished work (`OPEN_RUN:`).
3. If `step` is `null`, the run is over — `finished` (say `finished_because` if present: "No changes to merge", the user chose to stop at the warnings, or `merge-pr: awaiting-merge` — the PR waits for a person's required review, and `/wikicommit-merge` is to be run again after a person merges it), or halted (say `halted_reason`: another run still open, a blocking quality check — its findings are in `notes` — or a PR that could not be merged). Stop.
4. If `blocked` is true, the completion check for this step has failed repeatedly: stop and report the last `reason` to the user. Do not work around a check.
5. A `human` step: ask the user `ask`, offering `choices`, and pass the answer back with the `then` command.
6. An `agent` step: **read the file named in `instructions` now and follow it**. When it is done, run the `then` command with one of the `outcomes`, `--token` set to the `pass_token` in the instructions file's frontmatter, and the `--add`, `--reason` or `--count` that step's instructions ask for.
7. `done` prints the next step in the same form. If it prints `"accepted": false`, the step is **not** complete: read `reason`, fix what it names, and run `done` again. It never skips ahead, and it refuses a step other than the current one.

`skill_workflow.py next <run>` prints the current step again without changing anything — use it whenever you are unsure where the run is, and **always** after a compaction or when resuming in a new session (`skill_workflow.py status` lists the runs still open). Values the steps share — the default branch, the warnings, the PR number — are in the run record's `workflow.lists`, not in your memory; read them from there. A run whose session is gone for good is closed with `skill_workflow.py abandon <run> --reason "<why>"`, which only a person should decide.

**Why it works this way.** This Skill has more ways to stop partway than any other here — a blocking quality check, a PR that never reaches a mergeable state, a rate-limited Issue creation — and several of them leave a branch and a PR behind. A run that stops is recorded as halted with its reason, and one that is interrupted stays open, so `check_run_records.py` reports it either way instead of it looking like a run that never started.

The steps (the table is here as well as in the workflow engine's answers so the pointers survive a compaction):

| Step | Kind | Read | What it does |
|---|---|---|---|
| `freshness` | script | — | compares `.wikicommit/scripts/` with this Skill (warns, never stops) |
| `default-branch` | script | — | reads the default branch from GitHub, or assumes `main` with a warning |
| `awaited` | script | — | a PR an earlier run left for a person (`awaiting-merge`) that has been merged since: pulls the default branch and lists it (`awaited_prs`), so this run files its Issues |
| `unreviewed` | script | — | holds back the pages `wikicommit-generate` wrote that no AI review record judges as they now stand, and the management files naming them (`skipped`): every later step leaves them out, and they stay uncommitted |
| `detect` | script | — | Step 1: lists the changes |
| `work` | script | — | no change and no merged PR to follow up → the run finishes with "No changes to merge"; with only a merged PR, the steps that carry a change (`quality-checks`, `commit`, `open-pr`, `merge-pr`) are skipped |
| `open-runs` | script | — | refuses a change that carries files a still-open run touched |
| `classify-*` (7 steps) | script | — | Step 2: one list each in the run record (`changed_md`, `removing`, `new_sources`, `new_schema`, `new_vocab`, `policy_files`, `relations_file`) |
| `quality-checks` | script | — | Step 3: frontmatter, WikiLinks, raw HTML, orphans/duplicates; a blocking finding halts the run |
| `link-and-style-checks` | agent | `references/quality-checks.md` | Step 3: lychee over the changed pages only, in calls that return within the shell's time limit, and markdownlint-cli2 |
| `collect-warnings` | script | — | puts one `<tool> (<count>)` line per tool into the `warnings` list |
| `proceed-with-warnings` | human | — | only when there were warnings; a non-interactive run proceeds |
| `commit` | agent | `references/commit.md` | Steps 4–5: branch and commit |
| `open-pr` | agent | `references/open-pr.md` | Step 6: push and open the PR |
| `merge-pr` | agent | `references/merge-pr.md` | Step 7: wait for a mergeable state, merge, return to the default branch — or, when the default branch requires a review, leave the PR open for a person and finish (`awaiting-merge`) |
| `review-targets` | script | — | Step 8: the pending pages that no open tracking Issue names yet (`review_targets`) |
| `tracking-issues` | agent | `references/tracking-issues.md` | Step 8: one review tracking Issue per listed page; skipped when nothing needs one and the open Issues could be read |
| `failure-targets` | script | — | Step 9: the failed sources that no open generation-failure Issue names yet (`failure_targets`) |
| `failure-issues` | agent | `references/failure-issues.md` | Step 9: one Issue per listed source; skipped likewise |
| `report` | agent | `references/completion-report.md` | Step 10: close the run and report |

If `.wikicommit/scripts/skill_workflow.py`, `_workflow_checks.py` or `check_external_links.py` does not exist (`.wikicommit/scripts/` older than this Skill), the run cannot start (the first step halts on either of the latter two): tell the user to run `/wikicommit-update` first.

## Notes

- lychee's timeout can take up to 10 seconds × (1 + `max_retries` 2) per link, so `link-and-style-checks` checks a few changed pages per call and is called again until done (`LINKS: done`). It checks only the pages this merge changes: re-checking every page's links on every merge is not this Skill's job
- Never commit directly to the default branch. Commits always happen on a `wikicommit/merge-*` branch (Step 8 does not create a `wikicommit/review-*` branch itself — `review-issue-close-sync.yml` creates that branch when the tracking Issue is closed)
- Do not write to `.wikicommit/schema/` — this skill only ever *commits* new schema files `wikicommit-generate` Pass 2b already wrote to disk (Step 2 item 4, Step 5), it never creates or edits their content itself
- Do not use `--force-push`
- On a default branch that requires a review, the PR is not merged by this Skill: the run finishes with the PR open (`awaiting-merge`), and the **next** `/wikicommit-merge` after a person merges it files the tracking Issues. That run finds the PR through `.wikicommit/run/` on this machine; if the run record is gone (another machine, or rotated out), the next merge that carries a change still files them, since Step 8 scans the whole default branch
- Never delete a branch, PR, or Issue without the user's confirmation (present the cleanup procedure to the user and confirm before running it)
