---
name: sqlglot-python
description: Use for writing, reviewing, debugging, or testing Python code that parses, inspects, transforms, builds, qualifies, optimizes, formats, or transpiles SQL with SQLGlot. Trigger on parse_one/parse, sqlglot expressions and scopes, dialect conversion, AST traversal, lineage, qualification, schema-aware rewrites, and unsupported translation. Do not use for executing SQL, database query tuning, regex-only text edits, ORM query construction, SQLFluff lint configuration, or generic SQL unrelated to SQLGlot.
argument-hint: "[SQLGlot parse, AST, transform, dialect, or transpilation task]"
---

# SQLGlot Python

Produce dialect-explicit SQLGlot code that treats SQL as a typed syntax tree,
preserves caller ownership, separates syntactic rewrite from semantic proof, and
fails visibly when translation is unsupported.

## Boundary

Use this skill when the implementation imports SQLGlot or explicitly needs its
parser/transpiler/AST. SQLGlot does not execute against the target database and
is not an authorization sandbox, query optimizer for physical performance, or
substitute for database parameters. Use the database's own tooling for runtime
plans and execution semantics.

## Know the objects before editing

| Object | Meaning | Use it for |
|---|---|---|
| Dialect | Parser and generator rules for a SQL family. | Interpreting source tokens and emitting target syntax. |
| `Expression` | One AST node with named child arguments and parent/tree relationships. | Semantic inspection, construction, and transformation. |
| Statement expression | Root node such as `Select`, `Insert`, `Create`, or `Command`. | Classifying allowed jobs and preserving statement boundaries. |
| `Identifier` | A name whose quoting and normalization depend on dialect. | Tables, columns, aliases, and other identifiers—not data values. |
| `Literal` / placeholder node | A typed SQL value or bind marker in the AST. | Values; keep runtime user data parameterized by the executor. |
| Scope | A query-resolution context for sources, projections, subqueries, and CTEs. | Analysis that cannot be correct from local node search alone. |
| Schema mapping | Table/column type information supplied by the caller. | Qualification, star expansion, type annotation, and type-sensitive rewrites. |

`parse_one` returns one root expression; `parse` preserves a multi-statement
sequence. `.sql(dialect=...)` generates text from an AST. `transpile` combines
source parsing and target generation, but syntactic success is not proof of
equivalent behavior in the target engine. Expression methods can mutate nodes
or return changed trees; copy a caller-owned tree before modifying it unless
in-place mutation is the declared API. Read [the AST and dialect
model](references/object-model.md).

## Ordered workflow

1. Recover the contract: one or many statements, known source dialect, target
   dialect, allowed statement/node classes, required semantic preservation,
   available schema, output formatting, and error policy.
2. Pass `read=` whenever the source dialect is known. Do not let the SQLGlot
   superset dialect guess vendor syntax.
3. Parse once. Reject parse errors and disallowed roots before traversing or
   transforming.
4. Use `Expression` classes, `find_all`, scopes, builders, or `transform`; never
   use regex/string replacement for structural SQL edits.
5. Supply schema and qualify/type-annotate only when the transformation needs
   name or type resolution. Do not invent missing catalog facts.
6. Copy before changing a tree whose original must remain available.
7. Generate with an explicit target dialect and a strict unsupported-feature
   policy. Preserve statement count and ordering.
8. Reparse generated SQL in the target dialect, then run target-engine tests
   when semantic equivalence matters.

## Choose by intent

| Need | Use | Required guard |
|---|---|---|
| Parse exactly one known statement | `parse_one(sql, read=...)` | Establish that a one-statement boundary is intended. |
| Preserve a script's statements | `parse(sql, read=...)` | Validate every root; do not inspect only the first. |
| Find local syntax nodes | `find` / `find_all` with `exp` classes | Local traversal is not column resolution. |
| Resolve sources/columns across CTEs/subqueries | Scope/optimizer qualification utilities | Supply schema/catalog facts where required. |
| Rewrite nodes recursively | `Expression.transform` or explicit AST replacement | Preserve parentage and copy policy; test nested cases. |
| Construct SQL | `sqlglot.exp` nodes/builders | Keep identifiers distinct from literals and bind parameters. |
| Translate dialects | `transpile(read=..., write=...)` or parse then `.sql(dialect=...)` | Raise/report unsupported constructs; validate target semantics. |
| Canonical logical AST | supported optimizer entry point with schema | Not physical query-performance tuning. |

Read [the operation map](references/operations.md) before choosing parsing,
building, scope analysis, transformation, optimization, or generation APIs.

## Canonical strict transpilation

```python
import sqlglot
from sqlglot import ErrorLevel


def transpile_script(sql: str, source: str, target: str) -> list[str]:
    if not source or not target:
        raise ValueError("source and target dialects are required")
    return sqlglot.transpile(
        sql,
        read=source,
        write=target,
        unsupported_level=ErrorLevel.RAISE,
        pretty=True,
    )
```

The list preserves the possibility of multiple statements and rejects known
unsupported generation rather than warning and emitting a degraded query.
Callers that accept only one statement must check `len(result) == 1`. Reparse
each output with `read=target`; execute representative queries in the target
engine before claiming semantic equivalence.

## Canonical structural inspection

```python
from sqlglot import exp, parse_one


def selected_columns(sql: str, dialect: str) -> tuple[str, ...]:
    tree = parse_one(sql, read=dialect)
    if not isinstance(tree, exp.Select):
        raise ValueError(f"expected SELECT, got {type(tree).__name__}")
    return tuple(node.sql(dialect=dialect) for node in tree.expressions)
```

This inspects projection expressions rather than regex-matching commas or
column-like tokens. It does not claim to resolve `*`, aliases, or source columns;
that requires scopes and often schema qualification.

## High-risk rules

### Dialects and semantics

- Always specify the source dialect when known and target dialect when
  generating. Identifier case, quoting, function names, date arithmetic, casts,
  arrays, JSON, and null behavior can differ.
- Treat unsupported warnings as failures for correctness-critical translation.
  A successful parse means the syntax was represented, not that every target
  construct has an equivalent.
- Type-sensitive transpilation and optimization need schema information. If the
  catalog is unavailable, preserve the construct or return an uncertainty;
  never fabricate column types.
- SQLGlot optimization is logical canonicalization, not target physical-plan
  tuning. Benchmark or inspect the actual engine for performance claims.

### AST mutation and resolution

- Match nodes by class and semantic arguments, not `str(node)`. Preserve
  comments and formatting only to the degree the selected generator supports;
  regenerated SQL is not a textual round trip.
- Copy before mutation when a function promises not to alter its input. Test
  nested subqueries, CTE shadowing, aliases, quoted identifiers, stars, and
  correlated references.
- `find_all(exp.Column)` finds syntax nodes but does not resolve which table
  supplies them. Use scope/qualification analysis for lineage or authorization.
- Construct identifiers with identifier helpers/nodes and values with literals
  or executor placeholders. Never turn untrusted text into an expression by
  parsing it merely to avoid quoting.

### Security boundary

Parsing SQL does not make it safe to execute. If only read-only queries are
allowed, inspect every parsed statement and all prohibited node classes, reject
commands the parser represents generically, enforce database credentials and
resource limits, and bind data values at execution. Treat AST allowlisting as
defense in depth, not the sole authorization layer.

Run [the installed-API inspector](scripts/inspect_sqlglot.py), read [version and API
grounding](references/version-grounding.md), then apply [the AST verification
matrix](references/testing.md).

## Completion gate

Do not declare completion until source and target dialects are explicit or a
documented unknown branch exists; multi-statement input cannot bypass checks;
allowed root/node classes are enforced; mutations honor ownership; identifiers
and values remain distinct; schema-dependent transforms have real schema;
unsupported generation is surfaced; target output reparses; nested/quoted/CTE
fixtures pass; and semantic or performance claims are verified in the target
database rather than inferred from SQLGlot alone.

## References

- [AST and dialect model](references/object-model.md)
- [Operation map](references/operations.md)
- [Version and API grounding](references/version-grounding.md)
- [Testing SQLGlot transformations](references/testing.md)
