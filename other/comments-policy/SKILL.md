---
name: comments-policy
description: Code comments — none by default; type annotations and AAA markers.
---

# Comments Policy

The guiding principle: **code should be self-documenting through clear naming**. Comments are the exception, not the rule.

---

## Core Principle — Default: No Comments

Code communicates intent through clear naming, small focused functions, and proper structure. Comments become outdated, double the maintenance burden, and often signal unclear code.

**Before adding a comment, ask:**
- Can I make the code clearer with a better name or extracted method?
- Is this explaining WHAT (fix the code) or WHY (only valid reason)?
- Is this a required type/exception annotation?
- Will this comment become outdated?

---

## When NOT to Comment

| Anti-pattern | Rule |
|---|---|
| Explaining what code does | Improve the code instead |
| Commenting bad code | Fix the code instead |
| Noise / obvious annotations | Remove them |
| Commented-out dead code | Delete it — Git history exists |
| Version-control comments | Use Git commits |
| TODO / FIXME | Create an issue tracker ticket |
| Dividers (`// === Section ===`) | Use proper class/method structure |
| Journal / attribution | Use Git blame |
| Closing brace markers (`} // end if`) | Refactor to smaller functions |

See `references/anti-patterns.md` for full before/after code examples.

---

## When to Comment

| Case | Required? | Format |
|---|---|---|
| Business rule or regulatory constraint | Yes — explains WHY | Inline comment citing the rule |
| Non-obvious algorithm with external reference | Yes — explains WHY | Inline comment with URL |
| Workaround for a known external bug | Yes — explains WHY | Inline comment with ticket reference |
| Typed collections / generics | Yes — type annotation | Native language syntax |
| Exceptions / errors thrown | Yes — type annotation | Native language syntax |
| ORM/dynamic property types | Yes — type annotation | Native language syntax |
| Complex return shapes | Yes — type annotation | Native language syntax |
| Test structure | Yes — AAA markers | `// Arrange`, `// Act`, `// Assert` |

See `references/type-annotations.md` and `references/aaa-pattern.md` for full examples.

---

## Length Rule — Brief and Direct, Never a Block

When a comment is warranted (WHY, not WHAT), it must be **short**: 1 line as the default, 2–3 only when the constraint genuinely cannot be stated in one. State the rule/workaround/reference and stop — no restating of the surrounding code, no walkthrough of alternatives considered, no multi-paragraph rationale.

Hard limit: **max 3 lines per comment, max 3 comments per contiguous block** (e.g. per config section, per function). A comment that needs more than 3 lines to justify itself belongs in an ADR (`docs/development/adrs/`) or a commit message, referenced by a single short line — not inlined. This applies everywhere, not only source code: config files (nginx, YAML, Dockerfiles), infra scripts, and templates follow the same limit.

| Anti-pattern | Fix |
|---|---|
| Multi-line header block above a config section explaining history/context | One line stating the constraint; move the rest to an ADR or commit message |
| Walking through what was tried before landing on this line | Delete — Git history already has this |
| Repeating the same WHY across several adjacent lines | State it once, near the first line it applies to |

---

## Quick Reference

```
Need to add a comment?
├─ Explaining WHAT code does?           → ❌ Improve the code instead
├─ Explaining WHY (rule/workaround)?    → ✅ Add it with context
├─ Type info the language can't express? → ✅ Required — use native syntax
├─ Exceptions / error conditions?       → ✅ Required — use native syntax
└─ Test structure?                      → ✅ Required — use AAA markers
```

---

## Language-Specific Style

Detect the project's primary language and load the corresponding section:

| Language | Load |
|----------|------|
| JavaScript / TypeScript | `sections/javascript-typescript.md` |
| Python | `sections/python.md` |
| Go | `sections/go.md` |
| PHP, Ruby, Java, C#, Rust, or other | `sections/generic.md` |

If multiple languages are present, load the section for the dominant one (most source files).

---

## Conditional Section Loading

Load relevant sections based on context — don't load all sections eagerly:

| Context | Load |
|---------|------|
| Python files in scope | `skills/shared/comments-policy/references/type-annotations.md` |
| Test files in scope (`*.test.*`, `*_test.*`, `spec/`) | `skills/shared/comments-policy/references/aaa-pattern.md` |
| Legacy code review or refactor task | `skills/shared/comments-policy/references/anti-patterns.md` |
| Greenfield development | None — core SKILL.md is sufficient |

## Reference Material (load on demand)

- `references/aaa-pattern.md` — AAA test pattern with examples
- `references/type-annotations.md` — type annotation rules by language
- `references/anti-patterns.md` — anti-pattern examples (what NOT to do)
