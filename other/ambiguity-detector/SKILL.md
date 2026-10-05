---
name: ambiguity-detector
description: "Detect ambiguous, incomplete, or contradictory requirements and specifications with structured clarification templates. Use when reviewing requirements, user stories, API specifications, or any written specification before implementation begins. Turkish triggers: gereksinim belirsiz, çelişki var mı, eksik şartları bul, netleştir."
---

# Ambiguity Detector

Systematic detection of ambiguous, incomplete, contradictory, and underspecified requirements in software specifications, user stories, API contracts, and design documents. This skill provides classification frameworks for different types of ambiguity, detection heuristics, clarification question templates, and requirement quality metrics.

## When to Use This Skill

Use this skill for:

- Reviewing user stories or requirements before sprint planning
- Analyzing API specifications for undefined edge cases
- Evaluating design documents for contradictory or incomplete assumptions
- Checking acceptance criteria for testability and clarity
- Reviewing contracts between teams or services for ambiguous interfaces
- Preparing clarification questions for product owners or stakeholders
- Assessing the overall quality of a requirements document
- Preventing rework caused by misunderstood requirements

**Trigger phrases**: "ambiguous requirement", "unclear specification", "what does this mean", "requirements review", "missing details", "contradictory requirements", "incomplete spec", "ambiguity check", "requirements quality", "clarify this requirement", "underspecified"

## What This Skill Does

This skill provides a structured approach to finding and resolving ambiguity:

- **Ambiguity Classification**: Categorizes ambiguity by type (lexical, syntactic, semantic, pragmatic, scope, temporal) to target the right resolution strategy
- **Detection Heuristics**: Applies pattern-based rules to identify ambiguous words, phrases, and structural patterns in requirements text
- **Completeness Checking**: Verifies that requirements cover all necessary dimensions (inputs, outputs, error cases, performance, security, edge cases)
- **Contradiction Detection**: Identifies requirements that conflict with each other or with stated constraints
- **Clarification Templates**: Provides structured question templates for resolving each type of ambiguity
- **Quality Metrics**: Measures requirement quality using standardized metrics (ambiguity density, completeness score, testability score)

## Instructions

### Step 1: Classify the Type of Ambiguity

Different types of ambiguity require different resolution strategies.

| Ambiguity Type | Definition | Example | Resolution Strategy |
|---------------|-----------|---------|-------------------|
| **Lexical** | A word has multiple meanings | "The system should be fast" ("fast" is undefined) | Define the term precisely with measurable criteria |
| **Syntactic** | Sentence structure allows multiple interpretations | "Users and admins who are active" (does "active" apply to both?) | Restructure the sentence or add explicit grouping |
| **Semantic** | The logical meaning is unclear | "Process orders in real-time" (real-time means different things in different contexts) | Define the specific meaning in this context |
| **Pragmatic** | The intent or purpose is unclear | "Support mobile devices" (native app? responsive web? which devices?) | Clarify the business goal and constraints |
| **Scope** | The boundary of the requirement is undefined | "Handle user authentication" (which auth methods? MFA? SSO? password reset?) | Define explicit in-scope and out-of-scope boundaries |
| **Temporal** | Timing or ordering is unspecified | "Notify the user when the order is processed" (immediately? batched? what channel?) | Specify timing constraints and sequence |

### Step 2: Apply Detection Heuristics

Scan requirements text for patterns that commonly indicate ambiguity.

#### Ambiguous Word Detector

The following words and phrases are strong indicators of ambiguity in requirements:

| Category | Ambiguous Words/Phrases | Why They Are Ambiguous |
|----------|------------------------|----------------------|
| **Vague adjectives** | fast, slow, large, small, many, few, several, appropriate, adequate, reasonable | No measurable threshold defined |
| **Subjective qualifiers** | user-friendly, intuitive, easy to use, simple, modern, clean, elegant | Perception varies by person |
| **Indefinite references** | etc., and so on, and more, as needed, as appropriate, if necessary | Open-ended scope |
| **Passive voice** | "errors should be handled", "data should be validated" | Who/what performs the action? |
| **Weak obligations** | should, could, may, might, it would be nice | Unclear whether this is required or optional |
| **Undefined processes** | process, handle, manage, support, deal with | What specific actions are involved? |
| **Implicit assumptions** | obviously, clearly, naturally, of course, as expected | Assumes shared understanding that may not exist |
| **Unbounded lists** | including but not limited to, such as, for example | Scope is undefined |

#### Python Example: Automated Ambiguity Scanner

```python
import re
from dataclasses import dataclass, field
from typing import List


AMBIGUOUS_PATTERNS = {
    "vague_adjective": {
        "pattern": r"\b(fast|slow|large|small|many|few|several|appropriate|adequate|reasonable|significant|minimal|optimal)\b",
        "severity": "high",
        "message": "Vague adjective without measurable threshold",
    },
    "subjective_qualifier": {
        "pattern": r"\b(user-friendly|intuitive|easy to use|simple|modern|clean|elegant|seamless|smart)\b",
        "severity": "high",
        "message": "Subjective qualifier with no objective criteria",
    },
    "indefinite_scope": {
        "pattern": r"\b(etc\.?|and so on|and more|as needed|as appropriate|if necessary|when possible)\b",
        "severity": "medium",
        "message": "Open-ended scope boundary",
    },
    "weak_obligation": {
        "pattern": r"\b(should|could|may|might|it would be nice|ideally|preferably)\b",
        "severity": "medium",
        "message": "Unclear whether required or optional (use 'must' or 'shall' for requirements)",
    },
    "undefined_process": {
        "pattern": r"\b(process|handle|manage|support|deal with|take care of)\b",
        "severity": "medium",
        "message": "Undefined process -- specify concrete actions",
    },
    "implicit_assumption": {
        "pattern": r"\b(obviously|clearly|naturally|of course|as expected|needless to say)\b",
        "severity": "high",
        "message": "Implicit assumption -- state explicitly",
    },
    "passive_voice": {
        "pattern": r"\b(should be|must be|will be|can be|is to be)\s+(processed|handled|validated|managed|stored|sent|created|updated|deleted)\b",
        "severity": "low",
        "message": "Passive voice -- specify the actor/component responsible",
    },
}


@dataclass
class AmbiguityFinding:
    line_number: int
    text: str
    pattern_name: str
    matched_text: str
    severity: str
    message: str


def scan_for_ambiguity(text: str) -> List[AmbiguityFinding]:
    """Scan requirements text for ambiguous patterns."""
    findings = []
    lines = text.split("\n")

    for line_num, line in enumerate(lines, 1):
        for pattern_name, config in AMBIGUOUS_PATTERNS.items():
            for match in re.finditer(config["pattern"], line, re.IGNORECASE):
                findings.append(AmbiguityFinding(
                    line_number=line_num,
                    text=line.strip(),
                    pattern_name=pattern_name,
                    matched_text=match.group(0),
                    severity=config["severity"],
                    message=config["message"],
                ))

    return sorted(findings, key=lambda f: {"high": 0, "medium": 1, "low": 2}[f.severity])


# Usage
requirements = """
The system should process orders in real-time.
Users need a fast and intuitive search experience.
Handle errors appropriately and log them as needed.
The API must support mobile devices, etc.
Data should be validated before storage.
"""

findings = scan_for_ambiguity(requirements)
for f in findings:
    print(f"[{f.severity.upper()}] Line {f.line_number}: '{f.matched_text}' -- {f.message}")
```

#### JavaScript Example: Completeness Checker

```javascript
const REQUIRED_DIMENSIONS = [
    { name: "inputs", keywords: ["input", "request", "parameter", "argument", "payload", "accepts"] },
    { name: "outputs", keywords: ["output", "response", "return", "result", "produces"] },
    { name: "errors", keywords: ["error", "failure", "exception", "invalid", "reject", "deny"] },
    { name: "performance", keywords: ["latency", "throughput", "response time", "timeout", "SLA"] },
    { name: "security", keywords: ["auth", "permission", "role", "encrypt", "token", "access control"] },
    { name: "edge_cases", keywords: ["empty", "null", "zero", "maximum", "minimum", "boundary", "concurrent"] },
    { name: "data_format", keywords: ["format", "schema", "type", "encoding", "validation", "JSON", "XML"] },
    { name: "state_management", keywords: ["state", "persist", "store", "cache", "session", "idempotent"] },
];

function checkCompleteness(requirementText) {
    const lowerText = requirementText.toLowerCase();
    const results = [];

    for (const dimension of REQUIRED_DIMENSIONS) {
        const found = dimension.keywords.some(kw => lowerText.includes(kw));
        results.push({
            dimension: dimension.name,
            covered: found,
            status: found ? "COVERED" : "MISSING",
        });
    }

    const coveredCount = results.filter(r => r.covered).length;
    const completenessScore = (coveredCount / REQUIRED_DIMENSIONS.length * 100).toFixed(1);

    return {
        score: parseFloat(completenessScore),
        rating: completenessScore >= 80 ? "Good" : completenessScore >= 50 ? "Fair" : "Poor",
        dimensions: results,
        missingDimensions: results.filter(r => !r.covered).map(r => r.dimension),
    };
}

// Usage
const requirement = `
    The API endpoint accepts a JSON payload with user details,
    validates the schema, and returns a 201 response on success.
    Invalid requests return a 400 error with details.
`;

const result = checkCompleteness(requirement);
console.log(`Completeness: ${result.score}% (${result.rating})`);
console.log(`Missing: ${result.missingDimensions.join(", ")}`);
// Output: Missing: performance, security, edge_cases, state_management
```

#### Java Example: Contradiction Detector

```java
import java.util.*;
import java.util.regex.*;

public class ContradictionDetector {

    // Pairs of terms that may indicate contradictions when both appear
    private static final List<String[]> CONTRADICTORY_PAIRS = List.of(
        new String[]{"synchronous", "asynchronous"},
        new String[]{"real-time", "batch"},
        new String[]{"stateless", "maintain state"},
        new String[]{"immutable", "mutable"},
        new String[]{"public", "private"},
        new String[]{"optional", "required"},
        new String[]{"must", "must not"},
        new String[]{"always", "never"},
        new String[]{"all users", "admin only"},
        new String[]{"no downtime", "maintenance window"}
    );

    public record Contradiction(
        String termA,
        String termB,
        int lineA,
        int lineB,
        String contextA,
        String contextB
    ) {}

    public List<Contradiction> detect(String requirementsText) {
        List<Contradiction> contradictions = new ArrayList<>();
        String[] lines = requirementsText.split("\n");

        for (String[] pair : CONTRADICTORY_PAIRS) {
            List<int[]> matchesA = findOccurrences(lines, pair[0]);
            List<int[]> matchesB = findOccurrences(lines, pair[1]);

            if (!matchesA.isEmpty() && !matchesB.isEmpty()) {
                for (int[] a : matchesA) {
                    for (int[] b : matchesB) {
                        contradictions.add(new Contradiction(
                            pair[0], pair[1],
                            a[0], b[0],
                            lines[a[0] - 1].trim(),
                            lines[b[0] - 1].trim()
                        ));
                    }
                }
            }
        }
        return contradictions;
    }

    private List<int[]> findOccurrences(String[] lines, String term) {
        List<int[]> occurrences = new ArrayList<>();
        Pattern pattern = Pattern.compile("\\b" + Pattern.quote(term) + "\\b",
            Pattern.CASE_INSENSITIVE);
        for (int i = 0; i < lines.length; i++) {
            if (pattern.matcher(lines[i]).find()) {
                occurrences.add(new int[]{i + 1});
            }
        }
        return occurrences;
    }
}
```

### Step 3: Check for Completeness

Verify that requirements cover all necessary aspects using the INVEST criteria for user stories and a completeness checklist for specifications.

#### INVEST Criteria for User Stories

| Criterion | Question | Failure Indicator |
|-----------|----------|-------------------|
| **Independent** | Can this story be implemented without depending on other incomplete stories? | References other unfinished stories |
| **Negotiable** | Is the solution flexible, or is a specific implementation dictated? | Prescribes implementation details |
| **Valuable** | Does the story deliver value to a user or stakeholder? | No clear benefit stated |
| **Estimable** | Can the team estimate the effort? | Too vague or too large to estimate |
| **Small** | Can it be completed in one sprint? | Spans multiple epics or themes |
| **Testable** | Can acceptance criteria be verified? | No measurable acceptance criteria |

#### Specification Completeness Checklist

For each requirement, verify these dimensions are addressed:

1. **Happy path**: What happens when everything works correctly?
2. **Error cases**: What happens when inputs are invalid, services are down, or resources are unavailable?
3. **Boundary conditions**: What are the minimum and maximum values, empty inputs, and overflow conditions?
4. **Concurrency**: What happens when multiple users or processes access the same resource simultaneously?
5. **Performance**: What are the response time, throughput, and resource consumption expectations?
6. **Security**: Who is authorized to perform this operation? What data needs protection?
7. **Idempotency**: What happens if the operation is performed twice with the same inputs?
8. **Rollback**: What happens if the operation fails partway through? How is consistency restored?
9. **Monitoring**: How will we know if this feature is working correctly in production?
10. **Migration**: How will existing data or users transition to the new behavior?

### Step 4: Generate Clarification Questions

For each detected ambiguity, generate a structured clarification question.

#### Clarification Question Templates

**For vague adjectives/qualifiers**:
> The requirement states "{exact quote}". The term "{ambiguous term}" needs a measurable definition. Specifically:
> - What is the minimum acceptable threshold for "{ambiguous term}"?
> - What is the maximum acceptable threshold?
> - How will we measure compliance?

**For undefined scope**:
> The requirement states "{exact quote}". The scope is not clearly bounded:
> - What is explicitly included in this requirement?
> - What is explicitly excluded?
> - Are there known future extensions that should influence the design but are not part of this iteration?

**For missing error handling**:
> The requirement describes the happy path for "{feature}". The following error scenarios are not specified:
> - What should happen when {specific error condition}?
> - Should the user see an error message? What should it say?
> - Should the operation be retried automatically?
> - Should the error be logged, and at what severity level?

**For temporal ambiguity**:
> The requirement states "{exact quote}". The timing is not specified:
> - When exactly should this happen (immediately, after a delay, on a schedule)?
> - What triggers this action?
> - Is there a maximum acceptable delay?
> - What happens if the trigger occurs again before the previous action completes?

**For contradictory requirements**:
> Requirements #{id_a} and #{id_b} appear to conflict:
> - #{id_a}: "{text_a}"
> - #{id_b}: "{text_b}"
> Which requirement takes priority? Or do they apply to different contexts? If so, what distinguishes those contexts?

### Step 5: Calculate Requirement Quality Metrics

#### Ambiguity Density

```
Ambiguity Density = (Number of ambiguous findings) / (Number of requirements)
```

| Density | Rating | Action |
|---------|--------|--------|
| 0-0.5 | Good | Minor clarifications may be needed |
| 0.5-1.5 | Fair | Schedule clarification before implementation |
| 1.5-3.0 | Poor | Requirements need significant rework |
| >3.0 | Critical | Requirements are not ready for implementation |

#### Testability Score

```
Testability = (Requirements with measurable acceptance criteria) / (Total requirements) x 100
```

| Score | Rating | Interpretation |
|-------|--------|----------------|
| 90-100% | Excellent | Ready for test-driven development |
| 70-89% | Good | Most requirements are testable |
| 50-69% | Fair | Many requirements need acceptance criteria |
| <50% | Poor | Requirements are not testable as written |

### Step 6: Generate the Ambiguity Report

```
## Requirements Ambiguity Report

### Summary
- **Document**: {document name and version}
- **Requirements reviewed**: {count}
- **Ambiguities detected**: {count}
- **Ambiguity density**: {ratio} ({rating})
- **Completeness score**: {percentage} ({rating})
- **Testability score**: {percentage} ({rating})
- **Contradictions found**: {count}

### Findings by Severity
| Severity | Count | Percentage |
|----------|-------|------------|
| High | {n} | {%} |
| Medium | {n} | {%} |
| Low | {n} | {%} |

### Detailed Findings

#### 1. {Finding Title} (Severity: {level})
- **Requirement**: {ID or quote}
- **Ambiguity type**: {lexical / syntactic / semantic / pragmatic / scope / temporal}
- **Problem**: {What is ambiguous and why it matters}
- **Clarification question**: {Specific question to resolve the ambiguity}
- **Suggested resolution**: {Proposed rewrite if possible}

### Missing Dimensions
{List of completeness gaps across all requirements}

### Contradictions
{List of contradictory requirement pairs with references}

### Recommendations
1. {Priority action items}
```

## Best Practices

- **Review requirements before implementation begins**: the cost of fixing an ambiguous requirement is 10-100x higher after code is written; invest time in clarification upfront
- **Use concrete examples to test understanding**: for each requirement, write at least one concrete input/output example; if you cannot write an example, the requirement is ambiguous
- **Apply the "new team member" test**: would a developer joining the team tomorrow understand this requirement without additional verbal explanation? If not, it needs more detail
- **Distinguish between ambiguity and flexibility**: some requirements are intentionally flexible (allowing the team to choose the best approach); these should be marked as such, not flagged as ambiguous
- **Involve the whole team in ambiguity detection**: developers, testers, and designers each bring different perspectives; a requirement that is clear to a developer may be ambiguous to a tester
- **Keep a glossary of project-specific terms**: define terms like "user", "account", "active", and "real-time" once in a shared glossary and reference it from requirements
- **Track ambiguity resolution over time**: measure ambiguity density across sprints to confirm that requirements quality is improving
- **Use structured templates for requirements**: templates with specific fields (given/when/then, input/output/error) force completeness and reduce free-form ambiguity

## Common Pitfalls

- **Assuming shared context**: the most dangerous ambiguity is the one nobody notices because everyone assumes they have the same understanding; verify assumptions explicitly
- **Over-specifying implementation details**: in an effort to be precise, requirements sometimes prescribe specific technologies, algorithms, or UI layouts that constrain the solution space unnecessarily; specify what, not how
- **Ignoring non-functional requirements**: functional requirements (what the system does) are often well-specified while non-functional requirements (performance, security, availability) are left vague; both need equal rigor
- **Treating ambiguity detection as a one-time activity**: requirements evolve throughout the project; re-evaluate ambiguity whenever requirements change, not just at the beginning
- **Not prioritizing ambiguity resolution**: not all ambiguities are equally important; a vague adjective in a logging requirement is less critical than an undefined error behavior in a payment processing requirement; prioritize by business impact
- **Confusing ambiguity with disagreement**: sometimes two people interpret a requirement differently not because it is ambiguous but because they have different assumptions; surface the assumptions rather than just rewriting the text
- **Creating overly verbose requirements to avoid ambiguity**: excessively detailed requirements are difficult to read and maintain; aim for precision, not length; use examples rather than exhaustive prose
- **Failing to close the loop**: detecting ambiguity is useless if clarification questions are never asked or answers are never incorporated back into the requirements document; track resolution status for every finding
