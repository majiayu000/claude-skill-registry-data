---
name: diagram-update
description: Regenerate diagram/index.html — a single-file, interactive HTML diagram of the end-to-end workflow provided by this plugin's skills, hooks, and scripts. Use when the user wants to create, update, refresh, or regenerate the plugin workflow diagram, typically after skills have been added or changed. Runs only inside the dev-skills plugin repo itself (manifest name "dev") and refuses anywhere else. Renders the page from templates/workflow-diagram.html by substituting per-run data (groups, skills, steps, edges, overview layout) into the template's tokens — the template owns all presentation; the skill authors data only. Re-derives that data from the files on disk every run and overwrites any existing diagram/index.html wholesale — never merges or patches. Read-only towards everything except diagram/index.html; never commits or pushes. Step 0 confirms with the user before doing any work when invoked proactively; the confirmation is skipped when the user explicitly typed /diagram-update.
user-invocable: true
disable-model-invocation: false
argument-hint: (no arguments)
allowed-tools: Read, Write, Grep, Glob, Bash(git *), Bash(ls *), Bash(find *), Bash(mkdir *), Bash(test *), Bash(date *), Bash(jq *), Bash(pwd)
---

# diagram-update — Regenerate the plugin workflow diagram

You are running the `diagram-update` skill. Your job is to analyse **everything the plugin ships** — every skill under `skills/`, the hook config and scripts under `hooks/`, and any other executable or template — and render one high-quality, self-contained, interactive HTML page that explains the end-to-end workflow, saved as `diagram/index.html` at the repo root. The page is rendered by substituting per-run **data** into the plugin template `templates/workflow-diagram.html`, which owns all presentation and interaction; this skill never authors the page from scratch.

The diagram is a **generated artefact**: it carries no state of its own, so this skill rebuilds it wholesale every run. "Create" and "update" are the same operation — if `diagram/index.html` already exists it is **overwritten entirely**, never merged. Never hardcode the current skill set into reasoning shortcuts: the whole point of this skill is that the diagram is re-derived from whatever is on disk *now*.

This skill has nine steps (Steps 0–8). Execute them in order.

## Step 0 — Confirm before proceeding (when invoked proactively)

Check the most recent user message for the literal tag `<command-name>/diagram-update</command-name>` (or, equivalently, a leading `/diagram-update` typed by the user). If present, skip this step and continue with Step 1.

Otherwise (proactive invocation from natural-language intent), ask once via `AskUserQuestion`:

- **Question**: "Regenerate the plugin workflow diagram? This overwrites `diagram/index.html` from the current skills/hooks on disk."
- **Options**: "Yes, regenerate" / "No, skip".

On anything other than an explicit yes, stop without touching the filesystem.

## Step 1 — Gate: dev-skills repo only

- `git rev-parse --show-toplevel` → `repo_root`. If it fails, stop: this skill only runs inside the dev-skills plugin repo.
- `jq -r .name "<repo_root>/.claude-plugin/plugin.json"` must output exactly `dev`. If the file is missing or the name differs, stop with one line: `diagram-update: refused — this skill only runs inside the dev-skills plugin repo (manifest name "dev").`
- Record `plugin_version` (`jq -r .version`) and `generated_at` (`date -u +"%Y-%m-%d %H:%M UTC"`) for the page header.
- `template_file` = `<repo_root>/templates/workflow-diagram.html`. Verify it exists (`test -f`); if it is missing, stop with one line: `diagram-update: refused — templates/workflow-diagram.html is missing; restore it from git history before regenerating.` Do not fall back to authoring the page by hand.

## Step 2 — Inventory the plugin

Enumerate, from `repo_root`:

- `skills/*/SKILL.md` — every skill, including internal ones and this skill itself.
- `hooks/hooks.json` and every script it references (e.g. shell scripts under `hooks/`).
- `templates/` and any other scripts or executables the plugin ships.

Read **every one of these files in full**. Do not work from `CLAUDE.md` summaries or memory of the plugin — the files are the source of truth, and the diagram must reflect skills added or changed since any summary was written.

## Step 3 — Extract the model

For each skill, extract:

- **Identity**: slug, one-line purpose (from the frontmatter description), and the invocation surface derived from frontmatter — `user-invocable: false` → *Agent only*; `disable-model-invocation: true` → *User only*; otherwise → *User + Agent*.
- **Steps**: the skill's own ordered procedure steps (its `## Step N` headings, or numbered process sections for skills without formal step headings). When a step contains a lettered sub-step cycle that is the skill's core engine (e.g. an inner per-stage loop like `5a`–`5i`), extract each lettered sub-step as its own step too — a single opaque box hiding the cycle defeats the diagram. For each: a title of **at most three words** (e.g. "Confirm invocation", "Resolve paths", "Baseline tests") and a 2–4 sentence plain-language explanation of what the step does — written for a reader who has never opened the SKILL.md.
- **Approval gates**: every point where a human must answer before flow continues — Step 0 confirmation gates, `AskUserQuestion` decision points, plain-chat yes/no confirmations, verification handbacks.
- **Loop-backs**: every point where flow returns to an earlier step or another skill when something goes wrong — e.g. failed verification returning to diagnosis, a red test baseline halting into a bug-filing handover, a blocked plan returning to design.
- **Parallelism**: steps that fan out into concurrently running subagents, and which units run in parallel.
- **Delegation**: steps that run inside subagents rather than the main agent.
- **Cross-skill edges**: every reference from a step to another skill — internal-helper calls, chain-in/chain-out offers between stages, handovers, and hook-to-skill effects. Record the specific *step* each edge leaves from and (where determinable) arrives at.

For each hook: its trigger events, what the script actually does (read the script, not just the config), its throttling/no-op conditions, and any effect it has on skill flow.

## Step 4 — Derive the graph

- **Groups**: cluster the skills into workflow groups by their cross-references (e.g. a staged pipeline chained by chain-out offers; a bug workflow; eval scorers; reflection helpers; standalone utilities; hooks). Derive the groups from the edges — do not assume a fixed list.
- **Pipeline order**: where skills chain into one another, lay them out left-to-right in chain order as the dominant visual flow.
- **Shared services**: skills invoked by several others (resolvers, renderers, capture helpers) render as service boxes that multiple edges converge on.
- **Edge types**: distinguish *calls* (one skill invokes another), *chains into* (end-of-skill offer into the next stage), *hands over* (failure/handover path), and *loops back* (retry/return path). Every edge gets a source step, a target (step or skill), a type, and a short label.

## Step 5 — Author the data blocks

All presentation and interaction — cards, pop-ups, hover-revealed connectors, brackets, badges, the overview engine, legend, theming — lives in the template located in Step 1. This step authors **data only**: the eight values Step 6 substitutes into the template's anchored tokens.

| Token | Value |
|---|---|
| `PLUGIN_VERSION` | the version recorded in Step 1 (e.g. `0.3.22`). |
| `GENERATED_AT` | the UTC stamp recorded in Step 1. |
| `DIAGRAM_GROUPS` | JS array literal — one `{ id, name, accent, desc }` per Step 4 workflow group, each with a distinct accent colour. |
| `DIAGRAM_SKILLS` | JS array literal — one object per skill **and hook**: `{ slug, g: <group id>, inv: "user"\|"agent"\|"both"\|"hook", internal?, commits?, purpose, wraps?, steps }`. Each step is `{ k, t, d, gate?, sub?, commits?, par?, wrap? }` from the Step 3 extraction; `wraps` maps every `wrap` id used by the steps to its bracket label. |
| `DIAGRAM_EDGES` | JS array literal — `{ f, t, ty, l }`: `f`/`t` are `"slug.step"` (preferred — chips and hover anchoring depend on step precision) or a bare `"slug"` (anchors to the card header); `ty` ∈ `call\|chain\|hand\|loop\|data`; `l` is a short label. |
| `OVERVIEW_NODES` | JS array literal — `{ slug, x, y }` for the skills-only overview: **every skill and hook exactly once**; `x` in percent, `y` in px. Lay the chained pipeline left-to-right on one row, shared internal helpers as a hub row beneath it, remaining groups in rows below, utilities on the right. |
| `OVERVIEW_EDGES` | JS array literal — `{ f, t, ty, l, bend? }` with bare slugs; `bend` (px, negative = above) arcs a same-row edge clear of the nodes between. Leave the converging call fans unlabelled; label the load-bearing chain / handover / loop / data edges. |
| `WORKFLOW_C4_LINK` | `<a class="vchip" href="c4.html">architecture diagram &#8594;</a>` when `<repo_root>/diagram/c4.html` exists (`test -f`), otherwise the empty string. Resolved from the filesystem alone — this skill never inspects `/diagram-c4-update`, so the two stay independently re-derivable. |

Authoring conventions — each of these came out of a real review round; keep honouring them:

- Step titles are ≤3 words, and the closing chain-offer step of each pipeline skill is titled consistently: "Offer design", "Offer plan", "Offer implement", "Offer evals".
- A lettered sub-step cycle (Step 3) becomes steps sharing a `wrap` id, with its iteration and retry paths as same-skill `loop` edges (e.g. "next stage", "gap → more tests").
- A step that merely *launches* a subagent from the main agent carries no `sub` flag and stays outside the wrap bracket.
- Every cross-skill delegation must appear in `DIAGRAM_EDGES` anchored to the exact step — the engine derives the visible invocation chips from those edges. Never encode delegation only in a step's title or description.
- `par` lists name the actual concurrent units (eval dimensions, launched skills); the engine suppresses duplicate chips for targets the bracket already names.
- Counts (footer totals, pop-up connection lists, hover isolation) are computed by the engine — never author them into the data.

## Step 6 — Render from the template

- `Read` `template_file` in full and verify all eight anchored tokens are present — the five data anchors (`const GROUPS = {{DIAGRAM_GROUPS}};` and siblings) plus the three header tokens. If any is missing, stop and report that the template has drifted from this skill's contract; fix template and SKILL.md together (see *Modification points*), never improvise around it.
- Substitute each token with its Step 5 value.
- `mkdir -p "<repo_root>/diagram"`, then `Write` the substituted result wholesale to `<repo_root>/diagram/index.html`. Do not keep backups of the old file; git history is the record.
- A normal run's only write is `diagram/index.html`: never modify the template, and never hand-tune the engine markup/CSS/JS in the output.

## Step 7 — Verify the output

Static sanity checks on the file just written (fix and re-verify on any failure):

- None of the eight template tokens remains literal in the output. Grep for the exact anchored names (`{{DIAGRAM_SKILLS}}` etc.), **not** for bare `{{` — at least one step description legitimately contains a `{{…}}` figure of speech. Note that `{{WORKFLOW_C4_LINK}}` is correctly substituted with the *empty string* when there is no `diagram/c4.html`: check that the token is gone, never that it left something behind.
- Every skill folder under `skills/` appears exactly once as a card (Grep the file for each slug).
- The number of step boxes per skill matches the steps extracted in Step 3.
- Every step box has corresponding pop-up content, and every edge references element ids that exist in the file.
- No `http://` or `https://` references anywhere in the file.
- The legend covers every edge style, badge, and pill actually used.

## Step 8 — Report

Output a short summary and stop:

```
diagram-update: diagram/index.html regenerated — <S> skills, <T> steps, <E> edges, <G> approval gates, <L> loop-backs, <P> parallel clusters
Open diagram/index.html in a browser to view.
```

## Modification points — template vs data

The diagram has two owners; route every change to the correct one:

- **Data changes** — a new or edited skill, changed steps, new gates/edges, overview layout: nothing to edit anywhere. The next run re-derives everything (Steps 2–5). Never hand-edit `diagram/index.html`; it is overwritten wholesale.
- **Presentation / interaction changes** — badge kinds, bracket styles, pop-up behaviour, hover mechanics, colours, the overview engine: edit `templates/workflow-diagram.html` (outside a run), then re-run `/diagram-update` to regenerate. The template embodies the accumulated design decisions and must not regress them: skills-only overview panel with always-visible edges; detail-board connectors hidden until a step is hovered; cross-skill invocation chips derived from the edge list; dashed brackets for single-subagent runs and strategy-dependent step loops; parallel-unit brackets; amber gate badges; pop-up invocation pills; engine-computed counts; light/dark theme; fully self-contained output.
- **Contract changes** — adding a data field or token touches both sides: update the template's engine, its doc comment, and this skill's Step 5 table in the same change. A token renamed on only one side fails Step 6's verification — that is the tripwire working, not an error to route around.

## Constraints (non-negotiable)

- **Read-only except `diagram/index.html`.** Never modify skills, hooks, templates, or anything else; never write under `features/` or `bugs/`.
- **The template is the single source of presentation.** `diagram/index.html` is a generated artefact — hand edits to it are lost on the next run; engine changes go to `templates/workflow-diagram.html` outside a run, per *Modification points*.
- **Never commit or push.** Leave the regenerated diagram as a working-tree change for the user.
- **Always regenerate wholesale.** Never patch the existing diagram in place — rebuild from the files so the diagram can never drift from reality.
- **Everything is re-derived.** No skill list, group, edge, or count is ever hardcoded from memory; a skill added yesterday must appear without this SKILL.md changing.
- **Fully self-contained output.** No external assets, no symlinks, no files other than the single `index.html`.
- This skill does **not** call `lessons-capture` — like `bug-submit`, it is a simple rendering skill and the reflection overhead isn't worth it.
