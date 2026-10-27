---
name: copilot-context-engineering
description: "**DISCIPLINE SKILL** — refine a repo's `.github` customization files (agents, skills, instructions, prompts, constitution) after a merge: each lesson single-sourced in one owner file, inherited by reference, never duplicated. USE FOR: codify lessons, add a rule to customization files, pick a rule's owner, remove duplication or drift. DO NOT USE FOR: creating new files, publishing, code edits, hook/MCP config. FOR SINGLE OPERATIONS: none."
metadata:
   version: 0.3.0
---

# Context Engineering

Refine the host repo's **agent context file set** — `.github/agents`, `.github/skills`, `.github/instructions`, `.github/prompts`, and the root constitution (`.github/copilot-instructions.md` or `AGENTS.md`) — so each lesson learned is codified once in exactly one authoritative owner and inherited everywhere else **by reference**. Duplicated prose silently diverges as files get edited independently; one owner means one source of truth and one place to update.

**Scope**: the prose-bearing customization primitives only (constitution, instructions, skills, agents, prompts). Executable/config primitives — hooks, MCP servers, tool sets, plugins — belong to other workflows; full docs-grounded inventory: [references/primitives.md](references/primitives.md).

## Standard Layout

```text
.github/
├── copilot-instructions.md        # Root constitution: universal rules + authority model
├── agents/*.agent.md              # Agent behavior
├── skills/*/SKILL.md              # Task playbooks
├── instructions/*.instructions.md # Scoped policy (applyTo patterns)
└── prompts/*.prompt.md            # User shortcuts (deprecated for Agent Host; prefer skills)
```

Before refining: **read the root constitution first** — it carries the universal rules, the authority model, and protected areas; scoped owners elaborate it but never contradict it, and when no scoped file exists the constitution is itself a valid owner. Then confirm this layout exists (or the host's documented variant — `.claude/`, `.agents/`); adopt the host's documented authority model if present — it supersedes the default table below; never invent top-level conventions for a repo already on the `.github` standard; touch only customization files, never protected areas (generated artifacts, persisted state, shared framework code).

## Owner-Assignment Decision Table

Choose the **single most-specific owning file** per the host repo's authority model (if documented), otherwise per this default table:

| Concern kind | Default owner | Example |
|---|---|---|
| Repo-wide policy (operations, conventions, architecture, auth) | Scoped `.github/instructions/*.instructions.md` (or a section in the root constitution if no scoped files exist) | API conventions, tenant URL resolution |
| An agent's own execution/orchestration behavior | The agent's `.github/agents/*.agent.md` file | A QA smoke rule belongs in the QA agent file |
| A task playbook driven only by one skill | That skill's `.github/skills/<name>/SKILL.md` | A workflow only that skill drives |
| A user-invoked workflow shortcut | `.github/prompts/<name>.prompt.md` — but prompt files are deprecated for Agent Host sessions; prefer a skill when the workflow should auto-trigger or survive that migration | a `/changelog` prompt |

If a rule is both policy and an agent's execution rule, prefer the instruction file for the policy itself and let the agent reference it.

## Write Once, Inherit by Reference

1. **Write the lesson once** in its owner file (per the decision table above).
2. **Never restate the prose** in consumer files — add a one-line pointer naming the owner and, where helpful, the section: `→ see <file> ("Section")`.
3. **Use the platform's inheritance mechanisms:**
   - **Instructions**: `applyTo` attachment already covers matching files automatically; add a pointer only for consumers outside the pattern.
   - **Agents**: reference the owner from the agent body with a Markdown link or the `#file:<relative-path>` syntax (both documented ways for an agent to reuse an instructions file). Never paste the policy prose inline.
   - **Skills**: add a one-line related-files pointer in the `SKILL.md` body naming the owner's path; the reader loads the owner on demand. Never paste the policy prose inline.
   - **Root constitution**: stays a thin map — universal rules and pointers live there, not detailed lesson prose.
4. **Leave pre-existing divergent copies untouched** — do not edit them to sync; point consumers to the new owner.

## How To Workflow

1. **Name the lesson** in one sentence.
2. **Scan for an existing owner first**: `grep -ri "<key-phrase>" .github/copilot-instructions.md .github/agents .github/skills .github/instructions .github/prompts`
   - Already exists → point consumers at its owner; several divergent copies → keep the most authoritative, leave the copies untouched.
   - No owner → create it per the decision table.
3. **Write the lesson once** into the owner, in its natural section.
4. **Add thin pointers** in every consumer that must know the rule, using the inheritance mechanisms above.
5. **Verify no duplicate prose remains**: `grep -rl "<full-lesson-phrase>" <the same locations>` matches exactly one file — the owner. Pointers everywhere are fine; full prose only in the owner.

## Example

Worked example — four post-debug lessons, one owner each, pointers only in the orchestrator — plus guidance on what counts as a lesson: [references/example.md](references/example.md).

## Authoritative Sources

Platform conventions for these file types evolve — paths get renamed and mechanisms get deprecated. Before relying on a layout or mechanism claim, check the claim-to-source table in [references/sources.md](references/sources.md), verified against GitHub and VS Code docs on 2026-10-11. If a source URL 404s, search `docs.github.com` or `code.visualstudio.com` for the page title; the docs restructure frequently. Where a source conflicts with this skill, the source wins.

## Guardrails

- **Never duplicate.** One concern, one owner, one copy of the prose.
- **Never edit multiple owners** for a single concern.
- **Constitution wins.** Scoped owners refine the root constitution; they never contradict it — a lesson that changes a universal rule belongs in the constitution itself.
- **Keep pointers thin.** A pointer that grows into prose is drift in disguise — if a pointer needs a full paragraph, the rule belongs in the owner, not the pointer.
- **Respect protected areas.** Only modify agent customization files; never hand-edit persisted state, generated artifacts, or memory/knowledge-graph stores the repo governs through dedicated processes.
- **Do not edit third-party/upstream skill files** you don't own. Create clearly-suffixed forks if a customization requires deviation.
