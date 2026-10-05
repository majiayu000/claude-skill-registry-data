---
name: robust-testing
description: |
  Guidelines and strategies for constructing meaningful test suites, property-based tests, metamorphic relations, and fuzzing harnesses.
  Trigger when:
  - Designing verification bounds, writing tests, creating test invariants, or implementing validation gates.
  - Prompt contains: testing, test design, property-based testing, PBT, metamorphic testing, fuzzing, integration tests, E2E.
---

# Robust Testing & Verification Invariants

Guidelines for designing deterministic verification boundaries ($V(\mathbf{S})$). This skill instructs the agent on how to move beyond simple input-output example tests to construct property-based, metamorphic, and fuzz-testing harnesses that prevent regression and self-deception in generated code.

---

## 1. Core Philosophy

Traditional unit testing asserts that specific hardcoded inputs produce specific outputs. For AI-generated code, this example-based approach creates a **self-deception loop**: the agent generates both the implementation and the tests, propagating the same logical blind spots to both files.

To establish a mathematically sound validation boundary, you must verify the code against **properties and invariants** rather than static examples. A program is verified when its state transition satisfies high-level algebraic equations across a randomized input space.

### Iterative Refinement of Verification Boundaries ("Testing the Tests")
Because there is no deterministic validator to "test the test," the test suite must be converged and refined with the same rigor as the implementation:
* **Specification Traceability:** Every test case must explicitly trace to a constraint in the specification or state-space model.
* **Non-Trivial Failure Validation:** The baseline check is absolute: a test suite that passes on empty or unimplemented code ($\Delta E\_0 = 0$) is invalid.
* **Input Domain Scrutiny:** Generators must be audited to verify they generate the complete phase-space of input variables, explicitly including edge states (null, negative, empty structures, maximum limits).

---

## 2. Selection & Execution Rules

When executing the closed-loop optimization cycle, select verification methods based on the task domain:

* **Formal Specification Active:** Tests MUST trace directly to specification invariants, achieving 100% assertion coverage of normative constraints.
* **Algebraic Invariants Present:** If the domain exhibits algebraic properties (isomorphism, commutativity, etc.) and the target language has mature PBT support, Property-Based Testing (PBT) **MUST** be the primary validation gate.
* **Untrusted or Complex Input Boundaries:** If the program parses custom protocols, processes serialization formats, or handles external network payloads, Fuzz Testing **MUST** be applied to stress-test the boundary.
* **Oracle-Less Systems:** If the expected outputs are complex or computationally expensive to calculate (e.g., optimization routines, matrix operations), Metamorphic Testing **MUST** be used to assert functional relations across perturbed inputs.

---

## 3. Property-Based Testing (PBT)

Property-Based Testing validates that high-level code invariants hold true across a wide, randomized range of inputs. If a failure occurs, the framework automatically simplifies (shrinks) the input to locate the minimal reproducing case.

### The Prompts-to-Properties Workflow
1. **Property extraction:** Before generating implementation files, extract the core mathematical properties or algebraic invariants from the specification.
2. **Test formulation:** Define the input generator (e.g., using Python's `hypothesis` or Rust's `proftest`) and assert the invariant rules.
3. **Execution & shrinking:** Run the tests. If the test fails, feed the minimized counterexample back into the execution context for correction.

### Standard PBT Invariant Patterns
* **Round-trip (Isomorphism):** Applying a transform and its inverse returns the original state.
  $$\text{decode}(\text{encode}(x)) == x$$
* **Commutativity:** Reordering operations yields the same result.
  $$f(g(x)) == g(f(x))$$
* **Idempotency:** Repeated application yields the same result as a single application.
  $$f(f(x)) == f(x)$$
* **Monotonicity:** Increasing the size of the input monotonically shifts the output metric.
  $$\text{size}(x) > \text{size}(y) \implies \text{metric}(f(x)) \ge \text{metric}(f(y))$$

---

## 4. Metamorphic Testing (MT)

Metamorphic Testing addresses the **oracle problem** (cases where the correct output is unknown or computationally expensive to calculate). It checks whether the relationship between multiple inputs and their outputs matches a defined Metamorphic Relation (MR).

### Metamorphic Relation Classes

| Class | Input Transformation ($x \to x'$) | Metamorphic Relation ($f(x) \sim f(x')$) | Core Application |
| :--- | :--- | :--- | :--- |
| **Permutation** | Shuffle elements or arguments | $f(x) == f(x')$ | Sorting algorithms, search queries, database joins |
| **Scaling** | Multiply numeric inputs by factor $c$ | $f(c \cdot x) == c \cdot f(x)$ | Numerical algorithms, graphic coordinate math |
| **Monotonicity** | Add search filters / constraints | $|f(x)| \ge |f(x')|$ | Search engines, recommendation engines |
| **Invariance** | Paraphrase documentation or string formatting | $f(x) == f(x')$ | Prompt parsers, natural language models |

If a generated code piece is correct, it will maintain these semantic consistencies across input transformations. If it contains a logical defect, it will fail metamorphic consistency.

---

## 5. Fuzzing & Security Boundaries

Fuzzing bombards a program with randomized, structured, or mutated inputs to locate edge-case crashes, memory safety bugs, or infinite loops.

* **Fuzzing untrusted boundaries:** Write fuzzing harnesses whenever a module accepts external data, parses custom protocols, or manages state transitions from untrusted inputs.
* **LLM-assisted fuzzing:** Use LLMs to generate high-fidelity input generators or fuzzing harnesses. LLMs are highly effective at outputting syntactically valid but semantically unusual structures (such as malformed ASTs or SQL schemas) to stress-test compiler parsers.

---

## 6. Integration and End-to-End (E2E) Testing

Verifying units in isolation is insufficient; complex systems exhibit emergent errors at module boundaries.

### Integration Testing
Verify the interfaces and state transitions between decoupled modules:
* **Boundary Invariants:** Assert that data passed between modules conforms to interface contracts and types.
* **State Transition Verifications:** Validate that sequential operations across multiple modules (e.g., database writes followed by cache updates) transition the global state machine correctly.

### End-to-End (E2E) Testing
Simulate the complete execution trajectory under realistic scenarios:
* **System Liveness and Safety:** Verify that the system reaches its final state (liveness) without entering blocked or invalid configurations (safety).
* **Deterministic Mocks:** Mock external network APIs and hardware dependencies with deterministic stubs to keep the E2E verification loop fast and reproducible.

---

## 7. Hierarchical Verification Design

Structure your test suites in a hierarchy of increasing integration complexity:

```
[ Tier 1: Compiler & Linter Gates ]
       │
       ▼
[ Tier 2: Example-Based Happy Path Unit Tests ]
       │  (Verifies basic execution)
       ▼
[ Tier 3: Property-Based Verification (Invariants) ]
       │  (Runs randomized inputs to find edge-case logical bugs)
       ▼
[ Tier 4: Integration and End-to-End (E2E) Testing ]
       │  (Verifies module interfaces and global system liveness)
       ▼
[ Tier 5: Differential / Metamorphic Assertions ]
       │  (Verifies semantic consistency across implementations)
```

1. **Keep example tests brief:** Use example-based unit tests strictly to verify the happy path and basic syntax execution.
2. **Isolate test roles:** When writing tests, do not let the agent write example-based unit tests for its own code. Enforce PBT or metamorphic constraints to verify behaviors independently.
3. **Capture minimized inputs:** When a property test fails, document the minimal counterexample in the execution log. Use this minimized state as the target for debugging.
