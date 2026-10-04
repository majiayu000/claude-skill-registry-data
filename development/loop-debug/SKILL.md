---
name: loop-debug
description: Autonomous iterative Test-Diagnose-Fix-Retest loop
---
# Loop Debug & Empirical Verification Protocol

You are operating under the **Loop Debug** protocol. After completing any code, script, or system task, you MUST immediately enter a closed **Debug & Empirical Verification Loop** before delivering the final response to the user.

---

## 1. Core Execution Rules

1. **Pre-Delivery Code & Function Completeness Check (`code-completeness-debugger` Handshake)**:
   - Verify that zero functions are missing/undefined, zero code blocks are truncated or left as `TODO` stubs, and all cross-file imports/exports are properly wired.
   - If any function or code snippet is missing, write it completely before running the test.

2. **Automatic Entry into the Runtime Debug Loop**:
   - Immediately execute the program, build, syntax/AST check, or live state verification via `run_command`.
   - **Iteration**:
     - If any error, missing symbol, exception, syntax issue, or unexpected output occurs: diagnose the exact root cause -> apply a surgical fix -> re-run the test.
     - Repeat (`Test -> Diagnose -> Fix -> Retest`) until the exit code is `0` and all functions and features work 100% as requested.

3. **Strict Ban on Premature Claims or User Delegation**:
   - Never ask the user to test, debug, or complete missing code for you.
   - Never claim a task is done before terminal output empirically proves it.
   - Note: Read-only (`research`) sub-agents perform static code/function completeness verification only, without attempting `run_command`.

4. **Mandatory `Debug` Completion Confirmation**:
   - Once the project passes 100% of completeness and live tests with zero errors, explicitly confirm in the final response that `Debug` was completed (keeping `Debug` isolated on its own line surrounded by `\n\n` per `bilingual-clean-layout`):

```markdown
تم إنجاز المشروع وعمل:

`Debug`

بنجاح والتأكد من عمله بنسبة 100%:

[filename](file:///path/to/file)
```
