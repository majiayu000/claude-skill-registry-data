---
name: minispec
description: Plans a task as a MiniSpec change before the work starts. Use when the user asks for a feature, a refactor, or a fix that spans several files or modules, or when the user asks for a spec, a plan, or a change proposal. Not for a fix in one file.
argument-hint: "[change name]"
allowed-tools: Bash(minispec *)
---

<task>
Plan the task as a MiniSpec change, and stop when the plan is valid.
MiniSpec keeps a plan in files, so a long task keeps its state across a handoff.
The files are in `minispec/specs/` (the current specs) and `minispec/changes/<name>/` (one folder for each change).
The `minispec` command checks and moves the files.
Use it only to create, validate, show the status of, or archive a change.
Read and edit the files with `Read` and `Edit`, because each extra call costs time.
</task>

<tiers>
Pick the smallest tier that fits the work.

- Small: a fix in one file, or a change with a known result.
  Make no change folder.
  Do the work, run its check, and stop using this skill.
- Medium: one feature in a few files.
  The change has `proposal.md` and `tasks.md`.
- Big: a change over several modules, or a change to a public contract.
  The change also has `design.md` and `specs/<capability>/spec.md`.
- Large: a big change with many steps or with open choices.
  It has the files of a big change.
  Ask the `planner` agent for the first draft, then give the plan to the `reviewer` agent with the lens `plan` before the work starts.
</tiers>

<procedure>

1. Pick the tier, and a short name of lowercase words with hyphens, in any script, such as `add-export`.
   Use `$ARGUMENTS` as the name when it is given.
2. Create the change:

   ```bash
   minispec new <name> --tier <medium|big|large>
   ```

   For a big or large change, add `--capability <name>` when the spec belongs to a capability other than the change name.
3. Replace the example text in each file.
   - `proposal.md`: why, what changes, and the impact.
   - `design.md`: the decisions with the alternatives that you did not choose.
   - `specs/<capability>/spec.md`: each requirement says what the system SHALL do, and has a scenario with WHEN and THEN lines.
   - `tasks.md`: one line for each step, as `- [ ] 1.1 text`.
     Put the check of the task on the next line, indented, as `Check:` and a command in a code span, such as ``Check: `just test path` ``.
     A check in prose, such as "check that it works", is not a check.
     Name a command that exits with a status that shows pass or fail.
4. Validate the change:

   ```bash
   minispec validate <name>
   ```

   Fix each problem that it prints, then run it again.
   The command refuses a task whose check is prose.
5. Tell the user that the plan is ready, with the path of the change folder.
   Start the work with the skill `minispec-apply` when the user agrees, or when the user asked for the whole task.
</procedure>

<rules>
Ask the user only for a choice that the code and the docs cannot settle, and state each assumption in the proposal.
Write the plan for the request and no more.
Do not make a change folder for a small task.
Do not start a second change while a change has open tasks, unless the user asks.
</rules>
