---
name: metzify
description: "Knowledge base from \"99 Bottles of OOP\" (Milk/Ruby edition) by Sandi Metz, Katrina Owen & TJ Stankus. Use when applying Metz's frameworks for refactoring, finding the right abstraction, the Flocking Rules, Shameless Green, replacing conditionals with polymorphism, factories, code smells, or test design — while coding, studying the book, or referencing its concepts."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic, framework name, or chapter number]
---

# 99 Bottles of OOP (Milk / Ruby edition)
**Authors**: Sandi Metz, Katrina Owen, TJ Stankus | **Pages**: ~297 | **Chapters**: 9 | **Generated**: 2026-06-07

## How to Use This Skill
- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `flocking rules`, `shameless green`, `factories`, `code smells`, `LSP`, `testing`; I find and read the relevant chapter.
- **With a chapter** — ask for `ch06`; I load that chapter file.
- **Browse** — ask "what chapters do you have?" for the full index.

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**The book's one big arc**: *Shameless Green → wait for a change request → open the code → separate responsibilities → replace conditionals with polymorphism → add the feature (now trivial) → choose a factory → reap the benefits in your tests.* It's a single refactoring of the "99 Bottles" song, end to end.

**Shameless Green** — Reach green the fastest, simplest way, prioritizing *understandability over changeability*. Tolerate duplication; name nothing speculatively. It feels embarrassing and "not OO," and that's correct: **it is cheaper to manage temporary duplication than to recover from the wrong abstraction.** Don't abstract until the code *insists* on it.

**Judge code by value/cost, not taste** — Good code = highest value for lowest cost. Ask: (1) hard to write? (2) hard to understand? (3) expensive to change? #2 always applies. Replace opinion with facts via metrics: **SLOC** (volume), **Cyclomatic Complexity** (paths + minimum tests), **ABC** via **Flog** (cognitive size).

**The Flocking Rules** (how to find abstractions) —
1. Select the things that are **most alike**.
2. Find the **smallest difference** between them.
3. Make the **simplest change** to remove that difference.
Change one line at a time, run tests after each, undo on red. This is the engine that turns duplication into the right abstraction.

**Open/Closed Principle + Kent Beck's rule** — "Make the change easy, then make the easy change." When a requirement arrives, FIRST refactor the existing code to be *open* to it (add nothing new yet), THEN add the feature. Never conflate the two steps.

**Name by meaning, not implementation** — Name methods after *what they represent in the domain*, never what they do right now. The right name is one level of abstraction above the instances — the "column header" of a Number→Value table (`beverage`, not `milk`). A name tied to implementation rots the moment the implementation changes.

**Horizontal Refactoring** — Remove differences across the parallel branches of a conditional until they're identical, then collapse to one template. Finish the horizontal sweep before veering off on a vertical tangent. Pause only at **Stable Landing Points** (green, consistently shaped). Never refactor under red.

**Replace Conditional with Polymorphism** — A class dominated by identically-shaped conditionals on one value is a Switch Statement smell. Extract a subclass per special value, push each branch's body into its class, and select with a **Factory**. Conditionals vanish; the code becomes open to new variants.

**The Factory Continuum** — From least to most open: `case` statement → metaprogrammed convention (`const_get`) → key/value hash → dispersed `handles?` list → self-registering registry → `inherited`-hook auto-registration. Pick by how much *openness* you need vs. simplicity and coupling. "Factories are where conditionals go to die."

**Programming Aesthetic** (when to voluntarily improve working code) — Refactor when: code is *closed* to an incoming requirement; a method description contains **"and"** (SRP smell); a method has a **blank line** (topic change); an instance method *names a concrete class* (inject it); a method's only use of a param is *converting it* (move upstream); a **Demeter chain** appears (missing abstraction). Otherwise — it works and none fire — **walk away**; opportunity cost is real.

**Tests reveal design** — A hard-to-write test is a *design smell*: fix the code, not the test. Test **behavior, not implementation** (never assert one method equals another). Choose test scope by **visibility**: injected (visible) dependencies get a fake; internal (invisible) ones are tested through their enclosing unit. Omit a class's own unit test only if it's small + simple + invisible + single-context (all four). The factory always gets its own test.

**Core anti-patterns** (Ch 1) — *Incomprehensibly Concise* (logic crammed into strings), *Speculatively General* (indirection guarding against imagined change), *Concretely Abstract* (tiny DRY methods named after what they do now). All three cost more than Shameless Green.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-rediscovering-simplicity.md) | Rediscovering Simplicity | Shameless Green, Concrete↔Abstract Continuum, Value/Cost questions, code metrics |
| [ch02](chapters/ch02-test-driving-shameless-green.md) | Test Driving Shameless Green | Red/Green/Refactor, Green Bar Patterns, Horizontal vs Vertical Path |
| [ch03](chapters/ch03-unearthing-concepts.md) | Unearthing Concepts | Open/Closed Principle, The Flocking Rules, Gradual Cutover, Code Smells |
| [ch04](chapters/ch04-practicing-horizontal-refactoring.md) | Practicing Horizontal Refactoring | Horizontal Refactoring, Liskov Substitution, Meaningful Defaults, Stable Landing Points |
| [ch05](chapters/ch05-separating-responsibilities.md) | Separating Responsibilities | Code Smell Audit, Extract Class, Squint Test, Primitive Obsession |
| [ch06](chapters/ch06-achieving-openness.md) | Achieving Openness | Replace Conditional with Polymorphism, Factory Method, Data Clump, LSP guard |
| [ch07](chapters/ch07-manufacturing-intelligence.md) | Manufacturing Intelligence | Factory Continuum, `handles?` predicate, `inherited` auto-registration |
| [ch08](chapters/ch08-developing-a-programming-aesthetic.md) | Developing a Programming Aesthetic | Programming Aesthetic, Open/Closed Flowchart, Extract-and-Inject |
| [ch09](chapters/ch09-reaping-the-benefits-of-design.md) | Reaping the Benefits of Design | Tests-Reveal-Design, Visibility-Driven Test Strategy, Unit-Test Omission |

## Topic Index
- **ABC / Flog / metrics** → ch01
- **Abstraction (finding the right one)** → ch01, ch03, ch04
- **Code smells** → ch03, ch05
- **DRY / duplication** → ch01, ch02
- **Extract Class** → ch05
- **Factory / Factory Continuum** → ch06, ch07
- **Flocking Rules** → ch03
- **Gradual Cutover / changing signatures** → ch03, ch04
- **Horizontal Refactoring** → ch04, ch02
- **Liskov Substitution Principle** → ch04, ch05, ch06
- **Naming** → ch01, ch04
- **Open/Closed Principle** → ch03, ch06, ch08
- **Polymorphism (replacing conditionals)** → ch06
- **Primitive Obsession** → ch05
- **Programming Aesthetic / when to refactor** → ch08
- **Red/Green/Refactor / TDD** → ch02
- **Shameless Green** → ch01, ch02
- **Squint Test** → ch05
- **Testing (behavior, visibility, fakes)** → ch09, ch02
- **Value vs. cost of code** → ch01

## Supporting Files
- [glossary.md](glossary.md) — all key terms with definitions and chapter refs
- [patterns.md](patterns.md) — every technique with when/how/trade-offs
- [cheatsheet.md](cheatsheet.md) — the Flocking Rules, Factory Continuum, refactor-decision checklist on one page

---

## Scope & Limits
This skill covers the book's content (Ruby examples). The lessons are language-agnostic but the code is Ruby. For applying these to your own codebase, pair with project tooling and tests. For OO topics beyond this book (e.g. dependency management depth), see Metz's *Practical Object-Oriented Design* separately.
