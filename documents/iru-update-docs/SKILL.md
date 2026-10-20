---
name: iru-update-docs
description: Update a repository's Antora AsciiDoc documentation to reflect changes already made to the codebase (new/changed APIs, types, behavior, or conventions). Invoke as `/iru-update-docs` to cover uncommitted changes plus commits on the current branch not yet on the base branch, or `/iru-update-docs <git-ref-or-range>` to scope it to a specific ref/range (e.g. a commit, `main..HEAD`, a tag). Diagrams use Mermaid (`[mermaid]` blocks) and equations use MathJax (raw `\( \)` / `\[ \]` LaTeX) where they clarify behavior and the docs pipeline already supports them. If a documentation MCP (e.g. Confluence, Notion) is connected, also finds the relevant existing page(s) there and proposes matching updates — showing the exact change for the user to approve before anything is sent; if that connector only exposes read-access tools with no way to create or update a page, warns the user and skips this part instead. For repositories with a user interface it also maintains a **User interface** section — a navigation-flows page plus one page per screen/page/activity and per component/fragment/view/control, illustrated with the screenshots the UI tests captured under `.ui-screenshots/` (states × left-to-right/right-to-left × light/dark), copying only the screenshots the pages use into `images/ui/`, replacing the images of changed components and discarding the rest (`reference/ui-docs.md`). Use whenever source changes should be reflected in the docs site instead of leaving pages stale.
model: sonnet
---

# Update Docs

Bring an Antora-based documentation module's `.adoc` pages (and its `nav.adoc`/`antora.yml` if structure or
version changed) up to date with changes already made to the codebase. This skill only edits documentation — it
does not change source code, and it does not invent new documented behavior that isn't actually in the code. It
makes no assumptions about this being any particular repository, project, or language — discover everything
about the docs module and the codebase fresh each run.

## Step 1 — Determine the diff to document

- **Argument provided** (a commit, ref, or range like `main..HEAD`): use `git diff <arg>` as the scope.
- **No argument**: default to everything not yet merged plus anything still dirty:
  ```bash
  git status
  git diff <base-branch>...HEAD
  git diff
  ```
  (determine the repo's actual base branch first — e.g. `git symbolic-ref refs/remotes/origin/HEAD` or
  `git branch -a`; ask the user if it's genuinely ambiguous).
- If the resulting diff is empty (no local changes, branch even with base), tell the user there is nothing to
  document and stop rather than guessing at unrelated updates.
- Read the full diff, not just file names — the doc updates must be grounded in what actually changed, not in
  file names alone.

## Step 2 — Locate the documentation module

Don't assume a fixed docs path. Find the Antora module(s) actually present, typically by locating `antora.yml`
file(s) in the repository (`find . -name antora.yml -not -path '*/node_modules/*'`).

- **No `antora.yml` found anywhere**: there is no documentation module yet to update. Ask the user whether Antora
  documentation should be set up now (via the `iru-setup-antora` skill) before continuing — don't assume either way.
  - **User agrees**: delegate scaffolding to the `iru-setup-antora` skill, run as a sub-agent via the Agent tool.
    Brief that sub-agent with the actual context (what changed, per Step 1/3) so its starter pages aren't generic
    boilerplate disconnected from this update. After it finishes, re-run the `find . -name antora.yml ...` search
    to pick up the newly created module and proceed with the rest of this step as normal. If the sub-agent
    reports it stopped short (e.g. Node.js isn't installed, per its own Step 1) and therefore no module was
    created, relay that blocker to the user and stop rather than continuing without docs.
  - **User declines**: stop the `iru-update-docs` skill entirely — with no documentation module, there is nothing
    for it to update, so don't fall back to any other action.
- **One or more found**: for each one found:

- Read it to get the component name, version, and the nav file(s) it declares under `nav:`.
- Read each declared `nav.adoc` to get the real page list, then skim each listed page (title + first section is
  usually enough) to build a live map of what topic each page actually covers. Don't rely on page names alone —
  a page called `overview.adoc` in one repo might be called `index.adoc` or `intro.adoc` in another.
- Note the antora playbook file (commonly `antora-playbook.yml` or `site.yml`, usually near the docs module root
  or repository root) and read it once to check which Asciidoctor/Antora extensions are already wired up (e.g. a
  Mermaid extension, a MathJax/stem extension, `lunr` search) — this determines what's actually safe to use in
  Step 4, since a diagram/equation macro with no matching extension configured just renders as literal text.

## Step 3 — Understand what changed, in code terms

For every changed source file, determine in concrete terms, adapting to whatever language/stack this repository
actually uses:

- New or removed public classes/interfaces/functions/exports/endpoints, and any renamed ones.
- Behavioral changes to existing abstractions, especially ones already described in the docs (check the page
  map from Step 2).
- New variants/subtypes of an existing abstraction — these are the changes most likely to need a new branch in
  an existing decision tree/diagram or a new row in an existing comparison table.
- Changes to build/tooling that affect documented commands (e.g. a version bump, a new build profile, a new
  generated report, a changed CLI flag).

Cross-check against the repository's own contributor guide, if one exists (`CLAUDE.md`, `AGENTS.md`, or a
top-level `README`) so the docs stay consistent with it; if the diff changes something that guide also
describes, flag that to the user as a possible follow-up — this skill only edits the docs module, not that
guide.

## Step 4 — Map changes to affected pages, then edit them

Using the live page map built in Step 2 (not any assumption about fixed page names), decide which pages the
diff actually affects — don't touch pages the diff doesn't concern. A new abstraction variant typically touches
whichever page holds its decision tree/comparison table plus any page listing the top-level API surface. A
behavior-only fix with no API/semantics change usually needs no doc update at all — say so if that's the case
instead of forcing an edit. Only touch `nav.adoc`/`antora.yml` if a page was added/removed/renamed or the
component version should track a source version bump.

When editing:

- Match the conventions already used in that module's existing pages — read a couple of them first to learn the
  local section-title style, table syntax (`[cols=...]`), code-block language tags, and cross-link style
  (`xref:page.adoc[]`) rather than assuming AsciiDoc defaults or another project's conventions.
- Verify every class/method/field/endpoint named in prose or code blocks actually exists with that exact
  signature — read the real source rather than trusting the diff summary alone. Code snippets must be valid
  against the current API.
- **Mermaid diagrams** (`[mermaid]` fenced blocks): only use these if Step 2 confirmed a Mermaid extension is
  already wired into the playbook. Add one when a decision process, data flow, or before/after transformation is
  genuinely clearer as a diagram than prose — don't add one for something a short sentence already covers
  clearly, and don't introduce the syntax at all if the extension isn't configured (it would render as literal
  text) unless you also wire up the extension or explicitly flag the gap to the user.
- **MathJax equations** (raw LaTeX delimited by `\( ... \)` inline or `\[ ... \]` block, rendered client-side):
  only use these if Step 2 confirmed a MathJax/stem extension is wired in. Add one only if the change actually
  introduces math worth stating precisely (e.g. a complexity bound or a formal definition); most changes won't
  need one, so don't force one in.
- If a change needs an entirely new page, create it in the same directory as the module's other pages, add an
  `xref:` entry to the relevant `nav.adoc` in a sensible position, and link to/from related existing pages.
- Preserve any existing disclaimers/notices (e.g. an AI-generated-content notice) already present on a page
  unless the change specifically concerns them.

## Step 4b — Document the user interface (repositories with a UI only)

Read `reference/ui-docs.md` (next to this file) — it defines when a repository counts as having a UI, the
`ui/` page and `images/ui/` layout, what each page contains, which screenshots each page uses, and how screenshots
are synchronised. If the repository has no UI, skip this step. Otherwise:

- **No `ui/` section yet** (first run on a UI repository): build it for the whole UI, not only the diff — inventory
  every screen and component from the code and its doc comments, and every flow from the app's navigation
  definition, then write `ui/index.adoc`, `ui/navigation.adoc` and one page per screen/component, and add the
  **User interface** section to `nav.adoc`.
- **`ui/` section exists**: from Step 3's findings, regenerate the pages of every screen/component whose source
  changed, add pages for new ones, remove pages of deleted ones, and refresh `ui/index.adoc` and
  `ui/navigation.adoc` when the inventory or navigation changed. Leave untouched pages alone.
- Then run the screenshot synchronisation in `reference/ui-docs.md` §5 exactly once: fresh captures (offer to run
  the UI test gate when `.ui-screenshots/` is missing or stale), copy only referenced screenshots whose bytes
  changed, replace a changed component's old images, delete images and pages of removed components and any
  unreferenced image under `images/ui/`, then delete `.ui-screenshots/`.

If `reference/ui-docs.md` is missing (the skill was copied without it), document screens and components as
ordinary pages and leave screenshots out, and say so in Step 7's report.

## Step 5 — Update external documentation via a documentation MCP, if connected

Search for connected documentation/knowledge-base MCP tools (e.g. Confluence, Notion — `ToolSearch` with queries
like "confluence", "notion", "documentation", "wiki"). These are optional, environment-specific connectors, not
something every session has available.

- **If none is connected**: skip this step entirely and note that briefly in Step 7's report — there is nothing
  to do here.
- **If one or more are found**: before searching for pages, check what that connector's own tools (via
  `ToolSearch`) actually expose — read-oriented ones (search/get/read a page) vs. write-oriented ones
  (create/update/append a page). Some environments connect a documentation MCP in read-only mode deliberately
  (e.g. a Confluence connector scoped to search-and-read only, with no create-page/update-page tool at all).
  - **Only read tools are available, no write tool exists**: warn the user explicitly that the connected
    documentation MCP (name it) only supports read access, so no new or updated documentation can actually be
    generated/sent there this run, then skip the rest of this step entirely — don't spend effort drafting a page
    update that can never be applied. Note this briefly in Step 7's report too.
  - **A write tool is available**: continue with the sub-steps below.
  1. **Find the relevant existing page(s) first.** Search the connected space using keywords drawn from Step 3's
     findings (the changed classes/behaviors/commands) and the topics already touched in Step 4, so any update
     is grounded in that system's actual current content and structure rather than guessed at. Read the found
     page(s) in full — title, current structure/sections, and content — before drafting anything. If nothing
     relevant exists, say so rather than inventing a page to update.
  2. **Draft the proposed update** against that real content: what would change on each affected page (or, only
     if genuinely nothing relevant exists yet and a new page is clearly warranted, propose creating one) —
     grounded in the same diff-driven understanding from Step 3, never inventing behavior the code doesn't
     actually have.
  3. **Show the user the proposed change before sending anything.** Identify the page being targeted (title/
     link) and show a clear before/after (or diff-style listing) of exactly what would be written. Ask via
     `AskUserQuestion` whether to send it, skip it, or revise it further.
  4. **Only on explicit approval**, call the MCP tool to apply the update (update the existing page, or create
     the new one if that's what was proposed and approved). If the user declines or asks for changes, do not
     call the MCP write tool — revise the draft and re-confirm, or drop it if they'd rather skip external docs
     this round.
- This is a best-effort enrichment layered on top of the Antora updates from Step 4 — it never blocks, replaces,
  or substitutes for keeping the Antora pages themselves in sync.

## Step 6 — Verify the site still builds

If a working Node.js toolchain is available and the playbook found in Step 2 is an Antora playbook:

```bash
cd <docs-module-directory>
npm install
npx antora <playbook-file>
```

Report any Antora/Asciidoctor errors (broken `xref:`, malformed tables, bad Mermaid/MathJax syntax) and fix them
before finishing. If Node isn't available or the build can't be run, say so explicitly and note the pages were
updated but not locally verified against a real build.

## Step 7 — Report

Summarize, per page touched: what changed in the source that drove the edit, and what was updated in the docs.
Explicitly call out pages you considered but left unchanged because the diff didn't affect their content, and
any doc gaps you noticed but didn't fix because they were outside the scope of the diff being documented. For a UI repository, also report Step 4b's screenshot synchronisation: images added, replaced, unchanged and deleted, pages added/removed under `ui/`, and every state left "screenshot pending". If
Step 5 found a connected documentation MCP, also report what was sent (page, link), what was proposed but
declined/skipped by the user, and if none was connected, say so briefly.

End the report by reminding the user to check the generated documentation themselves before trusting it — point
them at the built site's start page under the module's build output directory (from Step 5, if the build ran),
since rendered Mermaid diagrams, MathJax equations, and cross-page links can look fine in source but render
wrong, and this skill's own build check does not visually inspect the output.
