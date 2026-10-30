---
name: reverse-engineering
description: >-
  Understanding how a compiled, obfuscated, packed or virtualized target works:
  binaries and firmware, Android APKs and iOS IPAs, .NET and JVM assemblies,
  WASM and custom VMs, browser extensions, network protocols, stripped Go/Rust,
  anti-debug and anti-VM logic — plus turning a website's traffic into a typed
  API client. Use when the job is to read a target's behaviour before porting,
  patching or exploiting it.
---

# reverse-engineering — targets, methods, technique library

> Home branch in Memora: `root/skill/reverse-engineering`.
>
> Work on copies inside the task's case directory. Never run an unknown sample,
> patch an original, or expand scope without a reason.

## Choosing a part

| Target | Part |
|---|---|
| Android APK & iOS IPA: unpack, decompile, smali, repackage, Frida, pinning | `parts/mobile-reverse/` |
| Cross-version symbol migration, BinDiff/Diaphora work | `parts/binary-diff/` |
| Chrome/Firefox extension: manifest, workers, message passing | `skills/reverse-engineering/parts/browser-extension-reverse/` |
| .NET / C# assembly (IL, obfuscators, dnSpy, de4dot) | `parts/dotnet-reverse/` |
| WASM-like custom VM, DSL interpreter, JS risk engine | `parts/dsl-vm-reverse/` |
| Ghidra headless or GUI, decompiler, MCP workflows | `parts/ghidra-reverse/` |
| Stripped Go or Rust binary: pclntab, metadata, panic strings | `parts/go-rust-reverse/` |
| IDA Pro workflows and scripting | `parts/ida-reverse/` |
| Frontend JavaScript: signature chains, page observation, hooks | `parts/js-reverse/` |
| macOS / Mach-O: codesign, Objective-C/Swift recovery | `parts/macos-reverse/` |
| Custom binary protocol, Protobuf/gRPC, WebSocket frames, PCAP | `parts/protocol-reverse/` |
| radare2 from the command line | `parts/radare2/` |
| Website → typed API client: capture HAR, generate Python/TS/Go/Java | `parts/reverse-api-engineer/` |

## Technique library (`references/`)

Read only the reference file the target requires:

- `references/tools.md`, `references/tools-dynamic.md`, `references/tools-advanced.md` — static/dynamic/deobfuscation toolchains (GDB, Ghidra, r2, IDA, Frida, angr, x64dbg, Qiling, VMProtect, LIEF).
- `references/anti-analysis.md` — anti-debug, anti-VM, anti-DBI, MBA simplification.
- `references/patterns.md`, `references/patterns-ctf.md`, `references/patterns-ctf-2.md`, `references/patterns-ctf-3.md` — VM opcodes, self-modifying code, lattice/crypto patterns.
- `references/languages.md`, `references/languages-compiled.md`, `references/languages-platforms.md` — Python bytecode, UEFI, Go, Rust, Swift, Kotlin, C++, Electron.
- `references/platforms.md`, `references/platforms-hardware.md`, `references/elf-analysis.md`, `references/go-reverse.md`, `references/kernel-driver-reverse.md`, `references/crypto-decode-tools.md`, `references/field-notes.md`, `references/awesome-re-resources.md`.

## Rules

- Walk `root/skill/reverse-engineering` (and the project root) in Memora before starting; record verified offsets, structures, and dead-ends as nodes.
- Use `ask_questions` when choosing between static reconstruction vs. dynamic instrumentation, or before running any sample on the host.
- State-changing operations happen on copies inside the task folder, never on the original artifact.

## Related

`security` (surface assessments, `skills/security/parts/malware-analysis/`), `browser` (extension runtime, HAR capture), `dev` (writing the clean port or client).
