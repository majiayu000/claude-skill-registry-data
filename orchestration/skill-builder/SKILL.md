---
name: skill-builder
description: "Multi-agent research-and-curation pipeline that builds or refreshes a technology skill for the domain-expert marketplace. The invoking session becomes a pure orchestrator: parallel Sonnet research agents WebFetch official documentation into a source-cited corpus under research/<skill>/, a gap audit closes coverage holes, then a single Opus curator distills the corpus into the skill (200–500 line SKILL.md, trigger-tuned frontmatter description, at least one references/ file, scripts/ when they earn it, per-section source URLs and fetch dates), and deterministic validation plus trigger-eval updates finish the release. WHEN: \"build a skill for X\", \"create a new skill\", \"add <technology> to the <domain> plugin\", \"deep research X and turn it into a skill\", \"refresh the <skill> skill for the new version\". Do NOT use for creating subagents in .claude/agents/ (agent-creator), for Agent Skills format questions detached from this marketplace (ai plugin's agent-skills), for updating installed plugin versions (update-plugin), or for whole-plugin architecture — strategizing which skills/agents/hooks a plugin ships or remodeling a skills repo into plugins (plugin-builder)."
license: MIT
---

# Skill Builder — Research Team Orchestration

This skill turns a technology, technique, or product into a marketplace-quality skill through a two-stage division of labor: a team of parallel Sonnet-class research agents builds a source-cited corpus on disk, and one Opus-class curator reads that corpus and writes the skill. Research runs can take hours; the design below exists so the parent session survives them.

**When this skill is invoked, you stop being an implementer and become an orchestrator.** Your sole duty is to scope the work, spawn and steer agents, track their manifests, and integrate the result. Every byte of research payload lives on disk, not in your context.

## The Orchestrator Contract

These rules are what keep a multi-hour research session from drowning the parent context. Violating them defeats the purpose of the pipeline.

- **Never research in the parent session.** No WebSearch, no WebFetch. If you catch yourself about to fetch a page, spawn an agent instead.
- **Never read corpus artifacts, drafted references, or fetched pages.** The only corpus files you touch are `BRIEF.md` and `INDEX.md` — both of which you write. Everything else is agent territory.
- **Every agent has a return contract measured in lines.** The payload goes to disk; the return value is a manifest. An agent that returns its findings inline instead of writing them has failed its contract — tell it so via SendMessage.
- **Run long agents in the background** (the default). You are re-invoked when they complete; never poll, never sleep-wait.
- **Steer, don't respawn.** A running or completed agent keeps its context — use SendMessage for follow-ups, corrections, and "also cover X" requests instead of launching a fresh agent that must re-read everything.
- **Launch independent agents in one message** so they run concurrently. Researchers on different dimensions never depend on each other.
- **Report progress in short status lines**, not summaries of findings. The user reads findings in the finished skill, not in your play-by-play.

Model assignment: researchers and auditors run `model: sonnet`; the curator runs `model: opus` (the strongest reasoning model the harness offers); mechanical checks (line counts, file listing, source extraction) run `model: haiku` or plain shell commands.

## Pipeline at a Glance

| Phase | Who | Model | Runs | Returns to orchestrator |
|---|---|---|---|---|
| 0. Scope | Orchestrator | — | inline | `BRIEF.md` written |
| 1. Research fan-out | 3–8 researchers | sonnet | parallel, background | manifest ≤ 20 lines each |
| 2. Gap audit | 1 auditor | sonnet | background | gap list ≤ 30 lines |
| 1b. Gap fill | targeted researchers | sonnet | parallel, background | manifest ≤ 20 lines each |
| 3. Curation | 1 curator | opus | background | file tree + line counts + eval proposals ≤ 40 lines |
| 4. Verify + integrate | 1 verifier + orchestrator | sonnet / shell | background / inline | pass/fail + violations |

Full copy-paste prompt templates for every role are in `references/agent-prompts.md` — use them; they encode the return contracts and citation rules.

## Corpus Workspace

The corpus lives at `research/<skill-name>/` in the domain-expert repo checkout — `research/` is already gitignored as the intermediate-research workspace. If invoked outside the marketplace checkout, ask where the checkout lives; this pipeline only makes sense inside it. If `research/` is missing from `.gitignore`, add it before spawning anything.

```
research/<skill-name>/
├── BRIEF.md              ← scope: target plugin, dimensions, version range, overlap notes (Phase 0)
├── INDEX.md              ← manifest log: every researcher's return block, appended verbatim
├── <dimension>/*.md      ← research artifacts, each with per-section source citations
└── curation-notes.md     ← curator's decisions: what was cut, why, claims needing re-verification
```

The corpus is **retained after the skill ships** — it is the raw material for future refresh runs. Never delete it as cleanup. Artifact format and the INDEX entry schema are specified in `references/corpus-format.md`.

## Phase 0 — Scope

Resolve these before spawning anything, asking the user only for genuine scope decisions (target plugin, version range, paid-tier coverage):

1. **Skill name and home.** Folder name is the invocation name (`/database:postgresql`), so kebab-case, self-explanatory, named for the technology. Confirm which domain plugin owns it. New skill vs refresh of an existing one.
2. **Overlap survey.** Grep the other plugins' skills for the same technology (`duckdb`, `kafka`, `grafana`, `splunk`, `spark` all exist in multiple plugins with different angles). Every overlap found becomes a mandatory negative clause in the final description and a boundary note in the brief.
3. **Version range.** Which versions are in support and deserve `references/versions/<v>.md` treatment.
4. **Refresh inputs.** For an existing skill, the researchers' starting point is its `## Sources` footer — pass the skill path in the brief; do not read the skill yourself beyond confirming it exists.

Write all of it into `BRIEF.md`. Every subsequent agent receives the brief path as its first input.

## Phase 1 — Research Fan-Out

Spawn one Sonnet researcher per dimension, all in one message, all in background. Default dimension set — merge for small technologies (3–4 agents), split further for sprawling ones (per-version researchers):

| Dimension | Captures | Feeds |
|---|---|---|
| core-concepts | architecture, mental model, terminology, design decisions | SKILL.md body |
| official-reference | config surface, CLI/API, defaults, limits | references/ |
| versions | supported versions, changelogs, new/deprecated per version | references/versions/<v>.md |
| operations | install/deploy, tuning, observability, troubleshooting | references/, scripts/ |
| pitfalls | failure modes, anti-patterns, gotchas the docs bury | SKILL.md directives |
| security | hardening, authn/z, secrets, advisory process | SKILL.md + references/ |
| ecosystem | integrations, adjacent tooling, where this tech stops | description NOT-clauses |

**Researcher rules** (the full prompt is in `references/agent-prompts.md`; these are the load-bearing ones):

- **WebSearch is for discovering URLs only. Every captured fact must come from a WebFetch of the actual page.** Never cite a page you did not fetch; never paraphrase from a search snippet. If a fetch redirects, record the final URL that actually served the content.
- Prefer official documentation, then vendor engineering blogs, then high-quality community sources — and record which tier each source is.
- Every artifact carries `> Source: <url>` at each section and ends with `## Sources` + `Fetched: <YYYY-MM-DD>`. Uncited content is treated as nonexistent by the curator.
- Write artifacts under `research/<skill>/<dimension>/`; return only the manifest block: files written with one-line content notes, source count, coverage claims, explicit gaps. ≤ 20 lines.

Append each returned manifest to `INDEX.md` verbatim as it arrives. That file — not your memory — is the record of what the corpus contains.

## Phase 2 — Gap Audit

When the fan-out completes, spawn one Sonnet auditor to read `BRIEF.md` plus the entire corpus and return only: missing dimensions, conflicts between artifacts, uncited sections, and sources that look stale or unofficial. ≤ 30 lines.

For each real gap, spawn a targeted researcher (same rules as Phase 1). For each reported conflict, SendMessage the original researcher to re-fetch and resolve. Loop audit → fill until the auditor reports clean or the remaining gaps are explicitly declared out of scope in `BRIEF.md`. Do not let "mostly covered" through — the curator cannot invent what the corpus lacks.

## Phase 3 — Curation

Spawn exactly **one** Opus curator with the brief, the index, and the corpus path. It reads everything; you read nothing. Its output is the skill directory itself. The standards it must hit:

**Frontmatter.** `name` (= folder name), `description`, `license: MIT`. The description is the trigger surface — it loads into every session's system context whether or not the skill fires, so every clause pays cache rent:

- Structure: WHAT the skill covers (dense noun phrases, no marketing adjectives) + WHEN to use it (quoted trigger terms a user would actually type) + a **Do NOT use** clause naming each overlapping skill from the Phase 0 survey and where to go instead.
- Budget: repo median is ~530 characters, p90 ~890. Stay under ~900 unless overlap disambiguation genuinely demands more; treat 1,500 as the ceiling. One paragraph, no line breaks.
- The description sells the *routing decision*, not the technology. "PostgreSQL technology expert covering ALL versions … WHEN: 'psql', 'VACUUM', 'pg_stat' …" triggers; "comprehensive guide to the world's most advanced open-source database" does not.

**Body.** 200–500 lines is the target; 1,000 is a hard fail. Directives over essays ("Always X. Never Y." + one-line why). Outcomes and constraints over rigid step lists. No filler a competent agent would already know. A routing table near the top pointing each request type at the right `references/` file — depth lives there, loaded on demand, never in the body.

**Bundled content.** At least one `references/` file, always. Version-specific knowledge goes in `references/versions/<v>.md` — never a nested skill or sub-SKILL.md. Add `scripts/` when a runnable diagnostic or worked example beats prose (deterministic beats descriptive); `assets/` for templates the skill emits. Start from `assets/skill-template.md`.

**Source traceability — equal in priority to the content itself.** Every reference file: `> Source:` per section, `## Sources` + `Fetched:` footer. SKILL.md itself ends with `## Sources` and the fetch date. These links are the entry point for every future refresh run; a skill without them is a dead end that must be re-researched from scratch.

Curator return contract: file tree with per-file line counts, description character count, one proposed positive and one near-miss negative trigger-eval prompt, and any claims it flagged as needing verification. ≤ 40 lines. The curator also writes `curation-notes.md` into the corpus recording what it cut and why.

## Phase 4 — Verify and Integrate

1. **Deterministic audit:** run `scripts/audit_skill.py <skill-dir>` — it checks frontmatter fields, name/folder match, line counts, description budget, references presence, nested-SKILL.md violations, and Sources/Fetched footers. Fix failures before proceeding; warnings need a reason to ignore.
2. **Claim spot-check:** spawn a Sonnet verifier that samples ~10 factual claims from the new SKILL.md and traces each back to a corpus artifact and its source URL. Any untraceable claim goes back to the curator via SendMessage. This is the anti-hallucination gate.
3. **Trigger evals:** add the curator's positive and near-miss prompts to the plugin's `evals/trigger-evals.json`.
4. **Release mechanics:** bump the plugin's `version` in `plugin.json` (users never receive unbumped updates), then `claude plugin validate .` and `claude plugin validate ./plugins/<domain>`.
5. **Report:** skill path, SKILL.md line count, reference/script inventory, source count, and the corpus location kept for future refreshes. Findings live in the skill; keep the report to logistics.

## Refreshing an Existing Skill

Same pipeline, narrower fan-out:

- Researchers start from the existing skill's `## Sources` URLs — re-fetch every one, diff reality against the current skill content, and separately hunt for versions and features newer than the recorded `Fetched:` date.
- The curator patches rather than rewrites: preserve the description unless coverage genuinely changed (trigger evals and users' muscle memory depend on its stability), update version references, refresh every `Fetched:` date it re-verified.
- If a source URL is dead, the researcher finds the successor page and records the replacement in the artifact — future refreshes inherit the fix.

## Failure Handling

| Failure | Response |
|---|---|
| Agent returns findings inline instead of a manifest | SendMessage it: write the payload to the corpus, return the manifest. Do not paste its output into `INDEX.md` — that is the context bloat this pipeline exists to prevent. |
| WebFetch blocked or paywalled on a key source | Researcher records the URL with `UNFETCHED:` and finds the nearest fetchable official mirror (docs repo on GitHub, archived copy). Never cite the blocked page as if read. |
| A background researcher dies or stalls | Respawn just that dimension; the corpus and `INDEX.md` show exactly what is missing. Never restart the whole fan-out. |
| Curator output overruns budgets | SendMessage it the audit failures — it has full context to cut. Cutting is its job; do not edit the skill in the parent session beyond mechanical fixes. |
| Verifier finds untraceable claims | Back to the curator: trace it, cut it, or spawn a researcher to source it. An unsourced directive never ships. |
| Two researchers claim contradictory facts | The gap audit surfaces it; resolution is a re-fetch by one researcher, recorded as a `CONFLICT:` entry — not a judgment call made in the parent session. |

## Worked Example

"Build a skill for Valkey in the database plugin" — a compact trace:

1. **Scope:** overlap grep finds `database:redis` and `messaging:redis-streams` → brief mandates NOT-clauses for both and pins the angle to Valkey-specific divergence. Version range 7.2/8.x. `BRIEF.md` written.
2. **Fan-out:** five Sonnet researchers spawned in one message (core-concepts, official-reference merged with versions, operations, pitfalls+security merged, ecosystem), all background. Five manifests land in `INDEX.md` over the next hours.
3. **Audit:** auditor reports one gap (8.1 release notes unfetched) and one conflict (default eviction policy). One gap-fill researcher spawned; original researcher re-fetches the conflict.
4. **Curation:** one Opus curator writes `plugins/database/skills/valkey/` — SKILL.md 340 lines, description 780 chars with both NOT-clauses, `references/versions/{7.2,8.0,8.1}.md`, one diagnostics script. Returns file tree + two eval prompts.
5. **Verify + integrate:** `audit_skill.py` clean; claim verifier traces 10/10; eval cases added; database plugin version bumped; `claude plugin validate` passes. Corpus retained at `research/valkey/`.

Parent-session context consumed across the entire multi-hour run: the brief, ~7 manifests, one audit report, one curator return, one verifier return — a few hundred lines total.

## Managing Hours-Long Runs

- Background agents re-invoke you on completion — between notifications there is nothing to do and nothing to poll.
- Keep a compact status table (dimension → agent → state) in your progress updates so the user can gauge the run at a glance.
- If the session is interrupted, the corpus and `INDEX.md` survive on disk: a new session resumes by reading `BRIEF.md` + `INDEX.md` and spawning only what is missing. This is why manifests go to disk immediately, not at the end.
- Never fabricate or predict a pending agent's results. If the user asks before a notification arrives, say it is still running.

## Bundled Content

- `references/agent-prompts.md` — full prompt templates: researcher, gap auditor, curator, claim verifier. Read before spawning each role.
- `references/corpus-format.md` — corpus layout, INDEX.md entry schema, artifact citation format.
- `scripts/audit_skill.py` — deterministic skill audit; run in Phase 4 and after any manual edit to a generated skill.
- `assets/skill-template.md` — the SKILL.md skeleton the curator starts from.
