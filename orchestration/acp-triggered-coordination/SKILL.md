---
name: acp-triggered-coordination
description: Use ACP as the trigger mechanism for agents to inspect and act on external context such as GitHub issues, PRs, and wiki changes. Use when one agent needs another agent to review a visible artifact and respond through the appropriate GitHub surface rather than through hidden chat alone.
---

# ACP-triggered coordination

Use ACP to trigger attention, not to replace durable external context.

## Principle
If the real coordination object is an issue, PR, or wiki page, keep the substantive discussion there.
Use ACP to tell the relevant agent to inspect that artifact and respond or act.

## Preferred pattern
1. write the question, assumption, or request on the GitHub issue or PR
2. use ACP to notify the relevant agent to review that artifact
3. have the agent respond by acting on the artifact or by asking for the right follow-up there

## Applies especially to
- Builder asking Spec or Orchestrator for clarification
- QA asking for a product-level decision
- specialists asking their parent agent to inspect externally visible context

## Avoid
- resolving durable project questions only inside hidden agent chat
- treating ACP conversation as the system of record when the issue or PR should hold the answer
