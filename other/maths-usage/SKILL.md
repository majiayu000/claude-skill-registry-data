---
name: maths-usage
description: "Picks Puck.Maths primitives and determinism rules: FixedQ4816, FixedVector3, rate accumulators, Pcg32XshRr, AliasTable, Fnv1aHash, rounding, saturation, primes. Law cases: maths-laws."
---

# Puck.Maths: choose, obey, verify

Puck.Maths is the deterministic numerics library for values a simulation
advances, compares, hashes, snapshots or replays: the same inputs give the same
bits on every machine, backend and run. Presentation-only floats, shaders,
renderer or UI math and explicit presentation conversions are outside this
contract. Each wing has a README that owns its contracts; when one disagrees
with this file, the wing wins.

## Choose

Search the library and the relevant wing README before hand-rolling numeric
behavior ([`content-search`](../content-search/SKILL.md) finds candidates). A
second implementation of a lerp, clamp, GCD, floor division, bit mixer or rate
carrier can diverge in rounding, overflow or floor and ceiling convention.

| The value is | Use | Not |
|---|---|---|
| A signed quantity with an integer part: position, velocity, accumulated advance | `FixedQ4816` (Q48.16 on a `long`) | `float`/`double`; a bare `long` scaled by hand |
| The same, never negative | `UFixedQ4816` | `FixedQ4816` plus an assertion |
| A fraction in `[0, 1)` | `UnitFraction16` or `UnitFraction32` | A Q48.16 promised to stay under one |
| A weight or probability that must reach 1 | `UnitInterval32` (closed `[0, 1]`) | `UnitFraction32`, which has no `One` |
| A 2D or 3D displacement | `FixedVector2` / `FixedVector3` | Three scalars |
| A rotation | `FixedComplex` (2D), `FixedQuaternion` (3D), `FixedRigidTransform` (rotation plus translation) | Hand-built matrices |
| A world position beyond a small scene | `FixedPosition` (cell indices plus a local offset) | A bare `FixedVector3`, which is a displacement |
| A rate integrated over ticks | `FixedRateAccumulator` / `FixedVector3RateAccumulator` | A per-second velocity pre-rounded into one per-tick delta |
| A target that eases or overshoots | `SecondOrderDynamics` | `SecondOrderFollower`, the presentation-only float twin |
| Lerp or clamp | `FixedQ4816.Lerp` / `.Clamp`, `FixedVector3.Lerp`, `FixedQuaternion.Slerp` | A hand-rolled `a + (b - a) * t` |
| Sequential random draws | `Pcg32XshRr` | `System.Random`, `Random.Shared` |
| A weighted pick | `WeightedSampler.Create` once at load, then `AliasTable<T>.Sample` | A per-call cumulative scan over floats |
| A shuffle | `Pcg32XshRr.Shuffle` | `OrderBy(_ => random)` |
| Spatial noise, per-cell randomness or a scattered point | `Pcg3dLatticeNoise` (`ValueNoise01`, `ScatterPoint`) | A per-call RNG; a second copy of the block formula |
| A one-shot weighted pick | `WeightedSampler.SampleOnce` | A cumulative scan; a table built to be thrown away |
| A 64-bit mix with an inverse | `InvertibleBitMix.Mix64` (SplitMix64's finalizer) | A hand-rolled multiply-xorshift |
| An angle in degrees entering the sim | `FixedQ4816.FromDegrees` (one rounding against `PiQ189`) | `FromDouble(degrees * (Math.PI / 180))`, a rounded radians-per-degree factor |
| π, π/2, 2π, or an angle reduced to one turn | `FixedQ4816.Pi`/`HalfPi`/`Tau`, `FixedQ4816.WrapAngle` | `FromDouble(Math.PI)`, `Pi + Pi` (one raw short of `Tau`), a floor-and-correct wrap |
| A vector shortened to a length, or rejected from an axis | `FixedVector3.ClampLength`/`WithLength` (toward zero, never above), `RejectFrom`/`TryRejectNormalized` | `(v / v.Length) * limit`, which can land above the limit |
| A sphere or cone test | `FixedVector3.IsWithin` (exact `\|d\|² ≤ r²`), `IsWithinCone` (apex inside, normalized forward) | `LengthSquared > r * r` (rounded twice), a cone that rejects its apex |
| Spread points, or stratification that must be a theorem | `LowDiscrepancy` (R1, R2), `DigitalNetSampler` | Plain random scatter |
| A per-tick state hash for a replay probe | `Fnv1aHash` | `string.GetHashCode` or `HashCode.Combine` (randomly seeded per process) |
| Hex cells, tile or chunk order, rings | `HexagonalCoordinate`, `HilbertCurve`, `LayerSequence` | Hand-rolled axial math |
| Floor or ceiling division, low masks, alignment, PDEP/PEXT, Morton codes | `BinaryIntegerFunctions` (`FloorDivide`, `CeilingDivide`, `LowMask`, `AlignUp`, `ParallelBitDeposit`, `BitwisePair`) | `/` on a negative dividend, `(1 << n) - 1`, a `Bmi2` call |
| Exact GF(2^k), mod p, a primality decision | `BinaryField<T>`, `PrimeField64`, `PrimeExtensions.IsPrime` | Floats; a rounded product |
| The Nth prime or a prime count within `uint` | `PrimeExtensions.NthPrime(uint)` / `PrimeCountingFunction(uint)` | A second sieve or counting implementation |
| A graph, lattice, language or finite structure | The `Oracle/` presented algebra | A bespoke solver |

`FixedQ3232`, `FixedInterval`, `FixedMassProperties`,
`FixedSymmetricSolve`, `CurvatureSpline`, the transforms (NTT, Walsh-Hadamard,
fixed FFT and DCT) and the `Research/` wing are in the wing READMEs' "At a
glance" tables. [references/complete-reference.md](references/complete-reference.md)
maps each question to its wing and README section.

## Contracts that bite

- **Rate accumulators carry authoritative state.** The sub-unit remainder and
  `TicksPerSecond` ride snapshots and state hashes, restored together with
  `FromRemainder` / `FromRemainders`. Call `Reset` when the integrated quantity
  is assigned, clamped or teleported outside the accumulator. Both are mutable
  structs: keep one in a field, an array slot or a `ref` local. A `readonly`
  field, a get-only property or a `List<T>` element hands `Integrate` a copy,
  and every advance is silently lost.
- **RNG state is simulation state.** One `Pcg32XshRr` stream per system,
  derived from the master seed with a small consecutive id
  (`Create(state: masterSeed, stream: id)`); persist `State`, `Increment` and
  `Multiplier` and restore through `FromRawBits`. Never share a generator
  across systems, never reseed to "resume", and keep draw order stable.
- **Alias tables are order-sensitive.** Build once at load from
  deterministically ordered entries; entry order is part of the table's
  identity. A sample consumes exactly two generator advances.
- **Seeking counts advances, not calls.** `Advance`-based seeking is exact only
  against fixed-cost draws (`NextUInt32()`, the fraction draws, the Gaussian
  pair, an alias sample). A bounded `NextUInt32(min, max)` and `Shuffle` can
  reject and consume extra advances.
- **Wrap is the default.** Bare operators are unchecked, `checked` forms throw
  after rounding, and `AddSaturating` / `SubtractSaturating` (unsigned and unit
  types) or `FixedSaturate` (`FixedQ4816` and vectors) clamp. Some saturators
  have no `Try...` sibling. State the rounding and overflow policy at each
  narrowing boundary.
- **Ties go to even** everywhere except `Exp2`, `Log2` and `Atan2`, which
  narrow half up. Do not add a fourth exception or "correct" one of the three.
- **Do not reassociate a rounded product.** `(a * b) * c` and `a * (b * c)`
  differ over `FixedQ4816`; the fused kernels round a whole expression once.
  Finite-field products are exact and may be reassociated.
- **Float presentation helpers live in `VectorFunctions`.** The angle wraps,
  easings, shortest arc, −Z-forward attitude readbacks and unorm packers every
  presentation seam shares are in `Puck.Maths.VectorFunctions`, outside the
  determinism contract and in every project's closure; a second float copy in
  a client or shader-side file is a defect.
- **Floats stay out of state.** Authoring in (`FromDouble`, a document weight)
  and presentation out (`ToVector3`, `ToQuaternion`,
  `FixedPosition.ToRenderRelative`) are the two boundaries; presentation seams
  are one-way, and nothing they return flows back into state.
- **Outbound precision needs an exact oracle.** The `FixedQ4816` float cast rounds
  its raw directly to single precision before exact binary scaling; routing it
  through double can manufacture a tie. The decimal-backed `Half` conversion
  is correctly rounded at the current Q16/Q32 scales, pinned at every Half
  midpoint by `scalar.half-midpoints-vs-exact-oracle`; do not assume that proof covers
  a future finer carrier. Generic `FixedQ3232`/`UFixedQ4816` peers round to the
  target grid before applying checked, saturating or width-truncating policy.
- **Generic peers support both hooks.** Verify `TryConvertFrom*` and
  `TryConvertTo*` directly through the derived-interface adapter in the Maths
  suite. `Create*` falls back to the other operand's hook and can conceal a
  missing half of the conversion contract.
- **Gate `PDEP`/`PEXT` on `BitManipulation.HasFastParallelBits`**, never
  `Bmi2.IsSupported`: AMD before Zen 3 (the Steam Deck's Zen 2 included) and
  Hygon's licensed Zen 1 run them in microcode at up to hundreds of cycles.
- **Do not infer a contract from a name.** Read the member's XML documentation,
  its wing README section and the tests that pin it.
- **A deliberate correction moves values.** A rounding or logic fix is expected
  to change state hashes: make it, and re-record the persisted replay or
  baseline it invalidates (`AGENTS.md` rule 4). Never keep a path that
  reproduces the old wrong result.

## Prime kernels

Work on `PrimeExtensions.IsPrime`, `NthPrime(uint)`, `PrimeKernels` and
`ScaledResidueRing64` follows
[references/prime-kernels.md](references/prime-kernels.md). Preserve the fast
single-value decision and its SIMD fallbacks. Wide prime counting, selection and
interval exploration are out of scope (the owner's ruling,
[prime exploration](../../../docs/reference/prime-exploration.md));
`Research/`, `Algebra/` and `Oracle/` are unaffected.

## Verify

Build the test project (`dotnet build tests/Puck.Maths.Tests/Puck.Maths.Tests.csproj
-c Release -nodeReuse:false`), then run the suite, which takes about half a minute:

```text
dotnet test tests/Puck.Maths.Tests/Puck.Maths.Tests.csproj -c Release --no-build
```

Pass `-nodeReuse:false` to the build step only
([verification](../verification/SKILL.md#build-before-you-test)). The run is
the Default tier. A rounding change or a new value
kernel also earns Deep (`--explicit on --filter-trait tier=Deep`). Exhaustive
takes tens of minutes: run it only when the member's waiver or the coverage
law declaration names it as the gate of record, and narrow it to one law with
`--explicit on --filter-display-name '<law-id>*'`. No tier measures time;
`puck bench` does. Report the exact commands you ran and where any failure came
from.

A new public Maths member lands with its classification (a law case or a
precise waiver) in the same change, and CI requires 100% line coverage of live
`src/`, so new code lands with a test that reaches it. Authoring the case and waiver belongs to
[`maths-laws`](../maths-laws/SKILL.md). The owner rules out recorded Maths
registers and coverage ratchets; completeness is checked from the current declarations.

## Route adjacent work

| Skill | Use when |
|---|---|
| [`maths-laws`](../maths-laws/SKILL.md) | Authoring or changing a Maths law, subject, oracle, leg, waiver or public-member classification. |
| [`dotnet-performance`](../dotnet-performance/SKILL.md) | SIMD, allocation and throughput questions on code that is not a simulation value path. |
| [`rendering`](../rendering/SKILL.md) | Shaders, renderer or UI math and presentation-only floats, which sit outside the determinism contract. |
| [`content-search`](../content-search/SKILL.md) | Finding textual occurrences, candidate hand-rollings, tokens or patterns across the tree. |
| [`symbol-analysis`](../symbol-analysis/SKILL.md) | Semantic C# questions about references, implementers, dead code, renames or deletion safety. |
| [`gaming-bricks`](../gaming-bricks/SKILL.md) | Verifying a Maths change that reaches emulator code and its dedicated batteries. |

