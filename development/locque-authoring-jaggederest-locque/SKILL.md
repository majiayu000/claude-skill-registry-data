---
name: locque-authoring
description: Author or update Locque .lq code and tests with the canonical M-expr syntax, CBPV rules, data/match forms, modules/imports/opens, and project conventions.
---

# Locque authoring

Use this skill when writing or editing Locque source or tests.

## Sources of truth

- `grammar.md` defines the canonical syntax and S-expr mapping.
- `AGENTS.md` lists project conventions and tooling.

## Workflow

1. Prefer `.lq` M-expr files; do not handwrite `.lqs`.
2. Keep paths lowercase. Every `lib/**` file must have a matching `test/**` file.
3. Use `Module::name` qualification; `open Alias exposing ... end` is explicit only.
4. Effects are explicit: computations are values via `compute ... end`, run via `perform`.
5. Multiline constructs must end with `end` (`function`, `compute`, `bind`, `match`, `data`, `typeclass`, `instance`, `module`, `open`, `pack`, `unpack`).
6. Data: `define ... as data ... in TypeN ... end` with constructors `Type::Ctor`; match uses `case Type::Ctor`.
7. No implicit coercions; use `of-type`, `lift`, `up`, `down`, `pack`, `unpack` as needed.
8. Use `ignored` instead of `_` for unused binders.
9. List literals are canonical: `[]` and `[a, b]` (commas required). Empty lists require `of-type [] (List A)` when no expected list type is in scope.

## Test conventions

- Use `assert::assert-eq` with an explicit type argument.
- Run `smyth test` after changes.

## Templates

Function:
```locque
# Assumes: import arithmetic as Ar
define transparent inc as
  function x Natural returns Natural value
    Ar::add x 1
  end
```

Data:
```locque
define transparent Option as data A Type0 in Type0
  case Option::none of-type Option A
  case Option::some of-type for-all x as A to Option A
end
```
