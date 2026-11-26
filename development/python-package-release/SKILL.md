---
name: python-package-release
description: "Use when packaging or publishing a Python repo with uv to PyPI."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [python, packaging, uv, pypi, release, ci]
---

# Python package release

Turn working scripts into an installable, publishable package. uv is the toolchain; PyPI
via trusted publishing is the destination.

## When to Use

- "Package this up", "make it installable", "publish it as our own `<x>` package"
- A script or toolkit needs a CLI entry point, tests and CI
- Cutting a version tag or wiring a release workflow

## When NOT to Use

- Deploying a service → `kernel-ops-ship`
- Publishing npm/Node packages

## Rules

1. **uv for everything**: `uv sync`, `uv lock`, `uv run`, `uv build`, `uv tool install`.
   Never `python -m venv` + manual activation, never bare `pip install` into a project.
2. **Gate before every commit and push**: `uv run ruff check .`, `uv run ruff format --check .`,
   `uv run pytest`. A red gate is not a stylistic problem, it is a stop.
3. **Prove the artifact, not the source tree.** `uv build`, then `uv tool install --force .`
   and run the console script by name. Import errors and entry-point typos pass pytest and
   only surface for a real user.
4. **Never publish to PyPI yourself.** Prepare everything, then hand over the one step that
   needs the user's PyPI login. Publishing is irreversible: a version number is spent
   forever, even if the upload is wrong.
5. **Check the name is free before naming anything.**
   `curl -s -o /dev/null -w '%{http_code}' https://pypi.org/pypi/<name>/json` — 404 means
   available. A 200 means pick another name and rewrite the URLs in `pyproject.toml` and the
   README now, not after the build.
6. **Scan for personal data and secrets before the first public push, not after it.** A tool
   built on someone's real data carries names, phone numbers and message counts into README
   examples, docstrings and test fixtures without anyone deciding to publish them. Public is
   forever: a follow-up commit does not un-publish the earlier one, so the scan is a
   pre-push gate and the only cheap moment to fix a hit is before `gh repo create --push`.
   Run `scripts/check_no_pii.py` over `git ls-files` plus a secrets scan over history, and
   read the README and every example by hand — a scanner cannot recognise a contact's name.

## Procedure

1. **Layout**: `src/<package>/` with `__init__.py` (holding `__version__`), `cli.py`,
   modules, `tests/`, `README.md`, `LICENSE`, `CHANGELOG.md`, `.python-version`.
2. **`pyproject.toml`**: setuptools backend, `package-dir = {"" = "src"}`,
   `packages.find where = ["src"]`, dynamic version from
   `attr = "<package>.__version__"`, `[project.scripts]`, dev tools in
   `[dependency-groups]` (not optional-dependencies).
3. **Lock and gate**: `uv venv && uv sync --all-groups`, then the three gate commands.
   Commit `uv.lock`; a library still benefits from a reproducible dev environment.
4. **Porting a working script? Prove behavioural equivalence on real data.** Re-run the old
   tool and the new package over the same live input, then set-diff record ids, diff each
   record's fields and byte-compare the generated files. Identical output is the bar for
   "refactor, not rewrite". Where a diff remains, re-read the live source before blaming the
   package — a live database or feed mutates between runs and can explain the delta honestly
   (and it must be reported, not hidden).
5. **Tests need a real fixture, not mocks of the parser.** Build the input the code actually
   consumes (a synthetic database, a fixture file) in `tests/conftest.py` and test the
   public API against it. Mock-shaped tests reimplement the old behaviour and pass while
   production breaks.
6. **Ignore before the first commit**: `.venv/`, `dist/`, `build/`, `*.egg-info/`,
   `__pycache__/`, caches. Whatever is staged in the initial commit is what the world sees.
7. **Scan the tracked tree before the first push** (rule 6): `python3 scripts/check_no_pii.py`
   for phones, emails, uuids and home paths; `gitleaks detect --source .` for credentials.
   Then read the README, docs and fixtures for names and real totals a regex cannot catch.
8. **Repo**: `git init -b main`, conventional commits, then
   `gh repo create <name> --public --source=. --remote=origin --push`. Confirm public vs
   private with the user first — visibility is their call, and it is public forever.
9. **CI**: matrix over the supported Pythons, `uv sync --locked`, lint, format check, tests,
   type check and coverage gate (see Hardening), plus the PII check and a secrets scan so the
   gate survives future commits. Copy `templates/ci.yml` and adjust.
10. **Release**: tag-triggered workflow with a version/tag equality check, then
    `uv publish --trusted-publishing always` in an `environment: pypi` job with
    `permissions: id-token: write`. Copy `templates/release.yml`.
11. **Create the environment the workflow names**:
    `gh api -X PUT repos/<owner>/<repo>/environments/pypi --input - <<< '{"deployment_branch_policy": null}'`.
12. **Hand over the PyPI step** and say exactly what to fill in: PyPI → Publishing → add a
    pending publisher with the project name, owner, repo, workflow filename and environment.
    Then `git tag v<version> && git push origin v<version>` triggers it.

## Hardening the test suite before a public release

A package that reads someone's data has a silent-corruption failure mode that ordinary
example tests miss. Before the first public release, add:

- **Property tests for the parser/decoder/serialiser.** Generated input, not hand-picked
  examples: arbitrary bytes never raise, every truncation is safe, `decode(encode(x)) == x`
  across every encoding branch, and valid payloads wrapped in junk still decode. `hypothesis`
  in Python. This is what finds the decoder bug that a fixture-based suite never will.
  Fixtures are created once per test _function_, not per example, so anything a fixture sets
  up (temp database, directory) must be built inside the example body.
- **Strict typing, and ship it.** `mypy --strict` (or pyright strict) over `src/` only, plus a
  `py.typed` marker so consumers get the annotations. Untyped `dict`/`Counter` generics are
  usually the only real complaints once the code is annotated.
- **A coverage floor that actually holds.** 100% is reachable on a stdlib package, but it
  flakes once property tests are in play: a randomized example reaches a branch only
  sometimes. Add one deterministic example per branch a property only sometimes covers, then
  run the gate three times before trusting it. Enforce it in `pyproject.toml`
  (`fail_under`) and in CI (`--cov-fail-under`), and add a committed SVG badge if the repo
  should show it without a third-party service.
- **Profile before publishing, not after.** A data-processing core usually hides one nested
  scan: `sum(1 for m in rows if m[g] == group[g])` inside a loop over groups is O(rows x
  groups) and can be a third of runtime — a single `Counter` pass replaces it. Measure with
  `cProfile` on real data, fix only the dominant line, then prove the output is identical to
  the previous version over the full dataset. An optimization that cannot show that equality,
  or that does not move the number, gets reverted rather than kept.

## Pitfalls

- **A patch commit does not scrub a leak already pushed.** If personal data reached a public
  remote, rewrite history (`references/pii-scrub.md`), force-push, and then _prove_ it: scan
  every blob in `git rev-list --all`, fetch the raw file back from GitHub, and check remote
  HEAD equals local. Tell the user the old objects still dangle on GitHub until it garbage
  collects, and that anyone who cloned in the window keeps a copy — do not claim it is gone.
- **Scan history with the gitleaks CLI on a repo whose first commit is a root.** Its GitHub
  Action derives a `<before>^..<after>` range from the event payload and asks git for
  `<root>^`, which cannot resolve; it exits "stderr is not empty" without scanning anything
  while the check reports failure. Install a pinned binary and run
  `gitleaks detect --source . --redact --verbose --exit-code 1` with `fetch-depth: 0`.
- **Verify an action's major tag exists before pinning `@vN`.** Releases can ship `v10.3.1`
  with no moving `v10` tag, and GitHub only fails at run time with "Unable to resolve".
  Check with `gh api repos/<owner>/<repo>/git/matching-refs/tags/v` and pin the newest tag
  that actually exists.
- **A dynamic `attr` version needs the package importable at build time.** If `package-dir`
  and `packages.find` disagree, the build succeeds and the wheel is empty — check the wheel
  contents with `unzip -l dist/*.whl`, not just that the file exists.
- **`python -m <pkg>` and the console script are separate wiring.** Test both; the
  `__main__.py` path is easy to leave broken because nothing imports it.
- **Do not trigger the release workflow before the PyPI publisher exists.** It fails at the
  publish step after consuming a tag, and re-tagging the same version is refused.
- **Do not fight a blocked `pip install` on the user's machine**; `uv tool install` gives the
  CLI its own environment and keeps the system interpreter clean.

## References

- `references/pii-scrub.md` — rewriting history with `git-filter-repo --replace-text`,
  re-adding the remote it drops, force-pushing, and proving the leak is gone from every blob
  plus what the rewrite does not undo.

## Scripts

- `scripts/check_no_pii.py` — scans `git ls-files` and fails on any phone number outside the
  reserved 555-01xx range, any email outside the allowlist (edit it for the maintainer's own
  address), any message/attachment uuid, any `/Users/<name>` path, and anything in an optional
  `--denylist FILE` kept outside the repo. Wire it into CI next to lint.

## Templates

- `templates/ci.yml` — lint, format check and tests across a Python matrix, plus a build job
  with a `twine check` metadata gate.
- `templates/release.yml` — tag-triggered build, tag/version equality check, trusted
  publishing to PyPI, GitHub release.
