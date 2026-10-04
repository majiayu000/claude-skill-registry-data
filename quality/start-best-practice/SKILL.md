---
name: start-best-practice
description: Use when responding to any user request — entry point into grimoire. Routes the input to the matching grimoire workflow (as listed in README.md), or exits silently if grimoire is not installed.
source: Toyota Production System poka-yoke (Shingo, 1986) — error prevention before the action, not after
tags: [proactive, interception, pre-action, best-practice-discovery, guardian, poka-yoke, quality-gate]
---

# Start Best Practice

Entry point into grimoire. Routes any user input to the matching grimoire workflow listed in README.md. Exits silently if grimoire is not installed or no workflow applies — invisible when not needed.

## Why This Is Best Practice

**Adopted by:** Toyota's poka-yoke principle (Shingo, 1986) is the foundation of error prevention in manufacturing — checking conditions *before* an action begins, not after defects appear. This principle is applied across aviation (pre-flight checklists), surgery (WHO Surgical Safety Checklist), and software (pre-commit hooks, CI gates).
**Impact:** The WHO Surgical Safety Checklist reduced surgical complications by 36% and deaths by 47% — not by changing technique, but by systematically intercepting the moment before each critical step (Haynes et al., 2009, NEJM). Pre-commit hooks catch an estimated 30–40% of common defects before they enter the codebase (GitHub internal data).
**Why best:** Reactive systems wait for the user to ask. Proactive interception closes the "I didn't know a best practice existed" gap — the most common reason practices aren't applied. The cost is minimal (a silent route check); the benefit is consistent practice application without requiring the user to know what to ask.

Sources: Shingo (1986) "Zero Quality Control: Source Inspection and the Poka-Yoke System"; Haynes et al. (2009) NEJM; GitHub Engineering blog

## Steps

### Step 0: Route to grimoire workflow (silent)

Silently match the input to a grimoire workflow. No scoring, no output. If no row matches, exit immediately and proceed with the original request unmodified.

| Intent signal | Route |
|---------------|-------|
| Describes a problem, goal, or situation without specifying an approach — including vague or unclear problems | invoke `suggest-best-practice` |
| Has a solution, plan, or design — wants gap analysis | invoke `review-best-practice-fit` |
| Needs 2+ practices coordinated in sequence — across one domain or many — and sub-problems are identifiable upfront | invoke `plan-best-practice-solution` |
| Complex problem where sub-problems are opaque and emerge through execution, not upfront | invoke `apply-best-practice-tree` |
| Mentions a domain or asks what skills/practices exist — without a specific problem to solve | invoke `discover-best-practices` |
| Wants to understand what a skill does, why it exists, or how to use it | invoke `explain-best-practice` |
| Wants to learn or teach a practice through structured explanation or walkthrough | invoke `teach-best-practice` |
| Wants to install, upgrade, or health-check grimoire | invoke `install-grimoire` |
| Wants to view, change, or validate grimoire settings or preferences | invoke `configure-grimoire` |
| Wants to activate a named paradigm or methodology (OOP, TDD, clean-architecture, etc.) | invoke `apply-best-practice-profile` |
| Wants to systematically align a project to stated practice preferences | invoke `apply-best-practice-driven-development` |
| Wants a compliance check of an artifact against pinned preferences | invoke `check-best-practice-compliance` |
| Has a specific finding from a compliance report to fix | invoke `fix-best-practice-finding` |
| Two practices exist — wants side-by-side comparison before deciding | invoke `compare-best-practices` |
| Two practices conflict — wants to reason through which fits better | invoke `resolve-best-practice-conflict` |
| Resolved a conflict — wants to save the decision for future sessions | invoke `pin-best-practice-preference` |
| **None of the above** | **exit silently** — grimoire not installed or not applicable |

Note: `analyze-best-practice-problem` has no direct routing row — vague or unclear problems are routed to `suggest-best-practice` (via "Describes a problem... including vague or unclear problems"), which internally invokes `analyze-best-practice-problem` via its clarity check. This keeps the routing table's problem-description row as the single entry point for all problem inputs.

**Transparent passthrough (exit silently — grimoire not applicable):**
- Primary verb is explanatory: *explain, describe, what is, how does, tell me about, define* — **exception:** "give me best practices for X" signals discovery, route to `discover-best-practices`
- Conversational acknowledgment: "ok", "thanks", "looks good", "got it", "continue"
- Explicit `/skill-name` invocations — user already knows what they want (see Rules)
- Follow-up message in an ongoing execution (not a new intent)
- User signals they know what they want: "just [verb]", "quickly [verb]", "I know how to…", "skip guidance", "no best practices"

**If ambiguous:** prefer the more specific workflow row. Only exit silently when no row matches.

**When a workflow matches:**
- Route to `suggest-best-practice` → invoke silently, no announcement
- Route to any other skill → announce first, then invoke:
  ```
  This looks like [matched situation]. Routing to [skill-name]...
  ```
Then stop — the routed skill handles everything from that point.

## Rules

- Never announce when no workflow matches — proceed silently
- No clarifying questions — route on what's available, or pass through silently
- If user explicitly invoked a skill by name, don't intercept — they already know what they want
- No scoring, no confidence thresholds — routing only

## Key Differences from `suggest-best-practice`

| | `suggest-best-practice` | `start-best-practice` |
|---|---|---|
| Invocation | User invokes directly | Runs automatically before every request |
| Unrelated inputs | N/A — user invokes directly | Exit silently (grimoire not installed) |
| Low confidence | Asks clarifying question | Exits silently |
| Scoring | Yes — scores all installed skills | No — routes only |
| Browse mode | Supported | Not supported |
| Dispatch role | No | Yes — entry point into grimoire |

## Common Mistakes

**Announcing a failed match**: if no row matches, say nothing and proceed. Interrupting the user for uncertain matches destroys trust.

**Intercepting explicit skill invocations**: if the user said `/write-unit-test`, they already know what they want. Don't re-intercept.

**Routing then not stopping**: after invoking a workflow skill, stop. The routed skill handles everything from that point.

**Treating task-starts as a special case**: "implement X", "write Y", "fix Z" all match "Describes a problem, goal, or situation" → route to `suggest-best-practice`. No separate domain scoring needed here.
