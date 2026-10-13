---
name: dev-npm-package
description: "Develop npm packages with Node.js and TypeScript following modern best practices. Use when: (1) Creating a new npm package, (2) Setting up package.json exports (dual ESM/CJS or ESM-only), (3) Configuring TypeScript for library authoring (Bundler or Node16 moduleResolution), (4) Building/publishing with tsup or tsc, (5) Creating CLI tools with bin field, (6) Testing with vitest, (7) CI/CD for npm publishing, (8) ESM/CJS interop issues, (9) Choosing a versioning / dist-tag / release-channel strategy — especially the pre-1.0 (0.x) ruling for what `latest` vs `next` should point at, how to tag prereleases, and avoiding the stale-`latest` footgun. Use this whenever the user mentions dist-tags, `latest`/`next`, prerelease tagging, 0.x versioning, or 'what version/release strategy should we use', even if they don't explicitly say 'npm package'. Keywords: npm package, publish to npm, library development, dist-tag, latest vs next, prerelease tagging, 0.x versioning, release strategy, semver channel."
---

# npm Package Development

## Quick Start: Recommended Stack

- **Build**: tsup (esbuild-powered, zero-config, dual CJS/ESM) or tsc alone (for ESM-only packages)
- **Test**: vitest (native ESM/TS, Jest-compatible API)
- **Lint**: Biome (all-in-one linter+formatter) or ESLint flat config + Prettier
- **Types**: TypeScript with `moduleResolution: "Bundler"` (with tsup) or `"Node16"` (with tsc alone)
- **Dev**: tsx for running TS, tsup --watch for rebuilding
- **Publish validation**: publint + @arethetypeswrong/cli (attw)

## Determine Package Type

1. **Library package** -> Follow "Library Setup" below
2. **CLI tool package** -> Follow "CLI Setup" below
3. **Both** -> Combine both patterns

## Library Setup

### Minimal package.json

```json
{
  "name": "my-library",
  "version": "0.1.0",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    }
  },
  "files": ["dist"],
  "sideEffects": false,
  "engines": { "node": ">=18" },
  "scripts": {
    "build": "tsup",
    "dev": "tsup --watch",
    "test": "vitest",
    "test:run": "vitest run",
    "lint": "biome check .",
    "typecheck": "tsc --noEmit",
    "prepublishOnly": "npm run build"
  },
  "devDependencies": {
    "@biomejs/biome": "^2.3",
    "tsup": "^8.4",
    "typescript": "^5.7",
    "vitest": "^3.0"
  }
}
```

### tsup.config.ts

```ts
import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["cjs", "esm"],
  dts: true,
  splitting: false,
  sourcemap: true,
  clean: true,
});
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "noUncheckedIndexedAccess": true,
    "noEmit": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### File Structure

```
my-library/
  src/
    index.ts
    index.test.ts
  package.json
  tsconfig.json
  tsup.config.ts
  vitest.config.ts
  biome.json
  .gitignore
  LICENSE
  README.md
```

## ESM-Only Library Setup

For packages targeting modern Node.js (>=18) without CJS compatibility needs. Simpler than dual publishing.

### Minimal package.json

```json
{
  "name": "@myorg/my-library",
  "version": "0.1.0",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "default": "./dist/index.js"
    }
  },
  "files": ["dist"],
  "engines": { "node": ">=18" },
  "scripts": {
    "build": "tsc",
    "test": "vitest run",
    "prepublishOnly": "tsc && vitest run"
  },
  "devDependencies": {
    "typescript": "^5.7",
    "vitest": "^3.0"
  }
}
```

### tsconfig.json (Node16, no bundler)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

**Important**: With `Node16` resolution, all relative imports must include the `.js` extension (even for `.ts` source files): `import { foo } from './utils.js'`.

### When to choose ESM-only over dual CJS/ESM

- Your package targets Node.js >=18 (or >=22 where CJS can `require()` ESM natively)
- You don't need CJS consumers
- You want the simplest possible setup with `tsc` only (no bundler)

## CLI Setup

### package.json (CLI-specific fields)

```json
{
  "bin": {
    "my-cli": "dist/cli.js"
  },
  "files": ["dist"]
}
```

**Note**: npm recommends bin paths without a `./` prefix (`"dist/cli.js"` not `"./dist/cli.js"`). Modern npm normalizes this automatically, but omitting `./` avoids warnings in older npm versions. Run `npm pkg fix` to check for issues.

### Entry file (src/cli.ts)

```ts
#!/usr/bin/env node
import { program } from "commander";

program
  .name("my-cli")
  .version("1.0.0")
  .description("Description here");

program
  .command("init")
  .option("-t, --template <name>", "template to use", "default")
  .action((options) => {
    console.log(`Template: ${options.template}`);
  });

program.parse();
```

CLI argument parsing libraries: **commander** (most popular, subcommands), **yargs** (validation, middleware), **citty** (lightweight ESM-first).

## Versioning & release channels (standard ruling)

The default install is the `latest` dist-tag: a tagless `npm install <pkg>` (or `pnpm add` / `pnpm dlx`) dereferences `latest` **directly** — it is NOT a semver range match, so whatever `latest` points at is exactly what new consumers get, prerelease or not. Keeping `latest` on the newest shippable build is the whole game; never strand it on an old version.

**Pre-1.0 (`0.x`) — ship clean `0.MINOR.PATCH` straight to `latest`.** Do not put a `-next`/`-beta` suffix on the everyday dev mainline. `0.x` (major-zero) is itself SemVer's "anything may change" signal, so a breaking change rides a **minor** bump (`0.2` → `0.3`) and everything else a **patch** bump. Every release is then a clean, monotonically-increasing version that npm routes to `latest` automatically — a tagless install always gets the newest build, with no machinery to get stuck (esbuild, pre-1.0 Vite, Bun, Biome all do this).

**Prereleases are an opt-in side channel, not the mainline.** Reserve `-alpha`/`-beta`/`-rc`/`-next` plus the `next` (or `canary`) dist-tag for genuine previews — a `1.0.0-beta` run-up, or a bleeding-edge line published *ahead of* `latest`. `next` conventionally means "ahead of/distinct from `latest`" — never mirror it onto `latest`.

**In CI, derive `--tag` from the version string and always pass it explicitly:** hyphen → `--tag next`, clean `X.Y.Z` → `--tag latest`. npm ≥ 11 hard-errors when you publish a prerelease without `--tag`; npm ≤ 10 silently routed prereleases onto `latest` (a silent-downgrade footgun). Never rely on the implicit default for a prerelease. At `1.0.0` the normal stable/preview split resumes automatically under this same rule — no special-casing.

Detailed mechanics, the **dual-tag "advance-latest" anti-pattern** that strands `latest`, and `^0.x` range gotchas: [references/publishing.md](references/publishing.md).

## Key Rules

### exports Field

- Always place `types` before `default` within each condition block
- `import` condition for ESM, `require` condition for CJS
- `main`/`module`/`types` at top level exist for backward compatibility with older tools

### files Field

Always use `files` as a whitelist (not `.npmignore`). Set to `["dist"]` to publish only build output. Verify with `npm pack --dry-run`.

### prepublishOnly

Always include a `prepublishOnly` script to build (and ideally test) before publishing:

```json
{ "prepublishOnly": "npm run build && npm test" }
```

For tsc-only projects, you can call commands directly: `"prepublishOnly": "tsc && vitest run"`.

### Scoped Packages

For scoped packages (`@myorg/pkg`), configure public access via `.npmrc` in the project root:

```
access=public
```

Alternatively, use `publishConfig` in `package.json`:

```json
{ "publishConfig": { "access": "public" } }
```

### sideEffects

Set `"sideEffects": false` for pure utility libraries to enable tree-shaking. If some files have side effects, list them: `"sideEffects": ["*.css"]`.

### Tree-Shaking

Use named exports (not default export of objects). Avoid classes when individual functions suffice.

## Pre-Publish Checklist

```bash
npm run build              # Build the package
npx publint                # Validate package.json/exports
npx attw --pack .          # Validate TypeScript types
npm pack --dry-run         # Inspect package contents
npm publish --dry-run      # Simulate publish
```

## Detailed References

Read these when you need specifics:

- **Build tools, tsconfig, testing, linting, monorepo**: [references/tooling.md](references/tooling.md) - tsup/tsdown/unbuild comparison, TypeScript config, vitest setup, Biome vs ESLint, pnpm workspaces + Turborepo, dev workflow
- **Publishing, versioning, dist-tags, CI/CD, security**: [references/publishing.md](references/publishing.md) - semver, **dist-tag strategy (`latest`/`next`, the pre-1.0 `0.x` clean-mainline ruling, the dual-tag stale-`latest` anti-pattern, `^0.x` range mechanics)**, Changesets/semantic-release, GitHub Actions OIDC trusted publishing, npm provenance, publint/attw, size-limit, supply chain security
- **Architecture, ESM/CJS, exports, CLI, dependencies**: [references/patterns.md](references/patterns.md) - dual publishing patterns, conditional exports, subpath exports, dependency types (peer/optional/bundled), CLI bin setup, argument parsing, tree-shaking optimization
