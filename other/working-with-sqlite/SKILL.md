---
name: working-with-sqlite
kind: skill
status: ready
provenance:
  principles:
  - P049
  - P022
  - P048
  - P050
  - P029
  - P042
  claims:
  - C00749
  - C00750
  - C00766
  - C00826
  - C00791
  - C00877
  - C00810
  - C00864
  - C00779
  - C00821
  - C00832
  - C00857
  evidence:
  - E00194
  - E00195
  - E00200
  - E00218
  - E00203
  - E00241
  - E00209
  - E00235
  - E00202
  - E00217
  - E00222
  - E00230
  source_anchors:
  - 9aa0ce19c36d-c0000
  - 9aa0ce19c36d-c0002
  - 9aa0ce19c36d-c0001
  - 9aa0ce19c36d-c0003
  authored_from_digest: 123cba924f394f0cb5c21df0c7e097045729311e37d4533aff93693797893184
---

# Working with SQLite

## Purpose

Apply SQLite's embedded, single-file, dynamically-typed model correctly — storage classes and type affinity, ROWID keys, NULL semantics, joins, and where SQLite fits.

## When to use

When choosing, designing for, or writing SQL against SQLite.

## Procedure

1. Reach for SQLite as an embedded, in-process, zero-configuration, single-file relational engine for small-to-medium applications; it is not a universal drop-in for a large-scale server RDBMS. (P049)
2. Understand storage classes and type affinity - SQLite has five storage classes, a column may hold mixed classes across rows, sort order is NULL then numbers then TEXT then BLOB, and each column has NUMERIC/INTEGER/TEXT/NONE affinity derived from its declared type (an unrecognized type defaults to NUMERIC, no type gives NONE). (P022)
3. Declaring a column INTEGER PRIMARY KEY makes it an alias for the table's 64-bit ROWID with auto-generated keys and is the one column whose type is enforced; default ROWIDs may be recycled and non-monotonic after deletes, so add AUTOINCREMENT only when the application truly needs never-reused, strictly increasing keys. (P048)
4. Handle NULL deliberately - NULL is the absence of a value (not zero, empty string, true, or false); test it with IS NULL / IS NOT NULL (never = NULL), expect it to propagate through expressions and three-valued logic, know that it is dropped by WHERE and ignored by aggregates, and use COALESCE to supply defaults in nullable expressions. (P050)
5. Prefer explicit JOIN ... ON syntax with table-qualified column names, avoid NATURAL JOIN (whose results silently change when columns are added or removed), and remember SQLite implements no RIGHT or FULL OUTER JOIN - rewrite them with a reversed LEFT JOIN or compound queries. (P029)
6. Use subqueries and compound queries knowing relational closure lets operations nest; a correlated subquery re-evaluates per outer row while an uncorrelated one runs once; compound queries (UNION/INTERSECT/EXCEPT) require equal column counts and a single trailing ORDER BY; UNION removes duplicates while UNION ALL keeps them; and pushing aggregation into a subquery before a join can cut the rows the join must match. (P042)

## Grounding

Distilled (no verbatim) from this package's principles (P049, P022, P048, P050, P029, P042) and their anchored claims/evidence. Verify version-specific PostgreSQL or SQLite syntax and behaviour against current official documentation.
