---
name: cruise-control
description: Automatic mode - shift through all 6 gears sequentially without stopping. Like cruise control or automatic transmission, this runs the entire StackShift workflow from analysis to implementation in one go. Perfect for unattended execution or when you want to let StackShift handle everything automatically.
---

# Cruise Control Mode 🚗💨

**Automatic transmission for StackShift** - Shift through all 6 gears sequentially without manual intervention.

---

## When to Use This Skill

Use cruise control when:
- You want to run the entire workflow automatically
- Don't need to review each step before proceeding
- Trust StackShift to make reasonable defaults
- Want unattended execution (kick it off and come back later)
- Prefer automatic over manual transmission

**Trigger Phrases:**
- "Run StackShift in cruise control mode"
- "Automatically shift through all gears"
- "Run the full workflow automatically"
- "StackShift autopilot"

---

## What This Does

Runs all 6 gears sequentially:

```
Gear 1: Analyze → Gear 2: Reverse Engineer → Gear 3: Create Specs →
Gear 4: Gap Analysis → Gear 5: Complete Spec → Gear 6: Implement
```

**Without stopping between gears!**

---

## Setup

### Initial Configuration (One-Time)

At the start, you'll be asked:

1. **Route Selection:**
   ```
   Choose your route:
   A) Greenfield - Shift to new tech stack
   B) Brownfield - Manage existing code
   ```

2. **Implementation Framework:**
   ```
   Choose implementation framework:
   A) GitHub Spec Kit - Feature specs in .specify/, /speckit.* commands
   B) BMAD Method - Same docs, hands off to BMAD's collaborative agents
   ```

3. **Clarifications Handling:** (Spec Kit only)
   ```
   How to handle [NEEDS CLARIFICATION] markers?
   A) Defer - Mark them, implement around them, clarify later
   B) Prompt - Stop and ask questions interactively
   C) Skip - Only implement fully-specified features
   ```

4. **Implementation Scope:** (Spec Kit only)
   ```
   What to implement in Gear 6?
   A) P0 only - Critical features only
   B) P0 + P1 - Critical and high-value
   C) All - Everything (may take hours/days)
   D) None - Stop after specs are ready
   ```

Then cruise control takes over!

**Note**: For BMAD Method, questions 3-4 are skipped. BMAD agents handle clarifications and implementation through their interactive workflow.

---

## Execution Flow

### GitHub Spec Kit Path

#### Gear 1: Analyze (Auto)
- Detects tech stack
- Assesses completeness
- Sets route and framework (from your selections)
- Saves state with `auto_mode: true`
- **Auto-shifts to Gear 2** ✅

#### Gear 2: Reverse Engineer (Auto)
- Launches `stackshift:code-analyzer` agent
- Extracts documentation based on route
- Generates all 9 files (including integration-points.md)
- **Auto-shifts to Gear 3** ✅

#### Gear 3: Create Specifications (Auto)
- Calls automated spec generation (F002)
- Generates constitution (appropriate template for route)
- Creates all feature specs programmatically
- Creates implementation plans for incomplete features
- Sets up `/speckit.*` slash commands
- **Auto-shifts to Gear 4** ✅

#### Gear 4: Gap Analysis (Auto)
- Runs `/speckit.analyze`
- Identifies PARTIAL/MISSING features
- Creates prioritized roadmap
- Marks [NEEDS CLARIFICATION] items
- **Auto-shifts to Gear 5** ✅

#### Gear 5: Complete Specification (Conditional)
- If clarifications handling = "Defer": Skips, moves to Gear 6
- If clarifications handling = "Prompt": Asks questions interactively, then continues
- If clarifications handling = "Skip": Marks unclear features as P2, moves on
- **Auto-shifts to Gear 6** ✅

#### Gear 6: Implement (Based on Scope)
- If scope = "None": Stops, specs ready
- If scope = "P0 only": Implements critical features only
- If scope = "P0 + P1": Implements critical + high-value
- If scope = "All": Implements everything
- Uses `/speckit.tasks` and `/speckit.implement` for each feature
- **Completes!** 🏁

---

### BMAD Method Path

#### Gear 1: Analyze (Auto)
- Detects tech stack
- Assesses completeness
- Sets route and framework (from your selections)
- Saves state with `auto_mode: true`
- **Auto-shifts to Gear 2** ✅

#### Gear 2: Reverse Engineer (Auto)
- Launches `stackshift:code-analyzer` agent
- Extracts documentation (same 9 files as Spec Kit path)
- Generates all docs in `docs/reverse-engineering/`
- **Skips to Gear 6** ✅

#### Gears 3-5: Skipped
- BMAD agents handle PRD creation, architecture, and clarifications collaboratively
- StackShift's reverse-engineering docs provide rich context for BMAD

#### Gear 6: BMAD Handoff
- Displays instructions for BMAD installation and setup
- Provides `*workflow-init` command to start BMAD workflow
- Explains how to point BMAD to `docs/reverse-engineering/`
- **StackShift completes - BMAD takes over!** 🏁

---

## Progress Monitoring

While cruise control is running, you can check progress:

```bash
# See current gear
node plugin/scripts/state-manager.js status

# Detailed progress
node plugin/scripts/state-manager.js progress

# Watch progress in real-time
watch -n 5 'node plugin/scripts/state-manager.js progress'
```

Or via MCP resource:
```
Read stackshift://progress
```

---

## Interrupting Cruise Control

You can stop cruise control at any time:

```
"Stop cruise control"
"Pause StackShift"
"Switch to manual mode"
```

This will:
- Save current state
- Set `auto_mode: false`
- Allow you to proceed manually from current gear

You can resume cruise control later:
```
"Resume cruise control from current gear"
```

---

## Example: Full Automatic Run

```
User: "Run StackShift in cruise control mode"

StackShift:
Setting up cruise control...

Choose your route:
A) Greenfield - Shift to new tech stack
B) Brownfield - Manage existing code

User: "B - Brownfield"

StackShift:
How to handle clarifications?
A) Defer - Clarify later
B) Prompt - Ask me now
C) Skip - Only implement clear features

User: "A - Defer"

StackShift:
Implementation scope?
A) P0 only
B) P0 + P1
C) All features
D) None (stop after specs)

User: "B - P0 + P1"

StackShift:
✅ Cruise control engaged! Shifting through all gears automatically...

🔍 Gear 1: Analyzing... ✅ Complete (2 min)
🔄 Gear 2: Reverse engineering... ✅ Complete (8 min)
📋 Gear 3: Creating specifications... ✅ Complete (5 min)
🔍 Gear 4: Gap analysis... ✅ Complete (3 min)
✨ Gear 5: Completing specs (deferred clarifications)... ✅ Complete (1 min)
🚀 Gear 6: Implementing P0 + P1 features... 🔄 In Progress (est. 45 min)

   Feature 1/8: user-authentication... ✅
   Feature 2/8: fish-management... ✅
   Feature 3/8: photo-upload... 🔄 In progress...

[... continues automatically ...]

🏁 All gears complete! Application at 85% implementation.

Deferred clarifications (3) saved in: .specify/memory/clarifications.md
You can resolve these later with: /speckit.clarify
```

---

## Configuration Options

Cruise control can be configured via state:

```json
{
  "auto_mode": true,
  "auto_config": {
    "route": "brownfield",
    "clarifications_strategy": "defer",
    "implementation_scope": "p0_p1",
    "pause_between_gears": false,
    "notify_on_completion": true
  }
}
```

---

## Advanced: Scheduled Execution

Run cruise control in background:

```bash
# Start in background
nohup stackshift cruise-control --route brownfield --scope p0 &

# Check progress
tail -f stackshift-cruise.log

# Or via state
watch stackshift://progress
```

---

## Use Cases

### 1. Overnight Execution
```
5pm: "Run cruise control, brownfield, P0+P1, defer clarifications"
9am: Check results, review generated specs, answer deferred questions
```

### 2. CI/CD Integration
```yaml
# .github/workflows/stackshift.yml
- name: Run StackShift Analysis
  run: stackshift cruise-control --route brownfield --scope none
  # Generates specs, doesn't implement (safe for CI)
```

### 3. Batch Processing
```
Run cruise control on multiple projects:
- project-a: greenfield
- project-b: brownfield
- project-c: brownfield
```

### 4. Demo Mode
```
"Show me what StackShift does - run full demo"
→ Runs cruise control with sample project
```

---

## Safety Features

### Checkpoints

Cruise control creates checkpoints at each gear:
- State saved after each gear completes
- Can resume from any checkpoint if interrupted
- Rollback possible if issues detected

### Validation

Before proceeding:
- Validates output files were created
- Checks for errors in previous gear
- Ensures prerequisites met

### User Intervention

Pauses automatically if:
- Critical error detected
- `/speckit.analyze` shows major inconsistencies
- Implementation fails tests
- Disk space low
- Git conflicts detected

---

## Manual Override

At any point, you can:

```
"Pause after current gear"
"Stop cruise control"
"Switch to manual mode"
"Take control"
```

State saved, you can continue manually from that point.

---

## Success Criteria

### GitHub Spec Kit Path

After cruise control completes:

- ✅ All 6 gears complete
- ✅ `.stackshift-state.json` shows 6/6 gears
- ✅ All output files generated
- ✅ GitHub Spec Kit initialized (`.specify/` directory)
- ✅ Features implemented (based on scope)
- ✅ Ready for production (or clarifications if deferred)

### BMAD Method Path

After cruise control completes:

- ✅ Gears 1, 2, 6 complete (3-5 skipped)
- ✅ `.stackshift-state.json` shows framework: "bmad"
- ✅ `docs/reverse-engineering/` structure generated (same 9 files as Spec Kit)
- ✅ BMAD handoff instructions displayed
- ✅ Ready for `*workflow-init` to create PRD/Architecture collaboratively

---

## Technical Notes

- Cruise control is a special skill that orchestrates other skills
- Each gear is still executed by its corresponding skill
- Auto mode can be toggled on/off at any time
- State tracks auto_mode for resume capability
- Great for CI/CD, batch processing, or overnight runs

---

**Remember:** Cruise control is like automatic transmission - convenient and hands-off. Manual mode (using individual skills) gives you more control. Choose based on your needs!

🚗 **Manual** = Control each gear yourself
🤖 **Cruise Control** = Let StackShift handle it

Both get you to the same destination!
