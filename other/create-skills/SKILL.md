---
name: create-skills
description: Use when the system identifies a skill gap and needs to autonomously
  generate a new skill to fill it. Works with find-skills to ensure no duplicates.
domain: meta
author: oyi77
license: Apache-2.0
subdomain: meta-skills
tags:
- create
- meta-learning
- self-improvement
- skill-evolution
- skills
version: 1.0.0
category: meta
---

persona:
  name: "Grace Hopper"
  title: "The Compiler Creator - Master of Systematic Generation"
  expertise: ['Code Generation', 'Template Systems', 'Quality Validation', 'TDD Methodology']
  philosophy: "The most damaging phrase in the language is: Weve always done it this way. My mission: generate what doesnt exist yet."
  credentials: ['Created the first compiler', 'Rear Admiral US Navy', 'Pioneer of high-level languages', 'COBOL co-creator']
  principles: ['Check before creating - no duplicates', 'Validate quality before deploying', 'Test everything automatically', 'Document what you generate', 'Fail safely with rollback']

# Create Skills - Autonomous Skill Generation System

## Overview

Autonomously generate new skills when gaps are identified. Works as the **creation layer** of the self-evolving system - after find-skills confirms no existing solution create-skills generates one.

**Builds what doesnt exist** - every capability gap gets filled automatically!


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use

**Trigger phrases:**
- "create skills"
- "meta/find-skills reports no existing skill for a need"
- "meta/auto-evolve identifies a capability gap from performance data"
- "User explicitly requests "create a skill for X""


**Automatic Activation** when:
- meta/find-skills reports no existing skill for a need
- meta/auto-evolve identifies a capability gap from performance data
- User explicitly requests "create a skill for X"
- Multiple failed requests detected for the same capability
- User feedback suggests missing features

## When NOT to Use

- An existing skill already covers the need (use find-skills first)
- The request is too vague to generate a useful skill
- Quality cannot be validated (insufficient test cases)
- Safety validation fails for the generated content

## Skill Generation Process
1. Validate input and check prerequisites
2. Initialize required connections and contexts
3. Execute core operation with monitoring
4. Validate output against expected format
5. Deliver results and log execution summary


### Step 1: Gap Analysis

Before generating analyze the gap thoroughly:

1. Review failed user requests related to this gap
2. Check performance data for patterns
3. Identify the core capability needed (not just the symptom)
4. Determine the skill category (marketing trading devops etc.)
5. Estimate complexity: basic intermediate or advanced

### Step 2: Requirements Extraction

Transform the gap into concrete skill requirements:

- **Intent**: What the skill must accomplish
- **Triggers**: What user phrases activate the skill
- **Domain**: Which category the skill belongs to
- **Dependencies**: What other skills or tools it needs
- **Safety**: Any concerns or restrictions
- **Quality Bar**: Minimum validation score required

### Step 3: Template Selection

Choose the right template based on complexity:

| Complexity | Template | Includes |
|------------|----------|----------|
| Basic | basic.md | Overview triggers examples troubleshooting |
| Advanced | advanced.md | Full persona integration multi-step process advanced usage |
| Meta | meta.md | Orchestration of other skills system-level capability |

### Step 4: Content Generation

Generate the skill content following TDD:

1. **RED**: Define what the skill MUST do (acceptance criteria)
2. **GREEN**: Write minimal content that satisfies criteria
3. **REFACTOR**: Improve clarity completeness and quality

Generated content must include:
- Frontmatter (name description persona)
- Overview section
- When to Use / When NOT to Use
- Step-by-step process
- Integration section
- Examples (minimum 3)
- Troubleshooting

### Step 5: Quality Validation

Validate the generated skill passes all checks:

| Check | Weight | Pass Threshold |
|-------|--------|---------------|
| Structure complete | 30% | All required sections present |
| Content quality | 40% | Clear actionable no filler |
| Lint pass | 15% | No markdown errors |
| Integration | 15% | References to related skills |

**Minimum score to deploy: 85/100**

### Step 6: Testing and Deployment

1. Create test scenarios for the skill
2. Run skill in sandbox mode
3. Validate output quality
4. Copy to appropriate category directory
5. Update activation rules
6. Notify meta-skills of new capability
7. Log generation for audit trail

## Templates
```yaml
name: skill-name
description: Brief description of what this skill does
domain: category
tags: 
- [tag1
- tag2
- tag3]
```


### Basic Skill Template

```markdown
---
name: {skill-name}
description: Use when {trigger-conditions}
---

# {Skill Title}

## Overview
{Brief description}

## When to Use
- {Use case 1}
- {Use case 2}
- {Use case 3}

## When NOT to Use
- {Non-use case 1}

## How It Works
1. {Step 1}
2. {Step 2}
3. {Step 3}

## Examples
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```

### Example 1: {Title}
{Example content}

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Operation times out | Network or service issue | Check connectivity and retry |
| Permission denied | Missing credentials | Verify API keys and access tokens |
| Invalid output | Input format mismatch | Validate input against expected schema |

### {Problem 1}
- {Solution}
```

### Advanced Skill Template

```markdown
---
name: {skill-name}
description: Use when {trigger-conditions}
---
persona:
  name: "{Persona Name}"
  title: "{Persona Title}"
  expertise: ['{Expertise 1}', '{Expertise 2}']
  philosophy: "{Philosophy}"
  principles: ['{Principle 1}', '{Principle 2}', '{Principle 3}']

# {Skill Title}

## Overview
{Comprehensive description}

## When to Use
- {Detailed use cases}

## When NOT to Use
- {Detailed non-use cases}

## How It Works
{Multi-step process with code examples}

## Integration
{How this skill works with other skills}

## Advanced Usage
{Advanced features}

## Examples
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```

### Example 1: {Title}
### Example 2: {Title}
### Example 3: {Title}

## Troubleshooting
{Comprehensive troubleshooting}

## Configuration
{Configuration options}
```

## Integration with Meta-Skills
- Connects with existing toolchain via standard interfaces
- Supports webhook-based event notifications
- Compatible with CI/CD pipelines for automated workflows
- Provides structured output for downstream consumption


### With meta/find-skills

create-skills always checks find-skills first:
1. find-skills.search(gap) - any existing skill?
2. Found? Install existing (skip generation)
3. Not found? Proceed with generation

### With meta/auto-evolve

auto-evolve orchestrates the flow:
1. Detect gap from performance data
2. find-skills searches existing
3. Not found? create-skills generates new
4. Validate and deploy
5. Monitor results via performance-monitor

### With meta/performance-monitor

performance-monitor tracks generation metrics:
- Generation time
- Quality score of generated skills
- User satisfaction after deployment
- Skill utilization post-deployment

### With meta/auto-learner

auto-learner records generation patterns:
- What types of gaps are most common
- Which templates produce best quality
- Which domains need most new skills

## Examples
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


### Example 1: Generate Marketing Skill

Gap: Users requesting LinkedIn outreach automation not covered by existing skills

create-skills process:
1. Gap analysis: LinkedIn specific outreach not generic social media
2. Requirements: LinkedIn connection requests messaging profile scraping
3. Template: Advanced (needs persona for professional tone)
4. Content: Generate linkedin-outreach skill with business persona
5. Quality: Score 88/100 - passes threshold
6. Deploy: Install to marketing/ category activate

### Example 2: Generate DevOps Skill

Gap: 15 failed requests for Kubernetes deployment help

create-skills process:
1. Gap analysis: K8s deployment automation missing
2. Requirements: Deploy scale rollback monitor K8s resources
3. Template: Advanced (complex multi-step process)
4. Content: Generate k8s-deploy skill with DevOps engineer persona
5. Quality: Score 92/100 - excellent
6. Deploy: Install to devops/docker/ category activate

### Example 3: Generate Meta Skill

Gap: System needs pattern recognition across skill categories

create-skills process:
1. Gap analysis: Cross-category pattern detection missing
2. Requirements: Scan skills find common patterns suggest improvements
3. Template: Meta (orchestrates other skills)
4. Content: Generate cross-category-patterns meta-skill
5. Quality: Score 85/100 - passes threshold
6. Deploy: Install to meta/ category activate

## Configuration

```json
{
  "defaultTemplate": "basic",
  "qualityThreshold": 85,
  "testCoverageRequired": 90,
  "autoTest": true,
  "maxRetries": 3,
  "templates": {
    "basic": "templates/basic.md",
    "advanced": "templates/advanced.md",
    "meta": "templates/meta.md"
  }
}
```

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Operation times out | Network or service issue | Check connectivity and retry |
| Permission denied | Missing credentials | Verify API keys and access tokens |
| Invalid output | Input format mismatch | Validate input against expected schema |


### Generated skill quality too low
- Review gap analysis for clarity
- Try advanced template instead of basic
- Add more specific requirements
- Increase maxRetries for regeneration

### Duplicate skill detected
- find-skills should catch this before generation
- If missed: delete generated skill install existing one
- Review find-skills search terms for gaps

### Generation fails
- Check gap description is specific enough
- Try simpler template
- Break complex skill into smaller skills
- Review dependency requirements

### Generated skill doesnt work as expected
- Review and refine acceptance criteria
- Add more test scenarios
- Check integration with related skills
- Consider manual refinement

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Meta-skill changes are applied without measuring performance impact
- Agent does not verify that changes maintain backward compatibility
- Watch for shortcuts and skipped steps

## Verification

After generating a new skill, confirm:

- [ ] Frontmatter complete (name, description, persona)
- [ ] All required sections present (Overview, When to Use, Process, Verification)
- [ ] Quality score ≥ 85/100
- [ ] Skill tested in sandbox mode
- [ ] Successfully copied to category directory
- [ ] Related skills cross-referenced
- [ ] User notified of new capability

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
