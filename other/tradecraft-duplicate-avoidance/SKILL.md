---
name: tradecraft-duplicate-avoidance
description: >
  Avoid burning time on bugs that will be closed as duplicates. Load during bug-bounty work when
  deciding what to report or where to dig, on "will this be a dup", "is this already known",
  maximizing unique findings. Signals: a mature/popular program, a common vuln on an obvious asset,
  a recently expanded scope.
domain: tradecraft
type: methodology
stability: learning
modes: [bugbounty]
schema_version: 1
---

# Duplicate avoidance

## When it applies
Bug-bounty payouts go to the *first* valid report. On popular programs the obvious bugs on obvious
assets are already found, so the skill is steering toward findings that are still unclaimed — and
recognising when a bug you have is likely already in the queue.

## Why it works
Duplication is a function of visibility and timing: the more hunters have seen an asset and the
longer it's been in scope, the lower your odds on a surface-level bug. Freshness and novelty move you
to the front of the line, where the same effort actually pays.

## Method
1. **Read the disclosed reports** for the program (and the researcher's public activity) to learn
   what's already been found and what patterns the program pays for.
2. **Hunt fresh surface**: newly added scope, a feature shipped this week, an acquisition's domains —
   the crowd hasn't swept these yet. Monitor scope-change and asset feeds (`automation-*`).
3. **Go deeper, not wider**: a chained/business-logic bug or a variant behind auth is far less likely
   to be a dup than reflected XSS on the marketing site.
4. **Vary the obvious**: if you find a common bug, look for the *non-obvious instance* (a second
   endpoint, a different parameter, a bypass of the partial fix) that others stopped short of.
5. **Move fast on fresh scope**: when a program expands, the first 24-48h are the least duplicated —
   prioritise then.
6. **Sanity-check before reporting**: does this need no special preconditions and sit on the most
   obvious asset? If so, assume others found it — raise the bar or add a unique angle.

## Gotchas
- "Informative"/duplicate closes still cost you and the triager time — quality over quantity.
- Some programs pay dupes partially or not at all; know the policy (`tradecraft-bugbounty-platforms`).
- Novelty isn't an excuse for a weak report — a unique bug still needs solid proof (`reporting-*`).

## Verify success
Before investing in a report you can name why it's likely *not* a duplicate — fresh asset, behind
auth, a chain, or a variant others missed — not just "it's a valid bug".

## References
Program disclosure timelines; researcher write-ups on dup rates; the `tradecraft-target-selection` skill.
