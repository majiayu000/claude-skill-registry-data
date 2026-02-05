---
name: skill-learning
description: Extract actionable knowledge from external sources and enhance existing skills using 4-tier novelty framework. Use when learning from URLs, documentation, or codebases. Use for enhancing existing skills or creating new ones from external patterns.
---

# Skill Learning Methodology

## Overview

Transform external knowledge (URLs, files, code) into skill enhancements. Uses novelty-detection to filter training data, matches insights to existing skills, proposes concrete additions.

**Core Loop**: Source → Extract → Match → Preview → Approve → Apply → Next

## Phase 1: Source Processing

### URL Sources
# OPTIMIZATION: Check for llms.txt first (10x faster when exists)
Detection order: {base_url}/llms-full.txt → llms.txt → llms-small.txt
If found: Use directly, skip full page scraping

Primary: WebFetch(url, "Extract technical patterns, gotchas, and implementation details")
Fallback: WebFetch("https://r.jina.ai/{url}", ...) if primary blocked

### Batch Processing Pattern
# When analyzing skill updates across 100+ skills
Strategy: Parallel Read operations for all SKILL.md files in one tool call block
Benefit: Claude Code processes parallel independent operations in one response
Anti-pattern: Sequential 100+ Read calls (timeout risk)

Example:
  Read(/skills/skill-1/SKILL.md)
  Read(/skills/skill-2/SKILL.md)
  ...
  Read(/skills/skill-100/SKILL.md)  # All in one <function_calls> block

### File Sources
Single file: Read(file_path)
Simple directory: Glob("*.md", path) + parallel Read
Code files: Extract comments, docstrings, error handling patterns

### Local Directory Discovery (Plugin/Marketplace Structures)
# Step 1: Detect directory structure
Check for common patterns:
  - AGENTS.md at root → Parse for skill paths (canonical source)
  - plugin.json files → Check for skills/ subdirectory
  - Flat skills/*.md → Direct skill files
  - Nested skills/*/SKILL.md → Skill subdirectories

# Step 2: Discovery commands by structure type

## Pattern A: AGENTS.md manifest (preferred)
Read({dir}/AGENTS.md)
Parse <available_skills> section → extract relative paths
Example paths: "hf-llm-trainer/skills/model-trainer/SKILL.md"

## Pattern B: Plugin directories with nested skills
Glob("*/skills/*/SKILL.md", path={dir})
OR
Glob("*/skills/*/*.md", path={dir})

## Pattern C: Flat skill collection
Glob("skills/*/SKILL.md", path={dir})

## Pattern D: Mixed/unknown structure
Glob("**/SKILL.md", path={dir})  # Find all SKILL.md recursively

# Step 3: Parallel read all discovered skills
For each discovered path:
  Read({full_path})
All reads in single <function_calls> block for parallelism

### Plugin Directory Example (Illustrative)
Given: ~/.claude/plugins/marketplaces/example-skills/

Step 1: Read AGENTS.md → Discover skill paths:
  - plugin-a/skills/database-migrations/SKILL.md
  - plugin-b/skills/api-testing/SKILL.md
  - plugin-c/skills/docker-compose/SKILL.md

Step 2: Parallel Read all discovered skills

Step 3: For each skill → Extract insights → Match/propose enhancements

### Directory Structure Detection Heuristics
| Indicator | Structure Type | Discovery Command |
|-----------|---------------|-------------------|
| AGENTS.md exists | Manifest-based | Parse AGENTS.md |
| plugin.json in subdirs | Plugin structure | Glob("*/skills/*/SKILL.md") |
| skills/ at root | Flat collection | Glob("skills/*/SKILL.md") |
| Only *.md at root | Simple docs | Glob("*.md") |
| None of above | Unknown | Glob("**/SKILL.md") |

### Repository Documentation Discovery

When learning from a code repository (not a skills/plugin directory):

# Step 1: Identify repo type
Check for indicators:
  - package.json → Node.js/TypeScript project
  - go.mod → Go project
  - Cargo.toml → Rust project
  - pyproject.toml → Python project

# Step 2: Find documentation files (priority order)
1. README.md, CONTRIBUTING.md, ARCHITECTURE.md (root)
2. docs/*.md, documentation/*.md
3. src/**/*.md (inline docs)
4. default/content/**/*.json (config/presets)
5. Key source files with heavy comments

# Step 3: Find schema/type definitions
- TypeScript: **/*.d.ts, **/types.ts, **/interfaces.ts
- Go: **/*_types.go, **/*_model.go
- JSON Schema: **/*.schema.json
- Validators: **/validator*.js, **/schema*.js

# Step 4: Find example/preset files
- **/examples/*, **/presets/*, **/templates/*
- **/default/*, **/samples/*
- **/*.example.*, **/*.sample.*

### Repository Learning Example (Express API)
Given: ~/projects/my-api

Step 1: Detect Node.js project (package.json exists)

Step 2: Read documentation:
  - README.md, CONTRIBUTING.md

Step 3: Read schemas/validators:
  - src/validators/*.js → Request/response validation schemas
  - src/models/*.js → Data model definitions

Step 4: Read examples/presets:
  - config/*.json → Environment configurations
  - examples/*.json → Sample request/response payloads

Step 5: Read key implementation files:
  - src/middleware/auth.js → Authentication flow
  - src/middleware/errorHandler.js → Error handling patterns

Step 6: Extract patterns → Create skills:
  - express-validation-patterns (from validators)
  - api-error-handling (from errorHandler)
  - jwt-auth-flow (from auth middleware)

### Repo-Specific Extraction Targets

| Repo Type | Key Extraction Targets |
|-----------|----------------------|
| UI Framework | Component patterns, state management, hooks |
| API/Backend | Endpoint structure, middleware, validation |
| AI/LLM App | Prompt templates, context assembly, memory |
| CLI Tool | Command structure, flags, output formatting |
| Library | Public API, usage patterns, configuration |
| Game/Interactive | State machines, event systems, save/load |

### Repo Learning vs Skill Learning

**Use Repo Learning when:**
- Analyzing a codebase for patterns to adopt
- Extracting schemas/formats (e.g., validation schemas, API specs)
- Learning from reference implementations
- Building NEW skills FROM a repo's patterns

**Use Skill/URL Learning when:**
- Enhancing EXISTING skills with insights
- Learning from documentation/articles
- Copying skills from plugin marketplaces

### Content Cleaning
- Strip navigation, ads, boilerplate
- Preserve code blocks verbatim
- Extract headings as domain signals
- Identify technology keywords (frameworks, libraries, APIs)

## Phase 2: Knowledge Extraction

**MANDATORY: Apply novelty-detection framework**

Skill: novelty-detection

### Tier Classification
| Tier | Include? | Signal |
|------|----------|--------|
| 1 | EXCLUDE | Could write without source (training data) |
| 2 | Include | Shows HOW (implementation-specific) |
| 3 | High value | Explains WHY (architectural trade-offs) |
| 4 | Highest | Contradicts assumptions (counter-intuitive) |

### The Novelty Test

**Ask yourself**: "Could I have written this WITHOUT reading the source?"

- If YES → Tier 1 (EXCLUDE)
- If NO → Continue to Tier 2-4 classification

### Calibration Examples

**API Documentation Analysis:**
```
Claim: "OpenAI provides an API for generating text"
→ Tier 1 ❌ — Generic, could write from training data

Claim: "Responses API uses max_output_tokens instead of max_tokens"
→ Tier 2 ✅ — Specific parameter name (HOW)

Claim: "Reasoning models put chain-of-thought in reasoning_content array,
        not content — must sum both for billing"
→ Tier 4 ✅✅✅ — Counter-intuitive, prevents billing surprise
```

**Database Performance:**
```
Claim: "Create indexes on foreign key columns for faster joins"
→ Tier 1 ❌ — Generic DBA advice

Claim: "PostgreSQL partial indexes reduce size 60%, improve write perf 40%"
→ Tier 2 ✅ — Specific feature with quantified benefit

Claim: "Covering indexes avoid heap lookups (3x faster reads, 15% slower writes)"
→ Tier 3 ✅✅ — Quantified trade-off, explains WHY

Claim: "JSONB GIN indexes do NOT support ORDER BY on JSON fields"
→ Tier 4 ✅✅✅ — Contradicts expectation, prevents bug
```

**Framework Patterns:**
```
Claim: "React uses a virtual DOM for efficient updates"
→ Tier 1 ❌ — Training data, everyone knows this

Claim: "Next.js App Router requires 'use client' directive for useState"
→ Tier 2 ✅ — Specific requirement (HOW)

Claim: "Server Components reduce JS bundle by 60% but can't use client state"
→ Tier 3 ✅✅ — Trade-off with quantification (WHY)

Claim: "generateStaticParams runs at BUILD time, not request time —
        dynamic data causes 404s"
→ Tier 4 ✅✅✅ — Contradicts mental model, prevents production bug
```

### Insight Structure
{
  "tier": 2,
  "domain": "sveltekit",
  "pattern": "Server-only load with +page.server.ts",
  "insight": "Data fetching in +page.server.ts runs only on server, +page.ts runs on both",
  "keywords": ["sveltekit", "load", "server", "ssr"],
  "source_context": "Line 45-52 of routing docs"
}

### Quality Filter
- Zero Tier 1 leakage (absolute)
- Minimum 3 Tier 2-4 insights per source (or skip)
- Each insight must have domain + keywords

## Phase 3: Skill Matching

### Discovery
# Find all skills
Glob("skills/*/SKILL.md")

### Matching Algorithm
1. **Exact domain match**: Insight domain === skill name (score: 100)
2. **Keyword overlap**: Insight keywords ∩ skill description/when_to_use (score: 60-90)
3. **Technology alignment**: Same framework/library family (score: 40-60)
4. **No match**: Score <40 → propose new skill

## Phase 4: Enhancement Proposal

### For Each Match (score >= 40)

**1. Read current skill**
Read(skills/{skill-name}/SKILL.md)

**2. Identify target section**
| Insight Type | Target Section |
|--------------|----------------|
| Quick fact | Quick Reference table |
| Pattern + example | Patterns / Examples |
| Gotcha / warning | Anti-Patterns / Common Mistakes |
| Workflow step | Process / Workflow |
| Validation rule | Checklist |

**3. Draft enhancement**
- Preserve existing structure exactly
- Add insight in appropriate format for section
- Include source attribution: `<!-- Source: {url/file} -->`

**4. CLEAR Validation**
Apply skills-enhancer CLEAR framework:
- C: Word count still <5000?
- L: Keywords in right places?
- E: Example shows transformation?
- A: Actionable pattern named?
- R: No duplication, uses references?

## Phase 5: User Approval

### For Each Enhancement
Present:
1. Skill name being enhanced
2. Insight being added (with tier)
3. Diff preview
4. Word count impact

Ask: "Apply this enhancement? [y/n/edit]"

### Response Handling
- **y (approve)**: Apply via Edit tool
- **n (reject)**: Skip, continue to next
- **edit**: User modifies, then apply

## Phase 6: New Skill Proposal

### When No Match Found
Insights with no match (score <40):
- Domain: {domain}
- Keywords: {keywords}
- Sample insight: {insight}

Propose new skill? [y/n]

### If Approved
**Generate using skill-creation methodology:**
Skill: skill-creation

## Phase 7: Loop Control

### After Each Source
Summary:
- Insights extracted: X (Tier 2: Y, Tier 3: Z, Tier 4: W)
- Skills enhanced: [list]
- New skills created: [list]
- Rejected: [count]

Next source? (file path, URL, or 'done')

## Quality Gates

### Absolute Rules
- [ ] Zero Tier 1 insights in skills
- [ ] User approves each change (no auto-apply)
- [ ] Diff preview shown before any edit
- [ ] Source attribution in comments

### Warning Triggers
- Skill exceeds 5000 words → suggest splitting
- Large source (10K+ pages) → create router skill
- Insight duplicates existing content → skip
- CLEAR validation fails → revise before applying

## Quick Reference

| Step | Action | Gate |
|------|--------|------|
| 1. Source | WebFetch/Read/Discover | Content extracted? |
| 2. Extract | novelty-detection | >=3 Tier 2-4 insights? |
| 3. Match | Glob + score | Any score >=40? |
| 4. Propose | Draft + CLEAR | Validation passes? |
| 5. Preview | Show diff | User understands? |
| 6. Apply | Edit | User approves? |
| 7. Loop | Next source | Continue or done? |
