---
name: module-planning
description: Interactive research and planning (Stages 0-1) for VCV Rack module development
allowed-tools:
  - Read # For contracts and references
  - Write # For architecture.md, plan.md
  - Edit # For state updates (MODULES.md, .continue-here.md)
  - Bash # For git commits, precondition checks
  - WebSearch # For professional module research
  - Grep # For searching existing implementations
  - Glob # For finding reference files
preconditions:
  - creative-brief.md must exist in modules/[Name]/.ideas/
  - Module must NOT already be past Stage 1
---

# module-planning Skill

**Purpose:** Handle Stages 0-1 (Research and Planning) through interactive contract creation without subagents. This skill creates the foundation contracts (architecture.md, plan.md) that guide implementation.

**Invoked by:** `/plan` command (to be created) or as first step of `/implement` workflow

---

## Entry Point

**Check preconditions first:**

1. Verify creative brief exists:
```bash
if [ ! -f "modules/${MODULE_NAME}/.ideas/creative-brief.md" ]; then
    echo "✗ creative-brief.md not found"
    exit 1
fi
```

2. Check module status in MODULES.md:
```bash
STATUS=$(grep -A 2 "^### ${MODULE_NAME}$" MODULES.md | grep "Status:" | awk '{print $2}')
```

- If status is 🚧 Stage N where N >= 2: **BLOCK** - Module already past planning
- If status is 💡 Ideated or not found: OK to proceed

3. Check for existing contracts:
```bash
# Check what already exists
test -f "modules/${MODULE_NAME}/.ideas/architecture.md" && echo "✓ architecture.md exists"
test -f "modules/${MODULE_NAME}/.ideas/plan.md" && echo "✓ plan.md exists"
```

**Resume logic:**
- If architecture.md exists but plan.md doesn't: Skip to Stage 1
- If both exist: Ask user if they want to regenerate or proceed to implementation
- If neither exists: Start at Stage 0

---

## Stage 0: Research

**Goal:** Create DSP architecture specification (architecture.md)

**Duration:** 5-10 minutes

**Process:**

1. Read creative brief:
```bash
cat modules/${MODULE_NAME}/.ideas/creative-brief.md
```

2. Identify module technical approach:
   - Module category (Oscillator, Filter, VCA, Effect, Utility, Sequencer, etc.)
   - Input/output configuration (audio, CV, gates, polyphonic channels)
   - Processing type (per-sample, block-based, time-domain, frequency-domain)

3. Research VCV Rack DSP patterns:
   - Search for relevant VCV Rack API classes (Module, Port, Param, Light)
   - Use WebSearch for VCV Rack documentation and examples
   - Document specific classes (e.g., rack::dsp::SchmittTrigger, rack::simd::float_4)
   - Research SIMD optimization patterns for polyphony

4. Research professional module examples:
   - Search web for industry modules (Mutable Instruments, Befaco, Instruo, etc.)
   - Document 3-5 similar modules from VCV Rack library or hardware Eurorack
   - Note sonic characteristics and typical parameter/CV ranges
   - Study polyphony implementation patterns

5. Research voltage ranges and standards:
   - Audio: typically ±5V (±10V peak)
   - CV: ±5V or ±10V (standard modulation)
   - Pitch: 1V/octave (C4 = 0V)
   - Gates: 0V (low) to 10V (high)
   - Triggers: brief high pulses (>1ms)

6. Check design sync (if mockup exists):
   - Look for `modules/${MODULE_NAME}/.ideas/mockups/v*-panel.yaml`
   - If exists: Compare mockup parameters with creative brief
   - If conflicts found: Invoke design-sync skill to resolve
   - Document sync results

**Output:**

Create `modules/${MODULE_NAME}/.ideas/architecture.md` using the template from `assets/architecture-template.md`.

**Required sections:**
1. Title: `# DSP Architecture: [ModuleName]`
2. Contract header (immutability statement)
3. `## Core Components` - Each DSP component with structured format
4. `## Processing Chain` - ASCII diagram showing signal flow
5. `## I/O Mapping` - Table mapping ports to DSP components
6. `## Parameter Mapping` - Table mapping parameters to DSP components
7. `## Algorithm Details` - Implementation approach for each algorithm
8. `## Polyphony Strategy` - How module handles polyphonic cables (if applicable)
9. `## Special Considerations` - Performance, denormals, sample rate, CPU budget
10. `## Research References` - Professional modules, VCV docs, technical resources

**VCV-specific sections:**

**Polyphony Strategy example:**
```markdown
## Polyphony Strategy

**Channel Handling:** Up to 16 polyphonic channels
**Processing:** Per-channel independent processing using SIMD (process 4 channels at a time)
**Port Configuration:**
- Input ports: Polyphonic (up to 16 channels)
- Output ports: Match input channel count
- CV ports: Monophonic CV applied to all channels

**Implementation:**
```cpp
// Process in SIMD blocks of 4 channels
int channels = std::max(1, inputs[AUDIO_INPUT].getChannels());
outputs[AUDIO_OUTPUT].setChannels(channels);

for (int c = 0; c < channels; c += 4) {
    // Process 4 channels at once using rack::simd::float_4
}
```
```

**State management:**

1. Create/update `.continue-here.md`:
```yaml
---
module: [ModuleName]
stage: 0
status: complete
last_updated: [YYYY-MM-DD HH:MM:SS]
---

# Resume Point

## Current State: Stage 0 - Research Complete

DSP architecture documented. Ready to proceed to planning.

## Completed So Far

**Stage 0:** ✓ Complete
- Module category defined
- Professional examples researched
- DSP feasibility verified
- Voltage ranges researched
- Polyphony strategy defined

## Next Steps

1. Stage 1: Planning (calculate complexity, create implementation plan)
2. Review research findings
3. Pause here

## Files Created
- modules/[ModuleName]/.ideas/architecture.md
```

2. Update MODULES.md status to `🚧 Stage 0` and add timeline entry

3. Git commit:
```bash
git add modules/${MODULE_NAME}/.ideas/architecture.md modules/${MODULE_NAME}/.continue-here.md MODULES.md
git commit -m "$(cat <<'EOF'
feat: [ModuleName] Stage 0 - research complete

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Decision menu (numbered format):**

```
✓ Stage 0 complete: DSP architecture documented

What's next?
1. Continue to Stage 1 - Planning (recommended)
2. Review architecture.md findings
3. Improve creative brief based on research
4. Run deeper VCV Rack investigation (deep-research skill) ← Discover troubleshooting
5. Pause here
6. Other

Choose (1-6): _
```

Wait for user input. Handle:
- Number (1-6): Execute corresponding option
- "continue" keyword: Execute option 1
- "pause" keyword: Execute option 5
- "review" keyword: Execute option 2
- "other": Ask "What would you like to do?" then re-present menu

---

## Stage 1: Planning

**Goal:** Calculate complexity and create implementation plan (plan.md)

**Duration:** 2-5 minutes

**Preconditions:**

Check for required contracts:
```bash
test -f "modules/${MODULE_NAME}/.ideas/parameter-spec.md" && echo "✓ parameter-spec.md" || echo "✗ parameter-spec.md MISSING"
test -f "modules/${MODULE_NAME}/.ideas/architecture.md" && echo "✓ architecture.md" || echo "✗ architecture.md MISSING"
```

**If parameter-spec.md OR architecture.md is missing:**

STOP IMMEDIATELY and BLOCK with this message:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✗ BLOCKED: Cannot proceed to Stage 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Missing implementation contracts:

Required contracts:
✓ creative-brief.md - exists
[✓/✗] parameter-spec.md - [exists/MISSING (required)]
[✓/✗] architecture.md - [exists/MISSING (required)]

WHY BLOCKED:
Stage 1 planning requires complete specifications to prevent implementation
drift. These contracts are the single source of truth.

HOW TO UNBLOCK:
1. parameter-spec.md: Complete panel mockup workflow
   - Run: /dream [ModuleName]
   - Choose: "Create panel mockup"
   - Design panel and finalize (Phase 4.5)
   - Finalization generates parameter-spec.md

2. architecture.md: Create DSP architecture specification
   - Run Stage 0 (Research) to generate architecture.md
   - Document DSP components and processing chain
   - Map I/O and parameters to DSP components
   - Save to modules/[ModuleName]/.ideas/architecture.md

Once both contracts exist, Stage 1 will proceed.
```

Exit skill and wait for user to create contracts.

**Process (contracts confirmed present):**

1. Read all contracts:
```bash
cat modules/${MODULE_NAME}/.ideas/parameter-spec.md
cat modules/${MODULE_NAME}/.ideas/architecture.md
```

2. Calculate complexity score:

**Formula:**
```
score = min(param_count / 5, 2.0) + min(io_count / 8, 2.0) + algorithm_count + feature_count
Cap at 5.0
```

**Extract metrics:**

From parameter-spec.md:
- Count parameters (each parameter definition = 1)
- param_score = min(param_count / 5, 2.0)

From architecture.md (I/O configuration):
- Count total input + output ports
- io_score = min(io_count / 8, 2.0)

From architecture.md (DSP components):
- Count distinct DSP algorithms/components
- algorithm_count = number of VCV Rack DSP classes or custom algorithms

Features to identify (from architecture.md):
- Polyphonic processing (up to 16 channels)? (+1)
- FFT/frequency domain processing? (+1)
- Complex modulation systems (LFOs, envelopes)? (+1)
- Expander module support? (+1)
- External communication (MIDI, OSC)? (+1)
- feature_count = sum of above

**Display breakdown:**
```
Complexity Calculation:
- Parameters: [N] parameters ([N/5] points, capped at 2.0) = [X.X]
- I/O Ports: [N] ports ([N/8] points, capped at 2.0) = [X.X]
- Algorithms: [N] DSP components = [N]
- Features: [List features] = [N]
Total: [X.X] / 5.0
```

3. Determine implementation strategy:
   - **Simple (score ≤ 2.0):** Single-pass implementation
   - **Complex (score ≥ 3.0):** Phase-based implementation with staged commits

4. For complex modules, create phases:

**Stage 4 (DSP) phases:**
- Phase 4.1: Core processing (essential audio/CV path)
- Phase 4.2: Parameter modulation (Param integration)
- Phase 4.3: Advanced features (polyphony, special processing)

**Stage 5 (GUI) phases:**
- Phase 5.1: Panel layout and basic widgets
- Phase 5.2: Advanced panel elements
- Phase 5.3: Polish and visual feedback (lights, animations)

Each phase needs description, test criteria, estimated duration.

**VCV-specific considerations:**

**CPU Budget Assessment:**
- Simple modules: <1% CPU (utilities, mixers, VCAs)
- Moderate modules: 1-3% CPU (oscillators, simple filters)
- Complex modules: 3-10% CPU (effects, complex filters)
- Heavy modules: >10% CPU (FFT processing, physical modeling)

Document expected CPU budget in plan.md based on algorithm complexity.

**Polyphony Performance:**
- Monophonic: Single channel processing
- Polyphonic (up to 16): 16x CPU usage (optimized with SIMD: 4x effective)
- Document polyphony impact on CPU budget

**Output:**

Create `modules/${MODULE_NAME}/.ideas/plan.md` using the template from `assets/plan-template.md`.

**Required sections:**
1. Title: `# Implementation Plan: [ModuleName]`
2. Contract header
3. `## Complexity Assessment` - Score breakdown and classification
4. `## Implementation Strategy` - Single-pass or phased approach
5. `## Stage Breakdown` - Detailed description of each stage
6. `## Phase Details` (if complex) - For each DSP/GUI phase
7. `## CPU Budget` - Expected CPU usage and optimization strategy
8. `## Polyphony Strategy` - Channel handling and SIMD optimization
9. `## Risk Assessment` - Technical challenges and mitigation
10. `## Timeline Estimate` - Expected duration for each stage

**State management:**

1. Update `.continue-here.md`:
```yaml
---
module: [ModuleName]
stage: 1
status: complete
last_updated: [YYYY-MM-DD HH:MM:SS]
complexity_score: [X.X]
phased_implementation: [true/false]
---

# Resume Point

## Current State: Stage 1 - Planning Complete

Implementation plan created. Ready to proceed to foundation (Stage 2).

## Completed So Far

**Stage 0:** ✓ Complete
**Stage 1:** ✓ Complete
- Complexity score: [X.X]
- Strategy: [Single-pass | Phased implementation]
- CPU budget: [<1% | 1-3% | 3-10% | >10%]
- Polyphony: [Monophonic | Polyphonic up to N channels]
- Plan documented

## Next Steps

1. Stage 2: Foundation (create build system)
2. Review plan details
3. Pause here

## Files Created
- modules/[ModuleName]/.ideas/architecture.md
- modules/[ModuleName]/.ideas/plan.md
```

2. Update MODULES.md status to `🚧 Stage 1` and add timeline entry

3. Git commit:
```bash
git add modules/${MODULE_NAME}/.ideas/plan.md modules/${MODULE_NAME}/.continue-here.md MODULES.md
git commit -m "$(cat <<'EOF'
feat: [ModuleName] Stage 1 - planning complete

Complexity: [X.X]
Strategy: [Single-pass | Phased implementation]
CPU Budget: [<1% | 1-3% | 3-10% | >10%]

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Decision menu (numbered format):**

```
✓ Stage 1 complete: Implementation plan created (Complexity [X.X], [single-pass/phased])

What's next?
1. Continue to Stage 2 - Foundation (via /implement) (recommended)
2. Review plan.md details
3. Adjust complexity assessment
4. Review contracts (parameter-spec, architecture) ← Discover design-sync
5. Pause here
6. Other

Choose (1-6): _
```

Wait for user input. Handle:
- Number (1-6): Execute corresponding option
- "continue" keyword: Execute option 1
- "pause" keyword: Execute option 5
- "review" keyword: Execute option 2
- "other": Ask "What would you like to do?" then re-present menu

---

## Handoff to Implementation

**When user chooses to proceed to Stage 2:**

1. **Delete planning handoff** to prevent confusion (two `.continue-here.md` files):
```bash
rm modules/${MODULE_NAME}/.ideas/.continue-here.md
```

2. **Create implementation handoff** at root that module-workflow skill expects:

```bash
# Create at modules/[ModuleName]/.continue-here.md (NOT in .ideas/)
```

```yaml
---
module: [ModuleName]
stage: 1
status: complete
last_updated: [YYYY-MM-DD HH:MM:SS]
complexity_score: [X.X]
phased_implementation: [true/false]
next_stage: 2
ready_for_implementation: true
---

# Ready for Implementation

Planning complete. All contracts created:
- ✓ creative-brief.md
- ✓ parameter-spec.md
- ✓ architecture.md
- ✓ plan.md

Run `/implement [ModuleName]` to begin Stage 2 (Foundation).
```

Display to user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Planning Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Module: [ModuleName]
Complexity: [X.X] ([Simple/Complex])
Strategy: [Single-pass | Phased implementation]
CPU Budget: [<1% | 1-3% | 3-10% | >10%]
Polyphony: [Monophonic | Polyphonic up to N channels]

Contracts created:
✓ creative-brief.md
✓ parameter-spec.md
✓ architecture.md
✓ plan.md

Ready to build. Run: /implement [ModuleName]
```

---

## VCV Rack Research Specifics

**When researching for Stage 0, focus on:**

### 1. VCV Rack API Classes

**Core Module Classes:**
- `rack::Module` - Base class for all modules
- `rack::Port` (Input/Output) - Audio/CV/gate ports
- `rack::Param` - Knobs, switches, buttons
- `rack::Light` - LED indicators

**DSP Utilities:**
- `rack::dsp::SchmittTrigger` - Gate/trigger detection
- `rack::dsp::PulseGenerator` - Generate trigger pulses
- `rack::dsp::ClockDivider` - Reduce processing rate
- `rack::dsp::RCFilter` - Simple RC filter
- `rack::dsp::ExponentialFilter` - Smoothing
- `rack::simd::float_4` - SIMD processing (4 channels at once)

**Example Research Notes:**
```markdown
## VCV Rack DSP Classes

**SchmittTrigger** (rack::dsp::SchmittTrigger)
- Purpose: Detect rising/falling edges on gate inputs
- Usage: `if (trigger.process(inputs[GATE_INPUT].getVoltage())) { /* triggered */ }`
- Hysteresis: 0.1V - 2.0V (configurable)

**SIMD float_4** (rack::simd::float_4)
- Purpose: Process 4 polyphonic channels simultaneously
- Usage: `simd::float_4 in = inputs[AUDIO_INPUT].getVoltageSimd<float_4>(c);`
- Performance: 4x faster than scalar processing
```

### 2. Polyphony Patterns

**Research how professional modules handle polyphony:**

```markdown
## Polyphony Research

**Mutable Instruments Plaits** (macro oscillator)
- Polyphony: Up to 16 channels
- Processing: SIMD optimized (process 4 channels per iteration)
- CPU Impact: ~2% mono, ~8% with 16 channels (4x effective with SIMD)

**Befaco EvenVCO** (oscillator)
- Polyphony: Monophonic only
- Rationale: Complex algorithm, high CPU
- CPU Impact: ~3% per instance

**Pattern**: Complex algorithms may need monophonic-only approach for CPU budget
```

### 3. Voltage Range Standards

```markdown
## VCV Rack Voltage Standards

**Audio Signals:**
- Range: ±5V nominal (±10V peak)
- RMS: ~5V for "full scale" audio

**CV Modulation:**
- Standard: ±5V (most common)
- Extended: ±10V (some modules)

**Pitch CV:**
- Standard: 1V/octave
- C4 (261.626 Hz) = 0V
- C5 (523.251 Hz) = 1V
- A4 (440 Hz) = -0.75V

**Gates:**
- Low: 0V
- High: 10V
- Threshold: ~1V (with hysteresis)

**Triggers:**
- Pulse: 10V
- Duration: >1ms (typical)
```

### 4. CPU Budget Research

**Research CPU usage of similar modules:**

```markdown
## CPU Budget Analysis

**Reference Modules** (measured at 44.1kHz, single instance):
- VCV VCO-1: 0.8% (basic oscillator)
- Fundamental VCF: 1.2% (4-pole filter)
- Audible Instruments Plaits: 2.5% mono, 9% poly (complex oscillator)
- Vult Tangents: 3.5% (waveshaping)
- ML Modules freeverb: 8% (reverb)

**Our Module** (estimated):
- Algorithm complexity: [Simple/Moderate/Complex]
- Polyphony: [Mono/Poly up to 16]
- Estimated CPU: [X%] mono, [Y%] poly (if applicable)
```

---

## Reference Files

Detailed stage implementations are in:
- `references/stage-0-research.md` - Research stage details
- `references/stage-1-planning.md` - Planning stage details

Templates are in:
- `assets/architecture-template.md` - DSP architecture contract template
- `assets/plan-template.md` - Implementation plan template

---

## Integration Points

**Invoked by:**
- `/plan` command (to be created)
- `/implement` command (if contracts missing)
- `module-workflow` skill (if contracts incomplete)

**Invokes:**
- `design-sync` skill (if mockup exists and needs validation)
- `deep-research` skill (if user requests deeper investigation)

**Reads:**
- `creative-brief.md` (from module-ideation)
- `parameter-spec.md` (from ui-mockup finalization)

**Creates:**
- `architecture.md` (Stage 0)
- `plan.md` (Stage 1)
- `.continue-here.md` (handoff to module-workflow)

**Updates:**
- MODULES.md (status progression)

---

## Error Handling

**If creative-brief.md missing:**
```
✗ Cannot start planning without creative brief.

Run: /dream [ModuleName]

This will guide you through the ideation process to create the creative brief.
```

**If module already past Stage 1:**
```
✗ [ModuleName] is already in Stage [N].

Planning (Stages 0-1) is complete. Contracts exist:
- architecture.md
- plan.md

To make changes, use /improve [ModuleName].
To continue implementation, use /continue [ModuleName].
```

**If contracts exist but user wants to regenerate:**
```
Contracts already exist for [ModuleName]:
✓ architecture.md (Stage 0)
✓ plan.md (Stage 1)

Options:
1. Review existing contracts
2. Regenerate contracts (will overwrite)
3. Continue to implementation (/implement)
4. Cancel

Choose (1-4): _
```

---

## Success Criteria

Planning is successful when:

- Stage 0: architecture.md created with complete DSP specification
- Stage 1: plan.md created with complexity assessment and strategy
- Voltage ranges researched and documented
- Polyphony strategy defined (if applicable)
- CPU budget estimated
- VCV Rack API classes identified
- Professional module examples researched
- Contracts reference real VCV Rack patterns and classes
- User understands complexity and implementation approach
- Handoff file created for module-workflow skill

---

## Notes for Claude

**CRITICAL RESEARCH REQUIREMENTS:**

1. **ALWAYS research VCV Rack API** - Don't assume JUCE patterns
2. **ALWAYS consider polyphony** - Even if monophonic, document why
3. **ALWAYS estimate CPU budget** - Critical for module viability
4. **ALWAYS document voltage ranges** - VCV Rack standards differ from other platforms
5. **ALWAYS reference professional modules** - Learn from existing implementations

**When executing this skill:**

1. Read creative-brief.md thoroughly before research
2. Use WebSearch to find VCV Rack documentation and examples
3. Research professional modules in same category
4. Document specific VCV Rack classes (not generic DSP theory)
5. Consider SIMD optimization for polyphonic modules
6. Estimate realistic CPU budget based on algorithm complexity
7. Present decision menus after each stage completion
8. Don't auto-proceed - wait for user confirmation

**Common pitfalls to AVOID:**

- ❌ Assuming JUCE patterns apply to VCV Rack
- ❌ Not considering polyphony (even if monophonic, document decision)
- ❌ Ignoring CPU budget (critical in VCV Rack ecosystem)
- ❌ Not researching VCV Rack API classes
- ❌ Using generic voltage ranges (use VCV Rack standards)
- ❌ Not referencing professional modules
- ❌ Auto-proceeding without user confirmation
