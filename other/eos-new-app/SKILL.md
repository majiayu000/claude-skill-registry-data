---
name: eos-new-app
description: Scaffold a new EmptyOS app end-to-end with every convention wired from the start — manifest, capabilities, EOS_UI helpers, settings panel, deep-link routing, test file, vault-map entry, release-tier registration — so it is runnable, testable, and release-ready the moment the skill finishes. Use when the user says "new app", "create app", "scaffold app <id>", or "add an app for <purpose>". Begins with a mandatory spec grill unless a grill-spec note is supplied. NOT for plugins (use eos-new-plugin) or apps whose logic is personal (those live in apps/personal/ and skip release tiers).
---

# EmptyOS New App

Scaffold a new core app end-to-end with every EmptyOS convention wired in from the start — manifest, capabilities, UI helpers, settings panel, deep-link routing, test file, vault-map entry, and release-tier registration. The goal is that the app is **runnable, testable, and release-ready** the moment this skill finishes.

## When to Use

- User says "new app", "create app", "scaffold app `<id>`", "add an app for `<purpose>`"
- Before starting any app that doesn't exist under `apps/` or `apps/personal/`
- **Not** for apps whose logic is personal → those go under `apps/personal/` and skip release-tier registration

## Reference files (read on demand)

`SKILL_DIR` = `D:/emptyos/.claude/skills/eos-new-app/`. The harness loads only
this file; read a sibling with the Read tool when you reach the step that needs it.

| File | Priority | Read when |
|---|---|---|
| `<SKILL_DIR>/scaffold-templates.md` | **Required before Step 3** | Every file template you write to disk — manifest, INTENT.md, app.py, index.html, test file, birth baseline, report |
| `<SKILL_DIR>/grill-questions.md` | Required for Step 1 Phase 1 | The 14-question bank + the Explore prompt + the spec-note section list |
| `<SKILL_DIR>/app-builder-mode.md` | Reference | The user asks about the autonomous loop, or a settled spec should be handed to `app-builder` |

---

## Process

Run steps in order. The grill at Step 1 is mandatory unless the user provides a `spec=<path>` arg pointing at an existing grill spec note (see "Pre-grilled spec" below) — naming and dependencies are hard to change later, and trivial-looking apps usually have a non-trivial sub-pattern hiding.

### Pre-grilled spec

If the user invokes this skill with `spec=<vault-path-to-spec.md>` (or pastes a grill spec note inline), skip Step 1 and read the spec instead. Specs are produced by:
- The web grill app at `/grill/` (recipe `new-app`)
- A previous Claude Code session that ran the Step 1 grill below

A valid spec has `tags: [grill-spec]` + `recipe: new-app` in frontmatter, plus a "Scaffold checklist" section. If frontmatter or checklist is missing, treat it as freeform notes and run Step 1.

---

### Step 1: Grill the Spec

Asking a 10-item form in one shot works for the 5th CRUD list app — it bites for everything else, because the model and the user both miss the manifest knobs that hurt later (hub-panel? voice-intent? addons? boards-view-layer? settings panel? hash routing? vault_map entry?). The grill front-loads those by walking through them with reasons attached.

**Phase 0 — Gate.** One question:

> Is this a trivial CRUD list app (matches the auto-UI shape: list + add + delete + optional stats), or a new shape (canvas / dashboard / generator / instrument / reading-surface)?

If "trivial CRUD": skip Phase 1 with these defaults — verb=add/list/delete, data_shape=vault notes OR data/ JSON (ask which), no hub panel, no voice intent, no detail view, capabilities=[read, write]. Re-ask only the genuinely required fields (id, name, description, where data lives). Skip Phase 2 brainstorm too; go straight to Phase 3 spec, then Phase 4 review.

If "new shape": run Phase 0.5 → Phase 1 → Phase 2 → Phase 3 → Phase 4 in order. Trivial CRUD also runs Phase 0.5 — duplicate-app catches are highest-value here.

**Phase 0.5 — Prior-art pass.** Before asking the user anything else, spawn a single Explore agent (quick breadth, ~60s budget) with the working title/verb to surface:

1. **Existing apps with overlapping verbs or data shapes** — under `apps/` and `apps/personal/`. If found, list with one-line summary of what they do today.
2. **SDK helpers that already cover what's being asked** — `emptyos/sdk/` (e.g. `VaultLibrary`, `BaseApp.embed_text`, `srs.py`, `parse_llm_json`). If a helper exists, the new app should consume it, not reimplement.
3. **`.claude/rules/` files this app will likely trigger** — based on the verb, name which rules to read before Phase 1.
4. **Plugins that already provide the capability** — if the app would just wrap an existing plugin (e.g. `playwright`, `comfyui`), flag it.

The Explore prompt template is in `grill-questions.md`. Surface the findings as a "Prior art" block back to the user. Then ask **one decision question**:

> Prior art found above. Proceed with a new app, or extend an existing one / contribute a hub-panel/voice-intent to it?

If the user picks extend/contribute, stop this skill and hand off (read the relevant rule file and edit the existing app's manifest). If they pick "proceed with new app", run Phase 1 — but feed the SDK helpers + rule files into the grill so the answers are informed. If the Explore agent returns nothing useful, proceed to Phase 1 silently — don't pad with empty results.

**Phase 1 — Grill.** Read `<SKILL_DIR>/grill-questions.md` and work the 14-question bank (1A Problem & Users, then 1B Solution shape). One question at a time; send each "Why" line with its question.

**Phase 2 — Brainstorm pass (mandatory for "new shape", skip for trivial CRUD).** With answers in hand, propose 2-3 alternative shapes the app could take (e.g. "as a vault-notes app with a hub panel" vs. "as a derived view over `apps/public/core/task` data" vs. "as a generator with no persistent storage") and let the user pick. Often the first answer to Phase 1 is the obvious shape; the brainstorm surfaces the non-obvious shape that would have been better. State the tradeoff for each (what it makes cheap, what it makes expensive later) — don't just list names.

**Phase 3 — Write the spec note (BA-shaped).** Write the answers + decisions to `{vault}/30_Resources/EmptyOS/grill/new-app-<id>-<ts>.md` with frontmatter `tags: [grill-spec]`, `recipe: new-app`. Section list: `grill-questions.md` §Phase 3. Anyone reading it should understand who the app is for and what "done" means, without re-running the grill.

**Phase 4 — Review gate (mandatory).** Before touching `apps/<id>/`, post the BA spec summary back to the user — problem + users + stories + acceptance + out-of-scope + non-functionals + solution shape + scaffold checklist — and ask one question:

> Spec looks like this. OK to scaffold, or anything to change?

Wait for explicit go-ahead. Common late corrections: "actually make it personal", "drop the hub panel", "rename to `<x>`", "data should be data/ JSON not vault". Edit the spec note in place and re-post the diff; don't move on until the user confirms. **Skip the review only if** the user invoked with `spec=<path>` (they already authored it) or said "just scaffold it" / "no review" up front.

If the user picks `personal`, the app goes under `apps/personal/` and Steps 6 + 7 are skipped.

---

### Step 2: Pre-flight

```bash
# Check id is free
ls apps/<id> apps/personal/<id> 2>/dev/null && echo "CLASH" || echo "OK"

# Check id doesn't shadow a plugin
ls plugins/<id> 2>/dev/null && echo "CLASH" || echo "OK"
```

Abort and ask for a new id if either clashes.

---

### Step 3: Create `apps/<id>/manifest.toml`

**Read `<SKILL_DIR>/scaffold-templates.md` now** — it holds the literal templates for Steps 3, 3.5, 4, 5b, 6, 9, and 10. Fill the manifest template from the Step 1 spec. Omit `[provides.settings]` if the spec said "none"; omit `[provides.events]` if emits is empty.

---

### Step 3.5: Create `apps/<id>/INTENT.md`

Every new app gets a **living design doc** alongside the manifest. The grill spec is the **birth certificate** (frozen at scaffold time); `INTENT.md` is the **living doc** (moves with the code); `{vault}/10_Projects/emptyos/log/app-development.md` is the **auto-written changelog**. Three docs, three lifetimes, three jobs. Don't conflate them. Template + fill rules: `scaffold-templates.md` §Step 3.5.

---

### Step 4: Create `apps/<id>/app.py`

Skeleton in `scaffold-templates.md` §Step 4. It must use capabilities (not raw tools), declare prompts as UPPERCASE constants, and wire the declared events.

Rules the skeleton must satisfy — verify before writing:

- `BaseApp` subclass, not a plain class
- All I/O via `self.read/write/search/think/vault_*` — no `open()`, no `requests`, no raw `subprocess`
- Hardcoded vault paths forbidden → use `self.vault_config("key")`
- If the app has `[provides.settings]`, read values with `self.app_config("<key>", <default>)`
- If the app calls an LLM, always pass `system=<ID>_SYSTEM` and set `temperature=` explicitly (0.1–0.3 parsing, 0.3–0.5 analysis, 0.6–0.8 creative)
- **DO NOT write a `@web_route("GET", "/")` handler to serve `pages/index.html`.** The platform auto-mounts `pages/index.html` at `{prefix}/` whenever the `pages/` directory exists (see `emptyos/web/server.py` `_mount_loaded_app_routes`). A custom `/` handler shadows the auto-mount and breaks the UI.
- **EmptyOS is FastAPI, not aiohttp.** Never import from `aiohttp.web`. Route handlers return plain `dict` (auto-serialized to JSON) or `fastapi.responses.HTMLResponse` / `FileResponse` for non-JSON content.

---

### Step 5: Decide whether you need a custom `pages/index.html`

**Default: skip this step.** New CRUD apps render via the auto-UI (`emptyos/web/auto_ui.py`) using the shared component bundle — list with hover-revealed trash buttons, "+ Add" modal with inferred fields, stats tiles where applicable. No HTML to write, full CRUD on first boot.

**Write a custom `pages/index.html` only when**:
- The app's primary surface isn't a list (deep-canvas like `canvas`/`improv`/`board`, single-shot generators like `voice-assistant`, dashboards with bespoke layouts).
- The app needs interactions auto-UI doesn't synthesize (drag-to-reorder, inline cell edit, custom widgets like cover pickers / audio recorders / map views).
- The app is a "reading surface" (journal, blog post viewer) where the layout *is* the product.

If none of those apply, ship without `pages/`. **Migration path** when an author wants to upgrade: open `http://localhost:9000/<id>/`, view source, save as `apps/<id>/pages/index.html`, edit. The platform serves `pages/index.html` in preference to auto-UI when both exist.

### Step 5b (only if Step 5 said "yes"): Create `apps/<id>/pages/index.html`

Template: `scaffold-templates.md` §Step 5b. Use the shared helpers; do not reinvent modals, cards, or detail routing. Never omit the stylesheet + `eos-components.js` imports.

---

### Step 6: Create `tests/test_sys_<id>.py`

Template + traceability-docstring rules: `scaffold-templates.md` §Step 6. Aim for **10+ cases** across API + UI per `.claude/rules/testing.md`. **Derive the test list from the spec's `## Acceptance criteria`, don't invent it** — every criterion maps to ≥1 named test; unmapped tests are labeled edge/regression.

If the app stores data anywhere `conftest.py` doesn't already clean up, add a cleanup block there keyed on `TEST_PREFIX`.

---

### Step 7: Register in `release.toml` (skip if personal)

Add `"<id>"` to the appropriate tier's `apps = [...]` list. Default is `standard` unless the spec said `core`.

```bash
python scripts/package-release.py --check
```

Must exit clean.

---

### Step 8: Vault-Map Entry (skip if no vault data)

If the app writes user-authored notes to the vault, declare where. Vault-map lives at `{vault}/30_Resources/EmptyOS/_vault-map.toml`. Read the current vault connection from `.claude/vault-connection.json`, open the file, and add:

```toml
[<id>]
path = "30_Resources/EmptyOS/<id>"
description = "<what the app stores>"
```

`self.vault_write(...)` will land under that path; `self.vault_config("path")` reads it. **Never hardcode a vault path in `app.py`.**

---

### Step 8.5: Mark the app installed in the Store gate

**Why this step exists.** The Store maintains per-user install state at `data/store/installed-apps.json`. Its first-boot seed (`store_state.seed_if_missing`) only fires when that file is **missing** — once any daemon has booted on this machine, the file persists across reboots. A new app under `apps/<id>/` is *discovered* by `app_loader.discover()` but **excluded from `enabled_ids()`** because it's not in the installed set, so the boot loop skips it and no routes are mounted → `/<id>/` returns **404** even though every scaffolded file is correct. Same applies to plugins (`installed-plugins.json`).

**The fix** — run before asking the user to restart:

```bash
cd D:/emptyos && python -c "
from pathlib import Path
from emptyos.runtime import store_state
store_state.mark_installed(Path('data'), 'apps', '<id>', '<version-from-manifest>')
print('installed:', store_state.is_installed(Path('data'), 'apps', '<id>'))
"
```

This writes one entry into `data/store/installed-apps.json` and is safe to run while the daemon is up (it's just a JSON write; the daemon picks it up on the next boot). It does **not** require an HTTP call to `/store/api/install/...` — that endpoint does the same JSON write and tells you to restart anyway.

**For plugins** scaffolded via `/eos-new-plugin`, use `'plugins'` as the kind: `store_state.mark_installed(Path('data'), 'plugins', '<id>', '<version>')`.

**Skip this step if** `data/store/installed-apps.json` doesn't exist yet (fresh-clone first boot — the seed will install everything automatically) or `[demo] enabled = true` in `emptyos.toml` (demo mode bypasses the gate).

---

### Step 9: Verify

```bash
# Restart the daemon so the new app is loaded — ask the user to run restart.bat
# (never restart :9000 yourself — .claude/rules/daemon-handling.md), then:

# Confirm the app registered
curl -s http://127.0.0.1:9000/api/apps | python -c "import sys,json; ids=[a['id'] for a in json.load(sys.stdin)]; print('<id>' in ids)"

# Self-documenting info
python -m emptyos app info <id>

# Run its test file (daemon must be up)
python -m pytest tests/test_sys_<id>.py -v
```

All three must succeed. If `eos app info` fails, the manifest is malformed. If tests fail against an empty implementation, that's expected — stub the handlers to return valid shapes so the baseline tests pass.

**Record the birth baseline on the spec note** after the pytest run — block shape in `scaffold-templates.md` §Step 9. Set-semantics: replace the section if re-running, don't accumulate. Touch only that section; the rest of the spec stays frozen.

---

### Step 10: Report

Report shape: `scaffold-templates.md` §Step 10.

## Safety

- **Never** scaffold over an existing app — if `apps/<id>` exists, abort and ask.
- **Never** commit personal config into the app's manifest or code — per-machine settings go in `emptyos.toml` `[apps.<id>]`, read via `self.app_config()`.
- **Never** add a wellbeing-wheel picker, dimension tag prompt, or wheel visual to the UI (CLAUDE.md §Development Rules 16). `dimensions = [...]` in manifest is manifest-only metadata.
- **Never** reference third-party brands in user-facing text (prompts, UI labels, error messages) — plugin integrations are the only exception.
- Don't hand-write release-tier entries for `personal` apps — they stay under `apps/personal/` and are gitignored.

## Automated mode (app-builder)

There is a second path executing the *same conventions* via claude-cli —
`POST /app-builder/api/run {spec_path}` scaffolds in a worktree behind a merge
gate. It reads this SKILL.md **and** `scaffold-templates.md` verbatim, so edits to
either propagate to both paths. Full loop, spec-note shape, and a which-path-when
table: `<SKILL_DIR>/app-builder-mode.md`.

## Relationship

- **Once the UI is fleshed out (not before — needs real content to evaluate)** → `/eos-page-design-review apps/<id>/pages/index.html`. Catches theme-bootstrap regressions, phantom tokens, doubled signals, and archetype-mismatched chrome at the cheapest possible point — when the patterns aren't yet calcified.
- Pre-commit after building out the scaffold → `/eos-simplify`
- End of session → `/eos-session-wrapup` (updates CLAUDE.md counts, safety scan, devlog)
- System health / what to build next → `/eos-architecture-review`
- Autonomous scaffolding → `docs/app-builder.md` (operational contract for the loop)
