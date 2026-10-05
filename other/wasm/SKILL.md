---
name: wasm
description: WebAssembly integration — Rust to WASM with wasm-pack/wasm-bindgen, WASI, browser usage, server-side WASM, and performance considerations
layer: domain
category: performance
triggers:
  - "wasm"
  - "webassembly"
  - "wasm-pack"
  - "wasm-bindgen"
  - "wasi"
  - "rust wasm"
  - "compile to wasm"
  - "wasm module"
  - "wasm performance"
inputs:
  - Performance-critical computation to offload
  - Source language (Rust, C/C++, Go, AssemblyScript)
  - Target environment (browser, Node.js, edge, WASI)
outputs:
  - WASM module build configuration
  - JavaScript/TypeScript bindings
  - Integration code for browser or server
  - Performance benchmarks and optimization guidance
linksTo:
  - rust
  - nodejs
  - nextjs
  - performance-profiler
  - cloudflare
linkedFrom:
  - optimize
  - media-processing
preferredNextSkills:
  - rust
  - performance-profiler
  - cloudflare
fallbackSkills:
  - nodejs
  - optimize
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects:
  - Adds wasm-pack or build tooling
  - Generates .wasm binary files
  - May require CORS headers for WASM loading
---

# WebAssembly Integration Specialist

## Purpose

Integrate WebAssembly modules into web and server applications for near-native performance. This skill covers compiling Rust to WASM with `wasm-pack` and `wasm-bindgen`, loading WASM in browsers and Node.js, WASI for server-side use, and understanding when WASM is (and is not) the right tool.

## When to Use WASM

| Use Case | WASM Benefit | Alternative |
|----------|-------------|-------------|
| Image/video processing | 5x-20x faster than JS | Canvas API (limited) |
| Cryptography | Constant-time, fast | SubtleCrypto API (limited algorithms) |
| Compression (zstd, brotli) | Near-native speed | Node.js native modules |
| Physics / simulation | Predictable performance | JS with typed arrays |
| Parsing (markdown, code) | Fast, portable | JS parsers (slower) |
| PDF generation | Complex layout engine | JS libs (slower, larger) |
| **Simple DOM manipulation** | No benefit, adds overhead | Use JavaScript |
| **I/O-heavy operations** | No benefit (I/O is async JS) | Use JavaScript |

## Key Patterns

### 1. Rust to WASM with wasm-pack

```bash
# Install tooling
cargo install wasm-pack
rustup target add wasm32-unknown-unknown

# Create a new WASM library
cargo init --lib my-wasm-lib
```

```toml
# Cargo.toml
[package]
name = "my-wasm-lib"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
wasm-bindgen = "0.2"
serde = { version = "1", features = ["derive"] }
serde-wasm-bindgen = "0.6"
js-sys = "0.3"
web-sys = { version = "0.3", features = ["console", "Performance", "Window"] }

# Optimize for size
[profile.release]
opt-level = "z"       # Optimize for size (or "s" for balanced)
lto = true            # Link-time optimization
codegen-units = 1     # Single codegen unit for better optimization
strip = true          # Strip debug symbols
```

```rust
// src/lib.rs
use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};

// Exported function -- callable from JavaScript
#[wasm_bindgen]
pub fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let mut a: u64 = 0;
            let mut b: u64 = 1;
            for _ in 2..=n {
                let temp = b;
                b = a + b;
                a = temp;
            }
            b
        }
    }
}

// Working with strings
#[wasm_bindgen]
pub fn process_text(input: &str) -> String {
    input
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(|line| line.trim().to_uppercase())
        .collect::<Vec<_>>()
        .join("\n")
}

// Passing complex types with serde
#[derive(Serialize, Deserialize)]
pub struct ImageData {
    width: u32,
    height: u32,
    pixels: Vec<u8>,
}

#[derive(Serialize, Deserialize)]
pub struct ProcessResult {
    processed_pixels: Vec<u8>,
    elapsed_ms: f64,
}

#[wasm_bindgen]
pub fn process_image(val: JsValue) -> Result<JsValue, JsValue> {
    let data: ImageData = serde_wasm_bindgen::from_value(val)
        .map_err(|e| JsValue::from_str(&e.to_string()))?;

    let start = js_sys::Date::now();

    // Apply grayscale transformation
    let mut output = Vec::with_capacity(data.pixels.len());
    for chunk in data.pixels.chunks(4) {
        let gray = (0.299 * chunk[0] as f64
            + 0.587 * chunk[1] as f64
            + 0.114 * chunk[2] as f64) as u8;
        output.extend_from_slice(&[gray, gray, gray, chunk[3]]);
    }

    let result = ProcessResult {
        processed_pixels: output,
        elapsed_ms: js_sys::Date::now() - start,
    };

    serde_wasm_bindgen::to_value(&result)
        .map_err(|e| JsValue::from_str(&e.to_string()))
}

// Structs exported to JS
#[wasm_bindgen]
pub struct Counter {
    count: u32,
}

#[wasm_bindgen]
impl Counter {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Counter {
        Counter { count: 0 }
    }

    pub fn increment(&mut self) {
        self.count += 1;
    }

    pub fn get_count(&self) -> u32 {
        self.count
    }
}
```

```bash
# Build for browser (generates pkg/ directory with JS + TS + WASM)
wasm-pack build --target web --release

# Build for bundler (webpack, vite, etc.)
wasm-pack build --target bundler --release

# Build for Node.js
wasm-pack build --target nodejs --release
```

### 2. Browser Integration (ES Modules)

```typescript
// Using wasm-pack "web" target
async function initWasm() {
  // Dynamic import of the generated JS glue code
  const wasm = await import("./pkg/my_wasm_lib.js");

  // Initialize the WASM module (required for "web" target)
  await wasm.default();

  // Use exported functions
  const result = wasm.fibonacci(40);
  console.log(`Fibonacci(40) = ${result}`);

  // Use exported struct
  const counter = new wasm.Counter();
  counter.increment();
  console.log(`Count: ${counter.get_count()}`);

  // Free memory when done (WASM objects are not GC'd automatically)
  counter.free();
}
```

```typescript
// React component with WASM
"use client";

import { useEffect, useRef, useState } from "react";

export function WasmProcessor() {
  const wasmRef = useRef<typeof import("./pkg/my_wasm_lib.js") | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    async function loadWasm() {
      const wasm = await import("./pkg/my_wasm_lib.js");
      await wasm.default();
      wasmRef.current = wasm;
      setReady(true);
    }
    loadWasm();
  }, []);

  const processImage = async (imageData: ImageData) => {
    if (!wasmRef.current) return;

    const result = wasmRef.current.process_image({
      width: imageData.width,
      height: imageData.height,
      pixels: Array.from(imageData.data),
    });

    return result;
  };

  return ready ? <div>WASM Ready</div> : <div>Loading WASM...</div>;
}
```

### 3. Vite / Next.js Configuration

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import wasm from "vite-plugin-wasm";
import topLevelAwait from "vite-plugin-top-level-await";

export default defineConfig({
  plugins: [wasm(), topLevelAwait()],
  optimizeDeps: {
    exclude: ["my-wasm-lib"],
  },
});
```

```typescript
// next.config.ts -- enable WASM in Next.js
const nextConfig: NextConfig = {
  webpack(config) {
    config.experiments = {
      ...config.experiments,
      asyncWebAssembly: true,
    };

    // Handle .wasm files
    config.module.rules.push({
      test: /\.wasm$/,
      type: "webassembly/async",
    });

    return config;
  },
};
```

### 4. Web Workers + WASM (Off Main Thread)

```typescript
// worker.ts -- run WASM in a Web Worker to avoid blocking UI
import init, { process_image } from "./pkg/my_wasm_lib.js";

let initialized = false;

self.onmessage = async (event: MessageEvent) => {
  if (!initialized) {
    await init();
    initialized = true;
  }

  const { type, payload } = event.data;

  switch (type) {
    case "process": {
      const result = process_image(payload);
      // Transfer ownership of ArrayBuffer for zero-copy
      self.postMessage(
        { type: "result", payload: result },
        { transfer: [result.processed_pixels.buffer] }
      );
      break;
    }
  }
};
```

```typescript
// main.ts -- use the worker
const worker = new Worker(new URL("./worker.ts", import.meta.url), {
  type: "module",
});

function processImageOffThread(imageData: ImageData): Promise<ProcessResult> {
  return new Promise((resolve) => {
    worker.onmessage = (event) => {
      if (event.data.type === "result") {
        resolve(event.data.payload);
      }
    };
    worker.postMessage({
      type: "process",
      payload: {
        width: imageData.width,
        height: imageData.height,
        pixels: Array.from(imageData.data),
      },
    });
  });
}
```

### 5. WASI (Server-Side WASM)

```typescript
// Run WASM modules with WASI system interface (Node.js 20+)
import { readFile } from "node:fs/promises";
import { WASI } from "node:wasi";

async function runWasi() {
  const wasi = new WASI({
    version: "preview1",
    args: ["my-program", "--flag"],
    env: { NODE_ENV: "production" },
    preopens: {
      "/sandbox": "./data", // Map /sandbox in WASM to ./data on host
    },
  });

  const wasmBuffer = await readFile("./my_module.wasm");
  const wasmModule = await WebAssembly.compile(wasmBuffer);
  const instance = await WebAssembly.instantiate(wasmModule, {
    wasi_snapshot_preview1: wasi.wasiImport,
  });

  wasi.start(instance);
}
```

```rust
// Rust WASI target
// Build with: cargo build --target wasm32-wasip1 --release

use std::fs;
use std::io::Read;

fn main() {
    // WASI provides filesystem, env vars, clock access
    let mut file = fs::File::open("/sandbox/input.txt").unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();

    let processed = contents.to_uppercase();
    fs::write("/sandbox/output.txt", processed).unwrap();

    println!("Processed {} bytes", contents.len());
}
```

### 6. Shared Memory with WASM

```typescript
// Direct memory access for maximum performance
async function processWithSharedMemory(data: Uint8Array) {
  const wasm = await import("./pkg/my_wasm_lib.js");
  await wasm.default();

  // Access WASM linear memory directly
  const memory = wasm.__wbg_get_memory();
  const inputPtr = wasm.allocate(data.length);

  // Copy data into WASM memory
  const inputArray = new Uint8Array(memory.buffer, inputPtr, data.length);
  inputArray.set(data);

  // Process in-place (no copy)
  const outputPtr = wasm.process_buffer(inputPtr, data.length);

  // Read result from WASM memory
  const outputArray = new Uint8Array(memory.buffer, outputPtr, data.length);
  const result = new Uint8Array(outputArray); // copy out

  // Free WASM memory
  wasm.deallocate(inputPtr, data.length);
  wasm.deallocate(outputPtr, data.length);

  return result;
}
```

### 7. Performance Benchmarking

```typescript
// Compare JS vs WASM performance
async function benchmark() {
  const wasm = await import("./pkg/my_wasm_lib.js");
  await wasm.default();

  const iterations = 1000;
  const input = 40;

  // JS implementation
  function fibonacciJS(n: number): number {
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
      [a, b] = [b, a + b];
    }
    return n === 0 ? 0 : b;
  }

  // Benchmark JS
  const jsStart = performance.now();
  for (let i = 0; i < iterations; i++) fibonacciJS(input);
  const jsTime = performance.now() - jsStart;

  // Benchmark WASM
  const wasmStart = performance.now();
  for (let i = 0; i < iterations; i++) wasm.fibonacci(input);
  const wasmTime = performance.now() - wasmStart;

  console.log(`JS:   ${jsTime.toFixed(2)}ms (${iterations} iterations)`);
  console.log(`WASM: ${wasmTime.toFixed(2)}ms (${iterations} iterations)`);
  console.log(`WASM is ${(jsTime / wasmTime).toFixed(1)}x faster`);
}
```

## Best Practices

1. **Profile before reaching for WASM** -- V8 is fast; WASM wins on compute-heavy, tight-loop workloads, not simple logic
2. **Minimize JS-WASM boundary crossings** -- Each call has overhead; batch work into single calls
3. **Use `SharedArrayBuffer` or typed arrays** for large data transfers instead of serializing to JSON
4. **Run WASM in a Web Worker** for heavy computation to keep the main thread responsive
5. **Optimize for size** with `opt-level = "z"`, LTO, and `wasm-opt` (from binaryen) for smaller downloads
6. **Use `wasm-bindgen`** for ergonomic Rust-JS interop rather than raw `extern "C"` bindings
7. **Lazy-load WASM modules** -- Do not include in the critical path; load on first use
8. **Cache compiled modules** -- Use `WebAssembly.compileStreaming()` for browser caching of compiled WASM
9. **Free resources explicitly** -- WASM-exported structs are not garbage-collected; call `.free()` when done
10. **Use `wasm-opt -Oz`** as a post-processing step to further reduce binary size

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Expecting WASM to speed up I/O | No improvement (I/O is JS-bound) | Only use WASM for CPU-bound computation |
| Loading WASM on the main thread synchronously | Blocks rendering | Use `WebAssembly.compileStreaming()` or Web Workers |
| Not freeing WASM-exported objects | Memory leak | Call `.free()` on every `wasm_bindgen` struct |
| Serializing large data as JSON across boundary | Slower than JS-only | Use shared memory / typed arrays |
| Missing CORS headers for `.wasm` files | Module fails to load | Serve with `application/wasm` MIME type and proper CORS |
| Using `opt-level = 3` for WASM | Large binary | Use `opt-level = "z"` or `"s"` for smaller output |
| Calling small WASM functions in a tight JS loop | Overhead dominates | Move the loop into WASM |
| Forgetting `asyncWebAssembly` in webpack/Next.js | Build errors | Enable the experiment in webpack config |

## Examples

### Example 1: Image Processing Pipeline

```
1. User uploads image in browser
2. Decode to ImageData via Canvas API (JS)
3. Transfer pixel buffer to Web Worker (zero-copy with transfer)
4. Worker calls WASM for resize + filter (Rust image crate)
5. Worker posts result back (zero-copy transfer)
6. Render processed image to canvas (JS)

Performance: 2048x2048 grayscale — JS: 180ms, WASM: 12ms
```

### Example 2: Markdown Parser on Edge

```
1. Compile pulldown-cmark (Rust) to WASM with wasm-pack
2. Deploy to Cloudflare Workers (WASM supported natively)
3. Parse markdown to HTML at the edge — 10x faster than JS parsers
4. Cache rendered output at CDN layer

Binary size: 45KB gzipped (after wasm-opt -Oz)
```
