---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [productivity, agent-workflow, handoff, collaboration]
---

**Trigger**: Use when you need to compact the current conversation into a handoff document so another agent or session can continue the work without losing context.

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Pitfalls
- Over-sharing context: include only what the next session needs, not the entire transcript.
- Ambiguous next steps: be specific about what the next agent should do first.
- Missing dependency context: if you installed tools or set env vars, include the commands.

## Verification
- Can another agent pick up the handoff and start working within 2 turns?
- Are all file paths absolute or relative-to-project-root?
- Does the handoff document fit in a single screen?

## Procedure
1. Scan the conversation history and extract: current goal, completed work, decisions made, open questions, and next steps.
2. Identify key files and directories modified — include their paths and a summary of changes.
3. Identify unresolved issues, blockers, and partial work.
4. Write the handoff document to a file using a structured format: `## Goal`, `## Progress`, `## Decisions`, `## Next Steps`, `## Open Questions`, `## Files Touched`.
5. Optionally include exact commands, API keys to re-export, or environment state needed to resume.
