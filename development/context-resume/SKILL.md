---
name: context-resume
description: Load module context from handoff files to resume work
allowed-tools:
  - Read
  - Bash
  - Skill # To invoke next skill
preconditions:
  - Handoff file must exist in one of 3 locations
---

# context-resume Skill

**Purpose:** Load module development context from `.continue-here.md` handoff files to enable pause/resume across sessions. Creates continuity between work sessions by preserving and restoring complete module development state.

## Overview

The handoff system allows modules to be paused at any point and resumed later with full context preservation. This skill is the universal entry point for resuming any type of work: implementation, ideation, panel iteration, or improvements.

**Key capabilities:**

- Locates handoff files across 3 possible locations
- Parses YAML frontmatter and markdown body for structured context
- Summarizes current state and progress
- Loads relevant contract files and source code
- Routes to appropriate continuation skill
- Handles missing or corrupted handoff files gracefully

## Handoff File Locations

### 1. Main workflow handoff

**Location:** `modules/[ModuleName]/.continue-here.md`
**Meaning:** Module is in active development (Stages 0-6)
**Created by:** module-workflow skill
**Contains:** Stage number, phase (if complex), completed work, next steps

### 2. Ideation handoff

**Location:** `modules/[ModuleName]/.ideas/.continue-here.md`
**Meaning:** Module is in planning/ideation phase
**Created by:** module-ideation skill
**Contains:** Creative brief status, panel status, ready-to-implement flag

### 3. Panel handoff

**Location:** `modules/[ModuleName]/.ideas/panels/.continue-here.md`
**Meaning:** Panel iteration in progress
**Created by:** panel-mockup skill
**Contains:** Current panel version, iteration notes, finalization status

---

## Resume Workflow

### Step 1: Locate Handoff

**When invoked with no module name:**

```bash
# User typed: /continue (no args)
# Present interactive selection menu
```

**List all modules with handoff files:**

```bash
# Search for .continue-here.md in all 3 locations
find modules -name ".continue-here.md" -type f

# Output format:
# modules/SimpleOsc/.continue-here.md
# modules/SimpleOsc/.ideas/.continue-here.md
# modules/WaveShaper/.continue-here.md
```

**Parse each handoff to extract:**
- Module name
- Type (workflow/ideation/panel)
- Stage/status
- Last updated timestamp

**Present interactive menu:**

```
Found 3 modules with active work:

1. SimpleOsc (Stage 3: Shell) - Updated 2 hours ago
2. SimpleOsc (Panel design v2) - Updated 1 day ago
3. WaveShaper (Stage 5: GUI) - Updated 3 days ago

Which module to resume?
1-3, or 'other': _
```

**When invoked with module name:**

```bash
# User typed: /continue SimpleOsc
MODULE_NAME="SimpleOsc"
```

**Search for handoff files:**

```bash
# Check all 3 locations
WORKFLOW_HANDOFF="modules/$MODULE_NAME/.continue-here.md"
IDEATION_HANDOFF="modules/$MODULE_NAME/.ideas/.continue-here.md"
PANEL_HANDOFF="modules/$MODULE_NAME/.ideas/panels/.continue-here.md"

# Determine which exist
test -f "$WORKFLOW_HANDOFF" && FOUND_WORKFLOW=true
test -f "$IDEATION_HANDOFF" && FOUND_IDEATION=true
test -f "$PANEL_HANDOFF" && FOUND_PANEL=true
```

**If multiple handoffs exist for same module:**

Present disambiguation menu:

```
SimpleOsc has multiple active handoffs:

1. Main workflow (Stage 3: Shell) - Updated 2 hours ago
2. Panel design (v2 iteration) - Updated 1 day ago

Which context to resume?
1-2, or 'other': _
```

**Recommendation logic:**
- Prefer workflow handoff if recent (< 24 hours)
- Prefer most recently updated handoff
- Suggest finishing panel before continuing workflow if panel incomplete

**If no handoff found:**

```
❌ No handoff file found for SimpleOsc

Checked locations:
- modules/SimpleOsc/.continue-here.md (not found)
- modules/SimpleOsc/.ideas/.continue-here.md (not found)
- modules/SimpleOsc/.ideas/panels/.continue-here.md (not found)

What's next?
1. Check MODULES.md - See if module exists but has no handoff
2. Start fresh - Begin new ideation for SimpleOsc
3. Other module - Resume different module
4. Other
```

### Step 2: Parse Handoff Context

**Load handoff file and parse YAML frontmatter:**

```markdown
---
module: SimpleOsc
stage: 3
stage_name: Shell
status: in_progress
last_updated: 2025-11-12T10:30:00Z
next_action: implement_module_struct
build_status: passing
test_status: not_run
---

## Current State

Stage 3 (Shell) implementation in progress.

## Completed Work

- ✓ Foundation complete (Stage 2)
  - CMakeLists.txt configured
  - Module registered in plugin.cpp
  - Build system validated

## Next Steps

1. Implement Module struct with DSP logic
2. Add process() method implementation
3. Test audio output with simple waveform

## Key Decisions

- Using simple wavetable oscillator (no anti-aliasing initially)
- 1V/oct tracking via standard frequency conversion
- Single monophonic voice for v1
```

**Extract structured data:**

```typescript
interface HandoffContext {
  // YAML frontmatter
  module: string;
  stage?: number;
  stage_name?: string;
  status: "in_progress" | "paused" | "blocked" | "ready_to_proceed";
  last_updated: string; // ISO timestamp
  next_action?: string;
  build_status?: "passing" | "failing" | "not_built";
  test_status?: "passing" | "failing" | "not_run";

  // Markdown body
  current_state: string;
  completed_work: string[];
  next_steps: string[];
  key_decisions: string[];
  blockers?: string[];
}
```

**Calculate time since last update:**

```typescript
const lastUpdated = new Date(context.last_updated);
const now = new Date();
const hoursSince = (now - lastUpdated) / (1000 * 60 * 60);

let timeAgo: string;
if (hoursSince < 1) timeAgo = `${Math.floor(hoursSince * 60)} minutes ago`;
else if (hoursSince < 24) timeAgo = `${Math.floor(hoursSince)} hours ago`;
else timeAgo = `${Math.floor(hoursSince / 24)} days ago`;
```

### Step 3: Present Context Summary

**Build user-facing summary:**

```
Resuming: SimpleOsc

📍 Where we are:
  Stage 3: Shell (DSP implementation)
  Status: In progress
  Last session: 2 hours ago

✓ Completed:
  - Stage 2: Foundation (CMake, module registration)
  - Build system configured and validated

→ Next steps:
  1. Implement Module struct with DSP logic
  2. Add process() method implementation
  3. Test audio output with simple waveform

📊 Build status: Passing
📊 Test status: Not run yet

🔑 Key decisions from planning:
  - Using simple wavetable oscillator
  - 1V/oct tracking via standard frequency conversion
  - Single monophonic voice for v1

Ready to continue?
1. Yes - Resume at Stage 3 Shell implementation (recommended)
2. Review contracts - See creative-brief.md, parameter-spec.md, plan.md
3. Check git history - See recent commits
4. Change direction - Start different work
5. Other
```

**Stale handoff warning:**

If `hoursSince > 24 * 14` (> 2 weeks):

```
⚠️ Stale handoff detected (last updated 18 days ago)

Code may have changed since last session. Recommend verification.

Options:
1. Resume anyway - Trust handoff state
2. Verify code first - Check for changes since last session
3. Start fresh - Discard stale handoff, begin anew
4. Other
```

### Step 4: Load Relevant Context

**Before invoking continuation skill, load contract files:**

**For workflow resume (Stages 0-6):**

```bash
MODULE_DIR="modules/$MODULE_NAME"

# Load contracts
test -f "$MODULE_DIR/.ideas/creative-brief.md" && cat "$MODULE_DIR/.ideas/creative-brief.md"
test -f "$MODULE_DIR/.ideas/parameter-spec.md" && cat "$MODULE_DIR/.ideas/parameter-spec.md"
test -f "$MODULE_DIR/.ideas/architecture.md" && cat "$MODULE_DIR/.ideas/architecture.md"
test -f "$MODULE_DIR/.ideas/plan.md" && cat "$MODULE_DIR/.ideas/plan.md"

# Load source files mentioned in handoff
if grep -q "src/" "$MODULE_DIR/.continue-here.md"; then
    # Extract file paths mentioned
    grep -o "src/[A-Za-z0-9_/-]*\\.cpp" "$MODULE_DIR/.continue-here.md" | while read file; do
        test -f "$MODULE_DIR/$file" && cat "$MODULE_DIR/$file"
    done
fi

# Check git log for recent changes
git log -10 --oneline --no-decorate -- "$MODULE_DIR"
```

**For ideation resume:**

```bash
MODULE_DIR="modules/$MODULE_NAME"

# Load creative brief
test -f "$MODULE_DIR/.ideas/creative-brief.md" && cat "$MODULE_DIR/.ideas/creative-brief.md"

# Check panel status
if [ -d "$MODULE_DIR/.ideas/panels" ]; then
    ls -t "$MODULE_DIR/.ideas/panels/" | head -5  # Latest 5 panel versions
fi
```

**For panel resume:**

```bash
MODULE_DIR="modules/$MODULE_NAME"

# Load creative brief and latest panel
test -f "$MODULE_DIR/.ideas/creative-brief.md" && cat "$MODULE_DIR/.ideas/creative-brief.md"

# Find latest panel version
LATEST_PANEL=$(ls -t "$MODULE_DIR/.ideas/panels/v*-panel.yaml" | head -1)
test -f "$LATEST_PANEL" && cat "$LATEST_PANEL"
```

### Step 5: Route to Continuation Skill

**Determine which skill to invoke based on handoff type:**

**Workflow handoff → module-workflow skill:**

```typescript
if (handoff.stage !== undefined) {
  // This is a workflow handoff (Stages 0-6)
  invoke("module-workflow", {
    module: handoff.module,
    resume_at_stage: handoff.stage,
    context: handoff,
  });
}
```

**Ideation handoff → module-ideation skill:**

```typescript
if (handoff.type === "ideation") {
  // This is ideation/planning handoff
  invoke("module-ideation", {
    module: handoff.module,
    context: handoff,
  });
}
```

**Panel handoff → panel-mockup skill:**

```typescript
if (handoff.type === "panel") {
  // This is panel iteration handoff
  invoke("panel-mockup", {
    module: handoff.module,
    resume_version: handoff.latest_version,
    context: handoff,
  });
}
```

**Improvement handoff → module-improve skill:**

```typescript
if (handoff.type === "improvement") {
  // This is improvement/modification handoff
  invoke("module-improve", {
    module: handoff.module,
    context: handoff,
  });
}
```

**Invoke with context preloaded:**

The continuation skill receives:
1. Module name
2. Handoff context (parsed YAML + markdown)
3. Loaded contract files in conversation history
4. Recent git history
5. Resume parameters (stage, version, etc.)

---

## Error Recovery

### No Handoff Found

**Check MODULES.md for module existence:**

```bash
grep -q "^- \*\*$MODULE_NAME\*\*" MODULES.md
```

**If module exists in MODULES.md but no handoff:**

```
Module exists but no active handoff found.

Checking git history to infer state...

Recent commits:
- feat(SimpleOsc): Stage 5 GUI complete (2 days ago)
- feat(SimpleOsc): Stage 4 DSP implementation (3 days ago)
- feat(SimpleOsc): Stage 3 Shell complete (4 days ago)

Based on git history, module appears complete (Stage 5 done).

What's next?
1. Verify completion - Test module in VCV Rack
2. Create improvement handoff - Make changes to completed module
3. Start fresh - Discard existing work, start over
4. Other
```

**If module doesn't exist anywhere:**

```
❌ Module not found: SimpleOsc

- Not in MODULES.md
- No source files in modules/SimpleOsc/
- No handoff files

What's next?
1. Start new module - Begin ideation for SimpleOsc
2. Different module - Choose existing module to resume
3. List all modules - See what's available
4. Other
```

### Corrupted Handoff File

**If YAML parsing fails:**

```bash
# Attempt to parse YAML frontmatter
if ! python3 -c "import yaml; yaml.safe_load(open('$HANDOFF_FILE').read().split('---')[1])" 2>/dev/null; then
    echo "YAML parsing failed"
fi
```

**Recovery:**

```
⚠️ Handoff file corrupted (YAML parsing failed)

Attempting to infer state from git log...

Recent commits:
- feat(SimpleOsc): Stage 3 Shell in progress (2 hours ago)
- feat(SimpleOsc): Stage 2 Foundation complete (1 day ago)

Inferred state: Stage 3 (Shell) in progress

What's next?
1. Resume at Stage 3 - Use inferred state from git
2. Manually recreate handoff - Fix corrupted file
3. Start fresh - Discard corrupted state
4. Other
```

### Multiple Handoffs for Same Module

**Present disambiguation menu:**

```
SimpleOsc has 2 active handoffs:

1. Main workflow (Stage 3: Shell)
   - Status: In progress
   - Updated: 2 hours ago
   - Next: Implement Module struct

2. Panel design (v2 iteration)
   - Status: Design iteration
   - Updated: 1 day ago
   - Next: Finalize v2 or iterate to v3

Recommendation: Complete panel design before continuing workflow

Which context to resume?
1. Main workflow (Stage 3)
2. Panel design (v2)
3. Cancel - Don't resume either
4. Other
```

### Stale Handoff (>2 weeks old)

**Check for code changes since last update:**

```bash
LAST_UPDATED=$(grep "^last_updated:" .continue-here.md | cut -d' ' -f2)
git log --since="$LAST_UPDATED" --oneline -- modules/$MODULE_NAME
```

**If changes detected:**

```
⚠️ Stale handoff + code changes detected

Handoff last updated: 18 days ago
Code changed: 3 commits since last update

Recent commits:
- fix(SimpleOsc): Parameter range correction (1 week ago)
- refactor(SimpleOsc): Cleanup DSP code (2 weeks ago)
- docs(SimpleOsc): Add inline comments (2 weeks ago)

What's next?
1. Review changes first - See what changed before resuming
2. Update handoff - Reconcile handoff with current code state
3. Discard handoff - Infer fresh state from code
4. Other
```

---

## Integration Points

**Invoked by:**

- `/continue` command (no args → interactive module selection)
- `/continue [ModuleName]` command (specific module)
- Natural language: "resume [ModuleName]", "continue working on [ModuleName]"

**Invokes:**

- `module-workflow` (workflow resume at specific stage)
- `module-ideation` (ideation resume for improvements)
- `panel-mockup` (panel iteration resume)
- `module-improve` (improvement implementation resume)

**Reads:**

- `.continue-here.md` files (all 3 locations)
- MODULES.md (status and version verification)
- Git log (commit history for inference)
- Contract files (creative-brief.md, parameter-spec.md, architecture.md, plan.md)
- Source files (if mentioned in handoff)
- CHANGELOG.md (for improvements)

**Updates:**

- Nothing directly (just reads and routes)
- Continuation skills will update handoff files as they proceed

---

## Success Criteria

Resume is successful when:

1. **Handoff located:** Found correct handoff file(s) from 3 possible locations
2. **Context parsed:** YAML and markdown extracted without errors
3. **State understood:** User sees clear summary of where they left off
4. **Continuity felt:** User doesn't need to remember details, handoff provides everything
5. **Appropriate routing:** Correct continuation skill invoked with right parameters
6. **Context loaded:** Contract files and relevant code loaded before proceeding
7. **Error handled:** Missing/corrupt handoff handled gracefully with fallbacks
8. **User control:** User explicitly chooses to continue, not auto-proceeded

---

## Notes for Claude

**When executing this skill:**

1. Always search all 3 handoff locations before declaring "not found"
2. Parse YAML carefully - handle missing optional fields gracefully
3. Present time-ago in human-readable format (not raw timestamps)
4. Show enough context that user remembers where they were
5. Don't auto-proceed - wait for explicit user choice
6. Load contract files BEFORE invoking continuation skill (provides context)
7. If handoff is stale/corrupt, use git log as backup source of truth
8. Preserve user's mental model - summary should match how they think about the module

**Common pitfalls:**

- Forgetting to check all 3 locations
- Auto-proceeding without user confirmation
- Not loading contract files before continuation
- Showing raw YAML instead of human summary
- Missing disambiguation when multiple handoffs exist

---

## VCV Rack Specific Context

**Module State Indicators:**

```yaml
# Workflow handoff typical fields
stage: 3  # 0-6
stage_name: "Shell"
build_status: "passing"  # passing/failing/not_built
rack_test_status: "not_run"  # passing/failing/not_run (manual testing in Rack)
helper_py_status: "success"  # success/failed (helper.py createmodule)
panel_finalized: true  # true/false (panel design locked)
```

**Ideation handoff typical fields:**

```yaml
creative_brief_status: "complete"  # draft/complete
panel_status: "in_progress"  # not_started/in_progress/finalized
latest_panel_version: 2
ready_to_implement: false  # true when brief + panel finalized
```

**Panel handoff typical fields:**

```yaml
latest_panel_version: 2
panel_finalized: false
iteration_count: 3
last_change: "Added scope display component"
```

**Git History Analysis for VCV Modules:**

Look for stage indicators in commit messages:
- "Stage 0: Ideation" or "panel design"
- "Stage 2: Foundation" or "CMake configured"
- "Stage 3: Shell" or "Module struct"
- "Stage 4: DSP" or "process() implementation"
- "Stage 5: GUI" or "ModuleWidget"
- "Stage 6: Validation" or "testing"

**Common Resume Scenarios:**

1. **Panel iteration paused:** Resume panel-mockup to continue design
2. **Mid-stage implementation:** Resume module-workflow at current stage
3. **Completed module improvement:** Resume module-improve to apply changes
4. **Ideation abandoned:** Check if worth resuming or starting fresh
5. **Multiple concurrent work:** Disambiguate between workflow/panel/ideation

**Time Sensitivity:**

- Panel iterations: Often paused for days (design thinking)
- Workflow stages: Usually completed in single session, pause indicates blocker
- Improvements: Can be paused indefinitely (backlog)
- Stale workflows (>2 weeks): High risk of context loss, verify code state
