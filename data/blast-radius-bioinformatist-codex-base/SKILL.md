---
name: blast-radius
description: Trace what an actual code change could break beyond its diff when interfaces, serialized data, database schemas, configuration, caches, lifecycle ordering, or cross-language consumers are involved. Use for explicit impact analysis; not local renames, prose edits, ordinary dependency bumps, or generic architecture discussion.
license: MIT
---

# Blast Radius

Follow the changed behavior beyond symbol callers. Read the actual diff and
reuse existing searches, tests, fixtures, and runtime checks before adding any.
Analysis alone authorizes no edits, production probes, delegation, or publication.

1. State the changed contract and the one or two facts its safety depends on.
   Find callers and consumers, including dynamic registration and generated code.
2. Follow applicable boundaries: API and CLI interfaces, serialization and wire
   formats, database readers and writers, config defaults and persisted values,
   caches and invalidation, startup/teardown or async ordering, and consumers in
   other languages. Check the pinned library source and local patches when the
   safety fact depends on dependency behavior. Mark irrelevant boundaries with
   the evidence that rules them out; do not invent consumers.
3. Give each plausible failure a mechanism, affected consumer, likelihood, and
   consequence. Classify it as confirmed, ruled out, or unproved. Cite file/line
   evidence and distinguish source reasoning from an executed check. A search
   with no hits is evidence only for the search's stated scope.
4. Test the critical safety fact with the cheapest existing check that exercises
   real behavior. Add a small reproduction only if a material gap remains and
   the task permits it. Report the actual command and result, or the unrun check
   and why it remains needed; a convincing explanation is not runtime proof.

Finish with changed behavior, critical safety facts, confirmed risks, ruled-out
cases, and unproved gaps with their next check. Stop when each applicable
boundary and safety fact has evidence or an explicit unresolved disposition.

Adapted from Lauren Tan's [pstack blast-radius](https://github.com/cursor/plugins/blob/6ce45c59b9301a638c1fe1a7b8dc2a82b650898f/pstack/skills/blast-radius/SKILL.md), under the [MIT license](LICENSE).
