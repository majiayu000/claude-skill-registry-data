---
name: rite-explain
description: User-invoked explainer that teaches one concept, diff, idea, or recent-work recap with an optional retrieval check-in.
argument-hint: "[a concept | a diff ref | an idea | \"what did I do this week?\"], or bare to be asked"
user-invocable: true
disable-model-invocation: true
---
<!-- loads: {"always":["rite-explain/reference/intake.md"],"triggers":{"repo":["devrites-lib/reference/standards/tooling.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md"],"style":["devrites-lib/reference/standards/prose-style.md"],"principles":["devrites-lib/reference/standards/principles.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --skill rite-explain` (no workspace: `--out <path>`) bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.

# /rite-explain: the human half of the learning loop

Agent-driven development removed the learning that writing code by hand used to give the
developer. When the agent writes the code, the human stops absorbing the codebase. `/rite-explain`
is the replacement: it teaches the developer **one** thing well (a concept, a change, an idea, or
a window of their own recent work) so they keep learning while the agents do the writing. For a
specific change, it can instead write a **walkthrough**: a human review guide organized by concern,
risk stops, and manual observations.

This is the **complement of [`/rite-learn`](../rite-learn/SKILL.md)**, and the two together are
the whole compounding story. `/rite-learn` teaches the **repo**. It promotes recurring lessons
into rules and principles the next feature reads. `/rite-explain` teaches the **person**: the
mental model the next feature needs a human to hold. A team that only runs `/rite-learn`
compounds a codebase whose own maintainers understand it less each week. Run both.

Read-only against source. It reads artifacts and code; it writes exactly one explainer file to
`.devrites/explainers/` and never edits source, specs, or rules.

## Who the explainer is for

The developer, personally. Dense, technical, one voice: no audience adaptation, no "for
beginners" softening, no executive summary. It is a display artifact: no embedded quizzes or
widgets: the check-in (below) happens live in the session, where an answer can be
graded. If the user asked for prep for a meeting or a teammate, it preps **them** to explain the
thing; it does not produce the deck.

## Workflow

### 1. Classify the input: load the intake reference

The four input shapes (concept · diff · idea · work-recap) each ground and compose differently,
and each drives a different check-in. Diff inputs also branch into explainer vs walkthrough
composition. Getting the shape wrong wastes the whole artifact.

**Load [`reference/intake.md`](reference/intake.md) now**. It owns the classification rules, the
`diff:` / `since:` / `output:` token table, the concept-vs-diff tiebreak, and the check-in
mechanics per shape. Do not improvise classification from this file; the detail lives there so this
one stays legible, and skipping it means guessing the shape.

**Bare invocation** (no input): ask **one** blocking question (`AskUserQuestion` when the harness
has it, else the harness's blocking-question tool: `request_user_input` on Codex; no interactive
question tool → render the ranked options as a plain numbered list and end the turn
(afk-hitl.md)). "What should I
explain?": offering "a recap of my recent work in this repo" as a shortcut option alongside free
text. Never emit a default explainer unprompted.

### 2. Ground

Match grounding to the shape (full rules in the intake reference). DevRites gives you grounding for
free: prefer it over re-deriving:

- A **diff** or **recap** → the workspace and archive: `seal.md`, `evidence.md`, `decisions.md`,
  `traceability.md`, the shipped `.devrites/archive/<slug>/`, and `git log` / `git diff`.
- A **concept** with footprint in this repo → live code through the primary index selected by
  [`tooling.md`](../devrites-lib/reference/standards/tooling.md) (one named-predicate cross-check only when needed), plus any
  `.devrites/principles.md` or ADRs that already take a position on it.
- An **idea** or a concept with no repo footprint → the user's framing plus, only if it sharpens
  the teaching, current external sources (weight by date).

Create the run directory before composing so the durable artifact has a home:

```bash
RUN_DIR=".devrites/explainers/$(date +%Y%m%d)-<slug>"; mkdir -p "$RUN_DIR"
```

### 3. Compose the explainer

For diff inputs that ask for `walkthrough:<ref>`, "checkpoint", "walk me through", or human review,
write `$RUN_DIR/walkthrough.md` using the walkthrough composition in `reference/intake.md`, then skip
the active-recall check-in unless the user asks for teaching too.

Otherwise write one dense artifact at `$RUN_DIR/explainer.md`. It must **teach**, not summarize:

1. **One thing.** A single clear takeaway named in the first two lines. If the input sprawls,
   teach the highest-leverage slice and say what you cut.
   **Completion:** the first two lines state one takeaway and any deferred topics.
2. **Build the model, don't list facts.** Start from what the developer already knows in *this*
   codebase and move to the new thing. Concrete before abstract: a real symbol, file, or line
   from the grounding beats a generic example every time.
   **Completion:** the explanation connects a known project anchor to the new model without a fact dump.
3. **Show the load-bearing detail.** Quote the actual diff hunk, the real function, the specific
   config, with `file:line` pointers so the developer can go read it.
4. **Visual where it earns it.** When the idea is spatial or relational (flows, before/after,
   architecture, comparable options) and a richer reviewable page would carry it faster than prose
   or an inline Mermaid sketch, treat this as a soft-required dual-read branch — not decoration and
   not a new lifecycle phase:
   1. Open matching playbooks via
      [`../devrites-lib/reference/visual-playbooks/index.md`](../devrites-lib/reference/visual-playbooks/index.md)
      first (progressive load; open every matching id; **never** preload all seven).
   2. Emit the pair under either the active workspace
      `.devrites/work/<slug>/visual/<name>.{html,outline.md}` **or** the explainers run dir with the
      same contract (`$RUN_DIR/visual/<name>.{html,outline.md}`). Copy required outline headings from
      [`outline-template.md`](../devrites-lib/reference/visual-playbooks/outline-template.md).
   3. Agents treat the outline as SSOT; if HTML and outline disagree, **outline wins** until both are
      regenerated. No Lavish runtime (`window.lavish.*`, `data-lavish-*`, poll/queue/share/ht-ml.app).
   4. In the reply, `Changed` / `Record` may cite the HTML+outline pair. Optionally tip the human to
      run `devrites-engine open-visual <path-or-name>` (document the tip only).
   Skip the branch when prose (or a tiny Mermaid/SVG sketch inside `explainer.md`) already carries
   the named relationship.
   **Completion:** matching playbooks loaded when taken; dual-read pair written with outline-wins /
   no-Lavish / no-new-phase; or the branch is explicitly skipped because prose won.
5. **Human voice.** Follow [`prose-style.md`](../devrites-lib/reference/standards/prose-style.md):
   no throat-clearing, no false-binary contrast, no marketing adjectives. One senior engineer
   explaining to another.

### 4. Offer the check-in (optional, active recall)

Retention comes from *retrieving*, not re-reading. After the explainer, offer one check-in via the
harness's blocking-question tool (`AskUserQuestion`, or `request_user_input` on Codex; no
interactive question tool → render the ranked options as a plain numbered list and end the turn
(afk-hitl.md)): the user
answers **first**, then you confirm or correct. The shape sets the
form (mechanics in the intake reference):

- **diff / recap** → **predict-then-reveal**: ask what a specific hunk changes or why a decision
  was made *before* showing the reveal.
- **concept / idea** → a **checked exercise**: one small problem the developer solves, then you
  grade it against the model you just taught.

Skippable when the material does not warrant retention work (a one-off, or the user declines). Do
not force it; offer once.

## Gotchas

- **Teach one thing.** An explainer that covers five things teaches none. Cut ruthlessly; queue the
  rest as "next time".
- **Ground it or don't claim it.** A concept explainer with no `file:line` or real example is a
  Wikipedia paragraph. If it has footprint in this repo, quote the repo.
- **Not a review.** `/rite-explain` never judges the code or files findings, that is `/rite-review`.
  It explains what *is*, adversarially neutral.
- **Not `/rite-learn`.** It writes to `.devrites/explainers/`, never to [`principles.md`](../devrites-lib/reference/standards/principles.md)
  or any rule file. Teaching the human is not promoting a repo rule.

## Output

```
Done: explained <the one thing> as a <concept|diff|idea|recap> explainer OR walked through <change> for human review.
Changed: .devrites/explainers/<date>-<slug>/<explainer.md|walkthrough.md>[; visual/<name>.html + visual/<name>.outline.md]
Evidence: grounded in <artifacts/files quoted>; check-in <offered+result | skipped>; walkthrough stops <count>; visual <pair|skipped>
Open: <none | next-time topics deferred | check-in awaiting the user>
Next: <single command — usually back to the calling phase, or /rite-learn if a repo rule surfaced; optional tip: devrites-engine open-visual …>
Record: .devrites/explainers/<date>-<slug>/explainer.md | walkthrough.md | visual/<name>.outline.md
↻ Hygiene: /clear after reading; the explainer is on disk
```
