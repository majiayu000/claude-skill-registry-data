---
model_tier: inherit
name: "refine-ticket"
description: "Refine a Jira/Linear ticket before planning — 'refine ticket', 'tighten AC on PROJ-123', 'ist das Ticket klar?'; rewritten ticket, risks, persona voices, close-prompt."
personas:
  - developer
  - senior-engineer
  - product-owner
  - stakeholder
  - critical-challenger
  - ai-agent
domain: product
scope:
  write: []
  verification_reason: "execution.handler is internal, so this skill spawns no subprocess — writes happen through the agent's declared allowed_tools. No command can prove a scope the skill never executes."
execution:
  type: assisted
  handler: internal
  allowed_tools: []
workspaces:
  - product
packs:
  - product-basic
requires_skills:
  - validate-feature-fit
  - threat-modeling
trust:
  level: professional
install:
  removable: true
---

# Refine Ticket

> Move a ticket from "raw idea" to "implementation-ready" in one run.
> Produces a rewritten ticket, Top-5 risks, and persona voices.
> Orchestrates `validate-feature-fit` and `threat-modeling` as sub-skills
> — never duplicates their logic. Output is copy-paste ready; the user
> decides write-back.

## When to use

- The user hands over a Jira / Linear ticket key, URL, branch name, or
  pasted ticket text and asks for a sanity check before planning.
- A ticket looks too vague, too broad, or smells wrong.
- Before `/feature-plan` or `/feature-explore` on a ticket-anchored scope.
- The user says "tighten the AC", "poke holes in this ticket",
  "is this ready to plan?", "ist das Ticket klar genug?",
  "verbessere das Ticket".

## When NOT to use (near-misses)

| Phrasing | Route to |
|---|---|
| "plan this feature" | `/feature-plan` (downstream) |
| "estimate this ticket" | `/estimate-ticket` (sibling, Phase 4) |
| "is this a duplicate feature?" | `validate-feature-fit` (sub-skill) |
| "threat-model this change" | `threat-modeling` (sub-skill) |
| "investigate this bug" | `/bug-investigate` (bug-focused) |

`/refine-ticket` **orchestrates** these — it does not replace them.

## Language strategy

The refined output's prose language is picked once, up front, and
applied to every section (refined description, risks, persona voices,
orchestration notes, close-prompt). Fallback order — first hit wins:

1. **User-message language.** If the latest user message is in
   German, the entire output is German; if English, English; etc.
   This honours the global `language-and-tone` iron law.
2. **Ticket body language.** When the user's message is ambiguous
   (one-word `/refine-ticket PROJ-123`), mirror the language the
   ticket is written in — detected from the summary + description.
3. **`.agent-settings.yml` default.** If both are silent or unclear,
   fall back to the project default in `.agent-settings.yml`
   (`personal.language` or equivalent). If that is also missing,
   default to English.

Quoted identifiers (ticket keys, file paths, command names, code
snippets) stay in their native form. Only the prose mirrors the
selected language.

## Inputs (four equivalent paths)

Reuses the `jira-ticket` command's loader. Accepts:

1. **Ticket key** — `/refine-ticket PROJ-123`
2. **Branch detection** — `/refine-ticket` with no arg; regex
   `[A-Z]+-[0-9]+` against `git branch --show-current`
3. **Pasted text** — `/refine-ticket` followed by a markdown block
4. **URL** — `/refine-ticket https://acme.atlassian.net/browse/PROJ-123`

If none resolve to a ticket, fall back to conversational discovery
(`feature-explore`-style): ask one focused question, then continue.

## Procedure

### 1. Load ticket

Delegate to `jira-ticket` §1-3:
- Extract ticket ID (branch / URL / arg).
- Fetch via Jira API (`GET /issue/{id}`) — summary, description,
  issue type, priority, status, comments, linked issues.
- Scan description + comments for Sentry URLs; pull stacktrace /
  tags when present.

If pasted text: skip API, parse markdown, extract title + AC
bullets + body.

**Auto-fetch parent (Phase F4).** Before detection, check the
issue type and fold parent context in:

```ts
import { issuetype_needs_parent, fold_parent_context } from 'scripts/refine_ticket_detect.js';

if (issuetype_needs_parent(ticket.issuetype)) {
    const parentKey = ticket.parent_key;        // from `fields.parent.key`
    const parent = fetch_jira_issue(parentKey); // +1 API call
    ticketBody = fold_parent_context(ticketBody, parent.body, parentKey);
}
```

Rules:
- Applies to `Story` and `Sub-task` (and their Linear / Shortcut
  equivalents). `Task` / `Bug` / `Epic` skip the auto-fetch unless a
  `parent` link field is already populated — in that case the agent
  folds explicitly without the issuetype guard.
- `fold_parent_context()` is idempotent; folding twice with the same
  parent does not duplicate the block.
- When the parent fetch fails (404, permission, network), skip the
  fold and append a line to orchestration notes:
  *"Parent `<key>` not reachable — AC may lack upstream context."*

Parent AC lines surfaced this way must be cited verbatim in the
refined output's *Open questions* section so the user sees which
constraints come from the parent.

### 2. Inspect ticket + detect orchestration triggers

Check the loaded ticket for clarity signals before orchestrating:
- Does the summary match the description body?
- Are AC bullets concrete (observable / testable) or vague ("works well")?
- Is the scope one feature, or multiple tangled together?
- Any sentence that references an existing module name, feature flag, or domain concept?

**Cross-source discrepancy scan** (per [`cross-source-consistency`](../../rules/cross-source-consistency.md), gated by `consistency.cross_source`): the ticket is rarely a single source. Compare every source against the others and surface any conflict as an *Open question* — never resolve it silently:
- **text ↔ attachment** — does the ticket text agree with every attached mockup / screenshot / diagram? (Canonical miss: text says "birthdays **today**", the mockup shows a birthday from two days ago.) If an attachment cannot be read, say so — do not assume it agrees.
- **silent-but-needed** — is the spec silent on a clearly-needed behavior (weekend/holiday shift, empty state, error path, timezone, permissions)? Surface it and ask before it becomes an implementation assumption — an inferred behavior is a scope expansion, not a given.
- **intra-ticket** — do the AC, description, and comments contradict each other?

Fold every discrepancy into the refined output's *Open questions* section (one batched list), never a second prompt. Full taxonomy + scan procedure: [`cross-source-consistency-mechanics`](../../../docs/guidelines/agent-infra/cross-source-consistency-mechanics.md).

Then run the deterministic detection helper — do **not** re-derive trigger
logic in prose:

```bash
./agent-config refine-ticket:detect <ticket-body-file>
# or, inside the skill run (scripts/refine_ticket_detect.ts):
#   import { detect, load_map } from 'scripts/refine_ticket_detect.js';
#   const decision = detect(ticketBody, load_map(), process.cwd());
```

The helper consumes [`detection-map.yml`](detection-map.yml) (co-located
in this skill folder) and returns:

- `validate-feature-fit` — fires when ≥ 2 distinct feature-area keywords
  appear in the body (see `sub_skills.validate-feature-fit.keywords`).
- `threat-modeling` — fires on any auth / webhook / upload / queue /
  secret / tenant / admin / PII / payment keyword, or a `CVE-YYYY-N`
  regex match.
- `repo_aware` — on when `.git/`, `agents/settings/contexts/`, `composer.json`,
  or `package.json` is present in the cwd; off otherwise.
- When `repo_aware=True`, `decision.repo_context` is populated by
  `gather_repo_context()`:
  - `recent_branches` — up to 20 most recent local branches (naming
    convention signal).
  - `recent_commits` — up to 30 most recent commit subjects (active
    modules + verb conventions).
  - `context_docs` — every `agents/settings/contexts/*.md` filename (domain
    vocabulary).
- Outside a repo the context is empty — the skill produces the same
  output shape, minus repo-specific citations (graceful degrade).

Use `repo_context.recent_branches` to anchor the "Refined ticket" title
naming (e.g. `feat/` vs `fix/` vs `refactor/` prefix), and
`repo_context.context_docs` to cite domain vocabulary in the Top-5
risks instead of inventing terms.

The match lists and `require_count` thresholds are owned by
`detection-map.yml` — edit the map, not this skill (DE + EN fixtures,
repo-aware + graceful-degrade coverage are regression-locked in this
package's own test suite).

### 3. Orchestrate

For every `SubSkillDecision` with `fired=True`, invoke the named sub-skill
with the ticket body as input:

- `validate-feature-fit` → returns duplicate / scope-creep findings
- `threat-modeling` → returns trust boundaries + abuse cases

**Cite, don't copy** — the output references findings by sub-skill name and
file:line where applicable. If a sub-skill reports zero findings, emit
`fired → clean` in the orchestration section. Skipped sub-skills appear
as `skipped (no trigger match)` — never silently omitted.

Each fired finding must map to at least one entry in the Top-5 risks
section; orchestration that does not influence the risks is waste.

### 4. Apply personas

Load the persona set from frontmatter (Core-6 default). Each persona
reviews the ticket through its lens and produces one paragraph:

- **Developer** — implementability, unknowns, test seams
- **Senior Engineer** — architectural fit, blast radius, hidden deps
- **Product Owner** — value, user story integrity, AC completeness
- **Stakeholder** — deadline fit, business impact, comms plan
- **Critical Challenger** — devil's advocate; what's wrong with this?
- **AI Agent** — automation hooks, tool boundaries, clarity for agents

Optional: `--personas=+qa` adds the QA persona (edge cases, regression
risk, test matrix).

Optional: `--user-type=<id>` loads one user-type from `user-types/<id>.md`
and adds an end-user simulation lens to the persona stack (e.g.
`--user-type=galabau-field-crew`). User-types compose orthogonally with
personas — persona = methodology / role lens; user-type = end-user / field
lens. v1 is CLI-only (no skill-level default; no frontmatter list). The
user-type voice renders as one paragraph in *Persona voices* labelled
`**User: <label>**`, citing Daily Workflow, Vocabulary, Operational
Constraints, and Ticket Red Flags from the loaded user-type. Contract:
[`docs/contracts/user-type-schema.md`](../../../docs/contracts/user-type-schema.md).

### 5. Synthesize + close-prompt

Produce the three-section output (template below). After rendering,
emit the close-prompt (below). Do **not** write to Jira. Do **not**
open a planning doc.

## Output template

Frozen per Q25.

````markdown
## Refined ticket

**Title:** <rewritten title>

<rewritten description — tightened AC, explicit out-of-scope,
open questions surfaced>

## Top-5 risks

1. <risk> — <mitigation / deferral>
2. <risk> — <mitigation / deferral>
3. <risk> — <mitigation / deferral>
4. <risk> — <mitigation / deferral>
5. <risk> — <mitigation / deferral>

## Persona voices

- **Developer** — <one paragraph>
- **Senior Engineer** — <one paragraph>
- **Product Owner** — <one paragraph>
- **Stakeholder** — <one paragraph>
- **Critical Challenger** — <one paragraph>
- **AI Agent** — <one paragraph>
- **[qa]** — *(only when `--personas=+qa`)* <one paragraph>
- **User: <label>** — *(only when `--user-type=<id>`)* <one paragraph
  citing Daily Workflow / Vocabulary / Operational Constraints /
  Ticket Red Flags from the loaded user-type>

## Orchestration notes

- `validate-feature-fit` — <fired / skipped; key findings or "clean">
- `threat-modeling` — <fired / skipped; key findings or "clean">
- Repo-aware — <on / off; contexts loaded>
````

The "Refined ticket" section is wrapped in a **copyable Markdown box**
so the user can grab it verbatim.

## Self-review (3-scan checklist)

Run these three scans on the rendered output before the close-prompt. Each is a fast pass; failure blocks emission and forces a fix.

1. **Spec coverage** — every AC bullet and constraint from the original ticket (and every parent-AC line surfaced via `fold_parent_context`) is reflected in the rewritten ticket, the Top-5 risks, or the *Open questions* section. Nothing from the input vanishes silently.
2. **Placeholder / TODO scan** — no `<placeholder>`, `TODO`, `FIXME`, `tbd`, `???`, `XXX` strings remain. The angle-bracket placeholders in the template (`<rewritten title>`, `<risk>`, `<one paragraph>`) must be replaced with concrete prose before the close-prompt fires.
3. **Type / shape consistency** — every module, file, route, or domain term cited in the rewritten ticket and Top-5 risks matches `repo_context.context_docs` and `recent_branches` vocabulary. Invented terms are flagged in *Open questions* or replaced with the project's actual term.

Self-review is mechanical (gaps, leftovers, naming drift); persona voices and orchestration outputs handle reasoning critique. Both run; neither replaces the other.

Source: adapted from an external reference.

## Close-prompt (mandatory final step)

**Probe write access first (Phase F6).** Before rendering, do a
cheap upfront check:

```ts
import { render_close_prompt } from 'scripts/refine_ticket_detect.js';

let write: boolean | null;
try {
    const me = jira_get('/myself');                 // existence → auth works
    const meta = jira_get(`/issue/${key}/editmeta`); // fields → write access
    write = Boolean(meta.fields);
} catch {
    write = null;                                    // probe itself failed
}

console.log(render_close_prompt(write));
```

Behaviour:

| Probe result | Prompt shape |
|---|---|
| Write access present (`True`) | Full three-option prompt (comment / replace / nothing) |
| Read-only (`False`) | Single option: *"Copy-paste — no write access to this project"* |
| Probe failed (`None`) | Full three-option prompt; skill degrades to copy-paste on selection (v1 fallback) |

Per user interaction rules, accept number or free text. `editmeta`
is cheap and cacheable; cache the result per Jira project key for
the session, re-probe on project change.

## Rubric pass (optional, surfacing-only)

After refinement, run
[`judge-artifact-completeness`](../judge-artifact-completeness/SKILL.md)
with rubric `ticket-quality-score` to verify DoR readiness — acceptance
criteria, test plan, risk, and estimate. Invoke when the user asks for a
DoR check — not automatically on every refinement.

## Output format

1. **Refined ticket** section with rewritten title + description, wrapped in a copyable markdown block.
2. **Top-5 risks** as a numbered list, each item paired with a mitigation or deferral.
3. **Persona voices** — one paragraph per persona from the active set; no skipped personas without explicit reason.
4. **Orchestration notes** naming every sub-skill that fired or was skipped, with a one-line reason.
5. **Close-prompt** with exactly three numbered options (comment / replace / nothing); no fourth option in v1.

## Gotcha

- The model tends to invent risks that sound plausible but aren't anchored in the ticket text. Every risk in Top-5 must cite a phrase, AC bullet, or sub-skill finding — no hypotheticals.
- Persona voices degrade into generic platitudes when the ticket is already tight. If a persona has nothing real to flag, write one sentence stating that — do not pad.
- Sub-skills (`validate-feature-fit`, `threat-modeling`) cost tokens; orchestrate only when the trigger matrix actually matches, not defensively on every run.
- Branch-detection matches the first `[A-Z]+-[0-9]+` in the branch name; chained keys (e.g. `feat/PROJ-1-and-PROJ-2`) pick the first and note the rest.

## Do NOT

- Do NOT write back to Jira in v1 — output is copyable markdown; write-back is user-gated via the close-prompt.
- Do NOT chain into `/estimate-ticket` or `/feature-plan` automatically — separate invocations by design (Q5 decision).
- Do NOT duplicate logic from `validate-feature-fit` or `threat-modeling` — orchestrate by reference, cite findings, don't re-derive them.
- Do NOT skip the close-prompt, even when the ticket looks fine and the user seems eager to move on — the prompt is the contract.
- Do NOT emit persona voices outside the active set; if the user passed `--personas=+qa`, add QA, otherwise do not.
- Do NOT emit a user-type voice unless `--user-type=<id>` was passed; loading a user-type proactively (e.g. "this ticket smells like field-crew") is forbidden — the axis is CLI-only in v1.

## See also

- [`jira-ticket`](../../commands/jira-ticket.md) — ticket loader
- [`validate-feature-fit`](../validate-feature-fit/SKILL.md) — orchestrated sub-skill
- [`threat-modeling`](../threat-modeling/SKILL.md) — orchestrated sub-skill
- [`feature-explore`](../../commands/feature-explore.md) — upstream idea capture; hints at `/refine-ticket` when input looks like a ticket
- [`feature-plan`](../../commands/feature-plan.md) — downstream planning
- [`adversarial-review`](../adversarial-review/SKILL.md) — same `critical-challenger` persona, different stage (post-plan)
- [`artifact-drafting-protocol`](../../rules/artifact-drafting-protocol.md) — this skill was drafted under it
