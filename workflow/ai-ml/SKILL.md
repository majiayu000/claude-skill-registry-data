---




name: ai-ml
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
description: Implements intelligent ai ml with multi-factor skill selection, fallback
  chains, and adherence to the 5 Laws of Elegant Defense
license: MIT
maturity: stable
metadata:
  domain: agent
  output-format: analysis
  related-skills: agent-confidence-based-selector, agent-task-routing
  role: orchestration
  scope: orchestration
  triggers: ai-ml, ai ml, how do i ai-ml, orchestrate ai-ml, automate ai-ml, agent
    ai-ml
  archetypes:
  - orchestration
  - strategic
  anti_triggers:
  - brainstorming
  - vague ideation
  - single-agent monolith
  response_profile:
    verbosity: medium
    directive_strength: high
    abstraction_level: tactical
version: "1.0.0"




---




# Ai Ml

Orchestrates intelligent skill selection and execution for ai ml workflows. Applies the 5 Laws of Elegant Defense to guide data naturally through the orchestration pipeline, preventing errors before they occur. Selects optimal skills based on multi-factor scoring including text similarity, historical performance, and system availability.

## TL;DR Checklist

- [ ] Parse all inputs at boundary before processing (Law 2)
- [ ] Handle edge cases with early returns at function top (Law 1)
- [ ] Fail immediately with descriptive errors on invalid states (Law 4)
- [ ] Return new data structures, never mutate inputs (Law 3)
- [ ] Implement minimum 2-level fallback chain for all skill executions
- [ ] Log all skill selections with context for full audit trail
- [ ] Validate skill metadata and dependencies before selection
- [ ] Update confidence scores after each execution for learning


┌───────────────────────────────────────────────────────────────────────────────┐
│                              Orchestration Flow                                               │
└───────────────────────────────────────────────────────────────────────────────┘

  User Request
      ↓
┌─────────────────┐
│  Parse Request  │
│  & Extract      │
│  Features       │
└────────┬────────┘
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    Evaluate Available Skills                                │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Skill A      │  │ Skill B      │  │ Skill C      │              │
│  │ - Match Score│  │ - Match Score│  │ - Match Score│              │
│  │ - Confidence │  │ - Confidence │  │ - Confidence │              │
│  │ - History    │  │ - History    │  │ - History    │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                       │
│         └─────────────────┴─────────────────┘                       │
│                          ↓                                          │
│                   Select Best Skill                               │
└─────────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────┐
│  Execute Skill  │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Handle Result  │
└────────┬────────┘
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    Error Handling & Fallback                                  │
│                                                                     │
│  Success? ────────► Return Result                                  │
│                                                                     │
│  Fail? ────────┐                                                    │
│                ↓                                                    │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │               Fallback Chain                                    │      │
│  │                                                             │      │
│  │  1. Retry with adjusted parameters                          │      │
│  │  2. Try Alternative Skill (if available)                    │      │
│  │  3. Defer to Human Operator (if critical)                   │      │
│  │  4. Log & Return Error                                      │      │
│  └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘

## When to Use

Use this skill when:

- Orchestrating multi-step workflows that require skill delegation
- Implementing adaptive skill routing based on confidence scores
- Building fallback mechanisms for failed skill executions
- Creating intelligent task decomposition and parallel execution
- Designing skill dependency graphs with automatic resolution
- Implementing skill selection with historical performance weighting
- Building agent systems that need to self-organize around tasks

## When NOT to Use

Avoid this skill for:

- Direct task execution without orchestration needs - use individual skills instead
- High-frequency trading scenarios where latency must be minimized - the selection overhead may be prohibitive
- Simple linear workflows without branching or fallback requirements
- Cases where skill metadata is unavailable or unreliable


## Core Workflow

1. **Parse and Analyze Request** - Extract intent, entities, and constraints from user input.
   **Checkpoint:** All required parameters must be present and in valid format before proceeding.

2. **Score Available Skills** - Calculate match scores using multi-factor algorithm:
   - Text similarity between request and skill triggers
   - Historical success rate for similar tasks
   - Skill availability and health status
   - Required dependencies and their availability
   
   **Checkpoint:** Skip to fallback if no skill scores above threshold.

3. **Select Optimal Skill** - Choose skill with highest score that meets minimum confidence.
   **Checkpoint:** Verify skill has not been disabled or deprecated.

4. **Execute with Fallback** - Run skill execution wrapped in retry and fallback logic.
   **Checkpoint:** Log all execution attempts for audit trail.

5. **Return or Fallback** - Either return successful result or apply fallback chain:
   - Retry with adjusted parameters
   - Try alternative skill from `related-skills`
   - Defer to human operator for critical tasks
   
   **Checkpoint:** Record outcome with timing and confidence metadata.

## Implementation Patterns

### Pattern 1: Skill Selection Logic

```python
def select_ml_component(
    task_spec: Dict,
    model_registry: List[Dict],
    latency_budget_ms: int = 500
) -> Optional[Dict]:
    """Select optimal ML model/component based on task constraints and registry metadata.
    
    Evaluates models against input schema compatibility, historical accuracy,
    and compute latency requirements. Implements multi-factor scoring for
    intelligent routing in AI/ML pipelines.
    
    Args:
        task_spec: Dict containing input_schema, expected_output_type, and constraints
        model_registry: List of available model metadata with performance metrics
        latency_budget_ms: Maximum acceptable inference latency
        
    Returns:
        Selected model metadata dict or None if no model meets constraints
    """
    if not task_spec.get("input_schema") or not model_registry:
        raise ValueError("Task spec requires input_schema and non-empty model registry")
        
    best_model = None
    best_score = 0.0
    
    for model in model_registry:
        schema_match = _check_schema_compatibility(task_spec["input_schema"], model["input_schema"])
        latency_ok = model.get("estimated_latency_ms", 9999) <= latency_budget_ms
        
        if not schema_match or not latency_ok:
            continue
            
        accuracy_weight = model.get("last_30d_accuracy", 0.0) * 0.6
        latency_weight = max(0, (1.0 - (model["estimated_latency_ms"] / latency_budget_ms))) * 0.4
        composite_score = accuracy_weight + latency_weight
        
        if composite_score > best_score:
            best_score = composite_score
            best_model = model
            
    if best_model is None:
        return None
        
    return {**best_model, "routing_score": best_score, "selected_at": time.time()}
```


### Pattern 2: Execution with Fallback

```python
def run_ml_inference_with_degradation(
    model: Dict,
    input_data: Any,
    fallback_models: List[Dict],
    cache: Dict
) -> Dict:
    """Execute ML inference with graceful degradation and fallback routing.
    
    Implements the Fail Fast, Fail Loud principle for AI pipelines:
    - Validates input schema immediately before inference
    - Falls back to simpler models or cached predictions on failure
    - Returns structured results with confidence and degradation metadata
    
    Args:
        model: Primary model metadata and endpoint config
        input_data: Raw input payload for inference
        fallback_models: Ordered list of alternative models for degradation
        cache: In-memory or Redis cache for prediction storage
        
    Returns:
        Dict with prediction, confidence, fallback_used, and latency_ms
    """
    if not _validate_input_schema(input_data, model["input_schema"]):
        raise PipelineValidationError("Input schema mismatch for model " + model["name"])
        
    cache_key = hashlib.md5(json.dumps(input_data, sort_keys=True).encode()).hexdigest()
    if cache_key in cache:
        return {"prediction": cache[cache_key], "fallback_used": "cache", "latency_ms": 0}
        
    for candidate in [model] + fallback_models:
        try:
            raw_output = _call_inference_endpoint(candidate, input_data)
            confidence = _extract_confidence(raw_output)
            
            if confidence < 0.5:
                continue
                
            cache[cache_key] = raw_output
            return {
                "prediction": raw_output,
                "model_used": candidate["name"],
                "fallback_used": False,
                "confidence": confidence,
                "latency_ms": time.time() * 1000
            }
        except EndpointTimeoutError:
            continue
            
    raise PipelineExecutionError("All models and fallbacks exhausted for task")
```

### MUST DO
- Always validate skill metadata before selection (Early Exit)
- Implement fallback chain with at least 2 levels (Fallback Skill + Human)
- Log all skill selections with full context for auditability
- Return new data structures instead of mutating inputs (Atomic Predictability)
- Fail immediately with descriptive errors on invalid states
- Update confidence scores after each execution for adaptive routing
- Reference `code-philosophy` (5 Laws of Elegant Defense) in all logic


### MUST NOT DO
- Select skills based on a single factor (e.g., only confidence score)
- Disable fallback mechanisms "temporarily" - this creates fragile systems
- Skip validation of skill dependencies before execution
- Return partial results - either complete success or clear failure
- Use magic numbers for confidence thresholds - make them configurable
- Cache skill selections without considering context changes


## TL;DR Checklist

- [ ] Parse all inputs at boundary before processing (Law 2)
- [ ] Handle edge cases with early returns at function top (Law 1)
- [ ] Fail immediately with descriptive errors on invalid states (Law 4)
- [ ] Return new data structures, never mutate inputs (Law 3)
- [ ] Implement minimum 2-level fallback chain for all skill executions
- [ ] Log all skill selections with context for full audit trail
- [ ] Validate skill metadata and dependencies before selection
- [ ] Update confidence scores after each execution for learning


## TL;DR for Code Generation

- Use guard clauses - return early on invalid input before doing work
- Return simple types (dict, str, int, bool, list) - avoid complex nested objects
- Cyclomatic complexity < 10 per function - split anything larger
- Handle null/empty cases explicitly at function top (Early Exit)
- Never mutate input parameters - return new dicts/objects
- Fail fast with descriptive errors - don't try to "patch" bad data
- Reference code-philosophy laws in comments for complex logic
- Include timing and confidence metadata in all return values


## Output Template

When applying this skill, produce:

1. **Selected Skills** - List of skill names with confidence scores
2. **Selection Rationale** - Why each skill was chosen (match score, history, availability)
3. **Execution Plan** - Order of execution with dependencies
4. **Fallback Strategy** - Which fallback skills will be tried and in what order
5. **Risk Assessment** - Any potential failure points and their impact
6. **Timing Estimates** - Expected latency including fallback scenarios



---

---

## Constraints

### MUST DO
- Define clear input/output contracts for every step in the orchestration flow with explicit validation
- Implement structured logging at each stage capturing context, inputs, outputs, timing, and errors
- Build in fallback paths: if the primary strategy fails, degrade gracefully to a simpler approach
- Validate all preconditions before starting — do not proceed if required resources or permissions are missing

### MUST NOT DO
- Do not create deep nesting of orchestration steps (>5 levels) — flatten workflows where possible
- Avoid silent failure modes: every step must either succeed, fail explicitly, or escalate to a higher handler
- Never use shared mutable state between parallel workflow branches — communicate via immutable messages only
- Do not hardcode execution order when the dependency graph naturally determines it; derive order from explicit dependencies


## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [PyTorch Documentation](<https://pytorch.org/docs/>)
- [Scikit-learn User Guide](<https://scikit-learn.org/stable/user_guide.html>)
- [TensorFlow Official Docs](<https://www.tensorflow.org/guide>)
- [ML Pipeline Orchestration (MLOps)](<https://ml-ops.org/content/mlops-principles>)
- [arXiv ML Survey](<https://arxiv.org/list/cs.LR/recent>)

## Related Skills

| Skill | Purpose |
|