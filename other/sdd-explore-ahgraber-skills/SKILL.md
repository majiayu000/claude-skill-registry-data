---
name: sdd-explore
description: |-
  Use when the user wants to think through ideas, investigate problems, or clarify requirements before or during any SDD path. Triggers: "explore", "think through", "help me figure out", "what should I build", "I'm not sure where to start", "let's brainstorm", "investigate this", "I want to explore".
---

# SDD Explore

Thinking partner for spec-driven development.
No fixed steps, no mandatory output.
Available before or during any SDD path.

> `SPECS_ROOT` is resolved by the `sdd` router before this skill runs.
> Replace `.specs/` with your project's actual specs root in all paths below.

## Writing Style

The conversation stays exploratory, but any artifact the user decides to keep is written in the voice of a professional technical writer.
Prefer ASD-STE100 Simplified Technical English: short sentences, one instruction per sentence, active voice, and one term per concept.
Keep identifiers, commands, paths, and RFC 2119 keywords exact.

## When to Use

- Before starting any SDD workflow — explore before speccing
- When requirements are unclear and writing a spec would be premature
- During change work when a decision blocks progress
- When you want to investigate the codebase before deciding what to spec

## When Not to Use

- You already know what to build — jump to `sdd-propose` or `sdd-derive`
- You have existing specs to convert — use `sdd-translate`

## Invocation Notice

- Tell the user when this skill is running: `sdd-explore`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Hard Rule: No Code

**Never write or implement code in this skill.**

Reading files and searching the codebase is fine — that's investigation.
Writing SDD artifacts (proposals, designs, specs) is fine — that's capturing thinking.
Writing implementation code is not allowed.

## Approach

### Start with the user's question

Ask: what are you trying to figure out?

Common entry points:

- "I want to understand how X works before speccing it"
- "I'm not sure if this should be one change or two"
- "I need to figure out the right capability breakdown"

### Read existing context

Before forming opinions:

1. Check `SPECS_ROOT/specs/` for existing baseline specs
2. Check `SPECS_ROOT/changes/` for active changes
3. Read relevant code files if the user wants codebase investigation

**One-time suggestion (codebase investigation only):** If the user wants to investigate the codebase, check `SPECS_ROOT/.sdd/suggested-tools`.

- If `code-review-graph` is not listed: present the suggestion below, then append `code-review-graph` to that file (create the file and directory if needed).
  Do this once and only once.
- If already listed: skip the suggestion.

> **Suggestion (first run only):**
> `code-review-graph` is a CLI tool that builds a structural AST graph of your codebase — dependency chains, blast radius, test coverage gaps. Useful for surfacing non-obvious architecture before speccing. Install: `uv tool install code-review-graph`. Say "skip" to dismiss. This won't appear again.

### Thinking tools

Use freely:

- ASCII diagrams for architecture and flows
- Decision tables for tradeoffs
- Lists of forces for or against an approach
- Stakeholder maps, actor lists
- Numbered alternatives with tradeoffs
- **Graph-aided investigation** (if `code-review-graph` is installed) — blast-radius queries, dependency chains, test coverage gaps.
  Run `code-review-graph build` then query by capability entry point.

### Crystallization

When thinking becomes clear enough to act:

- Offer to create an artifact: "Want me to capture this as a proposal?"
  or "Should I sketch a design?"
- Route to the right skill: `sdd-propose`, `sdd-derive`, `sdd-translate`
- Don't force it — the user decides when thinking is done

## Output

No required output.
May produce:

- Notes, summaries, or decision records (in the conversation)
- SDD artifacts if the user decides to capture decisions (proposal.md, design.md)
- A recommendation for which SDD skill to run next

## What You Don't Have To Do

- Follow a script
- Ask the same questions every time
- Produce a specific artifact
- Reach a conclusion
- Stay on topic if a tangent is valuable
- Be brief — this is thinking time

## Common Mistakes

- Writing implementation code (forbidden)
- Treating explore as a required step — it's optional, not a gate
- Forcing an artifact when the user just wants to think
- Not reading existing specs before forming opinions about the domain
