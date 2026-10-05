---
name: skill-builder
description: >
  Author a new processkit skill end-to-end — use-case interview,
  frontmatter, body sections, Gotchas, and trigger-phrase generation.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-skill-builder
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: index-management
        purpose: "Query existing skills before creating a new one to surface duplicates and to find related skills the new one should reference under uses:."
      - skill: event-log
        purpose: "Log skill.created and skill.reviewed events so the project's audit trail captures when new skills enter the catalog."
    provides:
      primitives: []
      mcp_tools: []
      assets: [skill-template]
      processes: [skill-creation]
    commands:
      - name: pk-skill-new
        args: "skill-topic"
        description: "Start the interactive skill-creation workflow for a given topic"
---

# Skill Builder

## Intro

`skill-builder` is the canonical interactive workflow for authoring a
new processkit skill from scratch. It walks the user through use-case
discovery, frontmatter authoring, body section drafting, mandatory
Gotchas authoring, validation against the 5 Skill Killers, and trigger
test generation — producing a complete `src/skills/<name>/` folder that
follows the [Agent Skills](https://agentskills.io) standard and
processkit's conventions.

This is the first skill to reach for whenever a new skill needs to be
written. Building a skill without skill-builder almost always produces
something with at least one of the 5 Skill Killers — usually a vague
description, a missing or generic Gotchas section, or scope creep.

## Overview

### The seven-step workflow

```
1. Interview      → 2-3 concrete use cases the skill should enable
2. Scope check    → confirm one-sentence-one-skill rule
3. Pattern pick   → match the use case to one of the 5 patterns (or none)
4. Frontmatter    → name, description (with triggers), metadata.processkit
5. Body draft     → Intro, Overview, Gotchas (mandatory!), Full reference
6. Self-check     → 5 Skill Killers + Anthropic troubleshooting playbook
7. Trigger tests  → positive cases that fire, negatives that don't
```

Walk the user through each step in order. Skipping a step (especially #1
or #5) is the single most common failure mode.

### Step 1 — Interview

Before writing any YAML or Markdown, ask the user for **2-3 concrete use
cases** the skill should enable. Anthropic's guide insists on this for
good reason: a skill defined without use cases ends up vague,
over-scoped, or both.

Good use case format:

```
Use Case: <name>
Trigger: User says "..." or "..."
Steps:
  1. ...
  2. ...
  3. ...
Result: <what success looks like>
```

For each use case, capture (a) the literal trigger phrases, (b) the
steps the skill would execute, (c) the result that proves success.

If the user can't articulate 2-3 use cases, the skill isn't ready to be
built. Push back: *"Can you give me one more concrete example where
you'd use this?"*

### Step 2 — Scope check

Apply the **one sentence, one skill** rule (Skills Master Class Level
2): if you can't describe what the skill does in one sentence without
conjunctions ("and", "also", "plus"), it's probably two skills. Split
before continuing.

| Bad scope | Good scope |
|---|---|
| "Create work items AND record decisions AND log events." | "Create work items with proper state-machine handling." |
| → Three skills (workitem-management, decision-record, event-log). | → One skill (workitem-management). |

### Step 3 — Pattern pick

Match the use cases to one of the **5 patterns** from Anthropic's guide
(PDF Chapter 5):

| Pattern | Use when | Example |
|---|---|---|
| **Sequential workflow orchestration** | Multi-step process in a specific order | Onboard a new customer (account → payment → subscription → email) |
| **Multi-MCP coordination** | Workflow spans multiple services with phase separation | Design-to-development handoff (Figma → Drive → Linear → Slack) |
| **Iterative refinement** | Output quality improves with iteration loops | Report generation (draft → quality check → refinement → finalization) |
| **Context-aware tool selection** | Same outcome, different tools depending on context | Smart file storage (cloud / docs / git / local based on file properties) |
| **Domain-specific intelligence** | Skill adds specialized knowledge beyond raw tool access | Payment processing with compliance checks before/after the call |

Some skills don't fit any pattern — pure knowledge skills like
`python-best-practices` or `code-review`. That's fine. Use no pattern;
just write the conventions clearly.

### Library expert skills

When the target skill is a library expert, use
`references/library-expert-template.md` as the starting point. Library expert
skills are version-pinned and recipe-heavy: the baked-in examples are primary,
and RAG/live-doc lookup is reserved for newer versions, missing recipes, or
integration-specific details.

Add these library-expert steps before frontmatter is final:

1. Verify the current stable version from official docs.
2. Choose the version range the skill owns; avoid unbounded "latest"
   claims.
3. Collect 5-15 common tasks as recipe candidates.
4. Prefer official examples, release notes, and migration guides over
   blog posts.
5. Decide the escalation rule for live docs or RAG before writing
   recipes.

Library expert skills must include `metadata.library` with `name`,
`version`, `homepage`, and `docs`. If any of those are unknown, stop at
a spike note instead of publishing the skill as authoritative.

### Step 4 — Frontmatter

Generate the YAML frontmatter following the Agent Skills standard.
Start from `assets/skill-template.md` and fill in the placeholders.
The shape:

```yaml
---
name: <kebab-case-name>
description: >
  <One-sentence imperative (verb-first): what the skill does.>
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-<kebab-case-name>
    version: "1.0.0"
    created: <YYYY-MM-DDTHH:MM:SSZ>
    category: <process|language|framework|infrastructure|...>
    layer: <0-4 for process skills, null otherwise>
    uses:
      - skill: <other-skill>
        purpose: "<one sentence: why this skill uses the other>"
    provides:
      primitives: [...]
      mcp_tools: [...]
      assets: [...]
    # If the skill has user-invocable workflows, add:
    commands:
      - name: <skill-name>-<workflow>
        args: "arg-shape"          # no angle brackets
        description: "One sentence: what this command does"
---
```

**Critical rules** (Anthropic PDF p10-11):

- `name` must be kebab-case, must match the directory name, must NOT
  contain "claude" or "anthropic" (reserved by Anthropic).
- `description` must be a **one-sentence imperative** (verb-first:
  "Author X", "Review Y for Z", "Generate W"). Under 200 characters.
  NO "Use when the user says…" — trigger phrases live in
  skill-finder's trigger table (Step 9), not here. NO XML angle
  brackets (`<` / `>`) in frontmatter — they inject into the system
  prompt.
- Every entry under `uses:` must have a `purpose` field — no bare
  strings.

### Step 5 — Body draft

The SKILL.md body has FOUR sections, in this order: Intro, Overview,
Gotchas, Full reference. See the template at `assets/skill-template.md`
for the canonical structure.

**Write Gotchas BEFORE finalizing Overview.** Anthropic's guide and the
Skills Master Class both call Gotchas the "highest-signal content" —
where the model goes wrong. Authoring it first surfaces the assumptions
the skill is implicitly making and often forces clarifications back into
Overview.

Rules for a good Gotchas section:

- **Agent-only failure modes**, not general practitioner pitfalls.
  (Those go in Anti-patterns under Full reference.)
- **Provider-neutral.** What's obvious to Claude may not be obvious to
  Gemini, ChatGPT, or whatever harness loads the skill. Don't assume
  the agent is Claude.
- **Specific.** "Don't be sloppy" is useless. "Always check call sites
  before approving a function signature change because the diff hides
  unchanged callers" is useful.
- **5-10 items.** Fewer means you haven't thought hard enough; more
  means you're padding.

To draft Gotchas, ask yourself five questions:

1. What would an agent get wrong on the first try?
2. What does the agent need to KNOW that the user wouldn't think to say?
3. Where would the agent helpfully overshoot (do more than asked)?
4. Where would the agent helpfully undershoot (leave the user hanging)?
5. What conventions are unique to this skill that the agent has to learn?

If you can't answer all five concretely, the Gotchas section isn't
ready.

### Step 6 — Self-check (the 5 Skill Killers)

Before declaring the skill done, run it through the **5 Skill Killers**
checklist (Skills Master Class Level 2):

| # | Killer | Self-check question |
|---|---|---|
| 1 | Description doesn't trigger | Does the description include literal trigger phrases? Specific enough that an agent would know when to load it? |
| 2 | Over-defining process | Did you over-prescribe steps when the agent should have degrees of freedom? |
| 3 | Stating the obvious | Is anything in the SKILL.md what a decent agent already knows? Cut it. (BUT — be careful about provider neutrality.) |
| 4 | Missing Gotchas | Is the Gotchas section present, specific, and provider-neutral? |
| 5 | Monolithic blob | Is the SKILL.md under 5000 words? If not, push detail to `references/`. |

Plus Anthropic's troubleshooting playbook (PDF p25-27): under-trigger,
over-trigger, instructions not followed, large context. Each has a
known fix listed there.

For library expert skills, also run the library-specific self-check
from `references/library-expert-template.md`: version is explicit,
recipes are runnable or clearly marked unverified, live-doc escalation
is defined, and examples do not mix major versions.

If any check fails, fix it before continuing.

### Step 7 — Trigger tests

Write a list of positive and negative trigger test cases. The agent (or
`skill-reviewer`) can run these mentally:

```
Should trigger:
  - "<phrase the user might actually say>"
  - "<paraphrased version>"
  - "<edge case that should still trigger>"

Should NOT trigger:
  - "<adjacent task that belongs to a different skill>"
  - "<too-vague phrase>"
  - "<unrelated task>"
```

If you can't write at least 3 positive and 3 negative cases, the
description is too vague — go back to Step 4.

### Step 8 — Create command adapter files

If the skill's `metadata.processkit.commands` list is non-empty, create one
adapter file per command under `commands/`:

**File:** `commands/pk-<workflow>.md`

```markdown
---
argument-hint: arg-shape
allowed-tools: []
---

Use the <skill-name> skill, Workflow X (name), for $ARGUMENTS.
```

Rules:
- File name must exactly match the `name` field in `commands:`.
- Processkit-category slash commands must use the reserved `pk-`
  prefix so every harness exposes a consistent command namespace.
- Body is one sentence — no logic, no workflow steps. Everything lives in SKILL.md.
- `allowed-tools` scoped as narrowly as possible. Use `[]` if no shell access is
  needed. Never use `Bash(*)` unless the command genuinely runs arbitrary shell.
- `argument-hint` must match the `args` field from `metadata.processkit.commands`.

Add a one-line mention of the command in SKILL.md's Overview so agents discover it
when reading the skill, not only when the user types `/command-name`:

```markdown
This skill also provides the `/pk-model-profile` command for direct
invocation — see `commands/pk-model-profile.md`.
```

Project each command into the supported harness surfaces:

- Copy the canonical adapter to `.claude/commands/<name>.md` for Claude Code
  slash-command registration.
- Create `.agents/skills/<name>/SKILL.md` with matching name/description/body
  for harnesses that trigger skills from natural-language requests instead of
  custom slash commands.

This skill also provides the `/pk-skill-new` command for direct
invocation — see `commands/pk-skill-new.md`.

### Step 9 — Update skill-finder

After the skill passes the self-check, add it to `skill-finder`:

1. Add 1–3 trigger phrases to the trigger-phrase table in
   `src/skills/skill-finder/SKILL.md`
2. Add a one-liner under the appropriate category in the by-category section
3. If no existing category fits, add a new one

This step is not optional — a skill that is not in skill-finder is
invisible to agents who do not already know its name.

## Gotchas

These are agent-specific failure modes you (the agent USING
skill-builder) will hit if you're not careful. Pause-and-self-check
items.

- **Skipping the interview and going straight to writing.** If the user
  says *"build me a skill for X"*, do NOT immediately produce a
  SKILL.md. Ask for 2-3 concrete use cases first, even if the user is
  impatient. A skill built without use cases is almost always too vague
  to trigger reliably and ends up rewritten.
- **Writing the description as narrative or including "Use when…".**
  The description must be a one-sentence imperative (verb-first, under
  200 characters). Trigger phrases ("Use when the user says X, Y, or
  Z") belong in skill-finder's trigger-phrase table (Step 9), NOT in
  the description field. "Use when…" in a description is a must-fix
  finding in skill-reviewer.
- **Padding Gotchas with general anti-patterns.** Gotchas is for
  agent-specific failure modes that recur across providers. If a pitfall
  applies to humans too, it belongs in Anti-patterns under Full
  reference, not Gotchas.
- **Defaulting Gotchas to "be careful" generalities.** *"Don't make
  mistakes"* teaches the agent nothing. Each Gotchas item must name a
  specific failure mode AND a specific countermeasure.
- **Forgetting the 1024-char description limit.** Anthropic's loader
  truncates descriptions over 1024 characters. Count characters before
  finalizing. If too long, trim by cutting the least-distinctive trigger
  phrases first, not the "what it does" part.
- **Using XML angle brackets in frontmatter.** Anthropic explicitly
  forbids `<` and `>` in any frontmatter field because the frontmatter
  lands in the system prompt and angle brackets could inject. Use them
  freely in body text where needed; never in frontmatter.
- **Naming a skill with "claude" or "anthropic" in the name.**
  Reserved by Anthropic. Use a neutral name even if your skill is
  Claude-specific (it shouldn't be — provider neutrality applies).
- **Putting the skill in the wrong category.** processkit's category
  taxonomy is fixed (`process`, `language`, `framework`, `infrastructure`,
  `architecture`, `design`, `data`, `ai`, `api`, `security`,
  `observability`, `database`, `performance`, `meta`). If the new skill
  doesn't fit, push back on the user — they're probably trying to build
  something out of scope, not invent a new category.
- **Inventing dependencies under `uses:` that don't exist.** Always
  query `index-management` first to confirm the skills you list under
  `uses:` actually exist. A `uses: [foo-thing]` entry pointing at a
  phantom skill makes the dependency graph invalid and silently breaks
  the agent's expectation that delegation will work.
- **Writing one giant skill instead of two focused ones.** If you find
  yourself writing "and also" or "plus" in the description, stop. Apply
  the one-sentence-one-skill rule and split.
- **Creating the skill folder before finalizing the design.** Don't
  write to disk during Steps 1-3. The folder should appear all at
  once after Step 6 passes — otherwise you end up with stranded
  half-finished skill folders that pollute the catalog.
- **Skipping the trigger-test step "because the description seems
  obvious".** If you can't write 3 positive and 3 negative test cases,
  the description is not as obvious as you think. The exercise of
  writing the negatives is what surfaces over-triggering risks.
- **Forgetting processkit commands use the `pk-` namespace.**
  Processkit command files must be named `pk-<workflow>.md`, not just
  `<workflow>.md`. Unprefixed names collide across skills once all
  commands land in `.claude/commands/`, and they do not trigger Codex
  skill shims consistently.
- **Writing logic into command adapter files.** The adapter's body is
  one sentence pointing at the skill and workflow. If you find yourself
  writing workflow steps in the adapter, move them to SKILL.md. The
  adapter is an invocation shim, not a skill.
- **Shipping an MCP server without tool annotations.** Every `@server.tool()`
  must carry explicit `readOnlyHint`, `destructiveHint`, `idempotentHint`,
  and `openWorldHint` annotations. Missing annotations are a must-fix in
  skill-reviewer. Default them conservatively: query tools get
  `readOnlyHint: true`; anything that overwrites state gets
  `destructiveHint: true`; HTTP-calling tools get `openWorldHint: true`.

## Full reference

### Asset: the SKILL.md template

`assets/skill-template.md` is a complete SKILL.md scaffold with TODO
markers in every section. Copy it as the starting point for any new
skill, then walk through Steps 1-7 to fill in each section.

### File system layout for the new skill

After running through all 7 steps, the new skill folder should look
like:

```
src/skills/<skill-name>/
  SKILL.md              ← required, the only file Claude reads automatically
  scripts/              ← always present (with .gitkeep), per processkit convention
  references/           ← only if SKILL.md > 5000 words and content was extracted
  assets/               ← only if the skill ships templates / icons / brand assets
  examples/             ← optional, recommended for skills with complex outputs
  commands/             ← only if metadata.processkit.commands is non-empty
    <skill>-<workflow>.md  ← one file per command; provider-specific adapter
  mcp/                  ← only if the skill ships an MCP server
```

Empty subdirectories (`scripts/`, especially) should still have a
`.gitkeep` so they survive the clone.

### Trigger phrase library

Common verbs that agents have learned to recognize as triggers:

| Skill type | Common trigger verbs |
|---|---|
| Creation | "create", "add", "make", "scaffold", "draft", "set up" |
| Review | "review", "check", "audit", "look at", "evaluate" |
| Query | "what's", "show me", "list", "find", "search" |
| Analysis | "analyze", "explain", "diagnose", "why", "investigate" |
| Decision | "should we", "compare", "trade-off", "pick", "choose" |
| Documentation | "document", "write up", "explain to others" |

When in doubt, prefer the user's actual words over a "cleaner" version.
The closer the description trigger matches what users naturally say,
the more reliably the skill loads.

### Description length budget

Anthropic's hard limit is 1024 characters, but the processkit
convention is stricter: **one-sentence imperative, under 200
characters**. Trigger phrases ("when the user says X") live in
skill-finder's trigger table, not the description. A good description
is 60-150 characters — short enough to skim in a catalog listing.
If you find yourself going over 200 characters, you are either
over-scoping the skill (split it) or smuggling trigger language
into the wrong field (move it to skill-finder Step 9).

### When to use skill-reviewer instead

If the task is reviewing or improving an EXISTING skill, use
`skill-reviewer` instead. skill-reviewer takes an existing SKILL.md
and runs the 5 Skill Killers + Anthropic troubleshooting playbook
against it, returning a report of what to fix. **skill-builder is for
greenfield; skill-reviewer is for brownfield.**

### Anti-patterns (general — humans + agents alike)

These are pitfalls that go wrong regardless of who is authoring:

- **Description-as-summary.** If the description reads like an "About"
  paragraph from a wiki, it's wrong. The description is a TRIGGER, not
  a summary.
- **Inventing categories.** Push back on the user about scope before
  inventing a new category — almost always the right answer is to fit
  into an existing one or to NOT build the skill.
- **Massive Full reference, empty Overview.** Overview is what the
  agent reads when it's actually doing work. Full reference is what the
  agent reads when something goes wrong. Don't put core workflow in
  Full reference.
- **Skipping the assets layer.** If the skill produces a structured
  artifact, ship the template under `assets/` so the agent fills it in
  instead of regenerating the structure each time.
- **Including a `README.md` inside the skill folder.** Anthropic's
  hard rule: no README.md inside a skill folder, including
  subdirectories. Documentation goes in SKILL.md or references/.
  MCP server documentation goes in `mcp/SERVER.md`, not
  `mcp/README.md`.
- **Omitting the commands mention from SKILL.md Overview.** If the skill has
  `commands/` adapter files, the Overview section must reference them so agents
  learn the commands exist from reading the skill — not only when the user
  happens to type the slash. One sentence per command is enough.

### Contributing improvements upstream

When you make a behavioral or content improvement to a file under
`context/` that was installed from processkit (it has a counterpart
in `context/templates/processkit/<version>/`), ask whether the
improvement is general enough to benefit all processkit consumers.

If yes:
1. Open a Discussion entity locally with `open_discussion` — title it
   "Upstream proposal: <short description>", note the changed file and
   the improvement in the body. This creates an audit trail so future
   sessions can see what was proposed and what was decided.
2. File an issue at the processkit repository so maintainers can
   consider it for the upstream catalog.

Nothing is mandatory — the project owner decides what to file
upstream. The Discussion entity records the decision either way.

### Cross-references

- `skill-reviewer` — for reviewing existing skills (brownfield)
- `index-management` — call before creating to avoid duplicates
- `event-log` — call after creating to log the new skill
- `src/skills/FORMAT.md` — the canonical format spec, always-current
  source of truth for frontmatter fields and conventions
- `src/skills/INDEX.md` — the catalog index, lists every shipped skill
