---
name: "chain"
description: "Build deep exploit chains \u2014 dispatches chain-builder agent. Given bug A, recursively walks the chain graph. Usage: /chain (then describe bug A)"
---

# Chain

*Sourced from h-mmer-pentest-agents*

Build exploit chain from: $ARGUMENTS

## Process

1. Read brain for current target context:
   `uv run python3 ../../tools/brain.py brief <target>`

2. Get bug A description:
   - If `$ARGUMENTS` contains a bug description → use it
   - Else if brain has a recent confirmed finding → use that
   - Else → ask user to describe the confirmed bug

3. Read `rules/chain-table.md` — the capability→next-bug table

4. Read `policy.md` — extract policy preamble for the agent

5. **ALWAYS dispatch `chain-builder` agent** (model: inherit) with:
   - The confirmed bug A description (exact HTTP request/response)
   - The full chain table from `rules/chain-table.md`
   - Policy preamble (scope + required headers + restrictions)
   - Brain context (tech stack, tested endpoints, known capabilities)
   - Writeup intelligence: call `search_writeups "chain <bug class> escalation"` if MCP available

6. After agent returns:
   - If chain found:
     - `uv run python3 ../../tools/brain.py record <target> confirmed "chain: <summary>" "<full chain>"`
     - Show chain to user with combined impact and CVSS
     - Suggest: `/validate` then `/report`
   - If dead end:
     - `uv run python3 ../../tools/brain.py record <target> exhausted "chain from <bug A>" "<candidates tried>"`
     - Show what was tried and why it failed

No inline chain logic. No capability table. The chain-builder agent does all the work.

## Top-Tier Chain Standard

A chain is valuable only when each link grants a concrete capability.

Before dispatching, classify bug A as one capability:
- identity control: login, link, session, token, role, invite
- data read: PII, secrets, tenant data, internal API response
- data write: config, webhook, template, profile, billing, integration
- execution: script, server-side call, command, workflow run, model/tool action
- network pivot: SSRF, callback, metadata, internal host reachability

Ask the chain-builder for three paths: fastest proof, highest impact, and safest policy-compliant path. Kill chains that require guessing, prohibited data access, or unbounded scanning. A reportable chain must include end-to-end reproduction, where link 2 consumes the capability from link 1 rather than merely coexisting with it.

