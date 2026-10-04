---
name: eos-sdk-extract
description: Detect cross-app duplication and extract the smallest honest shared unit into emptyos/sdk/, codifying CLAUDE.md Dev Rule 9 (extract on the *second* caller, not the first). Use when the user says "extract", "sdk-extract", "dedupe the apps", "what's been copy-pasted", when you notice a familiar pattern while editing an app, or as a periodic health pass. NOT for single-app refactors or speculative design-for-the-future helpers — two real callers is the floor.
---

# EmptyOS SDK Extract

Detect cross-app duplication and extract shared logic into `emptyos/sdk/` — codifying CLAUDE.md §Development Rule 9 ("build specific first in one app, extract to `sdk/` when a second app needs it"). The rule is active only if someone runs it; this skill is the runner.

Goal: **find duplicated patterns across ≥2 apps, extract the smallest honest shared unit, update callers, verify tests still pass.** Not refactoring for beauty — refactoring to stop the third app from also copying it.

## When to Use

- User says "extract", "sdk-extract", "dedupe the apps", "what's been copy-pasted"
- You just noticed while editing an app that the pattern looked familiar
- `/eos-simplify` flagged "this duplicates fragment from `apps/<other>`"
- Periodically, as a health pass — even if no one asked

**Not** for single-app refactors, new abstractions without a concrete second caller, or "design-for-the-future" helpers. Two callers is the floor. One caller is premature.

## Prerequisites

**No daemon required.** Every phase runs offline: the scans are static, the SDK
unit tests and the Phase 6 equivalence harness are pure-Python, and `pyflakes` /
`check_undefined_names.py` need nothing running.

A daemon is used by **exactly one optional check** — Phase 6 step 5, the caller
system tests — and only if `:9000` happens to already be up. If it isn't,
**do not start it**: `python -m emptyos start` / `restart.bat` / `taskkill`
against `:9000` are forbidden from a Claude session
(`.claude/rules/daemon-handling.md`). Skip the step and say so, or lease a
sandbox member (`.claude/rules/sandbox-driven-testing.md`).

Needs `pyflakes` on PATH (`pip install pyflakes`) — Phase 6 step 2 is the cheapest
catch for an import the extraction left behind.

## Process

Run phases in order. Every extraction is a **behaviour-preserving** change — no signature drift, no widened contract.

---

### Phase 1: Find Candidates

Look for duplication at three granularities — start wide, narrow down:

**1a. Module-level: duplicate imports across apps**
```bash
grep -rhn "^from emptyos.sdk" apps/ apps/personal/ --include="*.py" 2>/dev/null | sort | uniq -c | sort -rn | head -20
```
If many apps reuse the same SDK helpers, good — that's what the SDK is for. If many apps re-implement what an SDK helper already does, that's the inverse problem (Phase 1e).

**1b. Function-level: similarly-named private helpers**
```bash
grep -rhn "^    def _\|^def _" apps/ apps/personal/ --include="*.py" 2>/dev/null \
  | awk -F: '{print $3}' | sort | uniq -c | sort -rn | head -20
```
When `_parse_session`, `_extract_metrics`, `_score_attempt` appear in ≥2 apps, open all copies and compare.

**1c. Fragment-level: distinctive 3–5 line blocks**
Pick a distinctive-looking line from the app you're currently touching — something with a unique string literal, regex, or sequence of calls — and grep for near-duplicates:
```bash
grep -rn "<distinctive-fragment>" apps/ apps/personal/ --include="*.py"
```
Manually compare bodies around the hits. Rename drift (`session_id` vs `sess_id`) is still a duplicate.

**1d. Structural duplicates (names diverged, bodies identical)**
```bash
python scripts/sdk_duplicate_scan.py               # default: apps/, min 4 stmts
python scripts/sdk_duplicate_scan.py --min 3       # loosen
python scripts/sdk_duplicate_scan.py apps plugins  # extra roots
```
Parses every function body, strips locals to positional placeholders, hashes the normalised AST, and reports groups of identical bodies. Catches what 1b/1c miss: copy-paste where callers renamed variables, *and* inline code in one app that matches a helper in another. The duplicate that surfaced `_weekly_path` across 3 personal apps + 2 inline copies in `apps/public/standard/journal/app.py` came from this pass — grep would never have found it because the core app had no method name to grep for.

Treat each reported group as a Phase 2 candidate: open all listed sites, confirm they're doing the same job, then proceed.

**1e. Reimplementation of existing SDK helpers**
Scan for functions that do what these already do:
- `parse_frontmatter` / `strip_frontmatter` → many apps still hand-split on `---`
- `parse_llm_json` → many apps still `json.loads(text.strip("`").removeprefix("json"))`
- `slugify` → many apps roll their own
- `task_tier`, `compute_task_decay` → task-like apps reinvent scoring
- `VaultLibrary` → collections apps reinvent query+create
- `SessionStore` / `HistoryStore` → practice-style apps reinvent session runners
- SRS helpers `sm2_schedule`, `srs_due_items` → flashcard apps

**1f. Mixin families across apps**
```bash
grep -rn "^class \w\+Mixin" apps/ apps/personal/ --include="*.py"
```
Mixins are cohesive bundles (methods + state) composed via multiple inheritance. The 1d scanner hashes function bodies individually and will miss the *bundle* even when individual methods drift enough to not hash-collide. For each mixin file, list its public method names; if ≥2 apps have mixins whose method-name sets overlap meaningfully (≥3 shared names, or same domain — "vault stats", "session runner", "timeline"), that's a candidate for promotion to `emptyos/sdk/` as a shared mixin or small base class.

Classify each hit before treating it as a candidate:
- **App-family decomposition** (one app split into sibling mixins: `apps/reactor/reactions_*`, `apps/music-studio/{library,lyrics,visual,compose}.py`) → **not duplication**, skip. These are compositional decomposition within one app.
- **Cross-app reuse** (same mixin shape appears in ≥2 unrelated apps, e.g. two apps both exposing vault-health methods) → candidate for Phase 2.
- **Absorbed from a retired app** (single file like `apps/public/standard/app-analytics/vault_mixin.py` with no second caller today) → park; flag for re-review when a second caller appears.

Extraction target for cross-app mixins: a module in `emptyos/sdk/` exposing the mixin class (e.g. `emptyos/sdk/<name>_mixin.py`), apps changing `class MyApp(BaseApp, VaultMixin)` to import from sdk. Phase 3's "don't add a new base class casually" still applies — prefer pure functions when state isn't actually shared across methods.

For each candidate, record: **file paths**, **function names**, **approximate LOC per copy**, **variance** (identical / renamed / behavioural drift).

---

### Phase 2: Pick One and Confirm the Threshold

The bar from CLAUDE.md: **two callers minimum, actual duplication, not "might be useful someday."**

For the candidate, ask honestly:

| Check | Must hold? |
|---|---|
| Does it appear in ≥2 apps today? | **Yes** — one caller = premature |
| Are the copies doing the same job, not just looking similar? | Yes — coincidental shape is not duplication |
| Is the shared core stable, or are the copies diverging in meaningful ways? | Stable — if they're diverging on purpose, leave them |
| Would a third app landing tomorrow copy it again? | Yes — that's the predictive signal |
| Is there a natural name for the shared unit? | Yes — if you can't name it, you haven't found the boundary |

If any answer is "no," park the candidate and pick another. **Don't extract to hit a quota.**

---

### Phase 3: Design the Shared Unit

Smallest honest surface. Follow the shape of what's already in `emptyos/sdk/`:

- **Pure functions** go in `utils.py` (or a new single-purpose module) — e.g. `parse_llm_json`, `slugify`
- **Stateful helpers** get their own module — `session.py` (SessionStore), `srs.py` (scheduler), `vault_library.py` (collection base)
- **Domain scorers / math** get their own module — `scoring.py`, `stats.py`, `audio.py`
- **Base classes** stay in `base_*.py` — don't add a new base class casually

Rules:
- **Inputs/outputs must match the union of existing callers** — no widening, no narrowing. If caller A passes `session_id: str` and caller B passes `int`, either (a) both accept and normalise, or (b) don't extract — the drift is real.
- **No app-specific defaults** — if one copy hardcodes a path or tag, that config stays in the app, not in the SDK.
- **No imports from `apps/` or `plugins/`** — SDK is a leaf; apps depend on it, never the other way around.
- **Add to `emptyos/sdk/__init__.py`** so `from emptyos.sdk import X` works.

Write the signature down (single line) and show the user before writing the code:

```
Proposed extraction:
  emptyos.sdk.<module>.<name>(<args>) -> <return>
  Callers today: apps/<a>/..., apps/<b>/...
  Replaces: ~<N> lines per caller, <M> lines total
OK to proceed?
```

---

### Phase 4: Write the Shared Unit

Add the function / class to the chosen SDK module (new file only if none of the existing ones fit).

Constraints:

- Docstring: 1 line + rules section (when to use, when **not** to use). Follow `vault_library.py` / `srs.py` style.
- No f-string logging with secret paths — use `log.info("session %s", session_id)` style
- Prompts, if any, follow CLAUDE.md §Development Rule 12 — `UPPERCASE` constants, `system=` kwarg, explicit temperature, include "do NOT" examples
- Export from `emptyos/sdk/__init__.py` — add to both the `from ... import ...` block and `__all__`
- **No new dependencies** unless the user approves — check `pyproject.toml` before `import`-ing something new

Write a tiny test at the same time. Pick the pattern from `tests/test_sdk_*.py` if those exist; otherwise add a new `tests/test_sdk_<name>.py`. Do NOT put the test in
`tests/helpers.py` — that is the shared-assertion module, it holds no `test_*`
functions, and pytest's `python_files = test_*.py` never collects it, so a test
written there silently never runs. One test per branch of the function's behaviour — not comprehensive, just enough to catch a regression from a careless caller update.

---

### Phase 5: Update the Callers

Touch **only the N apps that were Phase 1 candidates**. Don't drag third-party callers in.

Per caller:
1. Replace the local helper/method with `from emptyos.sdk import <name>` + call site
2. Delete the old helper body (don't leave dead code behind)
3. If the local copy had app-specific config baked in, pass it as an argument — don't add a default to the SDK helper
4. Remove any now-unused imports in the caller

Diff hygiene:
- Each caller's diff should show: **N lines removed, 1–2 lines added** for the call + 1 import line
- If a caller's diff is growing (more lines after than before), stop — either the extraction is wrong or the caller needs app-specific glue you're hiding in the SDK

---

### Phase 6: Verify

**Step 0 — the equivalence harness. Do this first; it is the real evidence.**

Unit tests prove the *new* helper does what you decided it should. They say nothing
about whether it does what each *old* copy did — which is the only question an
extraction has to answer. Write a throwaway script that defines every pre-migration
body **verbatim** (copy them out of `git diff` / `git show HEAD:<file>`) and diffs
them against the helper over a deliberately hostile corpus:

```python
# scratchpad/<name>_equiv.py — throwaway, not committed
def orig_kb(s):        # verbatim pre-migration body, one per caller
    ...
CASES  = [("kb", orig_kb, dict(fallback="untitled")), ...]      # + each caller's kwargs
CORPUS = ["", "  ", "!!!", "机器学习", "Café", "a -- b", "2026-08-16",
          "a" * 90, "\xa0nbsp\xa0", "MULTI   SPACE", "_under_"]  # exotic > typical
for name, orig, kw in CASES:
    for t in CORPUS:
        assert orig(t) == new_helper(t, **kw), (name, t, orig(t), new_helper(t, **kw))
```

Report the comparison count (`N callers × M inputs`). The corpus must include the
inputs the *union* of callers could see — non-ASCII if any caller is vault-facing,
empty/whitespace-only, and anything longer than the shortest `max_len`.

When the originals **disagree with each other** on some input (they usually do, on
out-of-contract input like `None`), that is a finding, not a blocker: pick one,
state which callers change, and say so in the Phase 7 report. Don't paper over it.

```bash
# 1. SDK tests pass
python -m pytest tests/test_sdk_<name>.py tests/test_sdk_utils.py -q   # whichever applies

# 2. Static gates — catch an import the move left behind
python -m pyflakes <every changed file>      # undefined names + now-dead imports
python scripts/check_undefined_names.py      # incl. TYPE_CHECKING-only names

# 3. No lingering copy of the old helper anywhere
grep -rn "def <old_helper_name>" apps/ --include="*.py"     # expect 0
grep -rnF '<the distinctive regex/fragment>' <migrated files>   # expect 0

# 4. Import surface is stable
python -c "from emptyos.sdk import <name>; print('<name> importable')"

# 5. Each caller's system tests — ONLY if the daemon is already up
curl -s -m 5 http://127.0.0.1:9000/api/health -o /dev/null -w "%{http_code}\n"
python -m pytest tests/test_sys_<a>.py -q
```

**Never run `python -m emptyos start` or `python -m emptyos health` to make step 5
possible.** Both boot the kernel and open a syslog SQLite handle — forbidden from a
Claude session by `.claude/rules/daemon-handling.md`. If the daemon is down, say so
and lean on step 0; to verify Python changes end-to-end, lease a sandbox member
instead (`.claude/rules/sandbox-driven-testing.md`).

Also note the daemon holds the **pre-change** Python until it restarts, so a green
`test_sys_<a>` against a stale `:9000` is evidence about the old code, not yours —
see `feedback_harness_that_cannot_reproduce_lies`.

**Regression bar:** behaviour of the callers must be indistinguishable from before.
Step 0 is what establishes that; system tests are corroboration. If step 0 diverges
on in-contract input, the extraction widened or narrowed the contract — narrow the
helper, or leave that caller out.

---

### Phase 7: Report

```
SDK Extract: <name>

Location:
  emptyos/sdk/<module>.py          (+<N> lines)
  emptyos/sdk/__init__.py          (+2 lines — import + __all__)
  tests/test_sdk_<name>.py         (+<T> lines, <C> cases)

Callers migrated:
  apps/<a>/app.py                  −<X> lines
  apps/<b>/helpers.py              −<Y> lines
  Net: −<X+Y−N> lines across the codebase

Verified:
  equivalence  <N> callers x <M> inputs = <N*M> comparisons, all identical
  pytest       sdk + sys_<a> + sys_<b>   all passed   (or: daemon down, not run)
  static       pyflakes + check_undefined_names clean
  no orphan copies (grep clean)

Behaviour deltas (if any):
  - <input>: originals disagreed (<a> gave X, <b> gave Y) — unified to Z

Deferred (not extracted):
  - <candidate>: only 1 caller today — reconsider when a 2nd appears
  - <candidate>: copies are drifting deliberately — keep separate
```

End of turn: suggest `/eos-simplify` on the diff (catches any convention slip in the new SDK file) and `/eos-session-wrapup` at end of session.

## Safety

- **Two callers minimum.** One-caller "extractions" are the single most common mistake this skill exists to avoid. Park them.
- **Never widen the contract to unify drifting copies.** If A and B are diverging, they're not the same function anymore — leave them.
- **SDK has no upward deps.** No `from apps...`, no `from plugins...`. SDK is a leaf.
- **Behaviour-preserving only.** Don't "fix" a bug in the copies during extraction — that belongs in a separate commit so it shows up in git log.
- **Don't batch extractions in one pass.** One extraction, one commit, one verification. Stacking them makes rollback impossible.
- **Don't add new dependencies** to satisfy the extraction. If the pattern needs a new library, stop and ask.
- **`apps/personal/` code can be a caller** but must not be the *only* second caller if the SDK helper is meant to ship — personal apps are gitignored, community apps can't depend on their patterns.

## Relationship

- Pre-commit on the extraction diff → `/eos-simplify` (catches convention slip in the new SDK file)
- End of session with an extraction → `/eos-session-wrapup` (devlog captures the before/after LOC)
- Find candidates proactively as part of health review → `/eos-architecture-review` check mode
- New app built after extraction → `/eos-new-app` scaffold will naturally use the extracted helper
