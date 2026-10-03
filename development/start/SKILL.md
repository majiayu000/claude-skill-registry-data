---
name: start
description: Start a project on the Visual Stack — a multi-step setup form captures what's being built, recommends a stack, and either instantiates the vstack-template-base template, sets up a specs-and-design-only workspace, or records an existing codebase without touching it. Use when the user wants to start a new project, scaffold a repo, set up a codebase from the Cavalry template, pick a stack or add-ons, run Day-1 setup, or bring an existing app onto the visual stack.
---

Turns an idea — or an existing repo — into *this* project. One multi-step form, then whichever of three
paths its answers call for.

```
                                   ┌─ skip dev ──► specs/ + design/ only (no clone)
  idea ──► setup form ──► choice ──┤
                                   └─ full ─────► clone ──► delete the rest ──► toolchain ──► ready
  existing code ──► infer ──► confirm screen ──► recorded (nothing touched)
```

Every path ends with two files the rest of the chain reads: **`specs/product.md`** — what this product
is — and **`.vstack/pipeline.json`** — where the pipeline stands.

## 1 · Pick the mode

Look at the target directory first:

| The directory is | Mode |
|---|---|
| empty, missing, or has no real code | **fresh** — the form runs before anything exists |
| template-derived (`stacks/`, `add-ons/`, `design/`, `specs/` all present) | **template** — don't clone again; the form reads the real inventory |
| a real codebase that isn't template-derived | **existing** — infer, confirm, record; never scaffold or delete |

In fresh mode, don't interrogate up front — the form asks the questions. The only thing worth asking
before serving it is where the project directory should go if the user hasn't said.

## 2 · Serve the form

```bash
SKILL=<this skill dir>
node "$SKILL/assets/chooser-server.mjs" --repo <project dir> --port 7799
```

Start it with **`run_in_background: true`**, then tell the user to open **http://localhost:7799/**.

The form is four steps: **what** are you building → **details** (kind, name, one-liner) → **stack &
add-ons**, with a pack recommended from the earlier answers — → **confirm**. On step 3 the user can
instead **skip development setup** entirely; the whole path then produces UI and specs only.

Where the inventory comes from:

- **Template mode** (repo has `stacks/` + `add-ons/`): scanned from disk — a pack added upstream
  appears with no change here.
- **Fresh mode** (nothing on disk yet): the server fetches the **live `stacks/` + `add-ons/` listing
  of `vstack-template-base` from GitHub** (`"source": "github"`); offline or rate-limited it falls
  back to its built-in catalog snapshot (`"source": "snapshot"`). Either way, after cloning,
  **reconcile**: if the chosen pack or an add-on doesn't exist in the cloned template, stop and
  re-ask; if the template ships packs the form didn't show, mention them before deleting anything.
- **Existing mode**: no inventory. Infer the facts first — read `package.json` / lockfiles / framework
  configs / the directory layout / `README` / recent git log — write them as a prefill, and serve:

  ```bash
  node "$SKILL/assets/chooser-server.mjs" --repo <dir> --mode existing --prefill <dir>/.vstack/prefill.json
  ```

  Prefill shape: `{ "building": "webapp", "kind": "saas", "name": "…", "oneLiner": "…",
  "detected": "Next.js 14 app router, Prisma + Postgres, deployed on Vercel", "startAt": "confirm" }`.
  The page opens on the confirm step with everything filled in and editable.

It asks **once**: on send it writes `<repo>/.vstack/choice.json` and exits. Nothing stays listening.
That makes this the one place in the stack that waits rather than watches — there is a single answer
coming, so the **`run_in_background: true`** start above is also the wait: the server's exit
re-invokes you, and that is the moment to read `<repo>/.vstack/choice.json`. (The review and bridge
tools stream instead, because their pages keep talking.)

If the user would rather answer in chat, that's fine — ask the same questions in prose and write the
same JSON yourself. **Ask in product terms when you do** — *"will several organisations share one
deployment, with their data kept separate?"*, never *"do you want multi-tenancy?"*. The form is the
nicer path, not the only one.

## 3 · Act on the choice

`choice.json` carries `mode`, `building`, `kind`, `name`, `oneLiner`, `skipDev`, `pack`, `addons`,
`deleting`, and (existing mode) `detected`. Three paths:

### 3a · Development skipped → the minimal workspace

No clone. In the project directory:

```bash
mkdir -p <dir>/specs <dir>/design
```

Write `specs/product.md` (§4) and `.vstack/pipeline.json` (§6) with `"specsOnly": true`. Done — say
that `/vstack:review` and the spec stages now have a home, and that running `/vstack:start` again
later adds real development setup.

### 3b · Existing app → record only

Write `specs/product.md` and `.vstack/pipeline.json`; create `specs/` and `design/` only if missing.
**Touch nothing else** — no scaffolding, no deletions, no template. The `detected` text goes into
`product.md` as the stack section.

### 3c · Full setup → clone and instantiate

**With a GitHub repo** — keeps the template link and the history clean:

```bash
gh repo create <name> --template Cavalry-Collective/vstack-template-base --private --clone
```

**Local only:**

```bash
git clone --depth 1 https://github.com/Cavalry-Collective/vstack-template-base.git <name>
rm -rf <name>/.git && git -C <name> init && git -C <name> add -A
```

Then read the contracts — root `CLAUDE.md`, `apps/backend/CLAUDE.md`, `apps/frontend/CLAUDE.md`,
`db/CLAUDE.md`, `infra/CLAUDE.md` — and, if the choice came from the snapshot, **reconcile it** (§2)
before deleting anything.

**Adoption is deletion.** Show the delete list, get a yes, then:

```bash
cd <repo>
for p in $(jq -r '.deleting.packs[]'  .vstack/choice.json); do rm -rf "stacks/$p"; done
for a in $(jq -r '.deleting.addons[]' .vstack/choice.json); do rm -rf "add-ons/$a"; done
```

Record the choice in root `CLAUDE.md` **Learnings**: `Stack: <pack>; appendices under stacks/<pack>/`.
Then the rest of the Day-1 checklist, unchanged:

- **Toolchain** from the surviving pack's `README.md`: its **dev** command block → the root `CLAUDE.md`
  *Common commands* placeholder (delete the banner); its **CI** block → `.github/workflows/ci.yml`
  (**different blocks** — a dev-only migration command in CI is a real bug); `deploy.yml` filled or
  deleted per the pack's conflict register; a real `.env.example`; the remaining `ci.yml` gates the
  pack doesn't cover — i18n key parity, migration up/down round-trip, a11y scan.
- **Primary form factor** in `apps/frontend/CLAUDE.md` — `mobile-first`, `desktop-first` or
  `responsive-equal`. Ask; it isn't inferable and it changes every screen.
- **Rebrand and confirm the design guide** — edit the *primitive* tier in `design/tokens.css` to the
  project's brand, open `design/design-guide.html`, and have the user confirm it reads as one system.
  **This gates everything visual** — no screen gets built against an unconfirmed system.
- **Copy runtime config** — `.env` and any secrets, which don't come from the template.

## 4 · Write `specs/product.md`

Every path writes it. It is the product's constitution — the durable answer to *what is this*, which
every later stage reads before doing anything. Build it from `choice.json` **plus whatever the
conversation has already established** — constraints, audience, non-goals the user has mentioned:

```markdown
# <name>

<one-liner>

## What it is
<building · kind, in plain words — and anything the conversation added>

## Stack
<pack + add-ons | the detected stack, verbatim from the confirm screen | "Specs & design only — no development setup yet">

## Constraints & principles
<only what's actually been said — never invent principles to fill the section>
```

Thin is fine. A three-line `product.md` that is all true beats a page of boilerplate.

## 5 · Hand back the repo-level steps *(full setup only)*

Protect `main` with a required-CI rule, stand up staging if the pack defines one, confirm the first CI
run is green. **Don't do these unasked** — print them as a checklist and offer to run any of them.
Branch protection must come *after* the first green push, or a required-status rule rejects a branch
whose CI has never run.

Then confirm no placeholder survived — both must return nothing:

```bash
grep -rn 'FILL IN ON SETUP\|TODO: replace' . --exclude-dir=stacks --exclude-dir=specs --exclude-dir=.git \
  | grep -v '^\./README\.md:'
grep -n '^<pm> ' CLAUDE.md
```

Delete the template's own root `README.md` once instantiation is done — its Day-1 checklist is spent.

## Notes

- **Never edit `assets/chooser.html` or `chooser-server.mjs`** to fit a project — they're the engine. The shell chrome is stamped in from `lib/shell/` — see `lib/shell/README.md`.
- The form is a **one-shot** by design: it asks once, so it doesn't use the live-link machinery behind
  `wireframe` and `user-story-map`. Don't wire it into them.
- Unknown directories still work. A pack or add-on with no built-in blurb renders from its own README,
  so an upstream addition never breaks the page.
- Flags: `--out` moves `choice.json`; `--port` moves the port (busy usually means a form is already
  up); `--project` names the project when `--repo` doesn't exist yet; `--mode existing` +
  `--prefill <file>` is the existing-app path.
- The page always sends straight to the server — there is no copy-paste fallback. If the server has
  gone away it shows a retry state and keeps the answers until the tab closes, so if a send fails,
  restart the server and have the user press *Try again*.
- The **snapshot catalog** inside `chooser-server.mjs` mirrors the template's packs and add-ons. If
  the template gains one, add it there too — fresh mode can't scan what isn't cloned yet.

## State & handoff

- **Read** nothing — this is where the pipeline begins.
- **Write** `specs/product.md` and `<repo>/.vstack/pipeline.json`, the file every later stage reads:
  ```json
  { "version": 1, "project": "<name>", "stage": "start", "phase": null,
    "specsOnly": false,
    "artifacts": { "product": "specs/product.md", "stack": "<pack>", "addOns": ["…"] },
    "history": [{ "stage": "start", "at": "<iso>", "note": "<pack> + N add-ons" }] }
  ```
  `"specsOnly": true` and no `stack`/`addOns` keys on the skip-dev path; in existing mode `stack` is
  the detected description rather than a pack id. Commit it — it's a project record, not scratch.
  Keep `.vstack/choice.json` beside it as the raw answer.
- **Next** — `/vstack:requirements` writes `specs/requirements.md`. **That stage isn't built yet**;
  until it is, say so and offer to write `specs/requirements.md` by hand together, or go straight to
  a first screen with `/vstack:review`. Don't invent a requirements stage to fill the gap. From
  there the built chain runs `wireframe → spec → user-story-map → phase-preview → phase-build`.
  The former `/vstack:go` router is no longer part of the pipeline; it is a compatibility alias for
  the wireframe tool.
