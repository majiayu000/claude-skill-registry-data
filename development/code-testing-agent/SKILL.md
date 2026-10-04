---
name: code-testing-agent
description: >-
  Generates and writes new unit tests for any programming language using a
  Research-Plan-Implement pipeline. Use when asked to generate tests,
  write unit tests, add tests, improve test coverage, create test
  project, achieve high coverage, comprehensive tests, or asked to
  scaffold a new test project for an app, service, or library. Supports
  C#, TypeScript, JavaScript, Python, Go, Rust, Java, and more. Orchestrates
  the code-testing-generator sub-agent through research, planning, and
  implementation phases so tests compile, pass, and follow project
  conventions. DO NOT USE FOR: running existing tests or test filters
  (use run-tests); diagnosing coverage plateaus or project-wide
  coverage/CRAP analysis without writing tests (use coverage-analysis);
  targeted method/class CRAP scores (use crap-score); MSTest assertion
  guidance, MSTest test pattern modernization, or fixing existing MSTest test
  code (use writing-mstest-tests).
license: MIT
---

# Code Testing Generation Skill

Generate focused, workable tests for meaningful production behavior in any programming language. Use the coordinated pipeline when the scope benefits from it.

## When to Use This Skill

Use this skill when you need to:

- Generate unit tests for an entire project or specific files
- Improve test coverage for existing codebases
- Create test files that follow project conventions
- Write tests that actually compile and pass
- Add tests for new features or untested code

## When Not to Use

- Running or executing existing tests (use the `run-tests` skill)
- Migrating between test frameworks (use migration skills)
- Writing tests specifically for MSTest patterns (use `writing-mstest-tests`)
- Debugging failing test logic

## How It Works

This skill coordinates multiple specialized agents in a **Research → Plan → Implement** pipeline:

### Pipeline Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                     TEST GENERATOR                          │
│  Coordinates the full pipeline and manages state            │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌───────────┐  ┌───────────┐  ┌───────────────┐
│ RESEARCHER│  │  PLANNER  │  │  IMPLEMENTER  │
│           │  │           │  │               │
│ Analyzes  │  │ Creates   │  │ Writes tests  │
│ codebase  │→ │ phased    │→ │ per phase     │
│           │  │ plan      │  │               │
└───────────┘  └───────────┘  └───────┬───────┘
                                      │
                    ┌─────────┬───────┼───────────┐
                    ▼         ▼       ▼           ▼
              ┌─────────┐ ┌───────┐ ┌───────┐ ┌───────┐
              │ BUILDER │ │TESTER │ │ FIXER │ │LINTER │
              │         │ │       │ │       │ │       │
              │ Compiles│ │ Runs  │ │ Fixes │ │Formats│
              │ code    │ │ tests │ │ errors│ │ code  │
              └─────────┘ └───────┘ └───────┘ └───────┘
```

## Step-by-Step Instructions

### Step 1: Determine the user request

Establish the requested behavior and scope, then read the production code, relevant callers, and existing tests. Select cases from actual input/data flows, observed regressions, domain rules, and plausible failure modes. Reachable rare boundaries and security/error handling can matter; invented states that the supported flow cannot produce do not justify tests.

Use [unit-test-generation.prompt.md](unit-test-generation.prompt.md) for conventions, test selection, and language-specific patterns. There is no default coverage percentage or test-count target. Honor explicitly requested targets and applicable required checks, but do not add tests, abstractions, or infrastructure solely to improve a metric. Stop when the scoped meaningful behaviors and risks have been checked.

### Step 2: Invoke the Test Generator

For a small request, inspect the relevant flow and write the focused tests directly; skip sub-agents, phased plans, and `.testagent/` files. For larger independent work, use the available delegation tools and pass the same behavior-based scope and stopping rule to each agent. Where `code-testing-generator` is available, invoke it with:

```text
Generate unit tests for [path or description of what to test], following the [unit-test-generation.prompt.md](unit-test-generation.prompt.md) guidelines
```

The following phases describe the larger-scope pipeline; they are not mandatory ceremony for every request.

### Step 3: Research Phase (Automatic)

The `code-testing-researcher` agent analyzes your codebase to understand:

- **Language & Framework**: Detects C#, TypeScript, Python, Go, Rust, Java, etc.
- **Testing Framework**: Identifies MSTest, xUnit, Jest, pytest, go test, etc.
- **Production Behavior**: Traces relevant callers, input/data flows, existing assertions, and failure modes worth protecting
- **Project Structure**: Maps relevant source files, existing tests, and dependencies
- **Build Commands**: Discovers how to build and test the project

Output: `.testagent/research.md`

### Step 4: Planning Phase (Automatic)

The `code-testing-planner` agent creates a structured implementation plan:

- Groups files into logical phases (2-5 phases typical)
- Prioritizes plausible regressions and consequences, accounting for dependencies
- Specifies meaningful behavior and the production path each proposed test exercises; do not require a test for every file or method
- Defines scoped success criteria and a stopping point per phase

Output: `.testagent/plan.md`

### Step 5: Implementation Phase (Automatic)

The `code-testing-implementer` agent executes each phase sequentially:

1. **Read** source files and relevant callers to establish the intended behavior
2. **Write** tests that execute the actual production implementation and assert meaningful outcomes; mock external dependencies when useful, not the behavior under test
3. **Build** using the `code-testing-builder` sub-agent to verify compilation
4. **Test** using the `code-testing-tester` sub-agent to verify tests pass
5. **Fix** using the `code-testing-fixer` sub-agent if errors occur
6. **Lint** using the `code-testing-linter` sub-agent for code formatting

Each phase completes before the next begins, ensuring incremental progress.

### Coverage Types

Choose the applicable cases from the real contract and reachable inputs; this is a menu, not a checklist for every method.

- **Happy path**: Valid inputs produce expected outputs
- **Edge cases**: Empty values, boundaries, special characters
- **Error cases**: Invalid inputs, null handling, exceptions

## State Management

All pipeline state is stored in `.testagent/` folder:

| File                     | Purpose                      |
| ------------------------ | ---------------------------- |
| `.testagent/research.md` | Codebase analysis results    |
| `.testagent/plan.md`     | Phased implementation plan   |
| `.testagent/status.md`   | Progress tracking (optional) |

## Examples

### Strategy Selection

The generator picks a strategy based on request scope:

| User Request | Strategy | Why |
|---|---|---|
| "Generate tests for `src/services/UserService.ts`" | **Direct** | Single file, small scope — write tests immediately, skip sub-agents |
| "Add unit tests for my billing project" | **Single pass** | Moderate scope — one Research → Plan → Implement cycle covers it |
| "Achieve 80% coverage across the entire solution" | **Iterative, explicitly requested target** | Select meaningful remaining risks; report if the metric would require low-value padding instead of inventing tests |

### Pipeline Walkthrough

For a request spanning several related services, the pipeline can produce:

1. **Research** → `.testagent/research.md` containing detected language/framework, build commands, files to test ranked by priority, and existing test inventory
2. **Plan** → `.testagent/plan.md` containing phased approach with specific methods and test scenarios (happy path, edge cases, error cases) for each file
3. **Implement** → Test files written, built, and verified per phase. Fix cycle runs automatically if build/test errors occur
4. **Validate** → Run the relevant tests and applicable required checks; broaden only for affected integrations, failures, or unresolved risks
5. **Report** → Behaviors protected, checks actually run and their outcomes, and material limits; report coverage metrics only when requested or required

### Language-Specific Examples

The `code-testing-extensions` skill provides concrete, filled-in examples for each pipeline phase showing real source code, real research output, real plans, and real generated tests. Call the `code-testing-extensions` skill to discover available extension files, then read:

- **`dotnet-examples.md`** — MSTest example with InvoiceService: research output, plan output, generated test file, fix cycle walkthrough, and final report

## Agent Reference

| Agent                      | Purpose              |
| -------------------------- | -------------------- |
| `code-testing-generator`   | Coordinates pipeline |
| `code-testing-researcher`  | Analyzes codebase    |
| `code-testing-planner`     | Creates test plan    |
| `code-testing-implementer` | Writes test files    |
| `code-testing-builder`     | Compiles code        |
| `code-testing-tester`      | Runs tests           |
| `code-testing-fixer`       | Fixes errors         |
| `code-testing-linter`      | Formats code         |

## Requirements

- Project must have a build/test system configured
- Testing framework should be installed (or installable)
- A local build/test environment; named agents are optional, and these roles can be handled directly or through available delegation tools

## Troubleshooting

### Tests don't compile

Resolve compilation errors directly or through an available fixer agent. Check `.testagent/plan.md` if the pipeline created it. Use `code-testing-extensions` for language-specific error references when needed (e.g., `dotnet.md` for .NET).

### Tests fail

1. Read the actual test output
2. Compare the production code, callers, and intended contract to distinguish a test mistake from a production defect
3. Correct faulty tests; report a production defect or fix it only within authorized scope. Do not change a valid expectation merely to make current behavior pass
4. Never mark tests `[Ignore]` or `[Skip]` just to make them pass

### Wrong testing framework detected

Specify your preferred framework in the initial request: "Generate Jest tests for..."

### Environment-dependent tests fail

Isolate external dependencies when they make a focused check unreliable. A local integration check is appropriate when the relevant behavior crosses that boundary; "real behavior" does not require live production services. Do not replace the production implementation with mocks that merely confirm their own setup.

### Build fails on full solution

Build and test the affected project first. Run a broader build only when project dependencies, a failure, an unresolved concern, or an applicable requirement justifies it; unrelated workspace failures are not permission to expand scope.
