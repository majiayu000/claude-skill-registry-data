---
name: eda-schematics
description: Schematic capture and wiring. Create schematic sheets, place symbols, add wires and net labels, organize hierarchical designs.
allowed-tools: Read, Write, Glob, mcp__kicad-sch__create_schematic, mcp__kicad-sch__add_component, mcp__kicad-sch__search_components, mcp__kicad-sch__add_wire, mcp__kicad-sch__add_hierarchical_sheet, mcp__kicad-sch__add_sheet_pin, mcp__kicad-sch__add_hierarchical_label, mcp__kicad-sch__list_components, mcp__kicad-sch__get_schematic_info
---

# EDA Schematics Skill

Create and wire schematics for electronics projects.

## Auto-Activation Triggers

This skill activates when:
- User asks to "create schematic", "add component", "wire"
- User is working with `.kicad_sch` files
- User asks about net names, connections, or ERC
- Project has component selections but no schematic
- User mentions schematic organization or sheets

## Context Requirements

**Requires:**
- `docs/component-selections.md` - Selected components with LCSC numbers
- `docs/design-constraints.json` - Project constraints
- `datasheets/` - Component datasheets for reference circuits

**Produces:**
- `hardware/*.kicad_sch` - KiCad schematic file(s)
- `docs/schematic-status.md` - Status and progress tracking

## Workflow

### 1. Load Context
```
@docs/design-constraints.json
@docs/component-selections.md
@datasheets/ (relevant datasheets)
```

**From design-constraints.json, extract:**
- `power.topology` - LDO vs buck affects schematic complexity
- `power.rails[]` - All voltage rails to implement
- `board.layers` - 2-layer = simpler designs, 4+ = can be more complex
- `thermal.budget` - Identify hot components for grouping
- `dfmTargets.assembly` - Package sizes must match

### 1.5. Validate Readiness

Before starting schematic:

- [ ] All required components selected in `component-selections.md`?
- [ ] MCU selected with known pinout?
- [ ] Voltage regulators selected?
- [ ] Critical passives (decoupling values) defined?
- [ ] Datasheets downloaded for reference circuits?

If not, suggest running `/eda-source [role]` first.

### 2. Plan Sheet Organization

See `reference/SCHEMATIC-HIERARCHY-DECISION.md` for detailed guidance.

Based on complexity, organize into sheets:

**Simple design (1-2 sheets):**
- Sheet 1: Everything

**Medium design (3-4 sheets):**
- Sheet 1: Power (input, regulators)
- Sheet 2: MCU and core logic
- Sheet 3: Interfaces and I/O

**Complex design (5+ sheets):**
- Sheet 1: Power input and protection
- Sheet 2: Voltage regulation
- Sheet 3: MCU and clock
- Sheet 4: Communication interfaces
- Sheet 5: Connectors and I/O
- Additional sheets as needed

### 3. Create Schematic Structure
- Create main schematic file
- Add hierarchical sheets if multi-sheet
- Set up page sizes and title blocks

### 4. Place Components (Per Sheet)
For each component:
1. Place symbol from library
2. Set reference designator
3. Set value
4. Add LCSC part number to properties
5. Position logically

**Tool syntax:**
```
mcp__kicad-sch__add_component schematic_path="/path/to/file.kicad_sch" lib_id="EDA-MCP:SymbolName" reference="U1" value="10k" position=[100, 100]
```

- Use `symbol_ref` from `library_fetch` response (e.g., `EDA-MCP:ESP32-C3`)
- For standard parts, use KiCad libraries (e.g., `Device:R`, `Device:C`)
- Position uses grid-aligned coordinates (1.27mm grid)

**Placement guidelines:**
- Power flows top-to-bottom or left-to-right
- Signal flows left-to-right
- Group related components
- Leave space for wiring

### 5. Add Power Symbols
- Place VCC symbols for each rail
- Place GND symbols
- Use consistent power symbol naming

### 6. Wire Connections
Follow the reference circuits from datasheets:
1. Wire power connections first
2. Add decoupling capacitors to power pins
3. Wire critical signals (crystal, reset)
4. Wire communication buses
5. Wire remaining signals

Use net labels for:
- Inter-sheet connections
- Buses
- Avoiding wire crossing
- Named signals (for clarity)

### 7. Verify and Document
- Check all pins connected or marked NC
- Run ERC (electrical rules check)
- Document status

See `reference/ERC-VIOLATIONS-GUIDE.md` for fixing common ERC errors.

### 8. Pre-Layout Review

Before proceeding to layout, complete `reference/SCHEMATIC-REVIEW-CHECKLIST.md`:
- Power section verification
- Decoupling validation
- Interface protection check
- Test points present
- Net naming consistency
- Documentation complete

## Net Naming Convention

See `reference/NET-NAMING.md` for complete conventions.

**Quick reference:**
```
Power:    VCC_3V3, VCC_5V, VBAT, GND, GNDA
Reset:    MCU_RESET, nRESET
SPI:      SPI1_MOSI, SPI1_MISO, SPI1_SCK, SPI1_CS
I2C:      I2C1_SDA, I2C1_SCL
UART:     UART1_TX, UART1_RX
GPIO:     LED_STATUS, BTN_USER, or GPIO_PA0
```

## Output Format

### schematic-status.md

```markdown
# Schematic Status

Project: [name]
Updated: [date]

## Summary
- Total sheets: X
- Components placed: Y
- Wiring: Z% complete
- ERC: X errors, Y warnings

## Sheets

### Sheet 1: Power
- Status: Complete
- Components: U1 (regulator), C1-C4 (caps)
- Notes: ...

### Sheet 2: MCU
- Status: In Progress
- Components: U2 (MCU), Y1 (crystal), C5-C10
- Notes: Needs clock wiring

## ERC Issues
- [ ] Unconnected pin on U2.PA3 (intentional NC)
- [x] Missing power flag (fixed)

## Next Steps
- Complete MCU clock circuit
- Wire SPI bus to flash
- Run final ERC
```

## Guidelines

- Always check datasheets for reference circuits
- Place decoupling caps within 3mm of IC power pins (in layout)
- Use net labels for any signal that crosses sheets
- Keep schematic readable - avoid wire spaghetti
- Add notes for non-obvious connections
- Mark intentionally unconnected pins with NC flag

## Architecture Validation Warnings

Check these before proceeding to layout:

| Condition | Warning |
|-----------|---------|
| Buck converter selected but no inductor in schematic | Missing critical component |
| USB interface but no ESD protection | Add ESD diodes before layout |
| External connector but no protection | Add TVS/ESD on exposed signals |
| MCU with <100nF per VDD pin | Verify decoupling against datasheet |
| Crystal but no load cap calculation | Recalculate CL values |
| I2C bus but no pull-ups | Add pull-ups (4.7K-10K) |
| SPI CS lines floating | Add pull-ups to prevent glitches |
| Reset pin without RC debounce | Add debounce circuit |

## Reference Documents

| Document | Purpose |
|----------|---------|
| `reference/NET-NAMING.md` | Net naming conventions |
| `reference/SYMBOL-ORGANIZATION.md` | Schematic layout patterns |
| `reference/REFERENCE-CIRCUITS.md` | Common circuit patterns |
| `reference/SCHEMATIC-HIERARCHY-DECISION.md` | Sheet organization guidance |
| `reference/SCHEMATIC-REVIEW-CHECKLIST.md` | Pre-layout validation |
| `reference/ERC-VIOLATIONS-GUIDE.md` | Fixing ERC errors |

## Next Steps

After schematic is complete:
1. Generate netlist
2. Run `/eda-layout` to begin PCB layout
3. Update `design-constraints.json` stage to "pcb"
