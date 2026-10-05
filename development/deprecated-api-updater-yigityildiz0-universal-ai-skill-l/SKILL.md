---
name: deprecated-api-updater
description: Detect and automatically update deprecated API calls across codebases with migration mappings, automated rewriting, and validation. Use when upgrading.
---

# Deprecated API Updater

Systematic detection and migration of deprecated API calls across codebases. This skill covers deprecation detection techniques, migration mapping strategies, automated rewriting approaches, framework-specific update guides, and validation procedures to ensure that updated code behaves identically to the original.

## When to Use This Skill

Use this skill for:

- Upgrading a framework or library to a new major version with breaking changes
- Resolving deprecation warnings before they become errors in a future release
- Migrating from one library to a replacement library (e.g., moment.js to date-fns, requests to httpx)
- Updating code after a language version upgrade (Python 2 to 3, Java 8 to 17, Node.js LTS upgrades)
- Cleaning up technical debt caused by accumulated deprecation warnings
- Preparing for removal of deprecated features announced in release notes
- Auditing a codebase for end-of-life (EOL) dependency usage

**Trigger phrases**: "deprecated", "deprecation warning", "update API", "migrate API", "upgrade library", "breaking changes", "deprecated method", "EOL", "version upgrade", "migration guide", "update deprecated calls"

## What This Skill Does

This skill provides an end-to-end deprecation migration workflow:

- **Deprecation Detection**: Identifies deprecated API usage through compiler warnings, static analysis, annotation scanning, and changelog analysis
- **Migration Mapping**: Creates mappings from deprecated APIs to their replacements, including parameter transformation rules
- **Automated Rewriting**: Applies migration mappings to rewrite code automatically where the transformation is mechanical
- **Framework-Specific Guides**: Provides migration patterns for common framework upgrades (React, Spring, Django, Express, etc.)
- **Validation**: Verifies that updated code produces the same behavior as the original through test execution and output comparison
- **Risk Assessment**: Evaluates the risk of each migration and recommends the order of operations

## Instructions

### Step 1: Detect Deprecated API Usage

Identify all deprecated API calls in the codebase using multiple detection methods.

#### Detection Methods

| Method | What It Finds | Tooling |
|--------|-------------|---------|
| **Compiler/Interpreter warnings** | Deprecated annotations, decorator warnings | Language compiler with warnings enabled |
| **Static analysis** | Deprecated method calls, import paths | SonarQube, Semgrep, custom rules |
| **Dependency scanning** | EOL libraries, vulnerable versions | Dependabot, Renovate, pip-audit, npm audit |
| **Changelog analysis** | Breaking changes in upcoming versions | Release notes, migration guides |
| **Runtime warnings** | Deprecation warnings emitted at runtime | Log aggregation, test suite output |

#### Python Example: Detecting Deprecated Usage

```python
# Run with: python -W all your_script.py
# Or configure in code:
import warnings
warnings.simplefilter("always", DeprecationWarning)

# Common deprecated patterns in Python:

# 1. DEPRECATED: collections.MutableMapping (Python 3.9+)
from collections import MutableMapping  # DeprecationWarning
# REPLACEMENT:
from collections.abc import MutableMapping

# 2. DEPRECATED: datetime.utcnow() (Python 3.12+)
from datetime import datetime
now = datetime.utcnow()  # DeprecationWarning: use timezone-aware alternative
# REPLACEMENT:
from datetime import datetime, timezone
now = datetime.now(timezone.utc)

# 3. DEPRECATED: pkg_resources (in favor of importlib)
import pkg_resources  # DeprecationWarning in newer setuptools
version = pkg_resources.get_distribution("mypackage").version
# REPLACEMENT:
from importlib.metadata import version
ver = version("mypackage")

# 4. DEPRECATED: asyncio.get_event_loop() without running loop (Python 3.10+)
import asyncio
loop = asyncio.get_event_loop()  # DeprecationWarning
# REPLACEMENT:
loop = asyncio.new_event_loop()
# Or better: use asyncio.run() as the entry point

# 5. DEPRECATED: typing.Optional, typing.List, typing.Dict (Python 3.9+)
from typing import Optional, List, Dict
def process(items: List[str], config: Optional[Dict[str, int]] = None): ...
# REPLACEMENT: use built-in generics
def process(items: list[str], config: dict[str, int] | None = None): ...
```

#### JavaScript Example: Detecting Deprecated Node.js and React APIs

```javascript
// Node.js deprecated APIs

// 1. DEPRECATED: url.parse() (use URL constructor)
const url = require("url");
const parsed = url.parse("https://example.com/path?q=1");  // DEP0169
// REPLACEMENT:
const parsed = new URL("https://example.com/path?q=1");

// 2. DEPRECATED: Buffer(size) constructor (security risk)
const buf = new Buffer(10);  // DEP0005
// REPLACEMENT:
const buf = Buffer.alloc(10);     // zero-filled
const buf2 = Buffer.from([1, 2]); // from data

// 3. DEPRECATED: fs.exists() (use fs.access or fs.stat)
const fs = require("fs");
fs.exists("/path", (exists) => { ... });  // DEP0103
// REPLACEMENT:
const fsPromises = require("fs").promises;
try {
    await fsPromises.access("/path");
    // file exists
} catch {
    // file does not exist
}

// React deprecated APIs

// 4. DEPRECATED: componentWillMount (React 16.3+)
class MyComponent extends React.Component {
    componentWillMount() { /* ... */ }  // UNSAFE, renamed
}
// REPLACEMENT:
class MyComponent extends React.Component {
    // Move logic to constructor or componentDidMount
    componentDidMount() { /* ... */ }
}
// Or better: convert to functional component with hooks
function MyComponent() {
    useEffect(() => { /* ... */ }, []);
}

// 5. DEPRECATED: ReactDOM.render (React 18+)
import ReactDOM from "react-dom";
ReactDOM.render(<App />, document.getElementById("root"));
// REPLACEMENT:
import { createRoot } from "react-dom/client";
const root = createRoot(document.getElementById("root"));
root.render(<App />);
```

#### Java Example: Detecting Deprecated APIs

```java
// Compile with: javac -Xlint:deprecation *.java

// 1. DEPRECATED: Date/Calendar API (Java 8+)
import java.util.Date;
import java.util.Calendar;
Date now = new Date();
Calendar cal = Calendar.getInstance();
int year = cal.get(Calendar.YEAR);
// REPLACEMENT:
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.Instant;
LocalDateTime now = LocalDateTime.now();
int year = LocalDate.now().getYear();
Instant instant = Instant.now();

// 2. DEPRECATED: Thread.stop(), Thread.suspend(), Thread.resume()
thread.stop();  // @Deprecated(since="1.2", forRemoval=true)
// REPLACEMENT: use interrupt() and cooperative cancellation
thread.interrupt();
// In the thread's run method:
if (Thread.currentThread().isInterrupted()) {
    return; // Clean exit
}

// 3. DEPRECATED: javax.* namespace (Jakarta EE 9+)
import javax.servlet.http.HttpServletRequest;
import javax.persistence.Entity;
// REPLACEMENT:
import jakarta.servlet.http.HttpServletRequest;
import jakarta.persistence.Entity;

// 4. DEPRECATED: finalize() method (Java 9+)
@Override
protected void finalize() throws Throwable { /* cleanup */ }
// REPLACEMENT: use try-with-resources or Cleaner
public class MyResource implements AutoCloseable {
    @Override
    public void close() { /* cleanup */ }
}

// 5. DEPRECATED: SecurityManager (Java 17+, removal in future)
System.setSecurityManager(new SecurityManager());
// REPLACEMENT: use module system and other security mechanisms
```

### Step 2: Create Migration Mappings

For each deprecated API, define the mapping to its replacement.

#### Migration Mapping Structure

```python
@dataclass
class MigrationMapping:
    deprecated_pattern: str          # Regex or AST pattern for the deprecated call
    replacement_template: str        # Template for the replacement code
    parameter_transform: dict        # How parameters map from old to new
    requires_import_change: bool     # Whether import statements need updating
    old_import: str                  # Import to remove
    new_import: str                  # Import to add
    notes: str                       # Special considerations
    risk_level: str                  # low, medium, high
    automated: bool                  # Whether this can be automated safely


# Example migration mappings
PYTHON_MIGRATIONS = [
    MigrationMapping(
        deprecated_pattern=r"datetime\.utcnow\(\)",
        replacement_template="datetime.now(timezone.utc)",
        parameter_transform={},
        requires_import_change=True,
        old_import="from datetime import datetime",
        new_import="from datetime import datetime, timezone",
        notes="Returns timezone-aware datetime instead of naive UTC",
        risk_level="medium",
        automated=True,
    ),
    MigrationMapping(
        deprecated_pattern=r"from collections import (.*?)(MutableMapping|MutableSequence|MutableSet)",
        replacement_template=r"from collections.abc import \2",
        parameter_transform={},
        requires_import_change=True,
        old_import="from collections import MutableMapping",
        new_import="from collections.abc import MutableMapping",
        notes="Abstract base classes moved to collections.abc",
        risk_level="low",
        automated=True,
    ),
]
```

#### Framework-Specific Migration Tables

**React 17 to React 18 Migration**:

| Deprecated API | Replacement | Automated | Risk |
|---------------|-------------|-----------|------|
| `ReactDOM.render()` | `createRoot().render()` | Yes | Medium |
| `ReactDOM.hydrate()` | `hydrateRoot()` | Yes | Medium |
| `ReactDOM.unmountComponentAtNode()` | `root.unmount()` | Partial | Medium |
| `componentWillMount` | `useEffect` or `componentDidMount` | Partial | High |
| `componentWillReceiveProps` | `getDerivedStateFromProps` or `useEffect` | No | High |
| `componentWillUpdate` | `getSnapshotBeforeUpdate` | No | High |
| String refs | `createRef()` or `useRef()` | Partial | Medium |

**Spring Boot 2.x to 3.x Migration**:

| Deprecated API | Replacement | Automated | Risk |
|---------------|-------------|-----------|------|
| `javax.*` imports | `jakarta.*` imports | Yes | Low |
| `WebSecurityConfigurerAdapter` | Component-based security config | No | High |
| `spring.factories` auto-config | `AutoConfiguration.imports` | Partial | Medium |
| `@ConstructorBinding` on type | `@ConstructorBinding` on constructor | Yes | Low |
| Spring MVC `antMatchers()` | `requestMatchers()` | Yes | Low |

**Django 3.x to 4.x Migration**:

| Deprecated API | Replacement | Automated | Risk |
|---------------|-------------|-----------|------|
| `url()` in urlpatterns | `re_path()` or `path()` | Yes | Low |
| `default_app_config` | Remove, use `AppConfig.default_auto_field` | Yes | Low |
| `NullBooleanField` | `BooleanField(null=True)` | Yes | Low |
| `django.conf.urls.url` | `django.urls.re_path` | Yes | Low |
| `JSONField` from `django.contrib.postgres` | `django.db.models.JSONField` | Yes | Low |

### Step 3: Apply Automated Rewrites

For migrations marked as "automated", apply the transformation systematically.

#### Python Example: Automated Migration Script

```python
import re
import ast
from pathlib import Path
from typing import List, Tuple


class DeprecationMigrator:
    def __init__(self, migrations: List[MigrationMapping]):
        self.migrations = migrations
        self.changes_log: List[dict] = []

    def migrate_file(self, filepath: Path) -> Tuple[str, int]:
        """Migrate a single file. Returns (new_content, change_count)."""
        content = filepath.read_text()
        original = content
        change_count = 0

        for migration in self.migrations:
            if not migration.automated:
                continue

            # Count matches before replacement
            matches = re.findall(migration.deprecated_pattern, content)
            if matches:
                # Apply replacement
                content = re.sub(
                    migration.deprecated_pattern,
                    migration.replacement_template,
                    content
                )

                # Update imports if needed
                if migration.requires_import_change:
                    content = self._update_imports(
                        content,
                        migration.old_import,
                        migration.new_import
                    )

                change_count += len(matches)
                self.changes_log.append({
                    "file": str(filepath),
                    "pattern": migration.deprecated_pattern,
                    "matches": len(matches),
                    "risk": migration.risk_level,
                })

        return content, change_count

    def _update_imports(self, content: str, old_import: str, new_import: str) -> str:
        """Update import statements."""
        if old_import in content and new_import not in content:
            content = content.replace(old_import, new_import)
        return content

    def migrate_directory(self, directory: Path, dry_run: bool = True) -> dict:
        """Migrate all Python files in a directory."""
        total_changes = 0
        files_changed = 0

        for filepath in directory.rglob("*.py"):
            new_content, change_count = self.migrate_file(filepath)
            if change_count > 0:
                files_changed += 1
                total_changes += change_count
                if not dry_run:
                    filepath.write_text(new_content)
                print(f"{'[DRY RUN] ' if dry_run else ''}Updated {filepath}: "
                      f"{change_count} changes")

        return {
            "files_scanned": len(list(directory.rglob("*.py"))),
            "files_changed": files_changed,
            "total_changes": total_changes,
            "dry_run": dry_run,
        }
```

#### JavaScript Example: Automated Codemod with jscodeshift

```javascript
// codemod: migrate-react-18.js
// Run with: npx jscodeshift -t migrate-react-18.js src/

module.exports = function transformer(fileInfo, api) {
    const j = api.jscodeshift;
    const root = j(fileInfo.source);
    let hasChanges = false;

    // Migration 1: ReactDOM.render() -> createRoot().render()
    root.find(j.CallExpression, {
        callee: {
            object: { name: "ReactDOM" },
            property: { name: "render" },
        },
    }).forEach(path => {
        const [element, container] = path.node.arguments;

        // Replace with createRoot pattern
        const createRootCall = j.callExpression(
            j.memberExpression(
                j.callExpression(j.identifier("createRoot"), [container]),
                j.identifier("render")
            ),
            [element]
        );
        j(path).replaceWith(createRootCall);
        hasChanges = true;
    });

    // Migration 2: Update import statement
    if (hasChanges) {
        // Remove old import
        root.find(j.ImportDeclaration, {
            source: { value: "react-dom" },
        }).forEach(path => {
            j(path).remove();
        });

        // Add new import
        const newImport = j.importDeclaration(
            [j.importSpecifier(j.identifier("createRoot"))],
            j.literal("react-dom/client")
        );
        root.find(j.Program).get("body", 0).insertBefore(newImport);
    }

    return hasChanges ? root.toSource() : fileInfo.source;
};
```

#### Java Example: Automated javax to jakarta Migration

```java
import java.io.IOException;
import java.nio.file.*;
import java.util.*;

public class JakartaMigrator {

    private static final Map<String, String> PACKAGE_MAPPINGS = Map.of(
        "javax.servlet", "jakarta.servlet",
        "javax.persistence", "jakarta.persistence",
        "javax.validation", "jakarta.validation",
        "javax.annotation", "jakarta.annotation",
        "javax.inject", "jakarta.inject",
        "javax.transaction", "jakarta.transaction",
        "javax.ws.rs", "jakarta.ws.rs",
        "javax.json", "jakarta.json",
        "javax.websocket", "jakarta.websocket",
        "javax.mail", "jakarta.mail"
    );

    public record MigrationResult(
        int filesScanned,
        int filesModified,
        int totalReplacements,
        List<String> modifiedFiles
    ) {}

    public MigrationResult migrate(Path sourceDir, boolean dryRun) throws IOException {
        List<String> modifiedFiles = new ArrayList<>();
        int totalReplacements = 0;
        int filesScanned = 0;

        try (var stream = Files.walk(sourceDir)) {
            List<Path> javaFiles = stream
                .filter(p -> p.toString().endsWith(".java"))
                .toList();

            filesScanned = javaFiles.size();

            for (Path file : javaFiles) {
                String content = Files.readString(file);
                String updated = content;
                int replacements = 0;

                for (var entry : PACKAGE_MAPPINGS.entrySet()) {
                    String oldPkg = entry.getKey();
                    String newPkg = entry.getValue();

                    if (updated.contains(oldPkg)) {
                        int count = countOccurrences(updated, oldPkg);
                        updated = updated.replace(oldPkg, newPkg);
                        replacements += count;
                    }
                }

                if (replacements > 0) {
                    totalReplacements += replacements;
                    modifiedFiles.add(file.toString());
                    if (!dryRun) {
                        Files.writeString(file, updated);
                    }
                    System.out.printf("%s%s: %d replacements%n",
                        dryRun ? "[DRY RUN] " : "", file, replacements);
                }
            }
        }

        return new MigrationResult(filesScanned, modifiedFiles.size(),
            totalReplacements, modifiedFiles);
    }

    private int countOccurrences(String text, String pattern) {
        int count = 0;
        int idx = 0;
        while ((idx = text.indexOf(pattern, idx)) != -1) {
            count++;
            idx += pattern.length();
        }
        return count;
    }
}
```

### Step 4: Handle Non-Automatable Migrations

Some deprecations require manual analysis because the replacement involves structural changes or behavioral differences.

#### Manual Migration Process

1. **Document the change**: write a brief description of what changed and why
2. **Identify all call sites**: find every place the deprecated API is used
3. **Understand the behavioral difference**: the replacement may have subtly different behavior (e.g., different default values, different error handling, different thread safety)
4. **Migrate one call site at a time**: change one usage, run tests, commit, then move to the next
5. **Add tests for behavioral differences**: if the replacement behaves differently in edge cases, add tests that verify the new behavior is acceptable

#### Example: Manual Migration (Spring Security)

```java
// BEFORE: WebSecurityConfigurerAdapter (deprecated in Spring Security 5.7)
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
            .antMatchers("/api/public/**").permitAll()
            .antMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated()
            .and()
            .httpBasic();
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userDetailsService)
            .passwordEncoder(passwordEncoder());
    }
}

// AFTER: Component-based configuration (cannot be automated due to structural change)
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .httpBasic(Customizer.withDefaults());
        return http.build();
    }

    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public UserDetailsService userDetailsService() {
        // Configure user details service
        return new CustomUserDetailsService();
    }
}
```

### Step 5: Validate the Migration

After applying migrations, verify correctness through multiple validation layers.

#### Validation Checklist

1. **Compilation/Parsing**: the code compiles without deprecation warnings for migrated APIs
2. **Unit tests pass**: all existing unit tests pass without modification
3. **Integration tests pass**: all integration tests pass
4. **No new deprecation warnings**: the migration did not introduce new deprecation warnings
5. **Behavioral equivalence**: for high-risk migrations, verify output matches the pre-migration version
6. **Performance comparison**: for performance-sensitive APIs, benchmark before and after

### Step 6: Generate the Migration Report

```
## Deprecated API Migration Report

### Summary
- **Codebase**: {project name}
- **Migration scope**: {what was upgraded -- library name and versions}
- **Files scanned**: {count}
- **Files modified**: {count}
- **Total API calls migrated**: {count}
- **Automated migrations**: {count} ({percentage})
- **Manual migrations**: {count} ({percentage})
- **Remaining deprecations**: {count}

### Migrations Applied
| # | Deprecated API | Replacement | Occurrences | Method | Risk |
|---|---------------|-------------|-------------|--------|------|
| 1 | {old API} | {new API} | {count} | Auto | Low |
| 2 | {old API} | {new API} | {count} | Manual | High |

### Validation Results
| Check | Status | Details |
|-------|--------|---------|
| Compilation | PASS/FAIL | {warnings/errors remaining} |
| Unit tests | PASS/FAIL | {count} passed, {count} failed |
| Integration tests | PASS/FAIL | {count} passed, {count} failed |
| Deprecation warnings | PASS/FAIL | {count} remaining |

### Remaining Items
{List of deprecations that could not be migrated automatically and require manual attention}

### Risks and Notes
{Special considerations, behavioral differences, or follow-up actions}
```

## Best Practices

- **Always run migrations in dry-run mode first**: preview changes before applying them to understand scope and identify potential issues
- **Migrate in focused batches**: group migrations by library or framework and migrate one group per commit; this makes review and rollback manageable
- **Update tests alongside production code**: if the test code also uses deprecated APIs, update it in the same commit to keep tests consistent
- **Check migration guides from library maintainers**: official migration guides cover edge cases and behavioral changes that automated tools miss; always read them before starting
- **Preserve git blame**: use separate commits for mechanical migrations (import renames) and behavioral changes so that `git blame` remains informative
- **Run the full test suite after each batch**: do not accumulate multiple migration batches before testing; verify each batch independently
- **Monitor deprecation warnings in CI/CD**: configure CI to fail on new deprecation warnings so that deprecated API usage does not accumulate
- **Schedule regular deprecation cleanup**: quarterly or before major releases, audit and resolve accumulated deprecation warnings

## Common Pitfalls

- **Assuming deprecated APIs are drop-in replaceable**: the replacement API may have different default values, different exception behavior, different nullability contracts, or different thread safety guarantees; always read the documentation
- **Migrating deprecated APIs in code you do not own**: third-party libraries may use deprecated APIs internally; do not modify vendor code; instead, upgrade the library to a version that has already migrated
- **Applying regex-based replacements without understanding context**: a simple find-and-replace of `javax` to `jakarta` may modify string literals, comments, or non-Java files incorrectly; use AST-based tools when possible
- **Ignoring transitive dependencies**: your code may not directly use a deprecated API, but a dependency might; dependency scanning tools help identify this
- **Not testing with the target runtime version**: running tests with the old runtime version does not verify that the migration works on the new version; test with both during the transition period
- **Batch-migrating high-risk items**: high-risk migrations (behavioral changes, structural rewrites) should be done one at a time with full verification; do not combine them with low-risk mechanical migrations
- **Forgetting to update documentation and configuration**: after migrating code, update README files, configuration examples, deployment scripts, and developer setup guides that reference deprecated APIs
- **Not communicating the migration to the team**: other developers may be working on code that uses the deprecated API; coordinate migrations to avoid merge conflicts and duplicated effort
