---
name: CI/CD Optimization
description: Comprehensive CI/CD pipeline methodology with quality gates, release automation, smoke testing, observability, and performance tracking. Use when setting up CI/CD from scratch, build time over 5 minutes, no automated quality gates, manual release process, lack of pipeline observability, or broken releases reaching production. Provides 5 quality gate categories (coverage threshold 75-80%, lint blocking, CHANGELOG validation, build verification, test pass rate), release automation with conventional commits and automatic CHANGELOG generation, 25 smoke tests across execution/consistency/structure categories, CI observability with metrics tracking and regression detection, performance optimization including native-only testing for Go cross-compilation. Validated in meta-cc with 91.7% pattern validation rate (11/12 patterns), 2.5-3.5x estimated speedup, GitHub Actions native with 70-80% transferability to GitLab CI and Jenkins.
allowed-tools: Read, Write, Edit, Bash
---

# CI/CD Optimization

**Transform manual releases into automated, quality-gated, observable pipelines.**

> Quality gates prevent regression. Automation prevents human error. Observability enables continuous optimization.

---

## When to Use This Skill

Use this skill when:
- 🚀 **Setting up CI/CD**: New project needs pipeline infrastructure
- ⏱️ **Slow builds**: Build time exceeds 5 minutes
- 🚫 **No quality gates**: Coverage, lint, tests not enforced automatically
- 👤 **Manual releases**: Human-driven deployment process
- 📊 **No observability**: Cannot track pipeline performance metrics
- 🔄 **Broken releases**: Defects reaching production regularly
- 📝 **Manual CHANGELOG**: Release notes created by hand

**Don't use when**:
- ❌ CI/CD already optimal (<2min builds, fully automated, quality-gated)
- ❌ Non-GitHub Actions without adaptation time (70-80% transferable)
- ❌ Infrequent releases (monthly or less, automation ROI low)
- ❌ Single developer projects (overhead may exceed benefit)

---

## Quick Start (30 minutes)

### Step 1: Implement Coverage Gate (10 min)

```yaml
# .github/workflows/ci.yml
- name: Check coverage threshold
  run: |
    COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
    if (( $(echo "$COVERAGE < 75" | bc -l) )); then
      echo "Coverage $COVERAGE% below threshold 75%"
      exit 1
    fi
```

### Step 2: Automate CHANGELOG Generation (15 min)

```bash
# scripts/generate-changelog-entry.sh
# Parse conventional commits: feat:, fix:, docs:, etc.
# Generate CHANGELOG entry automatically
# Zero manual editing required
```

### Step 3: Add Basic Smoke Tests (5 min)

```bash
# scripts/smoke-tests.sh
# Test 1: Binary executes
./dist/meta-cc --version

# Test 2: Help output valid
./dist/meta-cc --help | grep "Usage:"

# Test 3: Basic command works
./dist/meta-cc get-session-stats
```

---

## Five Quality Gate Categories

### 1. Coverage Threshold Gate
**Purpose**: Prevent coverage regression
**Threshold**: 75-80% (project-specific)
**Action**: Block merge if below threshold

**Implementation**:
```yaml
- name: Coverage gate
  run: |
    COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
    if (( $(echo "$COVERAGE < 80" | bc -l) )); then
      exit 1
    fi
```

**Principle**: Enforcement before improvement - implement gate even if not at target yet

### 2. Lint Blocking
**Purpose**: Maintain code quality standards
**Tool**: golangci-lint (Go), pylint (Python), ESLint (JS)
**Action**: Block merge on lint failures

### 3. CHANGELOG Validation
**Purpose**: Ensure release notes completeness
**Check**: CHANGELOG.md updated for version changes
**Action**: Block release if CHANGELOG missing

### 4. Build Verification
**Purpose**: Ensure compilable code
**Platforms**: Native + cross-compilation targets
**Action**: Block merge on build failure

### 5. Test Pass Rate
**Purpose**: Maintain test reliability
**Threshold**: 100% (zero tolerance for flaky tests)
**Action**: Block merge on test failures

---

## Release Automation

### Conventional Commits
**Format**: `type(scope): description`

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code restructuring
- `test:` - Test additions/changes
- `chore:` - Maintenance

### Automatic CHANGELOG Generation
**Tool**: Custom script (135 lines, zero dependencies)
**Process**:
1. Parse git commits since last release
2. Group by type (Features, Fixes, Documentation)
3. Generate markdown entry
4. Prepend to CHANGELOG.md

**Time savings**: 5-10 minutes per release

### GitHub Releases
**Automation**: Triggered on version tags
**Artifacts**: Binaries, packages, checksums
**Release notes**: Auto-generated from CHANGELOG

---

## Smoke Testing (25 Tests)

### Execution Tests (10 tests)
- Binary runs without errors
- Help output valid
- Version command works
- Basic commands execute
- Exit codes correct

### Consistency Tests (8 tests)
- Output format stable
- JSON structure valid
- Error messages formatted
- Logging output consistent

### Structure Tests (7 tests)
- Package contents complete
- File permissions correct
- Dependencies bundled
- Configuration files present

**Validation**: 25/25 tests passing in meta-cc

---

## CI Observability

### Metrics Tracked
1. **Build time**: Total pipeline duration
2. **Test time**: Test execution duration
3. **Coverage**: Test coverage percentage
4. **Artifact size**: Binary/package size

### Storage Strategy
**Approach**: Git-committed CSV files
**Location**: `.ci-metrics/*.csv`
**Retention**: Last 100 builds (auto-trimmed)
**Advantages**: Zero infrastructure, automatic versioning

### Regression Detection
**Method**: Moving average baseline (last 10 builds)
**Threshold**: >20% regression triggers PR block
**Metrics**: Build time, test time, artifact size

**Implementation**:
```bash
# scripts/check-performance-regression.sh
BASELINE=$(tail -10 .ci-metrics/build-time.csv | awk '{sum+=$2} END {print sum/NR}')
CURRENT=$BUILD_TIME
if (( $(echo "$CURRENT > $BASELINE * 1.2" | bc -l) )); then
  echo "Build time regression: ${CURRENT}s > ${BASELINE}s + 20%"
  exit 1
fi
```

---

## Performance Optimization

### Native-Only Testing
**Principle**: Trust mature cross-compilation (Go, Rust)
**Savings**: 5-10 minutes per build (avoid emulation)
**Risk**: Platform-specific bugs (mitigated by Go's 99%+ reliability)

**Decision criteria**:
- Mature tooling: YES → native-only
- Immature tooling: NO → test all platforms

### Caching Strategies
- Go module cache
- Build artifact cache
- Test cache for unchanged packages

### Parallel Execution
- Run linters in parallel with tests
- Matrix builds for multiple Go versions
- Parallel smoke tests

---

## Proven Results

**Validated in bootstrap-007** (meta-cc project):
- ✅ 11/12 patterns validated (91.7%)
- ✅ Coverage gate operational (80% threshold)
- ✅ CHANGELOG automation (zero manual editing)
- ✅ 25 smoke tests (100% pass rate)
- ✅ Metrics tracking (4 metrics, 100 builds history)
- ✅ Regression detection (20% threshold)
- ✅ 6 iterations, ~18 hours
- ✅ V_instance: 0.85, V_meta: 0.82

**Estimated speedup**: 2.5-3.5x vs manual process

**Not validated** (1/12):
- E2E pipeline tests (requires staging environment, deferred)

**Transferability**:
- GitHub Actions: 100% (native)
- GitLab CI: 75% (YAML similar, runner differences)
- Jenkins: 70% (concepts transfer, syntax very different)
- **Overall**: 70-80% transferable

---

## Templates

### GitHub Actions CI Workflow
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Go
        uses: actions/setup-go@v4
      - name: Test
        run: go test -coverprofile=coverage.out ./...
      - name: Coverage gate
        run: ./scripts/check-coverage.sh
      - name: Lint
        run: golangci-lint run
      - name: Track metrics
        run: ./scripts/track-metrics.sh
      - name: Check regression
        run: ./scripts/check-performance-regression.sh
```

### GitHub Actions Release Workflow
```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: make build-all
      - name: Smoke tests
        run: ./scripts/smoke-tests.sh
      - name: Create release
        uses: actions/create-release@v1
      - name: Upload artifacts
        uses: actions/upload-release-asset@v1
```

---

## Anti-Patterns

❌ **Quality theater**: Gates that don't actually block (warnings only)
❌ **Over-automation**: Automating steps that change frequently
❌ **Metrics without action**: Tracking data but never acting on it
❌ **Flaky gates**: Tests that fail randomly (undermines trust)
❌ **One-size-fits-all**: Same thresholds for all project types

---

## Related Skills

**Parent framework**:
- [methodology-bootstrapping](../methodology-bootstrapping/SKILL.md) - Core OCA cycle

**Complementary**:
- [testing-strategy](../testing-strategy/SKILL.md) - Quality gates foundation
- [observability-instrumentation](../observability-instrumentation/SKILL.md) - Metrics patterns
- [error-recovery](../error-recovery/SKILL.md) - Build failure handling

---

## References

**Core guides**:
- Reference materials in experiments/bootstrap-007-cicd-pipeline/
- Quality gates methodology
- Release automation guide
- Smoke testing patterns
- Observability patterns

**Scripts**:
- scripts/check-coverage.sh
- scripts/generate-changelog-entry.sh
- scripts/smoke-tests.sh
- scripts/track-metrics.sh
- scripts/check-performance-regression.sh

---

**Status**: ✅ Production-ready | 91.7% validation | 2.5-3.5x speedup | 70-80% transferable
