---
name: intent-engine
description: >
  Activate when working on feature specs, complex multi-file tasks, agent
  workflows, or any task where goal clarity, conflict resolution, or
  verification criteria are needed. Translates human goals into structured,
  machine-actionable intent specs that Claude Code can execute, verify, and
  audit. Use before starting any task estimated to touch more than 3 files
  or requiring cross-functional decisions.
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

### Frontmatter

```yaml
---
intent: <short-slug>
version: "1.0"
priority: critical | high | medium | low
domain: <domain-name>
---
```

### Minimal Spec

```markdown
---
intent: fix-checkout
version: "1.0"
priority: high
---
# IntentSpec: Fix Checkout Bug
**Objective:** [1 sentence, evidence-grounded]
**Success:** [1 verifiable outcome]
**Constraint:** [1 must-not-break]
**Verify:** `[command]`
```

### Full Spec

```markdown
---
intent: <slug>
version: "1.0"
priority: critical | high | medium | low
domain: <domain>
---

## IntentSpec: <Title>

### Objective
<!-- What user problem are you solving? Ground it in evidence. -->
[Support ticket / metric / user quote that motivated this]

### User Goal
As a [user type], I need to [accomplish X] so that [outcome Y].

### Outcomes (Verifiable)
- [ ] Metric A moves from X to Y (measured via [method])
- [ ] Feature B behaves like [specific behavior] in [specific scenario]
- [ ] Error rate for C drops below D% for 7 consecutive days

### Constraints
- Must maintain backward compatibility with [API version / data schema]
- Must not increase p95 latency above [threshold]
- Must pass existing test suite without modifications to tests

### Edge Cases
- When [condition]: [expected behavior]
- When [condition]: [escalate to human / fail gracefully]

### Conflict Resolution
If speed vs. accuracy conflict: accuracy wins. Flag trade-off in PR description.

### Verification
- Automated: `[command that proves success]`
- Manual: [QA checklist or review step]
- Metric: [Observable measurement over time]
```

See also: `resources/templates/full-spec.md` and `resources/templates/minimal-spec.md`

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

Teams should add this to their CLAUDE.md:

```markdown
## Intent Architecture

### Goal Hierarchy (enforced, highest priority first)
1. [Your top priority]
2. [Second priority]
3. [Third priority]

### Decision Rules
- If [condition] vs [condition]: [which wins]. [What to do].
- If scope creep detected: complete stated task, add TODO for expansion.
- If ambiguous requirements: ask one clarifying question before proceeding.

### Hard Guardrails (never do these)
- [Forbidden action 1]
- [Forbidden action 2]

### Escalation Triggers (stop and ask before)
- [Trigger 1]
- [Trigger 2]
```

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

Before planning, infer and/or elicit what the user is optimizing for **right now**.

Populate `intent.personal_intent` with:
- modes: choose 1-2 from: ship, learn, explore, refactor, stabilize, mentor, document, de-risk
- values: 2-5 short phrases (e.g., simplicity, correctness, calm, speed)
- tradeoffs: at least 1 axis (e.g., speed vs correctness) + preference
- anti_goals: 1-3 explicit "do not do" items
- definition_of_done: 3-6 bullets
- energy_budget: low/medium/high
- time_horizon: today/this_week/this_month/long_term
- confidence: 0..1

Rules:
- If confidence < 0.6, set `verification.decision=clarify` and ask **1-3** concise questions BEFORE executing domain actions.
- Never therapize. Keep it practical and engineering-relevant.

Question bank (use sparingly, max 3):
- "Are we optimizing for shipping fast, learning deeply, or reducing risk?"
- "What would make this a win today?"
- "What do you explicitly *not* want (rewrites, yak-shaving, brittle magic)?"
- "Time/energy budget: quick patch, solid fix, or deep refactor?"

Reference: `resources/personal-intent.md`.

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

This creates an auditable record of what intents were active, what decisions
were made, and whether the goal hierarchy was respected.

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

Version history is tracked in the intent spec frontmatter and the audit log.
When updating an intent, bump the version and note what changed:

```yaml
---
intent: checkout-fix
version: "1.1.0"
priority: high
changelog:
  - "1.1.0: Added 3DS authentication edge case"
  - "1.0.0: Initial spec"
---
```

---

## Domain Plugins

Domain plugins live under `resources/plugins/`.

- ports: `resources/plugins/ports.plugin.md`
- ehs: `resources/plugins/ehs.plugin.md`

Plugins define:
- default constraints
- planning templates (step sequences)
- validator checklists
- clarification/escalation triggers
- personal-intent mapping (how mode changes the plan)
- **domain-specific goal hierarchy overrides**
- **domain-specific verification commands**

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

### EH&S Safety Task
```markdown
---
intent: osha-300-export-fix
version: "1.0.0"
priority: critical
domain: ehs
---
# IntentSpec: OSHA 300 Log Export Fix

**Objective:** Compliance officers can't export OSHA 300 logs for Q1 2026
(bug report #247, affects annual regulatory submission due March 31).

**User Goal:** As a safety manager, I need to export a correctly formatted
OSHA 300 log so I can submit it to OSHA on time.

**Outcomes:**
- [ ] Export generates valid CSV matching OSHA 300 column spec
- [ ] All 47 incident records from Q1 appear in output
- [ ] Export completes in < 5 seconds for 500 records

**Constraints:** Must not alter existing incident records; audit log required.

**Escalation:** Stop if regulatory field mapping is ambiguous.

**Verification:** `pytest tests/exports/test_osha300.py -v`
```

### Software Feature Task
```markdown
---
intent: dashboard-perf
version: "1.0.0"
priority: high
domain: general
---
# IntentSpec: User Dashboard Performance

**Objective:** Dashboard p95 load > 4s (observed in Datadog, 3 user complaints).

**User Goal:** As an operator, I need the dashboard to load quickly so I
can monitor facility status without delays.

**Outcomes:**
- [ ] p95 load time < 1.5s (measured via Lighthouse CI)
- [ ] No regression in data accuracy (all existing tests pass)
- [ ] Mobile layout unchanged (visual regression test passes)

**Constraints:** No changes to data model; no new external API calls.

**Conflict Resolution:** If caching vs. accuracy conflict -> accuracy wins.

**Verification:** `npm run test && npm run lighthouse`
```

See also: `resources/intent-examples.md`
