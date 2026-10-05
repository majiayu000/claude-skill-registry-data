---
name: martin-fowler-code-smells
type: reference
description: Reference for Martin Fowler's 24 code smells (Refactoring, 2nd ed. 2018). ALWAYS read before reviewing code quality, planning refactors, or cleaning up code, to identify smells and their fixes.
---

The 24 code smells from Martin Fowler's Refactoring (2nd edition, 2018). Each smell is a labelled heuristic that suggests refactoring — a judgement call, never a hard violation.

### Using This Baseline

- **The repo overrides**: A documented repo standard always wins; where it endorses something a smell would flag, suppress the smell.
- **Always a judgement call**: Each smell is a heuristic, never a hard violation. Skip anything a linter/formatter already enforces.
- **Match the smell to the change**: Match the smell to the change, not the whole codebase; only flag what is relevant to the diff or target files.

### The 24 Smells (2018, 2nd edition)

1. **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → Rename Function/Variable/Field; if no honest name comes, the design is murky.
2. **Duplicated Code** — the same logic shape appears in more than one place. → Extract Function; pull up to a shared module; Slide Statements then Extract.
3. **Long Function** — a function that does too much, often flagged by a felt need to comment a section. → Extract Function; Replace Temp with Query; Introduce Parameter Object; Decompose Conditional.
4. **Long Parameter List** — a function takes many params that travel together. → Introduce Parameter Object; Preserve Whole Object; Replace Parameter with Query.
5. **Global Data** — mutable state accessible from anywhere. → Encapsulate Variable; move into a module/class with controlled access.
6. **Mutable Data** — data that can change in ways hard to reason about. → Encapsulate Variable; make it immutable where possible; Separate Query from Modifier; Remove Setting Method.
7. **Divergent Change** — one module changes for several unrelated reasons. → Extract Class/Module so each changes for one reason.
8. **Shotgun Surgery** — one logical change forces scattered edits across many files. → Move Function/Field; Inline; gather what changes together into one module.
9. **Feature Envy** — a method that reaches into another object's data more than its own. → Move Function onto the data it envies; Extract then Move.
10. **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → Extract Class / Introduce Parameter Object.
11. **Primitive Obsession** — a primitive or string standing in for a domain concept. → Replace Primitive with Object; Replace Type Code with Subclasses or Polymorphism; Introduce Parameter Object.
12. **Repeated Switches** — the same switch/if-cascade on the same type recurs across the change. → Replace Conditional with Polymorphism, or one shared map both sites use.
13. **Loops** — explicit loops that obscure the processing pipeline. → Replace Loop with Pipeline (map/filter/reduce).
14. **Lazy Elements** — a class, function, or module that does too little to justify itself. → Inline Function / Inline Class; delete it.
15. **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → Remove the dead abstraction; Inline; Collapse Hierarchy.
16. **Temporary Field** — a field set only in certain circumstances, leaving it null/odd otherwise. → Extract Class; Introduce Special Case (Null Object); move the odd field.
17. **Message Chains** — long a.b().c().d() navigation the caller shouldn't depend on. → Hide Delegate; expose one method on the first object.
18. **Middle Man** — a class or function that mostly just delegates onward. → Remove Middle Man; Inline the delegation; call the real target direct.
19. **Insider Trading** — modules that know too much of each other's internals. → Move Function/Field; Hide Delegate; reduce coupling.
20. **Large Class** — a class doing too many things. → Extract Class; Extract Superclass/Subclass.
21. **Alternative Classes with Different Interfaces** — two classes doing the same job with different signatures. → Rename to unify; Extract Superclass; align the interfaces.
22. **Data Class** — classes with only fields and accessors, no behavior. → Encapsulate Record; Remove Setting Method; move behavior onto the data.
23. **Refused Bequest** — a subclass that ignores or overrides most of what it inherits. → Replace Inheritance with Delegation; Push Down Method/Field; Collapse Hierarchy.
24. **Comments** — comments used as deodorant for bad code. → Extract Function with an explanatory name; keep comments that explain _why_. When you see a comment, ask which smell it is masking.

### Edition Note

- Compared to the 1st edition (1999): adds Mysterious Name, Global Data, Mutable Data, Loops, Insider Trading; renames Long Method→Long Function, Switch Statements→Repeated Switches, Lazy Class→Lazy Element; drops Parallel Inheritance Hierarchies and Incomplete Library Class.
