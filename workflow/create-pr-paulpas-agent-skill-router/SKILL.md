---




name: create-pr
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
description: Implements intelligent create pr with multi-factor skill selection, fallback
  chains, and adherence to the 5 Laws of Elegant Defense
license: MIT
maturity: stable
metadata:
  domain: agent
  output-format: analysis
  related-skills: agent-confidence-based-selector, agent-task-routing
  role: orchestration
  scope: orchestration
  triggers: create-pr, create pr, how do i create-pr, orchestrate create-pr, automate
    create-pr, agent create-pr
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




# Create Pr

Orchestrates intelligent skill selection and execution for create pr workflows. Applies the 5 Laws of Elegant Defense to guide data naturally through the orchestration pipeline, preventing errors before they occur. Selects optimal skills based on multi-factor scoring including text similarity, historical performance, and system availability.

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
def prepare_pr_payload(
    source_branch: str,
    target_branch: str,
    pr_title: str,
    pr_body: str,
    repo_config: Dict
) -> Dict:
    """Prepare and validate a Pull Request payload before submission.
    
    Validates branch existence, checks for existing open PRs,
    and formats the payload according to repository conventions.
    
    Args:
        source_branch: Feature or fix branch name
        target_branch: Base branch (e.g., main, develop)
        pr_title: Concise PR title
        pr_body: Detailed PR description with checklist
        repo_config: Repository settings including labels and templates
        
    Returns:
        Validated PR payload dictionary ready for API submission
        
    Raises:
        ValidationError: If branches are invalid or PR already exists
    """
    # Guard clause - Early Exit (Law 1)
    if not source_branch or not target_branch:
        raise ValidationError("Source and target branches are required")
        
    # Parse input - Make Illegal States Unrepresentable (Law 2)
    sanitized_title = pr_title.strip()[:100]
    formatted_body = _apply_pr_template(pr_body, repo_config.get("template", "default"))
    
    # Check for existing open PRs to prevent duplicates
    existing_prs = _fetch_open_prs(repo_config["repo_url"], target_branch)
    for pr in existing_prs:
        if pr["head"] == source_branch and pr["state"] == "open":
            raise ValidationError(f"Open PR already exists for {source_branch}")
            
    # Atomic Predictability (Law 3) - Return new dict, don't mutate inputs
    payload = {
        "title": sanitized_title,
        "body": formatted_body,
        "head": source_branch,
        "base": target_branch,
        "labels": repo_config.get("default_labels", []),
        "maintainer_can_modify": repo_config.get("allow_fork_maintainer_edit", True)
    }
    
    # Validate required labels and reviewers
    if repo_config.get("required_reviewers"):
        payload["reviewers"] = repo_config["required_reviewers"]
        
    return payload
```


### Pattern 2: Execution with Fallback

```python
def execute_pr_creation(
    payload: Dict,
    github_client,
    max_retries: int = 2
) -> Dict:
    """Execute Pull Request creation with domain-specific fallback handling.
    
    Handles API rate limits, merge conflicts, and permission issues
    by implementing a targeted fallback chain for PR workflows.
    
    Args:
        payload: Validated PR payload dictionary
        github_client: Authenticated GitHub API client
        max_retries: Maximum retry attempts for transient API failures
        
    Returns:
        PR creation result with URL, status, and metadata
        
    Raises:
        PRCreationError: If all retries and fallbacks are exhausted
    """
    # Guard clause - validate payload structure (Early Exit)
    required_keys = {"title", "body", "head", "base"}
    if not required_keys.issubset(payload.keys()):
        raise PRCreationError("Missing required fields in PR payload")
        
    for attempt in range(max_retries + 1):
        try:
            # Execute PR creation via GitHub API
            response = github_client.create_pull_request(payload)
            
            # Success - Atomic Predictability (Law 3)
            return {
                "success": True,
                "pr_url": response["html_url"],
                "pr_number": response["number"],
                "status": response["state"],
                "attempts": attempt + 1,
                "created_at": response["created_at"]
            }
            
        except RateLimitExceededError as e:
            # Transient API limit - wait and retry with backoff
            if attempt == max_retries:
                return _fallback_to_manual_pr_creation(payload)
            time.sleep(2 ** attempt)
            
        except MergeConflictError as e:
            # Domain-specific conflict - adjust base branch or notify
            if attempt == max_retries:
                return _fallback_to_conflict_resolution(payload, e)
                
        except PermissionError as e:
            # Fail Fast - Don't retry permission issues (Law 4)
            raise PRCreationError(f"Permission denied for PR creation: {str(e)}") from e
            
    # All retries exhausted - Fail Loud (Law 4)
    raise PRCreationError(
        f"Failed to create PR after {max_retries + 1} attempts"
    )
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
- Validate branch naming conventions and PR scope before creating pull requests — enforce repository-level policies
- Require all CI checks to pass before merging; never allow bypass of required status checks without codeowner approval
- Implement automated changelog generation from commit messages using conventional commits format
- Maintain linear history via rebase on main branch; avoid merge commits except for release branches

### MUST NOT DO
- Do not force-push to shared or protected branches — only the original author may force-push their own feature branch
- Avoid squashing all commits during PR review when historical commit context is valuable for understanding evolution
- Never skip required code reviews regardless of how small the change appears — automation cannot assess architectural impact
- Do not create PRs larger than 400 lines of net changes without explicit approval from a senior reviewer


## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [GitHub Pull Requests Documentation](<https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>)
- [GitLab Merge Requests Guide](<https://docs.gitlab.com/ee/user/project/merge_requests/>)
- [Conventional Commits Specification](<https://www.conventionalcommits.org/en/v1.0.0/>)
- [PR Review Best Practices (Google)](<https://google.github.io/eng-practices/review/>)
- [CODEOWNERS File Configuration](<https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners>)

## Related Skills

| Skill | Purpose |
|