---
name: eslint-config-parity-check
description: >-
  Use when changing ESLint configuration rather than code — dropping or replacing a shared preset,
  migrating to flat config, upgrading eslint or a plugin major, consolidating rules into an inline
  rules block, or reordering config objects — and before merging any config-only change. Triggers
  include "eslint config migration", "drop the preset", "flat config", an eslint or plugin version
  bump, and a diff that touches only eslint.config.mjs.
---

# ESLint config parity check

## Profile keys consumed

- `make.lint_eslint`
- `framework.package_manager`

## Overview

A green lint run after a configuration change proves only that today's code passes the new config.
It proves nothing about which rules survived. Prove parity by dumping the **resolved** configuration
for every linted file before and after, and diffing the two.

## When to use

- Removing, replacing or inlining a shared preset.
- Upgrading `eslint` or a plugin across a major — new majors add, drop and re-scope rules.
- Migrating config format, or merging several config objects into fewer.
- Reviewing someone else's config-only change.
- Not for: fixing code that a stable config rejects, or tuning a single rule's options deliberately.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — `eslint.config.mjs` at the root, ESLint 9, the target mapped by `make.lint_eslint`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — `eslint.config.mjs` at
  the root, ESLint 9, the target mapped by `make.lint_eslint`.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes —
  `eslint.config.mjs` at the root, ESLint 9, the target mapped by `make.lint_eslint`.

Skip the confirming lint run with a recorded note when `make.lint_eslint` maps to `null`; the
resolved-config dump below still applies, since it goes through the ESLint API directly.

## Procedure

Run this before the change, keep the output, run it again after, and diff. Write both dumps outside
the worktree so they are never committed. Execute it with the runtime and runner resolved from
`framework.package_manager`, in the same place both times.

```js
import { ESLint } from 'eslint';
import { execFileSync } from 'node:child_process';

const eslint = new ESLint();
const files = execFileSync('git', ['ls-files', '*.ts', '*.tsx', '*.js', '*.jsx', '*.mjs', '*.cjs'])
  .toString()
  .trim()
  .split('\n');

const dump = {};
for (const file of files) {
  if (await eslint.isPathIgnored(file)) continue;
  const c = await eslint.calculateConfigForFile(file);
  const { parser, ...lang } = c.languageOptions ?? {};
  dump[file] = {
    rules: c.rules,
    settings: c.settings,
    plugins: Object.keys(c.plugins ?? {}).sort(),
    languageOptions: { ...lang, parser: parser?.meta?.name ?? parser?.name },
  };
}
console.log(JSON.stringify(dump, null, 2));
```

Two details make the dump comparable. Listing files from the index and filtering with
`isPathIgnored` resolves the same set the lint target does without paying for a full lint run — the
glob list has to cover the linter's full default scope, `.cjs` included, or a change that only alters
the resolved config of a CommonJS file (a `.cjs` config file, a `sourceType` flip) produces no
differing entry and the parity check passes while the rule really did change.
Replacing the parser object with its name keeps the diff readable — serialising the parser itself
emits its entire syntax table into every file's entry.

## Reading the diff

- **Rules present before and absent after** — a regression, unless the change explicitly intends it
  and says why.
- **Severity drops** — `error` to `warn`, or `warn` to `off`.
- **Option loss** — a rule that went from `[severity, options]` to a bare severity is weaker even
  though the rule is still listed.
- **Scope changes** — a rule that survives globally but disappears for one directory. Diff per file,
  not per rule set, or this is invisible.
- **Settings drift** — a preset often supplies `settings` such as the React version or an import
  resolver. These change rule behaviour and never appear in a code review of the config.
- **Language options** — parser identity, `ecmaVersion`, `sourceType`, and globals should be
  identical unless the migration required otherwise.

Record the result in the change description: files compared, rules removed or weakened (each with
its justification), and settings and language options confirmed unchanged. An undocumented weakening
is the thing this check exists to catch, and the compliant response is to keep the rule and fix the
code it flags.

## Common mistakes

- Trusting a green lint run as evidence of parity.
- Diffing only the config source — the resolved config is what the linter uses, and a preset's
  contents are invisible in the source diff.
- Guessing which rules a dropped preset supplied and re-listing them by hand.
- Running the two dumps in different places (host versus container, or different installs) so
  version differences pollute the diff.
- Deleting a rule because it is now noisy — that is a separate, argued decision, not a side effect
  of a refactor.
