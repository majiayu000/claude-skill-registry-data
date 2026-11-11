---
name: aspen-error-troubleshooting
description: Use this skill when an Aspen Plus simulation run returns errors or warnings (e.g. `run_simulation` reports failure, non-convergence, block status ≠ 0, or messages like "COLUMN DRIES UP", "COLUMN NOT IN MASS BALANCE", "AE_UNDERSPEC"). Covers the full diagnosis → fix → record workflow, including diagnostic paths, the privacy rules for what is recorded, and the `record_error` tool contract.
version: 1.0.0
---

# Aspen Error Troubleshooting

## When to use

Activate whenever an Aspen Plus run surfaces an error/warning — including non-convergence, block status != OK, severe error messages, or user reports of failed simulation. Do NOT activate for general Aspen setup questions.

## Diagnosis Workflow

Two locations hold error knowledge, and they are **not** the same place:

- `<ASPEN_DOCS_ROOT>` — the read-only docs shipped inside the installed `aspen-plus` MCP
  server. The server announces the absolute path in its MCP server instructions as a
  `ASPEN_DOCS_ROOT: <path>` line. Never guess a relative `aspen-mcp/docs/`.
- `<ASPEN_USER_DATA>` — this machine's own resolved-error log, at `~/.aspen-mcp/`
  (`%USERPROFILE%\.aspen-mcp\` on Windows). This is the only writable location; it
  survives plugin upgrades, which wipe the installed plugin directory.

Search for the error keyword in this order and **stop at the first match**:

1. Grep `<ASPEN_USER_DATA>/error-history.md` for the error keyword (uppercase). Skip if absent — it is created on first recorded fix.
2. Grep `<ASPEN_DOCS_ROOT>/error-history.md` for the error keyword (the curated log shipped with the server).
3. Grep across `<ASPEN_DOCS_ROOT>/` for the field or code the message names (the object docs hold no troubleshooting; known failure modes are in error-history.md, so this step finds the field's row, not a fix).
4. Apply general heuristics:
   - **Fix upstream before downstream** — upstream block errors cascade; always resolve the most upstream issue first.
   - Check feed T / P / composition.
   - Verify property method suits the system.
   - For columns: try `ALGORITHM=NEWTON` with `DAMPING=SEVERE`.
   - For recycle loops: provide initial estimates on tear streams; switch `TEAR_METHOD` to `BROYDEN` and raise `BR_MAXIT`.

## Diagnostic Paths

| Path | Purpose |
|------|---------|
| `\Data\Results Summary\Run-Status\Output\PER_ERROR` | Full simulation error text |
| `\Data\Blocks\{name}\Output\BLKSTAT` | 0 = OK, 1 = error |
| `\Data\Blocks\{name}\Output\BLKMSG` | Short block error summary |
| `\Data\Blocks\{name}\Output\PER_ERROR` | Full block error details |
| `\Data\Convergence\Convergence\{solver}\Output\ERR_TOL2` | Per-iteration convergence history (should trend to 0) |

## Fix & Re-run

Apply the chosen fix, then re-run `run_simulation`. If still failing, go back to step 1 with the new error keyword.

**Workbench mode** (the session's mode is `"workbench"`: its `[workbench]` lines, `workbench_read`'s
`"mode"`): the failed run belongs to a proposal, so the fix goes there. Revise **the same
proposal** (`workbench_edit(tab=<its tab id>, program=...)`, which makes rev 2), with the cause
and the fix in its reason, in process words and the user's language. The user approves and
runs it. Do not change the model with MCP calls and re-run it yourself. The exception is a
fix no block can make (a gap step: see aspen-process-workflow). Do that one right away, then
revise the proposal to run again. The diagnosis above (search order, paths) is the same in
both modes.

## Local Recording — `record_error`

After a confirmed fix, call `record_error`. It appends a generalized entry to
`<ASPEN_USER_DATA>/error-history.md` — that is `~/.aspen-mcp/error-history.md`
(`%USERPROFILE%\.aspen-mcp\error-history.md` on Windows) — creating the file if needed, and
sends nothing anywhere. No need to ask the user first, since nothing leaves the machine, but
every field must still be generalized (below) and written in **English**.

Entries use the shipped file's format: `## <ERROR KEYWORD>`, then `### <Block or object> — <cause>` with Cause and Fix lines. When Aspen printed no message, the keyword is the tool's own reply text (`REQUIRED INPUTS ARE INCOMPLETE`, `BLOCKS WITH NO RESULT`, `ERROR WRITING`, `INTERNAL FAULT`).

Never write into `<ASPEN_DOCS_ROOT>`: it lives inside the installed plugin/package and is
replaced wholesale on upgrade, so anything recorded there is silently lost.

**Strip before writing:**
- File paths (anything containing `C:\`, `/home/`, `~/`)
- Real component names → replace with `{component}`
- Real block names in Aspen paths → replace with `{name}`
- Specific numeric fix values (keep Aspen enum values like `NEWTON`, `SEVERE`)
- Simulation file names
- Any personally identifiable information

### What to keep and what to generalize

| Keep (generic knowledge) | Strip / Generalize |
|---|---|
| Error keyword (uppercase) | Component names → omit |
| Block type (RadFrac, Heater, …) | Specific numeric values → omit |
| Property method (NRTL, PENG-ROB) | Block/Stream names → omit |
| Aspen path pattern (`Data.Blocks.{name}.Input.X`) | File paths / session names → omit |
| Cause **type** (e.g. "spec exceeds physical limit") | Process config details → omit |
| Fix **direction** (keep Aspen enums like NEWTON, SEVERE) | Actual fix values → omit |
| What was tried and failed (generalized) | Any PII → omit |

### `record_error` fields

| Parameter | Description | Example |
|-----------|-------------|---------|
| `error_keyword` | Error message keyword | `COLUMN NOT IN MASS BALANCE` |
| `block_type` | Block type involved | `RadFrac` |
| `property_method` | Property method used | `NRTL` |
| `cause` | Root cause description | `BASIS_D exceeds total feed flow` |
| `fix_direction` | What was done to fix | `Ensure BASIS_D < total feed flow` |
| `fix_path` | Aspen path changed | `Data.Blocks.{name}.Input.BASIS_D` |
| `tried_failed` | Optional — what didn't work | |

## Related Files

- `<ASPEN_USER_DATA>/error-history.md` — this machine's resolved-error log (writable)
- `<ASPEN_DOCS_ROOT>/error-history.md` — curated log shipped with the server (read-only)
- `<ASPEN_DOCS_ROOT>/convergence/convergence.md` — default methods, tear streams, convergence blocks; a block's own convergence fields are in its `blocks/<type>-convergence.md`
