---
name: opentrons-temperature-module
description: Opentrons Temperature Module - precise heating and cooling (4-95°C) for sample storage, enzyme reactions, and temperature-sensitive protocols with aluminum block adapters for plates, tubes, and PCR strips
allowed-tools: ["*"]
---

# Opentrons Temperature Module

## Overview

The **Opentrons Temperature Module** provides precise temperature control (4-95°C) for maintaining samples at specific temperatures during automated protocols. Ideal for keeping reagents cold, pre-warming reaction components, temperature-sensitive incubations, and any workflow requiring stable thermal conditions without mixing.

**Core value:** Eliminate ice buckets and water baths. Maintain precise, reproducible temperatures on-deck for reagents, samples, and reaction components throughout your protocol.

## When to Use

Use the Temperature Module skill when:
- Keeping reagents cold during protocol (e.g., enzymes at 4°C)
- Pre-warming reaction components (e.g., buffers at 37°C)
- Maintaining samples at specific temperatures
- Temperature-sensitive enzyme reactions without mixing
- Cooling samples after thermal processing
- Any protocol requiring stable temperature control (4-95°C)

**Don't use when:**
- Need mixing/shaking during temperature control (use Heater-Shaker Module)
- Require PCR thermal cycling (use Thermocycler Module)
- Temperature outside 4-95°C range
- Precise temperature ramping or cycling needed

## Quick Reference

| Operation | Method | Key Parameters |
|-----------|--------|----------------|
| Load module | `protocol.load_module()` | `"temperature module gen2"`, location |
| Set temperature | `set_temperature()` | celsius (4-95) |
| Get current temperature | `.temperature` | Read-only property |
| Check status | `.status` | Returns "holding at target" or "idle" |
| Deactivate | `deactivate()` | - |

## Platform Compatibility

**Both Opentrons Flex and OT-2**

### Module Generations
- **GEN1** - Original temperature module
- **GEN2** - Improved cooling performance, better isolation (recommended)

**Key GEN2 improvements:**
- Plastic insulation around plate
- Shrouds for aluminum blocks
- Better cooling when sharing deck with running Thermocycler
- Same API as GEN1

## Loading the Module

```python
from opentrons import protocol_api

metadata = {'apiLevel': '2.19'}

def run(protocol: protocol_api.ProtocolContext):
    # Load Temperature Module GEN2
    temp_mod = protocol.load_module("temperature module gen2", "D1")  # Flex
    # temp_mod = protocol.load_module("temperature module gen2", "4")  # OT-2

    # Load labware on module
    cold_plate = temp_mod.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul")
```

**Module versions:**
- `"temperature module gen2"` - GEN2 (recommended)
- `"temperatureModuleV1"` - GEN1 (legacy)

**Deck slot:** Any compatible slot (Flex: A1-D3, OT-2: 1-11)

## Loading Labware

### Standalone Adapters (API 2.15+)

**Recommended approach** - Load adapter first, then labware:

```python
# 96-well aluminum block
temp_block = temp_mod.load_adapter("opentrons_96_well_aluminum_block")
sample_plate = temp_block.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt")
```

**Available adapters:**

| Adapter Name | Compatible Labware |
|--------------|-------------------|
| `opentrons_96_well_aluminum_block` | 96-well plates, PCR plates |
| `opentrons_aluminum_flat_bottom_plate` | Flat-bottom plates |
| `opentrons_96_deep_well_temp_mod_adapter` | Deep-well plates |

### Block-and-Tube Combinations

For tube racks with aluminum blocks:

```python
# 24-well block with various tube types
tubes_nest = temp_mod.load_labware("opentrons_24_aluminumblock_nest_1.5ml_snapcap")
tubes_generic = temp_mod.load_labware("opentrons_24_aluminumblock_generic_2ml_screwcap")
```

### Legacy Block-and-Plate Combinations

```python
# Pre-configured combinations (older API versions)
plate_combo = temp_mod.load_labware("opentrons_96_aluminumblock_biorad_wellplate_200ul")
```

**Recommendation:** Use standalone adapters (API 2.15+) for better flexibility.

## Temperature Control

### Setting Temperature

```python
# Set temperature and wait until reached
temp_mod.set_temperature(celsius=4)

# Protocol waits here until 4°C is reached

# Perform operations at target temperature
pipette.transfer(100, cold_reagent, dest_plate.wells())
```

**Temperature range:** 4-95°C (1°C resolution)

**Behavior:** Protocol execution **blocks** (waits) until target temperature is reached.

### Temperature Status

```python
# Get current temperature
current_temp = temp_mod.temperature
protocol.comment(f"Module at {current_temp}°C")

# Check status
status = temp_mod.status
# Returns: "holding at target" or "idle"

if status == "holding at target":
    protocol.comment("Temperature stable, proceeding")
```

### Deactivating

```python
# Turn off temperature control
temp_mod.deactivate()
```

**Important:** Module does **not** automatically deactivate at protocol end. Must be manually turned off via Opentrons App if protocol completes or is cancelled.

## Common Patterns

### Keeping Reagents Cold

```python
# Keep enzymes and master mix cold throughout protocol
temp_mod = protocol.load_module("temperature module gen2", "D1")
reagent_block = temp_mod.load_adapter("opentrons_24_aluminumblock_nest_1.5ml_snapcap")

# Set to 4°C before starting
temp_mod.set_temperature(4)

# Reagents stay cold during entire protocol
pipette.transfer(10, reagent_block["A1"], dest_plate.wells())
# ... rest of protocol ...

# Turn off at end
temp_mod.deactivate()
```

### Pre-Warming Reaction Components

```python
# Pre-warm buffer to 37°C
temp_mod = protocol.load_module("temperature module gen2", "C2")
warm_block = temp_mod.load_adapter("opentrons_96_well_aluminum_block")
warm_plate = warm_block.load_labware("corning_96_wellplate_360ul_flat")

# Set to reaction temperature
temp_mod.set_temperature(37)

# Use pre-warmed components
pipette.transfer(50, warm_plate["A1"], reaction_plate.wells())

temp_mod.deactivate()
```

### Cooling After Thermal Processing

```python
# Cool samples after PCR or heat inactivation
temp_mod = protocol.load_module("temperature module gen2", "D3")
cooling_block = temp_mod.load_adapter("opentrons_96_well_aluminum_block")

# Set to 4°C for cooling
temp_mod.set_temperature(4)

# Move hot samples to cooling block with gripper (Flex)
protocol.move_labware(hot_plate, temp_mod, use_gripper=True)

# Hold at 4°C
protocol.delay(minutes=5)

# Continue processing cooled samples
temp_mod.deactivate()
```

### Temperature-Sensitive Enzyme Reaction

```python
# Restriction digest at optimal temperature
temp_mod = protocol.load_module("temperature module gen2", "D1")
rxn_block = temp_mod.load_adapter("opentrons_96_well_aluminum_block")
rxn_plate = rxn_block.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt")

# Setup reaction
pipette.transfer(20, dna_samples, rxn_plate.wells()[:8])
pipette.transfer(5, enzyme_mix, rxn_plate.wells()[:8], mix_after=(3, 15))

# Incubate at optimal temperature
temp_mod.set_temperature(37)
protocol.delay(hours=2)

# Heat inactivation
temp_mod.set_temperature(65)
protocol.delay(minutes=20)

# Cool for downstream processing
temp_mod.set_temperature(4)

temp_mod.deactivate()
```

### Maintaining Temperature During Multi-Step Protocol

```python
# Keep samples at 4°C except during specific steps
cold_storage = protocol.load_module("temperature module gen2", "D1")
cold_block = cold_storage.load_adapter("opentrons_96_well_aluminum_block")
sample_plate = cold_block.load_labware("biorad_96_wellplate_200ul_pcr")

# Set to 4°C at start
cold_storage.set_temperature(4)

# Samples stay cold on module
# Move to room temp for specific operations
protocol.move_labware(sample_plate, "C2", use_gripper=True)

# ... perform room-temp operations ...

# Return to cold storage
protocol.move_labware(sample_plate, cold_storage, use_gripper=True)

cold_storage.deactivate()
```

## Integration with Other Modules

### With Thermocycler

```python
# Pre-cool samples before PCR
temp_mod = protocol.load_module("temperature module gen2", "D1")
tc_mod = protocol.load_module("thermocyclerModuleV2")

cold_block = temp_mod.load_adapter("opentrons_96_well_aluminum_block")
sample_plate = cold_block.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt")

# Keep samples cold
temp_mod.set_temperature(4)

# Setup PCR mix (samples stay cold)
# ... pipetting ...

# Transfer to thermocycler
tc_mod.open_lid()
protocol.move_labware(sample_plate, tc_mod, use_gripper=True)

# Run PCR
tc_mod.close_lid()
# ... thermal cycling ...

# Return to cold storage after PCR
tc_mod.open_lid()
protocol.move_labware(sample_plate, temp_mod, use_gripper=True)

temp_mod.deactivate()
```

### With Heater-Shaker

```python
# Cool after shaking/heating
hs_mod = protocol.load_module("heaterShakerModuleV1", "D1")
temp_mod = protocol.load_module("temperature module gen2", "D2")

# Pre-cool temperature module
temp_mod.set_temperature(4)

# Heat/shake on heater-shaker
hs_mod.set_and_wait_for_temperature(65)
hs_mod.close_labware_latch()
hs_mod.set_and_wait_for_shake_speed(1000)
protocol.delay(minutes=10)
hs_mod.deactivate_shaker()
hs_mod.deactivate_heater()
hs_mod.open_labware_latch()

# Transfer to temperature module for cooling
protocol.move_labware(reaction_plate, temp_mod, use_gripper=True)
protocol.delay(minutes=3)

temp_mod.deactivate()
```

### With Magnetic Block

```python
# Temperature-controlled magnetic separation
mag_block = protocol.load_module("magneticBlockV1", "D1")
temp_mod = protocol.load_module("temperature module gen2", "D2")

# Cool elution buffer
temp_mod.set_temperature(4)

# Magnetic separation
protocol.move_labware(sample_plate, mag_block, use_gripper=True)
protocol.delay(minutes=3)
pipette.transfer(150, sample_plate.wells(), waste.wells())

# Elute with cold buffer
protocol.move_labware(sample_plate, temp_mod, use_gripper=True)
pipette.transfer(50, cold_buffer, sample_plate.wells())

temp_mod.deactivate()
```

## Best Practices

1. **Set temperature before loading samples** - Allow module to stabilize
2. **Deactivate at protocol end** - Prevent equipment running indefinitely
3. **Use GEN2 for better performance** - Improved cooling and isolation
4. **Plan for thermal equilibration** - Large temperature changes take time
5. **Monitor ambient temperature** - Affects minimum achievable temperature (4°C target requires cool room)
6. **Use aluminum blocks** - Better thermal contact than direct plate placement
7. **Avoid pipetting during temperature changes** - Wait for "holding at target" status
8. **Consider thermal mass** - More liquid = slower temperature equilibration
9. **Don't rely on auto-deactivation** - Module stays on after protocol ends
10. **Check compatibility** - Verify labware fits adapter/block

## Common Mistakes

**❌ Pipetting during temperature change:**
```python
temp_mod.set_temperature(4)
# set_temperature() blocks until reached, but safer to check status
pipette.transfer(...)  # Risk if not fully stabilized
```

**✅ Correct:**
```python
temp_mod.set_temperature(4)
# Wait for status confirmation
if temp_mod.status == "holding at target":
    pipette.transfer(...)
```

**❌ Not deactivating module:**
```python
temp_mod.set_temperature(4)
# ... protocol ends ...
# Module stays at 4°C indefinitely!
```

**✅ Correct:**
```python
temp_mod.set_temperature(4)
# ... operations ...
temp_mod.deactivate()
```

**❌ Temperature out of range:**
```python
temp_mod.set_temperature(100)  # Error: max is 95°C
temp_mod.set_temperature(0)    # Error: min is 4°C
```

**✅ Correct:**
```python
temp_mod.set_temperature(95)  # Within range
temp_mod.set_temperature(4)   # Within range
```

**❌ Loading labware before temperature stabilizes:**
```python
temp_mod.set_temperature(4)
# Temperature not yet reached - samples warm during cooling
pipette.transfer(100, warm_samples, temp_block.wells())
```

**✅ Correct:**
```python
# Set temperature BEFORE loading samples
temp_mod.set_temperature(4)
# Now at 4°C, samples stay cold
pipette.transfer(100, warm_samples, temp_block.wells())
```

## Troubleshooting

**Module not reaching 4°C:**
- Check ambient room temperature (module can't cool below ambient by much)
- Ensure adequate airflow around module
- Verify module is on flat, level surface
- Consider using ice packs as supplement for very cold requirements

**Module not reaching high temperatures:**
- Verify temperature is ≤95°C
- Check module is not in cold environment
- Allow sufficient time for large thermal mass

**Temperature not stable:**
- Wait for status to show "holding at target"
- Avoid high-airflow environments
- Ensure good thermal contact between labware and block
- Use appropriate adapter for labware type

**Slow temperature changes:**
- Normal for large temperature differences
- Use smaller labware/tubes for faster equilibration
- Pre-cool/pre-warm module before critical steps
- Consider thermal mass of samples

**Module stays on after protocol:**
- This is expected behavior
- Manually deactivate via Opentrons App
- Or add `deactivate()` to protocol end

## Temperature Limits

| Parameter | Minimum | Maximum | Resolution |
|-----------|---------|---------|------------|
| Block temperature | 4°C | 95°C | 1°C |
| Cooling capacity | ~4°C below ambient | - | - |
| Heating capacity | - | 95°C | - |

**Note:** Actual minimum temperature depends on ambient conditions. In warm room (>25°C), reaching 4°C may be difficult.

## Advanced Techniques

### Temperature Gradient Protocol

```python
# Ramp temperature for optimization
temp_mod = protocol.load_module("temperature module gen2", "D1")

for temp in [4, 20, 37, 55, 70]:
    temp_mod.set_temperature(temp)
    protocol.comment(f"Now at {temp}°C")

    # Perform operations at each temperature
    # ... sampling, measurements, etc. ...

    protocol.delay(minutes=5)

temp_mod.deactivate()
```

### Dual Temperature Setup

```python
# Maintain two different temperatures simultaneously
cold_mod = protocol.load_module("temperature module gen2", "D1")
warm_mod = protocol.load_module("temperature module gen2", "D2")

cold_mod.set_temperature(4)
warm_mod.set_temperature(37)

# Use both temperature zones in protocol
pipette.transfer(10, cold_mod.labware["A1"], reaction_plate.wells())
pipette.transfer(50, warm_mod.labware["A1"], reaction_plate.wells())

cold_mod.deactivate()
warm_mod.deactivate()
```

### Temperature Shock Protocol

```python
# Quick temperature changes for cell work
temp_mod = protocol.load_module("temperature module gen2", "D1")
cell_plate = temp_mod.load_labware("corning_96_wellplate_360ul_flat")

# Ice incubation
temp_mod.set_temperature(4)
protocol.delay(minutes=20)

# Heat shock
temp_mod.set_temperature(42)
protocol.delay(seconds=45)

# Recovery
temp_mod.set_temperature(37)
protocol.delay(minutes=5)

temp_mod.deactivate()
```

## GEN2 vs GEN1

| Feature | GEN1 | GEN2 |
|---------|------|------|
| Temperature range | 4-95°C | 4-95°C |
| Cooling | Basic | Improved with insulation |
| Thermocycler compatibility | Poor cooling | Good cooling |
| Plate insulation | None | Plastic shroud |
| Block shrouds | No | Yes |
| API | Same | Same |
| Recommended | No | Yes |

**Recommendation:** Use GEN2 for all new protocols.

## API Version Requirements

- **Minimum API version:** 2.0 (temperature module support)
- **Standalone adapters:** API 2.15+
- **Recommended:** 2.19+ for full feature support

## Additional Resources

- **Temperature Module Documentation:** https://docs.opentrons.com/v2/modules/temperature_module.html
- **Labware Library:** https://labware.opentrons.com/
- **Opentrons Support:** https://support.opentrons.com/

## Related Skills

- `opentrons` - Main Opentrons Python API skill
- `opentrons-heater-shaker` - Temperature control with mixing (37-95°C)
- `opentrons-thermocycler` - PCR thermal cycling (4-99°C block)
- `opentrons-gripper` - Automated labware movement (Flex)
- `opentrons-magnetic-block` - Magnetic bead separation
