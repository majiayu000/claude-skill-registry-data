---
name: sci-paper-reader
description: Read academic papers from primary sources to answer targeted mechanism or evidence questions, compare prior work, or produce deep Chinese/bilingual understanding packets and requested derivatives. Use when the user wants to understand, translate, teach, compare, or turn a paper into Markdown, HTML, Word, Obsidian, or presentation-ready material. Match reading depth to the question; keep reusable packets project-neutral and return candidate project relevance as a typed reading handback to sci-research-manager, never as project evidence or an experiment allocation.
---

# SCI Paper Reader

Explain the method and evidence at the depth requested. Assume the reader is intelligent but may be new to the topic; teach the necessary prerequisites without substituting an abstract paraphrase for primary-source reading.

## Choose reading depth before producing artifacts

- For one mechanism, result, or comparison question, read the decisive source sections and return an anchored answer with checked and unchecked scope. Do not automatically build a full packet, register a paper, launch remote work, or create an experiment.
- For a requested deep read or reusable teaching packet, apply the complete understanding workflow below. Produce visual or document derivatives only when requested.
- Reuse unchanged sources, identity checks, manifests, and instructions already loaded in this task. Ask tools for exact sections, figures/tables, or selected metadata; keep full text available without repeatedly loading it into context. Truncated or inaccessible sections remain explicitly unverified.
- When evidence conflicts, reopen the decisive source and protocol even if this costs more context. Never drop controls, contrary findings, or source verification to save tokens.

## Ground the source first

1. Verify paper identity, source status, and available PDF/HTML/arXiv/DOI.
2. Mark uncertain authors, venue, year, identifiers, code links, or metrics `needs_verification`.
3. Use page, section, figure, and table anchors for exact claims.
4. Do not let the current project lens distort the paper's own argument.
5. Never turn a paper claim into project evidence.

Use `sci-literature-manager` for discovery/indexing and `sci-research-manager` when the reading changes project direction.

## Build Markdown first

For a full packet, default to a Chinese `paper_understanding.md` unless the user specifies another language or format. Produce Markdown before requested HTML/PPT/Word/Obsidian derivatives so they follow the same evidence spine. A targeted answer does not require a durable packet.

For a durable library, prefer:

```text
<category>/<paper-slug>/
  paper.pdf
  paper_understanding_YYYYMMDD.md
  paper_visual_YYYYMMDD.html
  assets/
  README.md
```

Preserve original figure aspect ratios. Treat visual crops as evidence objects, not decoration.

## Load only the needed reference

- Read [novice_depth_standard.md](references/novice_depth_standard.md) for a full beginner-readable packet.
- Read [packet_schema.md](references/packet_schema.md) before building a complete Markdown packet.
- Read [evidence_spine.md](references/evidence_spine.md) when proof logic, figures, or cross-paper relations are unclear.
- Read [html_visual_guidelines.md](references/html_visual_guidelines.md) before producing visual HTML.
- Run `scripts/check_html_assets.py <html>` after creating HTML.

## Reconstruct the evidence spine

Build this before writing derivatives:

`problem -> claimed cause -> method principle -> proof objects -> result/ablation interpretation -> limitation -> relation to other work`

If this chain is unclear, do not design slides or experiments yet.

For a mechanism or nearest-prior comparison, identify the prediction/action/objective, training and deployment inputs, supervision, controls, selection rule, evaluation unit, and limits. Separate observed results from the authors' interpretation; inspect whether a simple or competing explanation remains. An information-access difference matters only if it changes feasible inputs or the estimand under fair controls. Similarity, a failed proxy, or one negative run limits the tested formulation, not every possible intervention; do not require a complete causal proof before proposing a small informative test.

## Produce the understanding packet

Cover:

1. Plain-language orientation and prerequisites.
2. Paper identity and source verification.
3. Why the problem exists and why prior methods are insufficient.
4. Core claim, assumed cause, and method principle.
5. Inputs, outputs, mechanism, training/supervision, and what is genuinely new versus inherited.
6. Figure/table reading cards: what is visible, how to read it, what comparison matters, what it supports, and what it cannot prove.
7. Main results, ablations/diagnostics, robustness/generalization, failure cases, and limitations.
8. Relation to predecessor, competitor, and follow-up papers.
9. Durable takeaways, common misunderstandings, and evidence boundaries.

When project relevance is requested, return a separate typed reading handback; a targeted question does not first require a reusable artifact. Do not append project state to the paper authority or its derivatives.

For full structure and field details, follow `references/packet_schema.md` rather than expanding this coordinator.

## Teach instead of naming

- Explain a term before relying on it.
- Use a small concrete example for abstract tasks or formulas.
- Unpack formulas symbol by symbol when they are central.
- Describe what the reader physically sees before interpreting a figure.
- State what baseline/row/column makes a result meaningful.
- Distinguish “the paper claims” from “the evidence supports”.
- Explain why each module exists and what would fail without it.

Do not compress away the reasoning ladder. “Concise” means remove repetition, not prerequisites, proof logic, limitations, or controls.

## Return project relevance to the research owner

When project relevance is in scope, return this separate handback to `sci-research-manager`:

```markdown
## Reading Handback

- Source ID/version and reading date:
- Source-grounded statements and exact locations:
- Paper protocol and evidence boundary:
- Candidate relevance (not yet adopted):
- Candidate hypotheses/diagnostics:
- Required controls and evidence boundary:
- Missing verification:
- Decisive sections actually read and material unchecked scope:
- Return to: `sci-research-manager`
```

This handback may inspire a hypothesis but cannot create a project tag, LiteratureClaim, direction decision, experiment ID, or project evidence. The reusable paper packet remains project-neutral.

## Hand experiment candidates back carefully

Do not send the reusable paper packet or candidate implications directly to `sci-experiment-manager`. Return a typed reading handback to `sci-research-manager`, which decides project adoption, verifies any project LiteratureClaim, and—only when a falsifiable requirement exists—creates the official literature-to-experiment brief before delegating card implementation.

Only when an experiment candidate is requested, the same handback may include the relevant fields below; do not create another document by default:

```markdown
## Candidate Experiment Implications

Sources and verification status:
Candidate hypothesis/theory:
Variables/cues:
Required controls:
Minimal validation:
Success criterion:
Failure criterion:
Confounds/risks:
Do-not-do-next:
Recommended stage:
```

Do not create project registry rows, configs, runs, experiment IDs/results, or experiment claims in this skill.

## Validate derivatives

- Ensure Markdown, HTML, slides, and Word outputs share one evidence spine.
- Verify every local visual asset exists and is non-empty.
- Preserve screenshot aspect ratio and readable resolution.
- Keep source and assistant-drawn diagrams visibly distinct.
- Recheck that figures/tables support the nearby explanation.
- Mark every unresolved source detail instead of inventing it.
