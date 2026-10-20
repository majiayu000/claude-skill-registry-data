---
name: iru-python-bump-version
description: >-
  Set a Python project's version (FastAPI service, Django project, or plain library/package) to an exact value in every
  place it keeps one, following this catalog's PEP 440 `X.Y.Z.dev0` development-version convention (the Python
  counterpart of `-SNAPSHOT`/`-dev`). Rewrites `pyproject.toml` `[project].version` and/or `[tool.poetry].version`, a
  legacy `setup.cfg` `[metadata] version`/`setup.py` `version=` literal, tracked `__version__` literals in the package's
  `__init__.py`/`_version.py`/`__about__.py`/`version.py`, a Django settings `VERSION`/`APP_VERSION` literal or env
  default, and a `FastAPI(version=…)` literal only when it equals the package version; follows a file-based dynamic
  version (`[tool.hatch.version] path`, `[tool.setuptools.dynamic] version = {attr|file}`, flit's module
  `__version__`) to its source file; and for a VCS-derived dynamic version (hatch-vcs, setuptools-scm, versioningit,
  `*-dynamic-versioning`) reports that the git tag is the version and changes nothing. Validates the value as PEP 440
  and warns on non-canonical forms (`1.4.0-dev` → `1.4.0.dev0`), refreshes `uv.lock` with `uv lock` when it records the
  project's own version, and uses an embedded, tested Python helper with `--list`/`--dry-run` modes that refuses to
  write when the locations disagree until the user confirms. Invoke as `/iru-python-bump-version <new-version>` where
  `<new-version>` is the literal target (e.g. `1.4.0` or `1.5.0.dev0`) — this skill does not compute bumps itself
  (`iru-release` computes the release/next-dev values per the convention in Step 5 and passes each one through in
  turn). Also accepts `args` (`key: value` lines): `sync-files: yes|no` (default: ask) to also update `docs/antora.yml`
  and README/Antora version mentions, `next-version: <upcoming-version>` so that sync maps "Latest release" markers to
  `<new-version>` and "Current development version" markers to the upcoming value, and `dry-run: yes|no` (default
  `no`) to print the diff without writing anything. Reports every location found, the old and new version, and every
  file touched. Use whenever the user, or another skill such as `iru-release`, needs a Python project's version set to
  a specific value instead of hand-editing `pyproject.toml` and `__version__` strings.
model: haiku
allowed-tools: Read Bash(python3 *) Bash(uv lock*) Bash(uv version *) Bash(poetry check*) Bash(git ls-files *) Bash(git check-ignore *) Bash(git describe *) Bash(git tag *) Bash(grep *) Bash(find *) Bash(ls *) Bash(cat *) Bash(mkdir *)
---

# Python Bump Version

Set a Python project's version to an exact value across every file that must agree with it — `pyproject.toml`, any
`__version__` literal, Django settings, a matching `FastAPI(version=…)`, `uv.lock` — and, optionally, `docs/antora.yml`
and README/Antora version mentions. This skill never computes a version itself: it applies exactly the string it's
given, validated as PEP 440. The "which version comes next" logic belongs to the caller (typically `iru-release`) and
is defined in Step 5, so that caller has one place to read it from — the same contract `iru-java-bump-version`,
`iru-typescript-bump-version`, `iru-android-bump-version`, `iru-swift-bump-version` and `iru-php-bump-version` define
for their ecosystems.

## Step 0 — Resolve inputs

- The positional argument is `<new-version>` (e.g. `1.4.0`, `1.5.0.dev0`). Missing → ask for it before doing anything
  else; never guess or compute one here.
- `args` (`key: value` lines), if present:
  - `sync-files: yes|no` — also update `docs/antora.yml` and README/Antora mentions (Step 7). Omitted → ask once with
    `AskUserQuestion` after Step 3 shows such mentions exist; don't ask when none do.
  - `next-version: <upcoming-version>` — the upcoming development version (e.g. `1.5.0.dev0`) that "Current
    development version"/"Latest snapshot" markers should show after a release, while "Latest release" markers show
    `<new-version>`. Only meaningful with `sync-files: yes`; validated like `<new-version>`.
  - `dry-run: yes|no` — default `no`. `yes` runs everything through showing the diff, then stops: nothing is written
    and no mutating command (`uv lock`) runs; say so plainly in the report.

Reject before touching anything a value that is obviously not a version (empty, or containing whitespace).

## Step 1 — Write the helper and validate the version string

Python *does* have a version grammar — PEP 440 — and every packaging tool (pip, uv, build backends, PyPI) normalizes
to its canonical form. The helper below carries the PEP 440 pattern and renders the canonical form without needing
`packaging` installed (it runs on any `python3` ≥ 3.8 — no `tomllib`, which only exists from 3.11, so it parses
`pyproject.toml` tables with anchored regexes instead). Write it once per run:

```bash
mkdir -p "$TMPDIR/iru-python-bump-version"
cat > "$TMPDIR/iru-python-bump-version/py_version.py" <<'PY'
import difflib, pathlib, re, subprocess, sys

args = sys.argv[1:]
dry, force, antora = "--dry-run" in args, "--force" in args, "--antora" in args
validate = "--validate" in args
args = [a for a in args if not a.startswith("--")]
new = args[0] if args else None          # None => --list
root = pathlib.Path(".")

# PEP 440 (the public-version pattern from the spec, verbose form) + canonical rendering.
PEP440 = re.compile(r"""^\s*v?(?:(?P<epoch>[0-9]+)!)?(?P<release>[0-9]+(?:\.[0-9]+)*)
    (?P<pre>[-_.]?(?P<pre_l>alpha|a|beta|b|preview|pre|c|rc)[-_.]?(?P<pre_n>[0-9]+)?)?
    (?P<post>(?:-(?P<post_n1>[0-9]+))|(?:[-_.]?(?P<post_l>post|rev|r)[-_.]?(?P<post_n2>[0-9]+)?))?
    (?P<dev>[-_.]?(?P<dev_l>dev)[-_.]?(?P<dev_n>[0-9]+)?)?
    (?:\+(?P<local>[a-z0-9]+(?:[-_.][a-z0-9]+)*))?\s*$""", re.X | re.I)


def canonical(v):
    m = PEP440.match(v)
    if not m:
        return None
    s = (m["epoch"] + "!" if m["epoch"] and int(m["epoch"]) else "") + ".".join(str(int(x)) for x in m["release"].split("."))
    if m["pre"]:
        lab = {"alpha": "a", "beta": "b", "c": "rc", "pre": "rc", "preview": "rc"}.get(m["pre_l"].lower(), m["pre_l"].lower())
        s += lab + str(int(m["pre_n"] or 0))
    if m["post"]:
        s += ".post" + str(int(m["post_n1"] or m["post_n2"] or 0))
    if m["dev"]:
        s += ".dev" + str(int(m["dev_n"] or 0))
    if m["local"]:
        s += "+" + ".".join(p if not p.isdigit() else str(int(p)) for p in re.split(r"[-_.]", m["local"].lower()))
    return s


if validate:
    c = canonical(new or "")
    if c is None:
        sys.exit(f"invalid: {new!r} is not a PEP 440 version")
    print(f"canonical: {c}")
    if c != new:
        print(f"WARNING: {new} is valid PEP 440 but not canonical — packaging tools will normalize it to {c}")
    if not re.fullmatch(r"\d+\.\d+\.\d+(\.dev\d+)?", c):
        print("WARNING: not in this catalog's X.Y.Z / X.Y.Z.devN convention")
    sys.exit(0)

is_release = new is not None and canonical(new) is not None and re.fullmatch(r"[0-9.]+", canonical(new)) is not None


def read(p):
    return p.read_text(encoding="utf-8")


def ignored(p):
    try:
        return subprocess.run(["git", "check-ignore", "-q", str(p)], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


def tables(text):
    """Map TOML table name -> (start, end) offsets of its body (regex-based; no tomllib needed on Python < 3.11)."""
    heads = [(m.group(1).strip(), m.start(), m.end()) for m in re.finditer(r"(?m)^[ \t]*\[\[?([^\[\]\n]+)\]\]?[ \t]*(?:#.*)?$", text)]
    out = {}
    for i, (name, _, end) in enumerate(heads):
        out.setdefault(name, (end, heads[i + 1][1] if i + 1 < len(heads) else len(text)))
    return out


def key_in(text, span, key):
    rx = re.compile(r"(?m)^([ \t]*" + re.escape(key) + r"[ \t]*=[ \t]*)([\"'])([^\"'\n]*)(\2)")
    return [m for m in rx.finditer(text, *span)] if span else []


VERSION_ASSIGN = re.compile(r"""(?m)^(__version__[ \t]*(?::[ \t]*str[ \t]*)?=[ \t]*)(["'])([^"'\n]*)(\2)""")
SETTINGS_ASSIGN = re.compile(r"""(?m)^((?:APP_)?VERSION[ \t]*(?::[ \t]*str[ \t]*)?=[ \t]*)(["'])([^"'\n]*)(\2)""")
SETTINGS_ENV = re.compile(r"""(?m)^((?:APP_)?VERSION[ \t]*(?::[ \t]*str[ \t]*)?=[ \t]*(?:os\.environ\.get|os\.getenv|env\.str|env)\([ \t]*["'](?:APP_)?VERSION["'][ \t]*,[ \t]*(?:default[ \t]*=[ \t]*)?)(["'])([^"'\n]*)(\2)""")
FASTAPI_CTOR = re.compile(r"""(FastAPI\((?:[^()]|\([^()]*\))*?\bversion[ \t]*=[ \t]*)(["'])([^"'\n]*)(\2)""", re.S)
SKIP = {".venv", "venv", ".git", "node_modules", "build", "dist", "docs", "tests", "test", "migrations", ".tox", ".nox", "site-packages"}


def walk(globs):
    seen = []
    for g in globs:
        for p in sorted(root.glob(g)):
            if p.is_file() and not (set(p.parts) & SKIP) and p not in seen and not ignored(p):
                seen.append(p)
    return seen


locs = []      # (path, regex, kind, role) role: primary|mirror|conditional|antora
notes = []
pp = root / "pyproject.toml"
text = read(pp) if pp.exists() else ""
tb = tables(text)
name = None
if "project" in tb:
    n = key_in(text, tb["project"], "name")
    name = n[0].group(3) if n else None

dynamic = False
if "project" in tb:
    d = re.search(r"(?ms)^[ \t]*dynamic[ \t]*=[ \t]*\[(.*?)\]", text[tb["project"][0]:tb["project"][1]])
    dynamic = bool(d and re.search(r"[\"']version[\"']", d.group(1)))
backend = ""
if "build-system" in tb:
    b = key_in(text, tb["build-system"], "build-backend")
    backend = b[0].group(3) if b else ""
requires = text[tb["build-system"][0]:tb["build-system"][1]] if "build-system" in tb else ""


def module_file(dotted):
    parts = dotted.split(".")
    for base in (root / "src", root):
        for cand in (base.joinpath(*parts).with_suffix(".py"), base.joinpath(*parts, "__init__.py")):
            if cand.exists():
                return cand
    return None


def stop_vcs(why):
    print(f"version: dynamic — {why}; the version is derived from git tags, nothing to change")
    sys.exit(0)


if dynamic:
    hv = tb.get("tool.hatch.version")
    sd = tb.get("tool.setuptools.dynamic")
    pv = tb.get("tool.pdm.version")
    if hv and key_in(text, hv, "source") and key_in(text, hv, "source")[0].group(3) == "vcs":
        stop_vcs("[tool.hatch.version] source = \"vcs\" (hatch-vcs)")
    if pv and key_in(text, pv, "source") and key_in(text, pv, "source")[0].group(3) == "scm":
        stop_vcs("[tool.pdm.version] source = \"scm\"")
    if re.search(r"setuptools[-_]scm|hatch-vcs|versioningit|dynamic-versioning|uv-dynamic-versioning", requires + text, re.I) \
            or "tool.setuptools_scm" in tb:
        stop_vcs("a VCS versioning plugin (setuptools-scm / hatch-vcs / versioningit / *-dynamic-versioning) is configured")
    target = None
    if hv and key_in(text, hv, "path"):
        target = root / key_in(text, hv, "path")[0].group(3)
    elif pv and key_in(text, pv, "path"):
        target = root / key_in(text, pv, "path")[0].group(3)
    elif sd:
        body = text[sd[0]:sd[1]]
        a = re.search(r"""version[ \t]*=[ \t]*\{[^}]*attr[ \t]*=[ \t]*["']([^"']+)["']""", body)
        f = re.search(r"""version[ \t]*=[ \t]*\{[^}]*file[ \t]*=[ \t]*\[?[ \t]*["']([^"']+)["']""", body)
        if a:
            mod, _, attr = a.group(1).rpartition(".")
            target = module_file(mod)
            if attr != "__version__":
                notes.append(f"attr {a.group(1)}: only __version__ literals are rewritten — check {attr} by hand")
        elif f:
            vf = root / f.group(1)
            locs.append((vf, re.compile(r"\A()()([^\s]+)()"), "VERSION file (setuptools dynamic file)", "primary"))
    elif "flit" in backend and name:
        target = module_file(re.sub(r"[-.]+", "_", name).lower())
    if target is not None:
        if not target.exists():
            sys.exit(f"dynamic version points at {target.as_posix()}, which does not exist")
        locs.append((target, VERSION_ASSIGN, "__version__ (dynamic source)", "primary"))
    if not locs:
        sys.exit("dynamic version with an unrecognized source — explain to the user and stop; nothing was changed")
else:
    if "project" in tb and key_in(text, tb["project"], "version"):
        locs.append((pp, None, "[project].version", "primary"))

if "tool.poetry" in tb and key_in(text, tb["tool.poetry"], "version"):
    locs.append((pp, None, "[tool.poetry].version", "primary"))

cfg = root / "setup.cfg"
if cfg.exists():
    m = re.search(r"(?ms)^\[metadata\][^\[]*?^(version[ \t]*=[ \t]*)()([^\s]+)()", read(cfg))
    if m and not m.group(3).startswith(("attr:", "file:")):
        locs.append((cfg, re.compile(r"(?ms)(^\[metadata\][^\[]*?^version[ \t]*=[ \t]*)()([^\s]+)()"), "setup.cfg [metadata] version", "primary"))
spy = root / "setup.py"
if spy.exists() and re.search(r"""\bversion[ \t]*=[ \t]*["'][^"']+["']""", read(spy)):
    locs.append((spy, re.compile(r"""(\bversion[ \t]*=[ \t]*)(["'])([^"'\n]+)(\2)"""), "setup.py version=", "primary"))

dyn_targets = {l[0] for l in locs if l[2].startswith("__version__")}
for p in walk(["src/*/__init__.py", "src/*/_version.py", "src/*/__about__.py", "src/*/version.py",
               "*/__init__.py", "*/_version.py", "*/__about__.py", "*/version.py"]):
    t = read(p)
    if p not in dyn_targets and VERSION_ASSIGN.search(t):
        locs.append((p, VERSION_ASSIGN, "__version__ literal", "primary"))
    elif p not in dyn_targets and re.search(r"(?m)^__version__\s*=", t):
        notes.append(f"{p.as_posix()}: __version__ is computed (e.g. importlib.metadata.version()) — follows pyproject, untouched")
for p in walk(["*/settings.py", "*/settings/*.py", "*/*/settings.py", "*/*/settings/*.py"]):
    t = read(p)
    if SETTINGS_ENV.search(t):
        locs.append((p, SETTINGS_ENV, "settings VERSION env default", "primary"))
    elif SETTINGS_ASSIGN.search(t):
        locs.append((p, SETTINGS_ASSIGN, "settings VERSION literal", "primary"))
for p in walk(["app/*.py", "src/*/*.py", "src/*/*/*.py", "*/main.py"]):
    if FASTAPI_CTOR.search(read(p)):
        locs.append((p, FASTAPI_CTOR, "FastAPI(version=) literal — written only when it equals the package version", "conditional"))
ay = root / "docs" / "antora.yml"
if antora and ay.exists():
    locs.append((ay, re.compile(r"(?m)^(version:[ \t]*)(['\"]?)([^\s'\"#]+)(\2)"), "docs/antora.yml version (release versions only)", "antora"))

if not locs:
    sys.exit("No version location found (no [project].version, [tool.poetry].version, __version__ literal, setup.cfg/setup.py version)")

found, new_texts = [], {}
for path, rx, label, role in locs:
    t = new_texts.get(path, read(path))
    if rx is None:      # pyproject table keys
        span = tables(t)["project" if label.startswith("[project]") else "tool.poetry"]
        hits = key_in(t, span, "version")[:1]
    else:
        hits = list(rx.finditer(t))[:1]
    for m in hits:
        found.append([path.as_posix(), t.count("\n", 0, m.start(3)) + 1, m.group(3), label, role, path, m])
for f in found:
    print(f"{f[0]}:{f[1]}: {f[2]}    [{f[3]}]")
for n in notes:
    print(f"note: {n}")
primary = [f for f in found if f[4] == "primary"]
if not primary:
    sys.exit("No primary version location found — only mirrors/conditional ones")
values = {f[2] for f in primary}
current = primary[0][2]
print(f"current: {current}")
if len(values) > 1:
    print(f"WARNING: version locations disagree: {sorted(values)}", file=sys.stderr)
    if new is not None and not force:
        sys.exit("Refusing to write: confirm with the user, then re-run with --force to align every location")
if new is None:
    sys.exit(0)

for f in sorted(found, key=lambda f: -f[6].start()):  # rewrite back to front per file
    path, m, role = f[5], f[6], f[4]
    if role == "conditional" and f[2] != current:
        print(f"note: {f[0]}:{f[1]} FastAPI version {f[2]} differs from the package version — left alone (separate API version)")
        continue
    if role == "antora" and (not is_release or f[2] in ("~", "true", "false", "")):
        print(f"note: {f[0]} version left at {f[2]} (Antora's component version names releases only)")
        continue
    t = new_texts.get(path, read(path))
    new_texts[path] = t[:m.start(3)] + new + t[m.end(3):]
for path, t in new_texts.items():
    old = read(path)
    if t == old:
        continue
    if dry:
        sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), t.splitlines(True), str(path), str(path)))
    else:
        path.write_text(t, encoding="utf-8")
        print(f"updated {path.as_posix()}")
lock = root / "uv.lock"
if lock.exists() and name and re.search(r'(?m)^name = "' + re.escape(re.sub(r"[-_.]+", "-", name).lower()) + r'"\nversion = ', read(lock)):
    print("next: uv lock   (refreshes this project's own version entry in uv.lock)")
PY
python3 "$TMPDIR/iru-python-bump-version/py_version.py" "<new-version>" --validate
```

- `invalid: … is not a PEP 440 version` (exit 1) → stop and ask for a valid value; nothing can install or build a
  package with it.
- `WARNING: … not canonical` → the value is legal but every tool rewrites it (`1.4.0-dev` → `1.4.0.dev0`,
  `v1.4.0` → `1.4.0`, `1.0-alpha.2` → `1.0a2`): propose the printed `canonical:` form and use it unless the user
  insists, so the file, the wheel name, the git tag, and PyPI all spell it the same way.
- `WARNING: not in this catalog's X.Y.Z / X.Y.Z.devN convention` → flag, don't hard-stop: a project may deliberately
  ship `1.4.0rc1` or `1.4.0.post1`. Anything with a `.devN`, `aN`, `bN` or `rcN` part counts as a **pre-release**
  below (never written to `docs/antora.yml`).

## Step 2 — Survey the version locations

```bash
python3 "$TMPDIR/iru-python-bump-version/py_version.py" --list --antora
```

Run it from the repository root (the directory holding `pyproject.toml`, `setup.cfg`, or `setup.py`). Output: one
`<file>:<line>: <value>    [<location>]` line per location, any `note:` lines, then `current: <value>`. What it looks
for, in this order:

| Location | When it is used |
|---|---|
| `pyproject.toml` `[project].version` | PEP 621 static version — the scaffold contract's single source (`iru-setup-python-*`), also uv/hatch/setuptools/flit/pdm projects |
| `pyproject.toml` `[tool.poetry].version` | Poetry projects (Poetry 1, or Poetry 2 without a `[project]` version); written alongside `[project].version` when both exist |
| `setup.cfg` `[metadata] version` / `setup.py` `version="…"` | legacy setuptools projects with a literal (an `attr:`/`file:` value is left alone) |
| `__version__ = "…"` (optionally `: str`) in `src/<pkg>/` or `<pkg>/` `__init__.py`, `_version.py`, `__about__.py`, `version.py` | only literal strings in files **not ignored by git** (a generated `_version.py` from setuptools-scm/hatch-vcs is skipped). `__version__ = version("pkg")` (`importlib.metadata`) is reported as a `note:` and left alone — it already follows `pyproject.toml`, which is this catalog's recommended pattern |
| Django `VERSION`/`APP_VERSION` in `*/settings.py` or `*/settings/*.py` | a literal, or the default of `os.environ.get("APP_VERSION", "…")`/`os.getenv(…)`/`env(…, default="…")` |
| `FastAPI(…, version="…")` in `app/*.py`, `src/<pkg>/**.py`, `*/main.py` | **conditional**: rewritten only when it equals the package version (it then tracks the package); a different value (`"v2"`, `"2024-01"`) is a deliberate API version and is left alone with a `note:`. It feeds the OpenAPI `info.version` |
| `docs/antora.yml` `version:` (with `--antora`) | mirror, **release versions only** (Step 7); never part of the agreement check |

Migrations, tests, docs, `build/`, `dist/`, virtualenvs and `node_modules/` are never searched. Then:

- **Dynamic version, VCS-derived** — `version: dynamic — … derived from git tags, nothing to change` (exit 0): the
  project has `dynamic = ["version"]` with hatch-vcs (`[tool.hatch.version] source = "vcs"`), setuptools-scm
  (`[tool.setuptools_scm]` or `setuptools-scm` in `build-system.requires`), `[tool.pdm.version] source = "scm"`,
  versioningit, or a `*-dynamic-versioning` plugin. **Stop here**: explain that the build backend computes the version
  from the latest git tag (a dev build between tags gets a `.devN+g<hash>` version automatically), that the release
  *is* creating the tag `X.Y.Z`, and that no file was touched; skip Steps 4, 6 and 7. `iru-release` then treats it
  like a Swift library or a plain Composer package (Step 5).
- **Dynamic version, file-based** — `[tool.hatch.version] path = "…"`, `[tool.pdm.version] path = "…"`,
  `[tool.setuptools.dynamic] version = {attr = "pkg.__version__"}` / `{file = "VERSION"}`, or flit (module
  `__version__`): the helper lists that file as the `(dynamic source)` location and rewrites it; `pyproject.toml` has
  no version to write. An `attr` that isn't `__version__` gets a `note:` — check it by hand.
- **Unrecognized dynamic source** or **no location at all** (non-zero exit) → don't invent one silently. Show
  `pyproject.toml` and ask whether to add `version = "<new-version>"` under `[project]` (removing `"version"` from
  `dynamic`), then re-run `--list`.
- **Locations disagree** (`WARNING: version locations disagree`) — show the list and ask whether to align every
  location to `<new-version>` (Step 4 then passes `--force`) or which to leave alone (edit only the others by hand and
  say so in the report). A stale `__version__` literal is the usual cause — aligning it is normally right, and worth
  suggesting a switch to `importlib.metadata.version()` so it can't drift again.
- The current version for the report (and for `iru-release`, which reads it this way) is the `current:` line — the
  first primary location (`[project].version`, else `[tool.poetry].version`, else the dynamic source file, …). With
  uv, `uv version --short` prints the same value for a static `[project].version` (it errors on dynamic versions).

## Step 3 — Look for mirrored mentions

```bash
grep -n -i "latest release\|current development version\|latest snapshot\|pip install\|uv add\|poetry add" README.md 2>/dev/null
grep -rln -i "latest release\|pip install\|uv add" docs/modules/ROOT/pages 2>/dev/null; grep -n '^version:\|^prerelease:' docs/antora.yml 2>/dev/null
grep -rn '"VERSION"[[:space:]]*:' --include='*.py' . 2>/dev/null | grep -v '/\.venv/\|/migrations/'   # drf-spectacular SPECTACULAR_SETTINGS["VERSION"]
```

Only when something turns up is `sync-files` worth asking about (Step 0).

## Step 4 — Preview (`dry-run: yes`) or apply

```bash
python3 "$TMPDIR/iru-python-bump-version/py_version.py" "<new-version>" --dry-run [--antora]   # unified diff only
python3 "$TMPDIR/iru-python-bump-version/py_version.py" "<new-version>" [--antora]             # write
```

Pass `--antora` only when Step 7's sync was accepted (`sync-files: yes`); add `--force` only after the user confirmed
aligning disagreeing locations (Step 2). The script rewrites exactly the first match of each location `--list`
printed — dependency `version = "^2.0"` specifiers, `requires-python`, other tables, other `*_VERSION` names, and every
other file stay untouched — and prints `note:`/`next:` lines:

- `next: uv lock` — `uv.lock` records this project's own version (`[[package]] name = "<project>"` followed by
  `version = "…"`, present for a static version; uv omits it for a dynamic one). Run `uv lock` from the same directory
  (not with `dry-run: yes`): it rewrites only that entry (`Updated <project> v<old> -> v<new>`) and keeps every other
  pin, so it works offline (`uv lock --offline`) when the cache is warm. Without it, CI's `uv sync --locked` fails with
  a stale-lockfile error. `poetry.lock`/`pdm.lock`/`requirements*.txt` don't record the project's own version — nothing
  to refresh there.
- `note: … FastAPI version … differs` — the API version was left alone deliberately (Step 2 table); mention it.
- `note: docs/antora.yml version left at …` — a pre-release value; expected (Step 7).

Why not `uv version <new-version>` / `poetry version <new-version>`: each only rewrites its own `pyproject.toml` field,
not `__version__` literals, Django settings, or the FastAPI constructor, so the locations would drift.

A non-zero exit at any point → stop, show the error, and treat nothing as updated; never fall back to hand edits.

## Step 5 — The Python-catalog pre-release convention (for `iru-release` and other callers)

The Python equivalent of `iru-java-bump-version`'s `-SNAPSHOT`, `iru-typescript-bump-version`'s `-dev.N` and
`iru-php-bump-version`'s `-dev` — the contract `iru-release` calls this skill against (two calls per release, each
passing a computed `<new-version>`), and the one the `sync.yml` written by `iru-setup-python-github-workflows` and the
`iru-setup-python-*` scaffolds (`version = "0.1.0.dev0"`) use:

- **Current development version**: `X.Y.Z.dev0` (e.g. `1.4.0.dev0`) on the integration branch — PEP 440's
  developmental-release segment, already in canonical form. PEP 440 orders `1.3.0 < 1.4.0.dev0 < 1.4.0a1 < 1.4.0rc1 <
  1.4.0`, so a dev build always sorts before the release it leads to, and pip/uv skip it unless asked for pre-releases
  (`--pre`, `--prerelease=allow`) — it can never be picked up by accident. `N` stays `0`; only increment it when a
  project deliberately publishes several dev builds of the same target.
- **Cutting a release**: strip the `.devN` segment — `X.Y.Z.dev0` → `X.Y.Z`. Call this skill with `<new-version>:
  X.Y.Z`; that is also the call that moves `docs/antora.yml` to `X.Y.Z` (with `sync-files: yes`). A project that
  ships release candidates may cut `X.Y.ZrcN` first — a pre-release, so Antora is not touched for it.
- **Opening the next development cycle**: bump the minor (this catalog's default, matching `iru-release`'s
  recommended "minor bump" and the `sync.yml` workflow) and append `.dev0` — `X.Y.Z` → `X.(Y+1).0.dev0`; a patch
  (`X.Y.(Z+1).dev0`) or major bump is the caller's choice. Call this skill again (or let `sync.yml` do it after the
  release is published) with that exact value — this skill never decides which component to bump.
- **Git tags** are the bare release version (`X.Y.Z`, no `v` prefix by this catalog's convention), matching the
  canonical PEP 440 string in `pyproject.toml`.
- **VCS-derived dynamic versions**: no in-tree marker at all — the release *is* the git tag; there is nothing to strip
  and no next-dev value to write (the backend derives `X.Y.(Z+1).devN+g<hash>` between tags by itself), exactly like
  `iru-swift-bump-version`'s library case. `iru-release` skips its "must currently be a pre-release" check and its
  next-version question for it.
- **Non-canonical legacy spellings** (`1.4.0-dev`, `1.4.0.dev`, `1.4.0-SNAPSHOT` — the last one is not PEP 440 at
  all) count as the development marker when reading the current version, but every value this skill writes is the
  canonical `.dev0` form after Step 1.

## Step 6 — Sanity check

Skip with `dry-run: yes`. Otherwise:

```bash
python3 "$TMPDIR/iru-python-bump-version/py_version.py" --list [--antora]   # every location now shows <new-version>
uv lock --check --offline                                                   # only when uv.lock exists: lockfile is fresh
uv version --short                                                          # uv + static [project].version: prints <new-version>
python3 -c 'import ast,sys; [ast.parse(open(f).read(), f) for f in sys.argv[1:]]' <each rewritten .py file>
```

`--list` must print `<new-version>` for every primary location and no disagreement warning; `ast.parse` proves each
rewritten Python file still parses (the rewrite only replaces a quoted literal, but report it rather than assume).
For a Poetry project, `poetry check` when Poetry is installed; otherwise say it wasn't run.

## Step 7 — Optionally sync other files that mirror the version

Ask (or honor `sync-files`) whether to update the mentions Step 3 found, mapping each by what it names — the same
rule as `iru-java-bump-version`'s Step 7:

- `docs/antora.yml` `version:` → `<new-version>` only for a release (Antora's component version names released
  versions; skip `.devN`/`aN`/`bN`/`rcN`), if the site tracks the release version at all — the helper's `--antora`
  flag does exactly this and leaves `~` (an unversioned component) alone. A `prerelease:` key, if the site uses one,
  is left as is and mentioned in the report.
- "Latest release" markers (and a `Latest release` row in the README's status table) → `<new-version>` when it is a
  release; untouched when `<new-version>` is a pre-release.
- "Current development version"/"Latest snapshot" markers → `next-version` when given; otherwise `<new-version>`
  only if it is a pre-release, and untouched (warn in Step 8 that the caller should pass `next-version`) when it's a
  release — never regress a development marker to a release value.
- An install snippet for this project's own package (`pip install <name>==X.Y.Z`, `uv add "<name>>=X.Y"`,
  `<name> = "^X.Y"`) → the release value, only for a release; a service (FastAPI/Django) usually has none — then only
  the markers apply.
- A drf-spectacular `SPECTACULAR_SETTINGS = {..., "VERSION": "…"}` (the OpenAPI `info.version` of a Django API) →
  same rule as the helper's `FastAPI(version=…)`: `<new-version>` only when it currently equals the package version;
  a separate API version (`"1.0.0"` for `/api/v1/`) is left alone and mentioned.
- Antora pages under `docs/modules/ROOT/pages/` with the same markers/snippets → as for the README.

Targeted, scoped substitutions only — never a repository-wide replace of the old string. Offered, not automatic: a
README badge pulling the version live (PyPI/GHCR shields) must not be rewritten.

## Step 8 — Report

- Every location from `--list` with its old value (and the `current:` value), the new version, and whether the input
  was normalized to its canonical PEP 440 form.
- Every file changed (by the script, by `uv lock`, and by Step 7), or for a VCS-derived dynamic version that nothing
  changed because the git tag is the version.
- Any disagreement that was aligned with `--force` after the user confirmed, any FastAPI API version left alone, any
  computed `__version__` noted, and whether `docs/antora.yml` was written (release) or left (pre-release).
- Whether this was a `dry-run`, and the Step 6 result (`--list` agreement, `uv lock --check`, `ast.parse` per file).
- **Warn explicitly**: review the diff before committing (this skill commits nothing); a `.devN` version uploaded to
  PyPI is permanent (PyPI never lets a version be re-uploaded) — only release versions should be published; a
  container image or OpenAPI document built from this commit carries the new version.

## Verification notes

Verified in `$TMPDIR/iru-verify/python/docs-bump/` with uv 0.12.8 by running the exact helper above with the host's
`python3` **3.9.6** (no `tomllib`, no `packaging`) against a `uv init --lib` project and hand-written fixtures:

- `--validate`: canonical output matched `packaging.version.Version` (via `uv run --with packaging`) for `1.4.0-dev`
  → `1.4.0.dev0`, `1.0-alpha.2` → `1.0a2`, `1!2.0.post-3` → `1!2.0.post3`, `1.0.0-1` → `1.0.0.post1`, `2.0RC1.dev` →
  `2.0rc1.dev0`, `1.0+ubuntu-1` → `1.0+ubuntu.1`, `01.02.003` → `1.2.3`; `not.a.version` → exit 1.
- uv library (`[project].version = "0.1.0.dev0"`, `__version__` literal, `app/main.py` `FastAPI(title=str("x"),
  version="0.1.0.dev0")`, `docs/antora.yml` `version: 0.0.9`): `--dry-run` printed the diff and wrote nothing
  (checksums unchanged); `0.1.0 --antora` rewrote all four; `uv lock` printed `Updated demo-lib v0.1.0.dev0 -> v0.1.0`
  and changed only that entry; `0.2.0.dev0 --antora` rewrote the three code locations and left `antora.yml` at
  `0.1.0` with the note; `uv lock --offline` then `uv lock --check --offline` passed; `uv version --short` printed the
  new value.
- Poetry `[tool.poetry] version = "1.2.0-dev"` → `1.2.0`, with a `requests = { version = "^2.0" }` dependency
  untouched. hatch-vcs and setuptools-scm (`[tool.setuptools_scm]`) → "derived from git tags", exit 0, nothing written.
  `[tool.hatch.version] path` → `__about__.py` rewritten, a `version("acme")` `__init__.py` reported as computed.
  `[tool.setuptools.dynamic] version = {attr = "acme.__version__"}` with `__version__: str = …` → rewritten.
  `setup.cfg` `[metadata] version` and `setup.py` `setup(version=…)` → rewritten.
- Django `APP_VERSION = os.environ.get("APP_VERSION", "0.5.0.dev0")` in `config/settings/base.py` → listed and
  rewritten; a `VERSION = …` inside `migrations/` ignored.
- `pyproject` `1.0.0.dev0` vs `__version__ = "0.9.0"` → refused with the disagreement warning; `--force` aligned both.
  A `FastAPI(..., version="v2")` → left alone with the note. A git-ignored `_version.py` → not listed. A
  `pyproject.toml` with no version → non-zero exit.

Not verified: a real Poetry 2 / PDM project end-to-end (`poetry check`), flit's module lookup (implemented, no
fixture), and real scaffolds from `iru-setup-python-*` (written in parallel) — run `--list` on the first real scaffold
and adjust nothing silently if a location is missing.

## Sources

- irurueta docs: programming-languages/python/virtual-environments-and-packaging.adoc (PEP 621 `[project]` table,
  interchangeable backends, build/publish)
- irurueta docs: backend/fastapi/openapi-and-interactive-docs.adoc (`FastAPI(version=…)` is the API version, bumped
  each release)
- irurueta docs: backend/fastapi/deployment.adoc (committed `uv.lock`, `importlib.metadata.version`)
- PEP 440 — Version Identification and Dependency Specification (normalization, `.devN` ordering)
