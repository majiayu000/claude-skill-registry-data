---
name: cross-driver-parity
description: Preserve behavior and single sources across Windows, macOS, Linux, and web. Use when a change affects more than one driver.
---

# Cross-driver parity

## The layout

```
static/ergopti_plus/
├── _shared/      canonical data + logic shared by every driver
│   ├── core/  data/  lua/  modules/  tap_hold/  tests/  ui/
├── windows/      AHK v2 driver
├── macos/        Hammerspoon / Lua driver
├── linux/        Lua driver
└── extensions/
```

`_shared/` is the source of truth. Each layer resolves the shared root in exactly
one place — but per `project-shared-tree-layout` in
`docs/memory/shared-architecture.md`, several sites
bypass that SSOT, so **only the test suites catch a rename**. Never assume a move
is safe because the code compiles.

## The rule

When you change a value, default or behaviour that more than one driver
implements, you must either:

1. **Move it into `_shared/`** and have every driver read it from there, or
2. **Add a single-source test** that pins the copies together so drift fails CI.

Never leave two hand-maintained copies with no test between them. That is how
"fixed on Windows, still broken on macOS" ships.

## The enforcement suites

All of these run inside `npm run test:js` — you do not invoke them individually
in normal work, but knowing what they cover tells you which one your change will
trip:

| Family                                              | What it pins                                                                                                       |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `test:port-compliance`                              | ported logic matches its source driver                                                                             |
| `test:priority-parity`                              | resolution priority identical across drivers                                                                       |
| `test:manifest-parity`, `test:manifest-equivalence` | feature/menu manifests agree                                                                                       |
| `test:*-single-source`                              | one constant, one home (LLM defaults, temperature, max-tokens, Ollama port, versions, WPM, keycodes, buffer caps…) |
| `test:no-fallback-literals`                         | no hardcoded fallback shadowing a configured value                                                                 |
| `test:git-mv-resilience`, `test:doc-paths`          | path references survive moves                                                                                      |

The `*-single-source` family is the template: when you introduce a new shared
constant, **add its single-source test in the same commit**. Copy the closest
existing one in `tools/test/` — they are deliberately near-identical.

## Manifests and codegen

Several artifacts are generated, not hand-written — `npm run build:manifest`,
`build:menu`, `build:domain`, and the `codegen:*` scripts (terminators, prompt
builders, LLM profile data, keycode data, contracts). If you hand-edit a
generated file your change is reverted on the next build **and** the parity test
fails. Edit the source and regenerate.

## Running the other drivers' suites

```bash
npm run test:hs       # macOS Lua
npm run test:linux    # Linux Lua
```

Run the suite for every driver you touched, plus `npm run test:js` which holds
the cross-driver gates. See `ship-fix` for the full gate.

## Known intentional asymmetries

Do not "fix" these — they are documented decisions in the routed topics under
`docs/memory/`:

- macOS does not read `menu_manifest.json`'s `hotstrings_menu` / `layout_menu`
  keys (a drift gate exists; the migration does not).
- Per-driver tooltip border alphas differ on purpose.
- The Windows VK-keyed finger map is a deliberate third copy left untouched by DC-1.
- AHK vs Hammerspoon word-boundary framing diverges by design.

Check `docs/memory/README.md` before assuming a difference is a bug.
