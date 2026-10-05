---
name: handoff
category: meta-orchestration
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
loop-eligible: false

compatibility: claude-code codex opencode
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

**Mark what you didn't verify.** The next agent reads this document as a contract and will not re-check it, so a belief written as a fact becomes a false premise for everything after it. "X isn't built", "Y is done", "Z doesn't work" — unless this session actually observed it, write it as an assumption and say what would confirm it. Downgrading a claim costs one word; a wrong premise costs the next session.

**Report the path prominently, and flag its lifespan.** Temp is deliberate — a handoff is a transit document, not an artifact to maintain — but it is not durable: some environments clear temp between sessions, and reboots take `/tmp` with them. Print the full path as the last line of the run, and say plainly that a handoff being picked up later than the next hour, or under a different harness, should be copied somewhere durable first. Anything the document *points at* in temp has the same lifespan.

**Hand it over by path, never by paste.** Tell the user to point the fresh agent at the file — pasting the summary into a shell argument mangles backticks and `$(...)`, and it truncates silently rather than erroring, so the next agent starts on a quietly incomplete brief.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/handoff.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
