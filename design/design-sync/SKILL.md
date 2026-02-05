---
name: design-sync
description: Validate panel ↔ creative brief consistency, catch design drift
allowed-tools:
  - Read # Read contracts (brief, parameter-spec, panel YAML)
  - Edit # Update brief's Evolution section
preconditions:
  - creative-brief.md exists
  - Panel has been finalized (parameter-spec.md generated)
extended-thinking: true
thinking-budget: 8000 # Moderate creative reasoning
---

# design-sync Skill

**Purpose:** Validate panel design ↔ creative brief consistency and catch design drift before implementation begins.

## Overview

This skill compares the finalized panel design against the original creative brief to detect drift—where the implemented design diverges from the original vision. Catches misalignments before Stage 5 (GUI implementation) starts, preventing wasted work.

**Why this matters:**

Creative briefs capture intent. Panel designs capture reality. During design iteration, these can diverge:

- Brief says 10HP → Panel is 20HP
- Brief says 8 parameters → Panel has 15
- Brief says "minimal utility" → Panel is "feature-rich multi-function"
- Brief mentions scope display → Panel lacks it

Detecting drift early allows course correction before implementation locks in the design.

**Key innovation:** Dual validation (quantitative + semantic) with categorized drift levels and appropriate decision menus.

---

## Entry Points

**Invoked by:**

1. **Auto-invoked by panel-mockup** after Phase 5.5 (before C++ generation)
2. **Manual:** `/sync-design [ModuleName]`
3. **Stage 1 Planning:** Optional pre-check before implementation starts

**Entry parameters:**

- **Module name**: Which module to validate
- **Panel version** (optional): Specific version to check (defaults to latest)

---

## Workflow

### Step 1: Load Contracts

Read three files:

- `modules/[ModuleName]/.ideas/creative-brief.md` - Original vision
- `modules/[ModuleName]/.ideas/parameter-spec.md` - Finalized parameters from panel
- `modules/[ModuleName]/.ideas/panels/vN-panel.yaml` - Finalized panel spec

**Error handling:** If any missing, BLOCK with clear message:

```
❌ Cannot validate design sync

Missing required files:
- creative-brief.md: [EXISTS/MISSING]
- parameter-spec.md: [EXISTS/MISSING]
- panels/v[N]-panel.yaml: [EXISTS/MISSING]

design-sync requires finalized panel (parameter-spec.md generated).

Actions:
1. Generate parameter-spec.md - Finalize panel first
2. Create creative brief - Document vision before panel
3. Skip validation - Proceed without sync (not recommended)
4. Other
```

### Step 2: Quantitative Checks

**Extract data from contracts:**

```typescript
// From creative-brief.md
briefParamCount = extractParameterCount(brief); // Count mentioned parameters
briefHPWidth = extractHPWidth(brief); // Extract HP width if mentioned
briefFeatures = extractFeatures(brief); // Grep for keywords

// From parameter-spec.md
mockupParamCount = countParameters(parameterSpec);
mockupInputCount = countInputs(parameterSpec);
mockupOutputCount = countOutputs(parameterSpec);

// From panel YAML
panelHPWidth = yaml.panel.hp_width;
panelControls = countControls(panelYAML); // All UI elements

// Compare
paramCountDelta = mockupParamCount - briefParamCount;
hpWidthDelta = panelHPWidth - briefHPWidth;
missingFeatures = briefFeatures.filter((f) => !presentInPanel(f));
```

**Parameter count thresholds:**

- Match (0-1 difference): No drift
- Small increase (2-3): Acceptable evolution
- Large increase (4+): Drift requiring attention
- Any decrease: Drift requiring attention (scope reduction)

**HP width thresholds:**

- Match: No drift
- ±3HP: Acceptable adjustment
- 6HP+ difference: Drift requiring attention
- 2x or more: Critical drift (different form factor)

**Feature detection:**

Keywords to search in brief:

- "scope", "display", "screen"
- "CV input", "modulation input"
- "polyphonic", "poly"
- "preset", "presets"
- "sync", "clock"
- "LED", "indicator"

Check if panel YAML contains corresponding components.

### Step 3: Semantic Validation (Extended Thinking)

**Use extended thinking to answer:**

1. **Visual style alignment:**

   - Brief aesthetic: [extract quotes from "Panel Concept" section]
   - Panel aesthetic: [analyze YAML design system: colors, layout style, component arrangement]
   - Match? Yes/No + reasoning

2. **Feature completeness:**

   - Brief promises: [list all mentioned features]
   - Panel delivers: [list all implemented features]
   - Missing: [list gaps]
   - Assessment: Complete / Partial / Missing core features

3. **HP width appropriateness:**

   - Brief scope: [utility/simple/complex]
   - Panel HP: [actual width]
   - Match? Yes/No + reasoning

4. **Scope assessment:**
   - Additions justified? (evolution vs creep)
   - Reductions justified? (simplification vs missing)
   - Core concept preserved?

**Extended thinking prompt:**

```
Compare creative brief with panel design to assess alignment:

Creative Brief:
- Concept: [extract]
- Use Cases: [extract]
- Panel Concept: [extract]
- Parameters: [list]
- HP Width: [extract if mentioned]

Panel Design:
- HP Width: [from YAML]
- Layout: [from YAML]
- Components: [from YAML]
- Visual style: [colors, arrangement from YAML]
- Parameters: [from parameter-spec.md]

Answer:
1. Does panel HP width match brief's implied scope? (utility=6HP, standard=10HP, complex=20HP)
2. Does panel visual style match brief aesthetic intent? (minimal vs detailed, colorful vs subdued)
3. Are all brief-mentioned features present?
4. Are panel additions reasonable evolution or scope creep?
5. Does panel support the use cases in brief?

Assess confidence: HIGH / MEDIUM / LOW
```

### Step 4: Categorize Drift

Based on findings:

**No drift detected:**

- HP width matches or within ±3HP
- Parameter counts match (±1)
- All features present
- Style aligned (semantic validation: YES)
- Panel delivers on brief promise

**Acceptable evolution:**

- HP width adjusted ±3HP with justification
- Parameter count increased slightly (2-3)
- Layout refined for ergonomics
- Additions improve design (justified)
- Core concept intact

**Attention needed:**

- HP width differs significantly (6HP+)
- Missing features from brief
- Style mismatch (different direction)
- Significant scope change (±4 parameters)
- Brief and panel tell different stories

**Critical drift:**

- HP width 2x or more different (form factor change)
- Panel contradicts brief's core concept
- Missing essential features
- Massive scope change (2x parameters or more)
- Completely opposite visual style

### Step 5: Present Findings

#### If No Drift:

```
✓ Design-brief alignment verified

- HP width: 10HP (matches brief)
- Parameter count: 8 (matches brief)
- All features present: scope display, CV inputs, poly support
- Visual style aligned: Minimal, clean layout

What's next?
1. Continue implementation (recommended) - Alignment confirmed
2. Review details - See full comparison
3. Other
```

#### If Acceptable Evolution:

```
⚠️ Design evolution detected (acceptable)

**Changes from brief:**
- HP width: 12HP (brief: 10HP) +2HP
- Parameter count: 10 (brief: 8) +2 parameters
  - Added: SHAPE_MOD, SYNC_MODE
- Added features: Waveform LED indicators (not in brief)
- Visual refinements: Color-coded jacks, refined label placement

**Assessment:** Reasonable evolution based on design iteration

**Reasoning:**
Added parameters (SHAPE_MOD, SYNC_MODE) provide necessary modulation control not
anticipated in original brief. LED indicators improve visual feedback during performance.
+2HP accommodates additions while maintaining compact form factor. Core concept
("minimal oscillator") preserved.

What's next?
1. Update brief and continue (recommended) - Document evolution
2. Review changes - See detailed comparison
3. Revert to original - Simplify panel to match brief
4. Other
```

#### If Drift Requiring Attention:

```
⚠️ Design drift detected

**Issues found:**
1. Missing feature: "Scope display" mentioned in brief, absent in panel
   - Brief line 38: "Include mini oscilloscope for waveform preview"
   - Panel: No display component defined
2. HP width mismatch:
   - Brief: "6HP compact oscillator"
   - Panel: 12HP (2x larger than specified)
3. Visual style mismatch:
   - Brief: "Minimal, monochrome design"
   - Panel: Colorful multi-color theme with detailed graphics
4. Parameter count: 15 (brief: 8) - significant expansion (+7)
   - Added 7 unmentioned parameters

**Recommendation:** Address drift before implementation

**Confidence:** HIGH (clear quantitative + semantic misalignment)

What's next?
1. Update panel - Add scope, reduce HP width, simplify style to match brief
2. Update brief - Brief was too minimal, panel reflects realistic scope
3. Continue anyway (override) - Accept drift, proceed with panel as-is
4. Review detailed comparison - See side-by-side analysis
5. Other
```

#### If Critical Drift:

```
❌ Critical design drift - Implementation BLOCKED

**Critical issues:**
1. Brief core concept: "6HP minimal single-oscillator utility"
   Panel delivers: 20HP complex multi-oscillator with effects section
2. HP width: 20HP (brief: 6HP) - 3.3x larger (form factor change)
3. Parameter count: 35 (brief: 6) - 5.8x scope creep
   - Brief: FREQ, SHAPE, PW, LEVEL, TUNE, OCT
   - Panel: 29 additional parameters for features not mentioned in brief
4. Module type mismatch:
   - Brief: Simple oscillator
   - Panel: Multi-function synthesis workstation

**Action required:** Resolve drift before implementation can proceed

**Why blocking:**
Panel fundamentally contradicts brief's core concept of simplicity. Implementation
would deliver a completely different module than envisioned. High risk of complete rework.

What's next?
1. Update panel - Return to 6HP minimal design matching brief
2. Update brief - Revise vision to match complex multi-function design
3. Start over - Create new panel aligned with brief
4. Other

(Option to override not provided - critical drift must be resolved)
```

### Step 6: Execute User Choice

**Option 1: Update brief and continue**

Add "Design Evolution" section to creative-brief.md:

```markdown
## Design Evolution

### [Date] - Panel v[N] Finalization

**Changes from original vision:**

**HP Width:**

- Original: 10HP
- Finalized: 12HP (+2HP)
- Rationale: Additional space needed for SHAPE_MOD and SYNC_MODE parameters

**Parameters:**

- Added: SHAPE_MOD, SYNC_MODE (brief: 8 parameters, panel: 10)

**Features:**

- Added: Waveform LED indicators for visual feedback

**Visual Style:**

- Refined: Color-coded jacks (blue=input, red=output, green=poly)
- Refined: Improved label hierarchy for readability

**Rationale:**

- Additional parameters (SHAPE_MOD, SYNC_MODE) provide necessary modulation control
  not anticipated in original brief.
- LED indicators improve usability during live performance by showing waveform state.
- Color-coded jacks reduce patching errors in complex patches.
- +2HP accommodates additions while maintaining reasonable form factor.

**User approval:** [Date] - Confirmed these changes align with module vision
```

Update brief's "Panel Concept" section to reflect current panel (preserve original in "Evolution" section).

**Option 2: Update panel**

- Return user to panel-mockup skill
- Present drift findings
- Iterate design to align with brief
- Re-run design-sync after changes

**Option 3: Continue anyway (override)**

- Log override to `.validator-overrides.yaml`:
  ```yaml
  - date: 2025-11-12
    validator: design-sync
    finding: hp-width-mismatch
    severity: attention
    override-reason: User confirmed evolution is intentional
    panel-version: v3
  ```
- Return success (allow implementation)
- Warn: "Implementation may not match original vision"

### Step 7: Route Back to panel-mockup

**After Step 6 actions complete (brief updated, panel changed, or override logged), return to panel-mockup Phase 5.5 decision menu.**

**Present this menu:**

```
✓ Design-brief alignment complete

What's next?
1. Finalize and create implementation files (if satisfied and aligned)
2. Provide more refinements (iterate on design) ← Creates v[N+1]
3. Open in Inkscape (view/edit SVG manually)
4. Save as aesthetic template (add to library for reuse)
5. Finalize AND save aesthetic (do both operations)
6. Other

Choose (1-6): _
```

**This is the same decision point as panel-mockup Phase 5.5, minus the "Check alignment" option (already done).**

**Option handling:**
- **Option 1**: Proceed to panel-mockup Phase 6-10 (generate remaining files via helper.py)
- **Option 2**: Return to panel-mockup Phase 2 with new version number (iterate design)
- **Option 3**: Open SVG in Inkscape for manual editing
- **Option 4**: Invoke aesthetic-template-library "save" operation
- **Option 5**: Save aesthetic, then proceed to Phase 6-10
- **Option 6**: Other

**Why route back:**
- Validates the design is aligned before generating implementation files
- Prevents generating C++ boilerplate for misaligned panels
- Maintains checkpoint protocol (user decides next action after validation)

---

## Integration with panel-mockup

**panel-mockup Phase 5.5** (after design, before finalization):

```markdown
✓ Panel v3 design created (2 files)

What do you think?

1. Check alignment - Run design-sync validation (recommended)
2. Provide refinements (iterate on design)
3. Finalize and create implementation files
4. Other
```

If user chooses "Check alignment" → invoke design-sync skill

**Flow:**

1. panel-mockup finishes Phase 5 (generates YAML + SVG + commits)
2. Presents decision menu with "Check alignment" option
3. If chosen: Invokes design-sync skill
4. design-sync validates, presents findings
5. User resolves any drift
6. Returns to panel-mockup to continue Phase 6 (or iterate)

---

## Integration with module-workflow Stage 1

**Optional pre-check before planning:**

Stage 1 Planning detects finalized panel:

```markdown
Starting Stage 1: Planning

Contracts loaded:

- creative-brief.md: EXISTS
- parameter-spec.md: EXISTS (from panel v3)

Panel finalized: Yes (v3)
design-sync validation: Not yet run

Recommendation: Validate brief ↔ panel alignment before planning

What's next?

1. Run design-sync - Validate alignment (recommended)
2. Skip validation - Proceed with planning (trust panel)
3. Other
```

If user chooses "Run design-sync" → invoke this skill

**Why pre-check matters:**

Stage 1 generates plan.md based on parameter-spec.md. If parameter-spec doesn't match brief vision, plan will be misaligned. Better to catch drift before planning.

---

## Success Criteria

Validation is successful when:

- ✅ All contracts loaded (brief + parameter-spec + panel YAML)
- ✅ Quantitative checks completed (HP width, parameter count, feature detection)
- ✅ Semantic validation performed (extended thinking analysis)
- ✅ Drift category assigned (none / acceptable / attention / critical)
- ✅ Appropriate decision menu presented
- ✅ User action executed (update brief / update panel / override)

---

## Error Handling

**Missing contracts:**

```
❌ Cannot validate: creative-brief.md not found

design-sync requires creative brief to validate against panel.

Actions:
1. Create brief - Document vision before validation
2. Skip validation - Proceed without sync (not recommended)
3. Other
```

**No panel finalized:**

```
❌ Cannot validate: No finalized panel found

design-sync requires:
- panels/v[N]-panel.yaml (finalized panel spec)
- parameter-spec.md (generated from panel)

Current state:
- Panels: v1-panel.yaml, v2-panel.yaml (no parameter-spec.md)

Actions:
1. Finalize panel - Generate parameter-spec.md via panel-mockup
2. Skip validation - Proceed without sync (not recommended)
3. Other
```

**Ambiguous findings:**

```
⚠️ Drift assessment uncertain

Quantitative checks:
- HP width: 12HP (brief: 10HP) +2HP ← Minor difference
- Parameter count: 10 (brief: 8) +2 parameters ← Minor difference
- Features: All present

Semantic validation:
- Visual style: MEDIUM confidence alignment
  - Brief aesthetic: "Minimal design"
  - Panel aesthetic: "Clean layout with some color accents"
  - Ambiguous: Are color accents "minimal"?

**Asking for user input:**
Is this panel style aligned with your "minimal design" vision?

1. Yes - Style matches intent (acceptable evolution)
2. No - Style misses the mark (drift requiring attention)
3. Review side-by-side - See comparison
4. Other
```

**Override tracking:**

All overrides logged to `.validator-overrides.yaml`:

```yaml
overrides:
  - timestamp: 2025-11-12T14:32:00Z
    validator: design-sync
    module: SimpleOsc
    panel-version: v3
    finding: hp-width-increase
    severity: attention
    details: "Brief: 10HP, Panel: 12HP (+2HP)"
    override-reason: "User confirmed: +2HP needed for additional modulation controls"
    approved-by: User
```

Enables audit trail: "Why did we proceed with drift?"

---

## Notes for Claude

**When executing this skill:**

1. Always load all three contracts first (brief, parameter-spec, panel YAML)
2. Run quantitative checks before semantic validation (faster)
3. Use extended thinking for semantic validation (8k budget)
4. Categorize drift objectively (use thresholds from workflow)
5. Present appropriate decision menu (based on drift category)
6. Update brief's Evolution section if user approves evolution
7. Log overrides to .validator-overrides.yaml
8. Never auto-override (user must explicitly choose)

**Common pitfalls:**

- Forgetting to use extended thinking for semantic validation (critical for accuracy)
- Auto-categorizing as "acceptable" without checking (be objective)
- Not presenting "Continue anyway" for non-critical drift (user should have option)
- Providing "override" for critical drift (should be blocked)
- Updating panel instead of brief (panel is source of truth, brief gets updated)
- Not logging overrides (audit trail required)

---

## Quality Guidelines

**Good drift detection:**

- ✅ Specific findings ("Missing feature: scope display from brief line 38")
- ✅ Quantitative evidence (HP width, parameter counts, feature lists)
- ✅ Semantic reasoning (why style does/doesn't match aesthetic)
- ✅ Confidence levels stated (HIGH/MEDIUM/LOW)
- ✅ Actionable recommendations

**Avoid:**

- ❌ Vague assessments ("Panel looks different")
- ❌ Missing quantitative data (no HP width comparison)
- ❌ No semantic analysis (just counting, no reasoning)
- ❌ Unclear confidence (is this certain or uncertain?)
- ❌ No clear recommendations (what should user do?)

---

## VCV Rack Specific Validation

**HP Width Validation:**

- 3HP: Minimal utility (1-2 parameters)
- 6HP: Simple module (3-6 parameters)
- 10HP: Standard module (6-10 parameters)
- 12-16HP: Feature-rich module (10-20 parameters)
- 20HP+: Complex multi-function (20+ parameters)

**Component Density Validation:**

- Check if HP width supports component count
- Calculate components per HP ratio
- Flag if panel is cramped (>3 components/HP)
- Flag if panel is sparse (<0.5 components/HP)

**VCV Design Patterns:**

- Input jacks typically on left/bottom
- Output jacks typically on right/bottom
- Knobs typically in center/upper area
- LEDs near associated controls
- Labels above or below components

**Panel Constraint Validation:**

- Height must be 128.5mm
- Width must be HP × 5.08mm exactly
- Component positions within bounds
- Minimum spacing between components (10mm jacks, 12mm knobs)
