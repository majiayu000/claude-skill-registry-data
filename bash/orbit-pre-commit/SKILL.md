---
name: orbit-pre-commit
description: Install or troubleshoot the Orbit pre-commit hook in a WordPress plugin repo. Hook runs PHP lint on staged files, JSON validity check, scratch-pattern detector (var_dump/console.log/debugger), and a block.json apiVersion warning — all under 10 seconds. Use when the user says "install pre-commit", "block bad commits", "git hook for QA", or wants commit-time gating without slowing down their loop.
---

# 🪐 orbit-pre-commit — Catch obvious bugs before push

Install a fast, focused git pre-commit hook that runs in **<10 seconds** on every commit. Catches the things every WP dev forgets to remove: `var_dump`, debug `console.log`, `debugger`, dirty JSON, syntax errors, stale block.json apiVersion.

---

## What the hook checks

| Check | Time | Blocks commit? |
|---|---|---|
| `php -l` on every staged `.php` | ~2s | Yes (fatal errors) |
| JSON validity on every staged `.json` | <1s | Yes |
| `console.log('DEBUG`, `var_dump`, `debugger`, `dd(` | <1s | Yes |
| `block.json` apiVersion < 3 (WP 6.5+) | <1s | Warn only |
| Forbidden function calls (`error_reporting`, `phpinfo`) | <1s | Yes |

Everything else (PHPCS, PHPStan, tests) runs on `/orbit-gauntlet --mode quick` — not pre-commit. Pre-commit must stay fast.

---

## Install

```bash
cd ~/plugins/my-plugin     # any WP plugin repo
bash ~/Claude/orbit/scripts/install-pre-commit-hook.sh
```

Output:
```
✓ Installed .git/hooks/pre-commit
  Runs on every `git commit`. Bypass with --no-verify (only for WIP).
```

---

## Verify

Stage a deliberately broken file and try to commit:

```bash
echo '<?php var_dump($x);' >> test.php
git add test.php
git commit -m "test"
# → BLOCKED: var_dump in test.php:1
git reset HEAD test.php && rm test.php
```

---

## Common patterns the hook catches

```php
// BLOCKED — debug leftovers
var_dump($foo);              // remove before commit
print_r($bar, true);          // wrap in error_log() if you need it
error_log(print_r($baz, 1)); // OK — explicit

// BLOCKED — forbidden in production
error_reporting(E_ALL);
phpinfo();
ini_set('display_errors', 1);
```

```js
// BLOCKED
console.log('DEBUG', state);
debugger;

// OK
console.error('Real error', err);
```

```json
// WARNS — WP 6.5 expects apiVersion 3
{ "apiVersion": 2, "name": "my/block" }
```

---

## Bypass (use sparingly)

```bash
git commit --no-verify -m "wip: half-finished feature"
```

Acceptable for: work-in-progress branches the user will rebase later.
**Not acceptable for:** main / release branches. The hook is the last line of defence before a bad commit lands.

---

## Uninstall

```bash
rm .git/hooks/pre-commit
```

Or to disable temporarily:
```bash
chmod -x .git/hooks/pre-commit
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Hook doesn't run | `chmod +x .git/hooks/pre-commit` |
| `php: command not found` | Hook needs PHP CLI — install via Homebrew |
| Hook runs forever | Some staged files are huge — exclude vendor/, node_modules/ via `.gitattributes` |
| False positive on `var_dump` in a fixture | Add `# allow-dump` comment on the line |

---

## Pair with /orbit-gauntlet

Pre-commit catches cheap things in <10 sec. After commit, run the full gauntlet on a clean state:

```bash
git commit -m "feat: add mega menu"
bash scripts/gauntlet.sh --plugin . --mode quick
```

Pre-commit and gauntlet are complementary — never replace one with the other.
