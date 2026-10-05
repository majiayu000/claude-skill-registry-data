---
name: test-suite-prioritizer
description: Order and prioritize test suites for faster CI feedback using failure history analysis, code change correlation, coverage-based prioritization, risk-based.
---

# Test Suite Prioritizer

Order and prioritize test execution to deliver faster CI feedback by running the tests most likely to fail first. This skill applies failure history analysis, code change correlation, coverage-based prioritization, and risk-based ordering to reduce the time between code commit and actionable test results, often by 50-80%.

## When to Use This Skill

Use this skill when you need to:

- Reduce CI feedback time by running high-value tests first
- Implement test selection to skip tests unrelated to the current code change
- Prioritize tests based on failure history (tests that failed recently run first)
- Correlate code changes with the tests most likely to catch regressions
- Apply risk-based ordering where tests covering critical business logic run before tests covering cosmetic features
- Implement tiered test execution (fast smoke tests, then unit tests, then integration tests)
- Optimize parallel test distribution across CI runners
- Reduce CI costs by avoiding unnecessary full-suite runs

**Trigger phrases**: "prioritize tests", "test ordering", "faster CI", "test selection", "skip unrelated tests", "failure-based ordering", "risk-based testing", "CI optimization", "test parallelization", "smoke tests first", "test impact analysis"

## What This Skill Does

### Prioritization Strategies

#### 1. Failure History Prioritization

Tests that failed recently are more likely to fail again. Ordering tests by their recent failure rate provides the fastest feedback for regressions.

**Signal**: Failure count in the last N runs, time since last failure, failure rate trend

#### 2. Code Change Correlation (Test Impact Analysis)

Analyze which tests cover the files that changed in the current commit. Run only those tests, or run them first.

**Signal**: Coverage data mapping files to tests, dependency graph analysis

#### 3. Coverage-Based Prioritization

Tests that cover more unique code paths provide more value per execution second. Prioritize tests that maximize cumulative coverage.

**Signal**: Line/branch coverage per test, unique coverage contribution

#### 4. Risk-Based Ordering

Assign risk scores to code modules based on business criticality, defect density, and change frequency. Run tests covering high-risk modules first.

**Signal**: Business criticality labels, historical defect counts, code churn metrics

#### 5. Execution Time Optimization

Short tests provide faster feedback than long tests. Run the fastest tests first to catch obvious regressions within seconds.

**Signal**: Historical execution time per test

#### 6. Tiered Execution

Structure the test suite into tiers that run sequentially, with each tier providing progressively deeper coverage:

| Tier | Tests | Target Time | Purpose |
|---|---|---|---|
| 0 | Lint, type check | < 30 seconds | Catch syntax and type errors |
| 1 | Smoke tests | < 2 minutes | Verify critical paths work at all |
| 2 | Unit tests | < 5 minutes | Verify function-level correctness |
| 3 | Integration tests | < 15 minutes | Verify component interactions |
| 4 | E2E tests | < 30 minutes | Verify full user workflows |

## Instructions

### Step 1: Implement Failure History Prioritization

**Python:**
```python
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class TestExecutionRecord:
    test_name: str
    passed: bool
    duration_seconds: float
    timestamp: datetime


@dataclass
class FailureHistoryPrioritizer:
    """Prioritize tests based on their recent failure history."""

    history_file: Path
    history: dict = field(default_factory=dict)

    def load(self):
        """Load execution history from disk."""
        if self.history_file.exists():
            raw = json.loads(self.history_file.read_text())
            self.history = raw
        return self

    def save(self):
        """Persist execution history to disk."""
        self.history_file.write_text(json.dumps(self.history, indent=2, default=str))

    def record(self, result: TestExecutionRecord):
        """Record a test execution result."""
        if result.test_name not in self.history:
            self.history[result.test_name] = {
                "runs": [],
                "total_runs": 0,
                "total_failures": 0,
            }
        entry = self.history[result.test_name]
        entry["runs"].append({
            "passed": result.passed,
            "duration": result.duration_seconds,
            "timestamp": result.timestamp.isoformat(),
        })
        entry["total_runs"] += 1
        if not result.passed:
            entry["total_failures"] += 1
        # Keep only last 100 runs
        entry["runs"] = entry["runs"][-100:]

    def failure_score(self, test_name: str, window: int = 20) -> float:
        """Calculate a failure priority score (higher = more likely to fail).

        Score components:
        - Recent failure rate (last `window` runs)
        - Recency bonus (failures in the last 5 runs score higher)
        - Failure streak bonus (consecutive recent failures)
        """
        entry = self.history.get(test_name)
        if not entry or not entry["runs"]:
            return 0.5  # Unknown tests get medium priority

        recent_runs = entry["runs"][-window:]
        recent_failures = sum(1 for r in recent_runs if not r["passed"])
        failure_rate = recent_failures / len(recent_runs)

        # Recency bonus: failures in last 5 runs
        last_5 = entry["runs"][-5:]
        recent_failure_count = sum(1 for r in last_5 if not r["passed"])
        recency_bonus = recent_failure_count * 0.1

        # Streak bonus: consecutive failures from the most recent run
        streak = 0
        for r in reversed(entry["runs"]):
            if not r["passed"]:
                streak += 1
            else:
                break
        streak_bonus = min(streak * 0.05, 0.25)

        return min(failure_rate + recency_bonus + streak_bonus, 1.0)

    def prioritize(self, test_names: list[str]) -> list[str]:
        """Return test names sorted by failure priority (highest first)."""
        scored = [(name, self.failure_score(name)) for name in test_names]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in scored]


# Usage in a pytest plugin
def pytest_collection_modifyitems(config, items):
    """Reorder tests by failure history priority."""
    prioritizer = FailureHistoryPrioritizer(
        Path(".test_history.json")
    ).load()

    test_names = [item.nodeid for item in items]
    ordered_names = prioritizer.prioritize(test_names)

    name_to_index = {name: i for i, name in enumerate(ordered_names)}
    items.sort(key=lambda item: name_to_index.get(item.nodeid, len(ordered_names)))
```

**JavaScript (Jest custom sequencer):**
```javascript
// test-sequencer.js
const Sequencer = require("@jest/test-sequencer").default;
const fs = require("fs");
const path = require("path");

const HISTORY_FILE = path.join(process.cwd(), ".test_history.json");

class FailureHistorySequencer extends Sequencer {
  constructor() {
    super();
    this.history = this.loadHistory();
  }

  loadHistory() {
    try {
      return JSON.parse(fs.readFileSync(HISTORY_FILE, "utf-8"));
    } catch {
      return {};
    }
  }

  failureScore(testPath) {
    const entry = this.history[testPath];
    if (!entry || !entry.runs || entry.runs.length === 0) {
      return 0.5;
    }

    const recent = entry.runs.slice(-20);
    const failureRate = recent.filter((r) => !r.passed).length / recent.length;

    const last5 = entry.runs.slice(-5);
    const recentFailures = last5.filter((r) => !r.passed).length;
    const recencyBonus = recentFailures * 0.1;

    return Math.min(failureRate + recencyBonus, 1.0);
  }

  sort(tests) {
    return [...tests].sort((a, b) => {
      const scoreA = this.failureScore(a.path);
      const scoreB = this.failureScore(b.path);
      return scoreB - scoreA;
    });
  }
}

module.exports = FailureHistorySequencer;

// jest.config.js:
// module.exports = {
//   testSequencer: "./test-sequencer.js",
// };
```

**Java (JUnit 5 with custom test order):**
```java
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.MethodOrdererContext;
import org.junit.jupiter.api.TestMethodOrder;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Custom method orderer that prioritizes tests by failure history.
 */
public class FailureHistoryOrderer implements MethodOrderer {

    private static final Path HISTORY_FILE = Path.of(".test_history.json");
    private Map<String, Map<String, Object>> history;

    @Override
    public void orderMethods(MethodOrdererContext context) {
        loadHistory();
        context.getMethodDescriptors().sort((a, b) -> {
            double scoreA = failureScore(a.getMethod().getName());
            double scoreB = failureScore(b.getMethod().getName());
            return Double.compare(scoreB, scoreA);
        });
    }

    private void loadHistory() {
        try {
            if (Files.exists(HISTORY_FILE)) {
                var mapper = new ObjectMapper();
                history = mapper.readValue(
                        HISTORY_FILE.toFile(),
                        mapper.getTypeFactory().constructMapType(
                                HashMap.class, String.class, Map.class)
                );
            } else {
                history = new HashMap<>();
            }
        } catch (IOException e) {
            history = new HashMap<>();
        }
    }

    private double failureScore(String testName) {
        var entry = history.get(testName);
        if (entry == null) return 0.5;

        @SuppressWarnings("unchecked")
        var runs = (List<Map<String, Object>>) entry.get("runs");
        if (runs == null || runs.isEmpty()) return 0.5;

        var recent = runs.subList(Math.max(0, runs.size() - 20), runs.size());
        long failures = recent.stream()
                .filter(r -> !(boolean) r.get("passed"))
                .count();
        return (double) failures / recent.size();
    }
}

// Usage:
// @TestMethodOrder(FailureHistoryOrderer.class)
// class MyTest { ... }
```

### Step 2: Implement Test Impact Analysis (Code Change Correlation)

**Python:**
```python
import subprocess
import json
from pathlib import Path


class TestImpactAnalyzer:
    """Select tests based on which source files changed."""

    def __init__(self, coverage_map_file: str = ".coverage_map.json"):
        self.coverage_map_file = Path(coverage_map_file)
        self.coverage_map = {}  # {source_file: [test_file1, test_file2, ...]}

    def build_coverage_map(self):
        """Build a mapping from source files to the tests that cover them.

        Run this after a full test suite execution with coverage enabled.
        """
        # Parse coverage.py JSON report
        coverage_data = json.loads(Path("coverage.json").read_text())

        file_to_tests = {}
        for test_file, file_data in coverage_data.get("files", {}).items():
            executed_lines = file_data.get("executed_lines", [])
            for source_file in file_data.get("contexts", {}).keys():
                if source_file not in file_to_tests:
                    file_to_tests[source_file] = set()
                file_to_tests[source_file].add(test_file)

        self.coverage_map = {k: list(v) for k, v in file_to_tests.items()}
        self.coverage_map_file.write_text(json.dumps(self.coverage_map, indent=2))

    def load_coverage_map(self):
        """Load a previously built coverage map."""
        if self.coverage_map_file.exists():
            self.coverage_map = json.loads(self.coverage_map_file.read_text())
        return self

    def get_changed_files(self, base_ref: str = "main") -> list[str]:
        """Get the list of files changed relative to the base branch."""
        result = subprocess.run(
            ["git", "diff", "--name-only", base_ref, "HEAD"],
            capture_output=True, text=True,
        )
        return [f.strip() for f in result.stdout.strip().splitlines() if f.strip()]

    def select_tests(self, changed_files: list[str] = None) -> list[str]:
        """Select tests that are impacted by the changed files."""
        if changed_files is None:
            changed_files = self.get_changed_files()

        selected_tests = set()
        for changed_file in changed_files:
            # Direct mapping
            if changed_file in self.coverage_map:
                selected_tests.update(self.coverage_map[changed_file])
            # Check for partial path matches (e.g., src/module.py matches module.py)
            for source_file, tests in self.coverage_map.items():
                if changed_file.endswith(source_file) or source_file.endswith(changed_file):
                    selected_tests.update(tests)

        if not selected_tests:
            # If no mapping found, run all tests as a safety net
            return None  # Indicates "run everything"

        return sorted(selected_tests)


# Usage: select and run only impacted tests
analyzer = TestImpactAnalyzer().load_coverage_map()
changed = analyzer.get_changed_files()
selected = analyzer.select_tests(changed)
if selected:
    print(f"Running {len(selected)} impacted tests (out of full suite)")
    # pytest {' '.join(selected)}
else:
    print("No coverage map match; running full suite")
```

**JavaScript:**
```javascript
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

class TestImpactAnalyzer {
  constructor(coverageMapFile = ".coverage_map.json") {
    this.coverageMapFile = coverageMapFile;
    this.coverageMap = {};
  }

  loadCoverageMap() {
    try {
      this.coverageMap = JSON.parse(
        fs.readFileSync(this.coverageMapFile, "utf-8")
      );
    } catch {
      this.coverageMap = {};
    }
    return this;
  }

  getChangedFiles(baseRef = "main") {
    const output = execSync(`git diff --name-only ${baseRef} HEAD`, {
      encoding: "utf-8",
    });
    return output
      .trim()
      .split("\n")
      .filter((f) => f.length > 0);
  }

  selectTests(changedFiles = null) {
    if (!changedFiles) {
      changedFiles = this.getChangedFiles();
    }

    const selectedTests = new Set();
    for (const changedFile of changedFiles) {
      const tests = this.coverageMap[changedFile];
      if (tests) {
        tests.forEach((t) => selectedTests.add(t));
      }
    }

    if (selectedTests.size === 0) {
      return null; // Run everything
    }

    return [...selectedTests].sort();
  }
}

// Usage:
const analyzer = new TestImpactAnalyzer().loadCoverageMap();
const selected = analyzer.selectTests();
if (selected) {
  console.log(`Running ${selected.length} impacted tests`);
  // Execute: jest ${selected.join(' ')}
} else {
  console.log("Running full test suite");
}
```

### Step 3: Implement Coverage-Based Prioritization

**Python:**
```python
from dataclasses import dataclass


@dataclass
class TestCoverageInfo:
    test_name: str
    covered_lines: set  # {(file, line_number), ...}
    duration_seconds: float


class CoverageBasedPrioritizer:
    """Prioritize tests to maximize cumulative coverage gain per unit time."""

    def __init__(self, test_coverage: list[TestCoverageInfo]):
        self.test_coverage = test_coverage

    def prioritize_greedy(self) -> list[str]:
        """Greedy algorithm: at each step, select the test that covers the
        most uncovered lines per second of execution time."""
        remaining = list(self.test_coverage)
        covered = set()
        ordered = []

        while remaining:
            best = None
            best_score = -1

            for tc in remaining:
                new_coverage = tc.covered_lines - covered
                if tc.duration_seconds > 0:
                    score = len(new_coverage) / tc.duration_seconds
                else:
                    score = len(new_coverage) * 1000  # Instant tests score very high

                if score > best_score:
                    best_score = score
                    best = tc

            if best is None or best_score <= 0:
                # Remaining tests add no new coverage; append in original order
                ordered.extend(tc.test_name for tc in remaining)
                break

            ordered.append(best.test_name)
            covered |= best.covered_lines
            remaining.remove(best)

        return ordered

    def coverage_at_position(self, ordered: list[str], position: int) -> float:
        """Calculate cumulative coverage percentage at a given position in the ordering."""
        all_lines = set()
        for tc in self.test_coverage:
            all_lines |= tc.covered_lines

        covered = set()
        test_map = {tc.test_name: tc for tc in self.test_coverage}
        for name in ordered[:position]:
            if name in test_map:
                covered |= test_map[name].covered_lines

        return len(covered) / max(len(all_lines), 1) * 100


# Example usage
tests = [
    TestCoverageInfo("test_login", {("auth.py", 1), ("auth.py", 2), ("auth.py", 3)}, 0.5),
    TestCoverageInfo("test_signup", {("auth.py", 1), ("auth.py", 10), ("auth.py", 11)}, 0.8),
    TestCoverageInfo("test_logout", {("auth.py", 20), ("auth.py", 21)}, 0.2),
    TestCoverageInfo("test_profile", {("user.py", 1), ("user.py", 2)}, 1.5),
]

prioritizer = CoverageBasedPrioritizer(tests)
ordered = prioritizer.prioritize_greedy()
print("Prioritized order:", ordered)
for i in range(1, len(ordered) + 1):
    cov = prioritizer.coverage_at_position(ordered, i)
    print(f"  After {i} tests: {cov:.1f}% coverage")
```

### Step 4: Implement Risk-Based Ordering

**Python:**
```python
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ModuleRiskProfile:
    module_path: str
    business_criticality: float   # 0.0 to 1.0
    defect_density: float         # bugs per KLOC
    change_frequency: float       # commits per month
    complexity: float             # cyclomatic complexity average


class RiskBasedPrioritizer:
    """Prioritize tests by the risk score of the modules they cover."""

    def __init__(self, risk_profiles: list[ModuleRiskProfile],
                 test_to_modules: dict):
        """
        Args:
            risk_profiles: Risk profile for each module.
            test_to_modules: Mapping from test name to list of modules it covers.
        """
        self.risk_scores = {}
        for profile in risk_profiles:
            score = (
                profile.business_criticality * 0.4
                + profile.defect_density * 0.25
                + profile.change_frequency * 0.2
                + profile.complexity * 0.15
            )
            self.risk_scores[profile.module_path] = score

        self.test_to_modules = test_to_modules

    def test_risk_score(self, test_name: str) -> float:
        """Calculate the aggregate risk score for a test based on the modules it covers."""
        modules = self.test_to_modules.get(test_name, [])
        if not modules:
            return 0.0
        return max(self.risk_scores.get(m, 0.0) for m in modules)

    def prioritize(self, test_names: list[str]) -> list[str]:
        """Return tests ordered by risk score (highest risk first)."""
        scored = [(name, self.test_risk_score(name)) for name in test_names]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in scored]


def compute_change_frequency(repo_path: str, module_path: str,
                              months: int = 3) -> float:
    """Count commits touching a module in the last N months."""
    since = f"{months} months ago"
    result = subprocess.run(
        ["git", "log", f"--since={since}", "--oneline", "--", module_path],
        capture_output=True, text=True, cwd=repo_path,
    )
    return len(result.stdout.strip().splitlines())
```

### Step 5: Implement Tiered Test Execution in CI

**Python (pytest markers for tiered execution):**
```python
# conftest.py
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "tier0: lint and type checks")
    config.addinivalue_line("markers", "tier1: smoke tests (critical paths)")
    config.addinivalue_line("markers", "tier2: unit tests")
    config.addinivalue_line("markers", "tier3: integration tests")
    config.addinivalue_line("markers", "tier4: e2e tests")


# Usage in tests:
@pytest.mark.tier1
def test_health_check(client):
    """Smoke test: API is running and responding."""
    response = client.get("/health")
    assert response.status_code == 200


@pytest.mark.tier1
def test_login_basic(client):
    """Smoke test: basic login flow works."""
    response = client.post("/login", json={"email": "admin@test.com", "password": "test"})
    assert response.status_code == 200


@pytest.mark.tier2
def test_password_hashing():
    """Unit test: password hashing produces correct output."""
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)


@pytest.mark.tier3
def test_order_placement_with_database(db_session, client):
    """Integration test: full order placement flow."""
    response = client.post("/orders", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 201
    order = db_session.query(Order).first()
    assert order is not None
```

**CI pipeline configuration (GitHub Actions):**
```yaml
# .github/workflows/test.yml
name: Tiered Tests
on: [push, pull_request]

jobs:
  tier0-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy src/

  tier1-smoke:
    needs: tier0-lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e ".[test]"
      - run: pytest -m tier1 --timeout=30

  tier2-unit:
    needs: tier1-smoke
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e ".[test]"
      - run: pytest -m tier2 --timeout=300

  tier3-integration:
    needs: tier2-unit
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e ".[test]"
      - run: pytest -m tier3 --timeout=900
```

**JavaScript (Jest projects for tiered execution):**
```javascript
// jest.config.js
module.exports = {
  projects: [
    {
      displayName: "tier1-smoke",
      testMatch: ["<rootDir>/tests/smoke/**/*.test.js"],
      testTimeout: 10000,
    },
    {
      displayName: "tier2-unit",
      testMatch: ["<rootDir>/tests/unit/**/*.test.js"],
      testTimeout: 30000,
    },
    {
      displayName: "tier3-integration",
      testMatch: ["<rootDir>/tests/integration/**/*.test.js"],
      testTimeout: 60000,
    },
  ],
};

// Run specific tiers:
// npx jest --selectProjects tier1-smoke
// npx jest --selectProjects tier2-unit
```

### Step 6: Combine Multiple Prioritization Strategies

**Python:**
```python
from dataclasses import dataclass


@dataclass
class CompositeScore:
    test_name: str
    failure_score: float
    risk_score: float
    coverage_efficiency: float
    execution_time: float


class CompositePrioritizer:
    """Combine multiple prioritization signals into a single ordering."""

    def __init__(self, weights: dict = None):
        self.weights = weights or {
            "failure": 0.40,   # Recent failure history
            "risk": 0.25,      # Business risk of covered modules
            "coverage": 0.20,  # Coverage efficiency (coverage per second)
            "speed": 0.15,     # Execution speed (faster tests first)
        }

    def compute_composite_score(self, scores: CompositeScore) -> float:
        """Weighted combination of all prioritization signals."""
        # Normalize execution time (invert: shorter is better)
        speed_score = 1.0 / max(scores.execution_time, 0.01)
        max_speed = 1.0 / 0.01  # Normalize to 0-1
        speed_normalized = min(speed_score / max_speed, 1.0)

        return (
            self.weights["failure"] * scores.failure_score
            + self.weights["risk"] * scores.risk_score
            + self.weights["coverage"] * scores.coverage_efficiency
            + self.weights["speed"] * speed_normalized
        )

    def prioritize(self, test_scores: list[CompositeScore]) -> list[str]:
        """Return test names sorted by composite priority (highest first)."""
        scored = [
            (ts.test_name, self.compute_composite_score(ts))
            for ts in test_scores
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in scored]


# Usage
scores = [
    CompositeScore("test_login", failure_score=0.8, risk_score=0.9,
                   coverage_efficiency=0.5, execution_time=0.3),
    CompositeScore("test_signup", failure_score=0.2, risk_score=0.9,
                   coverage_efficiency=0.7, execution_time=1.2),
    CompositeScore("test_color_theme", failure_score=0.0, risk_score=0.1,
                   coverage_efficiency=0.3, execution_time=0.1),
    CompositeScore("test_payment", failure_score=0.5, risk_score=1.0,
                   coverage_efficiency=0.8, execution_time=2.5),
]

prioritizer = CompositePrioritizer()
ordered = prioritizer.prioritize(scores)
print("Prioritized order:")
for i, name in enumerate(ordered, 1):
    print(f"  {i}. {name}")
```

## Best Practices

- **Start with failure history prioritization**: It is the simplest to implement and provides the largest feedback time reduction; most CI systems already have test result data available
- **Build and update the coverage map regularly**: Run a full test suite with coverage weekly or on the main branch to keep the test-to-file mapping current
- **Fail fast with tiered execution**: Configure CI so that if tier 1 (smoke) fails, tiers 2-4 are skipped entirely; this saves the most time and money
- **Use test impact analysis for large monorepos**: In repositories with thousands of tests, running only the impacted subset can reduce CI time from 30 minutes to 3 minutes
- **Combine strategies with weighted scores**: No single strategy is optimal; a composite approach that weighs failure history, risk, coverage, and speed together produces the best ordering
- **Track metrics over time**: Measure "time to first failure" and "total CI time" before and after implementing prioritization to quantify the improvement
- **Maintain a safety net**: Periodically run the full test suite (e.g., nightly) to catch issues that test selection might miss
- **Distribute tests across parallel runners efficiently**: When using multiple CI runners, assign tests so that each runner has approximately equal total execution time

## Common Pitfalls

- **Optimizing test order without fixing slow tests**: Prioritization makes slow suites faster to produce feedback, but the total execution time remains the same; also invest in making individual tests faster
- **Relying solely on test selection**: Skipping tests based on code change analysis can miss indirect dependencies (e.g., a configuration change that affects all modules); always run the full suite periodically
- **Stale coverage maps**: A coverage map from last month may not reflect recent code changes; update it at least weekly
- **Ignoring flaky tests in failure history**: A test that fails due to flakiness (not real regressions) will be prioritized highly, wasting the benefit of failure-based ordering; fix flaky tests first (see the flaky-test-detector skill)
- **Over-partitioning into too many tiers**: Three to five tiers is sufficient; more tiers add complexity without proportional benefit
- **Not measuring the impact**: Implementing prioritization without measuring before/after metrics makes it impossible to justify the investment or identify regressions in the approach
- **Treating all tests as equal in parallel distribution**: Assigning tests round-robin to parallel runners ignores execution time differences; one runner may finish in 1 minute while another takes 10 minutes; use time-balanced distribution
- **Skipping integration tests too aggressively**: Unit tests passing does not guarantee integration correctness; always run at least a smoke-level integration test on every commit
