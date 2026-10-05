---
name: flaky-test-detector
description: Identify and diagnose flaky tests in CI pipelines by analyzing timing dependencies, shared state, ordering assumptions, and network reliance. Use when tests.
---

# Flaky Test Detector

Identify, diagnose, and stabilize flaky tests that intermittently pass or fail without code changes. This skill provides systematic detection strategies, root cause analysis patterns, and stabilization techniques to restore confidence in your CI pipeline.

## When to Use This Skill

Use this skill when you need to:

- Investigate tests that intermittently fail in CI but pass locally
- Diagnose whether a failure is a true regression or a flaky test
- Quarantine unreliable tests without losing track of them
- Stabilize a test suite that has eroded developer trust
- Implement flakiness detection infrastructure (repeat-run strategies, flakiness scores)
- Fix timing-dependent, order-dependent, or environment-dependent tests
- Reduce CI costs caused by unnecessary reruns of flaky pipelines
- Establish a flakiness budget or quality gate for test reliability

**Trigger phrases**: "flaky test", "intermittent failure", "test sometimes fails", "CI is unreliable", "test passes locally but fails in CI", "quarantine tests", "stabilize test suite", "non-deterministic test", "test ordering issue"

## What This Skill Does

### Flakiness Root Cause Taxonomy

Flaky tests arise from a finite set of root causes. Understanding the taxonomy allows targeted diagnosis rather than guesswork.

#### 1. Timing Dependencies

Tests that depend on wall-clock time, sleep durations, or timeout thresholds are the most common source of flakiness.

- **Symptom**: Test passes on fast machines, fails on slower CI runners
- **Root cause**: Hard-coded sleep values, race conditions between async operations, timeouts that are too tight
- **Detection signal**: Failure rate correlates with CI runner load or machine specs

#### 2. Test Ordering Dependencies

Tests that rely on side effects from previously executed tests break when execution order changes.

- **Symptom**: Test passes in full suite but fails when run in isolation (or vice versa)
- **Root cause**: Shared mutable state (global variables, database rows, files on disk) not cleaned up between tests
- **Detection signal**: Failure appears only in specific test ordering; randomizing order triggers failures

#### 3. Shared State and Resource Leaks

Tests that share database connections, file handles, ports, or in-memory caches can interfere with each other.

- **Symptom**: Test fails when run in parallel but passes sequentially
- **Root cause**: Two tests compete for the same port, database table, or temp file
- **Detection signal**: Parallel test execution reveals failures absent in serial execution

#### 4. Network and External Service Dependencies

Tests that call real HTTP endpoints, DNS, or external APIs are subject to network latency, rate limiting, and outages.

- **Symptom**: Test fails sporadically with connection timeouts or unexpected HTTP status codes
- **Root cause**: Missing mocks or stubs for external dependencies
- **Detection signal**: Failures cluster around specific network-dependent tests

#### 5. Non-Deterministic Data

Tests that use random data, current timestamps, or auto-generated IDs without controlling the seed.

- **Symptom**: Test fails for certain random seeds but passes for others
- **Root cause**: Assertions depend on specific ordering or values that change each run
- **Detection signal**: Failure is truly random with no environmental pattern

#### 6. Platform and Environment Differences

Tests that assume a specific OS, locale, timezone, filesystem behaviour, or library version.

- **Symptom**: Test passes on developer machines (macOS) but fails on CI (Linux)
- **Root cause**: Path separator differences, case-sensitive filesystems, locale-dependent string sorting
- **Detection signal**: Failures are platform-specific

### Detection Strategies

#### Repeat-Run Detection

Run each test multiple times (typically 10-50 repetitions) to detect intermittent failures.

#### Quarantine and Track

Move known flaky tests to a quarantine suite that runs but does not block the pipeline. Track flakiness scores over time.

#### Order Randomization

Run the test suite with randomized ordering to expose order-dependent tests.

#### Isolation Verification

Run each failing test in complete isolation (separate process, fresh environment) to distinguish test-interaction bugs from true flakiness.

## Instructions

### Step 1: Detect Flaky Tests with Repeat Runs

**Python (pytest with pytest-repeat):**
```python
# Install: pip install pytest-repeat
# Run each test 20 times to detect flakiness:
# pytest --count=20 -x tests/

# Alternatively, use a custom conftest.py marker:
import pytest

def pytest_collection_modifyitems(config, items):
    """Automatically repeat tests marked as potentially flaky."""
    for item in items:
        if item.get_closest_marker("suspect_flaky"):
            item.add_marker(pytest.mark.parametrize(
                "_run", range(20), ids=lambda i: f"run-{i}"
            ))

# Mark a suspect test:
@pytest.mark.suspect_flaky
def test_async_notification_delivery():
    result = send_notification_async("user@example.com")
    assert result.delivered_within(seconds=5)
```

**JavaScript (Jest with custom retry logic):**
```javascript
// jest.config.js - enable retries globally
module.exports = {
  // Retry failed tests up to 3 times
  retryTimes: 3,
  reporters: [
    "default",
    // Custom reporter to log flaky tests
    ["./flaky-reporter.js", {}],
  ],
};

// flaky-reporter.js - track tests that needed retries
class FlakyReporter {
  constructor(globalConfig, options) {
    this.flakyTests = [];
  }

  onTestCaseResult(test, testCaseResult) {
    if (testCaseResult.numPassingAsserts > 0 && testCaseResult.status === "passed") {
      // If the test was retried and eventually passed, it is flaky
      if (testCaseResult.retryReasons && testCaseResult.retryReasons.length > 0) {
        this.flakyTests.push({
          name: testCaseResult.fullName,
          retries: testCaseResult.retryReasons.length,
        });
      }
    }
  }

  onRunComplete() {
    if (this.flakyTests.length > 0) {
      console.warn("\n--- FLAKY TESTS DETECTED ---");
      this.flakyTests.forEach((t) => {
        console.warn(`  ${t.name} (retried ${t.retries} times)`);
      });
    }
  }
}

module.exports = FlakyReporter;
```

**Java (JUnit 5 with RepetitionInfo):**
```java
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.RepetitionInfo;
import static org.junit.jupiter.api.Assertions.*;

class FlakynessDetectionTest {

    /**
     * Run the suspect test 20 times to detect intermittent failures.
     * If any repetition fails, the test is flaky.
     */
    @RepeatedTest(value = 20, name = "Run {currentRepetition} of {totalRepetitions}")
    void detectFlakyAsyncOperation(RepetitionInfo info) {
        var result = NotificationService.sendAsync("user@example.com");
        assertTrue(result.isDeliveredWithin(java.time.Duration.ofSeconds(5)),
                "Failed on repetition " + info.getCurrentRepetition());
    }
}
```

### Step 2: Diagnose Timing Dependencies

**Python:**
```python
import time
import pytest


class TestTimingDependencyDiagnosis:
    """Demonstrate timing-dependent flakiness and the fix."""

    # FLAKY VERSION - depends on execution speed
    def test_cache_expiry_flaky(self):
        cache = TimedCache(ttl_seconds=1)
        cache.put("key", "value")
        time.sleep(1)  # Flaky: sleep(1) with ttl=1 is a race condition
        assert cache.get("key") is None  # Sometimes passes, sometimes fails

    # STABLE VERSION - use controlled time
    def test_cache_expiry_stable(self, monkeypatch):
        fake_time = FakeClock(start=1000.0)
        monkeypatch.setattr(time, "monotonic", fake_time.now)

        cache = TimedCache(ttl_seconds=60)
        cache.put("key", "value")

        fake_time.advance(59)
        assert cache.get("key") == "value"  # Not expired yet

        fake_time.advance(2)
        assert cache.get("key") is None  # Expired


class FakeClock:
    """Deterministic clock for testing time-dependent code."""

    def __init__(self, start: float = 0.0):
        self._current = start

    def now(self) -> float:
        return self._current

    def advance(self, seconds: float):
        self._current += seconds
```

**JavaScript:**
```javascript
describe("timing dependency diagnosis", () => {
  // FLAKY VERSION
  test("cache expires after TTL (flaky)", async () => {
    const cache = new TimedCache({ ttlMs: 1000 });
    cache.set("key", "value");
    await new Promise((r) => setTimeout(r, 1000));
    expect(cache.get("key")).toBeNull(); // Race condition
  });

  // STABLE VERSION - use fake timers
  test("cache expires after TTL (stable)", () => {
    jest.useFakeTimers();
    const cache = new TimedCache({ ttlMs: 1000 });
    cache.set("key", "value");

    jest.advanceTimersByTime(999);
    expect(cache.get("key")).toBe("value"); // Not expired

    jest.advanceTimersByTime(2);
    expect(cache.get("key")).toBeNull(); // Expired

    jest.useRealTimers();
  });
});
```

**Java:**
```java
import org.junit.jupiter.api.Test;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;
import static org.junit.jupiter.api.Assertions.*;

class TimingDependencyTest {

    // STABLE VERSION - inject a controllable clock
    @Test
    void cacheExpiresAfterTtl() {
        var fixedInstant = Instant.parse("2025-01-01T00:00:00Z");
        var clock = Clock.fixed(fixedInstant, ZoneId.of("UTC"));

        var cache = new TimedCache(clock, java.time.Duration.ofMinutes(5));
        cache.put("key", "value");

        // Advance clock to just before expiry
        var beforeExpiry = Clock.fixed(
                fixedInstant.plusSeconds(299), ZoneId.of("UTC"));
        cache.setClock(beforeExpiry);
        assertEquals("value", cache.get("key"));

        // Advance clock past expiry
        var afterExpiry = Clock.fixed(
                fixedInstant.plusSeconds(301), ZoneId.of("UTC"));
        cache.setClock(afterExpiry);
        assertNull(cache.get("key"));
    }
}
```

### Step 3: Diagnose Test Ordering Dependencies

**Python:**
```python
# Run with randomized order to detect ordering dependencies:
# pip install pytest-randomly
# pytest -p randomly --randomly-seed=12345

# Fix ordering dependency by ensuring each test sets up its own state:

import pytest

@pytest.fixture(autouse=True)
def reset_database(db_connection):
    """Roll back all changes after each test to prevent state leakage."""
    db_connection.begin()
    yield
    db_connection.rollback()


class TestUserRegistration:
    """Each test is independent thanks to the autouse fixture."""

    def test_register_new_user(self, db_connection):
        user = register_user(db_connection, "alice@example.com")
        assert user.id is not None

    def test_duplicate_email_raises(self, db_connection):
        register_user(db_connection, "bob@example.com")
        with pytest.raises(DuplicateEmailError):
            register_user(db_connection, "bob@example.com")

    def test_list_users_empty_initially(self, db_connection):
        # This test would fail if test_register_new_user ran first
        # without proper cleanup. The rollback fixture prevents this.
        users = list_users(db_connection)
        assert len(users) == 0
```

**JavaScript:**
```javascript
// Detect ordering issues by running with --randomize:
// jest --randomize

describe("test ordering dependency fix", () => {
  let db;

  beforeEach(async () => {
    // Fresh database state for each test
    db = await createTestDatabase();
    await db.migrate();
  });

  afterEach(async () => {
    await db.destroy();
  });

  test("register new user", async () => {
    const user = await registerUser(db, "alice@example.com");
    expect(user.id).toBeDefined();
  });

  test("list users is empty initially", async () => {
    // Independent of other tests because of beforeEach/afterEach
    const users = await listUsers(db);
    expect(users).toHaveLength(0);
  });
});
```

**Java:**
```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

// Randomize test order to detect dependencies:
@TestMethodOrder(MethodOrderer.Random.class)
class OrderingDependencyTest {

    private Database db;

    @BeforeEach
    void setUp() {
        db = TestDatabaseFactory.createFresh();
        db.migrate();
    }

    @AfterEach
    void tearDown() {
        db.destroy();
    }

    @Test
    void registerNewUser() {
        var user = UserService.register(db, "alice@example.com");
        assertNotNull(user.getId());
    }

    @Test
    void listUsersEmptyInitially() {
        var users = UserService.listAll(db);
        assertTrue(users.isEmpty());
    }
}
```

### Step 4: Diagnose Shared State and Resource Conflicts

**Python:**
```python
import pytest
import socket


def find_free_port() -> int:
    """Find a free port to avoid conflicts between parallel tests."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture
def server_port():
    """Each test gets its own port to prevent resource conflicts."""
    return find_free_port()


class TestApiServer:
    """Tests that avoid port conflicts through dynamic port allocation."""

    def test_server_starts_and_responds(self, server_port):
        server = start_test_server(port=server_port)
        try:
            response = http_get(f"http://localhost:{server_port}/health")
            assert response.status_code == 200
        finally:
            server.stop()

    def test_server_handles_concurrent_requests(self, server_port):
        server = start_test_server(port=server_port)
        try:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
                futures = [
                    pool.submit(http_get, f"http://localhost:{server_port}/health")
                    for _ in range(10)
                ]
                results = [f.result() for f in futures]
            assert all(r.status_code == 200 for r in results)
        finally:
            server.stop()
```

**JavaScript:**
```javascript
const getPort = require("get-port");

describe("shared state fix", () => {
  let server;
  let port;

  beforeEach(async () => {
    port = await getPort();
    server = await startTestServer({ port });
  });

  afterEach(async () => {
    await server.close();
  });

  test("server responds to health check", async () => {
    const response = await fetch(`http://localhost:${port}/health`);
    expect(response.status).toBe(200);
  });

  test("server handles concurrent requests", async () => {
    const requests = Array.from({ length: 10 }, () =>
      fetch(`http://localhost:${port}/health`)
    );
    const responses = await Promise.all(requests);
    responses.forEach((r) => expect(r.status).toBe(200));
  });
});
```

### Step 5: Diagnose Network Dependencies

Replace real network calls with deterministic mocks.

**Python:**
```python
from unittest.mock import patch, MagicMock


class TestExternalApiIntegration:
    """Replace network dependencies with deterministic mocks."""

    @patch("mymodule.requests.get")
    def test_fetch_weather_success(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"temperature": 22.5, "unit": "celsius"},
        )
        result = fetch_weather("London")
        assert result["temperature"] == 22.5

    @patch("mymodule.requests.get")
    def test_fetch_weather_timeout(self, mock_get):
        import requests
        mock_get.side_effect = requests.Timeout("Connection timed out")
        result = fetch_weather("London")
        assert result is None  # Graceful degradation

    @patch("mymodule.requests.get")
    def test_fetch_weather_server_error(self, mock_get):
        mock_get.return_value = MagicMock(status_code=500)
        result = fetch_weather("London")
        assert result is None
```

**JavaScript:**
```javascript
describe("network dependency stabilization", () => {
  beforeEach(() => {
    jest.spyOn(global, "fetch");
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("fetch weather returns data on success", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ temperature: 22.5, unit: "celsius" }),
    });
    const result = await fetchWeather("London");
    expect(result.temperature).toBe(22.5);
  });

  test("fetch weather returns null on network error", async () => {
    global.fetch.mockRejectedValueOnce(new Error("Network error"));
    const result = await fetchWeather("London");
    expect(result).toBeNull();
  });
});
```

**Java:**
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class NetworkDependencyTest {

    @Mock
    private HttpClient httpClient;

    @Test
    void fetchWeatherReturnsDataOnSuccess() throws Exception {
        when(httpClient.get("https://api.weather.com/London"))
                .thenReturn(new HttpResponse(200, "{\"temperature\":22.5}"));

        var service = new WeatherService(httpClient);
        var result = service.fetchWeather("London");

        assertEquals(22.5, result.getTemperature(), 0.01);
    }

    @Test
    void fetchWeatherReturnsNullOnTimeout() throws Exception {
        when(httpClient.get(anyString()))
                .thenThrow(new java.net.SocketTimeoutException("timed out"));

        var service = new WeatherService(httpClient);
        var result = service.fetchWeather("London");

        assertNull(result);
    }
}
```

### Step 6: Implement a Quarantine System

**Python (pytest marker-based quarantine):**
```python
# conftest.py
import pytest
import json
from pathlib import Path

QUARANTINE_FILE = Path(__file__).parent / "quarantined_tests.json"

def pytest_configure(config):
    config.addinivalue_line("markers", "quarantine: mark test as flaky/quarantined")

def pytest_collection_modifyitems(config, items):
    """Skip quarantined tests unless explicitly requested."""
    if config.getoption("--run-quarantine", default=False):
        return
    quarantine_marker = pytest.mark.skip(reason="Quarantined: flaky test")
    for item in items:
        if item.get_closest_marker("quarantine"):
            item.add_marker(quarantine_marker)

def pytest_addoption(parser):
    parser.addoption(
        "--run-quarantine",
        action="store_true",
        default=False,
        help="Run quarantined (flaky) tests",
    )


# Usage in tests:
@pytest.mark.quarantine
def test_known_flaky_notification():
    """Quarantined: intermittent timeout on CI runners. See JIRA-1234."""
    result = send_notification_async("user@example.com")
    assert result.delivered_within(seconds=5)
```

**JavaScript (Jest with test tagging):**
```javascript
// Create a quarantine utility
// quarantine.js
const QUARANTINED = process.env.RUN_QUARANTINE === "true";

function quarantinedTest(name, fn) {
  if (QUARANTINED) {
    test(name, fn);
  } else {
    test.skip(`[QUARANTINED] ${name}`, fn);
  }
}

module.exports = { quarantinedTest };

// Usage:
const { quarantinedTest } = require("./quarantine");

quarantinedTest("flaky notification delivery", async () => {
  const result = await sendNotificationAsync("user@example.com");
  expect(result.deliveredWithin(5000)).toBe(true);
});

// Run quarantined tests explicitly:
// RUN_QUARANTINE=true jest
```

**Java (JUnit 5 with custom annotation):**
```java
import java.lang.annotation.*;
import org.junit.jupiter.api.Tag;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Tag("quarantine")
public @interface Quarantined {
    String reason();
    String ticket() default "";
}

// Usage:
class NotificationTest {

    @Quarantined(reason = "Intermittent timeout on CI", ticket = "JIRA-1234")
    @Test
    void flakyNotificationDelivery() {
        var result = NotificationService.sendAsync("user@example.com");
        assertTrue(result.isDeliveredWithin(java.time.Duration.ofSeconds(5)));
    }
}

// Maven: exclude quarantined tests by default
// <configuration>
//   <excludedGroups>quarantine</excludedGroups>
// </configuration>
//
// Run quarantined: mvn test -Dgroups=quarantine
```

### Step 7: Compute and Track Flakiness Scores

**Python:**
```python
import json
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TestResult:
    name: str
    passed: bool
    timestamp: datetime


@dataclass
class FlakinessTracker:
    """Track flakiness scores across CI runs."""
    history: dict = field(default_factory=dict)

    def record(self, result: TestResult):
        if result.name not in self.history:
            self.history[result.name] = []
        self.history[result.name].append(result.passed)

    def flakiness_score(self, test_name: str, window: int = 100) -> float:
        """Return flakiness score between 0.0 (stable) and 1.0 (maximally flaky).

        A test that always passes or always fails scores 0.0.
        A test that alternates pass/fail scores close to 1.0.
        """
        runs = self.history.get(test_name, [])[-window:]
        if len(runs) < 2:
            return 0.0
        pass_rate = sum(runs) / len(runs)
        # Flakiness is highest when pass_rate is near 0.5
        return 4 * pass_rate * (1 - pass_rate)

    def get_flaky_tests(self, threshold: float = 0.1) -> list:
        """Return tests with flakiness score above the threshold."""
        flaky = []
        for name in self.history:
            score = self.flakiness_score(name)
            if score > threshold:
                flaky.append({"name": name, "score": round(score, 3)})
        return sorted(flaky, key=lambda x: x["score"], reverse=True)
```

## Best Practices

- **Treat flaky tests as bugs**: A flaky test is a defect in the test code or the production code; track it with the same urgency as a production bug
- **Fix or quarantine immediately**: A flaky test that blocks the pipeline erodes trust; quarantine it the same day and schedule a fix within the sprint
- **Make time deterministic**: Inject clocks and timers instead of using real wall-clock time; this eliminates the most common flakiness category
- **Isolate test state completely**: Each test must set up its own preconditions and tear down its own side effects; use transactions, temp directories, and fresh instances
- **Avoid arbitrary sleeps**: Replace `sleep(2)` with polling loops that have explicit timeouts, or use fake timers
- **Run tests in random order regularly**: This exposes ordering dependencies before they cause production pipeline failures
- **Monitor flakiness metrics continuously**: Track flakiness scores over time and set quality gates (e.g., no test may exceed a 5% flakiness rate)
- **Use retry with caution**: Automatic retries mask flakiness; use them only as a short-term mitigation while you fix the root cause
- **Document quarantined tests**: Every quarantined test should have a ticket, a root cause hypothesis, and a target fix date

## Common Pitfalls

- **Ignoring flaky tests because they "usually pass"**: Flaky tests that fail 5% of the time will fail daily in a suite of hundreds of tests
- **Adding retries without investigating**: Retries reduce visible failures but do not fix the underlying defect; the same race condition exists in production code
- **Blaming CI infrastructure**: While CI runner variance does contribute, most flakiness is caused by test design defects (shared state, timing, network dependencies)
- **Quarantining without a plan to fix**: Quarantine is a triage tool, not a permanent solution; quarantined tests that linger for months indicate a process failure
- **Running only in sequential order**: Sequential-only execution hides ordering dependencies that will surface when you parallelize for speed
- **Using real databases without isolation**: Shared test databases cause ordering dependencies and resource conflicts; use per-test schemas, transactions, or containers
- **Hardcoding ports and file paths**: Tests that bind to port 8080 or write to `/tmp/test.txt` conflict when run in parallel; use dynamic allocation
- **Testing async operations with sleep**: `sleep(2)` is never the right way to wait for an async operation; use explicit completion signals, polling with backoff, or fake timers
- **Merging code with known flaky tests**: Flaky tests in the main branch erode trust progressively; enforce a "no new flaky tests" policy in code review
