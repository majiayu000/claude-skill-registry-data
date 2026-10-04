---
name: jade-recipe-1.7-1.8-jdbc-odbc-bridge
description: >-
  Reviews a default sun.jdbc.odbc.JdbcOdbcDriver reference removed from the
  JDK in Java 8. Agent-mode recipe: there is no mechanical replacement, so
  this document defines the judgment call (fail fast vs. defer to config)
  and the invariant that only the literal default value may change.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-1.7-1.8-jdbc-odbc-bridge — JDBC-ODBC Bridge removal

Starting with JDK 8, `sun.jdbc.odbc.JdbcOdbcDriver` (the JDBC-ODBC Bridge) no
longer exists in the JDK. There is no drop-in replacement class — any code
that hard-codes this driver name will fail at `Class.forName` /
`DriverManager.getConnection` time on Java 8, where it previously "just
worked" for anyone with an ODBC data source configured. This recipe is agent
mode because the fix is a judgment call about failure behavior, not a
syntax rewrite.

## Scope of one task

You receive a shard contract. Edit **only** the files listed in
`editable_files`. `read_only_context` holds callers/subclasses of the
flagged class — read it to see whether any caller already supplies its own
driver (via a setter or constructor) before you decide how "load-bearing"
the default is.

## Transform

For the flagged site (`protected String driver = "sun.jdbc.odbc.JdbcOdbcDriver";`
in `DBKB.java`):

1. Confirm the field is still exactly this literal default (not already
   migrated).
2. Check `read_only_context` for every direct subclass/instantiation site of
   the owning class: does any of them call a driver-setting method (e.g.
   `setDriver(...)`) before opening a connection?
   - If **every** use site supplies its own driver, the default value is
     dead weight: replace the string literal with `null` and add a short
     comment noting the JDBC-ODBC Bridge was removed in Java 8 and a driver
     must be supplied explicitly (`FIXED`).
   - If **any** use site relies on the field's default (never calls a
     setter), do not silently swap in `null` — that turns a clear
     `ClassNotFoundException` at the old call site into a later, more
     confusing `NullPointerException` or silent no-op elsewhere. Report
     `NEEDS_REVIEW` and leave the code as-is, naming the relying call site(s)
     so a human can decide on a real replacement driver.
3. Never invent a "compatible" driver class name — none exists. Do not guess
   a vendor JDBC driver to substitute; that is a deployment decision, not
   something this recipe can determine from the source tree alone.

## When NOT to transform (report SKIPPED)

- The field no longer holds the removed driver string (already migrated by
  a prior run) — `SKIPPED`.

## Invariants

- No edit outside `editable_files`.
- No public signature changes — this rule is `body-local`; the field keeps
  its declared type (`String`) and the owning class's public API is
  untouched either way.
- Never fabricate a "fixed" status by picking an arbitrary substitute driver
  class — if the safe answer is "a human must choose the real driver",
  report `NEEDS_REVIEW`, not `FIXED`.

## Status to report

| status | when |
|---|---|
| `FIXED` | every use site already supplies its own driver; default literal safely nulled with an explanatory comment |
| `NEEDS_REVIEW` | at least one use site relies on the default; left as-is, relying call site(s) named in the report |
| `SKIPPED` | the flagged literal is no longer present (already migrated) |
| `FAILED` | file unreadable, or the flagged expression is not present |
