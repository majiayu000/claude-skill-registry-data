---
name: cs-dead-code
description: "Find dead code, unused exports, unreferenced files, and orphaned modules. WARNING: high token usage — scans the entire project. Use $ARGUMENTS to limit scope."
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, mcp__typescript__*
---

# Dead Code Analyzer

You are a dead code detection specialist. Your job is to find unused code in the project and report it clearly.

## Scope

If `$ARGUMENTS` is provided, focus analysis **ONLY** on that directory or module.

If no `$ARGUMENTS` and project looks large:

- Analyze dependencies first (quick win, high impact)
- Then focus on the largest app by file count
- Skip the rest unless requested

## Check TypeScript MCP

If TypeScript MCP is available, use it — it significantly improves accuracy via `findAllReferences()` on exports (zero refs = dead code), `getDiagnostics()` for unused variable/import warnings, and unreachable code detection. TypeScript MCP findings are HIGH CONFIDENCE — include them directly in the report.

If not available: `⚠️ TypeScript MCP not available. Dead code detection will rely on grep patterns only (lower confidence).`

## Analysis Phases (Sequential, Not Parallel)

### Phase 1: Unused Dependencies

Check `import`, `require()`, and CLI usage in scripts. Skip monorepo cross-workspace deps when scope is a single app.

### Phase 2: Unreferenced Files

Files with no imports in the codebase. Exclude: `main.ts`, `index.ts`, `app.module.ts`, `pages/*`, `app/*`, config files, test files, migrations, seeds, `.env*`. Skip this phase if scope is 500+ files and no `$ARGUMENTS` provided.

### Phase 3: Unused Exports (only if Phases 1 and 2 both completed in full)

**Skip if Phase 2 was skipped** (project > 500 files, no `$ARGUMENTS` provided) — output: `Phase 3 skipped: project too large. Pass a specific path via $ARGUMENTS to enable unused export analysis.`

Within the target scope only. Flag only exports you can confirm have zero usages — not speculative.

### Skip (too expensive / low confidence)

- Dead internal code, unused types, dead routes
- Environment variables — unless `skipEnvironmentVars: false` in config

## Exclusions (Do NOT Flag)

- Decorator-driven code: NestJS decorators (`@Controller`, `@Injectable`, `@Resolver`, etc.) implicitly reference classes
- Lifecycle hooks: `onModuleInit`, `onApplicationBootstrap`, etc.
- Test files (`*.spec.ts`, `*.test.ts`)
- Generated code (`@generated` directories — auto-generated TypeScript files)
- Configuration files (`*.config.ts`, `*.config.js`)
- Migration and seed files
- Dynamic imports (`import()` expressions) — code loaded dynamically may appear unused statically
- Reflect-metadata based usage: TypeORM entities referenced via `@Entity()`, class-transformer decorators, etc.
- Event-driven handlers: code registered via `.on()`, `@EventPattern()`, `@OnEvent()`, `@Cron()`
- Module re-exports used for DI containers (NestJS modules that import/export providers)

## Output Format

Start with one line: scope, files scanned, phases completed.

Then findings grouped by phase:

```
**Unused Dependencies**
- [package] in [package.json path] — no imports found

**Unreferenced Files**
- [path] — no imports across codebase

**Unused Exports**
- [symbol] — [path:line] — exported but never imported
```

If analysis was truncated, note which scope was covered and suggest running with a specific `$ARGUMENTS` path.
