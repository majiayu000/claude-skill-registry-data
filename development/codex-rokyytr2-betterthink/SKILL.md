---
name: betterthink
description: "Enforce a stricter execution workflow for coding tasks: reduce ambiguity before editing, complete and verify one work item before starting the next, keep the project's memory file lean and current when conventions or commands change, and screenshot-check UI work across mobile, tablet, and desktop. Use when the user wants more disciplined thinking, fewer assumptions, and higher-confidence execution."
---
# BetterThink
Apply this skill at the start of a coding task when correctness and discipline matter more than speed.
## Clarify Before Editing
- Drive uncertainty down before writing code.
- Ask focused questions when scope, behavior, stack, naming, or edge cases are materially ambiguous.
- If a small assumption is safe and non-destructive, state it explicitly and proceed.
- Do not silently fill important gaps with guesses.
Target: reach high confidence in the requested outcome before editing.
## Finish One Slice Before Starting The Next
- Work on one concrete to-do at a time.
- Verify the current slice before moving on: read the diff, run the relevant test or command, or inspect the behavior directly.
- Do not stack partially finished fixes with a plan to circle back later unless the task genuinely requires it.
Target: treat "probably done" as not done.
## Delegate Only When Codex Allows It
Codex may only use subagents when the user explicitly asks for delegation or parallel agent work. Do not force delegation when the runtime instructions do not allow it.
When delegation is explicitly allowed:
- Use `explorer` for scoped codebase questions, searches, and fact-finding.
- Use `worker` for isolated implementation or verification tasks with a clear file or module boundary.
- Keep the main thread on the critical path; delegate sidecar work, not the immediate blocker.
- Reuse the inherited model by default. Override the model only when there is a concrete task-specific reason.
## Keep Project Memory Lean
At the end of a meaningful change, update the existing project memory file if the repository already uses one, such as `AGENTS.md` or another established top-level guide.
Update it only when one of these happens:
- Add a new dependency
- Add a new script or command entry point
- Create a new top-level folder
- Change build, run, test, or deploy commands
- Introduce a new project convention or pattern worth preserving
Rules:
- Prefer the file the project already uses; do not create a new memory file unless the repo already expects one or the user asks.
- Record durable information only: architecture, conventions, commands, gotchas, and non-obvious decisions.
- Skip routine bug fixes, refactors, and task logs.
- Keep the file compact. If it starts growing into long-form documentation, move detail into a supplementary doc and leave one pointer line in the memory file.
## Screenshot-Verify UI Work
For any visible UI change:
1. Run the UI.
2. Capture screenshots at `375px`, `768px`, and `1440px`.
3. Inspect spacing, alignment, hierarchy, overflow, broken states, and tap targets.
4. Fix issues and capture again until all three viewports are acceptable.
Do not mark UI work complete just because it compiles or tests pass.
## Use Supplementary Docs Sparingly
- Create extra docs only when the information is too detailed for the project's main memory file.
- Store them at the project root or under `docs/`.
- Add a one-line pointer in the main memory file explaining when to read them.
- Do not read supplementary docs by default; load them only when the current task needs them.
## Stop Signals
Pause and re-check this skill if you catch yourself thinking:
- "I will just start coding and figure out the requirements later."
- "This part is mostly done, I can move on."
- "I will update the project memory file later."
- "The UI looks fine from the code alone."
