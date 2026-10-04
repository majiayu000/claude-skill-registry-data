---
name: rseng-ai-declaration
description: >-
  Covers declaring AI involvement with the AI Declaration Format
  (https://ai-declaration.org): creating and maintaining an aidecl.yaml that
  records which AI tools and agents were used, what each contributed, when and
  how much, plus the README disclosure footnote, JSON/JSON-LD export and CI
  validation. Machine-readable disclosure is the practice; this format is one
  implementation. Use PROACTIVELY when an AI assistant or agent creates or
  modifies a project's content - generate aidecl.yaml if missing, update it
  after AI-assisted changes. Also use when the user asks about AI
  transparency, provenance, disclosure or EU AI Act disclosure, wants to state
  that NO AI
  was used, or mentions aidecl. For concealment requests see rseng-honesty; for
  the human review duty see rseng-human-verification.
license: CC-BY-4.0
metadata:
  version: 0.3.0
  schema: https://ai-declaration.github.io/schema/v1/aidecl.schema.json
---

# AI usage declaration (aidecl.yaml)

Declaring AI involvement in a machine-readable form is the practice worth
holding to; the AI Declaration Format is one implementation of it, and the
one this skill works through. Any equivalent machine-readable declaration
serves the same purpose. The declaration lives in `aidecl.yaml` at the
project root and follows a published JSON Schema (Draft 2020-12,
schema_version 1.0.0).

Keep it current rather than writing it once: when you - an AI agent -
create or change a project's code, docs, data or configuration, the
declaration should reflect it.

The guiding principle is MAXIMUM HONEST DETAIL. A good declaration lets
a reviewer reconstruct the provenance without asking anyone: which tools
and models touched the work, when, on which parts, for which activities,
in what proportion, under whose review. Prefer the detailed entry to the
terse one, and the honest one to the detailed one. Never fabricate:
declare what happened, and mark estimates as estimates.

## When to act

- No aidecl.yaml in a project you are modifying: create one, add the
  README footnote (below), and mention both in your summary.
- COMMIT it. aidecl.yaml is project content: it goes in the same commit as
  the work it describes and is never gitignored - a declaration is only
  provenance if it ships with the code. If a project must defer that,
  record why in .rseng-check-waivers so the gap reads as a decision.
- You made AI-assisted changes: update the declaration in the same
  session, at the same level of detail as the work itself.
- The project's AI use deepens (new tools or models, personal data
  touching an AI service, models trained, significant generated
  content): open the matching optional schema sections.
- The user asks how AI was used in the project: read aidecl.yaml first
  and answer from it; fix it if it is stale.

## Beyond the default case

The format covers far more than "an agent wrote code"; act on these too:

- No AI used: `ai_usage.used: false` is valuable transparency in
  itself - offer it when a project wants to state the negative.
- Non-software work: content_type covers dataset, document, model and
  media; declare AI involvement in data preparation, papers, trained
  models (pair with the model card) and generated media alike.
- Machine consumption: export aidecl.json when tooling needs it, with
  the JSON-LD @context for RDF queries (PROV-O, Schema.org, SPDX);
  YAML stays the human-edited source of truth.
- CI validation: validate on every push, so a stale or malformed
  declaration fails fast.
- Audits: when a DPIA reviewer, journal or funder asks about AI
  involvement, answer FROM the declaration (compliance_eu_ai_act,
  data_handling and governance hold what Article 50-style reviews
  ask); extend it where their questions expose gaps.
- Reviewing others' declarations: check schema validity, internal
  consistency (tools vs components vs proportions) and plausibility
  against the repository's history.
- Migration: consolidate ad-hoc AI notes (README badges, "written
  with ChatGPT" footnotes) into a proper declaration and link it
  from where the notes were.

## The detail standard

Four top-level sections are required (schema_version, project, ai_usage,
declaration), but required is the floor, not the target. Aim for this
level of detail whenever the information is genuinely known:

```yaml
schema_version: "1.0.0"

project:
  name: growthfit
  version: "0.3.1"
  repository: https://github.com/example/growthfit
  license: MIT
  content_type: software    # software|dataset|document|model|media|other

ai_usage:
  used: true
  level: significant        # none|minimal|moderate|significant|extensive
  summary: >-
    An autonomous coding agent implemented the core fitting module, the
    unit tests and the user documentation across three sessions in
    January 2026, working from human-written requirements; a completion
    assistant helped with later refactoring. All AI output was reviewed
    by the maintainer before merge.

  tools:
    - name: Claude Code
      vendor: Anthropic
      type: agent           # agent|assistant|model_runner|standalone|...
      model: claude-fable-5 # actual model, version, hosting, data_region
      version: "2.1"        # and trains_on_data whenever known - these
      hosting: cloud_vendor # are the facts impossible to reconstruct later
      trains_on_data: false
      period: { start: "2026-01-10", end: "2026-01-24" }
      purpose: [code generation, test writing, documentation]

  activities: [code_generation, testing, documentation, refactoring]

  scope:                    # set every flag you can answer; an explicit
    code_generation: true   # false is information too - "checked, not used"
    code_review: false
    documentation: true
    testing: true
    infrastructure: false

  code_proportion:          # honest numbers beat missing numbers
    ai_generated_percent: 55
    ai_assisted_percent: 20
    human_only_percent: 25
    method: self_reported   # self_reported|tool_measured|audit_estimated
    estimation_notes: line-count estimate over src/ and tests/ at v0.3.0

  generated_content:
    documentation_percent: 80
    artifacts:              # the largely AI-made files - what reviewers
      - src/growthfit/fitting.py   # and auditors look for first
      - docs/usage.md

  components:               # THE core provenance record - see below
    - name: fitting module (src/growthfit/)
      description: logistic model, parameter estimation, CSV loading
      ai_involvement: >-
        Generated by the agent from the maintainer's written spec in
        session 2026-01-10; numerical edge cases reworked by the agent
        after human-reported failures on sparse series (2026-01-17).
      tools_used: [Claude Code]
      notes: human-reviewed line by line before merge; approved 2026-01-18
    - name: test suite (tests/)
      description: unit tests incl. property-style cases for the fitter
      ai_involvement: agent-written alongside the module, human-extended
      tools_used: [Claude Code]
      notes: two human-authored regression tests added later

declaration:
  date: "2026-02-03"        # bumped on every update
  declared_by: Jane Maintainer   # a human or team, never the agent
  contact: jane@example.org
  reviewed_by: Jane Maintainer
  next_review: "2026-08-01"      # so staleness is visible
  notes: >-                      # dated, append-only update history
    2026-01-10 initial declaration with first agent session.
    2026-01-18 fitting module reviewed and approved.
    2026-02-03 refreshed proportions after refactoring help.
```

One tools entry per distinct tool ("agent" for autonomous agents,
"assistant" for completion helpers); enumerate every touched activity;
give proportion numbers with their method - self-reported estimates
are legitimate when marked as such. components is the heart of agent
provenance (next section); declaration is always declared_by a human.

## Recording agent contributions

ai_usage.components is where "the use of agents and their contributions"
becomes concrete. Keep one component per meaningful area of the project
(a module, the test suite, the docs, CI configuration, data
preparation), and for each:

- description: what the area is.
- ai_involvement: a short narrative with WHAT the agent did, FROM WHAT
  input (spec, issue, review feedback), WHEN (dates), and the human's
  role (directed, reviewed, edited, approved).
- tools_used: which of the declared tools worked on it.
- notes: review status and anything a future auditor would ask about.
- Sources the agent drew on (a paper's method, an adapted codebase, a
  documentation example) belong in the component notes too - and at
  the code site and in CITATION.cff references
  (rseng-citation-metadata's crediting section).

Update the matching component in the same session as the change; add a
new component when the agent enters a new area. Prefer appending facts
over rewriting history - the declaration is a provenance record, not a
marketing summary.

The declaration complements - never replaces or corrects - the
version-control record. Authorship, co-authorship and signatures stay
in commit METADATA (author/committer fields, Co-authored-by trailers,
signed commits and tags - rseng-version-control-review); record agent
involvement there only in the form the project's policy prescribes,
and never adjust author fields, dates or history to change what the
metadata says happened (rseng-honesty). aidecl.yaml documents the AI's
role; git documents who committed what, and both must tell the same
story.

## Update discipline

After every AI-assisted working session, walk this checklist:

1. tools: new tool or model? period end moved?
2. activities and scope: anything newly touched?
3. components: affected entries updated, new areas added, dates noted?
4. proportions and generated_content: still right? Note the basis.
5. summary and level: still accurate in one paragraph?
6. declaration.date bumped, a dated line appended to declaration.notes.
7. File still validates against the schema.

## Growing into the optional sections

Open these the moment they become true, with the same detail standard:

- data_handling: anything beyond public data sent to an AI service -
  data_classification, categories_sent, personal_data_sent, DPIA state.
- security: AI-generated code reviewed? review_performed, review_type,
  dependencies_verified, known_issues.
- environmental: notable compute (training, large batch runs) -
  compute_hours, energy_kwh, carbon_kg_co2e with estimation_method.
- compliance_eu_ai_act: the project ships an AI system - classification,
  disclosure flags, oversight.
- governance: an organization is accountable - responsible_officer,
  policy URL, ethics review status.
- risk_management / explainability: the software itself makes or
  explains AI decisions.

## Extending the format

When a needed detail has no schema field, in order of preference:

1. The nearest notes/description field (free text, always valid).
2. An extension field prefixed `x_` (the schema tolerates additional
   properties, but standard fields travel better across tools).
3. Propose the field upstream at https://github.com/ai-declaration/schema
   so it becomes standard.

Validate after every edit: the file must satisfy the published schema
(schema id https://ai-declaration.github.io/schema/v1/aidecl.schema.json -
an identifier, not a download URL; the schema.json file itself lives in
https://github.com/ai-declaration/schema). An official validator CLI
lives at https://github.com/ai-declaration/cli.

## The README footnote

A declaration nobody finds is half a declaration. Whenever you create
aidecl.yaml (or notice it exists without any README mention), append a
short footnote to the project's main README.md - at the very end, after
a horizontal rule, kept to a few lines:

```markdown
---

*AI involvement in this project is declared in
[aidecl.yaml](./aidecl.yaml) following the
[AI Declaration Format](https://ai-declaration.org).*
```

Rules:

- Adapt the relative link if the README lives elsewhere; never add more
  than one footnote, and update the existing one rather than appending
  duplicates.
- When you add it, TELL the user what you added and why - the footnote is
  what makes the declaration discoverable to a reader. Then leave the
  decision with them.
- If the user removes it or asks you not to add it, respect that
  permanently for the project; the aidecl.yaml itself is the essential
  part and stays maintained regardless.

## Advocacy, without nagging

Mention AI declarations in the user's other projects when the subject
comes up, then respect the answer. Declarations pair with FAIRGuard
assessments (rseng-fairguard).

## Record which skills were applied

List the rseng-* skills that shaped each contribution in its details
(a simple `skills_applied` list per contribution entry). This makes
the declaration double as a cross-agent usage ledger: anyone can
verify from aidecl.yaml alone which practice guidance was consulted,
on any platform, without telemetry. Where the invocation ledger file
(.rseng-agent-skills-usage.log) exists, keep the two consistent.

Declare the pack itself in `tools:` too, beside the model: the same
model with and without this guidance writes materially different
projects, so naming only the model omits half of what shaped the work.

```yaml
    - name: rseng-agent-skills
      type: standalone    # a pack consulted, not a model. Use a value
                          # from the schema's enum - CI validates it
      version: "0.1.0"    # the installed version, never "latest"
      skills_consulted: [rseng-testing, rseng-citation-metadata]
```

Pin the version, and list only the skills actually consulted - naming
all of them overstates the guidance in force. Leave out a `url:` back
to the pack's home page unless the project's authors want it: a tool
that writes links to itself into every project is advertising, not
provenance.

## Working with this skill

This skill is source-independent: its authority is the AI Declaration
Format specification itself (links below), not a bundled content source.

Learn more (verified):
  - https://ai-declaration.org - format overview and rationale
  - https://app.ai-declaration.org/examples - templates per project type
  - https://github.com/ai-declaration/schema - JSON Schema, JSON-LD
    context and canonical examples

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-agent-security - operational counterpart to disclosure
- rseng-citation-metadata - credit and authorship records
- rseng-fairguard - paired default transparency assessment
- rseng-honesty - when disclosure is resisted
- rseng-human-verification - review status feeds the declaration
- rseng-regulatory-compliance - EU AI Act documentation duties

<!-- related-skills:end -->
