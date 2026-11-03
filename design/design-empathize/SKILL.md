---
name: design-empathize
description: Research a UI component before designing it — user needs, related components in the Figma design system and applicable WCAG requirements — into a research brief. Use when the user wants to design a new component and has nothing yet beyond its name or idea. Not for starting the whole design thinking process; see /workflow.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: design
  phase: 1
  artifact: 01-empathize.md
  figma-aware: true
---

# Empathize

Research the problem space for "$ARGUMENTS" before any design work begins. Gather user needs, existing patterns, accessibility requirements, and contextual constraints.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"design-empathize","workflow":"design","phase":1,"project":"<project>","event":"skipped","artifact":"01-empathize.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Empathize) of the Design Thinking workflow (`design`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `design` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise, unless the user named this skill, ask one question, since this is the first phase of its workflow: "Just this step, or the whole Design Thinking workflow?" End your turn and wait; on the whole workflow, hand off the same way; on just this step, continue here.

**Recall.** Before you ask the user anything, look for what this repository already holds about `<project>`: if a tool is available whose description says it searches or maps this repository (a memory or repo-map server such as `repo_map` or `entities`), query it for `<project>` and this phase's subject and read what it returns, keeping only results from this repository; in every case also list `.singularskills/*/<project>/` and read the **Decisions** and **Open questions** of any artifact there, and the lines of `.singularskills/log.jsonl` whose `project` is `<project>`. After the frontmatter and title, add a `## Recalled` section of at most ten lines naming what you found and where (path or tool), or the single line `Nothing recalled: no earlier artifacts, log lines or memory results for <project>.` Ask the user only what this did not answer. The trail's shape is described in `references/memory/trail.md`, bundled with this skill.

**Figma.** Steps marked *Figma* use a Figma MCP server you connect to this agent yourself; this pack ships none and makes no network calls. Before you ask the user anything or run the first such step, list the tools available to you and bind each capability the step names to one tool, as `references/figma-capabilities.md`, bundled with this skill, describes: the official Figma server's tool named there, else any tool whose description plainly does the same thing. With a capability bound, take the file key and node id from a Figma link in the request or the conversation, else from the `file:` line of the `## Tools` section of the latest earlier artifact of this project that has one; when a bound capability needs one and there is none, ask for the link once, with any other question you ask. With nothing bound, never ask for a link. Record the result in a `## Tools` section after any `## Recalled` section: a `- file:` line (the Design file; a board or a deck goes on a `- board:` or `- deck:` line), one line per bound capability (`- read-tokens: get_variable_defs (figma)`), and a `- created:` line for node ids you created; or the single line `No Figma server: steps marked Figma ran without one.`; a skill with no artifact says the same in its summary. For an unbound capability do what the step's *Without Figma* line says, using first any values the user gave in the request or in files it names: never ask the user to connect a server, never invent values a tool would have returned, and never report a step as run when it was not.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"design-empathize","workflow":"design","phase":1,"project":"<project>","event":"started","artifact":"01-empathize.md","note":""}`.

None — this is the first phase.

## Process

1. **Ask, after the Recall step, before anything else.** Ask one question at a time, in plain language, about the component's users (who picks with it and why), the contexts it appears in (which flows, platforms and locales) and known constraints (an existing component being replaced, complaints, deadlines). End your turn after the first question and wait for the answer; ask the next only if the answer leaves a gap the brief needs. Never ask about tooling: a missing Figma server or an unreadable file is noted in the brief, not raised with the user; a link to the design file is not tooling: when a capability is bound and no link was given, ask for it with your other questions.

2. **Read the design system.** *Figma (read-tokens, find-components, read-node, screenshot):* read the file's variables and styles, search its libraries for components that overlap with or relate to "<project>", and read the structure and a screenshot of each related component; document what exists, what works well and what is missing. *Without Figma:* read the values the user gave (in the request or in files it names), then the project's own token and component sources (a `tokens` package, CSS custom properties, a Tailwind config, component folders); for anything neither gave you, write one line under a **Not checked** heading in the brief and continue.

3. **Review accessibility requirements:**
   - Read `references/wcag-criteria.md` for applicable WCAG criteria; if it cannot be read, note that under **Not checked** and apply WCAG 2.2 AA from your own knowledge
   - Compute the contrast of each colour pair the related components use, as `references/a11y-checks.md` describes, marking each pair `computed` or `not checked`
   - Note specific accessibility requirements for this component type

4. **Synthesize findings** into a research brief covering:
   - User needs and common use cases for this component type
   - Existing patterns found in the design system
   - Accessibility requirements and considerations
   - Contextual constraints (design tokens available, conventions established)
   - Gaps and opportunities

5. **Write the artifact** to `.singularskills/design/<project>/01-empathize.md`

## Output

The research brief written to `.singularskills/design/<project>/01-empathize.md`. Present a summary to the user highlighting:
- Key user needs identified
- Existing components found (if any)
- Critical accessibility requirements
- Recommended approach for the Define phase

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"design-empathize","workflow":"design","phase":1,"project":"<project>","event":"finished","artifact":"01-empathize.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `none`, as this phase has no gate):

```yaml
---
skill: design-empathize
workflow: design
phase: 1
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
