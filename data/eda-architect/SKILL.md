---
name: eda-architect
description: Electronics project architecture and constraint definition. Guides users through defining project requirements, power systems, interfaces, and physical constraints.
allowed-tools: Read, Write, WebSearch, Glob
---

# EDA Architect Skill

Define the architecture and constraints for electronics projects.

## Auto-Activation Triggers

This skill activates when:
- User asks to "design a board", "create a project", "start a new PCB"
- User asks "what do I need for..." an electronics project
- Project has no `docs/project-spec.md` or `docs/design-constraints.json`
- User mentions requirements gathering or project planning

## Context Requirements

**Requires:** Nothing (this is the first step)

**Produces:**
- `docs/project-spec.md` - Human-readable specification
- `docs/design-constraints.json` - Machine-readable constraints

## Workflow

### 1. Understand the Project Goal
Ask the user about:
- What is this device/board intended to do?
- Target use case (prototype, production, hobby)?
- Any existing designs to reference?

### 2. Define Power Architecture
Determine:
- Input power source (USB, battery, mains, PoE, solar)
- Voltage rails needed (3.3V, 5V, 12V, etc.)
- Power topology per rail: LDO vs buck converter
  - See `reference/POWER-TOPOLOGY-DECISION.md` for decision tree
- Estimated power budget
- Battery life requirements if applicable

### 2.5 Thermal Budget
Estimate early:
- Total power dissipation (sum of all consumers)
- Hot components (any >0.5W needs attention)
- Cooling strategy: natural, forced, heatsink
- See `reference/THERMAL-BUDGET.md` for estimation guide

### 3. Processing Requirements
Establish:
- MCU/processor needs (or if needed at all)
- Processing requirements (speed, peripherals)
- Memory requirements (Flash, RAM)
- Preferred families (STM32, ESP32, RP2040, etc.)

### 4. Connectivity & Interfaces
Document:
- Wireless: WiFi, Bluetooth, LoRa, Zigbee, cellular
- Wired: Ethernet, USB, CAN, RS485, RS232
- User interfaces: buttons, LEDs, displays
- Debug/programming interfaces

### 4.5 Stackup Decision
Determine layer count based on complexity:
- 2-layer: Simple, LDO only, low-speed (I2C/SPI)
- 4-layer: MCU with switching regulator, USB, Ethernet, WiFi
- 6-layer: High-speed (>100MHz), DDR, dense routing
- See `reference/LAYER-COUNT-DECISION.md` for decision tree

### 5. Sensors & I/O
List:
- Required sensors
- Analog inputs/outputs
- Digital I/O requirements
- Any specialized interfaces (motor control, etc.)

### 6. Physical Constraints
Define:
- Target board dimensions
- Enclosure requirements
- Mounting hole positions
- Connector placement constraints
- Height restrictions

### 7. Environmental
Note:
- Operating temperature range
- Indoor/outdoor use
- IP rating if applicable

### 8. Manufacturing Targets
Capture:
- Target quantity
- Assembly method (hand, reflow, turnkey)
- Layer count preference
- Budget constraints

### 8.5 DFM Early Constraints
Capture manufacturer capabilities:
- Preferred manufacturer (JLCPCB, PCBWay, OSHPark)
- Assembly method constraints
- Fine-pitch components (affects hand soldering)
- Budget tier: prototype, low-volume, production

## Output Format

### project-spec.md Structure

```markdown
# Project Specification: [Name]

## Overview
[Brief description and goals]

## Requirements Summary
| Category | Requirement |
|----------|-------------|
| Power Input | ... |
| Voltage Rails | ... |
| MCU | ... |
| Connectivity | ... |

## Detailed Requirements
[Sections for each category with full details]

## Constraints
[Physical, environmental, budget constraints]

## Open Questions
[Any unresolved items]
```

### design-constraints.json Schema

See `reference/CONSTRAINT-SCHEMA.md` for full schema documentation.

## Guidelines

- Ask clarifying questions rather than assuming
- Suggest common solutions when user is unsure
- Flag potential issues early (power budget, space constraints)
- Keep the spec focused - avoid scope creep
- Document rationale for key decisions
- Use project templates from `reference/PROJECT-TEMPLATES.md` as starting points

## Architecture Validation Warnings

Before completing the architecture phase, check for these risky combinations:

| Condition | Warning |
|-----------|---------|
| 2-layer + switching regulator | "Consider 4-layer - switching regulators need solid ground plane" |
| 2-layer + USB/Ethernet | "Controlled impedance difficult on 2-layer - consider 4-layer" |
| >2W total + no thermal plan | "Add thermal budget - high power needs planning" |
| Hand assembly + fine-pitch (<0.5mm) | "Verify solderability - fine-pitch is difficult to hand solder" |
| >0.5W component + no thermal strategy | "Component dissipating >0.5W needs thermal attention" |
| Battery + LDO with high Vin-Vout | "Consider buck converter for battery life" |

When a warning condition is detected, present it to the user and ask if they want to:
1. Update the design to address it
2. Acknowledge the risk and proceed

## Next Steps

After completing architecture, suggest:
1. `/eda-source [component-role]` to begin component selection
2. Start with critical components: MCU, power regulators
