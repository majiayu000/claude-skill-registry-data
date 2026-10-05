---
name: writing-fragments
category: writing
description: >
  Mine the user for raw writing fragments — claims, vignettes, sharp sentences, half-
  thoughts — and append them to one document as material for a future article. Use when the
  user wants to develop ideas before imposing structure, or mentions "fragments" or "raw
  material".
codex-short-description: "Mine raw writing fragments into one document as material for a future article"
related-skills:
  - writing-shape
  - writing-humanize
loop-eligible: false

compatibility: claude-code codex opencode
---
<what-to-do>

Run a grilling session that produces fragments. Interview the user relentlessly about whatever they want to write about. Do not impose phases, outlines, or structure — that is explicitly out of scope.

As fragments emerge from either side of the conversation, append them to a single markdown file. The user will be editing this file during the session; always re-read it before writing so their edits are preserved.

If the user did not pass a path, ask once where to save the document, then remember it for the rest of the session.

On first write, put a single H1 at the top with a working title (it can change later) and nothing else — no metadata, no TOC, no date.

</what-to-do>

<supporting-info>

## What is a fragment

A fragment is any piece of text that might survive into the final article. It must be _readable by the author_ — the author can tell what it means — but it does not need to define its terms or be comprehensible to a cold reader. The bar is "is this a piece of good writing?", not "is this a self-contained argument?"

Fragments are deliberately heterogeneous. Examples of what could be a fragment:

- A sharp sentence you'd want to deploy somewhere but don't yet know where.
- A claim with a one-line justification.
- A vignette: a thing that happened, a code snippet, a scenario, an analogy.
- A half-thought: "something about how X feels like Y, work this out later."
- A quote, a piece of dialogue, an overheard line.
- A list of related observations that hang together by feel.
- A complaint, a confession, a punchline.

The novelist's diary is the model: years of unstructured noticings that later get mined for raw material. Fragments are noticings.

## How the session feels

Like a grilling session, with fragments as a by-product. The shape:

- Start by asking what the user is circling around. Let them ramble.
- Catch fragments from their words. When they say something quotable, capture it verbatim or slightly sharpened.
- Generate candidate fragments back at them. Try things on. Offer two or three versions of the same idea and let them pick or reject.
- When something lands, append it. When it doesn't, drop it.
- Press for more. Excavate. "You said X — say it three different ways." "What's the version of that you wouldn't say in public?" "What's the example that made you believe this in the first place?"
- Push on quality. The article will only be as good as its fragments. If a fragment is mushy, propose a sharper rewrite before appending.

Blue-sky generously, but apply pressure to deepen and tighten. Do not rush to outline. Do not group. Do not propose a structure. If the user starts asking about structure, redirect: "We're still mining. Structure comes later."

## File format

```markdown
# Working title

A first fragment lives here.

It can be multiple paragraphs. It can include lists, code, quotes — whatever
shape the fragment naturally takes.
---

A second fragment.

---

> A quoted line that the user wants to keep around.

A reaction to it.

---

- A cluster of related observations
- That hang together by feel
- And want to be near each other
```

Fragments are separated by a horizontal rule (`\n---\n`). No headings inside the body. No tags. No order beyond the order they were added.

## Writing rhythm

Append silently. Don't ask permission for each fragment. Mention what you added in passing ("adding that"), but don't interrupt the conversation with save dialogs.

Before every write: re-read the file from disk. The user may have edited, reordered, or deleted fragments between turns — preserve their changes. Never overwrite the file; only append (or, if the user asks, edit a specific fragment in place).

The user can say "cut the last one", "rewrite that one sharper", "merge those two" at any time. Treat those as first-class instructions.

## Out of scope

- Outlines, section plans, paragraph structure, transitions.
- Deciding the article's thesis, argument, or audience.
- Producing prose that reads as finished writing.
- Linking fragments together with connective tissue.

If the user is ready for any of that, the session is over and a different tool takes over. Do not name or recommend that tool — just stop.

</supporting-info>

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/writing-fragments.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
