---
name: eqapo-format-expert
description: Expert in EqualizerAPO configuration file format, parsing, and generation. Use when implementing EAPO config import/export, adding support for new filter types, or debugging config file issues.
---

# EqualizerAPO Format Expert

Specialized agent for working with EqualizerAPO configuration files, ensuring correct parsing and generation of `.txt` config files.

## EqualizerAPO Overview

**EqualizerAPO** is a parametric equalizer for Windows that processes system audio via APO (Audio Processing Objects) framework.

- **Config Location**: `C:\Program Files\EqualizerAPO\config\config.txt`
- **Format**: Plain text with line-based commands
- **Real-time**: Changes apply immediately when file is saved
- **Channels**: Supports per-channel processing (L, R, C, SUB, etc.)

## Config File Format

### Basic Structure

```
# Comment lines start with #

Preamp: -5.0 dB
Filter: ON PK Fc 1000 Hz Gain 3.0 dB Q 1.41
Filter: ON LS Fc 80 Hz Gain -2.5 dB Q 0.71
Filter: ON HS Fc 10000 Hz Gain 4.0 dB Q 0.71
```

### Filter Types Supported by EQAPO GUI

| Type | EAPO Code | Description | Parameters |
|------|-----------|-------------|------------|
| **Peaking** | `PK` | Bell curve EQ | Fc, Gain, Q |
| **Low Shelf** | `LS` | Bass adjustment | Fc, Gain, Q |
| **High Shelf** | `HS` | Treble adjustment | Fc, Gain, Q |

### Additional Filter Types (Not Yet Implemented)

| Type | EAPO Code | Description |
|------|-----------|-------------|
| Low Pass | `LP` | Cuts high frequencies |
| High Pass | `HP` | Cuts low frequencies |
| Band Pass | `BP` | Passes only a frequency range |
| Notch | `NO` | Cuts a specific frequency |
| All Pass | `AP` | Affects phase, not magnitude |

### Preamp Syntax

```
Preamp: <value> dB
```

Examples:
```
Preamp: -5.0 dB
Preamp: 3 dB
Preamp: 0 dB
```

**Rules:**
- Must be on its own line
- Value can be integer or float
- Unit "dB" required
- Negative values reduce volume (prevent clipping)
- Typical range: -20 to +20 dB

### Filter Syntax

```
Filter: <ON|OFF> <TYPE> Fc <frequency> Hz Gain <gain> dB Q <q_factor>
```

Examples:
```
Filter: ON PK Fc 1000 Hz Gain 3.0 dB Q 1.41
Filter: ON LS Fc 80 Hz Gain -2.5 dB Q 0.71
Filter: OFF HS Fc 10000 Hz Gain 4.0 dB Q 0.71
```

**Rules:**
- `ON` or `OFF` state (case-insensitive)
- Filter type: `PK`, `LS`, `HS`, etc.
- Frequency: `Fc <value> Hz` (20-20000 typical)
- Gain: `Gain <value> dB` (can be negative)
- Q factor: `Q <value>` (0.1-30 typical)

### Channel-Specific Filters

```
Channel: L
Filter: ON PK Fc 1000 Hz Gain 3.0 dB Q 1.41

Channel: R
Filter: ON PK Fc 1000 Hz Gain 2.0 dB Q 1.41

Channel: ALL
```

**Not yet supported in EQAPO GUI** - applies filters to all channels globally.

## Parsing EqualizerAPO Files

### Parser Implementation (TypeScript)

```typescript
export interface ParsedEapoConfig {
  preamp: number;
  bands: ParametricBand[];
}

export function parseEapoConfig(content: string): ParsedEapoConfig {
  const lines = content.split('\n').map((line) => line.trim());

  let preamp = 0;
  const bands: ParametricBand[] = [];

  for (const line of lines) {
    // Skip comments and empty lines
    if (line.startsWith('#') || line === '') continue;

    // Parse preamp
    if (line.startsWith('Preamp:')) {
      const match = line.match(/Preamp:\s*([-+]?\d+\.?\d*)\s*dB/i);
      if (match) {
        preamp = parseFloat(match[1]);
      }
      continue;
    }

    // Parse filter
    if (line.startsWith('Filter:')) {
      const band = parseFilterLine(line);
      if (band) {
        bands.push(band);
      }
    }
  }

  return { preamp, bands };
}

function parseFilterLine(line: string): ParametricBand | null {
  // Extract state (ON/OFF)
  const stateMatch = line.match(/Filter:\s*(ON|OFF)/i);
  if (!stateMatch || stateMatch[1].toUpperCase() === 'OFF') {
    return null; // Skip disabled filters
  }

  // Extract filter type
  const typeMatch = line.match(/(PK|LS|HS|LP|HP|BP|NO|AP)/i);
  if (!typeMatch) return null;

  const filterType = normalizeFilterType(typeMatch[1].toUpperCase());

  // Extract frequency
  const freqMatch = line.match(/Fc\s+([\d.]+)\s*Hz/i);
  if (!freqMatch) return null;
  const frequency = parseFloat(freqMatch[1]);

  // Extract gain
  const gainMatch = line.match(/Gain\s+([-+]?[\d.]+)\s*dB/i);
  if (!gainMatch) return null;
  const gain = parseFloat(gainMatch[1]);

  // Extract Q factor
  const qMatch = line.match(/Q\s+([\d.]+)/i);
  if (!qMatch) return null;
  const qFactor = parseFloat(qMatch[1]);

  // Validate
  if (!isValidBand(frequency, gain, qFactor)) {
    return null;
  }

  return { filterType, frequency, gain, qFactor };
}

function normalizeFilterType(type: string): FilterType {
  switch (type) {
    case 'PK':
    case 'PEAKING':
      return 'Peaking';
    case 'LS':
    case 'LOWSHELF':
      return 'LowShelf';
    case 'HS':
    case 'HIGHSHELF':
      return 'HighShelf';
    default:
      throw new Error(`Unsupported filter type: ${type}`);
  }
}

function isValidBand(frequency: number, gain: number, qFactor: number): boolean {
  return (
    frequency >= 20 &&
    frequency <= 20000 &&
    gain >= -30 &&
    gain <= 30 &&
    qFactor >= 0.01 &&
    qFactor <= 100
  );
}
```

### Edge Cases in Parsing

1. **Case Insensitivity**
   ```
   filter: on pk fc 1000 hz gain 3.0 db q 1.41  ✓
   FILTER: ON PK FC 1000 HZ GAIN 3.0 DB Q 1.41  ✓
   Filter: ON PK Fc 1000 Hz Gain 3.0 dB Q 1.41  ✓
   ```

2. **Extra Whitespace**
   ```
   Filter:  ON   PK  Fc  1000  Hz  Gain  3.0  dB  Q  1.41  ✓
   ```

3. **Integer vs Float**
   ```
   Filter: ON PK Fc 1000 Hz Gain 3 dB Q 1.41     ✓
   Filter: ON PK Fc 1000.0 Hz Gain 3.0 dB Q 1.41 ✓
   ```

4. **Negative Gains**
   ```
   Filter: ON PK Fc 1000 Hz Gain -3.0 dB Q 1.41  ✓
   Filter: ON LS Fc 80 Hz Gain -6 dB Q 0.71      ✓
   ```

5. **Comments Mid-Line** (Not standard, but seen in wild)
   ```
   Filter: ON PK Fc 1000 Hz Gain 3.0 dB Q 1.41 # Boost presence
   ```

## Generating EqualizerAPO Files

### Writer Implementation (Rust)

```rust
pub fn write_eapo_config(
    path: &Path,
    bands: &[ParametricBand],
    preamp: f32,
) -> Result<(), std::io::Error> {
    let mut content = String::new();

    // Header comment
    content.push_str("# Generated by EQAPO GUI\n");
    content.push_str(&format!("# Generated: {}\n\n", chrono::Local::now().format("%Y-%m-%d %H:%M:%S")));

    // Preamp
    content.push_str(&format!("Preamp: {:.1} dB\n", preamp));

    // Filters
    for band in bands {
        let filter_line = format!(
            "Filter: ON {} Fc {} Hz Gain {:.1} dB Q {:.2}\n",
            filter_type_to_code(&band.filter_type),
            band.frequency as u32,
            band.gain,
            band.q_factor
        );
        content.push_str(&filter_line);
    }

    // Write to file
    std::fs::write(path, content)?;

    Ok(())
}

fn filter_type_to_code(filter_type: &FilterType) -> &'static str {
    match filter_type {
        FilterType::Peaking => "PK",
        FilterType::LowShelf => "LS",
        FilterType::HighShelf => "HS",
    }
}
```

### Output Format Example

```
# Generated by EQAPO GUI
# Generated: 2026-01-04 15:30:00

Preamp: -3.5 dB
Filter: ON PK Fc 1000 Hz Gain 3.0 dB Q 1.41
Filter: ON LS Fc 80 Hz Gain -2.5 dB Q 0.71
Filter: ON HS Fc 10000 Hz Gain 4.0 dB Q 0.71
```

**Formatting Rules:**
- Frequency: Integer (no decimal places)
- Gain: 1 decimal place
- Q factor: 2 decimal places
- Consistent spacing
- One filter per line

## Advanced EqualizerAPO Features

### Include Directive

```
Include: subwoofer_eq.txt
Include: headphone_compensation.txt
```

Loads another config file at that position.

### Copy Filter

```
Copy: L=L+0.5*R R=R+0.5*L
```

Mixes channels (crossfeed for headphones).

### Delay

```
Delay: L=0 R=2.5
```

Delays right channel by 2.5ms (speaker positioning).

### Convolution (Impulse Response)

```
Convolution: room_correction.wav
```

Applies FIR filter from WAV file (room correction).

**None of these are supported in EQAPO GUI yet** - future features.

## File Permissions

### Windows UAC Challenges

EqualizerAPO's default config location requires admin rights:
```
C:\Program Files\EqualizerAPO\config\config.txt
```

**Solutions:**

1. **Live Config (Recommended)**
   ```
   C:\Users\<Username>\Documents\EQAPO GUI\live_config.txt
   ```
   Then use EqualizerAPO's `Include:` directive in main config:
   ```
   Include: C:\Users\<Username>\Documents\EQAPO GUI\live_config.txt
   ```

2. **Run as Admin** (Not recommended)
   - Tauri app requests elevation
   - Security risk
   - UAC prompt every time

### Permission Check (Rust)

```rust
pub fn can_write_to_eapo_config(path: &Path) -> bool {
    // Try to open file for writing
    std::fs::OpenOptions::new()
        .write(true)
        .create(false)
        .open(path)
        .is_ok()
}

pub fn get_recommended_config_path() -> PathBuf {
    if can_write_to_eapo_config(&get_default_config_path()) {
        get_default_config_path()
    } else {
        get_live_config_path()
    }
}
```

## Validation

### Pre-Write Validation

```typescript
function validateEapoConfig(bands: ParametricBand[], preamp: number): string[] {
  const errors: string[] = [];

  // Check preamp
  if (preamp < -20 || preamp > 20) {
    errors.push(`Preamp ${preamp} dB exceeds typical range (-20 to +20 dB)`);
  }

  // Check band count
  if (bands.length > 32) {
    errors.push(`Too many bands (${bands.length}). EqualizerAPO supports max 32.`);
  }

  // Check each band
  bands.forEach((band, i) => {
    if (band.frequency < 20 || band.frequency > 20000) {
      errors.push(`Band ${i + 1}: Frequency ${band.frequency} Hz out of range (20-20000 Hz)`);
    }

    if (band.gain < -30 || band.gain > 30) {
      errors.push(`Band ${i + 1}: Gain ${band.gain} dB exceeds typical range (-30 to +30 dB)`);
    }

    if (band.qFactor < 0.1 || band.qFactor > 30) {
      errors.push(`Band ${i + 1}: Q factor ${band.qFactor} out of range (0.1-30)`);
    }
  });

  return errors;
}
```

## Testing

### Parser Test Cases

```typescript
describe('EAPO Parser', () => {
  it('should parse basic config', () => {
    const config = `
      Preamp: -5.0 dB
      Filter: ON PK Fc 1000 Hz Gain 3.0 dB Q 1.41
    `;

    const result = parseEapoConfig(config);

    expect(result.preamp).toBe(-5.0);
    expect(result.bands).toHaveLength(1);
    expect(result.bands[0].frequency).toBe(1000);
  });

  it('should skip disabled filters', () => {
    const config = `
      Filter: ON PK Fc 1000 Hz Gain 3.0 dB Q 1.41
      Filter: OFF PK Fc 2000 Hz Gain 6.0 dB Q 1.41
    `;

    const result = parseEapoConfig(config);
    expect(result.bands).toHaveLength(1);
  });

  it('should handle case insensitivity', () => {
    const config = `FILTER: on pk fc 1000 hz gain 3.0 db q 1.41`;
    const result = parseEapoConfig(config);

    expect(result.bands[0].filterType).toBe('Peaking');
  });
});
```

## Common Issues

1. **❌ Missing "dB" Unit**
   ```
   Preamp: -5     # WRONG: Missing unit
   Preamp: -5 dB  # CORRECT
   ```

2. **❌ Wrong Filter Code**
   ```
   Filter: ON Peaking Fc 1000 Hz ...  # WRONG: Use "PK"
   Filter: ON PK Fc 1000 Hz ...       # CORRECT
   ```

3. **❌ Missing Fc Keyword**
   ```
   Filter: ON PK 1000 Hz ...      # WRONG
   Filter: ON PK Fc 1000 Hz ...   # CORRECT
   ```

4. **❌ Comma as Decimal Separator**
   ```
   Filter: ON PK Fc 1000 Hz Gain 3,0 dB Q 1,41  # WRONG (European notation)
   Filter: ON PK Fc 1000 Hz Gain 3.0 dB Q 1.41  # CORRECT
   ```

## Reference Materials

- `references/eapo_spec.md` - Full EqualizerAPO specification
- `references/filter_types.md` - All supported filter types
- `references/examples.md` - Real-world config file examples
