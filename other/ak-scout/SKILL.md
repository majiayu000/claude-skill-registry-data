---
name: ak-scout
description: "Scout a codebase fast with native search, optional Explore agents and user-permitted OpenCode probes."
when_to_use: "Invoke for file discovery, task context or scoped searches."
category: workflow
keywords: [codebase, scouting, file-discovery, search]
argument-hint: "[search-target] [ext] [--ultra]"
metadata:
  author: agentkit
  version: "1.1.2"
---

# Scout

Fast, token-efficient codebase scouting using parallel agents to find files needed for tasks.

## Arguments
- Default: Use local search for one owner/path; partition only independent domains when delegation is authorized and useful (`./references/internal-scouting.md`)
- `ext`: Scout using user-permitted OpenCode probes when native/local search is insufficient (`./references/external-scouting.md`)
- `--ultra`: Run the scout as a best-of-5 verifier pass (see Ultra Verifier Mode)

## When to Use

- Beginning work on feature spanning multiple directories
- User mentions needing to "find", "locate", or "search for" files
- Starting debugging session requiring file relationships understanding
- User asks about project structure or where functionality lives
- Before changes that might affect multiple codebase parts

## Fast path

For one pathname/symbol, search locally and return the verified path/role directly. Reuse a
source map while its revision and relevant files are unchanged. No standalone report is
required for one lookup. Use the fuller workflow below only for multiple independent domains;
explicit `--ultra` retains its separate five-candidate contract.

## Quick Start

1. Analyze user prompt to identify search targets
2. Use a wide range of `search_files` patterns to find relevant files and estimate scale of the codebase
3. Spawn parallel agents with divided directories only when the active runtime permits delegate_agent usage
4. Collect results into concise report

## Runtime Tooling

Use portable capabilities first:
- `search_files` for local discovery.
- `read_file` for scoped file reads.
- `run_shell` for local commands such as `rg`, `wc`, or `sed`.
- The live task-management surface for progress tracking when useful.
- `delegate_agent` for Explore subagents only when user request and runtime policy allow delegation.

Delegation follows the runtime's permission model rather than this skill's
text: some runtimes, including Codex Desktop, allow subagents only when the
user's own request asked for delegation or parallel agent work. Where that
authorization is absent, this skill scouts inline in the main agent with
`search_files` and `read_file`, which produces the same map and only costs
wall-clock.

Runtime mapping for `delegate_agent`:
- Claude Code: use the native delegate call with `subagent_type: "Explore"`.
- Codex Desktop: Explore is a deferred multi-agent role. If `multi_agent_v1`
  is not visible, call `tool_search` for multi-agent spawn tools first, then use
  `multi_agent_v1.spawn_agent` with `agent_type: "Explore"`. Do not set a model
  override; the Explore role owns its runtime model configuration.

## Workflow

### 1. Analyze Task
- Parse user prompt for search targets
- Identify key directories, patterns, file types, lines of code
- Determine optimal SCALE value of subagents to spawn

### 2. Divide and Conquer
- Split codebase into logical segments per agent
- Assign each agent specific directories or patterns
- Ensure no overlap, maximize coverage

### 3. Register Scout Work
- **Skip if:** Agent count ≤ 2 (overhead exceeds benefit)
- Discover the live task-management surface and check for existing scout work
- If available, register one scoped item per agent; otherwise update the active plan
- Keep tracking concise: scope, assigned directories, current status, and timeout
- Treat the active plan as the durable source of truth

### 4. Spawn Parallel Agents
Load appropriate reference based on decision tree:
- **Internal (Default):** `references/internal-scouting.md` (Explore subagents)
- **External:** `references/external-scouting.md` (OpenCode)

**Notes:**
- Record each scope as in progress before spawning its agent
- Prompt detailed instructions for each subagent with exact directories or files it should read
- Size each scope to fit one subagent's context window; a scope that cannot fit is two scopes
- Amount of subagents to-be-spawned depends on the current system resources available and amount of files to be scanned
- Each subagent must return a detailed summary report to a main agent
- In Codex Desktop, first expose deferred multi-agent tools through `tool_search` if they are not already visible.
- If runtime policy blocks subagents because the user did not explicitly request delegation, continue with main-agent scouting instead of forcing a spawn.

### 5. Collect Results
Invoke "the engineer project-organization skill" skill to organize the outputs.

- Timeout: 3 minutes per agent (skip non-responders)
- Record completed scopes and log timed-out agents in the report
- Aggregate findings into single report
- List unresolved questions at end

## Report Format

```markdown
# Scout Report

## Relevant Files
- `path/to/file.ts` - Brief description
- ...

## Unresolved Questions
- Any gaps in findings
```

## Ultra Verifier Mode (`--ultra`)

When `--ultra` is present, run the scout as a best-of-5 verifier pass instead
of a single pass. The controller builds one immutable evidence packet (the
search targets, scope boundaries, and any prior findings) plus a rubric, then
dispatches exactly five independent read-only candidate scout passes in one
parallel wave; a single strongest-model verifier scores them.

- **Candidate task:** each candidate produces a complete scout report — relevant
  files with one-line roles, relationships, and unresolved questions — from the
  same evidence packet.
- **Rubric:** coverage of the stated targets, evidence quality (paths verified,
  roles accurate), signal density, and honesty about gaps.
- **Finalizer:** the verifier returns the
  evidence-validated, deduplicated union of scouted findings across the five
  passes — a relevant file may surface in only one candidate. It drops paths it
  cannot validate; the controller emits the merged report.

Scout's no-delegation degrade path does not apply under `--ultra`: if the
runtime cannot dispatch five parallel read-only candidates,
hard-stop and name the missing capability — never degrade to main-agent
scouting for an ultra run. Full mechanics (evidence packet, anonymization, the
five-usable-candidate gate, reject-all, fail-closed dispatch) are in
`../ak-brainstorm/references/ultra-verifier-mode.md`. It is a best-of-5
verifier mode inspired by LLM-as-a-Verifier, not the full framework.

## References

- `references/internal-scouting.md` - Using Explore subagents
- `references/external-scouting.md` - Using user-permitted OpenCode probes

## Workflow Position

**Typically precedes:** `/ak-fix` (fix after locating code)
**Related:** `the engineer debug skill` (investigate after scouting), `/ak-brainstorm` (explore after scouting), `the installed code-review skill` (scout edge cases before review, engineer tier)
