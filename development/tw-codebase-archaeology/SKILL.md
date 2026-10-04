---
name: tw-codebase-archaeology
description: Systematically explore an unfamiliar codebase and build a reusable architecture summary. Use for repo onboarding, understanding legacy or inherited code, mapping architecture before a migration or refactor, tracing a bug or feature path, or answering "what does this project do?". Documentation-first, then data flow — ends in a concise technical architecture summary with file:line evidence, not a raw file dump.
---

# Codebase Archaeology

## Purpose

Build a practical mental model of an unfamiliar codebase without reading files randomly. Start with project guidance and documentation, then trace from entry points through domain logic, storage, integrations, configuration, and tests.

## Core rule: documentation first, then data flow

Before reading source, inspect the project-level context:

```bash
cat AGENTS.md CLAUDE.md README.md 2>/dev/null | head -200
find . -maxdepth 2 \( -name 'AGENTS.md' -o -name 'CLAUDE.md' -o -name 'README*' -o -name 'CONTRIBUTING*' -o -name 'ARCHITECTURE*' -o -name 'docs' \) -print
```

Do not skip this. Guidance files and docs often hold architecture notes, setup assumptions, local conventions, and non-obvious constraints that are expensive to rediscover from code alone.

## Inputs

| Input | Default | Notes |
|---|---|---|
| `scope` | whole repo | May be a package, service, directory, feature, route, command, or file set. |
| `depth` | standard | `quick` for a fast map, `standard` for a normal summary, `deep` for parallel exploration. |
| `focus` | architecture + data flow | May be entry points, one feature, storage, config, test strategy, or legacy risk. |
| `output` | architecture summary | Adapt for a map, migration notes, bug trace, or onboarding guide. |

## Workflow

### 1. Read project guidance and docs
Capture purpose, runtimes, package managers, local commands, conventions, and named services/apps/packages.

### 2. Classify repository shape
```bash
find . -maxdepth 2 -type f \( -name 'package.json' -o -name 'Cargo.toml' -o -name 'pyproject.toml' -o -name 'go.mod' -o -name 'pom.xml' -o -name 'build.gradle*' -o -name 'composer.json' \) -print
find . -maxdepth 2 -type d | sed 's#^./##' | sort | head -120
```
Classify as CLI/tooling, web frontend, backend service, full-stack app, library/package, monorepo, data pipeline, or infrastructure/config.

### 3. Identify entry points
```bash
rg -n "fn main|def main|if __name__ == ['\"]__main__['\"]|func main|public static void main|export default|createRoot|FastAPI\(|Flask\(|express\(|Router\(|app\.(get|post|put|delete)|clap|argparse|click|typer|cobra|commander|yargs" .
```
Record CLI commands, HTTP routes, bootstrap modules, workers/schedulers/consumers, and public library APIs.

### 4. Find the core domain model
```bash
rg -n "(export )?(pub )?(struct|enum|class|interface|type) [A-Z][A-Za-z0-9_]+|@dataclass|BaseModel|z\.object|createTable" .
```
Do not list every type. Identify the central 3–5 types and explain their relationships, ownership, and lifecycle.

### 5. Trace data flow
```text
entry point -> parser/router/controller -> service/use case -> domain logic -> storage/integration -> response/output
```
For each important flow: what input arrives, where validation happens, which module orchestrates, which domain objects change, where persistence/external I/O happens, what output is returned.

### 6. Map integrations and configuration
```bash
rg -n "process\.env|std::env|os\.environ|os\.getenv|dotenv|BaseSettings|viper|serde::Deserialize" .
rg -n "fetch\(|axios|reqwest|requests\.|httpx|grpc|GraphQL|sqlx|diesel|prisma|sequelize|typeorm|sqlalchemy|redis|kafka|sqs|s3|File::|fs\." .
```
Capture databases, external APIs/SDKs, file I/O, queues/event buses, cron/jobs, env vars, config files, defaults, CLI flags, and credential-loading points — without exposing secret values.

### 7. Read tests for intended behavior
```bash
find . -maxdepth 3 -type d \( -name test -o -name tests -o -name __tests__ -o -name spec \) -print
rg -n "describe\(|it\(|test\(|pytest|#\[test\]|func Test|@Test" .
```
Capture the framework, the test command, key fixtures, important tested behavior, and gaps where critical flows lack tests.

### 8. Synthesize — do not dump raw notes
Return a concise architecture model with `file:line` citations. Do not paste large source snippets. Label inferences and open questions as such.

## Parallel exploration (deep mode)

Only when the user asks for parallel/subagent exploration. Fan out read-only workers — one per topic: docs, entry points, domain model, data flow, integrations, tests. Use whatever your harness provides (Claude Code: the Task tool with the Explore agent; Codex: named read-only custom agents or the built-in explorer). Give every worker the same scope and constraints, forbid edits, require `file:line` evidence, then synthesize one architecture summary yourself. If parallel agents are unavailable, do the same passes inline and say so.

## Output template

```markdown
# [Project] — Technical Architecture Summary

## Executive Summary
[Project] is a [type] that [purpose]. Its main shape is [pattern], with [components].

## Repository Shape
- Languages/runtimes / package-build system / top-level modules / main commands

## Entry Points
| Entry | Location (path:line) | Purpose |

## Architecture Map
[input] -> [router/parser] -> [service] -> [domain] -> [storage/integration] -> [output]

## Key Types
| Type | Location | Purpose | Related modules |

## Data Flow — [flow name]
1. path:line — entry
2. path:line — validation/transform
3. path:line — domain logic
4. path:line — persistence/integration/output

## Integrations and Configuration
| Boundary | Location | Notes |

## Tests and Intended Behavior
- Framework / commands / notable coverage / gaps

## Mental Model
[One or two paragraphs on how to reason about the system when changing it.]

## Open Questions
## Suggested Next Dives
```

## Anti-patterns

| Do not | Do instead |
|---|---|
| Start by reading random large files | Read docs, manifests, and entry points first |
| Dump raw source into the answer | Synthesize a mental model with citations |
| List every class/type | Identify the few core abstractions |
| Ignore tests | Use tests to infer intended behavior |
| Treat inferred architecture as fact | Label inferences and open questions |
| Let exploration workers edit files | Keep archaeology read-only |
