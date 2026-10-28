---
name: configure-deno-commands
description: >-
  Configure and maintain Deno development commands (check, test, dev, prod). Use
  when the user wants to set up or update the standard command interface in
  deno.json and scripts/ directory.
---

# Configure Deno Commands

This skill ensures a standardized development interface using Deno tasks and scripts.

## Context

This skill can be invoked:
- **Standalone**: When a user wants to fix or update their Deno commands.
- **From init**: During project initialization to set up the standard interface.

## Standard Interface

The project must support these commands in `deno.json`:

- `deno task check`: Comprehensive verification (build, lint, fmt, static analysis, tests).
- `deno task test`: Run all tests or a specific test if a path is provided.
- `deno task dev`: Run in development mode with watch mode.
- `deno task prod`: Run in production mode.

## Rules & Constraints

1. **Idempotency**: Check existing `scripts/` and `deno.json` tasks before creating. Do not overwrite existing scripts unless user confirms.
2. **Scripts Location**: All complex logic must reside in `.ts` files within the `scripts/` directory.
3. **Task Definitions**: `deno.json` should point to these scripts.
4. **Standard Interface Compliance**: The `check.ts` script must implement the full verification checklist.
5. **Exit Codes**: Scripts must return non-zero exit codes on failure to break CI/CD and agent workflows.
6. **No External Dependencies**: Generated scripts must only use Deno built-in APIs and `@std/` stdlib. No cliffy, no npm packages.
7. **Parallel Execution**: Independent checks (fmt, lint, test, type-check) MUST run in parallel, not sequentially.
8. **Sequential Prerequisites**: If the project has build/codegen steps whose output is needed by subsequent checks, those steps MUST complete before parallel checks start.
9. **Buffered Output**: Each parallel command's stdout/stderr MUST be buffered (piped, not inherited) to prevent interleaving.
10. **Real-Time Progress**: Print a status line when each command starts and when it finishes (pass/fail).
11. **Output Ordering**: After all checks complete, print buffered output of passed checks first, then ALL failed checks at the end — for easy debugging.
12. **No Output Loss**: ALL stdout and stderr from every check MUST be printed regardless of success/failure. Print buffered output with `console.log` or `await Deno.stdout.write(...)` — an unawaited `Deno.stdout.write` followed by `Deno.exit(1)` can exit before the bytes are flushed, and the failing check's output is exactly the part that is lost (2026-09-06: a generated `check.ts` did this and failed the no-output-loss item).
13. **Subprocess Spawn Safety (fork-loop prevention)**: Any `.ts` file under `scripts/` that calls `Deno.Command`, `Deno.run`, or otherwise spawns a subprocess at module top level MUST wrap the spawn in `if (import.meta.main) { … }`. Reason: `deno test -A scripts/` walks the directory and **imports every file** to discover `Deno.test(…)` calls. Importing a file with an unguarded top-level `Deno.Command("deno", ["test", "-A", …])` immediately spawns another `deno test`, which imports the same file again — recursive fork-bomb that exhausts the host within seconds. This pattern crashed the dev host on 2026-05-09 (multiple WindowServer kernel panics).
14. **Prefer inline `deno.json` tasks over wrapper scripts**: If a task is a single command (`deno test -A`, `deno run --watch -A src/main.ts`), declare it directly in `deno.json` `"tasks"`. Generate a `scripts/<name>.ts` file ONLY for orchestration that needs Deno-script logic (e.g. parallel runs, conditional sequencing, output buffering). `scripts/check.ts` qualifies; `scripts/test.ts` and `scripts/dev.ts` do not — they should be inline tasks. When the user explicitly asks for a `scripts/test.ts` wrapper, apply rule 13 AND require an explicit path argument (do NOT call `deno test -A` without a path from inside `scripts/` — that triggers the recursion above).

## Workflow

1. **Analyze**: Check existing `deno.json` and `scripts/`.
2. **Scaffold Scripts**: Create `scripts/check.ts` if missing. The script must satisfy all Rules & Constraints above (parallel execution, buffered output, failed-last ordering, no external deps).
3. **Configure Tasks**: Update `deno.json` tasks to reference the scripts.
4. **Verify**: Run `deno task check` to ensure everything works.

## Examples

### deno.json tasks (preferred — inline tasks for single-command operations)
```json
{
  "tasks": {
    "check": "deno run -A scripts/check.ts",
    "test": "deno test -A",
    "dev": "deno run --watch -A src/main.ts",
    "prod": "deno run -A src/main.ts"
  }
}
```

### scripts/test.ts (only when user explicitly asks for a wrapper)
```ts
#!/usr/bin/env -S deno run -A
// Guard against re-entry: `deno test -A scripts/` would otherwise import
// this file, execute the spawn at top level, and cause a recursive
// fork-bomb (rule 13 in SKILL.md).
if (import.meta.main) {
  const path = Deno.args[0];
  if (!path) {
    console.error("usage: scripts/test.ts <path>  (passing no path triggers recursion)");
    Deno.exit(2);
  }
  const { code } = await new Deno.Command("deno", {
    args: ["test", "-A", path],
  }).spawn().status;
  Deno.exit(code);
}
```

## Verification

- [ ] `scripts/check.ts` exists and is executable.
- [ ] `deno.json` contains all standard tasks.
- [ ] `deno task check` passes cleanly.
