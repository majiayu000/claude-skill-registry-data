---
name: bug-reproduction-test-generator
description: Create minimal reproduction tests from bug reports and error descriptions. Use when writing failing tests from bug reports, creating minimal reproductions.
---

# Bug Reproduction Test Generator

Transform bug reports, error descriptions, and production incident logs into minimal, isolated reproduction tests that reliably demonstrate the defect. These tests serve as the foundation for debugging, patch validation, and long-term regression prevention.

## When to Use This Skill

Use this skill when you need to:

- Convert a natural-language bug report into a failing test case
- Create a minimal reproduction from a complex failure scenario
- Isolate a bug from its surrounding context to simplify debugging
- Generate regression tests from production incidents or customer-reported issues
- Build a test that reliably fails before a fix and passes after it
- Reduce a large, complex test to the smallest case that still triggers the bug
- Set up the exact environment conditions needed to reproduce an intermittent failure

**Trigger phrases**: "write a reproduction test", "create a failing test", "reproduce this bug", "minimal reproduction", "write a test for this bug report", "create regression test", "isolate the failure", "test case from bug report"

## What This Skill Does

### Methodology Overview

The reproduction test generation process follows five stages:

1. **Bug Report Parsing** -- Extract the essential facts from the report: inputs, expected output, actual output, error messages, and environment constraints.
2. **Environment Setup** -- Determine and configure the minimal environment needed to reproduce the bug (dependencies, database state, configuration, mocks).
3. **Minimal Reproduction Construction** -- Build the smallest possible test that triggers the defect, removing all unnecessary setup, data, and code paths.
4. **Assertion Generation** -- Write assertions that capture both the buggy behavior (to confirm the test fails before the fix) and the expected behavior (to confirm the test passes after the fix).
5. **Test Isolation** -- Ensure the test is independent of external state, execution order, and other tests so it can run reliably in any environment.

### Reproduction Quality Criteria

| Criterion | Description |
|-----------|-------------|
| Minimality | The test includes only the code and data necessary to trigger the bug |
| Reliability | The test fails 100% of the time on the buggy code (not flaky) |
| Isolation | The test does not depend on external services, file system state, or other tests |
| Clarity | The test clearly documents what the bug is and what the expected behavior should be |
| Speed | The test runs quickly (under 1 second for unit-level reproductions) |

## Instructions

### Step 1: Parse the Bug Report

Extract structured information from the bug report to guide test generation.

**Python: Bug report to test specification**

```python
from dataclasses import dataclass, field
import re

@dataclass
class TestSpecification:
    """Structured specification extracted from a bug report."""
    bug_id: str = ""
    title: str = ""
    module_under_test: str = ""
    function_under_test: str = ""
    input_values: dict = field(default_factory=dict)
    expected_output: str = ""
    actual_output: str = ""
    error_type: str = ""
    error_message: str = ""
    preconditions: list[str] = field(default_factory=list)
    environment: dict[str, str] = field(default_factory=dict)

def extract_test_spec(bug_report_text: str) -> TestSpecification:
    """Extract a test specification from a bug report."""
    spec = TestSpecification()

    # Extract bug ID from common formats
    id_match = re.search(r"(?:BUG|ISSUE|TICKET)[- #](\d+)", bug_report_text, re.IGNORECASE)
    if id_match:
        spec.bug_id = id_match.group(1)

    # Extract expected vs actual behavior
    expected_match = re.search(
        r"(?:expected|should)\s*(?:behavior|result|output)?[:\s]+(.+?)(?:\n|$)",
        bug_report_text, re.IGNORECASE,
    )
    if expected_match:
        spec.expected_output = expected_match.group(1).strip()

    actual_match = re.search(
        r"(?:actual|instead|but)\s*(?:behavior|result|output)?[:\s]+(.+?)(?:\n|$)",
        bug_report_text, re.IGNORECASE,
    )
    if actual_match:
        spec.actual_output = actual_match.group(1).strip()

    # Extract error information
    error_match = re.search(
        r"((?:Error|Exception|TypeError|ValueError|KeyError|NullPointer)\w*)[:\s]+(.+?)(?:\n|$)",
        bug_report_text,
    )
    if error_match:
        spec.error_type = error_match.group(1)
        spec.error_message = error_match.group(2).strip()

    # Extract code references
    file_match = re.search(r"(?:in|at|file)\s+[`'\"]?(\w+\.(?:py|js|java|ts))[`'\"]?", bug_report_text, re.IGNORECASE)
    if file_match:
        spec.module_under_test = file_match.group(1)

    func_match = re.search(r"(?:function|method|def)\s+[`'\"]?(\w+)[`'\"]?", bug_report_text, re.IGNORECASE)
    if func_match:
        spec.function_under_test = func_match.group(1)

    return spec


def generate_test_name(spec: TestSpecification) -> str:
    """Generate a descriptive test name from the specification."""
    parts = ["test"]
    if spec.bug_id:
        parts.append(f"bug_{spec.bug_id}")
    if spec.function_under_test:
        parts.append(spec.function_under_test)
    if spec.error_type:
        parts.append(f"raises_{spec.error_type.lower()}")
    elif spec.actual_output:
        sanitized = re.sub(r"[^a-zA-Z0-9]", "_", spec.actual_output[:30])
        parts.append(f"returns_{sanitized}")
    return "_".join(parts)
```

**JavaScript: Bug report to test specification**

```javascript
class TestSpecification {
  constructor() {
    this.bugId = "";
    this.title = "";
    this.moduleUnderTest = "";
    this.functionUnderTest = "";
    this.inputValues = {};
    this.expectedOutput = "";
    this.actualOutput = "";
    this.errorType = "";
    this.errorMessage = "";
    this.preconditions = [];
    this.environment = {};
  }
}

function extractTestSpec(bugReportText) {
  const spec = new TestSpecification();

  const idMatch = bugReportText.match(/(?:BUG|ISSUE|TICKET)[- #](\d+)/i);
  if (idMatch) spec.bugId = idMatch[1];

  const expectedMatch = bugReportText.match(
    /(?:expected|should)\s*(?:behavior|result|output)?[:\s]+(.+?)(?:\n|$)/i
  );
  if (expectedMatch) spec.expectedOutput = expectedMatch[1].trim();

  const actualMatch = bugReportText.match(
    /(?:actual|instead|but)\s*(?:behavior|result|output)?[:\s]+(.+?)(?:\n|$)/i
  );
  if (actualMatch) spec.actualOutput = actualMatch[1].trim();

  const errorMatch = bugReportText.match(
    /((?:Error|Exception|TypeError|RangeError)\w*)[:\s]+(.+?)(?:\n|$)/
  );
  if (errorMatch) {
    spec.errorType = errorMatch[1];
    spec.errorMessage = errorMatch[2].trim();
  }

  const fileMatch = bugReportText.match(
    /(?:in|at|file)\s+[`'"]?(\w+\.(?:js|ts|jsx|tsx))[`'"]?/i
  );
  if (fileMatch) spec.moduleUnderTest = fileMatch[1];

  const funcMatch = bugReportText.match(
    /(?:function|method)\s+[`'"]?(\w+)[`'"]?/i
  );
  if (funcMatch) spec.functionUnderTest = funcMatch[1];

  return spec;
}

function generateTestName(spec) {
  const parts = [];
  if (spec.bugId) parts.push(`bug ${spec.bugId}`);
  if (spec.functionUnderTest) parts.push(spec.functionUnderTest);
  if (spec.errorType) {
    parts.push(`throws ${spec.errorType}`);
  } else if (spec.actualOutput) {
    parts.push(`returns incorrect result`);
  }
  return parts.join(" - ") || "reproduction test";
}
```

**Java: Bug report to test specification**

```java
import java.util.regex.*;
import java.util.*;

public class TestSpecExtractor {
    public record TestSpecification(
        String bugId,
        String title,
        String moduleUnderTest,
        String functionUnderTest,
        String expectedOutput,
        String actualOutput,
        String errorType,
        String errorMessage,
        List<String> preconditions
    ) {}

    public static TestSpecification extract(String bugReportText) {
        String bugId = extractPattern(
            bugReportText, "(?i)(?:BUG|ISSUE|TICKET)[- #](\\d+)"
        );
        String expected = extractPattern(
            bugReportText,
            "(?i)(?:expected|should)\\s*(?:behavior|result|output)?[:\\s]+(.+?)(?:\\n|$)"
        );
        String actual = extractPattern(
            bugReportText,
            "(?i)(?:actual|instead|but)\\s*(?:behavior|result|output)?[:\\s]+(.+?)(?:\\n|$)"
        );
        String errorType = extractPattern(
            bugReportText,
            "((?:Error|Exception|NullPointer|ClassCast)\\w*)[:\\s]"
        );
        String errorMessage = extractPattern(
            bugReportText,
            "(?:Error|Exception|NullPointer|ClassCast)\\w*[:\\s]+(.+?)(?:\\n|$)"
        );
        String module = extractPattern(
            bugReportText,
            "(?i)(?:in|at|class)\\s+[`'\"]?(\\w+(?:\\.\\w+)*)[`'\"]?"
        );
        String function = extractPattern(
            bugReportText,
            "(?i)(?:function|method)\\s+[`'\"]?(\\w+)[`'\"]?"
        );

        return new TestSpecification(
            bugId != null ? bugId : "",
            "", module != null ? module : "",
            function != null ? function : "",
            expected != null ? expected.trim() : "",
            actual != null ? actual.trim() : "",
            errorType != null ? errorType : "",
            errorMessage != null ? errorMessage.trim() : "",
            List.of()
        );
    }

    private static String extractPattern(String text, String regex) {
        Matcher m = Pattern.compile(regex).matcher(text);
        return m.find() ? m.group(1) : null;
    }

    public static String generateTestMethodName(TestSpecification spec) {
        StringBuilder name = new StringBuilder("test");
        if (!spec.bugId().isEmpty()) {
            name.append("Bug").append(spec.bugId()).append("_");
        }
        if (!spec.functionUnderTest().isEmpty()) {
            name.append(spec.functionUnderTest()).append("_");
        }
        if (!spec.errorType().isEmpty()) {
            name.append("Throws").append(
                spec.errorType().replace("Exception", ""));
        } else {
            name.append("ReturnsExpectedResult");
        }
        return name.toString();
    }
}
```

### Step 2: Set Up the Minimal Environment

Determine what environment setup the test needs and configure it with the minimum required state.

**Python: Environment setup helpers**

```python
import tempfile
import os
from contextlib import contextmanager
from unittest.mock import MagicMock

@contextmanager
def minimal_file_system(files: dict[str, str]):
    """Create a temporary file system with only the files needed for reproduction."""
    with tempfile.TemporaryDirectory() as tmpdir:
        for relative_path, content in files.items():
            full_path = os.path.join(tmpdir, relative_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            yield tmpdir
        finally:
            os.chdir(original_cwd)


@contextmanager
def minimal_database_state(records: list[dict], table_name: str = "test_table"):
    """Create an in-memory SQLite database with minimal test data."""
    import sqlite3
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    if records:
        columns = records[0].keys()
        col_defs = ", ".join(f"{col} TEXT" for col in columns)
        cursor.execute(f"CREATE TABLE {table_name} ({col_defs})")

        placeholders = ", ".join("?" for _ in columns)
        for record in records:
            values = tuple(str(v) for v in record.values())
            cursor.execute(
                f"INSERT INTO {table_name} VALUES ({placeholders})", values
            )
        conn.commit()

    try:
        yield conn
    finally:
        conn.close()


def create_mock_dependency(interface_methods: dict[str, any]) -> MagicMock:
    """Create a mock object with specific return values for reproduction."""
    mock = MagicMock()
    for method_name, return_value in interface_methods.items():
        if callable(return_value):
            getattr(mock, method_name).side_effect = return_value
        else:
            getattr(mock, method_name).return_value = return_value
    return mock
```

**JavaScript: Environment setup helpers**

```javascript
const fs = require("fs");
const path = require("path");
const os = require("os");

function createMinimalFileSystem(files) {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "repro-"));

  for (const [relativePath, content] of Object.entries(files)) {
    const fullPath = path.join(tmpDir, relativePath);
    fs.mkdirSync(path.dirname(fullPath), { recursive: true });
    fs.writeFileSync(fullPath, content);
  }

  return {
    rootDir: tmpDir,
    cleanup() {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    },
  };
}

function createMockDependency(interfaceMethods) {
  const mock = {};
  for (const [method, behavior] of Object.entries(interfaceMethods)) {
    if (typeof behavior === "function") {
      mock[method] = jest.fn().mockImplementation(behavior);
    } else {
      mock[method] = jest.fn().mockReturnValue(behavior);
    }
  }
  return mock;
}

function withEnvironmentVariables(vars, testFn) {
  const original = {};
  for (const [key, value] of Object.entries(vars)) {
    original[key] = process.env[key];
    process.env[key] = value;
  }

  try {
    return testFn();
  } finally {
    for (const [key] of Object.entries(vars)) {
      if (original[key] === undefined) {
        delete process.env[key];
      } else {
        process.env[key] = original[key];
      }
    }
  }
}
```

**Java: Environment setup helpers**

```java
import java.nio.file.*;
import java.util.*;

public class MinimalEnvironment implements AutoCloseable {
    private final Path tempDir;

    public MinimalEnvironment(Map<String, String> files) throws Exception {
        this.tempDir = Files.createTempDirectory("repro-");

        for (var entry : files.entrySet()) {
            Path filePath = tempDir.resolve(entry.getKey());
            Files.createDirectories(filePath.getParent());
            Files.writeString(filePath, entry.getValue());
        }
    }

    public Path getRoot() {
        return tempDir;
    }

    public Path resolve(String relativePath) {
        return tempDir.resolve(relativePath);
    }

    @Override
    public void close() throws Exception {
        // Recursively delete temp directory
        Files.walk(tempDir)
            .sorted(Comparator.reverseOrder())
            .forEach(path -> {
                try { Files.delete(path); }
                catch (Exception ignored) {}
            });
    }
}
```

### Step 3: Generate the Minimal Reproduction Test

Build the test that demonstrates the bug with the least amount of code possible.

**Python: Reproduction test generator**

```python
def generate_python_reproduction_test(spec: TestSpecification) -> str:
    """Generate a Python reproduction test from the specification."""
    test_name = generate_test_name(spec)
    imports = []
    setup_lines = []
    act_lines = []
    assert_lines = []

    # Determine imports
    if spec.module_under_test:
        module = spec.module_under_test.replace(".py", "")
        if spec.function_under_test:
            imports.append(f"from {module} import {spec.function_under_test}")
        else:
            imports.append(f"import {module}")

    if spec.error_type:
        imports.append("import pytest")

    # Build setup section
    for key, value in spec.input_values.items():
        setup_lines.append(f"    {key} = {repr(value)}")

    if not setup_lines:
        setup_lines.append("    # TODO: Add the specific input values from the bug report")

    # Build act section
    if spec.function_under_test:
        if spec.error_type:
            act_lines.append(f"    with pytest.raises({spec.error_type}):")
            act_lines.append(f"        {spec.function_under_test}()")
            act_lines.append(f"        # TODO: Add the arguments that trigger the bug")
        else:
            act_lines.append(f"    result = {spec.function_under_test}()")
            act_lines.append(f"    # TODO: Add the arguments that trigger the bug")
    else:
        act_lines.append("    # TODO: Call the function that triggers the bug")
        act_lines.append("    result = None")

    # Build assert section
    if spec.expected_output and not spec.error_type:
        assert_lines.append(f"    # Bug: actual output was: {spec.actual_output}")
        assert_lines.append(f"    # Expected: {spec.expected_output}")
        assert_lines.append(f"    assert result == {repr(spec.expected_output)}")
    elif not spec.error_type:
        assert_lines.append(f"    # TODO: Assert the expected behavior")
        assert_lines.append(f"    # Before fix: this assertion should FAIL")
        assert_lines.append(f"    # After fix: this assertion should PASS")
        assert_lines.append(f"    assert result is not None")

    # Compose the test
    parts = []
    if imports:
        parts.append("\n".join(imports))
        parts.append("")

    parts.append("")
    parts.append(f"def {test_name}():")
    parts.append(f'    """Reproduction test for bug{" " + spec.bug_id if spec.bug_id else ""}.')
    parts.append(f"")
    if spec.title:
        parts.append(f"    {spec.title}")
    if spec.actual_output:
        parts.append(f"    Bug: {spec.actual_output}")
    if spec.expected_output:
        parts.append(f"    Expected: {spec.expected_output}")
    parts.append(f'    """')

    parts.append("    # Arrange")
    parts.extend(setup_lines)
    parts.append("")
    parts.append("    # Act")
    parts.extend(act_lines)
    parts.append("")

    if assert_lines:
        parts.append("    # Assert")
        parts.extend(assert_lines)

    return "\n".join(parts) + "\n"
```

**JavaScript: Reproduction test generator**

```javascript
function generateJestReproductionTest(spec) {
  const testName = generateTestName(spec);
  const lines = [];

  // Imports
  if (spec.moduleUnderTest) {
    const modulePath = spec.moduleUnderTest.replace(/\.(js|ts)$/, "");
    if (spec.functionUnderTest) {
      lines.push(
        `const { ${spec.functionUnderTest} } = require("./${modulePath}");`
      );
    } else {
      lines.push(`const module = require("./${modulePath}");`);
    }
    lines.push("");
  }

  // Test block
  lines.push(`describe("Bug Reproduction${spec.bugId ? ` #${spec.bugId}` : ""}", () => {`);
  lines.push(`  it("${testName}", () => {`);

  // Documentation
  if (spec.actualOutput) {
    lines.push(`    // Bug: ${spec.actualOutput}`);
  }
  if (spec.expectedOutput) {
    lines.push(`    // Expected: ${spec.expectedOutput}`);
  }
  lines.push("");

  // Arrange
  lines.push("    // Arrange");
  if (Object.keys(spec.inputValues).length > 0) {
    for (const [key, value] of Object.entries(spec.inputValues)) {
      lines.push(`    const ${key} = ${JSON.stringify(value)};`);
    }
  } else {
    lines.push(
      "    // TODO: Add the specific input values from the bug report"
    );
  }
  lines.push("");

  // Act
  lines.push("    // Act");
  if (spec.functionUnderTest) {
    if (spec.errorType) {
      lines.push(
        `    expect(() => ${spec.functionUnderTest}()).toThrow(${spec.errorType});`
      );
      lines.push(
        "    // TODO: Add the arguments that trigger the bug"
      );
    } else {
      lines.push(
        `    const result = ${spec.functionUnderTest}();`
      );
      lines.push(
        "    // TODO: Add the arguments that trigger the bug"
      );
    }
  } else {
    lines.push("    // TODO: Call the function that triggers the bug");
    lines.push("    const result = null;");
  }
  lines.push("");

  // Assert
  if (!spec.errorType) {
    lines.push("    // Assert");
    lines.push("    // Before fix: this assertion should FAIL");
    lines.push("    // After fix: this assertion should PASS");
    if (spec.expectedOutput) {
      lines.push(`    expect(result).toEqual(${JSON.stringify(spec.expectedOutput)});`);
    } else {
      lines.push("    expect(result).not.toBeNull();");
      lines.push("    // TODO: Add specific assertion for expected behavior");
    }
  }

  lines.push("  });");
  lines.push("});");

  return lines.join("\n") + "\n";
}
```

**Java: Reproduction test generator**

```java
public class ReproductionTestGenerator {

    public static String generateJUnit5Test(TestSpecExtractor.TestSpecification spec) {
        String testMethodName = TestSpecExtractor.generateTestMethodName(spec);
        StringBuilder sb = new StringBuilder();

        // Imports
        sb.append("import org.junit.jupiter.api.Test;\n");
        sb.append("import org.junit.jupiter.api.DisplayName;\n");
        if (!spec.errorType().isEmpty()) {
            sb.append("import static org.junit.jupiter.api.Assertions.assertThrows;\n");
        }
        sb.append("import static org.junit.jupiter.api.Assertions.*;\n");
        sb.append("\n");

        // Class
        String className = "Bug" + (spec.bugId().isEmpty() ? "Reproduction" : spec.bugId())
            + "ReproductionTest";
        sb.append("class ").append(className).append(" {\n\n");

        // Test method
        String displayName = "Reproduction: " + (spec.title().isEmpty()
            ? "Bug #" + spec.bugId() : spec.title());
        sb.append("    @Test\n");
        sb.append("    @DisplayName(\"").append(displayName).append("\")\n");
        sb.append("    void ").append(testMethodName).append("() {\n");

        // Documentation
        if (!spec.actualOutput().isEmpty()) {
            sb.append("        // Bug: ").append(spec.actualOutput()).append("\n");
        }
        if (!spec.expectedOutput().isEmpty()) {
            sb.append("        // Expected: ").append(spec.expectedOutput()).append("\n");
        }
        sb.append("\n");

        // Arrange
        sb.append("        // Arrange\n");
        sb.append("        // TODO: Set up the exact conditions from the bug report\n\n");

        // Act & Assert
        if (!spec.errorType().isEmpty()) {
            sb.append("        // Act & Assert\n");
            sb.append("        assertThrows(").append(spec.errorType()).append(".class, () -> {\n");
            if (!spec.functionUnderTest().isEmpty()) {
                sb.append("            // TODO: Call ").append(spec.functionUnderTest());
                sb.append(" with arguments that trigger the bug\n");
            }
            sb.append("        });\n");
        } else {
            sb.append("        // Act\n");
            if (!spec.functionUnderTest().isEmpty()) {
                sb.append("        // var result = instance.")
                    .append(spec.functionUnderTest()).append("();\n");
                sb.append("        // TODO: Add arguments that trigger the bug\n\n");
            }
            sb.append("        // Assert\n");
            sb.append("        // Before fix: this assertion should FAIL\n");
            sb.append("        // After fix: this assertion should PASS\n");
            if (!spec.expectedOutput().isEmpty()) {
                sb.append("        // assertEquals(\"")
                    .append(spec.expectedOutput()).append("\", result);\n");
            } else {
                sb.append("        // assertNotNull(result);\n");
                sb.append("        // TODO: Add specific assertion for expected behavior\n");
            }
        }

        sb.append("    }\n");
        sb.append("}\n");

        return sb.toString();
    }
}
```

### Step 4: Apply Test Minimization

Reduce an existing complex reproduction to its minimal form.

**Python: Test minimizer**

```python
def minimize_reproduction(
    original_test_fn,
    setup_elements: list,
    verify_failure_fn,
) -> list:
    """Reduce the setup of a reproduction test to its minimal elements.

    Args:
        original_test_fn: The original test function (callable).
        setup_elements: List of setup steps that can be individually toggled.
        verify_failure_fn: Returns True if the bug still reproduces
                           with the given subset of setup elements.
    """
    # Start with all elements
    current = list(setup_elements)

    # Try removing each element one at a time
    changed = True
    while changed:
        changed = False
        for i in range(len(current) - 1, -1, -1):
            candidate = current[:i] + current[i + 1:]
            if verify_failure_fn(candidate):
                current = candidate
                changed = True
                break

    return current


def minimize_input_data(
    original_data: dict,
    test_fn,
) -> dict:
    """Reduce a complex input dictionary to the minimal keys needed to trigger the bug."""
    minimal = {}

    # First pass: find which top-level keys are required
    for key in original_data:
        subset = {k: v for k, v in original_data.items() if k != key}
        try:
            test_fn(subset)
            # If the test passes without this key, the key is needed
            # (we want the test to fail, meaning the bug reproduces)
        except Exception:
            # Bug still reproduces without this key; it is not needed
            continue
        minimal[key] = original_data[key]

    # If no keys were identified as required, all are needed
    if not minimal:
        return original_data

    # Verify that the minimal set still triggers the bug
    try:
        test_fn(minimal)
        return original_data  # Minimal set does not trigger; return original
    except Exception:
        return minimal
```

### Step 5: Ensure Test Isolation

Verify that the reproduction test is fully isolated and does not depend on external state.

**Python: Test isolation checker**

```python
import subprocess
import sys

class TestIsolationChecker:
    """Verify that a reproduction test is properly isolated."""

    def __init__(self, test_file: str, test_name: str):
        self.test_file = test_file
        self.test_name = test_name

    def run_test(self, extra_args: list[str] = None) -> bool:
        """Run the test and return True if it produces the expected result."""
        cmd = [sys.executable, "-m", "pytest", f"{self.test_file}::{self.test_name}", "-v"]
        if extra_args:
            cmd.extend(extra_args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode != 0  # We expect the test to fail (bug reproduces)

    def check_order_independence(self, other_tests: list[str]) -> bool:
        """Verify the test produces the same result regardless of execution order."""
        # Run the reproduction test alone
        alone_result = self.run_test()

        # Run it after other tests
        for other_test in other_tests:
            subprocess.run(
                [sys.executable, "-m", "pytest", other_test, "-v"],
                capture_output=True,
            )
        after_result = self.run_test()

        return alone_result == after_result

    def check_no_network(self) -> bool:
        """Verify the test does not make network calls."""
        result = self.run_test(["--disable-socket"])
        return result  # Should still reproduce without network

    def check_no_filesystem_side_effects(self, watch_dir: str) -> bool:
        """Verify the test does not leave files behind."""
        import os
        before = set(os.listdir(watch_dir))
        self.run_test()
        after = set(os.listdir(watch_dir))
        return before == after

    def generate_isolation_report(self) -> dict:
        """Generate a complete isolation check report."""
        return {
            "reproduces_standalone": self.run_test(),
            "no_filesystem_side_effects": self.check_no_filesystem_side_effects("."),
            "order_independent": True,  # Requires other test names to check fully
        }
```

**JavaScript: Test isolation checker**

```javascript
const { execSync } = require("child_process");

class TestIsolationChecker {
  constructor(testFile, testName) {
    this.testFile = testFile;
    this.testName = testName;
  }

  runTest(extraArgs = []) {
    try {
      execSync(
        `npx jest ${this.testFile} -t "${this.testName}" ${extraArgs.join(" ")}`,
        { stdio: "pipe", timeout: 30000 }
      );
      return false; // Test passed (bug did not reproduce)
    } catch {
      return true; // Test failed (bug reproduced)
    }
  }

  checkReproducesStandalone() {
    return this.runTest(["--forceExit", "--detectOpenHandles"]);
  }

  checkOrderIndependence() {
    // Run in random order multiple times
    const results = [];
    for (let i = 0; i < 3; i++) {
      results.push(this.runTest(["--randomize"]));
    }
    return results.every(r => r === results[0]);
  }

  generateReport() {
    return {
      reproducesStandalone: this.checkReproducesStandalone(),
      orderIndependent: this.checkOrderIndependence(),
    };
  }
}
```

## Best Practices

- Write the reproduction test before attempting any fix. This ensures you have a reliable way to confirm the bug exists and to validate the fix.
- Make the test name descriptive and include the bug ID. Future developers searching for the test should be able to find it from the bug report and vice versa.
- Include the bug report details (expected behavior, actual behavior) as comments in the test. The test should serve as living documentation of the defect.
- Use the Arrange-Act-Assert pattern consistently. Each section should be clearly labeled and separated so readers can quickly understand the test structure.
- Prefer in-memory fixtures over file system or database fixtures. In-memory setup is faster, more portable, and less likely to cause test pollution.
- Minimize the test aggressively. Every line of setup code that is not strictly necessary to reproduce the bug is noise that makes the test harder to understand and maintain.
- Verify that the test fails before the fix and passes after it. A reproduction test that passes even without the fix is useless.
- Run the reproduction test in isolation (not as part of a larger suite) to confirm it does not depend on side effects from other tests.
- Tag reproduction tests with the bug ID so they can be easily filtered and run as a group (for example, `@pytest.mark.bug_123` or `@Tag("BUG-123")`).

## Common Pitfalls

- **Writing a test that passes without the fix.** If the test does not actually fail on the buggy code, it cannot serve as a reproduction. Always verify the test against the unfixed code first.
- **Including unnecessary setup.** A reproduction test with 50 lines of database setup for a bug that only requires two input parameters is misleading. Minimize ruthlessly.
- **Depending on external state.** A reproduction test that requires a running database, a specific file on disk, or a network service is fragile. Mock or stub external dependencies.
- **Making the test order-dependent.** If the reproduction test only fails when run after another specific test, it is not a true reproduction. Ensure it fails when run in isolation.
- **Forgetting to document what the test reproduces.** A test named `test_bug_fix` with no comments tells future developers nothing. Include the bug ID, the expected behavior, and the actual behavior.
- **Not testing the negative case.** After the fix is applied, verify that the test now passes. Also verify that removing the fix causes the test to fail again. This round-trip confirms the test is genuinely tied to the bug.
- **Reproduction tests that are too slow.** A reproduction test that takes 30 seconds to run will be skipped or ignored. Keep reproduction tests fast (under 1 second for unit-level, under 10 seconds for integration-level).
- **Hardcoding environment-specific values.** File paths, port numbers, and hostnames that work on your machine will fail in CI. Use environment variables, temporary directories, and dynamic port allocation.
