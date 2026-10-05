---
name: intent-engine
description: >
  Activate when working on feature specs, project planning, task breakdowns,
  requirements analysis, specifications, PRDs, user stories, acceptance criteria,
  complex multi-file tasks, agent workflows, or any task where goal clarity,
  conflict resolution, or verification criteria are needed. Also activate when
  the user asks to "plan", "spec out", "break down", "scope", "define requirements",
  "write a PRD", or "clarify what we're building". Translates human goals into
  structured, machine-actionable intent specs that Claude Code can execute, verify,
  and audit. Use before starting any task estimated to touch more than 3 files or
  requiring cross-functional decisions.
---

# Intent Engine

## Overview

The Intent Engine bridges the gap between vague human goals and precise,
executable agent behavior. It sits at the top of the three-layer stack:

- **Prompt**: What to do right now
- **Context**: What you know and can access
- **Intent**: What you should optimize for over time (this skill)

It provides:

1. **Intent Spec templates** -- structured task definitions with verification
2. **Goal hierarchy enforcement** -- explicit priority ordering for conflict resolution
3. **Escalation logic** -- when to pause and ask vs. proceed
4. **Personal intent awareness** -- align plans with what the user is optimizing for
5. **Session reinforcement** -- intent context that survives compaction
6. **Intent versioning** -- track how intents evolve over time

---

## IntentSpec Format

Every significant task should have an IntentSpec. Store in `.intents/<slug>.md`.

Use the appropriate template based on task complexity:

- **Simple tasks (1-3 files):** Use `resources/templates/minimal-spec.md` -- four fields: Objective, Success, Constraint, Verify.
- **Complex tasks (4+ files, cross-cutting):** Use `resources/templates/full-spec.md` -- includes goal hierarchy, edge cases, escalation triggers, and verification matrix.

Both templates use YAML frontmatter with `intent`, `version`, `priority`, and optional `domain` fields.

---

## Goal Hierarchy

Every project should define an explicit goal hierarchy. When goals conflict,
higher-priority goals always win. Without this, agents default to the
easiest-to-measure metric.

### Default Hierarchy (override in CLAUDE.md)

1. **Safety & compliance** -- never generate code that bypasses auth, skips validation, or removes error handling
2. **Data integrity** -- all changes have audit trails; never silently drop data
3. **Correctness** -- passing tests > passing linting > code elegance
4. **Performance** -- optimize only after correctness is verified
5. **Developer experience** -- readable code preferred over clever one-liners

### Conflict Resolution Defaults

- **Safety vs. Speed**: Safety wins. Always.
- **Completeness vs. Scope**: Complete stated task, propose expansion separately.
- **Clarity vs. Cleverness**: Clarity wins.
- **Accuracy vs. Throughput**: Accuracy wins. Log the trade-off.

### Goal Hierarchy Template

Teams should add this to their CLAUDE.md. See `resources/templates/goal-hierarchy.md` for
the full template including decision rules, hard guardrails, and escalation triggers.

---

## Escalation Logic

### When to Escalate (Stop and Ask)

The agent MUST pause and request human input when:

- Detected conflict between task scope and active intent
- Task touches security, authentication, or authorization logic
- Task touches compliance or regulatory logic
- File change count exceeds estimate by 3x or more
- Ambiguous regulatory or safety requirement
- Destructive operation (delete, overwrite, schema migration)
- Risk tier is high/critical and verification cannot be automated
- Personal intent confidence < 0.6 (unclear what user is optimizing for)

### Escalation Format

When escalating, provide:
```
ESCALATION: [reason]
Active Intent: [slug] (priority: [level])
Conflict: [what conflicts with what]
Options: [A] [B] [C]
Recommendation: [which option and why]
```

---

## Process

### Step 1 -- Compile Domain Intent

Extract and normalize:
- objective (single sentence, canonical)
- domain (e.g., ports, ehs, general)
- inputs (domain-specific)
- constraints (hard vs soft, with rationale)
- success criteria (verifiable)
- risk tier (low/medium/high/critical)
- ambiguity_policy and contradiction_policy
- output_format + evidence requirements
- **version** (semver string)
- **goal_hierarchy** (ordered list of priorities)
- **escalation_triggers** (conditions that require human input)
- **verification_commands** (runnable checks)

Then output `intent.json`.

### Step 1.5 -- Clarify Personal Intent

Before planning, infer what the user is optimizing for **right now**.

Populate `intent.personal_intent` with: modes, values, tradeoffs, anti_goals,
definition_of_done, energy_budget, time_horizon, and confidence.
See `resources/personal-intent.md` for the full field reference and examples.

Rules:
- If confidence < 0.6, ask **1-3** concise questions before proceeding.
- Never therapize. Keep it practical and engineering-relevant.

Question bank (use sparingly, max 3):
- "Are we optimizing for shipping fast, learning deeply, or reducing risk?"
- "What would make this a win today?"
- "What do you explicitly *not* want (rewrites, yak-shaving, brittle magic)?"
- "Time/energy budget: quick patch, solid fix, or deep refactor?"

### Step 2 -- Plan

Create a plan that is:
- Deterministic when possible (parsing, scanning, linting, tests)
- Tool-driven (retrieve, analyze, generate, validate, format)
- Verifiable (each step emits evidence)
- Aligned with goal hierarchy (higher-priority goals checked first)

Plans MUST use the tool keys defined in `resources/plugin-interface.md` and/or domain plugin specs.

Then output `plan.json`.

### Step 3 -- Verify

Verification must check:
- hard constraints satisfied
- evidence present if required
- output format correctness
- contradiction handling respected
- risk-tier gates applied
- **goal hierarchy compliance** (no lower-priority goal overrode a higher one)
- **personal intent alignment** (plan matches the user's mode)
- **verification commands pass** (run each command, report results)

Decision:
- accept: all hard constraints satisfied, success met, no unresolved contradictions
- revise: can fix automatically without new info
- clarify: missing info or contradictions require user input
- escalate: high/critical risk requires human review or ambiguity is too dangerous
- refuse: disallowed or unsafe request

Then output `verification.json`.

### Step 4 -- Audit Trail

Log every intent decision to `.intents/audit.log`:

```
[timestamp] intent=<slug> version=<ver> priority=<level> decision=<accept|revise|clarify|escalate|refuse> score=<0-1> goal_hierarchy_respected=<true|false> escalations=<count>
```

---

## Context Compaction Survival

During long sessions, context compaction may discard information. The following
MUST survive compaction and be restored if lost:

1. **Active intent slug and priority level**
2. **Goal hierarchy** (the ordered list of priorities)
3. **Hard guardrails** (what is forbidden)
4. **Escalation triggers** currently active
5. **Verification criteria** for in-progress tasks
6. **Personal intent mode** (ship/learn/stabilize/etc.)

### Compaction-Resistant Summary Format

After establishing intent, emit this summary block that can be quickly
restored if context is compacted:

```
--- INTENT ANCHOR (survive compaction) ---
ACTIVE INTENT: <title> (v<version>, priority: <level>)
GOAL HIERARCHY: 1.<top> 2.<second> 3.<third>
MODE: <personal intent mode>
GUARDRAILS: <comma-separated forbidden actions>
ESCALATE IF: <comma-separated triggers>
VERIFY: <verification command>
--- END INTENT ANCHOR ---
```

If context was compacted, begin recovery with:
```
Restore intent context: what is the active intent spec and priority level?
```

---

## Intent Versioning

Intents evolve as projects evolve. Use semantic versioning:

- **Patch** (1.0.1): Clarified wording, no behavioral change
- **Minor** (1.1.0): Added new constraint or edge case
- **Major** (2.0.0): Changed objective, goal hierarchy, or success criteria

Track changes in the intent spec frontmatter:

```yaml
changelog:
  - "1.1.0: Added 3DS authentication edge case"
  - "1.0.0: Initial spec"
```

---

## Domain Plugins

Domain plugins live under `resources/plugins/`.

- ports: `resources/plugins/ports.plugin.md`
- ehs: `resources/plugins/ehs.plugin.md`

Plugins define: default constraints, planning templates, validator checklists,
clarification/escalation triggers, personal-intent mapping, domain-specific
goal hierarchy overrides, and domain-specific verification commands.

---

## Output Contract

Return four things:

1. `intent.json` -- the structured intent object (with goal_hierarchy, escalation_triggers, version)
2. `plan.json` -- ordered steps with dependencies
3. `verification.json` -- checks + decision + required clarifications (if any)
4. A brief human-readable summary including the compaction-resistant anchor

All JSON must conform to `resources/intent.schema.json`.

---

## Examples

See `resources/intent-examples.md` for complete worked examples covering:
- Low-risk tasks (ports domain, ship mode)
- High-risk tasks (EH&S domain, de-risk mode)
- Same request with different personal intents (ship vs. stabilize)
