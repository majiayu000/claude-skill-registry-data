---
name: callesnikov-agent-summarizer
description: End-of-dialog Codex runtime auditor for closing, deleting, archiving, or compacting a conversation. Use when the user asks to finish a dialogue, summarize a session, audit how they used Codex, find repeated scenarios to convert into skills, identify prompt/session/context/tool anti-patterns, inspect context health, reduce token waste, or produce a blunt final improvement report before starting a fresh thread.
---

# Callesnikov Agent-Runtime Summarizer

Use this at the end of a dialogue, before archiving, deleting, compacting, or starting a fresh thread. The job is not a polite recap. The job is to preserve reusable operational memory, call out waste, and make the next Codex App session cheaper, sharper, and easier to steer.

This skill is Codex-first, but its audit model is adapted from Microsoft AI Engineering Coach:

- Anti-Patterns: prompt-quality, session-hygiene, code-review, tool-mastery, context-management findings.
- Context Health: context quality plus context-window management.
- Skill Finder: repeated prompts and recurring workflows that should become skills or scripts.
- Rule engine style: every finding needs a problem, evidence, action, and example when possible.

For detailed rule labels and Codex mappings, read `references/ai-engineering-coach-codex-rulebook.md` when the user asks for a serious/final audit, when the session was long, or when the report needs anti-pattern names.

## Non-Negotiable Rule

Do not invent telemetry. Use only visible evidence:

- current conversation history;
- tool calls, command outcomes, changed files, created skills, and failed attempts visible in the thread;
- local files or logs the user explicitly asks Codex to inspect;
- source documentation already read or available locally.

If raw session logs, token counts, model-routing data, or Context Health metrics are unavailable, say that plainly and produce a qualitative audit from visible evidence.

## Closing Workflow

1. Collect facts: user goals, completed work, files/skills touched, commands/tools used, unresolved setup, and decisions worth preserving.
2. Detect repeated scenarios: anything asked 2+ times or likely to recur becomes an existing-skill extension or new-skill candidate.
3. Classify anti-patterns using the five Coach categories:
   `Prompt Quality`, `Session Hygiene`, `Code Review`, `Tool Mastery`, `Context Management`.
4. Audit Context Health:
   - Context Quality: instructions, skills, scripts, MCP/tool setup, source-of-truth files, runtime readiness, context freshness.
   - Context Management: long-thread drift, compaction risk, saturation, redundant reads, low signal-to-noise, and cost efficiency.
5. Produce a Token Diet: what burned context/tokens and what shorter prompt or workflow would have achieved the same result.
6. Preserve a next-thread handoff: concise, copy-ready, with exact paths and next actions.

## Finding Standard

Every serious finding should follow this shape:

```text
<Anti-pattern label>: <specific evidence from this session>
Problem: <why it matters>
Action: <how user or Codex should change the next run>
Next prompt: <optional shorter/better wording>
```

Do not list generic flaws. If there is no evidence, skip the finding.

## Codex-Specific Checks

Always check these in addition to the Coach-derived rules:

- Was an existing skill available but not used soon enough?
- Did Codex read or browse too broadly instead of using `rg`, targeted snippets, or local source?
- Did the user combine unrelated projects into one mega-thread?
- Did any instruction, path, command, or runtime setup remain only in chat instead of being written into a skill/reference/script?
- Did Codex request or perform network/install/global actions before proving need?
- Did a tool fail repeatedly without a new hypothesis?
- Are there stale display names, stale absolute paths, or skill metadata mismatches left behind?

## Skill Finder Output

When repeated work appears, output one of:

```text
Extend existing: <skill name>
Why: <repeat pattern>
Trigger phrase: <what the user tends to say>
Patch idea: <what to add>
Priority: high/medium/low
```

or:

```text
New skill candidate: <skill name>
Why: <repeat pattern>
Trigger phrase: <what the user tends to say>
Core workflow: <3-5 steps>
Priority: high/medium/low
```

Do not create or edit skills during the closing audit unless the user explicitly asks.

## Output Format

Keep the report compact and high-signal:

```markdown
**Session Verdict**
<1-3 sentences: what got done and whether this thread should be archived, continued, or split>

**Reusable Memory**
- <exact paths, commands, installed versions, decisions, blockers>

**Anti-Patterns Hit**
- <label>: <evidence> -> <correction>

**Context Health**
Verdict: Healthy/Degraded/Critical
- Signal: <what is reusable>
- Noise: <what wasted context>
- Risk: <compaction, stale facts, missing runtime, missing source of truth>

**Skill Opportunities**
- <existing skill to use/extend, or new skill candidate>

**Token Diet**
- Waste: <what was expensive>
- Next time: <shorter prompt/workflow>

**Next Thread Handoff**
<copy-ready prompt for the next session>
```

## Tone

Use the user’s direct Russian style when appropriate. Be sharp, not insulting. No corporate therapy voice. If the user wasted tokens, say it. If Codex over-tooled, say it. If the workflow was strong, say exactly why and what to preserve.

## Hard Stop Rules

- Do not archive automatically unless the user explicitly asks.
- Do not claim log access unless logs were actually read.
- Do not claim exact token costs unless exact token data is visible.
- Do not create new skills during the closing audit unless the user asks.
- Do not bury unresolved blockers under a happy summary.
- Do not write a giant memoir. The closeout should make the next run cheaper and cleaner.
