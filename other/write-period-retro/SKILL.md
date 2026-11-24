---
name: write-period-retro
description: >-
  Load this skill when looking back over a period of work in a repo: what shipped, how work flowed,
  and the issues the history shows, each routed to a fix. Trigger on "write a retro", "what did we
  ship this week", "sprint retrospective", "how did the last month go".
argument-hint: "[since] [until]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI and a git working tree. The GitHub CLI (gh), authenticated, adds PR open and
  merge times and review counts. Without it, the retro uses merge commits only and says so.
license: Apache-2.0
---

# Write a period retro

Summarise a period of work from what the repository recorded, not from memory, and route each issue
the history shows to the skill that fixes it. Done means the retro is saved, every issue in this
repo's scope has been handed to its route, and the path, headline numbers, and routes are reported.

## Procedure

1. **Fix the period.** From `$ARGUMENTS`, otherwise from the day after the newest
   `.agents_workspace/product/retro/*-period.yaml` (or in the older `retros/` beside it), or
   `*-period.md` for a retro saved before
   `v3` with no YAML beside it, its date read from the start of the name in either form
   (`<YYYYMMDD-HHMMSS>` or the older `<YYYY-MM-DD>`), otherwise the last 14 days. State both dates in the retro.
2. **Collect the history.** Every number comes from a command, and the retro names the command:

   ```bash
   git log --since=<since> --until=<until> --no-merges --pretty='%h %ad %s' --date=short
   git log --since=<since> --until=<until> --merges --first-parent <default-branch> --pretty='%h %ad %s' --date=short
   git log --since=<since> --until=<until> --no-merges --name-only --pretty=format: | sort | uniq -c | sort -rn | head -10
   git log --since=<since> --until=<until> --grep='^Revert' --pretty='%h %s'
   ```

   With `gh`, add the merged PRs:
   `gh pr list --state merged --search "merged:<since>..<until>" --json number,title,createdAt,mergedAt,additions,deletions,reviews --limit 200`.

3. **Group what shipped** by Conventional Commits type and scope, or by top-level directory when
   the repo does not use them. One line per group, with the PRs or commits that make it up.
4. **Read the flow.** Compute only what the history supports: PRs merged, median and slowest time
   from open to merge, the largest diffs, reverts, fixes that touch a file changed earlier in the
   same period (a fix-of-a-fix), and the files changed most often (churn hotspots).
5. **Name at most three issues.** Each one states what went wrong and the commits or PRs that show
   it ("#41 and #47, each over 800 changed lines, took over 5 days to merge"). An issue with no
   evidence behind it is left out. Name the issue, not the fix: the routed skill finds the cause
   and designs the fix, and a fix drawn from history alone skips that step. Signals and the kind
   they usually are:

   | Signal                                                  | Kind          |
   | ------------------------------------------------------- | ------------- |
   | A revert, a fix-of-a-fix                                | Bug           |
   | A churn hotspot whose commits keep fixing the same area | Design        |
   | Large PRs, slow merges, PRs merged without review       | Project rule  |
   | Commits undoing the same kind of agent change           | Agent mistake |

6. **Route each issue**, then act on every route in this repo's scope, in this session:

   | Issue is                                                                                          | Route                                                             |
   | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
   | A bug in this repo's code or config                                                               | `ceh-coding-conduct:find-root-cause`, which writes the fix record |
   | A feature or design change in this repo                                                           | `ceh-build-plan:write-build-plan`                                 |
   | An agent mistake a check or guidance in this repo should have stopped                             | `ceh-every-session:prevent-repeat-mistake`                        |
   | A rule for how work is done in this repo                                                          | `ceh-every-session:record-project-decisions`                      |
   | Anything else in this repo                                                                        | Fix it directly, with the check that proves it                    |
   | Outside this repo: user settings or memory, an installed plugin, Claude Code itself, another repo | Left in the report for the user                                   |

   Every issue ends `handed off`, with the artifact its route wrote or the commit that fixed it,
   or `dropped`, with why acting on it is not worth it. An issue stays `open` only while it waits
   on a user decision, with `status_detail` naming that decision: one outside this repo, or one
   whose route's plugin is not installed, which waits on the user installing it. When the repo's
   README, `CLAUDE.md` or `AGENTS.md` names a backlog file, a row added there counts as handed off,
   with `status_detail` naming the row. When the user later decides, the session acting on it sets
   the issue's `status` and `status_detail` in place and renders the retro again, and the file
   keeps its name.

7. **Save and report** per Output.

## Rules

- Facts from history only. Something the history cannot show (why a PR stalled, how the team felt)
  is a question in the retro, not a finding.
- Measure the work, not the people. No per-person counts, rankings, or blame. Commits per author
  measure nothing worth improving and invite gaming.
- A small number is reported as a count, not a trend. Three PRs are not a velocity.
- Merge commits, bots, and generated files (lockfiles, snapshots) are excluded from churn counts.

## Output

Save one file, creating the directory if needed:
`.agents_workspace/product/retro/<YYYYMMDD-HHMMSS>-<session-id>-period.yaml`, holding the retro and
every issue, those fixed in this repo and those left for the user, because the next retro and the
routed work read it. It fills `assets/period-retro.template.yaml`, per the `period-retro/v3`
section of `references/period-retro-schema.md`. Take `<YYYYMMDD-HHMMSS>` from one `date +%Y%m%d-%H%M%S` call and `<session-id>` from `${CLAUDE_SESSION_ID}`.
After the last edit, run `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py render <file>.yaml`,
which writes the `.md` beside it in the layout of `assets/period-retro.template.md`, and fix the
YAML for each error it lists. Never edit the generated `.md`. On exit 2 or 3, or without uv, say
in the reply that the retro went unchecked and unrendered.
