---
name: cleancode
description: "Knowledge base from \"Clean Code: A Handbook of Agile Software Craftsmanship\" by Robert C. Martin (Uncle Bob). Use when writing, reviewing, or refactoring code and you want guidance on naming, functions, comments, formatting, error handling, unit tests / TDD, classes, systems, concurrency, or the smells-and-heuristics catalog."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic, framework name, or chapter number]
---

# Clean Code: A Handbook of Agile Software Craftsmanship
**Author**: Robert C. Martin (Uncle Bob), with contributors | **Pages**: ~462 | **Chapters**: 17 + Appendix A | **Generated**: 2026-06-07

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `naming`, `functions`, `TDD`, `boundaries`, `code smells`; I find and read the relevant chapter.
- **With a chapter** — ask for `ch03` or `ch17`; I load that file.
- **Browse** — ask "what chapters do you have?" to see the full index.

When you ask about a topic not covered in Core Frameworks below, I read the relevant chapter file before answering. The capstone reference is **ch17 (Smells and Heuristics)** — a 60-item review checklist.

---

## Core Frameworks & Mental Models

**The central thesis.** Code is read far more than it is written (~10:1), so optimize for the reader. Clean code does one thing well, reads top-to-bottom like prose, and was achieved by *cleaning dirty code*, not by being written perfect. "You must first write dirty code and then clean it" (Ch14).

**The Boy Scout Rule (Ch1).** *Leave the campground cleaner than you found it.* Every checkin should leave the codebase slightly cleaner than you checked it out — rename one variable, split one long function, kill one duplication. Continuous small improvement beats scheduled cleanup that never comes.

**LeBlanc's Law (Ch1).** *Later equals never.* A mess deferred is a mess kept; "I'll clean it up later" is how cruft becomes permanent. The only way to go fast is to keep the code clean.

**Meaningful Names (Ch2).** Use intention-revealing names; avoid disinformation; make meaningful distinctions (not `a1, a2`); use pronounceable and searchable names; avoid encodings (no Hungarian notation, no `m_` prefixes); pick one word per concept (`get`/`fetch`/`retrieve` — choose one). Name length should match scope size.

**Functions (Ch3) — the most cited rules:**
- *Small!* Functions should be ~≤20 lines; blocks inside `if`/`while` should be one line (a function call).
- *Do One Thing.* A function does one thing if all its statements are at one level of abstraction below its name.
- *One Level of Abstraction per Function*, read top-to-bottom via **The Stepdown Rule** ("To do A, we do B, then C…").
- *Arguments:* ideal count is 0 (niladic) > 1 (monadic) > 2 (dyadic); 3 (triadic) should be avoided; more → wrap in an **Argument Object**. **Flag arguments are ugly** — a boolean parameter means the function does more than one thing; split it.
- *No Side Effects;* obey **Command Query Separation** (a function either does something or answers something, never both); *Prefer Exceptions to Returning Error Codes;* **Extract Try/Catch Blocks**; **DRY — Don't Repeat Yourself**.

**Comments (Ch4).** *Comments are, at best, a necessary evil* — they compensate for failure to express intent in code. The best comment is the one you found a way not to write (replace it with a well-named function or variable). Good: legal, informative, intent, warning-of-consequences, TODO, amplification, public-API Javadoc. Bad: redundant, misleading, mandated, journal, noise, commented-out code (delete it — source control remembers).

**Formatting (Ch5).** Code is read like a newspaper (**The Newspaper Metaphor**): high-level at top, details below. Use **vertical distance** — declare variables near use, keep dependent functions close, vertically order by call. Files ~200 lines typical, 500 max. Adopt **team rules** over personal preference.

**Objects vs Data Structures (Ch6).** **Data/Object Anti-Symmetry**: *objects* hide data and expose behavior; *data structures* expose data and have no behavior. OO and procedural are complementary opposites — each makes the other's hard changes easy. Obey **The Law of Demeter** (talk to friends, not strangers); avoid **train wrecks** (`a.getB().getC().doD()`).

**Error Handling (Ch7).** Use exceptions, not return codes; write the try-catch-finally first; prefer unchecked exceptions (checked exceptions break Open-Closed); provide context with exceptions; **Don't Return Null, Don't Pass Null** — use the **Special Case Pattern** or empty collections instead.

**Boundaries (Ch8).** Encapsulate third-party interfaces behind your own; write **Learning Tests** (tests that pin third-party behavior — "better than free"); for code that doesn't exist yet, define the interface you *wish* you had and adapt later.

**Unit Tests (Ch9).** **The Three Laws of TDD**: (1) write no production code until you have a failing test; (2) write no more of a test than is sufficient to fail; (3) write no more production code than is sufficient to pass. Keep tests clean — *test code is as important as production code*. Tests must be **F.I.R.S.T.**: Fast, Independent, Repeatable, Self-Validating, Timely. One concept per test.

**Classes (Ch10).** Classes should be small — measured by *responsibilities*, not lines. **Single Responsibility Principle (SRP)**: one reason to change. Maintaining **cohesion** naturally yields many small classes. Organize for change (**Open-Closed Principle**) and isolate from change via **Dependency Inversion (DIP)**.

**Systems (Ch11).** Separate *constructing* the system from *using* it (move construction to `main` / **Abstract Factory** / **Dependency Injection**). Systems grow like cities; defer decisions to the last responsible moment; test-drive the architecture.

**Emergence (Ch12) — Kent Beck's Four Rules of Simple Design**, in priority order: a design is simple if it (1) **runs all the tests**, (2) contains **no duplication**, (3) **expresses the intent** of the programmer, (4) **minimizes** the number of classes and methods. Rules 2–4 are refactoring.

**Concurrency (Ch13 + App A).** Concurrency decouples *what* from *when*. Keep concurrency code separate (SRP); limit the scope of shared data; prefer copies; keep synchronized sections small; know your library and execution models (Producer-Consumer, Readers-Writers, Dining Philosophers). Treat spurious test failures as real threading bugs.

**The capstone (Ch17).** The whole book distilled into a numbered catalog of **Smells and Heuristics** (C / E / F / G / N / T / J codes) — use it as a code-review checklist.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-clean-code.md) | Clean Code | Boy Scout Rule, LeBlanc's Law, what is clean code |
| [ch02](chapters/ch02-meaningful-names.md) | Meaningful Names | intention-revealing, no encodings, one word per concept |
| [ch03](chapters/ch03-functions.md) | Functions | Small!, Do One Thing, Stepdown Rule, argument rules, CQS |
| [ch04](chapters/ch04-comments.md) | Comments | good vs bad comments, prefer code over comments |
| [ch05](chapters/ch05-formatting.md) | Formatting | Newspaper Metaphor, vertical distance, team rules |
| [ch06](chapters/ch06-objects-and-data-structures.md) | Objects & Data Structures | Data/Object Anti-Symmetry, Law of Demeter, train wrecks |
| [ch07](chapters/ch07-error-handling.md) | Error Handling | exceptions over codes, Special Case Pattern, no null |
| [ch08](chapters/ch08-boundaries.md) | Boundaries | wrap third-party code, Learning Tests, Adapter |
| [ch09](chapters/ch09-unit-tests.md) | Unit Tests | Three Laws of TDD, F.I.R.S.T., clean tests |
| [ch10](chapters/ch10-classes.md) | Classes | SRP, cohesion, OCP, DIP, small classes |
| [ch11](chapters/ch11-systems.md) | Systems | separate construction from use, DI, Abstract Factory |
| [ch12](chapters/ch12-emergence.md) | Emergence | Kent Beck's Four Rules of Simple Design |
| [ch13](chapters/ch13-concurrency.md) | Concurrency | defense principles, execution models, testing threads |
| [ch14](chapters/ch14-successive-refinement.md) | Successive Refinement | make it work then make it right (Args case study) |
| [ch15](chapters/ch15-junit-internals.md) | JUnit Internals | Boy Scout Rule applied (ComparisonCompactor) |
| [ch16](chapters/ch16-refactoring-serialdate.md) | Refactoring SerialDate | first make it work, then make it right |
| [ch17](chapters/ch17-smells-and-heuristics.md) | Smells and Heuristics | the 60-item review catalog (C/E/F/G/J/N/T) |
| [ch18](chapters/ch18-appendix-a-concurrency-ii.md) | Appendix A: Concurrency II | locking, deadlock conditions, atomicity, worked examples |

## Topic Index

- **Abstract Factory / construction** → ch11
- **Argument objects / flag arguments** → ch03
- **Boy Scout Rule** → ch01, ch15
- **Boundaries / third-party code** → ch08
- **Classes / cohesion / small classes** → ch10
- **Code smells / heuristics (checklist)** → ch17
- **Command Query Separation** → ch03
- **Comments** → ch04
- **Concurrency / threads / locking** → ch13, ch18
- **Deadlock / atomicity** → ch18
- **Dependency Injection / Inversion (DIP)** → ch10, ch11
- **DRY / duplication** → ch03, ch12, ch17
- **Error handling / exceptions** → ch07
- **F.I.R.S.T.** → ch09
- **Formatting / vertical distance** → ch05
- **Functions (size, one thing)** → ch03
- **Kent Beck's Four Rules of Simple Design** → ch12
- **Law of Demeter / train wrecks** → ch06
- **Learning Tests** → ch08
- **Naming** → ch02, ch17(N)
- **Newspaper Metaphor** → ch05
- **Null handling / Special Case Pattern** → ch07
- **Objects vs data structures** → ch06
- **Open-Closed Principle (OCP)** → ch07, ch10
- **Refactoring (case studies)** → ch14, ch15, ch16
- **Single Responsibility Principle (SRP)** → ch10, ch13
- **Stepdown Rule / abstraction levels** → ch03
- **Successive refinement** → ch14
- **Systems / architecture** → ch11
- **TDD / Three Laws** → ch09
- **Unit tests** → ch09

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — concrete techniques and refactorings
- [cheatsheet.md](cheatsheet.md) — one-page quick reference + pre-commit checklist

---

## Scope & Limits

This skill covers the book's content (Java-flavored examples; principles are language-agnostic). It is a knowledge base, not a linter — for mechanical enforcement combine with project tools (formatters, static analysis, coverage). For construction practice beyond this book, see the companion `decomplexify` skill (Code Complete). For topics outside the book, ask the agent directly.
