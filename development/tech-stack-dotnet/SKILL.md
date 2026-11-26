---
name: tech-stack-dotnet
description: .NET stack context for workflow skills — dotnet build, test and migration commands, EF Core and MediatR patterns, analyzer setup, C# coding guidelines and reference file paths.
license: MIT
compatibility:
  - claude-code
  - codex
type: tech-stack
user-invocable: false
---

# Tech Stack: .NET

## Overview

.NET/C# context for the workflow skills and review agents: commands, detection markers, the Moberg EF/MediatR rules, the analyzer wall, settings and scan recipes.

## When To Use

Loaded automatically by commands and skills when the active tech stack is `dotnet`. Not invoked directly.

## Build & Test Commands

- **Compile:** `dotnet build --nologo -v q`
- **Test (batch):** `dotnet test --nologo -v q --no-build --filter <project>` — under **Microsoft.Testing.Platform** (`.slnx`, or `global.json` runner set to MTP) `--filter` is rejected; pass runner args after `--`: `dotnet test --solution <slnx> -- --filter-class <FullyQualifiedClass>` (or `--filter-method`). A rejected filter fails the run, so a "filtered" test claim was never scoped — match the filter form to the runner.
- **Test (full):** `dotnet test --nologo -v q --no-build`
- **Migrations (`dotnet ef`):** in a multi-project solution supply **both** `--project <DataProject>` and `--startup-project <MigratorProject>`, name the context (`--context <DbContext>`), and export a dummy `ConnectionStrings__<Context>=Host=localhost;Database=x;Username=x;Password=x` so design-time construction succeeds without a live database. Omitting the startup project or the connection string is the recurring failure — three agents rediscovered it in one field run.
- **Bounded output is the default.** `--no-build` assumes the build step ran in the same checkpoint; when running tests alone, drop it. Batch checkpoints run these through `bash scripts/mtk-verify-run.sh --label <batch-id>-<step> -- <cmd>` — the wrapper's bounded tail is the evidence, the log path is the receipt. `-v q` hides analyzer warnings — acceptable, because the review lanes read the diff, not the build log.
- **Test (list-only):** enumerates discovered tests without executing them — the F7/command-verification list variant used to verify `dotnet test` is runnable without paying for a full suite run. Conditional on the solution format:
  - `.sln`: `dotnet test <sln> --list-tests`
  - `.slnx` (or `global.json` sets `"test": {"runner": "Microsoft.Testing.Platform"}`): `dotnet test --solution <slnx> --list-tests` — a bare `dotnet test <slnx> --list-tests` fails with `"Specifying a solution for 'dotnet test' should be via '--solution'"` under Microsoft.Testing.Platform.
- **Format:** whitespace + style only, never a bare `dotnet format` (see the Format Command section).

## File Extensions & Markers

How `setup-bootstrap` detects this stack in a repository:

| Marker | Confidence |
|---|---|
| `*.sln` or `*.slnx` | High |
| `*.csproj` | High |
| `global.json` | Medium |
| `Directory.Build.props` | Medium |

Detection command:
```bash
find . \( -name "*.sln" -o -name "*.slnx" -o -name "*.csproj" \) -not -path "*/bin/*" -not -path "*/obj/*" 2>/dev/null | head -5
```

## ORM & Data Layer Guidance

The single copy of the EF Core rules (the coding guidelines restate a few; the stack supplements do not):

- `.Select()` projection over `Include()` for DTO reads, and no `.Include()` at all when the query ends in a `Select(new ...)`: the projection already loads what it names.
- `AsNoTracking()` on read-only queries; async query methods; filter in the database, not after materialization.
- **Order and filter on the entity, not on a projected member.** Once `.Select()` has produced a record, `OrderBy`/`Where` on one of *its* members is untranslatable, and EF abandons the whole query instead of sorting in memory. Put them before the projection, or order by the entity property the member came from. It fails at runtime, so only a test catches it.
- One `SaveChanges` per handler; the transaction boundary covers audit writes and multi-aggregate changes (see `domain-finance.md`).
- Migrations use the `dotnet ef` form in `## Build & Test Commands`; review the generated migration before applying it.
- Schema changes ship expand-then-contract (`.claude/references/schema-migrations.md`): no drop, rename, type narrowing or `NOT NULL` on existing rows in the same deploy as code that still uses the old shape. Run every `Down()` before merging (`dotnet ef database update <PreviousMigration>`, or `0` when it is the first migration, same flags), and backfill in a batched job, not one `UPDATE` inside `Up()`.
- Non-ORM access the scan found (Dapper, RDS Data API, raw `SqlCommand`) stays as it is; do not migrate it to EF unless asked.

## Framework Patterns

**MediatR / CQRS (when detected):** `Request`, `Response` and `Handler` in one file; `Command`/`Query` suffixes; folder layout matching the neighboring slices; one `SaveChanges` per handler; validation through the project-standard mechanism (FluentValidation, DataAnnotations, whichever the scan found).

**Runtime:** `HttpClient` through `IHttpClientFactory`; `CancellationToken` propagated through async chains. In AWS Lambda, lazy-init heavy clients and secrets and keep `DbContext` scoped to the invocation.

## Test Level Guidance

- Handlers, endpoints, persistence, authorization and EF behavior get integration tests; pure logic, validators and mapping get unit tests.
- Never default to `UseInMemoryDatabase` when relational behavior matters (arrays, JSONB, timestamps, transactions, raw SQL). Provider and framework rules: `.claude/references/dotnet/testing-supplement.md`.

## Coding Style Reference

Path: `.claude/references/dotnet/coding-guidelines.md`

Source: `https://raw.githubusercontent.com/moberghr/coding-guidelines/<sha>/CodingStyle.md`, where `<sha>` is the commit pinned in the plugin manifest (`coding-guidelines.sha` in `${CLAUDE_PLUGIN_ROOT}/.claude/manifest.json`, with the expected sha256 under `coding-guidelines.files`). `setup-bootstrap` STEP 1 fetches that revision and verifies the hash. Never fetch from `main`.

Reviewer summary: lambda params `x` (nested `y`, `z`); chained LINQ on separate lines, one condition per `.Where()`; file-scoped namespaces; `var` for locals; early return over `else`; braces on all control flow.

## Analyzer Configuration

`.claude/references/dotnet/analyzer-config.md` carries the packages, the `.editorconfig` severities and **the analyzer wall**: in a warnings-as-errors repo, StyleCop (`SA*`), Sonar (`S*`) and Meziantou (`MA*`) cause most build-gate failures, not MTK's rules. Read it before the first build of a batch. Two of its facts matter on every run:

- **SA1512/SA1514 collide** on a `//` banner placed directly above a `///` doc comment; no blank-line choice satisfies both. Never stack them.
- A green `dotnet build` does not imply a green `dotnet format --verify-no-changes`; they run different rule sets. Gate on both.

Build with analyzer capture. Log to a file, never `tee /dev/tty` (agent shells have no controlling terminal):
```bash
mkdir -p .mtk
dotnet build 2>&1 | tee .mtk/build.log
bash "${CLAUDE_PLUGIN_ROOT}/hooks/parse-build-diagnostics.sh" --file .mtk/build.log > .mtk/analyzer-output.json
```

## Companion Plugin: dotnet-claude-kit

If `codewithmukesh/dotnet-claude-kit` is installed, use its Roslyn MCP tools: `DetectAntiPatterns` in pre-commit and batch review (treat results as `source: "analyzer"`, `confidence: 100`), `GetProjectGraph`/`GetDependencyGraph` to scope builds on large solutions, `FindDeadCode`/`DetectCircularDependencies` in architecture review, `GetDiagnostics` for per-file warnings, `GetTestCoverageMap` to check coverage claims. Without it, skills fall back to `parse-build-diagnostics.sh` and AI review.

## Recommended Tooling

`docs/recommended-tooling/dotnet.md` (with `docs/recommended-tooling/shared.md`): `csharp-lsp`, `dotnet-claude-kit`, `microsoft-learn`. `setup-bootstrap` prints both; install is manual.

## Reference Files

Loaded by commands and review agents when the active stack is `dotnet`:

- `.claude/references/dotnet/coding-guidelines.md` — Moberg C# coding style guide (upstream-pinned)
- `.claude/references/dotnet/testing-supplement.md` — test frameworks and EF Core test providers
- `.claude/references/dotnet/analyzer-config.md` — analyzer packages, `.editorconfig` severities, the analyzer wall
- `docs/recommended-tooling/dotnet.md` — recommended MCPs, plugins and editor integrations

The EF Core, MediatR and runtime rules live in this skill (`## ORM & Data Layer Guidance`, `## Framework Patterns`).

## Settings Additions

`setup-bootstrap` merges these, after `.claude/references/settings-baseline.md`, into the project's `permissions.allow` / `permissions.deny` (never an `allowedTools` key).

### allow (merge: union)
- `Bash(dotnet build:*)`
- `Bash(dotnet test:*)`
- `Bash(dotnet format:*)`

### deny (merge: union)
- `Read(**/appsettings.Production.json)`
- `Bash(dotnet publish:*)` — deny-only; publish is a deploy-adjacent action bootstrap should not pre-authorize. When a pattern appears in both `allow` and `deny`, deny wins, so it is listed here only.

### hooks (do NOT add)

`format-on-edit.sh` is wired by the plugin's own `hooks/hooks.json`. Bootstrap never copies an MTK hook into the target's `settings.json`; `setup-bootstrap` Settings Merge says why.

## Format Command

```bash
# Wired by the plugin's own hooks.json (queue at PostToolUse, flush at Stop) —
# not by the project's settings.json. See '### hooks (do NOT add)' above.
# Manual invocation (project-wide) — whitespace + style only, never `analyzers`:
dotnet format whitespace --verbosity quiet && dotnet format style --verbosity quiet
```

At flush the hook groups the turn's edited `.cs` files by their nearest `.csproj` (else `.sln`/`.slnx`) and runs `dotnet format whitespace` then `dotnet format style`, one `--include <relative paths>` call per workspace, from that workspace directory. The field facts behind that shape:

- `--include` matches only paths relative to the invocation directory; an absolute path matches nothing and still exits 0.
- The `analyzers` pass is excluded: bare `dotnet format` applies CA/third-party code fixes (a CA1001 fix broke a test class repeatedly; another run rewrote every `DbSet<T>` as nullable). Those are reviewed changes, not formatting.
- `dotnet format` loads the whole workspace before filtering, so one run per file is pathological. A `.cs` file with no project above it is skipped. Failures log to stderr and never block.

## Pre-Commit Review Items

Tool-keyed items for the generated `pre-commit-review-list.md`; `setup-bootstrap` keeps those whose tool the scan detected.

- [EF Core] `AsNoTracking` on reads, `Select()` over `Include()`, `CancellationToken` propagated, `DbContext` scoped/disposed correctly
- [MediatR] one `SaveChanges` per handler, validate request
- [Lambda] cold-start considerations — lazy-init heavy clients/secrets, avoid blocking work at startup

## Scan Recipes

Used by `setup-audit` when auditing a .NET repository.

### Dependency Registry Verification

Before planning the install of any NuGet package not already referenced, verify it exists and is the real one (criterion 0 of `.claude/references/dependency-intake-checklist.md`). Not found, or a typosquat-like name, is an immediate block; an unverified AI-recommended package is tagged `[ASSUMED]` with a `checkpoint:human-verify` step before any install.

```bash
dotnet package search <id> --exact-match --source https://api.nuget.org/v3/index.json
```

### Project Structure
```bash
find . -name "*.csproj" -not -path "*/bin/*" -not -path "*/obj/*" 2>/dev/null | sort
find . -name "*.sln" -not -path "*/bin/*" 2>/dev/null
grep -r "TargetFramework" --include="*.csproj" | head -10
grep -rh "PackageReference" --include="*.csproj" | sed 's/.*Include="//' | sed 's/".*//' | sort -u
```

### Patterns In Use
```bash
grep -rl "IRequest\|IRequestHandler\|IMediator" --include="*.cs" | head -20
find . \( -path "*/Commands/*" -o -path "*/Queries/*" \) | head -20
grep -rl "Result<\|Result\.Success\|Result\.Failure" --include="*.cs" | head -10
grep -rl "IDomainEvent\|DomainEvent\|INotification" --include="*.cs" | head -10
grep -rl "AbstractValidator\|IRuleBuilder" --include="*.cs" | head -10
grep -rl "IMapper\|CreateMap\|TypeAdapterConfig" --include="*.cs" | head -10
grep -rl "DbContext\|DbSet\|OnModelCreating" --include="*.cs" | head -10
```

### Data Layer
```bash
find . -name "*Configuration*.cs" -not -path "*/bin/*" | head -10
grep -rl "IEntityTypeConfiguration\|modelBuilder\.\|HasKey\|HasIndex" --include="*.cs" | head -5
grep -rn "FromSqlRaw\|ExecuteSqlRaw\|SqlQuery" --include="*.cs" | head -5
grep -rn "AsNoTracking" --include="*.cs" | head -5
grep -rc "\.Include(" --include="*.cs" | grep -v ":0" | head -5
grep -rc "\.Select(" --include="*.cs" | grep -v ":0" | head -5
grep -rn "ConnectionString\|UseNpgsql\|UseSqlServer\|UseInMemory" --include="*.cs" | head -5
grep -rl "DataApiHelper\|IAmazonRDSDataService\|Dapper\|SqlCommand" --include="*.cs" | head -5
```

### Infrastructure
```bash
grep -rh "Amazon\.\|AWS\.\|AWSSDK" --include="*.cs" --include="*.csproj" | sort -u | head -20
find . -name "*.csproj" \( -path "*cdk*" -o -path "*Cdk*" \) | head -5
grep -rl "ILambdaContext\|FunctionHandler\|LambdaSerializer" --include="*.cs" | head -5
grep -rn "Vpc\|SubnetType\|SecurityGroup\|NatGateway" --include="*.cs" | head -10
find . \( -name "Dockerfile" -o -name "docker-compose*" \)
grep -rl "IAmazonSQS\|IAmazonSNS\|SendMessageAsync\|SQSEvent" --include="*.cs" | head -5
grep -rl "SecretsManager\|GetSecretValue\|SecretResolver" --include="*.cs" | head -5
```

### Naming Conventions
```bash
find . -name "*Controller*.cs" -not -path "*/bin/*" | head -10
find . -name "*Handler*.cs" -not -path "*/bin/*" -not -path "*Test*" | head -10
grep -rn "AddSingleton\|AddScoped\|AddTransient\|AddDbContext" --include="*.cs" | head -10
```

### Testing Patterns
```bash
find . -name "*Test*" -name "*.csproj" -not -path "*/bin/*"
grep -rh "PackageReference" --include="*.csproj" | grep -i "xunit\|nunit\|mstest\|moq\|nsubstitute\|bogus\|fluentassert" | sort -u
grep -rn "UseInMemoryDatabase\|UseSqlite\|TestContainers" --include="*.cs" | head -10
grep -rl "WebApplicationFactory\|IClassFixture\|IntegrationTest" --include="*.cs" | head -5
```

### Configuration
```bash
find . -name "appsettings*.json" -not -path "*/bin/*" | head -10
grep -rl "IOptions\|IConfiguration\.\|builder\.Configuration" --include="*.cs" | head -10
grep -rl "ILogger\|Serilog\|NLog" --include="*.cs" | head -10
```

## Verification

- [ ] Tech stack skill is loaded when `.claude/tech-stack` contains `dotnet`
- [ ] Build and test commands execute correctly for the target project
- [ ] Reference files exist at the paths listed in `## Reference Files`
- [ ] Scan recipes produce meaningful output for a .NET repository
