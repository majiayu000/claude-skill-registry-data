---
name: requirement-enhancer
description: Improve the quality, completeness, and testability of software requirements by applying quality attributes analysis, enhancement patterns, acceptance.
---

# Requirement Enhancer

Analyze software requirements for quality defects (ambiguity, incompleteness, untestability, inconsistency) and systematically enhance them to be complete, consistent, testable, and traceable. This skill covers requirement quality assessment, structured enhancement patterns, acceptance criteria generation, user story refinement, and requirement review checklists for both agile and traditional development contexts.

## When to Use This Skill

Use this skill when you need to:

- Review and improve requirements before sprint planning or implementation
- Transform vague feature requests into implementable, testable specifications
- Generate acceptance criteria for user stories
- Identify ambiguous or conflicting requirements in a specification document
- Prepare requirements for handoff to development or QA teams
- Audit requirement quality for compliance or regulatory purposes
- Refine backlog items to meet a "definition of ready"
- Convert high-level business requirements into technical specifications
- Ensure non-functional requirements are measurable and verifiable
- Improve requirement traceability by adding structured identifiers and links

**Trigger phrases**: "improve requirements", "enhance requirements", "requirement quality", "refine user stories", "acceptance criteria", "definition of ready", "ambiguous requirement", "testable requirement", "requirement review", "backlog refinement"

## What This Skill Does

### Core Capabilities

- **Quality Assessment**: Score requirements against INVEST criteria and IEEE 830 quality attributes
- **Ambiguity Detection**: Identify vague, subjective, or undefined terms
- **Completeness Analysis**: Find missing information, edge cases, and boundary conditions
- **Testability Enhancement**: Transform untestable requirements into measurable, verifiable statements
- **Acceptance Criteria Generation**: Produce Given/When/Then or checklist-style acceptance criteria
- **Consistency Checking**: Detect contradictions or conflicts between requirements
- **Non-Functional Requirement Quantification**: Add measurable targets to performance, security, and usability requirements
- **User Story Refinement**: Apply the INVEST framework to improve story quality

### Requirement Quality Attributes

| Attribute | Definition | Defect Example |
|-----------|------------|----------------|
| Complete | All necessary information is present | "The system shall handle errors" (which errors? how?) |
| Consistent | No contradictions with other requirements | REQ-001 says "real-time" but REQ-015 says "batch processing" |
| Unambiguous | Only one interpretation is possible | "The system should be fast" (how fast? for whom?) |
| Testable | A test can verify whether the requirement is met | "The UI shall be user-friendly" (not measurable) |
| Traceable | Has a unique identifier and links to source/tests | "Some requirements mention logging" (no ID, no source) |
| Feasible | Can be implemented within constraints | "Respond in 0ms" (physically impossible) |
| Necessary | Required for stakeholder needs; not gold-plating | "Support 47 languages" (only 3 markets served) |

## Instructions

### Phase 1: Assess Requirement Quality

**Step 1.1: Parse and classify the requirement**

```python
from dataclasses import dataclass, field
from enum import Enum

class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"
    INTERFACE = "interface"
    USER_STORY = "user_story"

class QualityLevel(Enum):
    HIGH = "high"         # Ready for implementation
    MEDIUM = "medium"     # Needs minor enhancement
    LOW = "low"           # Needs significant rework
    CRITICAL = "critical" # Fundamentally flawed

@dataclass
class RequirementAssessment:
    id: str
    original_text: str
    requirement_type: RequirementType
    quality_level: QualityLevel
    issues: list[dict] = field(default_factory=list)
    enhanced_text: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
```

**Step 1.2: Scan for ambiguity indicators**

```python
# Words and phrases that signal ambiguity in requirements
AMBIGUITY_INDICATORS = {
    "vague_adjectives": [
        "fast", "slow", "quick", "efficient", "appropriate", "adequate",
        "reasonable", "significant", "minimal", "user-friendly", "intuitive",
        "robust", "scalable", "flexible", "reliable", "simple", "easy",
        "modern", "responsive", "performant", "lightweight",
    ],
    "vague_quantities": [
        "some", "several", "many", "few", "various", "numerous",
        "a lot", "a number of", "multiple", "large", "small",
    ],
    "weak_verbs": [
        "should", "may", "might", "could", "can",
        "would", "possibly", "optionally", "ideally",
    ],
    "escape_clauses": [
        "if possible", "as appropriate", "as needed", "when necessary",
        "to the extent possible", "where applicable", "if applicable",
        "as required", "etc", "and so on", "and so forth", "or similar",
    ],
    "undefined_references": [
        "the system", "the user", "the data", "the process",
        "the information", "the interface", "relevant", "normal",
        "standard", "typical", "common", "usual",
    ],
}

def detect_ambiguity(requirement_text: str) -> list[dict]:
    """Detect ambiguous terms and phrases in a requirement."""
    issues = []
    text_lower = requirement_text.lower()

    for category, indicators in AMBIGUITY_INDICATORS.items():
        for indicator in indicators:
            if indicator in text_lower:
                issues.append({
                    "type": "ambiguity",
                    "category": category,
                    "term": indicator,
                    "suggestion": get_ambiguity_fix(category, indicator),
                })

    return issues

def get_ambiguity_fix(category: str, term: str) -> str:
    """Suggest a fix for the detected ambiguity."""
    fixes = {
        "vague_adjectives": f"Replace '{term}' with a measurable criterion (e.g., response time < 200ms instead of 'fast')",
        "vague_quantities": f"Replace '{term}' with a specific number or range",
        "weak_verbs": f"Replace '{term}' with 'shall' (mandatory) or 'will' (declarative) or remove the requirement if optional",
        "escape_clauses": f"Remove '{term}' and specify the exact conditions under which the requirement applies",
        "undefined_references": f"Replace '{term}' with a specific named entity from the glossary or domain model",
    }
    return fixes.get(category, f"Clarify the meaning of '{term}'")
```

**Step 1.3: Assess completeness**

```python
def assess_completeness(requirement: dict) -> list[dict]:
    """Check a requirement for missing information."""
    issues = []

    # Check for missing actor (who?)
    actor_patterns = ["user", "admin", "system", "operator", "customer", "API client"]
    has_actor = any(actor in requirement["text"].lower() for actor in actor_patterns)
    if not has_actor:
        issues.append({
            "type": "completeness",
            "missing": "actor",
            "suggestion": "Specify who performs or triggers this action (e.g., 'The authenticated user shall...')",
        })

    # Check for missing action (what?)
    if not any(verb in requirement["text"].lower() for verb in ["shall", "will", "must"]):
        issues.append({
            "type": "completeness",
            "missing": "action_verb",
            "suggestion": "Use 'shall' to indicate a mandatory requirement",
        })

    # Check for missing conditions (when?)
    condition_indicators = ["when", "if", "after", "before", "during", "upon"]
    has_condition = any(c in requirement["text"].lower() for c in condition_indicators)
    if not has_condition and requirement.get("type") == "functional":
        issues.append({
            "type": "completeness",
            "missing": "trigger_condition",
            "suggestion": "Specify when or under what conditions this requirement applies",
        })

    # Check for missing error handling
    if requirement.get("type") == "functional":
        error_indicators = ["error", "fail", "invalid", "timeout", "unavailable"]
        has_error_handling = any(e in requirement["text"].lower() for e in error_indicators)
        if not has_error_handling:
            issues.append({
                "type": "completeness",
                "missing": "error_handling",
                "suggestion": "Specify what happens when the operation fails or receives invalid input",
            })

    # Check for missing boundary conditions
    number_pattern = r"\b\d+\b"
    has_numbers = bool(re.search(number_pattern, requirement["text"]))
    if has_numbers:
        boundary_words = ["minimum", "maximum", "at least", "at most", "between", "up to"]
        has_boundaries = any(b in requirement["text"].lower() for b in boundary_words)
        if not has_boundaries:
            issues.append({
                "type": "completeness",
                "missing": "boundary_conditions",
                "suggestion": "Specify minimum, maximum, and boundary values for numeric parameters",
            })

    return issues
```

**Step 1.4: Assess testability**

```python
def assess_testability(requirement_text: str) -> dict:
    """Evaluate whether a requirement can be objectively tested."""
    untestable_patterns = [
        (r"\b(user-friendly|intuitive|easy to use)\b", "Subjective quality; replace with measurable usability criteria (e.g., task completion rate > 95%)"),
        (r"\b(fast|quick|responsive|performant)\b", "Undefined speed; specify numeric latency or throughput targets"),
        (r"\b(secure|safe)\b", "Undefined security level; specify the security standard or threat model"),
        (r"\b(reliable|available)\b", "Undefined reliability; specify uptime percentage (e.g., 99.9%) or MTBF"),
        (r"\b(scalable)\b", "Undefined scale; specify the target load and growth expectations"),
        (r"\b(support|handle)\b(?!.*\b\d)", "Undefined capacity; specify what volume or variety must be supported"),
        (r"\b(all|every|any|none)\b", "Absolute quantifier; verify this is intentional and achievable"),
    ]

    testability_issues = []
    for pattern, suggestion in untestable_patterns:
        if re.search(pattern, requirement_text, re.IGNORECASE):
            testability_issues.append(suggestion)

    is_testable = len(testability_issues) == 0

    return {
        "testable": is_testable,
        "issues": testability_issues,
        "score": max(0, 10 - len(testability_issues) * 2),
    }
```

### Phase 2: Enhance the Requirement

**Step 2.1: Apply the enhancement pattern**

Transform defective requirements into high-quality ones using structured patterns.

Before and after examples:

```markdown
### Example 1: Vague Performance Requirement

**BEFORE (Low Quality)**:
> The system should be fast.

**Issues detected**:
- Vague adjective: "fast"
- Weak verb: "should"
- No actor specified
- No measurable criterion

**AFTER (High Quality)**:
> REQ-PERF-001: The API gateway shall respond to authenticated GET requests with a P95 latency of less than 200 milliseconds and a P99 latency of less than 500 milliseconds under a sustained load of 1,000 concurrent users.

---

### Example 2: Ambiguous Functional Requirement

**BEFORE (Low Quality)**:
> Users should be able to search for products easily.

**Issues detected**:
- Weak verb: "should"
- Vague adjective: "easily"
- Undefined scope of search
- No error handling

**AFTER (High Quality)**:
> REQ-FUNC-042: An authenticated or anonymous user shall search for products by entering a text query of 1 to 200 characters into the search field. The system shall return matching results within 500 milliseconds, ranked by relevance. If no results match the query, the system shall display a "No results found" message and suggest alternative search terms. The search shall match against product name, description, and category fields. Results shall be paginated with 20 items per page.

---

### Example 3: Untestable Security Requirement

**BEFORE (Low Quality)**:
> The application must be secure.

**Issues detected**:
- Untestable: "secure" is undefined
- No specific threat model or standard referenced
- No measurable criteria

**AFTER (High Quality)**:
> REQ-SEC-001: The application shall pass OWASP Top 10 verification using OWASP ASVS Level 2 criteria. Specifically:
> - All user input shall be validated against an allowlist before processing (ASVS 5.1)
> - All SQL queries shall use parameterized statements (ASVS 5.3)
> - All session tokens shall expire after 30 minutes of inactivity (ASVS 3.3)
> - All passwords shall be hashed using bcrypt with a minimum cost factor of 12 (ASVS 2.4)
> - All API endpoints shall enforce authentication except those listed in the public endpoint registry (ASVS 4.1)
```

**Step 2.2: Quantify non-functional requirements**

```python
NFR_QUANTIFICATION_TEMPLATES = {
    "performance": {
        "template": "The {component} shall {action} within {latency} at the {percentile} percentile under a load of {load} concurrent {actors}.",
        "example": "The search API shall return results within 200ms at the P95 percentile under a load of 500 concurrent users.",
        "required_fields": ["component", "action", "latency", "percentile", "load", "actors"],
    },
    "availability": {
        "template": "The {component} shall maintain {uptime}% availability measured over a {period} rolling window, excluding scheduled maintenance windows announced at least {notice_period} in advance.",
        "example": "The payment service shall maintain 99.95% availability measured over a 30-day rolling window, excluding scheduled maintenance windows announced at least 72 hours in advance.",
        "required_fields": ["component", "uptime", "period", "notice_period"],
    },
    "scalability": {
        "template": "The {component} shall support {current_load} {unit} at launch and scale to {target_load} {unit} within {timeframe} without architectural changes.",
        "example": "The messaging system shall support 10,000 messages per second at launch and scale to 100,000 messages per second within 12 months without architectural changes.",
        "required_fields": ["component", "current_load", "target_load", "unit", "timeframe"],
    },
    "security": {
        "template": "The {component} shall comply with {standard} at {level}. All {data_type} shall be {protection_method} using {algorithm} with a minimum key length of {key_length} bits.",
        "example": "The user data store shall comply with OWASP ASVS at Level 2. All personally identifiable information shall be encrypted at rest using AES-256 with a minimum key length of 256 bits.",
        "required_fields": ["component", "standard", "level", "data_type", "protection_method", "algorithm", "key_length"],
    },
    "usability": {
        "template": "A {user_profile} shall be able to complete {task} in fewer than {max_steps} steps and within {max_time} on their first attempt, without external assistance, as measured by usability testing with at least {sample_size} participants.",
        "example": "A new user with no prior training shall be able to complete the account registration process in fewer than 5 steps and within 3 minutes on their first attempt, without external assistance, as measured by usability testing with at least 10 participants.",
        "required_fields": ["user_profile", "task", "max_steps", "max_time", "sample_size"],
    },
}
```

### Phase 3: Generate Acceptance Criteria

**Step 3.1: Given/When/Then format (BDD style)**

```python
def generate_acceptance_criteria(requirement: dict) -> list[str]:
    """Generate Given/When/Then acceptance criteria from a requirement."""
    criteria = []

    # Happy path
    criteria.append(
        f"Given {requirement['precondition']}, "
        f"when {requirement['action']}, "
        f"then {requirement['expected_result']}."
    )

    # Error cases
    for error_case in requirement.get("error_cases", []):
        criteria.append(
            f"Given {error_case['precondition']}, "
            f"when {error_case['action']}, "
            f"then {error_case['expected_result']}."
        )

    # Boundary conditions
    for boundary in requirement.get("boundaries", []):
        criteria.append(
            f"Given {boundary['condition']}, "
            f"when {boundary['action']}, "
            f"then {boundary['expected_result']}."
        )

    return criteria
```

Example output:

```markdown
## REQ-FUNC-042: Product Search

### Acceptance Criteria

1. **Happy path**: Given the product catalog contains 1,000 products, when a user enters "wireless keyboard" in the search field and submits, then the system returns relevant products ranked by relevance within 500 milliseconds.

2. **Empty results**: Given the product catalog contains products, when a user searches for "xyznonexistent123", then the system displays "No results found" and suggests alternative search terms within 500 milliseconds.

3. **Empty query**: Given the search field is empty, when the user submits the search form, then the system displays a validation message "Please enter a search term" and does not perform a search.

4. **Maximum query length**: Given a user enters a search query of exactly 200 characters, when the user submits, then the system processes the search and returns results.

5. **Exceeded query length**: Given a user enters a search query of 201 characters, when the user submits, then the system truncates the query to 200 characters and performs the search with the truncated query.

6. **Special characters**: Given a user enters a search query containing special characters (e.g., "<script>alert(1)</script>"), when the user submits, then the system sanitizes the input and performs a safe search.

7. **Pagination**: Given a search returns 100 results, when the user views the first page, then 20 results are displayed with pagination controls showing 5 pages.
```

**Step 3.2: Checklist format (for non-BDD teams)**

```markdown
## REQ-SEC-001: Authentication

### Acceptance Criteria Checklist

- [ ] Users can log in with email and password
- [ ] Login fails with incorrect password and returns a generic error message (no enumeration)
- [ ] Login fails with non-existent email and returns the same generic error message
- [ ] Account locks after 5 consecutive failed login attempts
- [ ] Locked accounts unlock after 30 minutes
- [ ] Session token is generated upon successful login
- [ ] Session token expires after 30 minutes of inactivity
- [ ] Session token uses a cryptographically secure random generator (minimum 128 bits of entropy)
- [ ] Password is hashed with bcrypt (cost factor 12 or higher) before storage
- [ ] Login endpoint is rate-limited to 10 requests per minute per IP address
- [ ] All login attempts (success and failure) are logged with timestamp, IP, and user identifier
```

### Phase 4: User Story Refinement

**Step 4.1: Apply the INVEST framework**

```python
INVEST_CRITERIA = {
    "I": {
        "name": "Independent",
        "question": "Can this story be developed and delivered independently of other stories?",
        "fix": "Split coupled stories or redefine boundaries to reduce dependencies",
    },
    "N": {
        "name": "Negotiable",
        "question": "Is the solution open to discussion, or is the implementation prescribed?",
        "fix": "Focus on the 'what' and 'why', not the 'how'. Remove implementation details from the story.",
    },
    "V": {
        "name": "Valuable",
        "question": "Does this story deliver value to a user or stakeholder?",
        "fix": "Reframe in terms of user benefit. If no benefit is identified, question whether the story is necessary.",
    },
    "E": {
        "name": "Estimable",
        "question": "Can the team estimate the effort with reasonable confidence?",
        "fix": "Break down into smaller stories or conduct a spike to reduce uncertainty.",
    },
    "S": {
        "name": "Small",
        "question": "Can this story be completed within a single sprint?",
        "fix": "Split into smaller stories using SPIDR techniques (Spike, Paths, Interface, Data, Rules).",
    },
    "T": {
        "name": "Testable",
        "question": "Can the team write acceptance tests that verify this story is complete?",
        "fix": "Add specific, measurable acceptance criteria. Remove subjective language.",
    },
}

def assess_invest(story: dict) -> dict:
    """Assess a user story against INVEST criteria."""
    results = {}
    for criterion, details in INVEST_CRITERIA.items():
        # Score each criterion
        results[criterion] = {
            "name": details["name"],
            "question": details["question"],
            "passed": False,  # Set by analysis
            "notes": "",
            "fix": details["fix"],
        }
    return results
```

**Step 4.2: Story splitting techniques**

When a story is too large, split it using these patterns:

```markdown
## SPIDR Splitting Techniques

### 1. Spike: Split unknowns into a research spike + implementation story
**Before**: "As a user, I want to log in with biometric authentication"
**After**:
- Spike: Investigate biometric authentication SDK options (2 points)
- Story: Implement fingerprint login using [chosen SDK] (5 points)

### 2. Paths: Split by workflow paths (happy path, error paths, edge cases)
**Before**: "As a user, I want to reset my password"
**After**:
- Story: Reset password via email link (3 points)
- Story: Handle expired reset links with re-send option (2 points)
- Story: Handle account lockout during reset flow (2 points)

### 3. Interface: Split by interface (API, UI, mobile, CLI)
**Before**: "As a user, I want to view my order history"
**After**:
- Story: Build order history API endpoint (3 points)
- Story: Build order history web UI (5 points)
- Story: Build order history mobile view (3 points)

### 4. Data: Split by data scope or volume
**Before**: "As an admin, I want to export reports"
**After**:
- Story: Export reports as CSV (2 points)
- Story: Export reports as PDF with formatting (5 points)
- Story: Export reports with date range filtering (3 points)

### 5. Rules: Split by business rules
**Before**: "As a user, I want to apply discount codes at checkout"
**After**:
- Story: Apply percentage discount codes (3 points)
- Story: Apply fixed-amount discount codes (2 points)
- Story: Apply buy-one-get-one discount codes (5 points)
- Story: Validate discount code expiration and usage limits (3 points)
```

### Phase 5: Requirement Review Checklist

**Step 5.1: Pre-implementation review**

```markdown
## Requirement Quality Review Checklist

### Completeness
- [ ] Actor/stakeholder is identified
- [ ] Trigger condition or precondition is specified
- [ ] Expected behavior is described for the happy path
- [ ] Error cases and exception handling are specified
- [ ] Boundary conditions are defined with specific values
- [ ] Data formats and validation rules are specified
- [ ] Dependencies on other requirements are identified

### Clarity
- [ ] No ambiguous terms (fast, easy, user-friendly, etc.)
- [ ] All domain-specific terms are defined in a glossary
- [ ] No escape clauses (if possible, as appropriate, etc.)
- [ ] Uses "shall" for mandatory and "will" for declarative requirements
- [ ] Each requirement states exactly one thing (no compound requirements)

### Testability
- [ ] Every criterion is measurable or observable
- [ ] Acceptance criteria are written in Given/When/Then or checklist format
- [ ] Non-functional requirements have numeric targets
- [ ] Pass/fail criteria are unambiguous

### Consistency
- [ ] No contradictions with other requirements in the specification
- [ ] Terminology is used consistently across all requirements
- [ ] Referenced requirements exist and are current

### Traceability
- [ ] Has a unique identifier (REQ-XXX format)
- [ ] Links to the source (stakeholder request, regulation, business rule)
- [ ] Links to implementing code (or placeholder for post-implementation)
- [ ] Links to verifying tests (or placeholder for pre-testing)
```

## Best Practices

- Review requirements before implementation, not after; fixing a requirement defect costs 10-100x more after the code is written
- Use the ambiguity indicators list as a lint pass on every requirement; automated detection catches defects that human review misses
- Write acceptance criteria at the same time as the requirement, not later; if you cannot write acceptance criteria, the requirement is not testable
- Quantify every non-functional requirement with specific, measurable targets; "fast" is not a requirement, "P95 < 200ms" is
- Involve QA in requirement refinement; testers are skilled at identifying missing edge cases and untestable criteria
- Keep requirements small enough that each one can be independently implemented and verified in a single sprint
- Use a glossary of domain terms to eliminate ambiguity; if two people can interpret a term differently, define it
- Separate the "what" from the "how" in requirements; implementation details belong in design documents, not requirements
- Review requirements for consistency as a set, not individually; contradictions between requirements are only visible when reviewing the full specification
- Treat requirement enhancement as a continuous practice, not a phase; requirements evolve as understanding deepens

## Common Pitfalls

- **Gold-plating requirements**: Adding excessive detail or unnecessary precision that increases implementation cost without adding value. A requirement for an internal admin tool does not need the same rigor as a safety-critical system.
- **Writing solution requirements instead of problem requirements**: "Use React for the frontend" is a design decision, not a requirement. "The UI shall render on mobile devices with screen widths from 320px to 428px" is a requirement.
- **Skipping error case specification**: Most requirement defects are missing error handling. For every happy path, ask "what happens when this fails?" and document the answer.
- **Using compound requirements**: "The system shall authenticate users AND log all access attempts" is two requirements. Split compound statements so each can be independently tracked and tested.
- **Assuming shared understanding**: "The system shall follow our standard approval workflow" assumes everyone knows what "standard" means. Spell it out or reference a specific documented process.
- **Neglecting non-functional requirements entirely**: Functional requirements get all the attention, but performance, security, and usability defects cause the most production incidents. Treat non-functional requirements with equal rigor.
- **Writing requirements after implementation**: Reverse-engineering requirements from existing code produces descriptions of what the system does, not what it should do. This loses the intent and rationale.
- **Ignoring requirement dependencies**: Requirements that depend on other requirements should explicitly state the dependency. Missing dependencies cause implementation ordering problems and integration failures.
- **Not revisiting requirements when scope changes**: When a related requirement changes, dependent requirements may become inconsistent. Maintain a dependency map and review the chain when any requirement is modified.
- **Treating all requirements as equally important**: Not all requirements are critical. Use MoSCoW (Must, Should, Could, Won't) or similar prioritization to focus enhancement effort on the requirements that matter most.
