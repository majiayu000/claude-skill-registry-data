---
name: panel-mockup
description: Generate production-ready SVG panel designs in two phases - design iteration (2 files) then implementation scaffolding (5 files after approval)
allowed-tools:
  - Read
  - Write
  - Bash
preconditions:
  - None (can work standalone or with creative brief)
---

# panel-mockup Skill

**Purpose:** Generate production-ready SVG panel designs in two phases. The SVG generated IS the module panel, not a throwaway prototype.

## Workflow Overview

**TWO-PHASE WORKFLOW:**

### Phase A: Design Iteration (Fast)
Generate 2 design files for rapid iteration:
1. **v[N]-panel.yaml** - Machine-readable design specification
2. **v[N]-panel.svg** - Inkscape-compatible panel with component placeholders

**STOP HERE** - Present decision menu for user to iterate or finalize.

### Phase B: Implementation Scaffolding (After Finalization)
Generate 5 implementation files only after user approves design:
3. **[Module].svg** - Production SVG (copy to res/)
4. **[Module]-generated.cpp** - Auto-generated C++ from helper.py
5. **parameter-spec.md** - Parameter specification
6. **v[N]-integration-checklist.md** - Implementation steps
7. **v[N]-component-mapping.json** - Component position registry

**Why two phases?** SVG panels are cheap to iterate. C++ boilerplate is pointless if design isn't locked. This saves time by avoiding premature scaffolding generation.

All files saved to: `modules/[ModuleName]/.ideas/panels/`

## Phase 0: Check for Aesthetic Library

**Before starting design, check if saved aesthetics exist.**

```bash
if [ -f .claude/aesthetics/manifest.json ]; then
    AESTHETIC_COUNT=$(jq '.aesthetics | length' .claude/aesthetics/manifest.json)
    if [ $AESTHETIC_COUNT -gt 0 ]; then
        echo "Found $AESTHETIC_COUNT saved aesthetics"
    fi
fi
```

**If aesthetics exist, present decision menu:**

```
Found $AESTHETIC_COUNT saved aesthetics in library.

How would you like to start the panel design?
1. Start from aesthetic template - Apply saved visual system
2. Start from scratch - Create custom design
3. List all aesthetics - Browse library before deciding

Choose (1-3): _
```

**Option handling:**

- **Option 1: Start from aesthetic template**
  - Read manifest: `.claude/aesthetics/manifest.json`
  - Display available aesthetics with metadata
  - If user selects aesthetic: Invoke aesthetic-template-library skill with "apply" operation
  - Skip to Phase 4 with generated panel from aesthetic

- **Option 2: Start from scratch**
  - Continue to Phase 1 (load context)

- **Option 3: List all aesthetics**
  - Invoke aesthetic-template-library skill with "list" operation
  - Show preview paths
  - Return to option menu

**If no aesthetics exist:**
- Skip Phase 0
- Continue directly to Phase 1

---

## Phase 1: Load Context from Creative Brief

**CRITICAL: Always read creative-brief.md before starting.**

```bash
test -f "modules/$MODULE_NAME/.ideas/creative-brief.md"
```

**Extract panel context from creative-brief.md:**

- **Panel Concept section:** Layout preferences, visual style mentions
- **Parameters:** Count and types (determines control layout)
- **Module type:** Oscillator/effect/utility/sequencer (affects typical layouts)
- **Vision section:** Any visual references or inspirations
- **HP width requirement:** Often specified in brief

**VCV-specific considerations:**

- HP width (common: 6HP, 10HP, 12HP, 20HP)
- Input/output count (determines jack placement)
- Knob vs slider preference
- LED/display requirements

## Phase 1.5: Context-Aware Initial Prompt

**Adapt the prompt based on what's in the creative brief:**

**If rich panel details exist:**
```
I see you want [extracted description from Panel Concept] for [ModuleName]. Let's refine that vision. Tell me more about the layout, control arrangement, and visual elements you're imagining.
```

**If minimal panel details:**
```
Let's design the panel for [ModuleName]. You mentioned it's a [type] with [X] parameters. What layout and style are you envisioning? What HP width?
```

**If zero panel context:**
```
Let's design the panel for [ModuleName]. What do you envision? (HP width, layout, style, controls, visual elements)
```

**Why context-aware:** Don't ask the user to repeat information they already provided in the creative brief. Build on what they said.

**Listen for:**

- HP width ("8HP compact module", "20HP feature-rich")
- Layout preferences ("knobs in 2 rows", "vertical slider strip")
- Visual references ("like Mutable Instruments", "retro Buchla style")
- Mood/feel ("minimal and clean", "colorful and playful")
- Special requests ("waveform display", "multi-color LEDs")

**Capture verbatim notes before moving to targeted questions.**

## Phase 2: Gap Analysis and Question Prioritization

**Question Priority Tiers:**

- **Tier 1 (Critical):** HP width, I/O count, control types
- **Tier 2 (Visual):** Visual style, key visual elements (displays, scopes, labels)
- **Tier 3 (Polish):** Colors, typography, animations, LED colors

**Extract from Phase 1.5 response and creative brief, then identify gaps:**

1. Parse user's panel description
2. Check which tiers are covered
3. Identify missing critical/visual information
4. Never ask about already-provided information

**Example of context-aware extraction:**

```
Creative brief Panel Concept:
"Minimal 6HP oscillator with classic waveforms"

Phase 1.5 user response:
"I want three knobs vertically arranged for FREQ, SHAPE, PW"

Extracted:
- HP width: 6HP ✓
- Control type: knobs ✓
- Layout: vertical arrangement ✓
- Parameters: FREQ, SHAPE, PW ✓

Gaps identified:
- Waveform output jacks? (Tier 1)
- CV input jacks? (Tier 1)
- Visual feedback (LEDs/displays)? (Tier 2)
- Label style (minimal vs detailed)? (Tier 3)
```

## Phase 3: Question Batch Generation

**Generate exactly 4 questions using AskUserQuestion based on identified gaps.**

**Rules:**
- If 4+ gaps exist: ask top 4 by tier priority
- If fewer gaps exist: pad with "nice to have" tier 3 questions
- Provide meaningful options (not just open text prompts)
- Always include "Other" option for custom input
- Users can skip questions via "Other" option and typing "skip"

**Example question batch (via AskUserQuestion):**

```
Question 1:
  question: "How many output jacks for waveforms?"
  header: "Outputs"
  options:
    - label: "1 output (mixed)", description: "Single output jack"
    - label: "4 outputs (separate waveforms)", description: "Sine, Triangle, Saw, Square"
    - label: "6 outputs (full set)", description: "All common waveforms"
    - label: "Other", description: "Different output configuration"

Question 2:
  question: "CV inputs needed?"
  header: "Inputs"
  options:
    - label: "V/Oct only", description: "Just pitch tracking"
    - label: "V/Oct + FM", description: "Pitch and frequency modulation"
    - label: "V/Oct + FM + PWM", description: "Full modulation control"
    - label: "Other", description: "Different input configuration"

Question 3:
  question: "Visual feedback elements?"
  header: "Displays"
  options:
    - label: "LED indicators", description: "Simple status lights"
    - label: "Mini scope display", description: "Waveform preview"
    - label: "Both LEDs and scope", description: "Full visual feedback"
    - label: "None (controls only)", description: "Clean, minimal"

Question 4:
  question: "Label style?"
  header: "Typography"
  options:
    - label: "Minimal (icons only)", description: "No text, just symbols"
    - label: "Compact text labels", description: "Small parameter names"
    - label: "Detailed labels", description: "Full parameter descriptions"
    - label: "Other", description: "Different label approach"
```

**After receiving answers:**
1. Accumulate context with previous responses
2. Re-analyze gaps
3. Proceed to decision gate

## Phase 3.5: Decision Gate

**Use AskUserQuestion with 3 options after each question batch:**

```
Question:
  question: "Ready to finalize the panel design?"
  header: "Next step"
  options:
    - label: "Yes, finalize it", description: "Generate YAML and SVG"
    - label: "Ask me 4 more questions", description: "Continue refining"
    - label: "Let me add more context first", description: "Provide additional details"

Route based on answer:
- Option 1 → Proceed to Phase 4 (generate YAML and SVG)
- Option 2 → Return to Phase 2 (re-analyze gaps, generate next 4 questions)
- Option 3 → Collect free-form text, merge with context, return to Phase 2
```

## Phase 4: Generate Hierarchical YAML

**Create:** `modules/[Name]/.ideas/panels/v[N]-panel.yaml`

**Purpose:** Machine-readable design spec that guides SVG generation and C++ implementation.

**VCV Rack Panel Constraints:**

- **Height:** 128.5mm (fixed, Eurorack standard)
- **Width:** HP × 5.08mm (e.g., 10HP = 50.8mm)
- **Component positions:** In millimeters from top-left origin
- **Grid alignment:** 5.08mm horizontal grid recommended

**Structure:**

```yaml
panel:
  hp_width: 10
  width_mm: 50.8
  height_mm: 128.5
  module_name: "SimpleOsc"
  background_color: "#1a1a1a"

colors:
  background: "#1a1a1a"
  panel_border: "#2b2b2b"
  label_text: "#ffffff"
  component_accent: "#ff8800"

layout:
  style: "vertical-sections"  # or: grid, centered, custom
  sections:
    - id: header
      y: 5
      height: 20
      content: [module-title]
    - id: controls
      y: 30
      height: 70
      content: [freq-knob, shape-knob, pw-knob]
    - id: io
      y: 105
      height: 20
      content: [voct-input, out-output]

components:
  - id: freq-knob
    type: knob
    label: "FREQ"
    parameter: "frequency"
    range: [0.0, 10.0]
    default: 5.0
    position: {x: 25.4, y: 35}  # millimeters from top-left
    size: 9.0  # diameter in mm (large knob)
    color: "#ff8800"

  - id: voct-input
    type: input-jack
    label: "V/OCT"
    position: {x: 12.7, y: 110}
    color: "#4a9eff"

  - id: out-output
    type: output-jack
    label: "OUT"
    position: {x: 38.1, y: 110}
    color: "#ff4444"

  - id: freq-led
    type: led
    label: ""
    position: {x: 25.4, y: 55}
    color: "#00ff00"
    size: 2.0  # diameter in mm
```

**Component Types:**

- `knob` - Rotary control (6mm, 9mm, or 12mm diameter typical)
- `slider` - Linear fader (vertical or horizontal)
- `input-jack` - 3.5mm mono jack (input)
- `output-jack` - 3.5mm mono jack (output)
- `led` - Status indicator (1-3mm typical)
- `button` - Momentary or toggle button
- `switch` - Multi-position switch
- `display` - Text or graphic display area
- `label` - Text label (not interactive)

**Position Guidelines:**

- **X-axis:** 0 = left edge, HP×5.08 = right edge
- **Y-axis:** 0 = top edge, 128.5 = bottom edge
- **Jack spacing:** Minimum 10mm between jack centers
- **Knob spacing:** Minimum 12mm between knob centers
- **Edge margins:** 5mm minimum from panel edges

## Phase 5: Generate Inkscape-Compatible SVG

**Create:** `modules/[Name]/.ideas/panels/v[N]-panel.svg`

**Purpose:** Test panel design in Inkscape for visual iteration.

**VCV Rack SVG Requirements:**

### Critical Constraints

**1. Coordinate System:**
- Origin (0,0) at **top-left corner**
- Width: HP × 5.08mm (e.g., 10HP = 50.8mm viewBox width)
- Height: 128.5mm (Eurorack standard)
- Units: millimeters

**2. ViewBox:**
```xml
<svg viewBox="0 0 50.8 128.5" width="50.8mm" height="128.5mm">
```

**3. Component Layer Structure:**

```xml
<svg viewBox="0 0 50.8 128.5" width="50.8mm" height="128.5mm">
  <!-- Background layer -->
  <rect id="background" width="50.8" height="128.5" fill="#1a1a1a"/>

  <!-- Component placeholders layer -->
  <g id="components">
    <!-- Knobs: circles with center position -->
    <circle id="freq-knob" cx="25.4" cy="35" r="4.5"
            fill="none" stroke="#ff8800" stroke-width="0.5"/>
    <text x="25.4" y="32" text-anchor="middle" fill="#ffffff"
          font-size="2.5">FREQ</text>

    <!-- Input jacks: blue circles -->
    <circle id="voct-input" cx="12.7" cy="110" r="4.0"
            fill="#4a9eff" stroke="#2b2b2b" stroke-width="0.3"/>
    <text x="12.7" y="105" text-anchor="middle" fill="#ffffff"
          font-size="2">V/OCT</text>

    <!-- Output jacks: red circles -->
    <circle id="out-output" cx="38.1" cy="110" r="4.0"
            fill="#ff4444" stroke="#2b2b2b" stroke-width="0.3"/>
    <text x="38.1" y="105" text-anchor="middle" fill="#ffffff"
          font-size="2">OUT</text>

    <!-- LEDs: small circles -->
    <circle id="freq-led" cx="25.4" cy="55" r="1.0"
            fill="#00ff00"/>
  </g>

  <!-- Labels layer -->
  <g id="labels">
    <text x="25.4" y="12" text-anchor="middle" fill="#ffffff"
          font-size="4" font-weight="bold">SimpleOsc</text>
  </g>
</svg>
```

**4. Component Color Codes (for placeholders):**

- **Knobs:** Orange stroke `#ff8800`, no fill
- **Input jacks:** Blue fill `#4a9eff`
- **Output jacks:** Red fill `#ff4444`
- **LEDs:** Green fill `#00ff00` (or specified color)
- **Buttons:** Gray fill `#808080`
- **Labels:** White text `#ffffff`

**5. Text Constraints:**

- **Module title:** 4-5mm font size, bold
- **Parameter labels:** 2-2.5mm font size
- **Font family:** Sans-serif (Arial, Helvetica, or VCV default)
- **Text anchor:** `middle` for centered labels

**6. Inkscape Compatibility:**

- Use standard SVG elements (no custom extensions)
- Avoid complex filters or gradients (keep simple for iteration)
- Layer names don't need special prefixes
- All measurements in millimeters

### SVG Generation Strategy

**Base template approach:**

1. Start with background rectangle (panel color)
2. Add component placeholders from YAML (colored shapes)
3. Add labels from YAML (positioned text)
4. Add module title
5. Keep structure simple (no complex groups for design iteration)

**Example minimal SVG:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 50.8 128.5" width="50.8mm" height="128.5mm"
     xmlns="http://www.w3.org/2000/svg">

  <!-- Background -->
  <rect width="50.8" height="128.5" fill="#1a1a1a"/>

  <!-- Module title -->
  <text x="25.4" y="12" text-anchor="middle" fill="#ffffff"
        font-size="4.5" font-family="sans-serif" font-weight="bold">
    SimpleOsc
  </text>

  <!-- Components (from YAML) -->
  <g id="components">
    <!-- Generate from YAML components list -->
  </g>
</svg>
```

## Phase 5.3: Validate VCV Constraints (Before Decision Menu)

**CRITICAL:** Validate generated SVG against VCV Rack constraints before presenting to user.

**Validation checklist:**

```bash
# Check viewBox matches HP width
grep -q 'viewBox="0 0 [0-9.]* 128.5"' v[N]-panel.svg

# Check height is 128.5mm
grep -q 'height="128.5mm"' v[N]-panel.svg

# Check width matches HP formula (HP × 5.08)
EXPECTED_WIDTH=$(python3 -c "print(${HP_WIDTH} * 5.08)")
grep -q "width=\"${EXPECTED_WIDTH}mm\"" v[N]-panel.svg

# Check all components have valid positions (within bounds)
# X: 0 to (HP × 5.08), Y: 0 to 128.5
```

**Component position validation:**

```python
import xml.etree.ElementTree as ET

tree = ET.parse('v[N]-panel.svg')
root = tree.getroot()

hp_width = 10  # from YAML
max_x = hp_width * 5.08
max_y = 128.5

for circle in root.findall('.//{http://www.w3.org/2000/svg}circle'):
    cx = float(circle.get('cx'))
    cy = float(circle.get('cy'))

    if cx < 0 or cx > max_x:
        print(f"ERROR: Component {circle.get('id')} X position {cx} out of bounds")
    if cy < 0 or cy > max_y:
        print(f"ERROR: Component {circle.get('id')} Y position {cy} out of bounds")
```

**If validation fails:**
- ❌ REJECT: Regenerate panel with corrections
- Do NOT present to user until constraints are satisfied

## Phase 5.4: Auto-Open in Inkscape

**After validation passes, automatically open the SVG in Inkscape.**

```bash
open -a Inkscape modules/[ModuleName]/.ideas/panels/v[N]-panel.svg
```

This allows immediate visual inspection without requiring user to manually navigate and open the file.

**Note:** Uses `open -a` command (macOS). On other platforms, adjust command accordingly (e.g., `inkscape` on Linux, `start inkscape` on Windows).

## Phase 5.45: Version Control Checkpoint

**CRITICAL: Commit each panel version immediately after generation.**

**After Phase 5.4 completes (YAML + SVG generated and validated):**

```bash
cd modules/[ModuleName]/.ideas/panels
git add v[N]-panel.yaml v[N]-panel.svg
git commit -m "feat([ModuleName]): panel design v[N] (design iteration)"
```

**Why commit at this point:**
- Preserves design history between iterations
- Each version is recoverable
- Enables A/B comparison of different designs
- Atomic commits per iteration (not batched)

**Update workflow state (if in workflow context):**

```bash
if [ -f "modules/[ModuleName]/.ideas/.continue-here.md" ]; then
    # Update version tracking
    sed -i '' "s/latest_panel_version: .*/latest_panel_version: [N]/" .continue-here.md
    # Keep panel_finalized: false until user chooses "finalize"
    git add .continue-here.md
    git commit --amend --no-edit
fi
```

**State tracking in `.continue-here.md`:**

```markdown
current_stage: 0
stage_0_status: panel_design_in_progress
latest_panel_version: 2
panel_finalized: false
```

**Only proceed to Phase 5.5 after successful commit.**

---

## ⚠️ CRITICAL STOP POINT - Phase 5.5: Design Decision Menu

**DO NOT PROCEED TO PHASE 6 WITHOUT USER CONFIRMATION**

After generating YAML + SVG, present this decision menu:

```
✓ Panel v[N] design created (2 files)

Files generated:
- v[N]-panel.yaml (design specification)
- v[N]-panel.svg (Inkscape-editable panel)

What do you think?
1. Check alignment - Run design-sync validation (recommended before finalizing)
2. Provide refinements (iterate on design) ← Creates v[N+1]
3. Finalize and create implementation files (if satisfied and aligned)
4. Save as aesthetic template (add to library for reuse)
5. Finalize AND save aesthetic (do both operations)
6. Open in Inkscape (view/edit SVG manually)
7. Validate VCV constraints (run checks)
8. Other

Choose (1-8): _
```

**WAIT for user response before continuing.**

**Option handling:**
- **Option 1**: Check alignment → Invoke design-sync skill to validate panel ↔ creative brief consistency
- **Option 2**: User gives feedback → Return to Phase 2 with new version number (v2, v3, etc.)
- **Option 3**: User approves → Proceed to Phase 6-10 (generate remaining 5 files + finalize state)
- **Option 4**: Save aesthetic → Invoke aesthetic-template-library skill with "save" operation
- **Option 5**: Save aesthetic first, then proceed to Phase 6-10
- **Option 6**: Open SVG in Inkscape for manual editing
- **Option 7**: Validate VCV constraints (run Phase 5.3 checks again)
- **Option 8**: Other

**Only execute Phases 6-10 if user chose option 3 or 5 (finalize).**

---

## Phase 6: Copy Finalized SVG to Production (After Finalization Only)

**Prerequisites:** User confirmed design in Phase 5.5 decision menu.

**Create:** `modules/[Name]/res/[Module].svg`

**This SVG IS the module panel.** It will be registered with plugin.json and compiled into the module.

### Production SVG Preparation

**Copy and clean up the finalized design SVG:**

1. **Copy finalized SVG:**
   ```bash
   cp modules/[Module]/.ideas/panels/v[N]-panel.svg modules/[Module]/res/[Module].svg
   ```

2. **Replace component placeholders with production artwork:**

   **Before (design iteration):**
   ```xml
   <circle id="freq-knob" cx="25.4" cy="35" r="4.5"
           fill="none" stroke="#ff8800" stroke-width="0.5"/>
   ```

   **After (production):**
   ```xml
   <!-- Knob background (subtle shadow) -->
   <circle cx="25.4" cy="35" r="6.0" fill="#0a0a0a"/>
   <!-- Knob main body -->
   <circle cx="25.4" cy="35" r="5.5" fill="#2b2b2b"/>
   <!-- Knob indicator line -->
   <line x1="25.4" y1="35" x2="25.4" y2="30"
         stroke="#ff8800" stroke-width="0.8" stroke-linecap="round"/>
   ```

3. **Polish visual elements:**
   - Add subtle shadows/highlights
   - Refine label positioning
   - Add panel border if desired
   - Clean up any design iteration artifacts

**Critical: Maintain exact component positions from YAML** - These positions will be referenced in C++ code for input/output/param registration.

## Phase 7: Run helper.py createmodule (After Finalization Only)

**Prerequisites:** User confirmed design in Phase 5.5 decision menu.

**Generate:** `modules/[Name]/src/[Module]-generated.cpp`

**VCV Rack's helper.py script auto-generates C++ boilerplate from SVG.**

### Execution Steps

1. **Ensure SVG is in res/ directory:**
   ```bash
   test -f modules/[Module]/res/[Module].svg
   ```

2. **Run helper.py createmodule:**
   ```bash
   cd modules/[Module]
   python3 ../../helper.py createmodule [Module] res/[Module].svg
   ```

3. **Verify generated file:**
   ```bash
   test -f src/[Module]-generated.cpp
   ```

### What helper.py Generates

**Output:** `src/[Module]-generated.cpp` with:

```cpp
#include "plugin.hpp"

struct [Module] : Module {
    enum ParamId {
        // Auto-generated from SVG component IDs
        FREQ_KNOB_PARAM,
        SHAPE_KNOB_PARAM,
        PW_KNOB_PARAM,
        PARAMS_LEN
    };
    enum InputId {
        VOCT_INPUT,
        FM_INPUT,
        INPUTS_LEN
    };
    enum OutputId {
        OUT_OUTPUT,
        OUTPUTS_LEN
    };
    enum LightId {
        FREQ_LED,
        LIGHTS_LEN
    };

    [Module]() {
        config(PARAMS_LEN, INPUTS_LEN, OUTPUTS_LEN, LIGHTS_LEN);

        // Auto-generated param configs from SVG positions
        configParam(FREQ_KNOB_PARAM, 0.f, 10.f, 5.f, "Frequency");
        configParam(SHAPE_KNOB_PARAM, 0.f, 1.f, 0.5f, "Shape");
        configParam(PW_KNOB_PARAM, 0.f, 1.f, 0.5f, "Pulse Width");

        configInput(VOCT_INPUT, "V/Oct");
        configInput(FM_INPUT, "FM");

        configOutput(OUT_OUTPUT, "Audio");
    }

    void process(const ProcessArgs& args) override {
        // TODO: Implement DSP
    }
};

struct [Module]Widget : ModuleWidget {
    [Module]Widget([Module]* module) {
        setModule(module);
        setPanel(createPanel(asset::plugin(pluginInstance, "res/[Module].svg")));

        addChild(createWidget<ScrewSilver>(Vec(RACK_GRID_WIDTH, 0)));
        addChild(createWidget<ScrewSilver>(Vec(box.size.x - 2 * RACK_GRID_WIDTH, 0)));
        addChild(createWidget<ScrewSilver>(Vec(RACK_GRID_WIDTH, RACK_GRID_HEIGHT - RACK_GRID_WIDTH)));
        addChild(createWidget<ScrewSilver>(Vec(box.size.x - 2 * RACK_GRID_WIDTH, RACK_GRID_HEIGHT - RACK_GRID_WIDTH)));

        // Auto-generated component registration from SVG
        addParam(createParamCentered<RoundBlackKnob>(mm2px(Vec(25.4, 35)), module, [Module]::FREQ_KNOB_PARAM));
        addParam(createParamCentered<RoundBlackKnob>(mm2px(Vec(25.4, 50)), module, [Module]::SHAPE_KNOB_PARAM));
        addParam(createParamCentered<RoundBlackKnob>(mm2px(Vec(25.4, 65)), module, [Module]::PW_KNOB_PARAM));

        addInput(createInputCentered<PJ301MPort>(mm2px(Vec(12.7, 110)), module, [Module]::VOCT_INPUT));
        addInput(createInputCentered<PJ301MPort>(mm2px(Vec(25.4, 110)), module, [Module]::FM_INPUT));

        addOutput(createOutputCentered<PJ301MPort>(mm2px(Vec(38.1, 110)), module, [Module]::OUT_OUTPUT));

        addChild(createLightCentered<MediumLight<GreenLight>>(mm2px(Vec(25.4, 55)), module, [Module]::FREQ_LED));
    }
};

Model* model[Module] = createModel<[Module], [Module]Widget>("[Module]");
```

**Key features:**
- Enum IDs for params/inputs/outputs/lights
- config() call with correct counts
- configParam/configInput/configOutput with names
- Widget with panel SVG registration
- Component registration using mm2px() with SVG positions

### Integration with plugin.cpp

**Update plugin.cpp to register model:**

```cpp
#include "plugin.hpp"

Plugin* pluginInstance;

void init(Plugin* p) {
    pluginInstance = p;
    p->addModel(model[Module]);
}
```

## Phase 8: Generate parameter-spec.md (After Finalization Only)

**Prerequisites:** User confirmed design in Phase 5.5 decision menu AND this is the first panel version.

**If this is the first panel (v1):**

**Create:** `modules/[Name]/.ideas/parameter-spec.md`

**Purpose:** Lock parameter specification for implementation. This becomes the **immutable contract** for all subsequent stages.

**Extract from YAML:**

```markdown
# Parameter Specification: [ModuleName]

## Module Metadata

**HP Width:** 10HP
**Total Parameters:** 5
**Total Inputs:** 2
**Total Outputs:** 1
**Total LEDs:** 1

## Parameter Definitions

### frequency (FREQ_KNOB_PARAM)
- **Type:** Float
- **Range:** 0.0 to 10.0
- **Default:** 5.0
- **Unit:** V
- **Panel Position:** 25.4mm, 35mm
- **Control Type:** Rotary knob (9mm)
- **DSP Usage:** Oscillator frequency control

### shape (SHAPE_KNOB_PARAM)
- **Type:** Float
- **Range:** 0.0 to 1.0
- **Default:** 0.5
- **Unit:** Normalized
- **Panel Position:** 25.4mm, 50mm
- **Control Type:** Rotary knob (9mm)
- **DSP Usage:** Waveform shape morphing

### pulsewidth (PW_KNOB_PARAM)
- **Type:** Float
- **Range:** 0.0 to 1.0
- **Default:** 0.5
- **Unit:** Normalized
- **Panel Position:** 25.4mm, 65mm
- **Control Type:** Rotary knob (9mm)
- **DSP Usage:** Pulse wave duty cycle

## Input Definitions

### voct (VOCT_INPUT)
- **Type:** CV Input (1V/octave)
- **Panel Position:** 12.7mm, 110mm
- **Jack Color:** Blue (#4a9eff)
- **Purpose:** Pitch tracking (exponential frequency control)

### fm (FM_INPUT)
- **Type:** CV Input (modulation)
- **Panel Position:** 25.4mm, 110mm
- **Jack Color:** Blue (#4a9eff)
- **Purpose:** Frequency modulation input

## Output Definitions

### out (OUT_OUTPUT)
- **Type:** Audio Output
- **Panel Position:** 38.1mm, 110mm
- **Jack Color:** Red (#ff4444)
- **Purpose:** Mixed waveform output

## LED Definitions

### freq_indicator (FREQ_LED)
- **Type:** Status LED
- **Panel Position:** 25.4mm, 55mm
- **Color:** Green (#00ff00)
- **Purpose:** Frequency range indicator
```

## Phase 9: Generate Integration Checklist (After Finalization Only)

**Prerequisites:** User confirmed design in Phase 5.5 decision menu.

**Create:** `modules/[Name]/.ideas/panels/v[N]-integration-checklist.md`

**Purpose:** Step-by-step guide to integrate panel into module during Stage 5.

### Checklist Structure

```markdown
## Stage 5 (GUI) Integration Steps - [ModuleName]

### 1. Verify Auto-Generated Files
- [ ] SVG copied to res/[Module].svg
- [ ] helper.py generated src/[Module]-generated.cpp
- [ ] Enums created: ParamId, InputId, OutputId, LightId
- [ ] Component registration uses correct mm2px positions

### 2. Register Module in plugin.cpp
- [ ] Add `#include "[Module]-generated.cpp"` to plugin.cpp
- [ ] Add `p->addModel(model[Module]);` to init()
- [ ] Verify module appears in VCV Rack browser

### 3. Implement DSP Logic
- [ ] Add DSP state variables to Module struct
- [ ] Implement process() method
- [ ] Handle parameter reading via params[PARAM_ID].getValue()
- [ ] Handle CV inputs via inputs[INPUT_ID].getVoltage()
- [ ] Set outputs via outputs[OUTPUT_ID].setVoltage()
- [ ] Update LEDs via lights[LIGHT_ID].setBrightness()

### 4. Build and Test (Debug)
- [ ] Build succeeds: `make`
- [ ] Module loads in VCV Rack
- [ ] Panel artwork displays correctly
- [ ] All knobs/inputs/outputs are interactive
- [ ] Component positions match panel SVG

### 5. Test Parameter Functionality
- [ ] Knobs respond to mouse input
- [ ] Parameter ranges are correct (check min/max)
- [ ] CV inputs modulate parameters correctly
- [ ] Audio outputs produce expected signals
- [ ] LEDs indicate status correctly

### 6. Test Module Integration
- [ ] Patch cables connect to inputs/outputs
- [ ] V/Oct tracking is accurate (test with keyboard)
- [ ] Audio quality is good (no clipping, noise)
- [ ] CPU usage is acceptable (check VCV meters)
- [ ] Module state saves/loads correctly

### 7. VCV Rack Specific Validation
- [ ] Panel SVG viewBox is correct (HP × 5.08mm width, 128.5mm height)
- [ ] Component positions match visual layout
- [ ] Screws appear in correct corners
- [ ] Module width matches HP specification
- [ ] No SVG rendering artifacts
- [ ] Text labels are readable
```

## Phase 10: Generate Component Mapping (After Finalization Only)

**Prerequisites:** User confirmed design in Phase 5.5 decision menu.

**Create:** `modules/[Name]/.ideas/panels/v[N]-component-mapping.json`

**Purpose:** Machine-readable registry of component positions for troubleshooting and documentation.

```json
{
  "module": "SimpleOsc",
  "hp_width": 10,
  "panel_width_mm": 50.8,
  "panel_height_mm": 128.5,
  "version": 1,
  "generated_from": "v1-panel.yaml",
  "components": [
    {
      "id": "freq-knob",
      "type": "knob",
      "enum_id": "FREQ_KNOB_PARAM",
      "label": "FREQ",
      "position_mm": {"x": 25.4, "y": 35},
      "size_mm": 9.0,
      "range": [0.0, 10.0],
      "default": 5.0
    },
    {
      "id": "voct-input",
      "type": "input",
      "enum_id": "VOCT_INPUT",
      "label": "V/OCT",
      "position_mm": {"x": 12.7, "y": 110},
      "jack_type": "PJ301MPort"
    },
    {
      "id": "out-output",
      "type": "output",
      "enum_id": "OUT_OUTPUT",
      "label": "OUT",
      "position_mm": {"x": 38.1, "y": 110},
      "jack_type": "PJ301MPort"
    },
    {
      "id": "freq-led",
      "type": "led",
      "enum_id": "FREQ_LED",
      "position_mm": {"x": 25.4, "y": 55},
      "color": "#00ff00",
      "size_mm": 2.0
    }
  ],
  "layout_grid": {
    "horizontal_spacing_mm": 12.7,
    "vertical_spacing_mm": 15.0,
    "edge_margin_mm": 5.0
  }
}
```

## Phase 10.5: Finalization Commit

**CRITICAL: Commit all implementation files and update workflow state.**

**After Phase 10 completes (all 5 files generated):**

```bash
cd modules/[ModuleName]
git add res/[Module].svg src/[Module]-generated.cpp .ideas/panels/v[N]-integration-checklist.md .ideas/panels/v[N]-component-mapping.json

# If parameter-spec.md was created (v1 only)
if [ -f ".ideas/parameter-spec.md" ]; then
    git add .ideas/parameter-spec.md
fi

git commit -m "feat([ModuleName]): panel v[N] finalized (implementation files generated via helper.py)"
```

**Update workflow state (if in workflow context):**

```bash
if [ -f "modules/[ModuleName]/.ideas/.continue-here.md" ]; then
    # Update finalization status
    sed -i '' "s/panel_finalized: .*/panel_finalized: true/" .continue-here.md
    sed -i '' "s/finalized_version: .*/finalized_version: [N]/" .continue-here.md
    sed -i '' "s/stage_0_status: .*/stage_0_status: panel_design_complete/" .continue-here.md

    git add .continue-here.md
    git commit --amend --no-edit
fi
```

**Updated state in `.continue-here.md`:**

```markdown
current_stage: 0
stage_0_status: panel_design_complete
latest_panel_version: 2
panel_finalized: true
finalized_version: 2
```

## After Completing All Phases

Once user has finalized a design and all 5 files are generated, present this menu:

```
✓ Panel v[N] complete (5 files generated)

What's next?
1. Start implementation (invoke module-workflow)
2. Create another panel version (explore alternative design)
3. Open in Inkscape (view production SVG)
4. Other

Choose (1-4): _
```

## Versioning Strategy

**v1, v2, v3...** Each panel version is saved separately.

**Why multiple versions:**

- Explore different layouts without losing previous work
- A/B test designs in Inkscape before committing
- Iterate based on user feedback
- Keep design history

**File naming:**

```
modules/[Name]/.ideas/panels/
├── v1-panel.yaml
├── v1-panel.svg
├── v1-integration-checklist.md
├── v1-component-mapping.json
├── v2-panel.yaml  (if user wants alternative design)
├── v2-panel.svg
└── ... (v2 variants)
```

**Latest version is used for implementation** (unless user specifies different version).

## Success Criteria

**Design phase successful when:**
- ✅ YAML spec generated matching user requirements
- ✅ SVG panel works in Inkscape (correct dimensions, positions)
- ✅ Design files committed to git (Phase 5.45)
- ✅ `.continue-here.md` updated with version number (if in workflow)
- ✅ User presented with Phase 5.5 decision menu
- ✅ Design approved OR user iterates with refinements

**Implementation phase successful when (after finalization):**
- ✅ All 5 files generated and saved
- ✅ Production SVG is in res/ directory
- ✅ helper.py generated valid C++ boilerplate
- ✅ parameter-spec.md generated and locked (for v1 only)
- ✅ Implementation files committed to git (Phase 10.5)
- ✅ `.continue-here.md` updated with finalization status (if in workflow)

## Integration Points

**Invoked by:**

- `/dream` command → After creative brief, before parameter finalization
- `module-workflow` skill → During Stage 0 (panel design phase)
- `module-improve` skill → When redesigning existing module panel
- Natural language: "Design panel for [ModuleName]", "Create SVG for oscillator"

**Invokes:**

- `design-sync` skill → Validate panel ↔ brief alignment
- `aesthetic-template-library` skill → Save/apply aesthetic templates

**Creates:**

- `modules/[Name]/.ideas/panels/v[N]-*.{yaml,svg,md,json}` (5 files)
- `modules/[Name]/res/[Module].svg` (production panel)
- `modules/[Name]/src/[Module]-generated.cpp` (via helper.py)
- `modules/[Name]/.ideas/parameter-spec.md` (if v1 and doesn't exist)

**Updates:**

- `MODULES.md` → Mark panel designed (if part of workflow)
- `.continue-here.md` → Update workflow state (if part of workflow)

**Blocks:**

- Stage 1 (Planning) → Cannot proceed without parameter-spec.md
- Stage 5 (GUI) → Cannot implement without approved panel design

## VCV Rack Specific Notes

**HP Width Standards:**
- 3HP - Minimal utility module
- 6HP - Simple oscillator/effect
- 10HP - Standard feature-rich module
- 12-16HP - Complex multi-function module
- 20HP+ - Large multi-section module

**Component Spacing:**
- Jack spacing: 10mm minimum (comfortable patching)
- Knob spacing: 12mm minimum (avoid overlap)
- Edge margins: 5mm minimum (panel border clearance)
- Grid alignment: 5.08mm horizontal grid recommended

**SVG to C++ Position Mapping:**
- SVG uses millimeters from top-left
- C++ uses mm2px() helper to convert to screen pixels
- helper.py extracts positions automatically from SVG component IDs

**Common Pitfalls:**
- Forgetting to run helper.py after SVG changes
- Component IDs in SVG not matching C++ enum names
- Positions outside panel bounds
- Incorrect HP width calculation (must be HP × 5.08mm exactly)
