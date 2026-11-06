---
name: game-debug
description: Debug a web game with a living protocol of error signatures, causes, and verified fixes.
---

# Game Debug Skill

## When to use

- A game fails to build or test.
- A game crashes or has runtime errors.
- Assets, scenes, animations, or config values seem inconsistent.
- You need end-to-end verification that a game is playable.

## When NOT to use

- A single obvious typo in one file.
- Non-game code or pure environment/setup errors (missing Node.js, wrong package manager).
- Cases where the user explicitly wants a manual, one-off fix.
- First-time failures that are clearly caused by missing dependencies or bad configuration.

## Core idea

Maintain a **living debugging protocol**: a collection of `(signature, cause, fix)` entries plus generalized rules. Before running the game, validate known high-frequency inconsistency classes. When failures occur, match them against the protocol, apply known fixes, generate new fixes for novel errors, and record verified fixes back into the protocol.

## Protocol schema

The protocol is a JSON (or equivalent) data store. It can be per-project or shared across projects. Required top-level shape:

```json
{
  "version": 1,
  "entries": [
    {
      "id": "entry-TS2307-a1b2c3",
      "kind": "reactive",
      "signature": {
        "stage": "build",
        "errorCode": "TS2307",
        "messagePattern": "Cannot find module '(.+)' or its corresponding type declarations\\.",
        "fileContext": "src/**/*.ts"
      },
      "rootCause": "Import path uses the wrong relative depth after a file was moved.",
      "tags": ["import", "path"],
      "fix": {
        "type": "edit",
        "description": "Correct the relative import path.",
        "patch": "../../utils/physics|||../utils/physics"
      },
      "occurrences": 3,
      "contributingProjects": ["path/to/proj1", "path/to/proj2"]
    }
  ],
  "rules": []
}
```

Field meanings:

- `signature.stage`: `build`, `test`, or `runtime`.
- `signature.errorCode`: the normalized error code or class (e.g., `TS2307`, `TypeError`, `TextureNotFound`).
- `signature.messagePattern`: a regex with capture groups for variable parts.
- `signature.fileContext`: optional glob/path context used to narrow matches.
- `fix.type`: `edit`, `config`, `create`, `delete`, or `shell`.
- `fix.patch`: machine-applicable payload; for `edit` use `search|||replace`.
- `kind`: `reactive` (used after failure) or `proactive` (used before execution as a validation).

Default signature-match confidence threshold: **0.8**.

## Pre-execution validations

Split by cost. Run cheap checks first.

### Cheap static checks

These need only file reads and simple regex:

1. **Asset key consistency** — every texture/audio key referenced in code must exist in the asset pack or manifest.
2. **Config field consistency** — every `gameConfig.xxx` or `config.xxx` access must match a defined field in the config file.
3. **Scene/stage registration consistency** — every scene/stage transition target must be registered in the main entry file or router.
4. **Animation key consistency** — every animation key played in code must be defined in the animation manifest.
5. **Level order check** — the first entry in the level order should not be a template default like `Level1Scene`.

### Compile-dependent checks

Run these only when build/typecheck data is available or after a failed build:

6. **Type-only imports** — interface/type imports should use the `type` keyword.
7. **Override visibility** — override methods must not narrow base-class visibility.

## Debug loop

Run a verify–diagnose–repair cycle until the project builds and runs, up to a configurable maximum number of iterations (default **10**):

1. Load the current protocol.
2. Run cheap static validations and report violations.
3. REPEAT:
   - Run the build command (e.g., `npm run build`). Parse errors.
   - If failure: diagnose → repair → re-run the same stage to verify → record outcome.
   - Run the test command (e.g., `npm run test`). Parse errors.
   - If failure: diagnose → repair → re-run → record outcome.
4. UNTIL both build and test pass or the iteration limit is reached.
5. If the limit is reached, stop. Report remaining errors, save the trace, and escalate to the user. Do not loop forever.
6. If build and test pass, optionally run a dev-server probe:
   - Start the dev server.
   - Fetch the root URL and assert a successful response.
   - Capture any console/runtime errors.
   - Stop the server.
7. Save the debug trace and evolve the protocol.

If a test introduces a new error, treat it as the next failure in the same loop; do not roll back the previous build fix.

## Error parsing

Parse raw build/test/dev output into structured errors:

- TypeScript compiler errors with file, line, column, code, and message.
- Runtime errors such as `ReferenceError`, `TypeError`, `RangeError`, and `SyntaxError`.
- Engine-specific errors such as missing texture, missing animation, and missing scene/stage.
- Deduplicate errors by `code:file:line:message`.

## Error diagnosis

For each failure:

1. **Signature matching** — compare the parsed error against known entries:
   - Match error code / class (weight 0.5).
   - Match the normalized message regex (weight 0.35).
   - Match file context glob/path (weight 0.15).
   - Accept a match only if the weighted confidence is at least **0.8**.
2. **LLM fallback** — if no signature matches, ask an LLM to produce a candidate `(signature, rootCause, fix)` entry.
3. If still undiagnosed, attempt a direct LLM repair from the error and surrounding file content.

## Repair modes

Apply fixes in this order:

1. **Known fix** from a matched protocol entry.
2. **LLM-generated fix** from a candidate entry.
3. **Direct repair** from an LLM given the error and file content.

Supported fix types:

- `edit` — search/replace in a source file (`search|||replace`).
- `config` — update a JSON config file.
- `create` — create a new file with given content (`path::content`).
- `delete` — remove a file.
- `shell` — log the command but do not auto-execute it for safety.

Only record a fix to the protocol if a subsequent build/test shows fewer errors or passes.

## Protocol evolution

After each debug session:

1. Save the full trace (iterations, matched entries, new entries, validation results).
2. Group reactive entries by `errorCode`.
3. When an error code has occurred at least a configurable number of times (default **3**) and no rule exists yet, generalize the group into a reusable validation rule.
4. Rules can be generated by an LLM or by aggregating common tags and file contexts into regex-based `ValidationCheck` entries.
5. New rules are added to the protocol and run proactively in future sessions.

## Seed protocol

Initialize the protocol with hand-curated entries for common failures:

- Build errors: incorrect import paths, missing property declarations.
- Runtime errors: object accessed before initialization, infinite recursion.
- Engine-specific errors: missing texture key, missing animation key, missing scene/stage registration.

## Worked example

A build produces:

```
src/scenes/Level1.ts(10,23): error TS2307: Cannot find module '../../utils/physics' or its corresponding type declarations.
```

The diagnoser matches entry `entry-TS2307-a1b2c3` with confidence 0.95. The repairer applies the known `edit` patch `../../utils/physics|||../utils/physics`. The build is re-run and passes, so the entry's `occurrences` is incremented. After the same `TS2307` pattern is verified three times, the generalizer creates a proactive rule that flags likely wrong-depth imports before the next build.

## Best practices

- Always re-run the failing stage after a repair to verify the fix before recording it.
- Prefer minimal, targeted edits over broad refactors.
- Keep shell commands out of automatic execution; require human confirmation.
- Periodically review generalized rules to prevent false positives.
- Separate cheap static checks from compile-dependent checks to avoid misleading "pre-build" gates.
