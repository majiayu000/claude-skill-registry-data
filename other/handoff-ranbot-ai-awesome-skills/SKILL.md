---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. 
category: Document Processing
source: antigravity
tags: [api, claude, ai, agent, workflow, document]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/handoff
---


## When to Use

Use when this workflow matches the user request: Compact the current conversation into a handoff document for another agent to pick up.


_Source: [mattpocock/skills](https://github.com/mattpocock/skills) (MIT)._Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Example

**User request:**

> Use @handoff for this task: Compact the current conversation into a handoff document for another agent to pick up.

## Limitations

- Requires the upstream tool, account, API key, or local setup when the workflow names one.
- Does not authorize destructive, production, paid, or external-message actions without explicit user approval.
- Validate generated artifacts or recommendations against the user's real sources before treating them as final.
