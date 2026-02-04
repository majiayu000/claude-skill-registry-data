---
name: sdd-render
description: Render JSON specs to human-readable markdown with AI-enhanced insights, visualizations, and progressive disclosure
---

# Spec Rendering Skill

## Overview

Transform JSON specification files into beautifully formatted, human-readable markdown documentation. The sdd-render skill bridges the gap between machine-readable specs and human comprehension, making it easy to review progress, share status, and understand project structure at a glance.

**Features:**
- **Markdown generation** - Convert JSON specs to formatted markdown with progress tracking
- **Visual progress indicators** - Status icons and percentage completion for phases/tasks
- **Dependency visualization** - Show task dependencies and blockers
- **Hierarchical structure** - Phases, groups, tasks, and subtasks clearly organized
- **Metadata display** - Estimates, complexity, reasoning, and file paths
- **Multiple output destinations** - Default location or custom paths via --output flag

## Core Workflow

**⚠️ CRITICAL REQUIREMENT: MANDATORY PRE-EXECUTION CHECKLIST ⚠️**

Before executing ANY `sdd render` command, you MUST complete this validation:

```
┌─────────────────────────────────────────────────────────────┐
│ PRE-EXECUTION DECISION TREE (MANDATORY)                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ❓ Has user EXPLICITLY specified a rendering mode?         │
│    (e.g., "use basic mode", "render with full AI")         │
│                                                             │
│         YES ─────────┐              NO                      │
│                      │               │                      │
│                      │               ▼                      │
│                      │      ✋ STOP - DO NOT RENDER YET     │
│                      │               │                      │
│                      │               ▼                      │
│                      │      🔴 REQUIRED ACTION:            │
│                      │         Use AskUserQuestion tool     │
│                      │         to ask for mode preference   │
│                      │               │                      │
│                      │               ▼                      │
│                      └──────────► ✅ Proceed with render    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**CRITICAL: Always Ask User for Rendering Mode**

Unless the user has explicitly specified a rendering mode in their request, you MUST use the AskUserQuestion tool to ask which mode they want:

**Example Usage:**
```
AskUserQuestion(
  questions: [{
    question: "Which rendering mode would you like to use?",
    header: "Render Mode",
    multiSelect: false,
    options: [
      {
        label: "Basic (fast, no AI)",
        description: "Quick rendering without AI features (< 2 seconds)"
      },
      {
        label: "Enhanced - Summary",
        description: "Executive summary with AI (~1-2 minutes)"
      },
      {
        label: "Enhanced - Standard (recommended)",
        description: "Balanced AI features (~3-5 minutes) [DEFAULT]"
      },
      {
        label: "Enhanced - Full",
        description: "Complete AI analysis (~5-8 minutes)"
      },
      {
        label: "Generate all versions for comparison",
        description: "Creates basic, standard, and full versions"
      }
    ]
  }]
)
```

**When to skip asking:**
- User explicitly requested a mode: "render with basic mode", "use full AI enhancement"
- User requested multiple versions: "generate all three versions", "compare enhancement levels"
- User is batch rendering multiple specs (use default enhanced standard)

**After getting the answer:**
- Map user's choice to the appropriate CLI flags
- Execute sdd render with the selected mode
- Report the rendering time and output location

---

### ❌ ANTI-PATTERNS: What NOT to Do

**WRONG APPROACH #1: Immediate execution without asking**

```
User: "Let's call the sdd-render skill for /path/to/spec.json"

❌ Assistant: I'll render the specification file for you.
   [Immediately executes: sdd render /path/to/spec.json]

   PROBLEM: Skipped asking about rendering mode preference
```

**CORRECT APPROACH #1: Ask first, then execute**

```
User: "Let's call the sdd-render skill for /path/to/spec.json"

✅ Assistant: I'll help you render that specification. First, let me ask
   which rendering mode you'd like to use.
   [Uses AskUserQuestion tool to present mode options]
   [After user answers, executes with chosen mode]
```

---

**WRONG APPROACH #2: Assuming default is okay**

```
User: "Can you render this spec?"

❌ Assistant: I'll use the default enhanced standard mode.
   [Executes without asking]

   PROBLEM: Assumed user wants default without confirming
```

**CORRECT APPROACH #2: Explicit confirmation**

```
User: "Can you render this spec?"

✅ Assistant: Which rendering mode would you prefer?
   [Presents options with AskUserQuestion]
   [User selects mode]
   [Executes with selected mode]
```

---

**ONLY ACCEPTABLE: User explicitly specifies mode**

```
User: "Render this spec with basic mode for speed"

✅ Assistant: I'll render using basic mode as you requested.
   [Executes: sdd render <spec-id> --mode basic]

   REASON: User explicitly specified "basic mode" - no need to ask
```

**3-Phase Process:**

1. **Prepare** - Ask user for mode (unless explicit), locate spec file, verify output destination
2. **Render** - Execute sdd render with appropriate flags based on user choice
3. **Review/Share** - View output and distribute as needed

**Key principles:**
- **Rendering is read-only** - Never modifies source JSON specs
- **Output customization** - Use --output for specific destinations
- **Batch operations** - Process multiple specs when needed
- **Always render AFTER updates** - Let other skills modify specs first, then render
- **Always ask for mode** - Unless explicitly specified by user

**Quick decision guide:**
- ✅ Need quick status check? → Ask user, they might want basic mode for speed
- ✅ Sharing with team? → Ask user, they might want enhanced standard
- ✅ Multiple specs? → Use default enhanced standard for batch operations
- ❌ Need to modify spec? → Use `Skill(sdd-toolkit:sdd-plan)` instead
- ❌ Need to update tasks? → Use sdd-update-subagent first, then render

## Skill Family

This skill is part of the **Spec-Driven Development** family:
- **Skill(sdd-toolkit:sdd-plan)** - Creates specifications and task hierarchies
- **Skill(sdd-toolkit:sdd-next)** - Identifies next tasks and creates execution plans
- **Skill(sdd-toolkit:sdd-render)** (this skill) - Renders JSON specs to human-readable formats
- **sdd-update-subagent** - Updates task and spec progress

## Use This Skill When

**Reporting and Communication:**
- Need to review a spec's overall structure and progress quickly
- Want to share spec status with team members or stakeholders
- Creating documentation for project planning meetings
- Generating weekly/monthly progress reports
- Onboarding new developers to understand project scope

**Analysis and Planning:**
- Analyzing task dependencies visually before starting work
- Identifying blockers across multiple phases
- Understanding critical path and task relationships
- Reviewing spec structure for completeness
- Validating phase organization and task breakdown

**Documentation:**
- Creating permanent records of project plans
- Archiving completed specifications for reference
- Generating proposals or estimates from specs
- Producing client-facing project timelines

## Decision Matrix

### Rendering Scope Decision

| Scenario | Action | Why |
|----------|--------|-----|
| Single active spec review | `sdd render {spec-id}` | Quick status check |
| All active specs status | Batch render all active specs | Comprehensive project overview |
| Client presentation | `sdd render {spec-id} --output client/report.md` | Professional delivery |
| Debugging spec structure | `sdd render {spec-id} --verbose` | Detailed diagnostics |
| Daily standup prep | Render + grep for progress | Extract quick metrics |
| Post-update verification | Render after sdd-update | Visualize changes |

### Output Destination Decision

| Audience | Destination | Format Considerations |
|----------|------------|----------------------|
| Development team | `specs/.human-readable/` (default) | Version controlled, easy access |
| Stakeholders | `docs/reports/` or `docs/status/` | Permanent documentation location |
| Clients | Custom path + PDF conversion | Professional presentation format |
| CI/CD pipelines | stdout (`--output -`) | Pipeline integration, no file I/O |
| Archive | `docs/archive/` with timestamp | Historical record keeping |

### Troubleshooting Decision Tree

**When rendering fails, check in order:**

1. **Spec file exists?**
   - ❌ No → Use `sdd find-specs --verbose` to locate
   - ✅ Yes → Continue to step 2

2. **JSON is valid?**
   - Test: `python3 -m json.tool <spec-file>.json`
   - ❌ Invalid → Fix JSON syntax or regenerate with sdd-plan
   - ✅ Valid → Continue to step 3

3. **Output directory writable?**
   - Test: `ls -la $(dirname <output-path>)`
   - ❌ No permission → Create directory or use default location
   - ✅ Writable → Continue to step 4

4. **Still failing?**
   - Run with `--debug` flag for detailed error messages
   - Check Troubleshooting section (line 799) for specific errors
   - Verify sdd CLI is properly installed: `sdd render --help`

## Do NOT Use For

**Spec Modification:**
- Creating new specifications (use `Skill(sdd-toolkit:sdd-plan)`)
- Updating task status or progress (use sdd-update-subagent)
- Modifying spec structure or metadata (use `Skill(sdd-toolkit:sdd-plan)`)
- Adding or removing tasks (use `Skill(sdd-toolkit:sdd-plan)`)

**Task Execution:**
- Finding next tasks to work on (use `Skill(sdd-toolkit:sdd-next)`)
- Creating execution plans (use `Skill(sdd-toolkit:sdd-next)`)
- Actually implementing code (use appropriate coding tools)
- Running tests or verification (use `Skill(sdd-toolkit:run-tests)`)

**Other:**
- Writing conceptual documentation (tutorials, guides)
- Generating code or test files
- Real-time collaboration (this creates static snapshots)

## Tool Verification

**Before using this skill**, verify the required tools are available:

```bash
# Verify sdd render command is installed
sdd render --help
```

**Expected output**: Help text showing available options for the render command

**IMPORTANT - CLI Usage Only**:
- ✅ **DO**: Use `sdd render` CLI command (e.g., `sdd render {spec-id}`)
- ❌ **DO NOT**: Execute Python scripts directly (e.g., `python cli.py`, `python renderer.py`)

The CLI provides proper error handling, validation, argument parsing, and interface consistency. Direct script execution bypasses these safeguards and may fail.

If the verification command fails, ensure the SDD toolkit is properly installed and accessible in your environment.

## Agent Boundaries

**CRITICAL: This skill is READ-ONLY**

This skill transforms JSON specs into markdown. It NEVER modifies the source specification files or any code.

**MANDATORY: Pre-Execution Mode Selection**

Before executing ANY render command, you MUST ask the user for their preferred rendering mode using the AskUserQuestion tool (unless the user explicitly specified a mode in their request). This is a non-negotiable requirement of the skill contract. See the Pre-Execution Decision Tree in the Core Workflow section above.

**What this skill does:**
- ✅ Reads JSON spec files from specs/active, specs/completed, specs/archived
- ✅ Generates markdown output files
- ✅ Writes to specs/.human-readable/ or custom --output path
- ✅ Displays progress, dependencies, and task metadata

**What this skill NEVER does:**
- ❌ Modifies source JSON spec files
- ❌ Updates task status or completion timestamps
- ❌ Creates or modifies code files
- ❌ Changes spec metadata or structure
- ❌ Executes tests or verification steps

**Handoff Points - When to Use Other Skills:**

**After successful rendering:**

1. **Spec structure looks wrong?**
   - → Hand off to `Skill(sdd-toolkit:sdd-plan)` to modify spec structure
   - Example: Missing phases, incorrect task organization

2. **Task status needs updating?**
   - → Hand off to sdd-update-subagent to update progress
   - Example: Mark tasks as completed, update timestamps
   - **IMPORTANT:** Update first, THEN render to visualize changes

3. **Ready to implement tasks?**
   - → Hand off to `Skill(sdd-toolkit:sdd-next)` to identify next task
   - Example: Need execution plan with gathered context

4. **Need to verify implementation?**
   - → Hand off to `Skill(sdd-toolkit:run-tests)` to run tests
   - Example: Run verification steps from spec

5. **Output is satisfactory?**
   - → Done, no further action needed
   - Share the rendered markdown as needed

**Never chain this skill with spec modification:**
- ❌ **Wrong:** Update task status → Render (race condition risk)
- ✅ **Correct:** Use sdd-update-subagent → Then render separately

**Always render AFTER making changes:**
- Create new spec with sdd-plan → Render to review
- Complete tasks with sdd-update → Render to visualize progress
- Major spec updates → Render to verify changes

**Consultation is never required for rendering:**
- Rendering is a deterministic transformation (JSON → Markdown)
- If rendering fails, use Troubleshooting Decision Tree (line 102)
- No external tool consultation needed for render operations

---

## Quick Start

**Execution Workflow:**

1. **Ask user for mode preference** (unless they explicitly specified):
   - Use AskUserQuestion tool (see example in Core Workflow section above)
   - Present the 5 mode options

2. **Execute the appropriate command** based on user's answer:

   **If user chose "Basic (fast, no AI)":**
   ```bash
   sdd render {spec-id} --mode basic
   # ~2 seconds
   ```

   **If user chose "Enhanced - Summary":**
   ```bash
   sdd render {spec-id} --enhancement-level summary
   # ~1-2 minutes
   # Note: --mode enhanced is implied when --enhancement-level is specified
   ```

   **If user chose "Enhanced - Standard" (or didn't specify):**
   ```bash
   sdd render {spec-id}
   # Default: enhanced mode with standard level (~3-5 minutes)
   # Equivalent to: sdd render {spec-id} --enhancement-level standard
   ```

   **If user chose "Enhanced - Full":**
   ```bash
   sdd render {spec-id} --enhancement-level full
   # ~5-8 minutes
   # Note: --mode enhanced is implied when --enhancement-level is specified
   ```

   **If user chose "Generate all versions for comparison":**
   ```bash
   # Generate all three versions with different output names
   sdd render {spec-id} --mode basic -o specs/.human-readable/{spec-id}-basic.md
   sdd render {spec-id} --enhancement-level standard -o specs/.human-readable/{spec-id}-standard.md
   sdd render {spec-id} --enhancement-level full -o specs/.human-readable/{spec-id}-full.md
   ```

3. **Report results** to the user (output location and any relevant information)

**Output Location:**
By default, rendered markdown is saved to `specs/.human-readable/{spec-id}.md`

**Mode Options for AskUserQuestion:**

Present these 5 options to the user:

| Option Label | CLI Command | Use Case |
|-------------|-------------|----------|
| "Basic (fast, no AI)" | `--mode basic` | Quick status checks (~2s) |
| "Enhanced - Summary" | `--enhancement-level summary` | Executive summaries (~1-2 min) |
| "Enhanced - Standard (recommended)" | (default, no flags needed) | Most use cases (~3-5 min) [DEFAULT] |
| "Enhanced - Full" | `--enhancement-level full` | Comprehensive analysis (~5-8 min) |
| "Generate all versions for comparison" | Multiple commands with different `-o` paths | Side-by-side comparison |

See the [AI Enhancement Modes](#ai-enhancement-modes) section below for detailed feature comparison.

---

## Current Rendering Features

### Basic Markdown Generation

The renderer converts JSON specification files into clean, readable markdown with:

**Header Section:**
- Spec title and ID
- Overall status and progress (X/Y tasks, percentage)
- Estimated effort and complexity
- Description and objectives

**Phase Sections:**
- Phase titles with progress indicators
- Phase-level metadata (purpose, risk level, estimates)
- Phase dependencies (blocked by, depends on)
- Nested task groups

**Task Details:**
- Task title with status icon
- File path being modified
- Estimated hours
- Changes description and reasoning
- Dependencies and blockers
- Subtask hierarchy

**Verification Steps:**
- Verification type (manual, automated, integration)
- Commands to execute
- Expected outcomes

### Status Icons

Visual indicators make progress instantly recognizable:

- ⏳ **Pending** - Task not yet started
- 🔄 **In Progress** - Currently being worked on
- ✅ **Completed** - Successfully finished
- 🚫 **Blocked** - Waiting on dependencies
- ❌ **Failed** - Encountered errors

### Progress Tracking

Progress is calculated and displayed at multiple levels:

**Spec Level:**
```
User Authentication System
Status: in_progress (15/23 tasks, 65%)
```

**Phase Level:**
```
## Phase 2: Authentication Service (5/8 tasks, 62%)
```

**Group Level:**
```
### File Modifications (4/5 tasks)
```

### Dependency Visualization

Dependencies are clearly shown to understand task relationships:

```markdown
**Depends on:** task-1-2, task-1-3
**Blocked by:** task-2-1
**Blocks:** task-3-1, task-3-2, task-3-3
```

This makes it easy to:
- Identify what must be completed before starting a task
- See what's blocking progress
- Understand which tasks depend on the current task

### Output Customization

**Default Output:**
```bash
sdd render my-spec-001
# Creates: specs/.human-readable/my-spec-001.md
```

**Custom Output Path:**
```bash
sdd render my-spec-001 --output docs/current-project.md
# Creates: docs/current-project.md
```

**Specify Specs Directory:**
```bash
sdd render my-spec-001 --path /path/to/specs
# Useful when working with multiple projects
```

---

## AI Enhancement Modes

The sdd-render skill supports multiple rendering modes to balance speed and feature richness. Choose the mode based on your needs for performance versus detailed AI-generated insights.

### Mode Overview

**Default Rendering:**
When you run `sdd render {spec-id}` without any flags, it uses **Enhanced Mode with Standard level** for balanced performance and features (~3-5 minutes).

**Two primary modes:**

1. **Basic Mode** (`--mode basic`)
   - Fast, traditional markdown rendering
   - No AI features
   - Uses SpecRenderer for deterministic output
   - Typical rendering time: < 2 seconds
   - Use when speed is critical or AI features aren't needed
   - **Must be explicitly specified** to override the enhanced default

2. **Enhanced Mode** (default, `--mode enhanced` optional)
   - AI-powered analysis and insights
   - Uses external AI CLI tools (gemini, cursor-agent, codex)
   - Default enhancement level: `standard`
   - Typical rendering time: 1-8 minutes depending on level
   - Automatically falls back to basic mode if AI tools unavailable
   - **The `--mode enhanced` flag is optional** - specifying `--enhancement-level` automatically enables enhanced mode

### Enhancement Levels

When using enhanced mode (the default), you can optionally specify one of three enhancement levels:

| Level | Features | Performance | Best For |
|-------|----------|-------------|----------|
| **summary** | Executive summary only | ~1-2 minutes | Quick AI overview for stakeholders |
| **standard** | Base features + narrative enhancement | ~3-5 minutes | Team reviews and status reports |
| **full** | All AI features (insights, visualizations, analysis) | ~5-8 minutes | Comprehensive documentation and planning |

### Feature Comparison

| Feature | Basic | Enhanced (summary) | Enhanced (standard) | Enhanced (full) |
|---------|-------|-------------------|-------------------|-----------------|
| Markdown generation | ✅ | ✅ | ✅ | ✅ |
| Progress indicators | ✅ | ✅ | ✅ | ✅ |
| Dependency visualization | ✅ | ✅ | ✅ | ✅ |
| Task hierarchies | ✅ | ✅ | ✅ | ✅ |
| Executive summary | ❌ | ✅ | ✅ | ✅ |
| Narrative enhancement | ❌ | ❌ | ✅ | ✅ |
| Priority ranking | ❌ | ❌ | ❌ | ✅ |
| Complexity scoring | ❌ | ❌ | ❌ | ✅ |
| AI insights & recommendations | ❌ | ❌ | ❌ | ✅ |
| Dependency graphs (Mermaid) | ❌ | ❌ | ❌ | ✅ |
| Task grouping suggestions | ❌ | ❌ | ❌ | ✅ |

### Usage Examples

**Default Rendering (Enhanced Standard):**
```bash
# Uses enhanced mode with standard level by default
sdd render my-spec-001

# Equivalent explicit forms
sdd render my-spec-001 --enhancement-level standard
sdd render my-spec-001 --mode enhanced --enhancement-level standard

# With custom output
sdd render my-spec-001 --output docs/team-status.md
```

**Basic Mode (fastest, no AI):**
```bash
# Must explicitly specify --mode basic to override enhanced default
sdd render my-spec-001 --mode basic

# For quick status checks
sdd render my-spec-001 --mode basic --output /tmp/quick-status.md

# When AI features aren't needed
sdd render my-spec-001 --mode basic
```

**Enhanced Mode with Summary:**
```bash
# Specifying --enhancement-level automatically enables enhanced mode
sdd render my-spec-001 --enhancement-level summary

# For stakeholder updates (--mode enhanced is optional, implied by --enhancement-level)
sdd render my-spec-001 --enhancement-level summary --output reports/exec-summary.md
```

**Enhanced Mode with Full Features:**
```bash
# Specifying --enhancement-level automatically enables enhanced mode
sdd render my-spec-001 --enhancement-level full

# Maximum AI analysis with all features (--mode enhanced is implied)
sdd render my-spec-001 --enhancement-level full --output docs/comprehensive-plan.md
```

### Generating Multiple Versions for Comparison

You can generate all three versions to compare outputs:

```bash
#!/bin/bash
SPEC_ID="my-spec-001"

# Generate basic version (fast reference)
sdd render $SPEC_ID --mode basic --output specs/.human-readable/${SPEC_ID}-basic.md

# Generate standard enhanced version (balanced)
sdd render $SPEC_ID --mode enhanced --enhancement-level standard --output specs/.human-readable/${SPEC_ID}-standard.md

# Generate full enhanced version (comprehensive)
sdd render $SPEC_ID --mode enhanced --enhancement-level full --output specs/.human-readable/${SPEC_ID}-full.md

echo "Generated three versions in specs/.human-readable/"
ls -lh specs/.human-readable/${SPEC_ID}-*.md
```

### Choosing the Right Mode

**Use Default (Enhanced Standard) when:**
- ✅ Most common use case - balanced speed and features
- ✅ Team reviews and status reports
- ✅ Narrative flow improves comprehension
- ✅ Weekly/monthly updates
- ✅ Client-facing documentation
- ✅ No special requirements (this is the default!)

**Override to Basic Mode when:**
- You need quick status checks (< 2 seconds)
- Working iteratively with frequent renders (rapid feedback loop)
- AI insights are not needed
- Output will be consumed by automated tools
- CI/CD pipeline integration where speed matters
- Daily standup preparation with time constraints
- Offline environment or AI tools unavailable

**Override to Enhanced Summary when:**
- Stakeholders need high-level AI overview only
- Executive reporting required (lighter than standard)
- Want faster than standard (~1-2 minutes vs ~3-5 minutes)
- AI-generated executive summary is the primary value
- Quick decision-making with AI context

**Override to Enhanced Full when:**
- Comprehensive project planning with deep analysis
- Need AI insights, recommendations, and visualizations
- Visual dependency graphs are valuable
- Archiving/documentation purposes (one-time comprehensive render)
- New team member onboarding (detailed explanations helpful)
- Performance not critical (~5-8 minutes acceptable)
- Maximum information density desired

### Interactive Mode Selection

**When invoked via the sdd-render skill (not direct CLI):**

The skill will proactively ask you which rendering mode you prefer using an interactive question:

```
Which rendering mode would you like to use?
○ Basic (fast, < 2 seconds, no AI)
○ Enhanced - Summary (executive summary, ~1-2 minutes)
○ Enhanced - Standard (recommended, balanced, ~3-5 minutes) ← default
○ Enhanced - Full (comprehensive analysis, ~5-8 minutes)
```

**Benefits of interactive selection:**
- No need to remember command-line flags
- Clear explanation of each option's tradeoffs
- Visual comparison of performance vs features
- Can choose "Other" to specify custom CLI parameters
- Default option clearly marked (Enhanced Standard)

**When to skip the question:**
If you already know which mode you want, you can specify it in your initial request:
- "Render with basic mode"
- "Render with full AI enhancement"
- "Generate all three versions for comparison"

The skill will respect your explicit request and skip the interactive question.

### AI Tooling

Enhanced mode uses external CLI tools for AI processing:

**Tool Priority Order:**
1. **gemini** (pro) - Primary for strategic analysis and summaries
2. **cursor-agent** (composer-1) - Secondary for repository-wide context
3. **codex** (gpt-5-codex) - Tertiary for code-level insights (disabled by default)

**Automatic Fallback:**
- System detects available tools automatically
- Tries tools in priority order
- Falls back to basic rendering if no AI tools available
- Configurable via `.claude/ai_config.yaml` (`sdd-render.tools` and `sdd-render.models`)

### Performance Considerations

**Rendering Times:**
- Basic: < 2 seconds (deterministic, no network calls)
- Enhanced (summary): ~1-2 minutes (one AI call for executive summary)
- Enhanced (standard): ~3-5 minutes (summary + narrative enhancement)
- Enhanced (full): ~5-8 minutes (all AI features, multiple analysis passes)

**Network Requirements:**
- Basic mode: No network required
- Enhanced mode: Requires AI tool availability and API access
- Offline fallback: Enhanced mode falls back to basic if tools unavailable

**Cost Considerations:**
- Basic mode: No API costs
- Enhanced mode: AI tool usage may incur API costs depending on configured tools
- Full enhancement level uses the most AI tokens

---

## Output Samples

### Spec Header

```markdown
# User Authentication System

**Spec ID:** user-auth-2025-10-24-001
**Status:** in_progress (15/23 tasks, 65%)
**Estimated Effort:** 45 hours
**Complexity:** High

## Description

Implement a secure user authentication system with JWT tokens, role-based access control, and session management.

## Objectives

- Secure password hashing with bcrypt
- JWT token generation and validation
- Role-based access control middleware
- Session management and refresh tokens
- Account lockout after failed attempts
```

### Phase with Tasks

```markdown
## Phase 2: Authentication Service (5/8 tasks, 62%)

**Purpose:** Implement core authentication logic
**Risk Level:** Medium
**Estimated Hours:** 18

### Tasks

#### ✅ task-2-1: Create AuthService class
**File:** src/services/authService.ts
**Estimated:** 3 hours
**Status:** completed
**Completed:** 2025-10-24 14:30:15

**Changes:**
Implement user registration with password hashing, add login method with JWT generation, include password validation logic

**Reasoning:** Centralizes authentication logic

**Blocks:** task-2-2, task-2-3

---

#### 🔄 task-2-2: Implement JWT middleware
**File:** src/middleware/auth.ts
**Estimated:** 2 hours
**Status:** in_progress

**Changes:**
Create Express middleware for JWT verification, add token expiration checking, handle invalid token responses

**Reasoning:** Protects API routes

**Depends on:** task-2-1 ✅
**Blocks:** task-2-3, task-2-4, task-2-5

---

#### ⏳ task-2-3: Add role-based authorization
**File:** src/middleware/rbac.ts
**Estimated:** 2.5 hours
**Status:** pending

**Changes:**
Create role checking middleware, define permission mappings, add route-level access control

**Reasoning:** Enables fine-grained access control

**Blocked by:** task-2-2 🔄
```

### Verification Steps

```markdown
#### verify-2-1: Verify authentication flow
**Type:** integration
**Estimated:** 1 hour

**Commands:**
```bash
npm test -- auth.integration.spec.ts
```

**Expected Outcome:**
All authentication tests pass, JWT token format is valid, protected routes reject invalid tokens
```

### Before/After Comparison

**JSON Input:**
```json
{
  "id": "task-2-1",
  "type": "task",
  "title": "Create AuthService class",
  "status": "completed",
  "metadata": {
    "file_path": "src/services/authService.ts",
    "estimated_hours": 3,
    "changes": "Implement user registration with password hashing",
    "reasoning": "Centralizes authentication logic"
  },
  "dependencies": {
    "blocks": ["task-2-2", "task-2-3"]
  }
}
```

**Rendered Output:**
```markdown
#### ✅ task-2-1: Create AuthService class
**File:** src/services/authService.ts
**Estimated:** 3 hours
**Status:** completed

**Changes:**
Implement user registration with password hashing

**Reasoning:** Centralizes authentication logic

**Blocks:** task-2-2, task-2-3
```

---

## CLI Tools Reference

### Core Commands

**Default Rendering (Enhanced Standard):**
```bash
sdd render {spec-id}
```
Renders a JSON spec with AI-enhanced narrative to markdown in the default location (`specs/.human-readable/`). Uses enhanced mode with standard level by default.

**Basic Mode (Fast, No AI):**
```bash
sdd render {spec-id} --mode basic
```
Quick rendering without AI features for speed-critical scenarios. Must explicitly specify `--mode basic` to override the enhanced default.

**Full AI Enhancement:**
```bash
sdd render {spec-id} --enhancement-level full
```
Maximum AI analysis with insights, visualizations, and recommendations. The `--mode enhanced` flag is optional - it's automatically enabled when you specify `--enhancement-level`.

**Custom Output Path:**
```bash
sdd render {spec-id} --output {path}
sdd render {spec-id} -o {path}
```
Specify where to save the rendered markdown file

**Specify Specs Directory:**
```bash
sdd render {spec-id} --path {specs-dir}
```
Use when specs are not in the default location

**Render from File Path:**
```bash
sdd render /path/to/spec-file.json
```
Directly render a JSON file by providing its full path

### Command Options

**Available Options:**

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--mode` | | Rendering mode: `basic` (fast, no AI) or `enhanced` (AI features). Optional - automatically set to `enhanced` when `--enhancement-level` is specified. | `enhanced` (with `standard` level) |
| `--enhancement-level` | | AI enhancement level: `summary`, `standard`, or `full`. Automatically enables `enhanced` mode. | `standard` |
| `--output` | `-o` | Output file path | `specs/.human-readable/{spec-id}.md` |
| `--path` | | Specs directory path | Auto-discovery |
| `--verbose` | `-v` | Show detailed output | Off |
| `--debug` | | Show debug information | Off |

**Key Options Explained:**

- `--mode basic` - Explicitly disables AI features for fast rendering (< 2 seconds). Must be specified to override enhanced default.
- `--mode enhanced` - Enables AI features (default, can be omitted). Automatically enabled when `--enhancement-level` is specified.
- `--enhancement-level summary` - Executive summary only (~1-2 minutes). Automatically enables enhanced mode.
- `--enhancement-level standard` - Balanced AI features (default, ~3-5 minutes). Automatically enables enhanced mode.
- `--enhancement-level full` - All AI features including visualizations (~5-8 minutes). Automatically enables enhanced mode.

### Examples

**Render with default settings (enhanced standard):**
```bash
sdd render user-auth-2025-10-24-001
# Uses: mode=enhanced (default), level=standard (default) (~3-5 minutes)
```

**Fast render without AI (basic mode):**
```bash
sdd render user-auth-2025-10-24-001 --mode basic
# Must explicitly specify --mode basic to override enhanced default
# Quick status check (< 2 seconds)
```

**Executive summary only:**
```bash
sdd render user-auth-2025-10-24-001 --enhancement-level summary
# Automatically enables enhanced mode (~1-2 minutes)
```

**Full AI analysis:**
```bash
sdd render user-auth-2025-10-24-001 --enhancement-level full
# Automatically enables enhanced mode (~5-8 minutes)
```

**Render to custom location:**
```bash
sdd render user-auth-2025-10-24-001 --output docs/auth-plan.md
# Default enhanced standard mode with custom path
```

**Basic mode to custom location (fast):**
```bash
sdd render user-auth-2025-10-24-001 --mode basic --output /tmp/quick-status.md
# Speed-optimized with custom output
```

**Render with verbose output:**
```bash
sdd render user-auth-2025-10-24-001 --verbose
# Shows: Total tasks, output size, processing time, AI tool used
```

**Render from specific specs directory:**
```bash
sdd render my-spec-001 --path /projects/myapp/specifications
```

**Render and view immediately:**
```bash
sdd render my-spec-001 && less specs/.human-readable/my-spec-001.md
```

**Generate multiple versions for comparison:**
```bash
# Basic (fast reference)
sdd render my-spec-001 --mode basic -o specs/.human-readable/my-spec-001-basic.md

# Standard (default, balanced)
sdd render my-spec-001 -o specs/.human-readable/my-spec-001-standard.md

# Full (comprehensive)
sdd render my-spec-001 --enhancement-level full -o specs/.human-readable/my-spec-001-full.md
```

---

## Workflow Examples

### Example 1: Weekly Progress Report

**Situation:** Need to generate a progress report for the weekly team meeting

**When to use this approach:**
- ✓ Regular team meetings require status updates
- ✓ Spec has been updated recently (tasks completed, status changed)
- ✓ Need to track progress over time with dated reports
- ✓ Team members prefer markdown over JSON

**Decision checklist:**
- **Spec updated?** → Yes → Render will show current progress
- **Need comparison?** → Keep previous week's report for comparison
- **Multiple projects?** → Batch render all active specs (see Example 3)
- **Presentation format?** → Consider PDF conversion (see Example 2)

**Steps:**

1. **Render current spec:**
```bash
sdd render user-auth-2025-10-24-001 -o reports/week-$(date +%Y-%m-%d).md
```

2. **Review the output:**
```bash
less reports/week-2025-10-24.md
```

3. **Share with team:**
```bash
# Copy to shared docs folder
cp reports/week-2025-10-24.md /shared/team-docs/

# Or email directly
mail -s "Weekly Progress" team@company.com < reports/week-2025-10-24.md
```

**Output includes:**
- Overall progress percentage
- Completed tasks this week
- Upcoming tasks
- Any blockers

**Why this approach works:**
- Timestamped filenames create historical record
- Custom output path keeps reports organized
- Markdown format is email-friendly and readable in any text editor

### Example 2: Client Status Update

**Situation:** Client wants to see project progress in readable format

**Steps:**

1. **Render spec to client docs:**
```bash
sdd render mobile-app-2025-09-15-001 --output client/project-status-$(date +%B).md
```

2. **Convert to PDF** (optional, requires pandoc):
```bash
pandoc client/project-status-October.md -o client/project-status-October.pdf
```

3. **Send to client:**
- Markdown is readable in email or GitHub
- PDF is professional and printable

### Example 3: Onboarding New Developer

**Situation:** New developer joins and needs to understand project scope

**Steps:**

1. **Render all active specs:**
```bash
for spec in specs/active/*.json; do
  spec_id=$(basename $spec .json)
  sdd render $spec_id
done
```

2. **Create index document:**
```bash
ls specs/.human-readable/ > docs/project-index.txt
```

3. **Point developer to documentation:**
- All specs are now in readable format
- Developer can browse and understand scope
- No need to parse JSON manually

### Example 4: Pre-Planning Review

**Situation:** Before starting implementation, review the spec structure

**When to use this approach:**
- ✓ New spec just created with `Skill(sdd-toolkit:sdd-plan)`
- ✓ Want to verify structure before beginning work
- ✓ Looking for dependency issues or circular references
- ✓ Assessing scope and task breakdown quality

**Decision checklist:**
- **New spec?** → Always review before implementation starts
- **Complex dependencies?** → Look for dependency visualization in output
- **Team review?** → Share rendered version for feedback
- **Issues found?** → Hand off to `Skill(sdd-toolkit:sdd-plan)` to modify

**Steps:**

1. **Render the spec:**
```bash
sdd render api-redesign-2025-10-01-001 --verbose
```

2. **Review for issues:**
- Check dependency chains (look for circular dependencies)
- Verify phase organization (logical progression?)
- Look for missing tasks (gaps in implementation?)
- Identify potential blockers (tasks with no dependencies marked?)

3. **Make adjustments** (if needed):
- Use `Skill(sdd-toolkit:sdd-plan)` to update spec
- Re-render to verify changes
```bash
sdd render api-redesign-2025-10-01-001
```

**Why this approach works:**
- Human-readable format makes structural issues obvious
- Verbose mode shows additional diagnostics
- Iterative review-modify-verify cycle ensures quality
- Catches planning issues before implementation begins

### Example 5: Archiving Completed Project

**Situation:** Project is complete, need permanent documentation

**Steps:**

1. **Render final version:**
```bash
sdd render user-dashboard-2025-08-01-001 --output archive/user-dashboard-final-$(date +%Y-%m-%d).md
```

2. **Create summary document:**
```bash
echo "# User Dashboard Project - Completed $(date +%Y-%m-%d)" > archive/README.md
echo "" >> archive/README.md
echo "See user-dashboard-final-*.md for complete specification" >> archive/README.md
```

3. **Archive the spec:**
- Move JSON to specs/completed/
- Keep markdown in permanent docs
- Commit to git for history

### Example 6: Comparing Enhancement Levels

**Situation:** Evaluating AI enhancement value or choosing the right level for your workflow

**When to use this approach:**
- ✓ First time using AI enhancements (want to see differences)
- ✓ Deciding which level to use for regular workflows
- ✓ Demonstrating AI capabilities to stakeholders
- ✓ Benchmarking rendering performance
- ✓ Creating documentation at multiple detail levels

**Decision checklist:**
- **Evaluating features?** → Generate all three to compare side-by-side
- **Performance testing?** → Time each mode with `time` command
- **Choosing default?** → Try all levels once, then stick with preferred
- **Multiple audiences?** → Keep multiple versions (basic for developers, full for stakeholders)

**Steps:**

1. **Generate all three versions:**
```bash
#!/bin/bash
SPEC_ID="user-auth-2025-10-24-001"

echo "Generating basic version (no AI)..."
time sdd render $SPEC_ID --mode basic \
  --output specs/.human-readable/${SPEC_ID}-basic.md

echo "Generating standard version (default AI)..."
time sdd render $SPEC_ID --enhancement-level standard \
  --output specs/.human-readable/${SPEC_ID}-standard.md

echo "Generating full version (maximum AI)..."
time sdd render $SPEC_ID --enhancement-level full \
  --output specs/.human-readable/${SPEC_ID}-full.md

echo "All versions generated!"
```

2. **Compare file sizes and render times:**
```bash
ls -lh specs/.human-readable/${SPEC_ID}-*.md

# Example output:
# -rw-r--r-- 1 user user  45K Oct 24 10:15 user-auth-2025-10-24-001-basic.md     (1.2s)
# -rw-r--r-- 1 user user  78K Oct 24 10:16 user-auth-2025-10-24-001-standard.md (58s)
# -rw-r--r-- 1 user user 120K Oct 24 10:17 user-auth-2025-10-24-001-full.md     (92s)
```

3. **Review each version:**
```bash
# Quick scan of basic version
less specs/.human-readable/${SPEC_ID}-basic.md

# Review standard enhancements
less specs/.human-readable/${SPEC_ID}-standard.md

# Examine full AI features
less specs/.human-readable/${SPEC_ID}-full.md
```

4. **Compare specific sections using diff:**
```bash
# Compare basic vs standard
diff specs/.human-readable/${SPEC_ID}-basic.md \
     specs/.human-readable/${SPEC_ID}-standard.md | head -50

# Compare standard vs full
diff specs/.human-readable/${SPEC_ID}-standard.md \
     specs/.human-readable/${SPEC_ID}-full.md | head -50
```

**What to look for in each version:**

**Basic Mode:**
- Clean, fast markdown rendering
- Standard progress indicators and task lists
- No AI-generated content
- Smallest file size

**Enhanced Standard:**
- Includes basic features plus:
- Executive summary section
- Narrative transitions between phases
- Contextual explanations
- Moderately larger file size

**Enhanced Full:**
- Includes standard features plus:
- AI-generated insights and recommendations
- Priority ranking analysis
- Complexity scoring
- Dependency graphs (Mermaid diagrams)
- Task grouping suggestions
- Largest file size with most detail

**Why this approach works:**
- Side-by-side comparison shows clear value of each level
- Timing data helps make performance tradeoff decisions
- Can choose different levels for different use cases
- One-time evaluation informs long-term workflow choices
- Demonstrates ROI of AI features to team/management

**Making your choice:**
- **Choose Basic** if speed > features and you don't need AI insights
- **Choose Standard** if you want AI narrative without full analysis (balanced default)
- **Choose Full** if you need comprehensive AI features and time isn't critical

---

## Integration Points

### With Skill(sdd-toolkit:sdd-plan)

**Creating Specs → Rendering Specs:**

```
1. Create spec with sdd-plan
   ↓
2. Spec saved as JSON in specs/active/
   ↓
3. Render with sdd-render for human review
   ↓
4. Share rendered markdown with team
```

**Use case:** After creating a new specification, immediately render it to markdown for team review before beginning implementation.

### With Skill(sdd-toolkit:sdd-next)

**Understanding Context → Finding Tasks:**

```
1. Render spec to understand overall structure
   ↓
2. Use sdd-next to identify next actionable task
   ↓
3. Render again after completing tasks to see progress
```

**Use case:** Before starting work, render the spec to understand the big picture, then use sdd-next for focused task execution.

### With sdd-update-subagent

**Tracking Progress → Visualizing Progress:**

```
1. Complete a task
   ↓
2. Update status with sdd-update
   ↓
3. Render spec to see updated progress
   ↓
4. Share progress report with stakeholders
```

**Use case:** After completing milestones, render the spec to generate a progress report showing what's been accomplished.

### With Skill(sdd-toolkit:run-tests)

**Verification → Documentation:**

```
1. Run tests with run-tests skill
   ↓
2. Update verification steps with results
   ↓
3. Render spec to document test outcomes
```

**Use case:** After running verification steps, the rendered spec shows which verifications passed and which are pending.

### With External Tools

**Generated markdown can be:**

- **Committed to git** for version control of project plans
- **Converted to PDF** using pandoc or similar tools
- **Embedded in wikis** (GitHub, Confluence, Notion)
- **Included in reports** using standard markdown processors
- **Shared via email** (readable in plain text)
- **Published to static sites** using Jekyll, Hugo, etc.

---

## Common Workflows

### Daily: Quick Status Check

```bash
# Render and view current status
sdd render current-project-001 && less specs/.human-readable/current-project-001.md

# Look for:
# - Progress percentage
# - Tasks completed today
# - Upcoming blockers
```

### Weekly: Team Sync

```bash
# Generate weekly report
sdd render current-project-001 -o team-sync/week-$(date +%U).md

# Review in meeting:
# - Progress since last week
# - Upcoming milestones
# - Team allocation
```

### Monthly: Stakeholder Update

```bash
# Render all active projects
for spec in specs/active/*.json; do
  spec_id=$(basename $spec .json)
  sdd render $spec_id -o stakeholder-updates/$(date +%Y-%m)/$spec_id.md
done

# Create summary:
# - Cross-project status
# - Key achievements
# - Upcoming priorities
```

### As-Needed: Debugging Spec Structure

```bash
# Render with verbose output
sdd render problem-spec-001 --verbose --debug

# Check for:
# - Malformed JSON
# - Circular dependencies
# - Missing metadata
# - Progress calculation issues
```

---

## Troubleshooting

### Issue: Spec Not Found

**Symptoms:**
```
Error: Spec not found: my-spec-001
```

**Solutions:**

1. **Check spec ID is correct:**
```bash
# List available specs
sdd find-specs --verbose
```

2. **Specify specs directory explicitly:**
```bash
sdd render my-spec-001 --path /path/to/specs
```

3. **Use full path to JSON file:**
```bash
sdd render /path/to/specs/active/my-spec-001.json
```

### Issue: Output File Permission Denied

**Symptoms:**
```
Error: Permission denied: /output/path/file.md
```

**Solutions:**

1. **Check directory permissions:**
```bash
ls -la /output/path/
```

2. **Create output directory:**
```bash
mkdir -p /output/path
```

3. **Use default output location:**
```bash
# Omit --output flag to use default
sdd render my-spec-001
```

### Issue: Malformed JSON

**Symptoms:**
```
Error: Failed to load spec file: Invalid JSON
```

**Solutions:**

1. **Validate JSON:**
```bash
python3 -m json.tool specs/active/my-spec-001.json
```

2. **Check for common issues:**
- Trailing commas
- Missing quotes
- Unclosed brackets

3. **Regenerate spec:**
```bash
# Use sdd-plan to recreate the spec
# This ensures valid JSON structure
```

### Issue: Missing Metadata

**Symptoms:**
Rendered markdown shows "Untitled" or missing information

**Solutions:**

1. **Update spec with missing information:**
- Use `Skill(sdd-toolkit:sdd-plan)` to add metadata
- Ensure title, description, objectives are populated

2. **Re-render:**
```bash
sdd render my-spec-001
```

---

## Advanced Usage

### Batch Rendering

**Render all active specs:**
```bash
#!/bin/bash
for spec in specs/active/*.json; do
  spec_id=$(basename "$spec" .json)
  echo "Rendering $spec_id..."
  sdd render "$spec_id"
done
```

**Render all specs in a status folder:**
```bash
# Render all completed specs
for spec in specs/completed/*.json; do
  spec_id=$(basename "$spec" .json)
  sdd render "$spec_id" -o docs/completed/$spec_id.md
done
```

### Integration with Git Hooks

**Pre-commit hook to render specs:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Render all active specs before committing
for spec in specs/active/*.json; do
  if [ -f "$spec" ]; then
    spec_id=$(basename "$spec" .json)
    sdd render "$spec_id"
    git add "specs/.human-readable/$spec_id.md"
  fi
done
```

**Benefits:**
- Always have up-to-date rendered versions
- Track changes in readable markdown
- Easy to review spec changes in PRs

### Custom Output Processing

**Extract progress percentage:**
```bash
sdd render my-spec-001 -o /tmp/spec.md
grep "Status:" /tmp/spec.md | grep -oP '\d+%'
```

**Generate progress badge:**
```bash
progress=$(sdd render my-spec-001 -o - | grep -oP '\d+%' | head -1)
echo "![Progress](https://img.shields.io/badge/progress-$progress-blue)"
```

**Create searchable index:**
```bash
# Render all specs and create full-text search index
for spec in specs/active/*.json; do
  spec_id=$(basename "$spec" .json)
  sdd render "$spec_id" >> docs/searchable-index.md
done
```

---

## Performance Considerations

### Rendering Speed by Mode

**Basic Mode Performance:**
- Small spec (10-20 tasks): < 100ms
- Medium spec (50-100 tasks): < 500ms
- Large spec (200+ tasks): < 2 seconds
- Very large spec (500+ tasks): < 5 seconds

**Enhanced Mode Performance:**
Performance depends on the enhancement level chosen:

| Mode | Small Spec | Medium Spec | Large Spec | Very Large Spec |
|------|-----------|-------------|------------|-----------------|
| Basic (no AI) | < 100ms | < 500ms | < 2s | < 5s |
| Enhanced (summary) | ~1 min | ~1.5 min | ~2 min | ~2.5 min |
| Enhanced (standard) | ~3 min | ~4 min | ~5 min | ~6 min |
| Enhanced (full) | ~5 min | ~6 min | ~7 min | ~8 min |

**Note:** Enhanced mode times are dominated by AI processing rather than spec size, so scaling is relatively flat.

**Factors affecting basic mode performance:**
- Number of tasks and subtasks
- Depth of task hierarchy
- Size of metadata fields
- Output file I/O

**Factors affecting enhanced mode performance:**
- AI tool response time (network latency)
- Enhancement level (summary < standard < full)
- AI model availability (gemini is fastest)
- Spec complexity affects AI analysis quality, not time

### Optimization Tips

**For speed-critical workflows:**
```bash
# Use basic mode when speed matters
sdd render my-spec-001 --mode basic

# Output to stdout (skips file I/O)
sdd render my-spec-001 --mode basic --output -

# Batch render with basic mode
for spec in specs/active/*.json; do
  sdd render $(basename $spec .json) --mode basic
done
```

**For balanced workflows (default):**
```bash
# Default enhanced standard provides good balance
sdd render my-spec-001

# Cache results for repeated access
sdd render my-spec-001 --output /tmp/cached-spec.md
```

**For comprehensive analysis (one-time renders):**
```bash
# Full enhancement for documentation
sdd render my-spec-001 --enhancement-level full --output docs/comprehensive.md
```

### AI Enhancement Performance

**Default Behavior:**
- Mode: Enhanced (can be changed with `--mode basic`)
- Level: Standard (can be changed with `--enhancement-level`)
- Estimated time: ~3-5 minutes for most specs

**AI Tooling:**
AI enhancements use external CLI tools via subprocess. The default priority order is:
1. **gemini** (pro model) - Primary for strategic analysis and summaries
2. **cursor-agent** (composer-1 model) - Secondary for repository-wide context
3. **codex** (gpt-5-codex model) - Tertiary for code-level insights (disabled by default)

**Automatic Fallback:**
- System detects available tools automatically
- Tries tools in priority order
- Falls back to basic rendering if no AI tools available
- No user intervention required

**Configuration:**
AI tool settings can be customized in `.claude/ai_config.yaml` (`sdd-render` section)

**Performance characteristics:**
- AI processing is one-time per render (results embedded in markdown)
- Output file is static (no runtime overhead when viewing)
- Can switch between modes based on needs
- Enhanced mode results are cacheable for repeated access

---

## File Locations

### Default Paths

**Input:**
- Auto-discovered from: `specs/active/`, `specs/completed/`, `specs/archived/`
- Can be overridden with `--path` option

**Output:**
- Default: `specs/.human-readable/{spec-id}.md`
- Can be overridden with `--output` option

### Directory Structure

```
project/
├── specs/
│   ├── active/               # Active specifications (JSON)
│   │   └── my-spec-001.json
│   ├── completed/            # Completed specifications
│   ├── archived/             # Archived specifications
│   └── .human-readable/      # Rendered markdown (generated)
│       └── my-spec-001.md    # Human-readable version
└── docs/
    └── planning/             # Optional: copy rendered docs here
```

**Note:** The `.human-readable/` directory is automatically created if it doesn't exist.

---

## Success Criteria

A rendering operation is successful when:

**File Creation:**
- ✓ Markdown file created at expected location
- ✓ File size > 0 bytes (not empty)
- ✓ File is valid markdown format

**Content Completeness:**
- ✓ Contains expected sections (metadata, phases, tasks)
- ✓ Progress percentages calculated correctly
- ✓ Dependencies displayed accurately
- ✓ All task metadata present (file paths, estimates, status)
- ✓ Verification steps included (if present in spec)

**No Errors:**
- ✓ No error messages during rendering
- ✓ No warnings about missing data
- ✓ Spec JSON file unchanged (read-only verified)

### Validation Checklist

Run these commands to verify successful rendering:

```bash
# 1. Check file exists
test -f specs/.human-readable/{spec-id}.md && echo "✓ File created"

# 2. Check file size (should be > 0)
test -s specs/.human-readable/{spec-id}.md && echo "✓ File not empty"

# 3. Check key sections present
grep -q "^## Phase" specs/.human-readable/{spec-id}.md && echo "✓ Phases found"

# 4. Check progress indicators
grep -q "tasks, [0-9]*%)" specs/.human-readable/{spec-id}.md && echo "✓ Progress calculated"

# 5. Check status icons present
grep -E "^#### (✅|⏳|🔄|🚫|❌)" specs/.human-readable/{spec-id}.md && echo "✓ Status icons present"

# 6. Verify source JSON unchanged
git diff specs/active/{spec-id}.json && echo "✓ Source spec unchanged"
```

### When Rendering is NOT Successful

**Symptoms and solutions:**

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| File created but empty | Invalid JSON spec | Validate with `python3 -m json.tool` |
| Missing sections | Incomplete spec structure | Check spec has phases and tasks |
| Progress shows 0% with completed tasks | Task status fields incorrect | Verify task.status values |
| No dependency info | Dependencies not in spec | Check spec.dependencies structure |
| Permission denied | Output directory not writable | Use default location or create directory |
| "Spec not found" error | Wrong spec-id or path | Use `sdd find-specs --verbose` |

**When to troubleshoot vs escalate:**

- **Minor issues** (formatting, missing optional fields) → Check Troubleshooting section
- **Cannot render at all** → Verify installation: `sdd render --help`
- **Spec structure problems** → Use `Skill(sdd-toolkit:sdd-plan)` to fix spec
- **Persistent errors** → Check spec JSON validity with validation tools

---

## Summary

**Core Responsibility:**
Transform JSON specification files into human-readable, well-formatted markdown documentation for easy review, sharing, and understanding.

**Current Capabilities:**
- ✅ Convert JSON specs to formatted markdown
- ✅ Display progress with visual indicators
- ✅ Show task hierarchies and dependencies
- ✅ Include metadata (estimates, complexity, reasoning)
- ✅ Support custom output paths
- ✅ Handle specs from multiple status folders

**Integration Points:**
- Reads specs created by `Skill(sdd-toolkit:sdd-plan)`
- Visualizes progress updated by sdd-update-subagent
- Complements `Skill(sdd-toolkit:sdd-next)` for context understanding
- Works alongside `Skill(sdd-toolkit:run-tests)` for verification documentation

**Key Benefits:**
- Make specs accessible to non-technical stakeholders
- Enable quick progress reviews without parsing JSON
- Facilitate team communication and reporting
- Create permanent records of project plans
- Support multiple use cases (reports, onboarding, planning)

**When to Use:**
Use this skill whenever you need to convert a machine-readable spec into a human-friendly format for review, sharing, or documentation purposes.
