---
name: module-ideation
description: Adaptive brainstorming for VCV Rack module concepts and improvements
allowed-tools:
  - Read
  - Write
  - Bash
preconditions:
  - None (entry point)
---

# module-ideation Skill

**Purpose:** Interactive brainstorming and creative vision capture for new VCV Rack modules and improvements to existing modules.

## Mode Detection

**Check if module exists:**

```bash
grep "^### $MODULE_NAME$" MODULES.md
```

- If found → **Improvement Mode**
- If not found → **New Module Mode**

## New Module Mode

### Phase 1: Free-Form Collection

Start with open question:
```
What would you like to build?

Tell me about your module idea. Share as much or as little as you want—I'll ask follow-ups for anything missing.
```

**Extract from response:**
- Module name (if mentioned)
- Module category (Oscillator, Filter, VCA, Effect, Utility, Sequencer, etc.)
- Core concept and sonic/modular goals
- I/O ideas (CV inputs, audio inputs, gate inputs, polyphonic channels)
- Parameter ideas and voltage ranges
- Panel vision and HP width
- Use cases and target users
- Inspirations and references

### Phase 2: Gap Analysis and Question Prioritization

**Question Priority Tiers:**

- **Tier 1 (Critical):** Module category (Oscillator/Filter/VCA/etc.), core concept (what it does)
- **Tier 2 (Functional):** I/O configuration (CV/audio/gate), voltage ranges (±5V, 1V/oct), processing behavior
- **Tier 3 (Context):** Use cases, inspirations, special features (polyphony, expanders, alternative panels)
- **Tier 4 (NEVER ASK):** Panel details - if user volunteers panel info, capture it in the brief but NEVER prompt for panel design in ideation phase

**Extract from Phase 1 response, then identify gaps:**

1. Parse user's free-form description
2. Check which tiers are covered
3. Identify missing critical/functional information
4. Never ask about already-provided information

**Example of smart extraction:**

```
User: "I want a wavefolder with a CV-controlled fold amount. Should have 4HP and a clean minimal design."

Extracted:
- Category: Effect (wavefolder) ✓
- Core concept: Wavefolder with CV control ✓
- I/O: fold CV input (1 mentioned) ✓
- Panel: 4HP, minimal ✓ (capture but don't expand)

Gaps identified:
- What other I/O? (audio in/out, polyphonic?) (Tier 2)
- What voltage range for fold CV? (Tier 2)
- Specific wavefolder algorithm? (Tier 3)
- Primary use case? (Tier 3)
```

### Phase 3: Question Batch Generation

**Generate exactly 4 questions using AskUserQuestion based on identified gaps.**

**Rules:**
- If 4+ gaps exist: ask top 4 by tier priority
- If fewer gaps exist: pad with "nice to have" tier 3 questions
- Provide meaningful options (not just open text prompts)
- Always include "Other" option for custom input
- Users can skip questions via "Other" option and typing "skip"

**VCV-specific considerations for questions:**
- HP width (typical ranges: oscillators 8-12HP, filters 6-10HP, utilities 3-6HP, effects 6-12HP)
- Polyphony support (monophonic or up to 16 channels)
- Voltage standards (CV: ±5V or ±10V, Pitch: 1V/octave, Gates: 0V/10V)
- Port types (audio, CV, gate, trigger)

**Example question batch (via AskUserQuestion):**

For the wavefolder example above:

```
Question 1:
  question: "What I/O configuration?"
  header: "Ports"
  options:
    - label: "Simple (1 audio in/out)", description: "Minimal monophonic"
    - label: "Stereo (2 audio in/out)", description: "Dual channel processing"
    - label: "Polyphonic (poly in/out)", description: "Up to 16 channels"
    - label: "Other", description: "Custom configuration"

Question 2:
  question: "What voltage range for fold CV input?"
  header: "CV range"
  options:
    - label: "±5V (standard)", description: "Standard Eurorack CV range"
    - label: "0-10V (unipolar)", description: "Unipolar control"
    - label: "±10V (extended)", description: "Extended range"
    - label: "Other", description: "Custom range"

Question 3:
  question: "Any specific wavefolder reference?"
  header: "Inspiration"
  options:
    - label: "Buchla 259", description: "Classic complex waveforms"
    - label: "Serge Wave Multipliers", description: "Multiple stages"
    - label: "Modern digital", description: "Clean, precise"
    - label: "Other", description: "Different reference or none"

Question 4:
  question: "Primary use case?"
  header: "Usage"
  options:
    - label: "Harmonics/timbre shaping", description: "Musical tone sculpting"
    - label: "Extreme effects", description: "Aggressive distortion"
    - label: "Both", description: "Versatile range"
    - label: "Other", description: "Different use case"
```

**After receiving answers:**
1. Accumulate context with previous responses
2. Re-analyze gaps
3. Proceed to decision gate

### Phase 3.5: Decision Gate

**Use AskUserQuestion with 3 options after each question batch:**

```
Question:
  question: "Ready to finalize the creative brief?"
  header: "Next step"
  options:
    - label: "Yes, finalize it", description: "Create creative-brief.md"
    - label: "Ask me 4 more questions", description: "Continue refining"
    - label: "Let me add more context first", description: "Provide additional details"

Route based on answer:
- Option 1 → Proceed to Phase 4 (document creation)
- Option 2 → Return to Phase 2 (re-analyze gaps, generate next 4 questions)
- Option 3 → Collect free-form text, merge with context, return to Phase 2
```

**Context accumulation example:**

After Batch 1 answers: "Polyphonic", "±5V (standard)", "Serge Wave Multipliers", "Both"

Updated context:
- I/O: polyphonic audio in/out, fold CV input ✓
- CV range: ±5V ✓
- Inspiration: Serge Wave Multipliers ✓
- Use case: versatile ✓

New gaps for Batch 2:
- How many fold stages? (Tier 2)
- Additional CV modulation targets? (Tier 2)
- Symmetry/asymmetry control? (Tier 3)
- Specific Serge model reference? (Tier 3)

### Phase 3.7: Module Name (if not yet provided)

**Before creating documents, check if module name was provided at any point during conversation.**

If name NOT yet provided, ask via AskUserQuestion:

```
Question:
  question: "What should this module be called?"
  header: "Module name"
  options:
    - label: "[SuggestedName1]", description: "Based on core concept"
    - label: "[SuggestedName2]", description: "Alternative naming"
    - label: "[SuggestedName3]", description: "Different approach"
    - label: "Other", description: "I'll provide my own name"

Where suggested names are generated from the core concept.
Examples:
- Wavefolder → "FoldMaster", "HarmonicFolder", "WaveStack"
- Filter → "ResoMax", "MultiMode", "SlopeFilter"
- VCA → "VeloVCA", "PolyAmp", "DualVCA"
```

**If name already provided** (in initial description or in additional context), skip this phase entirely.

**Name validation:**
- Must be UpperCamelCase (e.g., "FoldMaster", not "fold master" or "foldmaster")
- No spaces or special characters
- If user provides invalid name, suggest cleaned version

### Phase 4: Document Creation

When user chooses "finalize" and name is confirmed, create:

**File:** `modules/[ModuleName]/.ideas/creative-brief.md`

**Format:**
```markdown
# [ModuleName] - Creative Brief

## Overview

**Category:** [Oscillator/Filter/VCA/Effect/Utility/Sequencer/etc.]
**Core Concept:** [One-sentence description]
**Status:** 💡 Ideated
**Created:** [Date]

## Vision

[Prose description of module concept, sonic/modular goals, inspiration]

## I/O Configuration

### Inputs
| Port | Type | Range | Polyphonic | Description |
|------|------|-------|------------|-------------|
| [Name] | [Audio/CV/Gate/Trigger] | [Range] | [Yes/No] | [Purpose] |
| ... | ... | ... | ... | ... |

### Outputs
| Port | Type | Range | Polyphonic | Description |
|------|------|-------|------------|-------------|
| [Name] | [Audio/CV/Gate/Trigger] | [Range] | [Yes/No] | [Purpose] |
| ... | ... | ... | ... | ... |

## Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| [Name] | [Min-Max] | [Value] | [Purpose] |
| ... | ... | ... | ... |

## Panel Concept

**HP Width:** [N]HP ([N * 5.08]mm)
**Layout:** [Description]
**Visual Style:** [Description]
**Key Elements:** [List special panel components]

## Use Cases

- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

## Inspirations

- [Module/hardware reference 1]
- [Module/hardware reference 2]
- [Sonic reference]

## Technical Notes

**Polyphony:** [Monophonic | Up to N channels]
**Sample Rate:** [Per-sample processing | Block-based]
**Special Considerations:** [Any specific DSP approaches, algorithms, or technical considerations mentioned]

## Next Steps

- [ ] Create panel mockup (`/dream [ModuleName]` → option 3)
- [ ] Start implementation (`/implement [ModuleName]`)
```

**Also update MODULES.md:**

Add entry if doesn't exist:
```markdown
### [ModuleName]

**Status:** 💡 Ideated
**Category:** [Oscillator/Filter/VCA/Effect/Utility/Sequencer/etc.]
**Created:** [Date]
**Description:** [One-sentence summary]
```

### Phase 5: Session Handoff

Create `.continue-here.md` in `modules/[ModuleName]/.ideas/`:

**Format:**
```markdown
---
module: [ModuleName]
stage: ideation
status: creative_brief_complete
last_updated: [YYYY-MM-DD HH:MM:SS]
---

# Resume Point

## Current State: Creative Brief Complete

Creative brief has been finalized for [ModuleName]. Ready to proceed to panel mockup or implementation.

## Completed So Far

**Ideation:** ✓ Complete
- Core concept defined
- I/O configuration specified
- Parameters defined
- Panel vision captured
- Use cases identified

## Next Steps

1. Create panel mockup to visualize design (recommended)
2. Start implementation directly
3. Research similar modules for inspiration

## Context to Preserve

**Key Decisions:**
- Module category: [Oscillator/Filter/VCA/Effect/Utility/Sequencer/etc.]
- Core concept: [Brief summary]
- HP width: [N]HP
- Polyphony: [Monophonic | Polyphonic up to N channels]

**Files Created:**
- modules/[ModuleName]/.ideas/creative-brief.md
```

### Phase 6: Decision Menu

Present next steps:

```
✓ Creative brief complete: [ModuleName]

What's next?
1. Create panel mockup (recommended) ← Visualize before building
2. Start implementation
3. Research similar modules ← Find inspiration and examples
4. Save for later
5. Other

Choose (1-5): _
```

**Handle responses:**
- Option 1 → Invoke `ui-mockup` skill (adapted for VCV panels)
- Option 2 → Invoke `module-workflow` skill (after warning about contracts)
- Option 3 → Invoke `deep-research` skill (Phase 7 - stub for now, just acknowledge)
- Option 4 → Confirm handoff file created, exit
- Option 5 → Ask what they'd like to do

## Improvement Mode

### Phase 0: Vagueness Detection

Check if request is specific:

**Request IS specific if it has:**
- Feature name (e.g., "resonance parameter")
- Action (e.g., "add", "fix", "change")
- Acceptance criteria (e.g., "range 0-1V", "increase to 6HP")

**Request IS vague if lacking above:**
- "improve the filter"
- "better presets"
- "panel feels cramped"

**If vague, present choice:**
```
Your request is somewhat vague. How should I proceed?

1. Brainstorm approaches first (recommended) ← Explore options together
2. Implement something reasonable ← I'll investigate and propose a solution

Choose (1-2): _
```

If option 1 chosen, continue with improvement brainstorming.
If option 2 chosen, exit to module-improve skill.

### Phase 1: Free-Form Collection

Ask:
```
What would you like to improve in [ModuleName]?

Describe what you want to change, add, or fix. I'll ask follow-ups for anything missing.
```

**Extract from response:**
- What aspect (DSP/Parameters/I/O/Panel)
- Current pain point or limitation
- Proposed change
- Why this improvement matters
- Backward compatibility concerns
- How to test success

### Phase 2: Gap Analysis and Question Prioritization

**Question Priority Tiers:**

- **Tier 1 (Critical):** What aspect (DSP/Parameters/I/O/Panel), current state vs proposed change
- **Tier 2 (Implementation):** Implementation details, testing criteria, backward compatibility
- **Tier 3 (Context):** Rationale, success metrics, version impact

**Extract from Phase 1 response, then identify gaps:**

1. Parse user's improvement description
2. Check which tiers are covered
3. Identify missing critical information
4. Never ask about already-provided information

### Phase 3: Question Batch Generation

**Generate exactly 4 questions using AskUserQuestion based on identified gaps.**

**Rules:**
- If 4+ gaps exist: ask top 4 by tier priority
- If fewer gaps exist: pad with "nice to have" tier 3 questions
- Provide meaningful options (not just open text prompts)
- Always include "Other" option for custom input

**Example question batch (via AskUserQuestion):**

```
Question 1:
  question: "Which aspect would you like to improve?"
  header: "Aspect"
  options:
    - label: "Audio/CV processing (DSP)", description: "Change how it sounds/behaves"
    - label: "Parameters/I/O", description: "Add/modify/remove controls or ports"
    - label: "Panel interface", description: "Layout or visual changes"
    - label: "Features/workflow", description: "Presets, polyphony, utilities"

Question 2:
  question: "What's the current behavior you want to change?"
  header: "Current state"
  options:
    - label: "It's broken", description: "Bug or error"
    - label: "It's limited", description: "Missing functionality"
    - label: "It's inefficient", description: "Performance issue"
    - label: "Other", description: "Different issue"

Question 3:
  question: "Version impact of this change?"
  header: "Version bump"
  options:
    - label: "Patch (bugfix)", description: "v1.0.0 → v1.0.1"
    - label: "Minor (new feature)", description: "v1.0.0 → v1.1.0"
    - label: "Major (breaking change)", description: "v1.0.0 → v2.0.0"
    - label: "Other", description: "Not sure"

Question 4:
  question: "How to verify success?"
  header: "Testing"
  options:
    - label: "A/B test audio", description: "Compare before/after sound"
    - label: "Check parameter behavior", description: "Test controls work"
    - label: "Visual inspection", description: "Panel looks correct"
    - label: "Other", description: "Different testing approach"
```

**After receiving answers:**
1. Accumulate context with previous responses
2. Re-analyze gaps
3. Proceed to decision gate

### Phase 3.5: Decision Gate

**Use AskUserQuestion with 3 options after each question batch:**

```
Question:
  question: "Ready to finalize the improvement brief?"
  header: "Next step"
  options:
    - label: "Yes, finalize it", description: "Create improvement proposal"
    - label: "Ask me 4 more questions", description: "Continue refining"
    - label: "Let me add more context first", description: "Provide additional details"

Route based on answer:
- Option 1 → Proceed to Phase 4 (document creation)
- Option 2 → Return to Phase 2 (re-analyze gaps, generate next 4 questions)
- Option 3 → Collect free-form text, merge with context, return to Phase 2
```

### Phase 4: Document Creation

Create: `modules/[ModuleName]/.ideas/improvements/[feature-name].md`

**Format:**
```markdown
# [ModuleName] - [Improvement Name]

**Created:** [Date]
**Type:** [Feature/Enhancement/Fix]
**Aspect:** [DSP/Parameters/I/O/Panel]
**Version Impact:** [PATCH/MINOR/MAJOR]

## Current State

[Description of current behavior or limitation]

## Proposed Change

[Detailed description of what should change]

## Rationale

[Why this improvement matters]

## Implementation Notes

[Technical considerations, files to modify, algorithms to use]

## Backward Compatibility

[Breaking/Non-breaking, migration strategy if needed]

## Testing Criteria

- [ ] [Test 1]
- [ ] [Test 2]
- [ ] [Test 3]

## Success Metrics

[How to know the improvement is complete and working]
```

### Phase 5: Session Handoff

Create `.continue-here.md` in `modules/[ModuleName]/.ideas/`:

```markdown
---
module: [ModuleName]
stage: improvement_planning
status: improvement_brief_complete
improvement: [feature-name]
last_updated: [YYYY-MM-DD HH:MM:SS]
---

# Resume Point

## Current State: Improvement Brief Complete

Improvement proposal finalized for [ModuleName]: [ImprovementName]

## Completed So Far

**Planning:** ✓ Complete
- Current state analyzed
- Proposed change defined
- Testing criteria established

## Next Steps

1. Start implementation (/improve [ModuleName])
2. Research implementation approaches
3. Review existing code

## Context to Preserve

**Improvement:** [feature-name]
**Type:** [Feature/Enhancement/Fix]
**Version Impact:** [PATCH/MINOR/MAJOR]

**Files Created:**
- modules/[ModuleName]/.ideas/improvements/[feature-name].md
```

### Phase 6: Decision Menu

```
✓ Improvement brief complete: [ImprovementName]

What's next?
1. Start implementation (recommended)
2. Research implementation approaches ← Find examples and best practices
3. Review existing code first
4. Save for later
5. Other

Choose (1-5): _
```

**Handle responses:**
- Option 1 → Invoke `module-improve` skill
- Option 2 → Invoke `deep-research` skill (Phase 7 - stub)
- Option 3 → Read relevant source files, then re-present menu
- Option 4 → Confirm handoff file created, exit
- Option 5 → Ask what they'd like to do

## Vagueness Detection Rules

**Check for specificity:**

```
Specific indicators:
- Named feature ("resonance parameter", "bypass switch")
- Concrete action ("add", "remove", "change from X to Y")
- Measurable criteria ("range 0-1V", "increase to 6HP", "reduce CPU by 20%")

Vague indicators:
- Generic improvements ("better", "improve", "enhance")
- Unspecified targets ("the panel", "presets", "sound")
- No success criteria mentioned
```

If 2+ vague indicators and 0 specific indicators → Present brainstorm vs implement choice.

## Grounded Feasibility

**When user proposes ambitious ideas:**

Don't shut down creativity, but flag for research:

```
That's an interesting direction! [Specific technical consideration] might be complex—we can research approaches in Stage 0 (Research phase).

Continue exploring, or finalize brief with a research note?
```

Examples:
- Physical modeling → "Physical modeling can be CPU-intensive in per-sample processing"
- Complex FFT → "FFT operations require careful buffer management in VCV Rack"
- Heavy polyphony → "16-channel polyphonic processing requires optimized algorithms"

**Gently note challenges without saying "no."**

## Examples: Question Generation Based on Input Detail

### Example 1: Detailed Input (New Module)

```
User: "I want a wavefolder with CV-controlled fold amount. Should have 4HP and a minimal design."

Extracted:
- Category: Effect (wavefolder) ✓
- Core concept: Wavefolder with CV control ✓
- I/O: fold CV input (1 mentioned) ✓
- Panel: 4HP, minimal ✓ (capture but don't expand)

Gaps identified (4 needed):
- What other I/O? (audio in/out, polyphonic?) (Tier 2)
- What voltage range for fold CV? (Tier 2)
- Specific wavefolder algorithm? (Tier 3)
- Primary use case? (Tier 3)

Question Batch 1 (via AskUserQuestion):
1. "What I/O configuration?" → [Simple (1 audio in/out), Stereo, Polyphonic, Other]
2. "What voltage range for fold CV?" → [±5V (standard), 0-10V (unipolar), ±10V (extended), Other]
3. "Any specific wavefolder reference?" → [Buchla 259, Serge, Modern digital, Other]
4. "Primary use case?" → [Harmonics/timbre shaping, Extreme effects, Both, Other]

[Then decision gate with 3 options]
```

### Example 2: Vague Input (New Module)

```
User: "A filter module"

Extracted:
- Category: Filter ✓
- Core concept: Filter (very generic)

Gaps identified (4 needed):
- What filter type? (Tier 1)
- What I/O configuration? (Tier 2)
- CV modulation targets? (Tier 2)
- Primary use case? (Tier 3)

Question Batch 1 (via AskUserQuestion):
1. "What filter type?" → [Low-pass (LP), High-pass (HP), Multi-mode (LP/BP/HP), Other]
2. "What I/O configuration?" → [Mono, Stereo, Polyphonic, Other]
3. "What CV modulation?" → [Cutoff only, Cutoff + Resonance, Full modulation matrix, Other]
4. "Primary use case?" → [Subtractive synthesis, Effects processing, Both, Other]

[Then decision gate]

If user chooses "Ask me 4 more questions":
- User answered: "Multi-mode", "Polyphonic", "Cutoff + Resonance", "Both"

Updated context:
- Category: Filter ✓
- Core concept: Multi-mode polyphonic filter ✓
- I/O: polyphonic audio in/out ✓
- CV: cutoff and resonance modulation ✓
- Use case: versatile ✓

New gaps for Batch 2:
- Cutoff CV range? (Tier 2)
- Resonance CV range? (Tier 2)
- Filter slope? (Tier 3)
- Specific filter reference? (Tier 3)

Question Batch 2:
1. "Cutoff CV range?" → [±5V (standard), 1V/oct (tracking), ±10V (extended), Other]
2. "Resonance CV range?" → [±5V (standard), 0-10V (unipolar), Other]
3. "Filter slope?" → [2-pole (12dB/oct), 4-pole (24dB/oct), Variable, Other]
4. "Specific filter reference?" → [Moog ladder, State variable, Sallen-Key, Other]

[Then decision gate again]
```

## Adaptive Questioning Strategy

**Extract first, then fill gaps:**

1. User provides initial description
2. Parse response for covered topics
3. Generate questions only for missing topics
4. Present 4 questions via AskUserQuestion
5. After each batch, re-evaluate what's still missing
6. Present decision gate
7. Repeat until user finalizes

**Don't ask redundant questions.**

If user says "I want a wavefolder with CV-controlled fold amount, 4HP, minimal design," don't ask:
- ❌ "What category of module?" (it's a wavefolder = effect)
- ❌ "HP width?" (4HP mentioned)
- ❌ "Visual style?" (minimal mentioned)

DO ask:
- ✓ "What I/O configuration?" (audio ports not specified)
- ✓ "What voltage range for fold CV?"
- ✓ "Any specific wavefolder references for the algorithm?"

## Continuous Iteration Support

User can request deep dives:

```
User: "Ask me more about the panel"
→ System focuses on panel-specific questions

User: "Let's explore presets"
→ System asks about preset strategy

User: "Tell me what you think about the DSP"
→ System provides feasibility analysis
```

**Support free-form exploration until user says "finalize."**

## Git Integration

After creating documents:

```bash
git add modules/[ModuleName]/.ideas/
git add MODULES.md
# Do NOT commit - user handles commits
```

**Stage files but don't commit.**

## Error Handling

**If module name contains invalid characters:**
```
Module names should be UpperCamelCase with no spaces or special characters.

Suggested: [CleanName]
Use this name? (y/n): _
```

**If improvement file already exists:**
```
Improvement proposal "[feature-name].md" already exists.

Options:
1. Create new version (/improve is better for implementing existing proposals)
2. Choose different name
3. Overwrite existing (not recommended)

Choose (1-3): _
```

**If creative brief already exists:**
```
Creative brief already exists for [ModuleName].

Options:
1. View existing brief
2. Create improvement proposal instead (/improve)
3. Overwrite (will lose existing brief)

Choose (1-3): _
```

## Integration Points

**Invoked by:**
- `/dream` command (new module or improvement)
- `/dream [ModuleName]` command
- Natural language: "I want to make...", "Explore improvements to..."

**Invokes:**
- `ui-mockup` skill (option after creative brief) - adapted for VCV panels
- `module-workflow` skill (option after creative brief)
- `module-improve` skill (option after improvement brief)
- `deep-research` skill (option for research) - Phase 7

## Success Criteria

Skill is successful when:
- Creative brief captures complete vision
- No redundant questions asked
- User feels heard and understood
- Document is actionable for implementation
- Handoff file enables resume
- Next steps are clear and discoverable
