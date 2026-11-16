---
name: test-architecture-rule
description: Use when forbidding X in layer Y with a static grep firewall — an architecture test, its path constants, a rule fragment, a bounded allow-list. Owns `tests/unit/test_architecture.py` in a standalone distributable and `tests/test_architecture.py` at the root of a repository of several members. Runtime behaviour belongs in an ordinary test; the constitution is `test-principles`.
---

# Test — Architectural Firewall Rule

Each function greps the source tree for a forbidden pattern and asserts the result is empty. What the file holds is wider than its name: every rule here is a property of the *source text* that no runtime test can reach, and most but not all of those are architectural — a ban on exiting the process outside the entry point is a rule about the process, enforced the same way. The name is the established one for this artifact and is worth keeping; read it as "the static source rules", not as a promise that every rule in the file is about layering. Where the file sits follows the shape of the tree, not the architecture family: one distributable puts it at `tests/unit/test_architecture.py`; a repository holding several members puts it at `tests/test_architecture.py` beside them, because its subject is the repository rather than anything in it. The firewall must stay collectable when the tree is broken.

## When to use vs. neighbours

- A static, absolute "layer Y must not import X" invariant the codebase needs enforced → this skill.
- Shared testing constitution → `test-principles`. That is prose the whole suite obeys; this is one
  grep that reddens a build.
- Runtime domain behavior → `hex-test-domain`, in the `pyhouse-hex` plugin.
- Runtime storage behavior → `flat-test-persistence`, in the `pyhouse-flat` plugin. Greps enforce
  static structure; runtime tests enforce dynamic behavior.
- Hex layer boundaries → `hex-architecture`, in the `pyhouse-hex` plugin.
- Flat repository boundaries → `flat-layered`, in the `pyhouse-flat` plugin.
- A type-correctness rule → `mypy` / `pyright` enforce it; do not duplicate as a grep test.
- A style or formatting rule → `ruff` enforces it; do not duplicate.
- A "should usually" rule with material exceptions → not a firewall candidate; document it in the
  skill that owns the layer instead. Firewalls are absolutes that accumulate exceptions and stop
  paying for themselves.
- An intent-based rule ("do not use `Any` *unless* at a true external boundary") → not a firewall
  candidate; greps either hit or do not, with no intent inspection.

## Template(s) — `grep` through `subprocess`, one plain pytest function per rule

### File scaffold (once per repository)

The standalone form follows — one distributable, one `src/`, one `tests/`. A repository of several
members replaces the path-constant block with the multi-member fragment below; the imports, the
`_grep` helper and every rule in this skill are identical in both.

```python
import subprocess
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / "src" / "myapp")
_TESTS = str(_ROOT / "tests")
_UNIT_TESTS = str(_ROOT / "tests" / "unit")


def _grep(pattern: str, *paths: str) -> list[str]:
    if not paths:  # a glob that matched nothing must not leave grep reading stdin
        return []
    result = subprocess.run(
        [
            "grep",
            "-rnE",
            "--include=*.py",
            "--exclude=test_architecture.py",
            pattern,
            *paths,
        ],
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]
```

Patterns run under `-E`: basic `grep`'s `\|` alternation is a GNU extension that BSD `grep` does not
reliably carry, while `-E` behaves the same on both. `grep` exits 1 when it finds nothing, which is the
ordinary case, so the helper must not check the return code — it reads `stdout` and lets an empty result
be an empty list. `parents[2]` walks up from `tests/unit/`; a firewall placed directly under `tests/`
uses `parents[1]`, and that constant is the only line the move changes.

### Multi-member path constants

For a repository of several members with the firewall at `tests/test_architecture.py`, replace the
scaffold's constants with the block below. The member directory names are a constant so that a
repository grouping its members differently overrides one tuple and every glob follows. `_TESTS` is a
list here, so a rule splats it: `_grep(pattern, *_TESTS)`.

```python
_ROOT = Path(__file__).resolve().parents[1]

# The directories under which this repository's members live, as it declared them.
_MEMBER_DIRECTORIES = ("packages", "services")
# Source trees only: a member's tests/ legitimately names what its src/ may not.
_SRC_DIRECTORIES = [str(path) for directory in _MEMBER_DIRECTORIES for path in _ROOT.glob(f"{directory}/*/src")]

# Tests live beside the member they cover, plus the root's own.
_TESTS = [str(path) for directory in _MEMBER_DIRECTORIES for path in _ROOT.glob(f"{directory}/*/tests")] + [
    str(_ROOT / "tests")
]
_UNIT_TESTS = [str(path) for directory in _MEMBER_DIRECTORIES for path in _ROOT.glob(f"{directory}/*/tests/unit")]
```

### Standard rule (no allow-list)

```python
def test_no_<rule_name>() -> None:
    hits = _grep("<pattern>", <paths>)
    assert hits == [], "<message>:\n" + "\n".join(hits)
```

Concrete, in the standalone form:

```python
def test_no_future_annotations_anywhere() -> None:
    hits = _grep(r"^from __future__ import annotations\b", _SRC, _TESTS)
    assert hits == [], "from __future__ import annotations found:\n" + "\n".join(hits)
```

The multi-member form is the same function over `*_SRC_DIRECTORIES, *_TESTS`.

### Rule with an in-test allow-list

The one allow-listed path is a constant at the top of the file, beside the others (rule 4). The example
is `exception-catalog` rule 13 enforced: the entry point is the one scope that renders a caught error and
maps it to an exit code, so a process exit anywhere else is a second rendering:

```python
_ENTRYPOINT = str(_ROOT / "src" / "myapp" / "__main__.py")


def test_no_process_exit_outside_the_entrypoint() -> None:
    all_hits = _grep(r"\bsys\.exit\(", _SRC)
    forbidden = [hit for hit in all_hits if not hit.startswith(_ENTRYPOINT)]
    assert forbidden == [], "sys.exit() outside the entry point:\n" + "\n".join(forbidden)
```

The pattern stays simple; the exception is explicit and visible to whoever reads the failure. A
library has no entry point, so there the rule is a standard one with no allow-list.

### Adding a new path constant (when a new scope is needed)

Append at the top of the file, next to the existing constants:

```python
_<SCOPE> = str(_ROOT / "src" / "myapp" / "<package>")
```

## Other bindings

- **Import-linter contracts**, declared in config and run as their own command. Forbidden
  relationships become layer and forbidden-module contracts instead of patterns, and because it
  resolves real imports there are no word-boundary or docstring false positives. One rule per
  contract, the named allow-list, the failure naming the offending module and the never-ship-it-red
  rule are unchanged; the firewall stops being a test, so collectability moves to the linter's run.
- **A linter's banned-API rule** (`flake8-tidy-imports`' `banned-api` under ruff). Cheapest — it runs
  in a pass the project already has, scoped per directory. It reaches import rules only, so every
  non-import invariant (a process exit, a sleep, a module-level engine) stays here and most projects carry
  both, and the hard stop on restating what the linter enforces decides which file a rule goes in.
- **An `ast` walk over the tree.** Distinguishes an import from the same word in a docstring, and a
  module-level call from one nested in a function. Only `_grep` is replaced — every rule below holds,
  and rule 8's escaping advice becomes a node test instead.

## Rules

Consult `test-principles` for the testing constitution. Where this skill contradicts
`test-principles`, the constitution wins. The *words inside* a rule's name — which layer, which
thing, which verb — are `naming`'s decision; the **patterns those words go into are rule 2 here**.

1. **One test function per rule, with nothing around it.** No fixtures, no parametrization, no async —
   `def test_*() -> None` under the pytest binding — and no `try/except` or conditional skip around the
   search, which would break the unconditional property that makes a firewall worth having. The test name **is** the rule, and the file's test
   list reads as the workspace's structural constitution.
2. **A rule's name states its scope and what is absent, in the form its meaning takes.** Do not
   pluralize, do not add qualifiers.
   - **A scope has no X:** `test_<scope>_has_no_<thing>`, e.g. `test_domain_has_no_pydantic`.
   - **X only inside a scope:** `test_no_<thing>_outside_<scope>`, e.g.
     `test_no_statement_outside_the_data_access_package`.
   - **X nowhere:** `test_no_<thing>`, e.g. `test_no_future_annotations_anywhere`.
   A name that does not say where the rule looks sends a reader to the pattern to find out, and the
   file stops being readable as a constitution.
3. **The failure names every offending location, never a count or a boolean.** Assert the collected
   hits against an empty collection so the runner prints the actual list beside the expected one —
   `assert hits == []` under pytest. `assert not hits` and `assert len(hits) == 0` say the firewall is
   red and nothing about where.
4. **Every scope a rule names is a named constant at the top of the file.** Add a new `_<NAME>`
   constant when a new scope is needed; a path written inside a test drifts silently when the tree
   moves, and the rule keeps passing over a directory that no longer exists.
5. **Run the rule against the current tree before committing.** Confirm zero unexpected hits, and
   never ship a firewall that is already red — narrow it or fix the hits. A rule that arrives red
   teaches everyone to skip it. A sweep widened over a directory holding a sanctioned exception lands
   with that exception's allow-list entry, in the same change.
6. **Exceptions are allow-listed inside the test, by name, and cap at three.** Filter the result
   against named paths — `startswith(...)` against a path constant under the grep binding — rather
   than weakening the pattern, so the pattern stays readable and the exception is visible to whoever
   reads the failure. A fourth entry means the rule has too many exceptions to be a firewall: split it
   into something more specific, or demote it to prose.
7. **A rule never imports what it forbids, or anything from the tree it polices.** Importing it
   defeats the firewall, and the file must stay collectable when the tree is broken — a broken import
   turns "the rule failed" into "the rule could not be collected", which reads as green in some
   reports.
8. **A pattern matches the whole token it names and nothing that merely contains it.** Under
   `grep -E` that is raw strings wherever a backslash appears, `\b` at both ends of a bare word, and
   plain `|` for alternation. A pattern that also catches a longer identifier, a comment or a
   docstring makes the rule's own name a lie, and the first false hit is what gets it deleted.
9. **An exemption for a package because of the role it holds reads the role's name from a constant
   the project declared, never from a directory name** — a hardcoded name is green on every project
   that named that package something else, and checks nothing. One constant per declared name; a
   per-member override table is a second allow-list with no cap (rule 6).

Each architecture family lists the invariants worth a firewall in its own architecture skill
(`hex-architecture`, in `pyhouse-hex`; `flat-layered`, in `pyhouse-flat`).

## Inlined typing / import rules

- `subprocess` and `pathlib.Path` only at the file level (already present).
- In a grep rule, never import from `myapp` — importing what you're trying to forbid defeats the firewall.
- Tests are sync `def test_*() -> None`.

## Hard stops

- The rule depends on intent or on runtime state → stop, this is not a grep-firewall rule; runtime
  behaviour is an ordinary test, and an intent-based rule is prose in the skill that owns the layer.
- The rule restates something the linter or type checker already enforces → stop, two enforcers for one
  rule means two places to change it.
- A "no `Protocol` in services" rule is proposed → stop unless the repository genuinely has none: a
  style that permits a port the moment a second implementation exists turns this into an allow-list
  that outgrows three entries, which rule 6 forbids. It is prose, not a firewall — the flat family
  already carries it as prose in `flat-layered`, in the `pyhouse-flat` plugin.
- Asked for the testing constitution the whole suite obeys → stop, use `test-principles`.
