---
name: pfc5-fish
description: Author and audit PFC 5.0 FISH for asphalt cases, including def/end functions, globals and locals, callbacks, numbered histories, object traversal, command blocks, IO, and stop logic.
---

# PFC5 FISH

Use this skill when a PFC 5.0 asphalt case needs FISH functions, callbacks,
histories, traversal, IO, controllers, or stop conditions.

## Required Inputs

- PFC2D/PFC3D 5.0 and target stage;
- object types and identifiers/groups;
- inputs, intended globals, outputs, callback timing, and stop rule;
- expected history/file schema and runtime probe.

## Workflow

1. Write the function contract before code: inputs, globals, return symbol, side effects.
2. Prefer the documented PFC5 `define name ... end` spelling and explicit command
   blocks; accept `def` only as a verified abbreviation in retained legacy sources.
3. Keep intentional globals few; initialize callback state before activation.
4. Use numbered `history id` outputs and document each ID.
5. Guard object pointers and empty collections.
6. Use either `whilestepping` (automatic registration at `-1.0`) or an explicit
   `set fish callback`; prove the expected call count with a counter/history.
7. Inspect callback registrations after restore and remove/re-register only from
   evidence; one removal clears only one duplicate registration.
8. Run `scripts/audit_pfc5_fish.py`, then a minimal PFC5 runtime probe.

Read [patterns.md](references/patterns.md) for maintained skeletons.

## Working Rules

- Do not mix syntax families in one block.
- Do not leave controller functions defined but never activated.
- Do not explicitly register a `whilestepping` function a second time unless double
  execution is intentional.
- Do not put unwrapped PFC commands directly inside a FISH function.
- Inline evaluation belongs at command level, not inside FISH expressions.
- Static delimiter checks do not validate intrinsic names.

## Output Contract

Return function/global/history/callback maps, source files, audit result,
activation proof, and runtime-validation status.

## Local Contents

- `references/patterns.md` — PFC5 function/history/callback patterns.
- `scripts/audit_pfc5_fish.py` — syntax-family and block-balance audit.
- `agents/openai.yaml` — interface metadata.
