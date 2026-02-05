---
name: create-project
description: "Create new projects. Load when user wants to START something new with a deliverable endpoint. Keywords: create project, new project, start project, plan project."
---

## 🎯 Onboarding Awareness (CHECK BEFORE STARTING)

**Before creating a project, AI MUST check user-config.yaml for incomplete onboarding:**

### Pre-Flight Check (MANDATORY)

```yaml
# Check learning_tracker.completed in user-config.yaml
learn_projects: false  → SUGGEST 'learn projects' skill FIRST
```

**If `learn_projects: false` AND this is user's FIRST project:**
```
💡 Before creating your first project, would you like a quick 8-minute tutorial
on how Nexus projects work? It covers:
- When to use projects vs skills (avoid common mistakes)
- Project structure and lifecycle
- How to track progress effectively

Say 'learn projects' to start the tutorial, or 'skip' to create directly.
```

**If user says 'skip':** Proceed with project creation but add this note at the end:
```
💡 Tip: Run 'learn projects' later if you want to understand the project system deeply.
```

**If `learn_projects: true`:** Proceed normally without suggestion.

### Recommended Onboarding Sequence

When checking `learning_tracker.completed`, if user hasn't done core onboarding:
1. `setup_goals: false` → Consider suggesting (but don't block project creation)
2. `learn_projects: false` → Suggest before FIRST project (high priority)

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CRITICAL EXECUTION REQUIREMENTS ⚠️

WORKFLOW: Structure FIRST, Collaborative Planning SECOND

MANDATORY STEPS (DO NOT SKIP):
1. ✅ Create TodoWrite with ALL steps
2. ✅ Offer project type selection (Build, Research, Strategy, Content, Process, Generic)
3. ✅ Ask project name
4. ✅ RUN init_project.py IMMEDIATELY (creates 4 directories + 3 planning files)
5. ✅ Display created structure
6. ✅ Load overview.md → Fill collaboratively → PAUSE → User confirms
7. ✅ Load plan.md → Apply mental models → Research dependencies → PAUSE → User confirms
8. ✅ Load steps.md → Break down execution → PAUSE → User confirms
9. ✅ Close session

ANTI-PATTERN (DO NOT DO THIS):
❌ Skip project type selection
❌ Skip running init_project.py
❌ Try to create files manually
❌ Generate content before structure exists
❌ Skip mental model questions (Socratic, devil's advocate)
❌ Skip dependency research
❌ Skip pauses between documents
❌ Complete skill in single response

CORRECT PATTERN (DO THIS):
✅ TodoWrite → Offer types → Ask name → RUN SCRIPT → Files created
✅ Then: Load overview.md → Fill collaboratively → PAUSE → Confirm
✅ Then: Load plan.md → Ask Socratic questions → Research dependencies → Add adaptive sections → PAUSE → Confirm
✅ Then: Load steps.md → Break down phases → PAUSE → Confirm
✅ Then: Close session

MENTAL MODELS (MANDATORY):
✅ Socratic Questioning during Approach section
✅ Devil's Advocate during risk assessment
✅ Dependency Research before completing plan.md

SCRIPT RUNS FIRST - ALWAYS!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create Project

Collaborative project design with intelligent, adaptive planning and deep thinking frameworks.

## Purpose

The `create-project` skill creates project structure and guides you through collaborative planning. The workflow: **Create structure FIRST** (via script), **THEN** fill in the templates with AI-guided depth.

**Key Features:**
- **Script-Generated Structure**: 4 directories (01-planning/, 02-resources/, 03-working/, 04-outputs/) + 3 planning files (overview, plan, steps) created immediately
- **Adaptive Planning**: Templates expand based on project type (Build, Research, Strategy, etc.)
- **Deep Thinking**: AI applies Socratic questioning and Devil's Advocate models
- **Dependency Research**: AI proactively finds and links related files/systems
- **Mandatory Pauses**: Review each document before proceeding
- **Separate Session Principle**: Project created now, executed later

---

## Two Modes
 
 This skill operates in two modes based on system state:
 
 ### 1. Workspace Setup Mode
 **When**: `02-projects/` directory doesn't exist
 **Purpose**: Create initial workspace folder structure (10-15 min)
 **Workflow**: See [workflows.md#workspace-setup](references/workflows.md#workspace-setup-workflow)
 
 ### 2. Project Creation Mode
 **When**: `02-projects/` exists
 **Purpose**: Full collaborative project planning (20-30 min)
 **Workflow**: See [workflows.md#project-creation](references/workflows.md#project-creation-workflow)

---

## Mode Detection Logic

**CRITICAL**: Before starting any workflow, detect which mode to use.

1. **Check for 02-projects/**:
   ```bash
   ls -d 02-projects/ 2>/dev/null
   ```
   - IF exists → **PROJECT_CREATION mode**
   - IF not exists → **WORKSPACE_SETUP mode** (System not initialized)

**Decision Tree**:
```
02-projects/ exists?
├── YES → PROJECT_CREATION mode
└── NO → WORKSPACE_SETUP mode
```

---

## Quick Start

### The One True Workflow: Intelligent Planning

**There is only ONE way to create projects** - always run the script first, then collaboratively plan with depth:

**Step 1: Initiation (< 1 minute)** ⚡
- Offer project types (Build, Research, Strategy, etc.)
- Run `scripts/init_project.py "Project Name" --path 02-projects`
- Auto-generates 4 directories: `01-planning/`, `02-resources/`, `03-working/`, `04-outputs/`
- Auto-generates 3 planning files in 01-planning/: `overview.md`, `plan.md`, `steps.md`

**Step 2: Collaborative Planning (15-30 minutes)** 🤔
- **overview.md**: Define purpose and success criteria
- **plan.md**:
  - AI suggests adaptive sections based on type
  - AI asks Socratic questions to test assumptions
  - AI researches dependencies and populates links
  - AI plays Devil's Advocate to identify risks
- **steps.md**: Break down execution into phases

**Step 3: Save & Execute Later** 💾
- Close session to save progress
- Execute project in a separate session with clean context

### Workflow Steps

1. **Detect mode** using logic above
2. **Offer project types** from [project-types.md](references/project-types.md)
3. **Run init_project.py** to create structure immediately
4. **Display** created structure
5. **Load workflow** from [workflows.md](references/workflows.md)
6. **Follow workflow step-by-step** with mandatory pauses
7. **Close session** to save state

---

## ⚠️ MANDATORY: Mental Models Selection

**CRITICAL**: Do NOT skip this step, even if you know which models to use from memory!

During the **plan.md** phase, AI **MUST run** select_mental_models.py script FIRST, then offer 2-3 relevant options to user.

**Required Workflow** (DO NOT SKIP):
1. **Run script FIRST** (before applying ANY models):
   ```bash
   python 00-system/mental-models/scripts/select_mental_models.py --format brief
   ```

2. **Review script output**: JSON array with all available mental models (59 models across 12 categories)

3. **Offer 2-3 relevant models** to user based on project type/context with brief (3-7 words) descriptions

4. **Wait for user selection**: User chooses which models to apply (or none)

5. **Load the specific model file** only after user selects:
   ```bash
   # Individual model files are in: 00-system/mental-models/models/{category}/{model-slug}.md
   # Example: 00-system/mental-models/models/cognitive/first-principles.md
   ```

6. **Apply questions** from selected models to fill plan.md collaboratively

**DO NOT**:
- ❌ Skip running select_mental_models.py script
- ❌ Apply models from memory without offering choice
- ❌ Auto-select models without user confirmation
- ❌ Skip user selection step

**Example Offer**:
```markdown
Now let's dive into planning. I've reviewed the mental models catalog and recommend for your Build/Create project:

1. **First Principles** – Strip assumptions, find fundamental truths
   Best for: Novel projects, challenging assumptions

2. **Pre-Mortem** – Imagine failure modes before implementation
   Best for: High-stakes projects, risk mitigation

3. **Stakeholder Mapping** – Identify all affected parties and interests
   Best for: Multi-party projects, organizational work

Which approach(es) sound most useful? Or we can combine them!
```

**Loading Pattern**:
```markdown
User picks: "First Principles + Pre-Mortem"

AI loads individual model files:
→ Read: 00-system/mental-models/models/cognitive/first-principles.md
→ Read: 00-system/mental-models/models/diagnostic/pre-mortem.md
→ Apply questions from both models to fill plan.md
```

**Benefits**:
- ✅ **Proactive** - AI always loads mental-models, shows what's available
- ✅ **User choice** - User picks which models (or none) to apply
- ✅ **Efficient metadata** - Brief (3-7 words) but descriptive
- ✅ **Individual files** - Each model has its own file with full details
- ✅ **Script-parseable** - YAML frontmatter for programmatic access
- ✅ **Maintainable** - Update one model file, all skills benefit

**See**: [`mental-models framework`](../../mental-models/mental-models.md) for full catalog and offering guidance

---

## Dependency Research

Before finalising **plan.md**, the AI will automatically:

- Scan the codebase for files that reference the same domain (using `codebase_search`).
- Look for existing **skills** that could be reused (e.g. `lead-qualification`).
- Identify external system configurations (MCP servers, Airtable schemas, Slack channels).
- Populate the **Dependencies & Links** section with concrete file paths and system names.

**Example auto‑generated section**:

```markdown
## Dependencies & Links
**Files Impacted**:
- `03-skills/lead-qualification/SKILL.md` – main workflow definition
- `04-workspace/airtable-schemas/leads.json` – lead data schema

**External Systems**:
- Airtable Base: "Leads" – source of lead data
- Slack Workspace: #sales – notification destination

**Related Projects**:
- Project 03: CRM Integration – shares Airtable connection
```

---

## Example Interaction Flow

```
AI: "What would you like to name your project?"
User: "Lead qualification workflow"

AI: "Great. This looks like a **Build/Create** project. I’ll add sections for Technical Architecture, Implementation Strategy, and Integration Points. Does that sound good?"
User: "Yes, go ahead."

AI: (runs init_project.py) → creates files.

AI: "Your project structure is ready. Let’s start with **overview.md**. What problem are you solving?"
User: "We lose leads because manual qualification takes too long."

AI: (fills purpose) → asks Socratic questions:
"What assumptions are you making about the current qualification time?"
User: "We estimate 30 minutes per lead based on recent logs."

AI: (adds to success criteria) → moves to **plan.md**.
AI: "I’ll now ask a few Socratic questions about your approach and then run a quick dependency scan."
... (continues) ...
```

---

## Resources

### scripts/
- **init_project.py**: ⚡ Quick project template generator
  - Auto-generates project structure with 4 directories (01-planning/, 02-resources/, 03-working/, 04-outputs/)
  - Auto-assigns next available project ID
  - Creates 3 planning files in 01-planning/: overview.md, plan.md, steps.md from templates
  - Usage: `python scripts/init_project.py "Project Name" --path 02-projects`

### references/
- **project-types.md**: Guide for offering project types and adaptive planning
- **workflows.md**: Complete interactive planning workflows for both modes
- **mental-models.md**: Full mental models catalog
- **project-schema.yaml**: YAML frontmatter schema documentation

---

## Error Handling

### Invalid Project ID/Name
- Explain validation rule clearly
- Show example of correct format
- Suggest correction

### Project Already Exists
- Inform user project exists
- Offer options: different name, different ID, or load existing

### Memory Files Missing
- Warn user: "Memory files not initialized"
- Suggest: "Please run 00-setup-memory project first"
- DO NOT create project

### User Abandons Mid-Creation
- Save partial work to temp file
- Inform: "Progress saved. Say 'continue project creation' to resume."

### User Skips Review
- Remind: "It's important we get this right!"
- Gently insist on review before proceeding

---

## Why This Design?

**Why Interactive?**
- Quality over speed: Thoughtful planning prevents rework
- User ownership: Collaborative design ensures buy-in
- Learning: Mental models teach strategic thinking
- Accuracy: Pauses catch issues early

**Why Mandatory Pauses?**
- Validation: User confirms understanding before proceeding
- Iteration: Catch issues before they cascade
- Ownership: User feels involved, not just spectator
- Quality: Better planning = smoother execution

**Why Separate Session?**
- Context management: Clean boundaries between planning and execution
- Focus: Execution session loads only execution context
- Memory: close-session properly saves state between phases
- UX: Matches natural work rhythm (plan now, execute later)

---

**Integration**:
- close-session automatically updates project-map.md every session
- validate-system checks project structure integrity
- Skills can reference project outputs in their workflows

---

**Remember**: This is a COLLABORATIVE DESIGN SESSION, not a quick generation tool. The time invested in thorough planning pays dividends during execution!
