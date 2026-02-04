---
name: project-type-determination
version: 1.0.0
description: |
  Determines project type from context to configure analysis thresholds.
  Checks prompt, scans documents, or asks user if type cannot be inferred.
  Outputs project_type for use by python-plan-optimization skill.
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Project Type Determination

Determine the project type to configure appropriate analysis thresholds for the python-plan-optimization skill.

## Core Mission

Identify the project type through a 3-step workflow:
1. Check if type was explicitly provided in the invoking prompt
2. Scan plan files for explicit project type statements
3. Ask the user if type cannot be determined

**Deliverable**: Project type classification with source attribution.

## Supported Project Types

| Type | Key Characteristic | Analysis Mode |
|------|-------------------|---------------|
| poc | Proof of concept, throw-away code | Critical issues only |
| mvp | Minimum viable product, ship fast | Critical + High issues |
| private | Personal/learning project | All issues, educational |
| enterprise | Production team project | All issues, verification required |
| opensource | Public library/tool | All issues, types + docs required |

## Workflow

### Step 1: Check Invoking Prompt

Look for explicit project type in the user's request:

**Direct Mentions:**
- "Analyze my **enterprise** project's PLAN.md"
- "Review this **MVP** plan"
- "Check my **POC** code in design.md"
- "Review my **open source** library"
- "Analyze my **personal** project"

**Pattern Matching:**

| Pattern | Detected Type |
|---------|---------------|
| `enterprise`, `production` | enterprise |
| `mvp`, `minimum viable` | mvp |
| `poc`, `proof of concept`, `prototype`, `spike` | poc |
| `open source`, `public library`, `pypi`, `pip install` | opensource |
| `personal`, `private`, `learning`, `experiment` | private |

**If type found in prompt:**
```yaml
project_type: [detected type]
source: prompt
```
→ **Done. Skip to Output.**

**If not found:** Continue to Step 2.

---

### Step 2: Scan Documents for Explicit Statements

Read the target documents and search for explicit project type declarations.

**Explicit Statement Patterns:**

| Type | Patterns to Match |
|------|-------------------|
| poc | "This is a (POC\|proof of concept\|prototype)", "POC for...", "Spike to validate..." |
| mvp | "MVP (for\|development\|plan)", "Minimum viable product", "MVP plan for..." |
| private | "Personal project", "Private project", "Learning exercise", "Experiment to..." |
| enterprise | "Enterprise (system\|deployment\|project)", "Production (system\|deployment)", "Enterprise-grade" |
| opensource | "Open source (library\|package\|project)", "Public (library\|package\|API)", "PyPI package", "Published to PyPI", "pip install" |

**Search Strategy:**
1. Use Grep to search document(s) for type patterns
2. Look in document headers, introductions, and project descriptions
3. Check for explicit statements like "This is a plan for an MVP"

**If explicit statement found:**
```yaml
project_type: [detected type]
source: document
```
→ **Done. Skip to Output.**

**If not found:** Continue to Step 3.

---

### Step 3: Ask User

When project type cannot be determined from context, ask the user.

**First, output explanation text:**

> I could not determine the project type from the prompt or documents. The project type affects analysis depth:
> - **POC**: Critical issues only (throw-away code)
> - **MVP**: Critical + High (ship fast, track debt)
> - **Private**: All suggestions (learning focus)
> - **Enterprise**: Strict analysis, verification required
> - **Open Source**: API stability, required types & docs

**Then invoke AskUserQuestion:**

```yaml
questions:
  - question: "What type of project is this?"
    header: "Project Type"
    multiSelect: false
    options:
      - label: "Private (Recommended)"
        description: "Full analysis with all suggestions - best for learning and personal projects"
      - label: "Open Source"
        description: "API-focused with required type hints and documentation"
      - label: "Enterprise"
        description: "Strict analysis with verification required for all claims"
      - label: "MVP"
        description: "Balanced analysis - critical and high priority issues only"
      - label: "POC"
        description: "Minimal analysis - only critical blocking issues"
```

**Map user selection to type:**

| Selection | Type |
|-----------|------|
| Private (Recommended) | private |
| Open Source | opensource |
| Enterprise | enterprise |
| MVP | mvp |
| POC | poc |
| Other (custom input) | Parse or default to private |

**After user responds:**
```yaml
project_type: [selected type]
source: user
```

---

## Output Format

Always output in this format for the optimization skill to parse:

```yaml
project_type: [poc|mvp|private|enterprise|opensource]
source: [prompt|document|user]
```

**Example Outputs:**

```yaml
# Type found in prompt
project_type: enterprise
source: prompt
```

```yaml
# Type found in document
project_type: mvp
source: document
```

```yaml
# User selected type
project_type: private
source: user
```

## Constraints

**DO:**
- Check prompt first (fastest path)
- Use exact pattern matching for document scanning
- Present explanation before asking user
- Default to "private" for ambiguous "Other" responses

**DO NOT:**
- Guess project type from code characteristics
- Infer type from file structure or naming
- Make assumptions about team size or deployment
- Skip the user question when type is ambiguous

## Success Criteria

Skill succeeds when:
- Project type is determined through one of three methods
- Output contains valid `project_type` and `source`
- User interaction (if needed) provides clear explanation before question
