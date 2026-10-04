---
name: windows-process-manager
description: Manage Windows-specific process isolation, stdio pipe decoding, and ANSI code page handling. Use when debugging Windows-specific MCP server issues, fixing stdio encoding, or handling Windows path discovery.
---

# Windows Process Manager

Manage Windows-specific process isolation and stdio handling for LibrAgent.

## Key Challenges

### 1. ANSI Code Page Handling

Windows uses ANSI code pages by default. Stdio output from MCP servers may contain non-UTF-8 characters.

```rust
// Convert ANSI to UTF-8
use std::os::windows::prelude::*;
use winapi::um::consoleapi::GetConsoleOutputCP;
```

### 2. Stdio Pipe Reading

Windows pipes require special handling for async reading:

```rust
use tokio::io::{AsyncReadExt, BufReader};
use tokio::process::Command;

let mut child = Command::new("cmd")
    .args(&["/C", "server.exe"])
    .stdout(Stdio::piped())
    .spawn()?;

let mut stdout = BufReader::new(child.stdout.take().unwrap());
let mut buffer = Vec::new();
stdout.read_to_end(&mut buffer).await?;
```

### 3. Path Discovery

Windows paths require normalization:

```rust
use std::path::{Path, PathBuf};

fn normalize_windows_path(path: &str) -> PathBuf {
    let path = Path::new(path);
    if path.is_absolute() {
        path.to_path_buf()
    } else {
        std::env::current_dir().unwrap().join(path)
    }
}
```

### 4. Process Spawning

```rust
use std::process::Stdio;

let mut cmd = Command::new(program);
cmd.args(args)
    .stdin(Stdio::piped())
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .creation_flags(CREATE_NO_WINDOW); // Hide console window
```

## Audit Checklist

- [ ] Stdio pipes use `Stdio::piped()` not `Stdio::inherit()`
- [ ] Process spawning uses `CREATE_NO_WINDOW` flag on Windows
- [ ] Output decoding handles ANSI code pages
- [ ] Path handling uses `PathBuf` and normalization
- [ ] No hardcoded Unix paths (`/usr/bin`, `/tmp`)
- [ ] Environment variables use Windows format (`%VAR%` vs `$VAR`)

## Platform Detection

```rust
#[cfg(target_os = "windows")]
{
    // Windows-specific code
}

#[cfg(not(target_os = "windows"))]
{
    // Unix-specific code
}
```
