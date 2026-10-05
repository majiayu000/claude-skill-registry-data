---
name: dead-code-eliminator
description: Find and safely remove dead code including unreachable functions, unused imports, obsolete features, and stale feature flags using static analysis and call.
---

# Dead Code Eliminator

Systematic detection and safe removal of dead code from codebases. This skill covers static analysis techniques, call graph construction, feature flag cleanup, and safe removal strategies that minimize the risk of accidentally removing code that is still needed through indirect references, reflection, or external integrations.

## When to Use This Skill

Use this skill for:

- Cleaning up a codebase before a major release or refactoring effort
- Removing code left behind after a feature deprecation or migration
- Eliminating unused imports, variables, functions, classes, and modules
- Cleaning up stale feature flags and their associated code paths
- Reducing bundle size, compilation time, or test execution time
- Improving code readability by removing distracting dead code
- Preparing a codebase for transfer to a new team or open-sourcing

**Trigger phrases**: "dead code", "unused code", "remove dead code", "unused imports", "unreachable code", "unused functions", "feature flag cleanup", "stale code", "code cleanup", "eliminate dead code", "unused variables", "orphan code"

## What This Skill Does

This skill provides a structured approach to dead code elimination:

- **Static Analysis**: Identifies unused imports, variables, functions, classes, and modules using language-specific analysis techniques
- **Call Graph Analysis**: Constructs function-level and module-level call graphs to identify unreachable code from known entry points
- **Feature Flag Cleanup**: Identifies stale feature flags and guides safe removal of both the flag checks and the dead code branches
- **Dynamic Analysis Guidance**: Recommends runtime instrumentation approaches for code where static analysis alone is insufficient
- **Safe Removal Strategies**: Provides step-by-step procedures for removing dead code while minimizing the risk of breaking hidden dependencies
- **Verification Procedures**: Defines testing and validation steps to confirm that removal is safe

## Instructions

### Step 1: Categorize Dead Code Types

Understand the different categories of dead code, each requiring a different detection approach.

| Category | Description | Detection Difficulty | Risk of False Positive |
|----------|-------------|---------------------|----------------------|
| **Unused Imports** | Imported modules, packages, or symbols never referenced | Easy | Low |
| **Unused Variables** | Declared variables never read | Easy | Low |
| **Unused Functions/Methods** | Defined but never called within the codebase | Medium | Medium (reflection, callbacks) |
| **Unused Classes** | Defined but never instantiated or referenced | Medium | Medium (dependency injection, serialization) |
| **Unreachable Code** | Code after unconditional return/throw/break, impossible conditions | Easy | Low |
| **Dead Conditional Branches** | Branches that can never execute due to constant conditions | Medium | Low |
| **Obsolete Feature Code** | Entire features that have been superseded or disabled | Hard | High (might be re-enabled) |
| **Stale Feature Flags** | Feature flags that have been permanently enabled or disabled | Medium | Medium (rollback scenarios) |
| **Unused Configuration** | Config entries, environment variables, or constants never read | Hard | High (external consumers) |
| **Orphaned Test Code** | Tests for functions or classes that no longer exist | Medium | Low |

### Step 2: Detect Dead Code Using Static Analysis

Apply language-specific static analysis to identify dead code candidates.

#### Python Example: Detecting Unused Code

```python
# DEAD CODE ANALYSIS RESULTS:
# 1. Unused import: 'json' (imported but never used)
# 2. Unused variable: 'temp_result' (assigned but never read)
# 3. Unused function: 'legacy_format_output' (defined but never called)
# 4. Unreachable code: lines after 'return' in 'process_data'
# 5. Dead conditional: 'if False:' block

import os
import json          # DEAD: unused import
import logging
from typing import List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

LEGACY_MODE = False  # Constant, never changed at runtime


@dataclass
class DataRecord:
    id: str
    value: float
    category: str


def process_data(records: List[DataRecord]) -> dict:
    """Process records and return summary."""
    if not records:
        return {"count": 0, "total": 0.0}

    total = sum(r.value for r in records)
    temp_result = total * 1.1  # DEAD: unused variable, never read

    result = {
        "count": len(records),
        "total": total,
        "average": total / len(records),
    }
    return result

    # DEAD: unreachable code after return
    logger.info("Processing complete")
    notify_downstream(result)


def legacy_format_output(data: dict) -> str:
    # DEAD: this function is never called anywhere in the codebase
    """Format output in legacy XML format."""
    parts = []
    for key, value in data.items():
        parts.append(f"<{key}>{value}</{key}>")
    return "<result>" + "".join(parts) + "</result>"


def format_output(data: dict) -> str:
    """Format output as JSON string."""
    return str(data)


def main():
    if LEGACY_MODE:
        # DEAD: conditional branch that never executes (LEGACY_MODE = False)
        logger.info("Running in legacy mode")
        records = load_legacy_records()
    else:
        records = load_records()

    result = process_data(records)
    output = format_output(result)
    print(output)
```

**Static analysis tools by language**:

| Language | Tool | Command | What It Detects |
|----------|------|---------|-----------------|
| Python | `vulture` | `vulture src/` | Unused functions, variables, imports, classes |
| Python | `autoflake` | `autoflake --check src/` | Unused imports and variables |
| Python | `pylint` | `pylint --disable=all --enable=W0611,W0612 src/` | Unused imports (W0611), unused variables (W0612) |
| JavaScript | ESLint `no-unused-vars` | `eslint --rule 'no-unused-vars: error' src/` | Unused variables, imports, functions |
| JavaScript | `ts-prune` | `ts-prune` | Unused exports in TypeScript |
| Java | IntelliJ / Eclipse | Built-in inspection | Unused declarations, unreachable code |
| Java | SpotBugs | `mvn spotbugs:check` | Dead local stores, unused fields |
| Java | PMD | `pmd check --rulesets category/java/bestpractices.xml` | Unused imports, variables, private methods |

#### JavaScript Example: Detecting Unused Exports and Functions

```javascript
// file: src/utils/formatting.js

// DEAD: exported but never imported anywhere
export function formatLegacyDate(date) {
    const d = new Date(date);
    return `${d.getMonth() + 1}/${d.getDate()}/${d.getFullYear()}`;
}

// ACTIVE: imported by 3 modules
export function formatISODate(date) {
    return new Date(date).toISOString().split("T")[0];
}

// DEAD: exported but never imported anywhere
export function formatCurrency(amount, currency = "USD") {
    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency,
    }).format(amount);
}

// DEAD: internal helper, only called by formatLegacyDate (which is also dead)
function padZero(num) {
    return num < 10 ? `0${num}` : String(num);
}

// ACTIVE: called by formatISODate
function validateDate(date) {
    const d = new Date(date);
    if (isNaN(d.getTime())) {
        throw new Error(`Invalid date: ${date}`);
    }
    return d;
}
```

#### Java Example: Detecting Unused Code with Call Graph

```java
// DEAD CODE ANALYSIS:
// 1. LegacyReportGenerator -- class never instantiated or referenced
// 2. UserService.getInactiveUsers() -- method never called
// 3. REPORT_VERSION constant -- never read
// 4. Unused import: java.util.LinkedList

import java.util.List;
import java.util.ArrayList;
import java.util.LinkedList;       // DEAD: unused import
import java.util.Map;
import java.util.stream.Collectors;

public class UserService {
    private static final String REPORT_VERSION = "2.1";  // DEAD: never read

    private final UserRepository userRepository;
    private final EmailService emailService;

    // ACTIVE: called from UserController.getUsers()
    public List<UserDTO> getActiveUsers() {
        return userRepository.findByStatus(Status.ACTIVE)
            .stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }

    // DEAD: never called from any reachable code path
    public List<UserDTO> getInactiveUsers() {
        return userRepository.findByStatus(Status.INACTIVE)
            .stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }

    // ACTIVE: called by getActiveUsers (and would be called by getInactiveUsers)
    private UserDTO toDTO(User user) {
        return new UserDTO(user.getId(), user.getName(), user.getEmail());
    }
}

// DEAD: entire class is never referenced anywhere in the codebase
public class LegacyReportGenerator {
    public String generateReport(List<UserDTO> users) {
        StringBuilder sb = new StringBuilder();
        sb.append("REPORT\n");
        sb.append("======\n");
        for (UserDTO user : users) {
            sb.append(user.getName()).append("\n");
        }
        return sb.toString();
    }
}
```

### Step 3: Build and Analyze Call Graphs

For non-trivial dead code detection, construct a call graph starting from known entry points.

#### Call Graph Construction Process

1. **Identify entry points**: main methods, HTTP endpoints, event handlers, scheduled tasks, CLI commands, test methods
2. **Build the forward call graph**: for each entry point, trace all functions/methods that are reachable through direct calls
3. **Identify unreachable nodes**: any function not reachable from any entry point is a candidate for removal
4. **Check for indirect references**: search for reflection, dynamic dispatch, dependency injection, serialization, and string-based method references that static analysis misses

#### Python Example: Simple Call Graph Builder

```python
import ast
import os
from collections import defaultdict
from typing import Dict, Set


class CallGraphBuilder(ast.NodeVisitor):
    """Build a simple call graph from Python source files."""

    def __init__(self):
        self.definitions: Dict[str, str] = {}  # func_name -> file
        self.calls: Dict[str, Set[str]] = defaultdict(set)  # caller -> callees
        self.current_function: str | None = None

    def visit_FunctionDef(self, node):
        old_function = self.current_function
        self.current_function = node.name
        self.definitions[node.name] = self._current_file
        self.generic_visit(node)
        self.current_function = old_function

    def visit_Call(self, node):
        if self.current_function and isinstance(node.func, ast.Name):
            self.calls[self.current_function].add(node.func.id)
        self.generic_visit(node)

    def analyze_file(self, filepath: str):
        self._current_file = filepath
        with open(filepath) as f:
            tree = ast.parse(f.read())
        self.visit(tree)

    def find_unreachable(self, entry_points: Set[str]) -> Set[str]:
        """Find functions not reachable from any entry point."""
        reachable = set()
        stack = list(entry_points)

        while stack:
            func = stack.pop()
            if func in reachable:
                continue
            reachable.add(func)
            for callee in self.calls.get(func, set()):
                if callee not in reachable:
                    stack.append(callee)

        all_defined = set(self.definitions.keys())
        return all_defined - reachable


# Usage
builder = CallGraphBuilder()
for root, dirs, files in os.walk("src"):
    for f in files:
        if f.endswith(".py"):
            builder.analyze_file(os.path.join(root, f))

entry_points = {"main", "handle_request", "process_event"}
unreachable = builder.find_unreachable(entry_points)
print(f"Potentially dead functions: {unreachable}")
```

### Step 4: Handle Special Cases

Static analysis and call graphs miss certain categories of "hidden" usage. Check each dead code candidate against these patterns before removal.

#### Hidden Usage Patterns

| Pattern | How It Hides Usage | Detection Strategy |
|---------|-------------------|-------------------|
| **Reflection** | `getattr(obj, method_name)`, `Class.forName()` | Search for reflection APIs; grep for function names as strings |
| **Dynamic Dispatch** | Plugin systems, strategy patterns via config | Check configuration files, plugin registries |
| **Dependency Injection** | Framework creates instances via config | Check DI container configs (Spring XML, Guice modules) |
| **Serialization** | Fields used only during JSON/XML serialization | Check `@JsonProperty`, `@XmlElement`, `Serializable` annotations |
| **External API** | Public library methods called by external consumers | Check if the code is a library with external dependents |
| **Database Mapping** | ORM fields mapped to DB columns but not accessed in code | Check ORM mappings (Hibernate, SQLAlchemy, Prisma) |
| **Template Engines** | Functions called from HTML/template files | Search template files for function references |
| **Scheduled Tasks** | Methods invoked by cron or task scheduler | Check scheduler configs, `@Scheduled` annotations |
| **Message Handlers** | Methods triggered by message queue consumers | Check message broker configs, `@EventListener` annotations |

#### Verification Grep Patterns

```bash
# Search for function name used as a string (reflection risk)
# Replace "myFunction" with the candidate dead function name
grep -r '"myFunction"' --include="*.py" --include="*.js" --include="*.java" src/
grep -r "'myFunction'" --include="*.py" src/

# Search in configuration files
grep -r "myFunction" --include="*.xml" --include="*.yaml" --include="*.json" .

# Search in template files
grep -r "myFunction" --include="*.html" --include="*.jinja2" --include="*.ejs" .

# Search in test files (dead code might be tested but unused in production)
grep -r "myFunction" --include="*.test.*" --include="*_test.*" --include="*Test.java" .
```

### Step 5: Clean Up Feature Flags

Feature flags that have been permanently enabled or disabled leave behind dead code paths that should be cleaned up.

#### Feature Flag Cleanup Process

1. **Inventory all feature flags**: list every flag, its current state, and when it was last changed
2. **Identify stale flags**: flags that have been in the same state (enabled or disabled) for longer than the team's flag lifecycle policy (typically 30-90 days after full rollout)
3. **Determine the live branch**: for each stale flag, identify which code path is active and which is dead
4. **Remove the dead branch**: delete the code in the inactive branch
5. **Remove the flag check**: replace the conditional with just the live branch code
6. **Remove the flag definition**: delete the flag from configuration, launch darkly, or wherever it is defined

#### JavaScript Example: Feature Flag Cleanup

```javascript
// BEFORE: Stale feature flag "new_checkout_flow" has been enabled for 6 months

import { isEnabled } from "./featureFlags";

async function processCheckout(cart) {
    if (isEnabled("new_checkout_flow")) {
        // This is the LIVE path (flag has been enabled for 6 months)
        const order = await createOrderV2(cart);
        await processPaymentV2(order);
        await sendConfirmationV2(order);
        return order;
    } else {
        // This is the DEAD path (flag is always enabled, this never executes)
        const order = await createOrder(cart);
        await processPayment(order);
        await sendConfirmation(order);
        return order;
    }
}

// AFTER: Flag removed, dead branch deleted

async function processCheckout(cart) {
    const order = await createOrderV2(cart);
    await processPaymentV2(order);
    await sendConfirmationV2(order);
    return order;
}

// ALSO REMOVE:
// - createOrder, processPayment, sendConfirmation (if only called from dead path)
// - "new_checkout_flow" from feature flag configuration
// - Any tests that specifically tested the old checkout flow
```

### Step 6: Safe Removal Strategy

Follow a systematic process to remove dead code safely.

#### Removal Procedure

1. **Mark, do not delete**: first, add deprecation annotations or comments to candidate dead code; deploy and monitor for a release cycle
2. **Add logging (optional)**: for uncertain cases, add a log statement inside the suspected dead code and monitor logs for a period; if the log never fires, the code is confirmed dead
3. **Remove in small batches**: delete dead code in focused commits (one logical group per commit) so that any regression can be easily traced and reverted
4. **Run the full test suite**: after each removal, run all tests (unit, integration, end-to-end) and verify nothing breaks
5. **Deploy to staging**: verify the removal in a staging environment before production
6. **Monitor after deployment**: watch error rates, logs, and metrics for 24-48 hours after deploying dead code removal to production

#### Python Example: Gradual Removal with Logging

```python
import logging
import warnings

logger = logging.getLogger(__name__)


# Step 1: Mark as deprecated (release N)
@deprecated("This function is believed to be dead code. "
            "If you see this warning, contact the platform team.")
def legacy_format_output(data: dict) -> str:
    # Step 2: Add monitoring
    logger.warning(
        "legacy_format_output was called -- this was believed to be dead code",
        extra={"caller": inspect.stack()[1]},
    )
    # Original implementation
    parts = []
    for key, value in data.items():
        parts.append(f"<{key}>{value}</{key}>")
    return "<result>" + "".join(parts) + "</result>"


# Step 3: After monitoring period confirms no calls, remove entirely (release N+1)
# Delete the function and all references
```

#### Java Example: Safe Removal with @Deprecated

```java
// Step 1: Mark as deprecated (release N)
/**
 * @deprecated This method is believed to be dead code as of 2024-01.
 *             If you encounter this deprecation warning, contact the
 *             platform team. Scheduled for removal in release 2024-Q2.
 */
@Deprecated(since = "2024-01", forRemoval = true)
public List<UserDTO> getInactiveUsers() {
    logger.warn("getInactiveUsers() was called -- believed to be dead code");
    return userRepository.findByStatus(Status.INACTIVE)
        .stream()
        .map(this::toDTO)
        .collect(Collectors.toList());
}

// Step 2: After monitoring confirms no calls, remove in next release
```

### Step 7: Generate the Dead Code Report

```
## Dead Code Analysis Report

### Summary
- **Files analyzed**: {count}
- **Dead code candidates found**: {count}
- **Estimated removable lines**: {count}
- **Estimated size reduction**: {percentage or KB}

### Findings by Category
| Category | Count | Lines | Confidence |
|----------|-------|-------|------------|
| Unused imports | {n} | {lines} | High |
| Unused variables | {n} | {lines} | High |
| Unused functions/methods | {n} | {lines} | Medium |
| Unused classes | {n} | {lines} | Medium |
| Unreachable code | {n} | {lines} | High |
| Stale feature flags | {n} | {lines} | Medium |
| Obsolete feature code | {n} | {lines} | Low-Medium |

### Detailed Findings
#### 1. {Dead Code Item}
- **Location**: {file}:{line range}
- **Type**: {category}
- **Confidence**: {high/medium/low}
- **Reason**: {why this is believed to be dead}
- **Hidden usage check**: {reflection: no, DI: no, serialization: no, ...}
- **Recommended action**: {remove / deprecate first / investigate}

### Removal Plan
- **Phase 1 (safe, immediate)**: {high-confidence items}
- **Phase 2 (deprecate and monitor)**: {medium-confidence items}
- **Phase 3 (investigate)**: {low-confidence items requiring further analysis}
```

## Best Practices

- **Start with high-confidence, low-risk removals**: unused imports and unreachable code after return statements are safe to remove immediately; build confidence before tackling uncertain cases
- **Use version control as your safety net**: always commit before removing dead code; if something breaks, you can revert the specific removal commit
- **Remove dead code before adding new features**: cleaning up dead code first reduces confusion and merge conflicts when new feature code is added
- **Do not comment out code instead of deleting it**: commented-out code is still dead code and adds visual noise; rely on version control history to recover deleted code if needed
- **Clean up related artifacts**: when removing a dead function, also remove its tests, documentation, configuration entries, and any supporting helper functions that become dead as a result
- **Automate detection in CI/CD**: configure linters and static analysis tools to flag unused imports and variables on every pull request to prevent new dead code from accumulating
- **Set a regular cleanup cadence**: schedule dead code analysis quarterly or after major feature launches to prevent gradual accumulation
- **Document removal decisions**: in the commit message, briefly explain why the code was determined to be dead and what analysis was performed

## Common Pitfalls

- **Removing code used via reflection or dynamic dispatch**: static analysis cannot detect usage through `getattr()`, `Class.forName()`, or plugin systems; always check for string-based references before removing
- **Removing public library APIs**: if the codebase is a library consumed by external projects, "unused" functions may have external callers that are invisible to your analysis; check download/usage metrics and maintain backward compatibility
- **Removing code referenced in configuration files**: functions referenced in Spring XML, Guice modules, routing tables, or scheduler configs appear unused in code but are invoked at runtime
- **Removing ORM-mapped fields**: database column mappings may appear unused in application code but are required for correct serialization and deserialization
- **Deleting "unused" event handlers or webhooks**: code that handles incoming webhooks, message queue events, or scheduled triggers may appear dead because the trigger is external
- **Confusing test-only code with dead code**: helper functions used exclusively in test files are not dead code; they are test utilities
- **Removing code too aggressively in a single commit**: large-scale removal makes it difficult to identify which specific deletion caused a regression; remove in small, focused batches
- **Not monitoring after removal**: even after thorough analysis, some dead code may have hidden callers that only manifest under specific conditions (monthly batch jobs, annual reports, error recovery paths); monitor for a full business cycle after removal
