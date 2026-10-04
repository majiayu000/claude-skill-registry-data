---
name: repoprompt-agent-run-mcp-not-inherited
description: |
  Fix for `mcp__RepoPrompt__agent_run` subagents failing at dependency-check
  because non-RepoPrompt MCP servers (`mcp__seo-utils__*`, `mcp__open-brain__*`,
  and other custom MCPs) are NOT inherited by spawned sub-agent sessions — only
  `mcp__RepoPrompt__*` is. Use when: (1) you delegated a skill via `agent_run
  op=start` and the subagent stops at Step 0 reporting "MCP X is not connected
  in this session", (2) a skill's `allowed-tools` frontmatter declares
  `mcp__seo-utils__*` or `mcp__open-brain__*` and yet a sub-agent claims those
  tools are unavailable, (3) you're designing a skill with mixed MCP
  dependencies and need to decide which steps must run inline in the parent
  session vs which can be safely delegated. Covers the inheritance rule, the
  orchestrator-vs-subagent role distinction, and the skill-design pattern for
  marking non-delegatable steps.
author: Claude Code
version: 1.0.0
date: 2026-05-02
---

# RepoPrompt agent_run MCP not inherited

## Problem

When you spawn a sub-agent with `mcp__RepoPrompt__agent_run op=start`, the
sub-agent's Codex CLI session does NOT inherit all the MCP servers that are
mounted in the parent (the session you are running in). Specifically: only
`mcp__RepoPrompt__*` is reliably available in the spawned session. Any other
MCP server you have configured — `mcp__seo-utils__*`, `mcp__open-brain__*`,
`mcp__chrome-devtools__*`, and so on — is NOT mounted in the sub-agent.

This is silent. The sub-agent does not warn you up front; it only discovers
the missing MCP when it tries to call a tool, at which point it stops and
reports something like *"`seo-utils` MCP is not connected in this session"*.
If the skill is well-written it will halt at a dependency check; if not, it
may silently degrade or hallucinate around the missing capability.

The skill's own `allowed-tools` frontmatter does not save you. Listing
`mcp__seo-utils__query_database` in `allowed-tools` is a permissions
declaration — it does not cause the MCP to be mounted in the spawned session.

## Trigger conditions

Any of:

1. You spawned a sub-agent via `agent_run op=start` and `op=wait`/`op=poll`
   returns a `Completed` status whose output reads *"X MCP is not connected
   in this session"* or *"only RepoPrompt is present"*.
2. A skill you delegated declares non-RepoPrompt MCP tools in its
   `allowed-tools` frontmatter (`mcp__seo-utils__*`, `mcp__open-brain__*`,
   etc.) and the sub-agent claims those tools are missing despite the
   declaration.
3. You're designing a skill that mixes RepoPrompt MCP work (file IO, code
   navigation) with non-RepoPrompt MCP work (database queries, semantic
   search, browser automation) and need to decide which steps can run in a
   delegated sub-agent and which must run in the parent session.

## Solution

The fix depends on which side you're on.

### If you're TRIGGERING this skill (delegated a skill that failed)

Don't wholesale-delegate the whole skill. Run the orchestrator role yourself
in the parent session — the one that has the missing MCP mounted — and
delegate only the sub-steps that need RepoPrompt MCP.

Concretely, for skills like `service-tier-brief-generator` and
`failure-brief-generator` that have a documented "runs inline in the
orchestrator" step:

1. Stay in the parent session (where seo-utils + OB1 are mounted).
2. Run the orchestrator-side steps yourself: GSC database queries, OB1
   thought searches, anything else that uses the non-RepoPrompt MCP.
3. Delegate only the wiki/repo research agents (Step 2 + Step 3 in those
   skills). Those use RepoPrompt MCP exclusively, so they are safely
   delegatable.
4. Synthesise the final artifact yourself, reading the dossier files the
   delegated agents wrote.

### If you're DESIGNING a skill that wants to be delegatable

Treat sub-agent capability as a strict subset:

| MCP class | Available in parent? | Available in sub-agent? |
|---|---|---|
| `mcp__RepoPrompt__*` | Yes | **Yes** |
| All other MCPs (seo-utils, open-brain, chrome-devtools, etc.) | Yes | **No** |
| Built-in tools (Read, Write, Bash, Edit, Glob, Grep) | Yes | Yes |

Design your skill's pipeline accordingly:

- **Steps that use only RepoPrompt MCP or built-ins**: safely delegatable.
  Dispatch with `agent_run op=start model_id="explore"|"engineer"|...`.
- **Steps that use other MCPs**: mark them inline-only. Add an explicit
  callout in the step heading so the next person doesn't try to wholesale-
  delegate the skill.
- **Mixed skills**: the parent session plays the orchestrator role. Dispatch
  the safely-delegatable parts; run the rest inline. This is the pattern
  used by `service-tier-brief-generator` Step 1b and `failure-brief-generator`
  Step 1b.

Recommended callout wording (mirror this in your own skills):

```markdown
**Architectural constraint — read before delegating.** Step Xb runs in the
orchestrator's session, not in a delegated sub-agent. The `mcp__<server>__*`
tools are NOT inherited by spawned `agent_run` sub-agent sessions — only the
session that loaded the skill has them. This means the whole skill cannot be
wholesale-delegated to an engineer/pair sub-agent: the orchestrator role
must be played by the parent session that has <server> mounted (or the run
fails at dependency check). Steps Y and Z are still safely delegatable
because they only need RepoPrompt MCP, which sub-agents do inherit.
```

## Verification

To verify a sub-agent's MCP availability before relying on it:

1. Spawn a tiny test agent (`agent_run op=start model_id="explore"`) with a
   one-shot prompt: *"List the MCP servers visible in your session and
   echo the names back. Don't do anything else."*
2. `op=wait` for completion; read the output.
3. Compare against the parent's available MCPs. If any non-RepoPrompt MCP
   is missing, plan the orchestrator role accordingly.

You can do this once per machine/setup; the result is stable until you
change RepoPrompt config.

## Example

You wrote a skill that does GSC keyword analysis (uses `mcp__seo-utils__*`)
followed by repo research (uses `mcp__RepoPrompt__*`). You try to delegate
the whole thing to an engineer sub-agent:

```
mcp__RepoPrompt__agent_run op=start model_id="engineer"
  message="Run my-gsc-skill on entity X"
```

The sub-agent comes back with:

> seo-utils MCP is not connected in this session, so Step 1 (GSC probe)
> cannot run. I verified available MCP servers, and only RepoPrompt is
> present. Smoke test fails at dependency check.

Fix: keep the GSC probe in the parent session, dispatch only the repo
research:

```
# In parent (where seo-utils is mounted)
result_a = run_gsc_probe_inline()  # uses mcp__seo-utils__*

# Delegate the RepoPrompt-only part
agent_run op=start model_id="explore"
  message="Walk app/routes/services/X/ and write findings to <dossier>"
  detach=true
agent_run op=wait session_id=<id>

# Synthesise inline
write_brief(result_a, dossier_findings)
```

## Notes

- This is specific to RepoPrompt's `agent_run` calling Codex CLI. Other
  agent backends or harnesses may have different inheritance rules. If
  RepoPrompt later changes the inheritance model, this skill should be
  marked deprecated.
- Built-in Claude Code tools (`Read`, `Write`, `Bash`, `Edit`, `Glob`,
  `Grep`) are reliably available in sub-agents — when a skill is
  RepoPrompt+built-ins only, full delegation works fine. The hazard is
  exclusively about non-RepoPrompt MCPs.
- The `allowed-tools` frontmatter of a skill is a permissions allowlist
  for the SESSION that loaded the skill; it doesn't trigger MCP mounting
  in spawned sub-agents. Don't read it as a guarantee of availability.
- When in doubt about whether a step is delegatable, default to
  inline-with-callout. Over-delegating costs you a wasted agent run plus
  the time to diagnose; over-running-inline only costs context.
- Skills that already follow this pattern correctly (good references):
  `service-tier-brief-generator` v2.3+ Step 1b, `failure-brief-generator`
  v1.8+ Step 1b, `entity-demand-check` (entirely orchestrator-side, never
  delegates).

## See also

- `repoprompt-agent-run-sandbox-approval` — sibling gotcha about a
  different `agent_run` failure mode: subagents pausing on file-write
  approvals when asked to write outside loaded RepoPrompt roots.
- `skill-creator-aggregate-benchmark-layout` — sibling gotcha about the
  workspace layout `aggregate_benchmark.py` expects.
