---
name: wasm
description: WebAssembly for high-performance browser code execution
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: web-development
---
## What I do
- Write WebAssembly modules
- Use Rust/AssemblyScript for WASM
- Integrate WASM in web apps
- Optimize performance-critical code

## When to use me
When needing near-native performance in browsers.

## Rust to WASM
```rust
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

```javascript
// Load WASM
const wasm = await WebAssembly.instantiateStreaming(
  fetch('add.wasm')
);
wasm.instance.exports.add(1, 2); // 3
```

## JavaScript WASM Loading
```javascript
async function loadWasm(url) {
  const response = await fetch(url);
  const buffer = await response.arrayBuffer();
  const wasm = await WebAssembly.instantiate(buffer);
  return wasm.instance.exports;
}
```
