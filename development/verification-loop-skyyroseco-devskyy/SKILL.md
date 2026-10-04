---
name: verification-loop
description: Runs the full DevSkyy gate battery (pytest, ruff, phpcs/phpstan, verify:theme, .min rebuild, live curl, eyes-on) and reports each result with an evidence-scope tag. Use when a feature, fix, or refactor is finished and you are about to claim "done", open a PR, or deploy. Do NOT use for choosing which gate to add or for reviewing code quality by reading it — that is code-review; this skill only executes gates that already exist and reports what they returned.
origin: ECC
---

# Gate Battery

The loop that stands between "I made the change" and "it works". Its only product is
**evidence**: for every surface the change touched, a command that could have returned
"no", the output it actually returned, and the scope tag that output earns.

The failure this prevents is not a missing gate. It is a gate that **ran, died, and was
counted as green** — or ran against a tree already red, so the new violation hid inside
the existing count.

## When to use

Run it when:

- a feature, bugfix, or refactor is finished and you are about to say "done"
- before `git commit` on anything under `wordpress-theme/`, `frontend/`, or the Python API
- before opening a PR, and before any `deploy-theme.sh` / `npm run deploy` STOP-AND-SHOW
- after a subagent reports success — a builder grading itself rounds up

Do **not** use it:

- mid-edit, on a tree you know is broken. Gates on a half-written change produce noise,
  not signal. Finish the edit first.
- to *judge* code you have not changed. That is `code-review`.
- as the last word on someone else's fix. An independent re-derivation is
  [`adversarial-verification`](../adversarial-verification/SKILL.md); this skill runs
  gates, it does not supply skepticism.

## Inputs

| Required | How to get it | If absent |
|---|---|---|
| The list of paths your change touched | `git diff --name-only` and `git status --porcelain` | **Stop.** A gate run without a change scope cannot attribute anything. |
| A pristine baseline of those paths | `git archive HEAD <path> \| tar -x -C <scratch>` | **Stop.** Without it you cannot tell your violation from the 1275 that were already there. **Never `git stash`** — the stash stack is shared across worktrees. |
| The gate binaries for the surfaces touched (`rtk`, `vendor/bin/phpcs`, `vendor/bin/phpstan`, `node_modules/.bin/playwright`) | `which rtk`, `ls wordpress-theme/skyyrose-flagship/vendor/bin/` | **Stop and say which gate cannot run.** A missing binary is an unrun gate, not a passing one. Name who installs it. |
| For any `[live]` claim: the production URL | `.env.wordpress` / the theme's own header | **Do not claim `[live]`.** Downgrade the claim to `[repo]` and say production is unverified. |

Sparse worktrees are a real input condition here: this worktree excludes
`assets/`, so asset gates **SKIP**. A SKIP is not a PASS (bug-257) — record it as
"not run here; closed by the full checkout or CI".

## Procedure

1. **Scope the change.** `git diff --name-only` → decide which of the four surfaces are
   in play: Python API, `frontend/`, `wordpress-theme/`, skills/docs.
2. **Extract the pristine baseline** for those paths into a scratch dir with
   `git archive HEAD <path> | tar -x -C <scratch>`. Symlink `vendor/` or
   `node_modules/` into it so the same gate can run there.
3. **Run the language gates for the touched surfaces only** (§ Verification). Do not run
   the whole battery on a docs-only change; do not skip the theme battery on a CSS change.
4. **When a gate fails, diff its contents against the baseline run**, not its state. A
   new violation hides as one extra line inside an already-red total — BLE001 sits at
   **1275 repo-wide**, so "still 1275" and "now 1276" look identical at the summary line.
5. **If the change touched theme CSS/JS, rebuild `.min` and re-run `min-sync`.**
   Production serves `.min`; a source-only edit ships nothing.
6. **If the change reached production, probe it live** with a cache-busted `curl`
   (Batcache serves stale) and then eyes-on via Playwright at 390px and desktop. Never
   `WebFetch` a live page — it strips `<script>`, so JSON-LD and OG tags vanish.
7. **Write the report with one tag per line** — `[repro]` for gates you ran, `[live]`
   only for production probes, `[inferred]` for anything you reasoned but did not
   observe. `[inferred]` never carries severity.
8. **Any gate that errored, timed out, or hit a session limit is re-run by hand.** Its
   zero-findings output is an artifact, not a result (bug-230, ×6).

## Verification

Run the gates for the surfaces the change touched. Each line states the command, what
counts as passing, and the tag it earns.

**Python API**

```bash
rtk proxy pytest tests/ -q          # PASS: "N passed", 0 failed. Baseline 6546 passed.  [test]
ruff check --select E722,BLE001 --statistics .   # PASS: E722 == 2, BLE001 == 1275 (the
                                    # observed baseline) — any HIGHER number is yours.   [repro]
isort . && ruff check --fix && black --check .   # PASS: black exits 0, "0 files would be
                                    # reformatted"                                       [repro]
```

Use `rtk proxy pytest`, never bare `pytest` — bare pytest in this repo can report
"no tests collected" and read as success.

**WordPress theme**

```bash
cd wordpress-theme && npm run verify:theme -- --json
# PASS: every CLI aspect reports ok — 16 CLI aspects exist (php-syntax, phpcs, phpstan,
# style-header, screenshot, templates, wc-support, min-sync, no-placeholders, no-secrets,
# i18n-domain, pot, file-size, json-manifests, escaping, a11y-static).                    [test]

cd wordpress-theme/skyyrose-flagship && vendor/bin/phpcs --standard=.phpcs.xml -s .
# PASS: 0 errors (this is the current baseline — any error is yours).                     [repro]

cd wordpress-theme && npm run build && npm run verify:theme -- --only min-sync
# PASS: min-sync ok — every .min byte-identical to a fresh build.                          [test]
```

The 3 BROWSER aspects (`cwv`, `responsive`, `a11y-interactive`) and 1 VISION aspect
(`product-fidelity`) do **not** run from the CLI. They are SKIPs. Name them as
"not executed — caller runs Playwright/axe/vision", never fold them into a pass count.

**Live (only after a deploy)**

```bash
curl -sI "https://skyyrose.co/?cb=$(date +%s)" | head -1
# PASS: HTTP/2 200                                                                        [live]
curl -s "https://skyyrose.co/wp-content/themes/skyyrose-flagship/style.css?cb=$(date +%s)" \
  | grep -i '^Version'
# PASS: matches SKYYROSE_VERSION in functions.php.                                        [live]
```

**Prove the battery can still fail** before trusting a green run: break one input once,
confirm red, restore.

```bash
printf '\n.sr-broken { color: }\n' >> wordpress-theme/skyyrose-flagship/assets/css/base.css
cd wordpress-theme && npm run verify:theme -- --only min-sync   # PASS-OF-THE-PROOF: this
# now reports min-sync STALE. If it stays green, the gate is decoration — stop and fix it.
git checkout -- skyyrose-flagship/assets/css/base.css           # restore                 [test]
```

## Worked example

A verification pass in this worktree on 2026-07-29, real commands, real output.

```bash
$ rtk proxy pytest tests/mcp/test_http_mount.py -q
......                                                                   [100%]
```

6 passed, 0 failed — `[repro]`. That is a real PASS.

```bash
$ rtk proxy pytest tests/test_asset_manifest.py -q
SKIPPED [1] tests/test_asset_manifest.py:42: sparse worktree deliberately excludes
  assets/products; this gate runs in full checkouts and CI
SKIPPED [1] tests/test_asset_manifest.py:51: ... (×4 total)
```

4 SKIPPED, 0 passed — `[repro]`. This is **not** a PASS. Reported as: "asset-manifest
integrity did not execute in this sparse worktree; CI/full-checkout closes it."
Folding these four into a "tests green" line is exactly the bug-257 failure.

```bash
$ ruff check --select E722,BLE001 --statistics .
BLE001 blind-except   count 1275
E722   bare-except    count 2      (wordpress_health_check.py, validate_wordpress_env.py)
```

`[repro]`. Both gates are already red repo-wide, so their **state** carries no
information about this change. Attribution requires diffing the counts against the
`git archive` baseline — 1275 → 1276 is a finding; 1275 → 1275 is not.

```bash
$ cd wordpress-theme && npm run verify:theme -- --list
Aspect ids (CLI = agent executes it · BROWSER/VISION = agent flags for caller):
  php-syntax  CLI · phpcs CLI · phpstan CLI · … · a11y-static CLI
  cwv BROWSER · responsive BROWSER · a11y-interactive BROWSER · product-fidelity VISION
```

`[repro]`. 20 aspects: 16 CLI, 3 BROWSER, 1 VISION. A theme report may claim at most 16.

```bash
$ curl -s "https://skyyrose.co/wp-content/themes/skyyrose-flagship/style.css?cb=$(date +%s)" \
    | grep -i '^Version'
Version:             1.12.9
```

`[live]`. Production is serving theme 1.12.9. Note this is the *only* line in the whole
pass entitled to the `[live]` tag — every other result above describes the working tree.

## Failure modes

| Symptom | What is really happening | Bug |
|---|---|---|
| Report says "all tests pass" and the suite printed only `SKIPPED` | A SKIP counted as a PASS. Sparse worktree / missing tree excluded the gate. | bug-257 |
| A gate errors or times out, its empty findings list is reported as clean | Fail-open. A gate that dies is not a gate that passed. | bug-230 (×6) |
| "Fixed a production bug" backed only by reading the repo | Scope jump: `[repo]` evidence carrying `[live]` severity. State the scope before the severity. | bug-287 |
| Every headless assertion green, founder sees nothing on the live site | Headless verification measured the DOM, not the human experience. `[repro]` never substitutes for `[live]` + eyes-on. | bug-193 |
| CSS edited, gates green, production unchanged | `.min` not rebuilt. Production serves `.min`; the source edit shipped nothing. | — |
| Deploy "succeeded" but riders vanished from production | `preflight_completeness()` only checks **git-tracked** files. Untracked riders are invisible to it. | bug-252 |
| `curl` shows old markup right after a confirmed deploy | Batcache served stale. Re-probe with `?cb=$(date +%s)`. | — |
| A new violation appears and the gate total is unchanged | You compared gate *state*, not gate *contents*, against the baseline. | — |
| `git stash` used to get a clean baseline, another session's work disappears | The stash stack is shared across worktrees. Use `git archive HEAD <path> \| tar -x`. | — |
