---
name: top-down-learning
description: Comprehensive codebase understanding through structured documentation and guided learning. Use when Claude needs to help a user understand how a project works by exploring and documenting the codebase architecture, concepts, and modules in a .learning/ directory, then guiding them through understanding the code with adaptive explanations. Triggered by requests like "help me understand this project", "document the architecture", "explain how this codebase works", or "guide me through the code".
---

# Top-Down Learning

Learn any codebase through structured exploration and adaptive guidance.

## Overview

This skill enables deep understanding of codebases through two complementary workflows:

1. **Exploration & Documentation**: Explore the project structure, identify patterns, and create structured documentation in `.learning/`
2. **Guided Learning**: Use the documentation to guide users through understanding with adaptive depth

The approach follows top-down learning principles: start with architecture and high-level concepts, then progressively dive deeper based on user needs.

## Workflow

### Phase 1: Initial Exploration & Setup

**When**: User wants to understand a new project for the first time

**Goal**: Create the foundation for top-down learning

**Steps**:

1. **Create .learning directory structure**:
   ```bash
   mkdir -p .learning/architecture .learning/concepts .learning/modules
   echo '*' > .learning/.gitignore
   echo '!.gitignore' >> .learning/.gitignore
   ```

2. **Scan project structure** using `view` tool:
   - Start at project root with `view .` to see top-level structure
   - Identify major directories (src/, lib/, components/, etc.)
   - Note directory organization patterns
   - Look for key files: package.json, tsconfig.json, requirements.txt, go.mod, etc.

3. **Identify key files** by viewing root and key directories:
   - **Config files**: package.json, tsconfig.json, .env files, config files
   - **Entry points**: main.*, index.*, app.*, __init__.py, __main__.py
   - **Documentation**: README.md, CONTRIBUTING.md, docs/
   - **Tests**: test directories, *_test.*, *.test.*, *.spec.*

4. **Read key files** to understand:
   - Primary language(s) and frameworks (from config files)
   - Dependencies and their purposes
   - Project structure and architecture hints
   - Scripts and build commands

5. **Generate `architecture/overview.md`** using the Architecture Overview Template (see `references/templates.md`):
   - System purpose and architectural style
   - Major components and their roles
   - Data flow through the system
   - Technology stack
   - Key architectural decisions and trade-offs

6. **Create `index.md`** with:
   - Project overview and purpose
   - Technology stack summary
   - Key file locations
   - Navigation guide to other documentation
   - Next steps for learning

**Output**: `.learning/` directory with initial structure and high-level architectural documentation

### Phase 2: Adaptive Guidance

**When**: User wants to learn about the codebase (first time or returning)

**Goal**: Guide user through understanding at the right pace and depth

**Steps**:

1. **Check if .learning exists**:
   - If no: Run Phase 1 first
   - If yes: Continue with guidance

2. **Assess the learner** (see `references/guided-learning.md` → Initial Assessment):
   ```
   To guide you effectively:
   
   1. What's your familiarity with [primary tech]?
      - Expert / Intermediate / Beginner / New
   
   2. What's your goal?
      - Quick overview / Deep understanding / Specific feature / Architecture
   
   3. Any specific interests or questions?
   ```

3. **Start the walkthrough**:
   - Present content from `.learning/architecture/overview.md`
   - Check understanding: "Does this match your expectations?"
   - Ask what to explore next

4. **Generate documentation on demand** as user explores:
   - When user asks about a concept → create `.learning/concepts/[name].md`
   - When user asks about a module → create `.learning/modules/[name].md`  
   - When user wants structured path → create `.learning/learning-paths/[topic].md`

5. **Maintain conversation flow**:
   - Reference previous topics: "Remember when we discussed [X]?"
   - Build connections: "This concept relates to [Y] that we covered earlier"
   - Check in regularly: "Ready to go deeper?" or "Want to explore something else?"

**Key principle**: Generate documentation incrementally as needed, not all at once

### Phase 3: Deep Dives

**When**: User wants detailed understanding of specific areas

**Steps**:

1. **For concepts** - Use Concept Documentation Template (`references/templates.md`):
   - Define the concept clearly
   - Explain why it exists (problem it solves)
   - Show where it's used in the codebase (with file paths)
   - Provide code examples from the actual codebase
   - Link to related concepts
   - Create as `.learning/concepts/[concept-name].md`

2. **For modules** - Use Module Documentation Template (`references/templates.md`):
   - Explain module purpose and responsibility
   - Document public interface (exports, key functions/classes)
   - Describe internal structure
   - Show data flow within module
   - Point to tests and usage examples
   - Create as `.learning/modules/[module-name].md`

3. **For learning paths** - Use Learning Path Template (`references/templates.md`):
   - Define prerequisites
   - Provide suggested reading order
   - Include key questions to answer
   - Suggest hands-on exercises
   - Create as `.learning/learning-paths/[topic].md`

**Exploration tips**:
- Use `view [path]` to examine specific files
- Use `bash_tool` with grep/find to search for patterns
- Read files to understand implementation details
- Cross-reference between files to trace data flow

## Adaptive Depth Guidelines

Match documentation detail to user's level (see `references/templates.md` → Documentation Depth Levels):

**Level 1 (High-level)** - For quick understanding:
- Architecture style and major components only
- 1-2 pages maximum
- Focus on what and why, not how

**Level 2 (Conceptual)** - For practical understanding:
- Key abstractions and how modules interact
- 5-10 pages across multiple docs
- Code snippets showing patterns
- Balance what, why, and how

**Level 3 (Detailed)** - For contribution-ready knowledge:
- Function-level breakdowns
- Detailed data structures and interfaces
- Error handling and edge cases
- 20+ pages with extensive examples
- Deep how with implementation details

## Interaction Principles

Follow these guidelines when guiding users (full details in `references/guided-learning.md`):

1. **Check before diving deep** - Confirm prerequisites before complex topics
2. **Use questions strategically** - Don't overwhelm; typically 1-3 questions at a time
3. **Watch for signals**:
   - Lost? Step back and simplify
   - Bored? Increase depth and pace
   - Overwhelmed? Break into smaller pieces
4. **Build mental models** - Help users organize knowledge with clear frameworks
5. **Adapt continuously** - Adjust based on user responses and questions

## File Organization

The `.learning/` directory structure:

```
.learning/
├── .gitignore              # Exclude from version control
├── index.md                # Project overview and navigation
├── architecture/
│   └── overview.md         # High-level architectural analysis
├── concepts/
│   ├── [concept-1].md      # Individual concept documentation
│   └── [concept-2].md
├── modules/
│   ├── [module-1].md       # Individual module documentation
│   └── [module-2].md
└── learning-paths/         # Optional: structured learning sequences
    └── [topic].md
```

## Common Patterns

**Pattern: User new to the codebase**
```
1. Check if .learning/ exists, create if not
2. Scan project structure with view tool
3. Read key config and entry point files
4. Generate architecture/overview.md
5. Ask about their experience and goals
6. Walk through architecture interactively
7. Generate concept/module docs on demand
```

**Pattern: User wants to understand specific feature**
```
1. Check if .learning/ exists, create if not
2. Ask what they already understand
3. Identify related modules and concepts (by viewing relevant directories)
4. Generate docs for those specific areas
5. Show how components connect to implement the feature
```

**Pattern: User wants to contribute**
```
1. Assess their general familiarity
2. Focus on architectural boundaries and module responsibilities
3. Generate detailed module docs for areas they'll modify
4. Explain testing patterns and conventions
5. Point to related code for reference
```

**Pattern: Returning user**
```
1. Check what documentation exists in .learning/
2. Ask what they want to explore today
3. Build on previous documentation
4. Reference prior topics covered
5. Generate new docs as they explore new areas
```

## Tips

- **Start small**: Don't document everything at once; generate docs as user explores
- **Use actual code**: Include real code examples from the codebase, not generic examples
- **Cross-reference**: Link between architecture, concepts, and modules bidirectionally
- **Check understanding**: Frequently verify the user is following along
- **Preserve context**: Remember what's been covered to build on previous knowledge
- **Be concise**: Quality over quantity; clear, focused docs are better than exhaustive ones
- **Explore iteratively**: Use view and bash tools to discover structure organically

## Exploration Commands

Useful bash commands for project exploration:

```bash
# Find all file types
find . -type f -name "*.ts" | head -20

# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Find entry points
find . -name "main.*" -o -name "index.*" -o -name "app.*"

# Find config files
find . -maxdepth 2 -name "*.json" -o -name "*.toml" -o -name "*.yaml"

# Search for patterns
grep -r "export.*function" src/ | head -10
```

## Resources

- **references/templates.md** - Documentation templates for architecture, concepts, modules, and learning paths
- **references/guided-learning.md** - Interaction patterns, conversation strategies, and assessment techniques
