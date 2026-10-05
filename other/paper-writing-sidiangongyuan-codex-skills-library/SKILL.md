---
name: paper-writing
description: Draft or restructure research-paper sections, refine local prose, and audit manuscript-wide consistency. Use for evidence-grounded academic writing and revision, not independent acceptance-risk review or official rebuttal management.
license: MIT
---

# Paper Writing

Make the paper's purpose, contribution, use, and evidence easy to follow. Adapt
the writing to the actual paper rather than fitting it to a method-paper template.

## Choose the scope before the workflow

- **Section writing:** draft or restructure the requested sections. Read their
  relevant guides below and identify the paper's main contribution before editing.
- **Local refinement:** read the target and its immediate context, then use
  [prose.md](references/prose.md). Preserve the settled story and verify affected
  links only. A caption correction does not require a new literature survey,
  contribution interview, full manuscript rewrite, or experiment run.
- **Whole-manuscript consistency:** read [consistency.md](references/consistency.md)
  and trace claims and terminology across the main text, visuals, and supplement.
  Use a section guide only where a concrete structural issue needs repair.

An assessment request authorizes diagnosis, not file changes. An explicit revision
request authorizes scoped edits and their normal verification. Missing experiments
are evidence gaps, not permission to launch jobs. Ask only when a decision changes
the scientific claim, scope, resources, or an external action; inspect existing
records first. Do not reopen settled choices without a concrete contradiction.

## Establish the argument

For structural work, identify from the draft and evidence:

- the reader's question and the paper's primary contribution;
- what the resource, method, or analysis enables, and how it is actually used;
- which evidence supports each principal claim, and what remains untested;
- the role of reference implementations, auxiliary supervision, and controls.

Keep this working map compact; it need not become a new document. For a benchmark
paper, lead with the resource and what its use demonstrates, not a compulsory
model invention. For a method paper, connect the problem to the tested design.
For a system paper, connect requirements and interfaces to end-to-end evidence.
For an analysis paper, connect the question and measurement to the finding.
Hybrid papers may combine roles without forcing every component into an equal
contribution. Do not invent a new name or mechanism to create a narrative turn.

## Read only the relevant guidance

- Abstract or Introduction: [front-matter.md](references/front-matter.md).
- Dataset/benchmark design and its use: [benchmark.md](references/benchmark.md).
- Related Work and positioning: [related-work.md](references/related-work.md).
- Method, formulation, and implementation exposition: [method.md](references/method.md).
- Experiments, tables, and result captions: [experiments.md](references/experiments.md).
- Conclusion, limitations, and supplement: [closing-material.md](references/closing-material.md).
- Sentence-level clarity and transitions: [prose.md](references/prose.md).
- Cross-section verification and rendered checks: [consistency.md](references/consistency.md).

## Evidence and scope boundaries

Preserve verified results and references. Do not fabricate support, silently change
evaluation populations, or turn pending cells into findings. Narrow unsupported
claims or identify the missing evidence. Fluent phrasing cannot repair a false
premise. A complete system's gain does not isolate a component's causal effect.

Focus is not concealment: secondary observations need not interrupt every headline,
but conditions that change the validity of a comparison must remain clear where
the claim is interpreted. Primary metrics, auxiliary tasks, statistical analyses,
page budgets, and punctuation preferences are project or venue decisions, not
universal rules. Do not automatically require or forbid additional experiments.

When uncertain citations or factual claims affect the requested edit, verify them
with primary sources; use `research-evidence` if available. Reuse still-applicable
verification rather than restarting a full search. Borrow an exemplar's rhetorical
function only after reading the relevant passage, not its unverified scientific
claims or alleged venue authority.

Separate the manuscript-ready replacement from the explanation to the author.
An evidence gap may need an editorial note without becoming a disclaimer inside
every revised sentence. Do not insert pending-run status into finished result prose.

## Result prose and tone

- Lead result paragraphs, abstracts, and conclusions with the supported main
  finding, contribution, or scientific implication. Let the paragraph land on
  that result rather than on a secondary cost that the reader can already inspect
  in a complete table.
- Let a table carry secondary metrics and tradeoffs when it gives the metric,
  unit, direction or interpretation, comparison scope, and necessary conditions
  clearly. A short table pointer is enough; do not repeat a visible value merely
  to make the prose sound balanced.
- Keep a condition in prose when omitting it would change the interpretation of
  fairness, applicability, or the central claim. State it once in the setup,
  caption, result discussion, or limitations section where it matters, instead of
  attaching it as a defensive final clause to every positive result.
- Prefer direct declarative language to defensive framing such as “we
  acknowledge,” “it should be noted,” or a pre-emptive concession. “But,”
  “however,” and “although” remain available when they express a real logical
  dependency; do not use them to manufacture a negative ending after a supported
  finding.
- For example, replace “Our method improves AP, but uses more memory” with
  “Our method improves AP under the matched setting (Table X).” If memory
  changes deployment feasibility or comparison validity, state that condition
  plainly where the reader needs it rather than hiding it or repeating it as a
  rhetorical concession.
- The same rule applies to Chinese prose: replace “性能更好，但显存更高” with
  “在评测设置下，该方法取得更高性能（表 X）” when the table already reports
  memory. State the memory boundary separately when it changes the deployment
  claim or comparison validity.

## Finish and hand off

Check that the changed text answers its intended reader question, follows from
the preceding passage, and matches the evidence. Validate affected references and
rendering in proportion to the edit. Stop when the requested criteria are met;
leave already clear and accurate passages alone. Report substantive changes,
remaining evidence gaps, and checks actually performed, not invented readiness.

Independent acceptance-risk assessment belongs to `paper-review-panel`; official
review responses to `rebuttal-response-skills`; new experiment design to
`experiment-planner`. Use those skills only when the task needs them. For actual
figure/table design or layout work, use `paper-visual-craft`, with
`paper-framework-figure-studio-pro` for framework planning. Caption wording alone
does not require redesigning a figure. None of these optional handoffs is a
mandatory writing pipeline.
