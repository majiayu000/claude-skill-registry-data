---
name: test-selection
description: >
  How dualdb chooses which tests to run, which to defer, and what new tests to
  generate. Use when selecting tests after a conversion, when deciding whether a
  test needs a database, when generating provider-selection tests, or when writing
  the test line of the report. Deferred tests are listed, never silently skipped.
---

# Test selection

Phase 1 does not touch databases. What it can still do is worth doing, and what it
cannot must be stated rather than quietly skipped.

## When to use

Selecting and running tests after a conversion; classifying a test as DB-requiring;
generating provider tests; writing the test line of the report.

## Decision procedure

1. **Impacted tests.** Reverse-dependency walk from the changed symbols - the
   analyzer already has the call graph. Run these.
2. **All existing unit tests that do not require a database.** Run these too; they
   are cheap and they catch collateral damage.
3. **DB-requiring tests: skip and *list*.** Detect them by connection-string
   usage, `[Category("Integration")]`-style attributes, `TestContainers`, or
   fixture setup that opens a connection. Record the count and the names.
4. **Generate provider-selection tests** for the code the tool introduced.
5. **Statically validate every generated PostgreSQL SQL artifact** by parsing it
   as PostgreSQL. Cheap, catches a lot, needs no server.

Explicitly do **not** iterate thousands of procedures against a database. Record
the count of DB-requiring things deferred to Phase 2.

## The generated tests

Pure unit tests, no database. Added to an existing test project, matching its
framework - **never add a new test framework**.

- config `SqlServer` yields a `SqlConnection`
- config `PostgreSql` yields an `NpgsqlConnection`
- an unknown provider value throws a clear error naming the key and the allowed
  values (`PG-CFG-001`)
- the dialect helper returns the expected fragment per provider
- each dispatcher routes to the right unit per provider - which is also the
  structural half of the rollback-equivalence claim

## Rollback equivalence

With the provider set to `SqlServer`, the converted application must exercise
exactly the original code paths. Assert it two ways:

- **structurally** - the dispatcher shape plus byte-identical `_SqlServer` bodies
  (that is the scope guard's immutability check);
- **behaviourally** - the existing unit tests, unchanged, still pass.

If the second one fails, the conversion is wrong no matter what the first says.

## Worked examples

### 1. Run - a test that asserts on SQL text

```csharp
[Fact]
public void InListSql_UsesOneParameterPerId() { ... }
```

No connection, no fixture. It is also *impacted*, because it asserts on a string
the conversion may have changed. Run it, and expect it to fail if the tool
rewrote that SQL - which is exactly the signal wanted.

### 2. Defer and list - a test that opens a connection

```csharp
[Fact(Skip = "requires a live SQL Server")]
public void ArchiveProcedure_ReturnsCount()
{
    using var connection = new SqlConnection("Server=localhost;...");
```

Already skipped, and it would need a database anyway. It appears in
`deferredDbRequired` with its name, and the report says
*"38 DB-requiring tests deferred to Phase 2"* and lists them. It does not appear
in a passed count.

### 3. Generate - a provider-selection test

```csharp
[Theory]
[InlineData("SqlServer", typeof(SqlConnection))]
[InlineData("PostgreSql", typeof(NpgsqlConnection))]
public void Factory_ReturnsConnectionForConfiguredProvider(string value, Type expected)
{
    var factory = BuildFactory(new Dictionary<string, string> { ["Data:Provider"] = value });
    Assert.IsType(expected, factory.CreateConnection());
}

[Fact]
public void Factory_RejectsUnknownProvider()
{
    var ex = Assert.Throws<InvalidOperationException>(
        () => BuildFactory(new Dictionary<string, string> { ["Data:Provider"] = "MySql" }));
    Assert.Contains("Data:Provider", ex.Message);
}
```

The second test matters as much as the first: fail-fast on an invalid value is a
requirement (`PG-CFG-001`), and requirements that are not tested decay.

## Traps

- **A skipped test is not a passing test.** Never fold deferred tests into a
  passed count, and never report a total that includes them.
- **A test asserting on SQL text will fail after a legitimate conversion.** That
  is a finding for the report, not a bug to paper over by editing the test - and
  editing tests is a forbidden change anyway.
- **`TestContainers` and Respawn-style fixtures** open connections in setup, not
  in the test body. Detect the fixture, not just the method.
- **Impacted-test selection is only as good as the call graph.** Where the graph
  is incomplete, prefer running more tests, not fewer.
- **Static SQL validation is not execution.** Parsing as PostgreSQL proves syntax,
  nothing about semantics or about the schema existing.

## Escalate when

- A test project cannot be built at the reached tier - its tests can be neither
  run nor honestly counted.
- A test asserts on provider types (`SqlConnection`, `SqlException`) as part of its
  contract - it needs a per-provider variant, which is a change to a test, so it
  is a review item rather than an automatic edit.
- The only coverage for a converted unit is a DB-requiring test. That unit is
  effectively unverified in Phase 1, and the report must say so.

## Do not

- Do not add a new test framework, or a new test project, unless none exists.
- Do not modify or delete existing tests. Deleting tests is a forbidden change.
- Do not run thousands of procedures against a database - that is Phase 2.
- Do not claim a test passed on PostgreSQL. Phase 1 never executes against it
  (guardrail R11).
