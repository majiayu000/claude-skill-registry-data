---
name: knip-dead-code
description: "Run Knip against a JS/TS project to detect unused files, unused dependencies, unused exports, and unused class/enum members. Scoped to production code; tests are entry-point-aware via Knip's framework plugins. Use after a feature or route is deleted and the project still compiles, or when `package.json` has accumulated dependencies nobody can account for."
metadata:
  keywords: "knip, dead-code, unused-exports, unused-dependencies, typescript"
  version: "1.1.5"
---

# knip-dead-code

Knip detects unused files, dependencies, exports, types, enum members,
and class members in JS/TS projects per the [Knip docs]. Requires
Node ≥ 20.19.0 (or Bun).

## When to use

- After a feature deletion when "everything still compiles" but you
  suspect dead code.
- Periodic cleanup to remove unused npm dependencies (security +
  bundle-size win).
- Pre-merge gate to prevent new dead exports from accumulating.

## Step 1 - Install

```bash
# Recommended: setup wizard (auto-detects framework)
npm init @knip/config

# Manual
npm install -D knip typescript @types/node
```

Add `package.json` script:

```json
{
  "scripts": {
    "knip": "knip"
  }
}
```

Per the [Knip docs].

## Step 2 - Configure entry points

`knip.json`:

```json
{
  "$schema": "https://unpkg.com/knip@5/schema.json",
  "entry": [
    "src/index.ts",
    "src/cli.ts",
    "scripts/**/*.ts"
  ],
  "project": ["src/**/*.{ts,tsx}"],
  "ignore": ["src/**/*.generated.ts"],
  "ignoreDependencies": [
    "@types/node"
  ],
  "ignoreExportsUsedInFile": true
}
```

Or `knip.config.ts` for typed config.

**Entry vs project:** `entry` = files Knip starts walking the import
graph from. `project` = the universe of files it considers reachable.
Anything in `project` not reached from `entry` is unused.

## Step 3 - First run

```bash
npx knip
```

Exit code: 0 if clean, non-zero if unused items found. Shows:

```
Unused files (3)
Unused dependencies (2)
Unused exports (12)
Unused exported types (4)
Unused exported enum members (1)
```

## Step 4 - Use framework plugins

For framework-aware scanning, enable plugins (auto-detected by `npm
init @knip/config`):

```json
{
  "next": {
    "entry": ["next.config.{js,ts,cjs,mjs}", "app/**/page.{js,ts,tsx}"]
  },
  "playwright": {
    "config": "playwright.config.ts",
    "entry": ["e2e/**/*.spec.ts"]
  }
}
```

Plugin list (Next.js, Remix, Astro, Vite, Storybook, Playwright, Jest,
etc.) - see the [Knip plugins page].

## Step 5 - Limit output during cleanup

```bash
# Show only top 5 of each issue type - useful when first adopting
npx knip --max-show-issues 5
```

Per the [Knip docs] for overwhelming output.

## Step 6 - CI gate

```yaml
# GitHub Actions
- name: Knip dead-code check
  run: npx knip
```

Fails build on any new dead code. For brownfield rollout, baseline
existing dead code first:

```bash
# Snapshot current findings; CI only fails on additions
npx knip --no-exit-code > knip-baseline.txt
```

## Step 7 - Per-issue triage

| Reported as | True positive? | Action |
|---|---|---|
| Unused file | Usually yes | Delete |
| Unused dependency | Usually yes | `npm uninstall` |
| Unused export | Sometimes (public API) | Mark with JSDoc `@public` + `tags: ["public"]` config |
| Unused enum member | Usually yes | Delete |
| Unused class member | Sometimes (public API) | Same as unused export |

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Run without entry points | Everything looks orphaned | Always set `entry` (Step 2) |
| Treat "unused export" as "delete now" | Public library APIs flag as unused | Use `tags: ["public"]` for library packages |
| Skip framework plugins | Next.js page files look orphaned (Knip doesn't know they're routes) | Enable plugin (Step 4) |
| Block PRs from day 1 in brownfield | Hundreds of pre-existing unused; team disables tool | Baseline first (Step 6 alt path) |
| Auto-fix mode on first run | `--fix` deletes legitimate unused public exports | Manual review first; `--fix` after baseline clean |

## Limitations

- Dynamic imports with computed paths (`import(\`./${name}\`)`) cannot
  be statically tracked; Knip flags dependencies as unused even though
  they load at runtime. Use `ignoreDependencies` for these cases.
- Side-effect imports (e.g., `import "./polyfill"`) are tracked, but
  reflection-heavy code (DI containers that instantiate via string
  names) requires manual `ignore` entries.

## References

- [Knip docs] - install, entry/project config, framework plugins
- [Knip plugins page] - full plugin list (Next.js, Remix, Astro,
  Storybook, Vite, etc.)

[Knip docs]: https://knip.dev/overview/getting-started
[Knip plugins page]: https://knip.dev/reference/plugins
