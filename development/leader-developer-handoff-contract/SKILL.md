---
name: leader-developer-handoff-contract
description: Shape the prompt a Leader sends when dispatching a sub-agent (Developer, Designer, Code Reviewer, drafting agent) so the result comes back verifiable and integrable. Use when about to call the Agent tool, writing or reviewing a dispatch prompt, deciding what a sub-agent must read or which skills it must invoke, or when asked "what should the sub-agent prompt include" / "which element am I missing". Does NOT own how many review rounds to run or how findings are adjudicated (subagent-review-cycles), nor the impl-notes file format (agent-impl-notes-log).
---

# Leader → Developer Handoff Contract

## Native mechanism

Claude Code's [Subagents](https://code.claude.com/docs/en/subagents) feature already gives a dispatched agent "its own context window with a custom system prompt, specific tool access, and independent permissions" — but the platform doesn't require or shape what goes in the dispatch *prompt* itself. This skill is the discipline layer on top: the 6 elements a prompt must contain regardless of how well-configured the subagent's own definition is.

- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.

## When to invoke

- About to dispatch a sub-agent (Developer / Designer / Code Reviewer / drafting agent).
- Writing the dispatch prompt.
- User asks "what should the sub-agent dispatch include / which elements am I missing".

## The 6 required elements

Every dispatch prompt must contain:

### 1. Task scope with verifiable target

- One sentence stating the goal.
- Explicitly name **the output file / section / behaviour**.
- Include a mechanically checkable success / failure condition.

**Good**: "Draft §5 Logger for `docs/foundations.md`; output format: complete markdown section; scope: adopt `os.Logger` defaults, with subsystem / category conventions and privacy default"

**Bad**: "Write something about logger"

### 2. Files / docs the sub-agent should read

- List file names + sections.
- Don't say "read design.md"; say "read `design.md §How.2`, `foundations.md §3-§4`".
- Add grep targets / line ranges when useful to save the sub-agent's exploration tokens.

### 3. Explicit skill list to invoke

- List the skill names the sub-agent should invoke (with plugin prefix).
- Don't assume the sub-agent will guess.
- Example: "invoke `apple-dev-skills:swift6-concurrency`, `apple-dev-skills:swiftpm-modularization`, `apple-dev-skills:swift-testing-baseline`; review-style dispatches also list `collaboration-skills:subagent-review-cycles`".
- When the dispatch target is a custom agent (`.claude/agents/` or a plugin's `agents/`), list them in that agent's `skills:` frontmatter instead — Claude Code preloads those at startup (the full skill content is injected, not only the description), so the prompt only needs to name skills the agent definition doesn't already carry. See https://code.claude.com/docs/en/sub-agents.

### 4. Expected return format

Pick one explicitly (or custom):
- **Code diff** (patch / full-file rewrite)
- **Markdown section** (drop into a specified file's §)
- **Decision text** (structured ACCEPT/REJECT/DEFER list)
- **Finding list** (BLOCKER / MAJOR / MINOR)

**Bad**: "Report results"
**Good**: "Return the complete §5 content as markdown, ready for the Leader to paste into `foundations.md`; no chit-chat"

### 5. Verification criteria

- The conditions under which it counts as done.
- For Developer: which tests must be green, which invariants must hold.
- For Code Reviewer: review dimensions; CLI is forbidden for probing API/runtime behavior (build, run, simctl, trial-and-error); read-only search (grep, rg, git log, git show) is allowed; allowed tools (WebSearch).
- For drafting agent: section structure, required subsections, required decisions.

### 6. Impl notes (non-trivial tasks)

Required when the task touches ≥2 files or adds new behavior (this catalog's M/L task-sizing
convention, if your workflow defines one); optional for a trivial one-file fix. Tell the sub-agent to open its running
impl-notes file at the *start* of the task, not when it first hits trouble — early assumptions
and scope calls are exactly what's invisible by the time a report is written.
`agent-impl-notes-log` owns the file's format and routing; this contract is what makes it start
on time, since that skill's own trigger fires on mid-task ambiguity.

## Template

```
You are a <role> dispatched by the Leader.

## Task scope
<verifiable target, output file/section, success condition>

## Inputs (read these in order)
1. <path> §<section>
2. <path>
<...>

## Skills to invoke
- <skill-name-1>
- <skill-name-2>
<...>

## Return format
<one of: code diff / markdown section / decision text / finding list>
<exact shape>

## Verification criteria
- <criterion 1>
- <criterion 2>
<...>

## Impl notes (non-trivial tasks)
Required if this task touches ≥2 files or adds new behavior: open `meetings/{date}_{topic}.impl-notes.md` at the start of the task (`collaboration-skills:agent-impl-notes-log`).

## Constraints (optional)
- DO NOT <forbidden action>
- DO use <required tool / approach>
- Base SHA (when `isolation:"worktree"`): <sha>; verify with `git log --oneline -5` before editing (see `subagent-conflict-detection`)
```

## Examples drawn from real dispatches

### Developer drafting design.md §How.3 (a feature section)

- **Scope**: draft `design.md §How.3` for the feature named in §What, covering its component / protocol / auth-fallback / scope breakdown
- **Inputs**: `design.md §What.<feature>`, `foundations.md §1-§4`
- **Skills**: `apple-dev-skills:swift6-concurrency`, `apple-dev-skills:swiftpm-modularization`, `apple-dev-skills:swift-testing-baseline`
- **Return**: complete markdown section, ready to merge into design.md
- **Verification**: includes the entities §What enumerates, the protocol covers the scope §What defines, auth failure has a fallback path

### Code Reviewer round 1 over §How 1–7

- **Scope**: review `design.md §How.1 – §How.7` for technical correctness
- **Inputs**: full design.md, foundations.md
- **Skills**: `collaboration-skills:subagent-review-cycles`
- **Return**: BLOCKER / MAJOR / MINOR finding list; each item with section location + suggestion
- **Verification**: covers 4 dimensions (correctness / consistency / completeness / efficiency); cites Apple docs instead of CLI experimentation
- **Constraints**: CLI is forbidden for probing API/runtime behavior (build, run, simctl, trial-and-error); read-only search (grep, rg, git log, git show) is allowed; DO use WebSearch

## Anti-patterns

- **Omitting verification criteria**: the sub-agent self-judges "done", often misaligned with the Leader's expectation.
- **Listing "related skills" instead of "skills to invoke"**: the sub-agent may not actually trigger them.
- **Return format written as "free-form"**: every round looks different and integration cost balloons.
- **Scope too large (multiple sections / files in one round)**: review and revision cost explodes; split fine.

## Verification checklist (for Leader before sending dispatch)

- All 6 elements present (scope / inputs / skills / return format / verification / impl-notes).
- Scope corresponds to "one verifiable target", not "a basket of work".
- Skill names spelled correctly, with plugin prefix.
- Return format is one of the four explicit categories.
- Verification conditions are mechanically checkable.
- Impl-notes slot included when the task touches ≥2 files or adds new behavior.

## Related skills

- `subagent-review-cycles`: handoff is the starting point of each review-cycle round.
- `spec-phase-orchestration`: every sub-agent dispatch in the spec phase follows this contract.
- `session-to-meeting-log`: dispatch + returned-result summary lands in the meeting log.
