---
name: fireworks-open-eli5
description: Create evidence-aware, interactive visual explainers as self-contained offline HTML. Use when a user asks to explain a concept, repository module, engineering tradeoff, or incident with a diagram, walkthrough, ELI5 treatment, data/request trace, failure view, or teach-back. Do not use for a plain short answer, ordinary prose rewrite, generic website implementation, or unsupported claims presented as facts.
license: Apache-2.0
compatibility: Codex, Claude Code, or another Agent Skills-compatible host with Node.js 18+ and local file access; no npm packages or network access required at render time. Native Pages export optionally requires macOS and Apple Pages.
---

# Fireworks Open ELI5

Turn a difficult system into a truthful visual story. Produce a portable JSON
spec first, then a deterministic, self-contained HTML explainer.

## Non-negotiable boundary

- Evidence comes before visual polish. Label every evidence item `verified`,
  `inferred`, or `analogy`.
- Never make an analogy look like implementation truth.
- A generated local HTML file is only `generated`. It is not `published`,
  uploaded, sent, or destination-verified.
- Do not publish, upload, send, or change access without the user's explicit
  request and the destination workflow's own verification.
- Rendering performs no network calls. A cited URL is a reader-facing link, not
  a runtime dependency. The optional native Pages action may call only the
  bundled same-origin helper on `127.0.0.1`; it must never contact a remote
  service.
- Browser-local history, favorites, and annotations are disabled until the
  reader opts in. They are convenience state, not evidence and never modify the
  source spec or generated artifact.
- Describe history precisely as same-origin explainers previously opened in
  that browser. Never claim that it enumerates every generated file.
- PDF export invokes the browser print dialog. PNG exports one scene; PPTX and
  Pages-compatible DOCX export one scene per slide or page. Native `.pages`
  output is allowed only after the installed Pages app really saves it; never
  rename a DOCX to `.pages`. Generated downloads are local artifacts only.

## Workflow

1. Identify the audience, question, language, and one thing that should travel
   through the story: a request, packet, decision, event, or user action.
2. Choose exactly one story grammar:
   - `concept`: intuition → mechanism → boundary.
   - `module`: entry point → transformations → outputs/dependencies.
   - `tradeoff`: shared goal → competing options → consequences/decision rule.
   - `incident`: normal path → break and propagation → detection/recovery.
3. Gather evidence. For repository work, inspect actual files and use local
   paths. For external claims, use authoritative sources when available. Record
   uncertainty explicitly.
4. Create a version 1 JSON spec following
   [references/spec-contract.md](references/spec-contract.md). Use 3–7 scenes,
   2–6 nodes per scene, a complete truth ladder, trace, glossary, teach-back,
   evidence map, and the required mode-specific `modeData`. Add failure
   information to consequential nodes.
5. Validate before rendering:

   ```bash
   node scripts/validate.mjs path/to/spec.json
   ```

6. Render to a new local file:

   ```bash
   node scripts/render.mjs path/to/spec.json path/to/explainer.html
   ```

   The renderer refuses an existing path. Only when the user explicitly wants
   to replace a known regular file, append `--force`. Forced rendering uses an
   atomic replacement and still refuses symbolic links and non-file paths.

7. Validate the spec and artifact together:

   ```bash
   node scripts/validate.mjs path/to/spec.json path/to/explainer.html
   ```

8. When browser access is available, inspect the local artifact at desktop
   width and 390px. Confirm one `h1`, readable labels, no horizontal overflow,
   keyboard focus, independent tablists, global and scene-local playback,
   viewport following, active real-edge and evidence-card synchronization,
   enter/hold/exit animation phases, failure lens, answer reveals, and zero
   remote resource requests. Every scene evidence card must expose its status,
   concise core basis, support scope, and a URL or explicit no-locator boundary.
9. Exercise the reader workspace: open and dismiss the modal drawer by mouse
   and keyboard; confirm focus return; enable the library intentionally; reload
   and verify favorites and a plain-text annotation; and confirm history
   contains only same-origin explainers that were actually opened. Use a
   markup-shaped annotation to verify it stays inert text.
10. Exercise export: confirm the print stylesheet, PNG signature and dimensions,
    PPTX and DOCX ZIP signatures and required OOXML parts, and the fallback
    download link when automatic downloads are suppressed. Visually confirm
    that scene artwork includes a bounded evidence footer with status, core
    basis, and source locator or boundary. When native Pages is in scope, run
    through `scripts/serve.mjs`, verify the `.pages` package contains
    `Index/Document.iwa`, then reopen it in Pages. Fix the spec or template and
    rerun both validators after any change.

## Report language

- Write the final QA, status, handoff, and generated-artifact report in the
  language of the user's latest substantive request by default.
- An explicit report-language request overrides that default.
- `spec.language` controls the generated explainer interface only; it does not
  force the conversation report language.
- In mixed-language conversations, ignore short acknowledgements when choosing
  the report language. Preserve code, commands, paths, identifiers, exact
  errors, and source titles when translation would reduce precision.

Read [references/reporting.md](references/reporting.md) for the full language
selection and delivery-report contract.

## Story construction rules

- Write the title as a concrete promise, not a category label.
- Keep the summary to one sentence and every node to one responsibility.
- Prefer 3–5 scenes. Use 6–7 only when omitting a stage would distort causality.
- Edges are relationships or actions. Use short verbs on labels.
- The trace must visit real node IDs in a meaningful order.
- Use failure data only when impact, visible symptom, and fallback are known.
- Keep the simple layer accurate enough to survive the technical layer.
- Put limitations in `truthLadder.caveat`, not in tiny disclaimers.
- Use source IDs on the scenes or nodes they support.
- Do not cite a source merely because it is adjacent to the claim.

Read [references/story-grammars.md](references/story-grammars.md) for mode
patterns, [references/evidence-rules.md](references/evidence-rules.md) for
claim boundaries, and [references/visual-system.md](references/visual-system.md)
before changing the renderer's visual language. Read
[references/library-and-export.md](references/library-and-export.md) before
changing persistence, navigation, playback, or export behavior.

## Quality gate

The work is ready as a local artifact only when:

- the validator returns `ok: true` for the spec and rendered HTML;
- all IDs and references resolve;
- every required interactive section has content;
- the selected story mode passes its own semantic contract;
- the HTML is deterministic and carries the spec SHA-256 meta tag;
- the artifact byte-matches the supplied spec and uses trusted CSP hashes;
- the artifact has no external resources, unsafe runtime APIs, or remote fonts;
- persisted reader state is opt-in, namespaced, bounded, same-origin, and kept
  outside the deterministic spec hash;
- annotations are rendered only as text and cannot create executable markup;
- global and local playback share one state machine and never run together;
- each trace step activates the real outgoing relationship path (or a sink's
  incoming path), keeps label and arrow state aligned, and highlights only the
  evidence that supports that step;
- scene evidence cards preserve verified/inferred/analogy boundaries and expose
  core text plus an actionable locator without fetching remote previews;
- scene PNG, PPTX, and DOCX packages have the expected signatures and
  structure and contain their evidence footer; a claimed native Pages export
  has also reopened in Pages;
- mobile uses the stacked flow rather than shrinking the desktop SVG;
- the final report follows the user's current interaction language, names the
  generated spec and HTML paths, and says whether desktop, mobile, persistence,
  playback, evidence, and export browser QA were run.

If evidence is incomplete, generate only when the evidence map and caveat make
the gap unmistakable. Otherwise stop and report the missing evidence.
