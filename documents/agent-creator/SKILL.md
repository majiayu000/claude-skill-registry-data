---
name: agent-creator
description: Author a safe project agent definition with valid frontmatter, bounded authority, skill-tool closure, and passing repository gates.
triggers:
  - create an agent
  - author a named agent
  - write an agent definition
  - add a subagent role
  - create an agents md file
  - configure a project agent
short-description: Author and validate a project agent
argument-hint: "Agent purpose, authority, skills, and boundaries"
user-invocable: true
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - write_file
  - search_replace
  - run_command
---

# Agent Creator

Create one named project agent under `.agents/agents/<name>.md`. This skill
follows `.agents/skills/skill-creator/SKILL.md` for its own authoring and
validation. Follow the security rules in `.agents/rules/10-security-privacy.md`.

## Procedure

1. Gather the requirements.

   Record the agent's purpose, users, task types, required authority, allowed
   skills, provider or model needs, output shape, and stop conditions. Set the
   smallest useful tool set. Decide if the agent is a read-only reviewer, a
   writer, or an implementation agent. Do not create an agent with authority
   that its task does not need.

2. Read the contracts.

   Read `.agents/agents/README.md` for the file shape and role conventions.
   Read `internal/config/agents_parse.go` for the runtime parser and validation
   rules. Read `scripts/check_agents.py` for the repository gate. Read
   `docs/product/agent.md` and
   `docs/architecture/skills.md` for loading, trust, tool, and skill-binding
   rules. Cite these canonical files in the agent body when a detail needs
   explanation. Do not copy their full contents into the prompt.

3. Choose the identity and file.

   Use a lowercase name that matches the filename exactly:
   `.agents/agents/<name>.md`. The runtime accepts the Markdown file in this
   workspace directory. Do not create `.mivia/agents/`, `.claude/agents/`, or a
   second copy of the definition.

   Check `ALLOWED_ROLES` in `scripts/check_agents.py`. Use an existing allowed
   role when it fits. If this is a new role, add its name to that explicit
   allowlist in the same change and run its gate tests. Do not silently weaken
   or remove the allowlist check.

4. Design the frontmatter.

   Use only keys accepted by `internal/config/agents_parse.go`. Set `name` and
   `description`. Declare `tools` as a full list, or use `inherits` with
   `tools_add` and `tools_remove`; do not combine a full list with either
   delta. Use `disallowed_tools` for a deny boundary. Use `tools_core` only
   when deferred schemas are needed. Use `skills` only for the skill names the
   agent must invoke.

   Keep the effective tool set small and explicit. For each listed skill,
   confirm the skill directory exists under `.agents/skills/`, then confirm
   every tool in that skill's frontmatter `tools:` list is in the agent's
   effective tools. `make verify-agent` checks both conditions. A skill list
   does not grant tools.

   Do not add `timeout_seconds` or `max_tokens` ceilings to a project agent.
   Keep `max_turns = 0` when the role needs unlimited turns. This is the repo
   decision recorded in `.agents/memories/no-per-agent-spend-ceilings.md`.
   Add a ceiling only when the operator gives a direct, current requirement
   that changes this decision.

5. Write the agent body.

   State the role, work boundary, input assumptions, required checks, output
   format, and failure behavior. Use ASD-STE100: short sentences, direct
   verbs, and known words. Keep the prompt project-specific only where that
   knowledge is required. Never include credentials, secrets, raw prompts,
   provider keys, absolute home paths, or instructions to bypass hooks.

   Include a `Disallowed operations` section for every ADLC role. State what
   the agent must not write, run, publish, commit, or push. A read-only role
   must say that it does not edit files. A writer role must state its file
   boundary. The body must not grant authority that is absent from frontmatter.

6. Validate the definition.

   Read the new file back. Check that the name matches the filename, every
   frontmatter key is supported, the tool list is valid, the skills resolve,
   and the effective tools cover each skill's declared tools. Check the body
   for the required boundary and `Disallowed operations` section when the role
   is an ADLC role.

   Run the actual gates:

   ```text
   make agents-check
   python3 scripts/verify_agent_config.py
   make verify-agent
   go test ./internal/agents -count=1
   ```

   If the role roster or compatibility fixtures name the committed roles,
   update those fixtures in the same change. Run `make verify` before delivery
   when the full repository audit is in scope. Fix every failure before you
   call the agent done. Do not claim a check passed unless it ran and returned
   success.

## Tool surface

`read_file`, `list_dir`, `grep`, `glob`, `find_references`, `write_file`,
`search_replace`, `run_command`.

This list is the frontmatter `tools:` list, and the two must stay equal.

## What this skill never does

- It never creates `.mivia/agents/` or `.claude/agents/`.
- It never writes credentials, secrets, raw prompts, or PII.
- It never bypasses Git hooks or protected-path policy.
- It never commits or pushes.
