---
name: design-prototype
description: Build a component in Figma with every variant and state from its contract, using design-system tokens and the chosen approach. Use when a design direction has been picked and the user wants the component actually drawn on the Figma canvas.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: design
  phase: 4
  artifact: 04-prototype.md
  stack-aware: true
  figma-aware: true
---

# Prototype

Build "$ARGUMENTS" in Figma as a component with all variants and states specified in the component contract.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"design-prototype","workflow":"design","phase":4,"project":"<project>","event":"skipped","artifact":"04-prototype.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 4 (Prototype) of the Design Thinking workflow (`design`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `design` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

**Stack.** Before you build, test, lint, run or generate code, read the `Stack` section of the project's `AGENTS.md`, or of `CLAUDE.md` when `AGENTS.md` has none. Use its commands exactly as written, its `layout` for where files go and its `rules` as requirements. If it names a `profile`, also read the file `<profile>.md` in the `stacks` folder of this skill's bundled references for the full commands, layout and rules; the project's own keys win where both speak. If there is no `Stack` section, run the `singular-detect` skill, state what you inferred in one line, and offer to write the section with `singular-init`. Never assume a package manager, test runner or formatter the project did not declare.

**Figma.** Steps marked *Figma* use a Figma MCP server you connect to this agent yourself; this pack ships none and makes no network calls. Before you ask the user anything or run the first such step, list the tools available to you and bind each capability the step names to one tool, as `references/figma-capabilities.md`, bundled with this skill, describes: the official Figma server's tool named there, else any tool whose description plainly does the same thing. With a capability bound, take the file key and node id from a Figma link in the request or the conversation, else from the `file:` line of the `## Tools` section of the latest earlier artifact of this project that has one; when a bound capability needs one and there is none, ask for the link once, with any other question you ask. With nothing bound, never ask for a link. Record the result in a `## Tools` section after any `## Recalled` section: a `- file:` line (the Design file; a board or a deck goes on a `- board:` or `- deck:` line), one line per bound capability (`- read-tokens: get_variable_defs (figma)`), and a `- created:` line for node ids you created; or the single line `No Figma server: steps marked Figma ran without one.`; a skill with no artifact says the same in its summary. For an unbound capability do what the step's *Without Figma* line says, using first any values the user gave in the request or in files it names: never ask the user to connect a server, never invent values a tool would have returned, and never report a step as run when it was not.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"design-prototype","workflow":"design","phase":4,"project":"<project>","event":"refused","artifact":"04-prototype.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"design-prototype","workflow":"design","phase":4,"project":"<project>","event":"started","artifact":"04-prototype.md","note":""}`.

Read `.singularskills/design/<project>/02-define.md` (required — hard gate enforced by hook).
Read `.singularskills/design/<project>/03-ideate.md`. If this file does not exist, tell the user:

> Phase 3 (Ideate) has not been completed for "<project>". Run `/design-ideate <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `.singularskills/design/<project>/02-define.md` for the component contract (props, variants, states, tokens)
   - Read `.singularskills/design/<project>/03-ideate.md` for the chosen design approach (if exists)
   - Read `references/component-contract-template.md` for reference

2. **Read the design system.** *Figma (read-tokens):* read the file's variables and styles for every token the contract names. *Without Figma:* read the values the user gave (in the request or in files it names), then the project's own token sources where the Stack section's `layout` says, else note `not checked` per token.

3. **Build the component.** *Figma (write-design):* following the patterns in `references/figma-capabilities.md`, create the base component with auto layout, text and shapes bound to the tokens read; one component per variant value with the axes in its name; combine them as a variant set laid out in a grid; apply each state (hover, focus, active, disabled, error, loading) as fills, opacity and effects; keep every node id you create. *Without Figma:* write a **build sheet** into the artifact instead: one table per variant axis and one per state with the exact token (or `not checked`) for every fill, stroke, text style, spacing and radius, the auto layout settings, and the variant grid, in the order a designer would build it.

4. **Verify.** *Figma (screenshot):* capture the variant set and compare it with the contract. *Without Figma:* re-read the build sheet against the contract's variant matrix and states.

5. **Write the artifact** to `.singularskills/design/<project>/04-prototype.md` with implementation notes

## References

- `references/stacks/bun-react-ts.md` and `references/stacks/rust-gpui.md`: the shipped stack profiles

## Output

The Figma component built on the canvas, or the build sheet, and notes written to `.singularskills/design/<project>/04-prototype.md`. Present to the user:
- Component node ids (in the `## Tools` section's `created:` line), or `build sheet` when no server was bound
- The screenshot of the component, when one was taken
- Any deviations from the contract and why
- Notes for the Test phase
- When the Stack section names a UI framework and no server was bound, one closing line offering `development-build` for a code prototype

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"design-prototype","workflow":"design","phase":4,"project":"<project>","event":"finished","artifact":"04-prototype.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: design-prototype
workflow: design
phase: 4
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
