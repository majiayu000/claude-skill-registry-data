---
name: init
description: Set up code-kit in a project, or bring an existing setup up to date. Works from the project's docs (new builds) or from its code (brownfield), drafts .claude/code-kit.json, the lane agents and the CLAUDE.md section, and shows the person exactly what changes before anything is enforced. Use when the person says to apply the kit to a project, to re-run or refresh it, or runs /code-kit:init [docs path].
---

# Set up or update code-kit

The argument, if given, is the path to the project's docs (a folder or one file).

Always the same shape: **read, draft, show, and switch on only once the person approves.** The hooks read only `.claude/code-kit.json`. Every draft goes to `.claude/code-kit.draft.json`, which enforces nothing.

The CLI is `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs"`, run from the project root. Its commands are `check`, `unowned`, `who`, `diff`, `baseline` and `graph`, each taking `--config <file>` to read the draft.

## Which situation

- **`.claude/code-kit.json` exists** → **Update** (section 4). The lanes stay in step with the build.
- **No config, and the docs describe the architecture** → **New from docs** (sections 1–3).
- **No config, and the docs are thin or missing** → **Brownfield** (sections 1–3, with the brownfield steps). The code is the main source, and the docs fill in what they can.

- **No config, no code and no docs** (just an idea) → stop and suggest `/code-kit:spec-design` first. It writes the brief, specs, architecture, standards, principles and plan this skill works from.

Say which one applies and why before you start.

## 1. Read everything first

1. **The docs, in full.** Every file under the docs path, not excerpts. Note where each of these is described:
   - **Layers:** names, which folders each covers, which way dependencies point, what each may not use.
   - **Work split:** lanes, teams, packages, apps or services, and who owns which paths. An implementation plan or a sub-agent table is the best source.
   - **Principles:** engineering rules, definitions of done, what counts as a contract.
   - **Protected things:** registers, contracts and schemas that need a person's sign-off.
   - **Design-first rules:** screens designed before they are built, and where approvals are listed.
   - **Commands:** test, lint, typecheck, database and deploy commands, and which must never run locally.
2. **The repository.** Map the real layout: `git ls-files | cut -d/ -f1-3 | sort | uniq -c`, package manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`), workspace files, existing lint, format and test scripts, CI workflows and CODEOWNERS.
3. **Existing kit.** If the project has `.claude/hooks`, agents or skills, read them. The kit replaces local hooks; agents and skills are kept and adapted, not rewritten. On an update (section 4), skills that came from the docs' recipes follow those recipes as they are now.
4. **Other tools.** Run `adapters --config .claude/code-kit.draft.json` once the draft exists. It lists the tools code-kit has an adapter for (such as Context Graph, found by its `.ctx/` folder), what each adds to the rules, and the setup each needs. Don't copy an adapter's paths into the config; they're added automatically while the tool is present.

**Brownfield, in addition:**

5. **Find the layers in the code.** Run `graph` (default depth 2, and `--depth 3` for deeper packages). It lists which folders import which, most-used first. Look for:
   - folders nothing depends on (the edges: apps, UI, entry points);
   - folders everything depends on (the core: domain, schemas, shared types);
   - edges in both directions between two folders. These are existing tangles; record them, don't design around them.
6. **Find the work split in the history.** Use `git log --format='%an' -- <folder> | sort | uniq -c | sort -rn | head` per top-level folder, plus CODEOWNERS. Folders that change together and are worked on by the same people make a lane.
7. **Check the checks.** Run each candidate check command once on the current code, before proposing it. If a command already fails, that's a finding, not a check to switch on silently. Offer three options: fix first, leave it out for now, or scope `files` narrower so it guards only new work.

## 2. Draft the config

Write `.claude/code-kit.draft.json`. Follow `${CLAUDE_PLUGIN_ROOT}/README.md` › Config for every field.

- **`docs`:**
  - `specs`, `principles` and `plan` as found. `plan` is the plan file itself; with stories in the `### ST-n` form, the dispatch, review and status skills work from it. Leave `specs` out if the project has no specs: without it, lanes aren't held to a spec-check report.
  - Brownfield: if there are no specs, say so, and offer the spec-check gate for later, once specs exist.
- **`layers`:** one entry per layer, documented or found in the graph. Each needs:
  - `paths`: globs matching where that layer's code really lives;
  - `mayImport`: the direction the docs set. For brownfield code, the direction most of the code already follows;
  - `denyPackages`: packages forbidden for that layer, for example `node:*` or a vendor SDK outside its adapter.
  - `label` (optional): what the layer delivers, in a few words ("API contract", "Data", "Service"), when its name doesn't say it.
  - Also add `importAliases` for path aliases in `tsconfig` `paths` that the graph can't see. Workspace package names are found automatically.
  - The import check reads JavaScript and TypeScript. For another language, record the layers anyway (agents and spec-check use them), and say the import check doesn't cover that language yet.
- **`lanes`:** one per documented or discovered ownership area. Each needs:
  - `agent`: a kebab-case agent name, for example `api-engineer`;
  - `paths` and `exclude`: every path must have exactly one owner.
  - `label` (optional): what the lane delivers, in a few words ("Screens", "Tests"), when its name doesn't say it.
- **A QA lane:** when lanes own screens, or the plan's journeys cross lanes, a `qa` lane with a `test-engineer` agent owning the end-to-end suites (the plan's work split names them; brownfield: the folders the existing end-to-end tests live in), even if the docs forgot it. Its agent's proving command runs the suites. Add a `checks` entry for them scoped by `files` to the suites, so verify runs them when they change. Unit tests stay with each lane.
- **`setup`:** `3`, the version of this setup, so `code-kit next` can tell an older project what re-running init adds.
- **`lead.paths`:** contracts, specs, design, root config, and anything the docs reserve for the lead.
- **`anyActor`:** lockfiles, if lanes may update them.
- **`protected`:** registers and contracts that need a person's sign-off, each with an `approval` name and a `why`.
- **`designGate`:** whenever a lane owns screens (web, mobile, desktop), designs come before code:
  - `register`: `design/register.json`, written now as `{ "screens": [] }`;
  - `screens`: a glob for each such lane's screen files (routes, pages, views), from the architecture's folders, with `not` for tests and stories. Where a file-based router puts other files beside its screens, `not` leaves out those that draw no screen: its layouts, API routes, middleware and special files (such as `_layout`, `+html`, `+native-intent`, `+middleware` and `*+api` in an Expo Router app, `route` and `middleware` in a Next.js one);
  - `howTo`: "Design it first: run /code-kit:design for this area's design story, and a person approves it.";
  - a `protected` entry for the register (approval `design`, why "only approved designs are built"). Never put `design` in `approvals.delegate`: approving a design is the person's.
- **`shell.block`:** deploy, release and production commands reserved for CI or a person. Each rule that names a command (`cdk deploy`, `supabase db push`, `terraform apply`) gets `"command": true`, with a pattern for the command and its arguments (`"cdk\\s+deploy\\b"`), so a grep, a heredoc or a commit message that mentions the command isn't refused, while running it, after `cd …`, through `npx` or `pnpm exec`, or in `sh -c`, still is. Leave `command` out only for a rule about the whole line, such as a download piped into a shell.
- **`shell.restricted`:** commands that affect a shared local service, limited to the lanes that own it.
- **`postEdit`:** the project's existing per-file linters and formatters, with `{file}`.
- **`checks`:** the typecheck, test, architecture and database commands, each scoped by `files`. Only include commands that pass on the current code, or ones the person chose to keep.
- **`harness.autonomy`:** ask the person how hands-off they want the build. With the code-kit mod (Claude Code 2.1.287 or later), once the plan has stories, a lead loop can keep the work moving between their prompts: it prompts the lead to dispatch ready stories, review finished ones and merge them where merges are delegated. Offer the four choices in plain words: `autonomous` (it keeps going on its own; they can pause it from the band), `propose` (each step waits in the band for their Go), `off`, or `vibe` (it keeps going on its own, and every product and project decision is the lead's: the specs for later milestones, the designs, CI, the standards, packages, weakened tests, merges and pushes; they're asked only for what nobody else can give, an account with a service provider, a key from one, a payment, or an act outside the repository). Say what vibe gives up: nobody but the lead reviews a decision before it's built on, and a push to the base can deploy. Put their answer in the draft as `"harness": { "autonomy": "…" }`. If they'd rather decide later, leave it out: the loop then asks them in the band before its first step. With `autonomous`, the lead owns delivery, so also draft `"merge": true` in `approvals.delegate`: the lead merges a reviewed branch once every check passes. With `vibe`, leave `approvals.delegate` out: vibe delegates everything, whatever it says, and the Settings tab shows every approval as the lead's.
- **`approvals.delegate`, who decides what (HELM-1, WHO-1):** the person is the product owner; the lead decides everything technical, so lanes ask the lead, never the person. With no `approvals.delegate`, that's the default: the lead approves new packages (only when the story's requirements need them and they fit the spec, the principles and the architecture; npm packages must also pass the registry limits on licence, popularity and age), every protected change except the specs (`spec`), the screens' designs (`design`), CI (`ci`) and the kit, merges into the base, and weakened tests on a lane's branch after its review. Show the person the split in two lines, what they keep and what the lead decides, and ask if they want to keep anything else. Only if they do, draft `approvals.delegate` with exactly what the lead keeps (`{ "protected": [...], "merge": true, "tests": true, "dependencies": {} }`, leaving out what they keep), or `false` to keep everything. They can change it later in the Settings tab's Approvals section.
- **`harness.agents.lanes.model`:** ask which model the lane agents run on. Each lane agent builds one story inside its own paths, with its requirements and acceptance criteria in its brief, and the hooks, `verify` and the lead's review catch what it gets wrong, so most stories don't need the session's model. Recommend `story`: each story runs on the model its `**Size:**` in the plan gives (Haiku for small, Sonnet for medium, Opus for large), raised to Opus for a security requirement, to Sonnet at least for a fix, and one step for each time its branch is sent back. Offer one model for every lane (`sonnet`) as the simpler choice, and say the lead, the reviewer and the security reviewer keep their own models either way. A lane's agent file with its own `model:` keeps that. Put their answer in `harness` as `"agents": { "lanes": { "model": "story" } }`, or leave it out for the session's model. A project set up before sizes existed has stories with none, which run on Sonnet until the lead sizes them.
- **`harness.report.on`:** ask whether agents may draft bug reports for code-kit itself when code-kit gets in their way (a refusal that shouldn't have happened, a crash). Each report holds only code-kit's own facts (its version, the rule, what it said, the command), never the project's code, paths or data, and waits in their band and the pane's Needs you: they read it and send it to code-kit's public GitHub under their own account, or discard it. Off unless they say yes; put `"report": { "on": true }` in `harness` if they do.
- **`docs.standards`:** `docs/standards.md` unless the project keeps its standards elsewhere (see Standards, below).
- **`approvals.lead`:** ask the person whether they'll ever approve from a phone or another chat-only client, where a `!` command arrives as plain text. If so, set it to `true`: the lead then records approvals they give in chat (`code-kit approve`), and runs the `shell.block` commands marked `person: true` when they say so. Mark a `shell.block` command `person: true` only if the person wants to be able to have the lead run it on their say-so. Leave the setting out if the lead will run unattended.

### Standards (spec 22)

After the layers, suggest the project's standards: named engineering rules every agent builds to, each graded and saying how firmly code-kit applies it. Standards are guardrails, and guardrails are the person's: suggest them, and write nothing until the person has approved, edited or dropped each one.

- **Format.** Each standard is a `### <id> <title>` heading in `docs/standards.md`, followed by its fields, one per line: `level` (required or recommended), `applied` (enforced, checked or advice), `layers` (layer names, or all), `why` (one or two sentences), `source` (where it came from) and, for an enforced one, `enforced by`. The id's prefix is its category: `PRI-` principles (judgement, such as single responsibility; never enforced), `PAT-` patterns (how a kind of problem is solved here), `ARC-` architecture (what may depend on what, where things live), `CON-` conventions (naming, layout, tests' shape), `POL-` policies (what must or must never happen). The title is one sentence an agent can act on.
- **How firmly.** Mark a standard `enforced` only where a rule the draft already has refuses the change, and name it: `enforced by: layers (domain may not import infrastructure)`, `layers (web may not import the package pg)`, `protected (<approval>)`, `check (<name>)` or `shell (<words of its why>)`. code-kit then names the standard in that rule's refusal. Everything else review can judge is `checked`; the rest is `advice`.
- **With specs**, suggest them from the architecture, the principles, the specs' threat models and the brief's decision log, each citing its source (`source: the threat model in docs/specs/03-payments.md`). A threat model saying card numbers are never stored is a `POL-` standard; a layer rule the architecture sets is an `ARC-` standard enforced by that layer rule. The engineering rules in `docs/principles.md` move into standards; principles keeps the definition of done, the commands and the privacy and residency targets.
- **With no specs but code**, infer them from the code: the import graph (`graph`) for layering and import directions; naming and folder layout; the data-access pattern (repositories, direct queries, an ORM); the formatter's and linter's configs; the tests' shape and where they live. Count, don't guess: each inferred standard carries its evidence (`source: the code: 41 of 43 modules reach the database through *Repository classes`), names the files that don't follow it, and starts as `recommended`. A pattern the code follows inconsistently (3 of 5 services through repositories, 2 querying directly) isn't a standard yet: put it to the person as a choice, with both counts, and write the way they pick.
- **Protect the file.** Add `{ "glob": "docs/standards.md", "approval": "standards", "why": "the project's standards" }` to `protected`, before any broader glob that also covers `docs/`. The lead may approve adding a recommended standard if the person puts `standards` in `approvals.delegate.protected`; removing a standard, or weakening a required one, is always the person's, whatever the config delegates.
- **Check it** once the config is written: `code-kit standards` reports a duplicate id, an unknown category, an enforced principle, or an `enforced by` that names no rule the config has. Each lane agent's rules then list the standards for its layers, one line each, and CLAUDE.md lists them all.

Prove the draft:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" check --config .claude/code-kit.draft.json
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" unowned --config .claude/code-kit.draft.json
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" baseline --config .claude/code-kit.draft.json
```

- **`check`:** fix every problem it reports.
- **`unowned`:** a file it lists can't be written by anyone. Give each one an owner, or confirm with the person that it should stay frozen.
- **`baseline`:** lists the layer violations already in the code.
  - New from docs: expect none. Any it finds are drift from the documented design; list them.
  - Brownfield: expect some. They'll be recorded as the baseline, so only new violations block.

## 3. Agents, CLAUDE.md, and switching on

Draft, alongside the config:

- **One agent per lane:** write `.claude/agents/<agent>.md` from `${CLAUDE_PLUGIN_ROOT}/templates/agent.md`, filled in from the docs (or the code, for brownfield):
  - owned paths;
  - its layers and what they may depend on;
  - the specs it reads;
  - the command that proves its work;
  - its lane rules: the rules the docs set for this lane, and anything the project adds to code-kit's own (its principles and architecture docs, its own words for what's banned). These are the project's, so they stay outside code-kit's part.
  - Leave out the template's `Always:` list: it's code-kit's part, which `code-kit instructions --write` adds once the config is written, between its markers.
  - If an agent already exists, keep its content and add only what's missing.
  - Drop the spec-check lines if the config has no `docs.specs`.
  - **The design tool, for reference (HAND-8):** where the architecture or the config names a design tool with an MCP server (Paper, Figma, Pencil), add that server's read-only tools to the `tools:` line of every lane agent that builds screens and of the QA lane's agent, and fill the template's **Design tool** line. Name the tools as this session lists them (`mcp__<server>__<tool>`, the server as it's installed here or in `.mcp.json`), and only the ones that read; never one that writes, exports, opens or switches a file:
    - **Paper:** `get_basic_info`, `get_selection`, `get_children`, `get_tree_summary`, `find_nodes`, `get_node_info`, `get_jsx`, `get_computed_styles`, `get_fill_image`, `get_font_family_info`, `get_tokens`, `get_screenshot`, `get_guide`, `list_resources`, `list_comment_threads`, `get_comment_thread`. Not `write_html`, `create_*`, `update_*`, `set_*`, `delete_*`, `duplicate_nodes`, `move_nodes`, `rename_*`, `arrange_pages`, `finish_working_on_nodes`, `export`, `export_combined_pdf` or `open_file`.
    - **Figma:** its read tools (`get_design_context`, `get_metadata`, `get_screenshot`, `get_variable_defs`, `get_code_connect_map`, and `get_code` or `get_image` where the server has them). Nothing that writes to the file.
    - **Pencil, or another tool:** the tools whose names and descriptions say they only read (`get_…`, `list_…`, `find_…`, screenshots, snapshots); leave out any that edits, creates or saves. When it isn't clear, leave it out and say so.
      The lanes still build from the register's exported files: they're the approved record, which the gate and the review hold the build to; the tool's live copy may have changed since, so it's for what the export can't carry (how parts relate, other artboards, interactions).
- **A security reviewer:** write `.claude/agents/security-reviewer.md` from `${CLAUDE_PLUGIN_ROOT}/templates/security-reviewer.md`, in the same approval as the lane agents, whenever the product handles sign-in, personal data, payments, input from outside (forms, APIs, webhooks, uploads) or secrets. That's almost every product; leave it out only for one with none of these, such as a static site or a local tool with no accounts, and say why. It is a reviewer, not a lane: no entry in `lanes`, no paths, and only read-only tools (Read, Grep, Glob, and Bash for commands that change nothing), so the hooks treat it as read-only too. Fill it in from the docs (or the code, for brownfield):
  - what's sensitive, who might attack it and the trust boundaries, from the specs' `## Threat model` sections (brownfield, or specs without one: from the data the code stores and the routes it exposes, as a question to the person);
  - the spec files it reads;
  - the privacy and data residency targets in the principles;
  - the project's audit commands (for example `npm audit --omit=dev`, `pip-audit`), each run once now; leave out one that isn't installed, and say so.
  - If the agent already exists, keep its content and add only what's missing.
- **CLAUDE.md:** code-kit's section is rendered from the config, not written by hand: once the config is written, `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" instructions --write` adds it between its markers (`<!-- code-kit:begin vN -->` … `<!-- code-kit:end -->`). Anything the project wants to say beyond it (its layer order in words, its docs, its own rules) goes in a section of its own, outside the markers, so a later code-kit never touches it.
- **Project skills, with the agents** (recipes like "new screen", "new migration" or "new endpoint"): one per recipe in the architecture's `## Recipes`, or any other doc that describes one step by step. Draft them now, alongside the agents, and show them in the same approval; the agents and their skills are one piece of work. Brownfield code without recipes in its docs: propose recipes from the patterns the code already follows (how its existing screens, endpoints or migrations are built), as drafts the person approves. Never write an empty one.
  - Write each as `.claude/skills/<name>/SKILL.md`, saying in its description which recipe in which doc it comes from, so an update can find it again.
  - List it under **Skills to use** on every lane agent whose paths the recipe touches, not only one: a recipe that adds a migration and the endpoint that uses it belongs to both lanes. A recipe only the lead follows goes in the CLAUDE.md section instead.

Show the person:

1. the layers and what each may depend on, and for brownfield the existing violations the baseline will record;
2. the lanes, their agents and their paths, and the security reviewer (or why it's left out);
3. protected paths, blocked and restricted commands, and checks (including any left out because they fail today);
   and whether the lead may record approvals given in chat (`approvals.lead`), how hands-off the build is (`harness.autonomy`), the lane agents' model (`harness.agents.lanes.model`), and whether agents may draft bug reports for code-kit (`harness.report.on`);
4. the project skills, and which lane agents use each;
   and the standards you suggest, each with its category, level, how it's applied and its source (for inferred ones, the evidence and the files that don't follow it), with the choices where the code is inconsistent;
5. the active adapters and what each adds, from `adapters`. A companion tool that's installed but not set up here (its init skill is in your skills list, for example `/context-graph:init` with no `.ctx/` folder): add `"adapters": { "<name>": true }` to the draft and say it will be set up before any code is written;
6. every **question**: where the docs or the code are silent, ambiguous or contradictory. Don't guess; a wrong owner or layer blocks real work.

Once they approve (with any changes):

1. Rename the draft to `.claude/code-kit.json`. From then on, every hook enforces it.
2. If there are existing violations, run `baseline --write`. This writes `.claude/code-kit.baseline.json`.
3. If the project had local hooks in `.claude/settings.json` that the kit replaces, remove those hook entries and the local hook files. Keep the `permissions` block.
4. Add `.claude/approvals/`, `.claude/state/` and `.claude/code-kit.draft.json` to `.gitignore`. Add `.claude/approval-log.jsonl merge=union` to `.gitattributes`: when lanes and the lead both log changes, merging keeps every entry instead of conflicting.
5. Apply each active adapter's `setup` lines (ignore files, merge drivers, the CLAUDE.md note), and say which you applied.
6. Offer CI enforcement, since the hooks only see Claude Code sessions. On yes:
   - write `.github/workflows/code-kit.yml` from `${CLAUDE_PLUGIN_ROOT}/templates/github-workflow.yml`;
   - set the version from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`;
   - fill in the steps that install the project's dependencies, from its existing CI or package manager (a fix story's test is run without its fix, REG-1). The job runs `verify --no-checks`: the merge queue already ran the checks before each merge. Ask whether people open pull requests from outside Claude Code and want those proven at once; only if they do, take `--no-checks` out;
   - make sure the lead owns the workflow file, and add it to `protected` (approval `ci`, why "the CI that enforces the rules"), so a lane can't switch it off;
   - tell the person to make the `code-kit` check required on the protected branches;
   - run `code-kit ci check` on the project's own workflows. Each story is its own branch, pull request and merge, so a workflow that runs its full suite on every push to the base or every pull request runs once per story, after the merge queue has already run the checks. Show the person what it found and the changes you propose: the full suite on `release/**` instead (`code-kit release <version>` cuts one when they release), a `timeout-minutes` on each job, and `concurrency` with `cancel-in-progress` on pull requests. Changing CI is theirs to approve (approval `ci`); make only the changes they approve.
7. Run `check` and `unowned` again, without `--config`.
8. Commit the setup straight onto the base branch (usually `main`), not a branch: while the base has no `.claude/code-kit.json` committed, the hooks let the lead make that one commit, so the rules the person just approved are in force on `main` and the lead can merge reviewed work from the start, with no first merge for anyone to make. The person's approval of the setup covers the protected files in it (the specs, the standards, the design register): they need no approvals of their own in that commit, and the kit records each in `.claude/approval-log.jsonl` as part of the setup. Don't ask the person for them. If the base already has rules (an update, section 4), commit on a branch as usual.
9. **A team, only if there is one.** Not every developer works in a team. Ask once: "Do other developers work in this repository with their own Claude Code sessions?" If yes, run `/code-kit:team-init` now (it asks who the tech lead is and who owns which lanes, and writes the `team` section). If no, or not yet, leave it out and say `/code-kit:team-init` sets it up any time.
10. Set up each companion the config now wants (`"adapters": { "<name>": true }`) by running its init skill, for example `/context-graph:init`, which asks nothing. Do it before reporting, so it's in place before the coding loop starts; `code-kit next` also gives `setup` until it is.

Report what was set up, what's enforced from now on, how many existing violations the baseline holds, and the open questions. Say who does what from here: the person owns the intent and the rules; the lead owns delivery, so it dispatches, reviews, sends back and merges, and decides what lanes ask for inside the guardrails, and only what crosses a guardrail (the specs, the architecture, a design, a product question the spec doesn't answer) comes to the person.

If the project has no `.ctx/` folder and Context Graph isn't installed, don't install it unless the person asks: "Context Graph can give each lane agent the why behind the files it edits (cards, rules and decisions kept in git), with this spec's requirements and layer rules in them: `/plugin marketplace add warrendeanlangeveldt/context-graph`, then `/plugin install context-graph@context-graph`."

## 4. Update an existing setup

Re-run whenever the build has moved on: new apps or packages, folders that moved, a changed plan, or files `unowned` keeps listing.

1. **Re-read** the docs and the repository as in section 1, including the brownfield steps if the code has grown past the docs.
2. **Draft** the whole config again into `.claude/code-kit.draft.json`, starting from the live one. Keep everything that's still right, so the diff shows only real changes. If the live config has no `harness.autonomy`, ask the person about it as in section 2.
   Bring code-kit's own instructions up to date: run `code-kit instructions`. Parts between markers are rewritten with `--write`. A part written before the markers (CLAUDE.md's `## Enforced, not advised` section, an agent's `Always:` list) is merged once: replace it with what `code-kit instructions show lead` or `show lane <lane>` prints, and move every line the project wrote itself into a section of its own outside the markers. Show the person the difference with the rest.
   A config without `"setup": 3` predates what setup now includes; add whichever of these the project is missing, as section 2 and 3 describe, and set `"setup": 3`:
   - project skills for the recipes in the docs (or, without recipes, the patterns the code follows), listed on the lane agents;
   - the design gate for every lane that owns screens, with its register; and design stories in the plan for screens not yet built (ask the person before adding stories);
   - the QA lane, its agent and its checks, when there are screens or journeys across lanes;
   - the security reviewer (`.claude/agents/security-reviewer.md`), unless the product handles no sign-in, personal data, payments, outside input or secrets; and, as a proposal for the person, a threat model and security requirements for each spec that lacks them (spec-design's section 4);
   - `"adapters": { "<name>": true }` for a companion that's installed but not set up, which is then set up before any code.
   - project standards, when the project has no `docs/standards.md`: suggest them as section 2's Standards describes, moving the engineering rules out of `docs/principles.md`, and protect the file.
3. **Show the difference:**

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" diff --config .claude/code-kit.draft.json
   node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" unowned --config .claude/code-kit.draft.json
   ```

   `diff` lists lanes, layers, checks and rules that were added (`+`), removed (`-`) or changed (`~`), and how many files change owner, route by route. Explain each change in a sentence, with where it came from: the doc section, or the folder in the repository.

4. **Also propose:**
   - agent files for new lanes, and updates to agents whose paths changed, and to the security reviewer when the specs' threat models changed;
   - **project skills**, by reading the recipes in the docs again and comparing them with `.claude/skills/`:
     - a new skill for each recipe the docs now describe that has none;
     - an update to each skill whose recipe changed, showing what changed;
     - removing a skill whose recipe is gone from the docs (ask first: the person may want it kept);
     - the matching **Skills to use** changes on every lane agent whose paths each recipe touches;
     - skills the person wrote themselves, with no recipe behind them, stay as they are;
   - a smaller baseline when `baseline` shows violations were fixed. It only ever shrinks.
5. **On approval:**
   1. Replace `.claude/code-kit.json` with the draft and delete the draft.
   2. Write or update the agents, and write, update or remove the project skills as approved, together.
   3. Run `baseline --write` if it shrank.
   4. Run `check` and `unowned`.
   5. Commit on a branch.

   Nothing changes until then.
