---
name: refactoring
description: Improve an existing codebase safely by establishing a behaviour baseline, finding seams and moving in small reviewable steps.
---

# Refactoring: change structure without changing behaviour

- Refactoring changes structure without changing behaviour. State the behaviour that must stay fixed and establish a test or characterization baseline first.
- Work in small, reviewable steps. Separate moves from behaviour changes so a regression has one obvious cause.
- Find seams: inject a dependency, extract a pure function, or isolate I/O behind an interface. Do not rewrite the world to test one branch.
- Keep the public interface stable unless the task explicitly changes it. Update every caller in the same change.
- Delete dead code only when you can prove it is unreachable; check reflection, configuration and external consumers first.
- Run the tests after each step. If behaviour changes, stop and decide whether that change belongs in this task.
- Report the structural change, the preserved behaviour and the tests that prove it.

---

_NullByte skill pack. Original guidance for this tool; no third-party skill text is bundled._
