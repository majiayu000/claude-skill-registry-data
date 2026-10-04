---
name: dev-project-builder
description: Create Claude-Project-like experiences inside Claude Code — persistent context, specialized responses, and working memory for a recurring workspace. Use when the user says "make a project", "persistent context for X", or "set up a workspace like Claude Projects". NOT for scaffolding an EmptyOS app (use eos-new-app) or optimizing CLAUDE.md itself (use dev-claude-md-optimizer).
---

# Project Builder

A methodology for creating "Claude Project-like" skills that provide persistent context, specialized behavior, and true memory through vault integration.

## The Pattern

Claude Projects provide: uploaded files, custom instructions, persistent memory, and specialized responses. In Claude Code, we replicate this with a 5-component structure:

```
┌─────────────────────────────────────────────────────────────┐
│                     PROJECT STRUCTURE                        │
├─────────────────────────────────────────────────────────────┤
│  1. Memory Note (the "persistent context")                  │
│     └── Background, current state, breakthroughs, patterns  │
│     └── Read on EVERY activation, update when insights emerge│
│     └── Location: 20_Areas/[area]/[name]-memory.md          │
│                                                              │
│  2. Core Document (the "map")                               │
│     └── Goals, progress, key reference info                 │
│     └── Location: 20_Areas/ or 10_Projects/                 │
│                                                              │
│  3. Reference Files (the "uploads")                         │
│     └── Frameworks, theory, templates, guides               │
│     └── Location: 30_Resources/ or 20_Areas/                │
│                                                              │
│  4. Working Folder (the "session history")                  │
│     └── Logs, session notes, drafts                         │
│     └── Location: 20_Areas/ or 50_Journal/                  │
│                                                              │
│  5. Skill Definition (the "instructions")                   │
│     └── Modes, templates, triggers, style guide             │
│     └── Location: .claude/skills/NAME/SKILL.md              │
└─────────────────────────────────────────────────────────────┘
```

### Memory Note vs Core Document

| Aspect | Memory Note | Core Document |
|--------|-------------|---------------|
| Purpose | Persistent context about the user | Reference info and plans |
| Updates | Frequently (after breakthroughs) | Less frequently |
| Content | Background, state, patterns, learnings | Goals, frameworks, timelines |
| Analogy | Claude Project's Memory feature | Uploaded reference files |

## When to Use This Skill

- User says "I want to create a skill for X"
- User says "帮我做一个像 Claude Project 那样的..."
- User has a complex domain with existing vault content that needs specialized AI interaction

## Workflow: Creating a New Project-Like Skill

### Step 1: Identify the Domain

Ask the user:
> "What topic or area do you want Claude to help with? What kind of companion or assistant are you looking for?"

### Step 2: Find Existing Content

Search the vault for related content:
- Look in `20_Areas/` for existing area documentation
- Look in `30_Resources/` for reference materials
- Look in `50_Journal/` for existing logs or entries
- Look in `10_Projects/` for active project plans

Report what you find:
> "I found these related files in your vault: [list]. Which of these are relevant to your new skill?"

### Step 3: Map to Structure

Help the user identify each component:

| Component | Question to Ask | Example |
|-----------|-----------------|---------|
| Memory Note | "Where should I store persistent context about you?" | `healing-memory.md` |
| Core Document | "What's the main 'map' that tracks your state/progress?" | `焦虑型依恋-我的疗愈地图.md` |
| Reference Files | "What frameworks, guides, or theory should I reference?" | CBT prompts, methodology docs |
| Working Folder | "Where should I write logs and session notes?" | `疗愈日志/`, `sessions/` |
| Modes | "What different ways do you want to interact?" | Trigger processing, check-in, review |

### Memory Note Template

```markdown
---
type: [domain]-memory
updated: YYYY-MM-DD
---

# [Domain] Memory

## Purpose & Context
[Why this matters, current life situation, background]

## Current State
[What's being actively worked on, recent focus areas]

## Core Patterns & Insights
[Identified patterns, key beliefs, recurring themes]

## Key Breakthroughs
[Significant insights with dates]
- YYYY-MM-DD: [breakthrough description]

## Approach & What Works
[Techniques, methods, phrases that help]

## Tools & Resources
[Books, frameworks, preferred approaches]
```

### Step 4: Define Modes

For each mode, define:
- **Trigger phrases**: What the user says to activate this mode
- **Workflow**: Step-by-step process
- **Output**: What gets created (logs, updates, etc.)

Common mode patterns:
- **Processing mode**: Work through something (e.g., trigger, problem, idea)
- **Check-in mode**: Quick status/energy check
- **Review mode**: Analyze patterns over time
- **Crisis mode**: Urgent support with grounding
- **Reference mode**: Look up and apply frameworks

### Step 5: Define Style Guide

Ask:
> "How should Claude respond in this domain? What tone, pacing, or approach works best?"

Common style elements:
- Communication tone (warm, direct, professional, etc.)
- Response pacing (one question at a time vs. comprehensive)
- Language preference (Chinese, English, bilingual)
- Key phrases or affirmations to use

### Step 6: Generate SKILL.md

Create the skill file using this template:

```markdown
---
name: skill-name
description: Brief description in preferred language
---

# Skill Name

Brief overview of what this skill does.

## Reference Files (Read on Activation)

| File | Purpose |
|------|---------|
| `path/to/core-document.md` | **REQUIRED** - Core context, always read first |
| `path/to/reference.md` | Framework/theory reference |
| `path/to/folder/` | Recent logs for pattern awareness |

## Working Folder

New content goes in: `path/to/working-folder/`

## Modes

### Mode 1: [Name]

**Trigger**: "phrase that activates this mode"

**Workflow**:
1. Step one
2. Step two
3. ...

**Output**: What gets created/updated

### Mode 2: [Name]
...

## Templates

### [Template Name]

\```markdown
Template content here
\```

## Style Guide

- Principle 1
- Principle 2
- ...

## Triggers (When to Suggest This Skill)

| Signal | Action |
|--------|--------|
| User says X | Suggest this skill |
```

### Step 7: Test

Run through a sample interaction:
1. Invoke the skill
2. Try each mode
3. Verify it reads context correctly
4. Verify it creates output in the right location

## Examples

### Example 1: Healing Companion

```
Core Document: 20_Areas/Health/焦虑型依恋-我的疗愈地图.md
Reference Files: CBT prompts, attachment theory, healing songs
Working Folder: 20_Areas/Health/疗愈日志/
Modes: Trigger processing, check-in, review, crisis, songs
Style: Therapeutic, validating, one question at a time
```

### Example 2: Career Coach (hypothetical)

```
Core Document: 20_Areas/Career/Career Development Map.md
Reference Files: Resume, skills inventory, industry research
Working Folder: 20_Areas/Career/reflections/
Modes: Goal review, interview prep, skill assessment, frustration processing
Style: Encouraging but realistic, action-oriented
```

### Example 3: Language Learning (hypothetical)

```
Core Document: 10_Projects/Japanese-Learning/Learning Plan.md
Reference Files: Grammar guides, vocabulary lists, resources
Working Folder: 50_Journal/language-practice/
Modes: Lesson, practice, review, immersion log
Style: Patient, encouraging, progressively challenging
```

## Key Principles

1. **Read before responding**: Always read the Core Document on activation
2. **Write to remember**: Log insights and sessions to the Working Folder
3. **Reference frameworks**: Apply theories and methods from Reference Files
4. **Respect user autonomy**: Ask before creating files or making updates
5. **Bilingual awareness**: Match user's language, search in both languages

## Integration with Other Skills

- **vault-index**: Find related notes and backlinks
- **moc-manager**: Create index notes for project content
- **knowledge-synthesis**: Connect insights across vault

---

#meta-skill #methodology #project-builder
