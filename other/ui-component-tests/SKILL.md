---
name: ui-component-tests
kind: rule
law: verifiability
description: Ready-made code and the order of checking a kit component and an application screen. Take it on a *.spec.ts next to a component, a frame in the end-to-end suite, a failed showcase snapshot and when deciding what confirms a layout edit. The "why" — testing and browser-verification.
---

# Checking a kit component and an application screen — the ready-made code

This tree's rule, not from the package. It does not repeat `testing` and `browser-verification` —
there it is said what counts as confirmation and where in the tree what lies. Here is what to write
by hand and in what order to run it.

**Cold part:** `pitfalls.md` next to it — measurements, numbers and cases from sorted-out
snapshots. Loaded on demand, not together with the rule.

## When it is taken

Creating or editing a component's spec, creating a story for the sake of checking a state, creating
a screen frame in the end-to-end suite, sorting out a failed snapshot, editing the snapshot harness,
a conclusion about layout.

## What answers which question

Four checks do not replace one another, and the choice between them is not a matter of taste.

| Question                                              | What to answer with                                       |
| ----------------------------------------------------- | ---------------------------------------------------------- |
| Did the state come about? Did the input arrive? Did the output fire? | a spec — the pattern `ui-component-tests-spec`   |
| Does the component look the same as before?           | a story snapshot — the pattern `ui-component-tests-visual` |
| Does the whole screen look the same?                  | a screen frame in the end-to-end suite — the pattern `testing-e2e` |
| Do the padding, the font size and the colour match the reference? | a measurement of computed values — `browser-verification-measure` |

- **A spec is silent about how it looks.** The class in the markup matches, while the padding is
  eaten and the label clipped — the run is green. A styling edit is confirmed by a snapshot, not by
  a spec.
- **A snapshot is silent about why it diverged.** It catches everything visible at once and says
  "it became different"; what exactly moved is answered by a measurement.
- **A measurement answers only the question asked.** The numbers match until somebody asks about
  the background on hover.

## How the law applies here

- **A wave of showings is closed by a sweep over all the stories, not by the colour of a run.**
  Green specs, a green taking of references and a green audit of the input tables together do not
  answer whether there is anything in the frame at all. Between "the run passed" and "what was shown
  is shown" there is nothing in this tree but the sweep — `pnpm run test:stories:v2`, sorted out in
  the pattern `ui-component-tests-visual`.
- **The sweep opens the overview pages too, and by the same call.** Nothing else opens them at all,
  so an error there stays invisible while every check of the tree is green. A sweep of their own
  would part from this one at the first edit of a wait.
- **The showing root is chosen by the mode, not by the first node a chain of selectors finds.** Both
  containers stand in the markup of any page at once, and the idle one has zero area: a chain
  returns it and calls an empty frame on a page that drew everything.
- **A check written for the wave judges the wrap, not the sighting.** It answers the question it was
  written to ask — every showing of one instance carries the pair — and stays green where the pair
  shows nothing: the frame root has an area, so the showing counts as drawn while both halves are
  empty. Such a
  check narrows what has to be looked at; it never replaces the look.
- **A state invisible in the frame is not checked by a snapshot.** A button under hover, a panel in
  an overlay, the branch after a file is chosen — they exist in the markup and not in the snapshot.
  Such a state gets a story of its own rather than being credited with a neighbour's coverage.
- **A state's sign is checked by the same thing a person sees it by: a frame or a measurement of
  the raster, not by the value of a written style.** A style set on a node proves only that it was
  set; whether it applied depends on what the showing registered.
- **A `play` step that asserts a node exists proves nothing about what is seen.** A 2x2 box exists
  as surely as a 400x300 one. A component that draws a surface asserts its size against a lower
  bound, not its presence.
- **If there is a pair of states, both must be in the frame.** A reference showing one side of a
  pair says nothing about the pair itself and stays green under any breakage of it.
- **A styling edit that passed the snapshots without divergences is half checked.** A small element
  takes hundredths of a frame; the comparison threshold can let it through. The sign is the share of
  the divergence, not the colour of the run.
- **A settled frame is waited for by an event, not by a countdown, and the technique is repeated in
  every harness.** A countdown checks the machine rather than the layout. What are waited for are
  signs independent of the machine's load: the fonts are up, the motion is stopped, the network went
  quiet, the size of the node being shot did not change over two frames in a row.
- **A wait that swallows its own refusal takes the frame too early.** Not having waited, it silently
  lets the shot go on, and the frame goes into the comparison without what was awaited. A wait's
  refusal costs a line of sorting out, a diverged snapshot a whole session.
- **A wait waits for what is awaited, not for its consequence.** A sign that comes about without the
  awaited thing stays silent instead of refusing: an icon's wait class takes the page's font
  readiness, and that comes about with an empty set too — the font declarations themselves never
  arrived, there is nothing to wait for, and the wait passes on a page with no icons at all. Such a
  wait does not swallow a refusal — there is simply nowhere for one to come from. What is waited for
  is the same subject the refusal is about: the families themselves, the node itself, the state
  itself; an indirect sign is taken only when there is no direct one, and then it is named together
  with what it does not cover.
- **An arrived resource and the component that noticed it are not the same, and both are waited
  for.** The font came up, while the icon component learns of it by its own signal and stays
  invisible until the redraw: between the two lies a race, and the frame lands in it. A wait knowing
  only the cause shoots into that gap; one knowing only the consequence stays silent where there was
  no cause. Each gets its own refusal, and it names which half broke.
- **A settled layout is not yet a drawn page, and the frame is taken after two in a row match.** The
  harness can wait for the sizes, the fonts, the network's silence and finished animations, and the
  frame still diverges by sub-pixel halos on the labels, and the browser gives no "the page is
  drawn" event. Two identical frames in a row say the same
  thing and are checked directly.
- **A settled page and a drawn page are different, and the frame waits for the second.** An
  animation frame's handler runs **before** the drawing, so a wait spinning such a cycle lets the
  shot go into the gap between "the layout settled" and "the frame was drawn". A frame taken in that gap diverges from
  the reference steadily, and a cycle of matching frames does not cure it: two early frames match
  each other no worse than two late ones. So what is waited for is the drawing itself —
  a nested pair of animation-frame calls, the second of which stands already past the drawn frame. A
  probe of its own guards the rollback, not the snapshots.
- **A value that comes from the machine is caught by two raisings of the showcase, not by one run.**
  Inside one raising it stands still, so a repeated run on the same showcase confirms nothing.

- **A size the kit did not declare is taken from the browser's default, and that default is not a
  constant.** A frame that moved with no edit is asked first whether the kit declared that size.

- **A divergence that falls out rarely leaves evidence, otherwise there is nothing to sort out.**
  The harness puts the difference frame and the run's conditions — the matching attempt, the window
  and page sizes, the point density, the worker's number — into a directory outside the repository,
  which the next run does not touch.
- **A shot beyond the window touches the page under the shutter, and that is cured not by a cycle
  but by the window.** A frame wider or taller than the window the browser takes by substituting the
  window for the duration of the frame: the page gets a `resize`, and everything computed from the
  window sizes moves right inside the frame. A cycle of matching frames pins the breakage instead
  of curing it: the shift is steady. The cure is the reverse order: the window is widened
  **before** the frame, the showing is waited for settled, and an ordinary frame is taken. In the reference `100vh` and `100vw` of such a story are
  then computed from the widened window.
- **A frame of a node beyond the window is cured the same way.** A node taller than the window goes past its bounds no less. The window is
  widened to the node being shot, not to the page: the page happens to be higher than the node, and a superfluous growth changes everything computed from the window at
  stories that did not ask for it.
- **The trace of such a shot is left at the story after the tall one.** The page keeps the shift, so
  the divergence lands on a neighbour whose content nobody touched, and rearranging the stories
  moves frames nobody edited. What tells one from the other is a measurement of the node before the
  frame and after it: a height that changed across the shutter names the shot, not the layout.
- **A frame is assembled from what lies in the tree, and the harness cuts the shot off from a
  foreign network.** What travels from outside brings a foreign availability into the frame, and
  the snapshot then diverges where nobody touched the layout. An article about it is too little: the
  harness fails the run on a request beyond the local machine instead.
- **A settled showing and a state that came about are not the same, and a story is waited for by the
  second.** A screen with skeletons has a size as motionless as a screen with a list, so the shared
  harness cannot tell them apart. The sign of the state is known only to the story — the node that
  exists in it and the node that no longer does — and the story waits for it by a `play` step.
- **An overlay opened by a story lives to the frame only where that is declared.** There is nothing
  to tell such a frame from a story that should have no panel at all — it is green and looks whole.
  So a story names the overlay's node as a shot parameter: the harness mutes the pointer leaving on
  its page and refuses when it does not find the promised node by the moment of the frame.
- **A wait removed from the harness is guarded by a probe, not by the snapshot run.** The run
  matches a frame against a reference taken by that same harness, so both move together and the run
  stays green on the miss. So such a wait is guarded directly: the probe reads whether the call
  stands in the harness and whether it stands after the shot, then holds back what is awaited on its
  approach and matches the frame before the wait against the frame after it. The first half catches
  a rollback by an edit, the second a rollback in substance: the call is in place, and it waits for
  the wrong thing.
- **A probe judges the markup it was created for.** A miss happens with one kind of markup and not
  with a neighbouring one, and a probe that took the wrong story is green on an unfixed harness. So
  it not only opens the story but asks it: is this the markup — and refuses when the story changed
  it for a neighbouring one.
- **A probe judging by one measurement inherits the very rarity it guards against.** A single match
  refuses a push on a tree with nothing to answer for, while the same command passes green on the
  next call. The measurements are taken one after another until they diverge; the refusal comes
  only when they all matched, and it names how many were taken.
- **A probe names the state of the showcase it was pointed at, not only the state of the harness.**
  A showcase goes stale by itself: after a branch switch its hot update loses a chunk, and every
  story hangs at preparing. A probe that dies there with the bare failure of a wait speaks of its
  own code, so the gate refuses a push for a reason that is not true. The wait is wrapped, and its
  refusal names the address, the count of the showing roots, whether the story is still preparing
  and which requests the showcase refused.
- **A probe reading the harness as text separates the code from the explanations.** A word search
  over the whole file finds them in a commented-out line too: a call taken out by one slash reads as
  live, and the probe stays green on exactly the rollback it stands for.
- **A reference is taken after the frame has been looked at, not before.** A shot pins down what got
  drawn: an empty frame becomes the sample, and afterwards the run is eternally green on emptiness.
  The order is one — a raised showcase, the eyes, then the reference. References are taken in a
  batch only for stories that have already been looked over.
- **A re-taken reference is confirmed by a second raising before it is committed.** A frame taken
  once says what the machine drew in that minute, not what it draws, and nothing in the browser's
  configuration pins the difference. Otherwise an unsteady re-take reaches the main branch.

- **A reference is re-taken deliberately and one at a time.** Re-taking everything at once erases
  the divergence that was not expected too.
- **A reference is taken from the same showcase the gate raises.** The tree assembles two, and at
  one markup their raster differs by a point or two. From the wrong one a reference comes out green
  here and red at the gate.
- **A frame is taken by the drawn span, not by the node's box.** A node shot clips the border box:
  a cell sticking out of the grid is cut in silence, alike in both halves of a pair. The span is
  clipped by whatever scrolls, and the window grows to its edges — never to a pinned width.
- **A one-off check script does not travel into the repository.** It lives in a temporary directory.
  A check called on the next wave too lives next to the snapshot runner, as a separate command.
- **A branch the spec does not reach is named in the PR.** A silent gap looks the same as coverage.
- **An application screen is closed by an end-to-end suite frame, not by a showcase story.** A story
  shows a component without the dictionary, the store and the route, while a screen diverges more
  often between its components than inside one. So a screen is shot where a user opens it: on a production build
  behind a stand, as a whole page, by the same path of clicks as the other end-to-end specs, and
  next to them — in that screen's spec rather than in a separate file "about snapshots". A window
  frame instead of a whole page clips a panel that went past the bottom edge, and the loss of half
  of it reads as "nothing has changed".
- **The end-to-end suite writes no settled-frame wait of its own.** The end-to-end spec runner mutes
  the motion, hides the caret, waits for the fonts and takes frame after frame until two in a row
  match pixel for pixel — the very thing the showcase harnesses do by hand. The showcases write it
  by hand because their runner does no such cycle at all: there a frame is taken once and matched at
  once. The difference is in the runner, not in the screen's steadiness, and a cycle of one's own
  next to it would be a second answer to one question — they would diverge silently.
- **Screen frames have no step of their own in the gate or in the pipeline.** They are taken inside
  the end-to-end suite's step, which stands in both already. A separate step would raise the stand a
  second time, and a neighbouring stand on the same machine makes the outcome of the shot a matter
  of chance. The showcases' frames have a step of their own precisely because they need no stand at
  all.
- **What drifts in a screen frame is removed by name, not covered by a threshold.** A threshold lets
  an eaten padding through together with the drifting value, so it is held at zero and the cause is
  looked for to the end. The order of sorting out is one: compare the frames pixel by pixel and see
  where exactly they diverged and by how much. What each kind of divergence means — the cold part.
- **A mask covers the content but not the width.** A column under a mask takes its place as before,
  and a drifting value inside it moves its neighbours past the mask. What drifts is cured in the
  seeding — by a constant value — and then no mask is needed at all.
- **Not only time is made constant but everything the application derived from it.** The application
  computes the derivative — the month key, the deadline, the freshness sign — at the minute of
  writing, so a seeding that edits the times after the write leaves it as it was. Otherwise the frame
  turns red months later on a day when not a line was added to the tree. The sign is visible by
  comparing two columns: the derivative stopped matching what it had to be derived from.
- **The seeding checks itself instead of relying on the frame.** The frame says "it became
  different" and is silent about why; a seeding refusal names the reason in words and arrives at the
  stand's startup, before a single frame is taken. The sign is taken so that it holds on any run
  day: the stand's data is the past, so a time value that landed on the run day or later was
  computed by the machine clock and not pinned by the seeding. A deliberate future — a far expiry
  date — is separated by a boundary and named apart.
- **The self-check judges the time columns of every table the screens read, not only those shown
  today.** A column is put on screen by one line of markup, and there is nobody to remember the
  seeding then: a check assembled by what is shown lags behind by exactly that line.

## The order

1. A spec on the behaviour — the input, the output, the state. The ready-made skeleton is the
   pattern `ui-component-tests-spec`.
2. A story for every visible state not yet in a frame — the pattern `ui-component-tests-visual`.
3. A sweep over the stories and a look at the frames by eye — before the first taking of references,
   otherwise the shot pins down emptiness.
4. A run of the specs, then `pnpm exec nx run @rt-tools/ui-kit-v2:typecheck`, then the snapshots,
   then the measurement — if the edit is about layout. Jest compiles without checking types: an
   import of a symbol that does not exist passes a green spec run.
5. A number in the PR: how many tests ran, how many snapshots matched, what the measurement showed.

## Commands

```bash
pnpm exec nx test @rt-tools/ui-kit --testFile=<path>   # one spec file
pnpm test                                              # the specs of all packages
pnpm exec nx run @rt-tools/ui-kit-v2:typecheck         # the types of the component and its specs: Jest checks neither
pnpm run check:affected                                # the same as the guard asks before a push
```

The snapshots go against an **already raised** showcase: their own is not raised, and the address is
overridden by `STORYBOOK_URL`.

## Two showcases — two snapshot harnesses

There is not one shared file between the kits: they are kept apart deliberately, and an edit for the
second one's sake would fail the first one's references.

|                     | `@rt-tools/ui-kit`                             | `@rt-tools/ui-kit-v2`                            |
| ------------------- | ---------------------------------------------- | ------------------------------------------------ |
| Showcase            | `pnpm run storybook:ui-kit-v1` — port 6006     | `pnpm run storybook:ui-kit-v2` — port 6007       |
| Snapshot harness    | `projects/ui-kit/.storybook/test-runner.ts`    | `projects/ui-kit-v2/.storybook/test-runner.ts`   |
| References          | `projects/ui-kit/.storybook/__snapshots__`     | `projects/ui-kit-v2/.storybook/__snapshots__`    |
| The audit           | `pnpm run test:visual`                         | `pnpm run test:visual:v2`                        |
| Pointed re-take     | `pnpm run test:visual:update <path sample>`    | `pnpm run test:visual:v2:update '<path sample>'` |
| Re-take of all      | `pnpm run test:visual:update`                  | `pnpm run test:visual:v2:update-all`             |
| What gets shot      | every story                                    | everything but what is marked `storySnapshotSkip` |
| The frame's area    | the whole page                                 | the showing root `[data-story-root]`             |
| Sweep over stories  | —                                              | `pnpm run test:stories:v2`                       |

The second showcase's agreement is `docs/specs/ui-kit-v2/`; the story parameters are
`src/showcase/story-snapshot.ts`, and how to set them is said in the rule `rt-tools-storybook`.

## Pitfalls

- **A green target does not mean the spec ran.** `passWithNoTests` is on: a package without spec
  files passes successfully. The number of tests is read from the report.
- **"Couldn't find story … after HMR" is a trace of hot reloading, not a defect.** The showcase is
  restarted, the code is not edited.
- **The pointer outlives the move between stories.** A hover from one arrives in the next one's
  snapshot: a story without a hover takes the pointer away into a corner.
- **A focused button outlives the pointer taken away.** The kit's tooltip opens on focus too, and a
  closed menu returns focus to its button, so `expectScreen` blurs a focused button or link before
  the shot. A field keeps its focus: that focus is part of the frame.
- **A story's values arrive at the wrapper later than its `ngOnInit`.** An initial state computed in
  the hook by the story's value is computed by the field's default. The needed state is reached by a
  click in `play`, not by an input.
- **A series of runs does not tolerate edits of the tree under it.** Hot reloading shoots the edited
  file, not the measured one; a merge, a commit and a stash restore count as edits. A series runs on
  a motionless tree, and one touched by an edit is restarted clean.
- **The stand's database outlives a run.** The specs create records dated by the run day, so the
  seeding's self-check stands inside the seeding, not after the suite.
- **A frame without a reference in the end-to-end suite is written by Playwright on the first run.**
  `updateSnapshots` stays at its default, so the second run is green against whatever was shot. The
  file is looked at against the mockup, and the index is read before the commit.
- **Sorting out a failed snapshot starts with the share of the divergence and the area.** A red run
  comes both from a shift of one pixel and from a lost block — by eye on the picture that is
  indistinguishable.
- **The snapshot container draws a fallback family without its semibold face.** A title bold in the
  mockup and regular in the frame is not a defect: the weight is checked by the computed
  `font-weight` in the end-to-end spec, and the divergence is named in the task record.

## Patterns

- `ui-component-tests-spec` — a ready-made component spec: the fixture, the second kit's harness,
  the doubles.
- `ui-component-tests-visual` — a story for the sake of a snapshot, a sweep over the stories,
  sorting out a failed run.
