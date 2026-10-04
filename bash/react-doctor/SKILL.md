---
name: react-doctor
description: Use when finishing a feature, fixing a bug, before committing React code, or when the user wants to improve code quality or clean up a codebase. Checks for score regression. Covers lint, accessibility, bundle size, architecture diagnostics.
version: "1.0.0"
---

# React Doctor

Scans React codebases for security, performance, correctness, and architecture issues. Outputs a 0–100 health score.

## Commands

```bash
bun run doctor                       # the enforced check; pinned, non-interactive
bunx react-doctor --verbose          # per-file, per-rule detail
bunx react-doctor why <file>:<line>  # why a rule fired, or why a suppression didn't apply
```

Always use the pinned copy (`bun run doctor` / `bunx react-doctor`), never
`npx react-doctor@latest`: the gate runs the pinned version, so a scan on
`@latest` can disagree with CI.

`bun run doctor` exits non-zero on any warning, so there is no score to
eyeball. It is part of `bun run test` and runs in CI, so a regression fails the
PR. For general cleanup, run the `--verbose` scan and fix errors before
warnings.

## Dorkroom specifics

- It scans **four** projects and prints **four** scores: `@dorkroom/source`
  (the app), `@dorkroom/mobile`, `@dorkroom/logic`, `@dorkroom/ui`. All four must be 100.
- The app scan resolves `@dorkroom/*` to package source, so the same physical
  file is reported under both `packages/.../src/...` and bare `src/...` — fix it
  once; verify it's gone from both.
- It **respects inline disables**. Prefer a real fix; only suppress a genuinely
  subjective/false-positive finding, always with a justifying comment:
  `// eslint-disable-next-line react-doctor/<rule> -- why` for native rules, or
  `jsx-a11y/<rule>` for a11y rules. Use `why <file>:<line>` to confirm a
  suppression applies, and check the rule name is current: upstream renames
  rules between versions.
- React Doctor's checks are separate from the gate: a 100 score does **not**
  mean `bun run test` passes (and the gate's typecheck is a no-op on the
  solution tsconfigs). Always run **both** `bun run test` and React Doctor.
- Config lives in **`doctor.config.json`** at the repo root. It ignores
  generated/vendored/non-React trees (`supabase/functions`) and the
  `deslop/unused-*` dead-code rules. Those
  dead-code rules are disabled because react-doctor's import analysis cannot
  resolve this repo's `@/` path alias, Vercel `api/` serverless entrypoints,
  Vitest manual mocks (`__mocks__`), `.mjs` build scripts, or shell-script CLI
  usage (e.g. `turbo-ignore` in `scripts/should-deploy.sh`, `lucide-static` in
  `apps/mobile/scripts/generate-tab-icons.mjs`) — so it reports those as
  "unused" false-positives. Circular-import detection stays on.
- **Re-check every rule ignore in `doctor.config.json` on each react-doctor
  upgrade.** Ignores added for upstream false positives go stale once upstream
  fixes the rule.
