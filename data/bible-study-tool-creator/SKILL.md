---
name: bible-study-tool-creator
description: Interactive skill for creating new bible study tools that generate AI-readable commentary data. Guides users through defining practical tasks, setting up proper file structure, and establishing self-learning loops for data generation.
permissions:
  - WebSearch
  - WebFetch
---

# Bible Study Tool Creator

## Overview

This skill helps create new bible study tools for the myBibleToolbox project through an interactive, step-by-step process. Each tool generates specific types of AI-readable commentary data (YAML files) that ground AI systems in truth when working with Biblical texts.

## When to Use

Use this skill when:
- Creating a new bible study tool
- Initializing file structure for a data generation task
- Setting up a self-learning loop for AI-driven biblical analysis

Do NOT use this skill when:
- Working on an existing tool (use that tool directly)
- Just querying Bible data (use other skills like quote-bible)

## How It Works

This skill guides Claude to interactively gather information from the user one question at a time, then generates all necessary files. The process:

1. Check for duplicate tools
2. Ask focused questions using AskUserQuestion tool
3. Build tool definition progressively
4. Generate complete file structure
5. Set up self-learning loop

## Interactive Creation Process

### Step 1: Ensure we clearly know what the user wants to do

 - [ ] We have collected user input on what they want to build
 - [ ] We have checked (list dir) of /bible-study-tools if it already exists
 - [ ] The grouping/purpose is clear (e.g., "all lexical data" vs "just Strong's")
 - [ ] The task is singular focused and not trying to do too much
 - [ ] The task is valuable and adds worthwhile context to simple LLMs so they would give stronger more accurate answers
 - [ ] The foreach scope has been determined (verse/chapter/book/etc.)

Follow the details in ./steps/step-discover-intent.md


### Step 2: Suggest Tool Name

- [ ] a clear name has been chosen that captures what it does and follows the guidelines
- [ ] Created bible-study-tools/{tool-name}/{tool-name}.yaml with key data

Follow the details in ./steps/step-suggest-tool-name.md

**After selecting tool name, create bible-study-tools/{tool-name}/{tool-name}.yaml** to preserve critical information.

### Step 3: Research and Propose Concrete Examples

- [ ] You have 5 excellent examples of high value
- [ ] You know how you created those examples and how you could build the tool
- [ ] Each validated example appended to bible-study-tools/{tool-name}/{tool-name}.yaml

Follow the details in ./steps/step-create-examples.md

**Present each example ONE AT A TIME** in separate AskUserQuestion calls with rating options.

### Step 5: Define Output Structure

Ask the user to describe the YAML structure they envision. Provide guidance:

```
"What data should each YAML file contain? Describe the structure, for example:
- Field names
- What each field represents
- Whether fields contain simple values, lists, or nested objects"
```

From their description, create both:
- `data_structure`: A complete example with sample data
- `yaml_structure_inline`: A concise version showing just the field hierarchy

### Step 6: Select Test Verse

Ask the user which verse to use for initial testing:

```
Question: "Which verse should we use for initial testing?"
Options:
- JHN 3:16 (Very familiar, good baseline)
- MAT 5:3 (Beatitudes, theological depth)
- GEN 1:1 (Creation, ancient context)
- PSA 23:1 (Poetry, metaphor-rich)
- Other (specify a verse)
```

### Step 7: Build Tool Definition YAML

Consolidate all gathered information into a YAML file at `/tmp/tool-definition.yaml`:

```yaml
tool_name: "[Tool Name in Proper Case, e.g., 'Semantic Groups']"
tool_name_kebab: "[kebab-case identifier, e.g., 'semantic-groups']"
task_name: "[SAME as tool_name_kebab - used in filenames like MAT-5-3-semantic-groups.yaml]"
description: "[One sentence description]"
test_verse: "[Selected verse e.g., JHN 3:16]"

goals_formatted: |
  1. [Goal 1]
  2. [Goal 2]
  3. [Goal 3]
  [etc.]

examples_formatted: |
  ### Example 1
  **Context**: [Context from user]
  **Insight**: [Insight from user]
  **Value**: [Value from user]

  ### Example 2
  [...]

  [... all 5 examples ...]

related_tools: "[List any related tools or 'None yet']"

data_structure: |
  ```yaml
  [Complete example structure with sample data]
  ```

yaml_structure_inline: |
  [Concise field hierarchy]
```

Note: `task_name` should always equal `tool_name_kebab` to maintain consistency.

### Step 8: Run Initialization Script

Execute the Python script to generate all files:

```bash
python3 /Users/chrispriebe/projects/context-grounded-bible/.claude/skills/bible-study-tool-creator/init-tool.py /tmp/tool-definition.yaml
```

The script creates this structure in `/bible-study-tools/{tool-name}/`:

**Files created**:
- `README.md` - Tool overview with description, goals, and examples
- `LEARNING.md` - Experiment log for self-learning loop
- `{tool-name}-template.md` - Agent prompt template
- `tests/README.md` - Test framework documentation

### Step 9: Register Tool in Tool Registry

Update `/bible-study-tools/tool-registry.yaml` to register the new tool:

**Ask the user these questions:**

1. **Scope** - What level of detail and data size does this tool provide?
   - `core`: Essential data, always included regardless of query depth
     - Size: Small files (~1-50 KB)
     - Examples: sermon illustrations, cross-references, basic commentary
     - Use when: Tool provides must-have foundational data for any verse study

   - `standard`: Standard research depth, typical scholarly analysis
     - Size: Moderate files (~50-500 KB)
     - Examples: word studies, historical context, semantic clusters
     - Use when: Tool provides valuable research data for deeper study (most tools)

   - `comprehensive`: Exhaustive reference data, complete collections
     - Size: Large files (>500 KB)
     - Examples: all translations (1000+), complete lexicon entries, full concordances
     - Use when: Tool provides comprehensive reference that's only needed for exhaustive analysis

2. **Category** - What type of data does this tool provide?
   - `lexical`: Word meanings, etymology, source languages
   - `theological`: Doctrine, theology, biblical themes
   - `practical`: Application, sermon illustrations, devotional insights
   - `historical`: Cultural context, historical background, archaeology
   - `linguistic`: Translation analysis, semantic clusters, language patterns
   - `topical`: Topic cross-references, thematic connections

**Then add an entry to the registry:**

```yaml
{tool-suffix}:
  name: {Tool Name}
  summary: {Brief description - max 20 words}
  scope: {core|standard|comprehensive}
  category: {lexical|theological|practical|historical|linguistic|topical}
```

**Registry Guidelines:**
- The tool suffix must match the filename suffix (e.g., `sermon-illustrations` for `MAT-5-3-sermon-illustrations.yaml`)
- Summary should explain what the tool does and why it's valuable (max 20 words)
- Scope determines BOTH when to include AND expected file size
- Category helps users understand the tool's purpose

**Query Depth Mapping:**
- Light queries (quick overview) → Include `core` tools only
- Medium queries (standard study) → Include `core` + `standard` tools
- Full queries (comprehensive) → Include `core` + `standard` + `comprehensive` tools

### Step 10: Update Related Tools (if applicable)

If this tool is a variant of or related to existing tools, update those tools' README.md files to cross-reference the new tool. Also summarize key learnings from related tools' LEARNING.md files.

### Step 11: Confirm Creation

Show the user a concise summary:

```
✅ Successfully created bible study tool: {tool-name}

Created files in /bible-study-tools/{tool-name}/:
- README.md (tool overview, goals, examples)
- LEARNING.md (experiment log)
- {tool-name}-template.md (agent prompt template)
- tests/README.md (test framework)

Updated:
- /bible-study-tools/tool-registry.yaml (registered tool for scripture-study integration)

Next steps:
1. Review generated files
2. Customize {tool-name}-template.md with specific instructions
3. Run first test on {test_verse}
4. Document learnings and iterate
5. Test integration with scripture-study skill
```

## Best Practices

**Check Initial Context First**: Always check if the user already described their intent when invoking the skill. Don't ask redundant questions if the user already told you what they want.

**Progressive Question Flow**: Ask questions one at a time. Don't overwhelm the user with multiple questions simultaneously.

**Search Before Building**: Always search for existing tools before starting the interactive flow. This prevents duplicate work.

**Validate Examples**: The 5 examples are crucial - they justify the tool's existence. Ensure each example:
- Is specific and concrete
- Shows clear practical value
- Demonstrates how the tool helps translators/pastors/students

**ALWAYS Use AskUserQuestion Tool**: ALL questions to the user MUST use the AskUserQuestion tool. Never ask questions in natural conversation text. Every time you need user input, create an AskUserQuestion with clear options.

**How to Structure Questions**:
- For structured choices: Provide 2-4 specific options (e.g., test verse selection, tool name options)
- For open-ended input: Provide representative examples as options with "Other" for custom input
- Always include an "Other" option that allows free-text input - this is automatically provided
- Use multiSelect: true when multiple answers can be selected (e.g., selecting multiple goals)

**Concise Feedback**: After gathering each piece of information, provide brief acknowledgment before moving to the next question.

## Example Interaction Flow

**Scenario A: User provides intent upfront**
```
User: "create a new bible study tool to extract all Greek words from each verse"
```
1. Capture intent: "extract all Greek words from each verse"
2. Search existing tools → None found
3. AskUserQuestion: "Tool name?" with suggested options → User selects or provides custom
4. AskUserQuestion: "One-sentence description?" with examples → User provides
5. AskUserQuestion: "How to provide goals?" → User selects approach
6. User provides goals (via AskUserQuestion if needed) → Acknowledged
7. AskUserQuestion: Present first researched example → User validates
8. Continue for examples 2-5 (each via AskUserQuestion)
9. AskUserQuestion: About YAML structure with examples → User describes
10. AskUserQuestion: "Test verse?" → User selects from options
11. Build YAML file → Run init script → Confirm creation

**Scenario B: User provides no initial context**
```
User: "create a new bible study tool"
```
1. Brainstorm 3-4 valuable tool ideas based on project mission
2. AskUserQuestion: "What would you like this tool to do?"
   - Options: [Greek/Hebrew extraction, Cultural metaphor adaptations, Translation patterns, Theological terms, Other]
   - User selects: "Cultural metaphor adaptations"
3. Search existing tools → None found
4. AskUserQuestion: "Tool name?" with suggested options → User selects
5. Continue with standard flow (all via AskUserQuestion)...

## Notes

- Follow USFM 3.0 book codes (MAT, JHN, GEN, etc.)
- Follow ISO-639-3 language codes
- YAML format ensures both human and AI readability
- The self-learning loop is essential for quality
- Goals must provide clear practical value, not just data for data's sake
