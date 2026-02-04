---
name: skill-recommender
description: Analyzes codebases and conversation context to recommend relevant existing skills and suggest valuable custom skills to create. Use when exploring a project for the first time, when asked what skills would be useful, or when seeking to optimize workflow for a specific codebase.
---

# Skill Recommender

## Overview

This skill analyzes directory structure, file types, frameworks, tech stack, and conversation context to provide comprehensive skill recommendations. It identifies which existing skills would be most valuable for the current project and suggests custom skills that could streamline project-specific workflows.

## When to Use This Skill

Invoke this skill when:
- User asks "what skills would be helpful for this project?"
- User requests skill recommendations for a directory
- User wants to optimize their workflow for a codebase
- Exploring a new project and wanting to understand applicable skills
- User asks "are there skills that could help with [project type]?"

## Analysis Workflow

This skill follows an automatic analysis workflow that gathers comprehensive information, then provides detailed recommendations.

### Step 1: Automated Codebase Analysis

Run the analysis script to gather comprehensive codebase information:

```bash
python3 scripts/analyze_codebase.py <directory>
```

This detects:
- File types and extensions
- Programming languages
- Frameworks and libraries
- Project structure patterns
- Tech stack components

**Output interpretation:**
- Review detected frameworks, languages, and project types
- Note file categories and their prevalence
- Identify patterns that suggest specific workflows

### Step 2: Directory Structure Scan

For additional context about project organization, optionally run:

```bash
python3 scripts/scan_directory.py <directory>
```

This provides:
- Simplified directory tree
- Important configuration files
- Project structure overview

Use this when you need to understand project organization or when automated analysis needs clarification.

### Step 3: Conversation Context Integration

Review recent conversation history to understand:
- User's stated goals and current tasks
- Technologies they're working with
- Problems they're trying to solve
- Workflows they've mentioned
- Pain points or repetitive tasks

Combine this context with codebase analysis to prioritize recommendations.

### Step 4: Pattern Matching

Match detected patterns against known skill mappings:

1. **Load analysis patterns reference** when you need detailed pattern-to-skill mappings:
   ```
   See references/analysis-patterns.md for comprehensive pattern matching
   ```

2. **Cross-reference findings:**
   - Match detected frameworks to relevant skills
   - Identify document processing needs
   - Spot testing and quality patterns
   - Recognize infrastructure patterns
   - Note documentation patterns

3. **Prioritize by relevance:**
   - Current user focus and goals
   - Frequency of detected patterns
   - Potential time savings
   - Workflow complexity

### Step 5: Generate Recommendations

Produce a comprehensive recommendation report with:

#### A. Existing Skills Recommendations

For each recommended skill:
- **Skill name** and identifier
- **Why it's relevant** to this project
- **Specific use cases** based on detected patterns
- **Priority level** (High/Medium/Low)

Example format:
```markdown
### Recommended Existing Skills

#### High Priority

**`document-skills:xlsx`** - Spreadsheet creation and analysis
- **Detected:** 45 .xlsx files, openpyxl dependency
- **Use cases:**
  - Analyze sales data spreadsheets
  - Generate financial reports from data
  - Process CSV exports into formatted Excel
- **Trigger examples:** "Analyze sales-report.xlsx", "Create summary spreadsheet from this data"

**`example-skills:webapp-testing`** - Frontend testing toolkit
- **Detected:** React application with Jest, Playwright in package.json
- **Use cases:**
  - Test user flows in the dashboard
  - Verify component rendering
  - Debug UI behavior issues
- **Trigger examples:** "Test the login flow", "Check if the form validates correctly"
```

#### B. Custom Skill Suggestions

For suggested custom skills, use the templates and guidelines from `references/skill-suggestion-examples.md`.

Load this reference when generating custom skill suggestions:
```
See references/skill-suggestion-examples.md for suggestion templates and examples
```

For each suggestion, provide:
- **Skill name** (descriptive, kebab-case)
- **Purpose** (1-2 sentences)
- **Key features** (3-5 specific capabilities)
- **When to use** (trigger scenarios)
- **Bundled resources** (scripts, references, assets needed)
- **Example use cases** (2-3 realistic scenarios)

Prioritize custom skill suggestions by:
1. Immediate applicability to user's goals
2. Potential time savings
3. Workflow complexity that would benefit from automation
4. Availability of resources (templates, schemas, etc.)

Example format:
```markdown
### Suggested Custom Skills

#### `api-integration-helper`

**Purpose:** Streamline integration with the company's internal REST API, handling authentication, common queries, and data transformation.

**Key Features:**
- Auto-authenticate with API credentials
- Query common endpoints (users, orders, products)
- Transform API responses to required formats
- Handle error cases and retries

**When to Use:**
- When fetching data from internal API
- When testing API endpoints
- When building features that consume API data

**Bundled Resources:**
- `references/api-docs.md` - Internal API documentation
- `references/schemas.md` - Request/response schemas
- `scripts/api_client.py` - Python client helper

**Example Use Cases:**
1. "Get all orders from the last month"
2. "Fetch user profile data for user ID 12345"
3. "Update product inventory via API"
```

### Step 6: Present Findings

Deliver a comprehensive analysis report with the following structure:

```markdown
# Skill Recommendations for [Project Name]

## Codebase Overview
[Brief summary of project type, primary languages, key frameworks]

## Analysis Summary
- **Total Files:** [count]
- **Primary Languages:** [languages with file counts]
- **Key Frameworks:** [frameworks detected]
- **Project Type:** [web app, data science, etc.]

## Recommended Existing Skills

### High Priority
[Skills that are immediately relevant and frequently useful]

### Medium Priority
[Skills that are relevant for specific tasks]

### Low Priority
[Skills that might be occasionally useful]

## Suggested Custom Skills

[2-5 custom skill suggestions, prioritized by value]

## Next Steps

1. Install recommended skills:
   ```bash
   claude skill install [skill-identifiers]
   ```

2. Consider creating custom skills for:
   - [Top priority suggestion]
   - [Second priority suggestion]

3. Start using skills by:
   - [Specific actionable suggestion based on user's context]
```

## Best Practices

### Analysis Depth

- **Quick scan:** Run only `analyze_codebase.py` for basic recommendations
- **Comprehensive:** Run both scripts and review references for detailed analysis
- **Context-heavy:** Spend more time on conversation context integration when user has specific goals

### Recommendation Quality

- **Be specific:** Provide concrete use cases, not generic descriptions
- **Be actionable:** Users should know exactly how to use each recommendation
- **Be realistic:** Only suggest skills that genuinely add value
- **Be prioritized:** Rank by actual relevance, not quantity

### Custom Skill Suggestions

- **Focus on patterns:** Suggest skills for workflows that repeat
- **Require specifics:** Need enough information to define useful behavior
- **Provide templates:** Use skill-suggestion-examples.md templates consistently
- **Consider resources:** Ensure suggested bundled resources are feasible

### Conversation Integration

Pay special attention to:
- **User's current task:** What they're working on right now
- **Mentioned pain points:** Frustrations or time-consuming processes
- **Technology references:** Tools and frameworks they discuss
- **Workflow patterns:** How they describe their process

## Handling Edge Cases

### Large Codebases

For projects with >10,000 files:
- Use `--depth` parameter to limit analysis depth
- Focus on root-level and key subdirectories
- Prioritize patterns by frequency and importance

### Monorepos

For monorepo structures:
- Analyze each major component separately
- Note which skills apply to which parts
- Suggest skills for monorepo management if relevant

### Unfamiliar Tech Stacks

When encountering unknown frameworks/patterns:
- Describe the pattern characteristics clearly
- Suggest general-purpose skills that might help
- Note the gap as a potential custom skill opportunity

### Minimal Conversation Context

When conversation history is limited:
- Rely more heavily on codebase analysis
- Provide broader recommendations
- Note that priorities can be refined with more context
- Ask user about their goals if appropriate

## Resources

This skill includes bundled resources for analysis and recommendation generation:

### scripts/

**`analyze_codebase.py`** - Comprehensive codebase analysis tool
- Detects file types, languages, frameworks, and patterns
- Outputs structured analysis data
- Use: `python3 scripts/analyze_codebase.py <directory>`

**`scan_directory.py`** - Quick directory structure scanner
- Provides simplified directory tree
- Identifies important configuration files
- Use: `python3 scripts/scan_directory.py <directory>`

### references/

**`analysis-patterns.md`** - Pattern-to-skill mapping reference
- Maps common codebase patterns to relevant skills
- Organized by category (documents, web, data, DevOps, etc.)
- Load when matching detected patterns to skills

**`skill-suggestion-examples.md`** - Custom skill suggestion templates
- Templates for different skill types
- Example suggestions with full details
- Guidelines for quality suggestions
- Load when generating custom skill recommendations
