---
name: pre-push
description: The local checks to run before every push of EasyTask code, in order, with what cannot run in the cloud. Use before committing/pushing a code change, after a refactor, or when the user says "controlla tutto" / "prima di pushare".
---

# Pre-push checks (EasyTask)

Run from the repo root, stop at the first failure and fix it. The CI runs the same things plus the ones that cannot run here.

```bash
npx eslint .
```
```bash
npx tsc -b
```
```bash
npm run e2e:typecheck
```
```bash
npx vitest run
```
```bash
npm run build
```
Only if `src-tauri` changed:
```bash
cd src-tauri && cargo fmt --check
```
`cargo clippy -- -D warnings` and `cargo test` need the Tauri system libraries (GTK, WebKit): on the user's PC they run; in the cloud container they do not compile, so the CI is the only check there. Read the code twice instead and expect clippy to reject dead code and unused imports.

## Faster loops
- One file: `npx vitest run src/path/to/file.test.ts`. The whole suite is about 280 files and 3400 tests (about 100 s).
- Coverage: the CI runs `npm run test:coverage`, not plain vitest, and fails below the thresholds of `vitest.config.ts` (statements 89, branches 83, functions 87, lines 91). Run it when a lot of code was added. New code needs its test.
- Release only: `npm run release:check` (versions in sync), the full list is in the `release` skill.

## Before you push
1. `git status --short`: only the files you mean to ship; no scratch files.
2. Re-read the diff as a reviewer: what would the CI reject? A removed translation key still used in `e2e/` (see `i18n-keys`), a new Tauri command without its permission (see `tauri-permission`), a drag test without the Linux skip.
3. Commit message in the style of the history (`fix(e2e): ...`, `chore(release): vX.Y.Z`); follow the attribution rule of the user (no signature lines when they asked so).
4. Push with `git push -u origin <branch>`; never to another branch without permission. In the cloud session, if the stop hook says the branch has no remote, check `git ls-remote origin <branch>` and `git update-ref refs/remotes/origin/<branch> HEAD`.
5. After the push, read the CI (see `ci-failure`).

## Not runnable in the cloud
- `npm run e2e`, `npm run ui-tour`, `npm run docs:screenshots` (need tauri-driver and a display): the CI runs the Linux e2e; the Windows ones are run by the user.
- `npm run tauri dev`: manual checks are done by the user on their PC.
