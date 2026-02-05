---
name: bible-tools
description: Orchestrate Bible study tools for generating messages, Sabbath School
  outlines, and studies. Use when asked about sermons, messages, Sabbath School
  lessons, Bible studies, or church content generation.
allowed-tools: [Bash, Read, Glob]
---

# Bible Tools Skill

This skill helps you use the Bible Tools CLI to generate and manage
church-related content.

## Capabilities

- Generate sermon messages on any topic
- Process Sabbath School lesson outlines (downloads PDFs, generates AI outlines)
- Create Bible study materials
- Revise content with specific instructions
- Export content to Apple Notes
- List existing outputs

## CLI Commands

The CLI is available as `bible` (symlinked to `packages/cli/bin/bible`).

**Important:** The `--model` flag is required for all generation/revision
commands.

### Messages

```bash
# Generate a new message
bible messages generate --model anthropic --topic "Hope in Christ"

# Revise an existing message
bible messages revise --model anthropic --file <path> --instructions "Make it more concise"

# List all messages
bible messages list [--json]

# Generate from Apple Note
bible messages from-note --model anthropic --note-id <id>
```

### Sabbath School

```bash
# Process current week's lesson (downloads PDF, generates outline)
bible sabbath-school process --model anthropic --year 2025 --quarter 2 --week 5

# Revise an existing outline
bible sabbath-school revise --model anthropic --year 2025 --quarter 2 --week 5

# Export to Apple Notes
bible sabbath-school export --year 2025 --quarter 2 --week 5
```

### Studies

```bash
# Generate a new study
bible studies generate --model anthropic --topic "Faith and Works"

# Revise an existing study
bible studies revise --model anthropic --file <path> --instructions "Add more scripture references"

# List all studies
bible studies list [--json]
```

### Export

```bash
# Export files to Apple Notes
bible export --files <path1> --files <path2>
```

## Context Awareness

### Current Quarter/Week Calculation

Calculate the current Sabbath School quarter and week:

- **Q1**: January 1 - March 31 (weeks 1-13)
- **Q2**: April 1 - June 30 (weeks 1-13)
- **Q3**: July 1 - September 30 (weeks 1-13)
- **Q4**: October 1 - December 31 (weeks 1-13)

Each quarter starts on the first Saturday of the quarter's first month.

### Output Locations

All outputs are stored in `packages/cli/outputs/`:

- `outputs/messages/` - Generated messages (YYYY-MM-DD-slug.md)
- `outputs/sabbath-school/` - Sabbath School outlines (YYYY-QX-WY.md)
- `outputs/studies/` - Bible studies (YYYY-MM-DD-slug.md)
- `outputs/readings/` - Chapter readings

## Workflows

### Generate Sabbath School Outline for This Week

1. Calculate current year, quarter, and week from today's date
2. Check if outline exists: `ls packages/cli/outputs/sabbath-school/`
3. If missing:
   `bible sabbath-school process --model anthropic --year YYYY --quarter Q --week W`
4. Read the generated file and summarize for the user

### Revise Content (Agent-Orchestrated Loop)

1. User provides feedback on content
2. Run:
   `bible <type> revise --model anthropic --file <path> --instructions "<feedback>"`
3. Read the updated file and show to user
4. Ask if further revisions needed
5. Repeat until satisfied

### Generate Message with Topic

1. Confirm topic with user
2. Run: `bible messages generate --model anthropic --topic "<topic>"`
3. Read the output file and summarize
4. Ask if user wants to revise or export

## Tips

- Always check existing outputs before generating new ones
- Use `--json` flag on list commands for easier parsing
- When revising, be specific with instructions
- Quarter boundaries: Q1=Jan, Q2=Apr, Q3=Jul, Q4=Oct
