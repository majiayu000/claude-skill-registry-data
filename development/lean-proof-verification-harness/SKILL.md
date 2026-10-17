---
name: lean-proof-verification-harness
description: Formal theorem proving, tactic validation, and invariant verification harness for Lean 4 and agent logic specs.
compatibility: node >= 18, typescript >= 5.0, optional lean4 toolchain
---

# Lean Proof Verification Harness

Executes formal verification on Lean 4 source files, theorem declarations, and state invariant proofs.

See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md) for shared operating requirements.

## Inputs & Outputs

### Input Schema

| Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `source` | `string` | **Yes** | Inline Lean 4 source code or path to `.lean` file |
| `strict` | `boolean` | No | Fail verification if `sorry` or unverified axioms exist (default: `true`) |
| `targetTheorem` | `string` | No | Target specific theorem/lemma name to verify |
| `routingTier` | `string` | No | Cost-routing gateway tier for proof tactic synthesis (default: `tier_2_frontier`) |

### Output Schema

```json
{
  "status": "VERIFIED | OPEN_OBLIGATIONS | FAILED",
  "theoremsFound": 3,
  "theoremsVerified": 3,
  "sorryCount": 0,
  "axiomsUsed": ["propext"],
  "diagnostics": [],
  "verificationDurationMs": 142
}
```

## Verification Pipeline

1. **Syntax & AST Analysis**: Extracts theorem signatures, tactic blocks (`by ...`), definitions, structures, and axioms.
2. **Obligation Auditing**: Audits proof bodies for `sorry`, `admit`, uninstantiated hypotheses, and ungrounded axioms.
3. **Compiler Integration**: Runs `lean --run` or `lake build` when Lean 4 toolchain is installed; executes deterministic AST invariant analysis when running in standalone mode.
4. **Frontier Proof Synthesis**: Routes unproven lemmas to the Multi-Model Cost-Routing Gateway on `tier_2_frontier` for tactic generation.
