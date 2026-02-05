---
name: collimator
description: Guide for using Collimator, a profunctor optics library for Lean 4. Use when writing code with lenses, prisms, traversals, or when accessing/modifying nested data structures.
---

# Collimator Optics Library

## Overview

Collimator is a profunctor optics library for Lean 4. Optics provide composable, type-safe access patterns for nested data structures.

## Imports

```lean
import Collimator.Prelude      -- Core optic types and operations
import Collimator.Operators    -- Haskell-style operators
import Collimator.Combinators  -- Advanced combinators
import Collimator.Instances    -- Instances for List, Option, String

open Collimator
open scoped Collimator.Operators  -- Enable operator syntax
```

## Optic Types

| Optic | Focus | Read | Write |
|-------|-------|------|-------|
| `Iso' s a` | Exactly 1 (reversible) | Yes | Yes |
| `Lens' s a` | Exactly 1 | Yes | Yes |
| `Prism' s a` | 0 or 1 (sum types) | Maybe | Yes |
| `AffineTraversal' s a` | 0 or 1 | Maybe | Yes |
| `Traversal' s a` | 0 or more | List | Yes |

## Operators

```lean
data ^. optic           -- View (Lens, Iso)
data ^? optic           -- Preview optional (Prism, AffineTraversal)
data ^.. optic          -- Collect all (Traversal)
data & optic %~ f       -- Modify with function
data & optic .~ value   -- Set value
```

## Creating Optics

### Lenses (struct fields)

```lean
structure Person where
  name : String
  age : Nat

-- Preferred: use fieldLens% macro
def nameLens : Lens' Person String := fieldLens% Person name
```

### Prisms (sum type constructors)

```lean
inductive JsonValue
  | str : String → JsonValue
  | num : Int → JsonValue

-- Preferred: use ctorPrism% macro
def strPrism : Prism' JsonValue String := ctorPrism% JsonValue.str

-- For Option.some
def somePrism (α : Type) : Prism' (Option α) α := ctorPrism% Option.some
```

## Composition

Optics compose with `∘`. Use `optic%` for type annotations:

```lean
-- Lens ∘ Prism = AffineTraversal
let emailAffine := optic%
  userProfileLens ∘ somePrism Profile ∘ emailLens
  : AffineTraversal' User String

user ^? emailAffine              -- Option String
user & emailAffine %~ toUpper    -- Modify if present
```

## Common Patterns

### Filtering
```lean
[-1, 2, -3, 4] & filteredList (· > 0) %~ (· * 2)  -- [-1, 4, -3, 8]
```

### List operations
```lean
[1, 2, 3] ^? _head                    -- some 1
[1, 2, 3, 4] & taking 2 %~ (· * 10)   -- [10, 20, 3, 4]
```

### Bifunctors
```lean
(3, 5) & both %~ (· * 2)  -- (6, 10)
```

## Built-in Instances

- **List**: `traversed`, `itraversed`, `atLens`, `ix`
- **Option**: `somePrism' α`, `traversed`
- **String**: `chars` (Iso), `traversed`
- **Tuples**: `_1`, `_2`
