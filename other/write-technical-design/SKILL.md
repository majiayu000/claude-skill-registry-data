---
name: write-technical-design
description: >-
  Load this skill when settling the technical design several features share, before any is
  planned, even if a README line seems enough: ARCHITECTURE.yaml. Trigger on "write the technical
  design", "pick the stack". Not for what is already built (use
  ceh-codebase-explanation:document-architecture).
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Checking and rendering ARCHITECTURE.yaml needs uv; without it the file is saved unchecked and
  its Markdown is not rendered.
license: Apache-2.0
---

# Write the technical design

Settle the technical decisions that several features share, before the first of them is planned,
and write them into `ARCHITECTURE.yaml`, per Output: each decision as one entry of
its `technical_design` section, found by its topic, and each diagram of what is not built yet
marked `planned: true`. A build plan then follows these entries and never decides them again for
one feature. Done means the file passes its check and the tests below, and the reply lists every
entry, diagram and answer assumed.

## Procedure

1. **Check and read what exists.** For each of `ARCHITECTURE.yaml`, `PRD.yaml`, `VISION.yaml` and
   `STRATEGY.yaml` that exists, in `.agents_workspace/product/` or at the path the repo's
   `CLAUDE.md` names for it, run
   `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py check <file>.yaml` before reading it
   (formats in `${CLAUDE_SKILL_DIR}/references/architecture-schema.md`, `prd-schema.md`,
   `vision-schema.md` and `strategy-schema.md`). On exit 1, stop and report its errors, because
   a design built on a broken source carries the error into every plan. On a stale `.md` alone,
   read the YAML instead. On exit 2 or 3, or
   without uv, say in the reply that the file went unchecked, and go on. A vision or strategy
   kept as `.md` in `docs/`, the root, or where the repo's `CLAUDE.md` says is read as it is.
   Then read the `design` of each plan in `.agents_workspace/product/plan/`, the README, and the
   code. Read no business plan. With no PRD, take the features from the request and the vision,
   and say so. With no `ARCHITECTURE.yaml`, start one per Output.
2. **List the decisions the features need,** per What belongs here. For each, write down the
   options and the one chosen with its reason. An entry `technical_design` already holds is
   kept unless the request changes it, and a change follows step 5.
3. **Ask the owner one round of questions,** each with a recommended answer, for what only they
   know: a stack they require, a hosting account, a budget. Decide everything else yourself.
4. **Write each decision as a `technical_design` entry.** `topic` is its name from What belongs
   here, and `reason` is one short paragraph on why: the features that need it, and one option
   rejected and why. `choice` holds the contract for the topic as Markdown (lists, tables, code
   blocks), exact enough that a plan cites it and a builder does not ask again: for `Stack` the
   versions, the folders and the commands that run, for `Persistence` each model with its
   fields and limits, for `Interfaces` the routes with body, status codes and error shape. A
   sub-section that stands on its own, such as the style fields of one model, is a part, with
   a `title` and a `body`. Keep a part small: one over 30 lines fails the check and becomes a
   topic of its own. Write no heading in any of these texts, because the renderer numbers them.
   Refer to another entry by its topic, and to a part by its topic and title, never by a
   section number, because the rendered numbers move when a topic is added. A first write adds
   nothing to `key_decisions`, because the entry holds its own reason, so a new file holds
   `key_decisions: []`.
5. **Record each change to an entry.** Edit the entry in place and append one `key_decisions`
   entry dated today with `status: Accepted`, titled `<topic>: <the new choice in a few words>`,
   whose `context` holds the old choice and why it no longer holds. Then mark every earlier
   `Accepted` entry of `key_decisions` that decides the same topic, whoever wrote it,
   `Superseded by <date> <title>` naming the new one. A first write whose choice an `Accepted`
   entry contradicts is a change too.
6. **Draw the diagrams the entries imply,** each with `planned: true`: Components, and Data
   model and Key flows when the product has them. A new file also gets its Overview, which
   takes no mark. Leave a diagram that shows built code as it is. When the design changes what
   such a diagram shows, add a second entry of the same `name` right after it, marked
   `planned: true` and showing the whole target. It replaces the built entry once the code
   matches it.
7. **Run the tests below,** and rewrite or cut what fails.
8. **Render.** Run `artifact.py render` on the file and fix the YAML for each error it lists.
   When the Mermaid CLI can run, render each new Mermaid block with
   `npx -p @mermaid-js/mermaid-cli mmdc -i <file>.md -o <out>.md` and look at the images.
   Otherwise say in the reply that the diagrams were not rendered.

## Rules

### What belongs here

A decision belongs in the technical design when two or more features depend on it, or when
reversing it would cost a migration or a refactor. Each gets one entry, under the topic name
given here, so every plan cites one spelling:

- `Stack`: the stack and runtime
- `Persistence`: persistence and the core data model
- `Components`: the components and their boundaries
- `Interfaces`: the interface between components
- `Ownership and auth`: who owns each resource, and how a caller is authenticated
- `Deployment`: the deployment target
- `Configuration and errors`: how both are handled across components

Add a topic of your own when the product needs one these do not cover. A decision one feature
alone needs stays for that feature's build plan. The PRD says what a feature must do and how to
tell it is done. The technical design fixes the exact data, routes and states the features
share.

### The tests

| Test       | Ask                                                                                                                | Fails when                                                       |
| ---------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Shared     | Which two features need each entry, or what would reversing it cost?                                               | One feature, cheap to reverse: it belongs in a plan              |
| Options    | Does each `reason` name an option rejected and why?                                                                | Only the chosen option appears                                   |
| Exact      | Could a builder implement the topic from the entry alone?                                                          | A field, route or status the plans need is left to the builder   |
| Covers     | Which component serves each feature in the PRD?                                                                    | A feature has none                                               |
| Qualities  | Which entry answers each `non_functional` item in the PRD?                                                         | An item has none and the reply does not list it as open          |
| Consistent | Does every diagram show only what the entries say, and does no `Accepted` entry of `key_decisions` contradict one? | A node or entity has no entry behind it, or such a decision does |

With no PRD, run Covers against the features taken in step 1 and mark Qualities
`not run: no PRD`.

### What always holds

- A `technical_design` entry states what holds now: edit it in place, and never write a second
  entry for its topic. `key_decisions` is its history: never delete an entry there, and edit no
  field of one but its `status`, so the trail stays whole and no `Accepted` entry disagrees
  with the section.
- Mark every diagram of what is not built `planned: true`, and never mark one that shows built
  code. The Overview is not a diagram entry and takes no mark.
  `ceh-build-plan:implement-from-plan` and `ceh-codebase-explanation:document-architecture`
  remove the mark once the code matches the diagram.
- Write the YAML only. `ARCHITECTURE.md` is rendered from it.
- The file carries no pricing, unit economics, or any test, stage or date from a business plan.

## Output

`.agents_workspace/product/ARCHITECTURE.yaml`, or the file step 1 found at the path the repo's
`CLAUDE.md` names, in the shape of `${CLAUDE_SKILL_DIR}/assets/architecture.template.yaml`, per the
`architecture/v3` section of `${CLAUDE_SKILL_DIR}/references/architecture-schema.md`. A missing
file starts as a copy of the template, and an `ARCHITECTURE.md` with no YAML is moved first, as
that section says. `ARCHITECTURE.md` is rendered beside it and never edited by hand.

Close the reply with the path, each entry by its topic, each entry changed with its history
entry, each diagram drawn, the result of each test, every `non_functional` item left open, and
every answer assumed.

## Stop conditions

- **No human to answer** (a headless run, or called by another agent): ask nothing. Take each
  recommended answer, write the entries, and end with each question and the answer assumed, so
  the owner can change an entry they disagree with.

## Hands off to

- To plan the first feature on this design, suggest `ceh-build-plan:write-build-plan`.
