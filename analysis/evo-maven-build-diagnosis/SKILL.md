---
name: evo-maven-build-diagnosis
description: Executes Maven builds, captures output, and parses error logs to identify root causes of build failures. Handles compilation errors, dependency resolution failures, POM configuration issues, and JDK version incompatibilities.
---

# evo-maven-build-diagnosis

Diagnoses Java Maven build failures by analyzing error logs and .travis.yml configuration.

## Key Functions

- `execute_maven_build(project_dir, goals, java_home, timeout_secs, pom_file)` - Run Maven build via subprocess
- `parse_compilation_errors(maven_log)` - Extract compilation errors with file/line/col/message
- `parse_dependency_errors(maven_log)` - Extract missing dependency artifacts
- `parse_plugin_errors(maven_log)` - Extract plugin execution failures
- `parse_pom_errors(maven_log)` - Extract POM-related errors (missing files, invalid XML)
- `parse_version_incompatibilities(maven_log)` - Extract source/target version issues
- `detect_java_version_from_pom(pom_path)` - Read Java version from pom.xml
- `classify_build_failure(maven_log)` - Classify the primary failure type
- `analyze_travis_yml(travis_yml_path)` - Check .travis.yml for issues like wrong file references
- `write_diagnosis_report(report_path, analysis_results, log_analysis, travis_analysis)` - Write failed_reasons.txt

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-maven-build-diagnosis/scripts')
from utils import (
    execute_maven_build, classify_build_failure, analyze_travis_yml,
    write_diagnosis_report, parse_compilation_errors, parse_pom_errors
)

# Analyze build logs
with open('build.log') as f:
    log = f.read()
analysis = classify_build_failure(log)

# Check .travis.yml
travis = analyze_travis_yml('.travis.yml')

# Write report
write_diagnosis_report('failed_reasons.txt', analysis, log_analysis=analysis, travis_analysis=travis)
```

## Common Error Patterns

1. **POM Configuration**: Missing/wrong POM file references (e.g., `build.pom.xml` vs `build-pom.xml`)
2. **Version Incompatibility**: Source/target version no longer supported by JDK
3. **Dependency Resolution**: Missing artifacts, tools.jar not found in JDK 9+
4. **Compilation**: Cannot find symbol, missing imports, missing method implementations
5. **Plugin Execution**: Failed plugin goals
