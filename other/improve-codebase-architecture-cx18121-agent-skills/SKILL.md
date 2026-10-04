---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present a visual report, then explore the selected candidate.
disable-model-invocation: true
---

# Improve Codebase Architecture

Find architectural friction and propose deepening opportunities that improve locality, leverage, and testability.

## 1. Choose the scan area

Use the module, subsystem, or pain point named in the request. Otherwise inspect a useful stretch of recent Git history and follow the paths that change repeatedly. Widen only when there is no clear hot spot.

Read current project guidance first. Read a domain glossary and relevant ADRs when they exist. Load `codebase-design` for the module, interface, depth, seam, adapter, leverage, and locality vocabulary.

## 2. Explore

Inspect source, callers, tests, and recent changes. Look for:

- Understanding one concept requires bouncing across many files.
- A module's interface is nearly as complex as its implementation.
- Closely related decisions leak across seams.
- Tests reach through the public interface to control internals.
- Repeated changes scatter across several owners.
- Deleting a suspected shallow module would merely move its complexity elsewhere.

Use subagents only when separate scan areas can produce distinct evidence. Keep one owner for synthesis.

## 3. Present candidates

Write a self-contained HTML report to the operating system temp directory and open it. Follow [`HTML-REPORT.md`](HTML-REPORT.md).

For each candidate, show:

- The files and current owner.
- The observed friction.
- The proposed deeper module.
- The smaller interface and what moves behind it.
- How callers and tests improve.
- A before and after diagram.
- Recommendation strength: `Strong`, `Worth exploring`, or `Speculative`.

End with one top recommendation and why it wins. Do not propose detailed interfaces yet. Do not edit the repository.

## 4. Explore the selected candidate

Ask which candidate to explore. Then use the `grill-me` process to settle only decisions that require judgment. Investigate factual questions yourself.

Use `codebase-design` to compare materially different interfaces when the seam is still unresolved. Finish with the recommended module shape, caller experience, important invariants, test surface, migration outline, and remaining tradeoffs.

Do not implement unless the request separately authorizes implementation.
