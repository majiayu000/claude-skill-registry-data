---
name: patch-fanout
description: Ports many independent patch units in parallel, one shark:code-writer for each unit, from an audit or a decision list. Use after shark:port-audit, or for a batch of small independent fixes.
---

# Patch fan-out

A **fan-out** runs many agents at the same time, each on one small task. Here the task is one **patch unit**: one
cause from the unit index of the `shark:port-audit` skill (`<scratch>/audit/UNITS.md`), or one item of a defect
list. Each **patch agent** ports one unit on its own branch. The lead (`shark:lead-merge` skill) merges the branches
as they arrive. An audit engineer (`shark:merge-audit` skill) reviews each merge. `<scratch>` is the session
scratch folder, outside the repository.

The **integration branch** (`<integration branch>`) collects the merged patches. Its newest commit is the
**integration head**.

```
UNITS.md ──► operator ──► patch agent U01 ─► pu/U01 + notes/U01.md ─┐
                     ├──► patch agent U02 ─► pu/U02 + notes/U02.md ─┼─► queue.md ─► lead-merge ─► <integration branch>
                     └──► patch agent U0n ─► pu/U0n + notes/U0n.md ─┘                       └─► merge-audit
```

## Project values

| Section of `AGENTS.md` (or `CLAUDE.md`) | Used for |
| --- | --- |
| `## Commands` › `setup` | Install the dependencies in each new worktree |
| `## Commands` › `test-db:copy` (optional) | A test database for each worktree, copied from the migrated template |
| `## Commands` › `lint`, `format`, `typecheck`, `test <paths>` | The light checks on the changed files |
| `## Invariants`, `## Architecture rules` | The rules that each port keeps |
| `## Owner rules` | Long checks, pushes, the attribution trailer |
| `## Secrets` | The files that an agent never reads |

If a section is missing, ask the user once. Suggest adding it to `AGENTS.md`.

## Files

| File | Content | Writer |
| --- | --- | --- |
| `<scratch>/port/pipeline.md` | The roles and rules of the run (patch agent, lead, audit engineer) | operator |
| `<scratch>/port/notes/<UNIT>.md` | The patch note of one unit (template: `references/patch-note-template.md`) | patch agent |
| `<scratch>/port/queue.md` | The units that wait for the lead, in batches (`shark:lead-merge`) | operator |

The templates are in `references/` in this skill folder (`${CLAUDE_PLUGIN_ROOT}/skills/patch-fanout/references/`).

## The operator: launch the units

1. Write `pipeline.md` once. Copy the patch-agent part from `references/patch-brief.md`. Add the lead part from
   `shark:lead-merge` and the audit part from `shark:merge-audit`.
2. Check free disk space (`df -h <repo parent>`). Each worktree holds its own dependencies.
3. Get the integration head from the lead. Every brief of a wave names this sha as the base.
4. Start a wave of about 6 to 8 patch agents (`shark:code-writer`), H units first. Use `references/patch-brief.md`
   for each brief.
5. Give a dependent unit the branch of the unit it depends on as its base, not the integration head.
6. Give two units of one conflict group to two agents only when the lead can merge them in sequence.
7. When an agent reports, add its unit to `queue.md`: branch, sha, what it did, and the merge items.
8. Turn each "not ported" item of a report into a follow-up unit in UNITS.md ("Added by the operator").
9. Start the next wave when an agent finishes. Do not wait for the lead.
10. Check each background agent at its timebox plus 5 minutes, by the clock. An agent can wait for hours on a
    permission prompt.

## The patch agent: the steps

Each step has a hard limit. The whole unit has a timebox of 20 minutes, plus one automatic grace of 20 %.

1. **Read.** Read `pipeline.md` and your unit row in UNITS.md. Then read its source rows in the group files and
   the owner decisions of the brief.
2. **Verify first (5 minutes at most).** Show that the rule exists in production and is missing or broken at the
   integration head:
   - production evidence: `git show <reference>:<path>`, or `git show <sha>^:<path>` for a commit that
     production does not have;
   - integration evidence: `git grep` and the file and line at the integration head.

   Stop and report in these cases:
   - **NOT A GAP:** the rule is present at the integration head, or a decision removed it. Give the evidence.
   - **PRE-EXISTING:** production does not have the rule either. Port it only if the unit says so.
3. **Worktree.** Make it from the base of the brief:

   ```bash
   git -C <repo> worktree add ../<repo name>-wt-pu-<UNIT> -b pu/<UNIT> <base sha>
   ```

   Then run the project's `setup` in it. If the tests need a database, run the project's `test-db:copy`. Never
   build a test database from zero.
4. **Test first.** Write a test that pins the production behaviour. Cite the decision ID in the test docstring, in one ASD-STE100 sentence with no notes in brackets. Run it with
   the project's `test <file>`. It must fail for the reason that you expect.
5. **Port.** Put the rule into the current architecture:
   - in the module and the layer that the unit names, or that the current design gives
     (the project's `## Architecture rules`);
   - keep every rule of the project's `## Invariants`;
   - never bring back a deleted module as a whole;
   - typed state: values stay in their native types, and text comes only at the presentation edge;
   - never parse display text into data;
   - no customer or tenant name and no tenant rule in shared code: tenant rules come from configuration or a spec;
   - one definition for each shared name: import the owner, do not copy a constant.
6. **Light checks.** Check only what you changed:
   - the project's `lint` and `format` on your changed files;
   - the project's `typecheck` on your changed files. If it gives false import errors on single files, run it
     with no paths, so that it uses the project configuration;
   - the project's `test` on your new or changed test files only.

   Do not run test folders, the snapshot test or the architecture tests: the lead runs them for each batch. If
   you add a new module, run the architecture test that checks deleted names and one-definition rules.
7. **Commit.** One conventional commit on `pu/<UNIT>`, with the attribution trailer of the brief
   (`shark:commit-blocks` gives the format).
8. **Patch note.** Write `<scratch>/port/notes/<UNIT>.md` with the Write tool
   (`references/patch-note-template.md`). The lead resolves conflicts from it.
9. **Report.** Short, outcome first (the report list of `references/patch-brief.md`).

**Do not wait for other units**, also when they change the same file. The lead resolves the conflicts.

**At the timebox**, the grace of 20 % is for the step in progress (a running check, the commit, the note), not
for new work. To get more time, ask the operator before the grace ends (`SendMessage` to `main`: what is left,
why, the minutes). With no answer at the end of the grace, commit what is green, mark the note PARTIAL, and list
each item that is not ported.

## Rules for every patch agent

- Write files only with the Edit or Write tool. Never `sed`, `awk`, `cp`, `git apply`, a heredoc, or a script
  write.
- No live model call and no paid API call in a test or a script. Never read or print an env file (the project's
  `## Secrets`).
- Never `git stash`, push, merge, rebase or `--no-verify`.
- Touch only what the unit needs. A shared name that another unit needs: name it in the report. Never decide a
  shared name alone: stop and report.
- A check that can run longer than 10 minutes needs the owner's OK (the project's `## Owner rules`). A patch agent
  never starts one.
- Leave no uncommitted fix in the worktree. Commit it, or name it in the report.

## Lessons

- **Agents break the rule "Edit or Write only".** Writer lanes write files with heredocs, `sed -i` and inline
  scripts, also when the brief forbids it. A rule in the brief does not stop it; a hook that refuses shell file
  writes does. In a repository without the hook, the lead reads each file that a shell command wrote, for damage.
- **Base each wave on the newest integration head.** A unit from an old base gets more conflicts, and the lead
  pays for them.
- **Build a dependent unit on the branch it depends on.** A follow-up of unit A that starts from the
  integration head before A merged does not have A's names.
- **A partial patch makes a follow-up unit.** A large unit can need two or more follow-ups. Give a large unit a
  smaller scope at the start.
- **Fakes must match the protocol.** A type checker refuses a fake whose parameter name differs from the
  protocol or the interface. Check the fakes in your tests with the type checker.
- **Disk space stops the run.** A full disk can stop the lead in the middle of a batch. Check free space before
  each wave, and let the lead remove each merged worktree.
