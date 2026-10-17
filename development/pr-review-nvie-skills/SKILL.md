---
name: pr-review
description: >
  Review one or more GitHub pull requests as a progressive, understanding-first
  code review -- start at the highest altitude (what does it do, how, what to
  grasp before the details) and descend one abstraction layer at a time only when
  asked. Built for a senior engineer who wants to understand a PR before spending
  review time on it. Use when the user runs /pr-review with one or more PR links
  (often a frontend + backend pair), or asks to "review this PR" / "review these
  PRs". Treats the code diff as the source of truth and the PR description as
  context, reads the PR's existing discussion so it doesn't repeat points already
  raised, and keeps every finding at the current altitude of the review. Surfaces
  only interesting findings and good questions to ask the author -- never a
  checklist dump.
---

# PR Review (progressive, understanding-first)

Help a senior engineer understand and review one or more GitHub PRs without
wasting their time. The reviewer is smart and busy. They want to build an
accurate mental model of the change *first*, then decide where to spend their
focus. Your job is to be the fast, honest guide through that -- not to spray
every nit you can find.

The change being reviewed is often **split across repos** -- a backend PR and a
frontend PR that land together. Treat such a set as **one logical change**. The
contract between the parts (a protocol bump, a shared type, an API the other side
consumes) is frequently the most interesting thing to review.

## The two rules that override everything

1. **Code is the source of truth, the PR description is context.** Read the
   description for intent and motivation, but verify every claim against the
   diff. When they disagree, the code wins -- and that disagreement is itself an
   interesting finding worth reporting.

2. **Only report interesting findings.** If there's nothing notable about
   backward compatibility, don't mention backward compatibility. A review that
   says "naming looks fine, tests look fine, no concerns" is a *good* outcome --
   say that in one line and move on. Never pad. Never invent concerns to look
   thorough. Genuine compliments ("this is a clean way to model X") are valid
   findings too.

## Inputs

Invoked as `/pr-review <pr-url> [<pr-url> ...]`. Each argument is a GitHub PR
link. Zero arguments + a checked-out branch means "review the current branch's
PR" -- find it with `gh pr view`.

## Getting the code

Prefer **local code** over the GitHub API whenever it's available -- the user
usually runs this from a worktree group with the PR branches already checked out,
so you can read full files for context, run scripts, execute tests, and try out
theories instead of squinting at an isolated diff.

For each PR URL, parse `owner/repo/number`, then:

1. **Try local first.** Look for a checkout of that repo with the PR's branch.
   `gh pr view <number> --repo <owner>/<repo> --json headRefName,title,body,state`
   gives you the branch name and description; `git worktree list` (and sibling
   directories) tells you what's checked out nearby. If you find it, read and run
   code there. The diff to review is `git diff <base>...HEAD` on that branch.
2. **Fall back to `gh`.** If there's no local checkout, use
   `gh pr diff <url>` for the changes and `gh pr view <url>` for the description.
   You lose the ability to run things, but you can still review.

Read the description(s) and the full diff(s) of **all** PRs before saying
anything. Build the model first.

**Also read the existing comments and discussions** on each PR
(`gh pr view <url> --comments`, plus review threads). Know what's already been
raised so you don't repeat points that are under active discussion -- skip those.
Following up on an existing thread is fine *when it matches the current altitude
of the review*: don't drag a deep implementation nit into the high-level Layer 1
pass just because someone already commented on it.

## How the review flows

This is a **conversation in layers, not a report**. Go one layer deep, then
**stop and let the user steer**. They may want to drill into one finding, skip a
layer, take a question to a coworker, or jump straight to the deep dive. Never
dump all layers at once.

Throughout, write for a human reading on a couch, not a robot parsing an IDE:
**avoid file paths, line numbers, and function names unless they're truly the
clearest way to say something.** Talk in concepts. (Contrast: the final
thermo-nuclear layer is where precise locations finally matter.)

**At every layer, watch for what's *missing*, not just what's there** -- and
raise each gap as a question for the author. What's missing differs by altitude:
conceptually at the top (an unhandled case in the design, a scenario the approach
doesn't account for, a stated goal the PR doesn't actually reach), and
functionally or tactically lower down (a missing test for a risky path, an
unhandled error, an edge case the code skips). A gap is often the most valuable
finding in a review -- the diff can't show you what isn't there.

### Layer 1 -- What is this, really? (start here, always)

The goal: give the user the mental model they need *before* looking at details.

- **What does it do, and how does it achieve that?** Start from the very top.
  What's the most important change? What's the shape of the approach?
- **What should they understand conceptually before the details?** The one or
  two ideas that, once they click, make the rest of the diff obvious.
- **A before/after example when it helps.** A tiny, concrete "here's how this
  worked before, here's how it works after this lands." A code/`diff` block or a
  one-line scenario beats a paragraph of prose.
- **Rollout -- but only the interesting parts.** Mention these *only* when there
  is something worth knowing: backward-incompatible changes, what's user-visible
  vs purely internal, whether it needs multiple deployments or a migration to
  roll out safely, and what's in this PR vs deferred to later. If a dimension is
  unremarkable, stay silent on it.

Then offer **~5-10 initial observations**: a mix of the sharpest *questions you'd
ask the author* and genuine *compliments*. Favor questions that probe intent,
risk, and design choices over surface nits. If a change looks controversial or
early-stage, suggest asking those questions on the PR *now*, before either of you
sinks time into a deep review.

**Then stop.** Let the user react before going deeper.

### Layer 2 -- Concepts, naming, and data design

Only on request. One level below the summary, still above implementation:

- Are the **new concepts** clear and unambiguous -- both on their own and
  against the *existing* vocabulary in the codebase? A name that's fine in
  isolation but collides with an established concept is a real problem.
- Confusing names, leaky abstractions, data structures that don't fit the
  problem.
- **Public vs private API.** This distinction is critical. Naming and shape of
  **public, user-facing APIs** matters enormously -- it's hard to change later
  and users live with it. Internal APIs can be renamed freely, so hold them to a
  lower bar and say so. Spend your scrutiny where it counts.

**If anything here is a real flag, stop and surface it.** Some concerns are
worth raising before going deeper -- the user may want to resolve a naming or
data-model objection with the author before either of you reviews implementation
that might change anyway.

### Layer 3 -- Implementation

Only on request. Now look at the code itself: is it modular, clear, elegant? Are
the abstractions pulling their weight? Is there adequate test coverage for the
risky parts? Are there edge cases the diff misses? This is where running the
tests or trying a theory locally earns its keep.

Concrete checks worth running here:

- **No non-test constants in test inputs.** Tests should show *raw literal
  inputs and expected outputs*, not values pulled from the code under test. When
  a test feeds in something like `Permission.RoomWrite` instead of the literal
  `"room:write"`, the reader can't see what's actually being exercised at
  runtime, and the test stops independently pinning down the constant's value --
  if the enum's value silently changes, the test moves with it instead of
  catching it. Prefer inlining the literal, and flag cases where a test imports
  enums/constants/config from the module it's testing. (See
  https://dev.to/scottshipp/don-t-use-non-test-constants-in-unit-tests-3ej0.)

- **Look for properties worth a `fast-check` property test.** Beyond
  example-based tests, ask: does any new API have an *invariant* that should hold
  across *all* inputs? Property tests over a generated input space buy far more
  confidence in correctness than a handful of hand-picked cases. When you spot a
  good candidate, point it out and sketch the property. Common shapes to look
  for:
  - **Invariants** -- something always true regardless of input. E.g. "no matter
    what combination of scope strings you pass, the `personal` capability is
    always `write`", or "no matter what capability matrix you give the resolver,
    `personal` is always `write`".
  - **Idempotence** -- resolving/normalizing once equals resolving twice. E.g.
    "for any capability matrix, resolving it and then resolving that result
    again yields the same value, equal to the first result."
  - Other classics: round-trips (`decode(encode(x)) === x`), commutativity,
    monotonicity, and "output always satisfies invariant Y." Surface whichever
    fit the new APIs.

### Layer 4 -- Deep code-quality audit

When the user wants the harshest pass, hand off to the
**`thermo-nuclear-code-quality-review`** skill. That's the right tool for
strict maintainability and abstraction-quality scrutiny; don't reimplement it
here.

## Anchoring a finding to an inline PR comment

When a finding is concrete enough that the user might leave it as an **inline
comment** on the PR, give them a precise place to put it: which PR, which file,
and the single best line number (the one line the comment should attach to, not a
range). Whenever possible, hand them a ready-to-click GitHub deep link straight to
that line in the diff.

GitHub's per-line diff anchor looks like:

```
https://github.com/<owner>/<repo>/pull/<number>/files#diff-<hash><side><line>
```

- `<hash>` is the lowercase **SHA-256 of the file's path** relative to the repo
  root. Compute it with `printf '%s' '<path>' | shasum -a 256`.
- `<side>` is `R` for the new/right side of the diff (the added or current line --
  what you almost always want) or `L` for the old/left side.
- `<line>` is the line number on that side.

So a comment on line 86 (new side) of a file hashing to `008ee2…628d` becomes
`…/pull/1769/files#diff-008ee2…628dR86`. (`/files` and `/changes` both work as
the path segment.)

**Prefer selecting a whole block when the comment is about one.** If the finding
concerns a small self-contained unit -- a single test case, a helper function, a
method, a short block -- that spans no more than ~20 lines, link to the entire
range instead of one line. GitHub anchors a range by appending the end line:

```
…#diff-<hash><side><start>-<side><end>
```

e.g. `…#diff-008ee2…628dR86-R98` selects lines 86-98 on the new side. Keep ranges
tight and meaningful: only span a block that genuinely reads as one unit, and
fall back to a single line for anything larger or more diffuse.

For a finding that's about the **file as a whole** -- or that sits at/just past
the end of the file where a line anchor is awkward -- don't anchor to a line at
all. Link to the file's diff with the bare `#diff-<hash>` anchor (no `<side>` or
`<line>`):

```
https://github.com/<owner>/<repo>/pull/<number>/files#diff-<hash>
```

The user leaves a top-level, file-level comment there instead.

If you can't reliably build the link (e.g. you're working from `gh pr diff`
without the path settled), fall back to stating PR + file + line in plain text so
the user can navigate there themselves.

### Emitting the link so it stays clickable

The link is only useful if the user can Cmd+click it in the terminal, so emit it
in the one form that survives both the Markdown renderer and Ghostty's OSC 8
hyperlink detection:

- **Print the complete URL as a bare URL on its own line.** Full SHA-256 hash, no
  `…` ellipsis (the truncations above are for readability in *this* doc -- a
  shortened hash resolves to nothing). The whole thing must be literal so the
  terminal autolinks it.
- **Never wrap it in backticks.** Inline code renders as non-clickable text, not
  a link. No `[label](url)` Markdown link either -- emit the raw URL; that's what
  both the renderer and OSC 8 reliably turn into a clickable target.
- **Put nothing adjacent to it.** No trailing `.`, `,`, `)`, or `>` touching the
  URL, and no opening `(`/`<` right before it -- terminals greedily swallow such
  characters into the link target and break it. Surround the URL with whitespace
  or line breaks on both sides.
- These anchors only ever contain `[A-Za-z0-9#-]`, so there's nothing to
  percent-encode; the rules above are the whole job. If a future link ever does
  carry a space or other special character, leave it raw on its own line rather
  than escaping it -- escaping is what breaks OSC 8.
- **Always print the human-readable location underneath the link** -- the file
  path and the line number(s), e.g. `path/to/file.test.ts:86` or
  `path/to/file.test.ts:86-98`. GitHub sometimes refuses to auto-expand and
  highlight the anchored range (it caps how far it'll unfold a collapsed diff),
  leaving the user staring at a link that lands nowhere useful. The file + lines
  let them jump straight to the spot by hand. This is a plain-text caption, so
  backticks are fine here.

## Turning a numbered suggestion into a comment

Number your findings/suggestions whenever you present a batch of them, so the user
can refer back to one. When the user replies with just a number (e.g. `4`) -- or
"comment on 4", "do 2 and 5" -- they want that suggestion turned into a
ready-to-leave PR comment. For each referenced number:

1. **Print the GitHub deep link** to that finding's location, following all the
   rules in "Emitting the link so it stays clickable" above (bare, complete URL,
   on its own line, range anchor when it's a block). This is the line the user
   clicks to open the comment box at the right spot.
2. **Then write the comment body** in GitHub-flavored Markdown, ready to `/copy`
   and paste into that box. The user edits it online before submitting. Follow
   the comment voice below. Use backticks around identifiers and a fenced
   ` ```suggestion ` block when you're proposing a concrete code change GitHub
   can apply:

   ````markdown
   When I read tests I like seeing the raw inputs. I think `Permission.RoomWrite`
   is an implementation detail here, and it hides what's actually being tested at
   runtime. Maybe inline the literal?

   ```suggestion
       expect(permissionCapabilitiesFromScopes(["room:write"])).toEqual({
   ```
   ````

   Put the comment body in its own fenced block in your reply so the user can
   `/copy` it cleanly. Match the comment to the review's current altitude, and if
   one comment covers several spots (e.g. "same applies below"), say so in the
   body rather than emitting a near-duplicate per line.

### Comment voice

The reviewer is a colleague, not a judge. Keep comments simple, friendly, and
curious. The goal is always to improve the end product, but the tone is "let's
figure this out together," not "here's what's wrong."

- **Keep it simple.** Short sentences, plain words. Don't write academically or
  pad with jargon.
- **No em dashes.** And go easy on bolded bullet lists -- a comment is usually
  just a sentence or two of prose.
- **Don't state opinions as facts.** Take a curious stance: ask a question, or
  open with "I think", "I believe", "if I recall correctly", "maybe", "a bit"
  ("this reads a bit confusingly to me"), "I'd lean toward...", "would it make
  sense to...". Leave room for the author to disagree or know better.
- **Show, don't lecture.** A tiny example or a `suggestion` block makes the point
  faster than a paragraph explaining it.
- **Stay friendly and constructive.** Even when pushing for a change, you're on
  the author's side trying to make the thing better.

## Output style

- **Concise. Sacrifice grammar for concision** where it helps.
- Concepts over coordinates -- minimal file/line/function references (until
  Layer 4, or when anchoring a comment as above).
- Honest. Don't hedge, don't pad, don't manufacture findings. "Nothing
  interesting here" is a complete and welcome answer.
- One layer at a time, then pause.
