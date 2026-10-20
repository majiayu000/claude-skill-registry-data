---
name: iru-php-bump-version
description: >-
  Set a PHP project's version to an exact value in every place its flavor keeps one, following this catalog's
  `x.y.z-dev` development-version convention. Detects the flavor the same way `iru-php-code-quality` does — Laravel
  application (`config/app.php` `'version' => env('APP_VERSION', '…')`, never a `composer.json` `"version"` field),
  WordPress plugin (main plugin file `Version:` header plus its `<PREFIX>_VERSION` constant), WordPress theme
  (`style.css` `Version:` header, plus a `<PREFIX>_VERSION` constant in `functions.php` when present), PrestaShop
  module (main module class `$this->version` and a tracked `config.xml` `<version>`), or plain Composer library (no
  in-tree version — the git tag is the version, so nothing is changed and that is reported). For WordPress, `readme.txt`
  `Stable tag:` is written only for release versions (never `-dev`), and a `package.json` `"version"` is updated with
  `npm version --no-git-tag-version` so its lockfile follows. Uses an embedded, tested Python helper with `--list` and
  `--dry-run` modes, and refuses to write when the locations disagree until the user confirms. Invoke as
  `/iru-php-bump-version <new-version>` where `<new-version>` is the literal target (e.g. `1.4.0` or `1.5.0-dev`) —
  this skill does not compute bumps itself (`iru-release` computes the release/next-dev values per the convention in
  Step 5 and passes each one through in turn). Also accepts `args` (`key: value` lines): `sync-files: yes|no` (default:
  ask) to also update README/Antora version mentions, `next-version: <upcoming-version>` so that sync maps
  "Latest release" markers to `<new-version>` and "Current development version" markers to the upcoming value, and
  `dry-run: yes|no` (default `no`) to print the diff without writing anything. Reports the flavor, the old and new
  version, every location found and every file touched. Use whenever the user, or another skill such as
  `iru-release`, needs a Laravel/WordPress/PrestaShop project's version set to a specific value instead of
  hand-editing headers and constants.
model: haiku
allowed-tools: Read Bash(python3 *) Bash(npm version *) Bash(npm install --package-lock-only*) Bash(php -l *) Bash(git ls-files *) Bash(git describe *) Bash(git tag *) Bash(grep *) Bash(find *) Bash(ls *) Bash(cat *) Bash(mkdir *)
---

# PHP Bump Version

Set a PHP project's version to an exact value across every file that must agree with it — which files depends on the
flavor (table in Step 2) — and, optionally, README/Antora version mentions. This skill never computes a version
itself: it applies exactly the string it's given, validated for shape. The "which version comes next" logic belongs
to the caller (typically `iru-release`) and is defined in Step 5, so that caller has one place to read it from — the
same contract `iru-java-bump-version`, `iru-typescript-bump-version`, `iru-android-bump-version` and
`iru-swift-bump-version` define for their ecosystems.

## Step 0 — Resolve inputs

- The positional argument is `<new-version>` (e.g. `1.4.0`, `1.5.0-dev`). Missing → ask for it before doing anything
  else; never guess or compute one here.
- `args` (`key: value` lines), if present:
  - `sync-files: yes|no` — also update README/Antora mentions (Step 7). Omitted → ask once with `AskUserQuestion`
    after Step 3 shows such mentions exist; don't ask when none do.
  - `next-version: <upcoming-version>` — the upcoming development version (e.g. `1.5.0-dev`) that "Current
    development version"/"Latest snapshot" markers should show after a release, while "Latest release" markers show
    `<new-version>`. Only meaningful with `sync-files: yes`; validated like `<new-version>`.
  - `dry-run: yes|no` — default `no`. `yes` runs everything through showing the diff, then stops: nothing is written
    and no mutating command (`npm version`) runs; say so plainly in the report.

Reject before touching anything a value that is obviously not a version (empty, or containing whitespace).

## Step 1 — Validate the version string

PHP has no tool that validates a version the way `npm version` does — `version_compare()` accepts anything — so use
this catalog's convention: `X.Y.Z` or `X.Y.Z-dev`.

```bash
python3 -c 'import re,sys; sys.exit(0 if re.fullmatch(r"\d+\.\d+\.\d+(-dev)?", sys.argv[1]) else 1)' "<new-version>"
```

No match → warn that it doesn't follow the `X.Y.Z`/`X.Y.Z-dev` convention and ask whether to proceed anyway (a
project may deliberately use `-beta.1`/`-RC1`, which `version_compare()` and Composer also order correctly). Flag,
don't hard-stop. Anything with a `-` suffix counts as a **pre-release** below (never written to `Stable tag:`).

## Step 2 — Write the helper and survey the version locations

The helper detects the flavor (first match wins — the same markers `iru-explore` and `iru-php-code-quality` use) and
knows every location this catalog's PHP scaffolds (`iru-setup-php-laravel`, `iru-setup-php-wordpress`,
`iru-setup-php-prestashop`) put a version in:

| Flavor | Detected by | Locations rewritten |
|---|---|---|
| `laravel` | `laravel/framework` in `composer.json` `require` **and** an `artisan` file | `config/app.php` `'version' => env('APP_VERSION', '<v>')` (or a plain `'version' => '<v>'`). Never `composer.json` — an application has no `"version"` field |
| `wordpress-plugin` | a root `*.php` whose header carries `Plugin Name:` | that file's `Version:` header (first 8 KB only, as WordPress reads it) **and** its `<PREFIX>_VERSION` constant (`define( 'ACME_VERSION', '…' )` or `const ACME_VERSION = '…'`; when several `*_VERSION` constants exist, e.g. `ACME_DB_VERSION`, the shortest name is the plugin version and the others are left alone); `readme.txt` `Stable tag:` **release versions only**; `package.json` `"version"` (via npm, Step 4) |
| `wordpress-theme` | `style.css` header carries `Theme Name:` | `style.css` `Version:` header; a `<PREFIX>_VERSION` constant in `functions.php` when one exists; `readme.txt` `Stable tag:` release only; `package.json` via npm |
| `prestashop-module` | a root `*.php` class that `extends Module`/`PaymentModule`/`CarrierModule` and sets `$this->version` | `$this->version = '…';` in that class **and** `config.xml` `<version>` (plain or `CDATA`) when `config.xml` is tracked by git (an untracked one is a cache PrestaShop regenerates) |
| `library` | anything else with a `composer.json` | **none** — the git tag is the version (like a Swift package); nothing is changed |

A `composer.json` `"version"` field is reported as a warning in every flavor and never written (Composer recommends
omitting it; it is not part of this convention).

```bash
mkdir -p "$TMPDIR/iru-php-bump-version"
cat > "$TMPDIR/iru-php-bump-version/php_version.py" <<'PY'
import difflib, json, pathlib, re, subprocess, sys

args = sys.argv[1:]
dry, force = "--dry-run" in args, "--force" in args
flavor = next((a.split("=", 1)[1] for a in args if a.startswith("--flavor=")), "auto")
args = [a for a in args if not a.startswith("--")]
new = args[0] if args else None          # None => --list
root = pathlib.Path(".")
is_release = new is not None and "-" not in new


def read(p):
    return p.read_text(encoding="utf-8")


def header(p, size=8192):
    return read(p)[:size]                 # WordPress reads only the first 8 KB for file headers


def tracked(p):
    try:
        r = subprocess.run(["git", "ls-files", "--error-unmatch", str(p)], capture_output=True)
        return r.returncode == 0 if r.returncode in (0, 1) else True
    except FileNotFoundError:
        return True                       # no git: treat an existing file as tracked


def composer():
    p = root / "composer.json"
    return json.loads(read(p)) if p.exists() else {}


def detect():
    c = composer()
    if "laravel/framework" in c.get("require", {}) and (root / "artisan").exists():
        return "laravel", None
    for p in sorted(root.glob("*.php")):
        if re.search(r"^[ \t/*#@]*Plugin Name:", header(p), re.M):
            return "wordpress-plugin", p
    css = root / "style.css"
    if css.exists() and re.search(r"^[ \t/*#@]*Theme Name:", header(css), re.M):
        return "wordpress-theme", css
    for p in sorted(root.glob("*.php")):
        t = read(p)
        if re.search(r"\bclass\s+\w+\s+extends\s+(Module|PaymentModule|CarrierModule)\b", t) and "$this->version" in t:
            return "prestashop-module", p
    return "library", None


# Each rule: (file, compiled regex with groups pre/value/post, release_only, note)
def rules(kind, main):
    out = []
    if kind == "laravel":
        out.append((root / "config/app.php",
                    re.compile(r"""(['"]version['"]\s*=>\s*(?:env\(\s*['"]APP_VERSION['"]\s*,\s*)?['"])([^'"]*)(['"])"""),
                    False, "config/app.php 'version'"))
    elif kind in ("wordpress-plugin", "wordpress-theme"):
        out.append((main, re.compile(r"^([ \t/*#@]*Version:[ \t]*)(\S+)()", re.M), False, "header Version:"))
        const_file = main if kind == "wordpress-plugin" else root / "functions.php"
        out.append((const_file,
                    re.compile(r"""(define\(\s*['"][A-Z][A-Z0-9_]*_VERSION['"]\s*,\s*['"])([^'"]+)(['"])"""
                               r"""|(const\s+[A-Z][A-Z0-9_]*_VERSION\s*=\s*['"])([^'"]+)(['"])"""),
                    False, "<PREFIX>_VERSION constant"))
        out.append((root / "readme.txt", re.compile(r"^(Stable tag:[ \t]*)(\S+)()", re.M | re.I), True,
                    "readme.txt Stable tag (release versions only)"))
    elif kind == "prestashop-module":
        out.append((main, re.compile(r"""(\$this->version\s*=\s*['"])([^'"]+)(['"])"""), False, "$this->version"))
        xml = root / "config.xml"
        if xml.exists() and tracked(xml):
            out.append((xml, re.compile(r"(<version>\s*(?:<!\[CDATA\[)?)([^<\]]+)((?:\]\]>)?\s*</version>)"),
                        False, "config.xml <version>"))
    return out


def groups(m):
    g = m.groups()
    if len(g) == 6 and g[0] is None:      # second alternative of the constant regex
        g = g[3:]
    return g[:3]


kind, main = (flavor, None) if flavor != "auto" else detect()
if flavor != "auto" and kind != "library":
    _, main = detect()
print(f"flavor: {kind}" + (f" (main file: {main.as_posix()})" if main else ""))

c = composer()
if "version" in c:
    print(f"WARNING: composer.json has a \"version\" field ({c['version']}); Composer recommends omitting it — "
          "it is not part of this convention and is left untouched", file=sys.stderr)

if kind == "library":
    print("library: no in-tree version — the git tag is the version; nothing to change")
    sys.exit(0)
if kind in ("wordpress-plugin", "wordpress-theme", "prestashop-module") and main is None:
    sys.exit(f"Could not find the main file for flavor {kind}")

found, new_texts = [], {}
for path, rx, release_only, label in rules(kind, main):
    if not path.exists():
        continue
    text = new_texts.get(path, read(path))
    hits = list(rx.finditer(text[:8192] if label == "header Version:" else text))
    if label in ("header Version:", "readme.txt Stable tag (release versions only)"):
        hits = hits[:1]
    elif label == "<PREFIX>_VERSION constant" and len(hits) > 1:
        # Several *_VERSION constants (e.g. ACME_DB_VERSION): the plugin/theme version is the shortest name.
        name = lambda m: re.search(r"[A-Z][A-Z0-9_]*_VERSION", m.group(0)).group(0)
        keep = min(hits, key=lambda m: len(name(m)))
        for m in hits:
            if m is not keep:
                print(f"note: ignoring {name(m)} in {path.as_posix()} (not the {name(keep)} version constant)")
        hits = [keep]
    for m in hits:
        pre, value, post = groups(m)
        found.append((path.as_posix(), text.count("\n", 0, m.start()) + 1, value, label, release_only))
    if new is None or not hits or (release_only and not is_release):
        continue
    def repl(m):
        pre, _, post = groups(m)
        return pre + new + post
    for m in reversed(hits):              # only the selected occurrences, never every regex match
        text = text[:m.start()] + repl(m) + text[m.end():]
    new_texts[path] = text

pkg = root / "package.json"
if pkg.exists() and kind != "laravel":
    v = json.loads(read(pkg)).get("version")
    if v is not None:
        found.append(("package.json", 0, v, "package.json version (written with npm, not by this script)", False))

for path, line, value, label, release_only in found:
    print(f"{path}:{line}: {value}    [{label}]")
required = {"laravel": "config/app.php 'version'", "wordpress-plugin": "header Version:",
            "wordpress-theme": "header Version:", "prestashop-module": "$this->version"}[kind]
if not any(f[3] == required for f in found):
    sys.exit(f"No {required} found — the version location this flavor's convention requires is missing")
values = {f[2] for f in found if not f[4]}
if len(values) > 1:
    print(f"WARNING: version locations disagree: {sorted(values)}", file=sys.stderr)
    if new is not None and not force:
        sys.exit("Refusing to write: confirm with the user, then re-run with --force to align every location")
if new is None:
    sys.exit(0)
for path, text in new_texts.items():
    old = read(path)
    if text == old:
        continue
    if dry:
        sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), text.splitlines(True), str(path), str(path)))
    else:
        path.write_text(text, encoding="utf-8")
        print(f"updated {path.as_posix()}")
if any(f[4] for f in found) and not is_release:
    print("note: readme.txt Stable tag left unchanged (only release versions are written there)")
if kind == "prestashop-module" and is_release and not (root / "upgrade" / f"upgrade-{new}.php").exists():
    print(f"note: no upgrade/upgrade-{new}.php — add one if this release changes the schema, configuration or hooks")
if pkg.exists() and kind != "laravel" and any(f[0] == "package.json" for f in found):
    print(f"next: npm version {new} --no-git-tag-version --allow-same-version  (package.json + lockfile)")
PY
python3 "$TMPDIR/iru-php-bump-version/php_version.py" --list
```

Run it from the repository root (the directory holding `composer.json`, the main plugin file, `style.css`, or the
module class). Add `--flavor=<flavor>` only when detection picks the wrong one (e.g. a repository holding both a
plugin and a theme — then run it once per directory the user wants bumped). Output: a `flavor:` line, then one
`<file>:<line>: <value>    [<location>]` line per location (`package.json` is listed for the agreement check but
written by npm in Step 4, not by the script). Then:

- **`library`** — it prints "the git tag is the version; nothing to change" and exits `0`. Stop here: report that the
  version of a plain Composer package is its git tag (created by the release, not by this skill), that no file was
  touched, and skip Steps 4, 6 and 7. `iru-release` then treats it like a Swift library (Step 5).
- **Required location missing** (non-zero exit, "No … found") — e.g. a Laravel app whose `config/app.php` has no
  `'version'` key, or a plugin with no `Version:` header. Don't invent one silently: show the file and ask whether to
  add the key/header in the convention's shape (`'version' => env('APP_VERSION', '<new-version>'),` right after
  `'name'` in `config/app.php`; ` * Version: <new-version>` in the plugin header), then re-run `--list`.
- **Locations disagree** (`WARNING: version locations disagree`) — `Stable tag:` is excluded from this check (on the
  development branch it rightly names the last release). Show the list and ask whether to align every location to
  `<new-version>` (Step 4 then passes `--force`) or which to leave alone (edit only the others by hand and say so in
  the report). A WordPress `package.json` left at an older value is the usual cause — aligning it is normally right.
- The current version for the report (and for `iru-release`, which reads it this way) is the value of the flavor's
  required location: `config/app.php` for Laravel, the `Version:` header for WordPress, `$this->version` for
  PrestaShop.

## Step 3 — Look for mirrored mentions

```bash
grep -n -i "latest release\|current development version\|latest snapshot\|composer require\|Stable tag" README.md 2>/dev/null
grep -rln -i "latest release\|composer require" docs/modules/ROOT/pages 2>/dev/null; grep -n '^version:' docs/antora.yml 2>/dev/null
```

Only when something turns up is `sync-files` worth asking about (Step 0).

## Step 4 — Preview (`dry-run: yes`) or apply

```bash
python3 "$TMPDIR/iru-php-bump-version/php_version.py" "<new-version>" --dry-run   # unified diff only
python3 "$TMPDIR/iru-php-bump-version/php_version.py" "<new-version>"             # write
```

Add `--force` only after the user confirmed aligning disagreeing locations (Step 2). The script rewrites exactly the
locations `--list` printed — headers beyond the first match, other `*_VERSION` constants, `Requires at least:`/
`Requires PHP:`/`Tested up to:`, changelog lines and every other file stay untouched — writes `Stable tag:` only when
`<new-version>` has no pre-release suffix, and prints `note:`/`next:` lines:

- `next: npm version <v> --no-git-tag-version --allow-same-version` — a WordPress `package.json` carries a version:
  run exactly that from the same directory (not with `dry-run: yes`). It updates `package.json` **and**
  `package-lock.json` together; `--no-git-tag-version` stops npm from committing/tagging, `--allow-same-version`
  keeps a re-run from failing. For a pnpm/yarn project use `iru-typescript-bump-version`'s Step 4 command for that
  package manager instead.
- `note: no upgrade/upgrade-<v>.php` (PrestaShop release) — this skill never creates upgrade scripts; tell the user
  that if this release changes the schema, configuration keys, or hooks, `upgrade/upgrade-<v>.php` with
  `upgrade_module_<x_y_z>()` must exist before release (see `iru-php-code-one-task`'s `reference/prestashop.md`).

A non-zero exit at any point → stop, show the error, and treat nothing as updated; never fall back to hand edits.

## Step 5 — The PHP-catalog pre-release convention (for `iru-release` and other callers)

The PHP equivalent of `iru-java-bump-version`'s `-SNAPSHOT` and `iru-typescript-bump-version`'s `-dev.N` — the
contract `iru-release` calls this skill against (two calls per release, each passing a computed `<new-version>`), and
the one the `sync.yml` written by `iru-setup-php-github-workflows` and the `iru-setup-php-*` scaffolds use:

- **Current development version**: `x.y.z-dev` (e.g. `1.4.0-dev`) on the integration branch. `version_compare()`
  orders `1.4.0-dev` before `1.4.0` (and after `1.3.0`), Composer parses it, and WordPress/PrestaShop accept it in
  `Version:`/`$this->version` — so upgrade routines keyed on version comparisons behave. `readme.txt` `Stable tag:`
  never carries it: it keeps naming the last release.
- **Cutting a release**: strip the suffix — `x.y.z-dev` → `x.y.z`. Call this skill with `<new-version>: x.y.z`; that
  is also the call that moves `Stable tag:` to `x.y.z`.
- **Opening the next development cycle**: bump the minor (this catalog's default, matching `iru-release`'s
  recommended "minor bump" and the `sync.yml` workflow) and re-append `-dev` — `x.y.z` → `x.(y+1).0-dev`; a patch
  (`x.y.(z+1)-dev`) or major bump is the caller's choice. Call this skill again (or let `sync.yml` do it after the
  release is published) with that exact value — this skill never decides which component to bump.
- **PrestaShop caveat (the convention is kept anyway — a deliberate decision)**: PrestaShop stores the installed
  version in `ps_module.version`, a `VARCHAR(8)` column, so a development version such as `0.1.0-dev` is truncated
  to `0.1.0-de` on a dev/test shop and the module manager keeps offering an "upgrade" for dev builds. Release
  versions of up to 8 characters (`x.y.z` up to `99.99.99`) are unaffected. Never install a `-dev` zip on a real
  shop; only release zips (built from the stripped `x.y.z`) go to production or the Addons marketplace. Mention this
  in the report whenever a PrestaShop module is bumped to a `-dev` value.
- **Plain Composer library**: no in-tree marker at all — the release *is* the git tag (`x.y.z`, no `v` prefix by this
  catalog's convention); there is nothing to strip and no next-dev value to write, exactly like
  `iru-swift-bump-version`'s library case. `iru-release` skips its "must currently be a pre-release" check and its
  next-version question for it.

## Step 6 — Sanity check

Skip with `dry-run: yes`. Otherwise:

```bash
python3 "$TMPDIR/iru-php-bump-version/php_version.py" --list     # every location now shows <new-version> (Stable tag: only for a release)
php -l <each rewritten .php file>                                # still parses
```

`--list` must print `<new-version>` for every non-`Stable tag:` location and no disagreement warning (after Step 4's
npm call for `package.json`). `php -l` needs a PHP binary — without one, say the syntax check wasn't run (the rewrite
only replaces a quoted literal, so it can't change the file's structure, but report it rather than assume).

## Step 7 — Optionally sync other files that mirror the version

Ask (or honor `sync-files`) whether to update the mentions Step 3 found, mapping each by what it names — the same
rule as `iru-java-bump-version`'s Step 7:

- "Latest release" markers (and a `Latest release` row in the README's status table) → `<new-version>` when it is a
  release; untouched when `<new-version>` is a `-dev` value.
- "Current development version"/"Latest snapshot" markers → `next-version` when given; otherwise `<new-version>` only
  if it is a `-dev` value, and untouched (warn in Step 8 that the caller should pass `next-version`) when it's a
  release — never regress a development marker to a release value.
- A `composer require <vendor>/<package>:^x.y` snippet for this project's own package (libraries; rarely a plugin
  distributed through Composer/wpackagist) → the release's `^x.y` constraint, only for a release.
- `docs/antora.yml` `version:` → `<new-version>` only for a release (Antora's component version names released
  versions; skip `-dev`), if the site tracks the release version at all.
- Antora pages under `docs/modules/ROOT/pages/` with the same markers/snippets → as for the README.

Targeted, scoped substitutions only — never a repository-wide replace of the old string. Offered, not automatic: a
README badge pulling the version live (WordPress.org, Packagist shields) must not be rewritten.

## Step 8 — Report

- The flavor (and how it was detected, or `--flavor` if forced), the main file, every location from `--list` with
  its old value, and the new version.
- Every file changed (by the script, by `npm version`, and by Step 7), or for `library` that nothing changed because
  the git tag is the version.
- Whether `Stable tag:` was written (release) or left at the last release (`-dev`), and any disagreement that was
  aligned with `--force` after the user confirmed.
- PrestaShop: the upgrade-script note when it fired, and — for a `-dev` value — the `VARCHAR(8)` truncation caveat
  from Step 5 (dev builds show as e.g. `1.5.0-de` and are never for a real shop).
- Whether this was a `dry-run`, and the Step 6 result (`--list` agreement, `php -l` per file or "not run — no PHP").
- **Warn explicitly**: review the diff before committing (this skill commits nothing); a `composer.json` `"version"`
  field, if reported, is not managed here; WordPress.org reads `Stable tag:` to decide which SVN tag users get, so it
  must only ever name a version that exists as a tag.

## Verification notes

Verified in `$TMPDIR/iru-verify/php-setup/workflows/bump/` by running the exact helper above (`python3` 3.13 in the
`python:3.13-slim` Docker image, and host `python3` 3.9 for the git-tracking case) against hand-written fixtures:

- Laravel `config/app.php` `'version' => env('APP_VERSION', '0.1.0-dev')` → listed and rewritten to `0.1.0`; a
  `config/app.php` without the key → non-zero exit "No config/app.php 'version' found".
- WordPress plugin: header `Version:`, `ACME_LOANS_VERSION` plus an unrelated `ACME_LOANS_DB_VERSION`, a later
  `// Version: 9.9.9` comment, `readme.txt` `Stable tag:` and a changelog line `* Stable tag: x`, and a `package.json`.
  `--dry-run` printed the diff and wrote nothing (checksums unchanged); `1.2.0` rewrote header + constant + `Stable
  tag:` only (DB constant, comment and changelog untouched); `1.3.0-dev` with `package.json` still at the old value was
  refused as a disagreement, and `--force` aligned the PHP locations while leaving `Stable tag:` at `1.2.0`.
- WordPress theme: `style.css` header, `const ACME_THEME_VERSION` in `functions.php`, `readme.txt` — `0.3.0` wrote all
  three; `0.4.0-dev` wrote the first two and left `Stable tag: 0.3.0` with the release-only note.
- PrestaShop: `$this->version` + `config.xml` `<![CDATA[…]]>` rewritten together with the upgrade-script note; with
  `config.xml` removed from the git index it was no longer listed or written.
- Library: reported "the git tag is the version", exit `0`, nothing written; a `composer.json` `"version"` produced
  the warning only.
- `php -l` (`php:8.4-cli`) passed on every rewritten PHP file, and `version_compare('1.3.0-dev', '1.3.0')` is `-1`,
  `version_compare('1.3.0-dev', '1.2.0')` is `1`.

Not verified: `npm version` on a real WordPress `package.json` here (its behavior is the one
`iru-typescript-bump-version` verified), and real scaffolds from `iru-setup-php-*` (written in parallel) — run `--list`
on the first real scaffold and adjust nothing silently if a location is missing.
