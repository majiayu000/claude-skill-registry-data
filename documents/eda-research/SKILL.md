---
name: eda-research
description: Component research and procurement. Search JLC for components, analyze datasheets, compare options, and document selections with rationale.
allowed-tools: Read, Write, WebFetch, WebSearch, Glob, mcp__jlc__*
---

# EDA Research Skill

Source and select components for electronics projects.

## Auto-Activation Triggers

This skill activates when:
- User asks to "find a component", "search for", "source"
- User asks about component specifications or comparisons
- User mentions LCSC, datasheets, or part numbers
- User asks "what MCU/regulator/sensor should I use"
- Project has `design-constraints.json` but missing component selections

## Context Requirements

**Requires:**
- `docs/design-constraints.json` (or prompt user for requirements)
- `docs/project-spec.md` (optional, for context)

**Produces:**
- `docs/component-selections.md` - Human-readable selection log
- `docs/bom-draft.json` - Machine-readable BOM
- `datasheets/*.pdf` - Downloaded datasheets for selected components

## Workflow

### 1. Load Context
Read existing project constraints:
```
@docs/design-constraints.json
@docs/project-spec.md
@docs/component-selections.md (if exists)
```

If constraints missing, ask user for minimum requirements:
- What does this component need to do?
- Key specifications (voltage, current, package)?
- Budget constraints?

### 2. Understand Requirements
For the target component role, identify:
- Critical specifications (must-have)
- Preferred specifications (nice-to-have)
- Package preferences (SMD size, through-hole)
- Any specific brands or series to consider/avoid

### 2.5 Check Architecture Constraints
Before searching, review `design-constraints.json` for:
- **Power topology:** LDO vs buck decision already made in architect phase
- **Thermal budget:** Max watts for this role (check `thermal.hotComponents`)
- **DFM targets:** Assembly method affects package choice
- **Board layers:** May affect component density

For power components, see `reference/REGULATOR-SELECTION.md` for selection criteria.
For passives, see `reference/PASSIVE-SELECTION.md` and `reference/DECOUPLING-STRATEGY.md`.

### 3. Research Options
Use web search to understand:
- Common solutions for this application
- Recommended parts from reference designs
- Known issues or considerations
- Alternative approaches

### 4. Search JLC
Use `mcp__jlc__component_search` to find candidates:
- Search with specific parameters
- Filter by stock availability
- Note pricing at target quantity
- Check for "Basic" parts (lower assembly fee at JLCPCB)

### 5. Analyze Candidates
For top 3-5 options:
- Download/fetch datasheets
- Extract key specifications
- Check application circuits
- Note layout requirements
- Identify any gotchas

### 5.5 Validate Against Constraints
Before presenting options, verify each candidate:

**Thermal validation:**
```
P_dissipation = (calculated from datasheet)
Thermal budget = (from design-constraints.json)
✓ P_dissipation < Thermal budget
```

**Assembly compatibility:**
- Hand assembly → 0603/0805 minimum, no fine-pitch
- Reflow → 0402+ OK
- Turnkey → Check JLCPCB availability

**Architecture compliance:**
- Meets LDO/buck decision from architect phase
- Noise specs OK for rail type (analog vs digital)
- Efficiency acceptable for battery applications

Flag any candidates that fail validation with specific concerns.

### 6. Present Comparison
Create a comparison table:

| Part | MPN | Key Specs | Price | Stock | Pros | Cons |
|------|-----|-----------|-------|-------|------|------|
| ... | ... | ... | ... | ... | ... | ... |

Include recommendation with rationale.

### 7. Confirm Selection
- Get user confirmation
- Document selection with rationale
- Update constraint file
- Save datasheet

### 8. Validate Symbol (After library_fetch)

When fetching online components with `mcp__jlc__library_fetch`, **analyze the returned `validation_data`**:

**Quick checks:**
| Check | Expected | Action if Failed |
|-------|----------|------------------|
| `pin_pad_count_match` | `true` | Check for exposed pads (EP) |
| `has_power_pins` | `true` (for ICs) | Review pin types |
| `has_ground_pins` | `true` (for ICs) | Review pin names |

**Common issues:**
- **QFN/BGA packages** often have exposed thermal pads (EP) not included in symbol
- **Pin electrical types** may be incorrect (power pins marked as passive)
- **Pin names** may not match datasheet

**Fixing with library_fix:**

Use `mcp__jlc__library_fix` to regenerate symbol with corrections:

```
mcp__jlc__library_fix lcsc_id="C#####" corrections='{
  "pins": [
    { "action": "add", "number": "EP", "name": "GND", "type": "passive" },
    { "action": "modify", "number": "1", "set_type": "power_in" }
  ]
}'
```

**Correction actions:**
- `add` - Add missing pin (number, name, type required)
- `modify` - Rename and/or change electrical type
- `swap` - Swap positions of two pins
- `remove` - Remove incorrect pin

## Output Format

### component-selections.md Entry

```markdown
### [Role]: [Part Name] ([LCSC Number])

**Selected:** [Date]
**MPN:** [Manufacturer Part Number]
**Manufacturer:** [Name]
**Price:** $X.XX @ [quantity]

**Specifications:**
- Key spec 1: value
- Key spec 2: value

**Rationale:**
[Why this part was chosen over alternatives]

**Alternatives Considered:**
- [Part 2] - rejected because [reason]
- [Part 3] - rejected because [reason]

**Design Notes:**
- [Any layout or application notes from datasheet]

**Datasheet:** `datasheets/[filename].pdf`
```

### bom-draft.json Entry

```json
{
  "role": "regulator-3v3",
  "lcsc": "C6186",
  "mpn": "AMS1117-3.3",
  "manufacturer": "AMS",
  "description": "3.3V 1A LDO Regulator",
  "value": "3.3V",
  "footprint": "SOT-223",
  "quantity": 1,
  "unitPrice": 0.04,
  "extendedPrice": 0.04,
  "category": "power",
  "basic": true
}
```

## Component Role Categories

See `reference/COMPONENT-CATEGORIES.md` for detailed role definitions.

Common roles:
- `mcu` - Main microcontroller
- `regulator-Xv` - Voltage regulators
- `crystal` - Oscillators/crystals
- `connector-*` - Various connectors
- `esd-*` - ESD protection
- `decoupling-*` - Bypass/bulk capacitors
- `led-*` - Indicator LEDs
- `sensor-*` - Various sensors

## Guidelines

- Prefer JLCPCB "Basic" parts when suitable (lower assembly cost)
- Check stock levels - avoid parts with < 100 in stock
- Consider package size vs hand soldering capability
- Note lead times for non-stock items
- Always document why a part was chosen
- Download datasheets for all selected components
- **Identify 1-2 alternatives** for critical components (see `reference/COMPONENT-ALTERNATIVES.md`)
- **Validate thermal** before confirming power components
- **Check architecture decisions** from design-constraints.json before selecting

## Reference Documents

| Document | Use For |
|----------|---------|
| `REGULATOR-SELECTION.md` | LDO vs Buck selection criteria |
| `DECOUPLING-STRATEGY.md` | Capacitor values for ICs |
| `PASSIVE-SELECTION.md` | Resistor/capacitor fundamentals |
| `COMPONENT-ALTERNATIVES.md` | Finding equivalent parts |
| `DATASHEET-ANALYSIS.md` | Extracting key specs |
| `COMPONENT-CATEGORIES.md` | Role naming conventions |
| `JLC-SEARCH-TIPS.md` | Search strategies |

## Next Steps

After component selection is complete:
1. Run `/eda-source` for remaining components
2. When all components selected, run `/eda-schematic`
3. Update `design-constraints.json` stage to "schematic"
