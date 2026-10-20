---
name: document
owner: baseline
description: Workflow Phase 10 — orchestrator for documentation work. Surveys the diff, routes any page on a documentation surface through `technical-writer`, standalone technical reference through the `documentation` skill, tutorials through `technical-tutorials`, and all other prose body work (inline docs, README updates, user-facing copy) through the `prose` skill (which mandates `humanizer` and conditionally `copywriting`). Verifies completeness and marks phase done.
---

# document — Phase 10 orchestrator

This skill does **not** write docs directly. It surveys the diff, decides what kinds of doc work are needed, and delegates via the Skill tool.

| Delegate skill | Kind | Runs on |
|---|---|---|
| `technical-writer` | A page on a documentation surface | docs-site pages, `docs/**` guides — anything a reader navigates to as documentation |
| `prose` | Prose body — any English writing that needs humanizing | inline docs, README surface, user-facing copy, summary/narrative sections |
| `documentation` | Technical reference | API docs, architecture notes, operational runbooks |
| `technical-tutorials` | Step-by-step narrative | quickstarts, walkthroughs, code tutorials |

The key shift: **`prose` is the sole channel for prose-shaping work**. It owns the `humanizer` pass so every word we ship is filtered. The other two are technical specialists that produce structured reference material; when they output prose paragraphs that matter, they invoke `prose` themselves.

## Prereq

`integrate` in `completed` (or `exceptions`).

## When each delegate fires

- **`technical-writer`** — the diff adds or changes a page on a documentation surface (a docs site, a `docs/**` guide). It runs the full SOP: source-gathering, `technical-writing`, `reader-level`, `humanizer`, then gates on `measure.mjs` and `score.mjs`. Prefer it over `documentation` whenever the deliverable is a *page* rather than a section of reference material.
- **`documentation`** — diff touches a public API, config surface, module architecture, or adds runbook-worthy operational behavior. Reference material a future engineer will look up.
- **`technical-tutorials`** — diff adds a feature a *first-time user* must learn by doing. Hands-on-learning, not lookup-reference.
- **`prose`** — when prose needs to be written or revised:
  - Narrative sections inside docs the above two skills produce.
  - README surface updates.
  - User-facing marketing/product copy on landing, pricing, feature pages.
  - One-paragraph summaries, migration narratives, release notes.

Multiple can fire on one diff. A feature that ships an API, needs a quickstart, and updates the pricing page triggers all three.

## Steps

1. **Verify prereq.** `integrate` is in `completed` or `exceptions`. Otherwise stop and say which phase is missing.

2. **Classify each surface from config, not from judgment.** Run the gate in preview to get the required surface → delegate map:

   ```
   node .claude/skills/document/document-gate.mjs --slug <slug>
   ```

   Its punch list IS this phase's to-do list. The map comes from `project.json → document.surfaces` (glob → `requires[]` + `reader_target`), so routing is a config lookup rather than a per-run decision. This exists because the prose rule below was correct and got skipped anyway: a sentence in a SKILL.md cannot fail a build.

   **After running each delegate, record a receipt** so the gate can verify it:

   ```
   node .claude/skills/document/cli.mjs receipt --slug <slug> --surface <path> --delegate <technical-writer|copywriting|prose|documentation|technical-tutorials>   # wraps receipts.mjs -> recordReceipt
   ```

   Never hand-write a receipt for work that was not done. The receipt asserts the delegate ran; forging one converts the gate into decoration.

2a. **Survey the diff for anything the config does not cover.** `git diff --name-status <merge-base>..HEAD`, then `git status --porcelain -uall` for the uncommitted and untracked work. The first command sees only what is already committed, so a file this change created is invisible to it. Classify touched files:
   - A page on a documentation surface → `technical-writer` candidate (takes precedence over the two below for that page).
   - Public API / CLI / contract surfaces → `documentation` candidate.
   - New capability a user learns by doing → `technical-tutorials` candidate.
   - Marketing / pricing / feature / landing pages (`site-src/**`) → BOTH registers (see 2.5).
   - README surface or prose anywhere in the diff → `prose` candidate.
   - Internal-only refactor with no external surface → just inline docstrings + the README sanity check.

   **2.5 Reflective public-site check (do NOT rely on file-presence alone).** The public site (`site-src/**/*.njk`) *describes* the harness's behavior; a behavior change can require a description update even when **no `site-src/**` file is in the diff**. Anchoring on "no site file changed → no site work" gets the direction backwards (backlog 5e07). So always run the reflective check:

   ```
   node .claude/skills/document/cli.mjs surfaces --touched <comma,separated,diff,paths> --json   # wraps public-site-reflect.mjs -> findDescribedSurfaces
   ```

   `findDescribedSurfaces` derives the skill/hook/command tokens the diff touches and returns the public pages that name them. For **each** returned page, route it through TWO registers (per the canonical user feedback, backlog 7b3e — *"on public website we need to describe features not just the behavior"*):
   - `documentation` (reference register) — update WHAT/HOW the page states, so the mechanism description stays accurate.
   - `prose` in the **persuasive / feature-value register** (name `copywriting` as the conditional skill) — frame the user-facing FEATURE VALUE, not just the mechanism. A `_thread.md` row that says "shelves the active thread and surfaces a resume summary" describes behavior; the feature value is "never lose your train of thought across a pivot, `/clear`, or flush."

   A `site-src/**` file that IS in the diff gets the same two-register treatment. If the reflective check returns nothing and no `site-src/**` file is in the diff, there is genuinely no public surface — say so.

3. **Always: inline docs.** For every changed public symbol — module-level docstring / header comment / doc comment appropriate to the language. Short. If you need a comment to explain *what*, the abstraction is wrong; comments are for non-obvious *why*.

4. **Delegate.** For each matched category, invoke the delegate skill with a scoped brief:
   - `technical-writer`: invoke via `Skill(technical-writer)` with the page path, its Diátaxis type, and the source material. It owns its own gates; do not declare the page done until both scorers exit 0.
   - `documentation` / `technical-tutorials`: invoke via `Skill(...)`. Include the diff slice, upstream spec/intake, and the specific deliverable (e.g., "API reference for the new retry endpoint"). Read its output and incorporate it.
   - `prose`: invoke via `Skill(prose)` with brief, source material (diff slice, spec excerpt), audience, register, and output target (file path or section). The `prose` skill applies `humanizer` always, plus the conditional skill you name.

5. **README surface check.** If the root `README.md` or any top-level doc claims behavior the diff changed, update it — route through `prose` so the copy gets humanized.

6. **Scrub.** No `TODO` / `FIXME` / `HACK` / `XXX` in files this phase touched. Seed.md forbids them; humanizer doesn't catch them.

6a. **Run the gate. It decides whether this phase is done.**

   ```
   node .claude/skills/document/document-gate.mjs --slug <slug>
   ```

   Exit 0 → every required delegate left a receipt; proceed to step 7. Exit 1 → the phase is **not** complete: run the named delegate for the named surface, or correct `project.json → document.surfaces` if the obligation is genuinely wrong. Correcting the config is a legitimate outcome — a false obligation trains people to override the gate, which destroys it — but it is a config edit with a reason, never a hand-written receipt.

   Do not append `"document"` to `completed` while the gate exits 1.

7. **Append `"document"` to `.claude/state/workflow.json → completed`.**

8. Tell the user: "Documentation pass complete. Invoked: `<list of delegates>`. Next: `/archive`."

## Constraints

- **Delegation is mandatory.** You do not write prose here; `prose` does. You do not write documentation pages here; `technical-writer` does. You do not write API reference here; `documentation` does. You do not write tutorials here; `technical-tutorials` does. This skill decides *who* writes *what* and stitches the result.
- **Do not skip the humanizer pass.** Everything in `prose` runs it. If you find yourself tempted to write a README paragraph inline to save a hop, don't — route it through `prose`.
- **Do not invoke delegates that don't apply.** Internal refactor with no external surface? Don't fire `prose` (persuasive register) just because the skill is available. Step 2's survey gates the invocations.
- **Keep this skill lightweight.** The body is mostly "decide → delegate → verify → mark done". Heavy lifting lives in the delegates.
- **YAGNI on docs.** A doc exists because the code change made it necessary. No speculative documentation.
