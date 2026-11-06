---
description: >-
  Review the prose you added in recent work — code comments, docstrings, and
  Markdown — against four equal defects: **existence** (it should not have been
  written at all), **durability** / **narration** (it narrates the change
  instead of the code's lasting contract), **tightness** / **bloat** (it spends
  more words than it informs), and **negation** / **polar bear** (it denies a
  thing the change removed, so the mention survives as its own denial). Rewrites,
  moves and cuts in place. Invoke as: /tend-prose [lens] [optional focus
  guidance] — naming one of the four, by either of its names, runs only that
  lens.
---

You are reviewing prose _you_ recently added — code comments, docstrings, and
Markdown (skill bodies, `docs/`, READMEs) — for four defects that carry **equal
weight**:

- **T**ightness — text that spends more words than it informs: it restates what
  the function name, signature, and types already convey, or stretches a real
  point past the length it needs. CLAUDE.md's docstring rule: document only the
  non-obvious contract (side effects, runtime constraints, cross-boundary
  coupling, don't-change-this traps).
- **E**xistence — text that should not have been written: a description of how
  the code works rather than a constraint on it, something a reader recovers
  from the code itself, or a real constraint filed where nothing will load it.
- **N**egation — text whose subject is a thing the change removed, surviving as
  its own denial instead of being removed altogether. It is written in clean
  present tense, so it reads as a constraint and no change verb fires. The idiom
  is _don't think about the polar bear_.
- **D**urability — text that describes the change that produced the code rather
  than the code's durable behaviour, whether it narrates against the state
  before the branch or against an earlier step inside it. CLAUDE.md: "Comments
  describe the code's lasting contract, not the change that produced it."

They are listed in the order that spells **TEND**, which is a memory aid only.
Step 2 has no order — it applies all four to each line in one pass — and Step 3
fixes in the opposite direction from this list: deletions before rewrites before
trims, so you never shorten a sentence you are about to cut.

The output is **edits, not a report**. Fix the clear cases in place; only ask
about genuinely ambiguous ones.

This skill is the long version of CLAUDE.md § "Writing things down", and the
only home for these rules.

## Single-lens mode

The argument may **name one lens**, optionally followed by focus guidance:
`/tend-prose durability`, `/tend-prose tightness src/db`,
`/tend-prose polar bear`.

1. `existence`
2. `durability`, alias `narration`
3. `tightness`, alias `bloat`
4. `negation`, alias `polar bear`

Then run **only** that lens: skip the other three in Step 2 and apply only its
fixes in Step 3. This is the mode for "I just saw narration in there", and for a
bare `polar bear here` on a PR comment — a targeted pass, not the full sweep.

With no lens named, all four run.

## When to use

- After an autonomous run (several commits since the operator last engaged),
  before handing back — all four defects accumulate step-to-step.
- When the scoped work **removed** a module, file, field or concept that prose
  described. That is the condition lens 4 exists for, and the only one that puts
  a defect in prose nobody rewrote.
- Any time you notice a comment reads like a diff note, or a docstring restates
  its own signature. If that is the whole complaint, name the lens.
- Skip if recent work added no prose (pure logic/test edits with no new
  comments).

## Step 1: Scope to what you added since the operator last engaged

In order:

1. **Uncommitted changes**: `git diff HEAD` + untracked files
   (`git status --short`).
2. **Commits since upstream / since the operator's last turn**:
   `git log --oneline @{u}..HEAD`, or the SHA range the session summary names.
   `git diff <range>` is the scope.
3. **Nothing matches** → tell the user there's nothing to review and stop.

Only the **added/changed** prose lines are in scope for lenses 1–3 — don't
rewrite pre-existing comments you didn't touch. Lens 4 is the exception, and
reads the other side of the same diff:

**Collect the removed nouns** once the range is fixed. From the removed lines
(`git diff <range>`) and the deleted files
(`git diff --diff-filter=D --name-only <range>`), list what the change took
away: identifiers, file paths, field and type names, and named concepts. Grep
each against the post-change tree. **A name that survives only inside prose is a
lens 4 candidate** — the code no longer has it, so any sentence still about it
is about nothing.

**Skip this sub-step when the diff removes nothing** — most additive work — so
the ordinary pass pays nothing for the lens.

## Step 2: Read each added prose line and ask all four questions

A line can fail any of the four, or several. Work through the diff **once**,
applying all four lenses to each comment — not one traversal per lens. (In
single-lens mode, only the named one.) Lens 4 also ranges over prose the diff
did not touch, since a sentence that survived a removal is exactly the one
nobody rewrote.

### Lens 1 — should it exist at all?

The default is not to write it. Prose costs context on every session that loads
it, and it goes stale invisibly — a constraint survives a refactor, a
description of how the constraint works does not.

Keep it only when **all three** hold:

1. It is a **constraint or an accepted cost**, not a description of how the code
   works.
2. It is **not recoverable** from the code and its docstrings by someone reading
   them — _or_ recovering it means taking in more modules and flows at once than
   anyone holds in their head, where a paragraph gets there faster. Even then,
   the candidate is a **docstring at the topmost point of the code**, not a
   separate file.
3. **Getting it wrong breaks something** — you can name the specific way a
   future editor goes astray without it.

Then check it is in the right home, and **move it if it isn't** — a rule that
only one call site can violate is a comment; a page nobody's glob reaches is
nothing. The homes, in order of preference — take the first that fits:

1. **A comment at the call site** — a trap that lives at one line.
2. **A docstring at the topmost point of the code it describes** — how a flow
   works, when following it means holding more modules in your head than fit at
   once.
3. **The skill or hook whose run it governs** — a step, or a rule that only
   binds while that process runs.
4. **The directory's own `CLAUDE.md`** — an obligation every edit in that
   directory's files must respect, loaded on the first read there.
5. **`.claude/rules/<area>.md`** (frontmatter `paths:`) — the same, for files no
   single directory bounds — `'**/*.test.ts'`, several scattered paths.
6. **A colocated `README.md`** — the big picture, for when not having it is
   itself what blocks the edit.
7. **A runbook page** (`docs/runbook/*.md`, or the project's equivalent) — a
   procedure a human executes.

**A line in the root `CLAUDE.md` answers one question before any of these**:
CLAUDE.md § "About this file"'s test, since that file loads on every turn. A
line that fails it moves to the first home above that loads when its process
runs.

**The alternatives already live in the PR or issue thread, and any of these
homes can cite it.** Add a `#1234` beside the line where a reader would
otherwise stop and wonder "hmm, why this and not the obvious thing?"; leave it
off where nobody would ask, because a citation on an unsurprising line is one
more thing to chase.

**Rule or README?** A rule — homes 4 and 5 alike — is what every edit in the
files it covers must respect _whether or not the editor went looking_ — an
obligation you can violate without noticing. It loads automatically, so it must
stay short and always-relevant. A README carries the part the code cannot:
**why** the arrangement is this one, where reading the modules end to end still
leaves the reason obscure. It is opened on purpose, by someone who has already
noticed they are lost, and it runs as long as that explanation takes. **The
default is a rule**; reach for a README when the obscure _why_ is the thing
worth writing, and spending every matched edit's context on it would be the
wrong trade.

**Never create a new top-level doc without asking the operator** — and when you
ask, argue the "don't" side. A top-level doc is the one home nothing scopes, so
every later session pays for it; an operator waving it through is easy to get
and is not the same as it being right. If nothing in the list fits, that is
usually the signal it does not need writing at all.

**Touching documented code is not a reason to edit the doc.** Edit a rule when
the _constraint_ changed — not when code near it moved, was renamed, or grew a
feature. A rule that names a function, module path or column is already suspect:
name it only when the rule is _about_ that name.

### Lens 2 — is it narration?

A line is narration when it only makes sense to a reader who knows an earlier
state of the code — the state before the branch, or a step inside it. Tells:

- Change verbs anchored to the past: **"no longer"**, **"now also"**, **"used
  to"**, **"previously"**, **"migrated from"**, **"this used to…"**, **"as of
  this change"**, **"renamed from"**.
- **"for now" / "temporarily" / "once X lands"** — situational hedges that go
  stale.
- References to a prior step, ticket, or version as if the reader is watching
  the diff.

The test: **would this sentence still be true and useful to someone reading the
final code a year from now, with no memory of the edit?** If it only informs
"what changed", it's narration.

**The special case is narration against an intermediate step inside the
branch.** In shipped prose it is the same defect as the rest of the lens. It
earns a name because it is the half that survives in the documents Step 4
excludes: a commit body is _meant_ to narrate the branch against the state
before it, and still has no business reporting what a draft became on the way
there (`@.claude/skills/squash-message/SKILL.md` owns that pass).

### Lens 3 — is it bloat?

A line is bloat when it costs a reader more than it tells them — either they
already had the fact from the name, signature, and types, or the fact is real
but buried in twice the prose it needs. Tells:

- **Restates the signature** — names the params or return type, or paraphrases
  the function name (`/** Fetches the user by id. */` over
  `fetchUserById(id: string)`).
- **Narrates the next lines of code** — "Loop over the items and set the flag",
  "If the list is empty we skip".
- **Restates a type's or enum's members** in prose sitting next to the
  declaration.
- **Ceremony** — "This function is responsible for…", "Helper that…", "Note
  that…" wrapped around one actual fact.
- **A docstring block on something that crosses no boundary** — the contract is
  already obvious from name + types, so the block is decoration.
- **Length**: **> 4 lines** is almost certainly too much; find the one or two
  facts that aren't self-evident and keep only those. Even exactly 4 is too much
  unless it's a proper docstring block on a function/class/etc. **A good inline
  clarification fits ~2 lines.** The point is often real and the prose still too
  long:
  - "We await this before returning, because otherwise the transaction may still
    be open by the time the caller commits, which can deadlock under concurrent
    writes." → "Await before returning — an open transaction here deadlocks
    concurrent writes."
  - "It's worth noting that this cache can only be used on the server, since the
    key includes the workspace id and the browser bundle has no access to it." →
    "Server-only: the cache key needs the workspace id."
- **Markdown**: an added paragraph that re-explains what the adjacent bullet or
  code block already shows; a "Note:" restating the rule directly above it.

### Lens 4 — is it about a thing that isn't there?

When a change removes something the prose described, the reflex is to **negate
the sentence in place** rather than delete it. The mention survives as its own
denial, and every later reader pays for a thing that is not there. Tells:

- **A subject from Step 1's removed-noun list.** The name survives only inside
  prose; grep says the tree no longer has it.
- **A negated predicate in clean present tense** — "X is not a Y", "nothing
  generates X", "X is not a segment". No change verb, which is exactly why lens
  2 waves it through. Step 3's negator sweep is its search.

The test: **with the sentence gone, would its subject have crossed the reader's
mind at all?** If the sentence is the only reason they are thinking about the
thing, the sentence is what put the bear there — which is Dostoevsky's point in
_Winter Notes on Summer Impressions_: set yourself the task of not thinking
about a polar bear, and the cursed thing comes to mind every minute. Denying a
removed thing sets the reader that task.

**The discriminator — constraint or residue.** This is where the lens
over-deletes if you run it on the tells alone, because a codebase's prose is
properly full of negative rules. Apply the test and the two separate cleanly: a
constraint's subject is something the reader reaches for **anyway**, so it
crosses their mind with or without the sentence.

- _"Dev artifacts go under gitignored `tmp/`, not as new `.gitignore` entries."_
  — a **constraint**. The next editor reaches for a `.gitignore` line whether or
  not anything was ever removed. Keep it.
- _"Copy is not a segment — every string sits in the module that renders it."_ —
  **residue**, if the copy catalogue was just deleted. Nobody reading the
  current tree would propose a catalogue; the sentence exists to answer the
  draft that had one. Cut it.

Same grammar, opposite verdicts: residue guards against something a previous
draft did, which no longer threatens anyone.

**A change whose point is removing something is where bears breed, and whoever
has the removed thing in mind — its author, or a reviewer reading the `-` lines
— cannot tell whether a fresh reader would think of it.** On such a change,
judge each candidate against the resulting file with the diff closed, and read
every line touching the removed behaviour's situation, not only the negator
hits: once a skip for branches that hold all the work is gone, "it runs after
every turn, a branch that holds all the work included" denies the skip without a
negator. A call still close after that goes to the operator, who reads the
result rather than the history.

## Step 3: Fix

**Existence:**

- **Delete** when the line describes how the code works, or restates something a
  reader recovers from the code — that is the most common outcome and it is a
  clean one.
- **Move** when the constraint is real but mis-homed: a rule only one call site
  can violate becomes a comment there; a paragraph of orientation in a rule
  becomes a colocated README; a procedure becomes a skill. State it once in its
  new home rather than in both.
- **Keep** a named trap beside the thing it traps, and a decision's alternatives
  in the PR thread with a `#1234` from the docstring that needs them.

**Narration:**

- **Rephrase to a present-tense property** when the underlying fact is durable:
  "The emoji is no longer parsed" → "Nothing parses the emoji." "Now also sets
  `x`" → "Sets `x`."
- **Delete** when the note carried no lasting information beyond the change
  itself ("Migrated from the old helper", "Renamed for clarity").
- **Keep** genuine forward-references to still-pending work (e.g. "§F2 is
  deferred") and durable rationale phrased in the present ("kept in sync by hand
  because…"). These are contracts, not changelog.

**Bloat:**

- **Cut to the non-obvious facts** — the side effect, the runtime constraint,
  the coupling, the trap. Drop every clause the name and types already carry.
- **Downgrade a docstring block to a one-line inline comment inside the
  function** when its only real purpose is a don't-break-this warning —
  CLAUDE.md says the dev editing the code will see it there, and that's enough.
- **Delete entirely.** This is a normal outcome and often the right one; a
  comment the code already makes true earns nothing by being shortened.
- If you can't say it in ~2 lines, question whether the **code** should be
  clearer rather than the comment longer.

**Negation:**

- **Delete.** A sentence whose whole content is that something is absent has
  nothing to restate positively, so this lens cuts where the others rewrite.
- **Keep the fact, drop the denial** where the mention carries a live fact
  alongside it. Rephrase as what _is_ there: "The mark is not generated —
  `public/aeapp-mark.svg` is committed" → "**One committed
  `public/aeapp-mark.svg` serves every consumer**", the page, the favicon and
  the Open Graph card alike.
- **Keep** a negative sentence that passes the constraint-vs-residue
  discriminator. A rule against a temptation the reader has anyway is a
  constraint, and cutting it is the false positive this lens must not produce.

**Resolve in this order** — existence, negation, durability, tightness (1, 4, 2,
3): the two deletion verdicts first, so no rewrite or trim is ever spent on a
line that is about to go.

**Then sweep the result for negators.** The order above runs lens 4 before the
lens that manufactures bears: durability's own fix turns "the emoji is no longer
parsed" into "nothing parses the emoji". So once every fix is applied, grep the
**resulting** text of each prose line in scope — every added line, plus whatever
lens 4 read outside the diff:

```bash
git diff -U0 <range-start> -- <files> | grep '^+' \
  | grep -niE "\b(not|no|nothing|none|neither|nor|never|nobody|without|cannot)\b|n't\b"
```

`<range-start>` against the working tree, so the uncommitted fixes are what gets
read. Only comments and Markdown prose count: a flag (`--no-sandbox`), a string
literal or a code span is code, and code is never a bear.

**The grep proposes; the discriminator decides.** Most negative sentences in a
codebase are constraints, so every hit goes through the constraint-vs-residue
test above, and only residue is fixed, by the negation fixes. A `no longer` hit
is a durability miss: rephrase it there, then put the rephrasing through the
same test.

The sweep belongs to lens 4 and runs wherever it does. It also runs after a
`durability` single-lens pass, over the lines that pass rewrote.

## Step 4: Do NOT touch

- **Commit messages and PR bodies** — narrating the branch is their job.
- **`docs/plans/*.md`** — transient by nature, swept at finalize.
- **`docs/remove-before-merging/<branch>/squash-message.md`** — a commit body,
  and transient by nature.
- **CHANGELOG / release-notes files** — a dated record of changes is the point.
- **Deliberately thorough reference prose** — length carrying rationale the
  reader can't get elsewhere is not bloat; length carrying nothing is. But that
  describes a colocated `README.md`, opened on purpose, not a directory's
  `CLAUDE.md` or a `.claude/rules/*.md` file: **a rule's length is a budget**,
  because it loads in full every time a file it covers is read. Paragraphs of
  rationale in a rule are a lens 1 finding — the orientation belongs in a README
  the rule links to.

## Step 5: Commit

Commit the edits, with the fixes and their reasons in the body.
