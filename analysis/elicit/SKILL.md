---
name: mk:elicit
version: 1.0.0
preamble-tier: 3
description: Structured second-pass reasoning after code review or plan evaluation. Offers named reasoning methods (pre-mortem, inversion, red team, Socratic, etc.) to re-examine findings through a specific lens. Use after /mk:review verdict or any time deeper analysis is needed on an existing output. NOT for initial review (see mk:review); NOT for creating implementation plans (see mk:plan-creator).
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
source: new
keywords:
  - elicit
  - second-pass-reasoning
  - pre-mortem
  - red-team-analysis
  - socratic
  - inversion
when_to_use: Use after a code review or plan evaluation — re-examines findings via named reasoning methods. NOT for initial review (see mk:review) or creating plans (see mk:plan-creator).
user-invocable: true
owner: research
criticality: medium
status: active
runtime: claude-code
---

# Elicitation — Structured Second-Pass Reasoning

Re-examine an existing output (review verdict, plan, analysis) through a named reasoning method.
Surfaces insights that generic "make it better" requests miss.

## When to Use

- After `/mk:review` verdict — deepen analysis before Gate 2
- After plan creation — stress-test assumptions before Gate 1
- After any agent output — when user wants a specific angle of analysis
- When user says "dig deeper", "what am I missing", "challenge this"

**NOT this skill if:** you have no existing artifact to re-examine — use `mk:brainstorming` for open exploration, or `mk:problem-solving` for approach-stuck situations.

## Reasoning Methods

| Method                  | Lens                                            | Best For                                      |
| ----------------------- | ----------------------------------------------- | --------------------------------------------- |
| **Pre-mortem**          | "Assume this shipped and failed. Why?"          | Risk discovery, failure mode analysis         |
| **Inversion**           | "What would make this maximally wrong?"         | Assumption testing, edge cases                |
| **Red Team**            | "You are an attacker. How do you exploit this?" | Security analysis, adversarial thinking       |
| **Socratic**            | "What evidence supports each claim?"            | Logic validation, gap detection               |
| **First Principles**    | "Strip assumptions. What's fundamentally true?" | Architecture decisions, design simplification |
| **Constraint Removal**  | "What if [constraint X] didn't exist?"          | Innovation, scope exploration                 |
| **Stakeholder Mapping** | "Who else is affected? What do they need?"      | Impact analysis, requirements gaps            |
| **Analogical**          | "What similar system solved this differently?"  | Alternative approaches, pattern matching      |

## Workflow

1. **Load context** — Read the output being re-examined (verdict file, plan file, or conversation context)
2. **Present methods** — Show the table above; ask user to pick one (or suggest based on context)
3. **Apply method** — Re-examine the output through the chosen lens
4. **Produce analysis** — Structured output with:
   - Method applied
   - Key findings (numbered, actionable)
   - Severity: CRITICAL / IMPORTANT / INFORMATIONAL
   - Recommendations (what to change, if anything)
5. **Optional repeat** — User may pick another method for multi-lens analysis

## Auto-Suggestion Logic

When invoked without a method choice, suggest based on context:

| Context                                | Suggested Method    |
| -------------------------------------- | ------------------- |
| Review found security issues           | Red Team            |
| Review found low coverage              | Pre-mortem          |
| Plan has many assumptions              | First Principles    |
| Architecture decision                  | Inversion           |
| Complex feature with many stakeholders | Stakeholder Mapping |
| Default / unclear                      | Socratic            |

## Output Format

```markdown
## Elicitation: [Method Name]

**Target:** [what was re-examined]
**Method:** [brief description of the lens applied]

### Findings

1. **[CRITICAL]** [finding] — [recommendation]
2. **[IMPORTANT]** [finding] — [recommendation]
3. **[INFORMATIONAL]** [finding] — [observation]

### Summary

[1-2 sentence synthesis of what this method revealed]

### Action Required

- [ ] [specific action items, if any]
```

## Integration with mk:review

After the review verdict (step-04), the reviewer MAY offer elicitation:

```
Review complete. Verdict: WARN (2 warnings).

Would you like to run elicitation on this verdict?
Pick a method: pre-mortem | inversion | red-team | socratic | first-principles | skip
```

Elicitation output appends to the verdict file as a supplementary section.
It does NOT change the verdict (PASS/WARN/FAIL) — it adds depth.

## Gotchas

- **Reasoning methods are not commutative — order changes the output** — running Red Team then Socratic surfaces attack vectors first and then validates them with evidence, producing a security-focused analysis; reversing to Socratic then Red Team validates assumptions before probing attacks, and often kills the adversarial framing entirely; always apply methods in the order that matches the user's primary concern.
- **Socratic method loops indefinitely without a termination criterion** — "What evidence supports this claim?" applied recursively has no natural stopping point; without an explicit depth limit (e.g., stop at 3 levels of questioning or when no new claims emerge), the agent keeps decomposing until the context window fills; set a max depth before starting Socratic elicitation.
- **Inversion only works reliably on binary decisions, not multi-option trade-offs** — "What would make this maximally wrong?" applied to a 3-option architectural choice produces a vague worst-case mix; inversion is sharp when the decision is yes/no (ship vs don't ship, add vs remove); for multi-option decisions, use Constraint Removal or Stakeholder Mapping instead.
- **Pre-mortem degenerates to a generic worry list without a concrete ship date and scope** — "Assume this shipped and failed" requires a specific artifact (the plan, the feature, the migration) to be meaningful; if the target is vague ("our auth system"), the pre-mortem produces abstract risks ("scalability", "security") that don't map to actionable mitigations; always attach pre-mortem to a specific, scoped output.
- **Elicitation output appended to the verdict file does NOT change the gate decision** — users sometimes interpret a CRITICAL finding from Red Team elicitation as requiring a Gate 2 re-evaluation; the skill explicitly does not change verdicts; if the elicitation reveals a CRITICAL issue, the user must manually trigger a new `mk:review` pass to produce a revised verdict before proceeding to Phase 5.

## What This Skill Does NOT Do

- Does NOT replace the review — it supplements it
- Does NOT change verdicts or gate decisions
- Does NOT generate code — analysis only
- Does NOT run automatically — always user-triggered
