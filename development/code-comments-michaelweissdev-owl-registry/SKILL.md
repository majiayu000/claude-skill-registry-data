---
name: code-comments
description: >
  Write purposeful, accurate, and maintainable code comments and API documentation
  across major programming languages. Use when deciding whether to add or remove
  comments, writing public API documentation (docstrings, rustdoc, Javadoc, JSDoc,
  GoDoc), explaining non-obvious algorithms, documenting security invariants,
  or refactoring noisy, redundant comments. Do not use for README or architecture
  documents, commit messages (use conventional-commits), changelogs, or when asked
  to leave comments untouched in a mechanical refactor.
compatibility: >
  Agent Skills-compatible coding agents reading, writing, or reviewing code comments
  across Python, Rust, C/C++, Go, Java, Kotlin, TS/JS, Swift, Bash, and SQL.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "comments, documentation, docstrings, javadoc, rustdoc, jsdoc, godoc, best-practices"
  topics: "documentation, software-development"
---

# Professional Code Comments and Documentation

Code explains **what** is being done and **how**. Comments must explain **why** it is done that way, what invariants and assumptions are held, and what contracts callers must respect. Gratuitous, redundant comments create clutter and drift out of sync; missing comments on non-obvious trade-offs create maintenance hazards.

Detailed language syntax specifications and positive/negative examples:
- [Language-Specific Commenting Guides](references/language-guides.md)
- [Real-World Positive & Negative Examples](references/examples-antipatterns.md)

---

## The Golden Rules of Code Commenting

1. **Document the "Why", not the "What"**: If the code is clear, do not paraphrase it in English. Explain rationale, edge-case workarounds, performance trade-offs, and external constraints.
2. **Never lie or invent details**: Never document arguments that don't exist, claim guarantees that aren't enforced, or invent error descriptions.
3. **Public APIs require complete contracts**: Every public function, class, and interface must document preconditions, postconditions, expected inputs, return semantics, and error conditions.
4. **Highlight safety, concurrency, and security invariants**: Explicitly document lock ordering, thread safety, ownership transfer, cryptographic constraints, and input sanitization requirements.
5. **Delete obsolete or zombie comments**: When refactoring code, update or remove accompanying comments immediately. An outdated comment is worse than no comment.
6. **Prefer self-documenting code first**: If a comment explains confusing variable names or convoluted logic, refactor the code first. Use comments when the code alone cannot convey intent.

---

## 1. When to Write Comments

### REQUIRED
- **Public API Documentation**: Format according to the ecosystem standard (PEP 257 docstrings in Python, `///` in Rust, `/** ... */` JSDoc in TS/JS, `//` in Go, Javadoc in Java).
- **Non-Obvious Decisions & Workarounds**: Why a standard library function was avoided, why a specific regex was chosen, or why a sleep/retry delay is necessary.
- **Bug Fixes with Issue References**: Linking a non-intuitive condition to an issue tracker or CVE (`// Workaround for upstream issue #412: ...`).
- **Mathematical / Algorithmic References**: Citations to papers, RFCs, or formal algorithms (`// Implements RFC 7519 Section 4.1.4: ...`).
- **Invariants and Assertions**: Explaining why a condition must be true at a given point in execution.

### FORBIDDEN
- **Restating the code**: `i = i + 1; // Increment i`
- **Trivial getter/setter noise**: `/** Sets the name */ public void setName(String name)`
- **Commented-out code (Zombie Code)**: Never leave dead code blocks commented out. Git tracks history.
- **Changelogs or Author Tags in file headers**: Use version control for authorship and history.

---

## 2. Decision Matrix

| Situation | Should You Comment? | What to Write |
| :--- | :--- | :--- |
| Public library function | **YES (Mandatory)** | Purpose, parameter descriptions, return value, errors raised, minimal usage example |
| Complex regex pattern | **YES (Recommended)** | Break down pattern components and describe matched/rejected inputs |
| Workaround for external browser/OS bug | **YES (Mandatory)** | Link to bug report, affected versions, and why the workaround works |
| Standard CRUD assignment | **NO (Forbidden)** | Clean variable and function names are sufficient |
| Dead/unused code | **NO (Delete it)** | Delete entirely; rely on git history |

---

## 3. High-Quality Comment Examples

### Explaining a Workaround (Good)
```python
# The upstream payment gateway returns HTTP 200 with an empty body when a card is declined
# instead of HTTP 402/400. We must explicitly parse the 'gateway_status' field in the JSON payload
# to detect declined charges. See vendor issue ticket #8841.
if response.status_code == 200 and payload.get("gateway_status") == "DECLINED":
    raise PaymentDeclinedError(payload.get("decline_reason", "Card declined"))
```

### Explaining Invariants (Good)
```rust
// SAFETY INVARIANT: The ring buffer capacity is guaranteed to be a power of two
// on initialization. We can therefore use bitwise AND (`index & mask`) instead of
// an expensive modulo operator (`index % capacity`) in this tight packet processing loop.
let slot = self.write_index & self.mask;
```

---

## 4. Multi-Language Quick Reference

| Language | Line Comment | Block Comment | Documentation Comment | Standard Tool |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | `#` | N/A | `""" docstring """` | Sphinx, MkDocs, PEP 257 |
| **Rust** | `//` | `/* */` | `///` (outer), `//!` (inner/module) | `cargo doc` (rustdoc) |
| **TypeScript / JS**| `//` | `/* */` | `/** ... */` | TSDoc, JSDoc |
| **Go** | `//` | `/* */` | `// SymbolName ...` preceding declaration | `go doc`, pkg.go.dev |
| **C / C++** | `//` | `/* */` | `/** ... */` or `///` | Doxygen |
| **Java** | `//` | `/* */` | `/** ... */` | Javadoc |
| **Kotlin** | `//` | `/* */` | `/** ... */` | KDoc, Dokka |
| **Swift** | `//` | `/* */` | `///` or `/** ... */` | DocC |
| **Bash** | `#` | N/A | `# Header / Function doc` | ShellCheck |
| **SQL** | `--` | `/* */` | `-- Header / Migration explanation` | pg_dump / schema tools |

---

## 5. Comments You Must Not Remove or Reword

Some comments are machine-read. Treat them as code and keep them unless you understand and change the behavior on purpose:

- Linter and type-checker directives: `# noqa`, `# type: ignore[code]`, `# pragma: no cover`, `// eslint-disable-next-line`, `// @ts-expect-error`, `#[allow(...)]` attributes with their justification, `// nolint`.
- Tool and build directives: `//go:generate`, `//go:build`, `// +build`, `#!shebang`, `# -*- coding -*-`, `/// <reference>`, `<!-- prettier-ignore -->`.
- Legal and provenance: license headers, `SPDX-License-Identifier`, copyright lines, required attribution.
- Safety documentation: Rust `// SAFETY:` comments and `# Safety`, `# Errors`, `# Panics` rustdoc sections; documented lock ordering.

Rule for suppressions: every suppression carries a reason and, when it is a workaround, a link to the issue (`# type: ignore[arg-type]  # upstream stubs miss Optional, see #123`). A bare suppression is a defect to flag, not noise to delete.

## 6. Pitfalls and Judgment Calls

| Situation | Wrong move | Better move |
| :--- | :--- | :--- |
| Docstring repeats types already in annotations | Maintain types in two places and let them drift | Keep types in the signature; describe meaning, units, and constraints in prose |
| `TODO` with no owner or reference | Permanent clutter | `TODO(#412): remove after API v2 rollout` or file an issue and delete the note |
| Comment states a guarantee the code does not enforce | Reader trusts a lie | Make the code enforce it (assert, type) or soften the comment |
| Mass-deleting comments during an unrelated change | Noisy diff, lost context | Touch only comments next to the lines you change |
| Documenting secrets, internal hostnames, or customer data in comments | Leak via source distribution | Reference the configuration source instead |
| Translating code into prose on AI-generated patches | Redundant comments that nobody maintains | Delete restating comments; keep rationale only |
| Public API docs without error behavior | Callers cannot handle failure | Add errors/panics/side effects and thread-safety notes |
| Example in a doc comment that no longer compiles | Misleads and breaks doc tests | Use runnable doc tests where the language supports them (`cargo test --doc`, Python `doctest`, Go `Example` functions) |

Diagnose a suspect comment by asking: could a reader derive this from the code in under ten seconds (delete it), is it true today (fix or delete), and does it tell the reader something the code cannot, such as why, a constraint, or a consequence (keep it).

## 7. Verification Checklist

- [ ] All public APIs have standard doc comments matching language conventions.
- [ ] No comments merely rephrase the syntax in natural language.
- [ ] No commented-out blocks of dead code exist.
- [ ] Parameter names and types in docstrings match the actual code signature exactly.
- [ ] Workarounds, security constraints, and safety assumptions are explicitly documented.
