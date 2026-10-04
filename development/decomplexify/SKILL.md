---
name: decomplexify
description: "Knowledge base from \"Code Complete, 2nd Edition\" by Steve McConnell. Use when applying McConnell's software-construction frameworks for design, routines, defensive programming, variables/naming, testing, debugging, refactoring, code tuning, integration, and layout/style — while coding, studying the book, or referencing its concepts."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic, framework name, or chapter number]
---

# Code Complete, 2nd Edition
**Author**: Steve McConnell | **Pages**: ~900 | **Chapters**: 35 | **Generated**: 2026-06-07

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `naming`, `defensive programming`, `code tuning`, etc.; I find and read the relevant chapter file.
- **With a chapter** — ask for `ch08`; I load that file.
- **Browse** — ask "what chapters do you have?" for the full index.

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file before answering. Supporting files: [glossary.md](glossary.md), [patterns.md](patterns.md), [cheatsheet.md](cheatsheet.md).

> Note: the source was extracted via pdftotext, so verbatim code listings aren't preserved. This skill captures McConnell's principles, checklists, and named frameworks — its durable value — not exact code.

---

## Core Frameworks & Mental Models

**Managing Complexity = Software's Primary Technical Imperative.** Every construction decision serves this. When two approaches are otherwise equal, prefer the one that reduces complexity. Complexity is attacked with abstraction (hide detail) and encapsulation (enforce the hiding). (Ch 5, Ch 34)

**Software Construction.** The central hands-on activity — detailed design, coding, debugging, unit/integration testing, integration — distinct from upstream requirements/architecture and downstream system test/management. It's the one universally guaranteed activity and consumes 30–80% of project time, with 10–20× variation between individual programmers. (Ch 1)

**Metaphors are searchlights, not road maps.** They tell you *how to look*, not where to find. Hold an **intellectual toolbox** of methods and resist 100% commitment to any single methodology — pick the tool that fits the problem. "Construction" beats "writing" or "farming" as the general metaphor. (Ch 2)

**Measure Twice, Cut Once.** Upstream prerequisites (problem definition, requirements, architecture) reduce risk. **Defect cost escalates** from 1× at requirements time to 10–100× post-release — so fix problems as far upstream as possible. A problem definition must "sound like a problem," not a solution. (Ch 3)

**Program *into* your language, not *in* it.** Decide what you want to do, then use the language's primitives to express it — don't let language limits dictate your design. Establish conventions (naming, layout, error handling) *before* construction; they can't be retrofitted. Note your **technology-wave position** (early vs. late) and adjust estimates. (Ch 4, Ch 34)

**Information Hiding & Design Heuristics.** Generate interfaces by asking **"what must this hide?"** Hide volatile, likely-to-change areas. Apply heuristics as an ordered toolkit: find real-world objects → form consistent abstractions → encapsulate → inherit only for genuine "is a" → hide secrets → identify areas likely to change → keep coupling loose → use design patterns. Design is a **wicked problem** — iterate; the second attempt is better. (Ch 5)

**Classes & Routines.** Every class implements one **Abstract Data Type**; **containment ("has a") is the workhorse**, inheritance the exception. Every routine should have **functional cohesion** (one operation) and **loose coupling** (small, visible, flexible connections; ≤7 parameters, ordered in→modified→out). The #1 reason to make a routine is intellectual manageability. (Ch 6, Ch 7)

**Defensive Programming.** **Assertions for bugs; error handling for expected conditions.** Build a **barricade**: validate all external data at the boundary (dirty outside, clean inside). The *architecture* — not individual developers — decides **correctness vs. robustness**. Use offensive programming to make errors impossible to overlook during development. (Ch 8)

**Pseudocode Programming Process (PPP).** Build a routine by writing intent-level pseudocode, mentally checking it, then translating line-by-line to code with the pseudocode left as comments. Back up to pseudocode if quality is poor — don't patch forward. (Ch 9)

**Variables & Naming.** Minimize **span** and **live time** (keep references close; live time < 7); declare at first use; minimize scope. No magic numbers. Names answer "what is this?" without context (10–16 chars typical); qualifiers at the end (`revenueTotal`); booleans in positive form (`isDone`). (Ch 10–13)

**The General Principle of Software Quality.** Improving quality *reduces* cost by eliminating rework. **No single technique removes more than ~70% of defects** — combine inspections, testing, and review. Formal (Fagan) inspection detects 45–70%; the meeting is for detection only, never fixing. (Ch 20, Ch 21)

**Testing & Debugging.** **Structured basis testing**: minimum tests = 1 + one per decision keyword; always test boundaries (min, min+1, max−1, max). Debug with the **scientific method**: stabilize → hypothesize → experiment → prove → fix one thing → scan for siblings. Finding/understanding the defect is ~90% of the work; fix the cause, not the symptom. (Ch 22, Ch 23)

**Refactoring & Code Tuning are inverses — never conflate them.** **Cardinal Rule of Software Evolution**: internal quality must not degrade with change. Refactor incrementally behind a regression-test safety net. For performance, **measure before tuning**: ~20% of code uses ~80% of run time, but only profiling reveals which — and benchmarks don't transfer across platforms. Make it correct first; enable compiler optimization before hand-tuning. (Ch 24, Ch 25, Ch 26)

**Integration & Layout.** Prefer **incremental integration** over big-bang; run a **daily build and smoke test** as the project heartbeat (a broken build is the #1 defect). The **Fundamental Theorem of Formatting**: layout must reveal logical structure. Comment **intent (why)**, not a restatement of code. (Ch 29, Ch 31, Ch 32)

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-welcome-to-software-construction.md) | Welcome to Software Construction | construction boundary, productivity variation |
| [ch02](chapters/ch02-metaphors-for-software-development.md) | Metaphors for a Richer Understanding | intellectual toolbox, heuristic vs. algorithm |
| [ch03](chapters/ch03-upstream-prerequisites.md) | Measure Twice, Cut Once | defect cost escalation, prerequisites checklist |
| [ch04](chapters/ch04-key-construction-decisions.md) | Key Construction Decisions | programming into the language, technology wave |
| [ch05](chapters/ch05-design-in-construction.md) | Design in Construction | managing complexity, information hiding, design heuristics |
| [ch06](chapters/ch06-working-classes.md) | Working Classes | ADTs, containment over inheritance, Law of Demeter |
| [ch07](chapters/ch07-high-quality-routines.md) | High-Quality Routines | functional cohesion, loose coupling, parameter order |
| [ch08](chapters/ch08-defensive-programming.md) | Defensive Programming | assertions, barricades, correctness vs. robustness |
| [ch09](chapters/ch09-pseudocode-programming-process.md) | The Pseudocode Programming Process | PPP, design by contract |
| [ch10](chapters/ch10-general-issues-using-variables.md) | General Issues in Using Variables | span, live time, binding time, scope minimization |
| [ch11](chapters/ch11-power-of-variable-names.md) | The Power of Variable Names | naming conventions, qualifier position, booleans |
| [ch12](chapters/ch12-fundamental-data-types.md) | Fundamental Data Types | magic numbers, enums, floating-point, type aliasing |
| [ch13](chapters/ch13-unusual-data-types.md) | Unusual Data Types | access routines, pointer isolation, structures |
| [ch14](chapters/ch14-organizing-straight-line-code.md) | Organizing Straight-Line Code | sequential dependencies, principle of proximity |
| [ch15](chapters/ch15-using-conditionals.md) | Using Conditionals | nominal-path-first, boolean function extraction |
| [ch16](chapters/ch16-controlling-loops.md) | Controlling Loops | loop-with-exit, loop type selection, safety counter |
| [ch17](chapters/ch17-unusual-control-structures.md) | Unusual Control Structures | guard clauses, recursion limits, goto discipline |
| [ch18](chapters/ch18-table-driven-methods.md) | Table-Driven Methods | direct / indexed / stair-step access |
| [ch19](chapters/ch19-general-control-issues.md) | General Control Issues | boolean clarity, structured programming, McCabe complexity |
| [ch20](chapters/ch20-software-quality-landscape.md) | The Software-Quality Landscape | General Principle of Software Quality, multi-technique QA |
| [ch21](chapters/ch21-collaborative-construction.md) | Collaborative Construction | formal inspection, walk-through, pair programming |
| [ch22](chapters/ch22-developer-testing.md) | Developer Testing | structured basis testing, boundary analysis, test-first |
| [ch23](chapters/ch23-debugging.md) | Debugging | scientific method of debugging, fix the cause |
| [ch24](chapters/ch24-refactoring.md) | Refactoring | Cardinal Rule of Evolution, code smells, DRY |
| [ch25](chapters/ch25-code-tuning-strategies.md) | Code-Tuning Strategies | Pareto 80/20, measure before optimizing, performance hierarchy |
| [ch26](chapters/ch26-code-tuning-techniques.md) | Code-Tuning Techniques | loop tuning, strength reduction, lookup tables |
| [ch27](chapters/ch27-program-size-affects-construction.md) | How Program Size Affects Construction | diseconomy of scale, right-weight methodology |
| [ch28](chapters/ch28-managing-construction.md) | Managing Construction | configuration management, estimation, Brooks's Law |
| [ch29](chapters/ch29-integration.md) | Integration | incremental integration, daily build & smoke test |
| [ch30](chapters/ch30-programming-tools.md) | Programming Tools | tool categories, accidental vs. essential difficulty |
| [ch31](chapters/ch31-layout-and-style.md) | Layout and Style | Fundamental Theorem of Formatting, pure block |
| [ch32](chapters/ch32-self-documenting-code.md) | Self-Documenting Code | intent comments, comment taxonomy, book paradigm |
| [ch33](chapters/ch33-personal-character.md) | Personal Character | curiosity, intellectual honesty, character as habit |
| [ch34](chapters/ch34-themes-in-software-craftsmanship.md) | Themes in Software Craftsmanship | conquer complexity, people first, iterate |
| [ch35](chapters/ch35-where-to-find-more-information.md) | Where to Find More Information | tiered reading plan, periodicals |

## Topic Index

- **Abstraction / ADTs** → ch05, ch06
- **Architecture / prerequisites** → ch03, ch04
- **Assertions / error handling** → ch08
- **Boolean expressions** → ch15, ch19
- **Classes / encapsulation** → ch05, ch06
- **Code smells** → ch24
- **Code tuning / optimization** → ch25, ch26
- **Cohesion / coupling** → ch06, ch07
- **Commenting / documentation** → ch32
- **Complexity (managing)** → ch05, ch19, ch34
- **Configuration management** → ch28
- **Conventions** → ch04, ch11, ch34
- **Debugging** → ch23
- **Defensive programming** → ch08
- **Design heuristics** → ch05
- **Estimation / project size** → ch27, ch28
- **Formatting / layout** → ch31
- **Inheritance vs. containment** → ch06
- **Inspections / reviews** → ch21
- **Integration / daily build** → ch29
- **Loops** → ch16, ch19
- **Magic numbers / constants** → ch12
- **Metaphors / mental models** → ch02, ch34
- **Naming** → ch11
- **Pair programming** → ch21
- **Pointers** → ch13
- **Pseudocode (PPP)** → ch09
- **Quality (General Principle)** → ch20
- **Recursion / goto** → ch17
- **Refactoring** → ch24
- **Routines** → ch07, ch09
- **Scope / span / live time** → ch10
- **Structured programming** → ch17, ch19
- **Table-driven methods** → ch18
- **Testing** → ch22
- **Tools** → ch30
- **Variables** → ch10, ch11, ch12, ch13

## Supporting Files

- [glossary.md](glossary.md) — key terms with definitions and chapter refs
- [patterns.md](patterns.md) — concrete techniques with when/how/trade-off
- [cheatsheet.md](cheatsheet.md) — quick-reference rules and decision tables

---

## Scope & Limits

Covers the book's content only. Verbatim code listings were not preserved through text extraction — for exact syntax consult the book or cc2e.com. For hands-on implementation in a real codebase, combine these frameworks with project-specific tools.
