---
name: search-kb
description: Search the product knowledge base for where a piece of work belongs — its domain, capability, and functionality — by reasoning over the KB router interface. Runs the inference sandwich (list domains, reason to the domain, read that shelf, reason to the capability/functionality) and emits a lightweight routing-result with the decision and why. Placement only — it does not evaluate product-profile conditions (that is selection, /shape's job). Use whenever a play or agent needs to know which part of the product model a request maps to.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Bash, Read
---

# search-kb

Routes a **piece of work** to its place in the KB tree: **domain → capability →
functionality**, with the decision and the reasoning recorded. This is C2 (#434).

## The interface

You call the KB router interface — never the KB files directly:

```
KB = core/components/memory/knowledge/domains/.pageindex/kb.py
python3 $KB domains            # all domains + triggers (the routing entry)
python3 $KB shelf <domain>     # full shelf markdown (to reason to capability/functionality)
python3 $KB search "<keywords>"# secondary keyword hint only
python3 $KB rebuild            # regenerate the index (if stale/missing)
```

The interface is the stable seam — today a local CLI, later a server; this skill
does not change when that moves.

## Procedure — the inference sandwich

Reasoning is yours (the skill); the interface only retrieves.

1. **List + reason to the domain (placement).** Run `python3 $KB domains`. Read the
   ~10 triggers and reason which domain the work belongs to. Pick one; pick more
   only if the work genuinely spans domains. This is **semantic placement** — do NOT
   consider product-profile conditions here.
2. **Read the shelf + reason to capability/functionality.** Run
   `python3 $KB shelf <chosen-domain>`. Reason over its `## Capabilities` to pick the
   capability and the functionality(ies) the work maps to. Note their profile
   conditions as metadata — do not evaluate them (that is selection, not placement).
3. **Emit the routing result** (schema below) with `why` for each placement.

If step 1 finds no domain that fits, set `unmatched: true` and stop — the
nothing-fits path (the `/route` caller) handles drafting a new node for review.

## Output — routing_result (lightweight; NOT an ADR)

```yaml
routing_result:
  work: "add SMS password reset for locked-out users"
  placements:
    - domain: user-management
      capability: Account Recovery
      functionality: [Password reset, Multi-channel support]
      confidence: high            # high | medium | low
      why: "credential recovery delivered over a non-default channel (SMS)"
      conditions:                 # metadata, copied — NOT evaluated here
        - "Multi-channel support — when shape.surfaces spans more than one, or shape.users: public"
  spans_multiple_domains: false
  unmatched: false
```

Emit it as JSON (the machine form). It must validate against
`.pageindex/validate_route.py`.

## Rules

- **Placement, not selection.** Never reject a placement because a profile condition
  fails — the asker already decided to build it. Return conditions as metadata only.
- **Reason over the small set.** With ~10 domains, do not lean on keyword `search`;
  read the whole `domains` list and reason. `search` is a hint, never the decision.
- **Record why.** Every placement carries a one-line rationale.
- **Honest confidence.** `low` when the work is vague or could sit in several places;
  flag `spans_multiple_domains` when it truly does.
