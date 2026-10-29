---
name: ghidra-basics
description: Use when you need to reverse engineer a compiled binary on an
  authorized task, such as a CTF reversing challenge, malware triage in a lab,
  or auditing a binary you have permission to analyze. Covers importing
  binaries into Ghidra 11.4, running auto-analysis, navigating functions and
  cross-references, reading the decompiler output, renaming and retyping for
  clarity, finding the main logic and input handling, string and import
  analysis, and basic Ghidra Python scripting. Use when source code is
  unavailable and you must understand what a binary does, or before writing
  an exploit for it.
version: 1.0.0
domain: binary
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [pwn-fundamentals, heap-exploitation]
tools:
  - name: Ghidra
    version: "11.4"
  - name: Java
    version: 21.x
  - name: Python
    version: "3.12"
---

Ghidra is a free software reverse engineering suite that disassembles a
binary and lifts the assembly into readable C-like pseudocode. It is the
standard first tool when you face a binary with no source: a CTF reversing
challenge, a suspicious sample in a lab, or a proprietary component you are
authorized to audit. This skill covers the operator workflow in Ghidra 11.4:
importing and analyzing a binary, navigating functions and references,
reading the decompiler, cleaning up the output with renames and types, and
automating repetitive work with Python scripts. All work targets binaries
you are authorized to analyze, such as CTF files, lab samples, or client
software in scope.

## Quick Workflow

1. Identify the binary: architecture, format, stripped or not, and
   protections, before opening Ghidra.
2. Create a Ghidra project, import the binary, and run auto-analysis with
   the default analyzers.
3. Find the entry point and `main`, then read the decompiler output for
   the input handling logic.
4. Rename functions and variables and fix data types so the decompilation
   reads like source code.
5. Follow cross-references to trace interesting calls: input reads,
   dangerous functions, and crypto or network APIs.
6. Review strings and imports for hardcoded secrets, URLs, and suspicious
   library calls.
7. Script repetitive tasks (renaming, string search, structure recovery)
   with Ghidra's Python interpreter.
8. Export notes or the decompiled listing for the report or the exploit
   developer.

## 1. Triage before importing

Know what you are opening. Thirty seconds of triage saves an hour of
confusion in Ghidra.

```bash
# File type, architecture, and format
file ./challenge
checksec --file=./challenge 2>/dev/null || \
  hardening-check ./challenge 2>/dev/null

# Strings triage: look for usage text, prompts, and suspicious content
strings ./challenge | head -40
strings ./challenge | grep -i -E 'flag|password|/bin/sh|http' | head -20

# Imported library calls (dynamically linked binaries)
objdump -T ./challenge 2>/dev/null | grep -E 'system|exec|strcpy|gets|scanf|malloc' | head
# Or with readelf
readelf -d ./challenge | head
```

Stripped binaries have no symbol names; expect `FUN_00401230` style names
and plan to rename as you understand each function. Packed binaries show
tiny import tables and high-entropy sections; unpack before importing.

## 2. Import and analyze

```bash
# Launch Ghidra (needs Java 21 for Ghidra 11.x)
ghidraRun &
```

In the project window: File, New Project, Non-Shared Project, then File,
Import File, select the binary. Accept the detected format and language
(compiler spec). When prompted, run analysis now with the default
analyzers enabled.

Key analysis options to leave on for a first pass:

- Decompiler Parameter ID: recovers function signatures.
- ASCII Strings, Stack, Function Start Search: finds code the entry
  point analysis missed.
- For large binaries, disable the slower analyzers on the first pass
  and re-run them on demand.

After analysis, open the binary in the CodeBrowser. The default layout
gives you the listing, the decompiler window, the symbol tree, and the
data type manager. If the decompiler window is closed, open it with
Window, Decompiler.

## 3. Find main and read the logic

Start from the entry point and walk to `main`.

```bash
# In the Ghidra UI: use the Symbol Tree, filter for 'main' or 'entry'
# Keyboard: press 'g' and type the address or symbol to jump
```

Typical navigation path:

1. In the Symbol Tree, expand Functions and look for `main`. On
   stripped binaries, find `entry` instead, open its decompilation,
   and follow the last call before `exit`, which is usually
   `__libc_start_main` receiving `main` as its first argument.
2. Double-click `main` to open it in the decompiler.
3. Read the decompiled C top to bottom. Mark the input functions
   (`scanf`, `fgets`, `read`, `gets`) and the decision logic.
4. Right-click a variable, choose Rename, and give it a meaningful
   name. Press `L` to change a variable's data type.

Decompiler tips that save time:

- Double-click any function name to jump to its decompilation; use
  Alt+Left (or the back button) to return.
- Right-click a call and choose Find References to see every caller.
- If the decompiler shows a huge `switch` or weird casts, the types
  are probably wrong. Fix the parameter types first, then re-read.
- Commit your renames often: File, Save, or Ctrl+S. Ghidra stores
  analysis in the project database, not in the binary.

## 4. Cross-references and data flow

Cross-references (xrefs) answer "who calls this" and "who reads this",
which is how you trace input to a vulnerable sink.

```bash
# In the UI: select a function or variable, press Ctrl+Shift+F
# to find all references, or right-click, References, Find References to
```

Operator patterns:

- Find every call to `strcpy`, `strcat`, `sprintf`, `gets`: select the
  import in the Symbol Tree, list references, and check whether the
  destination buffer size is enforced at each call site.
- Find every read of a global flag variable to locate win conditions
  in CTF binaries.
- Trace a user input buffer: start at the `read` or `fgets` call,
  follow the buffer variable forward through the decompilation, and
  note every function that touches it.

Use the Function Graph view (Window, Function Graph) for complex
control flow. It renders the basic blocks visually and makes loop and
branch structure obvious when the linear listing is confusing.

## 5. Strings and imports review

The defined strings window (Window, Defined Strings) is searchable and
faster than the command line for iterative work.

```bash
# In the UI: Window, Defined Strings, then use the Filter box
# Search for: flag, password, key, http, /bin/sh, usage, error
```

For each interesting string, right-click and choose References to find
the code that uses it. A hardcoded credential string referenced from an
authentication function is an instant finding.

Review the imports (Symbol Tree, Imports) for the binary's capabilities:

- `system`, `execve`, `popen`: command execution.
- `socket`, `connect`, `bind`: networking.
- `ptrace`, `getenv("LD_PRELOAD")`: anti-debugging.
- `mmap`, `mprotect`: JIT or unpacking behavior.

## 6. Fixing types and structures

Real binaries pass structs by pointer. Teaching Ghidra the struct
layout turns pointer arithmetic into readable field accesses.

```bash
# In the Data Type Manager: right-click, New, Structure
# Add fields with their sizes, name the struct, then:
# In the decompiler, right-click a parameter, Retype Variable, pick the struct
```

Workflow for an unknown struct:

1. Note the offsets accessed in the disassembly (`param_1 + 0x18`).
2. Create a structure with placeholder fields covering those offsets.
3. Retype the pointer, re-read the decompiler, and rename fields as
   their purpose becomes clear (`fd`, `size`, `name`).

This is the highest-value cleanup step on CTF binaries: five minutes
of struct recovery can turn an unreadable function into obvious logic.

## 7. Scripting with Python

Automate the boring parts with Ghidra's Python 3 interpreter
(Window, Script Manager, or the Python console).

```python
# List all functions and their addresses (run in the Ghidra Python console)
for func in currentProgram.getFunctionManager().getFunctions(True):
    print("{} @ {}".format(func.getName(), func.getEntryPoint()))
```

```python
# Rename functions matching a pattern, e.g. password check candidates
from ghidra.program.model.symbol import SourceType
fm = currentProgram.getFunctionManager()
for func in fm.getFunctions(True):
    addr = func.getEntryPoint()
    for ref in getReferencesTo(addr):
        pass  # extend: inspect callers and rename by behavior
```

```python
# Find all calls to a dangerous import and print caller addresses
target = None
for sym in currentProgram.getSymbolTable().getSymbols("strcpy"):
    target = sym
    break
if target:
    for ref in getReferencesTo(target.getAddress()):
        print("strcpy called from {}".format(ref.getFromAddress()))
```

Save useful scripts in the Script Manager so the whole team reuses
them. Keep scripts small and single-purpose.

## 8. Exporting results

```bash
# Export the decompiled listing: File, Export Program
# Choose C/C++ format for the decompiler output, or ASCII for the listing
```

For exploit development, export the addresses you need: `main`, the
vulnerable function, `system` in the PLT, and string addresses. A short
text file with symbol-to-address mappings is more useful to the exploit
developer than a full export.

## Edge cases

- The binary is stripped. Everything is `FUN_` prefixed. Rename
  aggressively from `main` outward; the call graph from entry is your
  map.
- The binary is statically linked. The function list has thousands of
  library entries. Use FLIRT-style signature matching (Ghidra applies
  some automatically) and focus on the non-library code near `main`.
- Auto-analysis misses code, common in obfuscated or hand-written
  assembly. Use Search, For Instruction Patterns, or disassemble
  manually at a suspicious address with `D`.
- The decompiler output is nonsense for one function. The function
  boundaries are probably wrong. Clear the function (right-click,
  Delete) and recreate it with `F` at the true start.
- Ghidra runs out of memory on huge binaries. Raise the heap in
  `support/launch.properties` (`-Xmx4G` or higher) and restart.
- The binary targets an exotic architecture. Check that Ghidra has a
  language module (`.ldefs`) for it; without one, use the closest
  available or a different tool.

## Escalation

- You cannot find `main`: analyze the `entry` function, identify the
  `__libc_start_main` call, and its first argument is `main`. On
  stripped static binaries, look for the function that calls the most
  I/O routines.
- Control flow is flattened (obfuscator): the decompiler shows a giant
  dispatcher switch. Note the obfuscation, then work at the
  disassembly level block by block, or use a devirtualization script
  if the obfuscator is a known one.
- The binary unpacks itself at runtime: set a breakpoint on the
  unpacked entry in a debugger, dump the process memory, and import
  the dump into Ghidra instead of the packed file.
- You need a specific struct from a header file: use File, Parse C
  Source to import real C headers into the Data Type Manager instead
  of hand-building structures.
- Analysis must be shared: export the project or use a Ghidra server
  so teammates see your renames and comments.

## Detection and defender view

Ghidra is an offline analysis tool, so defenders do not detect its use;
they defend against what it enables. Anti-reverse-engineering controls
include stripping symbols, enabling compiler obfuscation or packing,
anti-debugging checks, and moving sensitive logic server-side. None of
these stop analysis, they only raise its cost. For defenders triaging
unknown binaries, the same Ghidra workflow inverts: import the sample,
check imports and strings for capability indicators, and trace network
and execution behavior before letting it run anywhere important.

## Key references

- CWE-798 (Use of Hard-coded Credentials): secrets found in strings.
- CWE-119 (Improper Restriction of Operations within the Bounds of a
  Memory Buffer): the memory bugs this analysis usually leads to.
- MITRE ATT&CK T1027 (Obfuscated Files or Information): packed or
  obfuscated binaries.
- MITRE ATT&CK T1106 (Native API): suspicious import usage.
- Ghidra documentation: https://ghidra-sre.org/documentation.html
- Ghidra API reference: https://ghidra.re/ghidra_docs/api/
- NSA Ghidra GitHub: https://github.com/NationalSecurityAgency/ghidra

## See also

- `ctf-reversing-basics`: Use it instead for the competition reversing workflow, adding dynamic debugging and deobfuscation around the Ghidra work.
- `ctf-reversing-basics-static-analysis-ghidra`: Use it instead for the competition version of the Ghidra static-analysis step.
