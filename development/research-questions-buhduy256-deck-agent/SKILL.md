---
name: research-questions
description: Generate a research checklist from a use case. Reads the UC, its FRs, NFRs, and BRs, then produces questions grouped by requirement. For technical questions, provides options with tradeoffs. Used at the start of Phase 1.
---

# Research questions

Generate the research checklist for a use case build.

## Input

The PO names a UC or a build scope (e.g., "UC-001"). Use the active version from
`dev/versions/README.md`. Read these files:

1. The version spec UC file: `dev/versions/vN/spec/02-use-cases/UC-XXX.md`
2. Every in-scope FR in `dev/versions/vN/spec/` referenced in the UC's step table and
   alternative flows.
3. Every NFR and BR referenced by those FRs or by the UC.
4. Existing research in `dev/research/` — to avoid asking already-answered questions.
5. Existing decisions in `dev/decisions/` — to avoid asking already-decided questions.

## Process

### Step 1 — Build the flow model

Before generating any questions, trace the runtime flow end-to-end:

1. Read the UC's step table (S1, S2, ...) and alternative flows (A1, A2, ...).
2. For each step, think through the concrete technical operations that happen at
   runtime. Go from trigger to completion. Example for "system fetches chapter":
   - Browser sends URL to backend API
   - Backend resolves DNS, checks for SSRF
   - Backend sends HTTP GET to target site
   - Target site returns HTML (or blocks the request)
   - Backend parses HTML, locates chapter content
   - Backend extracts text, strips ads/navigation
   - Backend returns structured text to frontend
3. Write each sub-step as a node in the flow. This is the **flow model**.
4. For alternative flows, branch from the main flow at the decision point.

The flow model goes into the checklist as a visible section so the PO can see
the full picture before reading individual questions.

### Step 2 — Derive questions from the flow

Walk through the flow model step by step. At each node, ask:

1. "Do we know HOW to do this?" — if not, that's a research question.
2. "Are there CHOICES to make here?" — if yes, that's a decision question.
3. "Can this FAIL, and do we know how to handle it?" — if not, that's a resilience
   question.
4. Check if existing research already answers the question — if yes, reference it and
   mark as `answered` or `decided`.
5. For technology choices, provide an options table:

   | Option | Description | Fits requirements | Tradeoffs |
   |---|---|---|---|

6. **Runtime questions.** When a flow node runs through the runtime (OpenCode:
   sessions, tool calls, model calls, streaming, permissions), ask how the runtime
   handles it and where DeckAgent hooks in — unless `dev/research/` already answers it.
   This research is mandatory for builds that touch the runtime (WORKFLOW.md "Phase 1").
7. **LLM boundary questions.** When it is unclear whether a node should call the model
   or use prebuilt, deterministic parts (themes, layouts, animations, renderers), ask
   it as a decision question. The default is deterministic code.
8. Tag each question with:
   - **Flow step:** which node in the flow model it comes from.
   - **Why it matters:** which FR/AC depends on the answer.

## Output

Create `dev/versions/vN/builds/UC-XXX-label/research-checklist.md` from the template at
`dev/templates/research-checklist.md`.

The checklist has two main sections:

1. **Flow model** — the step-by-step runtime trace, in prose. Each node shows what
   happens technically. Questions are annotated inline so the PO can see where each
   one comes from.

2. **Questions table** — grouped by FR/NFR. Each question has:
   - A unique ID: `RQ-N` (scoped to this UC)
   - The question text
   - **Flow step** reference (e.g., "S2.3 — Parse HTML")
   - Why it matters (which FR/AC)
   - Status: `open`, `answered`, or `decided`
   - Options table (for technical choices)

### Step 3 — Generate sequence diagrams for tickets

When creating GitHub Issues for research questions (using `research-ticket` template),
generate a Mermaid sequence diagram for each ticket that:

1. Shows the full UC flow as a sequence diagram with the actual participants
   (User, Frontend, Backend, External services).
2. Highlights the step(s) this question relates to using `rect rgb(255, 230, 150)`
   with a `note` pointing to the RQ number.
3. Keeps the unhighlighted steps visible but simple — the reader sees the full context
   but their eye goes to the highlighted area.
4. Uses the same diagram across related questions, just moving the highlight.

The diagram is the first thing the reader sees — before the question itself.

Create deliverable files for each question:
- **Research answer:** add a section `## UC-XXX/RQ-N: Title` to the matching topic
  file in `dev/research/`. Research files are **topic-based containers** — one file
  per topic, questions from multiple UCs accumulate in the same file.
- **Decision record:** create `dev/decisions/DEC-NNN-topic.md` from the template at
  `dev/decisions/_TEMPLATE.md`, with the **options table pre-filled only**. Leave
  `Choice` and `Why` empty — the PO writes those after researching (see
  WORKFLOW.md "Roles").

Include a **deliverable map** table in the checklist linking each RQ to its file.

Also seed the traceability matrix at `dev/versions/vN/builds/UC-XXX-label/traceability-matrix.md` from
`dev/templates/traceability-matrix.md` — one row per in-scope FR/AC and NFR, with the
Tier column seeded from each AC's `Check` field (`deterministic` → ci, `evaluation` →
eval) — so the spine exists from the start of the build.

Follow WORKFLOW.md "Document rules": front-load the checklist's `## At a glance` block,
keep the template's section order, and reference matrix rows rather than restating
requirement text.

## Linking convention

All cross-references must be clickable Markdown links (see WORKFLOW.md "Linking
convention"). At the start, derive the repo base URL:

```bash
git remote get-url origin
# https://github.com/{owner}/{repo}.git → base = https://github.com/{owner}/{repo}
```

Apply to every output:

- **Research checklist:** Ticket column uses `[#N]({base}/issues/N)`, Deliverable map
  File column uses `[dev/research/topic.md]({base}/blob/main/dev/research/topic.md)`.
- **Research files** (`dev/research/`): `**Ticket:** [#N]({base}/issues/N)` and
  `**Blocked by:** [#N]({base}/issues/N)`.
- **Decision files** (`dev/decisions/`): `ticket [#N]({base}/issues/N)`.

## Rules

- The agent supplies questions and options tables only. It does **not** answer the
  research questions and does **not** fill the `Choice` or `Why` of a decision
  record — the PO does that (see WORKFLOW.md "Roles"). This is the one
  phase where the human keeps the thinking.
- Do not generate questions about product requirements — those are settled in the spec.
- Do not generate questions answerable by reading the spec — read it first.
- Do not generate questions about implementation details that can be decided during
  coding (variable names, internal function splits). Focus on decisions that affect
  the architecture, the test strategy, or the ticket structure.
- If a question spans multiple FRs, list it once under the most relevant FR and
  cross-reference.
- Existing answered questions in `dev/research/` are referenced, not duplicated.
