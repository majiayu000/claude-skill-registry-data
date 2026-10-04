---
name: qlty-eslint-runtime-mismatch
description: >-
  Use when a Qlty check is red with "Build errored. Check the log for more information." and the
  cloud build log ends in linter stderr rather than findings — an ESLint version banner followed by
  "Error while loading rule 'react/display-name'; contextOrFilename.getFilename is not a function" —
  or after bumping eslint or copying a .qlty/qlty.toml plugin pin from another repository.
---

# Qlty ESLint runtime mismatch

## Profile keys consumed

- `framework.package_manager`
- `framework.ui`
- `make.lint_eslint`

## Overview

An `[[plugin]] name = "eslint"` block with `package_file` / `package_filters` supplies the _plugin_
packages from the repository — never the ESLint runtime. Qlty installs its own, and a newer Qlty CLI
defaults that to a major the locked plugins do not support, so the linter dies at rule-load time and
takes the whole build down with zero findings. Pin the runtime to what the lockfile produced by
`framework.package_manager` resolves.

## When to use

- A Qlty status reads `Build errored. Check the log for more information.` and the build log holds
  linter stderr instead of findings.
- The cloud build log prints an ESLint version banner followed by a `TypeError` in a rule loader.
- An ESLint upgrade just landed, or a `.qlty/qlty.toml` pin was copied from a sibling repository.
- Not for: a red Qlty status whose build log contains no linter stderr at all — that is the
  transient cloud-outage shape, diagnosed separately.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — `.qlty/qlty.toml` exists with an unpinned eslint plugin block, but the file is
  untracked, so a pin added there stays local; the lockfile resolves `eslint@9.39.4`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — a tracked
  `.qlty/qlty.toml` already carries `version = "9.39.4"`, matching the lockfile, plus the
  literal-`react`-version fix below in `eslint.config.mjs`.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial —
  `.qlty/qlty.toml` is tracked but unpinned, and the lockfile resolves `eslint@9.39.5`, so the
  Next.js shape's literal would be the wrong pin here.

## Diagnosis: read the cloud build log

The status text is identical for a runtime crash and a cloud outage; only the build log separates
them, and it lives in Qlty Cloud — ask for the log or for qlty.sh access rather than inferring a
verdict from the status. A crash names the runtime it installed:

```bash
eslint/lint STDERR:
ESLint: 10.9.1
TypeError: Error while loading rule 'react/display-name':
  contextOrFilename.getFilename is not a function
  at .../eslint-plugin-react/lib/util/version.js:31
```

ESLint 10 removed `context.getFilename()`; `eslint-plugin-react` 7.37.5 — the version all three
shapes lock — still calls it.

Three misleading signals:

- **"Another pull request on the same lockfile is green."** A passing run proves nothing if its
  changed-file set never loads the failing rule. Compare build logs, not statuses.
- **"Local `qlty check` is green."** The local CLI may resolve an older cached runtime; list
  `~/.qlty/cache/tools/eslint/` to see which one it has. Local green does not imply cloud green.
- **"Just retry it."** Re-triggering is the remedy for the outage shape only; against a runtime
  crash it never converges.

## Pinning the runtime

Add `version` to the eslint plugin block, equal to the resolved lockfile version, in
`.qlty/qlty.toml`:

```bash
[[plugin]]
name = "eslint"
version = "9.39.4"          # must equal what the lockfile resolves
package_file = "package.json"
package_filters = ["eslint", "jest", "prettier"]
```

Verify after every ESLint bump or pin edit by reading the resolved version out of the lockfile that
`framework.package_manager` maintains:

```bash # profile-example
grep -oE '"eslint@[0-9][^"]*"' bun.lock | sort -u
```

`package.json` carries a caret range, so the lockfile moves under it independently. That range is
`^9` in all three shapes, so ESLint 10 can only ever arrive through the runtime Qlty installs —
which is exactly why the pin, not the manifest, is the control.

## Second-order fix: stop the plugin probing the filesystem

Stating `settings.react.version` as a literal instead of `'detect'` removes the
`context.getFilename()` call from the rule loader, so a sandboxed runner on a newer ESLint no longer
dies on the first TypeScript file. Read the major.minor from this repository's own React dependency
(`framework.ui`), never from a copied constant:

```ts
const REACT_VERSION = '19.2'; // this repo's own `react` major.minor, not a copied constant
// settings: { react: { version: REACT_VERSION } }
```

Re-run the target mapped by `make.lint_eslint` after the edit — skip with a recorded note when it
maps to `null` — so the literal is proven against the repository's own gate before it is pushed.

## Tracking the config

The pin only reaches the cloud if the file is committed. In the component-library shape the
repository ignores `.qlty/*` and negates the config with `!.qlty/qlty.toml`; `git add` prints an
"ignored path" hint and stages it anyway.

## Common mistakes

- Trusting a green sibling run — its changed files may never load the failing rule.
- Copying a `version` pin verbatim between repositories — re-read the lockfile after copying.
- Retrying a runtime crash as an outage — one log read beats a series of pushes.
- Expecting `package_filters` to set the runtime — it only supplies plugin packages.
