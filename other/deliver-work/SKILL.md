---
name: deliver-work
description: Takes finished work to a reviewed, CI-green pull request, reports it, and carries out a merge or discard only when the operator authorizes it. Use when implementation is complete and the operator asks to finish, wrap up, ship, deliver or open a PR for the work ("open a PR", "ship it", "we're done, wrap this up"), to respond to review feedback on that PR, to merge a finished branch ("merge it", "land it on main") or to discard one.
---

# Deliver Work

This skill takes finished work on a branch to a reviewed, CI-green pull
request and reports it. It does not plan or build: unfinished work goes back
to its plan.

## Adapt

An operator instruction, then the project's declared workflow for PRs,
merges, tickets or releases, win over every default below. A workflow
applies only when it is written down (CLAUDE.md, AGENTS.md, CONTRIBUTING and
the documents they name, PR templates, CI configuration) or the operator
states it. Where a workflow and a step here differ, the workflow decides how
the step runs. Merge, discard, force push, removal of a checkout and a push
to the default branch need the operator's authorization (step 8); a merge
authorization covers pushing that merge. The operator can skip a step; that
removes only that step, and the report lists it as skipped at the operator's
request.

## Procedure

1. **Find the work,** in this order:
   - **Branch:** the current branch, unless the operator names one. On the
     default branch or with no branch checked out, create a branch at the
     current commit with the project's naming convention before anything is
     pushed, and leave the local default branch as it is.
   - **Uncommitted changes:** commit those that belong to the work, with the
     project's message convention. Leave the rest untouched: never stash,
     reset or commit them, and never carry them to another branch. Tell the
     operator when they could change a check's result.
   - **Base,** the first of these that exists: the base of the branch's open
     PR (a closed or merged PR does not count); the base the operator or the
     project declares (the plan, the graph header); the repository's default
     branch. Never the branch's own upstream. When two of these differ, ask.
     With no remote, the base is the commit the work started from; when that
     is not known, ask. A base that is the same commit as the work compares
     the work with itself: stop and ask.
   - **Requirements:** the design, spec, plan, issue or request the work
     answers. Step 3 reviews against them.
   - **A plan or work graph** with an open item is unfinished: say so and
     stop. When the work comes from one, a defect found while delivering
     goes back to it as a new item, and delivery resumes at step 2 when
     that item is done.

2. **Verify the tree being delivered.**
   - Bring the branch up to date with its base by merging the base into it.
     Merge, not rebase: rebasing pushed commits needs a force push. A
     conflict you cannot resolve from the code goes to the operator.
   - Run every check CI runs for this diff. Read the CI configuration (the
     jobs a PR triggers, their path filters) and the project's verification
     rules. Include the PR-title and commit-message lints where the project
     has them, against the planned title and the branch's commit messages.
   - Read each check's output and its overall exit status, not a summary
     line. A check that cannot run here (secrets, another OS) is named; CI
     runs it in step 6.
   - Fix failures the work caused, test-first for code, and commit. Report
     the others with their output; do not work around them.

3. **Review stage.** Review the whole branch, from where it left its base to
   its head, adversarially. The reviewer, in this order: the operator's or
   the project's declared reviewer; else a fresh reviewer that has not seen
   this session, with the `judgment` capability. Brief the reviewer with the
   range, the requirements and the project's rules; not this session's
   history. Its task: find defects, not approve; report each with its
   location, the failure it causes and the evidence, and name each
   requirement the diff does not meet.
   - Verify each finding: read the cited code and reproduce it, for code
     with a failing test. Mark it confirmed or refuted, with the evidence.
   - Fix each confirmed finding test-first, then run step 2's checks again.
   - A requirement the delivered code does not meet is fixed in the code;
     when the operator accepts the delivered behavior instead, write a dated
     amendment to the requirement document so that it describes what
     shipped, marked as the operator's call.
   - Keep each refuted finding with its evidence for the report.
   - The stage passes when no confirmed finding is open.

A capability names the class of task. A session maps it to the subagent or model it uses for that class of task — `judgment` for demanding or nuanced coding work, `implementation` for normal coding work, `mechanical` and `lookup` for simple work — and never to a newer or frontier model beyond that class. When the session's configuration assigns a model to a role (an implementer, a reviewer, a planner), that assignment wins over the capability.

4. **Review feedback** from the operator or a PR reviewer. Read every item
   first, and ask about each unclear item before changing anything: items
   interact. Check each item against the code. An item that contradicts an
   earlier decision of the operator goes to the operator. Then, in order:
   fix each correct item test-first; run step 2's checks; push; answer each
   item where it was raised, with the pushed commit that fixed it, or, for
   a wrong item, the evidence (file:line, test output).

5. **Push and open the PR.**
   - Title and body: the project's conventions and PR template. Otherwise
     the title states the change, and the body gives what changed, why, the
     verification evidence (each check and its result, the review result)
     and the open items. Link the ticket the way the project's workflow says.
   - Open the PR against the base right after the first push, before any
     further push, so CI runs once. When the branch already has an open PR,
     push to it and update its body.
   - A rejected push means the remote branch moved: read the new commits,
     merge them, and run step 2 again. Never force it (step 8).
   - A failing commit or push hook: fix its cause. Never bypass it.
   - No remote: push, PR and CI do not apply; deliver the branch locally and
     report it.

6. **Watch CI to green.** On a failure, read the failing job's log, not a
   local reproduction, and list the differences between CI and this machine
   (license, HOME, OS, toolchain) before you guess a cause. Find the cause by
   reading the code path from the log's symptom to its source. Fix what the
   work caused test-first, run step 2's checks, push, and watch again. A
   failure the work did not cause: report it with the log excerpt; re-run
   the job only when the log shows an infrastructure fault.

7. **Report** (below).

8. **After delivery.** Each action below needs the operator's authorization:
   their words in this session, or a standing authorization in the project's
   instruction files (CLAUDE.md, AGENTS.md, CONTRIBUTING, the documents they
   name). A workflow an agent wrote, or one stated only in a tracker or
   ticket, is not one, and a standing authorization never covers a discard.
   The request that started this skill authorizes the delivery (push and
   PR), not a merge, unless it asks for the merge in so many words ("merge
   it", "land it on main"); "ship it", "wrap up" and "finish" do not.
   Words in this session cover the state the operator saw. A merge asked
   for in the starting request also covers the commits this skill makes for
   this delivery in steps 1-6. Show the commits and ask again for commits
   from elsewhere, or for commits made after the operator saw a report and
   answered it.

   Never change a checkout that has uncommitted files, except by a confirmed
   discard (below).
   - **Merge** only when authorized. First confirm the head being merged is
     the head that passed steps 2, 3 and 6. Show a failing check or an open
     finding to the operator and wait for their answer. Use the project's
     merge method; when the project declares none, ask which.
   - **Merge without a forge** into the local base branch. When the base has
     moved, merge it into the work branch first and run steps 2 and 3 again.
     When the base branch has commits that are not on the remote base, stop
     and ask: never merge onto unreviewed local commits. Run step 2's checks
     on the merged tree before the merge commit; on failure, abandon the
     merge, which leaves the base branch as it was, and stop. With a remote,
     push the base branch; the merge authorization covers this push. A
     rejected push stops: report it, and never force it.
   - **Discard** only on the operator's words in this session. First name
     what will be lost: the branch, its commits, whether they were pushed,
     any open PR, and any checkout with its uncommitted files. Act only after
     the operator confirms that list in this session, local steps first;
     when a local step fails, stop before closing the PR and report. Delete a
     remote branch only when the operator names it.
   - **Remove a checkout** only when authorized, only if this delivery or its
     plan created it, and only after the merge or a discard. Show a refused
     removal to the operator; never force it outside a confirmed discard.
     Leave any other checkout in place and say so.
   - **Delete the branch** only when the operator asks. Show a refusal; do not
     escalate to a forced delete unasked.
   - **Force push** only when authorized for this branch, and only in the
     form that refuses to overwrite commits you have not seen.

## Report

- branch, base, and PR link;
- every commit hash on the branch since its base;
- each check and its result, and the CI state;
- the review: fixed findings, refuted findings with their evidence, and the
  requirement amendments written;
- every open item, every step skipped at the operator's request, and every
  check that did not run, marked not run with its reason.

Every claim cites a result from this session. Something not run is reported
as not run. Then wait for the operator for the actions that still need
authorization (step 8). When the merge is already authorized and that
authorization covers the head, continue to step 8.
