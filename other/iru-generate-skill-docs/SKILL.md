---
name: iru-generate-skill-docs
description: Analyze every Claude Code skill (`.claude/skills/*/SKILL.md`) and agent (custom definitions under `.claude/agents/*.md`, plus built-in agent types referenced from skills via the `Agent` tool) defined in this repository, and generate/update the Antora documentation describing them — a reference table and dependency graph in `index.adoc`, purpose-grouped sections for the catalog's recurring end-to-end workflows, and one detail page per skill/agent under `docs/modules/ROOT/pages/skills/` and `.../agents/` covering its purpose, inputs, outputs, execution flow, and dependencies. Invoke as `/iru-generate-skill-docs`. Idempotent — safe to re-run whenever skills/agents are added, removed, or changed; it regenerates content from the current `SKILL.md`/agent definitions rather than hand-maintaining pages that drift from them. Use whenever this catalog's own documentation needs to reflect its actual current set of skills and agents, instead of manually writing or updating each page by hand.
model: sonnet
---

# Generate Skill Docs

Turn the actual, current set of Claude Code skills and agents defined in this repository into an Antora
documentation site: a reference table, a dependency graph, purpose-grouped workflow walkthroughs, and one
detail page per skill/agent. This skill only writes documentation — it never edits a `SKILL.md`, an agent
definition, or any other source file. It makes no assumption about which skills or agents exist; discover
the real, current set fresh each run so the generated docs never drift from what's actually on disk.

## Step 1 — Locate the Antora documentation module

Find `antora.yml` (`find . -name antora.yml -not -path '*/node_modules/*'`).

- **Not found**: there is no documentation module to write into yet. Ask the user whether to bootstrap one
  now via the `iru-setup-antora` skill (run as a sub-agent via the `Agent` tool, briefed that it's about to be
  followed by this skill so its starter pages don't need to anticipate skill/agent documentation). If they
  decline, stop here — there's nothing for this skill to write into.
- **Found**: read it for the component name and the `nav:` file(s) it declares, then read that `nav.adoc` to
  get the current page list. Note the antora playbook (commonly `antora-playbook.yml`) and confirm it wires
  up a Mermaid extension — every diagram this skill produces is a `[mermaid]` block, and it's silently
  useless if the extension isn't configured. If it isn't, tell the user and either stop or fall back to
  plain bulleted/tabular descriptions instead of diagrams, per their choice.

## Step 2 — Discover every skill and agent actually defined

- **Skills**: `find .claude/skills -maxdepth 2 -name SKILL.md`. Each is one skill; its directory name is its
  canonical name (should match the `name:` frontmatter field — flag any mismatch).
- **Custom agents**: `find .claude/agents -maxdepth 1 -name '*.md'` (the directory may not exist yet — that's
  not an error, just means there are none). Each is one custom agent definition.
- **Built-in agent types actually used**: grep every `SKILL.md` found above for `Agent(` / `Agent tool` /
  `subagent_type` usage. For each call site, note whether it names a specific agent type (e.g. `"Explore"`)
  or omits `subagent_type` entirely (which resolves to Claude Code's default, `general-purpose`, at
  invocation time). Only document a built-in type here if some skill in this repository actually spawns it
  — don't produce a page for every agent type Claude Code ships, only the ones this catalog uses.
- Build a plain list of every skill name and every agent (custom or built-in-but-used) found. This is the
  complete inventory the rest of this skill documents — if it's empty of skills, tell the user there's
  nothing to document and stop.

## Step 3 — Read and classify each skill/agent, via one sub-agent per item

Reading every skill's full `SKILL.md` (and every custom agent's definition) directly in this conversation is
exactly the kind of thing this catalog's own `iru-gate-runner`/`iru-change-summarizer` agents exist to avoid elsewhere —
with a few dozen skills, doing that inline here would make this one of the heaviest single passes in the whole
catalog. Instead, dispatch one sub-agent per skill/agent found in Step 2, each reading only its own file and
returning a compact, structured summary — not its full content — for this conversation to collect and use in
Steps 4 onward. Dispatch these concurrently (they're independent, each reading a different file) rather than one
at a time.

For each skill:

```
Agent({
  description: "Extract metadata for <skill-name>",
  prompt: "Read .claude/skills/<skill-name>/SKILL.md in full. Extract and report back, concisely — not the file's
    raw content:
    - purpose: the description frontmatter field expanded into a short paragraph grounded in the skill's opening
      paragraph and step list.
    - invocation: the exact slash-command form(s) from the description's 'Invoke as' text.
    - inputs: any positional argument(s) or an args key:value block accepted, what happens when an expected
      argument is missing, and defaults.
    - outputs: concrete artifacts/side effects (files created/modified, PRs/branches opened, or 'report only') —
      grounded in the skill's own final Report step and any step that explicitly writes/edits something.
    - steps: the numbered '## Step N' headings in order, each with a one-line summary including any real branch
      (an early stop, an AskUserQuestion choice, a loop back to an earlier step).
    - invokes: every other skill this one calls via Skill(...) or 'invoke the X skill' prose, with the step
      number and why.
    - spawns: every Agent(...) call this one makes — which built-in or custom agent type it names (or 'default,
      i.e. general-purpose' if none is named), the step number, and why a sub-agent is used there.
    - external_deps: any skill named that does NOT exist under .claude/skills/ in this repository.",
  run_in_background: false
})
```

For each custom agent (`.claude/agents/*.md`), dispatch the same shape, adapted: purpose, and `tools` (its
`tools:` frontmatter) — skip `used_by`, since Step 4 derives it by inverting every skill's own `spawns` list
rather than asking the agent's own file about its callers.

For each built-in agent type found in Step 2 (e.g. `Explore`, `general-purpose`), there's no file to dispatch a
sub-agent against — summarize its definition directly from the session's own agent-type list (or, absent that,
general Claude Code documentation); the detail worth capturing is *where and why this repository's skills use
it*, gathered from the `spawns` fields collected above.

Collect every returned summary, keyed by skill/agent name — this collected set, not the raw files, is what Steps
4 onward work from.

## Step 4 — Build the dependency graph

Use the `invokes`/`spawns`/`external_deps` fields Step 3 already collected for every skill — there's no need to
re-read or re-scan any `SKILL.md` here, Step 3's dispatch already extracted exactly this:

- **Skill invokes skill**: from each skill's `invokes` field — the calling skill's step number and *why* (e.g.
  "to ground the plan in a prior exploration").
- **Skill spawns agent**: from each skill's `spawns` field — which built-in/custom agent type each one uses (or
  "default, i.e. `general-purpose`" if none is named) and why a sub-agent is used here specifically (context
  isolation from a verbose report, running a delegated skill with a clean context, parallelizing independent
  work) — this "why" belongs on both the skill's page and the agent's page.
- **External dependencies**: from each skill's `external_deps` field — a skill referenced by name that does
  **not** exist under `.claude/skills/` in this repository (e.g. one assumed to be available globally/
  session-wide rather than checked into this catalog). Record these separately — they get named in prose on the
  relevant detail page(s) and in the dependency graph, but never get their own detail page or a broken `xref:`
  link.
- Invert the "invokes"/"spawns" edges to get "invoked by"/"used by" for each target.
- A skill or agent with no inbound edges from this repository's own skills is a top-level entry point
  (typically invoked directly by a person) — note that explicitly rather than leaving its "invoked by"
  section looking like an oversight.

## Step 5 — Group by purpose

Cluster the skills into a small number of purpose groups based on the role each plays, using the dependency
graph from Step 4 and each skill's own description as evidence — orchestrators and the skills they invoke
usually belong together. Don't assume a fixed taxonomy or a fixed number of groups: infer groups that fit
the actual current skill set, and expect this to change as skills are added or removed. Give each group a
short, descriptive name and a one-paragraph summary of what it covers. Assign every skill to exactly one
primary group, even if it's also reused from a workflow that spans groups (note that reuse in prose rather
than double-counting it).

## Step 6 — Identify the catalog's recurring end-to-end workflows

Separately from the purpose groups (which categorize skills), identify the handful of real, multi-skill
sequences a user actually runs end to end — evidenced by an orchestrator skill's own step list, or by two
standalone skills that are commonly run back-to-back per their own descriptions (e.g. "run after code has
already changed"). Typical examples in a repository like this one: bootstrapping a brand-new repository,
going from a tracked issue to an open/reviewed pull request, cutting a release, and refreshing docs/README/
changelog after unrelated code changes — but derive the actual list from what this repository's skills
really support rather than assuming these four apply verbatim. For each workflow, note the ordered sequence
of skills involved and any decision points (e.g. "hand off to `/iru-code` automatically, or stop for manual
review?").

## Step 7 — Write `index.adoc`

Update (don't blindly overwrite unrelated hand-written content) the top-level page to contain, in this
order:

1. Whatever introductory/conceptual material already exists (what this repository is, why it exists) —
   preserve it; only add a short "core concepts" note about agents if Step 2 found any custom or built-in
   agent usage and the page doesn't already explain the skill/agent distinction.
2. **A reference table**: one row per skill and per documented agent, with columns for name, purpose group
   (linking to that group's section via an anchor, e.g. `xref:index.adoc#group-<slug>[]`), a one-line
   purpose, and a link to its detail page (`xref:skills/<name>.adoc[]` or `xref:agents/<name>.adoc[]`).
   Every name in this table must resolve to a real page created in Step 8 — no dangling links, and no row
   for an external dependency that isn't actually part of this catalog.
3. **Purpose groups**: one subsection per group from Step 5, each with its own anchor (`[[group-<slug>]]`
   immediately above the `===` heading) matching what the table links to, a short description, and the
   skills it contains.
4. **A dependency graph**: a single `[mermaid]` `flowchart` (subgraphs per purpose group keep a catalog of
   more than a handful of skills readable) showing every "invokes" edge as a solid arrow and every "spawns
   an agent" edge as a dotted arrow, per Step 4. Name any external dependency in the diagram (e.g. as a
   dashed/external-looking node) without linking it anywhere.
5. **Common workflows**: one subsection per workflow from Step 6, each with a short `[mermaid]` flowchart of
   its skill sequence and prose noting any decision points and which skills also work standalone.

Match the AsciiDoc conventions already used on this page (table `[cols=...]` syntax, `xref:` link style,
any existing AI-generated-content disclaimer note — keep it on every page you touch or create).

Give the page (or refresh it, if already present) SEO document attributes right after the `= AI Catalog`
title line, with **no blank line between the title and the attributes** — a blank line ends the AsciiDoc
document header, and Antora's default UI only reads `:description:`/`:keywords:` into the page's
`<meta name="description">`/`<meta name="keywords">` tags when they're real header attributes, not body
text:
- `:description:` — a single plain-text line (no markup, no xrefs), 120-155 characters, summarizing what
  this catalog actually is right now (grounded in Step 1's opening paragraph and the current skill/agent
  count from Step 2).
- `:keywords:` — 6-10 lowercase comma-separated terms grounded in the actual current catalog: "claude code
  skills", "claude code agents", the purpose-group names from Step 5, and the languages/platforms this
  catalog's skills actually cover (e.g. java, dotnet, github, jira — only ones truly present).

## Step 8 — Write one detail page per skill and per documented agent

Create (or update, if re-running after a skill/agent changed) `docs/modules/ROOT/pages/skills/<name>.adoc`
for every skill, and `docs/modules/ROOT/pages/agents/<name>.adoc` for every custom agent — or a single
`docs/modules/ROOT/pages/agents/overview.adoc` covering all built-in agent types together, if there is no
`.claude/agents/` directory to give each one its own natural page. Give every page this shape:

1. `= <Title>` heading, immediately followed — **no blank line in between**, since a blank line ends the
   AsciiDoc document header and Antora's default UI only picks up `:description:`/`:keywords:` as page
   metadata (`<meta name="description">`/`<meta name="keywords">`) when they're real header attributes — by:
   - `:description:` — a single plain-text line (no markup, no backticks, no xrefs), 120-155 characters,
     a concrete summary of what this specific skill/agent does, grounded in Step 3's expanded purpose.
     Distinct per page; never reused boilerplate.
   - `:keywords:` — 6-10 lowercase comma-separated terms grounded in this page's actual content: the
     skill/agent's own name, "claude code skill" or "claude code agent", the specific technology/domain it
     actually mentions, and 2-3 action-oriented phrases describing what it does.
   Then the repository's existing AI-generated-content disclaimer note if one is used elsewhere in this
   docs module.
2. A short intro paragraph (the expanded purpose from Step 3).
3. `== Purpose` — the fuller explanation of what problem this skill/agent solves and how it fits the catalog.
4. `== Purpose group` — an `xref:index.adoc#group-<slug>[]` link to its Step 5 group (skills only).
5. `== Invocation` and `== Inputs` — the slash command and a table of arguments (name, required, description,
   default), grounded in Step 3.
6. `== Outputs` — grounded in Step 3.
7. `== Execution flow` — a `[mermaid]` `flowchart` derived from the skill's real `## Step N` headings (or the
   agent's real behavior) — collapse a long, repetitive sub-loop (e.g. "for each task: implement, test,
   document, quality-check") into one labeled node rather than drawing every sub-step literally, but don't
   omit a real branch or stopping condition.
8. `== Dependencies` with `=== Invokes` / `=== Invoked by` / `=== Related agents` subsections (skills), or
   `=== Used by` (agents) — every real edge from Step 4, each catalog skill linked via `xref:skills/<name>.adoc[]`
   and each documented agent via `xref:agents/<name-or-overview>.adoc[]`; external dependencies named in prose
   with no link; "None" stated explicitly rather than the section being silently empty when there really are
   no edges.
9. `== Source` — a link to the actual file this page documents, so a reader can jump straight from the
   generated docs to the definition it was generated from. Derive the repository's web URL and current
   branch (`git remote get-url origin`, `git branch --show-current` or equivalent default-branch lookup) once
   and reuse it for every page rather than hand-guessing or hardcoding a stale one. Skip this section
   entirely for a built-in agent type (there is no repository file to link to) or note "not tracked in this
   repository" instead of a broken link if the remote can't be resolved (e.g. no `origin`, or it isn't a
   web-viewable host).
   - Skill page link text: "SKILL.md on GitHub", target `<repo-url>/blob/<branch>/.claude/skills/<name>/SKILL.md`
   - Custom agent page link text: "<name>.md on GitHub", target `<repo-url>/blob/<branch>/.claude/agents/<name>.md`

When re-running this skill after a skill/agent was added, removed, or materially changed: update only the
pages whose source actually changed, add pages for new skills/agents, and remove pages (and their `nav.adoc`
entries and any table rows/edges referencing them) for ones that no longer exist — don't regenerate every
page from scratch on every run if most of the catalog is unchanged.

## Step 9 — Update `nav.adoc`

Add an `xref:` entry for every new page from Step 8 that isn't already listed, nested under a "Skills" and,
if any agent pages exist, an "Agents" heading (matching whatever nesting style `nav.adoc` already uses
elsewhere in this module). Preserve the order and content of existing entries; remove entries only for pages
Step 8 determined no longer exist.

## Step 9b — Angle brackets in Mermaid labels

Applies to every `[mermaid]` block written in Steps 7 and 8. Placeholder names are written `<timestamp>`,
`<task-id>`, `<key>` and so on throughout this catalog's prose — but inside a Mermaid **node or edge label**
that spelling is silently destroyed, and the failure is invisible in the build:

- An AsciiDoc literal block (`....`) escapes `<` to `&lt;` in the HTML, and Asciidoctor passes an entity
  reference already in the source (`&lt;`) straight through unchanged. Both spellings therefore reach the
  browser as `&lt;…&gt;`, and `textContent` hands Mermaid a literal `<timestamp>`.
- Mermaid renders labels as HTML (`htmlLabels`, on by default), so `<timestamp>` is parsed as an unknown tag
  and **dropped from the diagram entirely** — `meeting-<timestamp>/meeting.md` renders as
  `meeting-/meeting.md`. Setting `htmlLabels: false` does not help; the text is lost either way.

So write the placeholder **double-escaped** in the AsciiDoc source — `&amp;lt;timestamp&amp;gt;` — which
reaches Mermaid as `&lt;timestamp&gt;` and renders as the intended `<timestamp>`:

```
F --> G["Create meeting-&amp;lt;timestamp&amp;gt;/meeting.md\n(Summary + Full transcription)"]
```

Do **not** use Mermaid's `#60;`/`#62;` entity codes for this. They work in `["…"]` and `{"…"}` nodes but throw
`Invalid character` in the stadium (`(["…"])`) and subroutine (`[["…"]]`) shapes this catalog's diagrams use,
which kills the whole diagram. Rewording the label to avoid angle brackets altogether is also fine.

Only label *text* is affected. Never touch link syntax — `-->`, `-.->`, `==>`, `<-->` are Mermaid operators and
must stay literal. `\n` inside a label is fine and does produce a line break.

The same care applies to **double quotes inside a quoted label**. Mermaid has no backslash escape: a label
written `G["Report \"coverage not wired\""]` ends the string at the first inner quote and the parser then fails
on the rest, which — unlike the angle-bracket case — kills the whole diagram with a syntax error. Either reword
the label so it needs no inner quotes (`G["Report: coverage not wired"]`, `H["run dotnet test --collect:\nXPlat
Code Coverage"]`), or use single quotes inside the double-quoted label. Don't reach for `#quot;` for the same
reason `#60;`/`#62;` are avoided above.

## Step 10 — Verify the site builds

From the docs module directory:

```bash
npx antora <playbook-file>
```

Fix any broken `xref:` (a typo'd skill/agent name, a page created under the wrong path), malformed table, or
invalid Mermaid syntax before finishing — don't report success against a build that actually failed or
warned about content this skill just wrote.

A clean Antora build proves nothing about the diagrams: the extension emits the block as a `<div class="mermaid">`
and the browser renders it, so a diagram that throws a syntax error or quietly drops a swallowed label still
builds without a single warning. Check the diagrams themselves — grep the `[mermaid]` blocks just written for
raw `<…>` placeholders per Step 9b, and confirm each one still says what it should.

## Step 11 — Report

Summarize: how many skills and agents were found and documented, the purpose groups and workflows
identified (name them), any external dependency named but not linked, any page added/updated/removed versus
the previous run (if this is a re-run), and the build result from Step 10. Remind the user to review the
generated pages themselves, particularly the dependency graph and any workflow this skill inferred rather
than found spelled out explicitly in an orchestrator skill's own steps.
