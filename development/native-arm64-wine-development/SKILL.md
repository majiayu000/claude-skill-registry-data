---
name: native-arm64-wine-development
description: Orchestrate native ARM64 Wine and compatibility-layer development on Apple Silicon, including ARM64EC/ARM64X, PE and Mach-O boundaries, x86 and AArch64 emulation, custom DLLs, build systems, dependency integration, graphics translation, debugging, validation, and performance work. Use when a task spans several skills in this package or needs an end-to-end implementation plan for Wine, FEX, DXVK, vkd3d-proton, DXMT, MoltenVK, LLVM-MinGW, or Xcode-based native ARM64 development.
---

# Native ARM64 Wine Development

Coordinate cross-cutting native ARM64 Wine work. Keep architecture boundaries explicit, choose the smallest specialist skill set that covers the task, and validate each binary at the ABI boundary where it will run.

## Start with the execution map

Before editing code, identify:

1. The host OS and CPU architecture.
2. Every produced binary's format: Mach-O, ELF, PE/COFF, or hybrid ARM64X.
3. The calling convention and runtime owner at each boundary.
4. The guest architecture being supported: AArch64, ARM64EC, x86_64, or i386/WoW64.
5. The graphics path, if any: Direct3D, DXGI, Vulkan, SPIR-V, MoltenVK, or Metal.
6. The build system, cross toolchain, sysroot, and dependency prefixes.

Do not treat “ARM64” as a complete target description. Record the object format, ABI, platform, and runtime together.

## Route to specialist skills

Load only the skills needed for the current task:

- Architecture and ABI: `assembly-arm`, `assembly-x86`, `dynamic-linking`, `simd-intrinsics`
- Compilers and linkers: `clang`, `llvm`, `cross-gcc`, `msvc-cl`, `linkers-lto`, `binary-hardening`
- Builds and dependencies: `make`, `cmake`, `meson`, `ninja`, `conan-vcpkg`, `build-acceleration`
- Debugging and correctness: `lldb`, `sanitizers`, `static-analysis`, `debug-optimized-builds`, `concurrency-debugging`, `memory-model`
- Performance: `cpu-cache-opt`, `pgo`
- Graphics translation: `directx-translation-development`, `slang-shader-engineer`
- Apple build tooling: `spm-build-analysis`, `xcode-build-benchmark`, `xcode-build-fixer`, `xcode-build-orchestrator`, `xcode-compilation-analyzer`, `xcode-project-analyzer`

For Wine graphics failures, start with `directx-translation-development`, then add architecture, linker, shader, or debugger skills only after locating the first failing boundary.

## Build in dependency order

1. Pin source revisions and record patches.
2. Establish the native host toolchain and SDK.
3. Build foundational libraries into architecture-specific prefixes.
4. Build emulation or CPU-provider components.
5. Build Wine and custom PE modules against the intended ABI.
6. Build graphics translation layers from the lowest API upward.
7. Assemble the runtime without mixing incompatible prefixes.

Keep downloaded source, build directories, installation prefixes, and final bundles separate. Make every generated target depend on its real inputs; avoid timestamp-only or order-dependent build rules.

## Validate every boundary

Use format-aware inspection before runtime testing:

- Mach-O: `file`, `lipo`, `otool`, `nm`, `codesign`
- PE/COFF: `llvm-readobj`, `llvm-objdump`, `llvm-nm`, `llvm-dlltool`
- ELF: `readelf`, `objdump`, `nm`, loader diagnostics
- Shaders: DXBC/DXIL, SPIR-V, and Metal validation tools appropriate to the stage

Confirm architecture, imports, exports, install names or loader paths, symbol visibility, and signatures. Then run a minimal smoke test for each layer before testing a full application.

## Debug from the first divergence

Capture logs from each translation boundary and find the earliest observable mismatch. Prefer a minimal reproducer over changing several layers at once. Preserve exact compiler commands, binary metadata, environment variables, and runtime logs in the report.

## Finish with reproducibility

Record pinned commits, patches, toolchain versions, dependency versions, build commands, and checksums. The result should be rebuildable in a clean tree without relying on untracked local prefixes.
