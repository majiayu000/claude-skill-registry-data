---
name: setup-pstack
description: Configure pstack for Codex using project-local explicit preferences.
  Use when asked to set up pstack, change review counts or inspect available delegation
  capabilities.
---

# Setup pstack for Codex

Read [Codex runtime contract](../../CODEX-RUNTIME.md).

1. Inspect the current host tool schemas and project AGENTS.md. State whether delegation, browser interaction and authenticated forge access are actually available. Do not invoke external actions to probe authorization.
2. Read .agents/pstack-config.md if present. Missing configuration needs no setup: every role inherits the parent model and effort, and comparisons use two independent runs where permitted.
3. Resolve the user's requested changes. For unspecified settings preserve the defaults. Only propose model overrides that the actual host exposes and applicable instructions authorize. Do not manufacture an entitlement list or modify host model settings.
4. Write the following project-local Markdown file, preserving unrelated content if one exists. poteto-mode reads it explicitly. This is not an always-loaded Codex rule.

```markdown
# pstack for Codex preferences
All roles: inherit-parent
Candidate count: 2
Review count: 2
Execution: native delegation when available and permitted; sequential otherwise
Scheduling: session-bounded; no background schedule provisioned
```

5. Report the written path and actual capability limits. Existing harnesses remain authoritative; when no behavioral harness exists, mention create-verification-skill only if relevant to the task.
