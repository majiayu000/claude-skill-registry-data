---
name: tooling-audit
description: "Trigger: tooling audit, test tooling gaps. Detect build/test/coverage/mutation tooling for refactor safety plans."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.0.3"
  status: testing
---

# Tooling Audit
Read-only detection skill for hardening and refactor planning at high or critical risk. Use it to identify existing test infrastructure, missing safety tooling, installation tasks, verification commands, and compatibility checks.

## Shared contract

Load the tooling-compatibility-matrix skill. The matrix owns offline version/tool baselines.

## Files to inspect

Prefer direct reads/globs for these files only when they are in or above the resolved target scope:

- `pom.xml`, `build.gradle`, `build.gradle.kts`, `gradle/wrapper/gradle-wrapper.properties`
- `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `tsconfig.json`, `vite.config.*`, `jest.config.*`, `vitest.config.*`
- `pyproject.toml`, `requirements*.txt`, `setup.cfg`, `tox.ini`, `pytest.ini`, `poetry.lock`
- `.java-version`, `.sdkmanrc`, `.tool-versions`, Maven compiler properties, Gradle Java toolchain declarations

## Detection rules

- Record language version with evidence when available.
- Record build tool with evidence.
- Detect present `test_framework`, `assertion_lib`, `coverage`, and `mutation` tooling.
- Emit max 5 gaps, prioritized by safety impact.
- For each gap, create an install task using the compatibility matrix and include exact verify command.
- Include compatibility checks such as Java/PIT requirements or Node/Python floors.
- If version evidence is missing, mark the version as `hypothesis` and require verification.

## Compact output

```yaml
tooling_audit:
  language: ""            # include version and evidence file:line
  build_tool: ""
  present:
    test_framework: {}
    assertion_lib: {}
    coverage: {}
    mutation: {}
  gaps: []                # max 5
  install_tasks:
    - tool: ""
      matrix_ref: ""
      build_file: "file:line insertion point"
      snippet: ""
      verify_command: ""
      verify_latest_at_execution: true
  compatibility_checks:
    - "PIT >=1.15 requires Java 11+; detected Java 17: OK"
```
