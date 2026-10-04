---
name: dspy-program-security
description: Review a DSPy application for unsafe signature design, optimizer dataset leakage, prompt-program boundary failures, weak typed output enforcement, and insecure tool-wrapper behavior.
last_reviewed: 2026-04-27
---

# DSPy Program Security

## First Principle

**DSPy compiles your examples into prompts. The security of your compiled program is only as strong as the security of your training data.**

DSPy's optimizer (teleprompter) takes examples you provide and compiles them into prompt instructions and few-shot demonstrations. This is a powerful capability — and a new attack surface. If attacker-influenced content reaches your optimizer dataset, it can be compiled into the prompt program and persist across all future invocations of that program. Unlike a one-shot injection, a compiled-in injection survives every deployment of the program until the program is recompiled without the poisoned examples. DSPy moves security left: the threat is not just in the runtime prompt, it is in the training pipeline.

Read the base [core-llm-prompt-security/SKILL.md](../core-llm-prompt-security/SKILL.md) first for the shared prompt and output controls. This skill narrows the controls to concrete DSPy review points.

## Framework Focus

- `Signature` definitions, modules, adapters, and prompt-program composition
- Optimizers and teleprompters including training and evaluation example sets
- Tool wrappers, retrieval modules, and evaluation pipelines

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Optimizer datasets, compiled prompts, module inputs, evaluator examples, and tool-wrapper arguments are all validated before they influence program behavior or tool execution. |
| **Scope** | Each DSPy module can access only the tools, retrieval paths, and context it strictly requires for its signature. Broad global tool exposure is not permitted. |
| **Isolate** | A poisoned optimizer dataset or injected module input cannot silently propagate into compiled programs or privileged tool execution paths. |
| **Enforce** | Typed signatures, schema validation, curated optimizer datasets, and explicit tool policies are the deterministic enforcement layer. |

## DSP.1 Prompt Program and Optimizer Boundary Review

**The DSPy-specific risk:** Optimizer datasets that contain instruction-bearing text, adversarial few-shot examples, or production user content without sanitization can embed that content into the compiled program — where it influences every future invocation, not just the session in which it was introduced.

### Check

- Are optimizer and teleprompter datasets sourced, sanitized, and approved through a controlled data pipeline — or are they assembled from raw production logs, user interactions, or retrieved documents without review?
- Does any optimizer dataset contain instruction-bearing phrases, policy override text, or content that could become hidden control logic when compiled into the prompt program?
- Are compiled prompt programs versioned, reviewed, and treated as production artifacts with the same controls as model weights?

### Action

- **Establish a dataset curation pipeline for optimization.** Every example that enters an optimizer dataset must pass through:
  1. Source validation: is this from an approved, controlled source?
  2. Instruction pattern scan: does the example contain directive phrases that could become control logic when compiled?
  3. PII and secret scan: does the example contain sensitive content that would persist in the compiled program?
  4. Human or automated review: has an authorized team member approved this example for training use?

```python
def validate_optimizer_example(example: dspy.Example) -> bool:
    if injection_filter.contains_directive(example.context or ""):
        raise DatasetPoisoningError(f"Instruction-bearing text in example: {example}")
    if pii_scanner.contains_pii(example.context or ""):
        raise SensitiveDataError(f"PII in optimizer example: {example}")
    return True

safe_examples = [ex for ex in candidate_examples if validate_optimizer_example(ex)]
```

- **Separate optimization datasets from live user content.** Never use raw production interactions as optimizer training data without explicit sanitization, redaction, and approval. Create a separate, curated dataset pipeline that is disconnected from the production data path.
- **Version and review compiled programs.** Treat compiled DSPy program artifacts (exported JSON or prompt files) as versioned assets. Review them before deployment — specifically: do the compiled few-shot examples contain any content that should not appear in production prompts?
- **Scope retrieval modules and subprogram context.** Each DSPy module's `dspy.Retrieve` or equivalent should be scoped to the minimum required data for that signature's task, not the full retrieval index.

### Failure Modes

- A developer uses recent user interactions as teleprompter training data without sanitization. One user had injected `Ignore previous instructions` in their message. This phrase is now compiled into the program's few-shot demonstrations.
- A compiled program is exported, shared, and deployed without review. It contains PII from a test user's interaction that was used as a training example.
- Module composition passes the full planner output to a sub-signature as context. The planner output was influenced by an injection. The sub-signature follows the injected instruction.

## DSP.2 Typed Output and Tool Wrapper Enforcement

**The DSPy-specific risk:** DSPy's type-annotated signatures define expected output fields, but enforcement requires that the application validates parsed output — not just that the signature declares the type. Tool wrappers in DSPy are Python functions; if they accept model-produced arguments without schema validation, they are argument injection surfaces.

### Check

- Is every DSPy module output that drives code, tools, or business logic validated outside the model layer — by deterministic code, not by trusting the signature annotation alone?
- Do tool wrappers validate their arguments before execution, and are they scoped to the minimum permissions needed for the module's task?
- Are module-level tool access boundaries defined — or does every module have access to a global tool set?

### Action

- **Enforce typed output parsing for every consequential module.** Parse the module's output fields with a strict validator and treat parse failures as security events:

```python
class AnalysisResult(BaseModel):
    summary: str
    action: Literal["approve", "reject", "escalate"]  # strict enum
    confidence: float                                   # 0.0–1.0

# After DSPy module call:
raw_output = analysis_module(input=user_request)
try:
    result = AnalysisResult.model_validate({"summary": raw_output.summary, "action": raw_output.action, "confidence": raw_output.confidence})
except ValidationError as e:
    log_security_event("dspy_output_schema_violation", error=e, module="analysis")
    raise
```

- **Validate tool wrapper arguments.** Every tool wrapper must validate its input arguments against a typed schema before executing. Use the same schema validation approach as for direct tool use.
- **Per-module tool allowlists.** Define which tools each DSPy module may call. Pass only the relevant subset of tools when constructing module context. Modules that do analysis should not have access to write or delete tools.

### Minimum Deliverable Per Review

- [ ] DSPy program graph: modules, signatures, optimizers, evaluators, and tool wrappers with their input/output types
- [ ] Optimizer dataset curation pipeline: source, validation steps, and approval workflow
- [ ] Compiled program review: contents inspected before deployment
- [ ] Typed output validation: enforcement point per module whose output drives actions
- [ ] Tool wrapper scope: per-module allowlists and argument validation

## Quick Win

**Audit your optimizer dataset source.** Ask: where did every example in this dataset come from? If the answer is "production logs" without sanitization, or "user interactions" without review — stop and implement a curation pipeline before running the next optimization pass. Compiled injections are harder to find and fix than runtime injections.

## References

- Shared prompt and output controls → [core-llm-prompt-security/SKILL.md](../core-llm-prompt-security/SKILL.md)
- Wrapper and action-policy hardening → [tool-use-execution-security/SKILL.md](../tool-use-execution-security/SKILL.md)
- Framework notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
