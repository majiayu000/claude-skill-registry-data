---
name: snx-gpu-shader
description: "Write and optimize ScarletNX's own compute shaders (astc.comp, vic.comp, future ones) for what the GPU actually executes. It covers constant tables, bit tricks, uniform branches, fewer fetches, and workgroup and subgroup structure. It also covers proofs of exactness, and the GLSL-as-C++ tests and lavapipe time measurements that check them. Use it when you write, review or speed up a GLSL shader under src/nx/gpu/. Use it also when you decide if you split a shader."
---

# GPU shaders that cost less

Our shaders must give the same bytes as the CPU reference. They must also run well on drivers that optimize little.
Our shaders are `src/nx/gpu/texture/astc.comp` with `astc_decode.glsl`, and `src/nx/gpu/video/vic.comp` with
`vic_compose.glsl`. Assume that the backend lowers SPIR-V literally:
- It does not inline a function that you did not inline.
- It does not fold constants from uniform data.
- It does no strength reduction.
- It does not unroll loops.
- It puts private arrays in scratch memory.
- A select evaluates the two sides.

glslang `-O` (cmake/glsl.cmake) inlines and removes locals, and does nothing more. It made the old VIC shader slower
on lavapipe. Write the source as the machine code that you want.

## Before you change anything

1. Read the CPU reference (`tests/support/astc.c`, `compose_cpu` in `vic.c`). Read also the invariants that its
   callers guarantee. For example, `slot_resolve` clips slots to the target, and NV12 starts are even.

   Invariants are free optimizations. Write each one down where the code uses it. Make the host refuse jobs that
   break it (`vic_gpu_params` returns 0 and the CPU composes). Do not pay for the invariant per pixel.
2. Count the cost of a pixel or texel now. Count loads, stores, shared memory accesses, barriers and
   multiplications. Count also the branches that differ within a subgroup. Find where the work repeats: work per
   pixel that is the same for each slot, job, pair or row.

## The techniques, the cheapest first

**Move invariants to the host.** Calculate a value that is the same for the whole dispatch one time in C, and pass it
in. VIC's clamp, alpha and background are already output bytes. The host scales the matrix coefficients before the
dispatch. Rectangle ends replace start plus size. Block linear constants are shifts and masks (`bsh`, `ysh`, `gm`,
`bstride`).

Put constants per job or per pipeline in specialization constants (the footprint of ASTC).

**Uniform data in a uniform buffer.** Put the parameters that every invocation reads in a UBO. NVIDIA serves a UBO as
instruction operands, and AMD as scalar loads. Do not put them in a storage buffer, and never copy them to shared
memory.

Keep the struct std140-safe. Use only 32 bit members. Make every struct a multiple of 16 bytes that starts on 16.
Then one declaration serves GLSL, C (`#define uint u32` around the include) and the C++ tests (`vic_params.glsl`).

**Find the winner, then do the work.** Later work can write over earlier work (VIC's slots). Then start from the last
item, and stop when every pixel has a slot that claims it. That gives one pass for the usual case, not one pass per
layer.

**Skip identities.** Examples are `(v << 2) >> 2`, a disabled matrix and a copy. VIC without its matrix moves whole
words. Before you write the arithmetic, look for a mode that makes it an identity.

**Fold shifts and clamps.** These folds are exact: `floor(floor(x / a) / b) = floor(x / (a * b))`, and
`(x << k) * c == x * (c << k)` modulo 2^32. A monotone map commutes with clamp
(`clamp(v, lo, hi) >> 2 == clamp(v >> 2, lo >> 2, hi >> 2)` for `lo <= hi`). Check every fold for overflow against
the real ranges. For example, 20 bit coefficients times 10 bit samples fit in 31 bits, but coefficients with a shift
of 15 do not.

**Share terms.** Some values are common to a pair, a row or a 2x2 quad (chroma, a row offset, the endpoints of a
block). Calculate them one time per group. Give each invocation a block of outputs (VIC: 4x2 pixels). Then the shared
values stay in registers and need no shared memory.

**Constant tables in a word.** A small table that a few bits index is a shift and a mask of a constant
(`(0xC88C >> mode) & 1`, nibble tables, the encodings of ASTC). A replication is a multiplication
(`v * 0x01010101`, a 4 bit mask to bytes: `((m * 0x204081) & 0x01010101) * 0xFF`). A range of lanes is
`(1 << hi) - (1 << lo)`. A partial merge is `a ^ ((a ^ b) & mask)`.

Split a shift that can reach 32 (`(w << 1) << (31 - s)`), or guard it with a uniform branch. A range test is one
unsigned compare (`y - y0 < h`). Put two 16 bit lanes in one 32 bit multiply-add when neither lane carries (the
interpolation of ASTC).

**Words, not bytes.** Load and store 32 bits. An unaligned window is two funneled loads
(`(w0 >> s) | (w1 << (32 - s))`). A store with a full mask needs no read. A mask on a byte that no output uses is
dead code. Prove that no output uses it, and delete the mask (in VIC, the bytes past the end of a plane are columns
past the row).

**Branches where the whole subgroup agrees.** Branch on facts per job, per slot or per plane. Examples are the
alignment of a slot's source, an enabled matrix, and block linear or pitch. These branches never diverge. Use masks
and selects for choices per pixel.

Arrange the invocations so that the work for each row parity is the same in every invocation. In VIC, each
invocation owns two rows, so it has an even and an odd row. Otherwise half the lanes do nothing.

**Fewer fetches through the hardware.** With a sampler, let the filter unit do the arithmetic. A bicubic filter
(Catmull-Rom or B-spline) is 4 bilinear fetches at offset coordinates, with the weights folded in (16 taps to 4). A
separable Gaussian or box filter uses the bilinear lerp to take two taps per fetch. `textureGather` brings 4 texels
in one fetch.

Our integer shaders read buffers. Thus this applies only when a shader samples images (the scale step in VIC, a
future upscaler). Before you use the filter, check that its precision meets the requirement of the reference. Many
GPUs have 8 bit fractional weights.

**Workgroups, shared memory, barriers: only when invocations share data.** Stage data into shared memory when many
invocations read the same inputs many times. ASTC's decoded blocks are an example: every texel of a block reads them.
Stage data also when a phase changes the shape of the work (serial decode, then wide stores).

When each input has only one read, direct loads that coalesce cost less. The old VIC staged windows into shared
memory behind two barriers. It was 3 to 4 times slower than direct loads.

Size tiles to the memory layout (a 64x8 tile is one GOB of 8 bit luma). Keep 64 invocations. Cull at tile level only
when it removes work, not to save a compare. Subgroup operations (ballot, shuffle) can replace shared memory for
neighbor exchange. Use them only where the code handles the subgroup size of every vendor (32 or 64, and lavapipe
varies).

**One shader, builds by define.** Split into variants only when a variant removes per-pixel work that the uniform
branch cannot remove. An example is the unaligned build of VIC: it has atomics and funnels that the aligned case does
not pay for. Build variants from one source with `snx_glsl_spirv(... DEFINES X)`, never from a copied file.

## Prove that it gives the same bytes

- The body is GLSL that is also C++. `tests/glsl/glsl.hpp` has the rules: macros for case labels, no out params, no
  swizzles and no whole-array assignment. A test includes the body in a struct and runs it on the CPU against the
  reference. The tests are `astc_glsl` and `vic_glsl`. `vic_glsl` sends random jobs through the real config parser,
  for the two builds and every format and layout. It also checks that the shader wrote nothing around the output
  planes.
- Mutation-test the test. Break each optimization on purpose (a shift, a mask, a parity case, a bound) and make sure
  that the test fails. A mutation that survives is a hole in the test or dead code. Find which of the two it is.
- `vulkan_headless` (`-DSNX_TEST_VULKAN=ON`, lavapipe) runs the real SPIR-V through the real renderer. Make sure that
  a mutation fails there too. That proves that the build made the SPIR-V again (an edit to an include must cause a
  recompile).
- Write each identity that the shader uses, and how you checked it, in the header comment of the shader. Write them
  also in its doc (`docs/ASTC.md`, `docs/VIC.md`).

## Measure

Lavapipe (`VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json`) runs shaders on the CPU. It counts operations, but
it shows nothing of how loads coalesce, of divergence or of occupancy. Its barriers are expensive. A gain there is
real, but it does not tell all. Say which device a number comes from.

Measure the time of the old shader against the new one in one process:
1. Compile the old shader and its host file with renamed symbols (`git show HEAD:path | sed`). Put them in a scratch
   benchmark next to the new one.
2. Check that the two write the same bytes.
3. Report the median of repeated runs.

Use `snx-perf-expert` to profile on a real GPU (timestamp queries, vendor tools). Use `snx-vulkan-expert` for
questions about pipelines and synchronization.
