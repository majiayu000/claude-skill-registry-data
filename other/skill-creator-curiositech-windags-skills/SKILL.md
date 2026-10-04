---
license: Apache-2.0
name: skill-creator
description: 'Use this skill when creating a new Claude skill from scratch, editing or improving an existing skill, or measuring skill performance with evals and benchmarks. Invoke whenever the user says things like ''make a skill for X'', ''turn this workflow into a skill'', ''test my skill'', ''improve my skill'', ''run evals'', ''benchmark this'', or ''optimize my skill description''. Also use proactively when the conversation has produced a repeatable workflow that would benefit from being captured as a skill. Covers the full lifecycle: capture intent, draft SKILL.md, run evals, review with user, iterate, optimize description, package. NOT for general coding help, debugging runtime errors, building MCP servers, writing Claude hooks, or creating plugins - use domain-specific skills for those.'
metadata:
  tags:
    - skill-creation
    - evals
    - benchmarking
    - skill-improvement
    - meta
category: Agent & Orchestration
tags:
  - skill-creation
  - authoring
  - templates
  - meta
  - development
---

# Skill Creator

A skill for creating new skills and iteratively improving them through systematic testing and evaluation.

## Decision Points

Navigate based on the user's entry point and current skill state:

```
Entry Assessment
├── "Make a skill for X" → Capture Intent → Draft SKILL.md
├── "Turn this workflow into a skill" → Extract from conversation → Confirm intent
├── "Test/improve my skill" → Locate skill → Run test cases
├── "Optimize description" → Load skill → Generate trigger evals
└── Proactive detection → Assess if workflow is repeatable → Suggest skill creation

Skill State Check
├── No skill exists → Full creation flow (intent → draft → test → iterate)
├── Draft exists, no tests → Create test cases → Run evaluations
├── Has tests, poor performance → Analyze failures → Improve skill → Retest
└── Working skill → Description optimization → Package

Test Case Strategy
├── Objectively verifiable outputs (code, data, files) → Create quantitative assertions
├── Subjective outputs (writing, design) → Skip assertions, focus on qualitative review
└── Mixed outputs → Assertions for verifiable parts, human review for subjective

Evaluation Scope
├── First iteration → 2-3 focused test cases
├── Subsequent iterations → Rerun same cases for comparison
└── Final validation → Expand to 5-10 diverse cases

Improvement Trigger
├── User feedback identifies specific issues → Target those areas
├── Quantitative benchmarks show regression → Analyze root cause
├── No clear feedback but low pass rates → Review transcripts for patterns
└── Consistent success across tests → Move to description optimization
```

## Failure Modes

### Vague Intent Capture (Symptom: Poor skill performance on diverse inputs)
**Detection**: If skill works on test cases but fails when users try different variations of the same task type.
**Diagnosis**: Intent interview was too narrow or focused only on specific examples rather than the general capability.
**Fix**: Restart intent capture with broader questions: "What are all the ways someone might ask for this?" and "What edge cases should we handle?"

### Weak Test Coverage (Symptom: High pass rates but skill doesn't work in practice)
**Detection**: If assertions are passing but user feedback consistently identifies problems, or if skill works only on the exact test prompts.
**Diagnosis**: Test cases don't represent real usage patterns, or assertions are non-discriminating.
**Fix**: Apply discriminating assertion test - would a clearly wrong output also pass this assertion? Rewrite assertions to check specific content only a correct output would have.

### Iteration Tunnel Vision (Symptom: Endless tweaking without improvement)
**Detection**: If 3+ iterations show no meaningful progress, or changes only address test cases without improving general capability.
**Diagnosis**: Over-optimization on specific examples rather than addressing root capability gaps.
**Fix**: Step back and analyze failure patterns across all test cases. Consider fundamental approach changes rather than incremental tweaks.

### Missing Baseline Reality Check (Symptom: False confidence in skill value)
**Detection**: If you're only testing with the skill and never comparing to without-skill performance.
**Diagnosis**: No objective measure of whether the skill actually improves outcomes over baseline Claude.
**Fix**: Always run baseline comparisons (without-skill for new skills, old-version for improvements) to measure actual value added.

### Premature Description Optimization (Symptom: Great triggering, poor execution)
**Detection**: If spending time on description optimization before the skill reliably works on test cases.
**Diagnosis**: Optimizing discoverability before ensuring quality.
**Fix**: Complete the test-improve cycle first. Only optimize descriptions once the skill consistently passes evaluations.

## Worked Examples

### Example 1: Creating a Documentation Skill from Scratch

**Initial Request**: "I keep having to explain our API structure to new developers. Can we make a skill for that?"

**Intent Capture Decision Tree**:
- What should skill do? → Generate API documentation from code/schemas
- When should it trigger? → "document the API", "create API docs", "explain our endpoints"
- Output format? → Markdown with examples and parameter tables
- Test cases needed? → Yes (verifiable structure and content)

**Draft Process**:
- Interview revealed: Uses OpenAPI specs, needs examples for each endpoint, must include authentication section
- Created SKILL.md with sections for parsing specs, generating examples, formatting output
- Identified need for `scripts/openapi_parser.py` based on repetitive parsing logic

**Test Cases Design**:
```json
{
  "skill_name": "api-documenter", 
  "evals": [
    {
      "id": 1,
      "prompt": "Document our user authentication API endpoints",
      "files": ["evals/files/auth_spec.yaml"],
      "expectations": [
        "Output includes authentication section with bearer token example",
        "Each endpoint has request/response examples",
        "Parameter tables include required/optional indicators"
      ]
    }
  ]
}
```

**First Iteration Results**:
- With-skill: Generated docs but missing parameter validation rules
- Without-skill: Basic endpoint list, no examples or detailed parameters
- User feedback: "The examples are great, but developers need to know which fields are validated how"

**Improvement Applied**:
- Added validation parsing to OpenAPI script
- Updated skill instructions to emphasize validation documentation
- Added section on error response formats

**Second Iteration**: Pass rate improved from 60% to 95%, user satisfied with comprehensive coverage.

### Example 2: Improving an Existing Code Review Skill

**Entry Point**: User says "My code review skill keeps missing security issues"

**State Assessment**: Skill exists, has test cases, but low performance on security-related assertions.

**Failure Analysis**:
- Reviewed transcripts: Skill was checking syntax/style but not analyzing security patterns
- Baseline comparison showed without-skill Claude actually caught more security issues
- Root cause: Skill was too focused on formatting, not enough on vulnerability detection

**Improvement Strategy**:
- Added security-focused checklist with OWASP patterns
- Included examples of common vulnerabilities (SQL injection, XSS, auth bypasses)
- Created `references/security_patterns.md` with detailed detection guidance

**Test Case Iteration**:
- Reran existing cases: General improvement across all assertions
- Added security-specific test case with intentionally vulnerable code
- New assertions focused on specific vulnerability detection rather than general "security check"

**Key Learning**: The skill was solving the wrong problem - automating style checks instead of augmenting security analysis. Success required fundamental reframing, not incremental improvement.

## Quality Gates

- [ ] Intent is clearly defined with specific trigger phrases and expected outputs identified
- [ ] Skill description includes both what it does AND when to use it (addresses undertriggering)
- [ ] At least 2 realistic test cases created that represent actual user scenarios
- [ ] If outputs are verifiable, assertions check specific content only correct execution would produce
- [ ] Each test case includes both with-skill and baseline runs for comparison
- [ ] Quantitative results show meaningful improvement over baseline (>20% better pass rate or significant time/quality gains)
- [ ] User feedback from viewer review is incorporated into skill improvements
- [ ] Skill instructions explain the "why" behind requirements, not just rigid rules
- [ ] Any repeated helper scripts across test cases are bundled in scripts/ directory
- [ ] Final iteration achieves user satisfaction or 95%+ pass rate on discriminating assertions
- [ ] If the skill creation flow ever invokes git: it works in a git worktree (`git worktree add ../$repo-skill-creator-$task`), stages by explicit path (no `git add -A`/`add .`/`add -u`), runs `git status --porcelain` as a dirty-tree check before commit, and does not push without explicit authorization. See ADR 0001 in this repo (`docs/adr/0001-background-agent-git-discipline.md`) for the rationale and the triggering incident.

## NOT-FOR Boundaries

**What this skill should NOT handle:**

- **Runtime debugging**: For "my skill crashes when I run it" → Use debugging/troubleshooting skills instead
- **MCP server development**: For "build an MCP server that uses my skill" → Use MCP development skills instead  
- **Plugin architecture**: For "integrate this with VS Code/JetBrains" → Use IDE integration skills instead
- **General coding help**: For "help me write Python code" → Use language-specific programming skills instead
- **Infrastructure deployment**: For "deploy my skill to production" → Use deployment/DevOps skills instead

**When to delegate:**
- For skill hosting/distribution → Use deployment skills
- For testing frameworks beyond basic eval scripts → Use testing framework skills  
- For integration with external APIs → Use API integration skills
- For performance optimization of skill code → Use optimization/profiling skills

This skill focuses exclusively on the skill creation lifecycle: capturing requirements, drafting instructions, creating test cases, running evaluations, and iterating based on results.