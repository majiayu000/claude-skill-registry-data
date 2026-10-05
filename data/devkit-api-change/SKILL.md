---
name: devkit-api-change
description: Trace and verify every consumer before changing a public signature in src/devkit/ (env.py, db.py, oauth.py, mcpsecurity.py, mcpserver/, bridge/, bootstrap.py). Use when renaming, adding or removing a parameter, changing a default or return type, moving a symbol between modules, or when asked "what breaks if I change this".
allowed-tools: Read, Grep, Glob, Bash
---

# Changing a public signature in devkit

devkit is installed **editable** into every consumer's venv (`-e ${HOME}/Documents/code/devkit`).
A change here is live everywhere on the next process start — consumers break at *their*
next boot, not at yours, and nothing in this repo's test suite will catch it.
`CLAUDE.md` says "grep the consumers first". This is that procedure.

## The consumer set

Verified by import, not by assumption:

| Repo | Imports |
|---|---|
| `/storage1/Documents/code/erp` | `devkit.env`, `devkit.db` (`constants.py`, `database.py`), `devkit.mcpserver` (`mcp_tasker/`) |
| `/storage1/Documents/code/vacbat` | `devkit.env`, `devkit.db` (`solar/config.py`, `solar/db.py`, prefix `SOLAR`) |
| `/storage1/Documents/code/deebot` | `devkit.env`, `devkit.db` (`constants.py`, `database.py`) — a `devkit-new` scaffold |

Also in scope: **`src/devkit/bootstrap.py`'s templates**. The generated `constants.py`
and `database.py` are consumers too, and they are the only ones that will not exist yet
when you break them.

Re-derive the set rather than trusting this table if it looks stale:

```bash
grep -rln 'devkit' /storage1/Documents/code/*/ --include=*.py --include=*.txt --include=*.toml \
  | grep -v '/\.venv/\|/devkit/'
```

## Procedure

**1. Name the symbol, then find every call site in one parallel sweep.** Search the
consumer repos *and* `bootstrap.py` templates *and* this repo's own `tests/` in a single
batch of Grep calls — not one repo at a time.

Search for all of: the bare name (`load_env`), the qualified form (`db.connect`,
`devkit.env.load_env`), and any `from devkit... import` line that binds it under an alias.

**2. Read each hit.** A call site that passes the changed argument positionally breaks
differently from one that passes it by keyword. Grep counts are not an impact analysis.

**3. Classify the change.**

- *Additive with a default* — safe. Note it and move on.
- *Renamed / reordered / removed parameter, changed default, changed return type* —
  every hit must be updated in the same change, or the change is not done.
- *Moved between modules* — check for `from devkit.x import y` forms that will
  `ImportError` even though the symbol still exists.

**4. Verify by import, not by eye.** Each consumer has its own venv:

```bash
/storage1/Documents/code/erp/.venv/bin/python    -c 'import constants, database; print("erp ok")'
/storage1/Documents/code/vacbat/.venv/bin/python -c 'import solar.config, solar.db; print("vacbat ok")'
/storage1/Documents/code/deebot/.venv/bin/python -c 'import constants, database; print("deebot ok")'
```

Run these from each repo's own directory. A failure here is the whole point of the skill.

**5. If `bootstrap.py` templates changed**, scaffold into the scratchpad and boot it —
the generated project must still match the topology in `CLAUDE.md`:

```bash
devkit-new --help    # confirm the entry point still resolves
```

**6. Report** which consumers were touched, which were checked and clean, and which you
could not verify (e.g. a missing venv). Do not report "no impact" on the strength of a
grep that returned nothing — say what you searched for.

## Guardrail

Adding a helper to `env.py` or `db.py`? It must not add a dependency (invariant 1).
If it needs one, it belongs in a subpackage behind an extra in `pyproject.toml`.
