---
name: ast-grep-cli
description: Find code by AST shape or relationships with ast-grep. Use for structural searches that text matching cannot express.
---

# ast-grep code search

Use `run` for a single-node pattern:

```bash
ast-grep run --pattern 'console.log($$$ARGS)' --lang javascript src
```

Use `scan --inline-rules` for relational or combined conditions. Check uncertain rules against a positive and a negative example with `--stdin`.

Relational `stopBy` changes the search boundary:

- `neighbor` (default) checks immediate relations.
- `end` traverses to the root for `inside` or to the leaves for `has`, including nested scopes.
- A rule-valued `stopBy` stops at a matching syntax node. That node can also match the relational rule.

For function-local queries, bound traversal so nested function bodies cannot satisfy an outer function's rule.

Single-quote shell patterns containing `$` metavariables. Use `--debug-query` with `cst`, `ast`, or `pattern` when parsing is unclear. See the [rule and CLI reference](references/rule_reference.md) for syntax and examples.
