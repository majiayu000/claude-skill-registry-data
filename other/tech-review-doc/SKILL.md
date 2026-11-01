---
name: tech-review-doc
version: "1.1.0"
user-invocable: true
description: "Turn a technical design doc into a product/QA-readable technical review markdown (business language + Mermaid). Hard-gates §1 background/goals until the user explicitly approves before writing the file. Triggers — 「技术评审文档」「生成评审文档」「design to review」「tech review doc」「写技术评审」. Do NOT use for marketing articles (article-writer), code PDCA (solve-workflow), or AI de-slop rewriting (humanizer)."
dependencies:
  - clarifying-question-discipline
  - report-output-discipline
---

# Technical Design → Technical Review Document

Convert a **code-heavy design document** into a **technical review document** for product, QA, and engineers who are not deep in the code.

## Core principles

| Principle | Requirement |
|-----------|-------------|
| Audience | Non-code-deep readers can understand §§1–4 on their own |
| Language | Concise and plain; §§1–3 **zero code**; from §4 onward keep only necessary interface/field/table **purpose** |
| Diagrams | Mermaid; nodes use **business/module names**, not class or file names |
| Source of truth | The design doc is factual; user-confirmed content overrides vague design wording |
| Brevity | For each section ask: “Does anyone in the review meeting need this?” — if not, omit it |
| Template | Use sibling **[template.md](template.md)** |

## Inputs

| Input | Notes |
|-------|-------|
| **Design document path** (required) | User `@` or path |
| **Review type** (optional) | Scheme / implementation / acceptance review; default scheme review |

Read the design document fully before starting; scan related PRD or OpenSpec change when useful.

If the design exceeds ~1500 lines, skim structure and headings first, then deep-read sections as needed.

## Output

Write the file **next to the input document**, named `tech-review-{topic}-{YYYY-MM-DD}.md`.

Derive `{topic}` from the design title keywords; use the current date for `YYYY-MM-DD`.

Registry row: `技术评审文档` in `report-output-discipline/reference.md` (`human` + `接入`). After the Markdown file is written, derive `tech-review-{topic}-{YYYY-MM-DD}.html` beside it following `report-output-discipline`, and report both paths.

---

## Flow (five steps, hard gate)

```
Step 0 Startup check
  ↓
Step 1 Background & goals (clarify; no file write until user approves §1)
  ↓ user explicitly approves §1
Step 2 Generate §2 necessary diagrams (ask if unsure)
  ↓
Step 3 Multi-option comparison → §3 (skip if none)
  ↓
Step 4 Core content summary → §4
  ↓
Step 5 Complete §§5–7 and write the file
```

<HARD-GATE>
**Until Step 1 is done and the user explicitly approves §1, do not create or write the review file, and do not run Steps 2–5.**
</HARD-GATE>

---

## Prerequisite skill check

On load, verify `clarifying-question-discipline` and `report-output-discipline` are available. If either is missing, abort and print:

`npx skills add FuDesign2008/open-skills -g --skill '*' --yes`

Do not silently fall back.

---

## Step 0: Startup check

1. Confirm the design document path; ask if missing or invalid
2. Read sibling `template.md`
3. Extract from the design: title, surfaces/modules, whether multi-option comparison exists, existing Mermaid
4. Restate understanding in 3–5 sentences and state that Step 1 clarification starts next

---

## Step 1: Background & goals (mandatory)

Design backgrounds are usually written for engineers. Review §1 must use **business language** for product/QA.

Follow `clarifying-question-discipline`: **one question per turn**, multi-round until clear; prefer structured single-choice when the agent supports it; include a recommended answer when a default is knowable. Describe intent only — do not hard-code a platform-specific questioning tool.

### 1.1 Goal

Jointly confirm and refine **§1 Background & goals**. Treat design-doc background as a **draft only** — never paste it verbatim.

### 1.2 Coverage (ask across rounds as needed)

Business motivation, user scenarios, success criteria, Non-Goals, glossary terms that product/QA need.

Translate technical motives into business language before asking for confirmation.

### 1.3 Suggested questions (pick one at a time)

1. Whose problem, and what problem, does this mainly solve?
2. What is the business cost of doing nothing?
3. What change can users/ops **directly perceive**?
4. What is the single most important QA acceptance check?
5. What is explicitly out of scope?
6. Do any terms need more business-friendly names for product/QA?

### 1.4 Deliverable and gate

- Present a **§1 draft** (business language only, no code)
- Ask: “Is this background and goal accurate? After you confirm, I will generate diagrams and the full document.”
- Enter Step 2 **only** after explicit user confirmation

---

## Step 2: §2 Solution overview (diagrams)

### 2.1 Which diagrams (as needed)

| Diagram | When needed |
|---------|-------------|
| **System topology** | ≥2 clients/deploy boundaries |
| **Architecture** | Module responsibilities need a separate view |
| **Data flow** | Config/state crosses modules, or migration |
| **Logic flow** | Main path has branches, validation, or failure paths |

Ask the user when unsure. Only draw diagrams that are needed; omit unused diagram types from the document.

### 2.2 Drawing rules

- **Rewrite** Mermaid from the design; do not copy diagrams that embed code symbols
- Each diagram: title + 1–2 sentence caption tying back to §1 goals
- §2.1 solution summary: 2–3 sentences

---

## Step 3: §3 Options and selection (conditional)

| Case | Action |
|------|--------|
| Substantive multi-option comparison exists | Generate §3 (decision context + comparison table + selection conclusion only) |
| Single chosen approach, no comparison | **Skip §3** |

Comparison dimensions: goal fit, user experience, delivery cost, risk/rollback, long-term maintenance.

---

## Step 4: §4 Core content summary

### Keep

- Change scope (**product module names**)
- Main flows; meaning of critical data/config; storage and migration
- Business meaning of interface changes (fold into flow narrative; no standalone API tables)

### Drop or compress

- Function signatures, class names, large code/JSON dumps
- Unit-test filenames, commit-level churn
- Standalone interface/contract tables

**Self-check**: a developer unfamiliar with the business can answer “which areas change, how data moves, what happens to old data” after §4.

---

## Step 5: §§5–7 and write file

| Section | Points |
|---------|--------|
| §5 Risks & boundaries | Risk list (required) + known limits (required); security/compliance only when relevant |
| §6 Release & ops | **Conditional**: only when canary/rollout or server-side data backfill applies; otherwise omit |
| §7 Conclusion | Draft verdict + Action Items |

After writing, remove the template’s trailing “模板使用说明” section. In chat, report: output path, whether §1 was confirmed, which diagrams were generated, whether §3/§6 were skipped, and any placeholders left for the user.

---

## Language conversion reference

| Technical phrasing | Review phrasing |
|--------------------|-----------------|
| Call API / RPC | A requests data from B |
| Write Redis / cache | Temporarily remember this state for next time |
| DB migration | Reorganize old data under the new rules |
| Config push | Admin rules sync to clients |
| Degrade / fallback | On failure, automatically fall back to the old path |
| Idempotent | Repeating the action has no extra side effects |
| Transaction | All succeed together, or nothing changes |

Prefer “who does what to whom, and what the user sees” over implementation detail.

---

## Host auto-mode contract

When invoked under `write-workflow` **auto mode**:

- The §1 HARD-GATE still applies — **no** file write and **no** Steps 2–5 until the user explicitly approves §1.
- After §1 approval, Steps 2–5 MAY run continuously (diagrams → remaining sections → write file) without per-step confirmation.
- Standalone or manual-host invocation keeps the interactive §1 gate as in Step 1.4.

## Relationship to other skills

| Skill | Relationship |
|-------|--------------|
| `clarifying-question-discipline` | Strong dependency for Step 1 |
| `report-output-discipline` | Owns the derived HTML contract |
| `write-workflow` | Optional host (eight-stage) that routes here by default for tech-review writing |

---

## Success criteria

- [ ] Step 1 explicitly confirmed by the user
- [ ] §§1–3 have no code blocks except Mermaid
- [ ] §2 only necessary diagrams
- [ ] §3 generated or skipped per rules
- [ ] §6 generated or skipped per rules
- [ ] §4 is not a code dump
- [ ] File written with traceable link to the design doc
- [ ] Path and naming match the Output rules
