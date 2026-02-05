---
name: audit-performance
description: Performance-focused audit that can run in background during implementation. Checks for inefficiencies, memory leaks, widget rebuilds. Injects P0 findings to main agent.
---

# Performance Audit Skill

Specialized audit focusing on performance concerns. Can run standalone or in background during /implement.

---

## When to Use

- **Background Mode**: Automatically during /implement (spawned by implement skill)
- **Standalone Mode**: `/audit-performance {files or feature}` for independent performance review
- When optimizing code for performance before release

---

## Agent Compatibility

- OUTPUT_DIR: `.claude/output` for Claude Code, `.codex/output` for Codex CLI
- Background mode uses Task tool with `run_in_background: true`
- Injection to main agent via findings file or direct message

---

## Check Categories

### P0 - Critical Performance (MUST FIX IMMEDIATELY)

| Check | Description | Example |
|-------|-------------|---------|
| Infinite Loops | Unbounded loops or recursion | `while(true)` without break |
| Memory Leaks | Undisposed controllers/streams | Missing `dispose()` calls |
| Main Thread Blocking | Expensive sync operations | Large JSON parse on UI thread |
| O(n²) on Large Data | Quadratic algorithms on lists | Nested loops on 1000+ items |
| Uncontrolled Growth | Unbounded list/map growth | Adding without cleanup |
| Blocking I/O | Sync file/network on main | `File.readAsStringSync()` |

### P1 - Important Performance (SHOULD FIX)

| Check | Description | Example |
|-------|-------------|---------|
| Unnecessary Rebuilds | Widgets rebuilding too often | Missing const, wrong keys |
| Missing Const | Non-const constructors | `Widget()` instead of `const Widget()` |
| Expensive build() | Heavy computation in build | Parsing/sorting in build() |
| Inefficient List Ops | Repeated list traversals | Multiple `.where()` calls |
| Missing Virtualization | Long lists without lazy loading | ListView without builder |
| Repeated Calculations | Same computation multiple times | No memoization |
| Large Image Loading | Unoptimized image loading | Full-res images in lists |
| Excessive Providers | Too many provider rebuilds | Over-granular state |

### P2 - Minor Performance (CONSIDER)

| Check | Description | Example |
|-------|-------------|---------|
| String Concatenation | Repeated + in loops | Use StringBuffer |
| Suboptimal Algorithm | Could be more efficient | O(n log n) possible |
| Missing Caching | Repeated network calls | No local cache |
| Verbose Code | Could be simplified | Unnecessary conversions |

---

## Flutter/Dart Specific Checks

### Widget Rebuild Issues

```dart
// P1: Missing const
return Container(  // ❌
  child: Text('Hello'),
);

return const Container(  // ✓
  child: Text('Hello'),
);

// P1: Widget method instead of class
Widget _buildHeader() {  // ❌ Causes parent rebuild
  return Text('Header');
}

class HeaderWidget extends StatelessWidget {  // ✓
  const HeaderWidget();
  @override
  Widget build(context) => const Text('Header');
}

// P1: Missing keys in lists
ListView.builder(
  itemBuilder: (ctx, i) => ItemWidget(items[i]),  // ❌ No key
);

ListView.builder(
  itemBuilder: (ctx, i) => ItemWidget(
    key: ValueKey(items[i].id),  // ✓
    items[i],
  ),
);
```

### Memory Management

```dart
// P0: Missing dispose
class MyController extends StateNotifier<MyState> {
  final StreamSubscription _sub;

  MyController() : super(MyState()) {
    _sub = stream.listen(onData);
  }

  // ❌ Missing dispose - memory leak!
}

// ✓ Correct disposal
@override
void dispose() {
  _sub.cancel();
  super.dispose();
}

// P0: Undisposed TextEditingController
final _controller = TextEditingController();  // ❌ In StatelessWidget
```

### Expensive Operations

```dart
// P0: Blocking main thread
void loadData() {
  final data = File(path).readAsStringSync();  // ❌ Sync I/O
  final json = jsonDecode(data);  // ❌ Large parse on main
}

// ✓ Async with isolate
Future<void> loadData() async {
  final data = await File(path).readAsString();
  final json = await compute(jsonDecode, data);
}

// P1: Expensive build
@override
Widget build(context) {
  final sorted = items.toList()..sort();  // ❌ Sort on every build
  return ListView(...);
}
```

---

## Execution Flow

### Background Mode (During /implement)

```
/implement invokes background audit:
    │
    ├── Task tool (background: true)
    │   └── Prompt: "Run /audit-performance on files: {list}"
    │
    ├── Audit scans each file
    │   ├── Check P0 items
    │   ├── Check P1 items
    │   └── Check P2 items
    │
    ├── Generate findings
    │   └── Write to: .claude/output/audit-{session}-performance.json
    │
    └── Injection Decision
        ├── If P0 found: Inject immediately to main agent
        │   └── Message: "PERFORMANCE P0: {finding}. Fix before continuing."
        │   └── Main agent MUST fix before next task
        │
        └── If only P1/P2: Collect for summary
            └── Report at end of implementation
```

### Standalone Mode

```
/audit-performance {target}
    │
    ├── Identify target files
    │   ├── Feature name → find related files
    │   ├── File paths → use directly
    │   └── "all" → scan entire codebase
    │
    ├── Run all performance checks
    │
    ├── Generate report
    │   └── .claude/output/audit-performance-{feature}.md
    │
    └── Display summary with P0/P1/P2 counts
```

---

## Output Format

### JSON Output (for background mode injection)

```json
{
  "audit_type": "performance",
  "timestamp": "2026-01-03T10:30:00Z",
  "files_scanned": ["file1.dart", "file2.dart"],
  "severity_summary": {
    "P0": 0,
    "P1": 4,
    "P2": 3
  },
  "inject_to_main": false,
  "estimated_impact": "medium",
  "findings": [
    {
      "severity": "P1",
      "category": "missing_const",
      "file": "lib/src/screens/home_screen.dart",
      "line": 45,
      "code": "return Container(",
      "message": "Widget could be const",
      "fix": "Add const keyword: return const Container("
    }
  ]
}
```

### Markdown Report (for standalone mode)

```markdown
# Performance Audit Report: {Feature}

## Summary

| Severity | Count | Impact |
|----------|-------|--------|
| P0 (Critical) | 0 | - |
| P1 (Important) | 4 | Medium |
| P2 (Minor) | 3 | Low |

**Overall**: PASS (no P0 issues)
**Estimated Impact**: Medium rebuild reduction

## Important Findings (P1)

### 1. Missing const constructors (3 occurrences)
- **Files**: home_screen.dart, profile_screen.dart
- **Impact**: Unnecessary widget rebuilds
- **Fix**: Add `const` keyword to widget constructors

### 2. Expensive operation in build()
- **File**: list_screen.dart:67
- **Code**: `items.toList()..sort()`
- **Impact**: Sorting on every rebuild
- **Fix**: Move sorting to controller/state

## Minor Findings (P2)
...

## Performance Recommendations
1. Add const to 15 widgets for ~20% fewer rebuilds
2. Move sorting to controller for ~50ms improvement
3. Consider virtualization for product list (100+ items)
```

---

## Injection Protocol

When running in background mode and P0 is found:

```
1. Write finding to audit file immediately
2. Send message to main agent:

   "⚡ PERFORMANCE P0 DETECTED

   File: {file}:{line}
   Issue: {category}
   Code: {code snippet}

   Impact: {description of performance impact}
   Fix Required: {fix description}

   ⚠️ You MUST fix this before continuing to the next task."

3. Main agent receives message and:
   a. Stops current task
   b. Fixes the performance issue
   c. Re-runs audit on fixed file
   d. Continues only when P0 count = 0
```

---

## Integration with RPI Workflow

### In /implement Phase 2.5

```markdown
After completing each task group (e.g., after T1-T3):

1. Get list of files created/modified
2. Spawn background performance audit:

   Task tool:
     subagent_type: "general-purpose"
     run_in_background: true
     prompt: "Run /audit-performance on: {file list}.
              Write findings to .claude/output/audit-{session}-performance.json.
              If P0 found, report immediately."

3. Continue with next task group
4. Before Phase 3 (Verification):
   - Wait for background audit completion
   - Check for any P0 findings
   - Fix all P0 before proceeding
```

---

## Prompt Template

When invoked, execute:

```
## Performance Audit: {target}

Analyzing for performance issues...

### Files to Audit
{list of files}

### P0 Checks (Critical)
□ Infinite loops
□ Memory leaks (undisposed resources)
□ Main thread blocking
□ O(n²) on large data
□ Uncontrolled growth
□ Blocking I/O

### P1 Checks (Important)
□ Unnecessary widget rebuilds
□ Missing const constructors
□ Expensive build() operations
□ Inefficient list operations
□ Missing virtualization
□ Repeated calculations
□ Large image loading
□ Excessive provider rebuilds

### Flutter-Specific Analysis

For each widget file:
- Check for const usage
- Check for proper keys in lists
- Check for widget methods vs classes
- Check for expensive operations in build()

For each controller/service:
- Check for proper disposal
- Check for stream subscription cleanup
- Check for async patterns

### Findings

[Analyze each file and report findings by severity]

### Summary

| Severity | Count |
|----------|-------|
| P0 | {n} |
| P1 | {n} |
| P2 | {n} |

**Status**: {PASS if P0=0, FAIL otherwise}
**Estimated Impact**: {low/medium/high}

{If P0 > 0: List required fixes}
{If background mode and P0 > 0: Inject to main agent}
```

---

## Quick Reference

```
# Standalone
/audit-performance                     # Audit current feature
/audit-performance lib/src/screens/    # Audit specific directory
/audit-performance home_screen.dart    # Audit specific file

# Background (invoked by /implement)
# Automatically runs during implementation
```
