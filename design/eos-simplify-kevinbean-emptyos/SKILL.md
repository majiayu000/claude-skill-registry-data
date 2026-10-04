---
name: eos-simplify
description: Review *changed* code against EmptyOS conventions (CLAUDE.md patterns) for reuse, quality, and efficiency, then apply the fixes — the EmptyOS-aware cousin of the generic simplify skill. Use before committing a meaningful change, before eos-session-wrapup, or when the user says "simplify", "eos-simplify", "clean up my changes", "review my changes", or "check my work". Bare "review" is NOT this skill — it names no surface, and eos-architecture-review, eos-page-design-review and /code-review all answer to it. Quality only — NOT a correctness-bug hunt (use /code-review) and NOT a UI/design pass (use eos-design-system-audit / eos-page-design-review).
---

# EmptyOS Simplify

Review **changed** code against EmptyOS conventions, then fix what you find. This is the EmptyOS-aware cousin of the generic `simplify` skill: same spirit (reuse, quality, efficiency), but tuned to the patterns in `CLAUDE.md` so the review catches things a generic pass would miss.

Run this **before committing a meaningful change**, or when the user says "simplify", "clean up my changes", or "review my changes".

## When to Use

- After building or modifying an app, plugin, or shared SDK/frontend code
- Before `/eos-session-wrapup` or a commit
- When the user says "simplify", "eos-simplify", "clean this up", "review my changes", "check my work"

> **Bare "review" is NOT this skill**, in the body as well as the frontmatter — it names no
> surface, and `eos-architecture-review`, `eos-page-design-review` and `/code-review` all
> answer to it. Ask which, or route on what the user named.

## Scope

Operate **only on changed files** — don't rewrite the whole repo:

```bash
git diff --name-only HEAD
git diff --name-only --cached
git status --short
```

If nothing is changed, ask the user to scope the review (single file, single app, or a diff range).

## The Checklist

Work through these in order. For each finding, **fix it in place** unless it's a judgment call — then flag it and ask.

### 1. Capabilities over raw tools (backend)

Apps MUST use capabilities, never direct tools (CLAUDE.md §Development Rules 1).

Grep the changed `app.py` / plugin files for:

| Bad | Good |
|---|---|
| `open(path)`, `Path(...).read_text()` in an app | `await self.read(path)` |
| `requests.get`, `httpx.get` to an LLM | `await self.think(prompt, domain=...)` |
| `subprocess.run("grep ...")` in an app | `await self.search(query)` |
| `json.dump` to a vault path | `await self.vault_create_note(...)` or `self.vault_write(...)` |
| hardcoded vault path (`D:/Vault/...`) | `self.vault_config("key")` |

Exceptions: plugins may wrap external binaries directly; `data/` SQLite/JSON writes are fine.

### 2. Vault data access patterns

- If the app stores a collection of typed notes (songs, jobs, people…), it should use **VaultLibrary** (`emptyos/sdk/vault_library.py`), not hand-rolled `Path.glob()` + frontmatter parsing.
- If the app queries by frontmatter, prefer `self.vault_query(tags=..., **props)` over globbing.
- If the change adds a vault write, confirm the path comes from `_vault-map.toml` via `self.vault_config()`, not a string literal.
- **Two-domain rule**: human-authored / recovery-critical → vault; high-frequency telemetry → `data/`. Flag any crossover.
- **YAML-None crash check** — grep the diff for the fragile shape:

  ```bash
  grep -nE "\.get\([^)]+,\s*\"[^\"]*\"\)\.(lower|upper|strip|startswith|endswith|split|replace)" <changed-files>
  ```

  YAML `key:` (empty) parses to `None`, not absent. `dict.get(K, "")` returns the default *only when the key is missing* — when present-but-None, it returns `None`, and `.lower()` / `.startswith()` / `.split()` raises `AttributeError`. Fix shape: `(d.get(K) or "").method()` instead of `d.get(K, "").method()`. The `or` chain catches both `None` and absent. Triage hits by source: `fm.get(...)` / `props.get(...)` / `p.get(...)` from a YAML-parsed dict are dangerous; `request.headers.get(...)` / `request.query_params.get(...)` / `os.environ.get(...)` are always strings and safe. See memory `feedback_yaml_get_method_crash.md`.

### 3. Frontend reuse (EOS_UI / EOS helpers)

Grep the changed `pages/*.html` for reinvented wheels:

| Bad | Good |
|---|---|
| Hand-rolled modal `<div class="modal">` | `EOS_UI.modal({...})` / `EOS_UI.formModal({...})` |
| Hand-rolled stat cards grid | `EOS_UI.statCards([...])` |
| `confirm("Are you sure?")` | `EOS_UI.confirm({...})` |
| Custom settings sidebar | `EOS_UI.settingsPanel({...})` |
| Manual `location.hash` juggling for detail view | `EOS_UI.hashRoute({onShow, onHide})` |
| `esc(path)` for a vault note path | `EOS.noteActions(path)` — renders view + edit + open-external |
| Hardcoded `D:\` or backslash paths in JS | `EOS.normPath(path)` |
| Inline `<style>` redefining button / card / donut | reuse `eos-components.css` classes |

Then cross-check the changed page against `docs/FRONTEND-DESIGN-LANGUAGE.md` — specifically DL-1 (hardcoded hex colors), DL-2/3 (off-scale spacing/radius), DL-6 (forbidden patterns — `alert/confirm/prompt`, wheel UI, brand names), and DL-7 (AI-surface markers for any AI-authored content). Fix DL-1 and DL-6 in place; flag DL-2/3/7 if the call is non-mechanical. For a full-repo audit use `/eos-design-system-audit`.

### 4. Mandatory UI patterns

- Apps with `[provides.settings]` in manifest **must** have a ⚙ Settings button using `EOS_UI.settingsPanel` (`.claude/rules/app-ui-patterns.md` §In-App Settings Panel). If missing, add it.
- Apps with a `showDetail(id)` pattern **must** use `EOS_UI.hashRoute` so deep links work (CLAUDE.md §Deep-linking Detail Views). If missing, add it.
- Every POST/GET list API added in this diff should have a UI surface — no backend-only features.

### 5. Prompts are first-class (CLAUDE.md §Development Rules 12)

For any `self.think(...)` or `think_stream(...)` in the diff:

- Prompt text must be a module-top `UPPERCASE` constant, not inline f-string
- Persona/rules go in `system=` kwarg; the user message carries the specific request
- Content-generating prompts must include a **what NOT to do** section
- Temperature set explicitly: parsing 0.1–0.3, analysis 0.3–0.5, creative 0.6–0.8
- No thin prompts — user-facing output needs host persona + quality rules + structure

If a prompt is inline or missing these, refactor it to a constant and add the missing pieces.

### 6. Events over imports

If app A newly imports from app B, flag it. Cross-app coordination should use:

- `await self.call_app("otherapp", "method", ...)` for request/response
- `await self.emit("event:name", payload)` for fire-and-forget

Same for reverse: if the diff adds a new event emitter, confirm `[provides.events] emits = [...]` is updated in the manifest.

### 7. Manifest completeness

For each changed app, verify the manifest declares what the code actually does:

- New `@web_route` → `[provides.web] prefix = "..."` present
- New `await self.emit(...)` → event listed in `[provides.events].emits`
- New `self.call_app("X", ...)` → `"X"` listed in `[requires].apps`
- New capability used (`self.speak`, `self.draw`, ...) → listed in `[requires].capabilities`

### 8. Extract-shared heuristic (CLAUDE.md §Development Rules 9)

If the diff duplicates a pattern that already exists in another app (session runner, feedback form, metrics ring, SRS scheduler, etc.), flag it. Rule of thumb: **build specific first in one app; extract to `sdk/` when a second app needs it.** If this is the second app, propose the extraction — don't silently copy.

Cheap grep: pick a 3–5 line distinctive fragment from the new code and search other apps for near-duplicates.

**Same heuristic for workflows → skills.** Code-duplication isn't the only repeatable thing. If *you* hand-ran a multi-step workflow this session (a sequence of greps + edits + checks you walked manually, a prompt you typed near-verbatim, a process you narrated step-by-step), and you'd done that same shape before, it's a `.claude/skills/<name>/SKILL.md` candidate — the workflow analogue of an SDK extraction. Same trigger as code: **second occurrence, not first** (don't make a skill for a one-off — that just bloats the library). Same action: **flag it, don't auto-build** — propose "this felt repeatable; want a skill?" so the user decides. Extraction is a build step (`/eos-sdk-extract` for code, hand-writing a `SKILL.md` for workflows), not something simplify does silently.

### 9. Wellbeing wheel as lens, not feature (CLAUDE.md §Development Rules 16)

**Refuse** UI additions that expose the 8-dimension wheel to the user:

- dimension pickers / tag selects
- "which dimension does this serve?" prompts
- wheel visualisations inside an app's own page

The wheel is a silent rubric for *what gets built*, not what the user sees. Manifest-level `dimensions = [...]` is allowed; user-facing dimension UI is not. If found, remove it and explain why.

### 10. Branding & personal data

Run the two scripts on the diff:

```bash
python scripts/check-personal.py
python scripts/check-branding.py
```

- **Personal**: no personal paths/names/coordinates/API keys in tracked files — move to `emptyos.toml` (gitignored)
- **Branding**: no Obsidian/Suno/Kindle/etc. in app UIs, prompts, error messages — use generic terms ("markdown vault", "source URL", "Open external"). Plugin code integrating with a specific service is exempt.

Fix violations before continuing.

### 11. Tests for the change

- Touched an app's UI → run `pytest tests/test_sys_<app>.py -v`
- Touched an app's API/backend → `pytest tests/ --ignore=tests/personal -k "not test_ui" -v`
- Multi-app change → full `pytest tests/ --ignore=tests/personal -v`
- New app → ensure `tests/test_sys_<new>.py` exists with 10+ cases
- Fixed a bug → add a user-story test that would have caught it (`tests/test_user_stories.py`)
- **Any test added in this diff → prove it fails without the fix.** A test that has only
  ever been green is not evidence that it pins anything (`.claude/rules/audits.md` §Failure
  mode 3). Invoke `.claude/skills/eos-mutation-verify` — **don't re-derive the loop by hand**;
  this checklist item exists because a simplify pass caught exactly that omission.

If tests fail, fix the code (not the test) unless the test itself encodes stale behaviour.

### 12. Small-thing hygiene

- Windows paths normalised (`.replace("\\", "/")` or `EOS.normPath()`)
- No comments explaining WHAT the code does — keep only WHY comments for non-obvious invariants
- No `// removed` or `# TODO: cleanup` debris from the edit
- HTML pages hot-reload; Python changes need server restart — mention if the user needs to `restart.bat`

## Report Format

After the pass, output:

```
EOS Simplify — <N> files reviewed

Fixed in place:
  - apps/foo/app.py: inlined prompt → module-top FOO_SYSTEM constant
  - apps/foo/pages/index.html: replaced hand-rolled modal with EOS_UI.modal
  - apps/foo/manifest.toml: added "bar" to [requires].apps

Flagged (needs your call):
  - apps/foo/app.py:142 — duplicates session-runner from apps/practice/; extract to sdk/?
  - apps/foo/pages/index.html — proposes a wheel-dimension picker; removed, confirm intent

Safety:
  check-personal: CLEAN
  check-branding: CLEAN

Tests:
  test_sys_foo.py — 12 passed
```

Keep the report tight. Don't restate the diff; surface only what was changed by this pass and what still needs user judgment.

## Safety

- **Only modify files already changed in the working tree** — don't drag unrelated files into the cleanup.
- **Preserve behaviour** — simplification, not redesign. If a fix would change app behaviour materially, flag it instead of applying it.
- **Never touch `emptyos.toml`, `data/`, or anything under `apps/personal/` or `engines/personal/`** unless the user's diff already touched them.
