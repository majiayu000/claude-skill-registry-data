---
name: traceability-matrix-generator
description: Generate requirement-to-code traceability matrices for compliance audits, regulatory reporting, and quality assurance. Use when preparing for audits.
---

# Traceability Matrix Generator

Generate comprehensive requirement-to-code traceability matrices that map every requirement to its implementing code, associated tests, and verification status. This skill supports compliance frameworks (ISO 27001, SOC 2, FDA, DO-178C), audit preparation, gap analysis, and continuous traceability enforcement in CI/CD pipelines.

## When to Use This Skill

Use this skill when you need to:

- Prepare for a compliance audit (ISO 27001, SOC 2, PCI DSS, HIPAA)
- Generate traceability evidence for regulatory submissions (FDA, DO-178C, IEC 62304)
- Validate that all requirements have corresponding implementations and tests
- Identify gaps where requirements lack test coverage or implementation
- Produce a requirements coverage report for stakeholders
- Map user stories or acceptance criteria to code changes
- Verify that all acceptance criteria are covered by automated tests
- Track requirement changes and their impact on implementation and tests
- Support bi-directional traceability (requirement to code and code to requirement)

**Trigger phrases**: "traceability matrix", "requirement traceability", "requirements coverage", "audit preparation", "compliance mapping", "requirement-to-code mapping", "test coverage mapping", "gap analysis", "requirements tracking"

## What This Skill Does

### Core Capabilities

- **Requirement Extraction**: Parse requirements from various sources (Jira, Markdown, DOORS, CSV)
- **Code Mapping**: Link requirements to implementing source files and functions
- **Test Mapping**: Link requirements to verifying test cases and test results
- **Gap Analysis**: Identify requirements without implementation or test coverage
- **Bi-Directional Tracing**: Trace from requirement to code and from code back to requirement
- **Coverage Metrics**: Calculate implementation and verification coverage percentages
- **Compliance Reporting**: Generate audit-ready reports in multiple formats
- **Change Impact Analysis**: Show which requirements are affected by a code change

### Traceability Levels

```
Requirements  <--->  Design  <--->  Implementation  <--->  Tests  <--->  Verification
  (what)             (how)         (source code)        (test code)     (test results)
```

| Level | Description | Example |
|-------|-------------|---------|
| Forward | Requirement -> Code -> Test | "REQ-001 is implemented in user.ts and tested by user.test.ts" |
| Backward | Test -> Code -> Requirement | "user.test.ts verifies user.ts which implements REQ-001" |
| Horizontal | Requirement -> Requirement | "REQ-001 depends on REQ-005 (authentication prerequisite)" |

## Instructions

### Phase 1: Define the Requirement Source

**Step 1.1: Extract requirements from structured sources**

From Jira (using the REST API):

```python
import requests

def extract_jira_requirements(jira_url: str, project_key: str, token: str) -> list[dict]:
    """Extract requirements from Jira issues."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    jql = f'project = {project_key} AND issuetype in (Story, Requirement, "Acceptance Criteria") ORDER BY key ASC'

    response = requests.get(
        f"{jira_url}/rest/api/3/search",
        headers=headers,
        params={"jql": jql, "maxResults": 1000, "fields": "key,summary,description,status,labels,customfield_10001"},
    )
    response.raise_for_status()

    requirements = []
    for issue in response.json()["issues"]:
        requirements.append({
            "id": issue["key"],
            "title": issue["fields"]["summary"],
            "description": issue["fields"].get("description", ""),
            "status": issue["fields"]["status"]["name"],
            "labels": issue["fields"].get("labels", []),
            "acceptance_criteria": issue["fields"].get("customfield_10001", ""),
        })

    return requirements
```

From Markdown requirement documents:

```python
import re

def extract_markdown_requirements(filepath: str) -> list[dict]:
    """Extract requirements from a structured Markdown document."""
    requirements = []
    current_req = None

    with open(filepath) as f:
        for line in f:
            # Match requirement IDs like REQ-001, FR-001, SEC-001
            match = re.match(r"^##\s+((?:REQ|FR|NFR|SEC|PERF)-\d+):\s+(.+)$", line.strip())
            if match:
                if current_req:
                    requirements.append(current_req)
                current_req = {
                    "id": match.group(1),
                    "title": match.group(2),
                    "description": "",
                    "acceptance_criteria": [],
                }
            elif current_req:
                # Capture acceptance criteria
                ac_match = re.match(r"^-\s+\*\*AC\d+\*\*:\s+(.+)$", line.strip())
                if ac_match:
                    current_req["acceptance_criteria"].append(ac_match.group(1))
                elif line.strip():
                    current_req["description"] += line

    if current_req:
        requirements.append(current_req)

    return requirements
```

**Step 1.2: Standardize requirement format**

```python
from dataclasses import dataclass, field
from enum import Enum

class RequirementStatus(Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    DEFERRED = "deferred"

@dataclass
class Requirement:
    id: str
    title: str
    description: str
    status: RequirementStatus
    acceptance_criteria: list[str] = field(default_factory=list)
    priority: str = "medium"
    category: str = "functional"
    source: str = ""
    implementing_files: list[str] = field(default_factory=list)
    verifying_tests: list[str] = field(default_factory=list)
    verification_status: str = "not_verified"
```

### Phase 2: Map Requirements to Code

**Step 2.1: Identify code annotations and markers**

Embed requirement IDs in source code using consistent markers:

```typescript
// TypeScript/JavaScript: Use JSDoc tags
/**
 * @requirement REQ-001
 * @requirement REQ-002
 * Authenticates a user with email and password.
 */
export async function authenticateUser(email: string, password: string): Promise<AuthResult> {
    // Implementation
}
```

```python
# Python: Use docstring markers
def authenticate_user(email: str, password: str) -> AuthResult:
    """Authenticate a user with email and password.

    Requirements: REQ-001, REQ-002
    """
    pass
```

```java
// Java: Use custom annotations
@Requirement({"REQ-001", "REQ-002"})
public AuthResult authenticateUser(String email, String password) {
    // Implementation
}
```

**Step 2.2: Extract requirement-to-code mappings**

```python
import os
import re
from collections import defaultdict

def extract_code_mappings(codebase_path: str) -> dict[str, list[dict]]:
    """Scan codebase for requirement markers and build the mapping."""
    mappings = defaultdict(list)

    # Patterns to match requirement references in code
    patterns = [
        re.compile(r"@requirement\s+([\w-]+)", re.IGNORECASE),
        re.compile(r"Requirements?:\s*([\w-]+(?:\s*,\s*[\w-]+)*)", re.IGNORECASE),
        re.compile(r"#\s*req:\s*([\w-]+)", re.IGNORECASE),
        re.compile(r"//\s*implements:\s*([\w-]+(?:\s*,\s*[\w-]+)*)", re.IGNORECASE),
    ]

    code_extensions = {".ts", ".js", ".py", ".java", ".cs", ".go", ".rs"}

    for root, dirs, files in os.walk(codebase_path):
        # Skip test directories for implementation mapping
        if "test" in root.lower() or "spec" in root.lower() or "__test__" in root:
            continue

        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext not in code_extensions:
                continue

            filepath = os.path.join(root, filename)
            with open(filepath) as f:
                content = f.read()

            for pattern in patterns:
                for match in pattern.finditer(content):
                    req_ids = [r.strip() for r in match.group(1).split(",")]
                    line_num = content[:match.start()].count("\n") + 1
                    for req_id in req_ids:
                        mappings[req_id].append({
                            "file": filepath,
                            "line": line_num,
                            "type": "implementation",
                        })

    return dict(mappings)
```

**Step 2.3: Extract requirement-to-test mappings**

```python
def extract_test_mappings(test_path: str) -> dict[str, list[dict]]:
    """Scan test files for requirement markers."""
    mappings = defaultdict(list)

    # Test-specific patterns
    patterns = [
        re.compile(r"@requirement\s+([\w-]+)", re.IGNORECASE),
        re.compile(r"verifies?:\s*([\w-]+(?:\s*,\s*[\w-]+)*)", re.IGNORECASE),
        re.compile(r"#\s*tests?:\s*([\w-]+)", re.IGNORECASE),
        re.compile(r'(?:it|test|describe)\s*\(\s*["\'].*?((?:REQ|FR|NFR|SEC)-\d+)', re.IGNORECASE),
    ]

    for root, dirs, files in os.walk(test_path):
        for filename in files:
            if not any(filename.endswith(ext) for ext in [".test.ts", ".spec.ts", "_test.py", "_test.go", "Test.java"]):
                continue

            filepath = os.path.join(root, filename)
            with open(filepath) as f:
                content = f.read()

            for pattern in patterns:
                for match in pattern.finditer(content):
                    req_ids = [r.strip() for r in match.group(1).split(",")]
                    line_num = content[:match.start()].count("\n") + 1
                    for req_id in req_ids:
                        mappings[req_id].append({
                            "file": filepath,
                            "line": line_num,
                            "type": "verification",
                        })

    return dict(mappings)
```

### Phase 3: Build the Traceability Matrix

**Step 3.1: Assemble the full matrix**

```python
def build_traceability_matrix(
    requirements: list[Requirement],
    code_mappings: dict[str, list[dict]],
    test_mappings: dict[str, list[dict]],
) -> list[dict]:
    """Build the complete traceability matrix."""
    matrix = []

    for req in requirements:
        implementations = code_mappings.get(req.id, [])
        tests = test_mappings.get(req.id, [])

        # Determine coverage status
        has_implementation = len(implementations) > 0
        has_tests = len(tests) > 0

        if has_implementation and has_tests:
            coverage_status = "FULLY_TRACED"
        elif has_implementation and not has_tests:
            coverage_status = "IMPLEMENTED_NOT_VERIFIED"
        elif not has_implementation and has_tests:
            coverage_status = "TEST_WITHOUT_IMPLEMENTATION"
        else:
            coverage_status = "NOT_TRACED"

        matrix.append({
            "requirement_id": req.id,
            "title": req.title,
            "priority": req.priority,
            "category": req.category,
            "status": req.status.value,
            "implementing_files": [
                {"file": m["file"], "line": m["line"]} for m in implementations
            ],
            "verifying_tests": [
                {"file": m["file"], "line": m["line"]} for m in tests
            ],
            "coverage_status": coverage_status,
            "acceptance_criteria_count": len(req.acceptance_criteria),
        })

    return matrix
```

**Step 3.2: Calculate coverage metrics**

```python
def calculate_coverage_metrics(matrix: list[dict]) -> dict:
    """Calculate traceability coverage metrics."""
    total = len(matrix)
    if total == 0:
        return {"error": "No requirements found"}

    fully_traced = sum(1 for r in matrix if r["coverage_status"] == "FULLY_TRACED")
    implemented_only = sum(1 for r in matrix if r["coverage_status"] == "IMPLEMENTED_NOT_VERIFIED")
    not_traced = sum(1 for r in matrix if r["coverage_status"] == "NOT_TRACED")
    test_only = sum(1 for r in matrix if r["coverage_status"] == "TEST_WITHOUT_IMPLEMENTATION")

    # By priority
    high_priority = [r for r in matrix if r["priority"] == "high"]
    high_traced = sum(1 for r in high_priority if r["coverage_status"] == "FULLY_TRACED")

    # By category
    categories = {}
    for req in matrix:
        cat = req["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "traced": 0}
        categories[cat]["total"] += 1
        if req["coverage_status"] == "FULLY_TRACED":
            categories[cat]["traced"] += 1

    return {
        "total_requirements": total,
        "fully_traced": fully_traced,
        "implemented_not_verified": implemented_only,
        "not_traced": not_traced,
        "test_without_implementation": test_only,
        "implementation_coverage": round(
            (fully_traced + implemented_only) / total * 100, 1
        ),
        "verification_coverage": round(fully_traced / total * 100, 1),
        "full_traceability_coverage": round(fully_traced / total * 100, 1),
        "high_priority_coverage": round(
            high_traced / max(len(high_priority), 1) * 100, 1
        ),
        "by_category": {
            cat: round(data["traced"] / data["total"] * 100, 1)
            for cat, data in categories.items()
        },
    }
```

### Phase 4: Gap Analysis

**Step 4.1: Identify traceability gaps**

```python
def perform_gap_analysis(matrix: list[dict]) -> dict:
    """Identify and categorize traceability gaps."""
    gaps = {
        "missing_implementation": [],
        "missing_tests": [],
        "orphaned_tests": [],
        "high_priority_gaps": [],
    }

    for req in matrix:
        if req["coverage_status"] == "NOT_TRACED":
            gap = {
                "requirement_id": req["requirement_id"],
                "title": req["title"],
                "priority": req["priority"],
                "gap_type": "No implementation and no tests",
            }
            gaps["missing_implementation"].append(gap)
            if req["priority"] == "high":
                gaps["high_priority_gaps"].append(gap)

        elif req["coverage_status"] == "IMPLEMENTED_NOT_VERIFIED":
            gap = {
                "requirement_id": req["requirement_id"],
                "title": req["title"],
                "priority": req["priority"],
                "implementing_files": req["implementing_files"],
                "gap_type": "Implemented but no test coverage",
            }
            gaps["missing_tests"].append(gap)
            if req["priority"] == "high":
                gaps["high_priority_gaps"].append(gap)

        elif req["coverage_status"] == "TEST_WITHOUT_IMPLEMENTATION":
            gaps["orphaned_tests"].append({
                "requirement_id": req["requirement_id"],
                "title": req["title"],
                "verifying_tests": req["verifying_tests"],
                "gap_type": "Tests exist but no implementation mapping found",
            })

    return gaps
```

**Step 4.2: Generate gap remediation recommendations**

```python
def generate_remediation_plan(gaps: dict) -> list[dict]:
    """Generate a prioritized remediation plan for traceability gaps."""
    plan = []

    # Priority 1: High-priority requirements with no implementation
    for gap in gaps["high_priority_gaps"]:
        if gap["gap_type"].startswith("No implementation"):
            plan.append({
                "priority": "CRITICAL",
                "action": f"Implement {gap['requirement_id']}: {gap['title']}",
                "reason": "High-priority requirement with no implementation",
            })

    # Priority 2: High-priority requirements with no test coverage
    for gap in gaps["high_priority_gaps"]:
        if gap["gap_type"].startswith("Implemented"):
            plan.append({
                "priority": "HIGH",
                "action": f"Add test coverage for {gap['requirement_id']}: {gap['title']}",
                "reason": "High-priority requirement implemented but not verified",
            })

    # Priority 3: All other missing implementations
    for gap in gaps["missing_implementation"]:
        if gap["priority"] != "high":
            plan.append({
                "priority": "MEDIUM",
                "action": f"Implement {gap['requirement_id']}: {gap['title']}",
                "reason": f"{gap['priority']}-priority requirement with no implementation",
            })

    # Priority 4: Missing test coverage
    for gap in gaps["missing_tests"]:
        if gap["priority"] != "high":
            plan.append({
                "priority": "LOW",
                "action": f"Add tests for {gap['requirement_id']}: {gap['title']}",
                "reason": "Implemented but not verified by tests",
            })

    return plan
```

### Phase 5: Generate Reports

**Step 5.1: Markdown traceability report**

```python
def generate_markdown_report(
    matrix: list[dict],
    metrics: dict,
    gaps: dict,
) -> str:
    """Generate a Markdown traceability matrix report."""
    lines = []

    lines.append("# Requirements Traceability Matrix")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().isoformat()}")
    lines.append(f"**Total Requirements**: {metrics['total_requirements']}")
    lines.append("")

    # Coverage summary
    lines.append("## Coverage Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Implementation Coverage | {metrics['implementation_coverage']}% |")
    lines.append(f"| Verification Coverage | {metrics['verification_coverage']}% |")
    lines.append(f"| Full Traceability | {metrics['full_traceability_coverage']}% |")
    lines.append(f"| High Priority Coverage | {metrics['high_priority_coverage']}% |")
    lines.append("")

    # Full matrix table
    lines.append("## Traceability Matrix")
    lines.append("")
    lines.append("| Req ID | Title | Priority | Implementation | Tests | Status |")
    lines.append("|--------|-------|----------|----------------|-------|--------|")

    for req in matrix:
        impl_files = ", ".join(m["file"].split("/")[-1] for m in req["implementing_files"]) or "None"
        test_files = ", ".join(m["file"].split("/")[-1] for m in req["verifying_tests"]) or "None"
        status_icon = {
            "FULLY_TRACED": "Traced",
            "IMPLEMENTED_NOT_VERIFIED": "No Tests",
            "NOT_TRACED": "GAP",
            "TEST_WITHOUT_IMPLEMENTATION": "Orphaned",
        }.get(req["coverage_status"], req["coverage_status"])

        lines.append(
            f"| {req['requirement_id']} | {req['title'][:50]} | {req['priority']} | {impl_files} | {test_files} | {status_icon} |"
        )

    # Gap analysis
    lines.append("")
    lines.append("## Gap Analysis")
    lines.append("")

    if gaps["high_priority_gaps"]:
        lines.append("### Critical Gaps (High Priority)")
        lines.append("")
        for gap in gaps["high_priority_gaps"]:
            lines.append(f"- **{gap['requirement_id']}**: {gap['title']} -- {gap['gap_type']}")
        lines.append("")

    if gaps["missing_tests"]:
        lines.append("### Missing Test Coverage")
        lines.append("")
        for gap in gaps["missing_tests"]:
            lines.append(f"- **{gap['requirement_id']}**: {gap['title']}")
        lines.append("")

    return "\n".join(lines)
```

**Step 5.2: CSV export for spreadsheet tools**

```python
import csv
import io

def generate_csv_report(matrix: list[dict]) -> str:
    """Generate a CSV traceability matrix for import into Excel or Google Sheets."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow([
        "Requirement ID",
        "Title",
        "Priority",
        "Category",
        "Status",
        "Implementing Files",
        "Implementing Lines",
        "Verifying Tests",
        "Coverage Status",
    ])

    for req in matrix:
        writer.writerow([
            req["requirement_id"],
            req["title"],
            req["priority"],
            req["category"],
            req["status"],
            "; ".join(m["file"] for m in req["implementing_files"]),
            "; ".join(str(m["line"]) for m in req["implementing_files"]),
            "; ".join(m["file"] for m in req["verifying_tests"]),
            req["coverage_status"],
        ])

    return output.getvalue()
```

### Phase 6: CI/CD Integration

**Step 6.1: Traceability gate in CI/CD**

```yaml
# .github/workflows/traceability-check.yml
name: Traceability Check
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  traceability:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate traceability matrix
        run: |
          python scripts/traceability-matrix.py \
            --requirements docs/requirements/ \
            --codebase src/ \
            --tests tests/ \
            --output traceability-report.json

      - name: Check traceability thresholds
        run: |
          python scripts/traceability-gate.py \
            --report traceability-report.json \
            --min-implementation-coverage 90 \
            --min-verification-coverage 80 \
            --fail-on-high-priority-gaps

      - name: Upload traceability report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: traceability-report
          path: traceability-report.json
```

**Step 6.2: Pre-commit hook for requirement markers**

```bash
#!/bin/bash
# .git/hooks/pre-commit - Verify new code includes requirement markers

# Find new or modified source files (excluding tests)
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=AM | grep -E '\.(ts|js|py|java)$' | grep -v test | grep -v spec)

MISSING_MARKERS=0
for file in $CHANGED_FILES; do
    if ! grep -qiE '@requirement|Requirements?:|# req:|// implements:' "$file"; then
        echo "WARNING: $file has no requirement marker"
        MISSING_MARKERS=$((MISSING_MARKERS + 1))
    fi
done

if [ $MISSING_MARKERS -gt 0 ]; then
    echo ""
    echo "$MISSING_MARKERS file(s) are missing requirement traceability markers."
    echo "Add @requirement REQ-XXX or equivalent markers to link code to requirements."
    echo ""
    # Warning only; change to 'exit 1' to enforce
    exit 0
fi
```

### Change Impact Analysis

When requirements change, identify the downstream impact:

```python
def analyze_change_impact(
    changed_requirement_id: str,
    matrix: list[dict],
    dependency_graph: dict,
) -> dict:
    """Analyze the impact of a requirement change on implementation and tests."""
    req = next((r for r in matrix if r["requirement_id"] == changed_requirement_id), None)
    if not req:
        return {"error": f"Requirement {changed_requirement_id} not found"}

    impacted_files = set()
    impacted_tests = set()

    # Direct implementation files
    for impl in req["implementing_files"]:
        impacted_files.add(impl["file"])
        # Find other files that depend on this implementation
        for dep_file in dependency_graph.get(impl["file"], []):
            impacted_files.add(dep_file)

    # Direct test files
    for test in req["verifying_tests"]:
        impacted_tests.add(test["file"])

    return {
        "requirement": changed_requirement_id,
        "title": req["title"],
        "impacted_implementation_files": sorted(impacted_files),
        "impacted_test_files": sorted(impacted_tests),
        "total_impacted_files": len(impacted_files) + len(impacted_tests),
        "recommendation": "Review and update all impacted files after requirement change",
    }
```

## Best Practices

- Embed requirement markers directly in source code rather than maintaining a separate mapping document; code-embedded markers stay in sync with the code as it evolves
- Use a consistent marker format across the entire codebase and document it in the project's contributing guide
- Automate traceability matrix generation in CI/CD rather than generating it manually before audits
- Start with high-priority requirements when building traceability; 100% traceability across all requirements is ideal but not always feasible immediately
- Include acceptance criteria in the traceability chain, not just top-level requirements; one requirement may have multiple acceptance criteria, each needing its own test
- Generate both human-readable (Markdown, HTML) and machine-readable (JSON, CSV) reports to serve different audiences
- Review the traceability matrix as part of sprint reviews or release planning to catch gaps early
- Use bi-directional traceability to detect orphaned tests (tests that do not map to any requirement) and orphaned code (code that does not implement any requirement)
- Version the traceability matrix alongside the code in source control so that historical traceability is preserved
- Treat traceability gaps in high-priority or security-critical requirements as blockers, not warnings

## Common Pitfalls

- **Maintaining the matrix separately from the code**: A spreadsheet-based traceability matrix that is updated manually will inevitably drift out of sync with the actual code. Embed markers in the code and generate the matrix automatically.
- **Mapping requirements too broadly**: Linking a single requirement to an entire module ("REQ-001 is implemented in src/services/") provides no useful traceability. Map to specific files and functions.
- **Ignoring negative requirements**: Requirements like "the system shall NOT store passwords in plain text" need verification too. Include negative test cases in the traceability matrix.
- **Treating traceability as a one-time exercise**: Traceability must be maintained continuously. A matrix generated once before an audit will be outdated by the next sprint.
- **Not including non-functional requirements**: Performance, security, and reliability requirements are often omitted from traceability matrices. They are equally important for compliance and should be traced to their implementing controls and verification tests.
- **Over-engineering the marker format**: Complex marker formats discourage adoption. Keep it simple (a comment with the requirement ID is sufficient) and enforce consistency with linting rules.
- **Missing transitive traceability**: A requirement may be implemented through a chain of modules. Ensure the traceability follows the full implementation chain, not just the top-level entry point.
- **Not linking to test results**: Traceability to test code is necessary but not sufficient. For audit purposes, link to actual test execution results (pass/fail) to prove verification.
- **Ignoring orphaned code**: Code that does not map to any requirement may indicate scope creep, unused features, or missing requirements. Investigate orphaned code during gap analysis.
- **Failing to update traceability when requirements change**: When a requirement is modified, split, or deleted, the traceability matrix must be updated accordingly. Include traceability review as part of the requirement change process.
