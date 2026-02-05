---
name: manage-reatom-stores
description: Create or update Reatom stores in this repo. Use when adding a new store under `src/stores`, changing store state shape, adding computed atoms, or creating/updating related store service functions.
---

# Manage Reatom Stores

Follow these steps to create or update stores using the existing appSession patterns.

## 1) Define or update state types

Create or update the state interface in `src/api/*` when the store shape is shared or reused.

Example:

```ts
export interface Movie {
  id: string
  title: string
  year: number
  tags?: string[]
}
```

## 2) Create or update the store atom

Add a new file in `src/stores/*` or update the existing atom.

Example:

```ts
import { atom, computed } from '@reatom/core'
import { Movie } from '../api/movie'

export const moviesAtom = atom<Movie[]>([])

export const movieCountAtom = computed(() => moviesAtom().length)
```

Keep initial state explicit, and prefer small, focused atoms.

## 3) Add or update service functions (if needed)

If store updates involve side effects or async logic, place functions in `src/stores/*.service.ts` and mutate state via `*.set`.

Example:

```ts
import { moviesAtom } from './movies'

export function addMovie(movie: Movie): void {
  moviesAtom.set((movies) => [...movies, movie])
}
```

## 4) Update usages

Search for all usages and update them to match the new store shape.

Use:
- `rg -n "moviesAtom|movieCountAtom|addMovie" src`

## 5) Keep types strict and clean

Ensure no unused imports or params remain, and that `strict` TypeScript checks pass.
