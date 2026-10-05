---
description: Analyze Phel source for clean-code issues and phel-pdo rule compliance (.claude/rules/*.md)
argument-hint: "[file-or-directory]"
context: fork
agent: Explore
allowed-tools: "Read, Glob, Grep"
---

# Refactor Check

Read and analyze the specified file(s) from `$ARGUMENTS` (default: `src/pdo.phel` + `src/pdo/statement.phel`).

phel-pdo is a thin idiomatic PDO wrapper, pure Phel, struct-based. There are no classes, no Gacela modules, no compiler phases - judge against the project rules, not OOP/SOLID.

## API Design (`.claude/rules/api-design.md`)

| Check | Rule |
|-------|------|
| One fn per method | One Phel fn per exposed PDO method, kebab-case (`lastInsertId` → `last-insert-id`) |
| Arg order | Wrapped struct first (`conn`/`stmt`), then PDO args in PHP order, then `& [optional]` |
| Optionals | Default in body via `(or x \PDO/DEFAULT)`, never overloads |
| Mutators | `execute`/`bind-value`/`set-attribute` return the wrapped struct (thread with `->`) |
| Reads | `fetch`/`fetch-all`/`row-count`/… return Phel-native data |
| Rows out | Every raw fetch routed through `row->map` (keys → keywords) |
| Params in | User maps/vectors run through `phel->php` before PDO |
| Errors | Rely on `ERRMODE_EXCEPTION`; never re-wrap `\PDOException` |
| Encapsulation | No public fn exposes raw `\PDO` / `\PDOStatement` |

## Clean Code

- **Naming**: kebab-case, intention-revealing? `defn-`/`def-` for non-public?
- **Functions**: Small? One responsibility? Threading (`->`, `->>`) where it clarifies?
- **Docstrings**: Public fns carry a terse `:doc` one-liner? Return-type tag reflects the underlying PDO type?
- **Comments**: `;` inline, `;;` standalone, `;;;` section header? No commented-out forms left behind?
- **Purity**: Pure functions only outside the PDO call sites; no globals?
- **Interop**: Boundary crossed only via `phel->php` / `php->phel`, `(php/-> (x :pdo) ...)` / `(php/-> (x :stmt) ...)`?

## Cross-File Hygiene

| Check | Rule |
|-------|------|
| Namespace | `statement.phel` opens with `(in-ns phel.pdo)` |
| Declares | New cross-file decls via `declare` in `src/pdo.phel` before `(load "pdo/statement")` |
| API tables | `README.md` connection/statement tables list every public fn |

## Output Format

```markdown
# Refactor Analysis: <file/directory>

## Summary
- **API Design Issues:** X
- **Clean Code Issues:** X
- **Cross-File Issues:** X

## Critical Issues (High Priority)
### [API] <fn> leaks raw \PDOStatement
**File:** `src/pdo/statement.phel:42`
**Problem:** ...
**Suggestion:** ...

## Moderate Issues (Medium Priority)
...

## Minor Issues (Low Priority)
...

## Recommended Refactoring Steps
1. ...
```
