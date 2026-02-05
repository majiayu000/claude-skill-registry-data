---
name: ui-mockup
description: Orchestrator for WebView UI mockup workflow - delegates design iteration to ui-design-agent and implementation scaffolding to ui-finalization-agent. Use when user mentions UI design, mockup, WebView interface, or requests 'design UI for [plugin]'.
allowed-tools:
  - Read
  - Task
  - AskUserQuestion
preconditions:
  - None (can work standalone or with creative brief)
---

# ui-mockup Skill

Pure orchestrator for WebView UI mockup workflow. Gathers requirements from user, delegates file generation to specialized subagents.

**Orchestration Pattern:**
- NEVER generates files directly
- Phase A (design iteration): Delegates to ui-design-agent
- Phase B (implementation scaffolding): Delegates to ui-finalization-agent
- User interaction handled by orchestrator
- File generation handled by subagents in fresh contexts

## Two-Phase Workflow

### Phase A: Design Iteration

**Purpose:** Generate 2 design files for rapid iteration.

**Outputs:**
1. `v[N]-ui.yaml` - Machine-readable design specification
2. `v[N]-ui-test.html` - Browser-testable mockup

**STOP:** Do NOT proceed to Phase B until user approves design via Phase 5.5 decision menu.

### Phase B: Implementation Scaffolding

**Purpose:** Generate 5 implementation files ONLY after Phase A approval.

**Outputs:**
3. `v[N]-ui.html` - Production HTML
4. `v[N]-PluginEditor.h` - C++ header boilerplate
5. `v[N]-PluginEditor.cpp` - C++ implementation boilerplate
6. `v[N]-CMakeLists.txt` - WebView build configuration
7. `v[N]-integration-checklist.md` - Implementation steps

All files saved to: `plugins/[PluginName]/.ideas/mockups/`

## Workflow Context Detection

**Standalone Mode:**
- No `.continue-here.md` file present
- Generates mockups independently
- Skips state updates

**Workflow Mode:**
- File `plugins/[PluginName]/.continue-here.md` exists with `current_stage` field
- Updates workflow state after each phase

Check for `.continue-here.md` existence to determine mode. If present, update state files. If absent, skip state updates.

## Phase 0: Check for Aesthetic Library

Check if `.claude/aesthetics/manifest.json` exists. If found, count aesthetics using jq.

**If aesthetics exist, present menu:**

```
Found {N} saved aesthetics in library.

How would you like to start the UI design?
1. Start from aesthetic template - Apply saved visual system
2. Start from scratch - Create custom design
3. List all aesthetics - Browse library before deciding

Choose (1-3): _
```

**Option 1:** Display aesthetics from manifest with metadata (name, vibe, colors, source). Invoke ui-template-library skill with "apply" operation. Skip to Phase 4 with generated mockup.

**Option 2:** Continue to Phase 1 (load context).

**Option 3:** Invoke ui-template-library skill with "list" operation, show previews, return to menu.

**If no aesthetics:** Skip directly to Phase 1.

See `references/aesthetic-integration.md` for complete integration details.

---

## Phase 1: Load Context from Creative Brief

If `plugins/$PLUGIN_NAME/.ideas/creative-brief.md` exists, read it and extract:
- Plugin type (compressor, EQ, reverb, synth, utility)
- Parameter count and types
- Visual style mentions
- Layout preferences
- Special elements (meters, waveforms, visualizers)
- Color/theme references

See `references/context-extraction.md#example-extracting-from-creative-brief` for extraction examples.

**Extract UI context:**
- UI Concept section: Layout preferences, visual style
- Parameters: Count and types (determines control layout)
- Plugin type: Affects typical layouts
- Vision section: Visual references or inspirations

## Phase 1.5: Context-Aware Initial Prompt

Adapt prompt based on creative brief contents:

**Rich UI details exist:**
```
I see you want [extracted description from UI Concept] for [PluginName]. Let's refine that vision. Tell me more about the layout, control arrangement, and visual elements you're imagining.
```

**Minimal UI details:**
```
Let's design the UI for [PluginName]. You mentioned it's a [type] with [X] parameters. What layout and style are you envisioning?
```

**Zero UI context:**
```
Let's design the UI for [PluginName]. What do you envision? (layout, style, controls, visual elements)
```

Don't ask user to repeat information from creative brief. Build on what they provided.

**Listen for:** Layout preferences, visual references, mood/feel, special requests.

Capture verbatim notes before moving to targeted questions.

## Phase 2: Gap Analysis and Question Prioritization

**Question Priority Tiers:**
- **Tier 1 (Critical):** Layout structure, control types
- **Tier 2 (Visual):** Visual style, key visual elements
- **Tier 3 (Polish):** Colors, typography, animations

Extract from Phase 1.5 response and creative brief. Identify gaps in coverage. Never ask about already-provided information.

## Phase 2.5: Calculate Recommended Dimensions

Calculate space requirements before asking for window size.

See `references/layout-validation.md` Section 2 (Calculation Helpers) for formulas.

**Steps:**
1. Parse requirements: Count controls, identify layout type, note special elements
2. Estimate control sizes using typical sizes from layout-validation.md
3. Apply layout-specific formula (horizontal/vertical/grid)
4. Calculate: `recommended = absolute_minimum × 1.2`, round to nearest 50px
5. Enforce constraints: min 400×300, max 1200×800

**Present calculation:**
```
Based on your requirements:
- Layout: [type]
- Controls: [count] controls ([types])
- Special elements: [list]

Calculated space requirements:
- Absolute minimum: [min_width] × [min_height] px
- Recommended: [rec_width] × [rec_height] px

[Continue to Phase 3]
```

Store calculated dimensions for Phase 3. DO NOT ask for window size yet.

## Phase 3: Question Batch Generation

Generate exactly 4 questions using AskUserQuestion based on identified gaps.

**Rules:**
- If 4+ gaps exist: ask top 4 by tier priority
- If fewer gaps: pad with tier 3 questions
- Provide meaningful options (not just open text)
- "Other" option automatically added
- Users can skip via "Other" and typing "skip"

**Note:** Internal questions use AskUserQuestion tool. Final decision menus (Phase 5.5, 10.7) use inline numbered format per checkpoint protocol.

**Window Size Question (uses Phase 2.5 calculations):**

```
Question:
  question: "Window dimensions for your plugin?"
  header: "Window size"
  options:
    - label: "[calculated_width]×[calculated_height] (recommended)"
      description: "Calculated based on your layout and controls"
    - label: "Custom size"
      description: "Specify different dimensions"
```

If custom size chosen, ask for specific dimensions. If smaller than absolute minimum, present warning menu.

See `references/design-questions.md#example-question-batches` for question templates and tiering examples.

## Phase 3.5: Decision Gate

Use AskUserQuestion after each question batch:

```
Question:
  question: "Ready to finalize the mockup design?"
  header: "Next step"
  options:
    - label: "Yes, finalize it"
      description: "Generate YAML and test HTML"
    - label: "Ask me 4 more questions"
      description: "Continue refining"
    - label: "Let me add more context first"
      description: "Provide additional details"
```

**Route based on answer:**
- Option 1 → Proceed to Phase 4
- Option 2 → Return to Phase 2 (re-analyze gaps)
- Option 3 → Collect free-form text, return to Phase 2

## Phase 4-5.45: Dispatch ui-design-agent

Invoke ui-design-agent via Task tool to generate YAML + test HTML.

See `references/delegation-protocols.md` for complete invocation protocol.

**Summary:**
1. Read context files in parallel (creative-brief.md, aesthetic template, previous version)
2. Detect version number (find highest v[N], increment)
3. Construct prompt with all context
4. Invoke via Task tool with subagent_type: "ui-design-agent"
5. Wait for JSON report
6. Handle result (error menu if failed, continue to Phase 5.5 if success)

---

## Phase 5.5: Design Decision Menu (GATE)

**CRITICAL:** Phases 6-10 ONLY execute if user chooses option 2 (Finalize).

Present decision menu:

```
✓ Mockup v[N] design created (2 files)

Files generated:
- v[N]-ui.yaml (design specification)
- v[N]-ui-test.html (browser-testable mockup)

What would you like to do?

1. Iterate - Refine design, adjust layout
2. Finalize - Validate alignment and complete mockup
3. Save as template - Add to aesthetic library for reuse
4. Other

Choose (1-4): _
```

**Option 1: Iterate**
- Collect refinement feedback
- Return to Phase 2 with new version (v2, v3, etc.)
- Invoke NEW ui-design-agent instance (fresh context)

**Option 2: Finalize**
- Proceed to Phase 5.6 (automatic brief update)
- Mockup is source of truth for UI sections
- No user interaction needed
- Continue to Phase 6-10 after brief sync

**Option 3: Save as template**
- Invoke ui-template-library skill with "save" operation
- After saving, return to Phase 5.5 menu

**Option 4: Other**
- Handle custom request (test in browser, validate constraints, etc.)

See `references/decision-menus.md#phase-5-5-design-decision-menu` for detailed routing.

---

## Phase 5.6: Update Creative Brief from Finalized Mockup

**Trigger:** User selected "Finalize" in Phase 5.5

**Protocol:**

1. Check if `creative-brief.md` exists. If not, skip to Phase 6-10.
2. Determine plugin name and mockup version.
3. Execute: `.claude/utils/sync-brief-from-mockup.sh "${PLUGIN_NAME}" "${MOCKUP_VERSION}"`
4. Script preserves conceptual sections (Vision, Use Cases, Inspirations), updates Parameters and UI Concept from mockup.
5. Update `.continue-here.md` with sync metadata (if workflow mode).
6. Commit changes.
7. Present confirmation, continue to Phase 6-10.

**No user interaction required** - automatic update with confirmation display only.

---

## Phase 6-10: Implementation Scaffolding (PHASE B)

**Prerequisites for ALL Phase B phases:**
- User confirmed design in Phase 5.5 (selected option 2: Finalize)
- Phase A files exist (`v[N]-ui.yaml`, `v[N]-ui-test.html`)
- Finalization marker present in YAML

See `references/phase-b-enforcement.md` for guard implementation.

## Phase 6-10.5: Dispatch ui-finalization-agent

Invoke ui-finalization-agent via Task tool to generate 5 implementation files.

See `references/delegation-protocols.md` for complete invocation protocol.

**Summary:**
1. Read finalized design files in parallel (YAML, HTML, parameter-spec.md if exists)
2. Detect if parameter-spec.md generation needed (v1 mockups only)
3. Construct prompt with contracts
4. Invoke via Task tool with subagent_type: "ui-finalization-agent"
5. Wait for JSON report
6. Handle result (error menu if failed, continue to Phase 10.7 if success)

---

## Phase 10.7: Completion Menu

Present completion menu after ui-finalization-agent returns successfully.

See `references/decision-menus.md#completion-menu` for format and routing.

---

## Orchestration Protocol

Pure orchestrator pattern with strict delegation rules.

### Delegation Rules

**This skill NEVER generates mockup files directly. ALL file generation delegated to subagents.**

Correct sequence:
1. Orchestrator: Gather requirements (Phases 0-3.5)
2. Orchestrator: Invoke ui-design-agent via Task tool
3. ui-design-agent: Generate YAML + test HTML, commit, return JSON
4. Orchestrator: Parse JSON, present Phase 5.5 menu
5. If iterate: Orchestrator invokes NEW ui-design-agent
6. If finalize: Orchestrator updates brief (Phase 5.6)
7. Orchestrator: Invoke ui-finalization-agent via Task tool
8. ui-finalization-agent: Generate 5 files, commit, return JSON
9. Orchestrator: Parse JSON, present completion menu

See `references/delegation-protocols.md` for enforcement details.

### State Management

Subagents update `.continue-here.md` with their phase results. Orchestrator verifies `stateUpdated` flag in JSON report.

**State Verification Protocol:**

After subagent returns `stateUpdated: true`, verify actual state contents match expected values (not just boolean flag).

Read `.continue-here.md`, parse YAML, check specific fields match JSON report values. If mismatch, present state recovery menu.

See `references/state-tracking.md` for complete state schema and verification protocol.

### Iteration Protocol

Each iteration runs in fresh agent context. User chooses "Iterate" → Orchestrator collects feedback → Invokes NEW ui-design-agent with incremented version. Fresh context prevents context window bloat during iterative design.

### Error Handling

**Agent failures:** Present error menu (retry/manual fix/debug/cancel).

**Validation failures:** Agent returns `validationPassed: false` → Present error menu.

**State update failures:** Agent returns `stateUpdated: false` → Present state recovery menu (verify/manual update/continue anyway).

---

## Versioning Strategy

**Pattern:** v1, v2, v3... Each version saved separately.

**Purpose:** Explore layouts without losing work, A/B test designs, keep history for rollback.

**File naming:** All 7 files prefixed with version (e.g., `v2-ui.html`, `v2-PluginEditor.h`).

**Implementation:** Latest version used for Stage 3 (GUI) unless user specifies different version.

See `references/versioning.md` for file management details.

---

## Success Criteria

**Design phase successful when:**
- YAML spec generated matching user requirements
- Browser test HTML works (interactive controls, parameter messages)
- Design files committed to git
- `.continue-here.md` updated with version (if workflow mode)
- User presented with Phase 5.5 decision menu
- Design approved OR user iterates with refinements

**Implementation phase successful when:**
- All 7 files generated and saved to `.ideas/mockups/`
- Production HTML complete (no placeholders)
- C++ boilerplate matches YAML structure (correct parameter bindings)
- parameter-spec.md generated and locked (v1 only)
- Implementation files committed to git
- `.continue-here.md` updated with finalization status (if workflow mode)

---

## Integration Points

**Invoked by:**
- `/dream` command → After creative brief, before implementation
- `plugin-workflow` skill → During Stage 0 (UI design phase)
- `plugin-improve` skill → When redesigning existing plugin UI
- Natural language: "Design UI for [PluginName]", "Create mockup for compressor"

**Always invokes (via Task tool):**
- `ui-design-agent` subagent (Phase 4-5.45) - REQUIRED for design iteration
- `ui-finalization-agent` subagent (Phase 6-10.5) - REQUIRED for implementation files

**Also invokes:**
- `ui-template-library` skill (if user saves aesthetic)

**Creates (via subagents):**
- `plugins/[Name]/.ideas/mockups/v[N]-*.{yaml,html,h,cpp,txt,md}` (7 files)
- `plugins/[Name]/.ideas/parameter-spec.md` (if v1 and doesn't exist)

**Updates (via subagents):**
- `PLUGINS.md` → Mark UI designed (if workflow)
- `.continue-here.md` → Update workflow state (if workflow)

**Blocks:**
- Stage 1 (Foundation) → Cannot proceed without parameter-spec.md
- Stage 3 (GUI) → Cannot implement without approved UI mockup

---

## Reference Documentation

Progressive disclosure - load references when reaching specific phases:

- **Phase 0:** `references/aesthetic-integration.md` - Aesthetic library integration
- **Phase 1:** `references/context-extraction.md` - Creative brief extraction
- **Phase 2-3:** `references/design-questions.md` - Question templates and tiering
- **Phase 2.5:** `references/layout-validation.md` - Dimension calculation formulas
- **Phase 4-5.45:** `references/delegation-protocols.md` - Subagent invocation
- **Phase 5.5:** `references/decision-menus.md` - Menu format and routing
- **Phase 5.6:** `references/state-tracking.md` - Brief sync protocol
- **Phase 6-10:** `references/phase-b-enforcement.md` - Phase B guard
- **Anti-patterns:** `references/common-pitfalls.md` - What to avoid

**Technical details:**
- `references/html-generation.md` - Production HTML rules
- `references/browser-testing.md` - Browser test workflow
- `references/cmake-configuration.md` - WebView build settings
- `references/cpp-boilerplate-generation.md` - C++ template generation
- `references/ui-design-rules.md` - Design constraints and patterns
- `references/versioning.md` - File management

## Template Assets

- `assets/ui-yaml-template.yaml` - YAML structure
- `assets/webview-boilerplate.md` - C++ integration templates
- `assets/integration-checklist-template.md` - Integration guide
- `assets/parameter-spec-template.md` - Parameter specification format
