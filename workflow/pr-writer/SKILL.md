---




name: pr-writer
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
description: Implements intelligent pr writer with multi-factor skill selection, fallback
  chains, and adherence to the 5 Laws of Elegant Defense
license: MIT
maturity: stable
metadata:
  domain: agent
  output-format: analysis
  related-skills: agent-confidence-based-selector, agent-task-routing
  role: orchestration
  scope: orchestration
  triggers: pr-writer, pr writer, how do i pr-writer, orchestrate pr-writer, automate
    pr-writer, agent pr-writer
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




# Pr Writer

Orchestrates intelligent skill selection and execution for pr writer workflows. Applies the 5 Laws of Elegant Defense to guide data naturally through the orchestration pipeline, preventing errors before they occur. Selects optimal skills based on multi-factor scoring including text similarity, historical performance, and system availability.

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
def analyze_changes_and_generate_pr_content(
    diff_content: str,
    commit_history: List[str],
    pr_template: Dict[str, Any]
) -> Dict[str, Any]:
    """Analyze git diff and commit history to generate structured PR content.
    
    Extracts changed files, categorizes changes by type (feat/fix/refactor),
    and maps them to the PR template sections. Implements Law 2 by 
    validating diff format before parsing.
    
    Args:
        diff_content: Raw git diff output
        commit_history: List of commit messages
        pr_template: Template dict with sections like '## Changes', '## Testing'
        
    Returns:
        Dict containing categorized changes, generated markdown, and metadata
    """
    # Law 1: Early exit on invalid input
    if not diff_content or not commit_history:
        raise ValueError("Diff content and commit history are required")
        
    # Law 2: Parse and validate diff structure
    changed_files = _extract_changed_files(diff_content)
    if not changed_files:
        return {"status": "empty_diff", "content": pr_template.get("empty_template", "")}
        
    # Categorize changes based on commit messages and file paths
    categorized = _categorize_changes(changed_files, commit_history)
    
    # Law 3: Return new structure, never mutate template
    generated_pr = dict(pr_template)
    generated_pr["## Changes"] = _format_changes(categorized)
    generated_pr["## Files Changed"] = "\n".join(changed_files)
    generated_pr["metadata"] = {
        "files_count": len(changed_files),
        "categories": list(categorized.keys()),
        "generated_at": time.time()
    }
    return generated_pr
```


### Pattern 2: Execution with Fallback

```python
def execute_pr_generation_with_fallback(
    repo_context: Dict,
    pr_template: Dict,
    max_attempts: int = 2
) -> Dict:
    """Generate PR description with fallback chain for resilience.
    
    Implements Law 4 (Fail Fast) by validating repo state upfront.
    Fallback chain:
    1. Generate from full diff
    2. Generate from summary of changed directories
    3. Fall back to default template with manual review flag
    
    Args:
        repo_context: Dict with 'diff', 'commits', 'branch', 'base_branch'
        pr_template: PR markdown template
        max_attempts: Retry limit for diff parsing
        
    Returns:
        Final PR content dict with generation strategy and confidence
    """
    # Law 1: Validate repo context immediately
    required_keys = {"diff", "commits", "branch"}
    if not required_keys.issubset(repo_context.keys()):
        raise ValueError(f"Missing required repo context keys: {required_keys - set(repo_context.keys())}")
        
    strategy = "full_diff"
    pr_content = None
    
    for attempt in range(max_attempts + 1):
        try:
            if strategy == "full_diff":
                pr_content = analyze_changes_and_generate_pr_content(
                    repo_context["diff"], repo_context["commits"], pr_template
                )
            elif strategy == "directory_summary":
                pr_content = _generate_directory_summary(repo_context, pr_template)
            else:
                pr_content = _apply_default_template(repo_context, pr_template)
                
            if pr_content.get("status") != "empty_diff":
                pr_content["generation_strategy"] = strategy
                pr_content["confidence"] = 0.9 if strategy == "full_diff" else 0.6
                return pr_content
                
        except DiffParseError as e:
            # Law 4: Fail fast on corrupt diff, move to fallback
            if attempt == max_attempts:
                strategy = "default_template"
                continue
            strategy = "directory_summary"
            
    # All strategies exhausted - return with manual review flag
    return {
        "status": "fallback_applied",
        "content": pr_content,
        "requires_manual_review": True,
        "fallback_reason": "Diff parsing failed after all strategies"
    }
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
| `requesting-code-review` | The counterpart skill — use this when writing PRs, load requesting to learn how to frame them for review |
| `code-review` | Provides the review methodology that PR writers should anticipate and align their submissions toward |

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

> Authoritative documentation links for this domain. The model follows markdown links at load time to resolve external references and inline content.

- [GitHub: Creating a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) — Official GitHub documentation on creating and writing PR descriptions
- [CONTRIBUTING.md Best Practices (GitHub Guides)](https://github.blog/open-source/open-source-tools/how-to-contribute-open-source/) — Guide to effective contribution workflows including PR writing standards
- [Open Source PR Templates (GitHub Docs)](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-pull-request-template-for-your-repository) — Best practices for structuring PR templates and descriptions
- [Writing Good Commit Messages and PR Descriptions (Atlassian)](https://www.atlassian.com/git/tutorials/comitting-changes/commit-message) — Atlassian's guide on writing clear, actionable pull request documentation
- [What We've Learned from Reviewing 1,000+ Pull Requests (Stripe)](https://stripe.com/blog/code-review-at-stripe) — Engineering blog post with lessons from large-scale code review processes