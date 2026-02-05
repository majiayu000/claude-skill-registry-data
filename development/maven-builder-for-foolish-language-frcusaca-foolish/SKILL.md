---
name: maven-builder-for-foolish-language
description: Comprehensive Maven build strategies for mixed Java/Scala projects with parallel execution, intelligent test running, and targeted debugging workflows. Use this skill when user asks to build the project, run tests, compile code, clean build, run Maven commands, fix compilation errors, or analyze test failures. Automatically invoked for requests like "make a fresh build", "run all tests", "build and test", "clean and compile", or any Maven-related build tasks.
---

# Maven Builder Skill

## Overview
This skill provides comprehensive Maven build strategies for mixed Java/Scala projects with emphasis on parallel execution, intelligent test running, and targeted debugging workflows.

## Resource Detection

All build commands use dynamic resource detection to optimize parallelism based on the current machine:

```bash
# CPU cores (for thread calculations)
CORES=$(nproc)

# Total memory in GB (rounded down)
TOTAL_MEM_GB=$(free -g | awk '/^Mem:/{print int($2)}')

# Calculate optimal thread counts (rounded down to integers)
THREADS_2C=$((CORES * 2))      # Aggressive: 2 threads per core
THREADS_1C=$CORES              # Conservative: 1 thread per core
TEST_THREADS=$((CORES * 4))    # Test parallelism: 4 threads per core

# Memory allocation (50% of total, rounded down)
MAVEN_MEM_GB=$((TOTAL_MEM_GB / 2))
```

**Inline command examples** embed these calculations directly for single-line execution.

## Core Capabilities

### 1. Build Modes

#### Clean Parallel Build (From Scratch)
Use when starting fresh or after significant changes:
```bash
mvn clean compile -T $(($(nproc) * 2))
```
- **When to use**: Major refactoring, dependency updates, or when incremental builds seem unreliable
- **Parallel strategy**: 2 threads per core for maximum throughput (dynamically calculated)
- **Note**: This compiles both Java and Scala sources

#### Compilation Debugging (Skip Tests)
**CRITICAL**: When debugging compilation errors, ALWAYS skip tests to focus on making code compile:
```bash
mvn clean compile -T $(($(nproc) * 2)) -DskipTests
```
- **When to use**: Compilation errors, fixing type issues, resolving dependencies
- **Why skip tests**: Compilation must succeed before tests can run
- **Focus**: Get code to compile first, then worry about tests
- **Fast iteration**: Much faster feedback loop for fixing compiler errors

For incremental compilation debugging:
```bash
mvn compile -DskipTests
```

#### Compilation Debugging (Skip Tests)
**CRITICAL FOR BUILD ISSUES**: When debugging compilation errors, ALWAYS skip tests to focus on making code compile:
```bash
mvn clean compile -T $(($(nproc) * 2)) -DskipTests
```
- **When to use**: Compilation errors, refactoring broken code, fixing import issues
- **Why skip tests**: Tests can't run if code doesn't compile; faster iteration on compilation fixes
- **After fixing**: Run tests separately once compilation succeeds
- **Note**: Use `-DskipTests` not `-Dmaven.test.skip` (the latter skips test compilation too)

#### Incremental Build
For routine compilation after code changes:
```bash
mvn compile -T $(nproc)
```
- **When to use**: Normal development cycle with isolated changes
- **Parallel strategy**: 1 thread per core (conservative, dynamically calculated)

#### Source Generation (ANTLR4 or other generators)
When `.g4` files or other source generators are modified:
```bash
mvn generate-sources -T $(($(nproc) * 2))
```
- **When to use**: Changes to ANTLR4 grammars, protobuf definitions, or other code generators
- **Parallel strategy**: 2 threads per core (dynamically calculated)
- **Follow-up**: Usually requires `mvn compile -T $(($(nproc) * 2))` afterward

### 2. Test Execution Modes

#### Standard Parallel Test Run
Default testing approach for comprehensive validation:
```bash
mvn -T $(nproc) test -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4)) -DperCoreThreadCount=false
```
- **Parallelization**:
  - 1 thread per core for Maven build orchestration (dynamically calculated)
  - 4 threads per core for test execution (classes AND methods run in parallel, dynamically calculated)
  - `perCoreThreadCount=false` because threadCount already includes core multiplication
- **Parallel strategy**: Both test classes AND test methods run concurrently for maximum throughput
- **Output**: XML reports in `target/surefire-reports/` with readable summaries
- **When to use**: After code changes, before commits, CI/CD validation
- **Alternative**: Use `-Dparallel=classes -DthreadCount=$(($(nproc) * 4))` if method-level parallelization causes issues

#### Failed Tests Only (Verbose)
When tests fail and you need detailed diagnostics:
```bash
mvn -T $(nproc) surefire:test -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4)) \
  -Dsurefire.rerunFailingTestsCount=0 \
  -DtrimStackTrace=false \
  -Dsurefire.printSummary=true \
  -Dsurefire.useFile=true \
  -Dsurefire.reportFormat=xml
```
- **Purpose**: Generate extremely verbose XML output for failed tests
- **Still parallel**: Maintains parallelism (classes AND methods) for speed (dynamically calculated)
- **Output location**: `target/surefire-reports/*.xml`
- **Key flags**:
  - `trimStackTrace=false`: Full stack traces
  - `printSummary=true`: Readable summary in console
  - `useFile=true`: Detailed output to files

To re-run only failed tests from previous run:
```bash
mvn -T $(nproc) surefire:test -Dsurefire.rerunFailingTestsCount=0 -DrerunFailingTestsCount=0
```

#### Single Test Execution (Debugging)
For focused debugging of one specific test:
```bash
mvn test -Dtest=ClassName#methodName -DtrimStackTrace=false
```
- **Sequential execution**: No parallelism for clearer output
- **When to use**: Debugging specific test failures, race conditions, or flaky tests
- **Pattern matching**: Use `*` for wildcards, e.g., `-Dtest=*IntegrationTest`

#### Single Test Class
```bash
mvn test -Dtest=ClassName -DtrimStackTrace=false
```

### 2A. Approval Tests Parallelization

#### Background
Approval tests (also called golden master tests or snapshot tests) typically involve:
1. Loading test case definitions from resource files
2. Processing each test case
3. Comparing output against expected/approved results

Traditional loop-based approach is sequential:
```java
// Sequential - slow for many test cases
@Test
public void approvalTests() {
    for (String testFile : loadTestFiles()) {
        runApprovalTest(testFile);
    }
}
```

#### Parallelization Strategy

**Use JUnit 5 @ParameterizedTest with parallel execution:**

```java
@ParameterizedTest
@MethodSource("approvalTestCases")
@Execution(ExecutionMode.CONCURRENT)
void approvalTest(ApprovalTestCase testCase) {
    // Each test case runs in parallel
    String input = testCase.loadInput();
    String expected = testCase.loadExpected();
    String actual = processInput(input);
    
    assertEquals(expected, actual, 
        "Approval test failed for: " + testCase.getName());
}

static Stream<ApprovalTestCase> approvalTestCases() {
    // Load all test case files from resources
    return loadApprovalTestFiles()
        .map(ApprovalTestCase::fromFile);
}
```

**For JUnit 4, use parallel test methods:**

```java
public class ApprovalTests {
    private static List<ApprovalTestCase> TEST_CASES;
    
    @BeforeClass
    public static void loadTestCases() {
        TEST_CASES = loadApprovalTestFiles();
    }
    
    // Generate one @Test method per approval test case
    @Test public void approvalTest_001() { runTest(TEST_CASES.get(0)); }
    @Test public void approvalTest_002() { runTest(TEST_CASES.get(1)); }
    // ... etc, or use dynamic test generation
    
    private void runTest(ApprovalTestCase testCase) {
        String actual = processInput(testCase.getInput());
        assertEquals(testCase.getExpected(), actual);
    }
}
```

**Best approach: Dynamic test generation with JUnit 5 @TestFactory:**

```java
@TestFactory
Stream<DynamicTest> approvalTests() {
    return loadApprovalTestFiles()
        .map(testCase -> DynamicTest.dynamicTest(
            "Approval: " + testCase.getName(),
            () -> {
                String actual = processInput(testCase.getInput());
                assertEquals(testCase.getExpected(), actual);
            }
        ));
}
```

Then enable parallel execution in `junit-platform.properties`:
```properties
junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
junit.jupiter.execution.parallel.mode.classes.default=concurrent
```

#### Running Parallelized Approval Tests

**Full parallel execution:**
```bash
mvn test -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))
```

**Debugging single approval test:**
```bash
# For parameterized tests, specify the parameter
mvn test -Dtest="ApprovalTests#approvalTest*testCase001*" -DtrimStackTrace=false

# Or use display name filtering (JUnit 5)
mvn test -Dtest="ApprovalTests" \
  -Djunit.jupiter.displayname.generator.default=org.junit.jupiter.api.DisplayNameGenerator\$Simple \
  -DtrimStackTrace=false
```

**Debugging specific subset of approval tests:**
```bash
# Filter by test case name pattern
mvn test -Dtest="ApprovalTests#*edge_case*" -DtrimStackTrace=false
```

#### Approval Test File Organization

Recommended structure:
```
src/test/resources/
└── approval-tests/
    ├── basic/
    │   ├── test_001_input.txt
    │   ├── test_001_expected.txt
    │   ├── test_002_input.txt
    │   └── test_002_expected.txt
    ├── edge-cases/
    │   ├── null_handling_input.txt
    │   ├── null_handling_expected.txt
    │   └── ...
    └── regression/
        └── bug_123_input.txt
        └── bug_123_expected.txt
```

#### Benefits of Parallelized Approval Tests

1. **Speed**: 100 approval tests can run in ~1/4 the time with 4 threads
2. **Isolation**: Each test case is independent, reducing flakiness
3. **Debugging**: Can target single test case easily
4. **Scalability**: Add more test cases without impacting runtime proportionally
5. **CI/CD**: Faster feedback in continuous integration

#### Migration Pattern

**Phase 1: Refactor to parameterized tests** (still sequential)
```java
// Before: loop-based
@Test void allApprovalTests() { for(...) { ... } }

// After: parameterized (can run sequentially first)
@ParameterizedTest
@MethodSource("testCases")
void approvalTest(TestCase tc) { ... }
```

**Phase 2: Enable parallelization**
```bash
# Add to pom.xml or junit-platform.properties
# Then run with: mvn test -Dparallel=classesAndMethods
```

**Phase 3: Verify and optimize**
```bash
# Check test timings in XML reports
cd target/surefire-reports/
grep "time=" TEST-*.xml | sort -t'"' -k2 -n
```

### 3. Combined Build + Test Workflows

#### Full Clean Build with Tests
```bash
mvn clean test -T $(($(nproc) * 2)) -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))
```

#### Verify (includes integration tests)
```bash
mvn clean verify -T $(($(nproc) * 2)) -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))
```

### 4. Output Analysis Strategy

#### Reading Test Results After Execution

**CRITICAL**: After running Maven tests, ALWAYS check test results in this order:

1. **First: Check console output** for summary statistics (tests run, failures, errors, skipped)

2. **If failures occurred: Read XML reports directly**
   ```bash
   # List all files with failures
   grep -l "failures=\"[1-9]" target/surefire-reports/TEST-*.xml

   # Then READ the specific XML files for failed tests
   # Use the Read tool on: target/surefire-reports/TEST-ClassName.xml
   ```

3. **For detailed failure analysis**: Use the Read tool to read the full XML file:
   - Location: `target/surefire-reports/TEST-<ClassName>.xml`
   - Format: XML with full stack traces, error messages, and test timings
   - Contains: `<testcase>` elements with `<failure>` or `<error>` subelements

4. **Alternative: Read plain text reports** (less detailed but more readable):
   - Location: `target/surefire-reports/<ClassName>.txt`
   - Format: Plain text summaries

**Best practice**: Use `grep` to identify which test classes failed, then use the Read tool to read the corresponding `TEST-*.xml` files directly.

#### Quick Scan Commands

Find all failures:
```bash
grep -l "failures=\"[1-9]" target/surefire-reports/TEST-*.xml
```

View specific failed test details:
```bash
grep -A 20 "testcase.*FAILED" target/surefire-reports/TEST-ClassName.xml
```

#### Understanding Parallel Test Failures
Common patterns when tests fail in parallel but not sequentially:
- **Shared state**: Tests modifying static variables or singletons
- **Resource contention**: Database connections, file locks, ports
- **Timing dependencies**: Tests assuming execution order
- **Test pollution**: One test leaving state that affects others

### 5. Debugging Workflow

When you encounter test failures:

1. **Identify the failure pattern**
   ```bash
   mvn -T $(nproc) test -Dparallel=classes -DthreadCount=$(($(nproc) * 4))
   ```
   Review XML output in `target/surefire-reports/`

2. **Run failed tests with verbose output**
   ```bash
   mvn test -Dtest=FailedTest1,FailedTest2 -DtrimStackTrace=false
   ```

3. **If multiple related failures, group analysis**
   - Look for common stack traces
   - Check recently modified files
   - Review files that the failed tests interact with
   - Consider transitive effects (new behavior triggering old bugs)

4. **Single test deep dive**
   ```bash
   mvn test -Dtest=SpecificTest#specificMethod -DtrimStackTrace=false -X
   ```
   The `-X` flag enables debug output from Maven itself

5. **Create regression test from debug code**
   If you write a temporary test program to verify assumptions:
   - Consider adding it to the test suite as a regression test
   - Label it clearly: `@Category(RegressionTest.class)` or similar
   - Add comments explaining what bug it prevents.(Recall '!!' starts line comment and '!!!' starts block comments in foolish.)

### 6. Advanced Patterns

#### Skip Tests During Build
```bash
mvn clean compile -T $(($(nproc) * 2)) -DskipTests
```

#### Run Only Integration Tests
```bash
mvn verify -DskipUnitTests -Dparallel=classes -DthreadCount=$(($(nproc) * 4))
```

#### Specific Test Categories
```bash
mvn test -Dgroups=com.example.FastTests -Dparallel=classes -DthreadCount=$(($(nproc) * 4))
```

#### Memory Configuration for Large Projects
```bash
export MAVEN_OPTS="-Xmx$(free -g | awk '/^Mem:/{print int($2 / 2)}')g -XX:+UseG1GC"
mvn clean verify -T $(($(nproc) * 2)) -Dparallel=classes -DthreadCount=$(($(nproc) * 4))
```

### 7. Scala-Specific Considerations

For mixed Java/Scala projects:

#### Ensure Scala compilation
```bash
mvn scala:compile -T $(($(nproc) * 2))
```

#### Full clean build with Scala
```bash
mvn clean scala:compile compile -T $(($(nproc) * 2))
```

#### If using scala-maven-plugin
Check that `<configuration>` includes parallel compilation:
```xml
<recompileMode>incremental</recompileMode>
```

### 8. Common Issues and Solutions

#### Issue: Compilation errors blocking progress
**CRITICAL DEBUGGING PRINCIPLE**: When you have compilation errors, ALWAYS skip tests. Tests cannot run if code doesn't compile.

**Solution**: Focus exclusively on making code compile first:
```bash
# Step 1: Skip tests, focus on compilation
mvn clean compile -T $(($(nproc) * 2)) -DskipTests

# Step 2: Fix compilation errors iteratively
mvn compile -T $(nproc) -DskipTests

# Step 3: Only after compilation succeeds, run tests
mvn test -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))
```

**Why this matters**:
- Faster iteration: Compilation is faster without test compilation/execution
- Clear focus: One problem at a time (compilation, then tests)
- Better error messages: Maven shows compilation errors clearly without test noise
- Resource efficiency: Don't waste CPU on tests that can't run anyway

**Common scenario**:
```bash
# ❌ WRONG: Trying to build and test broken code
mvn clean test -T $(($(nproc) * 2))
# Result: Compilation errors + can't run tests = confusing output

# ✅ CORRECT: Fix compilation first
mvn clean compile -T $(($(nproc) * 2)) -DskipTests
# Result: Clear compilation errors, fix them one by one
# Then once compilation works:
mvn test -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))
```

#### Issue: Parallel builds fail inconsistently
**Solution**: Check for:
- Plugin version conflicts
- Non-thread-safe plugins
- Missing dependency declarations (works sequentially due to luck)

**Debug**: Run sequentially first
```bash
mvn clean compile test
```
Then try parallel:
```bash
mvn clean compile -T $(($(nproc) * 2)) test -Dparallel=classes -DthreadCount=$(($(nproc) * 4))
```

#### Issue: ANTLR4 generation seems incomplete
**Solution**:
1. Clean generated sources
   ```bash
   mvn clean
   ```
2. Generate with parallelism
   ```bash
   mvn generate-sources -T $(($(nproc) * 2))
   ```
3. Verify output in `target/generated-sources/antlr4/`

#### Issue: Test output is too verbose to read
**Solution**: Use XML filtering
```bash
# Find failures
grep -l "failures=\"[1-9]" target/surefire-reports/*.xml

# Extract failure details
for f in $(grep -l "failures=\"[1-9]" target/surefire-reports/*.xml); do
  echo "=== $f ==="
  grep -A 10 "failure message" "$f"
done
```

#### Issue: Need to debug one specific test without noise
**Solution**: Targeted sequential run with maximum verbosity
```bash
mvn test -Dtest=MyTest#specificMethod \
  -DtrimStackTrace=false \
  -Dsurefire.printSummary=true \
  -X 2>&1 | tee test-debug.log
```

### 9. Decision Tree for Build Selection

```
Code Change Type:
├── Compilation errors / syntax issues
│   └── mvn clean compile -T $(($(nproc) * 2)) -DskipTests (focus on fixing compilation first)
│
├── ANTLR4 grammar (.g4 files)
│   └── mvn clean generate-sources -T $(($(nproc) * 2)) && mvn compile -T $(($(nproc) * 2)) -DskipTests
│       (then after compilation verified: mvn test -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4)))
│
├── Major refactoring / dependency changes
│   └── mvn clean compile -T $(($(nproc) * 2)) test -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))
│
├── Normal code changes (Java/Scala)
│   └── mvn compile -T $(nproc) test -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))
│
├── Only tests changed
│   └── mvn test -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))
│
└── Debugging specific test failure
    ├── First: mvn test -Dtest=TestClass -DtrimStackTrace=false
    └── Then: mvn test -Dtest=TestClass#method -DtrimStackTrace=false -X
```

### 10. Best Practices

1. **Skip tests when fixing compilation**: ALWAYS use `-DskipTests` when debugging compilation errors - tests can't run if code doesn't compile
2. **Always start with parallel**: Default to `-T $(nproc)` or `-T $(($(nproc) * 2))` unless debugging (dynamically calculated)
3. **Parallelize tests at both levels**: Use `-Dparallel=classesAndMethods` for maximum throughput
4. **Use XML output**: Easier to parse and analyze than console output
5. **Incremental debugging**: Start broad (all tests) → narrow (specific test)
6. **Preserve debug tests**: Convert debugging code into regression tests
7. **Monitor resource usage**: If builds/tests are slow, check CPU/memory with `htop`
8. **Clean when uncertain**: `mvn clean` is cheap insurance against stale builds
9. **Group related failures**: Fix multiple related issues together, they often share root causes
10. **Parallelize approval tests**: Refactor loop-based approval tests to @ParameterizedTest for 3-4x speedup

### 11. Quick Reference Commands

```bash
# Clean parallel build (skip tests for compilation debugging)
mvn clean compile -T $(($(nproc) * 2)) -DskipTests

# Clean build + parallel tests
mvn clean test -T $(($(nproc) * 2)) -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))

# Re-generate sources (ANTLR4, etc.) - skip tests until compilation verified
mvn clean generate-sources -T $(($(nproc) * 2))
mvn compile -T $(($(nproc) * 2)) -DskipTests

# Run specific test verbosely
mvn test -Dtest=MyTest -DtrimStackTrace=false

# Run only failed tests from last run
mvn surefire:test

# Full clean with verify (integration tests)
mvn clean verify -T $(($(nproc) * 2)) -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))

# Parallel build, skip tests (for compilation debugging)
mvn clean compile -T $(($(nproc) * 2)) -DskipTests

# Single test with debug output to file
mvn test -Dtest=MyTest#method -DtrimStackTrace=false -X > debug.log 2>&1

# Run approval tests in parallel
mvn test -Dtest=ApprovalTests -Dparallel=classesAndMethods -DthreadCount=$(($(nproc) * 4))

# Debug single approval test case
mvn test -Dtest="ApprovalTests#*testCase001*" -DtrimStackTrace=false
```

## Integration with Claude Code

When using this skill:

1. **Assess the situation**: Understand what changed (code, tests, grammar files)
2. **Choose appropriate mode**: Use decision tree above
3. **Execute and analyze**: Run command, scan output/XML files
4. **Iterate if needed**: Narrow focus if failures occur
5. **Consider regression tests**: Preserve debugging insights as tests

## Output File Locations

- **Compiled classes**: `target/classes/` (Java/Scala)
- **Test classes**: `target/test-classes/`
- **Generated sources**: `target/generated-sources/`
- **Test reports**: `target/surefire-reports/` (XML + TXT)
- **Integration test reports**: `target/failsafe-reports/`

## Notes

- The `-T` flag specifies threads: `-T $(nproc)` = 1 per core, `-T $(($(nproc) * 2))` = 2 per core, dynamically calculated
- All commands use inline shell arithmetic `$((...))` to calculate thread counts based on available cores
- The `threadCount` for tests is independent of Maven's `-T` setting and also dynamically calculated
- Memory allocation uses `$(free -g | awk '/^Mem:/{print int($2 / 2)}')g` for 50% of total RAM (rounded down)
- XML test reports include full stack traces even when console output is trimmed
- Failed tests generate both `.xml` and `.txt` reports for easy analysis
