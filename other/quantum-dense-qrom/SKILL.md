---
name: quantum-dense-qrom
description: "Evaluate dense Pauli-encoded QROM and packetized lookup as a structural replacement for material coherent table lookup costs."
---

# Sardinebüchs (quantum-dense-qrom)

Change how table information is loaded and read. Read [dense-encoding QROM](references/paper.md).

Read the [shared contract](../quantum-structural-lanes/references/lane-contract.md) before a trial. Start with the five-line post; the shared native-test order, stop rules and promotion gate apply.

## Practical lane
First prove lookup is actually present in the scored path. Record table entries N, output bits b, address split, allowed gates, dirty workspace D and current lookup/use/unlookup cost. A classically supplied addend has no automatic lookup saving.

First experiment: implement the elementary two-entry read on a small channel/unitary model with a superposed address and a dirty qubit entangled with a spectator. Compare the complete operation to XOR lookup tensor identity. Include nonzero output targets and both Pauli choices. Preserve the true inverse of the load: changing inverse order can introduce a phase error.

Only then emit the complete table lookup with finite-size accounting. Compare the existing implementation, dense encoding and dense encoding plus packets under the same workspace cap. Include row selection, controls, output basis changes, padded rows, unload and the consumer boundary. Use a local name such as `block_rows` instead of confusing the paper's lambda with a board failure parameter.

## Structural extension
Co-design the table interface with a consumer that remains in a useful representation. Any removal of lookup cleanup needs its own correctness proof. Dirty workspace must be available during the whole borrow interval, not merely elsewhere in the circuit.

Stop if the evaluator cannot represent the needed operation stream, no usable table is in the objective, finite overhead dominates, or workspace raises global Q enough to erase the gain. Classical basis-only testing cannot validate this encoding. Deliver actual table shape, emitted resource curve across feasible block/packet choices, identity-on-borrowed-state evidence and whole-path result.
