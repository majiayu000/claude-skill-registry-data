---
name: pair-capability-design-manual-tests
description: "Designs a manual test suite for post-release validation by analyzing the project's artifacts, architecture, and deployment targets. Generates critical path files (CP*.md) and a suite README following manual-testing guidelines and the manual-test-case-template. Invocable independently or as a prerequisite of /pair-capability-execute-manual-tests."
version: 0.4.1
author: Foomakers
---

# /pair-capability-design-manual-tests — Manual Test Suite Designer

Analyze a project's released artifacts, deployment targets, and user-facing surfaces to generate a complete manual test suite. Produces critical path files (`CP*.md`) and a suite `README.md` in the test suite directory.

Each test case follows the [manual-test-case-template](../../../.pair/knowledge/guidelines/collaboration/templates/manual-test-case-template.md). For design principles, see [manual-testing.md](../../../.pair/knowledge/guidelines/quality-assurance/manual-testing.md). For the organizational context, see [manual-verification.md](../../../.pair/knowledge/guidelines/quality-assurance/manual-verification.md).

## Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `$output` | No | Directory where suite files are written. Default: `qa/release-validation/` at project root. |
| `$scope` | No | Artifact categories to cover: `website`, `cli`, `dataset`, `registry`, `all` (default: `all`). Comma-separated for multiple. |

## Algorithm

Execute in sequence. For every step, follow the **check → skip → act → verify** pattern.

### Step 1: Check Existing Suite

1. **Check**: Does `$output` already contain `CP*.md` files?
2. **Skip**: If suite exists and is non-empty → present current coverage summary, ask: _"Suite already exists with N critical paths, N test cases. Regenerate from scratch, extend, or abort?"_
   - **Regenerate**: proceed to Step 2 (overwrites).
   - **Extend**: proceed to Step 2 but merge new tests into existing CPs (append, no duplicates).
   - **Abort**: HALT.
3. **Act**: Create `$output` directory if it doesn't exist.
4. **Verify**: Output directory ready.

### Step 2: Discover Project Surfaces

Analyze the project to build an inventory of testable surfaces. For each category, read the relevant sources:

1. **Check**: Which artifact categories are in `$scope`?
2. **Act**: For each category in scope, discover:

| Category | Discovery Sources | What to Extract |
| --- | --- | --- |
| **Website** | Deployment config, `package.json` scripts, adoption files, sitemap, route files | Base URL, page routes, interactive features (search, forms), responsive breakpoints, meta tags, accessibility targets |
| **CLI** | `package.json` `bin` field, Commander command definitions, `--help` output | Command names, flags, positional args, exit code expectations, output formats |
| **Dataset** | KB config files, registry definitions, adoption files | Registries, install strategies (mirror/add), validation commands, expected directory structure |
| **Registry** | `package.json` `publishConfig`, workflow files, adoption files | Package scope, registry URL, publish mechanism, expected metadata |

1. **Act**: For each category, also read:
   - **PRD** (`.pair/product/adopted/PRD.md`) — for user-facing requirements and acceptance criteria
   - **Architecture** (`.pair/adoption/tech/architecture.md`) — for deployment topology
   - **Way of working** (`.pair/adoption/tech/way-of-working.md`) — for release process, quality gates
   - **Tech stack** (`.pair/adoption/tech/tech-stack.md`) — for framework specifics (e.g., Next.js → check SSR, static pages)

2. **Verify**: Surface inventory built. Present to user:

```text
DISCOVERED SURFACES:
├── Website: [N pages, N interactive features, N responsive breakpoints]
├── CLI: [N commands, N flags]
├── Dataset: [N registries, N validation rules]
└── Registry: [N packages, N distribution channels]
```

Ask: _"Proceed with these surfaces? Add or remove anything?"_

### Step 3: Design Critical Paths

For each category, design critical paths ordered by release risk.

1. **Act**: Apply the following heuristic to group tests:

| CP Pattern | Category | Priority | Covers |
| --- | --- | --- | --- |
| CP1 | Website Critical Path | P0 | Landing loads, core navigation, responsive, meta tags, favicon, key CTAs |
| CP2 | CLI Artifact Critical Path | P0 | Checksum verification, extraction, binary execution, version output |
| CP3 | CLI Functional Path | P0-P1 | Install, update, key commands, error handling, idempotency |
| CP4 | Dataset Validation | P1 | KB structure, validation commands, content integrity |
| CP5 | Website Docs Completeness | P1 | All doc pages return 200, sidebar matches routes |
| CP6 | Website Search & Navigation | P1-P2 | Search functionality, responsive navigation, 404 handling |
| CP7 | Registry Publish | P2 | Package visibility, install from registry, functional after install |

- **Skip** CPs for categories not in `$scope`.
- **Merge** if a category has very few tests (< 3) — combine into the nearest related CP.
- **Split** if a category has many tests (> 20) — break into sub-CPs (e.g., CP3a, CP3b).

1. **Verify**: CP plan built. Present CP outline with estimated test counts before generating files.

### Step 4: Generate Test Cases

For each CP, generate individual test cases.

1. **Act**: For each test case:
   - Assign ID: `MT-CP{N}{NN}` (e.g., `MT-CP101`, `MT-CP201`)
   - Set priority: P0 (blocks release) / P1 (important) / P2 (nice-to-have)
   - Define preconditions (reference earlier test IDs where needed)
   - Write concrete, observable steps using variables (`$VERSION`, `$BASE_URL`, `$WORKDIR`, `$RELEASE_URL`, `$REGISTRY`)
   - Write objective expected results (HTTP status, exit code, file existence, string match — no subjective criteria)
   - Add notes for edge cases, platform differences, related tests

2. **Act**: Apply test design principles from [manual-testing.md](../../../.pair/knowledge/guidelines/quality-assurance/manual-testing.md):
   - **Version-agnostic**: never hardcode versions
   - **Environment-isolated**: filesystem tests use `$WORKDIR`
   - **Idempotent**: re-running produces same result
   - **Observable**: every step has verifiable output
   - **Atomic**: one test = one concern

3. **Verify**: Each CP has a balanced distribution of P0/P1/P2 tests. P0 tests cover release blockers only.

### Step 5: Generate Suite README

1. **Act**: Write `$output/README.md` with:
   - **Variables** section: list all variables with descriptions and resolution strategy
   - **Execution order**: CP1 → CP2 → ... → CPN
   - **Tool strategy table**: which tools to use for each test category
   - **Preconditions**: what must be ready before execution (e.g., release published, website deployed)
   - **Context management**: how to maintain state across CPs (e.g., `$WORKDIR` shared)

2. **Verify**: README is self-contained — an agent reading only README + CP files can execute the full suite.

### Step 6: Write Files

1. **Act**: Write all files to `$output/`:
   - `README.md` — suite overview
   - `CP{N}-{slug}.md` — one file per critical path (e.g., `CP1-website-critical-path.md`)

2. **Verify**: All files written. Present summary:

```text
MANUAL TEST SUITE GENERATED:
├── Output:  [{output path}]
├── Files:   [N critical path files + README]
├── Tests:   [N total (N P0, N P1, N P2)]
├── Categories: [list]
└── Ready for: /pair-capability-execute-manual-tests
```

## Composition Interface

When composed by `/pair-capability-execute-manual-tests` (Step 1 gate):

- **Input**: `/pair-capability-execute-manual-tests` detects no suite → suggests running `/pair-capability-design-manual-tests`.
- **Output**: Returns the suite directory path. `/pair-capability-execute-manual-tests` can then re-invoke with `$suite` pointing to the generated directory.

When invoked **independently**:

- Generates the full suite and presents the summary.
- User can then invoke `/pair-capability-execute-manual-tests` to run it.

## Notes

- This skill **generates test definitions** — it does not execute tests or modify application code.
- Test case IDs are stable across regenerations if the same surfaces are discovered.
- The skill is idempotent: re-running on an existing suite offers regenerate/extend/abort.
- Generated test cases are version-agnostic by design — they work across releases without modification.
- Suite maintenance (adding tests for new features) should re-invoke this skill with `extend` mode.
