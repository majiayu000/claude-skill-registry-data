---
name: quantum-guarded-permutation-audit
description: Find wrong-branch swaps and stale stream caches when a chunked reversible-circuit optimizer changes native endpoints. Use for deferred wire permutations, nested classical guards, or two nominally equivalent builds that disagree.
---

# Hüetlispiler (quantum-guarded-permutation-audit)

*Audit deferred swaps across guarded chunks*

An eliminated SWAP leaves a permutation of physical wires. Record the guard under which the swap executed. Every subsequent quantum operand must use the correct map, and any physical operation that settles the permutation must execute on exactly those branches that owe it.

## Smallest failing program

Start with `(q0,q1)=(1,0)`. Emit `CX 0 1; CX 1 0; CX 0 1; PUSH c` and end the chunk. Leave the matching POP to the next chunk. The source exchanges the bits for **both** values of `c`. A pass that appends three restoring CXs after the PUSH returns `(1,0)` when `c=0`. A trial with equal input bits or only `c=1` hides the defect.

1. Freeze the raw input, actual chunk boundaries, pass order and emitted bytes. Locate the first differing boundary and then the first differing pass. Compare in the same physical wire frame, including the ambient classical stack.
2. Reverse-scan the chunk. Count locally available POPs and match each to the nearest preceding PUSH. For a PUSH whose POP is in a later chunk, settle any outstanding outer permutation immediately before entering it. Settle a scope's own permutation before popping it. A locally balanced nested scope may still optimize if the implementation preserves the maps on entry and exit.
3. Exercise all four data states and both guard values. Extend to nested true/false guards, chunks starting inside a guard, and a POP closing an incoming scope. Compare the complete live state, classical stack and phase. Couple shared measurement draws by original event identity for diagnosis and reserve distinct draws for new events. Run the ordinary native evaluator with its own prescribed randomness for qualification.
4. If a cold evaluation and a warm replay disagree, key the prefix cache on the full stream content, evaluator format/version and the inputs that determine the prefix. Include the header and hash domain where either sets the draw or wire width. Forge a control with different bytes, equal length and equal file timestamp. Both warm results must reproduce their respective cold results.

Report the smallest input, chunk span and branch causing the discrepancy, raw and pass hashes, and the first differing state. Remeasure cost only on the repaired pipeline. A local campaign test found the old pass wrong on 123,196 of 768,000 small circuit/input combinations. The four-row witness explains the failure independently of that sample.

For the underlying register-permutation semantics, see [Hietala et al.](https://arxiv.org/abs/1912.02250).
