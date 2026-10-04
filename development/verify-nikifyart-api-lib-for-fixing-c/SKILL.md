---
name: verify
description: Run the full verification pass on a large change — clean-room install, complete test suite, lint, packaging check, CLI smoke test, and the project's safety invariants — then optionally collect any bugs or glitches the user hit. Use this skill whenever a hook reports a push exceeding the large-push line threshold, whenever the user types /verify, and whenever the user asks to verify, validate, sanity-check, or confirm that a big change actually works end to end. Prefer this over running tests ad hoc whenever a change is large enough that a passing test suite alone is not convincing.
---

# Verify

The deep check for a large change. `push-checkpoint` asks *did anything in this
batch look wrong*; `verify` asks *does the project actually still work from a
clean start*.

Run every step. A large change can break packaging, the entry point, or an
install path while every unit test still passes — those are exactly the failures
this catches.

## How this gets triggered

`.claude/hooks/push-counter.py` measures each successful push (insertions plus
deletions, read from the remote-tracking ref's reflog) and asks for this skill
when it exceeds `LARGE_PUSH_LINES`, currently 100. The user can also run
`/verify` at any time.

Skills cannot fire themselves on an event — the hook is what makes this
automatic. If verify never triggers on a big push, debug the hook, not this file.

## Step 0 — scope

The hook names the range it measured. Otherwise fall back to the last verified
point:

```bash
cat .claude/state/last-verified 2>/dev/null || echo "(never verified)"
git rev-parse HEAD
git diff --stat <range>
```

State what you are verifying before you start.

## Step 1 — clean-room install

Unit tests run against the working tree; users install a package. Verify the
install path separately, in a throwaway environment so nothing already present
can mask a missing dependency:

```bash
python3 -m venv /tmp/verify-env
/tmp/verify-env/bin/pip install --quiet -e ".[dev]"
/tmp/verify-env/bin/docfix --version
```

A missing dependency in `pyproject.toml` shows up here and nowhere else.

## Step 2 — the full suite

```bash
python3 -m pytest
```

Every test, no filtering, no `-x`. Report the count.

## Step 3 — lint

```bash
python3 -m ruff check .
```

Must be clean. Do not silence a rule to pass — fix the code, or say why the rule
is wrong here.

## Step 4 — packaging, against a real wheel

**An editable install cannot prove this.** `pip install -e` resolves data files
straight from the source tree, so a file missing from `package-data` works
perfectly in development and crashes for anyone who installs the package. This
has already happened once, to `docfix/fonts/catalog.yaml`.

So build a wheel and inspect it:

```bash
/tmp/verify-env/bin/pip install --quiet build
/tmp/verify-env/bin/python -m build --wheel --outdir /tmp/verify-wheel
/tmp/verify-env/bin/python -c "
import glob, zipfile
wheel = sorted(glob.glob('/tmp/verify-wheel/*.whl'))[-1]
names = zipfile.ZipFile(wheel).namelist()
data = [n for n in names if n.endswith(('.yaml', '.yml', '.json'))]
print('data files in wheel:'); [print('  ', n) for n in data]
assert any('presets' in n for n in data), 'preset YAML missing from the wheel'
assert any('catalog' in n for n in data), 'font catalogue missing from the wheel'
"
```

Then install that wheel — not the source tree — into a *second* clean
environment and confirm it actually runs:

```bash
python3 -m venv /tmp/verify-wheel-env
/tmp/verify-wheel-env/bin/pip install --quiet "$(ls /tmp/verify-wheel/*.whl)[pdf]"
/tmp/verify-wheel-env/bin/python -c "
from docfix.fonts import load_catalog, pool
from docfix.templates import list_presets, load
assert load_catalog().licenses, 'font catalogue did not load from the install'
assert list_presets(); [load(n) for n in list_presets()]
print('packaged install works')
"
/tmp/verify-wheel-env/bin/docfix --version
```

Any runtime data file — preset YAML, the font catalogue, anything loaded by
path rather than imported — must appear in that listing.

## Step 5 — exercise it for real

Not a unit test — actually use the tool on a real file:

```bash
printf '#  T  \n\n\n* a\n+ b\n\ntext   \n' > /tmp/verify-doc.md
/tmp/verify-env/bin/docfix check /tmp/verify-doc.md
/tmp/verify-env/bin/docfix format /tmp/verify-doc.md -t formal
cat /tmp/verify-doc.formatted.md
```

Read the output. Is it actually correct, or merely non-crashing?

## Step 6 — the invariants

These are the promises the project makes. Check them directly, not through the
tests that also check them:

1. **The source file is never modified.** Compare the input's checksum before
   and after a format run.
2. **Formatting is idempotent.** Format the output again; it must not change.
3. **Writing over the source is refused.** `docfix format f.md -o f.md` must
   exit non-zero.

```bash
md5sum /tmp/verify-doc.md
/tmp/verify-env/bin/docfix format /tmp/verify-doc.md -o /tmp/verify-2.md -q
md5sum /tmp/verify-doc.md   # must be unchanged
/tmp/verify-env/bin/docfix format /tmp/verify-2.md -o /tmp/verify-3.md -q
diff /tmp/verify-2.md /tmp/verify-3.md && echo "idempotent"
```

## Step 7 — record the verified point

Only if every step above passed:

```bash
git rev-parse HEAD > .claude/state/last-verified
```

Never record a verified point after a failure. `.claude/state/` is gitignored.

## Step 8 — report

State each step's result plainly:

- **Scope** — the range verified.
- **Install / tests / lint / packaging / real run / invariants** — pass or fail.
- **Failures** — root cause for each, and what you did about it.
- **Verdict** — is this change safe to build on?

Lead with a failure if there is one. A verify that always passes is worthless.

## Step 9 — optional: bugs and glitches

Only after reporting, and only if the session is interactive, offer the user a
chance to report anything *they* hit that the checks above would not catch —
wrong-looking output, confusing messages, rough edges.

Ask once, with `AskUserQuestion`, and make skipping the obvious default:

- "Nothing to report" (default)
- "Yes — something looked wrong"

If they have something, hand off to the `report-bug` skill to capture it
properly. If they skip, say nothing further about it.

This step is **optional and never blocking**. Do not ask it when running
unattended, do not ask twice, and never hold up the verdict waiting for it.
