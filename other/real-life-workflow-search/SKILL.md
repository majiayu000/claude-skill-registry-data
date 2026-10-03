---
name: real-life-workflow-search
description: Search the Real Life Workflows source universe and write a full workflow-understanding packet. Use when an operator or developer asks to find real-world workflow examples, research workflow patterns, create a workflow packet, compare adjacent workflow doors, or prepare source-backed candidates for later skill extraction in Claude Code, Codex, opencode, or another agent harness.
---

# Real-Life Workflow Search

Use this skill to search the Real Life Workflows catalog and create a durable
workflow-understanding packet.

## Agent Runtime Usage

This is a packaged skill for agent runtimes such as Codex, Claude Code,
opencode, and Antigravity-style environments. Invoke it as a skill from the
runtime surface. Do not treat the command wrapper as the primary operator path.

## Contract

- Start from the operator's workflow topic or job-to-understand.
- Search the curated workflow doors and adjacent source universe.
- Return a full packet by default, not only a ranked list.
- Write the packet to disk on every run.
- Report the packet path back to the operator.
- Include provenance in the packet.

## Packet Write Boundary

Before writing, identify the caller or primary project's approved artifact area.
Use that location as the output path.

Do not write packets into:

- `node_modules`
- dependency project trackers
- dependency `AGENTS.md` files
- dependency skill definitions
- this package's installed skill folder

If the caller has no approved artifact area, stop and ask for one. Do not pick
a dependency-owned path as a fallback.

## Skill Invocation

Ask the agent runtime to use `$real-life-workflow-search` with the workflow
topic and approved output artifact area:

```text
Use $real-life-workflow-search to create a workflow-understanding packet for
"customer billing exception workflows" and write it to the primary project's
approved workflow-packets artifact area.
```

Use a limit only when the operator asks for broader or narrower output:

```text
Use $real-life-workflow-search with a broader recommendation limit for
"document evidence research workflows".
```

## Package Smoke Test

Use the command wrapper only to verify the exported local package. It is not the
normal operator-facing skill invocation path:

```bash
npx real-life-workflow-search \
  --query "customer billing exception workflows" \
  --output projects/example/artifacts/workflow-packets/customer-billing-exceptions.md
```

The wrapper refuses protected output paths and creates parent directories for
valid packet paths.

## Packet Shape

Every packet must include:

- query
- intake question
- visible recommendation count
- provenance
- human review boundary
- Direct Matches
- Strong Adjacent Matches
- Supporting Building Blocks
- Maybe Useful

Every visible recommendation must include:

- why it matters
- why it is here
- what it does
- source link
- local door or source path
- reliability
- possible skill to extract
- expansion candidates when available

## Quarantine Boundary

The packaged search data comes from a quarantined import. Treat it as source
evidence only.

Do not report quarantined imported `SKILL.md` files as active Real Life
Workflows skills. They are not active callable skills, not discoverable as
project skills, and not promotable as-is. Future skills must be rewritten
through a tracked task before becoming active.

## Human Boundary

Workflow packets are learning and design artifacts. They do not prove medical,
legal, financial, compliance, engineering, safety, eligibility, coverage, or
operational correctness. Require human review before external action or before
turning a packet into a reusable skill.
