---
name: format-user-output
description: Format all user-facing output with consistent visual structure. Apply when displaying questions, results, progress, errors, or any message to the user. Use dividers, emojis, and clear sections.
---

# User Output Formatting Guidelines

**CRITICAL: All user-facing output must be visually structured and easy to scan.**

## When to Use This Skill

Apply this formatting when:
- Displaying questions to users
- Showing progress updates
- Returning results from agents
- Presenting errors or warnings
- Offering next step options
- Summarizing work completed

## Core Formatting Patterns

### 1. Box Headers (Major Sections)

Use for major section starts:

```markdown
╔═══════════════════════════════════════════════════════════════════════════╗
║                        SECTION TITLE HERE                                  ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### 2. Heavy Dividers (Section Breaks)

Use to separate distinct sections:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Emojis (Visual Scanning)

Use consistently:
- ✅ Success/Complete
- ⚠️ Warning
- ❌ Error/Failure
- 🔄 In Progress
- ⏳ Pending/Waiting
- 📋 Questions/Checklist
- 📊 Reports/Stats/Data
- 🔍 Investigation/Details
- 💡 Tips/Suggestions/Insights
- 🚀 Next Steps/Actions
- 📄 Files/Documents
- ⏸️ Paused/Waiting for Input
- 🎯 Goals/Objectives
- 🔐 Security/Sensitive

### 4. File Paths

Always use code blocks:
```markdown
Spec created: `@gabe-os/specs/2025-11-04-feature-name/`
```

### 5. Status Indicators

Use clear status:
```markdown
Status: ✅ COMPLETED
Status: 🔄 IN PROGRESS
Status: ⏳ PENDING
Status: ⚠️ BLOCKED
Status: ❌ FAILED
```

## Scenario-Specific Templates

### Template: Asking Questions

Use when agents need user input:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 QUESTIONS: [Topic Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Context sentence explaining why questions are needed]

1. [First question with assumption]

2. [Second question]

3. [Continue numbered questions]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏸️ WAITING FOR YOUR RESPONSE
Please answer the questions above. I'll continue once you respond.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Template: Phase Transitions

Use when moving between workflow phases:

```markdown
✅ PHASE 1 COMPLETE: [Phase name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 PHASE 2: [Next phase name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[What's happening in this phase]
```

### Template: Success Summary

Use when workflow completes:

```markdown
╔═══════════════════════════════════════════════════════════════════════════╗
║                   ✅ [WORKFLOW NAME] COMPLETE                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

[Brief success message]

📄 Files Created:
   • `[file-path-1]` - [Description]
   • `[file-path-2]` - [Description]
   • `[file-path-3]` - [Description]

✅ Key Accomplishments:
   • [Achievement 1]
   • [Achievement 2]
   • [Achievement 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 NEXT STEPS:
   [1] [Option 1 description]
   [2] [Option 2 description]
   [3] [Option 3 description]
```

### Template: Error/Warning Messages

Use when reporting problems:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ ERROR: [Error type]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: [Clear description of what went wrong]
Location: [File path or step where it occurred]

[IF CODE RELEVANT:]
```language
[Code snippet showing the issue]
```

💡 Suggested Fix:
[Actionable suggestion for how to resolve]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Template: Agent Completion Report

Use when agent returns to orchestrator:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ [AGENT NAME] COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Brief summary of what was accomplished]

📊 Key Metrics:
   • Items processed: [X]
   • Files analyzed: [Y]
   • [Other relevant metric]: [Z]

[IF FINDINGS:]
🔍 Key Findings:
   • [Finding 1]
   • [Finding 2]

📄 Report saved: `[file-path]`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready for [next step].
```

### Template: Progress Updates

Use when showing ongoing work:

```markdown
🔄 [TASK NAME] IN PROGRESS

Progress: [████████████░░░░░] 60%

Currently: [What's happening right now]

✅ Completed:
   • [Step 1]
   • [Step 2]

⏳ Remaining:
   • [Step 3]
   • [Step 4]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Template: Presenting Options

Use when user needs to choose:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 CHOOSE YOUR NEXT ACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Context explaining why user needs to choose]

[1] [Option 1 title]
    → [Brief description]
    → [Impact or outcome]

[2] [Option 2 title]
    → [Brief description]
    → [Impact or outcome]

[3] [Option 3 title]
    → [Brief description]
    → [Impact or outcome]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please respond with your choice (1, 2, or 3).
```

## Formatting Don'ts

❌ **Don't:**
- Use plain text for section breaks
- Omit visual structure
- Mix emoji styles inconsistently
- Use generic file paths (show actual paths!)
- Hide next steps in walls of text
- Use ambiguous status indicators
- Dump raw data without structure

✅ **Do:**
- Use dividers generously
- Add emojis for visual scanning
- Structure everything in sections
- Show specific file paths
- Make next steps explicit
- Use clear status indicators
- Format data in tables or lists

## Examples: Before & After

### ❌ Before (Poor Formatting)

```
The spec-shaper has prepared questions for you to answer. Please provide responses to the following: 1. Should this use TypeScript? 2. What database? 3. Any existing code to reuse?

Also if you have mockups please add them to the visuals folder.

Let me know your answers.
```

### ✅ After (Good Formatting)

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 SPEC RESEARCH QUESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The spec-shaper has analyzed your project and prepared these questions:

1. Should this feature use TypeScript?
   → I see your project uses TypeScript. Continue with TypeScript?

2. What database will store this data?
   → Options: PostgreSQL, MySQL, MongoDB, or other?

3. Is there existing code we should reference?
   → Any similar features or components to model after?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📸 VISUAL ASSETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Do you have design mockups or wireframes?

If yes, place them in: `@gabe-os/specs/2025-11-04-feature-name/planning/visuals/`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏸️ WAITING FOR YOUR RESPONSE
Please answer the questions above. I'll continue once you respond.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Quick Reference

**Opening a section:**
```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[EMOJI] [SECTION TITLE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Closing a section:**
```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Bullet points:**
```markdown
   • Point 1
   • Point 2
   → Alternative bullet style for actions/outcomes
```

**File paths:**
```markdown
Always in code blocks: `path/to/file.ts`
```

**Status:**
```markdown
Status: [EMOJI] [ALL CAPS STATUS TEXT]
```

## Apply Automatically

This skill should activate automatically whenever you:
- Display output to users
- Return results from agents
- Present questions
- Show progress
- Report completions
- Present errors

**Always prioritize clarity and visual structure over brevity.**
