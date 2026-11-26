---
name: quantum-affine-lookup-synthesis
description: Lower Toffoli cost in a repeated small reversible XOR lookup or modular squarer by sharing nonlinear terms across outputs, testing affine basis changes and proving arbitrary-target behavior before measuring the full circuit.
---

# Spickzettel (quantum-affine-lookup-synthesis)

*Synthesize the lookup in the caller's frame*

Extract the actual address-to-word table, caller guard, scratch assumptions and observed call multiplicities from the frozen source. Record output bit ordering, legal address domain and behavior for unused encodings. The contract of an XOR lookup is `(a,t) → (a,t XOR F(a))` for arbitrary incoming `t`.

1. For an address bit `x`, let `F0` and `F1` be **word-valued** cofactors and `D=F0 XOR F1`. Price Shannon selection, positive Davio `F0 XOR (x AND D)`, and negative Davio `F1 XOR ((NOT x) AND D)`. Share reusable terms across output columns. Include creating, controlling and uncomputing each helper. Try invertible linear output coordinates where they expose identical terms. For a basis `L`, the target enters as `L(t)`, receives `L(F(a))`, and leaves through `L⁻¹`.
2. For a modular squarer on canonical residues modulo an odd prime, `x` and `p−x` have equal squares. Explore a half-table only if the address fold, zero case, garbage removal and restored original address all fit the width and price. Specify behavior on noncanonical inputs whenever the source admits them.
3. Exhaust the addresses at each emitted table size and verify address, target, phase and borrowed workspace. Checking target zero and the single-bit target vectors proves arbitrary-target correctness **only after** establishing the map is affine in the incoming target at each address. If a target can influence a nonlinear control, prove the restriction, exhaust targets, or use equivalence checking. Test disabled guards, inverse direction and bit/basis adapters.
4. Recompile in the actual caller, rebase insertion spans and inverse spans on the exact parent, and price the combined build. Count printed gates, compiled CCX and executed Toffolis independently. Remeasure call multiplicities after other rewrites. In paired panels retain failure IDs and passing-state digests. Test the emitted stream's own benchmark draw separately.

See [Boolean expansions](https://arxiv.org/abs/2601.02515), [vector multiplicative complexity](https://arxiv.org/abs/1407.6169) and [exact multiplicative complexity](https://arxiv.org/abs/2005.01778).
