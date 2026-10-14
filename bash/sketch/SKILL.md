---
name: sketch
description: Agrees the direction of a screen in the conversation before anything is drawn — the list of what has to be decided, one question at a time with a recommendation, a table of what was settled, a rough text wireframe of each moment the screen changes, a tree of which state follows which, and what differs from today. It writes nothing, to Figma or to disk; the sketch is how a direction gets agreed, and once it is, each part of it already has a home elsewhere. Use it on its own to settle a direction before a spec or a conversation with engineering, or let `/fig:draw` pick it up in the same conversation. Triggers - "/fig:sketch", "sketch this screen first", "wireframe this", "agree the layout before drawing", "와이어프레임 먼저", "스케치부터 해줘", "방향부터 맞추자".
allowed-tools: AskUserQuestion, Bash, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__get_design_context, mcp__claude_ai_Notion__notion-fetch
---

# fig:sketch — agree the direction before the file

**A table of rules does not show anybody a screen.** A spec entry can be complete and still leave the person who asked for it unable to picture what they are agreeing to — and a write to a shared file is the most expensive place to find out they meant something else. So where the work changes how a screen looks or behaves — a new screen, a layout that moves, a flow that gains states — the direction is agreed in the conversation first, in text, before a single node is written.

That step used to live inside `/fig:draw`. It turned out to be useful well before anybody draws: to settle a direction before a spec is written, before a conversation with engineering, or simply to find out whether two people mean the same screen. Bundled into `draw`, it could only be reached by starting a Figma write. Here it stands on its own and touches nothing.

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install fig@byjunyoung`), rather than improvising what the scripts do.

## When to invoke

- "sketch this first", "wireframe this", "what would this screen look like"
- A screen is about to look or behave differently, and nobody has pictured it yet
- Before `/pm:prd` writes the entry for a screen whose layout is not settled — a spec drafted before the direction is agreed carries values chosen by whoever drafted it

## When NOT to invoke

- A stub whose `TBD (needs confirmation): …` already settles the layout, where the canonical screen fixes the rest — there is nothing left to picture. Go straight to `/fig:draw`
- Writing anything into the file → `/fig:draw`
- Stubbing the states a page is missing → `/fig:prep`
- Writing the rules down as a spec → `/pm:prd`

## Inputs

- `target` (required): the screen or the change, in words — or a stub's URL, or a canonical screen's URL to start from
- `spec_url` (optional): what the direction has to fit. **Omitted, `qa.baseline.prd` from the config is used**, the same default `/fig:draw` reads. Where that is `null` too, go on without one and say so

```
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --js <fileKey>
```

Only `qa.baseline.prd` is read here. The rest of the config governs what is drawn, and nothing is drawn here.

## Read today before sketching tomorrow

Step 6 below says what differs from today, and that cannot be written from memory. Where the target changes an existing screen, read it first — `get_metadata` for its structure, one `get_screenshot` to see it — and read the spec entry it is held to. Where it is new, read the nearest screen in the same feature area: the sketch inherits its shell (header, nav, whatever chrome every screen shares) the same way `/fig:draw` will when it clones it. Name what was read in the first message, so the person can say *that is the wrong screen* before anything is built on it.

## The shape — always the same, in this order

1. **The list of what has to be decided**, numbered, before the first question — so the size of it is visible
2. **One question at a time**, each with two or three lines of context and a recommended option. When an answer opens a question the list did not have — moving something out of a panel raises where it goes instead — ask that before moving to the next number
3. **A table once it is settled** — item │ decision — so the whole direction reads in one place
4. **A rough text wireframe for each moment the screen changes** — at rest, right after the action, while it is in progress, collapsed or returned, any secondary view — with one line under each saying what changed since the last. Labels inside the boxes are ASCII: short English words, or letters keyed to a legend written outside the box. A wide character (Korean, Japanese, Chinese) takes two columns in a monospace terminal and pushes every right-hand border out of line. Generate the lines with a short script rather than counting columns by hand, and mark any size as an estimate
5. **A transition tree** — which state follows which, on what input — with its vertical lines only at the left edge, for the same reason
6. **Two or three lines on what differs from today**

Then ask once whether the sketch is right. **That acceptance is the end of this skill.** It is not a go for anything — nothing here writes, and the go for a write belongs to the skill that writes.

## Nothing is saved, on purpose

The sketch is a means of agreeing, not a deliverable. Every part of it has a canonical home once it is agreed, and a second copy kept beside that home is one nobody updates when the first one changes:

```
decision table      ->  the spec entry                 /pm:prd
each state          ->  a frame on the page            /fig:prep stubs it, /fig:draw draws it
transition tree     ->  the flow arrows                /fig:arrows
what differs        ->  the AS-IS section, the diff    /fig:diff
```

So this skill writes no file and no Figma node, and the report says where each settled item goes next rather than storing it. Where somebody needs the sketch outside this conversation, it is the conversation's own text — copy it from there.

## Handing on to draw

`/fig:draw` skips its own sketch step when this one ran **in the same conversation** and the person accepted it. Nothing is passed between them but the conversation itself, which is why nothing has to be saved. In a new conversation, `draw` sketches again — a direction agreed last week is worth confirming before a write, not assuming.

## What the report says

```
[read]       the screen(s) and spec entry the sketch started from
[settled]    the decision table
[states]     the wireframes, one per moment, and the transition tree
[differs]    what changes from today
[open]       anything the person deferred, and which spec entry it belongs to
[next]       where each settled item goes — spec, stubs, arrows, draw
```

`[open]` names the question and the entry it belongs to, and stops there — who decides it and by when belongs to the spec.

## Traps

| Trap | What to do |
|---|---|
| Opening with a full direction whose values you chose yourself | The person has to judge every point at once and usually cannot picture any. List, then one question at a time |
| A spec draft written before the sketch is agreed | Its values were chosen by whoever drafted it and read as decided. Sketch first, then `/pm:prd` |
| Korean labels inside a box | Two columns each in a monospace terminal; every right border drifts. ASCII inside, legend outside |
| Counting columns by hand | Generate the lines with a short script |
| Sketching only the resting state | The screen changes on input. One wireframe per moment, and the tree between them |
| "What differs from today" written without reading today | Read the existing screen first and name it |
| Saving the sketch to a file or the canvas | Each part already has a home. A copy beside it goes stale the first time the home changes |
| Treating acceptance as a go to draw | This skill writes nothing. `/fig:draw` still previews and takes its own go |

## Constraints

- **Zero writes** — no `use_figma`, no file on disk, no page in a docs tool
- Wireframe labels are ASCII; any size in one is an estimate and says so
- One decision per question, with a recommendation
- Never present a value as decided that the person did not decide
