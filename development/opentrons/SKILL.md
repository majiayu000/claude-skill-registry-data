---
name: opentrons
description: Expert guidance for Opentrons Python API v2 - automated liquid handling, protocol development, labware management, and hardware module integration for OT-2 and Flex robots
allowed-tools: ["*"]
---

# Opentrons Python API v2

## Overview

The **Opentrons Python API v2** enables laboratory automation through Python protocols that control liquid handling robots (OT-2 and Flex). Write protocols that automate pipetting, temperature control, magnetic separation, plate reading, and complex multi-step workflows with reproducible precision.

**Core value:** Transform manual, error-prone pipetting workflows into automated, reproducible protocols. A 100-line protocol can replace hours of manual work with precise, documented liquid handling.

## When to Use

Use the Opentrons skill when:
- Writing automated liquid handling protocols
- Setting up serial dilutions, plate replication, or reagent distribution
- Integrating temperature control, magnetic separation, or plate reading into workflows
- Adapting OT-2 protocols for Opentrons Flex
- Troubleshooting protocol execution or hardware integration
- Optimizing pipetting parameters (flow rates, tip positions, mixing)

**Specialized subskills available:**
- `heater-shaker` - Temperature control with orbital mixing
- `absorbance-reader` - Microplate spectrophotometry
- `gripper` - Automated labware movement (Flex only)
- `thermocycler` - PCR thermal cycling
- `temperature-module` - Precise heating/cooling (4-95°C)
- `magnetic-block` - Magnetic bead separation (Flex only)

**Don't use when:**
- Working with non-Opentrons liquid handlers
- Writing general Python code unrelated to lab automation
- You need detailed module-specific guidance (use the specialized subskills)

## Robot Platforms

### Opentrons Flex
Modern platform with advanced capabilities:
- Gripper for automated labware movement
- 96-channel pipetting
- Coordinate-based deck slots (A1-D3)
- Larger working volume and deck space
- Trash bin requires explicit loading (API 2.16+)
- Staging area slots in column 4

### OT-2
Established platform:
- Numeric deck slots (1-12)
- Fixed trash in slot 12
- 1-channel and 8-channel pipettes
- Proven reliability for standard protocols

**Both platforms use identical API syntax** with platform-specific parameters.

## Protocol Structure

Every Opentrons protocol follows this framework:

```python
from opentrons import protocol_api

# 1. Metadata - Protocol identification
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@example.com>',
    'description': 'Brief description of what this protocol does',
    'apiLevel': '2.19'
}

# 2. Requirements - Robot specification (Flex)
requirements = {"robotType": "Flex", "apiLevel": "2.19"}

# 3. Main function - Setup and commands
def run(protocol: protocol_api.ProtocolContext):
    # Setup: Load labware, pipettes, modules
    tips = protocol.load_labware("opentrons_flex_96_tiprack_1000ul", "A1")
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "B1")
    pipette = protocol.load_instrument("flex_1channel_1000", "left", tip_racks=[tips])

    # Commands: Sequential robot instructions
    pipette.pick_up_tip()
    pipette.aspirate(100, plate["A1"])
    pipette.dispense(100, plate["B1"])
    pipette.drop_tip()
```

**Key principles:**
- Protocols execute **completely linearly** - follow line-by-line to understand robot actions
- Use descriptive variable names that mirror lab terminology
- Add comments to document workflow steps
- Group related operations logically

## Core API Components

### 1. Loading Equipment

**Labware** - Plates, tubes, reservoirs:
```python
# Load standard labware from registry
plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "B1")
tips = protocol.load_labware("opentrons_flex_96_tiprack_1000ul", "A1")

# Load custom labware (JSON definition required)
custom = protocol.load_labware("custom_24_tuberack_1500ul", "C1")
```

**Pipettes** - Single, 8-channel, or 96-channel:
```python
# Flex pipettes
left_pip = protocol.load_instrument("flex_1channel_1000", "left", tip_racks=[tips])
right_pip = protocol.load_instrument("flex_8channel_1000", "right", tip_racks=[tips])

# OT-2 pipettes
p300 = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])
```

**Modules** - Temperature, magnetic, thermocycler:
```python
# Load module in specific deck slot
temp_mod = protocol.load_module("temperature module gen2", "D1")
# Load labware on module
temp_plate = temp_mod.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul")
```

**Trash bin** (Flex, API 2.16+):
```python
trash = protocol.load_trash_bin("A3")
```

### 2. Accessing Wells

**Individual wells:**
```python
plate["A1"]           # Single well by name
plate.wells()[0]      # First well by index
plate.wells_by_name()["A1"]  # Dictionary access
```

**Well ranges and groups:**
```python
plate.wells()[:8]     # First row (A1-H1)
plate.rows()[0]       # All wells in row A
plate.columns()[0]    # All wells in column 1
plate.wells("A1", "H12")  # Range from A1 to H12
```

**8-channel pipetting patterns:**
```python
# Pipette to entire column with 8-channel
pipette.transfer(100, reservoir["A1"], plate.columns()[0])
```

### 3. Liquid Handling Commands

**Basic operations:**
```python
pipette.pick_up_tip()
pipette.aspirate(volume=100, location=plate["A1"], rate=1.0)
pipette.dispense(volume=100, location=plate["B1"], rate=1.0)
pipette.blow_out(location=plate["B1"])
pipette.mix(repetitions=3, volume=50, location=plate["B1"])
pipette.drop_tip()  # or pipette.return_tip()
```

**Complex transfers:**
```python
# Single source to multiple destinations
pipette.distribute(
    volume=50,
    source=reservoir["A1"],
    dest=[plate.wells()[i] for i in range(8)],
    new_tip="once"
)

# Multiple sources to single destination (pooling)
pipette.consolidate(
    volume=20,
    source=plate.rows()[0],
    dest=reservoir["A2"],
    new_tip="always"
)

# One-to-one transfer with mixing
pipette.transfer(
    volume=100,
    source=plate.columns()[0],
    dest=plate.columns()[1],
    mix_after=(3, 50),
    new_tip="always"
)
```

### 4. Position Control

**Well positions:**
```python
# Top of well (default: 1mm below top)
location = plate["A1"].top()
location = plate["A1"].top(z=-2)  # 2mm below top

# Bottom of well (default: 1mm above bottom)
location = plate["A1"].bottom()
location = plate["A1"].bottom(z=2)  # 2mm above bottom

# Center of well
location = plate["A1"].center()
```

**Movement:**
```python
# Move to location without liquid operations
pipette.move_to(plate["A1"].top())

# Delay at current position
protocol.delay(seconds=5)
protocol.delay(minutes=2)
```

### 5. Tip Management

**Flexible pickup strategies:**
```python
# Pick up from specific tip rack location
pipette.pick_up_tip(tips["A1"])

# Automatic tip tracking
pipette.pick_up_tip()  # Uses next available tip

# Reset tip tracking
tips.reset()  # Mark all tips as available again
```

### 6. Liquid Tracking

**Define liquids for better protocol documentation:**
```python
# Define reagents
water = protocol.define_liquid(
    name="Water",
    description="Molecular biology grade H2O",
    display_color="#0000FF"
)

buffer = protocol.define_liquid(
    name="Lysis Buffer",
    description="10mM Tris-HCl pH 8.0",
    display_color="#00FF00"
)

# Assign liquids to wells with volumes
reservoir["A1"].load_liquid(liquid=water, volume=50000)  # 50mL
plate["A1"].load_liquid(liquid=buffer, volume=200)
```

### 7. Runtime Parameters

**User-configurable variables:**
```python
def add_parameters(parameters):
    parameters.add_int(
        variable_name="sample_count",
        display_name="Number of Samples",
        description="How many samples to process",
        default=24,
        minimum=1,
        maximum=96,
        unit="samples"
    )

    parameters.add_float(
        variable_name="transfer_volume",
        display_name="Transfer Volume",
        default=50.0,
        minimum=10.0,
        maximum=200.0,
        unit="µL"
    )

def run(protocol: protocol_api.ProtocolContext):
    # Access parameters
    num_samples = protocol.params.sample_count
    vol = protocol.params.transfer_volume
```

## Hardware Modules

Opentrons supports multiple hardware modules for specialized workflows. Each module has dedicated API methods:

### Temperature Module
Precise heating/cooling (4-95°C):
```python
temp_mod = protocol.load_module("temperature module gen2", "D1")
plate = temp_mod.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul")

temp_mod.set_temperature(celsius=4)  # Blocks until reached
temp_mod.deactivate()
```

**Use the `temperature-module` subskill** for detailed guidance.

### Heater-Shaker Module
Temperature control with orbital mixing:
```python
hs_mod = protocol.load_module("heaterShakerModuleV1", "D1")
adapter = hs_mod.load_adapter("opentrons_96_flat_bottom_adapter")
plate = adapter.load_labware("nest_96_wellplate_200ul_flat")

hs_mod.close_labware_latch()
hs_mod.set_and_wait_for_temperature(37)
hs_mod.set_and_wait_for_shake_speed(500)  # rpm
protocol.delay(minutes=5)
hs_mod.deactivate_shaker()
hs_mod.deactivate_heater()
hs_mod.open_labware_latch()
```

**Use the `heater-shaker` subskill** for detailed guidance including non-blocking temperature control, speed ranges, and OT-2 deck restrictions.

### Thermocycler Module
PCR thermal cycling:
```python
tc_mod = protocol.load_module("thermocyclerModuleV2")
plate = tc_mod.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt")

tc_mod.close_lid()
tc_mod.set_lid_temperature(105)
tc_mod.set_block_temperature(95, hold_time_seconds=180, block_max_volume=50)

# PCR profile
profile = [
    {"temperature": 95, "hold_time_seconds": 30},
    {"temperature": 57, "hold_time_seconds": 30},
    {"temperature": 72, "hold_time_seconds": 60}
]
tc_mod.execute_profile(steps=profile, repetitions=30, block_max_volume=50)
tc_mod.set_block_temperature(72, hold_time_minutes=5)

tc_mod.deactivate_lid()
tc_mod.deactivate_block()
tc_mod.open_lid()
```

**Use the `thermocycler` subskill** for detailed guidance including auto-sealing lids and advanced profiling.

### Absorbance Plate Reader (Flex only)
Microplate spectrophotometry:
```python
reader = protocol.load_module("absorbanceReaderV1", "D3")

reader.close_lid()
reader.initialize("single", [450])  # Single wavelength
reader.open_lid()

# Move plate to reader with gripper
protocol.move_labware(plate, reader, use_gripper=True)

reader.close_lid()
data = reader.read(export_filename="my_plate_data")
reader.open_lid()

# Access results
absorbance_a1 = data[450]["A1"]  # OD at 450nm for well A1
```

**Use the `absorbance-reader` subskill** for detailed guidance including multi-wavelength reading and data formats.

### Magnetic Block (Flex only)
Magnetic bead separation:
```python
mag_block = protocol.load_module("magneticBlockV1", "D1")
mag_plate = mag_block.load_labware("biorad_96_wellplate_200ul_pcr")

# Move plate to magnetic block with gripper
protocol.move_labware(mag_plate, mag_block, use_gripper=True)

# Wait for bead separation
protocol.delay(minutes=3)

# Pipette supernatant (beads held by magnets)
pipette.transfer(100, mag_plate["A1"], waste["A1"])

# Move plate away from magnets
protocol.move_labware(mag_plate, "C1", use_gripper=True)
```

**Use the `magnetic-block` subskill** for detailed guidance.

## Flex-Specific Features

### Gripper
Automated labware movement:
```python
# Move labware between locations
protocol.move_labware(
    labware=plate,
    new_location="C2",
    use_gripper=True
)

# Move to module
protocol.move_labware(plate, temp_mod, use_gripper=True)

# Dispose in waste chute
protocol.move_labware(plate, protocol.load_waste_chute(), use_gripper=True)

# Move with offset adjustments
protocol.move_labware(
    plate,
    "D2",
    use_gripper=True,
    pick_up_offset={"x": 0, "y": 0, "z": 2},
    drop_offset={"x": 0, "y": 0, "z": 1}
)
```

**Important:** Open module lids/latches before gripper movement (e.g., `tc_mod.open_lid()`, `hs_mod.open_labware_latch()`).

**Use the `gripper` subskill** for detailed guidance.

### 96-Channel Pipetting
Full-plate transfers in single operations:
```python
pipette_96 = protocol.load_instrument("flex_96channel_1000", "left")

# Pick up entire tip rack
pipette_96.pick_up_tip()

# Transfer entire plate
pipette_96.transfer(100, source_plate.wells(), dest_plate.wells())

pipette_96.drop_tip()
```

### Staging Area Slots
Column 4 slots (A4, B4, C4, D4) serve as staging areas for:
- Absorbance reader lid storage
- Temporary labware placement
- Gripper operations

**Note:** Cannot load labware in column 4 when absorbance reader is present.

## Adapting OT-2 Protocols for Flex

**Key changes required:**

1. **Update requirements:**
```python
requirements = {"robotType": "Flex", "apiLevel": "2.19"}
```

2. **Update pipette models:**
```python
# OT-2
p300 = protocol.load_instrument("p300_single_gen2", "left")

# Flex
p1000 = protocol.load_instrument("flex_1channel_1000", "left")
```

3. **Update tip racks:**
```python
# OT-2
tips = protocol.load_labware("opentrons_96_tiprack_300ul", "1")

# Flex
tips = protocol.load_labware("opentrons_flex_96_tiprack_1000ul", "A1")
```

4. **Load trash bin (API 2.16+):**
```python
trash = protocol.load_trash_bin("A3")
```

5. **Update deck slots (optional - both formats work):**
```python
# Numeric (OT-2 style, works on both)
plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "1")

# Coordinate (Flex style, works on both)
plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "D1")
```

## Common Patterns

### Serial Dilution
```python
def serial_dilution(pipette, source, destinations, dilution_factor, volume):
    """Perform serial dilution across wells."""
    # Transfer from source to first destination
    pipette.transfer(volume, source, destinations[0])

    # Serial transfers with mixing
    for i in range(len(destinations) - 1):
        pipette.transfer(
            volume / dilution_factor,
            destinations[i],
            destinations[i + 1],
            mix_after=(3, volume / 2)
        )

# Use pattern
serial_dilution(
    pipette=p1000,
    source=reservoir["A1"],
    destinations=plate.rows()[0],  # Row A
    dilution_factor=2,
    volume=100
)
```

### Plate Replication
```python
# Replicate entire plate
pipette.transfer(
    volume=50,
    source=source_plate.wells(),
    dest=dest_plate.wells(),
    new_tip="always"
)
```

### Cherry Picking
```python
# Transfer specific wells
source_wells = [source_plate["A1"], source_plate["C3"], source_plate["E5"]]
dest_wells = [dest_plate["B2"], dest_plate["D4"], dest_plate["F6"]]

pipette.transfer(100, source_wells, dest_wells, new_tip="always")
```

### Reagent Distribution
```python
# Distribute from reservoir to plate
pipette.distribute(
    volume=50,
    source=reservoir["A1"],
    dest=plate.wells(),
    disposal_volume=10,  # Extra volume for blowout
    new_tip="once"
)
```

## Best Practices

1. **Use liquid tracking** - Define and load liquids for better protocol documentation
2. **Add runtime parameters** - Make protocols configurable without editing code
3. **Optimize tip usage** - Use `distribute`/`consolidate` to minimize tip consumption
4. **Set flow rates appropriately** - Adjust for viscous or volatile liquids
5. **Include delays** - Allow time for mixing, settling, or temperature equilibration
6. **Deactivate modules** - Turn off heaters/shakers/coolers at protocol end
7. **Test with simulation** - Validate protocols before running on hardware
8. **Document thoroughly** - Use comments, metadata, and liquid definitions
9. **Handle errors gracefully** - Add pauses for user intervention when needed
10. **Calibrate labware offsets** - Ensure accurate positioning for your specific labware

## Advanced Features

### Conditional Logic
```python
# Dynamic protocol behavior based on parameters
if protocol.params.include_control:
    pipette.transfer(100, control_buffer, plate["A1"])

# Process only occupied wells
for well in plate.wells():
    if well.has_liquid():
        pipette.mix(3, 100, well)
```

### Air Gaps
Prevent dripping between wells:
```python
pipette.aspirate(100, source_well)
pipette.air_gap(10)  # 10µL air gap
pipette.dispense(110, dest_well)
```

### Touch Tip
Remove droplets from pipette exterior:
```python
pipette.aspirate(100, source_well)
pipette.touch_tip(location=source_well, radius=0.8, v_offset=-2)
pipette.dispense(100, dest_well)
```

### Blow Out
Ensure complete dispense:
```python
pipette.aspirate(100, source_well)
pipette.dispense(100, dest_well)
pipette.blow_out(dest_well.top())
```

## Common Mistakes

**❌ Forgetting to pick up tips:**
```python
pipette.aspirate(100, plate["A1"])  # Error: no tip attached
```

**✅ Correct:**
```python
pipette.pick_up_tip()
pipette.aspirate(100, plate["A1"])
```

**❌ Not deactivating modules:**
```python
temp_mod.set_temperature(4)
# Protocol ends - module stays at 4°C!
```

**✅ Correct:**
```python
temp_mod.set_temperature(4)
# ... operations ...
temp_mod.deactivate()
```

**❌ Gripper movement with closed latch:**
```python
protocol.move_labware(plate, hs_mod, use_gripper=True)  # Error: latch closed
```

**✅ Correct:**
```python
hs_mod.open_labware_latch()
protocol.move_labware(plate, hs_mod, use_gripper=True)
hs_mod.close_labware_latch()
```

**❌ Wrong deck slot format for Flex:**
Using numeric slots without quotes may cause confusion; both work, but coordinate format is clearer:
```python
plate = protocol.load_labware("corning_96_wellplate_360ul_flat", 1)  # Works but unclear
```

**✅ Correct:**
```python
plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "D1")  # Clear
```

## Troubleshooting

**Protocol won't load:**
- Check API version in requirements matches your robot firmware
- Verify labware names are correct (check Opentrons labware library)
- Ensure module loading specifies valid deck slots for your robot

**Pipetting errors:**
- Verify tip rack is correctly loaded and has available tips
- Check volume is within pipette range
- Ensure source/destination wells have sufficient volume/space

**Module errors:**
- Open lids/latches before gripper movement
- Allow modules to reach target temperature before proceeding
- Verify module is loaded in compatible deck slot

**Gripper errors:**
- Ensure labware is grippable (has compatible geometry)
- Check destination is accessible and not occupied
- Verify use_gripper=True is set

## Installation

Protocols run on Opentrons robots via the Opentrons App. For protocol development and simulation:

```bash
pip install opentrons
```

**Simulation:**
```bash
opentrons_simulate protocol.py
```

## Additional Resources

- **Official Documentation:** https://docs.opentrons.com/v2/
- **Protocol Library:** https://protocols.opentrons.com/
- **Python API Reference:** https://docs.opentrons.com/v2/new_protocol_api.html
- **Labware Library:** https://labware.opentrons.com/
- **Support Forum:** https://support.opentrons.com/
- **GitHub:** https://github.com/Opentrons/opentrons

## Related Subskills

For detailed module-specific guidance:
- `heater-shaker` - Heater-Shaker Module
- `absorbance-reader` - Absorbance Plate Reader
- `gripper` - Flex Gripper
- `thermocycler` - Thermocycler Module
- `temperature-module` - Temperature Module
- `magnetic-block` - Magnetic Block
