---
name: project-architect
description: >
  Documentation-first project planning that produces implementation-ready blueprints and
  single-shot coding agent prompts. Generates 4 interconnected docs — SPECIFICATION.md,
  IMPLEMENTATION.md, TASKS.md, BRANDING.md — plus a self-contained PROMPT.md for autonomous
  execution by any coding agent. Includes interactive tech stack selection, design pattern
  recommendations, and architecture decisions with trade-off analysis. Trigger when user
  wants to: plan a project, create specs, architect a system, break work into tasks, choose
  a tech stack, get design pattern advice, generate a coding agent prompt, or do
  documentation-first development. Phrases: "plan my project", "spec this out", "architect",
  "help me plan", "what stack should I use", "generate a prompt", "break this into tasks",
  "project docs", "I want to build X".
license: MIT
compatibility: >
  Works with any coding agent that supports file read/write and user interaction.
  Optimized for WrongStack and Claude Code, also compatible with Cursor, Gemini CLI, Codex,
  and other agentskills.io-compatible agents.
metadata:
  author: ersinkoc
  version: "1.1.0"
  category: development
---

# Project Architect

A documentation-first project planning system that produces **implementation-ready blueprints**
and **agent-ready prompts**. The philosophy: think deeply, document thoroughly, then
execute with zero ambiguity. The final PROMPT.md is self-contained and portable — hand it to
**WrongStack**, **Claude Code**, or any agent that reads and writes files.

## Output Pipeline

```
[Discovery]  →  SPECIFICATION.md  →  IMPLEMENTATION.md  →  TASKS.md  →  BRANDING.md
                  (The What)           (The How)           (The Work)    (Identity)
                       ↓                    ↓                   ↓
                       └────────────────────┴───────────────────┘
                                          ↓
                                     PROMPT.md
                             (Single-Shot Agent Prompt)
```

Each document feeds the next. The final PROMPT.md synthesizes all documents into a single
prompt optimized for single-shot execution by any coding agent (WrongStack, Claude Code,
Cursor, and others).

## Reference Files

Read the appropriate reference file before generating each document:

| Phase | Reference File | When to Read |
|-------|---------------|--------------|
| Discovery | `${CLAUDE_PLUGIN_ROOT}/references/elicitation-guide.md` | Before asking any questions |
| Tech Stack | `${CLAUDE_PLUGIN_ROOT}/references/tech-stacks.md` | When user needs stack selection help |
| Patterns | `${CLAUDE_PLUGIN_ROOT}/references/design-patterns.md` | When making architecture decisions |
| Specification | `${CLAUDE_PLUGIN_ROOT}/references/specification-guide.md` | Before generating SPECIFICATION.md |
| Implementation | `${CLAUDE_PLUGIN_ROOT}/references/implementation-guide.md` | Before generating IMPLEMENTATION.md |
| Tasks | `${CLAUDE_PLUGIN_ROOT}/references/tasks-guide.md` | Before generating TASKS.md |
| Branding | `${CLAUDE_PLUGIN_ROOT}/references/branding-guide.md` | Before generating BRANDING.md |
| Prompt | `${CLAUDE_PLUGIN_ROOT}/references/agent-prompt.md` | Before generating PROMPT.md |

## Workflow

### Phase 0: Discovery & Elicitation

Read `${CLAUDE_PLUGIN_ROOT}/references/elicitation-guide.md` for the full question framework.

Before writing anything, understand the project through structured conversation.
Use `AskUserQuestion` tool aggressively for choices — the user should tap, not type,
whenever possible.

**Minimum understanding before any document generation:**
1. What does this project do? (elevator pitch)
2. Who is it for? (target audience)
3. What's the project type? (web app, CLI, library, API, mobile, desktop, infra tool)
4. What's the scope? (MVP vs full product)
5. Tech stack direction (or "help me choose")

**If the user says "help me choose a stack":**
Read `${CLAUDE_PLUGIN_ROOT}/references/tech-stacks.md` and run the interactive stack selection flow.
Present options with trade-offs using `AskUserQuestion`.

### Phase 1: SPECIFICATION.md

Read `${CLAUDE_PLUGIN_ROOT}/references/specification-guide.md` before generating.

Defines **what** the project is. Technology-aware but not implementation-detailed.
After generating, pause for user review.

### Phase 2: IMPLEMENTATION.md

Read `${CLAUDE_PLUGIN_ROOT}/references/implementation-guide.md` AND `${CLAUDE_PLUGIN_ROOT}/references/design-patterns.md` before generating.

Translates specification into **how** to build it. This is where you:
- Recommend design patterns based on the project's needs (consult patterns reference)
- Define concrete directory structures with file-by-file purpose
- Choose dependencies with rationale
- Define module interfaces and data flows
- Include code snippets for critical patterns (signatures, types, structural examples)

**Pattern Recommendations:** Consult `${CLAUDE_PLUGIN_ROOT}/references/design-patterns.md` and recommend specific
patterns with rationale. Don't just name-drop — show how each pattern applies to THIS project
with a short code sketch.

### Phase 3: TASKS.md

Read `${CLAUDE_PLUGIN_ROOT}/references/tasks-guide.md` before generating.

Converts implementation into **ordered work items**. Each task must be:
- Completable by a coding agent in a single session
- Self-contained with full context
- Ordered by strict dependency chain
- Include the exact files to create/modify

### Phase 4: BRANDING.md (Optional)

Read `${CLAUDE_PLUGIN_ROOT}/references/branding-guide.md` before generating.

Only generate if user wants it or the project is user-facing.

### Phase 5: PROMPT.md (Always Generate)

Read `${CLAUDE_PLUGIN_ROOT}/references/agent-prompt.md` before generating.

**This is the most critical output.** Synthesize all documents into a single-shot prompt
that any coding agent (WrongStack, Claude Code, Cursor, …) can execute to build the entire
project from scratch. The prompt must be completely self-contained, with inline code for
complex patterns and an ordered checklist of every file to create.

## Operating Rules

1. **Document order is sequential.** SPEC → IMPL → TASKS → BRANDING → PROMPT. Never skip ahead.

2. **Pause between documents.** Present each doc, ask for approval before the next.

3. **Use `AskUserQuestion` for decisions.** Tech stack, database, auth, deployment — any
   decision with 2-4 clear options should use interactive selection, not freeform questions.

4. **Recommend, don't dictate.** Present 2-3 options with trade-offs. Let user choose.
   If user says "you pick", choose and explain why.

5. **Scale to project size.** Weekend project = concise docs, 15-30 tasks. Enterprise
   platform = thorough docs, 100+ tasks. Match depth to ambition.

6. **Always save as files.** Every document goes to `./[project-name]/docs/` in the current
   working directory as Markdown files. Use the `Write` tool to save them.

7. **Cross-reference between documents.** IMPL references SPEC sections. TASKS reference IMPL
   modules. PROMPT inlines everything needed.

8. **No filler.** Every line must be specific to THIS project. Remove sections that would be
   generic boilerplate.

9. **Design patterns are recommendations.** When choosing patterns for IMPLEMENTATION.md,
   consult `${CLAUDE_PLUGIN_ROOT}/references/design-patterns.md` and match patterns to the project's specific needs.
   Include a brief "why this pattern" rationale for each recommendation.

## Plugin-Aware Integration

Check if the user has other Claude Code plugins or skills installed. If they do:

- **Frontend framework planner** (react-app-planner, nextjs-app-planner, etc.) → Suggest
  using it for deeper framework decisions after architect docs are done
- **Frontend design** → Reference it for UI component guidance in IMPLEMENTATION.md
- **Brand/design skills** → Integrate into BRANDING.md generation
- **MCP builder** → If project includes an MCP server, note the skill for implementation phase
- **Language-specific skills** (typescript-mastery, etc.) → Incorporate coding standards
  from that skill into IMPLEMENTATION.md

Mention relevant skills naturally: "You have a react-app-planner skill — want me to use it
for deeper React architecture decisions after we finish the high-level plan?"

## Handling Partial Input

| Scenario | Action |
|----------|--------|
| Vague 1-liner | Full elicitation flow with `AskUserQuestion` |
| Detailed brief | Extract answers, ask only gaps |
| Existing spec uploaded | Validate, suggest improvements, continue from Phase 2 |
| "Just the spec" | Generate SPECIFICATION.md only, offer to continue later |
| "Skip to tasks" | Gather context, generate lightweight spec+impl, then tasks |
| "Just give me a prompt" | Condensed discovery → direct PROMPT.md generation |
| "Help me choose a stack" | Run tech stack advisor from `${CLAUDE_PLUGIN_ROOT}/references/tech-stacks.md` |
| "What patterns should I use?" | Consult `${CLAUDE_PLUGIN_ROOT}/references/design-patterns.md`, ask about project |
