---
name: snx-gpu-shader
description: "Write and optimize ScarletNX's own compute shaders (astc.comp, vic.comp, future ones) for what the GPU actually executes: constant tables, bit twiddling, uniform branches, fewer fetches, workgroup and subgroup structure, exactness proofs, and the GLSL-as-C++ tests and lavapipe timing that check them. Use when writing, reviewing or speeding up a GLSL shader under src/nx/gpu/, or when deciding whether to split one."
---

# GPU shaders that cost less

Our shaders (`src/nx/gpu/texture/astc.comp` with `astc_decode.glsl`, `src/nx/gpu/video/vic.comp` with
`vic_compose.glsl`) must give the CPU reference's bytes and run well on drivers that optimize little. Assume
the backend lowers SPIR-V literally: no inlining across what you didn't inline, no constant folding of uniform
data, no strength reduction, no loop unrolling, private arrays in scratch memory, a select that evaluates both
sides. glslang `-O` (cmake/glsl.cmake) inlines and removes locals, nothing more: it made the old VIC shader
slower on lavapipe. Write the source as the machine code you want.

## Before changing anything

1. Read the CPU reference (`tests/support/astc.c`, `vic.c`'s `compose_cpu`) and the invariants its callers guarantee
   (`slot_resolve` clips slots to the target, NV12 starts are even). Invariants are free optimizations; write
   each one down where it is used, and make the host refuse jobs that break it (`vic_gpu_params` returns 0,
   the CPU composes) instead of paying for them per pixel.
2. Count what a pixel or texel costs now: loads, stores, shared memory accesses, barriers, multiplications,
   branches that differ within a subgroup. Find where the work repeats (per pixel what is per slot, per job,
   per pair, per row).

## The techniques, cheapest first

**Move invariants to the host.** Anything the same for the whole dispatch is computed once in C and passed
in: VIC's clamp, alpha and background are output bytes already, matrix coefficients are pre-scaled, rectangle
ends replace start plus size, block linear constants are shifts and masks (`bsh`, `ysh`, `gm`, `bstride`).
Per job or per pipeline constants go in specialization constants (ASTC's footprint).

**Uniform data in a uniform buffer.** Parameters every invocation reads go in a UBO, which NVIDIA serves as
instruction operands and AMD as scalar loads, not in a storage buffer and never copied to shared memory. Keep
the struct std140-safe: only 32 bit members, every struct a multiple of 16 bytes starting on 16. Then one
declaration serves GLSL, C (`#define uint u32` around the include) and the C++ tests (`vic_params.glsl`).

**Find the winner, then do the work.** When later work overwrites earlier work (VIC's slots), walk from the
last and stop when every pixel is claimed: one pass for the common case, not one per layer.

**Skip identities.** `(v << 2) >> 2`, a matrix that's disabled, a copy: VIC without its matrix moves whole
words. Check for a mode that makes the arithmetic an identity before writing the arithmetic.

**Fold shifts and clamps.** `floor(floor(x / a) / b) = floor(x / (a * b))`; a monotone map commutes with
clamp (`clamp(v, lo, hi) >> 2 == clamp(v >> 2, lo >> 2, hi >> 2)` for `lo <= hi`); `(x << k) * c == x * (c << k)`
modulo 2^32. Check every fold for overflow against the real ranges (20 bit coefficients times 10 bit samples
fit 31 bits, coefficients shifted by 15 don't).

**Share terms.** What a pair, a row or a 2x2 quad have in common (chroma, a row offset, a block's endpoints)
is computed once per group. Own a block of outputs per invocation (VIC: 4x2 pixels) so the sharing is in
registers and needs no shared memory.

**Constant tables in a word.** A small table indexed by a few bits is a shift and a mask of a constant
(`(0xC88C >> mode) & 1`, nibble tables, ASTC's encodings). A replication is a multiplication
(`v * 0x01010101`, a 4 bit mask to bytes: `((m * 0x204081) & 0x01010101) * 0xFF`). A range of lanes is
`(1 << hi) - (1 << lo)`. A partial merge is `a ^ ((a ^ b) & mask)`. A shift that can reach 32 is split
(`(w << 1) << (31 - s)`) or guarded by a uniform branch. A range test is one unsigned compare
(`y - y0 < h`). Two 16 bit lanes in one 32 bit multiply-add when neither carries (ASTC's interpolation).

**Words, not bytes.** Load and store 32 bits. A window that isn't aligned is two loads funneled
(`(w0 >> s) | (w1 << (32 - s))`). A store whose mask is full needs no read. Masking a byte that provably no
output uses is dead code: prove it (VIC: bytes past a plane's end are columns past the row) and delete it.

**Branches where the whole subgroup agrees.** Branch on per-job, per-slot, per-plane facts (alignment of
a slot's source, a matrix enabled, block linear or pitch): those never diverge. Per-pixel choices are masks
and selects. Arrange invocations so per-row parity work is identical in every invocation (VIC owns two rows,
so every invocation has an even and an odd row) rather than half the lanes idle.

**Fewer fetches through the hardware.** With a sampler, let the filter unit do the arithmetic: a bicubic
(Catmull-Rom or B-spline) filter is 4 bilinear fetches at offset coordinates with weights folded in
(16 taps to 4), a separable Gaussian or box uses the bilinear lerp to take two taps per fetch, and
`textureGather` brings 4 texels in one fetch. Our integer shaders read buffers, so this applies when a
shader samples images (scaling in VIC, a future upscaler): check that the filter's precision (8 bit
fractional weights on many GPUs) meets what the reference requires before using it.

**Workgroups, shared memory, barriers: only when data is reused across invocations.** Stage into shared
memory when many invocations read the same inputs many times (ASTC's decoded blocks, read by every texel of a
block) or a phase changes the work's shape (serial decode then wide stores). When each input is read once,
direct loads that coalesce are cheaper: the old VIC staged windows into shared memory behind two barriers and
was 3 to 4 times slower than loading straight. Size tiles to the memory layout (a 64x8 tile is one GOB of
8 bit luma), keep 64 invocations, and cull at tile level only when it removes work, not to save a compare.
Subgroup operations (ballot, shuffle) replace shared memory for neighbor exchange only where the subgroup
size is handled for every vendor (32 or 64; lavapipe varies).

**One shader, builds by define.** Split into variants only when a variant removes per-pixel work the
uniform branch can't (VIC's unaligned build: atomics and funnels the aligned case doesn't pay for). Build
variants from one source with `snx_glsl_spirv(... DEFINES X)`, never a copied file.

## Proving it gives the same bytes

- The body is GLSL that is also C++ (`tests/glsl/glsl.hpp` has the rules: macros for case labels, no out
  params, no swizzles, no whole-array assignment). A test includes it in a struct and runs it on the CPU
  against the reference: `astc_glsl`, `vic_glsl` (random jobs through the real config parser, both builds,
  every format and layout, plus a check that nothing around the output planes was written).
- Mutation-test the test: break each optimization on purpose (a shift, a mask, a parity case, a bound)
  and see it fail. A mutation that survives is either a hole in the test or dead code: find out which.
- `vulkan_headless` (`-DSNX_TEST_VULKAN=ON`, lavapipe) runs the real SPIR-V through the real renderer.
  Confirm a mutation fails there too: it proves the build rebuilt the SPIR-V (an include edit must recompile
  it).
- Write each identity used, with how it was checked, in the shader's header comment and its doc
  (`docs/ASTC.md`, `docs/VIC.md`).

## Measuring

Lavapipe (`VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json`) runs shaders on the CPU: it counts
operations and shows nothing of coalescing, divergence or occupancy, and its barriers are expensive. A gain
there is real but not the whole story; say which device a number comes from. Time old against new in one
process: compile the old shader and its host file under renamed symbols (`git show HEAD:path | sed`) into a
scratch benchmark beside the new one, check both write the same bytes, and report the median of repeated runs.
Use `snx-perf-expert` for real-GPU profiling (timestamp queries, vendor tools) and `snx-vulkan-expert` for
pipeline and synchronization questions.
