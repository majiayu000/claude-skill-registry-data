---
name: notebooklm-lesson-planner
description: Create structured Google NotebookLM lesson plans with curated sources and tailored audio overview prompts. Use when the user wants to create a NotebookLM notebook, generate learning content with audio overviews, or build a curriculum with multiple focused segments. Handles both single lesson creation and batch processing of multiple topics.
---

# NotebookLM Lesson Planner

Create comprehensive lesson plans for Google NotebookLM with validated sources and customized audio overview prompts.

## What This Skill Does

This skill helps you create NotebookLM notebooks by:

1. **Finding high-quality sources** - Identifying 10-20 online resources that are publicly accessible, LLM-readable, and substantive
2. **Validating sources** - Ensuring all URLs are active, accessible, and not behind paywalls or crawler blocks
3. **Generating tailored prompts** - Creating specific prompts for each learning area that guide NotebookLM's audio overview generation
4. **Structuring content** - Organizing lessons to avoid redundancy and ensure comprehensive coverage

## When to Use This Skill

Use this skill when the user wants to:
- Create a NotebookLM notebook on a specific topic
- Generate a learning curriculum with multiple focused audio overviews
- Build educational content with curated sources
- Process multiple topics in batch (e.g., 100+ lesson plans)

## Workflow Overview

The process varies based on whether you're creating a single lesson or processing a batch:

**Single Lesson Mode:**
1. Gather requirements from user
2. Find and validate sources
3. Generate prompts for each learning area
4. Provide complete lesson plan

**Batch Mode:**
1. Process JSON specification file
2. For each lesson: find sources, validate, generate prompts
3. Output complete lesson plans for all topics

## Single Lesson Mode

### Step 1: Gather Requirements

Ask the user for:

1. **Main topic** - The overall subject (e.g., "Firewall Configuration")
2. **Learning areas** - Specific subtopics to cover (e.g., "ACLs", "NAT", "VPN", "Logging")
3. **Listener context** - Information about the learner:
   - What they already know
   - Expertise level (beginner, intermediate, advanced)
   - What they want to learn
   - Why they're learning this (use case, goal)
4. **Target source count** - How many sources to find (recommend 15, range 10-20)

### Step 2: Find Sources

Use web_search to find sources that:
- Cover the main topic and learning areas
- Are publicly accessible (no paywall, no login)
- Are high-quality and substantive
- Provide appropriate depth for listener's level

**Search strategy:**
1. Start with comprehensive sources covering multiple learning areas
2. Find specialized sources for each specific learning area
3. Ensure diversity in source types (tutorials, documentation, analysis)
4. Aim for 10-20 total sources

See `references/source_finding.md` for detailed strategies on:
- Source quality criteria
- Search techniques
- Source type evaluation
- Coverage matrix planning

### Step 3: Validate Sources

After finding sources, validate them using the validation script:

```bash
scripts/validate_sources.py url1 url2 url3 ... --verbose
```

The script checks:
- URL is active (200 status)
- No paywall detected
- Content is substantive (>500 chars)
- No obvious crawler blocking

**If sources fail validation:**
- Remove invalid sources
- Find replacements using web_search
- Re-validate until all sources pass

### Step 4: Generate Prompts

For each learning area, create a tailored prompt for NotebookLM's audio overview generator.

**Read prompt templates first:**
```bash
view references/prompt_templates.md
```

**Each prompt must include:**

1. **Topic/Learning Area** - What specific area this overview covers
2. **Listener Profile** - Who the listener is, what they know, their expertise level
3. **Coverage Scope** - What this overview should cover in detail
4. **Previous Coverage** - What was covered in the last episode (for continuity)
5. **Upcoming Topics** - What will be covered in future episodes (to avoid going into detail)
6. **Exclusions** - Critical! What NOT to cover in detail (handled by other overviews)
7. **Approach and Goals** - Tone, depth, teaching style, and learning objectives
8. **Length Suggestion** - Duration target: [~15 min] for standard, [~22 min] for longer episodes
9. **Additional Context** - Any other relevant information

**Exclusion and continuity strategy:**
- Overview 1: No previous coverage, upcoming: areas 2, 3, 4
- Overview 2: Previous: area 1, upcoming: areas 3, 4
- Overview 3: Previous: areas 1-2, upcoming: area 4
- Overview 4: Previous: areas 1-3, no upcoming topics

This ensures each overview is focused, non-redundant, and builds on prior knowledge.

**Case Study Requirement:**
One audio overview in every lesson MUST be a real-life case study focusing on real companies and their experiences. This overview should analyze actual implementation stories, challenges faced, and lessons learned from real organizations.

### Step 5: Generate Quiz Prompts

For each lesson, create 4 quiz prompts based on the audio overviews. Each quiz prompt should:

1. **Reference the audio overview** - Which overview this quiz is based on
2. **Specify length** - short, default, or long
3. **Specify difficulty** - medium or hard
4. **Guide quiz content** - What topics/concepts to focus on

**Quiz distribution:**
- Quiz 1: Based on Overview 1 (difficulty: medium, length: default)
- Quiz 2: Based on Overview 2 (difficulty: medium, length: short)
- Quiz 3: Based on Overview 3 (difficulty: hard, length: default)
- Quiz 4: Based on Overview 4 or case study (difficulty: hard, length: long)

### Step 6: Deliver Lesson Plan

Provide the user with:

1. **Complete source list** - All validated URLs with brief descriptions
2. **Coverage summary** - Which sources cover which learning areas
3. **Audio Overview Prompts** - One prompt per learning area, numbered and ready to use (including length suggestions)
4. **Quiz Prompts** - Four quiz prompts with length and difficulty specified
5. **Instructions** - How to use the lesson plan with NotebookLM:
   - Add all sources to NotebookLM notebook
   - For each audio overview, copy the corresponding prompt
   - Generate audio overviews in sequence
   - Generate quizzes using the quiz prompts

**Output format:**

```markdown
# NotebookLM Lesson Plan: [Topic]

## Sources (15)

1. [Source 1 Title] - [URL]
   Coverage: [Learning areas covered]

2. [Source 2 Title] - [URL]
   Coverage: [Learning areas covered]

...

## Audio Overview Prompts

### Overview 1: [Learning Area 1] [~15 min]

[Full prompt text including: coverage, previous coverage, upcoming topics, approach and goals]

### Overview 2: [Learning Area 2] [~15 min]

[Full prompt text]

### Overview 3: [Case Study] [~22 min]

[Full prompt text - real-life case study of real companies]

...

## Quiz Prompts

### Quiz 1: [Topic] (Based on Overview 1)
**Length**: default | **Difficulty**: medium

[Full quiz prompt text]

### Quiz 2: [Topic] (Based on Overview 2)
**Length**: short | **Difficulty**: medium

[Full quiz prompt text]

...

## Usage Instructions

1. Create a new notebook in Google NotebookLM
2. Add all 15 sources to the notebook
3. For each audio overview:
   - Click "Generate Audio Overview"
   - Copy and paste the corresponding prompt above
   - Generate the overview
4. For each quiz:
   - Click "Generate Quiz"
   - Copy and paste the corresponding quiz prompt
   - Generate the quiz
5. Listen to overviews in sequence (1→2→3→...)
```

## Batch Mode

For processing multiple topics from a JSON file.

### Step 1: Understand Batch Specification

The user provides a JSON file with this structure:

```json
{
  "lessons": [
    {
      "topic": "Sandwich Making",
      "learning_areas": ["bread", "proteins", "cheeses", "vegetables"],
      "listener_context": {
        "knows": ["basic cooking"],
        "wants_to_learn": ["gourmet techniques"],
        "skill_level": "intermediate"
      },
      "target_sources": 15
    },
    {
      "topic": "Firewall Configuration",
      "learning_areas": ["ACLs", "NAT", "VPN"],
      ...
    }
  ]
}
```

### Step 2: Process Each Lesson

For each lesson in the batch:
1. Follow the Single Lesson Mode workflow
2. Find sources (may need multiple web_search calls)
3. Validate sources
4. Generate prompts
5. Save lesson plan to individual JSON file

**Important for batch processing:**
- Process lessons sequentially (don't try to parallelize)
- Be efficient with web_search (combine queries when possible)
- Validate sources in batches using the script
- Save progress incrementally (one lesson at a time)

### Step 3: Output Structure

Create a directory structure:

```
output/
├── lesson_001_sandwich_making.json
├── lesson_002_firewall_configuration.json
├── lesson_003_database_optimization.json
...
└── batch_summary.md
```

Each JSON file contains:
```json
{
  "topic": "Sandwich Making",
  "learning_areas": ["bread", "proteins", "cheeses", "vegetables"],
  "listener_context": {...},
  "sources": [
    {
      "url": "https://example.com/sandwich-guide",
      "title": "Complete Sandwich Making Guide",
      "coverage": ["bread", "proteins", "cheeses", "vegetables"]
    },
    ...
  ],
  "prompts": [
    {
      "area": "bread",
      "prompt": "Topic: Bread Selection for Sandwiches\n\n..."
    },
    ...
  ]
}
```

The batch_summary.md provides an overview of all lessons created.

## Quality Guidelines

### Source Quality
- Minimum 10 sources, maximum 20
- All sources must pass validation
- Each learning area covered by at least 3 sources
- Mix of comprehensive and specialized sources
- Appropriate depth for listener's expertise level

### Prompt Quality
- Each prompt 200-350 words (optimal with new requirements)
- Clear previous coverage and upcoming topics sections
- Clear exclusions to avoid overlap
- Listener context consistent across all prompts
- Specific coverage guidance
- Appropriate tone and depth for audience
- Length suggestion included ([~15 min] or [~22 min])
- Approach and goals clearly stated
- At least one case study overview per lesson

### Quiz Quality
- 4 quizzes per lesson minimum
- Each quiz mapped to a specific audio overview
- Mix of difficulty levels (medium and hard)
- Mix of lengths (short, default, long)
- Clear guidance on topics to test
- Questions should reinforce key concepts from the audio overviews

### Coverage Balance
- No learning area should dominate (unless intentional)
- No learning area should be under-represented
- Sources should provide diverse perspectives
- Both breadth and depth appropriate for topic scope

## Tips and Best Practices

**Finding sources:**
- Start broad, then get specific
- Use multiple search queries per learning area
- Look for official documentation first
- Check publication date for time-sensitive topics
- Verify accessibility before adding to list

**Writing prompts:**
- Be explicit about exclusions
- Reference other overviews by number
- Provide specific examples of what to cover
- Match technical depth to listener's level
- Include practical context (why they're learning this)

**Validating sources:**
- Always run validate_sources.py before finalizing
- Manually spot-check 3-5 sources
- If >20% fail validation, reconsider search strategy
- Replace failed sources before generating prompts

**Batch processing:**
- Process 10-20 lessons at a time
- Check one complete lesson before processing all
- Save progress frequently
- Use consistent listener_context format across batch

## Common Issues

**Sources failing validation:**
- Check for paywall indicators in URL or title
- Try alternative sources on the same topic
- Ensure using HTTPS not HTTP
- Verify site isn't down temporarily

**Overlapping prompts:**
- Review exclusion sections
- Ensure each area has clear boundaries
- Consider if learning areas need restructuring
- Make exclusions more specific

**Coverage gaps:**
- Add more specialized sources
- Use more specific search queries
- Look for sources that bridge multiple areas
- Consider if learning areas are too granular

**Batch processing slow:**
- Combine search queries where possible
- Validate sources in batches
- Process during off-peak hours
- Consider breaking into smaller batches

## Files and Scripts

**Scripts:**
- `validate_sources.py` - Validate URLs for NotebookLM compatibility

**References:**
- `prompt_templates.md` - Templates and examples for creating prompts
- `source_finding.md` - Strategies for finding high-quality sources

**Usage examples in references files.**
