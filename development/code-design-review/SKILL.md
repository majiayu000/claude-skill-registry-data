---
name: code-design-review
version: "1.3.0"
user-invocable: true
description: "Authoritative framework for reviewing the design quality of proposed code changes — before implementation. Evaluates architecture-level quality attributes (testability, modularity, reliability, scalability, dependency direction via ISO 25010 + Clean Architecture + SDP) and code-level metrics (accidental complexity, coupling via Myers/Connascence, cohesion, change amplification, tech debt, cyclomatic/cognitive complexity, Law of Demeter) plus a security pass (OWASP Top 10). Use this skill whenever a proposed solution involves code changes and you need to assess whether the code is well-designed — not just whether it works, but whether it is maintainable, testable, and does not introduce design debt. Triggers — 「代码审查」「代码设计审查」「代码设计质量」「审查代码设计」「代码架构审查」「设计质量评估」「代码质量评审」「这个代码设计合理吗」「耦合度审查」「代码可维护性」 / code design review, code architecture review, design quality assessment, coupling analysis, maintainability review."
---

# Code Design Review

> **Role**: A pre-implementation design-quality review for solutions that involve code changes. It evaluates whether the proposed code is well-crafted — maintainable, testable, properly decoupled — not just whether it solves the problem. It is the code-specialized companion to `solution-review` (which handles decision-level review for any solution type). PDCA hosts declare this skill in frontmatter `dependencies` and invoke it after a prerequisite check (the host aborts at startup if this skill is missing).
>
> **Detailed framework entries** (author, year, thresholds, source) and the full blocking/non-blocking criteria live in [reference.md](reference.md).

## Why this skill exists

A code solution can be correct (it solves the problem) and still be poorly designed — introducing coupling that makes the next change harder, complexity that exceeds what the problem demands, or tech debt the team does not know it holds. These design failures are invisible to "does it work?" testing; they surface months later as maintenance pain, regression cascades, and fear of change.

**AI-era premise:** when implementation is cheap (including AI-assisted coding), "it works and is near-term maintainable" is a weak bar. Architectural elegance and **long-term** maintainability must carry higher review weight — rewriting a better structure often costs less than living with the debt.

This skill applies software-engineering theory — not opinion — to evaluate code design quality before a single line is written. Every check item traces to a named framework (Brooks, Myers, Yourdon-Constantine, Fowler, McCabe, ISO 25010, Clean Architecture, OWASP). The meta-lesson:

> **Code that works but is poorly designed becomes tomorrow's maintenance crisis. Review design quality before implementation, when changing direction is still cheap — and do not defer a clearly better architecture just because shipping the weaker one is easy.**

## When to use

Strong signals (any one):

- A proposed solution **involves code changes** and you need to assess its design quality before implementation.
- You are reviewing a design doc, technical proposal, or approach that includes code structure decisions (new modules, API design, refactoring, dependency changes).
- Someone asks "is this code well-designed?" or "will this be maintainable?" or "is the coupling acceptable?"
- A solution involves architecture-level decisions (new abstraction layers, dependency direction changes, module boundary shifts).

This skill is for **code** solutions only. For non-code solutions (config, process, tooling, architecture decisions without code), use `solution-review`. When a solution involves code, use **both**: `solution-review` for the decision, this skill for the code craft.

## Relationship to other skills

| Skill | Responsibility | Relationship to this skill |
|-------|---------------|----------------------------|
| `solution-review` | Decision-level review (effectiveness, risks, reversibility, operability, cost) | The superset. For code solutions, `solution-review` checks the decision; this skill checks the code design. Use both. |
| PDCA hosts | Host workflows | **Referenced by** PDCA hosts via frontmatter `dependencies` (missing → host aborts). Deep-dive of their "review solution" phase for code-affecting solutions. Hosts are SoT for that edge. |

## The code design quality model

Three layers, **ordered by importance — architecture first** — with depth scaled to the solution's scope. Presentation order encodes review priority: architecture-level attributes and long-term maintainability get the reviewer's attention before code-level craft.

### Layer A — Architecture-level quality attributes

These evaluate the solution's impact on system-level quality attributes — the layer that carries architectural design and long-term maintainability weight. Run full Layer A when the solution adds modules, changes dependency direction, crosses module boundaries, crosses process or layer boundaries, or alters public contracts. **Quick path** (small, isolated change with no new boundaries and no dependency-direction impact) may do a fast Layer A skim — state that limitation in the report. Do not skip Layer A because implementation looks easy.

1. **Testability** (Clean Architecture — Uncle Bob) — Can business logic be tested without the UI, database, web server, or external services? If the solution makes logic un-testable in isolation, that is an architecture violation. Hard-to-test signals: hidden dependencies, static method calls, singletons, law-of-Demeter violations.
2. **Modularity** (ISO/IEC 25010 — Maintainability → Modularity) — Does one change minimize impact on other components?
3. **Reliability / resilience** (ISO/IEC 25010 — Reliability → Fault tolerance, Recoverability) — Does the solution consider failure scenarios (degradation, retry, circuit breaking)?
4. **Scalability** (ISO/IEC 25010 — Performance efficiency → Capacity) — Can the solution handle expected data volume / concurrency growth, or does it embed a bottleneck?
5. **Dependency direction** (Stable Dependencies Principle + Clean Architecture Dependency Rule) — Do dependencies point toward stability (stable modules depended-on by unstable ones), or does a stable module depend on an unstable one (inverted, fragile)? **Architecture-boundary verification** (for solutions crossing process or layer boundaries): (a) *runtime initialization location* — which process/layer actually initializes the called capability (FFI handles, databases, caches, service singletons); (b) *boundary legality* — can the caller legally reach it, or would a cross-layer static or dynamic import pull the callee's dependency tree (with its circular dependencies) into the caller's bundle graph? Bundler static pre-scanning means dynamic `require`/`import` does **not** bypass this; (c) *ownership classification* — is the capability a system capability (belongs in the shell/host layer) or a data/product capability (belongs in the service/product layer), and does that match the calling layer's positioning?

### Layer B — Code-level design metrics (every code change, mandatory)

These are the metrics that apply to any code change, regardless of scale. Each traces to a named SE framework:

6. **Accidental complexity** (Fred Brooks, *No Silver Bullet*, 1986) — Does the solution introduce indirection, configuration, or abstraction that does not map to the problem's inherent complexity? Every new abstraction needs a reason that exists *now*; "might need it later" is accidental complexity — cut it at review.
7. **Coupling classification** (Myers coupling taxonomy + Connascence, Page-Jones 1996) — What type of coupling does the change introduce? Data coupling (passing data, acceptable) → Stamp (sharing composite structures, low risk) → Control (passing flags that direct another module's logic, leaks decisions) → Common (shared mutable state, high risk) → Content (directly manipulating another module's internals, unacceptable). Connascence sharpens this: name/type connascence is benign; algorithmic/execution/timing connascence is fragile.
8. **Cohesion gradient** (Yourdon & Constantine, *Structured Design*, 1979) — After the change, do the module's elements converge on one purpose (Functional cohesion, strongest) or are they bundled by time/logic/coincidence (Temporal / Logical / Coincidental, weakest)? A downgrade in cohesion is an early design-degradation signal.
9. **Change amplification** (Fowler, *Shotgun Surgery* code smell + Open-Closed Principle) — Does the solution localize frequent changes, or scatter one logical change across many files? Good design separates volatile decisions (business rules, config) from stable cores (data models, algorithms).
10. **Tech debt classification** (Fowler, Technical Debt Quadrant) — Is the debt Prudent-Deliberate (knowingly chosen with a repayment plan, acceptable) or Reckless-Inadvertent (introduced because a better design was unknown — God Object, Speculative Generality, Primitive Obsession)? Reckless-Inadvertent debt must be blocked because the holder does not know the debt exists and will never repay it.
11. **Complexity metrics** — **Cyclomatic complexity** (McCabe, 1976): count decision points + 1; threshold >10 warrants review, >15 is high risk, >20 is unacceptable for a single function. **Cognitive complexity** (SonarSource, 2016): weights nesting, recursion, and logical operators to capture human-readable difficulty; threshold >15 warrants review. Prefer cognitive complexity — it catches what cyclomatic misses (deep nesting reads as hard even with few branches).
12. **Law of Demeter** (Lieberherr & Holland, 1989) — A method should only talk to its immediate friends, not strangers: `a.b().c().d()` ("train wreck") couples the caller to the internal structure of distant objects. Flag chains deeper than 2 levels in the proposed design.

### Layer C — Security pass (when the solution touches a trust boundary)

13. **OWASP Top 10 lightweight review** — When the solution touches authentication, authorization, input handling, data storage, or external communication, run a lightweight OWASP pass: injection (unparameterized queries), broken auth, sensitive data exposure, XXE, broken access control, security misconfiguration. This is not a full security audit; it catches the design-level security mistakes before they become code.

> Detailed method, thresholds, and source citations for each item are in [reference.md](reference.md).

## How to apply

1. **Confirm the solution involves code.** If not, use `solution-review` instead.
2. **Run Layer A** (architecture) per its scope rules — full vs quick path; always disclose the path in the report.
3. **Run Layer B** for every code change. Produce a pass/fail for each of the 7 metrics with concrete reasoning tied to the proposed code structure.
4. **Run Layer C** only if the solution touches a trust boundary (auth, input, data, external comms). Otherwise skip.
5. **Produce a structured review report** (see Output below) with per-item verdict, blocking/non-blocking classification, and overall conclusion.
6. **Gate on blocking issues.** Blocking issues mean the code design does not pass. Low implementation cost (including AI assistance) does **not** convert a material architecture gap into a non-blocking note.

### Blocking vs non-blocking (summary)

**Blocking** (any one → code design does not pass):
- Dependency direction inverted — a stable module depends on an unstable one (violates SDP).
- **(Layer A, full path)** Business logic cannot be tested in isolation from external dependencies (violates Clean Architecture testability), with no compensating measure.
- **(Layer A, boundary-crossing solutions)** The called capability has no runtime in the caller's process/layer, or a cross-layer import pulls an unrelated dependency tree into the caller — blocking unless explicitly accepted as Prudent-Deliberate debt with a repayment plan. Short-term cost advantages (reuse of an existing implementation, single-repo change, no cross-team coordination) do not downgrade this verdict.
- Content coupling (directly manipulating another module's internals) or Common coupling (shared mutable state) with no alternative.
- Reckless-Inadvertent tech debt — God Object / Speculative Generality / Primitive Obsession introduced without awareness of better design.
- A single business change requires cascading edits to 3+ modules with no direct business relationship (Shotgun Surgery), with no convergence strategy.
- **(Security)** An OWASP Top 10 category is violated at the design level (e.g., design allows injection, broken access control).
- A **clearly superior** modular / dependency / boundary design is identified, is **feasible within the current change scope**, and **materially improves long-term maintainability** — and the team has not explicitly accepted Prudent-Deliberate debt with a repayment plan. Do **not** pass solely because the weaker design is correct and near-term maintainable.

**Non-blocking** (note as recommendation, do not block):
- Style or naming preferences that do not change structure, coupling, or change amplification.
- Prudent-Deliberate tech debt with a documented repayment plan (including an explicitly accepted weaker architecture).
- Cyclomatic/cognitive complexity slightly above threshold in an inherently complex domain (document the reasoning).
- A more elegant *implementation detail* (same architecture) exists, but the current one is correct and does not worsen long-term maintainability.

> Full blocking/non-blocking criteria with framework-specific thresholds are in [reference.md](reference.md).

## Output

A code design review report with this structure:

```
【Code design review report】
- Subject: [solution name / code area]
- Path: [quick / full] + [security pass: yes/no]
- Layer A architecture quality attributes (full path):
  1. Testability: ✅/❌/N/A
  2. Modularity: ✅/❌/N/A
  3. Reliability / resilience: ✅/❌/N/A
  4. Scalability: ✅/❌/N/A
  5. Dependency direction: ✅/❌/N/A
- Layer B code-level design metrics:
  6. Accidental complexity: ✅/❌ [reasoning]
  7. Coupling type: ✅/❌ [type identified + risk level]
  8. Cohesion: ✅/❌ [cohesion level + trend]
  9. Change amplification: ✅/❌ [shotgun surgery check]
  10. Tech-debt classification: ✅/❌ [quadrant identified]
  11. Complexity measures: ✅/❌ [cyclomatic / cognitive estimate]
  12. Law of Demeter: ✅/❌ [train-wreck check]
- Layer C security pass (trust boundary):
  13. OWASP lightweight pass: ✅/❌/N/A
- Issue list: [#] [description] [severity: blocking/non-blocking]
- Verdict: ✅ pass / ❌ fail
- [On ❌] Optimization guidance: [per-issue improvement direction]
```

## Anti-patterns (forbidden moves)

1. **Approving code that "works" without a design pass** — correctness is necessary but not sufficient; skipping Layer A/B/C entirely because tests are green is how design debt accumulates invisibly.
2. **Running Layer C (security) on everything** — the OWASP pass is for trust-boundary-touching changes only. Over-applying it wastes review effort; under-applying it on trust boundaries is dangerous.
