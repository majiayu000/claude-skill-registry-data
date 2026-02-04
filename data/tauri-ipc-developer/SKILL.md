---
name: tauri-ipc-developer
description: Specialized agent for implementing type-safe IPC communication between React frontend and Rust backend in Tauri v2 applications. Use when adding new Tauri commands, implementing bidirectional events, debugging IPC serialization issues, or optimizing command performance.
---

# Tauri IPC Developer

Expert agent for developing type-safe Inter-Process Communication (IPC) between React frontend and Rust backend in Tauri v2 applications.

## Core Responsibilities

### 1. Implement New Tauri Commands

When adding new backend functionality accessible from the frontend:

**Rust Side (`src-tauri/src/commands.rs`):**
```rust
use tauri::command;
use crate::types::ParametricBand;
use crate::profile::ProfileManager;

#[command]
pub async fn save_profile(
    name: String,
    bands: Vec<ParametricBand>,
    preamp: f32,
) -> Result<String, String> {
    // Implementation
    match ProfileManager::save(&name, bands, preamp) {
        Ok(path) => Ok(path.to_string_lossy().to_string()),
        Err(e) => Err(format!("Failed to save profile: {}", e)),
    }
}
```

**Key Requirements:**
- Use `#[command]` attribute macro
- Return `Result<T, String>` for error handling (String errors appear in frontend)
- Use `async` only if the command performs I/O or blocking operations
- Keep command functions thin - delegate to modules (`profile.rs`, `audio_monitor.rs`)
- Handle all error cases explicitly

**Frontend Side (`lib/tauri.ts`):**
```typescript
import { invoke } from '@tauri-apps/api/core';
import type { ParametricBand } from './types';

export async function saveProfile(
  name: string,
  bands: ParametricBand[],
  preamp: number
): Promise<string> {
  return await invoke<string>('save_profile', { name, bands, preamp });
}
```

**Type Safety Checklist:**
- ✅ TypeScript types match Rust struct definitions
- ✅ Error handling with try/catch in frontend
- ✅ Proper serialization of complex types (Vec, HashMap, Option)
- ✅ Command name matches exactly (snake_case)

### 2. Type Synchronization

**Critical**: Frontend and backend types MUST stay in sync.

**Rust Types (`src-tauri/src/types.rs`):**
```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ParametricBand {
    pub filter_type: FilterType,
    pub frequency: f32,
    pub gain: f32,
    pub q_factor: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum FilterType {
    Peaking,
    LowShelf,
    HighShelf,
}
```

**TypeScript Types (`lib/types.ts`):**
```typescript
export interface ParametricBand {
  filterType: 'Peaking' | 'LowShelf' | 'HighShelf';
  frequency: number;
  gain: number;
  qFactor: number;
}

export type FilterType = 'Peaking' | 'LowShelf' | 'HighShelf';
```

**Synchronization Rules:**
- Use `#[serde(rename_all = "camelCase")]` in Rust for JS compatibility
- Rust `f32/f64` → TypeScript `number`
- Rust `String` → TypeScript `string`
- Rust `Vec<T>` → TypeScript `T[]`
- Rust `Option<T>` → TypeScript `T | null`
- Rust enums → TypeScript union types

### 3. Bidirectional Events

For backend → frontend communication (e.g., audio peak meter updates):

**Rust Emitter (`src-tauri/src/audio_monitor.rs`):**
```rust
use tauri::{AppHandle, Emitter};
use serde::{Serialize, Deserialize};

#[derive(Clone, Serialize, Deserialize)]
pub struct PeakMeterUpdate {
    pub peak_db: f32,
    pub device_name: String,
    pub sample_rate: u32,
}

pub fn emit_peak_update(app: &AppHandle, update: PeakMeterUpdate) {
    let _ = app.emit("peak_meter_update", update);
}
```

**Frontend Listener (`lib/use-audio-status.ts`):**
```typescript
import { listen } from '@tauri-apps/api/event';
import { useEffect, useState } from 'react';

interface PeakMeterUpdate {
  peakDb: number;
  deviceName: string;
  sampleRate: number;
}

export function useAudioStatus() {
  const [peakData, setPeakData] = useState<PeakMeterUpdate | null>(null);

  useEffect(() => {
    const unlisten = listen<PeakMeterUpdate>('peak_meter_update', (event) => {
      setPeakData(event.payload);
    });

    return () => {
      unlisten.then((fn) => fn());
    };
  }, []);

  return peakData;
}
```

**Event Naming Convention:**
- Use `snake_case` for event names
- Prefix domain: `audio_*`, `profile_*`, `ab_test_*`
- Document event payloads in both codebases

### 4. Error Handling Patterns

**Rust Command Error Handling:**
```rust
#[command]
pub async fn load_profile(name: String) -> Result<EqProfile, String> {
    ProfileManager::load(&name)
        .map_err(|e| match e.kind() {
            ErrorKind::NotFound => format!("Profile '{}' not found", name),
            ErrorKind::PermissionDenied => "Permission denied".to_string(),
            _ => format!("Failed to load profile: {}", e),
        })
}
```

**Frontend Error Handling:**
```typescript
try {
  const profile = await loadProfile(name);
  setCurrentProfile(profile);
} catch (error) {
  console.error('Load failed:', error);
  toast.error(error as string); // Tauri errors are strings
}
```

**Error Best Practices:**
- Return user-friendly error messages from Rust
- Log detailed errors server-side before converting to strings
- Use `thiserror` crate for structured Rust errors
- Catch and display errors in UI (toast notifications)

### 5. Performance Optimization

**Debouncing Frequent Commands:**

For real-time EQ adjustments, debounce on frontend:

```typescript
import { debounce } from 'lodash-es';

const debouncedApply = useMemo(
  () =>
    debounce(async (bands: ParametricBand[], preamp: number) => {
      await applyProfile(bands, preamp);
    }, 250),
  []
);

useEffect(() => {
  debouncedApply(bands, preamp);
}, [bands, preamp]);
```

**Batching Updates:**

Send multiple changes in one IPC call instead of multiple:

```typescript
// ❌ Bad: 3 IPC calls
await updatePreamp(preamp);
await updateBands(bands);
await saveSettings();

// ✅ Good: 1 IPC call
await updateSettings({ preamp, bands, autoSave: true });
```

**Async vs Sync Commands:**

- Use `async` for I/O operations (file reads, network)
- Use sync for CPU-bound operations < 16ms (audio math)
- Never block the main thread for > 16ms

### 6. Security Considerations

**Input Validation:**

Always validate on the Rust side:

```rust
#[command]
pub fn set_frequency(band_id: usize, freq: f32) -> Result<(), String> {
    if !(20.0..=20000.0).contains(&freq) {
        return Err("Frequency must be between 20 and 20000 Hz".to_string());
    }
    if band_id >= MAX_BANDS {
        return Err(format!("Band ID {} exceeds maximum {}", band_id, MAX_BANDS));
    }
    // Safe to proceed
    Ok(())
}
```

**Path Traversal Prevention:**

```rust
use std::path::PathBuf;

#[command]
pub fn load_profile_by_path(path: String) -> Result<EqProfile, String> {
    let profile_dir = ProfileManager::get_profile_dir()?;
    let requested_path = PathBuf::from(&path);

    // Prevent path traversal attacks
    if !requested_path.starts_with(&profile_dir) {
        return Err("Invalid profile path".to_string());
    }

    ProfileManager::load_from_path(requested_path)
}
```

## Command Registration

All commands must be registered in `src-tauri/src/lib.rs`:

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            commands::apply_profile,
            commands::save_profile,
            commands::load_profile,
            commands::list_profiles,
            commands::delete_profile,
            commands::get_settings,
            commands::update_settings,
            commands::import_eapo_config,
            commands::export_eapo_config,
            // Add new commands here
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Testing IPC Commands

**Unit Tests (Rust):**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_save_profile() {
        let result = save_profile(
            "Test Profile".to_string(),
            vec![],
            0.0
        ).await;
        assert!(result.is_ok());
    }
}
```

**Integration Tests (Frontend):**
```typescript
import { describe, it, expect } from 'vitest';
import { saveProfile } from './tauri';

describe('Tauri IPC', () => {
  it('should save profile', async () => {
    const result = await saveProfile('Test', [], 0);
    expect(result).toBeDefined();
  });
});
```

## Common Pitfalls

1. **Command Name Mismatch**
   - Rust: `save_profile` (snake_case)
   - Frontend: `'save_profile'` (must match exactly)

2. **Async Overuse**
   - Don't use `async` for simple calculations
   - Only for I/O or operations > 16ms

3. **Missing Error Handling**
   - Always return `Result<T, String>`, never panic in commands
   - Handle all error branches

4. **Type Mismatches**
   - Rust `f32` vs TypeScript `number` (OK)
   - Rust `u32` serializes as number, but may overflow in JS
   - Use `i64` for large numbers (JS safe integer limit: 2^53)

5. **Serialization Failures**
   - Missing `#[derive(Serialize, Deserialize)]`
   - Circular references (use `#[serde(skip)]`)
   - Non-serializable types (file handles, closures)

6. **Event Memory Leaks**
   - Always unlisten in `useEffect` cleanup
   - Remove listeners when components unmount

## Reference Materials

For detailed examples and patterns, see:
- `references/command_patterns.md` - Common IPC command patterns
- `references/type_mappings.md` - Rust ↔ TypeScript type reference
- `references/event_patterns.md` - Event-driven communication examples

## Development Workflow

When implementing new IPC features:

1. **Define Rust types** in `src-tauri/src/types.rs`
2. **Implement command** in `src-tauri/src/commands.rs`
3. **Register command** in `src-tauri/src/lib.rs`
4. **Mirror types** in `lib/types.ts`
5. **Create wrapper** in `lib/tauri.ts`
6. **Test with curl or Tauri dev tools**
7. **Integrate in React components**
8. **Add error handling** throughout the stack

## Performance Benchmarks

Target response times:
- **Simple queries** (get settings): < 1ms
- **File I/O** (load profile): < 10ms
- **Config write** (apply EQ): < 50ms
- **Heavy computation** (FFT analysis): < 100ms

If commands exceed these targets:
- Profile with `cargo flamegraph`
- Consider caching frequently accessed data
- Move heavy work to separate threads
- Use streaming for large data sets

## Support

For Tauri-specific questions:
- [Tauri v2 Docs](https://v2.tauri.app/)
- [Tauri Discord](https://discord.gg/tauri)
- Check `examples/` in the Tauri repository
