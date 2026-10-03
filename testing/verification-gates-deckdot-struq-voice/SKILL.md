---
name: verification-gates
description: "The verification tiers and gate commands for Struq Voice. Use whenever finishing a slice, before a commit, or when asked to 'verify', 'run the gates', 'typecheck', 'lint', 'run tests', 'which tier is this', or 'check it works'. Knows the T1/T2/T3 tier table and which tier a change takes, runs pnpm typecheck, pnpm lint, pnpm test and the boot smoke, knows that pnpm test:e2e must NOT be run unprompted (slow, flaky hook spec), and how to clean up stray Electron processes. NOT for understanding the codebase (use project-context), for branching and PRs (use github-workflow), or for cutting a release (use shipping-a-release)."
argument-hint: "[tier | typecheck | lint | test | smoke]"
---

# Verification gates for Struq Voice

Pick the lowest tier that fully covers the change, then run it. The tier also
decides who may merge, which is why guessing low is not a shortcut.

## The tiers

| Tier | Scope | Proof | Merges |
|---|---|---|---|
| T1 | docs, copy, screenshots, comments | `pnpm typecheck && pnpm lint` | agent, once CI is green |
| T2 | renderer views, state machines, IPC, engines, post-processing | T1 + `pnpm test` | Roy |
| T3 | native modules, updater, paste, meeting worker, release scripts | T2 + `pnpm smoke:boot`, and say what was observed | Roy |

Four rules that fall out of the table:

- **A branch takes the highest tier it touches.** One line in `paste.ts`
  makes the whole branch T3.
- **A change to a skill, to `AGENTS.md`, or to this table is never T1.** It
  changes how everything after it runs.
- **Tier up when unsure.** The cost of a tier too high is two minutes.
- **Report what was run AND what was deliberately not run.** A gate nobody
  can see the output of is a claim, not a check.

## The gates

```bash
pnpm typecheck    # tsc --noEmit -p tsconfig.node.json && web && e2e
pnpm lint         # eslint . (typescript-eslint strictTypeChecked)
pnpm test         # vitest run (risk-weighted unit suite)
```

Zero errors. There is no softer bar within a tier.

## Boot smoke (T3)

```bash
pnpm smoke:boot
```

The script expects the production bundle to stay alive for ten seconds. It
uses isolated user data, hides the window, kills only its own process tree, and
removes its temporary files. Electron 39 for Windows does not accept a
`--headless` command-line switch.

This is the gate that catches a broken quit or a native module that fails to
load, neither of which any unit test sees.

## e2e: a deliberate probe, never automatic

`pnpm test:e2e` builds and runs Playwright. It is headless but slow, and
`hook.spec.ts` needs a real microphone and real OS focus, so it fails in
isolation on machines without a mic or with hook contention.

**Do not run it unprompted, at any tier.** Roy runs it himself. Do not "fix"
the e2e specs without being asked. A gate that flakes is a gate that gets
switched off, which is why this one stays opt-in rather than being wired into
T3.

## Cleanup

Always kill stray processes after any smoke or manual launch:

```bash
taskkill //F //IM electron.exe
taskkill //F //IM "Struq Voice.exe"
```

## Lint pitfalls that come up often

- No async functions without an await (add `await Promise.resolve()` in
  fakes).
- No returning a void expression from an arrow shorthand; wrap in braces.
- Template literals with numbers need `String(n)`.
- No unnecessary type assertions or conditionals the checker can prove.
- No unused imports or variables (names must match `/^_/` to be exempt).
- `noUncheckedIndexedAccess`: index arrays only after a bounds check.
- `exactOptionalPropertyTypes`: do not set optional fields to `undefined`.
