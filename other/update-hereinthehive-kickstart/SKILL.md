---
description: Audit the project's Claude Code setup. Runs the curator (external best practices) and caretaker (internal integrity) subagents in parallel and presents merged findings in plain language.
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Agent
---

You are the `/update` orchestrator. Your job: invoke the curator and caretaker subagents in parallel, merge their findings, write `.claude/update-report.md`, and present the user with a friendly summary.

## Step 1: Tell the user what's about to happen

Brief plain-language preview:

> "I'll check your setup against current Claude Code best practices (curator) and audit the project's own state for clutter or rot (caretaker). About 30-60 seconds. I won't change anything without asking."

## Step 2: Invoke both subagents in parallel

In a single message, call the Agent tool twice:

- `subagent_type: curator` — prompt: "Audit the Claude Code setup in the current project root against current external best practices. Read CLAUDE.md, .claude/settings.json, .claude/skills/, and .claude/knowledge.md if present. Return findings in the format your subagent definition specifies. Do not modify files."
- `subagent_type: caretaker` — prompt: "Audit the project's internal integrity in the current project root. Check preference rot, adoption signals (kill criteria), and shim/config integrity per your subagent definition. Return findings in the format your subagent definition specifies. Do not modify files."

Both run concurrently. Wait for both before proceeding.

## Step 3: Merge findings

Compose `.claude/update-report.md` with this exact structure:

```
# Setup audit — [today's date]

## In plain words
[Friendly 2-3 sentence summary covering BOTH audits. Lead with overall health.
If there are quick wins, end with: "I can apply these for you if you'd like — just say yes."
Plain language only. No jargon.]

## What's healthy
[merged bullets from both subagents — "external" and "internal" tagged]

## What needs attention
[merged bullets, sorted by severity]

## Recommended removals
[caretaker's kill-criteria findings + any curator-flagged deprecations]

## Detailed findings
### From curator (external)
[curator's full structured output]

### From caretaker (internal)
[caretaker's full structured output]

## Next steps
- Want me to apply the quick wins? Say yes.
- Want to ignore a recommendation? Tell me which.
- Want more detail on something? Ask.
```

## Step 4: Present to the user

Show only the "In plain words" section in your response. The full report lives in `.claude/update-report.md` for reference. Then ask:

> "Want me to apply any of these? Tell me which, or say 'none' and we're done."

## Step 5: Apply on confirmation

If the user approves quick wins, apply them. If the user approves a removal, walk them through it explicitly (for skill removal, show which files would be deleted before doing it).

## Hard rule

Never auto-prune. Every preference removal, skill removal, or config change requires explicit user confirmation in the current session — even if `/update` is running via `/loop`.

## When invoked on a schedule (via `/loop weekly /update`)

Same flow. The user will see the "In plain words" summary in their next session's transcript. They can act on it then or not at all.
