---
name: change-build
description: >-
  Plans and builds a medium-sized change in one file, `docs/changes/<slug>.md`: a fix or
  small enhancement too big for `quick-fix` but with no real design to do. Writes the
  problem, cause, approach and a short task list, gets one yes, then builds each task with
  the builder and reviewer agents and opens the PR. Use for a fix across several files, a
  fix that needs a few tests, or a small addition to existing behavior. Hands over to
  `feature-explore` when the change needs a design.
user-invocable: true
argument-hint: <describe the change, or a change slug to resume>
---

# change-build

The middle lane. `quick-fix` makes one small edit in place. The `feature-*` pipeline writes
a brief, a design and a plan before any code. Most work sits between the two: the cause is
known, the way to fix it is clear, but it touches several files and needs a few tests. This
skill plans that work in one file and builds it through the same gate as `feature-build`.

## Scope

- IN: one change whose approach is clear, or needs at most one choice the user can answer
  in a line. Usually two to five tasks. Bug fixes across several files, a fix that needs
  more than one new test, a small addition to an existing screen or endpoint, a refactor a
  fix depends on.
- OUT: anything the size test below sends elsewhere. Release steps, CMS majors
  (`major-upgrade`), and porting to another version line (`change-backport`).

## Argument

`$ARGUMENTS` is one of:

- A description of the change in the user's words.
- Starting material from another skill: a tracker issue with its triage findings, an
  `investigate-bug` report, or a fix `quick-fix` found too big. Use what it already says;
  ask only about what's missing.
- A slug, or nothing on a branch named for one: resume the change file that matches (see
  "Finding the file").

If it's empty and no file matches the branch, ask what the change is.

## Where this writes

- **Owns:** `docs/changes/<slug>.md` and, when a task changes a screen,
  `docs/changes/<slug>-screens/`. If the project's `CLAUDE.md` sets a different docs path for
  plans, put `changes/` next to its plans folder instead.
- **Finding the file:** strip the branch's `vN/` and type prefix (`fix/`, `feat/`), as
  `CLAUDE.md`'s "Finding the current feature's plan folder" rule does, and look for
  `docs/changes/<remainder>.md`.
- Code never links to the file, and the file names plans and ideas by name, never by path,
  so archiving it breaks nothing.

## Size test

Read the code the change touches before deciding. Then pick the first that fits:

1. **Cause unknown.** A bug where nobody can say what causes it: stop and hand off to
   `investigate-bug`. A plan built on a guessed cause fixes the wrong thing.
2. **Fits `quick-fix`.** One concern, about 20 lines, at most one new test, nothing for a
   reviewer to weigh up: hand off to `quick-fix`. Don't write a change file for it.
3. **Needs a design.** Any one of these is a hard stop, not a judgment call:
   - A new screen, dialog, workspace or section, or a change to an existing screen big
     enough that someone should see a mockup first. Adding one field, button or column to
     an existing screen is fine.
   - A new entity, table or migration, or a change to stored data.
   - A breaking change to public API or a manifest `alias`. An addition, or a change made
     safe by an `[Obsolete]` proxy as `umbraco-package-conventions` describes, is fine.
   - More than one real design choice, or a choice the user can't answer in one line.
   - More than about five tasks.

   Hand off to `feature-explore` with what you've gathered as its starting material: the
   problem, the cause, the repro, and the code you read.
4. **Otherwise**, it's this skill's. Go on.

Say which one you picked, and why, in one line.

## Plan: write the change file

1. **Check the tree.** Confirm the working tree is clean and you're on the project's trunk
   (see `CLAUDE.md`'s Feature workflow section). If not, stop and report. Pick a short,
   kebab-case slug.
2. **Write the file** from `templates/change.md`:
   - **Problem:** what's wrong or missing, for whom, in the user's terms.
   - **Repro**, for a bug: the steps or test that show it, through the real entry point
     (`feature-build`'s "Smoke the real entry point" lists them). Write one if none was given.
   - **Cause**, for a bug: where it lives, the layer that produces the bad value or makes the
     wrong call, not the line that throws. Grep for other places with the same cause, as
     `quick-fix` step 7 does, and list them. Fix them in this change if they share the fix;
     else they go under Follow-ups.
   - **Approach:** one short paragraph. What changes and where, and why this way over the
     obvious other way.
   - **Tasks:** an ordered checklist, each task one commit that leaves the build green. A
     task that changes a screen says which screen and its click path.
   - **Out of scope:** what this change won't do, so the reviewer doesn't flag it as
     missing.
3. **Ask once, up front.** Put the one open choice, if there is one, into the same message
   that shows the file, with the options and your recommendation. Offer the file as
   `markdown-preview` says to. Wait for a yes on the whole file. This is the only stop
   before the PR.

   If the answer or the reading so far shows the change fails the size test, stop there and
   hand off as the size test says. The file isn't committed yet: pass its content on, and
   ask before deleting it.

## Build

1. **Branch.** Create a short-lived branch off trunk, named by `git-workflow`'s branch
   naming with the slug as its slug (`fix/<slug>`, `feat/<slug>`, or the project's `vN/`
   form). Use the project's `WorktreeCreate` hook if it has one, as `feature-build`'s
   Preflight step 4 does. Commit the change file there first: `docs: add change plan for
   <slug>`. Nothing goes on trunk.
2. **Start the demo site once**, if there is one, as `feature-build`'s Preflight steps 6 and
   7 do. Its `Demo site:` line goes at the top of the file's Log section.
3. For each unchecked task, in order, follow `feature-build`'s loop (build, pre-review
   checks, review, recurse, smoke, commit), with these differences:
   - **Build.** Give the `builder` the task text and the file's Problem, Repro, Cause and
     Approach in place of `ARCHITECTURE.md` and `SPEC.md`.
   - **Review.** Give the `reviewer` the same sections, and the Out of scope list.
   - **Tick and log.** Tick the task in the change file, and add its commit SHA and what was
     verified to the Log. A choice the builder made that the file left open goes in the
     Decisions section, dated, with who decided, as `feature-build` step 7 says.
   - **Too big after all.** If a task runs into one of the size test's hard stops, or the
     reviewer's findings show the approach is wrong, stop. Commit nothing more. Report what
     was built, and hand off to `feature-explore` with the change file as its starting
     material. The branch stays as it is for the user to decide.

## Finish

1. Run the full test suite. Run the Repro through the real entry point and see it pass.
2. Run `feature-build`'s whole-feature review, with the change file as the design and its
   Decisions section in place of `DECISION-LOG.md`.
3. Stop the demo site.
4. Invoke `pr-describe` with the change file's path. Don't write the PR body yourself.
5. Offer the "Other version lines" step from `issue-resolve`'s "Closing the loop" if the
   project supports more than one line.

## Archive

Once the PR merges, move the file out of `docs/changes/` so that folder holds only live
work. Follow `feature-close`'s "Close each plan" steps with the change file in place of a
plan folder, as `major-upgrade`'s "Archive" does:

- The status line goes at the top of the change file, under its title.
- Step 2 reads the file's Decisions section.
- Open Follow-ups: list them for the user to turn into tracker issues before the move.
- The file moves to `<archive-path>/changes/<slug>.md`, and its screenshots folder with it.

## Rules

- One change per run, one change file per change.
- The size test runs before the file is written, and again whenever a task finds something
  new. Never shrink the fix to stay in this lane; hand off instead.
- Builder writes code, reviewer gates it, this skill owns the change file. Never edit code
  here yourself, even one line.
- Never commit to trunk. Pushing and opening the PR follow `git-workflow`.

## Hand off

Report the change file, tasks done with their commits, what the Repro showed, the review
verdict, and the PR link. List the Follow-ups, one line each.

- **If another skill started this one**, return those and stop. That skill decides what runs
  next.
- **Otherwise**, offer the Archive step once the PR merges.
