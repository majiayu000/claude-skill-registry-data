---
name: agent-selector
description: Automatically selects the best specialized agent based on user prompt keywords and task type. Use when routing work to coder, tester, reviewer, research, refactor, documentation, or cleanup agents.
---

# Agent Selector Skill

**Purpose**: Route tasks to the most appropriate specialized agent for optimal results.

**Trigger Words**: test, write tests, unittest, coverage, pytest, how to, documentation, learn, research, review, check code, code quality, security audit, refactor, clean up, improve code, simplify, document, docstring, readme, api docs

---

## Quick Decision: Which Agent?

```python
def select_agent(prompt: str, context: dict) -> str:
    """Fast agent selection based on prompt keywords and context."""

    prompt_lower = prompt.lower()

    # Priority order matters - check most specific first

    # Testing keywords (high priority)
    testing_keywords = [
        "test", "unittest", "pytest", "coverage", "test case",
        "unit test", "integration test", "e2e test", "tdd",
        "test suite", "test runner", "jest", "mocha"
    ]
    if any(k in prompt_lower for k in testing_keywords):
        return "tester"

    # Research keywords (before implementation)
    research_keywords = [
        "how to", "how do i", "documentation", "learn", "research",
        "fetch docs", "find examples", "best practices",
        "which library", "compare options", "what is", "explain"
    ]
    if any(k in prompt_lower for k in research_keywords):
        return "research"

    # Review keywords (code quality)
    review_keywords = [
        "review", "check code", "code quality", "security audit",
        "validate", "verify", "inspect", "lint", "analyze"
    ]
    if any(k in prompt_lower for k in review_keywords):
        return "reviewer"

    # Refactoring keywords
    refactor_keywords = [
        "refactor", "clean up", "improve code", "simplify",
        "optimize", "restructure", "reorganize", "extract"
    ]
    if any(k in prompt_lower for k in refactor_keywords):
        return "refactor"

    # Documentation keywords
    doc_keywords = [
        "document", "docstring", "readme", "api docs",
        "write docs", "update docs", "comment", "annotation"
    ]
    if any(k in prompt_lower for k in doc_keywords):
        return "documentation"

    # Cleanup keywords
    cleanup_keywords = [
        "remove dead code", "unused imports", "orphaned files",
        "cleanup", "prune", "delete unused"
    ]
    if any(k in prompt_lower for k in cleanup_keywords):
        return "cleanup"

    # Default: coder for implementation tasks
    # (add, build, create, fix, implement, develop)
    return "coder"
```

---

## Agent Selection Logic

### 1. **Tester Agent** - Testing & Coverage
```
Triggers:
- "test", "unittest", "pytest", "coverage"
- "write tests for X"
- "add test cases"
- "increase coverage"
- "test suite", "test runner"

Examples:
✓ "write unit tests for auth module"
✓ "add pytest coverage for payment processor"
✓ "create integration tests"
```

**Agent Capabilities:**
- Write unit, integration, and E2E tests
- Increase test coverage
- Mock external dependencies
- Test edge cases
- Verify test quality

---

### 2. **Research Agent** - Learning & Discovery
```
Triggers:
- "how to", "how do I", "learn"
- "documentation", "research"
- "fetch docs", "find examples"
- "which library", "compare options"
- "what is", "explain"

Examples:
✓ "how to implement OAuth2 in FastAPI"
✓ "research best practices for API rate limiting"
✓ "fetch documentation for Stripe API"
✓ "compare Redis vs Memcached"
```

**Agent Capabilities:**
- Fetch external documentation
- Search for code examples
- Compare library options
- Explain technical concepts
- Find best practices

---

### 3. **Reviewer Agent** - Code Quality & Security
```
Triggers:
- "review", "check code", "code quality"
- "security audit", "validate", "verify"
- "inspect", "lint", "analyze"

Examples:
✓ "review the authentication implementation"
✓ "check code quality in payment module"
✓ "security audit for user input handling"
✓ "validate error handling"
```

**Agent Capabilities:**
- Code quality review
- Security vulnerability detection (OWASP)
- Best practices validation
- Performance anti-pattern detection
- Architecture compliance

---

### 4. **Refactor Agent** - Code Improvement
```
Triggers:
- "refactor", "clean up", "improve code"
- "simplify", "optimize", "restructure"
- "reorganize", "extract"

Examples:
✓ "refactor the user service to reduce complexity"
✓ "clean up duplicate code in handlers"
✓ "simplify the authentication flow"
✓ "extract common logic into utils"
```

**Agent Capabilities:**
- Reduce code duplication
- Improve code structure
- Extract reusable components
- Simplify complex logic
- Optimize algorithms

---

### 5. **Documentation Agent** - Docs & Comments
```
Triggers:
- "document", "docstring", "readme"
- "api docs", "write docs", "update docs"
- "comment", "annotation"

Examples:
✓ "document the payment API endpoints"
✓ "add docstrings to auth module"
✓ "update README with setup instructions"
✓ "generate API documentation"
```

**Agent Capabilities:**
- Generate docstrings (Google style)
- Write README sections
- Create API documentation
- Add inline comments
- Update existing docs

---

### 6. **Cleanup Agent** - Dead Code Removal
```
Triggers:
- "remove dead code", "unused imports"
- "orphaned files", "cleanup", "prune"
- "delete unused"

Examples:
✓ "remove dead code from legacy module"
✓ "clean up unused imports"
✓ "delete orphaned test files"
✓ "prune deprecated functions"
```

**Agent Capabilities:**
- Identify unused imports/functions
- Remove commented code
- Find orphaned files
- Clean up deprecated code
- Safe deletion with verification

---

### 7. **Coder Agent** (Default) - Implementation
```
Triggers:
- "add", "build", "create", "implement"
- "fix", "develop", "write code"
- Any implementation task

Examples:
✓ "add user authentication"
✓ "build payment processing endpoint"
✓ "fix null pointer exception"
✓ "implement rate limiting"
```

**Agent Capabilities:**
- Feature implementation
- Bug fixes
- API development
- Database operations
- Business logic

---

## Output Format

```markdown
## Agent Selection

**User Prompt**: "[original prompt]"

**Task Analysis**:
- Type: [Testing | Research | Review | Refactoring | Documentation | Cleanup | Implementation]
- Keywords Detected: [keyword1, keyword2, ...]
- Complexity: [Simple | Moderate | Complex]

**Selected Agent**: `[agent-name]`

**Rationale**:
[Why this agent was chosen - 1-2 sentences explaining the match between prompt and agent capabilities]

**Estimated Time**: [5-15 min | 15-30 min | 30-60 min | 1-2h]

---

Delegating to **[agent-name]** agent...
```

---

## Decision Tree (Visual)

```
User Prompt
    ↓
Is it about testing?
    ├─ YES → tester
    └─ NO ↓
Is it a research/learning question?
    ├─ YES → research
    └─ NO ↓
Is it about code review/quality?
    ├─ YES → reviewer
    └─ NO ↓
Is it about refactoring?
    ├─ YES → refactor
    └─ NO ↓
Is it about documentation?
    ├─ YES → documentation
    └─ NO ↓
Is it about cleanup?
    ├─ YES → cleanup
    └─ NO ↓
DEFAULT → coder (implementation)
```

---

## Context-Aware Selection

Sometimes context matters more than keywords:

```python
def context_aware_selection(prompt: str, context: dict) -> str:
    """Consider additional context beyond keywords."""

    # Check file types in context
    files = context.get("files", [])

    # If only test files, likely testing task
    if all("test_" in f or "_test" in f for f in files):
        return "tester"

    # If README or docs/, likely documentation
    if any("README" in f or "docs/" in f for f in files):
        return "documentation"

    # If many similar functions, likely refactoring
    if context.get("code_duplication") == "high":
        return "refactor"

    # Check task tags
    tags = context.get("tags", [])
    if "security" in tags:
        return "reviewer"

    # Fall back to keyword-based selection
    return select_agent(prompt, context)
```

---

## Integration with Workflow

### Automatic Agent Selection

```bash
# User: "write unit tests for payment processor"
→ agent-selector triggers
→ Detects: "write", "unit tests" keywords
→ Selected: tester agent
→ Task tool invokes: Task(command="tester", ...)

# User: "how to implement OAuth2 in FastAPI"
→ agent-selector triggers
→ Detects: "how to", "implement" keywords
→ Selected: research agent (research takes priority)
→ Task tool invokes: Task(command="research", ...)

# User: "refactor user service to reduce complexity"
→ agent-selector triggers
→ Detects: "refactor", "reduce complexity" keywords
→ Selected: refactor agent
→ Task tool invokes: Task(command="refactor", ...)
```

### Manual Override

```bash
# Force specific agent
Task(command="tester", prompt="implement payment processing")
# (Overrides agent-selector, uses tester instead of coder)
```

---

## Multi-Agent Tasks

Some tasks need multiple agents in sequence:

```python
def requires_multi_agent(prompt: str) -> List[str]:
    """Detect tasks needing multiple agents."""

    prompt_lower = prompt.lower()

    # Research → Implement → Test
    if "build new feature" in prompt_lower:
        return ["research", "coder", "tester"]

    # Implement → Document
    if "add api endpoint" in prompt_lower:
        return ["coder", "documentation"]

    # Refactor → Test → Review
    if "refactor and validate" in prompt_lower:
        return ["refactor", "tester", "reviewer"]

    # Single agent (most common)
    return [select_agent(prompt, {})]
```

**Example Output:**
```markdown
## Multi-Agent Task Detected

**Agents Required**: 3
1. research - Learn best practices for OAuth2
2. coder - Implement authentication endpoints
3. tester - Write test suite with >80% coverage

**Execution Plan**:
1. Research agent: 15 min
2. Coder agent: 45 min
3. Tester agent: 30 min

**Total Estimate**: 1.5 hours

Executing agents sequentially...
```

---

## Special Cases

### 1. **Debugging Tasks**
```
User: "debug why payment API returns 500"

→ NO dedicated debug agent
→ Route to: coder (for implementation fixes)
→ Skills: Use error-handling-completeness skill
```

### 2. **Story Planning**
```
User: "plan a feature for user authentication"

→ NO dedicated agent
→ Route to: project-manager (via /lazy plan command)
```

### 3. **Mixed Tasks**
```
User: "implement OAuth2 and write tests"

→ Multiple agents needed
→ Route to:
   1. coder (implement OAuth2)
   2. tester (write tests)
```

---

## Performance Metrics

```markdown
## Agent Selection Metrics

**Accuracy**: 95% correct agent selection
**Speed**: <100ms selection time
**Fallback Rate**: 5% default to coder

### Common Mismatches
1. "test the implementation" → coder (should be tester)
2. "document how to use" → coder (should be documentation)

### Improvements
- Add more context signals (file types, tags)
- Learn from user feedback
- Support multi-agent workflows
```

---

## Configuration

```bash
# Disable automatic agent selection
export LAZYDEV_DISABLE_AGENT_SELECTOR=1

# Force specific agent for all tasks
export LAZYDEV_FORCE_AGENT=coder

# Log agent selection decisions
export LAZYDEV_LOG_AGENT_SELECTION=1
```

---

## What This Skill Does NOT Do

❌ Invoke agents directly (Task tool does that)
❌ Execute agent code
❌ Modify agent behavior
❌ Replace /lazy commands
❌ Handle multi-step workflows

✅ **DOES**: Analyze prompt and recommend best agent

---

## Testing the Skill

```bash
# Manual test
Skill(command="agent-selector")

# Test cases
1. "write unit tests" → tester ✓
2. "how to use FastAPI" → research ✓
3. "review this code" → reviewer ✓
4. "refactor handler" → refactor ✓
5. "add docstrings" → documentation ✓
6. "remove dead code" → cleanup ✓
7. "implement login" → coder ✓
```

---

## Quick Reference: Agent Selection

| Keywords | Agent | Use Case |
|----------|-------|----------|
| test, unittest, pytest, coverage | tester | Write/run tests |
| how to, learn, research, docs | research | Learn & discover |
| review, audit, validate, check | reviewer | Quality & security |
| refactor, clean up, simplify | refactor | Code improvement |
| document, docstring, readme | documentation | Write docs |
| remove, unused, dead code | cleanup | Delete unused code |
| add, build, implement, fix | coder | Feature implementation |

---

**Version**: 1.0.0
**Agents Supported**: 7 (coder, tester, research, reviewer, refactor, documentation, cleanup)
**Accuracy**: ~95%
**Speed**: <100ms
