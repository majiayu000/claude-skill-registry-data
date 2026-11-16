---
name: release-packaging
description: Building and releasing Navigator -- the navigator-fm distribution and navfm alias on PyPI, the single __version__, python -m build and twine, the .deb/.rpm built by packaging/linux/build.sh with nfpm, the apt/dnf repositories, GPG signing-subkey rules, .github/workflows/release.yml, native_version.py, and `nav --version`. Use for anything about packaging, versions, PyPI, Linux packages or the release workflow.
---

# Packaging and releasing

Packaging is setuptools via
`pyproject.toml`: `./venv/bin/python -m build` (needs `pip install build`, and setuptools 77+ for the PEP 639
`license = "MIT"` expression the metadata uses).

**The packages are listed in `setup.py`, not `pyproject.toml`**: Help's pages are `docs/` at the top of the
repository and are installed as `navigator/docs/` (`package_dir`), a package `packages.find` cannot find. Its
package-data takes `**/*.md` and `**/*.ans` only (`navigator-help` skill, *Shipping*). Everything else is still
`pyproject.toml`'s.

The **distribution** name is `navigator-fm`; the **import** names stay `navigator`, `navkit`, `navml` and the command
stays `nav`. Plain `navigator` and `nav` were taken on PyPI before this project existed. Installation folds only runs of
`-`, `_` and `.` into one separator, but *registration* is stricter -- PyPI refuses a new name that collides with an
existing one once those characters are deleted outright, so `navigator-fm` reserves `navigatorfm` against everybody,
this project included; see below. Versions are placeholders in the 0.0.x series until the first real release, which
keeps 0.1.0; PyPI never lets a version number be re-used, so a botched upload costs a version rather than being
replaceable.

**The version is written in exactly one place**, `navigator/__init__.py`'s `__version__`. `pyproject.toml` declares
`dynamic = ["version"]` and reads it through `[tool.setuptools.dynamic]`, which setuptools resolves by parsing the
syntax tree rather than importing the package -- so it must stay a plain string literal, and the build needs none of
the run-time dependencies to find it. `packaging/navfm/pyproject.toml` deliberately does *not* track it: the alias
depends on `navigator-fm` unpinned, so it is re-uploaded approximately never.

Verify a build with
`./venv/bin/python -m twine check dist/*` and by installing the wheel into a throwaway venv and running `nav
--list-themes` from *outside* the checkout -- that is what proves the `importlib.resources` asset lookup survives
installation, which a run from the repository root cannot.

`nav --version` prints the version, the directory the running copy was imported from, and the interpreter, in
`pip --version`'s format. The path is the point: Navigator can be installed as a system package, a pipx copy and a
checkout at once, and `~/.local/bin` precedes `/usr/bin` on most PATHs, so the copy that runs is often not the one
that was just installed. `version_banner()` prefers `importlib.metadata` over `__version__` because the two diverge
exactly when a checkout has been edited since it was installed.

`packaging/navfm/` holds the one near-miss name worth holding, as its own project with its own `pyproject.toml`,
`README.md` and a copy of the root `LICENSE` (setuptools will not follow `license-files` out of a project directory).
It is an **alias, not a build of this code**: `packages = []` makes it a metadata-only distribution whose sole
dependency is `navigator-fm`, unpinned, so `pip install navfm` resolves to the current real release and never has to be
re-uploaded alongside it. Adding a module to it would defeat the point.

```
./venv/bin/python -m build -o dist .
./venv/bin/python -m build -o dist packaging/navfm
./venv/bin/python -m twine check dist/*
```

`navigator-fm` has to reach PyPI before the alias is installable, so upload it first. The alias chain is verified by
`pip install --find-links dist navfm` into a throwaway venv: it must pull `navigator-fm`, `pyte`, `pygments`, `watchdog`, `markdown-it-py`, `docutils` and `boto3` in behind it and
leave a working `nav`.

`packaging/linux/` builds the `.deb` and the `.rpm`, both from one `nfpm.yaml`:
`NFPM=/path/to/nfpm PYTHON=./venv/bin/python ./packaging/linux/build.sh` after a `python -m build`. Output lands in
`build/pkg/` (gitignored). Three things about it are load-bearing:

- **The tree is staged by `pip install --target`, not by copying directories**, so the files that reach the package
  are exactly the ones the wheel declares -- `navigator/styles/*.nss` included. `build.sh` then asserts the stylesheet
  and every theme the checkout has (counted there, not a fixed number) are present, because losing them yields an
  application that starts and *then* fails to theme.
- **One `arch: all` / `noarch` package serves every interpreter from 3.12 up**, because every dependency is pure
  Python. A venv could not: it bakes its minor version into `lib/python3.N/site-packages` and into `pyvenv.cfg`, so it
  would need one build per distro. `build.sh` fails the build if a `.so` ever appears in the staged tree, since that
  is the moment the claim stops being true. One is removed first: wcwidth (pyte's) ships an *optional* C accelerator
  in a platform wheel since 0.9 and falls back to its own Python without it (`HAS_C_EXTENSION`). PyYAML's libyaml loader (`yaml/_yaml*.so`) goes the same way, `yaml` falling back to its
  pure-Python reader. python-bidi is held
  below 0.5 for the same reason (0.5+ is Rust); it and arabic-reshaper are vendored like the rest, `six` with them,
  so distributions' `python3-bidi` (Ubuntu 24.04: 0.4.2) is never a dependency.
- **`/usr/bin/nav` runs `python3 -sP`, and the `-P` is not hygiene.** A file manager is launched inside arbitrary
  directories, and without it a directory that merely *contains* an `icons.py` or a `pyte.py` shadows the real module,
  so Navigator dies on startup in that one directory and nowhere else. This is verified, not assumed: dropping a
  decoy `pyte.py` into the working directory crashes `-s` and leaves `-sP` untouched.

`packaging/linux/repo/` publishes the two repositories, and `.github/workflows/release.yml` drives the whole release
from a `v*` tag: tests, then PyPI, then the packages, then the site. Four things there are not obvious:

- **The repository scripts add to a published site, they do not build one.** apt indexes by scanning the pool and
  `createrepo_c` by scanning the directory, so the previously released files have to be *present* or the new index
  silently forgets them and every pinned or older install breaks. The workflow checks out `gh-pages` first for that
  reason, and passes `EXPECT_AT_LEAST` -- the count read off the live site -- so the scripts refuse to publish an index
  smaller than reality. Comparing before with after inside one run cannot catch this: a run that started from an empty
  directory has nothing to lose, which is exactly the failing case.
- **`GPG_KEY_ID` must be the *signing subkey's* 16-hex-digit long key id**, and each half of that sentence was paid
  for. nfpm parses it as a 64-bit integer, so a 40-character fingerprint is `value out of range` -- and so is a
  17-character one, which is what `make-signing-key.sh` printed until it stopped slicing the id off the end of the
  fingerprint. Given the *primary's* id nfpm fails differently and far less helpfully, with `no valid signing keys`:
  CI holds an `--export-secret-subkeys` export, so the primary is a stub with no private key, and it is certify-only
  besides. `ghaction-import-gpg` has the same blind spot from the other side -- without its `fingerprint` input it
  presets the passphrase against the stub primary's keygrip and dies on gpg-agent error 67108891 (source 4,
  code 27, `NOT_FOUND`) before nfpm is ever reached. gpg itself is the relaxed one: `--local-user` takes a subkey id
  without complaint, which is why the repository scripts never noticed the question. `release.yml`'s
  published-key check therefore matches `GPG_KEY_ID` against **both** the `pub` and `sub` records of the committed
  keyring; matching `pub` alone rejected precisely the value that works.
- **The two ecosystems verify different things.** apt verifies the *index* (`InRelease`/`Release.gpg`) and takes
  per-package integrity from the SHA256 in `Packages` -- it does not check per-package signatures at all. dnf is the
  reverse: `gpgcheck=1` verifies a signature inside each `.rpm`, which nfpm has to write at *build* time, and
  `repo_gpgcheck=1` verifies `repomd.xml.asc`. Signing only one half of either leaves a repository that warns or
  refuses.
- **CI signs with a subkey, and that subkey is exported *without* a passphrase.** `make-signing-key.sh` exports
  `--export-secret-subkeys`, so the certifying primary never leaves the maintainer's machine and a leaked CI secret
  can be revoked without users having to trust a new key. The missing passphrase is not an oversight: **nfpm cannot
  decrypt a subkey whose primary is the `gnu-dummy` stub such an export leaves behind**, and fails with
  `signing key is encrypted` no matter what passphrase it is given -- measured against nfpm 2.47.0, which is the
  latest, with a key whose passphrase was known. The same file with no passphrase signs. The alternatives were
  handing CI the full secret key, which puts the certifying primary on a build runner and gives up the property
  above, or taking the `.rpm` signature away from nfpm and doing it with `rpmsign`. Dropping the passphrase costs
  least, because it never protected anything: it would have lived in the same GitHub secret store as the key it
  protects. `make-signing-key.sh` asserts the export is unprotected rather than trusting it, since the failure
  otherwise surfaces only in CI. There is consequently **no `GPG_PASSPHRASE` secret** -- do not reintroduce one.

The apt half is verified end to end without Docker: point the real `apt-get` at a private `Dir::State`/`Dir::Cache` and
a `file://` source, and it accepts the signed repository, lists both published versions and refuses the same repository
under a different key (exit 100, `NO_PUBKEY`). The rpm half has no such local check -- `createrepo_c` and `rpm` are not
installed here -- and is exercised only in CI.

`native_version.py` imports **`packaging`, the PyPI distribution** -- not `packaging/`, this repository's directory of
the same name -- so `build.sh` needs it installed and names it if it is missing. Every development venv carries it via
`build` and `pytest` and a bare CI runner does not, which is why the release workflow installs it explicitly and why
its absence first surfaced as a `ModuleNotFoundError` several jobs into a release.

`native_version.py` maps a PEP 440 version onto the Debian and RPM spelling, and `tests/test_packaging.py` checks the
result against `dpkg --compare-versions` rather than against a table -- what matters is the ordering, not the string.
A pre-release takes `~` so it sorts *below* its release; `.devN` takes **two**, because past a single tilde `a` < `d`
would put `~dev5` after `~a1` and invert PEP 440. That inversion is asserted in the tests so the reason cannot be
optimised away.

**Do not add a `packaging/navigatorfm/` back.** It was tried and PyPI answered `400 Bad Request`. PyPI "ultranormalises"
a proposed new name -- separators deleted rather than folded, and confusable characters such as `l`/`1`/`i` and `0`/`o`
run together -- and refuses it if the result matches an existing project. `navigator-fm` ultranormalises to
`navigatorfm`, so that spelling is already reserved against everyone and is unregisterable by us for the same reason.
The 400 carries no explanation (warehouse#17375), which is what makes this worth writing down. The same rule is why
`navfm` is a separate name and does have to be held deliberately.


## Assets must survive installation

Assets are found through `importlib.resources`, never relative to `__file__`. `navigator/styles/*.nss` and
`navigator/styles/themes/` (which has its own `__init__.py`) are declared as package data; **a new asset directory needs
a matching `[tool.setuptools.package-data]` entry** or it works from a checkout and vanishes on install. Component
markup and stubs ship through the one `"*" = ["*.nml", "*.pyi"]` key.
