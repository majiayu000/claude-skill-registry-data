---
name: stations
version: 0.1.0
license: MIT
description: Use when facing two or more independent pieces of work - separate bugs, separate subsystems, separate repos - that could be executed by concurrent agents, before dispatching any of them. Also use when the user says "fan out", "parallelize this", or hands over a pile of unrelated failures.
---

# stations

A kitchen runs fast because each station cooks its own dish: garde manger does not wait for the grill. But the speed comes from the cuts being made before service, and two cooks at one board ruin both dishes. This skill is the expeditor's fan-out: deciding what is genuinely separate work, giving each station a complete ticket, and tasting everything together before it leaves.

**Core principle:** parallelism is earned by proving independence, not assumed from the symptom list. The fan-out is the last step of triage, never the first move.

## Triage before any dispatch

The expensive mistake is dispatching one agent per symptom. Symptoms group by root cause, and a refactor that broke four things usually broke two things twice.

1. **Cluster by suspected cause, not by file.** Two failures in different test files that both touch the same layer (the same data shape, the same recent change) are one cluster until proven otherwise. Check what actually changed (`git log`, the refactor's diff) before declaring anything independent. Symptoms living in different files is not independence; it is the same bug crashing in two places.
2. **One cluster, one station.** A shared root cause dispatched to two agents buys two local symptom patches that each make their own test green and disagree with each other - one patches the data producer, the other patches a consumer, and the suite is green while the design is incoherent. The cluster goes to a single agent with the whole picture, applying [refire](../refire/SKILL.md)'s root-cause discipline inside.
3. **Check the write sets.** Stations that would edit the same files do not run concurrently: serialize them, or give each its own worktree (prefer the harness's native worktree tool; verify a manual worktree directory is gitignored). Read-only overlap is fine.
4. **Anything exploratory stays with you.** If you do not yet know what is broken, that investigation is not parallelizable; fan out after it, not instead of it.

When in doubt, fewer stations. A wrongly merged cluster costs one slightly bigger ticket; a wrongly split one ships two half-fixes.

## The ticket each station gets

Subagents inherit nothing; the prompt is everything they know. Each ticket carries:

- **One scope**, named: the file, test file, or subsystem it owns, and the instruction to touch nothing else.
- **The full symptom**: actual error text, failing test names, expected vs observed. Not "fix the race condition".
- **The relevant context**: what changed recently, what the documented contract says, where the working sibling lives.
- **Constraints**: do not edit tests to make them pass, do not refactor beyond the named scope, stop and report rather than improvise if reality contradicts the ticket.
- **An output contract**: the diff, the verification command they ran, its actual output, and anything they noticed that smells like another station's problem (an overlap signal for you, not theirs to fix).

## When they return

1. Read every report; confirm each diff stayed inside its scope (`git diff --stat` does not lie; reports sometimes do).
2. Look for semantic conflicts, not just textual ones: two green stations can still disagree about a data shape. Cross-cutting smells reported by one station get checked against the others' diffs.
3. Run the full suite and every checker yourself, once, on the integrated result ([check](../check/SKILL.md): a station's "verified" is a claim, not evidence). Per-station green proves each piece; only the integrated run proves the meal. The final verification is yours and is never delegated.
4. One station red or blocked? Handle it directly or redispatch with something changed (more context, smaller scope). Do not let one red station hold the integration of the green ones longer than it must.

## Common mistakes

- One agent per failing test file, straight from the CI list, no triage. The symptom list is not a work breakdown.
- "All independent, already root-caused" declared from symptom descriptions alone. A symptom description is not a root cause; the cluster check takes five minutes and the double-fix costs an afternoon.
- Treating file-disjoint edits as proof of independence while two stations patch the producer and the consumer of the same broken data.
- Parallel writers in one working tree on overlapping files, then an integration step that is mostly conflict archaeology.
- Tickets that say "fix the test" without the error text, so the station spends its run rediscovering what you already knew.
- Skipping the integrated full-suite run because every station reported green. The dishes were tasted; the meal was not.
