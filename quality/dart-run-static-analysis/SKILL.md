---
name: dart-run-static-analysis
description: Execute `dart analyze` to identify warnings and errors, and use `dart fix --apply` to automatically resolve mechanical lint issues. Use during development to ensure code quality and before committing changes.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Fri, 24 Apr 2026 15:09:34 GMT
---

## Contents
- [Analysis Configuration](#analysis-configuration)
- [Diagnostic Suppression](#diagnostic-suppression)
- [Workflow: Executing Static Analysis](#workflow-executing-static-analysis)
- [Workflow: Applying Automated Fixes](#workflow-applying-automated-fixes)
- [Examples](#examples)

## Analysis Configuration
Configure the Dart analyzer using `analysis_options.yaml` at the package root.

- **Base Configuration:** Include a standard rule set (e.g., `package:lints/recommended.yaml` or `package:flutter_lints/flutter.yaml`).
- **Strict Type Checks:** Enable `strict-casts: true`, `strict-inference: true`, and `strict-raw-types: true`.
- **Linter Rules:** Enable or disable specific rules under `linter: rules:`.
- **Formatter Configuration:** Set `page_width` and `trailing_commas` under `formatter:`.
- **Analyzer Plugins:** Add plugins under `analyzer: plugins:`.

## Diagnostic Suppression
- **File-level Exclusion:** Use `analyzer: exclude:` with glob patterns (e.g., `**/*.g.dart`).
- **File-level Suppression:** `// ignore_for_file: <diagnostic_code>`.
- **Line-level Suppression:** `// ignore: <diagnostic_code>`.
- **Pubspec Suppression:** `# ignore: <diagnostic_code>`.

## Workflow: Executing Static Analysis
- [ ] 1. Verify `analysis_options.yaml` exists at the project root.
- [ ] 2. Run `dart analyze <target_directory>`.
- [ ] 3. Review the diagnostic output.
- [ ] 4. If info-level issues must be failures, use `--fatal-infos` flag.
- [ ] 5. Resolve reported errors or proceed to Automated Fixes workflow.

## Workflow: Applying Automated Fixes
- [ ] 1. Preview changes: `dart fix --dry-run`.
- [ ] 2. Review the proposed fixes.
- [ ] 3. Verify corresponding linter rules are enabled.
- [ ] 4. Apply fixes: `dart fix --apply`.
- [ ] 5. Format code: `dart format .`.
- [ ] 6. Re-run static analysis to verify all diagnostics are resolved.

### Example: Comprehensive `analysis_options.yaml`
```yaml
include: package:flutter_lints/recommended.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "lib/generated/**"
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    todo: ignore
    invalid_assignment: warning
    missing_return: error

linter:
  rules:
    avoid_shadowing_type_parameters: false
    await_only_futures: true
    use_super_parameters: true

formatter:
  page_width: 100
  trailing_commas: preserve
```

### Example: Inline Diagnostic Suppression
```dart
// ignore_for_file: unused_local_variable, dead_code

void processData() {
  // ignore: invalid_assignment
  int x = ''; 
  
  const y = 10; // ignore: constant_identifier_names
}
```
