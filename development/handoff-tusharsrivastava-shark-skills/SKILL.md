---
name: handoff
description: Records and prunes the handoff file, the state that carries between sessions. Use at the end of a session, before a context reset, or when the user asks where things stand.
---

# Handoff file

The handoff file holds what a new session needs and cannot find by looking: what to do next, what waits on the
user, known defects that are not fixed yet, open decisions, and gotchas that are not fixed at their site yet.

**Where the file is:** the path in the project `AGENTS.md`, section `## Docs layout` (key: handoff file). Default:
`HANDOFF.md` at the repository root. If `## Docs layout` is missing, use the default and tell the user once that
they can add the path to `AGENTS.md`. This skill calls the file "the handoff file".

Everything else has a home already:

- the code and the commits;
- `AGENTS.md` (working rules);
- the decisions log (gaps between the spec and the code, and how the team resolved them: `## Docs layout`);
- the spec (what the system must do) and the handbook (how the code does it);
- a skill or an agent file of the project;
- a plan file.

A copy of these in the handoff file is a **cache**, and a cache becomes stale.

**Do not copy the state of the repository.** git holds the commit, the branch, the distance to the remote, a
clean or changed tree, and the worktrees, and git is never stale. A new session gets them with `git status -sb`,
`git log -1 --oneline`, and `git worktree list`. Write a git fact only when its *reason* is not in git, for
example "the refactor on branch `x` stops at step 3, on purpose". Then it is a normal entry in Next or Queue,
with an exit. The same applies to results that a command gives again: a test count, a gate result, a file count.

If nobody prunes the file, it fills with **sediment**: old layers that nobody dares to delete, until they hide
the live items. The cure: every entry has an **exit**, a condition that removes it from the file, and a place
where it goes.

**Budget: 2,000 words** (`wc -w <handoff file>`). If the file is over the budget, prune it before you record.

## Sections

Use these sections, in this order. Each entry is one to three lines. Put longer detail in a plan file, and let
the entry point to it.

| Section | Holds | Exit |
|---|---|---|
| Header line | `Last edited: <YYYY-MM-DD HH:MM> <time zone>`, nothing else. The local time of the edit, written before the commit | Write it again at each edit |
| Start here | Session start steps that `AGENTS.md` does not give | `AGENTS.md` or a skill now gives the step: delete |
| Next | The one thing to do first, then five more at most | Done: delete; the commit records it |
| Waiting on the user | Questions that only the user can answer, each with the recommendation | Answered: the answer goes where it acts (spec, decisions log, plan, code, `AGENTS.md`); delete |
| Queue | Known defects and small fixes not done yet: what, where, the failure | Fixed: delete. A dated item ("on or after ...") is due: move it to Next |
| Recently merged | Merges that the user has not tried by hand yet, one entry for each merge, with its commit range | The user's test round covered it, or 14 days passed: delete; `git log` holds it |
| Direction | Pointers to the plans and to the stage status in the build plan | A plan is finished: its row says so in one word |
| Left open on purpose | Decisions parked on purpose, each with the condition that opens it again | Opened again and decided: the answer goes where it acts; delete |
| Cost time once | Gotchas whose fix is not at the site yet | **Promoted** to where it applies (a guard or a test at the site, an `AGENTS.md` rule, a handbook pitfall, a skill, or a memory): delete |

## Record

Add or change one entry. This usually happens at the end of a turn.

1. **Search first.** `grep` the file for the subject of the entry. If an entry exists, update it in place. The
   same item twice is one item.
2. **Put it in its section**, by the table above, in one to three lines. If it needs more detail, write the
   detail in a plan file, and let the entry name the file.
3. **Close what this work finished.** Each entry that the work completed, answered, or fixed leaves now, by its
   exit.
4. **Update the header line** to the current local time (`date '+%Y-%m-%d %H:%M %Z'`), before the commit.
5. **Check the budget.** If the file is over 2,000 words, do the Prune procedure now.

Done when the entry is in one place only, no finished item stays, and the file is within the budget.

## Prune

Do a full pass when the file is over the budget, when you write it again for a session restart, or when the user
asks.

1. **Measure.** Write down the word count.
2. **Test each entry** against these conditions, in this order. The first condition that applies decides:
   - **Done**: the commit, code, or file that it asks for exists (check with `git log`, `grep`, `ls`). Delete
     it.
   - **Derivable**: the repository says it already (the code, `AGENTS.md`, the decisions log, the handbook, the
     frontmatter of a skill, a plan file). Delete it, or replace it with a pointer of one line when the fact is
     hard to find.
   - **Duplicate**: another entry has the same meaning. Merge it into the entry in the better place.
   - **Promotable**: a gotcha or a rule that belongs where it applies. Write it there, then delete it here.
   - **Overlong**: more than three lines. Move the detail to a plan file. Keep a pointer of one line.
   - **Stale**: it names a file, a flag, a sha, a count, or a date that is not true now. Verify it, then correct
     it or delete it.
   - **Live**: it is still true, still necessary, and nowhere else. Keep it.
3. **Keep each open item somewhere.** Never delete an unanswered user question, an unfixed defect, or a parked
   decision without a new home. It stays here, or the entry that points to its new home stays.
4. **Write the header line again** with the current local time, before the commit.

Done when you tested each entry, the file is within the budget, and you can find each open item from before the
pass.

## Report

Give one line to the user: the words before to after, then the counts by exit (deleted as done, deleted as
derivable, merged, promoted with the place of each promotion, moved to plans, corrected). Commit the promotions
that changed a tracked file through `shark:commit-blocks`, together with the handoff file change.
