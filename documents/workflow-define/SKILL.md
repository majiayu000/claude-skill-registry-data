---
name: workflow-define
description: Define custom workflows with steps, triggers, and conditions as markdown files
auto_trigger: true
trigger_keywords:
  - define workflow
  - create workflow
  - new workflow
  - workflow editor
  - custom workflow
  - automation workflow
  - make a workflow
  - workflow template
allowed-tools: Read, Write, mcp__flywheel__get_folder_structure, mcp__flywheel__search_notes
---

# Workflow Define

Create custom workflow definitions as markdown files that can be referenced and executed.

## Trigger Detection

Activate when user:
- Wants to create a new workflow
- Needs a custom automation sequence
- Wants to define reusable process steps

## Examples

- "Create a workflow for code review"
- "Define a workflow for content publishing"
- "Make a new workflow for bug triage"
- "I want to create a custom workflow"

## Process

1. **Gather Requirements**
   Ask user for:
   - Workflow name
   - What triggers it (keywords, conditions)
   - What steps it should perform
   - Any conditions or branches

2. **Generate Workflow Definition**
   Create markdown file with:
   - Frontmatter (name, triggers, description)
   - Step definitions
   - Conditions and branches
   - Expected outputs

3. **Save to Workflows Folder**
   - Create `workflows/` folder if needed
   - Save as `workflows/[name].md`
   - Confirm creation

## Workflow Definition Format

```yaml
---
name: workflow-name
description: What this workflow does
trigger:
  keywords:
    - keyword 1
    - keyword 2
  conditions:
    - file_type: meeting
    - has_tag: actionable
---

# Workflow: [Name]

## Description
[What this workflow accomplishes]

## Trigger
Activated when: [trigger description]

## Steps

### Step 1: [Name]
**Action**: read | search | extract | write | ask
**Target**: [file path or search query]
**Output**: [what this step produces]

### Step 2: [Name]
**Action**: [action type]
**Input**: {{step1.output}}
**Target**: [target]
**Condition**: [optional condition]

### Step 3: [Name]
**Action**: [action type]
**Target**: [target]

## Expected Output
[What the workflow produces when complete]

## Notes
[Any additional context or variations]
```

## Action Types

| Action | Description | Example |
|--------|-------------|---------|
| `read` | Read a file | Read meeting notes |
| `search` | Search for notes | Find notes with tag |
| `extract` | Extract data | Get action items |
| `write` | Write/edit file | Update daily note |
| `ask` | Prompt user | Confirm before action |
| `delegate` | Call another agent | Use action-extraction-agent |

## Conditions

Workflows can include conditions:

```markdown
### Step 3: Create Tasks
**Condition**: {{step2.count}} > 0
**Action**: write
**Target**: daily-notes/{{date}}.md
```

## Variables

Available variables in workflows:

| Variable | Description |
|----------|-------------|
| `{{date}}` | Current date (YYYY-MM-DD) |
| `{{input.path}}` | User-provided file path |
| `{{input.text}}` | User-provided text |
| `{{stepN.output}}` | Output from step N |
| `{{stepN.count}}` | Count from step N |

## Example Workflows

### Code Review Workflow

```yaml
---
name: code-review
description: Structured code review with feedback template
trigger:
  keywords:
    - review this code
    - code review
    - review PR
---

# Workflow: Code Review

## Steps

### Step 1: Identify Code
**Action**: read
**Target**: {{input.path}}
**Output**: code_content

### Step 2: Generate Review
**Action**: analyze
**Target**: {{step1.output}}
**Template**: |
  ## Code Review

  ### Summary
  [Brief summary]

  ### Issues Found
  - [ ] Issue 1

  ### Suggestions
  - Suggestion 1

  ### Approval
  [ ] Approved / [ ] Changes Requested

### Step 3: Create Review Note
**Action**: write
**Target**: reviews/{{date}}-{{input.filename}}.md
**Content**: {{step2.output}}
```

### Content Publishing Workflow

```yaml
---
name: publish-content
description: Review and publish content to destination
trigger:
  keywords:
    - publish this
    - ready to publish
---

# Workflow: Content Publishing

## Steps

### Step 1: Read Draft
**Action**: read
**Target**: {{input.path}}

### Step 2: Check Requirements
**Action**: validate
**Checks**:
  - has_frontmatter: true
  - has_section: "## Summary"
  - word_count: "> 500"

### Step 3: Confirm Publish
**Action**: ask
**Question**: "Ready to publish '{{input.title}}'?"

### Step 4: Move to Published
**Condition**: {{step3.confirmed}}
**Action**: move
**From**: {{input.path}}
**To**: published/{{input.filename}}
```

## Six Gates Compliance

| Gate | Status | Notes |
|------|--------|-------|
| 1. Read Before Write | ✅ | Reads existing workflows first |
| 2. File Exists Check | ✅ | Checks for workflow folder |
| 3. Chain Validation | N/A | Single-step skill |
| 4. Mutation Confirm | ✅ | Confirms before creating |
| 5. MCP Health | N/A | No MCP mutations |
| 6. Post Validation | ✅ | Verifies file created |

## Notes

- Workflows are documentation + reference, not auto-executed
- Users invoke workflows via natural language matching keywords
- Complex workflows should delegate to agents
- Keep steps atomic and verifiable
