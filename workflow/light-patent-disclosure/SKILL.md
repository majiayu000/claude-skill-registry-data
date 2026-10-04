---
name: light-patent-disclosure
description: >-
  Prepare evidence-backed patent invention disclosure materials for attorney or
  patent-agent review. Use when the user asks for 专利点挖掘, 技术交底书, 现有技术/查新记录,
  claim/patent-point support mapping, invention disclosure drafts, patent figures,
  or a handoff package for a software/research/project invention. This is an
  off-DAG engineering/IP handoff skill: it does not provide legal advice, does
  not submit filings, does not guarantee novelty, grant, allowance, validity or
  registration, and emits no Light research findings or back-edges.
---

# Patent disclosure handoff

Turn a real project or research result into an attorney-reviewable invention
disclosure packet: what problem is solved, what technical means solve it, why
it differs from nearby work, what embodiments support the breadth, what figures
are needed, and what counsel still needs to decide.

Read
[`references/patent-resource-map.md`](references/patent-resource-map.md)
before jurisdiction- or filing-sensitive work. It records the peer skills,
official sources, borrowed mechanisms and honest boundaries.
Read
[`references/patent-interview-and-search.md`](references/patent-interview-and-search.md)
before patent-point mining, public search, claim-ladder drafting or attorney
handoff. It contains the detailed interview, search and QC rules.

## Non-negotiable boundaries

1. This skill is not legal advice and never certifies `READY_TO_FILE`.
   Deliver only `DRAFT`, `NEEDS_USER_INPUT`, or `READY_FOR_ATTORNEY_REVIEW`.
2. Do not guarantee grant, novelty, inventive step, non-infringement, validity,
   ownership, freedom to operate, or registration outcome.
3. Preserve uncertainty. If a search, date, assignee, inventor, public
   disclosure, foreign-filing rule, or priority fact is not verified, write
   `UNKNOWN`, `PLANNED`, or `UNAVAILABLE` with the next check.
4. Evidence comes from real artifacts: repository files, design docs, lab notes,
   papers, experiment logs, issue discussions or user-supplied records. Keep
   relative locators and SHA-256. Do not invent implementation details.
5. Patent figures must be programmatic/vector/manual sources such as Mermaid,
   Graphviz, PlantUML or SVG. Do not use AI-generated bitmap images for patent
   drawings.
6. Keep the skill off the research DAG. It has no stage, no `STAGE_GATES`, no
   `ROUTES`, no `light.findings.v1`, and no scientific back-edge.

## Workflow

### 1. Intake the decision facts and risk triage

Ask for or mark `UNKNOWN`:

- jurisdiction and intended route: CN invention/utility model, US provisional,
  US nonprovisional, PCT, EP, or undecided;
- owner/applicant, inventors/contributors, employment or sponsor constraints;
- public disclosures, papers, demos, GitHub releases, sales, thesis defense,
  posters, standards submissions, and their dates;
- deadline, prior filings, priority claim, secrecy/export/confidentiality risk;
- whether a licensed attorney or patent agent will review the output.

Record `risk_triage` for public disclosure, ownership/inventorship,
foreign-filing/secrecy and trade-secret redaction. Stop for the user when a
public disclosure, ownership dispute, foreign filing strategy, secrecy review,
or filing deadline could change the next action.

### 2. Build the evidence packet

Scan only files placed in scope. For each source artifact record:

- `id`, relative `path`, `sha256`, freshness/date if known;
- what claim element or embodiment it supports;
- whether private or third-party confidential content must be redacted before
  sharing with outside counsel.

If the source is a paper, product demo, notebook, API contract, dataset or
diagram, bind the exact locator. Do not let chat memory become evidence.

### 3. Mine patent points with problem-solution-effect discipline

For each candidate patent point, write:

- technical problem, not business desire;
- concrete technical means, algorithm, architecture, protocol, data structure,
  control loop, signal processing, model pipeline, hardware arrangement or UI
  interaction rule;
- technical effect and measurable advantage;
- distinguishing features versus the closest known work;
- fallback embodiments, alternatives, parameter ranges and failure cases;
- support artifact IDs for every feature.

Prefer one strong, defensible invention story over a pile of vague features.
Ask targeted questions for tacit knowledge that the repo cannot show.
Keep a short inventor interview log: problem, failed alternatives, key insight,
constraints, contributors, disclosure dates and known prior art.

### 4. Do prior-art / novelty-context work honestly

Search the relevant official or public sources available in the current
environment, then record:

- databases/pages searched, query strings, date, filters and failures;
- nearest results with locators and relationship to the invention;
- whether the search is `VERIFIED`, `PLANNED`, `UNKNOWN`, or `UNAVAILABLE`.

Keep `inventor_known_prior_art` separate from `prior_art`. The former is what
the team already knows; the latter is the agent-run public search log. A
verified public search records `searched_sources`; if non-patent literature is
not searched, write why.

Do not call this a legal novelty opinion. If search coverage is shallow, say
so and list the missing source or professional search still needed.

### 5. Build the claim ladder

Before drafting final sections, write a claim strategy:

- broadest defensible technical point;
- dependent/fallback positions and why each is narrower;
- enablement support summary: embodiments, variants, parameter ranges, edge
  cases and alternatives;
- artifact support for every strategy item.

If the broad point is unsupported, narrow it or mark it as counsel question.

### 6. Draft the disclosure for counsel

Use a plain, editable structure:

1. title and technical field;
2. background and nearest known approaches;
3. technical problem;
4. summary of the technical solution;
5. beneficial technical effects;
6. figure list and programmatic figure sources;
7. detailed embodiments, variants and fallback implementations;
8. draft patent points or draft claims with element-level support;
9. novelty/difference table;
10. open questions for attorney or patent agent review.

Claims are only drafts for review. Keep terminology consistent with the
description and avoid over-broad elements unsupported by artifacts.

### 7. Run the machine gate before delivery

Create a packet following
[`templates/patent-disclosure-packet.example.json`](templates/patent-disclosure-packet.example.json),
then run:

```bash
python scripts/disclosure_gate.py --packet patent-disclosure-packet.json --base <project-root> --as-of 2026-07-05
python scripts/disclosure_gate.py --selftest
```

The gate must pass before saying the packet is ready for attorney review. It
checks risk triage, inventor-known prior art, public search coverage, claim
ladder, support mapping, figure source, QC flags and anti-overclaim language.
A failed gate means fix the packet, lower the claim, or mark the missing fact.

## ACT / ASK / NEVER

ACT:

- bind every invention feature and draft claim element to source artifacts;
- use official/current sources for jurisdiction-specific requirements;
- produce counsel-facing open questions, not hidden assumptions;
- generate figures as Mermaid/Graphviz/PlantUML/SVG or other auditable vector
  sources;
- record prior-art search limits instead of pretending completeness.

ASK:

- jurisdiction and filing route;
- whether public disclosure has already happened and when;
- ownership/inventor facts that are not in the repository;
- whether to redact trade secrets before outside review;
- whether a risky broad claim should be narrowed or left as counsel question.

NEVER:

- submit, file, sign, pay fees, or interact with patent offices on the user's
  behalf;
- promise grant/allowance/registration, novelty, inventive step or FTO;
- turn generated pictures into patent drawings;
- infer inventorship, ownership, disclosure dates or legal status from code
  alone;
- route this skill into the Light research DAG.
