---
name: syrup
description: Syrup binary serialization for OCapN/CapTP wire format. Canonical encoding for capability messages.
version: 1.0.0
---

# Syrup: Binary Serialization for OCapN

**Trit**: -1 (MINUS - constraining/validating serialization)
**Color**: #8B4513 (Saddlebrown - like syrup)
**Source**: [ocapn/syrup](https://github.com/ocapn/syrup)

---

## Overview

Syrup is a lightweight binary serialization format for the [OCapN](https://github.com/ocapn/ocapn) (Object Capability Network). It provides canonical encoding - the same data always serializes to identical bytes - making it suitable for hashing, signing, and capability transport.

**Core principle**: Simple, canonical, easy to implement across languages.

---

## Type Encoding Reference

| Type | Format | Example |
|------|--------|---------|
| Boolean | `t` or `f` | `t` = true |
| Positive int | `<digits>+` | `42+` |
| Negative int | `<digits>-` | `123-` = -123 |
| Bytestring | `<len>:<bytes>` | `3:cat` |
| String | `<len>"<utf8>` | `5"hello` |
| Symbol | `<len>'<utf8>` | `3'foo` |
| Float | `F<4 bytes>` | IEEE 754 single |
| Double | `D<8 bytes>` | IEEE 754 double |
| List | `[<items>]` | `[3+4+5+]` = [3,4,5] |
| Dict | `{<k><v>...}` | `{3"age12+}` |
| Set | `#<items>$` | `#3:a3:b$` |
| Record | `<<label><args>>` | `<4"date2024+5+1+>` |

---

## Installed Implementations

### Python

```python
# pip install via: gh repo clone ocapn/syrup && cd syrup/impls/python
from syrup import syrup_encode, syrup_decode, Symbol, record

# Encode
syrup_encode({"name": "alice", "age": 30})
# => b'{3"age30+4"name5"alice}'

# Decode  
syrup_decode(b'{3"age30+4"name5"alice}')
# => {'age': 30, 'name': 'alice'}

# Symbols (for Lisp-like keys)
syrup_encode({Symbol('species'): b'cat'})
# => b"{7'species3:cat}"

# Records (custom types)
syrup_encode(record('date', 2024, 5, 1))
# => b'<4"date2024+5+1+>'
```

### Guile Scheme

```scheme
;; Install: copy syrup.scm to your Guile load path
(use-modules (syrup))

;; Encode
(syrup-encode 42)
;; => #vu8(52 50 43)  ; "42+"

(syrup-encode '("hello" "world"))
;; => #vu8(91 53 34 104 101 108 108 111 53 34 119 111 114 108 100 93)

;; Decode
(syrup-decode #vu8(52 50 43))
;; => 42

;; Records
(syrup-encode (make-syrec* (string->utf8 "date") 2024 5 1))
```

### Racket

```racket
#lang racket
(require syrup)

;; Encode
(syrup-encode #hash(("name" . "alice") ("age" . 30)))
;; => #"{3\"age30+4\"name5\"alice}"

;; Decode
(syrup-decode #"{3\"age30+}")
;; => #hash(("age" . 30))

;; Records
(syrup-encode (record* #"date" 2024 5 1))
;; => #"<4:date2024+5+1+>"

;; Marshalling custom types
(struct point (x y) #:transparent)
(syrup-encode (point 1 2)
              #:marshallers (list (cons point? 
                                       (λ (p) (record* 'point (point-x p) (point-y p))))))
```

**Package**: `syrup` (installed via `raco pkg`)

---

## Canonical Property

Syrup guarantees canonical encoding:

1. **Dictionaries**: Keys sorted by their serialized byte representation
2. **Sets**: Items sorted by their serialized byte representation
3. **No duplicate keys**: Dicts must not contain the same key twice

This means: `hash(syrup_encode(x)) == hash(syrup_encode(y))` iff `x == y`

---

## Backwards Compatibility

Syrup decoders accept:
- **Bencode**: `d3:agei12ee` → dict
- **Canonical S-expressions**: `(3:foo 3:bar)` → list

```python
# Bencode
syrup_decode(b'd3:agei12e4:name5:Missye')
# => {b'age': 12, b'name': b'Missy'}

# S-expressions
syrup_decode(b'(3:cat 7:tabatha)')
# => [b'cat', b'tabatha']
```

---

## GF(3) Triads

```
# Wire Format Bundle
syrup (-1) ⊗ captp (0) ⊗ gay-mcp (+1) = 0 ✓  [Colored Capabilities]
syrup (-1) ⊗ localsend-mcp (0) ⊗ tailscale-file (+1) = 0 ✓  [P2P Transfer]
syrup (-1) ⊗ beeper-mcp (0) ⊗ agent-o-rama (+1) = 0 ✓  [Message Encoding]

# Serialization Stack
syrup (-1) ⊗ preserves (0) ⊗ json (+1) = 0 ✓  [Format Spectrum]
```

---

## Commands

```bash
# Python (after installing to PYTHONPATH)
python3 -c "from syrup import *; print(syrup_encode({'test': 42}))"

# Guile (after installing to load path)
guile -c "(use-modules (syrup)) (display (syrup-encode 42))"

# Racket (after raco pkg install)
racket -e "(require syrup) (displayln (syrup-encode #hash((\"x\" . 1))))"
```

---

## Use Cases

| Use Case | Why Syrup |
|----------|-----------|
| **CapTP messages** | Wire format for capability transport |
| **Content addressing** | Canonical = deterministic hashes |
| **Signing** | Sign serialized form, verify anywhere |
| **Storage** | Compact binary, self-describing |
| **Cross-language** | Same bytes from Python/Guile/Racket |

---

## Related Skills

| Skill | Relation |
|-------|----------|
| **captp** | CapTP uses Syrup as wire format |
| **preserves** | Syrup is a Preserves serialization |
| **localsend-mcp** | P2P transfer could use Syrup |
| **acsets** | Serialize ACSets with Syrup |

---

## Installation

```bash
# Clone the repo
gh repo clone ocapn/syrup

# Python: add to PYTHONPATH or copy syrup.py
cp syrup/impls/python/syrup.py ~/.local/lib/python3/

# Guile: copy to load path
cp syrup/impls/guile/syrup.scm ~/.local/share/guile/site/3.0/

# Racket: install package
cd syrup/impls/racket && raco pkg install syrup/
```

---

## References

- [OCapN Organization](https://github.com/ocapn/ocapn)
- [Preserves Data Model](https://preserves.gitlab.io/preserves/)
- [Spritely Institute](https://spritely.institute/)
- [Draft Specification](https://github.com/ocapn/syrup/blob/main/draft-specification.md)

---

**Skill Name**: syrup  
**Type**: Binary Serialization Format  
**Trit**: -1 (MINUS)  
**GF(3)**: Constrains data to canonical form  
**Invariant**: Same data → same bytes, always


## ACP atlas

Part of: `acp-commons`.
