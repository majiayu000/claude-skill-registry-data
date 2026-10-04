---
model_tier: inherit
name: design-tokens
description: "Author a 3-layer DTCG token system (primitive → semantic → component) with light/dark theming; generate CSS vars + Tailwind colors and lint hardcoded values. Use on design tokens / CSS variables."
domain: engineering
personas:
  - frontend-engineer
workspaces:
  - engineering
packs:
  - frontend-design
trust:
  level: professional
install:
  removable: true
scope:
  write: []
  verification_reason: "execution declares no handler, so this skill runs nothing of its own — every write is the calling agent's, under the rules that govern it. No command can prove a scope the skill never executes."
execution:
  type: manual
---

# design-tokens

> Token *authoring* skill: the 3-layer DTCG model
> (**primitive → semantic → component**) with light/dark theming, a
> TypeScript toolchain (`scripts/tokens.ts` — generate / validate /
> embed, run via ./scripts-run), and a starter template. Selection of
> *which* token values fit the product comes grounded from
> [`design-intelligence`](../design-intelligence/SKILL.md) (WCAG-adjusted
> color sets, typography pairings); this skill turns the selection into a
> maintained token system.

Toolchain provenance: port of the upstream `.cjs` trio
(`generate-tokens`, `validate-tokens`, `embed-tokens`) from
`nextlevelbuilder/ui-ux-pro-max-skill` `design-system` sub-skill
@ `b7e3af80f6e331f6fb456667b82b12cade7c9d35` (MIT, last checked
2026-06-07); the HTML surface of upstream's `html-token-validator.py` is
folded into `validate` so there is exactly **one** token-discipline
linter. Obligations: [`design-intelligence/ATTRIBUTION.md`](../design-intelligence/ATTRIBUTION.md).

## When to use

- A project needs a token system (new design system, theme overhaul,
  dark-mode introduction).
- Hardcoded hex/px/rem values keep leaking into components — wire the
  validate linter into review/polish.
- The design brief landed WCAG-checked values that must become
  maintainable CSS variables / Tailwind theme entries.

## The 3-layer model

| Layer | Names | References | Example |
|---|---|---|---|
| **Primitive** | raw scales | literal values only | `primitive.color.blue.600 = #2563EB` |
| **Semantic** | meaning | primitives via `{primitive.…}` | `semantic.color.primary = {primitive.color.blue.600}` |
| **Component** | per-widget | semantics via `{semantic.…}` | `component.button.bg = {semantic.color.primary}` |

Rules: components never reference primitives directly; dark mode lives
under `dark.semantic.*` overriding the same semantic names (emitted as a
`.dark { … }` block); every value is a `{"$value": …, "$type": …}` pair
(DTCG). Start from
[the bundled starter template](templates/design-tokens-starter.json).

## Toolchain (`scripts/tokens.ts` — skill-relative, any cwd)

```bash
# tokens.json → CSS variables (primitives + semantic + components + .dark)
./scripts-run <skills-root>/design-tokens/scripts/tokens generate \
  --config tokens.json -o assets/design-tokens.css

# tokens.json → Tailwind theme.extend.colors snippet
./scripts-run …/tokens generate --config tokens.json --format tailwind

# token-discipline lint: hardcoded hex/rgb/px/rem outside token files
./scripts-run …/tokens validate --dir src/ [--json]

# embeddable inline CSS for standalone HTML artifacts
./scripts-run …/tokens embed --tokens assets/design-tokens.css --minimal --style
```

`validate --json` emits findings with `"kind": "token_violation"` — the
exact finding kind the UI directive set's polish step auto-converts
against `state.ui_audit.design_tokens`. Wire it into review/polish runs:
scan the changed files, append the findings to
`state.ui_review.findings`, and let the polish round fix them
(`var(--token)` over hardcoded hex — the validation rule the council's
four-operation split assigns to *rules/linters*, not the corpus).

**Set `artifact_covered: true` on a finding whose value traces to a provided
design artifact.** Without it the polish round edits AWAY from the artifact:
`polish.ts::partition_artifact_covered` drops flagged findings and treats every
unmarked one as actionable, and this path appended `token_violation` findings
without the flag — so a hex the handover states was converted to a project token
by a loop nobody asked. The flag is per finding, not per run: a hardcoded hex
the artifact never mentioned stays actionable and is still fixed. Marking is not
suppression — the finding stays in the report as informational, so a reader
still sees that the spec carries a value the token system does not.
(AI council 2026-09-09 on `blocker: findings-actionability-default`, option (b):
one call site, no package-wide default changed. Reopens if a second
artifact-derived finding path reaches the loop without provenance — recurrence
would argue for carrying provenance in the finding TYPE rather than at a third
call site.)

## Procedure

1. **Inspect the existing styling surface** — detect the stack (Tailwind
   config, global CSS, component conventions) and survey current
   hard-coded values, so the token set covers what the codebase
   actually uses.
2. **Ground the values** — `design-intelligence` query gives the
   WCAG-checked semantic color set + typography pairing for the product.
   No brand and no corpus match (a genuinely from-scratch palette) →
   derive the accent set in `oklch()` with shared lightness and chroma,
   varied hue (`oklch(50% 0.15 250)` / `… 200` / `… 280`) — equal L/C
   keeps the hues perceptually balanced where random hex codes drift in
   saturation; cross-check the result against C1/C5 avoidance before
   locking it in.
3. **Author `tokens.json`** from the starter: fill primitives, point
   semantics at them, add `dark.semantic` overrides.
4. **Generate** CSS vars (and the Tailwind snippet when the stack is
   Tailwind — see [`tailwind-engineer`](../tailwind-engineer/SKILL.md)).
5. **Validate** the codebase; convert violations to `var(--token)`.
6. Re-run `validate` until clean — exit code 0 is the evidence.

## Output format

1. `tokens.json` (DTCG, 3 layers + `dark.semantic`).
2. Generated `design-tokens.css` (+ Tailwind `theme.extend.colors`
   snippet when the stack is Tailwind).
3. `validate` report — exit 0 evidence, or the violations list handed to
   the polish round as `token_violation` findings.

## Security constraints

`scripts/tokens.ts` is the only shipped script.

- **What it may touch** — the `tokens.json` config path it is given, the
  directory it is asked to `validate`, and the `--output` path it is asked
  to write. Nothing outside the paths named on the command line.
- **What it must never do** — reach the network, spawn a subprocess, or
  write to a path the caller did not name. It never edits the generated CSS
  it produced earlier; regeneration replaces, it does not patch.
- **Default invocation** — read-only. `generate` prints to stdout unless
  `--output PATH` is passed; `--output` is the flag that makes it mutating,
  and it creates only that file's parent directory. `validate` never writes.
- **Outbound** — nothing. No network access.

## Do NOT

- Do NOT hand-edit generated CSS — `tokens.json` is the single source.
- Do NOT let components reference primitives directly — semantic layer
  in between, always.
- Do NOT auto-fix validate findings blindly — `#000`/`#fff` and
  runtime-computed values are legitimate; review each.
- Do NOT port the brand→token pipeline without the watch-note trigger
  (deferred per council).

## Gotchas

- `validate` intentionally skips `#000`/`#fff`(+6-digit forms), values on
  lines already using `var(--…)`, comments, token-definition files, and
  known external asset hosts — review its output, don't blindly allowlist.
- Brand→token sync (`brand-guidelines.md` → scale generation) is
  **deferred** per council 2026-06-07 (fork D2) — watch note:
  `agents/settings/contexts/domain-watch/brand-token-pipeline.md`.
- Keep `tokens.json` the single source; never hand-edit the generated CSS.

## See also

- [`design-canon.md`](../../../docs/guidelines/design-canon.md) § Colour references — a11y-contrast + culturally-specific palettes + named-system token models.
- [`design-intelligence`](../design-intelligence/SKILL.md) — grounded value selection.
- [`tailwind-engineer`](../tailwind-engineer/SKILL.md) — utility-discipline consumer.
- [`react-shadcn-ui`](../react-shadcn-ui/SKILL.md) — shadcn token conventions.
- [`docs/guidelines/design-antipatterns.md`](../../../docs/guidelines/design-antipatterns.md) — when authoring the colour layer, avoid the C5 cream/sand default palette (OKLCH L 0.84–0.97, C < 0.06) and C1 purple/violet primaries unless the brand explicitly defines them; the `brand-consistency` rule validates emitted tokens against the active brand profile.
