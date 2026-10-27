---
name: record-rule
description: Only when explicitly asked to record a rule, interview to clarify the note, reconcile org-wide or project-local guidance, and publish, activate, and verify it across configured agents.
disable-model-invocation: true
argument-hint: "<note, e.g. 'never use paid CI runners; always self-hosted'>"
---

# Record a rule

Take the user's note from wording to live behaviour: reconcile it with what
already exists, edit the canonical sources, land every changed repo on
`main`, refresh this machine, and prove each configured agent discovers the
result. A committed edit no agent loads is unfinished work.

Start only on an explicit request to record a rule. A quoted example or passive
remark is not authorization to publish changes or activate Home Manager.

Canonical sources: org policies and skills live in the `darkmatter/skills`
checkout, org adhere rules in `darkmatter/standards`, project rules in the
invoking project's own repo. Installed copies (e.g. under `~/.omp`) are build
output — always edit the source checkout, never the install.

## 1. Capture scope and interview

Record the note verbatim, its intended behaviour, and the invoking project's
identity (root, remote, name). Keep targeting that project if the cwd moves.

If scope is not explicit, ask only **Org-wide** (every darkmatter repo/agent)
or **Project-local** (this project only), then wait for the answer.
"Never"/"always" does not imply org scope.

Then interview if ambiguity or missing detail could change when the rule applies
or does not, exceptions, terms, or requirements vs preferences; use examples and
counterexamples. Resolve repository facts yourself. Batch related user decisions
and follow up until material gaps are settled; skip extra questions for clear notes.
When asking, wait for the user's actual reply; never simulate answers or approval.
If interaction is unavailable, show the open questions and stop before edits.
Restate agreed intent and boundaries before editing; do not invent the user's intent.

Done when: note, scope, project identity, intent and boundaries are recorded and settled.

## 2. Inventory what already governs this

Read indexes before bodies, in the scope's repos:

- Org-wide: every `skills/*/SKILL.md` name + description and
  `docs/catalog.md` in darkmatter/skills; then relevant bodies and their
  reference files, `docs/agents/*`, `docs/adr/*`, and installed preset guidance
  (agents, commands, instructions, contexts) discovered from the client config.
  Include standards `.adhere/rules/<topic>/<id>/RULE.md` and `RULE.ts` sources;
  trace generated exports to their authoring inputs.
- Project-local: the project's `AGENTS.md` chain, its own agent-context and
  policy directories, its local skills, and its `.adhere/rules/`. Discover
  the directory spelling the project actually uses (`.agent/`, `.agents/`,
  …) and confirm from its config (flake, agent config, docs) which paths
  its agents actually load — follow that convention; never assume one.
- Where inventory overlaps both scopes (an org rule already covers a
  project-local note, or vice versa), read both.

Done when: every existing policy, skill, ADR, and rule touching the note's
behaviour is listed with its location.

## 3. Reconcile

Compare the note against the inventory: duplicates, contradictions,
exceptions, and guidance the note makes obsolete. Then state a compact
decision per affected artifact — edit, merge, remove, retain, or no-op —
each with a one-line reason. Three decisions always need an explicit reason:
**no-op** (note already fully in force), **skip adhere** (nothing
file-checkable), and **new skill** (no existing home fits).

Reconciliation bounds:

- Remove or merge only in-scope text the note supersedes; preserve unrelated
  content and decision history (ADRs keep their record; supersede, don't
  rewrite).
- Prefer editing a suitable existing skill over creating a new one.
- Org-wide content stays project-neutral; project specifics stay in the
  project. Never record secrets or secret-derived values.
- If inventory exposes a new ambiguity (including authority or policy
  tradeoffs), return to step 1's interview before choosing or editing.
  Otherwise decide from evidence and show the reason.

Done when: decisions cover step 2's inventory and all material ambiguities are resolved.

## 4. Route each piece to its home

Use the routing table in the darkmatter/skills `README.md` ("Where to put
what"); in short:

- **Unconditional rule** → the shortest possible always-on line:
  `docs/agents/<order>-<topic>.md` (org) or the project's always-on instruction
  source (project-local). If instructions are generated, edit their composition
  inputs and regenerate, not the rendered block. An on-demand skill alone never
  carries an unconditional rule.
- **Reusable task/domain guidance** → edit the matching existing skill; a
  new `skills/<name>/SKILL.md` only when step 3 justified it, plus its
  `docs/catalog.md` row (org skills only). Validate any org skill you create
  or edit with `scripts/validate-skill.sh skills/<name>`.
- **A decision future contributors would re-litigate** → an ADR only where
  that repo's ADR convention exists and the note warrants it.
- Reuse existing policies, skills, and validators by reference. Create no
  scripts, automation, or always-on headers unless the note itself requires
  that mechanism.

## 5. Adhere rules for enforceable content

Add or update an adhere rule only for note content an automated judge can
check against files (code, config, workflow YAML…). Operational preferences
with no file surface stay prose — say "skip adhere" with that reason instead
of inventing a fake lint.

- Org-wide: author in `darkmatter/standards` at
  `.adhere/rules/<topic>/<id>/RULE.md`. Project-local: author in the
  project's own `.adhere/rules/` layout as discovered in step 2.
- Follow the adhere authoring contract as documented there (`RULE.md`
  frontmatter, must/never vs should wording, good/bad examples, stated
  scope); mirror a neighbouring rule's shape. Run that repo's `adhere
  validate` so contradictions with sibling rules surface before landing.
- Rules installed from standards are **owned copies** in each consumer repo.
  Landing a standards change does not update consumers, and `adhere install
  --force` overwrites local edits — never run it blind. For each consumer
  that must change: diff its copy first, preserve or explicitly supersede
  local edits, and treat the consumer update as its own repo change in step 6.

## 6. Land, activate, and verify — required final phase

Follow [reference/rollout.md](reference/rollout.md) for publication and
distribution of every changed repo: landing on `main` through each repo's
normal protection and review gates (preserving any unrelated user work in
those checkouts), refreshing local sources, the targeted Home Manager
input-lock update, activation, and fresh-session discovery proof in every
configured agent. Repeat inputs create no duplicate skill/rule or empty source
commit, but still run rollout steps 3–5 and repair stale distribution. A no-op
means the note is already in force in both canonical sources and live consumers.

This skill is not done at edit, commit, branch, or `main` alone. It is done
when rollout.md's completion criteria hold for every repo this run touched.

## Report

End with exact evidence, no inferred success:

- The note, its scope, and the step-3 decisions (changed / removed /
  retained, with reasons, including any no-op or skip-adhere).
- Per repo: files changed and the resulting `main` SHA.
- Activation result and, per configured agent, the fresh-discovery evidence
  from rollout.md — or the concrete blocker for that agent.
- Scope limits stated plainly: already-running sessions keep their loaded
  context; claim reload only where a fresh session proved it.
