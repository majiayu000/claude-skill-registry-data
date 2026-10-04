---
name: draw
description: Draws a screen, or fills a stub `/fig:prep` left behind, inside the file's own conventions rather than as a loose fragment. It looks up the file's own arrangement pattern first and, where none exists, stops and has one defined rather than inventing a one-off. It anchors to the nearest canonical screen and clones it, so what comes out is the whole screen with the change in it, not a swatch of the part that is new. Copy comes from a spec, from the running system, or from the file's own precedent — never from what sounds plausible. One undecided fact is pinned on the node it belongs to, never left as a blank frame standing in for the whole screen. Where a screen is about to look or behave differently, the direction is agreed in the conversation first — item by item, then as a rough text sketch of each state — before anything reaches the file. Triggers - "/fig:draw", "draw this screen", "fill this placeholder", "design this state", "이 화면 그려줘", "placeholder 채워줘", "이 상태 디자인해줘".
allowed-tools: AskUserQuestion, Bash, Skill, mcp__plugin_figma_figma__use_figma, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__search_design_system, mcp__plugin_figma_figma__get_design_context, mcp__claude_ai_Notion__notion-fetch, mcp__plugin_figma_figma__whoami
---

# fig:draw — draw the screen

Every other skill here is explicit about staying out of this step. `/fig:prep` lays the skeleton and stubs what is missing, `/fig:arrows` wires the flow around it, `/fig:lint` only ever reads. In between, a screen has to actually get drawn — and until now that step was a sentence in the README rather than a skill, so none of this plugin's own conventions reached it. This is that step brought inside the same discipline as the rest: the config decides the naming, the canonical page and the arrangement pattern, not whoever happens to be drawing.

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install fig@byjunyoung`), rather than improvising what the scripts do.

**Prerequisites**: always load the `figma:figma-use` skill before calling `use_figma`. **Assembly is not this skill's work** — where a screen needs components discovered, imported and composed, load `figma:figma-generate-design` and let it do that; where a component master or a variant set has to be built, `figma:figma-generate-library`. This skill decides what gets drawn, where it belongs and what it has to match, and hands the building to them.

**Seat check before the first write** — call `whoami` once. Where every plan it lists carries `seat: View`, stop before any `use_figma` write and say so: reading the file works on a View seat, writing to it needs an Edit seat on that file's plan, and no retry changes that. Where the seats are mixed, go ahead — and if the first write comes back as a permission error, report the seat table and stop rather than retrying.

## When to invoke

- "draw this screen", "design this state", "fill this placeholder"
- Right after `/fig:prep` leaves stubs behind — the natural second half of that run
- A state exists in the spec and nowhere in the file

## When NOT to invoke

- Laying out the section skeleton or stubbing missing cases → `/fig:prep`
- Creating or syncing flow arrows → `/fig:arrows`
- Checking for violations only, zero writes → `/fig:lint`
- Auditing token bindings → `/fig:tokens`
- Applying finished work into the canonical page → `/fig:sync`
- Marking what changed between two designs → `/fig:diff`
- Turning a finished design into a working prototype → `/fig:proto`
- Applying a finished design to front-end code → `/fig:code`

## Inputs

- `target` (required): a stub `/fig:prep` left — its URL, or its name and section — or, with nothing stubbed yet, a description of the screen or state to draw
- `spec_url` (optional): the requirements the drawn content has to match. **Omitted, `qa.baseline.prd` from the config is used** — the same spec `/fig:qa` judges against later, so a screen is drawn against the document it will be measured by. Where that is `null` too, ask for a source or record that there is none

## Where the rules come from — the config file (same source as fig:prep, fig:lint, fig:sync)

```
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --js <fileKey>
```

Sections read: `naming` (frame and section patterns, state suffixes, the common and pattern pages) · `pages` (strictness, the canonical axis, excluded sections) · `placeholder_style` (how a stub is recognized, and what its removal has to leave behind) · `design_system` (which library is searched first) · `references` (screen-reference services consulted only when a pattern has to be newly defined) · `layout` (spacing, where nothing existing says where to put something) · `qa.baseline.prd` (the default spec).

- **Strictness comes from the target page's name**, the same way `/fig:prep` reads it. A match in `pages.readonly` means refuse the work and say so. On `pages.free` the drawing discipline still applies in full — anchoring, pattern reference and grounding are not a `pages.strict` luxury — only the section and layout rules are relaxed
- `pages.canonical` names the page everything is compared against, the same axis `/fig:sync` resolves. `null` means it has not been settled for this file: resolve it once the way `/fig:sync` does, by name pattern or by the divider band it sits in, and ask rather than guessing per screen

## What this skill decides, and what it hands off

| Decided here | Handed off |
|---|---|
| Which pattern the thing being drawn follows | Discovering and composing components → `figma:figma-generate-design` |
| Which canonical screen it is anchored to | Building a master or a variant set → `figma:figma-generate-library` |
| Which page, section and name it lands under | Whether colours are bound to tokens → `/fig:tokens` |
| Where the copy came from | Whether it is placed and connected legally → `/fig:lint` |
| What is finished and what is still open | The skeleton and the to-draw list → `/fig:prep` |

## Pattern first — the file's own arrangement rules

**Inconsistency is rarely carelessness. It is what happens when there was nothing to refer to.** Draw an alert row today and a second one a fortnight later and both will be defensible; they will not be the same. Each was invented, because nothing in the file said how that kind of thing is arranged here.

That rule is a third thing, and it needs its own place:

| Layer | What lives there | The question it answers |
|---|---|---|
| Design system | the parts | what does a button look like |
| **Pattern page** | **how the parts are arranged** | **how is a list row built in this file** |
| Common page | one copy of a repeated state | what does a generic loading state look like |

`naming.pattern_page_pattern` names the page, `naming.pattern_frame_prefix` the frames on it. **Before drawing anything, look up the pattern for it** — the row of a list, the empty treatment inside a panel, the failure treatment of a control, the way a form reports a bad field. Three outcomes:

1. **The pattern is there** → follow it. Instance it where it is a component, clone it where it is not
2. **No pattern, but the file has two or more precedents** → derive the pattern from them, write it to the pattern page, then draw from it. This is the common case and the valuable one: the rule already existed, unwritten, and the second screen is where it either gets recorded or gets forgotten
3. **Nothing anywhere** → a new pattern has to be defined. It binds every screen after this one, so it is not a detail of this screen: propose it, say what it will bind, and take its own go. Where `references.sources` names a connected screen-reference service, look there first for how shipped products arrange the same thing, and let two or three of them inform the proposal — named in the proposal as what it was compared against. They inform an arrangement only: the parts still come from the design system, and copy never comes from another product's screen

**A pattern goes into a section on that page, not loose on the canvas.** The structure audit reports any frame sitting directly on a page, whatever the page is for, and it does not read page strictness to decide; the coverage exception that lets a pattern off the flow requirement only reaches frames that are inside a section. So both rules point the same way — one section per family of patterns, named to `naming.section_pattern` like any other.

**Cases 2 and 3 are a separate write, behind their own preview → go.** The pattern page is a different page from the one being drawn on, and a script may set the current page only once; an error also rolls the whole call back, so a combined write loses the screen along with the pattern. Two gates, two calls, in that order — pattern first, then draw from it.

**Where `naming.pattern_page_pattern` is `null`, propose creating the page.** That is what the setting means here: not a check to skip, but a convention the file has not adopted yet. Drawing on without it is how the next inconsistency gets made.

**The pattern that was followed is named in the report, and nowhere else on the canvas.** No annotation goes on the drawn frame for it — `/fig:lint` reads a reference annotation on a Default as *this screen's state is covered on the common page*, and a pattern reference sitting in the same place would be counted as state coverage that does not exist. The durable record is the pattern page itself.

**When a pattern is used often enough to harden, it graduates to a component** — that is `figma:figma-generate-library`'s work, not this skill's. The pattern page is where something lives while it is already a rule and not yet a component.

## Anchor to canonical, not to a blank canvas

**A component drawn on its own proves the component works. It says nothing about what the person opening the file sees.** A card with the right padding, alone on an empty canvas, cannot show whether it fits where it has to fit, what it displaces, or what the screen around it now looks like. A reviewer cannot approve from that file — they have to imagine the whole, and an imagined whole is exactly where a change that *should* work turns out not to.

So the target is drawn **inside** its nearest canonical relative:

1. **Find the nearest canonical relative** — the screen this target is a variant of, or for genuinely new work the closest screen in the same feature area. A brand-new domain still inherits the app's shell: the header, the nav, whatever chrome every canonical screen shares. Clone that much even when nothing else applies
2. **Widen the search before concluding there is nothing to anchor to.** The same move `/fig:prep` makes for a state-count baseline: a sibling page that looks empty is not *no canonical*, it is canonical one hop away. Look at the file this one was branched from, the product's main file, whatever the team's guide names. Only after that comes up empty is a screen built from shell components alone the right answer — and it is said plainly that that is what happened
3. **Clone the whole screen, not the fragment that changed**, and reparent it with `absorb()` so it lands as a real child of the target section rather than a page-level orphan
4. **Change only what the target describes**, on the clone, in place. Everything else stays as canonical drew it — the discipline `/fig:sync` already states for applying work in the other direction

What comes out is a frame someone can screenshot and hand over as *this is what it will look like*, because it is the screen and not a swatch of the new part.

## Reuse before inventing

Before drawing a state — an error, a disabled control, an empty list — **check whether the design system already answers it.** `search_design_system` first, by the component's own likely name (one word finds more than a description does); failing that, read how the same kind of state already renders on an existing screen. A file that shows a bad field with a red border and a line of text under it has already answered *what an error looks like here*. Drawing a different answer for the new screen is not a design decision.

Only when neither turns anything up is inventing right, and it is said openly — *no existing error variant, built one from the base input's border and colour tokens* — so the next person can tell a considered gap from an overlooked one.

## What's undecided stays inline, not blank

**A blank dashed frame is the right answer to "nothing here is known yet" and the wrong answer to "one fact here is not decided yet."** Most of what a stub stands for is not unknown: the layout follows from the screen type, the visual language from the design system, the copy from a spec or from how the same message reads elsewhere. What is actually undecided is usually one thing — a threshold, a line of copy nobody has signed off, a policy call. Blanking the screen for the sake of that one thing hides the ninety percent that was never in question, and hands the reviewer nothing to review.

So draw the real screen. Where one fact is genuinely unsettled, leave a plausible value **and pin it** on the exact node it lives on:

```
TBD (needs confirmation): <the question, specifically>
```

That is `/fig:prep`'s own wording, reused verbatim and deliberately: one search then finds every open question in the file, whether it sits on a stub prep left or on a screen this skill finished. **The annotation carries no category** — `task_tracker.annotation_category` belongs to `/fig:diff`, and an open question filed as a change is read as a change.

A target that really carries nothing decidable — a state nobody has spec'd at all, on a screen with no precedent to read — is the one case where handing it back as a stub is still correct. That is the boundary: **stub what nothing yet answers, draw what something does.**

## Ground content, don't invent it

Copy, labels and sample values come from somewhere real: the spec, the file's own precedent for the same kind of message, or — for content a running system produces — that system, read before drawing rather than guessed at. Text that sounds plausible reads exactly like text that is sourced, right up until a reviewer who knows the product opens the file.

**And it does not stop in the file.** The ticket's acceptance conditions are written from the design's structure and its copy, so a plausible string drawn here is a plausible string somebody builds against, checks off, and ships. Where nothing sources a piece of content and it is not itself a state-defining fact, say so rather than filling the gap to look finished — a value marked as unsourced beats a confident wrong one.

## Sketch the direction before the file

**A table of rules does not show anybody a screen.** A spec entry can be complete and still leave the person who asked for it unable to picture what they are agreeing to — and a write to a shared file is the most expensive place to find out they meant something else. So where the work changes how a screen looks or behaves — a new screen, a layout that moves, a flow that gains states — the direction is agreed in the conversation before a single node is written, and always in the same shape:

1. **The list of what has to be decided**, numbered, before the first question — so the size of it is visible
2. **One question at a time**, each with two or three lines of context and a recommended option. When an answer opens a question the list did not have — moving something out of a panel raises where it goes instead — ask that before moving to the next number
3. **A table once it is settled** — item │ decision — so the whole direction reads in one place
4. **A rough text wireframe for each moment the screen changes** — at rest, right after the action, while it is in progress, collapsed or returned, any secondary view — with one line under each saying what changed since the last. Labels inside the boxes are ASCII: short English words, or letters keyed to a legend written outside the box. A wide character (Korean, Japanese, Chinese) takes two columns in a monospace terminal and pushes every right-hand border out of line. Generate the lines with a short script rather than counting columns by hand, and mark any size as an estimate
5. **A transition tree** — which state follows which, on what input — with its vertical lines only at the left edge, for the same reason
6. **Two or three lines on what differs from today**

The sketch does not replace preview → go. It is what makes the preview something the person can judge: they are no longer weighing the direction and the details in the same breath. And a spec draft written before the sketch is agreed has the same problem one step earlier — values chosen by whoever drafted it, presented as if they had been decided.

**Skip it for a stub whose `TBD` already settled the layout**, where the canonical screen fixes the rest. There is nothing left to picture.

## Procedure

### 1. Take the target

A stub: read its name, its position, and its `TBD (needs confirmation): …` description. **That description is the interview `/fig:prep` already ran** — do not re-ask what it answered. A description instead of a stub: settle what screen, what state and what is explicitly out before drawing, and settle the spec (see Inputs).

### 2. Read the sources

The spec, the file's own precedent, and where the content is something a running system produces, that system. This is the step that decides whether step 7 writes sourced copy or invented copy, and it cannot be done afterwards.

### 3. Anchor to canonical

Per "Anchor to canonical" above. Name what was found and where, or name the search and say it came up empty.

### 4. Look up the pattern

Per "Pattern first" above, for each kind of thing being drawn. Cases 2 and 3 take their own preview → go and their own `use_figma` call, **before** the screen is drawn.

### 5. Sketch → agree

Per "Sketch the direction before the file" above, where the screen is about to look or behave differently. Nothing is previewed until the person accepts the sketch.

### 6. Preview → go

State the canonical source, the pattern each element follows, what changes on the clone, where the copy comes from, and what stays open and where it will be pinned. **Write nothing before the go.** One screen or one state per gate — redoing a wrong batch of five costs more than redoing a wrong one.

### 7. Draw the state

Clone, reparent with `absorb()`, then change only what is in scope. **Where the target was a stub, the clone takes the stub's exact name and position** — `/fig:arrows` drew the existing `-->` and `[state]` lines against that name, and a renamed or moved frame turns them into orphans, which `/fig:lint` grades blocking. Where the target is new, the name follows `naming.frame` **after the canonical screen it anchors to**, so `/fig:sync` can pair the two when the work is applied later.

### 8. Pin what is still open

Per "What's undecided stays inline" above. Draw first, annotate second, and never let one open question keep the rest of the screen from being real.

### 9. Verify

**The mandatory last action — call `/fig:lint` (via the Skill tool).** A clone happened, so this is never optional: get `STRUCT PASS` and `FLOW PASS`, fix what comes back, call again. Its `[mode]` check is the one a clone trips most: a screen cloned off a page that set the colour mode lands in the collection default.

**Call `/fig:tokens` in its check-only mode on every frame drawn, cloned or not.** A clone copies whatever its source carried, and a source that is itself a draft built earlier in the work — a component nobody has handed over yet — carries its hand-typed colours into every screen that uses it. Those colours looked right in the mode they were typed for, and disappear in the other. "It was cloned, so it is clean" is only true of a canonical source.

**Then render every frame drawn, together, and look.** One image of all of them at a reduced scale — the whole section, or several sections side by side — not a screenshot per frame. Each screen looked at alone passes; a dark screen among light siblings, an empty box where a label should be, a hover-only control left showing, are obvious only next to the others. Lint and tokens measure what they can name; this is where what nobody named turns up. Where the drawn frames span more than one page, the design tool's image export renders them in one request.

No audit lives in this file. The verdict comes from those two skills alone, the same way `/fig:prep` and `/fig:arrows` take theirs.

## Implementation — the parts that are not delegated

The preamble is `${CLAUDE_PLUGIN_ROOT}/_common/scripts/prep-ops.js`, the same as `/fig:prep`. Two things here are this skill's own; everything about composing components belongs to `figma:figma-generate-design` and is not repeated.

**Clone into place and retire the stub, in one call**

```js
const canonicalFrame = await figma.getNodeByIdAsync(CANONICAL_ID)
const stub = STUB_ID ? await figma.getNodeByIdAsync(STUB_ID) : null
const section = await figma.getNodeByIdAsync(SECTION_ID)
const clone = canonicalFrame.clone()
await absorb([[clone.id, section.id]])          // group+ungroup — survives local fonts, unlike appendChild
clone.x = stub ? stub.x : NEXT_X
clone.y = stub ? stub.y : NEXT_Y
clone.name = stub ? stub.name : `${SCREEN}-${STATE}`
for (const n of [clone, ...clone.findAll(n => n.annotations && n.annotations.length)])
  n.annotations = []                             // a clone carries every pin its source had, nested instances included
if (stub) stub.remove()                          // one frame at that position, never two
return { createdNodeIds: [clone.id], removedStubId: stub ? stub.id : null }
```

**Empty the clone's annotations in the same call.** A clone brings every Dev Mode annotation its source carried, down to pins on instances deep inside it — last round's change labels, navigation notes, open questions that were already answered. Nobody wrote them for this screen, they read as if somebody did, and they multiply with every clone of a clone. The same holds for anything cloned *into* a screen, a modal or a card taken from another frame: clear it the moment it lands.

**The only annotation this skill writes is the open question** (`TBD (needs confirmation): …`, see "What's undecided stays inline"). Everything else already has a home that is not the canvas — navigation is the flow arrows, before-and-after is the AS-IS section, rules are the spec, implementation notes are the ticket, and "this is a draft suggestion" is the spec entry's own marker. Writing any of them as a pin puts a second copy on the canvas that nobody updates when the first one changes. The same question pinned on several sibling frames is one pin, on the representative frame.

`absorb()` decides its coordinate correction from the parent **before** the call, so a node already inside that section is not shifted twice. Fonts are the reason it exists: text in a font that is not synced to the cloud cannot be moved with `appendChild` or `insertChild`, and the whole call is rejected.

**Pin an open question**

```js
const node = await figma.getNodeByIdAsync(UNDECIDED_NODE_ID)
node.annotations = [{ labelMarkdown: `TBD (needs confirmation): ${question}` }]
```

No `categoryId` — see "What's undecided stays inline". Annotations are visible in Dev Mode only, so a screenshot cannot confirm them; read `node.annotations` back.

## What the report says

```
[drawn]      page · section · frames, state variants included
[pattern]    followed {…} · derived from precedent {…} · newly defined {…} (what it binds)
[coverage]   N of the N states the target asked for · what is left and why
[sources]    where each string came from · values with no source
[open]       the question, and which spec entry it belongs to
[decisions]  what forked while drawing, for somebody else to settle
[gates]      lint · tokens · not handed over yet, no version pinned
```

Two of those lines exist for whatever files the ticket. `[drawn]` is a section-by-section frame list because the acceptance checklist carries **one step per screen**, state variants included, and it is built from this list rather than by reading the file again. `[open]` names the question and the entry it belongs to, and **stops there** — who decides it and by when belongs to the spec, and an owner invented here would read as an agreed one.

**Nothing in this skill pins a version or claims a handover.** The line saying a build matches the design and the version it matches travel together, and they are `/fig:handoff`'s to write once somebody saves the named version. Until then the report says so, in those words.

## Traps

| Trap | What to do |
|---|---|
| Drawing a component in isolation because finding the canonical screen is slower | Faster to draw, slower to review, and nobody can see it in place. Clone the screen |
| Reading "no finished screen on this page" as "nothing to anchor to" | Widen the search the way `/fig:prep` does — a sibling page, the branched-from file, the team's main file |
| Inventing an arrangement because no pattern page exists | That is the case the pattern page exists for. Derive it from precedent or define it, behind its own go |
| Rebuilding a row from scratch with absolute positioning | The file already answered how that row is built. Clone the working one — a rebuilt row with absolutely-positioned children lands on top of its own text |
| Writing the pattern and the screen in one call | One page per call, and an error rolls the whole call back. Pattern first, then the screen |
| Blanking a whole frame because one fact in it is undecided | Draw the rest for real. Pin the one node the open question lives on |
| Copy that reads plausibly | It ends up in the acceptance checklist. Read the spec, the system, or the file's own precedent, and mark what nothing sourced |
| Renaming or moving the stub's frame while filling it | The arrows were drawn against that name and position. Keep both, or fix the flow with `/fig:arrows` |
| Reparenting a clone with `appendChild` | Local-font text fails to load and the call is rejected. Use `absorb()` |
| Opening with a full preview, or a spec draft, whose values you chose yourself | The person has to judge the direction and the document at once, and usually cannot picture either. Agree the direction item by item, show the text sketch of each state, then preview |
| Pins that came along with a clone | Last round's labels read as this round's decisions. Clear the clone's annotations in the call that clones it, including those on nested instances |
| Explaining the screen in pins — navigation, before/after, rules, code notes | Each already lives in the arrows, the AS-IS section, the spec or the ticket. Pin only an open question, once |
| Calling it done on an isolated screenshot | The gate is `/fig:lint` plus a whole-section screenshot, as everywhere else here |
| Skipping `/fig:tokens` because every frame was cloned | A clone of a draft carries the draft's hand-typed colours. Check every drawn frame |
| Checking each drawn screen on its own | Render all of them in one image before reporting — a screen that is wrong only relative to its siblings looks fine alone |
| A cloned screen that looked right on its source page | It may have been borrowing that page's colour mode. Name the mode on the screen itself |

## Constraints

- **A change to how a screen looks is sketched in text and agreed before its preview.** A stub the canonical screen already settles is exempt
- **Preview → go before writing**, split per screen or per state, and a pattern write takes a gate of its own
- **`/fig:lint` and `/fig:tokens` after every run**, on every frame drawn — every run clones, and a clone carries whatever its source carried. Never report done without a `PASS`
- Sections matching `pages.exclude_sections` are never drawn into, and a page matching `pages.readonly` is refused
- Never invent an arrangement the file or its pattern page could have settled
- Never invent a fact a source could have settled, and never leave an unsourced value unmarked
- Never change anything on the cloned screen the target did not call for
- Never draw a new visual language for a state the design system already answers
- Never create an annotation category, and never file an open question under the one `/fig:diff` uses
- Never leave a cloned frame carrying its source's annotations, and never pin anything but an open question

## Notes

- This is the one skill in the bundle that writes new screens rather than tidying, checking or applying existing ones. Everything else here assumes this step happened
- A stub whose `TBD (needs confirmation): …` is itself ambiguous is a cue to ask, not to guess past. The interview already happened once, and re-running it on a guess moves the ambiguity downstream
- The spec is worth asking for even when it was not offered. A screen drawn against a real source and one drawn against what sounds about right look identical until somebody checks
