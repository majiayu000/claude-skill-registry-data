---
name: harness-skill-compare
description: Use for a substantive comparison of skill triggers, behavior or curation choices. Scale narrow overlap questions to the relevant branches.
---

# Harness Skill Compare

Compare selected skills at the depth the question requires. For a narrow overlap
question, read descriptions, relevant body branches and their direct dependencies.
For a full behavioral comparison, inventory all shipped instructions, metadata
and scripts, distinguishing inspected code from executed behavior.

Consult `harness_lifecycle/registry/` for classification and prior decisions:
`INDEX.md` for coordinates, `skill-records/` for our skills' lineage, history and
earlier reviews, `references/<harness>.md` for rulings on reference capabilities.
Use configured bounded delegation only when helpful; no mandatory subagent-choice
question applies.

For a durable comparison that decides a merge, upgrade or rebuild of one of our
skills, write a skill review: `harness_lifecycle/registry/reviews/<yyyy-mm-dd>-skill-<our-skill>.md`
(`registry/README.md` §5a). Its parts, in order:

1. **Set**: our skill and each upstream counterpart, with repo, path and the
   pinned commit read.
2. **Components**: each behavioral component (step, gate, template, rule,
   heuristic, red-flag table) with `file:line`. A heading is not a component.
3. **Matrix**: one row per component, one column per skill: `✓` present, `~`
   variant, `—` absent.
4. **Differences**: for every `~` row and differing `✓` row, how each skill
   realises it and which mechanism is stronger, with the reason.
5. **Verdict**: substitutes or complements; what to take, from where, and what
   to leave, each with its reason.

A narrow answer stays in chat and creates no file. State coverage and unverified
behavior; description text alone does not prove actual invocation frequency.

Comparison is read-only on the compared skills. Rulings belong to authorized
harness-evaluate work, which cites the review in each event's `evidence`.
