---
name: doc-coauthoring
description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
---

# Doc Co-Authoring Workflow

This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions writing documentation: "write a doc", "draft a proposal", "create a spec", "write up".
- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC".
- User seems to be starting a substantial writing task.

**Initial offer:** offer the user a structured workflow for co-authoring the document. Explain the three stages:

1. **Context Gathering** — user provides all relevant context while Claude asks clarifying questions.
2. **Refinement & Structure** — iteratively build each section through brainstorming and editing.
3. **Reader Testing** — test the doc with a fresh Claude (no context) to catch blind spots before others read it.

Explain that this approach helps ensure the doc works well when others read it (including when they paste it into Claude). Ask if they want to try this workflow or prefer to work freeform.

If user declines, work freeform. If user accepts, proceed to Stage 1.

## Reference map

| When | Read |
|---|---|
| Running Stage 1 (full info-dump flow, integration handling, clarifying-question generation) | [`references/stage1-context.md`](references/stage1-context.md) |
| Running Stage 2 (full 6-step per-section loop, quality checking, near-completion review) | [`references/stage2-refinement.md`](references/stage2-refinement.md) |
| Running Stage 3 (sub-agent vs manual testing approaches, per-step prompts) | [`references/stage3-reader-testing.md`](references/stage3-reader-testing.md) |

## Collaboration, revision, and review constraints

- **User owns the doc.** Recommend a final human read-through before completion. Verify facts, links, and technical details yourself only when explicitly asked.
- **Don't write the doc *for* them — guide them through writing it.** Ask first, propose options, get curation feedback, then draft.
- **Always use `str_replace` for edits, never reprint the whole doc.** This preserves their work and keeps token cost down.
- **Never use artifacts for brainstorming lists** — that's just conversation. Artifacts are for the drafting scaffold and section content only.
- **Don't accept silent direct edits as approval.** If the user edits the doc directly and asks for a re-read, note the changes mentally and apply them to future sections — they're signaling preferences.
- **Reader Testing must use a fresh Claude with no context.** Sub-agent (Claude Code) or a separate Claude.ai conversation (web). Don't simulate reader-testing in the same conversation that drafted the doc.
- **Don't fabricate facts, links, or technical details.** If you don't know, ask the user or flag the gap explicitly with `[verify: ...]`.
- **Stop after 3 no-substantial-change iterations on a section** and ask if anything can be removed. Don't churn.
- **Respect "skip this stage" requests.** Always give the user agency to adjust the process; don't enforce the workflow over their judgment.

---

## Stage 1: Context Gathering

**Goal:** close the gap between what the user knows and what Claude knows, enabling smart guidance later.

### Initial questions

Ask the user for meta-context about the document:

1. What type of document is this? (technical spec, decision doc, proposal, etc.)
2. Who's the primary audience?
3. What's the desired impact when someone reads this?
4. Is there a template or specific format to follow?
5. Any other constraints or context to know?

Inform them they can answer in shorthand or dump information however works best for them.

### Info dumping + clarifying questions (summary)

Encourage the user to dump everything they have — background, related discussions, why alternatives are rejected, organizational context, timeline pressures, technical dependencies, stakeholder concerns. Then ask 5–10 numbered clarifying questions based on the gaps. Full integration handling (Slack / Teams / Google Drive / SharePoint / MCP), image alt-text logic, unknown-entity handling, and clarifying-question generation rules: [`references/stage1-context.md`](references/stage1-context.md).

**Exit condition:** sufficient context has been gathered when questions show understanding — edge cases and trade-offs can be discussed without needing basics explained.

**Transition:** ask if there's any more context to provide, or if it's time to move on to drafting. When ready, proceed to Stage 2.

---

## Stage 2: Refinement & Structure

**Goal:** build the document section by section through brainstorming, curation, and iterative refinement.

**Section ordering:** start with whichever section has the most unknowns — usually the core proposal for decision docs; the technical approach for specs. Summary sections come last. If the user doesn't know what sections they need, suggest 3–5 appropriate for the doc type.

**Once structure is agreed:** create the initial document scaffold with placeholder text (`[To be written]`) for all sections — `create_file` artifact if available, otherwise a markdown file in the working directory.

**Per-section loop (6 steps).** Full prompts and edit rules in [`references/stage2-refinement.md`](references/stage2-refinement.md):

1. **Clarifying questions** — 5–10 specific questions about what to include in this section.
2. **Brainstorming** — 5–20 numbered options depending on section complexity. Look for context already shared that may have been forgotten plus angles not yet mentioned.
3. **Curation** — user indicates keep/remove/combine ("Keep 1,4,7,9"; "Remove 3 (duplicates 1)"; "Combine 11 and 12"). Freeform feedback OK — parse intent and apply.
4. **Gap check** — ask if anything important is missing.
5. **Drafting** — use `str_replace` to replace placeholder text with the actual section. Tell the user to indicate what to change rather than editing directly (helps Claude learn their style for future sections).
6. **Iterative refinement** — `str_replace` for every edit, never reprint the doc. After 3 no-substantial-change iterations, ask if anything can be removed.

**Repeat for all sections.** When section is done, confirm and ask if ready to move to the next.

**Near completion (≥80% of sections done):** re-read the entire document and check for flow, consistency, redundancy, contradictions, generic filler. Provide feedback. After final refinement, ask if ready to move to Reader Testing.

---

## Stage 3: Reader Testing

**Goal:** test the document with a fresh Claude (no context bleed) to verify it works for readers.

**Approach selection:**

| Environment | Approach |
|---|---|
| Claude Code (sub-agents available) | Sub-agent-driven testing — perform directly without user involvement |
| Claude.ai web / no sub-agents | Manual testing — user runs questions in a fresh Claude.ai conversation |

Four-step sequence for both approaches (full per-step prompts in [`references/stage3-reader-testing.md`](references/stage3-reader-testing.md)):

1. **Predict reader questions** — 5–10 questions readers would realistically ask when trying to discover the doc.
2. **Test** — invoke a sub-agent with just the doc content + each question, or instruct the user to paste the doc + questions into a fresh Claude.ai conversation.
3. **Additional checks** — ambiguity, false assumptions, contradictions, assumed knowledge.
4. **Report and fix** — list specific issues, loop back to Stage 2 refinement for problematic sections.

**Exit condition (both approaches):** when Reader Claude consistently answers questions correctly and surfaces no new gaps or ambiguities, the doc is ready.

---

## Final Review

When Reader Testing passes:

1. Recommend the user do a final read-through themselves — they own this document and are responsible for its quality.
2. Suggest double-checking facts, links, and technical details.
3. Ask them to verify it achieves the impact they wanted.

Ask if they want one more review, or if the work is done.

**If user wants final review, provide it. Otherwise:** announce document completion with a few final tips:
- Consider linking this conversation in an appendix so readers can see how the doc was developed.
- Use appendices to provide depth without bloating the main doc.
- Update the doc as feedback is received from real readers.

---

## Tips for Effective Guidance

**Tone:**
- Be direct and procedural.
- Explain rationale briefly when it affects user behavior.
- Don't try to "sell" the approach — just execute it.

**Handling deviations:**
- If user wants to skip a stage: ask if they want to skip this and write freeform.
- If user seems frustrated: acknowledge this is taking longer than expected and suggest ways to move faster.
- Always give the user agency to adjust the process.

**Context management:**
- Throughout, if context is missing on something mentioned, proactively ask.
- Don't let gaps accumulate — address them as they come up.

**Artifact management:**
- Use `create_file` for drafting full sections.
- Use `str_replace` for all edits.
- Provide artifact link after every change.
- Never use artifacts for brainstorming lists — that's just conversation.

**Quality over speed:**
- Don't rush through stages.
- Each iteration should make meaningful improvements.
- The goal is a document that actually works for readers.
