---
name: production-check
description: Use when verifying code is production-ready. Runs build, lint, and test commands to check compilation, code quality, and test suite. Essential validation step for /build and /audit commands.
---

# Production Check Skill

**Purpose:** Verify code is production-ready by running build, lint, and test commands
**Trigger:** After code changes, before deployment or sign-off
**Input:** Working directory, package manager (pnpm)
**Output:** `{ passed: boolean, build_result, lint_result, test_result, failures[] }`

---

## Workflow

**1. Verify working directory and package manager**

- Confirm cwd is monorepo root
- Verify pnpm is available (`pnpm --version`)
- If package manager not found: return error

**2. Run pnpm build**

- Execute: `pnpm build` (or `pnpm build --filter=...` if scoped)
- Capture stdout/stderr
- Status: ✓ pass or ✗ fail
- If turbo available: runs in parallel (turbo handles dependencies)

**3. Run pnpm lint**

- Execute: `pnpm lint`
- Capture stdout/stderr
- Status: ✓ pass or ✗ fail
- Non-blocking if only warnings

**4. Run pnpm test**

- Execute: `pnpm test` (or `pnpm test --run` for CI mode)
- Capture stdout/stderr
- Status: ✓ pass or ✗ fail
- Can fail tests but collect results

**5. Aggregate results**

- Collect all failures into array
- Return final status (passed = all 3 commands succeeded)
- Provide diagnostic output for fixing

---

## Output Format

**Success Case:**

```json
{
  "passed": true,
  "build_result": {
    "status": "pass",
    "duration": "12s"
  },
  "lint_result": {
    "status": "pass",
    "warnings": 0
  },
  "test_result": {
    "status": "pass",
    "tests": "42 passed"
  },
  "failures": []
}
```

**Failure Case:**

```json
{
  "passed": false,
  "build_result": {
    "status": "fail",
    "error": "TypeScript compilation failed",
    "stderr": "src/types.ts:45: error TS2322: Type 'string' not assignable to type 'number'"
  },
  "lint_result": {
    "status": "pass"
  },
  "test_result": {
    "status": "fail",
    "error": "2 tests failed",
    "stderr": "FAIL  src/__tests__/auth.spec.ts"
  },
  "failures": [
    "Build failed: TypeScript compilation",
    "Tests failed: 2 tests in src/__tests__/auth.spec.ts"
  ]
}
```

---

## Error Handling

| Scenario           | Action                                             |
| ------------------ | -------------------------------------------------- |
| pnpm not found     | Return error, ask user to install pnpm             |
| Wrong working dir  | Return error, ask user to run from monorepo root   |
| Build fails        | Stop, return build error details for fixing        |
| Lint warnings only | Continue (non-blocking), log warnings              |
| Tests fail         | Continue (collect results), return test error list |
| Unknown error      | Capture stderr, return for debugging               |

---

## Key Rules

- **Root execution:** Always run from monorepo root (`pwd` must show root)
- **Turbo optimization:** If turbo.json exists, pnpm build uses turbo (automatic)
- **Parallel execution:** Build runs in parallel (turbo handles), lint and test sequential
- **Capture output:** All stdout/stderr captured for diagnostics
- **No modifications:** Read-only execution, no file changes

---

## Integration

**Called by:**

- `/build` command (validation phase)
- `/audit` command (quality validation)
- `validation-phase` skill (before reporting)

**Calls:** pnpm scripts (no subagents)

**Next step:** Report results to calling agent for decision

---

## Example

**Input:**

```
cwd: "/home/user/monorepo"
package_manager: "pnpm"
```

**Execution:**

```
$ cd /home/user/monorepo
$ pnpm build
→ ✓ Build succeeded (12s)

$ pnpm lint
→ ✓ Lint passed

$ pnpm test --run
→ ✓ 42 tests passed
```

**Output:**

```json
{
  "passed": true,
  "build_result": { "status": "pass", "duration": "12s" },
  "lint_result": { "status": "pass", "warnings": 0 },
  "test_result": { "status": "pass", "tests": "42 passed" },
  "failures": []
}
```

---

## Configuration

| Setting   | Value            | Rationale                   |
| --------- | ---------------- | --------------------------- |
| User      | root             | Monorepo root required      |
| Timeout   | 5 minutes max    | Allow large test suites     |
| Fail-fast | No (collect all) | Show all issues in one pass |
| Format    | JSON output      | Machine-readable for agents |
