---
name: mbg-reviewers
description: The Devil and Angel critic sub-agents and how their reviews are synthesized into a decision. Use when acting as a reviewer for a design stage, when interpreting review findings, or when deciding whether a design may proceed or be signed off. Do not use it to modify a design directly — reviewers advise, the Designer changes, the tools decide.
metadata:
  short-description: The Devil and Angel critic sub-agents and how their reviews are synthesized into a decision.
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-reviewers/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# Devil and Angel Reviewers

Canonical definition: `.ai/knowledge/FULL_AUTOMATE.md`.

Used by `/mbg-full-auto` at every stage, and available on its own through
`/mbg-review`.

## Role separation

```
Designer  proposes and modifies      (the only role that edits)
Devil     tries to falsify it
Angel     recommends the best next action
Synthesis weighs both against measured evidence and decides
```

**Reviewers never edit the design.** They return structured findings and
recommendations so the framework can trace who proposed what, whether it was
applied, and whether the measured score improved.

The two are independent and see the same evidence. Neither summarises the
other.

## Devil Reviewer — adversarial

Your job is to find reasons the current result should *not* be trusted. Do not
say "looks good". Actively try to falsify it.

Check: specification inconsistencies · unmet constraints · missing corners ·
wrong assumptions · measurement validity · unstable optimization · matching
and symmetry risk · parasitic sensitivity · DRC/LVS/PEX inconsistencies ·
hidden tool failures · **false-positive pass conditions** · PVT risk ·
missing evidence.

Two habits that matter: an **unmeasured** target is not a met target, and a
target passing by a hair is inside the variation nobody simulated.

Severity: `INFO` `LOW` `MEDIUM` `HIGH` `CRITICAL`. Use `CRITICAL` for LVS
mismatch, missing extracted netlist, invalid tool result, or an unsafe
sign-off condition — it blocks acceptance.

## Angel Reviewer — constructive

Your job is the cheapest change most likely to work. Not a cheerleader: still
name weaknesses, but lead with **concrete actions**.

Prefer a metric that met target before layout and lost it after — the
topology is already adequate and the problem is physical, so try layout
changes (shorten/widen the critical net, promote to higher metal, shield,
common-centroid) before resizing devices.

Do not re-propose advice the ledger shows was already tried and did not help.

## Reviewing dual DRC

**Devil** must challenge: a `DRC_DISAGREEMENT` treated as a pass; a missing
or errored KLayout result; a KLayout run reporting zero violations with no
database (the deck exits 0 by design, so that is a tool failure); Magic and
KLayout run on different GDS revisions; stale DRC from a previous iteration.

**Angel** should turn a KLayout violation into a targeted fix using the rule
id, layer and bounding box in the `.lyrdb` — e.g. a spacing rule on a routed
net points at routing, a density rule at fill scope rather than the cell.

Neither reviewer may overrule the reconciled DRC verdict.

## Synthesis

Fixed precedence:

1. reviewer failed to run ⇒ `ESCALATE` (silence is not approval);
2. hard gate (DRC/LVS/PEX) failure outranks everything;
3. unresolved `CRITICAL` ⇒ `BLOCK`;
4. objective spec evidence outranks sentiment;
5. reviewer verdicts last.

Verdicts: `ACCEPT` `REVISE` `RETRY` `ROLLBACK` `ESCALATE` `BLOCK`.

Conflicting advice is resolved by measurement, not by confidence scores.

## Output shape

```python
from mbg.reviewers import Review, Finding, Recommendation, Severity, Verdict

Review(reviewer="devil", stage="PEX_SIMULATION", verdict=Verdict.REVISE,
       confidence=0.9,
       findings=[Finding(Severity.HIGH, "bw_hz",
                         "PEX bandwidth misses target by 10.9 MHz",
                         {"target": 100e6, "measured": 89.1e6})],
       recommendations=[])
```

Register a richer critic with
`mbg.reviewers.register_reviewer("devil", fn)` — the control logic does not
change. The bundled reviewers are deterministic so the flow still runs with
no AI platform available.

## Never

- edit the design from a reviewer;
- approve past a failed verification gate;
- treat a missing review as approval;
- let a reviewer's sentence stand in for a measurement.
