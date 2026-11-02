---
name: pr-description
description: Write a concise, informal PR description summarizing this branch's diff, organized by area of change to help manual review. Use when the user asks to write/draft a PR description, or summarize a diff for review.
---

# PR description writer

Produce a PR description from the diff of the commit range the PR covers, once
that range is confirmed with the user (see Scope).

## Rule 0 — conciseness is the main parameter for correctness

Above every other rule here: between two phrasings of the same fact, the
shorter one is the correct one. A bullet is one clause where one clause will
do. Cut every word whose removal loses no information — qualifiers ("now",
"already", "end to end"), parentheticals spelling out steps, and trailing
clauses naming when or where something happened.

- No filler phrases ("found along the way", "as part of this effort", etc.) — cut anything that doesn't change what the reviewer needs to know.
- No incidental stats (line counts, "N import sites updated", etc.) unless they materially help review.
- No implementation-level specifics (exact function/type names, internal mechanics) unless the bullet is meaningless without them. Prefer "small fixes to X handling" over naming the specific enum/refine/helper that changed.
- Before handing it over, re-read the draft against this rule and the leave-out
  list: if a bullet survives only as rationale, consequence or emphasis, delete
  it. Expect to cut, not to add.

- ❌ "Dataset export now encodes the tree through the psps-dto and bigint-safe
  codecs on every hop (client body → route → RPC), so an int64/uint64 dataset
  exports instead of throwing at request time."
- ✅ "Dataset export encodes through the psps-dto and bigint-safe codecs, int64
  datasets export instead of throwing."
- ❌ "Native `JSON.parse`/`JSON.stringify` are banned by lint across both
  workspaces; the sites that legitimately use them carry a reason, and unit
  tests and Cypress specs are exempt."
- ✅ "Native `JSON.parse`/`JSON.stringify` are banned by lint across both
  workspaces; exceptions carry a reason, unit tests and Cypress specs are
  exempt."
- ❌ "Key-path comparison and map keys are consolidated into one helper,
  replacing the ad-hoc stringify comparisons and two joined-string prefix
  checks that matched across segment boundaries."
- ✅ "Key-path comparison and map keys consolidated into one helper, replacing
  stringify comparisons."

Cutting is not shortening every bullet uniformly: a bullet that means nothing
on its own is cut entirely, not trimmed. "Export sends the same component
payload shape as write and copy" tells a reviewer nothing by itself — fold it
into the bullet it qualifies, or drop it.

A bug fix reads defect first, then what closed it — otherwise the bullet names
a behavior with no visible problem.

- ❌ "Validation rejects non-finite values; the serializer throws instead of
  writing `null`."
- ✅ "A non-finite value reached the saved file as `null`; validation and the
  serializer now reject it."

## Never use the em dash

The character `—` is banned from the output. Use a comma, a colon, parentheses,
or two sentences.

## Describe the shape of the change, not an inventory of its parts

The reviewer already has the file list; the diff shows every path added, deleted
and renamed. Repeating it is the one failure mode that matters here. Your job is
the part the diff **can't** show: what the change did structurally. Report it
flatly — you are summarizing, not advocating, steering or reviewing.

So a bullet says what happened, not which files it happened in:

- ✅ "removed the planning docs and combined the guides into a single document"
- ❌ "dropped plan X, inventory Y and decision record Z; the surviving guide now covers A, B and C"
- ✅ "consolidated the four component loaders into one"
- ❌ "deleted `loader-a.ts`, `loader-b.ts`, `loader-c.ts`, added `loader.ts`"

Corollaries:

- **Never recap the contents of a changed doc or module** — its sections, what it
  now covers. That the guide exists and absorbed the others is the change; its
  table of contents is not.
- **Name a path only when it's the useful anchor for a bullet** — one file a
  reviewer should open, a rename that would otherwise read as delete + create.
  Not as a way to list what's in the diff.
- **A deletion is one bullet, however many files it spans.** "PCS dropped its own
  server layer and route handlers" — not the five routes by name.

## Scope — establish the commit range before writing a word

**Never infer the range.** Run `git log --oneline <base>..HEAD` first. If the
user didn't say which commits the PR covers and that range holds more than one,
**ask** (`AskUserQuestion`, offering the candidate ranges — the whole branch,
the last commit only, a specific commit or range) and wait for the answer. A
description written for the wrong range describes a different PR than the one
being opened, so it is worse than no description at all. The same applies when
the base itself is unclear: ask rather than assume `develop`.

- Describe **only the diff of the confirmed range**, not the base branch's history. Confirm with git what's actually new/changed there (e.g. `git diff --stat <base>...HEAD`) — don't assume from memory or from a file's current content alone.
- Never attribute a file/feature to this PR if it already existed on the base branch. Conversely, never narrate what earlier/other PRs did as context — that's git history, not something this PR's reviewer needs. If a file was renamed or moved in this PR, verify it (e.g. `git log --oneline --follow -- <path>`, `git log --diff-filter=D -- <old-path>`) — a big diff on one path and a full deletion on another is often a rename, not "gutted" or "new."

## Format

- Short bullets grouped by area of change, not prose paragraphs.
- One line per change, not per file — several files moving together are one bullet.
- Say what changed, not how or why in detail.
- Informal, easy to read — this is for someone scanning before they read the diff, not a spec.

## What to leave out

The first draft is almost always too long, and it's always too long in the same
ways. Cut these:

- **A fact already stated in another section.** State it once, in the section it
  belongs to. If the store section says the model now tracks a sequence number,
  the backend section doesn't repeat it.
- **Trailing "so that…" clauses.** The consequence of a change, or the interface
  it leaves behind, is not part of the change. "extracted a common dialog shell —
  layout, folder tree, item details, confirm/cancel" is done; "…so both editors
  supply only a filter row and a confirm handler" is not.
- **Sub-details of a change already stated.** Once the extraction is a bullet,
  the props it exposes and the call sites it touched are not further bullets.
- **Enumerated states and options** — which chips are enabled, which variants
  exist, what each flag value does. Inventory in a different costume.
- **Cosmetic changes:** label and copy renames, a button being disabled, styling
  tweaks. They're in the diff and they don't shape a review.
- **Commentary about the diff itself** — how git will render a rename, why a
  stat looks odd, which commit did what. State the rename; skip the tooling
  aside.
- **Rationale and defense.** Why a design was chosen, why a bug was silent, why
  a test was added. A reviewer forms that judgment from the diff.
- **Reviewer steering** — "worth a look", "note that", "this is the risky part".
  Every bullet gets equal weight; let the reviewer prioritize.
- **Test and CI status.** Whether suites pass, what's still unverified. That's a
  message to whoever asked, not part of the description.

## Verify before writing

Get the facts right before describing them:

- Check `git diff --stat <base>...HEAD` for the actual file list and change sizes.
- For any file whose story seems surprising (fully rewritten, deleted-and-recreated elsewhere), check rename/history before describing it — don't guess.
