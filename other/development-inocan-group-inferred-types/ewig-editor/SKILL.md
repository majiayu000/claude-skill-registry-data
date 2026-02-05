---
name: ewig-editor
description: The eternal text editor — Didactic Ersatz Emacs demonstrating immutable
version: 1.0.0
---


# Ewig - Eternal Didactic Text Editor

The eternal text editor — Didactic Ersatz Emacs demonstrating immutable data-structures and the single-atom architecture.

## Repository
- **Source**: https://github.com/bmorphism/ewig (fork of arximboldi/ewig)
- **Language**: C++ (immer library)
- **Pattern**: Persistent data structures + single atom state

## Core Concept

Ewig demonstrates how to build a text editor using:
1. **Immutable data structures** - All state changes create new versions
2. **Single-atom architecture** - One atom holds the entire application state
3. **Structural sharing** - Efficient memory via shared structure

```cpp
// Single atom state
atom<editor_state> state;

// All mutations are pure transformations
state.update([](editor_state s) {
    return s.insert_char('x');  // Returns new state, doesn't mutate
});
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                      Ewig                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│   ┌─────────────────────────────────────────────┐   │
│   │              Single Atom                    │   │
│   │         (immutable editor_state)            │   │
│   └─────────────────────────────────────────────┘   │
│        │                              │             │
│        ▼                              ▼             │
│   ┌─────────┐                    ┌─────────┐       │
│   │ immer   │   structural       │ lager   │       │
│   │ vectors │   sharing          │ cursors │       │
│   └─────────┘                    └─────────┘       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Key Libraries

### immer
Persistent immutable data structures for C++:
```cpp
#include <immer/vector.hpp>

immer::vector<char> buffer = {'h', 'e', 'l', 'l', 'o'};
auto new_buffer = buffer.push_back('!');  // O(log n), shares structure
```

### lager
Unidirectional data-flow architecture:
```cpp
auto store = lager::make_store<action>(
    model{},
    lager::with_reducer(update),
    lager::with_effect(effect)
);
```

## Relevance to CRDT/Collaborative Editing

Ewig's immutable architecture aligns with CRDT principles:

| Ewig Concept | CRDT Parallel |
|--------------|---------------|
| Immutable state | Operation-based CRDT |
| Structural sharing | Delta-state CRDT |
| Single atom | Causal consistency |
| Pure transformations | Commutative operations |

## Integration with crdt-vterm-bridge

The single-atom pattern can be applied to terminal state:

```cpp
// Terminal state as immutable atom
struct terminal_state {
    immer::flex_vector<line> lines;
    cursor_pos cursor;
    gf3_trit trit;  // GF(3) assignment
};

atom<terminal_state> term_state;
```

## Building

```bash
git clone https://github.com/bmorphism/ewig
cd ewig
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make
./ewig
```

## Related Skills
- `code-refactoring` - Immutable refactoring patterns
- `bisimulation-game` - State equivalence
- `gay-mcp` - Deterministic UI coloring



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.