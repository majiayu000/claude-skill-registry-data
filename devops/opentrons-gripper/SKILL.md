---
name: opentrons-gripper
description: Opentrons Flex Gripper - automated labware movement between deck locations, modules, waste chute, and off-deck storage with precise positioning and offset control for hands-free plate transfers
allowed-tools: ["*"]
---

# Opentrons Flex Gripper

## Overview

The **Opentrons Flex Gripper** enables fully automated labware movement without manual intervention. It moves plates, reservoirs, and tip racks between deck slots, hardware modules, trash/waste chute, and off-deck storage with precise positioning and optional offset adjustments.

**Core value:** Eliminate manual plate transfers during protocols. Automatically move labware between modules, enabling complex multi-step workflows without pausing for user intervention.

**Platform:** Opentrons Flex only (not available on OT-2)

## When to Use

Use the Gripper skill when:
- Moving labware between deck locations automatically
- Transferring plates between hardware modules (Temperature, Heater-Shaker, Magnetic Block, etc.)
- Loading plates onto Absorbance Reader or Thermocycler
- Disposing labware in waste chute
- Moving labware to/from off-deck storage
- Automating workflows that would otherwise require manual intervention

**Don't use when:**
- Working with OT-2 robot (gripper is Flex-only)
- Labware is not grippable (lacks compatible geometry/features)
- Manual control is preferred for delicate operations
- Pipette can accomplish the task without moving entire labware

## Quick Reference

| Operation | Method | Key Parameters |
|-----------|--------|----------------|
| Move labware | `protocol.move_labware()` | labware, new_location, use_gripper=True |
| Move with offsets | `protocol.move_labware()` | pick_up_offset, drop_offset |
| Move to module | `protocol.move_labware()` | labware, module_object, use_gripper=True |
| Dispose in waste | `protocol.move_labware()` | labware, waste_chute, use_gripper=True |
| Move off-deck | `protocol.move_labware()` | labware, OFF_DECK, use_gripper=True |
| Manual movement | `protocol.move_labware()` | use_gripper=False (pauses for user) |

## Platform Requirements

**Opentrons Flex only**
- **API version:** 2.15+ (gripper support)
- **Robot type:** Must specify `"robotType": "Flex"`

## Basic Usage

### Moving Between Deck Slots

```python
from opentrons import protocol_api

metadata = {'apiLevel': '2.19'}
requirements = {"robotType": "Flex", "apiLevel": "2.19"}

def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    source_plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "C1")

    # Move labware to new deck slot
    protocol.move_labware(
        labware=source_plate,
        new_location="D2",
        use_gripper=True
    )
```

**Deck slot formats (both work):**
- Coordinate format: "A1", "B2", "C3", "D1" (preferred for Flex)
- Numeric format: "1", "2", "3", etc. (OT-2 legacy, still compatible)

### Moving to Hardware Module

```python
# Load module and labware
temp_mod = protocol.load_module("temperature module gen2", "D1")
plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "C2")

# Move plate to temperature module
protocol.move_labware(
    labware=plate,
    new_location=temp_mod,
    use_gripper=True
)
```

### Moving to Waste Chute

```python
# Load waste chute
waste_chute = protocol.load_waste_chute()

# Dispose of used plate
protocol.move_labware(
    labware=used_plate,
    new_location=waste_chute,
    use_gripper=True
)
```

### Moving Off-Deck

```python
from opentrons.protocol_api import OFF_DECK

# Move labware off the deck (to storage)
protocol.move_labware(
    labware=archive_plate,
    new_location=OFF_DECK,
    use_gripper=True
)

# Later: bring back from off-deck storage
protocol.move_labware(
    labware=archive_plate,
    new_location="B3",
    use_gripper=True
)
```

**Use case:** Free up deck space by temporarily storing labware off-deck

## Position Offsets

Fine-tune pickup and drop positions with offset vectors:

### Basic Offset Syntax

```python
protocol.move_labware(
    labware=plate,
    new_location="D2",
    use_gripper=True,
    pick_up_offset={"x": 0, "y": 0, "z": 2},  # Lift 2mm higher when picking up
    drop_offset={"x": 0, "y": 0, "z": 1}      # Place 1mm higher when dropping
)
```

**Offset units:** Millimeters
**Coordinates:**
- **x:** Left (-) / Right (+)
- **y:** Back (-) / Front (+)
- **z:** Down (-) / Up (+)

### When to Use Offsets

**Pick-up offset:**
- Labware sits higher/lower than expected
- Adapters or custom labware with non-standard height
- Ensure proper gripper engagement

**Drop-off offset:**
- Ensure proper seating on module or adapter
- Accommodate non-standard landing surfaces
- Avoid collision with deck features

### Example with Custom Labware

```python
# Custom deep-well plate requires higher pickup
custom_plate = protocol.load_labware("custom_deepwell_96", "C1")

protocol.move_labware(
    labware=custom_plate,
    new_location="D1",
    use_gripper=True,
    pick_up_offset={"x": 0, "y": 0, "z": 3},  # Pickup 3mm higher
    drop_offset={"x": 0, "y": 0, "z": 0}      # Standard drop
)
```

## Manual Movement Alternative

Set `use_gripper=False` to pause protocol for user to manually move labware:

```python
# Pause for manual movement
protocol.move_labware(
    labware=delicate_plate,
    new_location="D3",
    use_gripper=False  # Protocol pauses, user moves plate manually
)
```

**Use case:** Delicate labware, non-grippable items, or troubleshooting

## Module Integration

### Temperature Module

```python
temp_mod = protocol.load_module("temperature module gen2", "D1")
plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "C2")

# Move to temperature module
protocol.move_labware(plate, temp_mod, use_gripper=True)

# Set temperature
temp_mod.set_temperature(4)
protocol.delay(minutes=5)

# Move off module
protocol.move_labware(plate, "C2", use_gripper=True)

temp_mod.deactivate()
```

### Heater-Shaker Module

**Critical:** Open labware latch before gripper operations

```python
hs_mod = protocol.load_module("heaterShakerModuleV1", "D1")
adapter = hs_mod.load_adapter("opentrons_96_flat_bottom_adapter")
plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "C2")

# Open latch BEFORE moving plate to module
hs_mod.open_labware_latch()

# Move plate to heater-shaker
protocol.move_labware(plate, hs_mod, use_gripper=True)

# Close latch for shaking
hs_mod.close_labware_latch()
hs_mod.set_and_wait_for_temperature(37)
hs_mod.set_and_wait_for_shake_speed(500)
protocol.delay(minutes=10)
hs_mod.deactivate_shaker()
hs_mod.deactivate_heater()

# Open latch BEFORE removing plate
hs_mod.open_labware_latch()

# Move plate off module
protocol.move_labware(plate, "C2", use_gripper=True)
```

### Thermocycler Module

**Critical:** Open lid before gripper operations

```python
tc_mod = protocol.load_module("thermocyclerModuleV2")
plate = protocol.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt", "C2")

# Open lid BEFORE moving plate to thermocycler
tc_mod.open_lid()

# Move plate to thermocycler
protocol.move_labware(plate, tc_mod, use_gripper=True)

# Close lid and run PCR
tc_mod.close_lid()
tc_mod.set_lid_temperature(105)
# ... PCR cycling ...

# Open lid BEFORE removing plate
tc_mod.open_lid()

# Move plate off thermocycler
protocol.move_labware(plate, "C2", use_gripper=True)
```

### Magnetic Block (Flex)

```python
mag_block = protocol.load_module("magneticBlockV1", "D1")
mag_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", "C2")

# Move plate to magnetic block for bead separation
protocol.move_labware(mag_plate, mag_block, use_gripper=True)

# Wait for beads to collect
protocol.delay(minutes=3)

# Pipette supernatant (beads held by magnets)
pipette.transfer(150, mag_plate.wells(), waste.wells())

# Move plate off magnets for resuspension
protocol.move_labware(mag_plate, "C2", use_gripper=True)
```

### Absorbance Plate Reader

**Critical:** Reader lid must be open before gripper operations

```python
reader = protocol.load_module("absorbanceReaderV1", "D3")
assay_plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "C2")

# Initialize reader
reader.close_lid()
reader.initialize(mode="single", wavelengths=[450])

# Open lid BEFORE moving plate to reader
reader.open_lid()

# Move plate to reader
protocol.move_labware(assay_plate, reader, use_gripper=True)

# Close lid and read
reader.close_lid()
data = reader.read()

# Open lid BEFORE removing plate
reader.open_lid()

# Move plate off reader
protocol.move_labware(assay_plate, "C2", use_gripper=True)
```

## Common Patterns

### Multi-Module Workflow

```python
# DNA extraction with module transfers
sample_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", "C1")
hs_mod = protocol.load_module("heaterShakerModuleV1", "D1")
mag_block = protocol.load_module("magneticBlockV1", "D2")
temp_mod = protocol.load_module("temperature module gen2", "D3")

# 1. Lysis on heater-shaker
hs_mod.open_labware_latch()
protocol.move_labware(sample_plate, hs_mod, use_gripper=True)
hs_mod.close_labware_latch()
hs_mod.set_and_wait_for_temperature(56)
hs_mod.set_and_wait_for_shake_speed(1000)
protocol.delay(minutes=15)
hs_mod.deactivate_shaker()
hs_mod.deactivate_heater()
hs_mod.open_labware_latch()

# 2. Bead binding on magnetic block
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
protocol.delay(minutes=3)
pipette.transfer(150, sample_plate.wells(), waste.wells())

# 3. Elution on temperature module (cold)
protocol.move_labware(sample_plate, temp_mod, use_gripper=True)
temp_mod.set_temperature(4)
pipette.transfer(50, elution_buffer, sample_plate.wells())

# 4. Return to deck
protocol.move_labware(sample_plate, "C1", use_gripper=True)
temp_mod.deactivate()
```

### Plate Stacking Workflow

```python
# Process multiple plates sequentially
plates = [
    protocol.load_labware("corning_96_wellplate_360ul_flat", "C1"),
    protocol.load_labware("corning_96_wellplate_360ul_flat", "C2"),
    protocol.load_labware("corning_96_wellplate_360ul_flat", "C3")
]

reader = protocol.load_module("absorbanceReaderV1", "D3")
reader.close_lid()
reader.initialize(mode="single", wavelengths=[600])
reader.open_lid()

for i, plate in enumerate(plates):
    # Read each plate
    protocol.move_labware(plate, reader, use_gripper=True)
    reader.close_lid()
    data = reader.read(export_filename=f"plate_{i+1}_od600")
    reader.open_lid()

    # Move to off-deck storage
    protocol.move_labware(plate, OFF_DECK, use_gripper=True)
```

### Waste Management

```python
# Dispose of used consumables
waste_chute = protocol.load_waste_chute()

# After using tip rack
protocol.move_labware(empty_tips, waste_chute, use_gripper=True)

# After processing sample plate
protocol.move_labware(used_plate, waste_chute, use_gripper=True)
```

### Dynamic Deck Space Management

```python
# Free up deck space by moving inactive labware off-deck
storage = OFF_DECK

# Initial setup - plates start on deck
plate_1 = protocol.load_labware("corning_96_wellplate_360ul_flat", "B1")
plate_2 = protocol.load_labware("corning_96_wellplate_360ul_flat", "B2")
plate_3 = protocol.load_labware("corning_96_wellplate_360ul_flat", "B3")

# Process plate 1
# ... operations on plate_1 ...

# Move plate 1 off-deck to free space
protocol.move_labware(plate_1, storage, use_gripper=True)

# Process plate 2
# ... operations on plate_2 ...

# Retrieve plate 1 when needed again
protocol.move_labware(plate_1, "B1", use_gripper=True)
```

## Grippable Labware

**The gripper can only move labware with compatible geometry.**

### Compatible Features

Labware must have one of:
- **Gripper-compatible rim** - Extended lip or ridge for gripper jaws
- **Side grips** - Indentations or features on sides
- **Opentrons-certified labware** - Verified gripper compatibility

### Checking Compatibility

Most Opentrons labware and major brands (Corning, NEST, Axygen, Bio-Rad) are gripper-compatible. Check labware definition or test before protocol deployment.

### Non-Grippable Labware

Examples of labware that may NOT be grippable:
- Very small tubes or vials without grip features
- Irregularly shaped containers
- Custom labware without gripper considerations
- Delicate or fragile items

**Solution:** Use `use_gripper=False` to prompt manual movement, or use adapters.

## Best Practices

1. **Open module lids/latches before gripper movement** - Required for Heater-Shaker, Thermocycler, Absorbance Reader
2. **Use descriptive variable names** - Track labware clearly through movements
3. **Test with simulation first** - Verify gripper movements before running on hardware
4. **Add protocol comments** - Document why labware is being moved
5. **Plan deck layout** - Minimize unnecessary movements, optimize for efficiency
6. **Use OFF_DECK strategically** - Free up deck space for complex protocols
7. **Check labware compatibility** - Ensure labware is grippable before deploying
8. **Use offsets judiciously** - Only when necessary for proper positioning
9. **Consider manual fallback** - Have `use_gripper=False` backup for troubleshooting
10. **Dispose properly** - Use waste chute for used consumables to maintain workspace

## Common Mistakes

**❌ Moving to Heater-Shaker with closed latch:**
```python
protocol.move_labware(plate, hs_mod, use_gripper=True)  # Error: latch closed
```

**✅ Correct:**
```python
hs_mod.open_labware_latch()
protocol.move_labware(plate, hs_mod, use_gripper=True)
```

**❌ Moving to Thermocycler with closed lid:**
```python
protocol.move_labware(plate, tc_mod, use_gripper=True)  # Error: lid closed
```

**✅ Correct:**
```python
tc_mod.open_lid()
protocol.move_labware(plate, tc_mod, use_gripper=True)
```

**❌ Moving non-grippable labware:**
```python
# Custom labware without gripper features
protocol.move_labware(custom_tubes, "D2", use_gripper=True)  # Error: cannot grip
```

**✅ Correct:**
```python
# Use manual movement for non-grippable labware
protocol.move_labware(custom_tubes, "D2", use_gripper=False)
```

**❌ Forgetting to specify use_gripper:**
```python
protocol.move_labware(plate, "D2")  # Defaults to use_gripper=False, pauses protocol
```

**✅ Correct:**
```python
protocol.move_labware(plate, "D2", use_gripper=True)  # Explicit gripper use
```

**❌ Moving to occupied location:**
```python
plate_1 = protocol.load_labware("corning_96_wellplate_360ul_flat", "C1")
plate_2 = protocol.load_labware("corning_96_wellplate_360ul_flat", "C2")
protocol.move_labware(plate_1, "C2", use_gripper=True)  # Error: C2 occupied by plate_2
```

**✅ Correct:**
```python
# Move plate_2 first, then plate_1
protocol.move_labware(plate_2, OFF_DECK, use_gripper=True)
protocol.move_labware(plate_1, "C2", use_gripper=True)
```

## Troubleshooting

**Gripper cannot grip labware:**
- Verify labware has gripper-compatible features
- Check labware is properly seated on deck/module
- Try adjusting pick_up_offset (increase z)
- Use `use_gripper=False` for non-compatible labware

**Gripper collision errors:**
- Ensure module lids are open (Thermocycler, Absorbance Reader)
- Verify Heater-Shaker latch is open
- Check deck layout for obstructions
- Confirm destination location is clear

**Labware not properly seated after movement:**
- Adjust drop_offset to ensure proper placement
- Check module/adapter compatibility with labware
- Verify destination surface is level and clear

**Protocol pauses unexpectedly:**
- Check that `use_gripper=True` is specified
- Verify gripper is enabled for protocol
- Ensure labware is grippable

**OFF_DECK movement errors:**
- Import OFF_DECK constant: `from opentrons.protocol_api import OFF_DECK`
- Track labware location - cannot move from OFF_DECK if not there
- Ensure sufficient off-deck storage slots

## Advanced Techniques

### Conditional Gripper Use

```python
# Use gripper for standard labware, manual for custom
def move_smart(protocol, labware, destination, is_grippable=True):
    if is_grippable:
        protocol.move_labware(labware, destination, use_gripper=True)
    else:
        protocol.comment(f"Please manually move {labware} to {destination}")
        protocol.move_labware(labware, destination, use_gripper=False)

move_smart(protocol, standard_plate, "D2", is_grippable=True)
move_smart(protocol, custom_tubes, "D3", is_grippable=False)
```

### Offset Calibration Helper

```python
# Test offsets to find optimal values
def test_gripper_offset(protocol, labware, destination, z_offset_range):
    for z in z_offset_range:
        protocol.comment(f"Testing pickup offset z={z}")
        protocol.move_labware(
            labware,
            destination,
            use_gripper=True,
            pick_up_offset={"x": 0, "y": 0, "z": z}
        )
        protocol.pause("Check if pickup was successful. Resume to continue.")
        # Move back
        protocol.move_labware(labware, "C1", use_gripper=True)

# Run test
test_gripper_offset(protocol, test_plate, "D2", z_offset_range=[0, 1, 2, 3])
```

### Plate Carousel Pattern

```python
# Rotate plates through processing stations
def process_plate_carousel(protocol, plates, processing_station):
    """Process multiple plates through single module."""
    for i, plate in enumerate(plates):
        protocol.comment(f"Processing plate {i+1}/{len(plates)}")

        # Move to processing station
        protocol.move_labware(plate, processing_station, use_gripper=True)

        # Process (example: read absorbance)
        # ... processing steps ...

        # Move to archive
        protocol.move_labware(plate, OFF_DECK, use_gripper=True)

process_plate_carousel(protocol, [plate1, plate2, plate3], reader_module)
```

## Deck Layout Planning

**Tips for efficient gripper workflows:**

1. **Keep high-traffic locations accessible** - Place frequently moved labware in central deck positions
2. **Group modules logically** - Arrange modules in workflow order to minimize travel distance
3. **Reserve column 4 for Absorbance Reader** - If using reader, entire column 4 is staging area
4. **Use OFF_DECK for storage** - Free up deck space for active labware
5. **Plan waste chute access** - Ensure gripper can reach waste chute without obstacles

**Example efficient layout:**
```
     1          2          3          4
A  [Plates]  [Module1]  [Reader]  [Reserved]
B  [Plates]  [Module2]  [Reader]  [Reserved]
C  [Tips]    [Reagent]  [Reader]  [Reserved]
D  [Tips]    [Waste]    [Reader]  [Reserved]
```

## Integration with Staging Area Slots

Flex staging area slots (column 4: A4, B4, C4, D4) are used for:
- Absorbance Reader lid storage (automatic)
- Temporary labware holding
- Gripper intermediate positions

**Important:** When Absorbance Reader is loaded, column 4 cannot be used for labware.

## API Version Requirements

- **Minimum API version:** 2.15 (gripper support introduced)
- **Recommended:** 2.19+ for full feature support
- **Robot type:** Must be Opentrons Flex

## Additional Resources

- **Gripper Documentation:** https://docs.opentrons.com/v2/new_protocol_api.html#protocol_api.ProtocolContext.move_labware
- **Labware Library:** https://labware.opentrons.com/ (check gripper compatibility)
- **Opentrons Support:** https://support.opentrons.com/

## Related Skills

- `opentrons` - Main Opentrons Python API skill
- `opentrons-heater-shaker` - Heater-Shaker Module (requires gripper integration)
- `opentrons-absorbance-reader` - Absorbance Plate Reader (requires gripper)
- `opentrons-magnetic-block` - Magnetic Block (designed for gripper workflow)
- `opentrons-thermocycler` - Thermocycler Module (gripper-compatible)
- `opentrons-temperature-module` - Temperature Module (gripper-compatible)
