---
name: sdlc-feature
description: Invoked explicitly by /feature. Captures a raw feature request into a structured intake document, allocates a FEAT-ID, classifies whether the feature is AI-backed, and opens its state machine entry. This is the entry point of the SDLC chain.
argument-hint: "\"<one-line feature request>\""
disable-model-invocation: true
---

# /feature — intake

Turns a sentence into a document the PRD phase can start from.

## Protocol (shared — do not restate here)
Framework assets — `.agent/framework.yaml`, `.agent/steps/`, `.agent/rules/`,
`.agent/gates/`, `.agent/templates/`, `.agent/modules/` — resolve **project-first**: use
the repository's copy when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/…`. That is
how one repo can override a single template or rule without forking the framework.
`.agent/project-context.yaml` and `.agent/state/` are **always project-local** — never
read or write them under the plugin root.
1. If `.agent/state/context-cache.md` exists and its `framework_version` matches
   `.agent/framework.yaml`, Read ONLY that file. Otherwise Read
   `.agent/steps/context-loader.md` and execute it, then write the digest back to the cache.
2. Read `.agent/steps/gate.md` and execute it with the phase inputs below.
3. On completion, format output per `.agent/steps/report-footer.md`.
Never copy the contents of those files into this skill.

**Phase inputs** — phase `intake`, gate `G0`, template
`{{paths.templates_dir}}/feature-request.md`, output
`{{paths.product_dir}}/{FEAT-ID}-{slug}.md`.

---

## Step 1 — Allocate the FEAT-ID

`{ticket_prefix}-{NNN}`, zero-padded to three digits, next free number across
`{{paths.product_dir}}`, `.agent/state/features/` **and** `.agent/state/archive/`.

Never reuse an id, including from an abandoned feature. Trace rows, branch names and
findings all key on it, and a reused id silently merges two histories.

Derive `slug` from the title: lowercase, hyphenated, at most five words.

## Step 2 — Write the document, mark what you cannot know

**Do not interview.** Write the intake document from the template, filling every section
you can genuinely infer from the request, and marking every section you cannot as:

```
TBD (Q<n>: <the specific question, phrased so it can be answered in one line>)
```

Then add a row to `## Open questions` for each `Q<n>`, with the blocked phase and
`owner: PO/BA`.

**The document is the question list.** The person who owns this feature edits the file,
answers the TBDs in place, and re-runs `/feature` (or goes straight to `/prd`, whose
input check will re-read it). That works asynchronously and leaves a record; an
interactive Q&A works only while someone is sitting at the terminal, and leaves none.

What you can usually infer from a one-line request: the problem statement, a first guess
at who it is for, and the AI classification. What you almost never can: the success
signal's current value, the out-of-scope boundary, and the constraints.

**Never invent a success signal.** `TBD (Q1: which number moves if this works, and what
is it today?)` is a useful artifact. "Improve user satisfaction by 20%" is a fabricated
target that everything downstream will then be aimed at, and nobody will remember it was
invented here.

Write questions that can be answered without rephrasing:

| Weak | Usable |
|---|---|
| "What are the requirements?" | "Which number moves if this works, and what is it today?" |
| "Any constraints?" | "Is there a date this must ship by, or a system it must not change?" |
| "Who uses this?" | "Which role hits this problem, and roughly how many times a week?" |

## Step 3 — Classify the AI surface

Set `ai_class` from `.agent/framework.yaml` → `ai_classes`:

| Value | When |
|---|---|
| `none` | no model in the path — ordinary code |
| `llm-generation` | the model writes text a user reads |
| `llm-extraction` | the model pulls structured data out of unstructured input |
| `llm-classification` | the model chooses from a fixed set of labels |
| `rag` | retrieval feeds the model, and retrieval quality is part of the outcome |
| `agentic` | the model chooses and calls tools in a loop |

**This single field decides how much process the feature carries.** `none` skips prompt
specs, eval sets and every eval gate for the rest of the chain. Do not mark a feature
AI because the product is an AI product — mark it AI because *this behaviour* comes from
a model.

If the request does not make this determinable, write
`TBD (Q<n>: does this behaviour come from a model, or is it ordinary code?)` and leave
`ai_class` unset. Do not guess: `none` on an AI feature means the quality of the thing
that matters most is never measured, and AI on a plain feature taxes it with an eval
harness that will rot.

## Step 4 — Finish the document

Use `{{paths.templates_dir}}/feature-request.md`. Every section is present in the output,
either filled or carrying an explicit `TBD (Q<n>: …)`. Never leave a silent blank — a
blank section reads as "considered, and there is nothing to say", which is a different
claim from "nobody has answered this yet".

Set the header: `Owner role: PO/BA` and `Status: draft`. The owner changes `Status` to
`ready` themselves once the TBDs are answered; nothing in the framework sets it for them,
because that flag is the human's statement that the content is theirs.

Enforce the banned-term list on every word.

## Step 5 — Open the state machine

Create `.agent/state/features/{FEAT-ID}.yaml` from
`{{paths.templates_dir}}/state/feature.yaml` with `kind`, `ai_class`, `phase: intake`,
`loop_iteration: 0`, the branch name from `conventions.branch_format`, the request
artifact path **and its content hash**, and any `open_questions`.

Then update `.agent/state/current.yaml`: add the feature, set `active_feature`, set
`next_command`.

## Step 6 — Evaluate G0 and report the gaps

Run `.agent/gates/G0-intake.yaml`. Write the verdict and `input_hash` into the feature
state file.

`revise` or `block` is the **expected** outcome of a first run from a one-line request —
the success signal and the constraints are almost never inferable. That is not a failure.
Report it as:

```
Status : ⚠️ Warnings
Gate   : G0 Intake — revise
         C2 success signal is not a number  -> Q1, owner PO/BA
         C3 AI classification not set       -> Q2, owner PO/BA
Next   : answer the TBDs in docs/product/features/{FEAT-ID}-{slug}.md, then /prd {FEAT-ID}
```

List the unanswered questions with their file and section. Do not ask them. Do not
suggest `/prd` as if the document were finished — but do name it as the next command, so
whoever answers the questions knows where they are going.

---

## Boundaries

- **Do not design.** No use cases, no requirements, no architecture, no UC-IDs. Those
  are born in the PRD and the SRS. An intake document that already contains the solution
  has skipped the step where someone could have questioned the problem.
- Do not create a branch, a PRD, or any directory beyond what is listed here.
- One feature per invocation. If the request contains several, say so and propose the
  split — do not silently create one bloated feature.
