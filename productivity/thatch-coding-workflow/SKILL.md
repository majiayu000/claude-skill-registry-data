---
name: thatch-coding-workflow
description: 'Plan and execute code changes with a task-list-driven workflow. Use when implementing features, fixing bugs, or making multi-file changes that benefit from milestone planning and a verification checklist. This is the procedure skill: it tells you how to structure the work of making a change. Pair with thatch-code-archaeology, which tells you how to understand the code as it currently is before you start.'
---

You are about to make code changes. This skill gives you a workflow for planning, executing, and verifying those changes. Use it when the change is non-trivial: more than a single-line fix, touches multiple files, or requires understanding existing code first.

This skill tells you _how to structure the procedure for making a change_ — task lists, milestones, verification. It does not tell you how to _understand_ the code you are changing. For that, use `thatch-code-archaeology` first: it explores the code base from multiple angles so you have the complete picture before you plan. Use archaeology first; use this skill second.

## Triage: Single-step vs Multi-step

Before writing any code, assess the scope.

**Single-step changes** — discrete changes to 1-3 files with a clear boundary.
- Research the problem space and dependencies.
- Look for existing patterns in the codebase that you can reuse.
- Check for existing tests that cover the code you are changing. If yes, run them before making changes as a baseline. If no, consider writing one.
- Plan your changes, then execute them. Check the file after each edit for correctness, formatting, and syntax.

**Multi-step changes** — complex or open-ended changes that span multiple components or require design decisions.
- Use a task list (the todo tool) to plan milestones. Name each milestone descriptively; there may be follow-up requests later in the conversation.
- Include a brief rationale for each milestone explaining the implementation choice.
- Research affected features and components to map dependencies before planning milestones.
- Execute milestones in order. Verify each milestone's output before moving to the next.

## Skills first

Before planning milestones, check whether a matching skill applies:

- **`thatch-code-archaeology`** — use when you need to understand the code you are about to change. It explores the code base from multiple angles (data model, state flow, git history, sibling features) and surfaces skeletons and hidden assumptions before you start coding. This is the research skill that should precede any non-trivial change.
- **Code review skills** — use after changes are complete, not before.
- **Other skills** — prefer invoking a matching skill over building bespoke steps. If declining an obviously relevant skill, state briefly why and proceed.

## Pre-flight

- Check for unstaged changes you were not aware of. If present, ask the user before proceeding. It is fine to work on top of your own changes from earlier in the session.
- Use thatch_memory_recall to check for prior knowledge about the area you are working in. Previous sessions may have already investigated it.
- Use the memory tools to record learnings as you discover them.

## Post-coding checklist

After all changes are complete, verify in this order:

1. **Verify the changes were applied.** Inspect the files you edited. Confirm the edits landed, not just appeared in tool output. Tools can report success while applying nothing.
2. **Review the changes.** Use a code review skill or manually review the diff. Pass the scope and design intent explicitly. Do not rely on a reviewer to guess the target.
3. **Address findings.**
   - Pre-existing bugs unrelated to your changes: report them to the user separately.
   - Simple fixes: fix immediately.
   - Complex fixes: plan as a separate milestone.
4. **Run tests, linters, and formatters.** Address any issues they surface. If the project has a quality gate (make check, npm run check, mise run check), run it.
5. **Repo finish gate.** If the current repo defines its own definition-of-done skill (in the thatch repo: `thatch-dev-done`), load it and work its checklist before claiming the task complete. The generic verification above does not cover repo-specific duties: QA use cases, doc tiers, count touch points, commit conventions.

## Blockers vs intermediate states

A **blocker** is a fundamental contradiction where proceeding in any direction would violate the user's intent or produce an unsound result. If you find a genuine blocker, stop and explain it to the user. They are unfamiliar with the changes you just made and may need context to understand the problem.

The following are **not blockers** — they are normal intermediate states in a multi-step change. When you encounter them, continue to the next milestone:
- Incomplete work or missing modules planned for a later milestone
- Failing tests from code that hasn't been implemented yet
- Partial tool output that needs another iteration
- Bugs in scaffolded code that you can fix in the next pass

Do not stop to check in on these. Keep going.

## Coding attitude

- Do not report success if you did not actually apply the changes. Verify before claiming success.
- Do not check with the user over and over when they instructed you to make changes. Do the work.
- Fix the entire problem, not just the superficial part.
- Make the Right Thing the Easy Thing to do. If the code makes it hard to do the right thing, fix the code so it doesn't.

## Cruft and tech debt

If the code is a mess and needs significant work to be maintainable and safe to change, explain that to the user once. If they do not instruct you to do the mass refactor, do your best with what you have. Don't let the perfect be the enemy of the good.

It is fine to be blunt about the state of the code and separation-of-concerns problems you encounter.

## User feedback

Keep the user updated on your progress. Note when you find something unexpected, interesting, or relevant to them. If the code is well-crafted or solves a problem cleverly, say so.
