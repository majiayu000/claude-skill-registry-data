---
name: "Web: Design"
description: "Design a new interface from a scope document, a roadmap task or an interview: inventory, layout, a wireframe in the product's own tokens with numbered callouts, approval, then the principles check"
when_to_use: "When a new interface or page is to be designed before it is built. The invocation names a scope document path, a roadmap task id or `interview`; with no argument, the claimed task, then scope documents, then the interview are offered in that order."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: web
  goblin-spinner: taking inventory|drawing boxes|numbering callouts
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Edit", "Bash", "AskUserQuestion"]
argument-hint: "[path to a scope document | roadmap task id | interview]"
---

# Design a new interface

Load `web-conventions` and `artefact-conventions` first. This skill ends at an approved, checked wireframe: the build spec. The build itself sits in a wider task; `web-check` at sign-off and `web-walkthrough` follow it.

## Step 1: Resolve the source

`$ARGUMENTS` is one of:

- **A path** to an existing file: the scope document. Go to Step 3.
- **A roadmap task id** (letters and digits with dots, `2SE.1`): find it with `python3 ~/.claude/marketplace/roadmap/scripts/roadmap.py open --json` and take its description, milestone and notes as the seed of a scope document. Go to Step 2 with the interview narrowed to what the task leaves open.
- **`interview`**: go to Step 2.
- **Nothing**: detect in this order and confirm each hit with one question before using it.
  1. `roadmap.py ready --json` lists `claimed`; a task claimed by Jason is offered first.
  2. `docs/**/*scope*.md` and `docs/specs/**/*.md`; every hit is offered.
  3. Neither: offer the interview.

Nothing starts without a confirmation.

- [ ] Source named back to Jason in one line before anything else

## Step 2: Interview (when chosen)

Rounds of 2 to 4 questions, the `roadmap:create-interview` discipline. Each round ends with *"Anything else, or shall I write up the scope?"*. Work through the scope template's sections in order, skipping any the seed already answers:

1. Who it is for, and what each audience arrives to do.
2. Devices and viewports, with the source for each (principle 8).
3. The copy brief: who the words address, register and mood, what may be said outright and what must stay unsaid (principle 10).
4. The inventory, one region at a time: what it holds, how many, which actions, which open states (principle 1).
5. Requirements, numbered `R1`, `R2` so callouts can cite them.

Write the result to `docs/scope/<slug>.md` from `~/.claude/library/templates/web-scope.md`, show the path, then continue as from a scope document. The interview's answers are the document; nothing is remembered outside it.

- [ ] Scope document written and its path shown before Step 3

## Step 3: Start

Run the shared start from `web-conventions`: collate, name the gaps, fill them. For a scope document the gaps are its empty sections; a device list and a copy brief block the drawing until filled or recorded as assumptions in the document's §8.

## Step 4: Inventory and layout

Principles 1, 2 and 11, written into the scope document before any drawing:

- **§4 Inventory** complete for every route the design covers.
- **§5 Layout decisions**: one row per region, the shape chosen because of what the row holds (short field lists side by side; long homogeneous lists as rows; dense sets as a card grid; one column only when nothing else fits).
- **§6 First screen**: per route, whether principle 11's trigger holds and what folds if it does.

Show §5 and §6 and get a yes before drawing.

- [ ] Every region in §4 has a row in §5
- [ ] §6 states triggered or not, with the reason, per route

## Step 5: Wireframe

One page per route under `docs/artefacts/<slug>/wireframe-<route>.html`, or a single `wireframe.html` for one route. Principle 6 governs:

- **Product tokens.** Copy the product's `:root` block (found in Step 3) into the page and cite the file in the mapping-notes comment. The mock uses the product's own faces; annotations use a mono face so they never read as part of the design. If the product ships one colour scheme, the mock shows that one and says so.
- **Numbered callouts**: a badge (`.co`, absolutely positioned inside the mock) per decision worth approving, and an explain list under the mock, one item per badge, each citing the requirement or inventory row it answers (`R3`, `§4 queue`). A badge that cites nothing comes out.
- **The mock collapses** at the scope's viewports, so narrowing the window shows the phone layout; the explain list says what moves.
- **Masthead** per `artefact-conventions`: product, task, the scope document's path, the viewports drawn.

Open the page (`open <path>`) and ask for approval with one question: approve, change (saying what) or redraw. Iterate until approved; record the approval date in the scope document's status row.

- [ ] Every callout cites an `R` id or an inventory row
- [ ] Mapping-notes comment names the CSS file the tokens came from
- [ ] Approval recorded in the scope document

## Step 6: Check

Run `web-check` in `wireframe` mode against the approved page and the scope document. Findings go to `docs/artefacts/<slug>/observations.json` through `observations.py add` (design mode has no live store). An unwaived finding reopens Step 5.

## Step 7: Hand over

Report: the scope document, the approved wireframes, the check's verdict and any waivers. State the next steps in one line each: build on the branch; `/web-check signoff` when built; `/web-walkthrough`. Offer shelving once, per `web-conventions`.
