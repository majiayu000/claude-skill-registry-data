---
name: mips-uclibc-static-triage
description: Use when statically analyzing MIPS little-endian uClibc firmware binaries, ELF objects, static archives, shared libraries, relocations, symbols, disassembly, exec/system wrappers, or Broadcom/router-style native code. Helps distinguish argv-based exec paths from shell-string execution.
metadata:
  short-description: Static triage for MIPS/uClibc firmware code
---

# MIPS/uClibc Static Triage

Use this skill for read-only MIPS firmware binary/object analysis. Prefer conservative conclusions and cite artifact names, symbols, relocation offsets, and disassembly addresses where practical.

See `references/TOOLS.md` for the external command-line and MIPS-capable Binutils setup used by this workflow.

## Workflow

1. Classify artifacts.
   - Run `file`, `readelf -h`, `readelf -S`, `readelf -s`, and `readelf -r`.
   - Note stripped vs unstripped, relocatable object vs executable/shared object, endian, ABI, and architecture.

2. Locate symbols and imports.
   - Use `nm -A` for object files and archives.
   - Use `readelf -Ws` or dynamic symbols for stripped ELF binaries/shared libraries.
   - For stripped executables, map imports through PLT/GOT call sites and nearby strings; treat names recovered from strings as candidates unless call linkage is shown.
   - Track wrappers around `system`, `_eval`, `execve`, `execv`, `execvp`, `popen`, `fork`, `waitpid`, `kill`, `unlink`, `mktemp`, upload/file APIs, and NVRAM APIs.

3. Disassemble with the right target.
   - For MIPS little-endian objects, prefer:

```sh
objdump -Dr -b elf32-little -m mips:isa32 artifact.o
```

   - For ELF executables/shared libraries, `objdump -dr artifact` may be enough if binutils recognizes the target.

4. Determine execution model.
   - `system(char *cmd)`, `popen`, or `/bin/sh -c` means shell-string execution.
   - `fork` plus `execv/execvp/execve` with `char *const argv[]` means argv-based execution. Confirm by checking argument register setup (`a0 = argv[0]`, `a1 = argv`) when possible.
   - Wrapper functions can make execution mixed across the program. Report per call site.

5. Handle relocatable objects carefully.
   - Calls may appear as branch/jump instructions with relocation records naming the real target.
   - Use relocation tables to resolve external call names.
   - Do not infer final linked addresses from `.o` offsets alone.

## MIPS Notes

- Arguments usually flow through `$a0-$a3`; return values through `$v0`.
- `jal`/`jalr` call targets may require relocation, dynamic symbol, or GOT/PLT review.
- Delay slots can contain meaningful instructions.
- String address construction often uses `lui/addiu` pairs or GOT-relative loads.

## Reporting Rules

- Label whether an execution path is `argv-based`, `shell-string`, or `mixed/unclear`.
- Separate wrapper behavior from caller-controlled data flow.
- Avoid exploitability claims unless user-controlled data reaches a dangerous sink with enough evidence.
