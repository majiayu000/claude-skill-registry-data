---
name: scope-guard
description: >
  What dualdb is allowed to change, and how that is enforced mechanically. Use
  before writing any patch, when a change feels like an improvement rather than a
  port, when the guard rejects a unit, or when adding a forbidden-change detector.
  The guard is the difference between this tool and a general coding agent.
---

# Scope guard

Build it early, keep it on by default. Its strongest assertion is the tool's core
promise, and that promise is a checked number rather than a hope:

> SQL Server code paths: **0 bytes changed** across N units.

## When to use

Before writing any patch; when deciding whether a change is in scope; when the
guard rejects a unit; when adding a detector.

## Decision procedure

Every patch is validated before it is applied, and the immutability pass runs
again **after** apply.

1. **File allow-list.** The file must appear in `inventory.json` as containing a
   finding, or be a class the tool may create: provider factory, dialect helper,
   provider-keyed SQL, generated PostgreSQL DDL, config, generated tests.
2. **Hunk-to-finding mapping.** Every changed hunk maps to at least one finding id
   and at least one rule id. An unmapped hunk is rejected.
3. **Forbidden-change detectors.** Reject hunks that change a project's TFM
   without a database reason; convert `packages.config` to `PackageReference`;
   rename or move types; modify method signatures outside data-access types; touch
   `.aspx`/`.ascx`/`.cshtml` markup; alter arithmetic, comparison or control flow
   in non-data-access code; reformat whole files; reorder `using` directives
   wholesale; delete tests.
4. **Diff budget.** Per-file and per-run line ceilings, with a loud warning at
   80%. Prevents runaway rewrites.
5. **Audit line.** Every applied hunk gets a row in `changeset.json`: file, range,
   findings, rules, decision, confidence, source.
6. **SQL Server path immutability** - the one that matters most.

## The immutability check

For every `add-pg-alternate` unit:

- The pre-conversion unit body and the post-conversion `<Name>_SqlServer` body,
  normalised only by stripping common leading indentation, must be **identical**.
  Any difference at all rejects the whole unit.
- The public signature of the original method is unchanged: name, accessibility,
  return type, parameter names, types, order, defaults, modifiers, attributes.
- The dispatcher body matches the approved template **exactly** - a single
  provider test returning one of two calls. No logic, no logging, no null checks,
  no try/catch.
- No caller of the unit appears in the diff.

For `add-pg-file` and `.sql` additions: the original file's bytes are unchanged,
except for adding a `partial` keyword where that was the chosen mechanism.

## The guardrails, as named checks

| Guardrail | Check |
|---|---|
| R1 SQL Server behaviour unchanged | `sqlserver-immutability` - fatal, pre and post |
| R2 no business-logic change | `no-logic-change` - detectors plus unit purity |
| R3 no schema redesign | `no-schema-redesign` - unless `allow_schema_changes` |
| R4 no unflagged lossy mapping | `lossy-mapping-flagged` - needs a risk entry |
| R5 no credentials in source | `no-secrets` - placeholders only, never echo a value |
| R6 parameterize everything | `parameterized` - in generated alternates |
| R7 provider resolved once | `no-provider-sniffing` |
| R9 no silent approximation | `no-equivalent-flagged` - needs 2-3 options |
| R10 deterministic, no reformatting | `no-reformat` plus run-level determinism |

R11 (both engines exercised) and R12 (report mandatory) are reporting
obligations, enforced in the report renderer rather than the patch guard.

## Worked examples

### 1. Allowed - the sanctioned in-place edit

```csharp
- using var connection = new SqlConnection(ConfigurationManager.ConnectionStrings["AppDb"].ConnectionString);
+ using var connection = _dbFactory.CreateConnection();
```

Permitted **only** at a site the inventory marked `ConnectionSite`, and tracked as
its own decision class in the report. This is the single exception to "never edit
the SQL Server path", because seam 1 cannot exist otherwise.

### 2. Rejected - a helpful-looking improvement

```csharp
- catch (SqlException ex) when (ex.Number == 2627)
+ catch (DbException ex) when (_dialect.IsUniqueViolation(ex))
```

Correct, portable, and **rejected** in the original unit: it changes a working SQL
Server code path. The widening belongs in the generated alternate. Under
`--strict-scope` the unit is routed to manual review.

The same applies to parameterizing the original's concatenated SQL - a real
security improvement, and still not this tool's change to make (it is reported as
a finding instead).

### 3. Rejected - a dispatcher with an opinion

```csharp
public IList<Order> GetOrders(int customerId, int take)
{
    _log.Debug("GetOrders");                                   // rejected
    if (customerId <= 0) throw new ArgumentException();        // rejected
    return _db.Provider == DatabaseProvider.PostgreSql
        ? GetOrders_PostgreSql(customerId, take)
        : GetOrders_SqlServer(customerId, take);
}
```

The dispatcher must match the template exactly. Logging and validation are new
behaviour on both paths - including the SQL Server one, which is precisely what
R1 forbids. They also make the diff unreviewable as a mechanical transform.

## Traps

- **"It is obviously an improvement" is the failure mode**, not an exception to
  the rule. The tool's only job is: same behaviour, two databases, config switch,
  buildable, honestly reported.
- **A whitespace-only difference still fails immutability.** That is intended: the
  check is worth nothing if it tolerates "harmless" edits.
- **`--no-strict-scope` is a debugging flag**, not a normal mode. Document it as
  such wherever it appears.
- **The post-apply pass is not redundant.** A patch can apply differently than it
  validated, and the headline claim must be checked against what is on disk.

## Escalate when

- A unit cannot be converted without changing its signature.
- A finding sits in a file the allow-list does not cover and that is not a file
  class the tool may create.
- The diff budget is exceeded - that usually means a decision upstream was wrong,
  not that the budget is too small.

## Do not

- Do not modernize: no `packages.config` migration, no C# syntax updates, no
  `HttpContext.Current` cleanup, no warning fixes.
- Do not fix a build diagnostic that cannot be mapped to a finding. Report it.
- Do not reformat, reorder usings, or rename anything.
- Do not let the AI layer write files. It proposes patches; the apply stage
  validates and applies them through this guard.
