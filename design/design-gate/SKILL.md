---
name: design-gate
description: >-
  Produce the rendered evidence a human-gated frontend PR owes its reviewer: capture each
  changed surface (plus the before state for anything modified, plus mobile width), then
  generate one self-contained local HTML page the founder can open and review without
  checking anything out. Use when a PR is gated by the "Frontend changes are HUMAN-GATED"
  section of CLAUDE.md, or when the user says "/design-gate", "screenshot evidence for this
  PR", "prep this for founder review", "build the design evidence page", "what does this
  look like before and after". The page comes from a template script, not hand-written
  markup. Output is session-local and never committed. Do NOT use for non-gated changes:
  typo/grammar/factual fixes in an unchanged block, dead link targets, alt/ARIA fixes with
  no visual change, cache-bust bumps, or refactors with no rendered diff.
version: 1.0.0
argument-hint: "<PR number, branch, or list of changed surfaces>"
---

# design-gate

Implements the reviewer's half of the **human gate**. `CLAUDE.md` § *Frontend changes are
HUMAN-GATED — founder review before merge* says a gated PR does not merge on green CI, and:

> **What a gated PR owes the reviewer:** rendered evidence, not a description — a screenshot
> of each changed surface (and both light and dark if theming is touched), plus the before
> state for anything modified rather than added. Reviewing a diff of HTML is not reviewing a
> design.

This skill produces exactly that artifact, cheaply. **Read the CLAUDE.md section before
running** — it is the contract; this skill is only the delivery mechanism. If that section
changes, revise this skill.

## Token discipline — the reason this exists

The first hand-made evidence page cost ~190k tokens and 124 tool calls, most of it the model
typing `<div>`s. It must never do that again.

- The model writes a **manifest** (a small JSON object, a few hundred tokens).
- `scripts/build_evidence.py` emits the HTML. **Every run, no exceptions.**
- The model decides *what to capture and what to say about it*. It does not decide markup,
  CSS, or layout — those live in the script.

**If you find yourself writing HTML tags during a `/design-gate` run, stop.** Either the
manifest supports what you need, or the script needs a small change committed back to this
skill — not one-off markup in the output.

## When NOT to use

Per `CLAUDE.md`, these are **not gated** and need no evidence page — ship on green:

- Typo, grammar, and factual corrections inside an existing block, layout unchanged
- Dead or wrong link targets
- `alt` text, ARIA attributes, and other accessibility fixes that add no visual change
- Cache-bust version bumps
- Comments, and refactors with **no rendered diff**

Gated (use this skill): new/removed/relocated user-facing page or section; layout, structure,
or component composition; design tokens, color, typography, spacing, motion; nav, footer,
`window.GAIA_MOUNTS`, or entrypoint wiring; public-page copy that changes the *message*;
anything rendering the graph, badges, cards, or OG images. **When genuinely unsure, gate it.**

## Procedure

### 1. Scope the surfaces

From the PR diff (`gh pr diff <n> --name-only`, or `git diff --name-only origin/main...HEAD`),
list every surface a visitor could see differently. For each, record whether it is **modified**
(needs a before) or **added** (no before exists — label it, do not fake one).

For the static site, a changed shared asset (`docs/js/site-nav.js`, `docs/css/*`,
`docs/js/mounts.js`) means **several** surfaces changed, not one. Pick the representative
pages, and say in the manifest note which ones you picked.

### 2. Detect theming — do not assume it

```bash
grep -rl "prefers-color-scheme\|data-theme" docs/ | head
```

Capture a second theme **only if the changed pages actually have one.** Across `docs/` today
this is almost entirely absent, so most runs have exactly one visual state. When there is only
one, the page must **say so** in `gaps` — a stated gap is reviewable, a silent omission is not.
Never quietly drop a dark shot the reviewer might expect.

### 3. Capture

Use the session's browser preview tooling. Static site:

```
preview_start  { url: "http://localhost:8080/" }     # after: python -m http.server 8080 --directory docs
```

Next.js or any app with a dev server: add the entry to `.claude/launch.json` and
`preview_start { name: "<entry>" }`. Then per surface:

- `resize_window { preset: "desktop" }` → `computer { action: "screenshot" }`
- `resize_window { preset: "mobile" }` → `computer { action: "screenshot" }`

Rules:

- **Mobile width is mandatory for anything with layout.** Nav and footer break there first.
- **Before states**: `git stash` / check out `origin/main` into a second worktree and serve
  that, or capture the deployed production page. A diff cannot show whether a new nav item
  crowds what was already there.
- Save PNGs into `<scratchpad>/design-gate/<pr>/img/`.
- Scroll to the changed region before shooting; a full-page shot of an unchanged hero proves
  nothing.

### 4. Write the manifest

Copy `manifest.example.json` and fill it in. Fields: `pr`, `url`, `branch`, `title`,
`summary` (one line), `gaps` (list of strings), and `surfaces[]` with `name`, `route`, `note`,
and `shots[]` of `{viewport, before, after}` — omit `before` (or set `"added": true`) for
newly added surfaces and the script renders a single frame labelled *added - no before*.

Image paths are **relative to the manifest**.

### 5. Generate

```bash
python3 .claude/skills/design-gate/scripts/build_evidence.py <scratchpad>/design-gate/<pr>/manifest.json
# add --inline to embed the PNGs as data URIs
```

Stdlib only, no dependencies. Prints the output path plus surface/shot counts.

**Relative paths (default) vs `--inline`:** relative keeps the HTML a few KB and the PNGs
inspectable, but the page only works alongside its `img/` folder — moving the HTML alone
breaks it. `--inline` produces one genuinely portable file that survives being copied or
attached anywhere, at roughly 1.35× the total PNG bytes (base64 overhead), which gets slow to
open past a couple dozen shots. **Default to relative; use `--inline` when the founder is
going to move or forward the file.**

### 6. Present

Surface the page with `SendUserFile` using `display: "render"`. If that tool is unavailable in
the session, report the absolute path and offer `open <path>` — do not paste the HTML into
chat.

## Output is session-local — never committed

Everything lands in the **session scratchpad**, never in the repo.

- PNG evidence is **not repo-pushable** — a previous attempt to push an `evidence/*` branch was
  blocked by a permission gate. Do not try, and do not ask the user to work around it.
- The artifact is for the founder's eyes in-session, then discarded. The PR body links to
  nothing; the review happens on the rendered page.
- Do not add screenshots to `docs/`. They would become site-served Class S bytes.

## Guardrails

- **Never merge the gated PR.** This skill produces evidence and stops. Marking a PR ready is
  allowed; merging is the founder's, always. Squash is disabled on this repo — merge commits only.
- **Do not edit the frontend during a `/design-gate` run.** Capture what is on the branch. If a
  surface looks wrong, report it and let the founder decide.
- **Do not fabricate a before state.** If the previous state is genuinely unavailable, say so in
  `gaps`.
- **Stop at human gates.** Anything needing a founder decision rather than an implementation
  choice: stop and report.

## Files

| Path | Role |
|---|---|
| `SKILL.md` | This contract |
| `scripts/build_evidence.py` | Manifest → self-contained HTML. Stdlib only. |
| `manifest.example.json` | Copy-and-fill starting point |

Mirrored byte-identical in `.claude/skills/design-gate/` and `.agents/skills/design-gate/`;
edit both (verify with `diff -r`).
