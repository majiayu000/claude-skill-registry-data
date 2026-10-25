---
name: author-skills
description: Internal repository rules for authoring, modifying, and pruning skills and subagents within the amiga-ia suite.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: Author Skills (Internal Repository Guide)

This skill governs the standards for creating, revising, and maintaining skills and subagents within the `amiga-ia` repository.

## When a Skill or Agent Earns Its Place

1. **The Rule of Two Manual Frictions (Skills):**
   A skill earns its place only after the same task has been performed manually twice and caused friction (non-obvious sequences, rediscovered edge cases, or near-miss defects).
   Never create skills speculatively or "to complete a set".
2. **Unification over Proliferation (Skills):**
   If two proposed skills share most of their procedural logic, create a single skill with clearly structured modes or branches rather than fragmenting the catalog.
3. **When an Agent Earns Its Place (2026 Context Isolation & Tool Boundary Gate):**
   Subagents introduce latency, token multiplication, and multi-hop serialization overhead. An `agents/*.md` definition is justified ONLY when at least one of the following architectural conditions holds:
   - **Strict Information Barrier / Zero-Contamination Context:** The subagent must be blind to the parent conversation's implementation bias or prior reasoning (e.g., Double-Blind Cleanroom `ami-cleanroom-builder` / `ami-cleanroom-tester`, or fresh-context `ami-adversarial-verifier`).
   - **High-Volume Context Window Protection (Fan-Out):** The subagent absorbs verbose intermediate outputs (large repo scans, multi-module audits, dataset profiling) and returns only a distilled summary to protect the primary conversation's attention budget.
   - **Distinct Permission Sandbox:** The subagent enforces a stricter tool boundary than the parent (e.g., `sandbox_mode = "read-only"` auditors or evaluators).
   Never create subagents merely for "thinking before thinking", multi-round roleplay chatter, or tasks that a single-pass skill in the main thread can execute directly.

## Architectural Boundaries

1. **Procedural Instruction vs. Evidence:**
   - `SKILL.md` must be strictly procedural and concise (under 250 lines).
   - Long case studies, benchmark data, and historical incidents belong in `references/<topic>.md`, which loads on demand rather than bloating the system prompt.
2. **Zero Agent-Skill Procedural Duplication (DRY Gate):**
   - Procedural workflows belong in `skills/<name>/SKILL.md`, while agent profiles (`agents/<role>.md`) define the role identity, invariants, permission boundaries, and dispatch triggers.
   - Never copy-paste a skill's step-by-step phases into an agent file; instruct the agent to read and follow `skills/<name>/SKILL.md`.
3. **Token Efficiency & Description Budget:**
   - The YAML frontmatter `description` is loaded into the system prompt on every turn.
   - Keep `description` under 50 words using a functional, declarative summary: what the skill does and exact triggers.
   - Never place change logs, version numbers, or verbose narrative in the frontmatter.
4. **Never Hardcode Queryable Facts:**
   - Do not hardcode git statuses, PR numbers, version tags, or tool availability. Query them live via terminal tools.

## Standardized Workflow Patterns

1. **Numbered Confirmation Gates:**
   - Any skill that triggers an irreversible effect (modifying files, running git commands, compiling releases) must include an explicit in-line numbered stop point:
     `CONFIRMATION N - <Action>: STOP and present <data> to the user. Await explicit approval.`
2. **Anti-Duplication Gate as Step 0:**
   - For skills that perform external searches, benchmarking, or context gathering, Step 0 must verify whether the answer already exists locally (in `docs/`, `references/`, or repository caches).
3. **No Emojis in Prompts & Instructions:**
   - Adhere strictly to Rule 18: Skill instructions (`SKILL.md`) and subagent prompts (`agents/*.md`) must not contain emojis or pictographs. Use Markdown headings, bullet points, and severity tags (`[Blocker]`, `[Warning]`).
4. **Naming Conventions:**
   - Skills are named as actions/verbs: `ami-<verb>-<object>` (e.g., `ami-plan-feature`).
   - Agents are named as roles/nouns: `ami-<role>` (e.g., `ami-tech-lead`).
   - All public suite components must carry the `ami-` prefix.

## Verification Gate

After authoring or modifying any skill, agent, or hook in this repository, execute the diagnostic suites:

```bash
node bin/setup.js --doctor
npm test
```

All checks must pass with zero errors before declaring work complete.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
