---
name: npm-publishing
description: Use when preparing, packaging, testing, publishing, or troubleshooting npm packages, including scoped packages, CLI bins, npm 2FA/web login, env-file tokens, GitHub Actions trusted publishing, provenance, and post-publish install verification.
triggers:
  - npm publish
  - publish npm package
  - package publishing
  - npm pack
  - npm provenance
  - trusted publishing
  - GitHub Actions npm publish
  - npm 2FA
  - npm auth
  - npm E401
  - npm E403
  - temp prefix install
tools:
  - run_command
  - read_file
  - search_files
  - apply_patch
---

# npm Publishing

## Core Rule

Never expose credentials. Do not print, paste, commit, or log npm tokens, `.npmrc`, `.env`, OTPs, cookies, recovery codes, or full auth URLs after they are consumed. Prefer verified commands and registry checks over assumptions. If npm prints an auth URL, open it directly for the user when possible, but do not preserve it in commits, docs, or logs.

Use this skill when the user asks to make a repo installable through npm, publish a package, fix npm auth, add trusted publishing, or verify npm installation.

## Package Readiness

Inspect the repo before editing:

```bash
git status -sb
cat package.json
ls -la
```

For a CLI package, ensure `package.json` has the expected basics:

```json
{
  "name": "@scope/package-name",
  "version": "0.1.0",
  "bin": {
    "command-name": "bin/command-name.js"
  },
  "files": [
    "bin/",
    "src/",
    "README.md",
    "package.json"
  ],
  "scripts": {
    "test": "npm run check",
    "pack:dry-run": "npm pack --dry-run"
  }
}
```

Prefer a narrow `files` allowlist over a broad `.npmignore`. If using `.npmignore`, explicitly exclude generated output, caches, logs, local archives, `.env`, `.npmrc`, and secrets.

## Pre-Publish Checks

Run checks before every publish:

```bash
npm test
npm run pack:dry-run
npm pack --json
```

Inspect the dry-run tarball output. Block publish if it includes any of:

- `.env`, `.npmrc`, tokens, cookies, keys, OTPs, debug logs;
- generated caches such as `__pycache__`, `.pytest_cache`, `.DS_Store`;
- large private artifacts that do not belong in the package;
- files unrelated to the install surface.

If `npm pack` creates a local `.tgz`, delete it after inspection or confirm it is ignored before committing.

Check registry state:

```bash
npm view @scope/package-name version --json
npm whoami
```

`E404` from `npm view` means the package is not yet published. A published package needs a new version before another publish.

For scoped packages, verify scope rights before assuming auth is enough:

```bash
npm org ls scope-name
npm access list packages @scope --json
```

If the account is an org owner but the new package still returns `E404`, treat it as an initial package-creation/bootstrap issue, not a normal version publish.

## Smooth Local Release Helper

When a repo will be published repeatedly, prefer adding a deterministic release helper instead of retyping the release sequence each time. The helper should:

- require a clean git tree;
- compute `patch`, `minor`, `major`, or exact `x.y.z` target versions;
- reject versions already published on npm;
- run `npm whoami`, `npm test`, and `npm pack --dry-run`;
- update `package.json` and any lockfile;
- commit `Release vX.Y.Z` and tag `vX.Y.Z`;
- run `npm publish --access public` in a TTY so web/2FA approval can complete;
- verify `npm view` and a temp-prefix global install;
- push the release commit and tag only after publish succeeds.

Expose it through package scripts:

```json
{
  "scripts": {
    "release:npm": "node scripts/npm-release.js",
    "release:npm:dry-run": "node scripts/npm-release.js patch --dry-run",
    "publish:npm:current": "node scripts/npm-release.js current"
  }
}
```

Typical use:

```bash
npm run release:npm:dry-run
npm run release:npm -- patch
```

If npm auth expires after the release commit/tag is created but before publish completes, keep the same version and recover with `npm run publish:npm:current`.

## Authentication

First test the current session:

```bash
npm whoami
```

If unauthenticated, use web login:

```bash
npm login --auth-type=web
```

If npm prints a browser URL and waits, tell the user to complete login or 2FA on a trusted device, then keep the CLI session alive. For publish-time approval, run the publish in a real TTY/PTTY, press Enter when npm asks to open the browser, and wait for completion:

```bash
npx -y npm@^11.10.0 publish --access public
```

Non-interactive command capture may redact npm auth URLs as `***`, making them unrecoverable after the command exits. Prefer a TTY session for web-auth publish attempts. If the auth URL expires or npm ends with `GET https://registry.npmjs.org/-/v1/done?authId=***` plus `E404`, rerun the publish command to generate a fresh auth URL.

For token-based publishing, read tokens from an uncommitted env file without printing values:

```bash
# .env, not committed:
# set NPM_TOKEN privately
# set NODE_AUTH_TOKEN privately if your tooling expects it
NPM_CONFIG_REGISTRY=https://registry.npmjs.org
```

Use a temporary npm config for token commands and delete it afterward:

```bash
TMP_NPMRC="$(mktemp)"
npm config set //registry.npmjs.org/:_authToken "$NPM_TOKEN" --userconfig "$TMP_NPMRC"
NPM_CONFIG_USERCONFIG="$TMP_NPMRC" npm whoami
rm -f "$TMP_NPMRC"
```

If `whoami` returns `E401`, the token is invalid, expired, scoped incorrectly, or lacks registry access. Do not publish until auth succeeds.

Do not infer token validity from token shape, length, or `npm_` prefix. Always verify with `npm whoami` through the same temporary npm config that will be used for publish.

## Publish Workflow

For public scoped packages:

```bash
npm publish --access public
```

For provenance-capable CI releases:

```bash
npm publish --access public --provenance
```

If npm requires publish authentication, share only the current approval URL with the user and wait. After success, verify the registry:

For a first publish of a new scoped package, npm may require one bootstrap publish by local web-auth/OTP or by a granular token with 2FA bypass. Trusted publishing cannot reliably create the first package version until npm has a package record and trusted publisher configuration.

```bash
npm view @scope/package-name version dist.tarball --json
```

Then verify a real global install in a temporary prefix:

```bash
TMP_PREFIX="$(mktemp -d)"
npm install --prefix "$TMP_PREFIX" -g @scope/package-name
"$TMP_PREFIX/bin/command-name" --version
rm -rf "$TMP_PREFIX"
```

Report the package name, version, npm URL, install command, validation commands, and any remaining publishing setup.

## GitHub Actions Trusted Publishing

After the first package version exists, configure tokenless future releases with npm trusted publishing. npm trust requires npm 11.10+ and the package must already exist on the registry.

Workflow requirements:

```yaml
permissions:
  contents: read
  "id-token": write
```

Publish job outline:

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
  with:
    node-version: "22"
    registry-url: https://registry.npmjs.org
- run: npm install -g npm@^11.10.0
- run: npm test
- run: npm pack --dry-run
- run: npm publish --access public --provenance
```

Trusted publisher setup:

```bash
npx -y npm@^11.10.0 trust github @scope/package-name --repo owner/repo --file npm-publish.yml --allow-publish
```

Some npm 11 builds require `--allow-publish`; others reject it and accept only `--repo` and `--file`. Start with the permission flag. If the CLI returns "Unknown flag: --allow-publish", retry without it. For staged publishing, use `--allow-stage-publish` only when the local help shows that flag.

The npm CLI may require account-level 2FA and package write access. Like publish, run trust setup in a TTY when you need a browser-auth flow. Non-interactive output may redact the auth URL. If the CLI cannot complete setup, configure the trusted publisher from the npm package settings page with the same package, repository, and workflow filename.

Run the workflow only after trust is configured:

```bash
gh workflow run npm-publish.yml --repo owner/repo
gh run watch <run-id> --repo owner/repo --exit-status
```

## Common Failures

- `E401 Unauthorized`: login expired or token invalid; rerun `npm whoami` and refresh auth.
- `E403 Forbidden`: account lacks package/scope rights, package name is protected, or version already exists.
- `E404 Not Found` from `npm view`: package has not been published yet.
- `E404 Not Found` from `npm publish` in GitHub Actions after provenance is signed: OIDC ran, but npm did not accept the package write. Common causes are missing trusted publisher configuration, attempting trusted publishing before the first package exists, or insufficient scope/package rights.
- `EPUBLISHCONFLICT`: version already exists; bump `version` and retry after checks.
- Expired 2FA web approval: rerun `npm publish` to get a fresh URL.
- `npm trust github` says a permission flag is required: rerun with `--allow-publish` or `--allow-stage-publish`.
- Trusted publishing fails before first publish: npm requires the package to exist first; bootstrap the first version locally or with a valid bypass-2FA granular token.

## Completion Check

Before final response:

- working tree is clean or all edits are explained;
- package checks passed;
- registry shows the expected version;
- temp-prefix install works;
- docs and CI changes are committed and pushed if the user requested repository updates;
- no credentials or one-time auth material were committed or echoed.
