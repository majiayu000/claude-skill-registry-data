---
name: opentrons-magnetic-block
description: Opentrons Magnetic Block for Flex - unpowered magnetic bead separation using gripper-based labware movement with high-strength neodymium magnets for DNA/RNA purification, immunoprecipitation, and bead-based workflows
allowed-tools: ["*"]
---

# Opentrons Magnetic Block

## Overview

The **Opentrons Magnetic Block** is an unpowered, 96-well magnetic separator exclusively for Opentrons Flex. It uses high-strength neodymium magnets to pull magnetic beads to the side of wells, enabling supernatant removal for DNA/RNA purification, protein cleanup, immunoprecipitation, and other bead-based separation protocols.

**Core value:** Automate magnetic bead-based purification workflows without manual plate transfers. Combine gripper-based plate movement with magnetic separation for fully automated DNA extraction, PCR cleanup, and bead-based assays.

**Platform:** Opentrons Flex only (not compatible with OT-2)

## When to Use

Use the Magnetic Block skill when:
- Performing DNA/RNA extraction with magnetic beads
- PCR product cleanup (AMPure, SPRIselect beads)
- Magnetic bead-based library preparation (NGS)
- Protein purification or immunoprecipitation with magnetic beads
- Cell sorting or enrichment with magnetic particles
- Any protocol requiring magnetic bead separation

**Don't use when:**
- Working with OT-2 robot (Magnetic Block is Flex-only)
- Need vertical bead movement within solution (block only pulls to side)
- Require heated magnetic separation
- Working without Opentrons Flex gripper

## Quick Reference

| Operation | Method | Key Parameters |
|-----------|--------|----------------|
| Load module | `protocol.load_module()` | `"magneticBlockV1"`, location |
| Move plate to block | `protocol.move_labware()` | labware, mag_block, use_gripper=True |
| Wait for separation | `protocol.delay()` | minutes (typically 2-5) |
| Pipette supernatant | `pipette.transfer()` | source, dest |
| Move plate off block | `protocol.move_labware()` | labware, new_location, use_gripper=True |

## Platform Requirements

**Opentrons Flex only**
- **API version:** 2.15 or later (Magnetic Block introduced)
- **Gripper required:** All plate movement uses gripper
- **Robot type:** Must specify `"robotType": "Flex"`

## Key Characteristics

### Unpowered Design

**Important:** The Magnetic Block is completely unpowered:
- No electronic control
- No on/off switching
- Always magnetic when plate is present
- Robot and Opentrons App are **not aware** of magnetic state

**Implication:** All control is manual through:
- Physical plate positioning (gripper movement)
- Timed delays for bead separation
- Pipetting operations

## Loading the Module

```python
from opentrons import protocol_api

metadata = {'apiLevel': '2.19'}
requirements = {"robotType": "Flex", "apiLevel": "2.19"}

def run(protocol: protocol_api.ProtocolContext):
    # Load Magnetic Block
    mag_block = protocol.load_module(
        module_name="magneticBlockV1",
        location="D1"
    )

    # Load compatible labware
    mag_plate = mag_block.load_labware(
        name="biorad_96_wellplate_200ul_pcr"
    )
```

**Compatible deck slots:** Any Flex slot (A1-D3)
**Recommended:** D1, D2, or D3 (bottom row for workflow efficiency)

## Compatible Labware

The Magnetic Block works with 96-well plates that fit the magnetic footprint:

**Common compatible labware:**
- `biorad_96_wellplate_200ul_pcr`
- `nest_96_wellplate_100ul_pcr_full_skirt`
- `opentrons_96_wellplate_200ul_pcr_full_skirt`
- Other 96-well PCR plates with standard footprint

**Important:**
- Labware must be grippable (compatible with Flex gripper)
- Wells must align with magnet positions
- Standard 96-well footprint required

## Basic Magnetic Separation Workflow

### Step 1: Load Sample Plate

```python
# Start with sample plate on deck (not on magnetic block yet)
sample_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", "C1")

# Add magnetic beads and binding buffer
pipette.transfer(10, bead_stock, sample_plate.wells())
pipette.transfer(100, binding_buffer, sample_plate.wells(), mix_after=(5, 80))
```

### Step 2: Incubate for Binding

```python
# Incubate to allow beads to bind target (DNA/RNA/protein)
protocol.delay(minutes=5)

# Optional: Mix during incubation (use Heater-Shaker)
```

### Step 3: Move to Magnetic Block

```python
# Move plate to magnetic block using gripper
protocol.move_labware(
    labware=sample_plate,
    new_location=mag_block,
    use_gripper=True
)
```

### Step 4: Wait for Bead Separation

```python
# Allow beads to collect at side of wells
protocol.delay(minutes=3)

# Beads are now held at well edges by magnets
```

### Step 5: Remove Supernatant

```python
# Pipette supernatant while beads are held by magnets
pipette.transfer(
    volume=110,
    source=sample_plate.wells(),
    dest=waste.wells(),
    new_tip="always"
)

# Beads remain in wells, held by magnetic field
```

### Step 6: Move Off Magnetic Block

```python
# Move plate off magnets for bead resuspension
protocol.move_labware(
    labware=sample_plate,
    new_location="C2",
    use_gripper=True
)

# Beads are now free to resuspend
```

### Step 7: Wash and Repeat

```python
# Add wash buffer
pipette.transfer(150, wash_buffer, sample_plate.wells())

# Mix to resuspend beads
pipette.mix(repetitions=5, volume=100, location=sample_plate.wells())

# Return to magnetic block
protocol.move_labware(sample_plate, mag_block, use_gripper=True)

# Wait for separation
protocol.delay(minutes=2)

# Remove supernatant
pipette.transfer(150, sample_plate.wells(), waste.wells(), new_tip="always")
```

### Step 8: Elute

```python
# Move off magnets
protocol.move_labware(sample_plate, "C2", use_gripper=True)

# Add elution buffer
pipette.transfer(50, elution_buffer, sample_plate.wells(), mix_after=(5, 30))

# Incubate
protocol.delay(minutes=2)

# Final magnetic separation
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
protocol.delay(minutes=2)

# Transfer eluate (purified product)
pipette.transfer(45, sample_plate.wells(), elution_plate.wells(), new_tip="always")
```

## Complete DNA Extraction Protocol

```python
# Complete automated DNA extraction workflow
def run(protocol: protocol_api.ProtocolContext):
    # Modules and labware
    mag_block = protocol.load_module("magneticBlockV1", "D1")
    sample_plate = mag_block.load_labware("biorad_96_wellplate_200ul_pcr")

    # Additional labware
    tips = protocol.load_labware("opentrons_flex_96_tiprack_1000ul", "A1")
    waste = protocol.load_trash_bin("A3")
    reagents = protocol.load_labware("nest_12_reservoir_15ml", "C2")

    # Pipette
    pipette = protocol.load_instrument("flex_8channel_1000", "left", tip_racks=[tips])

    # Reagent locations
    lysis_beads = reagents["A1"]
    wash_buffer = reagents["A2"]
    elution_buffer = reagents["A3"]

    # Samples already in plate (loaded manually or via earlier steps)

    # 1. Add lysis beads and bind DNA
    pipette.transfer(100, lysis_beads, sample_plate.columns()[0], mix_after=(5, 80))
    protocol.delay(minutes=5)

    # 2. Magnetic separation - remove lysate
    protocol.move_labware(sample_plate, mag_block, use_gripper=True)
    protocol.delay(minutes=3)
    pipette.transfer(200, sample_plate.columns()[0], waste, new_tip="always")

    # 3. First wash
    protocol.move_labware(sample_plate, "C1", use_gripper=True)
    pipette.transfer(150, wash_buffer, sample_plate.columns()[0], mix_after=(5, 100))
    protocol.move_labware(sample_plate, mag_block, use_gripper=True)
    protocol.delay(minutes=2)
    pipette.transfer(150, sample_plate.columns()[0], waste, new_tip="always")

    # 4. Second wash
    protocol.move_labware(sample_plate, "C1", use_gripper=True)
    pipette.transfer(150, wash_buffer, sample_plate.columns()[0], mix_after=(5, 100))
    protocol.move_labware(sample_plate, mag_block, use_gripper=True)
    protocol.delay(minutes=2)
    pipette.transfer(150, sample_plate.columns()[0], waste, new_tip="always")

    # 5. Dry beads
    protocol.delay(minutes=5)

    # 6. Elute DNA
    protocol.move_labware(sample_plate, "C1", use_gripper=True)
    pipette.transfer(50, elution_buffer, sample_plate.columns()[0], mix_after=(5, 30))
    protocol.delay(minutes=2)

    # 7. Final magnetic separation
    protocol.move_labware(sample_plate, mag_block, use_gripper=True)
    protocol.delay(minutes=2)

    # 8. Collect purified DNA
    elution_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", "C3")
    pipette.transfer(45, sample_plate.columns()[0], elution_plate.columns()[0], new_tip="always")
```

## Common Patterns

### PCR Cleanup (AMPure Beads)

```python
# Clean PCR product with AMPure beads
mag_block = protocol.load_module("magneticBlockV1", "D1")
pcr_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", "C1")

# 1. Add beads (0.8x ratio for >300bp fragments)
pipette.transfer(40, ampure_beads, pcr_plate.wells(), mix_after=(5, 35))
protocol.delay(minutes=5)

# 2. Magnetic separation
protocol.move_labware(pcr_plate, mag_block, use_gripper=True)
protocol.delay(minutes=3)
pipette.transfer(90, pcr_plate.wells(), waste.wells())

# 3. Ethanol washes (2x)
for _ in range(2):
    pipette.transfer(150, ethanol_70, pcr_plate.wells())
    protocol.delay(seconds=30)
    pipette.transfer(150, pcr_plate.wells(), waste.wells())

# 4. Dry
protocol.delay(minutes=5)

# 5. Elute
protocol.move_labware(pcr_plate, "C2", use_gripper=True)
pipette.transfer(30, water, pcr_plate.wells(), mix_after=(5, 20))
protocol.delay(minutes=2)

# 6. Final separation and collection
protocol.move_labware(pcr_plate, mag_block, use_gripper=True)
protocol.delay(minutes=2)
pipette.transfer(25, pcr_plate.wells(), clean_plate.wells())
```

### NGS Library Preparation

```python
# Magnetic bead-based library prep
mag_block = protocol.load_module("magneticBlockV1", "D2")
lib_plate = mag_block.load_labware("biorad_96_wellplate_200ul_pcr")

# After adapter ligation...

# 1. Add SPRI beads for size selection (0.6x for >400bp)
pipette.transfer(30, spri_beads, lib_plate.wells(), mix_after=(5, 25))
protocol.delay(minutes=5)

# 2. Bind large fragments
protocol.move_labware(lib_plate, mag_block, use_gripper=True)
protocol.delay(minutes=3)

# 3. SAVE supernatant (contains fragments to remove)
protocol.move_labware(lib_plate, "C1", use_gripper=True)

# 4. Add more beads to supernatant (bring to 1.0x total)
pipette.transfer(20, spri_beads, lib_plate.wells(), mix_after=(5, 30))
protocol.delay(minutes=5)

# 5. Bind desired fragments
protocol.move_labware(lib_plate, mag_block, use_gripper=True)
protocol.delay(minutes=3)

# 6. Discard supernatant
pipette.transfer(100, lib_plate.wells(), waste.wells())

# 7. Wash and elute (standard protocol)
```

### Protein Immunoprecipitation

```python
# Magnetic bead IP
mag_block = protocol.load_module("magneticBlockV1", "D1")
ip_plate = mag_block.load_labware("biorad_96_wellplate_200ul_pcr")

# 1. Pre-coupled antibody-bead complex in wells

# 2. Add lysate
pipette.transfer(100, lysate_plate.wells(), ip_plate.wells(), mix_after=(3, 80))

# 3. Incubate (binding)
protocol.delay(minutes=30)

# 4. Wash unbound protein
for wash_num in range(3):
    protocol.move_labware(ip_plate, mag_block, use_gripper=True)
    protocol.delay(minutes=2)
    pipette.transfer(150, ip_plate.wells(), waste.wells())

    protocol.move_labware(ip_plate, "C1", use_gripper=True)
    pipette.transfer(150, wash_buffer, ip_plate.wells(), mix_after=(3, 100))

# 5. Elute bound protein
protocol.move_labware(ip_plate, "C1", use_gripper=True)
pipette.transfer(50, elution_buffer, ip_plate.wells(), mix_after=(5, 30))
protocol.delay(minutes=5)

# 6. Collect eluate
protocol.move_labware(ip_plate, mag_block, use_gripper=True)
protocol.delay(minutes=2)
pipette.transfer(45, ip_plate.wells(), analysis_plate.wells())
```

## Integration with Other Modules

### With Heater-Shaker (Heated Lysis)

```python
# Combine heating with magnetic purification
hs_mod = protocol.load_module("heaterShakerModuleV1", "D1")
mag_block = protocol.load_module("magneticBlockV1", "D2")
sample_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", "C1")

# 1. Heat lysis on heater-shaker
hs_mod.open_labware_latch()
protocol.move_labware(sample_plate, hs_mod, use_gripper=True)
hs_mod.close_labware_latch()
hs_mod.set_and_wait_for_temperature(56)
hs_mod.set_and_wait_for_shake_speed(1000)
protocol.delay(minutes=15)
hs_mod.deactivate_shaker()
hs_mod.deactivate_heater()
hs_mod.open_labware_latch()

# 2. Magnetic bead binding
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
protocol.delay(minutes=3)

# ... continue with washes and elution ...
```

### With Temperature Module (Cold Elution)

```python
# Cold elution for stability
temp_mod = protocol.load_module("temperature module gen2", "D3")
mag_block = protocol.load_module("magneticBlockV1", "D2")

# Pre-cool elution buffer
temp_mod.set_temperature(4)

# After magnetic washes...
protocol.move_labware(sample_plate, "C1", use_gripper=True)

# Add cold elution buffer
pipette.transfer(50, cold_elution, sample_plate.wells(), mix_after=(5, 30))

# Move to cold module for elution
protocol.move_labware(sample_plate, temp_mod, use_gripper=True)
protocol.delay(minutes=5)

# Final separation
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
protocol.delay(minutes=2)
pipette.transfer(45, sample_plate.wells(), storage_plate.wells())

temp_mod.deactivate()
```

### With Thermocycler (Post-PCR Cleanup)

```python
# PCR → Cleanup workflow
tc_mod = protocol.load_module("thermocyclerModuleV2")
mag_block = protocol.load_module("magneticBlockV1", "D2")

# Run PCR
tc_mod.close_lid()
# ... PCR cycling ...
tc_mod.set_block_temperature(4)
tc_mod.open_lid()

# Move to deck for bead addition
pcr_plate = tc_mod.labware
protocol.move_labware(pcr_plate, "C1", use_gripper=True)

# Add AMPure beads
pipette.transfer(40, ampure_beads, pcr_plate.wells(), mix_after=(5, 35))
protocol.delay(minutes=5)

# Cleanup on magnetic block
protocol.move_labware(pcr_plate, mag_block, use_gripper=True)
# ... cleanup steps ...
```

## Best Practices

1. **Allow sufficient separation time** - Typically 2-5 minutes depending on bead type
2. **Use gripper for all plate movements** - Manual movement defeats automation purpose
3. **Avoid disturbing beads when pipetting** - Aspirate from opposite side of well
4. **Mix thoroughly after moving off magnets** - Ensure complete bead resuspension
5. **Track bead volume in calculations** - Account for beads when calculating total volume
6. **Use consistent bead types** - Different beads have different separation times
7. **Plan deck layout** - Position magnetic block near other modules for efficiency
8. **Test separation time** - Optimize delay for your specific beads and sample type
9. **Don't over-dry beads** - Can reduce elution efficiency
10. **Validate elution volume** - Leave some headroom to avoid transferring beads

## Separation Time Guidelines

**Typical separation times by bead type:**
- **AMPure/SPRIselect (DNA):** 2-3 minutes
- **RNAClean (RNA):** 3-4 minutes
- **Protein G/A beads:** 2-3 minutes
- **High-density beads:** 1-2 minutes
- **Large volume samples:** 4-5 minutes

**Factors affecting separation:**
- Bead concentration
- Sample volume
- Viscosity
- Magnetic bead strength
- Well geometry

**Recommendation:** Start with 3 minutes, adjust based on visual inspection or protocol optimization.

## Common Mistakes

**❌ Moving plate without gripper:**
```python
# Manual movement not practical in automated protocol
protocol.move_labware(sample_plate, mag_block, use_gripper=False)
# User must manually move plate - defeats automation
```

**✅ Correct:**
```python
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
```

**❌ Insufficient separation time:**
```python
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
protocol.delay(seconds=30)  # Too short - beads still in solution
pipette.transfer(100, sample_plate.wells(), waste.wells())  # Transfers beads!
```

**✅ Correct:**
```python
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
protocol.delay(minutes=3)  # Adequate time for separation
pipette.transfer(100, sample_plate.wells(), waste.wells())
```

**❌ Pipetting through bead pellet:**
```python
# Aspirating from center may disturb beads on side
pipette.aspirate(100, sample_plate.wells()[0])
```

**✅ Correct:**
```python
# Aspirate from side opposite beads
pipette.aspirate(100, sample_plate.wells()[0].bottom(z=2))
# Or use touch_tip to ensure beads aren't transferred
```

**❌ Incomplete bead resuspension:**
```python
protocol.move_labware(sample_plate, "C1", use_gripper=True)
pipette.transfer(150, wash_buffer, sample_plate.wells())  # Beads may not resuspend
```

**✅ Correct:**
```python
protocol.move_labware(sample_plate, "C1", use_gripper=True)
pipette.transfer(150, wash_buffer, sample_plate.wells(), mix_after=(5, 100))  # Mix to resuspend
```

**❌ Using incompatible labware:**
```python
# Deep well plates may not align with magnets properly
mag_plate = mag_block.load_labware("nest_96_wellplate_2ml_deep")
```

**✅ Correct:**
```python
# Use standard 96-well PCR plates
mag_plate = mag_block.load_labware("biorad_96_wellplate_200ul_pcr")
```

## Troubleshooting

**Beads not separating:**
- Increase separation time (try 4-5 minutes)
- Check bead type and concentration
- Verify plate is properly seated on magnetic block
- Ensure labware is compatible with magnet positions

**Beads being transferred with supernatant:**
- Extend separation time
- Pipette more carefully (avoid bead pellet)
- Reduce aspiration flow rate
- Leave more residual volume

**Incomplete elution:**
- Ensure beads are fully resuspended before elution incubation
- Mix more vigorously
- Extend elution incubation time
- Verify beads haven't dried excessively
- Use appropriate elution buffer volume

**Bead clumping:**
- Mix more thoroughly when resuspending
- Ensure beads are well-mixed before adding to samples
- Avoid drying beads too long
- Check bead storage conditions

**Variable recovery across wells:**
- Ensure consistent bead addition volumes
- Mix uniformly across all wells
- Use consistent separation times
- Check for plate positioning issues on magnetic block

## Advanced Techniques

### Dual-Size Selection

```python
# Select DNA fragments within specific size range
# First selection: Remove large fragments
pipette.transfer(30, spri_beads, lib_plate.wells(), mix_after=(5, 25))  # 0.6x
protocol.delay(minutes=5)
protocol.move_labware(lib_plate, mag_block, use_gripper=True)
protocol.delay(minutes=3)

# Collect supernatant (has small + target fragments)
protocol.move_labware(lib_plate, "C1", use_gripper=True)
pipette.transfer(80, lib_plate.wells(), temp_plate.wells())

# Second selection: Bind target fragments
pipette.transfer(20, spri_beads, temp_plate.wells(), mix_after=(5, 30))  # Brings to 1.0x
protocol.delay(minutes=5)
protocol.move_labware(temp_plate, mag_block, use_gripper=True)
protocol.delay(minutes=3)

# Discard supernatant (small fragments removed)
pipette.transfer(100, temp_plate.wells(), waste.wells())

# Wash and elute target size range
```

### Differential Elution

```python
# Elute different targets sequentially
# After binding multiple targets to beads...

# First elution (low stringency)
pipette.transfer(50, elution_buffer_1, sample_plate.wells(), mix_after=(5, 30))
protocol.delay(minutes=2)
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
protocol.delay(minutes=2)
pipette.transfer(45, sample_plate.wells(), fraction_1_plate.wells())

# Second elution (high stringency)
protocol.move_labware(sample_plate, "C1", use_gripper=True)
pipette.transfer(50, elution_buffer_2, sample_plate.wells(), mix_after=(5, 30))
protocol.delay(minutes=2)
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
protocol.delay(minutes=2)
pipette.transfer(45, sample_plate.wells(), fraction_2_plate.wells())
```

## No Electronic Control

**Remember:** The Magnetic Block has no electronic interface.

**This means:**
- ❌ Cannot turn magnets on/off programmatically
- ❌ No status reporting to robot
- ❌ No automatic timing
- ✅ Full control through plate positioning
- ✅ Predictable, passive magnetic field
- ✅ No calibration or initialization required

**Control strategy:** Move plate TO block = magnets engaged, move plate OFF block = magnets disengaged

## API Version Requirements

- **Minimum API version:** 2.15 (Magnetic Block introduced)
- **Recommended:** 2.19+ for full Flex feature support
- **Robot type:** Must be Opentrons Flex

## Additional Resources

- **Magnetic Block Documentation:** https://docs.opentrons.com/v2/modules/magnetic_block.html
- **Gripper Documentation:** https://docs.opentrons.com/v2/new_protocol_api.html#opentrons.protocol_api.ProtocolContext.move_labware
- **Protocol Library:** https://protocols.opentrons.com/
- **Opentrons Support:** https://support.opentrons.com/

## Related Skills

- `opentrons` - Main Opentrons Python API skill
- `opentrons-gripper` - Automated labware movement (required)
- `opentrons-heater-shaker` - Heated incubation with mixing
- `opentrons-temperature-module` - Temperature control
- `opentrons-thermocycler` - PCR for molecular workflows
