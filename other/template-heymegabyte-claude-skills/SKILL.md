---
name: my-skill
description: >
  Use when [TRIGGER CONDITION — what causes someone to invoke this skill].
  Handles [PRIMARY TASK]. Outputs [DELIVERABLE].
  Keywords: [comma-separated discovery keywords]
license: MIT
compatibility: Requires any Agent Skills-compatible tool (Claude Code >=2.0.0, Codex, Cursor, Gemini CLI, …)
metadata:
  version: "1.0"
  author: brian@megabyte.space
  # internal: true  # Uncomment to hide from /menu picker. See rules/internal-skill-discovery.md.
allowed-tools: Read Grep Glob  # Add Bash(cmd:*) and mcp__server__* as needed.
---

<!-- Remove <SUBAGENT-STOP> unless this is a meta-skill (session-recap, self-improve, drift-check). -->
<!-- <SUBAGENT-STOP>: skip this skill when running inside a subagent. -->
<!-- <SUBAGENT-STOP/> -->

# [Skill Display Name]

One-sentence mission: what this skill accomplishes and for whom.

**When to use** — [specific trigger: "after a multi-agent run", "before deploying", "when asked to audit X"]
**Inputs** — `$ARGUMENTS` ([what the user passes]); [env vars or files consumed]
**Outputs** — [concrete deliverables: files created, reports, commands run]
**Verification** — [how to confirm the skill succeeded]
**Can update ~/.agentskills or ~/.claude?** [YES with scope / NO — project work only]

---

## Protocol

Step-by-step. Each step is a tool call or decision:

1. **[Step name]** — [what to do]. Use `[ToolName]` with `[specific args]`.
2. **[Step name]** — [what to do].
3. **[Step name]** — [what to do].

If [edge case], then [alternative path].

---

## Output format

```
[SKILL NAME]: [scope or target]

[SECTION]:
- [item]

STATUS: PASS / FAIL / [domain-specific]
```

---

## Rules

- [Non-negotiable constraint 1]
- [Non-negotiable constraint 2]
- Never [anti-pattern].

---

## See

- `[[rule-name]]` — [why relevant]
- `[[skill-name]]` — [relationship]
- `references/REFERENCE.md` — [if you have a references/ subdir]
