---
name: reverse-eng-dotnet
description: >
  Reverse a .NET / C# assembly — decompile, deobfuscate, debug, and IL-patch managed binaries.
  Load when the target is a managed PE (.exe/.dll with a CLR header), a Sharp* red-team tool
  (Rubeus, SharpHound, Seatbelt), a ConfuserEx/SmartAssembly/Babel/.NET-Reactor-obfuscated
  sample, or a .NET loader/stealer. Signals: "mscoree" / "_CorExeMain" / "mscorlib" strings,
  garbled Unicode class names in a decompiler, "deobfuscate this .NET", "patch/keygen a C# binary".
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
mitre: [T1027]
tools: [dnspyex, de4dot, ilspycmd, die, dnlib]
schema_version: 1
---

# .NET / C# assembly reversing

## When it applies
The binary is a managed .NET assembly — a thick client, a Sharp* red-team tool, or a captured
loader/stealer — and it is in scope (`tradecraft-scope-roe`, `scope.txt`). Pure-native PEs, IL2CPP
Unity builds, and NativeAOT output carry no CLR metadata: those go to `reverse-eng-binary-triage`.
dnSpyEx (the only GUI with an IL editor and debugger) is Windows-only; on Linux/macOS use
`ilspycmd` + `dotnet de4dot.dll` and accept that interactive patching/debugging needs Windows.

## Why it works
Managed assemblies keep near-complete metadata — type, method, and field names survive
compilation, so decompilation recovers close-to-source C#. Obfuscators only scramble names,
strings, and control flow, and de4dot automates the unscrambling for the common families. The IL
instruction stream is the ground truth: the C# view loses or distorts compiler-generated code
(async state machines, closures, `yield`), so decisive reads and every patch happen at IL level.

## Method
> Obfuscator identification table, de4dot options, anti-tamper bypasses, and IL patch recipes:
> see [`cheatsheet.md`](cheatsheet.md) next to this file.

1. **Confirm managed, not native.** `strings target.exe | grep -iE "mscoree|_CorExeMain|mscorlib|System\."`
   and `diec target.exe` (Detect It Easy reports .NET plus the obfuscator). Hard proof: PE data
   directory 14 (CLR header) non-zero, `_CorExeMain` entry, `#~`/`#Strings` metadata streams.
2. **Detect and strip obfuscation.** `de4dot --detect target.exe` to identify the family, then
   `de4dot target.exe -o target-clean.exe`. Keep the original untouched — all further analysis
   runs on the clean copy.
3. **Static in dnSpyEx.** C# view for fast browsing and string search (`password`, `verify`,
   `encrypt`, `http`, `Config`), IL view for anything decisive. Read order: `<module>` `.cctor`
   (deobfuscator/anti-tamper init runs first) → `Main` → the method that uses your located string
   (find via cross-references).
4. **Dynamic with the dnSpyEx debugger** when strings or config decrypt only at runtime: break on
   the decryptor's return and read the plaintext from Locals/Watch. Set exception breakpoints —
   obfuscators hide real control flow in `try`/`catch` dispatch, and breaking the thrown exception
   type shows the actual path. .NET debugging exposes object values directly; prefer it over
   grinding static IL.
5. **Patch via Edit IL, never Edit Method (C#).** Flip `ldc.i4.0`→`ldc.i4.1`, replace a check with
   `ldc.i4.1; ret`, or `nop` out a validation block, then File → Save Module as a new file. C#
   recompile fails constantly on state machines and lambdas; IL edits are instruction-exact.

## Gotchas
- **IL2CPP / NativeAOT look like .NET but are native** — `System.Private.CoreLib` strings, no CLR
  header. Route to `reverse-eng-binary-triage`.
- **New ConfuserEx anti-tamper / .NET Reactor necrobit defeat de4dot** — patch the integrity check
  to `ret` first, or run the binary and dump the decrypted assembly from memory (MegaDumper /
  ExtremeDumper), then clean the dump with de4dot. Themida .NET is a native virtualizing wrapper —
  de4dot cannot touch it; dump and go native.
- **Exception-driven control flow** can't be `nop`'d — trace the `catch` dispatch to find the real logic.
- **Keep artifacts on disk**: original, `*-clean.exe`, patched copy, and the extracted
  config/C2/keys — the findings folder needs reproducible evidence.
- **Run unknown samples in an isolated VM** — executing a managed binary runs its `.cctor`.

## Verify success
You can name the obfuscator (or confirm none), show decrypted strings/config/C2 or a patched
binary whose behavior provably changed, and the original sample is preserved for the diff.

## References
dnSpyEx, de4dot, and dnlib documentation; Washi's "Misconceptions about .NET reversing" (IL over
C# decompiler output).

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
