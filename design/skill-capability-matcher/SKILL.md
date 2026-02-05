---
name: skill-capability-matcher
description: |
  This skill should be used when matching user requirements to available skills from a
  compiled registry. It receives a skill registry (from registry-loader) and user requirements,
  then scores each skill based on capability alignment, producing prioritized matches with
  confidence scores.

  Triggers: "match skills to requirements", "find relevant skills for workflow", "which skill
  handles X", "score skill capabilities", "/build" (after registry load), "find skills for
  this task", "match my requirements to skills".

  Second step in looplia workflow building pipeline: takes user requirements and skill registry,
  recommends skill sequences with missions. Designs one workflow step → one skill-executor
  → multiple skills orchestration pattern.
model: haiku
---

# Skill Capability Matcher

Match natural language requirements to available skills, designing an optimal workflow step sequence.

## Purpose

Parse user's workflow description, understand their intent, and recommend which skills should handle each part of the workflow. Output includes step IDs, skill names, missions, and data flow.

## Process

### Step 1: Parse Requirements

Extract from the user's description:

**Input Types:**
- video transcript
- audio transcript
- article/blog post
- documentation
- raw text
- structured data (JSON/YAML)

**Processing Goals:**
- analyze (deep understanding)
- summarize (condensation)
- generate (create new content)
- transform (change format)
- extract (pull specific data)
- validate (check correctness)

**Output Format:**
- JSON structure
- Markdown document
- Summary text
- Structured data

### Step 2: Load Registry

Read the plugin registry from registry-loader output (v0.7.0):

```json
{
  "plugins": [...],
  "summary": { "totalSkills": N, "installedSkills": N, "availableSkills": N }
}
```

Build a capability index from skill descriptions and inferred capabilities.
Include `installed` status when scoring - prefer installed skills for immediate execution.

### Step 3: Match Capabilities

Score each skill by:
1. **Description match** - Does skill description align with requirements?
2. **Capability overlap** - Do inferred capabilities match processing goals?
3. **Input/output compatibility** - Can skill handle input type and produce expected output?

### Step 4: Design Step Sequence

For each matched skill:
1. Create a step ID (kebab-case, descriptive)
2. Determine dependencies (`needs:`)
3. Write a mission description (what to accomplish)
4. Define data flow (input → output)

### Step 5: Recommend Sequence

Order skills logically:
1. Analysis skills first (understand content)
2. Generation/transformation skills second
3. Assembly/output skills last

Ensure proper data dependencies.

### Step 6: Flag Gaps

If requirements can't be fully satisfied:
- List unmatched capabilities as gaps
- Suggest creating custom skills if needed
- Indicate if workflow is partial

## Input

Provide:
1. User's natural language description
2. Registry JSON from plugin-registry-scanner

## Output Schema

```json
{
  "requirements": {
    "inputType": "video transcript",
    "goals": ["extract key points", "generate outline"],
    "outputFormat": "structured JSON"
  },
  "recommendations": [
    {
      "skill": "media-reviewer",
      "suggestedStepId": "analyze-content",
      "goalId": "analyze",
      "matchScore": 0.92,
      "capabilities": ["content analysis", "theme extraction"],
      "mission": "Deep analysis of video transcript. Extract key themes, quotes, and narrative structure.",
      "rationale": "Primary skill for content understanding"
    },
    {
      "skill": "idea-synthesis",
      "suggestedStepId": "generate-ideas",
      "goalId": "generate",
      "matchScore": 0.85,
      "capabilities": ["idea generation", "hooks and angles"],
      "mission": "Generate hooks, angles, and questions from the analysis. Read user profile for personalization.",
      "rationale": "Creates engaging content ideas from analysis"
    }
  ],
  "suggestedSequence": ["analyze-content", "generate-ideas", "build-output"],
  "dataFlow": {
    "analyze-content": {
      "needs": [],
      "provides": "analysis.json"
    },
    "generate-ideas": {
      "needs": ["analyze-content"],
      "provides": "ideas.json"
    },
    "build-output": {
      "needs": ["analyze-content", "generate-ideas"],
      "provides": "output.json"
    }
  },
  "gaps": [],
  "customSkillNeeded": false,
  "clarificationNeeded": true,
  "clarifications": {
    "sections": [
      {
        "id": "input",
        "title": "Input",
        "completed": false,
        "questions": [
          {
            "id": "content-type",
            "text": "What type of content will this workflow process?",
            "type": "single-select",
            "options": [
              { "id": "video", "label": "Video transcripts", "inferred": true },
              { "id": "audio", "label": "Audio transcripts" },
              { "id": "text", "label": "Text articles" },
              { "id": "web", "label": "Web pages (fetched via search)" }
            ],
            "reason": "Inferred 'video' from description, confirm or change"
          }
        ]
      },
      {
        "id": "goals",
        "title": "Goals",
        "completed": false,
        "questions": [
          {
            "id": "primary-goal",
            "text": "What are the primary goals for this workflow?",
            "type": "multi-select",
            "options": [
              { "id": "analyze", "label": "Analyze and extract key insights" },
              { "id": "summarize", "label": "Create structured summaries" },
              { "id": "generate", "label": "Generate creative content ideas" },
              { "id": "document", "label": "Build comprehensive reports" }
            ]
          },
          {
            "id": "depth",
            "text": "How deep should the analysis be?",
            "type": "single-select",
            "options": [
              { "id": "quick", "label": "Quick overview (1-2 key points)" },
              { "id": "standard", "label": "Standard analysis (5-7 key points)" },
              { "id": "deep", "label": "Deep analysis (comprehensive)" }
            ]
          }
        ]
      },
      {
        "id": "output",
        "title": "Output",
        "completed": false,
        "questions": [
          {
            "id": "format",
            "text": "What output format do you need?",
            "type": "single-select",
            "options": [
              { "id": "json", "label": "Structured JSON" },
              { "id": "markdown", "label": "Markdown document" },
              { "id": "both", "label": "Both JSON and Markdown" }
            ]
          }
        ]
      },
      {
        "id": "review",
        "title": "Review",
        "completed": false,
        "questions": []
      }
    ]
  }
}
```

## Scoring Guidelines

| Match Type | Score |
|------------|-------|
| Exact capability match | 0.9-1.0 |
| Strong description overlap | 0.7-0.9 |
| Partial capability match | 0.5-0.7 |
| Weak/inferred match | 0.3-0.5 |
| No clear match | < 0.3 |

## Scoring Rubric

Use these concrete criteria when assigning scores:

### Relevance Score (Primary Factor)
- **90-100**: Skill's primary purpose directly addresses requirement
- **70-89**: Skill clearly capable of addressing requirement
- **50-69**: Skill partially addresses requirement
- **30-49**: Skill tangentially related
- **0-29**: Minimal or no relevance

### Completeness Score
- **90-100**: Skill fully addresses all aspects of requirement
- **70-89**: Skill addresses most aspects, minor gaps
- **50-69**: Skill addresses core need, notable gaps
- **Below 50**: Significant portions unaddressed

### Specificity Score
- **90-100**: Skill specifically designed for this exact use case
- **70-89**: Skill well-suited for use case category
- **50-69**: General-purpose skill applicable to use case
- **Below 50**: Very general skill with broad applicability

### Confidence Calculation

```
confidence = (relevance * 0.5) + (completeness * 0.3) + (specificity * 0.2)
```

**Minimum threshold: 60%** - Skills below this should not be recommended.

## Semantic Matching Guidelines

Match requirements to skills beyond simple keyword matching:

### 1. Synonym Recognition
Match conceptually equivalent terms:
- "authentication" ↔ "login", "session management", "user verification"
- "database" ↔ "data persistence", "storage", specific ORMs
- "analyze" ↔ "review", "examine", "inspect", "assess"
- "generate" ↔ "create", "produce", "synthesize", "build"

### 2. Hierarchical Matching
Understand skill scope and specificity:
- General skill may satisfy specific requirement (e.g., "api-client" for "REST calls")
- Prefer specific skill over general when available (e.g., "stripe-integration" over "payment-api")

### 3. Intent Extraction
Focus on what user wants to accomplish, not just keywords:
- "I need to send emails" → match email/notification skills
- "Process video content" → match media-reviewer, not just skills with "video" in name
- "Build a report from data" → match assembly/documentation skills

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No matches above 60% threshold | Return empty `recommendations[]` with `gaps` listing unmet needs |
| Multiple skills with identical scores | Prefer more specific skill (higher specificity score) |
| Ambiguous user requirements | Set `clarificationNeeded: true` with targeted questions |
| Skill matches multiple requirements | Include once with highest-scoring requirement as primary |
| Installed vs available skills | Prefer installed skills when scores are within 10% |

## Mission Writing Guidelines

Each mission should:
- Start with an action verb (Analyze, Extract, Generate, Create, Transform)
- Describe the specific goal for this step
- Mention key outputs expected
- Reference context from previous steps if applicable
- Be 2-4 sentences

**Good mission example:**
```
Deep analysis of video transcript. Extract key themes, important quotes with timestamps, and narrative structure. Focus on insights that would interest the user based on their profile.
```

**Bad mission example:**
```
Analyze the content.
```

## Important Rules

1. **Skills-first** - Never recommend agents, only skills
2. **Include missions** - Every recommendation must have a detailed mission
3. **Score realistically** - Don't inflate match scores
4. **Complete data flow** - Ensure all dependencies are resolvable
5. **Flag gaps honestly** - Report capabilities that can't be matched
6. **Include goalId** - Each recommendation must have a `goalId` linking it to a clarification goal

## Clarifications Schema (v0.6.4)

When user requirements are ambiguous, include clarifying questions in the response. The wizard UI uses these to gather additional context before generating the final workflow.

### Clarification Fields

| Field | Type | Description |
|-------|------|-------------|
| `clarificationNeeded` | boolean | Whether clarifying questions should be shown |
| `clarifications.sections` | Section[] | Tab-based sections for wizard navigation |

### Section Schema

```json
{
  "id": "goals",
  "title": "Goals",
  "completed": false,
  "questions": [...]
}
```

### Question Schema

```json
{
  "id": "primary-goal",
  "text": "What are the primary goals for this workflow?",
  "type": "single-select | multi-select | text",
  "options": [
    { "id": "analyze", "label": "Analyze and extract key insights", "inferred": true }
  ],
  "reason": "Optional explanation for why this was inferred"
}
```

### Question Types

| Type | Description | Use Case |
|------|-------------|----------|
| `single-select` | One option only (●/○) | Content type, depth level |
| `multi-select` | Multiple options (✓/☐) | Goals, features to include |
| `text` | Free-form input | Custom names, descriptions |

### Inferred Values

Set `inferred: true` on options that match keywords in the user's description:
- "video" or "youtube" → infer video content type
- "analyze" → infer analyze goal
- "summar" → infer summarize goal
- "generat" or "creat" → infer generate goal

### Recommendation goalId

Each recommendation must include a `goalId` that links to a goal option:

```json
{
  "skill": "media-reviewer",
  "suggestedStepId": "analyze-content",
  "goalId": "analyze",
  "matchScore": 0.92
}
```

This allows the wizard to filter recommendations based on selected goals in real-time.

## Structured Preferences for Enriched Prompt (v0.6.4)

When wizard answers are included in the enriched prompt (via "User clarifications: Q: ... A: ..."), these become **structured preferences** that MUST be incorporated into the workflow.

### Common Preference Types

| Preference Category | Example Questions | How to Use |
|---------------------|-------------------|------------|
| **PLATFORMS** | "Which social media platforms?" | Inject into social/output step missions |
| **ARTICLE_COUNT** | "How many articles/items?" | Inject into search/filter step missions |
| **FOCUS_AREAS** | "Which topics/areas to focus on?" | Inject into search and analysis missions |
| **OUTPUT_FORMAT** | "What format should output be?" | Inject into final output step mission |
| **DEPTH** | "How deep should analysis be?" | Adjust analysis step detail level |

### Preference Extraction from Enriched Prompt

When receiving an enriched prompt like:
```
User clarifications: Q: Which platforms? A: twitter, linkedin. Q: How many articles? A: top5. Q: Focus areas? A: llm, adoption.
```

Extract as structured data:
```
PLATFORMS: twitter, linkedin
ARTICLE_COUNT: 5
FOCUS_AREAS: llm, adoption
```

### Mission Templates with Preferences

**WITHOUT preferences (BAD):**
```
Search for AI news articles.
```

**WITH preferences (GOOD):**
```
Search for top 5 AI news articles focusing on LLM developments and adoption trends.
```

**WITHOUT preferences (BAD):**
```
Compile findings into a report.
```

**WITH preferences (GOOD):**
```
Create engaging social media posts optimized for twitter and linkedin, focusing on LLM and adoption angles.
```
