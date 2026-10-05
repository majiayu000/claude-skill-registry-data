---




name: build
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
description: Implements intelligent build with multi-factor skill selection, fallback
  chains, and adherence to the 5 Laws of Elegant Defense
license: MIT
maturity: stable
metadata:
  domain: agent
  output-format: analysis
  related-skills: agent-confidence-based-selector, agent-task-routing
  role: orchestration
  scope: orchestration
  triggers: build, build, how do i build, orchestrate build, automate build, agent
    build
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




# Build

Orchestrates intelligent skill selection and execution for build workflows. Applies the 5 Laws of Elegant Defense to guide data naturally through the orchestration pipeline, preventing errors before they occur. Selects optimal skills based on multi-factor scoring including text similarity, historical performance, and system availability.

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
def select_build_tool(
    project_root: str,
    available_build_systems: List[str],
    build_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Select optimal build tool based on project structure and configuration.
    
    Evaluates project files (Makefile, CMakeLists.txt, package.json, etc.)
    against available build systems to determine the most efficient runner.
    Applies multi-factor scoring: file presence, dependency graph complexity,
    and historical build success rates.
    """
    if not os.path.isdir(project_root):
        raise ValueError(f"Project root not found: {project_root}")
        
    project_files = os.listdir(project_root)
    scoring = {}
    
    for tool in available_build_systems:
        score = 0.0
        if tool == "make" and "Makefile" in project_files:
            score += 0.4
        elif tool == "cmake" and "CMakeLists.txt" in project_files:
            score += 0.4
        elif tool == "npm" and "package.json" in project_files:
            score += 0.3
        elif tool == "bazel" and "BUILD" in project_files:
            score += 0.5
            
        # Factor in build config overrides
        if build_config.get("preferred_tool") == tool:
            score += 0.2
            
        # Factor in historical success rate
        score += build_config.get("historical_success", {}).get(tool, 0.0) * 0.4
        scoring[tool] = score
        
    best_tool = max(scoring, key=scoring.get)
    if scoring[best_tool] < 0.5:
        return {"tool": None, "reason": "insufficient_match"}
        
    return {
        "tool": best_tool,
        "confidence": scoring[best_tool],
        "config_path": os.path.join(project_root, f"{best_tool}.config.yaml"),
        "timestamp": time.time()
    }
```


### Pattern 2: Execution with Fallback

```python
def execute_build_pipeline(
    build_spec: Dict[str, Any],
    project_root: str,
    fallback_targets: List[str] = None
) -> Dict[str, Any]:
    """Execute build pipeline with domain-specific fallback handling.
    
    Runs the selected build tool, monitors output for common failure modes
    (dependency resolution, compilation errors, cache misses), and applies
    targeted fallbacks without breaking the build contract.
    """
    if fallback_targets is None:
        fallback_targets = ["clean_build", "cached_artifacts", "manual_review"]
        
    build_cmd = build_spec.get("command", f"{build_spec['tool']} build")
    env_vars = {**os.environ, "BUILD_ROOT": project_root}
    
    for attempt in range(3):
        try:
            result = subprocess.run(
                build_cmd.split(),
                cwd=project_root,
                env=env_vars,
                capture_output=True,
                text=True,
                timeout=build_spec.get("timeout", 300)
            )
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "artifacts": _scan_artifacts(project_root),
                    "stdout": result.stdout[-500:],
                    "attempts": attempt + 1
                }
                
        except subprocess.TimeoutExpired:
            logger.warning(f"Build timed out on attempt {attempt + 1}")
            continue
        except FileNotFoundError:
            # Tool missing, trigger fallback chain
            return _apply_build_fallback(build_spec, fallback_targets)
            
    # All attempts failed - escalate to fallback
    return _apply_build_fallback(build_spec, fallback_targets)
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


## Related Skills

| Skill | Purpose |
|---|---|
| `commit` | Source control commit workflows |

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

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Wikipedia — Build Automation](https://en.wikipedia.org/wiki/Build_automation)
- [GNU Make Manual](https://www.gnu.org/software/make/manual/make.html)
- [GitHub Actions — Build & CI/CD Pipeline Examples](https://docs.github.com/en/actions/use-cases-and-examples/building)
- [Apache Maven — Build Automation Guide](https://maven.apache.org/guides/index.html)