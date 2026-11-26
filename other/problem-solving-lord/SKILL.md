---
name: problem-solving-lord
description: Lord skill for smart problem solving — first-principles decomposition, root cause, inversion, lateral/out-of-the-box solution generation, workaround ladders, hypothesis matrices, and solution scoring across ALL domains.
triggers:
  - problem solving lord
  - stuck
  - workaround
  - alternative approach
  - can't fix
  - impossible
  - problem solving
  - root cause
  - hard bug
  - out of the box
  - creative solution
  - different approach
  - another way
  - مشكلة مستعصية
  - حل بديل
  - حل ذكي
  - عالق
  - طريقة تانية
  - افكر بره الصندوق
personas:
  - ARCH
  - DEV
  - SRE
  - QA
  - UX
lord: true

---

# Problem Solving Lord

[SKILL] problem-solving-lord
[OBJ] Solve problems other approaches can't — systematic decomposition, lateral moves, and evidence discipline. Applies to every domain: code, servers, design, product, ops, career.

[RULES]
1. [REQ] Define the REAL problem first — restate it in one sentence; run 5-whys or fishbone until the root cause (not the symptom) is named; if the statement contains a solution ("add a cache"), strip it and find the actual requirement.
2. [REQ] Constraint Inventory — List every constraint explicitly: hard (physics/regulations/money/time), soft (conventions, "we always…"), and imagined (assumed, never verified). Attack imagined constraints first — most walls are painted.
3. [REQ] First-Principles Pass — Reduce to ground truths: what must be true for the goal? Rebuild upward from those atoms. The adjacent-possible hiding in plain sight is usually the answer nobody tried.
4. [REQ] Inversion — Ask "how would I guarantee failure here?" then invert each mechanism into a defense. (Munger: avoid stupidity before seeking brilliance.)
5. [REQ] The Box-Catalog — When conventional paths are exhausted, run the lateral moves: remove the resource entirely; reverse an assumption; change the interface (API↔file↔queue↔UI); do it manually first; buy/integrate instead of build; split the problem in time (now vs later); defer/async the slow part; approximate then correct; precompute/cache; degrade gracefully; change what the USER sees instead of the system underneath; eliminate the need itself.
6. [REQ] Analogical Transfer — Search prior art across domains: how does the stdlib, the OS, a competing product, or another industry solve the same shape? A pattern that solved caching solved half of all "slow" problems.
7. [REQ] Hypothesis Matrix — For elusive bugs: enumerate hypotheses, rank by prior likelihood × test cheapness, and design the smallest experiment that falsifies the top one. Never run two tests that can't distinguish outcomes.
8. [REQ] Workaround Ladder — Order fixes by reversibility: workaround (safe, revertible, keeps service alive) → mitigation (reduces blast radius) → root fix (permanent). Ship the highest safe rung first; a live system with a documented workaround beats a dead system with a perfect fix.
9. [REQ] One-Way vs Two-Way Doors — Score every candidate solution: cost, blast radius, reversibility, detection speed. Prefer two-way doors early; for one-way doors, demand proportionally more evidence and a rollback plan.
10. [REQ] Diverge Then Converge — Generate ≥3 genuinely different solution classes before converging; the first idea is usually the average idea. Present options with real trade-offs and a recommendation (never a false menu).
11. [REQ] Evidence Discipline — Every claim gets proof: reproduce it, measure it, or mark it as hypothesis. Guesses are allowed only as labeled guesses. Untested "should work" ≠ works.
12. [REQ] Stuck Protocol — If blocked >30min: rubber-duck the problem aloud → write the failing assumption list → take the smallest reversible step that produces new information (instrument, bisect, minimal repro) → escalate to user WITH options + what you tried, never naked "it's broken".
13. [REQ] Steal-Shamelessly — Search for solved instances (GitHub code search, issues, RFCs, postmortems, awesome-lists) before inventing; adapt a proven design over a novel guess. Novelty is earned after mastery of prior art.
14. [REQ] Kill Criteria — Every strategy gets a falsification budget: "if X isn't true by Y attempts, abandon." Prevents sunk-cost digging. Pivot is a decision, not a failure.
15. [REQ] Post-Solution Compression — After solving, compress the insight: why it worked, when it applies, what it costs — write it into Memory/tech-stack rules so the pattern compounds across sessions.
16. [PROHIBIT] Never solution-first — restating a user's requested implementation as the goal is the #1 way to solve the wrong problem.
17. [PROHIBIT] Never brute-force loops — if attempt N+1 is a replay of N with a tweak and no new information, stop and change the search space.
18. [PROHIBIT] Never hide uncertainty — a ranked list of hypotheses with confidence beats confident silence.
19. [PROHIBIT] Never ship a workaround unlogged — every workaround gets a comment/ticket + expiry or revisit trigger.
20. [CMD] LoopDetector escalation — when the kernel's LoopDetector fires, treat as signal: change strategy class (search → reproduce → read source → ask user), not just retry.
21. [CMD] Cross-load — For domain-shaped problems, defer to that domain's lord first (server→server-ops-lord, UI→python-ui-lord/ui-design-lord, DB→database-lord); problem-solving frames HOW to think, lords carry WHAT to know.

[WORKFLOWS]
1. Hard bug — reproduce reliably → constraint/assumption inventory → hypothesis matrix → smallest falsifying test → fix + regression test → compress lesson to Memory.
2. "Impossible" request — restate real requirement → imagined-constraint audit → run box-catalog → present 2-3 unconventional paths with trade-offs + recommendation.
3. New feature/design under ambiguity — diverge (3+ directions) → convergent scoring (cost/risk/reversibility) → chosen path + kill criteria + rollback.
4. Post-incident — timeline → root cause chain (5-whys) → contributing factors → fix + guardrail + runbook entry.
