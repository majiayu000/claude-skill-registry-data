---
name: why-driven-decision
description: FOUNDATIONAL SKILL - Analyze every prompt for underlying motivation using Golden Circle (WHY->HOW->WHAT). Runs BEFORE any other skill. No action without understanding WHY.
---

# WHY-Driven Decision Making

## Foundational Layer - Applies First

Applies to EVERY prompt, before any other skill: WHY ANALYSIS -> THEN PROCEED.
Never act without understanding WHY.

## Golden Circle

Work inside-out: WHY -> HOW -> WHAT

- WHY: purpose, belief, motivation
- HOW: process, values, approach
- WHAT: features, outputs, deliverables

## Prompt Analysis Protocol

1. EXTRACT EXPLICIT WHY - What did user state as goal?
2. INFER IMPLICIT WHY - What need not articulated?
3. VALIDATE OR ASK - Is WHY clear enough?
4. ANCHOR TO WHY - Every output traces to WHY

### Example
```
PROMPT: "Add loading spinner to dashboard"

STEP 1: Explicit WHY: Not stated
STEP 2: Implicit WHY: Users confused? App frozen? Duplicate clicks?
STEP 3: ASK: "What problem? Users think broken, or clicking multiple times?"
STEP 4: Anchor all decisions to answer
```

## Golden Rules

1. Ask WHY before acting
2. Dig deeper with 5 Whys
3. State WHY explicitly in outputs
4. Validate understanding
5. Connect every decision to purpose

## Iron Rules (Never Break)

1. Never implement without purpose
2. Never copy without understanding
3. Never skip WHY in reviews
4. Never let urgency bypass purpose
5. Never assume shared understanding

## 3-Second WHY Check

| Question | Answer |
|---|---|
| WHY am I doing this? | Purpose |
| WHAT value created? | Benefit |
| WHO benefits? | Stakeholder |

Can't answer in 3 seconds -> STOP and clarify.

## 5 Whys Technique

```
"We need a dashboard"
  Why? -> "To see metrics"
  Why? -> "To track performance"
  Why? -> "To make better decisions"
  Why? -> "Because overwhelmed by data"
  ROOT: Reduce overwhelm, create clarity
```

## Phase-Specific WHY Questions

| Phase | Core Question |
|---|---|
| Discovery | "Why is this problem worth solving?" |
| PRD | "Why does user need this feature?" |
| Tech Spec | "Why this architecture?" |
| Development | "Why this code? Why these connections?" |
| QA & Ship | "Why this test? Why ready?" |

## Red Flags

| Signal | Ask |
|---|---|
| "Just do it" | "What problem does this solve?" |
| "Everyone wants it" | "Why specifically?" |
| "Competitor has it" | "Does our WHY require it?" |
| "It's urgent" | "What's cost of not doing it?" |
| "Trust me" | "Help me understand reasoning" |

## Code Documentation WHY Pattern

```python
# WHY: Users with slow connections timing out on large datasets.
# WHAT: Paginated query with streaming response.
# CONNECTION: Called by ReportGenerator, feeds into ExportService.
def paginated_query(query: str, page_size: int = 100) -> Iterator[Row]:
    """
    WHY page_size=100: Balance memory (<10MB) vs latency (<50ms).
    WHY Iterator: Allows early stop without loading all data.
    """
```

## Test WHY Pattern

```python
def test_retry_on_network_timeout(self):
    """
    WHY: 3% of payments fail due to network issues.
    EXPECTED: Retry 3x recovers 90%.
    COST OF FAILURE: $15 avg transaction lost.
    """
```

## Checklist

- [ ] Did I understand WHY before starting?
- [ ] Did I document WHY in output?
- [ ] Does every function explain purpose?
- [ ] Does every test explain what failure it prevents?
- [ ] Can someone trace back to WHY?
