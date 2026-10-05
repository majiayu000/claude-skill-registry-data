---




name: issues
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
description: Implements intelligent issues with multi-factor skill selection, fallback
  chains, and adherence to the 5 Laws of Elegant Defense
license: MIT
maturity: stable
metadata:
  domain: agent
  output-format: analysis
  related-skills: agent-confidence-based-selector, agent-task-routing
  role: orchestration
  scope: orchestration
  triggers: issues, issues, how do i issues, orchestrate issues, automate issues,
    agent issues
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




# Issues

Orchestrates intelligent skill selection and execution for issues workflows. Applies the 5 Laws of Elegant Defense to guide data naturally through the orchestration pipeline, preventing errors before they occur. Selects optimal skills based on multi-factor scoring including text similarity, historical performance, and system availability.

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
def triage_issue_request(
    issue_context: Dict[str, Any],
    routing_rules: List[Dict[str, Any]],
    min_confidence: float = 0.75
) -> Optional[Dict[str, Any]]:
    """Route an incoming issue to the appropriate handling skill.
    
    Analyzes issue metadata, title, and body to determine intent.
    Matches against routing rules using keyword extraction and priority scoring.
    Implements Law 2: Parse at boundary, make illegal states unrepresentable.
    """
    if not issue_context.get("title") or not issue_context.get("body"):
        raise ValueError("Issue must contain title and body for triage")
        
    title = issue_context["title"].lower()
    body = issue_context["body"].lower()
    combined_text = f"{title} {body}"
    
    # Extract intent signals
    intent_signals = {
        "bug": bool(re.search(r"error|crash|fail|broken|issue", combined_text)),
        "feature": bool(re.search(r"request|add|implement|enhancement|suggestion", combined_text)),
        "docs": bool(re.search(r"doc|guide|how to|explain|clarify", combined_text)),
        "config": bool(re.search(r"config|setup|env|variable|permission", combined_text))
    }
    
    best_match = None
    best_score = 0.0
    
    for rule in routing_rules:
        score = 0.0
        for keyword in rule.get("keywords", []):
            if keyword.lower() in combined_text:
                score += rule.get("weight", 1.0)
        
        # Boost score if intent signals match rule type
        rule_type = rule.get("type")
        if rule_type in intent_signals and intent_signals[rule_type]:
            score += 2.0
            
        if score > best_score and score >= min_confidence:
            best_score = score
            best_match = rule
            
    if best_match is None:
        return None
        
    # Return immutable routing decision
    return {
        "routed_skill": best_match["skill_id"],
        "confidence": best_score,
        "extracted_labels": [k for k, v in intent_signals.items() if v],
        "priority": best_match.get("priority", "normal")
    }
```


### Pattern 2: Execution with Fallback

```python
def execute_issue_workflow(
    issue_id: str,
    routing_decision: Dict[str, Any],
    issue_handler: Callable,
    fallback_queue: List[str]
) -> Dict[str, Any]:
    """Execute the assigned skill against the issue with domain-specific fallbacks.
    
    Handles issue state transitions, API interactions, and untriaged fallbacks.
    Implements Law 4: Fail fast on invalid issue states, fail loud on API errors.
    """
    if not issue_id or not routing_decision:
        raise ValueError("Issue ID and routing decision are required")
        
    skill_id = routing_decision["routed_skill"]
    labels = routing_decision.get("extracted_labels", [])
    
    try:
        # Apply skill to issue (e.g., update labels, assign, comment)
        result = issue_handler(
            issue_id=issue_id,
            skill_id=skill_id,
            labels=labels,
            priority=routing_decision.get("priority", "normal")
        )
        
        return {
            "status": "resolved",
            "issue_id": issue_id,
            "skill_applied": skill_id,
            "action_taken": result.get("action"),
            "timestamp": time.time()
        }
        
    except RateLimitError:
        # Fallback 1: Queue for retry with exponential backoff
        fallback_queue.append(issue_id)
        return {
            "status": "queued",
            "issue_id": issue_id,
            "reason": "rate_limited",
            "retry_after": 60
        }
        
    except MissingInfoError as e:
        # Fallback 2: Request clarification instead of failing silently
        return {
            "status": "awaiting_response",
            "issue_id": issue_id,
            "reason": "missing_info",
            "requested_fields": e.missing_fields
        }
        
    except InvalidStateError:
        # Fail loud: Issue already closed or locked
        raise SkillExecutionError(f"Issue {issue_id} is in invalid state for routing")
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
|

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
- [GitHub Issues Documentation](<https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues>)
- [Jira Issue Management REST API](<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/>)
- [Linear API Documentation](<https://developers.linear.app/docs>)
- [Issue Triage Methodology (Open Source)](<https://opensource.guide/building-community/#issue-and-pull-request-triage>)
- [GitHub Issues Labels and Automation](<https://docs.github.com/en/issues/using-labels-milestones-and-project/using-labels/managing-labels>)
