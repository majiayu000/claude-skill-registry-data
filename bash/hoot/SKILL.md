---
name: hoot
description: Scheme→WebAssembly compiler (4K lines info).
metadata:
  trit: 0
---

# hoot

Scheme→WebAssembly compiler (4K lines info).

## Compile

```bash
guild compile-wasm -o out.wasm script.scm
```

## Features

- Full tail call optimization
- First-class continuations
- JavaScript interop
- Standalone Wasm modules

## Example

```scheme
(define-module (my-module)
  #:export (greet))

(define (greet name)
  (string-append "Hello, " name "!"))
```

## Runtime

```javascript
import { Hoot } from '@aspect/guile-hoot';
const mod = await Hoot.load('out.wasm');
mod.greet("World");
```


## REPL atlas

Part of: `repl-commons`. Family canonical: `guile`.
