---
name: openrewrite
description: OpenRewrite recipe development and test maintenance. Use when writing OpenRewrite recipes, fixing test failures, or working with import ordering in recipe tests.
---

# OpenRewrite Recipe Development

This skill provides guidelines for developing OpenRewrite recipes and maintaining their tests, with a focus on import ordering issues.

## Fixing Import Ordering Test Failures

🔧 OpenRewrite recipe tests often fail due to import order differences, not actual transformation issues.

### Problem

OpenRewrite recipe tests fail with diffs showing only import order differences:

```diff
-import java.util.List;
-import org.assertj.core.api.Assertions;
+import org.assertj.core.api.Assertions;
+import java.util.List;
```

### Root Cause

OpenRewrite manages imports automatically based on:

- Existing imports in the file
- JavaTemplate configuration
- Import optimization rules
- The order may differ from test expectations

### Solution Approach

#### 1. Fix the Recipe (if imports are missing)

Ensure your JavaTemplate is properly configured:

```java
JavaTemplate template = JavaTemplate
    .builder("Your.template.code()")
    .imports(
        "org.assertj.core.api.Assertions",
        "org.eclipse.collections.impl.utility.Iterate"
    )
    .contextSensitive()  // Important for proper context handling
    .javaParser(JavaParser.fromJavaVersion()
        .classpath("assertj-core", "eclipse-collections", "eclipse-collections-api")
    )
    .build();
```

Don't forget to call:

```java
maybeAddImport("org.assertj.core.api.Assertions");
maybeAddImport("org.eclipse.collections.impl.utility.Iterate");
maybeRemoveImport("old.package.OldClass");
```

#### 2. Fix the Test Expectations

Accept the actual import order that OpenRewrite produces:

❌ Instead of forcing a specific order:

```java
// DON'T expect a specific order you want
"import java.util.List;\n" +
"import org.assertj.core.api.Assertions;\n"
```

✅ Use the actual order OpenRewrite produces:

```java
// DO accept the order OpenRewrite generates
"import org.assertj.core.api.Assertions;\n" +
"import org.eclipse.collections.impl.utility.Iterate;\n" +
"\n" +
"import java.util.List;\n"
```

#### 3. Common Import Ordering Patterns

OpenRewrite typically orders imports as:

1. Third-party packages (org.assertj, org.eclipse.collections, etc.)
2. Blank line
3. Java standard library (`java.*`, `javax.*`)
4. Blank line (if static imports exist)
5. Static imports

### Quick Fix Steps

1. Run the failing test and copy the actual output from the error message
2. Replace the expected output in your test with the actual output
3. Verify the transformation logic is correct (ignore import order)
4. Re-run the test to confirm it passes

### Note on ~~> Syntax

The `~~>` prefix in test expectations is not standard in all codebases. It's used in some OpenRewrite projects to indicate "ignore everything before this line" but isn't recognized in all contexts. If you see it failing, remove it and use exact matching instead.

### Example Fix

```java
@Test
void replacesVerifyWithAssertJ() {
    rewriteRun(
        java(
            // Input
            """
            import org.eclipse.collections.impl.test.Verify;
            import java.util.List;

            class Test {
                void test() {
                    List<String> list = List.of("a", "b", "c");
                    Verify.assertCount(2, list, each -> each.length() > 0);
                }
            }
            """,
            // Expected output - use actual order from test failure
            """
            import org.assertj.core.api.Assertions;
            import org.eclipse.collections.impl.utility.Iterate;

            import java.util.List;

            class Test {
                void test() {
                    List<String> list = List.of("a", "b", "c");
                    Assertions.assertThat(Iterate.count(list, each -> each.length() > 0)).isEqualTo(2);
                }
            }
            """
        )
    );
}
```

## Maven POM Dependency Ordering

Maven POM files should follow a consistent dependency ordering structure. See the `pom-ordering` skill for detailed guidelines.
