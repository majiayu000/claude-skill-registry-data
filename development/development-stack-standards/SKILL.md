---
name: development-stack-standards
description: Development stack standards - five-level maturity model, dimension specs, assessment criteria, tool guidance
---

# Development Stack Standards

Reference for creating and assessing language-specific development stacks. Defines what constitutes a complete stack, maturity progression, assessment criteria.

**Used by:**
- `/stack-assess` - Grade projects against stack standards
- `/stack-guide` - Create/validate/customize stack definitions
- Stack skills (configuring-python-stack, configuring-javascript-stack, etc.)

## Five-Level Maturity Model

### Level 0: Foundation (EVERY project)

**Dimensions:** 8 required

| Dimension | Purpose | Required Capabilities |
|-----------|---------|----------------------|
| **Package manager** | Reproducible builds | Install deps, lockfile, isolation (venv/node_modules) |
| **Format** | Consistent style | Auto-fix, deterministic, configurable line length |
| **Lint** | Catch bugs | Auto-fix safe changes, configurable rules |
| **Typecheck** | Static correctness | Type analysis, strict mode available |
| **Test** | Verify behavior | Unit tests, fast execution |
| **Coverage** | Measure testing | Line/branch/function measurement, reporting |
| **Build** | Create artifacts | Package for distribution |
| **Clean** | Reset state | Remove generated files, dependencies |

**Justfile recipes:** (implements aug-just/justfile-interface Level 0)
- `dev-install` - Setup environment
- `format` - Auto-fix formatting
- `lint` - Auto-fix linting
- `typecheck` - Static type checking
- `test` - Run unit tests
- `coverage` - Measure coverage (any threshold)
- `build` - Create artifacts
- `clean` - Remove generated files
- `check-all` - Run all checks (format → lint → typecheck → coverage)
- `default` - Show available commands

**When:** All projects, no exceptions

**Assessment:**
- All 8 dimensions present?
- All 10 justfile recipes present?
- Can fresh clone execute `just dev-install && just check-all`?

---

### Level 1: Quality Gates (CI/CD)

**Adds:** 4 dimensions

| Dimension | Purpose | Required Capabilities |
|-----------|---------|----------------------|
| **Coverage threshold** | Enforce testing | 96% threshold, fail on miss, unit tests only |
| **Complexity check** | Limit complexity | Cyclomatic complexity ≤10, auto-check in lint |
| **Test separation** | Isolate slow tests | Unit (fast, coverage-gated) vs integration (slow, no threshold) |
| **Test watch** | Fast feedback | Continuous test execution on file changes |

**Justfile adds:**
- `test-watch` - Continuous testing
- `integration-test` - Integration tests, no threshold, never blocks
- `complexity` - Detailed complexity report (informational)
- `loc` - Largest files by lines of code

**Updates:**
- `coverage` - Now enforces 96% threshold for unit tests only
- `lint` - Now checks complexity ≤10

**When:** CI/CD pipeline, multiple developers, quality enforcement

**Assessment:**
- Coverage fails below 96% for unit tests?
- Complexity threshold ≤10 enforced?
- Integration tests marked/tagged?
- Integration tests excluded from coverage threshold?

---

### Level 2: Security & Compliance (Production)

**Adds:** 4 dimensions

| Dimension | Purpose | Required Capabilities |
|-----------|---------|----------------------|
| **Vulnerability scanning** | Security | Scan dependencies for CVEs, severity reporting |
| **License analysis** | Compliance | List all licenses, flag GPL/restrictive, prod vs dev |
| **SBOM** | Supply chain | Generate CycloneDX SBOM, all dependencies |
| **Dependency tracking** | Freshness | List outdated packages, update recommendations |

**Justfile adds:**
- `deps` - Show outdated packages
- `vulns` - Scan for vulnerabilities
- `lic` - Analyze licenses
- `sbom` - Generate software bill of materials

**When:** Production deployment, security requirements, compliance needs

**Assessment:**
- Vulnerability scanner configured?
- License checker present?
- SBOM generation works?
- Dependency update tracking available?

---

### Level 3: Metrics (Large codebases)

**Adds:** Detailed analysis (already have basic from Level 1)

| Dimension | Purpose | Required Capabilities |
|-----------|---------|----------------------|
| **Complexity reporting** | Refactoring targets | File-by-file analysis, avg/max metrics |
| **LOC analysis** | Size tracking | Lines by file, identify large files |

**Justfile:** Uses existing `complexity` and `loc` from Level 1

**When:** Refactoring needs, large codebases, technical debt management

**Assessment:**
- Complexity reporting detailed enough for refactoring decisions?
- LOC tracking identifies largest files?

---

### Level 4: Polyglot (Multi-language)

**Structure:** Root justfile orchestrates language-specific subprojects

**Root commands:** Subset (orchestration only)
- `dev-install`, `check-all`, `clean`, `build`, `deps`, `vulns`, `lic`, `sbom`
- Delegates to subprojects via `_run-all`

**Subproject commands:** Full interface (each implements Level 0+)

**When:** Multiple languages, monorepo, microservices

**Assessment:**
- Root orchestrates without duplication?
- Each subproject standalone (`cd api && just check-all`)?
- `_run-all` fails fast?

---

## Dimension Specifications

### Package Management

**Purpose:** Reproducible dependency installation

**Required capabilities:**
- Install dependencies from manifest
- Generate/maintain lockfile
- Isolation (virtual env, node_modules, local Maven repo)

**Examples:**
- Python: uv (fast, handles venv + install + lock)
- JavaScript: pnpm (fast, efficient, good lockfile)
- Java: Maven (standard, handles everything)

**Assessment questions:**
- Can fresh clone install dependencies? (`just dev-install`)
- Is lockfile committed?
- Are dependencies isolated from system?

**Config files:**
- Python: `pyproject.toml`, `uv.lock`
- JavaScript: `package.json`, `pnpm-lock.yaml`
- Java: `pom.xml`, `pom.xml.lock` (if using Lockfile Plugin)

---

### Code Formatting

**Purpose:** Consistent style, zero bikeshedding

**Required capabilities:**
- Auto-fix (modify files in place)
- Deterministic (same input → same output)
- Configurable (line length, indent size)

**Examples:**
- Python: ruff (fast, opinionated, handles format + lint)
- JavaScript: prettier (standard, works everywhere)
- Java: spotless + Google Java Format (standard for Java)

**Assessment questions:**
- Does `just format` succeed?
- Is config file present?
- Does `just format` change files, then second run changes nothing?

**Config files:**
- Python: `pyproject.toml` → `[tool.ruff]` section
- JavaScript: `.prettierrc`
- Java: `pom.xml` → spotless plugin config

**Standard settings:**
- Line length: 100 (balance readability vs horizontal space)
- Indent: Language default (4 for Python, 2 for JS, 2 for Java)

---

### Linting

**Purpose:** Catch bugs, enforce patterns

**Required capabilities:**
- Auto-fix safe changes
- Configurable rules
- Complexity checking (Level 1+)

**Examples:**
- Python: ruff (fast, handles format + lint + import sort)
- JavaScript: eslint (standard, many plugins)
- Java: spotbugs (static analysis, bug detection)

**Assessment questions:**
- Does `just lint` succeed?
- Are rules configured?
- Does lint auto-fix safe issues?
- Is complexity threshold ≤10 enforced? (Level 1+)

**Config files:**
- Python: `pyproject.toml` → `[tool.ruff]` section
- JavaScript: `eslint.config.js`
- Java: `pom.xml` → spotbugs + checkstyle plugins

**Standard rules:**
- Level 0: Error detection, code quality
- Level 1: Add complexity check (≤10)

---

### Type Checking

**Purpose:** Catch type errors before runtime

**Required capabilities:**
- Static type analysis
- Strict mode available
- IDE integration (LSP)

**Examples:**
- Python: mypy (standard, strict mode)
- JavaScript/TypeScript: tsc (built into TypeScript)
- Java: javac (built into compiler)

**Assessment questions:**
- Does `just typecheck` succeed?
- Is strict mode enabled?
- Are type annotations required/present?

**Config files:**
- Python: `pyproject.toml` → `[tool.mypy]` with `strict = true`
- JavaScript: `tsconfig.json` with `strict: true`
- Java: `pom.xml` compiler settings (warnings as errors)

**Standard settings:**
- Strict mode enabled
- Disallow untyped code
- Treat type errors as failures

---

### Testing

**Purpose:** Verify correctness, enable refactoring

**Required capabilities:**
- Unit test execution
- Fast (Level 0: any speed, Level 1: fast subset)
- Watch mode (Level 1+)
- Integration separation (Level 1+)

**Examples:**
- Python: pytest (standard, powerful, fast)
- JavaScript: vitest (fast, modern, good DX)
- Java: JUnit 5 (standard, modern features)

**Assessment questions:**
- Tests exist?
- Does `just test` run unit tests?
- Are unit/integration separated? (Level 1+)
- Does `just test-watch` work? (Level 1+)

**Config files:**
- Python: `pyproject.toml` → `[tool.pytest.ini_options]` with markers
- JavaScript: `vitest.config.ts`
- Java: `pom.xml` → surefire plugin, use JUnit 5 tags

**Test organization:**
- Level 0: Tests exist, run via `just test`
- Level 1: Separation (unit fast, integration marked/tagged)
- Marker examples: `@pytest.mark.integration`, `@Tag("integration")`

---

### Coverage

**Purpose:** Measure test completeness

**Required capabilities:**
- Line/branch/function coverage
- Threshold enforcement
- HTML reports
- Exclude integration tests from threshold (Level 1+)

**Examples:**
- Python: pytest-cov (pytest plugin)
- JavaScript: vitest coverage (built-in)
- Java: JaCoCo (Maven plugin)

**Assessment questions:**
- Coverage measured?
- Threshold enforced? (Level 1: 96%)
- Integration tests excluded from threshold? (Level 1+)
- HTML report generated?

**Config files:**
- Python: `pyproject.toml` → `[tool.coverage.report]` with `fail_under = 96`
- JavaScript: `vitest.config.ts` → coverage thresholds 96
- Java: `pom.xml` → JaCoCo plugin with 0.96 minimum

**Thresholds:**
- Level 0: Coverage measured (any threshold or none)
- Level 1: 96% for unit tests, no threshold for integration

**Rationale for 96%:**
- High enough to ensure thorough testing
- Allows 4% for legitimately hard-to-test code
- Prevents "get to 100% by testing trivial code" waste

---

### Complexity

**Purpose:** Limit function complexity, identify refactoring targets

**Required capabilities:**
- Cyclomatic complexity measurement
- Threshold enforcement (Level 1: ≤10)
- Detailed reporting (file-by-file, avg/max)

**Examples:**
- Python: radon (detailed reports), ruff (threshold enforcement)
- JavaScript: eslint complexity rule, @pnpm/complexity
- Java: checkstyle (threshold), PMD (detailed reports)

**Assessment questions:**
- Complexity threshold ≤10 enforced? (Level 1+)
- Detailed reporting available? (Level 3+)
- Are violations caught in `just lint`?

**Config files:**
- Python: ruff for threshold, radon for reporting
- JavaScript: eslint.config.js complexity rule, pnpm dlx for reporting
- Java: checkstyle for threshold, PMD for reporting

**Thresholds:**
- Level 1: Max complexity ≤10 enforced
- Level 3: Detailed reporting for refactoring decisions

**Rationale for ≤10:**
- Functions with complexity >10 harder to understand and test
- Standard threshold in many style guides
- Encourages small, focused functions

---

### LOC (Lines of Code)

**Purpose:** Identify large files, track codebase size

**Required capabilities:**
- Count lines by file
- Sort by size
- Language filtering

**Examples:**
- Python: pygount (Python ecosystem tool)
- JavaScript: cloc (universal, widely available)
- Java: cloc (universal)

**Assessment questions:**
- Can identify N largest files?
- Output readable/parseable?

**Justfile pattern:**
```just
loc N="20":
    @echo "📊 Top {{N}} largest files by LOC:"
    @[language-specific command] | sort -rn | head -{{N}}
```

**Tool choice:**
- Ecosystem tool preferred if available and good
- Universal tool (cloc) acceptable
- Any tool that counts accurately

---

### Vulnerability Scanning (Level 2)

**Purpose:** Identify known security vulnerabilities in dependencies

**Required capabilities:**
- Scan dependencies for CVEs
- Severity reporting (critical/high/medium/low)
- Exit code on findings

**Examples:**
- Python: pip-audit (official, comprehensive)
- JavaScript: pnpm audit (built-in)
- Java: dependency-check (OWASP, comprehensive)

**Assessment questions:**
- Scanner configured?
- Runs in CI? (recommended for Level 2)
- Failures on critical/high vulns?

**Justfile recipe:**
```just
vulns:
    [scan command]
```

---

### License Analysis (Level 2)

**Purpose:** Track dependency licenses, identify compliance issues

**Required capabilities:**
- List all dependency licenses
- Flag restrictive licenses (GPL, AGPL, etc.)
- Separate prod vs dev dependencies

**Examples:**
- Python: pip-licenses (summary mode)
- JavaScript: license-checker (pnpm dlx)
- Java: license-maven-plugin (third-party report)

**Assessment questions:**
- License scanner present?
- Can identify all licenses?
- Flags GPL/restrictive licenses?

**Justfile recipe:**
```just
lic:
    [license command] --summary
```

---

### SBOM Generation (Level 2)

**Purpose:** Software bill of materials for supply chain security

**Required capabilities:**
- Generate CycloneDX format SBOM
- Include all dependencies
- Output to file

**Examples:**
- Python: cyclonedx-py
- JavaScript: @cyclonedx/cyclonedx-npm
- Java: cyclonedx-maven-plugin

**Assessment questions:**
- SBOM generator configured?
- Output CycloneDX format?
- Includes all dependencies?

**Justfile recipe:**
```just
sbom:
    [sbom generator command] -o sbom.json
```

---

### Dependency Tracking (Level 2)

**Purpose:** Track outdated dependencies, enable updates

**Required capabilities:**
- List outdated packages
- Show current vs latest versions
- Readable output

**Examples:**
- Python: `uv pip list --outdated`
- JavaScript: `pnpm outdated`
- Java: `mvn versions:display-dependency-updates`

**Assessment questions:**
- Command shows outdated deps?
- Output shows current vs latest?

**Justfile recipe:**
```just
deps:
    [outdated command]
```

---

## Stack Skill Template

Language-specific stack skills follow this structure:

```markdown
---
name: configuring-[language]-stack
description: [Language] stack - [tools summary] ([coverage threshold])
---

# [Language] Stack

## Standards Compliance

| Standard | Level | Status |
|----------|-------|--------|
| aug-just/justfile-interface | Baseline (Level 0) | ✓ Full |
| development-stack-standards | Level [N] | ✓ Complete |

**Dimensions:** [X]/[Y] ([dimension summary])

## Toolchain

| Tool | Use |
|------|-----|
| **[tool]** | [purpose] |
| ... | ... |

## Quick Reference

```bash
[common commands]
```

## Docker Compatibility

Web services: Bind to `0.0.0.0` (not `127.0.0.1`)

```[language]
[example code for binding]
```

## Standard Justfile Interface

**Implements:** aug-just/justfile-interface (Level 0 baseline)

```just
[complete justfile for this stack]
```

## Configuration Files

### [config-file-name]

```[format]
[complete config]
```

## Notes

- [Stack-specific guidance]
- [Integration test marking]
- [Coverage threshold notes]
```

**Required sections:**
1. Frontmatter (name + description)
2. Standards Compliance table
3. Toolchain table
4. Quick reference (bash commands)
5. Docker compatibility
6. Standard justfile interface
7. Configuration files
8. Notes

---

## Assessment Criteria

### Level 0 Assessment

**Dimensions present?** (8/8 required)
- Package manager
- Format
- Lint
- Typecheck
- Test
- Coverage measurement
- Build
- Clean

**Justfile recipes?** (10/10 required)
- All baseline recipes present
- `check-all` dependencies: `format lint typecheck coverage`
- Comments match aug-just/justfile-interface

**Functional?**
- `just dev-install` succeeds
- `just check-all` succeeds or fails meaningfully

### Level 1 Assessment

**All Level 0 complete?** (prerequisite)

**Dimensions added?** (4/4 required)
- Coverage threshold 96% (unit tests only)
- Complexity threshold ≤10
- Test separation (unit vs integration)
- Test watch mode

**Justfile recipes added?** (4/4 required)
- `test-watch`
- `integration-test`
- `complexity`
- `loc`

**Functional?**
- `just coverage` fails below 96%
- `just lint` checks complexity ≤10
- Integration tests marked and excluded from threshold
- `just test-watch` runs continuously

### Level 2 Assessment

**All Level 1 complete?** (prerequisite)

**Dimensions added?** (4/4 required)
- Vulnerability scanning
- License analysis
- SBOM generation
- Dependency tracking

**Justfile recipes added?** (4/4 required)
- `deps`
- `vulns`
- `lic`
- `sbom`

**Functional?**
- Each command succeeds
- Output meaningful and parseable

### Level 3 Assessment

**Uses Level 1 tools** (complexity, loc) for detailed analysis

**Complexity reporting:**
- File-by-file breakdown
- Average and max metrics
- Identifies refactoring targets

**LOC analysis:**
- Identifies largest files
- Sortable output
- Helps scope refactoring

### Level 4 Assessment

**Structure:**
- Root justfile orchestrates
- Subproject justfiles implement full interface
- Each subproject standalone

**Root recipes:**
- Subset only: `dev-install`, `check-all`, `clean`, `build`, `deps`, `vulns`, `lic`, `sbom`
- Delegates via `_run-all`

**Subprojects:**
- Each implements Level 0+ independently
- Can run `cd [subproject] && just check-all`
- Languages follow their stack standards

---

## Tool Selection Guidance

### When ecosystem tool exists and is good

**Use it.** Example: pytest (Python), vitest (JS), Maven (Java)

### When multiple good options exist

**Prefer:**
1. Most widely adopted in ecosystem
2. Best maintained
3. Simplest to configure
4. Fastest

### When ecosystem lacks good option

**Use universal tool.** Example: cloc for LOC across languages

### Avoid

- Abandoned tools
- Tools requiring complex setup
- Tools with poor documentation
- Tools that fight the ecosystem

---

## YAGNI Enforcement

**Stop at the level you need:**

Library (no deployment): 0 → 1 → 2 (stop)

Web app (CI/CD + deploy): 0 → 1 → 2 → maybe 3

Solo project: 0 → 2 (skip quality overhead, add security)

Monorepo: 0 → 1 → 4 → 2 → 3

**Don't add:**
- Level 1 if no CI/CD
- Level 2 if not deploying
- Level 3 if codebase small
- Level 4 if single language

**Do add:**
- Level 0 always
- Levels only when "when" criteria met
- Specific patterns as needed
