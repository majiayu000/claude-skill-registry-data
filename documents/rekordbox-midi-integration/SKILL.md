---
name: rekordbox-midi-integration
description: Specialist in Rekordbox MIDI Learn integration, including MIDI mapping workflow, CSV file format, Rekordbox function reference, official documentation, and real-world DDJ controller examples. Use when working on Rekordbox MIDI controllers, CSV generation/import/export, function mapping, or debugging Rekordbox MIDI integration.
---

# Rekordbox MIDI Integration Expert

Master Rekordbox MIDI Learn integration for creating compatible controller mappings. This skill provides comprehensive knowledge of Rekordbox's MIDI system, official documentation, CSV structure, complete function reference, MIDI code formats, and real-world examples from Pioneer DDJ controllers.

## When to Use This Skill

- Understanding Rekordbox MIDI Learn workflow and features
- Generating Rekordbox-compatible CSV files
- Mapping MIDI controllers to Rekordbox functions
- Parsing or validating CSV structure
- Looking up Rekordbox function names and categories
- Debugging CSV import/export issues
- Understanding MIDI code hex format
- Implementing deck assignments
- Working with control types and options
- Referencing official Rekordbox documentation
- Learning from real-world DDJ controller mappings
- Reviewing MIDI-related code changes

## Rekordbox MIDI Learn System Overview

### What is MIDI Learn?

Rekordbox MIDI Learn (available in version 4.0.6+) enables free assignment of rekordbox dj (Performance mode) features to MIDI controllable equipment. You can assign functions like Play/Pause, Hot Cue, loops, effects, and browser controls to physical buttons, knobs, faders, and encoders on MIDI controllers.

**Key features:**
- Assign any Rekordbox function to any MIDI control
- Modify preset mappings for supported controllers
- Create custom mappings for unsupported hardware
- Export/import CSV mapping files
- LED feedback support for compatible hardware

### MIDI Learn Workflow

1. **Connection**: Connect MIDI controller via USB to computer
2. **Launch**: Open rekordbox in PERFORMANCE mode
3. **MIDI Settings**: Click MIDI button (upper right, next to Preferences)
4. **Device Selection**: Select connected device from dropdown
5. **Function Assignment**:
   - Click [ADD] to add function from category tabs
   - Click function row, then [LEARN] button
   - Operate physical control (button/knob) on hardware
   - MIDI code automatically captured in [MIDI IN] column
6. **Testing**: Test control sends correct MIDI and triggers function
7. **Export**: Click [EXPORT] to save CSV mapping file

### MIDI Setting Window Components

**Menu bar:**
- Device selector dropdown
- [DEFAULT] - Reset to factory settings
- [LEARN] - Enable MIDI learn mode
- [ADD] - Add function from category
- [DUPLICATE] - Copy function to other decks
- [DELETE] - Remove function
- [IMPORT] - Load CSV file
- [EXPORT] - Save CSV file

**Category tabs:**
- Deck (playback, tempo, loops)
- Mixer (faders, EQ, filter)
- Browser (track selection, load)
- FX (effects units, parameters)
- Sampler (sample pads, banks)

**MIDI setting columns:**
- Function: Rekordbox function name
- Deck: Deck assignment (1-4, or global)
- MIDI IN: 4-digit hex code received from hardware
- Type: Control type (Button, Knob, Rotary, etc.)
- MIDI OUT: 4-digit hex code sent for LED feedback
- Comment: User notes

## CSV File Format Specification

### File Structure

Rekordbox CSV files have a specific 15-column structure:

```
@file,1,ControllerName,,,,,,,,,,,,
#name,function,type,input,deck1,deck2,deck3,deck4,output,deck1,deck2,deck3,deck4,option,comment
```

### Column Definitions

| # | Column Name | Description | Example |
|---|-------------|-------------|---------|
| 0 | #name | Internal identifier (purpose unclear) | `PlayPause`, `#CrossFader` |
| 1 | function | **Rekordbox function to map** (key column) | `PlayPause`, `Browse+Press` |
| 2 | type | Control type | `Button`, `Rotary`, `KnobSliderHiRes` |
| 3 | input | MIDI IN code (4-digit hex) | `900B`, `B640` |
| 4-7 | deck1-4 | Input deck channel assignments | `0`, `1`, `2`, `3` |
| 8 | output | MIDI OUT code (4-digit hex) | `900B`, `B640` |
| 9-12 | deck1-4 | Output deck channel assignments | `0`, `1`, `2`, `3` |
| 13 | option | Optional flags (semicolon-separated) | `Fast;Priority=50`, `RO` |
| 14 | comment | Human description | `Play/Pause` |

**Note:** Column 1 (`function`) determines the actual mapping. If empty, the row has no functional mapping. See `REKORDBOX-MIDI-CSV-SPEC.md` for full specification.

### Special Rows

```csv
@file,1,DDJ-FLX4,,,,,,,,,,,,           # Metadata header
#name,function,type,input,deck1,...   # Column header
,,,,,,,,,,,,,,                          # Empty separator rows
# Browser,,,,,,,,,,,,,,                 # Section comment
```

## MIDI Code Format

### 4-Digit Hex Format

MIDI codes are represented as **4-digit hexadecimal** strings:

```
[Status Byte][Data Byte]
    ↓           ↓
   90          3C
```

### Status Byte Breakdown

```
Status Byte = Command Nibble + Channel Nibble

Example: 0x90 = Note On (0x9x) + Channel 1 (0x0)
Example: 0xB6 = Control Change (0xBx) + Channel 7 (0x6)
```

### Common MIDI Commands

| Hex | Command | Usage |
|-----|---------|-------|
| `9x` | Note On | Buttons, Pads |
| `8x` | Note Off | Button release |
| `Bx` | Control Change (CC) | Knobs, Faders, Encoders |

### Channel Encoding (0-indexed)

| Deck | CSV Value | MIDI Channel | Hex Nibble |
|------|-----------|--------------|------------|
| Deck 1 | `0` | Ch 1 | `x0` |
| Deck 2 | `1` | Ch 2 | `x1` |
| Deck 3 | `2` | Ch 3 | `x2` |
| Deck 4 | `3` | Ch 4 | `x3` |
| Global | `6` | Ch 7 | `x6` |

**Note:** Rekordbox uses 0-indexed channels internally (0-15), but MIDI convention displays them as 1-16.

### MIDI Code Examples

```csv
# Button (Note On, Ch 1, Note 0x0B)
900B    → Status: 0x90 (Note On, Ch 0), Data: 0x0B (note 11)

# Knob (CC, Ch 7, CC 0x40)
B640    → Status: 0xB6 (CC, Ch 6), Data: 0x40 (CC 64)

# Rotary (CC, Ch 1, CC 0x00)
B000    → Status: 0xB0 (CC, Ch 0), Data: 0x00 (CC 0)
```

## Control Types

### Button and Pad Types

| Type | Description | MIDI Message | Use Case |
|------|-------------|--------------|----------|
| `Button` | Standard button | Note On/Off | Play, Cue, Hot Cue |
| `Pad` | Velocity-sensitive pad | Note On (with velocity) | Performance pads |

### Knob and Slider Types

| Type | Description | Resolution | Range |
|------|-------------|------------|-------|
| `Knob` | Standard knob | 7-bit | 0-127 (0x00-0x7F) |
| `KnobSlider` | Standard fader | 7-bit | 0-127 (0x00-0x7F) |
| `KnobSliderHiRes` | High-resolution fader | 14-bit | 0-16383 (0x0000-0x3FFF) |

### Encoder Types

| Type | Description | Behavior |
|------|-------------|----------|
| `Rotary` | Rotary encoder | Relative values (64=center, >64=CW, <64=CCW) |
| `JogRotate` | Jog wheel rotation | Continuous rotation |
| `JogTouch` | Jog wheel touch | Touch detection |
| `Difference` | Position difference | Search/seek |

### Special Types

| Type | Description | Use Case |
|------|-------------|----------|
| `Indicator` | Output only (no input) | LED feedback |
| `Value` | Special value input | Needle Search, Velocity Sampler |

## Rekordbox Function Reference

### Deck Functions

**Playback Control:**
- `PlayPause` - Play/Pause toggle
- `Cue` - Cue point set/play
- `JumpToTrackStart` - Return to start
- `Sync` - Beat sync on/off
- `Master` - Master tempo control

**Loop Control:**
- `LoopIn` - Set loop in point
- `LoopOut` - Set loop out point
- `ActiveLoop` - Enable/disable active loop
- `4BeatLoop`, `8BeatLoop`, `16BeatLoop` - Auto-loop sizes
- `LoopHalf` - Halve loop size
- `LoopDouble` - Double loop size

**Hot Cues:**
- `HotCue1` through `HotCue8` - Hot cue points
- `PAD1_HotCue` through `PAD8_HotCue` - Performance pad hot cues

**Tempo Control:**
- `TempoSlider` - Tempo fader
- `TempoRange` - Tempo range selector
- `BeatJump` - Beat jump forward/backward

### Jog/Scratch Functions

- `JogScratch` - Scratch mode
- `JogPitchBend` - Pitch bend mode
- `JogSearch` - Track search
- `JogTouch` - Touch detection
- `WheelPitchBend` - Outer wheel pitch bend

### Mixer Functions

- `CrossFader` - Crossfader
- `ChannelFader` - Channel volume fader
- `Gain` - Channel gain
- `HighEQ`, `MidEQ`, `LowEQ` - 3-band EQ
- `FilterKnob` - Filter control

### Browser Functions

- `Browse` - Track/folder selection
- `Load` - Load track to deck
- `Forward` - Open folder
- `Back` - Close folder
- `RelatedTracks` - Related tracks view
- `SwitchActiveWindow` - Toggle browse view

### FX Functions

- `FX1`, `FX2`, `FX3` - FX units
- `FXSelect` - FX type selector
- `FXKnob1`, `FXKnob2`, `FXKnob3` - FX parameters
- `BeatFX` - Beat FX toggle

## CSV Options Field

### Option Flags

Options are semicolon-separated flags in column 13:

```csv
# Examples
Fast;Priority=50
Blink=600
RO
Fast;Blink
```

### Common Options

| Option | Description | Use Case |
|--------|-------------|----------|
| `Fast` | High-priority processing | Time-critical controls (tempo, play) |
| `Priority=N` | Priority level (0-100) | Control processing order |
| `Blink=N` | Blink rate in milliseconds | LED feedback blink speed |
| `RO` | Read-Only (output only) | Indicator LEDs, feedback |

## Deck Assignment Patterns

### Per-Deck Assignment

Each function can be assigned to specific decks:

```csv
# Deck 1 and 2 only
PlayPause,PlayPause,Button,900B,0,1,,,900B,0,1,,,Fast,Play/Pause
                           ↑   ↑ ↑
                           |   | Deck 2: Ch 2 (0x1)
                           |   Deck 1: Ch 1 (0x0)
                           Input MIDI code
```

### Global Functions

Global functions use channel 6 (Ch 7):

```csv
# Browser (not deck-specific)
Browse,Browse,Rotary,B640,,,,,,,,,,,Browse Track Select
                      ↑
                      Ch 7 (global)
```

### Empty Deck Slots

Empty slots indicate the function doesn't apply to that deck:

```csv
Load,Load,Button,,9646,9647,,,,,,,,,Load to Deck
              ↑
              Empty = no deck 1 assignment
```

## Parsing Strategy

### Header Detection

```python
# Skip metadata
if row[0].startswith('@'):
    continue

# Skip column headers
if row[0].lower() == '#name':
    continue

# Skip empty rows
if not row or not row[0].strip():
    continue

# Skip comment rows
if row[0].startswith('#'):
    continue
```

### MIDI Code Parsing

```python
def parse_midi_code(code: str) -> tuple:
    """
    Parse 4-digit hex MIDI code

    Args:
        code: 4-digit hex string (e.g., '900B')

    Returns:
        (status_byte, data_byte, message_type, channel, note_or_cc)
    """
    if not code or len(code) != 4:
        return None

    status = int(code[:2], 16)  # First 2 digits
    data = int(code[2:], 16)    # Last 2 digits

    command = (status & 0xF0) >> 4  # Upper nibble
    channel = status & 0x0F          # Lower nibble

    # Determine message type
    if command == 0x9:
        msg_type = 'note_on'
    elif command == 0x8:
        msg_type = 'note_off'
    elif command == 0xB:
        msg_type = 'control_change'
    else:
        msg_type = 'unknown'

    return (status, data, msg_type, channel, data)
```

### Deck Channel Extraction

```python
def extract_deck_channels(row) -> list:
    """Extract input deck channel assignments from CSV row"""
    channels = []
    for i in range(4, 8):  # Columns 4-7
        if i < len(row) and row[i].strip():
            try:
                channels.append(int(row[i]))
            except ValueError:
                channels.append(None)
        else:
            channels.append(None)
    return channels
```

## Common Patterns

### Standard Button Mapping

```csv
PlayPause,PlayPause,Button,900B,0,1,,,900B,0,1,,,Fast;Priority=50,Play/Pause
```

- Function: `PlayPause`
- Type: `Button`
- Input: `900B` (Note On, Ch 1, Note 11)
- Decks: 1 (Ch 0) and 2 (Ch 1)
- Output: Same as input (LED feedback)
- Options: Fast processing, Priority 50

### Rotary Encoder Mapping

```csv
Browse,Browse,Rotary,B640,,,,,,,,,,,Browse Track/Folder
```

- Function: `Browse`
- Type: `Rotary`
- Input: `B640` (CC, Ch 7, CC 64)
- Decks: Global (no specific deck)
- Output: None (no LED feedback)

### High-Resolution Fader

```csv
TempoSlider,TempoSlider,KnobSliderHiRes,B000,0,1,,,,,,,,Fast,Tempo Control
```

- Function: `TempoSlider`
- Type: `KnobSliderHiRes` (14-bit resolution)
- Input: `B000` (CC, Ch 1, CC 0)
- Decks: 1 and 2
- Options: Fast processing

## Validation Rules

### Required Fields

1. **FunctionName** (column 0): Must not be empty
2. **Type** (column 2): Must be valid control type
3. **InputMIDI** (column 3): Must be 4-digit hex or empty for indicators
4. At least one deck assignment OR global assignment

### MIDI Code Validation

```python
def validate_midi_code(code: str) -> bool:
    """Validate 4-digit hex MIDI code"""
    if not code:
        return False
    if len(code) != 4:
        return False
    try:
        int(code, 16)  # Must be valid hex
        return True
    except ValueError:
        return False
```

### Control Type Validation

```python
VALID_TYPES = {
    'Button', 'Pad',
    'Knob', 'KnobSlider', 'KnobSliderHiRes',
    'Rotary', 'JogRotate', 'JogTouch', 'Difference',
    'Indicator', 'Value'
}

def validate_control_type(control_type: str) -> bool:
    return control_type in VALID_TYPES
```

## Generation Example

### Creating a New Mapping

```python
def generate_csv_row(
    function: str,
    display_name: str,
    control_type: str,
    input_midi: str,
    decks: list,
    output_midi: str = '',
    out_decks: list = None,
    options: str = '',
    comment: str = ''
) -> list:
    """Generate a CSV row for Rekordbox"""

    # Default output to input
    if not output_midi:
        output_midi = input_midi
    if out_decks is None:
        out_decks = decks

    # Pad deck lists to 4 elements
    while len(decks) < 4:
        decks.append('')
    while len(out_decks) < 4:
        out_decks.append('')

    row = [
        function,
        display_name,
        control_type,
        input_midi,
        *[str(d) if d != '' else '' for d in decks[:4]],
        output_midi,
        *[str(d) if d != '' else '' for d in out_decks[:4]],
        options,
        comment
    ]

    return row

# Example usage
row = generate_csv_row(
    function='PlayPause',
    display_name='Play/Pause',
    control_type='Button',
    input_midi='900B',
    decks=[0, 1],  # Deck 1 and 2
    options='Fast;Priority=50',
    comment='Play/Pause toggle'
)
```

## Testing CSV Files

### Import Test Procedure

1. Generate CSV file
2. Launch Rekordbox (Performance mode)
3. Click MIDI button (upper right)
4. Select controller from dropdown
5. Click IMPORT button
6. Select generated CSV file
7. Verify functions appear in MIDI setting list
8. Test physical controls send correct MIDI

### Common Import Errors

**"Invalid file format"**
- Missing @file header
- Missing #name header row
- Incorrect column count

**"MIDI code conflict"**
- Duplicate MIDI codes for different functions
- Same MIDI code assigned multiple times

**"Function not recognized"**
- Invalid function name
- Typo in function identifier

## Performance Considerations

### Fast Processing

Functions marked `Fast` are prioritized:
- Playback controls (Play, Cue)
- Tempo controls
- Time-critical operations

### Priority Levels

`Priority=N` (0-100) controls processing order:
- Higher priority = processed first
- Default priority = 50
- Use for conflict resolution

## Real-World DDJ Controller Examples

### DDJ-FLX4 Controller Mapping

The DDJ-FLX4 is an entry-level 2-deck controller with 259 MIDI mappings. Key examples from its CSV:

**Browser controls (global, Ch 7):**
```csv
Browse,Browse,Rotary,B640,,,,,,,,,,,Browse(Track/Folder Select)
Forward,Browse+Press,Button,9641,,,,,,,,,,,Library Forward (Folder Open)
Back,Browse+Press+Shift,Button,9642,,,,,,,,,,,Library Back (Folder Close)
Load,Load,Button,,9646,9647,,,,,,,,,Load to Deck / Instant Double (double click)
```

**Playback controls (Deck 1 & 2):**
```csv
PlayPause,PlayPause,Button,900B,0,1,,,900B,0,1,,,Fast;Priority=50,Play/Pause
Cue,Cue,Button,900C,0,1,,,900C,0,1,,,Fast;Priority=50,Cue Set/Play Cue Back
JumpToTrackStart,Cue+Shift,Button,9048,0,1,,,9048,0,1,,,Fast;Priority=50,Jump to track start
```

**Jog wheel (complex control types):**
```csv
JogScratch,JogScratch,JogRotate,B022,0,1,,,,,,,,RO,Scratch
JogPitchBend,JogPitchBend,JogRotate,B023,0,1,,,,,,,,RO,Pitch Bend
JogTouch,JogTouch,JogTouch,9036,0,1,,,,,,,,RO,Touch
```

**High-resolution fader (14-bit):**
```csv
TempoSlider,TempoSlider,KnobSliderHiRes,B000,0,1,,,,,,,,Fast,Tempo Control
CrossFader,CrossFader,KnobSliderHiRes,B61F,,,,,,,,,,Fast,Crossfader
ChannelFader,ChannelFader,KnobSliderHiRes,B013,0,1,,,,,,,,,CH Fader
```

**Mixer controls:**
```csv
Gain,Gain,KnobSliderHiRes,B004,0,1,,,,,,,,Fast,Gain
HighEQ,HighEQ,KnobSliderHiRes,B007,0,1,,,,,,,,Fast,High EQ
MidEQ,MidEQ,KnobSliderHiRes,B00B,0,1,,,,,,,,Fast,Mid EQ
LowEQ,LowEQ,KnobSliderHiRes,B00F,0,1,,,,,,,,Fast,Low EQ
```

### DDJ-FLX10 Controller Mapping

The DDJ-FLX10 is a professional 4-deck controller with 567 MIDI mappings. Notable features:

**4-deck support:**
```csv
PlayPause,PlayPause,Button,900B,0,1,2,3,900B,0,1,2,3,Fast;Priority=50;Dual,Play/Pause
Cue,Cue,Button,900C,0,1,2,3,900C,0,1,2,3,Fast;Priority=50;Dual,Cue Set/Play Cue Back
Sync,Sync,Button,9058,0,1,2,3,9058,0,1,2,3,Blink=600;Dual,Sync On/Off
```

**Advanced loop controls:**
```csv
LoopIn,LoopIn,Button,9010,0,1,2,3,9010,0,1,2,3,Dual;Fast,Loop in/Loop in adjust
LoopOut,LoopOut,Button,9011,0,1,2,3,9011,0,1,2,3,Dual;Fast,Loop out/Loop out adjust
LoopHalf,LoopIn,Button,9012,0,1,2,3,9012,0,1,2,3,Dual;Fast,Loop Size Select (Half)
LoopDouble,LoopOut,Button,9013,0,1,2,3,9013,0,1,2,3,Dual;Fast,Loop Size Select (Double)
4BeatLoop,4BeatLoop,Button,9014,0,1,2,3,9014,0,1,2,3,Dual;Fast,Auto Loop On/Off
```

**Key Sync features:**
```csv
KeySync,KeySync,Button,9065,0,1,2,3,9065,0,1,2,3,Dual,Key Sync On/Off
MasterTempo,KeySync+LongPress,Button,901A,0,1,2,3,901A,0,1,2,3,Dual,MasterTempo On/Off
KeyReset,KeySync+Shift,Button,9064,0,1,2,3,9064,0,1,2,3,Dual,Key Reset
```

**Special options:**
- `Dual` - Dual deck mode for 4-deck controllers
- `Fast;Priority=50` - High-priority time-critical controls
- `Blink=600` - LED blink rate in milliseconds
- `RO` - Read-Only (output/indicator only)

### Common DDJ Mapping Patterns

**Pattern 1: Shift button modifiers**
```csv
# Primary function
PlayPause,PlayPause,Button,900B,0,1,,,900B,0,1,,,Fast;Priority=50,Play/Pause
# Shift+function variant
PlayPause,PlayPause+Shift,Button,900E,0,1,,,900E,0,1,,,Fast;Priority=50,Play/Pause
```

**Pattern 2: Load with multi-deck support**
```csv
# Empty first deck column means no deck 1 assignment
Load,Load,Button,,9646,9647,,,,,,,,,Load to Deck
```

**Pattern 3: Global browser controls**
```csv
# Empty deck columns, global channel (6 = Ch 7)
Browse,Browse,Rotary,B640,,,,,,,,,,,Browse Track Select
```

**Pattern 4: Jog wheel with RO (output only)**
```csv
# No MIDI OUT, RO option
JogScratch,JogScratch,JogRotate,B022,0,1,,,,,,,,RO,Scratch
```

## Complete Rekordbox Function Reference

### Official Function List (from RB_CSV_6.7.4.xml)

**Playback Functions:**
- `PlayPause` - Play/Pause toggle (type: Button)
- `Cue` - Cue point set/play (type: Button)
- `JumpToTrackStart` - Return to track start (type: Button)
- `TrackNext` - Next track (type: Button)
- `TrackPrev` - Previous track (type: Button)
- `SearchFwd` - Search forward (type: Button)
- `SearchRev` - Search reverse (type: Button)
- `NeedleSearch` - Position search (type: Value)
- `Slip` - Slip mode (type: Button)
- `Quantize` - Quantize on/off (type: Button)
- `Reverse` - Reverse playback (type: Button)
- `SlipReverse` - Slip reverse (type: Button)
- `Vinyl` - Vinyl mode (type: Button)
- `AutoCue` - Auto cue (type: Button)

**Tempo Functions:**
- `TempoSlider` - Tempo fader (type: Knob/Fader)
- `TempoRange` - Tempo range selector (type: Button)
- `TempoReset` - Reset tempo to 0% (type: Button)
- `Sync` - Beat sync on/off (type: Button)
- `SyncRate` - Sync rate (type: Button)
- `Master` - Master tempo control (type: Button)
- `TapBpm` - Tap tempo (type: Button)
- `MasterTempo` - Master tempo on/off (type: Button)
- `PitchBendUp` - Pitch bend up (type: Button)
- `PitchBendDown` - Pitch bend down (type: Button)

**Loop Functions:**
- `LoopIn` - Set loop in point (type: Button)
- `LoopOut` - Set loop out point (type: Button)
- `ActiveLoop` - Enable/disable active loop (type: Button)
- `LoopHalf` - Halve loop size (type: Button)
- `LoopDouble` - Double loop size (type: Button)
- `LoopHalfDouble` - Loop size adjust (type: Rotary)
- `LoopMove` - Move loop (type: Rotary)
- `LoopMoveRight` - Move loop right (type: Button)
- `LoopMoveLeft` - Move loop left (type: Button)
- `ReloopExit` - Reloop/exit (type: Button)
- `ReTrigger` - Loop retrigger (type: Button)
- `4BeatLoop` - 4-beat auto loop (type: Button)
- `AutoLoop` - Auto loop on/off (type: Button)
- Beat loop sizes: `BeatLoop1_64`, `BeatLoop1_32`, `BeatLoop1_16`, `BeatLoop1_8`, `BeatLoop1_4`, `BeatLoop1_2`, `BeatLoop1`, `BeatLoop2`, `BeatLoop4`, `BeatLoop8`, `BeatLoop16`, `BeatLoop32`, `BeatLoop64`, `BeatLoop128`, `BeatLoop256`, `BeatLoop512`

**Key Shift Functions:**
- `SemitoneUp` - Semitone up (type: Button)
- `SemitoneDown` - Semitone down (type: Button)
- `KeySync` - Key sync (type: Button)
- `KeyReset` - Reset key (type: Button)

**Grid Functions:**
- `GridAdjust` - Grid adjust (type: Button)
- `GridSlide` - Grid slide (type: Button)
- `GridAdjustHalf` - Grid adjust half (type: Button)
- `GridAdjustDouble` - Grid adjust double (type: Button)

**DVS Functions:**
- `DvsAbsolute` - DVS absolute mode (type: Button)
- `DvsRelative` - DVS relative mode (type: Button)
- `DvsInternal` - DVS internal mode (type: Button)
- `DvsThrough` - DVS through mode (type: Button)
- `DvsAbsRelInt` - DVS mode toggle (type: Button)

**Track Separation Functions:**
- `ActivePartInst` - Instrumental stem (type: Button)
- `ActivePartVocal` - Vocal stem (type: Button)
- `ActivePartDrums` - Drums stem (type: Button)

**Capture:**
- `SlicerCapture` - Slicer capture (type: Button)

### Function Type Reference

Type codes from RB_CSV_6.7.4.xml:
- `type="1"` - Button/Pad
- `type="2"` - Rotary encoder (relative values)
- `type="3"` - Knob/Fader (absolute values)
- `type="5"` - Indicator (output only)
- `type="7"` - Value (special input like NeedleSearch)

## References

**Project Documentation:**
- `REKORDBOX-MIDI-CSV-SPEC.md` - Community specification (reverse-engineered)
- `references/Rekordbox_MIDI_Learn_Guide_v5.3.0.pdf` - Official MIDI Learn operation guide

**Controller CSV Examples:**
- `references/DDJ-FLX10.midi.csv` - Professional 4-deck controller (567 mappings)
- `references/DDJ-GRV6.midi.csv` - 2-channel controller (339 mappings)

**Implementation:**
- `sniffer.py` - MIDI sniffer with CSV parser (class `RekordboxCSVParser`)

**External Sources:**
- Rekordbox installation: `/Applications/rekordbox 7/rekordbox.app/Contents/Resources/MidiMappings/`
