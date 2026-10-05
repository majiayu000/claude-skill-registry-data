---
name: papertrace-deep-dive
description: Build or revise a bilingual, interactive PaperTrace explanation for a specific research paper. Use for paper deep-dives, formula walkthroughs, research connections, or paper-specific demos in this repository; do not use for ordinary literature summaries outside PaperTrace.
---

# PaperTrace Deep Dive

Create an explanation that helps a reader reconstruct the paper's argument and test its central mechanism, not merely read a longer abstract.

## Evidence boundary

- Read the primary paper before editing. Use its official project, code, supplement, or venue page when needed.
- Distinguish the paper's reported result, your derivation, and your interpretation.
- Never invent benchmark values, ablations, citations, architecture details, or implementation behavior. Mark an unresolved fact `[VERIFY]` until checked.
- Preserve known limitations, evaluation conditions, and negative results. A vendor or author claim remains labeled until independently reproduced.

## Build the smallest complete learning path

1. Identify the reader's prerequisite and the single question the page should answer.
2. Write the paper's claim as input → mechanism → measurable outcome, and name the closest baseline.
3. Explain each necessary equation by defining symbols, dimensions, and the role it plays. Skip equations that do not change understanding.
4. Give one concrete example that follows the method end to end.
5. Connect the work to its strongest predecessors and downstream use without turning the page into a citation list.
6. Add an interactive demo only when changing a parameter, state, or input makes the mechanism materially clearer. The demo must state what it demonstrates and what it does not prove.
7. Include limitations, open questions, primary links, and a short takeaway.

## Repository contract

- Follow the existing `useLang()` and `t(en, zh)` pattern; English and Chinese must convey the same claim.
- Reuse `PaperHeader`, `Math`, `Widget`, and existing visual primitives when appropriate.
- Keep the page compatible with static export. Avoid server-only runtime dependencies and unconfigured remote images.
- Add the page to the relevant metadata/index only when that edit does not overwrite another contributor's active work.
- Keep accessibility intact: labels for controls, keyboard-operable interactions, adequate contrast, and text equivalents for visual conclusions.

## Verification

Exercise every new control and boundary state when a browser is available. Always run `npm run build`. Treat build success as type/static-export verification, not visual QA; report when browser QA could not run.
