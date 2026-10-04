---
name: tauri-impl-testing
description: >
  Use when writing tests for Tauri 2 commands, mocking IPC calls, or setting up E2E test suites.
  Prevents untestable command handlers and stale mock state from missing clearMocks() between tests.
  Covers Rust unit testing, frontend IPC mocking with mockIPC/mockWindows, WebDriver E2E testing, and integration testing.
  Keywords: tauri testing, mockIPC, mockWindows, clearMocks, cargo test, E2E testing, WebDriver, Vitest.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-testing

## Quick Reference

### Testing Layers

| Layer | Tool | What It Tests |
|-------|------|---------------|
| Rust Unit Tests | `cargo test` | Command logic, state management, error handling |
| Frontend Unit Tests | Vitest / Jest + `@tauri-apps/api/mocks` | UI components, IPC call handling |
| Integration Tests | Vitest / Jest + mockIPC | Frontend-backend contract |
| E2E Tests | WebDriver (Selenium/Playwright) | Full application behavior |

### Mock API Imports

```typescript
import { mockIPC, mockWindows, mockConvertFileSrc, clearMocks } from '@tauri-apps/api/mocks';
```

### Mock Functions

| Function | Purpose | Scope |
|----------|---------|-------|
| `mockIPC(handler, options?)` | Intercept `invoke()` calls | All commands |
| `mockWindows(current, ...rest)` | Mock window labels | Window API |
| `mockConvertFileSrc(platform)` | Mock file-to-URL conversion | Asset protocol |
| `clearMocks()` | Remove all mocks | All |

### Critical Warnings

**ALWAYS** call `clearMocks()` in `afterEach()` -- failing to do so leaks mocks between tests, causing flaky test results.

**NEVER** test Tauri commands by running them through IPC in unit tests -- test the underlying Rust function directly. Commands are regular functions.

**NEVER** import `@tauri-apps/api` modules in test files without mocking first -- they throw errors outside a Tauri webview context.

**ALWAYS** use `mockIPC` before any `invoke()` call in frontend tests -- without it, `invoke()` attempts to use the actual IPC bridge which does not exist in a test environment.

**NEVER** forget to handle the `Promise<UnlistenFn>` return type when testing event listeners -- `listen()` returns a Promise, not a synchronous function.

---

## Essential Patterns

### Pattern 1: Rust Unit Testing (Commands Are Regular Functions)

Tauri commands decorated with `#[tauri::command]` are plain Rust functions. Test them directly without any Tauri runtime:

```rust
// src-tauri/src/commands.rs
#[tauri::command]
pub fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}

#[tauri::command]
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_greet() {
        let result = greet("World".to_string());
        assert_eq!(result, "Hello, World!");
    }

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
    }
}
```

Run with `cargo test` from the `src-tauri/` directory.

### Pattern 2: Testing Commands That Return Result

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("not found: {0}")]
    NotFound(String),
    #[error("invalid input: {0}")]
    InvalidInput(String),
}

impl serde::Serialize for AppError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::ser::Serializer {
        serializer.serialize_str(self.to_string().as_ref())
    }
}

#[tauri::command]
pub fn parse_number(input: String) -> Result<i64, AppError> {
    input.parse::<i64>().map_err(|_| AppError::InvalidInput(input))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_valid() {
        assert_eq!(parse_number("42".to_string()), Ok(42));
    }

    #[test]
    fn test_parse_invalid() {
        let result = parse_number("abc".to_string());
        assert!(result.is_err());
    }
}
```

### Pattern 3: Testing Commands With State (Mutable)

Commands that use `tauri::State` cannot be tested directly with a State parameter. Extract the business logic into separate functions:

```rust
use std::sync::Mutex;

#[derive(Default)]
pub struct Counter {
    pub value: u32,
}

// Business logic -- easily testable
pub fn increment_counter(counter: &mut Counter) -> u32 {
    counter.value += 1;
    counter.value
}

// Tauri command -- thin wrapper
#[tauri::command]
pub fn increment(state: tauri::State<'_, Mutex<Counter>>) -> u32 {
    let mut counter = state.lock().unwrap();
    increment_counter(&mut counter)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_increment() {
        let mut counter = Counter::default();
        assert_eq!(increment_counter(&mut counter), 1);
        assert_eq!(increment_counter(&mut counter), 2);
        assert_eq!(increment_counter(&mut counter), 3);
    }
}
```

### Pattern 4: Frontend IPC Mocking (mockIPC)

```typescript
import { mockIPC, clearMocks } from '@tauri-apps/api/mocks';
import { invoke } from '@tauri-apps/api/core';
import { describe, it, expect, afterEach } from 'vitest';

afterEach(() => {
  clearMocks();
});

describe('greet command', () => {
  it('returns greeting message', async () => {
    mockIPC((cmd, args) => {
      if (cmd === 'greet') {
        return `Hello, ${(args as Record<string, unknown>).name}!`;
      }
      throw new Error(`Unknown command: ${cmd}`);
    });

    const result = await invoke<string>('greet', { name: 'Test' });
    expect(result).toBe('Hello, Test!');
  });

  it('handles errors', async () => {
    mockIPC((cmd) => {
      if (cmd === 'risky_operation') {
        throw new Error('Operation failed');
      }
    });

    await expect(invoke('risky_operation')).rejects.toThrow('Operation failed');
  });
});
```

### Pattern 5: Mocking Windows

```typescript
import { mockWindows, clearMocks } from '@tauri-apps/api/mocks';
import { getCurrentWindow } from '@tauri-apps/api/window';
import { afterEach, it, expect } from 'vitest';

afterEach(() => {
  clearMocks();
});

it('identifies current window', () => {
  // First argument is the "current" window label
  // Remaining arguments are other window labels
  mockWindows('main', 'settings', 'about');

  const win = getCurrentWindow();
  expect(win.label).toBe('main');
});
```

### Pattern 6: Mocking File Source Conversion

```typescript
import { mockConvertFileSrc, clearMocks } from '@tauri-apps/api/mocks';
import { convertFileSrc } from '@tauri-apps/api/core';
import { afterEach, it, expect } from 'vitest';

afterEach(() => {
  clearMocks();
});

it('converts file paths to URLs', () => {
  mockConvertFileSrc('linux');

  const url = convertFileSrc('/path/to/image.png');
  expect(url).toContain('image.png');
});
```

### Pattern 7: Mocking IPC With Event Support

```typescript
import { mockIPC, clearMocks } from '@tauri-apps/api/mocks';
import { listen, emit } from '@tauri-apps/api/event';

mockIPC(
  (cmd, args) => {
    // Handle commands
    if (cmd === 'get_data') return { value: 42 };
  },
  { shouldMockEvents: true }
);

// Now event APIs also work in tests
const unlisten = await listen('test-event', (event) => {
  console.log(event.payload);
});

await emit('test-event', 'hello');
unlisten();
clearMocks();
```

### Pattern 8: Testing React Components With Tauri APIs

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { mockIPC, clearMocks } from '@tauri-apps/api/mocks';
import { afterEach, beforeEach, it, expect } from 'vitest';
import { MyComponent } from './MyComponent';

beforeEach(() => {
  mockIPC((cmd, args) => {
    if (cmd === 'get_user') {
      return { name: 'Alice', age: 30 };
    }
  });
});

afterEach(() => {
  clearMocks();
});

it('displays user data from backend', async () => {
  render(<MyComponent />);

  await waitFor(() => {
    expect(screen.getByText('Alice')).toBeInTheDocument();
  });
});
```

### Pattern 9: Testing Async Commands in Rust

```rust
#[tauri::command]
pub async fn fetch_data(url: String) -> Result<String, String> {
    reqwest::get(&url)
        .await
        .map_err(|e| e.to_string())?
        .text()
        .await
        .map_err(|e| e.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_fetch_data() {
        // Use a mock HTTP server or known endpoint
        let result = fetch_data("https://httpbin.org/get".to_string()).await;
        assert!(result.is_ok());
    }
}
```

For async Rust tests, add `tokio` as a dev dependency:

```toml
[dev-dependencies]
tokio = { version = "1", features = ["rt", "macros"] }
```

---

## E2E Testing Strategy

### WebDriver-Based Testing

Tauri apps can be tested with WebDriver (Selenium, Playwright) by enabling the webview's DevTools protocol.

**Step 1:** Enable DevTools in development:

```rust
WebviewWindowBuilder::new(app, "main", WebviewUrl::App("/".into()))
    .devtools(true)
    .build()?;
```

**Step 2:** Use Playwright or Selenium to connect to the webview:

```typescript
// playwright.config.ts (conceptual -- Tauri-specific setup required)
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    // Connect to the Tauri app's webview via CDP
    connectOptions: {
      wsEndpoint: 'ws://localhost:9222',
    },
  },
});
```

**Note:** E2E testing with Tauri requires platform-specific WebDriver setup. The recommended approach is:

1. Build the app in debug mode: `npm run tauri build -- --debug`
2. Use `tauri-driver` (a WebDriver server for Tauri apps)
3. Connect your test framework (Jest, Playwright, etc.) to the WebDriver

### tauri-driver Setup

```bash
cargo install tauri-driver
```

```bash
# Start tauri-driver (listens on port 4444 by default)
tauri-driver
```

Then use any WebDriver client to control the app.

---

## Test Organization

### Recommended Directory Structure

```
my-tauri-app/
├── src/
│   ├── components/
│   │   ├── Greeting.tsx
│   │   └── Greeting.test.tsx      # Component + IPC tests
│   └── __tests__/
│       └── integration.test.ts     # Cross-component tests
├── src-tauri/
│   └── src/
│       ├── commands.rs             # Commands
│       └── commands_test.rs        # OR tests in same file
├── e2e/
│   ├── app.spec.ts                 # E2E tests
│   └── setup.ts                    # WebDriver setup
└── vitest.config.ts
```

### Vitest Configuration for Tauri Projects

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test-setup.ts'],
  },
});
```

```typescript
// src/test-setup.ts
import { afterEach } from 'vitest';
import { clearMocks } from '@tauri-apps/api/mocks';

afterEach(() => {
  clearMocks();
});
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for mock functions and test utilities
- [references/examples.md](references/examples.md) -- Working test examples for Rust, TypeScript, and E2E
- [references/anti-patterns.md](references/anti-patterns.md) -- Common testing mistakes and how to avoid them

### Official Sources

- https://v2.tauri.app/develop/tests/
- https://v2.tauri.app/reference/javascript/api/namespacemocks/
