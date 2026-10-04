---
name: rca-component-structuring
description: >-
  Use when writing a new React UI component or growing an existing one and the rust-code-analysis
  complexity gate must pass first time — symptoms include the metrics target mapped by
  `make.lint_metrics` reporting lloc_function, nargs_function, cyclomatic, nom_functions_file,
  lloc_file or halstead_volume over its limit, a component file that has grown past roughly 120
  logical lines, a render body doing hook wiring plus styling plus SVG, or a plan to split a
  component into files before the gate is run.
---

# RCA-compliant component structuring

## Profile keys consumed

- `make.lint_metrics`
- `quality.metrics_enforced`
- `make.lint_tsc`
- `make.lint_eslint`
- `make.format`
- `make.test_unit_client`
- `quality.coverage_statements`
- `architecture.source_root`
- `architecture.component_prefix`

The authoritative reading of the gate is the target mapped by `make.lint_metrics`, enforced when
`quality.metrics_enforced` is true; skip it with a recorded note when the key maps to `null` and say
so rather than guessing the verdict.

## Overview

The complexity gate is thresholded per function **and** per file, so component size is a layout
decision, not a cleanup step. Choosing the file split up front — and copying an already-passing
component's shape — is what makes the gate a formality instead of a rework loop.

## When to use

- Starting a new component and deciding which files it needs.
- The target mapped by `make.lint_metrics` fails on a component with a length, argument-count,
  function-count or Halstead finding.
- A single `index.tsx` has absorbed the hook, the styles, the SVG and the dev warnings.
- Not for: non-component logic modules, or tuning the thresholds themselves — the policy file is a
  reviewed contract, never edited to clear a finding.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — `config/metrics-policy.json`, the target mapped by `make.lint_metrics`, components
  under the source root's prefixed component folders (`architecture.component_prefix`, e.g.
  `src/components/ui-*`), unit tests under `tests/unit/`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — identical
  `config/metrics-policy.json` values and the same mapped metrics target; components under
  `<source root>/components`, tests under `src/test/`.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — identical
  policy values; the mapped metrics target runs in a container, each component owns a folder under
  the source root's prefixed component folders, and every test lives under `tests/`.

## Ceilings that drive the layout

All three repository shapes ship the same `hard` block. The ones that shape a component:

| Metric                       | Limit |
| ---------------------------- | ----- |
| Logical lines per function   | 10    |
| Parameters per function      | 3     |
| Cyclomatic / cognitive       | 10/15 |
| Exit points per function     | 3     |
| Functions per file           | 10    |
| Closures per file            | 6     |
| Functions plus closures      | 15    |
| Logical lines per file       | 120   |
| Halstead volume per function | 1000  |

## Standard component layout

One folder per component, each file carrying one concern:

- `index.tsx` — the `forwardRef` wrapper plus a wired and a static render function.
- `types.ts` — interfaces only, no runtime code.
- `styles.ts` — `sx` builders and style constants.
- `<name>-content.tsx` — the shared label plus glyph tree both render paths use.
- `<name>-glyph.tsx` — the SVG path and its wrapper. Never inline an SVG in `index.tsx`.
- `use-<name>.ts` — the view model, defaults, and activation gating.
- `<name>-warnings.ts` — development-time warnings.
- `<name>.stories.tsx` — the story, excluded from coverage.

## Core pattern

Two small render functions plus a thin dispatch keeps every function under the line ceiling, and a
single props object keeps every one of them at one parameter — well inside the limit of three.

```ts
interface AddButtonShellProps {
  button: UiAddButtonProps;
  model: AddButtonModel;
  buttonRef: React.ForwardedRef<HTMLButtonElement>;
  sx: SxProps<Theme>;
}

function WiredAddButton({ button, model, buttonRef, sx }: Readonly<AddButtonShellProps>) {
  return (
    <Box component="button" type="button" aria-disabled={model.ariaDisabled}
         onClick={model.onActivate} ref={buttonRef} sx={sx}>
      <AddButtonContent label={model.label} />
    </Box>
  );
}

const UiAddButton = React.forwardRef<HTMLButtonElement, UiAddButtonProps>((props, ref) => {
  const model = useAddButton(props);
  const sx = addButtonSx({ interactive: model.interactive, sx: props.sx });
  return model.interactive
    ? <WiredAddButton button={props} model={model} buttonRef={ref} sx={sx} />
    : <StaticAddButton button={props} model={model} buttonRef={ref} sx={sx} />;
});
```

The activation guard lives in the hook, not the JSX, so the disabled branch never reaches the DOM
layer. More splitting patterns — style helpers, Halstead extraction, and the load-bearing
destructure gotcha — are in [patterns.md](patterns.md).

## Verify before pushing

Aim for full statement, branch, function and line coverage on every executable file — the floor
named by `quality.coverage_statements`; `types.ts` and `*.stories.tsx` are already excluded from the
coverage scope in all three repository shapes. Test the hook apart from the JSX. Then run the
targets mapped by `make.lint_tsc`, `make.lint_eslint`, `make.format` and `make.test_unit_client` for
the component's files, and finish with the target mapped by `make.lint_metrics`, which is the only
authoritative reading of the gate.

## Common mistakes

- Writing the whole component in `index.tsx` and splitting after the gate fails; the split then
  fights already-written tests.
- Inventing a novel file layout instead of copying a component that already passes.
- Adding a fourth parameter rather than grouping the related fields into one props object.
- Deleting a destructure that looks unused — see the gotcha in the patterns reference.
- Treating a file-level function-count finding as a naming problem; it means a file needs splitting.
