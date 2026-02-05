---
name: cljr-feature-dev
description: Develop features for the Cljr Clojure-to-.NET compiler. Use when adding emitter features, expression types, analyzer support, or testing features. Guides the complete workflow from Expr.cs to C# tests to NRepl verification. Critical for REPL-oriented development.
---

# Cljr Feature Development

This skill guides you through the complete workflow for adding features to the Cljr compiler, with proper testing in both C# unit tests and NRepl evaluation.

## When to use this skill

- Adding new language features to the emitter
- Creating new expression types in the analyzer
- Modifying existing expression handling
- Testing features via C# unit tests
- Testing features via NRepl evaluation (CRITICAL for REPL-oriented workflow)

## Feature Development Workflow

### Step 1: Define Expression Type (if new)

**Location:** `src/Cljr.Compiler/Analyzer/Expr.cs`

Add a new record type extending `Expr`:

```csharp
/// <summary>
/// Description of what this expression represents
/// </summary>
public record MyFeatureExpr(
    string Property1,
    Expr Property2
) : Expr;
```

See [expressions.md](expressions.md) for all existing expression types.

### Step 2: Add Analyzer Support

**Location:** `src/Cljr.Compiler/Analyzer/Analyzer.cs`

- Add case in `AnalyzeForm()` or `AnalyzeSeq()` to recognize the new form
- Build the expression AST
- Handle type hints and symbol resolution

### Step 3: Add Emitter Support

**Location:** `src/Cljr.Compiler/Emitter/CSharpEmitter.cs`

- Add case to `EmitExpr()` switch statement
- Generate valid C# code for the expression

```csharp
case MyFeatureExpr e:
    EmitMyFeature(e);
    break;
```

### Step 4: Write C# Unit Test for Compilation (REQUIRED)

**Location:** `tests/Cljr.Compiler.Tests/`

Test that the emitter generates correct C# code:

```csharp
[Fact]
public void MyFeature_EmitsCorrectCSharp()
{
    var source = "(my-feature args)";
    var result = Compile(source);
    Assert.Contains("expected C# output", result);
}
```

### Step 5: Write C# Unit Test for NRepl Eval (REQUIRED)

**Location:** `tests/Cljr.Compiler.Tests/ReplNamespaceTests.cs`

This is **CRITICAL** for the REPL-oriented workflow. Test via `NreplSession.EvalAsync()`:

```csharp
[Fact]
public async Task MyFeature_WorksInRepl()
{
    var session = new NreplSession();

    var result = await session.EvalAsync("(my-feature args)");

    Assert.Null(result.Error);
    Assert.Equal(expectedValue, result.Values[0]);
}
```

See [testing-patterns.md](testing-patterns.md) for comprehensive test patterns including:
- State persistence across evaluations
- Namespace isolation
- Error handling

### Step 6: Manual NRepl Verification (Optional)

Start the REPL and test interactively:

```bash
./nrepl.sh
# or
dotnet run --project src/Cljr.Cli -- nrepl
```

Then test your feature in the REPL to verify developer experience.

## Key Files

| File | Purpose |
|------|---------|
| `src/Cljr.Compiler/Analyzer/Expr.cs` | Expression type definitions |
| `src/Cljr.Compiler/Analyzer/Analyzer.cs` | Parsing and AST construction |
| `src/Cljr.Compiler/Emitter/CSharpEmitter.cs` | C# code generation |
| `tests/Cljr.Compiler.Tests/ReplNamespaceTests.cs` | NRepl evaluation tests |
| `src/Cljr.Repl/NreplSession.cs` | REPL session API |

## Testing Requirements

Every feature MUST have:

1. **C# compilation test** - Verify the emitter generates correct C#
2. **C# NRepl eval test** - Verify the feature works in REPL evaluation via `NreplSession.EvalAsync()`

The NRepl eval test is especially important because it ensures the feature works in the interactive REPL-oriented development workflow that Clojure developers expect.

## Run Tests

```bash
# Run all compiler tests
dotnet test tests/Cljr.Compiler.Tests/

# Run specific test
dotnet test tests/Cljr.Compiler.Tests/ --filter "MyFeature"
```

## References

- [Expression Types](expressions.md) - All 30+ expression types in Expr.cs
- [Testing Patterns](testing-patterns.md) - C# and NRepl test examples
