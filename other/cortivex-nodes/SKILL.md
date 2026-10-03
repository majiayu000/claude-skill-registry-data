---
name: cortivex-nodes
version: 1.0.0
description: Complete reference for all Cortivex pipeline node types with configurations and usage guidance
category: reference
tags: [nodes, reference, configuration, agents, node-types]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [node-reference, node-configuration, custom-node-creation]
---

# Cortivex Node Type Reference

Every node in a Cortivex pipeline is an instance of a node type. Each node type defines a specialized agent role with default behaviors, model assignments, and configuration options.

## Node Type Summary Table

| # | Node Type | Category | Description | Default Model | Avg Cost | Avg Runtime |
|---|-----------|----------|-------------|---------------|----------|-------------|
| 1 | SecurityScanner | analysis | Scans code for vulnerabilities, insecure patterns, and dependency risks | claude-sonnet-4-20250514 | $0.004 | 15s |
| 2 | CodeReviewer | analysis | Reviews code for quality, patterns, bugs, and best practices | claude-sonnet-4-20250514 | $0.018 | 45s |
| 3 | BugHunter | analysis | Actively searches for bugs, edge cases, and logic errors | claude-sonnet-4-20250514 | $0.015 | 40s |
| 4 | PerformanceProfiler | analysis | Identifies performance bottlenecks and optimization opportunities | claude-sonnet-4-20250514 | $0.012 | 35s |
| 5 | ArchitectAnalyzer | analysis | Analyzes codebase structure, dependencies, and architecture patterns | claude-sonnet-4-20250514 | $0.020 | 50s |
| 6 | AutoFixer | modification | Automatically fixes identified issues in code | claude-sonnet-4-20250514 | $0.012 | 30s |
| 7 | LintFixer | modification | Runs linters and auto-fixes style/formatting issues | claude-haiku-4-20250414 | $0.002 | 10s |
| 8 | RefactorAgent | modification | Performs structural refactoring while preserving behavior | claude-sonnet-4-20250514 | $0.025 | 60s |
| 9 | TypeMigrator | modification | Converts JavaScript to TypeScript with type annotations | claude-sonnet-4-20250514 | $0.030 | 90s |
| 10 | DependencyUpdater | modification | Updates dependencies, resolves conflicts, applies migrations | claude-sonnet-4-20250514 | $0.008 | 20s |
| 11 | TestGenerator | testing | Generates unit tests for untested or under-tested code | claude-sonnet-4-20250514 | $0.022 | 55s |
| 12 | E2ETestWriter | testing | Generates end-to-end tests using Playwright, Cypress, or similar | claude-sonnet-4-20250514 | $0.025 | 65s |
| 13 | TestRunner | testing | Executes test suites and reports results with coverage | claude-haiku-4-20250414 | $0.003 | 60s |
| 14 | DocWriter | documentation | Generates or updates documentation (README, API docs, guides) | claude-sonnet-4-20250514 | $0.015 | 40s |
| 15 | ChangelogWriter | documentation | Generates changelogs from git history and code analysis | claude-haiku-4-20250414 | $0.004 | 12s |
| 16 | CodeExplainer | documentation | Produces human-readable explanations of code for onboarding | claude-sonnet-4-20250514 | $0.016 | 42s |
| 17 | APIDesigner | design | Designs REST/GraphQL API schemas from requirements | claude-sonnet-4-20250514 | $0.018 | 50s |
| 18 | PRCreator | integration | Creates or updates pull requests with summaries and labels | claude-haiku-4-20250414 | $0.003 | 8s |
| 19 | Orchestrator | control | Meta-node that coordinates sub-pipelines or conditional branches | claude-sonnet-4-20250514 | $0.005 | 5s |
| 20 | CustomAgent | custom | User-defined agent with fully custom system prompt and tools | configurable | varies | varies |

## Detailed Node Type Reference

---

### 1. SecurityScanner

**Category:** analysis
**Purpose:** Scans source code and dependencies for security vulnerabilities, insecure coding patterns, exposed secrets, and known CVEs in dependencies.

**When to use:**
- Before merging any PR that touches authentication, authorization, cryptography, or data handling
- As part of nightly or pre-release security audits
- When onboarding a new dependency
- After any code change to security-sensitive modules

**Default configuration:**
```yaml
- id: security_scan
  type: SecurityScanner
  config:
    model: claude-sonnet-4-20250514
    scan_depth: standard          # shallow | standard | deep
    check_dependencies: true      # scan package.json / requirements.txt / Cargo.toml etc.
    check_secrets: true           # scan for hardcoded secrets, API keys, tokens
    check_patterns: true          # scan for insecure coding patterns (SQL injection, XSS, etc.)
    severity_threshold: medium    # low | medium | high | critical (only report at or above)
    ignore_paths:                 # paths to exclude from scanning
      - node_modules/
      - vendor/
      - "*.test.*"
    cve_database: latest          # use latest CVE database
    max_files: 500                # limit to avoid excessive cost on huge repos
    output_format: structured     # structured | markdown | sarif
```

**Output:**
```json
{
  "vulnerabilities": [
    {
      "severity": "high",
      "type": "sql_injection",
      "file": "src/db/queries.ts",
      "line": 47,
      "description": "User input directly interpolated into SQL query",
      "recommendation": "Use parameterized queries",
      "cwe": "CWE-89"
    }
  ],
  "dependency_issues": [
    {
      "package": "lodash",
      "version": "4.17.15",
      "cve": "CVE-2021-23337",
      "severity": "high",
      "fix_version": "4.17.21"
    }
  ],
  "secrets_found": 0,
  "summary": {
    "total_issues": 3,
    "critical": 0,
    "high": 2,
    "medium": 1,
    "low": 0
  }
}
```

---

### 2. CodeReviewer

**Category:** analysis
**Purpose:** Performs comprehensive code review, checking for code quality, design patterns, potential bugs, naming conventions, complexity, and adherence to best practices.

**When to use:**
- On every PR before merging
- When reviewing unfamiliar code
- After large refactors to validate quality
- As part of periodic codebase quality audits

**Default configuration:**
```yaml
- id: code_review
  type: CodeReviewer
  config:
    model: claude-sonnet-4-20250514
    review_scope: changed_files   # changed_files | full | directory
    target_path: null             # specific directory to review (when scope is directory)
    check_patterns:               # what to check for
      - error-handling
      - naming-conventions
      - complexity
      - dry-violations
      - dead-code
      - type-safety
      - edge-cases
      - documentation
    max_issues: 50                # cap issues to avoid overwhelming output
    severity_levels: true         # categorize issues by severity
    suggest_fixes: true           # include fix suggestions for each issue
    ignore_patterns:              # file patterns to skip
      - "*.generated.*"
      - "*.min.*"
    complexity_threshold: 15      # cyclomatic complexity warning threshold
    line_length_limit: 120        # flag lines exceeding this length
```

**Output:**
```json
{
  "issues": [
    {
      "severity": "warning",
      "category": "complexity",
      "file": "src/utils/parser.ts",
      "line": 23,
      "description": "Function parseInput has cyclomatic complexity of 18 (threshold: 15)",
      "suggestion": "Extract nested conditionals into helper functions"
    }
  ],
  "summary": {
    "files_reviewed": 12,
    "total_issues": 7,
    "errors": 1,
    "warnings": 4,
    "info": 2
  },
  "overall_quality": "good"
}
```

---

### 3. BugHunter

**Category:** analysis
**Purpose:** Actively searches for bugs, logic errors, race conditions, off-by-one errors, null pointer issues, and other defects that could cause runtime failures.

**When to use:**
- When investigating reported bugs to find root cause and related issues
- As part of pre-release quality gates
- On complex business logic code
- After major refactors to catch regressions

**Default configuration:**
```yaml
- id: bug_hunt
  type: BugHunter
  config:
    model: claude-sonnet-4-20250514
    hunt_scope: changed_files     # changed_files | full | directory
    target_path: null
    bug_categories:               # what types of bugs to hunt
      - null-safety
      - off-by-one
      - race-conditions
      - resource-leaks
      - type-coercion
      - boundary-conditions
      - error-propagation
      - state-mutations
    include_edge_cases: true      # look for edge case inputs that could trigger bugs
    trace_data_flow: true         # follow data through call chains
    max_depth: 5                  # call chain depth for data flow analysis
    report_confidence: true       # include confidence level per finding
```

**Output:**
```json
{
  "bugs": [
    {
      "confidence": "high",
      "category": "null-safety",
      "file": "src/services/user.ts",
      "line": 89,
      "description": "user.profile accessed without null check; getUser() returns null when user is deleted",
      "reproduction": "Call getUserProfile() with a deleted user ID",
      "suggested_fix": "Add null check: if (!user?.profile) return null;"
    }
  ],
  "edge_cases": [
    {
      "file": "src/utils/math.ts",
      "line": 12,
      "description": "divide() does not handle divisor of 0",
      "input": "divide(10, 0)",
      "expected": "Error or Infinity",
      "actual": "NaN propagates silently"
    }
  ],
  "summary": {
    "bugs_found": 4,
    "high_confidence": 2,
    "medium_confidence": 1,
    "low_confidence": 1,
    "edge_cases": 3
  }
}
```

---

### 4. PerformanceProfiler

**Category:** analysis
**Purpose:** Identifies performance bottlenecks, inefficient algorithms, excessive memory allocation, N+1 queries, unnecessary re-renders, and optimization opportunities.

**When to use:**
- When users report slow performance
- Before and after performance optimization work
- As part of pre-release performance validation
- On database query code and API endpoints

**Default configuration:**
```yaml
- id: perf_profile
  type: PerformanceProfiler
  config:
    model: claude-sonnet-4-20250514
    profile_scope: changed_files  # changed_files | full | directory | hot_paths
    target_path: null
    check_categories:
      - algorithm-complexity       # O(n^2) loops, inefficient sorting, etc.
      - memory-allocation         # excessive object creation, memory leaks
      - database-queries          # N+1, missing indexes, full table scans
      - network-calls             # sequential requests that could be parallel
      - caching-opportunities     # repeated expensive computations
      - bundle-size               # large imports, tree-shaking issues
      - render-performance        # unnecessary re-renders (React/Vue)
    include_benchmarks: false     # if true, suggest benchmark code
    complexity_analysis: true     # analyze Big-O complexity of functions
```

**Output:**
```json
{
  "bottlenecks": [
    {
      "severity": "high",
      "category": "algorithm-complexity",
      "file": "src/search/filter.ts",
      "line": 34,
      "description": "Nested loop creates O(n*m) complexity; items and filters are both unbounded",
      "current_complexity": "O(n*m)",
      "suggested_complexity": "O(n+m)",
      "suggestion": "Build a Set from filters for O(1) lookup, reducing overall to O(n+m)"
    },
    {
      "severity": "medium",
      "category": "database-queries",
      "file": "src/api/orders.ts",
      "line": 67,
      "description": "N+1 query: fetching user details inside a loop over orders",
      "suggestion": "Use a JOIN or batch fetch users with an IN clause"
    }
  ],
  "summary": {
    "bottlenecks_found": 5,
    "high_severity": 1,
    "medium_severity": 3,
    "low_severity": 1,
    "estimated_impact": "2-5x improvement possible in hot paths"
  }
}
```

---

### 5. ArchitectAnalyzer

**Category:** analysis
**Purpose:** Analyzes the overall architecture of a codebase, mapping module structure, dependency graphs, design patterns in use, and providing structural understanding for downstream nodes.

**When to use:**
- As the first node in pipelines that need codebase context
- Before major refactors to understand current structure
- For onboarding documentation generation
- To detect architectural anti-patterns (circular dependencies, god modules)

**Default configuration:**
```yaml
- id: architect
  type: ArchitectAnalyzer
  config:
    model: claude-sonnet-4-20250514
    target_path: ./                # root of analysis
    analyze_dependencies: true     # map module dependency graph
    detect_patterns: true          # identify design patterns in use
    detect_antipatterns: true      # flag architectural smells
    map_entry_points: true         # identify application entry points
    language_detection: auto       # auto-detect languages
    max_depth: 10                  # directory depth for analysis
    include_metrics: true          # LOC, file count, complexity per module
    output_format: structured      # structured | markdown
    ignore_paths:
      - node_modules/
      - vendor/
      - dist/
      - build/
      - .git/
```

**Output:**
```json
{
  "architecture": {
    "type": "monolith",
    "languages": ["TypeScript", "JavaScript"],
    "framework": "Express.js",
    "entry_points": ["src/index.ts", "src/worker.ts"],
    "modules": [
      {
        "path": "src/api/",
        "purpose": "REST API route handlers",
        "files": 15,
        "loc": 2340,
        "dependencies": ["src/services/", "src/models/"]
      },
      {
        "path": "src/services/",
        "purpose": "Business logic layer",
        "files": 8,
        "loc": 1560,
        "dependencies": ["src/models/", "src/utils/"]
      }
    ],
    "patterns_detected": ["repository-pattern", "middleware-chain", "dependency-injection"],
    "antipatterns": [
      {
        "type": "circular-dependency",
        "between": ["src/services/auth.ts", "src/services/user.ts"],
        "suggestion": "Extract shared logic into src/services/identity.ts"
      }
    ]
  },
  "metrics": {
    "total_files": 87,
    "total_loc": 12450,
    "avg_complexity": 8.3,
    "test_coverage_estimate": "65%"
  }
}
```

---

### 6. AutoFixer

**Category:** modification
**Purpose:** Automatically applies fixes for issues identified by analysis nodes (SecurityScanner, CodeReviewer, BugHunter). Creates clean, minimal diffs.

**When to use:**
- After CodeReviewer or BugHunter identifies fixable issues
- To auto-remediate security vulnerabilities
- For bulk style and pattern fixes
- After linting to fix remaining issues

**Default configuration:**
```yaml
- id: auto_fix
  type: AutoFixer
  config:
    model: claude-sonnet-4-20250514
    fix_categories:               # which issue categories to fix
      - style
      - bugs
      - performance
      - security
    require_confirmation: false   # if true, show fixes before applying
    create_backup: true           # backup original files before modifying
    max_files: 50                 # limit files modified per run
    fix_mode: minimal             # minimal | comprehensive
    preserve_formatting: true     # maintain existing code style
    validate_fixes: true          # verify fix doesn't break syntax
    commit_message_prefix: "fix:" # prefix for commit messages
```

---

### 7. LintFixer

**Category:** modification
**Purpose:** Runs project linters (ESLint, Prettier, Ruff, Clippy, etc.) and auto-fixes all fixable issues. Lightweight and fast.

**When to use:**
- Before TestRunner to ensure clean code
- After code generation or migration steps
- As a quick cleanup pass

**Default configuration:**
```yaml
- id: lint_fix
  type: LintFixer
  config:
    model: claude-haiku-4-20250414
    fix_mode: auto                # auto | report-only
    config_file: auto             # auto-detect .eslintrc, .prettierrc, etc.
    typescript_rules: true        # enable TypeScript-specific rules
    format_on_save: true          # run formatter after fixing
    ignore_paths:
      - node_modules/
      - dist/
      - "*.min.*"
```

---

### 8. RefactorAgent

**Category:** modification
**Purpose:** Performs structural refactoring operations -- extracting functions/classes, renaming across codebase, reorganizing modules -- while preserving all existing behavior.

**When to use:**
- When code complexity exceeds thresholds
- To break apart god classes/modules
- To improve naming consistency
- When preparing codebase for new features

**Default configuration:**
```yaml
- id: refactor
  type: RefactorAgent
  config:
    model: claude-sonnet-4-20250514
    refactor_scope: targeted      # targeted | module | full
    target_path: null             # specific file or directory
    operations:                   # which refactoring operations to consider
      - extract-function
      - extract-class
      - rename-symbol
      - move-module
      - inline-function
      - simplify-conditional
    preserve_public_api: true     # do not change exported interfaces
    max_changes_per_file: 10      # limit changes to keep diffs reviewable
    include_tests: true           # update test imports/references
    dry_run: false
```

---

### 9. TypeMigrator

**Category:** modification
**Purpose:** Converts JavaScript files to TypeScript, adding type annotations, interfaces, and type guards. Handles JSDoc to TypeScript type conversion.

**When to use:**
- When migrating a JavaScript project to TypeScript
- When adding types to specific modules
- After scaffolding new code that needs type definitions

**Default configuration:**
```yaml
- id: type_migrate
  type: TypeMigrator
  config:
    model: claude-sonnet-4-20250514
    source_dir: src/              # directory to migrate
    strict_mode: false            # if true, no implicit any
    add_types: inferred           # inferred | explicit | minimal
    preserve_jsdoc: true          # keep JSDoc comments alongside types
    generate_interfaces: true     # extract interfaces for object shapes
    handle_imports: true          # update import paths (.js -> .ts)
    tsconfig_update: true         # update tsconfig.json include/exclude
    file_extension: .ts           # .ts | .tsx (for React components)
    batch_size: 20                # files per batch to manage cost
    skip_patterns:
      - "*.test.js"
      - "*.spec.js"
      - "*.config.js"
```

---

### 10. DependencyUpdater

**Category:** modification
**Purpose:** Updates project dependencies to latest compatible versions, resolves conflicts, applies required migration steps, and validates the update.

**When to use:**
- Scheduled weekly or monthly dependency maintenance
- When security vulnerabilities are found in dependencies
- Before major version upgrades
- As part of CI/CD dependency health checks

**Default configuration:**
```yaml
- id: dep_update
  type: DependencyUpdater
  config:
    model: claude-sonnet-4-20250514
    update_scope: all             # all | security-only | major | minor | patch
    package_manager: auto         # auto | npm | yarn | pnpm | pip | cargo
    include_dev: true             # update devDependencies too
    respect_ranges: true          # stay within semver ranges in package.json
    check_breaking: true          # review changelogs for breaking changes
    auto_migrate: true            # apply migration scripts when available
    lockfile_update: true         # regenerate lockfile after updates
    max_updates: 20               # limit updates per run
```

---

### 11. TestGenerator

**Category:** testing
**Purpose:** Generates unit tests for functions, classes, and modules that lack test coverage. Analyzes code to understand expected behavior and edge cases.

**When to use:**
- To increase test coverage on under-tested code
- After writing new features that need test coverage
- Before refactoring to establish a safety net
- As part of coverage boost campaigns

**Default configuration:**
```yaml
- id: test_gen
  type: TestGenerator
  config:
    model: claude-sonnet-4-20250514
    test_scope: uncovered         # uncovered | changed_files | directory | all
    target_path: null
    test_framework: auto          # auto | jest | mocha | pytest | vitest | go-test
    test_style: arrange-act-assert
    coverage_target: 80           # target coverage percentage
    include_edge_cases: true      # generate tests for boundary conditions
    include_error_cases: true     # generate tests for error paths
    mock_strategy: minimal        # minimal | comprehensive | none
    output_directory: auto        # auto = alongside source or in tests/ dir
    naming_convention: auto       # auto-detect from existing tests
    max_tests_per_file: 15
```

---

### 12. E2ETestWriter

**Category:** testing
**Purpose:** Generates end-to-end tests that simulate real user workflows through the application interface using Playwright, Cypress, or similar frameworks.

**When to use:**
- For critical user flows (login, checkout, onboarding)
- When unit tests alone are insufficient
- Before major releases to validate user journeys
- When adding new user-facing features

**Default configuration:**
```yaml
- id: e2e_test
  type: E2ETestWriter
  config:
    model: claude-sonnet-4-20250514
    framework: auto               # auto | playwright | cypress | selenium
    target_flows:                 # user flows to test
      - login
      - registration
      - checkout
      - navigation
    base_url: http://localhost:3000
    include_visual: false         # screenshot comparisons
    include_accessibility: true   # a11y checks within E2E tests
    browser: chromium             # chromium | firefox | webkit
    timeout_per_test: 30000       # ms per test
    retry_flaky: 2                # retry count for flaky tests
    output_directory: tests/e2e/
```

---

### 13. TestRunner

**Category:** testing
**Purpose:** Executes test suites, captures output, reports pass/fail status, coverage metrics, and performance of the test run itself.

**When to use:**
- After any code modification to validate correctness
- After AutoFixer or RefactorAgent to confirm no regressions
- As the final gate before PRCreator
- In CI/CD validation pipelines

**Default configuration:**
```yaml
- id: test_run
  type: TestRunner
  config:
    model: claude-haiku-4-20250414      # lightweight model sufficient
    test_command: auto              # auto-detect: npm test, pytest, cargo test, etc.
    coverage_enabled: true
    coverage_threshold: 80          # fail if coverage below this
    coverage_report: lcov           # lcov | text | html | json
    timeout_seconds: 300            # overall test timeout
    fail_fast: false                # stop on first failure
    parallel: true                  # run tests in parallel if framework supports
    retry_flaky: 1                  # retry failed tests once
    env_vars: {}                    # additional environment variables
    output_verbose: false           # full test output vs summary only
```

---

### 14. DocWriter

**Category:** documentation
**Purpose:** Generates or updates project documentation including README files, API docs, architecture guides, and usage examples.

**When to use:**
- After major code changes to keep docs current
- When creating a new project or module
- As part of documentation refresh campaigns
- Before public releases

**Default configuration:**
```yaml
- id: doc_write
  type: DocWriter
  config:
    model: claude-sonnet-4-20250514
    doc_types:                     # which docs to generate/update
      - readme
      - api
      - architecture
      - setup-guide
    target_path: ./
    output_format: markdown
    include_examples: true         # include code examples
    include_diagrams: false        # include mermaid diagrams
    update_mode: merge             # merge (update existing) | overwrite | create-only
    toc_generation: true           # add table of contents
    link_validation: true          # verify internal links
```

---

### 15. ChangelogWriter

**Category:** documentation
**Purpose:** Generates changelog entries from git history, PR descriptions, and code analysis. Follows Keep a Changelog format.

**When to use:**
- Before releases to document changes
- As part of PR pipelines to update CHANGELOG.md
- For automated release notes

**Default configuration:**
```yaml
- id: changelog
  type: ChangelogWriter
  config:
    model: claude-haiku-4-20250414
    format: keep-a-changelog       # keep-a-changelog | conventional | custom
    source: git-log                # git-log | pr-descriptions | both
    since: last-tag                # last-tag | last-release | <date> | <commit>
    categories:                    # changelog sections
      - Added
      - Changed
      - Deprecated
      - Removed
      - Fixed
      - Security
    include_authors: true
    include_pr_links: true
    output_file: CHANGELOG.md
    prepend: true                  # add to top of existing file
```

---

### 16. CodeExplainer

**Category:** documentation
**Purpose:** Produces human-readable explanations of code, architecture decisions, and data flows. Designed for onboarding new developers.

**When to use:**
- When creating onboarding documentation
- To explain complex algorithms or business logic
- For knowledge transfer before team changes
- To document legacy code

**Default configuration:**
```yaml
- id: explainer
  type: CodeExplainer
  config:
    model: claude-sonnet-4-20250514
    explain_scope: full            # full | module | file | function
    target_path: ./
    audience: junior               # junior | mid | senior | non-technical
    include_diagrams: true         # mermaid flow diagrams
    include_examples: true         # usage examples
    explain_why: true              # explain design decisions, not just what
    link_to_source: true           # reference file:line in explanations
    output_format: markdown
    max_depth: 3                   # how deep into call chains to explain
```

---

### 17. APIDesigner

**Category:** design
**Purpose:** Designs REST or GraphQL API schemas from requirements, including endpoint definitions, request/response schemas, authentication flows, and error handling patterns.

**When to use:**
- When designing new API endpoints
- When converting internal functions to API surfaces
- For API review and consistency checking
- When migrating between API styles (REST to GraphQL)

**Default configuration:**
```yaml
- id: api_design
  type: APIDesigner
  config:
    model: claude-sonnet-4-20250514
    api_style: rest                # rest | graphql | grpc
    spec_format: openapi-3.1      # openapi-3.1 | openapi-3.0 | graphql-schema
    include_auth: true             # design authentication endpoints
    include_pagination: true       # add pagination to list endpoints
    include_errors: true           # define error response schemas
    include_examples: true         # request/response examples
    naming_convention: kebab-case  # kebab-case | camelCase | snake_case
    versioning: url-prefix         # url-prefix | header | query-param
    output_file: api-spec.yaml
```

---

### 18. PRCreator

**Category:** integration
**Purpose:** Creates or updates pull requests with structured summaries, labels, reviewer assignments, and links to related issues.

**When to use:**
- As the final node in PR-focused pipelines
- After AutoFixer or RefactorAgent to submit changes
- For automated dependency update PRs

**Default configuration:**
```yaml
- id: pr_create
  type: PRCreator
  config:
    model: claude-haiku-4-20250414
    action: create                 # create | update | draft
    title_format: conventional     # conventional | descriptive | custom
    include_summary: true          # generate PR description from changes
    include_checklist: true        # add review checklist
    include_test_results: true     # embed test results in PR body
    labels:                        # labels to apply
      - cortivex-generated
    reviewers: []                  # GitHub usernames to request review
    draft: false                   # create as draft PR
    base_branch: main              # target branch
    link_issues: true              # auto-link related issues from commit messages
```

---

### 19. Orchestrator

**Category:** control
**Purpose:** Meta-node that coordinates sub-pipelines, conditional branching, and dynamic node generation. Used for complex workflows that need runtime decisions.

**When to use:**
- When pipeline behavior depends on runtime conditions
- To fan-out work across multiple sub-pipelines
- For A/B testing different pipeline strategies
- When dynamic node generation is needed

**Default configuration:**
```yaml
- id: orchestrate
  type: Orchestrator
  config:
    model: claude-sonnet-4-20250514
    strategy: conditional          # conditional | fan-out | priority-queue
    conditions:                    # runtime conditions for branching
      - if: "security_scan.critical_count > 0"
        then: "halt_pipeline"
        else: "continue"
    max_sub_pipelines: 5           # limit concurrent sub-pipelines
    timeout_minutes: 15            # overall orchestration timeout
    collect_results: true          # aggregate results from sub-pipelines
```

---

### 20. CustomAgent

**Category:** custom
**Purpose:** Fully customizable agent node with user-defined system prompt, tools, and behavior. Use when no built-in node type fits your needs.

**When to use:**
- For domain-specific tasks not covered by built-in nodes
- For experimental workflows
- To integrate external tools or APIs
- For one-off specialized agents

**Default configuration:**
```yaml
- id: custom_agent
  type: CustomAgent
  config:
    model: claude-sonnet-4-20250514
    system_prompt: |
      You are a specialized agent that...
      [Your custom instructions here]
    tools:                         # MCP tools to make available
      - file_read
      - file_write
      - bash
    temperature: 0.5
    max_tokens: 4096
    timeout_seconds: 300
    input_schema:                  # expected input format
      type: object
      properties:
        task: { type: string }
    output_schema:                 # expected output format
      type: object
      properties:
        result: { type: string }
        status: { type: string, enum: [success, failure] }
```

## Creating Custom Node Types

To create a reusable custom node type, define it in a YAML file:

```yaml
# custom-nodes/MarkdownLinter.yaml
node_type:
  name: MarkdownLinter
  category: documentation
  description: Lints markdown files for style, broken links, and formatting issues
  default_model: claude-haiku-4-20250414

  system_prompt: |
    You are a markdown documentation linter. Analyze markdown files for:
    - Broken internal links
    - Inconsistent heading levels
    - Missing alt text on images
    - Spelling and grammar issues
    - Formatting inconsistencies

    Report issues in structured JSON format.

  default_config:
    check_links: true
    check_spelling: true
    check_formatting: true
    style_guide: google           # google | microsoft | custom
    ignore_patterns:
      - CHANGELOG.md
      - node_modules/

  input_schema:
    type: object
    properties:
      target_path:
        type: string
        description: Directory containing markdown files

  output_schema:
    type: object
    properties:
      issues:
        type: array
        items:
          type: object
          properties:
            file: { type: string }
            line: { type: number }
            severity: { type: string }
            message: { type: string }
      summary:
        type: object
        properties:
          files_checked: { type: number }
          total_issues: { type: number }
```

Register custom node types with:

```
cortivex_nodes({
  action: "register",
  definition_file: "custom-nodes/MarkdownLinter.yaml"
})
```

Then use it in pipelines like any built-in node:

```yaml
nodes:
  - id: lint_docs
    type: MarkdownLinter
    config:
      target_path: docs/
      check_links: true
```

## Node Selection Guide

Use this decision tree to select the right node type:

**Need to analyze code without changing it?**
- Security concerns -> SecurityScanner
- Code quality/patterns -> CodeReviewer
- Finding bugs -> BugHunter
- Performance issues -> PerformanceProfiler
- Understanding structure -> ArchitectAnalyzer

**Need to modify code?**
- Fix identified issues -> AutoFixer
- Fix lint/style issues -> LintFixer
- Structural changes -> RefactorAgent
- Add TypeScript types -> TypeMigrator
- Update dependencies -> DependencyUpdater

**Need to test code?**
- Generate unit tests -> TestGenerator
- Generate E2E tests -> E2ETestWriter
- Run existing tests -> TestRunner

**Need documentation?**
- READMEs, API docs, guides -> DocWriter
- Release notes/changelogs -> ChangelogWriter
- Code explanations for humans -> CodeExplainer

**Need to design?**
- API schemas and endpoints -> APIDesigner

**Need integration?**
- Create/update PRs -> PRCreator

**Need control flow?**
- Conditional branching, sub-pipelines -> Orchestrator

**None of the above?**
- Build your own -> CustomAgent

## Reasoning Protocol

Before selecting a node type, reason through explicitly:

1. **What is the primary action?** Categorize as: analyze, modify, test, document, design, integrate, or control. This narrows the candidates immediately.
2. **Does the task require code changes?** If no, use an analysis node. If yes, use a modification node followed by a validation node.
3. **What model tier is appropriate?** Tasks requiring deep reasoning (CodeReviewer, BugHunter, RefactorAgent) need Sonnet. Mechanical tasks (LintFixer, TestRunner, PRCreator) work well with Haiku at a fraction of the cost.
4. **Is there a built-in node that fits?** Check the 20 node types above before resorting to CustomAgent. CustomAgent should be the exception, not the default.
5. **What output does the downstream node need?** Select nodes that produce the output format expected by the next node in the pipeline.

Think step-by-step through the decision tree above. State your reasoning before selecting a node type.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Using CodeReviewer when you need BugHunter | CodeReviewer checks style and patterns; BugHunter finds runtime bugs | Match the node to the specific problem type |
| Using Sonnet for LintFixer | Paying 10x more for a task Haiku handles identically | Use the default model unless you have evidence it underperforms |
| CustomAgent for everything | Loses the benefit of specialized prompts and configurations | Only use CustomAgent when no built-in node fits |
| SecurityScanner on a docs-only repo | Wastes cost scanning files with no security surface | Add conditions to skip nodes when irrelevant |
| TestGenerator without TestRunner | Generates tests but never verifies they actually pass | Always follow test generation with test execution |
| ArchitectAnalyzer at the end of a pipeline | Analysis output is only useful before modification nodes | Place analysis nodes at the start |
| Omitting output format configuration | Downstream nodes may not parse the output correctly | Set `output_format: structured` for machine consumption |

**WRONG:**
```yaml
# Wrong node for the job
- id: find_bugs
  type: CodeReviewer      # CodeReviewer checks patterns, not bugs
  config:
    model: claude-sonnet-4-20250514
    check_patterns: [bugs]  # This is a style check, not bug hunting
```

**RIGHT:**
```yaml
# Correct node for bug finding
- id: find_bugs
  type: BugHunter
  config:
    model: claude-sonnet-4-20250514
    bug_categories: [null-safety, race-conditions, boundary-conditions]
    trace_data_flow: true
```

## Grounding Rules

- **Cannot decide between two node types:** Ask yourself what the primary output should be. If it is a list of issues to review, use an analysis node. If it is modified source code, use a modification node.
- **Node produces poor quality output:** Before switching to a more expensive model, check if the configuration is correct. A misconfigured Sonnet node will underperform a well-configured Haiku node.
- **Need a capability not covered by built-in nodes:** Create a CustomAgent with a clear, specific system prompt. Do not write vague instructions like "analyze the code" -- specify exactly what to look for and what format to produce.
- **Unsure about cost estimates:** The cost column in the summary table reflects median runs on medium-sized repositories (50-200 files). Scale estimates linearly with file count for larger repos.

## Advanced Capabilities

### Custom Node Creation

Register new node types at runtime via the `cortivex_node_register` MCP tool for dynamic node creation from pipelines or scripts.

```json
{
  "method": "cortivex_node_register",
  "params": {
    "name": "ComplianceAuditor",
    "category": "analysis",
    "description": "Audits code for regulatory compliance (SOC2, HIPAA, GDPR)",
    "default_model": "claude-sonnet-4-20250514",
    "system_prompt": "Analyze source code for regulatory framework violations.",
    "default_config": { "framework": "SOC2", "severity_threshold": "medium" },
    "input_schema": {
      "type": "object",
      "properties": {
        "target_path": { "type": "string" },
        "framework": { "type": "string", "enum": ["SOC2", "HIPAA", "GDPR"] }
      }
    }
  }
}
```

Registration response:
```json
{ "result": { "node_type": "ComplianceAuditor", "registered": true, "id": "custom_node_a7f3" } }
```

### Node Performance Profiling

Every node execution emits telemetry conforming to this schema for capacity planning and cost attribution.

```json
{
  "title": "NodePerformanceMetrics",
  "type": "object",
  "properties": {
    "node_id": { "type": "string" },
    "node_type": { "type": "string" },
    "pipeline_run_id": { "type": "string" },
    "timing": {
      "type": "object",
      "properties": { "queue_wait_ms": { "type": "number" }, "execution_ms": { "type": "number" }, "total_ms": { "type": "number" } }
    },
    "tokens": { "input_tokens": { "type": "integer" }, "output_tokens": { "type": "integer" } },
    "cost_usd": { "type": "number" },
    "outcome": { "type": "string", "enum": ["success", "partial", "failure", "timeout"] }
  }
}
```

### Auto-Scaling Node Configurations

Configure auto-scaling rules that adjust concurrency, model tier, and batch sizes based on queue depth and latency.

```yaml
auto_scaling:
  enabled: true
  rules:
    - node_type: CodeReviewer
      min_instances: 1
      max_instances: 8
      scale_up: { metric: queue_depth, threshold: 10, cooldown_seconds: 60 }
      scale_down: { metric: idle_time_seconds, threshold: 120 }
      model_fallback:
        primary: claude-sonnet-4-20250514
        fallback: claude-haiku-4-20250414
        fallback_trigger: queue_depth > 25
    - node_type: TestRunner
      min_instances: 2
      max_instances: 12
      scale_up: { metric: pending_jobs, threshold: 5 }
      batch_config: { max_batch_size: 10, batch_timeout_seconds: 15 }
  global_limits:
    max_total_instances: 30
    max_cost_per_hour_usd: 50.00
    circuit_breaker: { error_rate_threshold: 0.25, evaluation_window_seconds: 300 }
```

### Node Chaining Patterns

The `cortivex_node_chain` MCP tool defines multi-step sequences where each node's output feeds into the next. Use `depends_on` and `input_map` to wire outputs to downstream inputs.

```json
{
  "method": "cortivex_node_chain",
  "params": {
    "chain_id": "security-fix-verify",
    "nodes": [
      { "id": "scan", "type": "SecurityScanner", "config": { "scan_depth": "deep" } },
      {
        "id": "fix", "type": "AutoFixer", "depends_on": "scan",
        "input_map": { "issues": "$.scan.vulnerabilities" },
        "config": { "fix_categories": ["security"] }
      },
      { "id": "verify", "type": "TestRunner", "depends_on": "fix", "config": { "fail_fast": true } }
    ],
    "on_failure": "halt"
  }
}
```

Response with execution handle:

```json
{ "result": { "chain_id": "security-fix-verify", "execution_id": "exec_8b2c4d1f", "status": "running", "current_node": "scan", "progress": { "completed": 0, "total": 3 }, "estimated_completion_seconds": 105 } }
```

### Cost-Optimized Model Selection

Evaluate model options per node against latency and quality constraints. The cost analysis API recommends assignments that minimize spend while meeting SLA targets.

```json
{
  "title": "CostAnalysisRequest",
  "type": "object",
  "properties": {
    "pipeline_id": { "type": "string" },
    "optimization_target": { "type": "string", "enum": ["minimize_cost", "minimize_latency", "balance"] },
    "constraints": {
      "max_cost_per_run_usd": { "type": "number" },
      "max_latency_seconds": { "type": "number" },
      "min_quality_score": { "type": "number", "minimum": 0, "maximum": 1 }
    },
    "node_overrides": [{ "node_id": { "type": "string" }, "locked_model": { "type": "string" } }]
  },
  "required": ["pipeline_id", "optimization_target"]
}
```

The response provides per-node recommendations with projected savings:

```typescript
interface CostAnalysisResult {
  pipeline_id: string;
  recommendations: Array<{
    node_id: string;
    current_model: string;
    recommended_model: string;
    quality_delta: number;       // -1.0 to 1.0
    cost_reduction_pct: number;
    latency_delta_ms: number;
  }>;
  summary: { current_cost_per_run: number; optimized_cost_per_run: number; total_savings_pct: number; quality_impact: "none" | "minimal" | "moderate"; nodes_changed: number };
}
```

## Security Hardening (OWASP AST10 Aligned)

### AST03: Per-Node Permission Manifests

Every node declares a permission manifest (AST03 -- Excessive Permissions) enumerating allowed file paths, tools, and network access. The runtime denies anything not listed.

```yaml
node_permissions:
  SecurityScanner:
    filesystem: { read: ["src/**", "lib/**", "package.json", "Cargo.toml"], write: [] }
    tools: { allowed: [file_read, grep, glob], denied: [file_write, bash, file_delete] }
    network: { allowed_hosts: ["cve.circl.lu", "osv.dev"], denied: ["*"] }
  AutoFixer:
    filesystem: { read: ["src/**", "lib/**", "tests/**"], write: ["src/**", "lib/**"] }
    tools: { allowed: [file_read, file_write, grep, glob], denied: [bash, file_delete] }
    network: { denied: ["*"] }
  TestRunner:
    filesystem: { read: ["**/*"], write: ["/tmp/**", "coverage/**"] }
    tools: { allowed: [file_read, bash], denied: [file_write, file_delete] }
    network: { allowed_hosts: ["localhost"], denied: ["*"] }
```

```json
{ "method": "cortivex_permission_validate", "params": { "node_type": "AutoFixer", "requested_access": { "filesystem_write": ["src/utils/parser.ts"], "tools": ["file_write"] } } }
```

### AST06: Shell Command Allowlists for TestRunner and CustomAgent

Only TestRunner and CustomAgent may invoke shell commands (AST06 -- Excessive Agency), both under strict allowlists.

```yaml
shell_policy:
  enforcement: strict
  default_action: deny
  TestRunner:
    allowed_commands:
      - { pattern: "npm test*", timeout_seconds: 300 }
      - { pattern: "npx jest*", timeout_seconds: 300 }
      - { pattern: "pytest*", timeout_seconds: 300 }
      - { pattern: "cargo test*", timeout_seconds: 300 }
    blocked_patterns: ["rm *", "curl *", "wget *", "*| bash*", "sudo *"]
  CustomAgent:
    allowed_commands: []              # must be explicitly configured per-instance
    require_explicit_allowlist: true
    blocked_patterns: ["rm -rf *", "eval *", "exec *", "sudo *", "> /dev/*"]
  argument_sanitization: { strip_shell_metacharacters: true, block_path_traversal: true }
```

```json
{ "method": "cortivex_shell_validate", "params": { "node_type": "TestRunner", "command": "npm test -- --coverage" } }
```

### Secret Handling During SecurityScanner Execution

SecurityScanner detects secrets but must never persist them to disk or logs (in-memory only, zeroized on completion).

```yaml
secret_handling:
  SecurityScanner:
    detection: { patterns: ["API[_-]?KEY", "SECRET[_-]?KEY", "PRIVATE[_-]?KEY", "ghp_[a-zA-Z0-9]{36}"] }
    output_policy: { redact_values: true, report_location_only: true, max_context_chars: 40 }
    storage: { persist_to_disk: false, persist_to_logs: false, memory_policy: zeroize_on_complete }
```

```json
{ "method": "cortivex_secret_policy_check", "params": { "node_type": "SecurityScanner", "checks": ["no_disk_persistence", "output_redaction", "memory_zeroization"] } }
```

### Custom Node Registration Validation

Custom node registration (AST03, AST06) validates definitions to reject unsafe system prompts and excessive tool requests.

```typescript
const registrationPolicy = {
  system_prompt_checks: {
    block_patterns: ["ignore previous instructions", "act as root", "bypass security", "disable safety"],
    max_length: 10000,
    require_role_declaration: true,
  },
  tool_access_checks: {
    max_tools: 5,
    prohibited_tools: ["file_delete", "process_kill", "env_set", "network_raw"],
  },
  resource_checks: { max_timeout_seconds: 600, max_tokens: 16384, max_output_size_bytes: 1048576 },
};
```

```json
{ "method": "cortivex_node_register", "params": { "name": "ComplianceAuditor", "system_prompt": "You are a compliance auditing agent.", "tools": ["file_read", "grep"], "validate_security": true } }
```

```json
{ "registered": false, "validation_errors": [{ "check": "system_prompt_checks", "reason": "Blocked pattern detected", "ast_risk": "AST03" }, { "check": "tool_access_checks", "reason": "Tool 'file_delete' is prohibited", "ast_risk": "AST06" }] }
```

### Model Tier Enforcement

Security-critical nodes require minimum model capability (AST06) to prevent false negatives from underpowered models.

```yaml
model_tier_enforcement:
  tiers:
    tier_1_high:
      minimum_model: claude-sonnet-4-20250514
      applies_to: [SecurityScanner, BugHunter, RefactorAgent]
    tier_2_standard:
      minimum_model: claude-sonnet-4-20250514
      applies_to: [CodeReviewer, ArchitectAnalyzer, AutoFixer, TestGenerator]
    tier_3_lightweight:
      minimum_model: claude-haiku-4-20250414
      applies_to: [LintFixer, TestRunner, PRCreator, ChangelogWriter]
  overrides: { allow_downgrade: false, allow_upgrade: true, audit_downgrades: true }
```

```json
{ "method": "cortivex_model_tier_check", "params": { "pipeline": "security-audit", "node_assignments": [{ "node_id": "security_scan", "type": "SecurityScanner", "model": "claude-haiku-4-20250414" }] } }
```

```json
{ "valid": false, "violations": [{ "node_id": "security_scan", "assigned_model": "claude-haiku-4-20250414", "minimum_required": "claude-sonnet-4-20250514", "tier": "tier_1_high", "ast_risk": "AST06" }] }
