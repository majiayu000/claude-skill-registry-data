---
name: directx-translation-development
description: Develop, integrate, debug, and validate DirectX translation stacks spanning D3D9-D3D12, DXGI, HLSL/DXBC/DXIL, Wine, DXVK, vkd3d-proton, DXMT, Vulkan, MoltenVK, SPIR-V, and Metal on Windows, Linux, macOS, or Apple Silicon. Use for rendering corruption, device creation failures, shader compilation or conversion bugs, feature-cap mismatches, synchronization and resource-lifetime faults, translation-layer architecture, Wine DLL routing, GPU capture analysis, performance regressions, and DirectX-to-Vulkan/Metal compatibility work.
---

# DirectX Translation Development

Treat the graphics stack as a sequence of independently testable contracts. Locate the first boundary where observable behavior diverges before changing code.

## Start with evidence

1. Read repository instructions and build metadata.
2. Record the guest architecture, host architecture, OS, Wine build, prefix, executable bitness, D3D API, translation DLLs, Vulkan/Metal implementation, GPU, and exact revisions.
3. Preserve the first failing logs, shader hashes, pipeline state, API result, and reproduction steps.
4. Identify which component owns each DLL and API boundary. Do not assume that `dxgi.dll`, `d3d12.dll`, or the shader compiler came from the same project.
5. Compare against the narrowest available oracle: native Windows, upstream Wine, a known-good DXVK/vkd3d-proton build, a Vulkan-native probe, or a Metal-native probe.

For the layer map and selection rules, read [references/architecture.md](references/architecture.md).

## Route the task

- D3D9/10/11, DXGI, DXVK, or Vulkan behavior: read `architecture.md` and [references/debugging.md](references/debugging.md).
- D3D12, DXGI interop, descriptor heaps, barriers, DXR, or vkd3d-proton: read `architecture.md` and `debugging.md`.
- HLSL, DXBC, DXIL, SPIR-V, MSL, reflection, binding, or precision problems: read [references/shaders.md](references/shaders.md).
- macOS, Apple Silicon, MoltenVK, DXMT, Winemetal, Xcode GPU capture, PE-to-Mach-O bridging, or SharpWine: read [references/apple-silicon.md](references/apple-silicon.md).
- Version-sensitive claims: consult [references/sources.md](references/sources.md), then verify the checked-out revision and current primary documentation.

## Debugging workflow

1. **Reproduce once without speculative overrides.** Capture the exit status and complete logs.
2. **Prove DLL routing.** Establish which PE DLLs loaded and which Unix/Mach-O modules they reached. A zero-byte layer log or missing module is a routing failure, not a shader failure.
3. **Prove adapter/device creation.** Record feature levels, extensions, formats, queues, memory types, and portability-subset restrictions.
4. **Minimize the failing workload.** Reduce to one adapter, device, resource, pipeline, draw/dispatch, present, or shader.
5. **Enable one diagnostic layer at a time.** Avoid changing synchronization, cache, compiler, and feature overrides simultaneously.
6. **Classify the first bad boundary:** API/ABI, object lifetime, state translation, shader translation, synchronization, memory/residency, presentation, or host driver/backend.
7. **Fix the owning layer.** Do not paper over a lower-layer defect with an application profile until the invariant and affected scope are known.
8. **Verify with a focused regression test, an upstream-style test when available, and the original application.** Recheck both debug and optimized builds.

Run `python3 scripts/triage_graphics_logs.py <logs...>` to summarize large mixed logs. Treat its categories as routing hints, not proof.

## Engineering guardrails

- Keep API correctness separate from performance tuning.
- Preserve HRESULT, Vulkan result, Metal error, shader hash, and object identity across logs.
- Treat DXVK and vkd3d-proton environment variables as revision-sensitive developer interfaces.
- Do not infer synchronization correctness from a successful frame. Express ownership, access, stage, layout, and queue transitions explicitly.
- Do not infer shader equivalence from successful compilation. Validate resources, layout, interpolation, precision, derivatives, subgroup/wave behavior, atomics, and outputs.
- Do not silently mix upstream Wine vkd3d, vkd3d-proton, DXVK DXGI, DXMT, or native Microsoft DLLs.
- On Apple Silicon, keep Windows guest bitness, PE module architecture, Wine CPU execution, native ARM64 bridge architecture, Vulkan portability, and Metal shader compilation as separate axes.
- Preserve reproducibility: pin revisions, hashes, patches, compiler versions, SDK versions, and generated shader artifacts.

## SharpWine specialization

When the repository is SharpWine/MetalSharp, first read its current `README.md`, release guarantees, architecture decisions, DXMT patch set, lockfiles, and validation scripts. Preserve these project invariants unless the user explicitly changes them:

- host Mach-O code remains ARM64-only;
- PE guest architecture does not determine the native bridge architecture;
- paired DXMT PE modules and ARM64 Winemetal bridge come from the same pinned source/configuration;
- Wine/GEM execution correctness and graphics translation correctness are validated independently;
- native Windows or another explicit oracle supplies behavioral evidence where macOS cannot establish the DirectX contract alone.

Never upgrade a planning claim into a compatibility claim without a runnable D3D acceptance fixture and captured evidence.
