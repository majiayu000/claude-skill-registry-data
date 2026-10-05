---
name: lax-simulator-run
description: >
  Run compiled LAX VSP programs on the local runsim simulator (S32DS/tools/LAX_Simulator/runsim).
  Executes an .eld file on a chosen VSPA3 device model (2AU / 16AU / 64AU), prints cycle
  counts, program flow, or redirected stdout, and forwards simulator-level flags before the
  .eld and program-level flags after the .eld. Use when the user asks to "simulate a LAX
  program", "run this .eld on runsim", "get the cycle count on VSPA3 16AU", or similar.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[compiler, lax, simulator, runsim, vspa3, eld, cycle-count, dsp, s32, embedded]'
---

# LAX Simulator Run (runsim)

Run a compiled LAX executable (`.eld`) on the local `runsim` cycle-accurate simulator
shipped with S32 Design Studio under `S32DS/tools/LAX_Simulator/runsim`. Report exit
status, cycle counts, and program-flow traces.

> `runsim` executes **only `.eld` files** (linked LAX executables produced by `laxcc`).
> Object files (`.eln`), source (`.c`, `.sl`), or any other extension are rejected by this
> skill before invocation. If the user has only source or `.eln` files, first build an
> `.eld` with `lax-compiler-explorer` or `lax-linker-explorer`.

## When to use

Use this skill when:
- User asks "run this `.eld` on the LAX simulator"
- User asks "what's the cycle count of this program on VSPA3 16AU / 64AU?"
- User asks "trace program flow / show register values while executing on LAX"
- User wants to redirect simulator stdout to a file for later inspection

Do **not** use this skill for:
- Compiling C/C++ to LAX assembly -> `lax-compiler-explorer`
- Linking `.eln` objects into `.eld` -> `lax-linker-explorer`
- Static size/symbol analysis of an `.eld` -> `lax-binary-analysis`
- ARM simulation -> unrelated toolchains

## Available capabilities

This skill uses the standardized `search_actions` + `execute_action` MCP tool surface.

| Action name | Purpose |
|---|---|
| `compiler.list_lax_simulator_tools` | Discover simulator binaries; call first |
| `compiler.lax_simulator_execute` | Run `runsim` on an `.eld` |

Invoke via:
1. `search_actions(query="lax simulator")` to retrieve the action schema.
2. `execute_action(action_name="compiler.list_lax_simulator_tools")` to discover.
3. `execute_action(action_name="compiler.lax_simulator_execute", params={...})` to run.

## The runsim command line

```
runsim [simulator-options] <eldfile> [program-options]
```

Two argument regions with different meaning:

1. **Simulator flags** -- everything **before** the `.eld` filename. These configure the
   simulator itself (device model, verbosity, tracing, output redirection, exit label,
   etc.). They are what you place in the `args` parameter of `compiler.lax_simulator_execute`.
2. **Program flags** -- everything **after** the `.eld` filename. These are passed
   through to the user program (`argv[]` seen by the LAX application). They are **not**
   interpreted by `runsim`.

The `compiler.lax_simulator_execute` action already appends the resolved `.eld` path after
`args`, so put simulator flags in `args`. If the program itself needs arguments, append them
to `args` **after** you have confirmed with the user; keep in mind the action positions the
`.eld` at the end -- if program-level arguments are required, invoke with `executable_file`
omitted and inline both the eld and trailing args in `args` (see "Passing program arguments"
below).

### Simulator flags (runsim options)

Reference (from `runsim -h`):

| Flag | Meaning |
|------|---------|
| `-d <device>` | Alternate device model. Supported: `vspa3_2au`, `vspa3_16au`, `vspa3_64au` |
| `-l` | Be loud (verbose simulator log) |
| `-t` | Output timing / cycle count |
| `-v`, `-ver` | Print simulator version |
| `-h` | Display help and exit |
| `-redir <fname>` | Redirect simulated stdout to `<fname>` |
| `-showpc` | Print program flow (equivalent to Debugger Shell `print on`) |
| `-showregs` | Print program flow + core register values (`print on` + `trace on`) |
| `-exitlbl <label>` | Replace default exit label `___crt0_end` with `<label>` |
| `-imodel` | Option applied during simulator initialization |
| `-smodel` | Option applied after init, before execution begins |

### Program flags

Anything after the `.eld` is forwarded verbatim to the LAX program. `runsim` does not
inspect these; use them only if the compiled program actually parses `argv`.

## Quickstart

### 1. Discover the simulator

```
execute_action(action_name="compiler.list_lax_simulator_tools")
```

Verify `runsim` (or `runsim.exe` on Windows) is present. If not, stop and tell the user
the LAX simulator is not installed.

### 2. Validate the input file

Before calling `compiler.lax_simulator_execute`:
- The `executable_file` **must end in `.eld`** (case-insensitive). Reject anything else
  with a clear message telling the user to build/link an `.eld` first.
- Confirm the file exists on disk.

### 3. Run runsim with cycle count on VSPA3 16AU

```jsonc
execute_action(
  action_name="compiler.lax_simulator_execute",
  params={
    "binary": "runsim",
    "args": "-d vspa3_16au -t",
    "executable_file": "output/main.eld"
  }
)
```

Resulting command line:

```
runsim -d vspa3_16au -t <abs>/output/main.eld
```

Report `exit_code`, cycle count (from stdout), and the `saved_to` scratch dir.

### 4. Program-flow / register trace

```jsonc
execute_action(
  action_name="compiler.lax_simulator_execute",
  params={
    "binary": "runsim",
    "args": "-d vspa3_64au -showregs",
    "executable_file": "output/main.eld"
  }
)
```

Use `-showpc` for lighter flow-only tracing; `-showregs` can produce very large logs on
long-running programs -- warn the user first.

### 5. Redirect simulated stdout

```jsonc
execute_action(
  action_name="compiler.lax_simulator_execute",
  params={
    "binary": "runsim",
    "args": "-d vspa3_16au -redir sim_stdout.txt",
    "executable_file": "output/main.eld"
  }
)
```

`sim_stdout.txt` is written into the per-call scratch dir (`saved_to`).

## Passing program arguments (post-eld flags)

`compiler.lax_simulator_execute` always appends the `.eld` path last when `executable_file`
is provided. If the user needs to pass flags **to the program** (i.e. real post-eld
arguments), do one of:

- Recompile / relink the LAX program so it does not require argv (preferred), OR
- Call with `executable_file` omitted and inline both the eld and the trailing program
  args in `args`, for example:

  ```jsonc
  execute_action(
    action_name="compiler.lax_simulator_execute",
    params={
      "binary": "runsim",
      "args": "-d vspa3_16au -t <abs path to main.eld> --my-prog-flag 42"
    }
  )
  ```

  Always resolve `<abs path to main.eld>` first and verify it ends in `.eld`.

## Configuration

Key simulator facts:
- Binary: `runsim` (`runsim.exe` on Windows), under
  `S32DS/tools/LAX_Simulator/`
- Accepted input: linked LAX executable, extension `.eld` only
- Default device: whatever `runsim` picks if `-d` is omitted -- **always pass `-d`**
  explicitly to make results reproducible
- Device options: `vspa3_2au`, `vspa3_16au`, `vspa3_64au`
- Default exit label: `___crt0_end` (override with `-exitlbl`)

## Guardrails

**Scope**
- Uses only `compiler.list_lax_simulator_tools` and `compiler.lax_simulator_execute`
  via `execute_action`. No user files modified; all outputs written to the per-call
  scratch directory (`saved_to`).

**Input validation**
- Reject any `executable_file` whose extension is not `.eld`. Do not attempt to run
  `.eln`, `.c`, `.sl`, or unknown files through `runsim`.
- Refuse if the file does not exist.

**Refuse-and-escalate**
- If `runsim` is not found under the configured LAX simulator root, stop and report.
- If the user does not specify a device (`-d`), ask which VSPA3 variant to target --
  results differ substantially between `2au`, `16au`, and `64au`.
- Do not silently mix simulator flags and program flags; explicitly place simulator
  flags in `args` (before the eld) and only add program flags with user confirmation.

**Resource limits**
- `-showregs` and `-l` on long programs can generate huge logs. Warn the user before
  enabling either on programs whose runtime is unknown.

**Secrets**
- Do not echo redirected simulator stdout that may contain sensitive user data beyond
  what the user requested.

## Workflow

### Step 1 -- Discover

```
execute_action(action_name="compiler.list_lax_simulator_tools")
```

Confirm `runsim` (or `runsim.exe`) is present in the output.

### Step 2 -- Confirm device

Ask the user which VSPA3 variant to target if not specified:

| User hint | Flag |
|-----------|------|
| Minimal / 2AU  | `-d vspa3_2au`  |
| S32R45-like / 16AU | `-d vspa3_16au` |
| Full width / 64AU  | `-d vspa3_64au` |

### Step 3 -- Validate the eld

Ensure `executable_file` ends in `.eld` and exists. Otherwise abort with a clear
message.

### Step 4 -- Compose simulator flags

Place all `runsim` flags (device, `-t`, `-showpc`, `-showregs`, `-redir`, `-exitlbl`,
`-imodel`, `-smodel`, ...) in `args`. Do **not** put program flags there unless the user
explicitly asked and understood the ordering constraint.

### Step 5 -- Execute

```jsonc
execute_action(
  action_name="compiler.lax_simulator_execute",
  params={
    "binary": "runsim",
    "args": "<simulator flags>",
    "executable_file": "<path to .eld>"
  }
)
```

### Step 6 -- Report

Summarize:
- Command line actually run (from `command` field in the result)
- Exit code (`0` = success; other values = simulator/program error)
- Cycle count / timing (if `-t` was set)
- Trace snippets (if `-showpc`/`-showregs` were set)
- Path to `saved_to` for full logs and any `-redir` output file

## Validation loop

1. `execute_action(action_name="compiler.list_lax_simulator_tools")` shows `runsim` (or `runsim.exe`).
2. `executable_file` ends in `.eld` and exists on disk.
3. `args` contains an explicit `-d vspa3_{2,16,64}au`.
4. `execute_action(action_name="compiler.lax_simulator_execute", ...)` returns `success=true` (or a clearly reported failure).
5. Requested metric (cycle count / trace / redirected stdout) is visible in the result
   or under `saved_to`.

## Out of scope

- Compilation / linking (use `lax-compiler-explorer`, `lax-linker-explorer`)
- Static binary analysis (use `lax-binary-analysis`)
- ARM simulation

## See also

- `lax-compiler-explorer` -- build `.eln`/`.eld` from C/C++
- `lax-linker-explorer` -- link `.eln` objects into an `.eld`
- `lax-binary-analysis` -- inspect symbols/sections in an `.eld`
