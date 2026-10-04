---
allowed-tools: Read Write Edit Bash
description: Build scientific presentations and speaker notes. Use when turning research results into a talk or conference deck.
license: MIT license
metadata:
    github-path: skills/scientific-slides
    github-pinned: v2.65.0
    github-ref: refs/tags/v2.65.0
    github-repo: https://github.com/K-Dense-AI/scientific-agent-skills
    github-tree-sha: 2f01dda0a53313e13131f8f04c4d0877fc33115e
    openclaw:
        envVars:
            - description: OpenRouter API key for optional image-generation steps.
              name: OPENROUTER_API_KEY
              required: false
        primaryEnv: OPENROUTER_API_KEY
    skill-author: K-Dense Inc.
    version: "1.7"
name: scientific-slides
---
# Scientific Slides

Create a talk the audience can follow: a clear question, interpretable evidence, and
conclusions proportional to the results. Slides support the speaker; notes support
spoken explanation. Neither is a record of the agent's production process.

## Start with the requested deliverable

- Establish audience, duration, key message, and required format from the available
  context. Ask only for missing decisions that block useful work.
- When revising an existing deck or writing notes, work from that deck and its source
  material. Do not restart literature research or rebuild slides unless needed.
- Use supplied results, figures, and references first. Search literature when a claim
  needs support, context is missing, or the user requests it. There is no paper quota.
- Use only supplied or confirmed author, affiliation, funding, and contact details.
- Keep confidential material local unless external processing is authorized.

## Content and speaker notes

- Give each slide one main message supported by the relevant evidence. Explain what
  was done, what the audience should notice, and why it matters; omit parts that add
  nothing on that slide. Use natural transitions rather than identical page templates.
- Write notes as speakable prose at the audience's technical level. Explain symbols,
  comparisons, and important numbers where needed to understand the result. Use complete
  words and concrete actions in Chinese; preserve English code identifiers. Follow the
  user's wording preferences. Do not repeat the slide text word for word.
- State results and their conditions directly. Avoid rhetorical reversals, imagined
  objections, and definitions followed by unrelated denials. Compare real quantities
  when the slide requires a comparison. Begin each explanation with its content and
  avoid routine opening previews or closing recaps. Keep a requested conclusion slide
  or a conclusion needed by the talk's structure.
- Incorporate corrections into the current account. Do not narrate earlier errors,
  assert that instructions were followed, or repeatedly defend against claims nobody
  in the audience has heard.
- Preserve distinctions that affect interpretation: simulation versus experiment,
  measured versus inferred results, metric definitions and denominators, quantization,
  evaluation conditions, and unequal optimization budgets. State shared conditions
  once near their first use; repeat only when a later comparison needs them.
- Bound conclusions directly: describe the best result within the tested conditions,
  rather than repeatedly denying global optimality. Do not suppress a real limitation
  just to make the talk sound confident.
- On a sequence of figures, explain shared color scales or preprocessing once, then
  focus on each figure's result. Mention rendering choices only when they affect what
  the audience can infer. Avoid repeated export, preview, or repair commentary.
- Keep citations with the claims or figures they support. Put detailed local paths,
  JSON field mappings, per-slide provenance, and validation logs in separate reference
  material only when useful or requested, not in the spoken script. Code/path details
  belong in the talk when reproducibility or implementation is itself the topic.

## Build only what is needed

For new decks, outline the argument and timing before choosing layouts. Prefer real
research figures and editable text. Use clear labels, readable equations, accessible
contrast, and enough whitespace. A text-only slide is acceptable when it serves the
message; decoration and image counts are not goals.

Choose the format from the task and existing project:

- **PowerPoint**: use an available PPTX workflow when editability or a template matters.
- **Beamer**: use `references/beamer_guide.md` for mathematical or LaTeX-based decks.
- **Image-generated slides**: optional, not the default for scientific results. Read
  `references/prompt_writing.md` and `references/script_reference.md` before using
  `scripts/generate_slide_image.py`. Check credentials and external-transfer permission.
  Keep formatting consistent, supply real citations, and verify generated text visually.
  Do not use generative redrawing as the authoritative rendering of quantitative data.

Existing figures must preserve their data, labels, axes, units, and provenance. Use
schematics to explain concepts, clearly distinguished from observations or results.

## Review and delivery

- Check agreement among slides, notes, and source results: values, units, terminology,
  captions, citations, and scope of conclusions. Resolve unsupported additions.
- Read notes aloud or estimate timing honestly; do not claim a rehearsal you did not do.
- For a rendered deck, inspect slide images for clipping, overlap, contrast, and
  legibility. Use `references/visual_review_workflow.md` and bundled rendering scripts
  when applicable. Writing notes alone does not require rebuilding the deck.
- Read once as an audience member unfamiliar with the editing conversation. Remove
  production commentary and repetitive qualifications; preserve scientific caveats.
- **Audience-view check:** every slide and spoken note should explain the research or its
  interpretation, not defend the production process or state a paper's relationship to a
  source. Put a scientific condition beside the result it qualifies: for example,
  “Measured in one clinic; transfer to other settings is untested.” Do not add a
  “not a reproduction” panel. Retain real model boundaries, user-requested comparisons,
  formal limitations, and required disclosures. Editorial questions belong in native
  document comments, never speaker notes, captions, or footnotes; if comments are
  unavailable, put them in the conversation outside the deck.
- Deliver the requested files or text. Speaker notes, captions, and slide footers are
  audience content, not places for operating instructions. Omit routine check reports
  and self-scores; include a review report only when requested.

## Read on demand

- Planning and stages: `references/presentation_workflow.md`
- Talk structure and duration: `references/presentation_structure.md`,
  `references/talk_types_guide.md`, `assets/timing_guidelines.md`
- Layout and accessible figures: `references/slide_design_principles.md`,
  `references/data_visualization_slides.md`
- PowerPoint styling: `assets/powerpoint_design_guide.md`
- Beamer starting points: `assets/beamer_template_conference.tex`,
  `assets/beamer_template_seminar.tex`, `assets/beamer_template_defense.tex`
- Common problems: `references/common_pitfalls.md`

Detailed references provide implementation examples, not universal quotas for visuals,
words, citations, or practice runs. Use this entrypoint's scope and output boundaries
when adapting them to the requested task.
