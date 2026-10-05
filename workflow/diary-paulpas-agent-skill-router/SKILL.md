---




name: diary
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
description: Implements intelligent diary with multi-factor skill selection, fallback
  chains, and adherence to the 5 Laws of Elegant Defense
license: MIT
maturity: stable
metadata:
  domain: agent
  output-format: analysis
  related-skills: agent-confidence-based-selector, agent-task-routing
  role: orchestration
  scope: orchestration
  triggers: diary, diary, how do i diary, orchestrate diary, automate diary, agent
    diary
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




# Diary

Orchestrates intelligent skill selection and execution for diary workflows. Applies the 5 Laws of Elegant Defense to guide data naturally through the orchestration pipeline, preventing errors before they occur. Selects optimal skills based on multi-factor scoring including text similarity, historical performance, and system availability.

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
def route_diary_request(
    user_input: str,
    current_time: datetime,
    available_diary_skills: List[Dict],
    min_confidence: float = 0.75
) -> Optional[Dict]:
    """Route a diary request to the optimal skill based on intent and context.
    
    Parses natural language diary inputs, extracts temporal entities,
    and matches against registered diary capabilities (create, query, modify, sync).
    """
    if not user_input or not user_input.strip():
        raise ValueError("Diary input cannot be empty")
        
    # Extract temporal and action features specific to diary workflows
    parsed_intent = _parse_diary_intent(user_input)
    temporal_context = _extract_temporal_markers(parsed_intent, current_time)
    
    best_match = None
    best_score = 0.0
    
    for skill in available_diary_skills:
        # Domain-specific scoring: prioritize temporal alignment and action match
        action_match = _calculate_action_similarity(parsed_intent["action"], skill["triggers"])
        temporal_match = _calculate_temporal_relevance(temporal_context, skill.get("temporal_scope", "any"))
        history_weight = skill.get("success_rate", 0.5) * 0.2
        
        score = (action_match * 0.5) + (temporal_match * 0.3) + (history_weight * 0.2)
        
        if score > best_score and score >= min_confidence:
            best_score = score
            best_match = skill
            
    if best_match is None:
        return None
        
    # Return immutable result with routing metadata
    return {
        "skill": best_match["name"],
        "parameters": _prepare_diary_params(parsed_intent, temporal_context),
        "confidence": best_score,
        "routing_timestamp": current_time.isoformat()
    }
```


### Pattern 2: Execution with Fallback

```python
def execute_diary_workflow(
    routing_result: Dict,
    user_context: Dict,
    diary_storage: DiaryBackend,
    max_retries: int = 2
) -> Dict:
    """Execute diary operations with domain-specific fallback chains.
    
    Handles diary entry creation, modification, or retrieval with
    resilience against storage timeouts, sync conflicts, and API limits.
    """
    skill_name = routing_result["skill"]
    params = routing_result["parameters"]
    
    # Validate diary entry constraints before execution
    if not _validate_diary_entry(params):
        raise DiaryValidationError("Entry violates temporal or content constraints")
        
    for attempt in range(max_retries + 1):
        try:
            if skill_name == "create_entry":
                result = diary_storage.create_entry(params, user_context["user_id"])
            elif skill_name == "query_history":
                result = diary_storage.query_entries(params["date_range"], user_context["user_id"])
            elif skill_name == "sync_calendar":
                result = diary_storage.sync_with_external_calendar(params, user_context["oauth_token"])
            else:
                raise ValueError(f"Unsupported diary skill: {skill_name}")
                
            return {
                "status": "success",
                "skill": skill_name,
                "data": result,
                "attempts": attempt + 1,
                "timestamp": datetime.now().isoformat()
            }
            
        except StorageTimeoutError:
            if attempt < max_retries:
                continue # Retry with exponential backoff
            # Fallback: Queue for async processing or notify user
            return _handle_diary_fallback(skill_name, params, user_context)
            
        except SyncConflictError as e:
            # Domain-specific conflict resolution
            return _resolve_diary_conflict(e, params, user_context)
            
    raise DiaryExecutionError(f"Failed to process diary request after {max_retries + 1} attempts")
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

- [Zettelkasten Method (Wikipedia)](<https://en.wikipedia.org/wiki/Zettelkasten>)
- [Bullet Journal Method (Ryder Carroll)](<https://bulletjournal.com/>)
- [GTD Getting Things Done Method](<https://www.agilealliance.org/glossary/getting-things-done/>)
- [Personal Knowledge Management Systems](<https://en.wikipedia.org/wiki/Personal_knowledge_management>)
- [Obsidian Help Documentation](<https://help.obsidian.md/>)

## Related Skills

| Skill | Purpose |
|