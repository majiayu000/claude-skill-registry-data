---
name: to-writing-style
description: "Turn the developer's rewrites and rejections of reader-facing prose an agent wrote (Google Docs, blog posts, in-app text, academic writing) into proposed updates to the writing style sheets (docs/writing-voice.md, docs/writing-craft.md, docs/academic-writing-style.md) and to the piece-spec grilling doc (docs/pieces/grilling.md). Mines a session transcript (this session or another agent's), or a Piece's Agent draft against its edited Deliverable. Not for code, comments, commits or agent docs; those go to /to-code-style."
disable-model-invocation: true
---

Legend: 🪤 what the developer changed · 📝 what to write.

Mine a session, or a Piece's Agent draft against its edited Deliverable, for **prose rulings**: every place the developer rewrote, struck or rejected reader-facing prose an agent wrote ([defined in `prose-files.md`](../../../docs/agents/prose-files.md#terms)). Propose the edits to the three style sheets ([`docs/writing-voice.md`](../../../docs/writing-voice.md), [`docs/writing-craft.md`](../../../docs/writing-craft.md) and [`docs/academic-writing-style.md`](../../../docs/academic-writing-style.md)) and to the grilling doc, [`docs/pieces/grilling.md`](../../../docs/pieces/grilling.md), that would let the next draft come out right.

The spine test, applied to every candidate:

> **Propose only what a doc could have told you before the draft was written.**

What a piece _says_ (its facts, its argument, which section goes first in this one Doc) belongs to that piece, but the grilling question that would have drawn it out before the draft belongs in the grilling doc. A ruling about _how prose sounds_, for this piece or any, belongs in a style sheet, even though it was decided this session. A retro that restates the developer's edits has failed even if every line is true; the rule is the generalization of the edit.

Do steps 0-3 silently. The developer sees only step 4.

## 0. Pick the mode and inputs

- **A repo and a writing issue number** (`<repo> <n>`): pair mode on the Agent draft of `<repo>#<n>`. The parent spec's number covers the whole Piece; a sub-issue's covers only its Sections.
- **Two Doc names, IDs or URLs**: pair mode on those Docs, for an older Piece with no Agent draft.
- **No argument**: transcript mode on this session.
- **A session ID or path**: transcript mode on that transcript.
- **"The last session"**: transcript mode on the newest transcript that is not your own, found by [`docs/session-transcripts.md`](../../../docs/session-transcripts.md).

Say in one line which mode and which inputs you chose.

**Pair mode**: run the setup in [`pair-mode.md`](./pair-mode.md) before step 1. The diff is the evidence; transcripts only attribute its changes.

**Transcript mode: the transcript is the only input.** Do not read Doc comments or suggestions, and do not diff a Doc's current text against the agent's draft. The agent's drafts are in the transcript already, in its replies and in the `text` of its gworkspace tool calls.

When the session is not yours, also:

- **Read the user's turns before anything else**, with the command in [`docs/session-transcripts.md`](../../../docs/session-transcripts.md), which also says which `type:"user"` entries are the developer's. Then read the agent's drafts only around the corrections.
- **Check every candidate against the style sheets as they are now.** A later session may have added it already. `git log -- docs/writing-voice.md docs/writing-craft.md docs/academic-writing-style.md docs/writing-voice docs/writing-craft docs/academic-writing-style` shows what changed since.

## 1. Hunt

Name every instance of these kinds. Be relentless: the one the developer stated outright surfaces on its own, and stopping there is the failure mode.

- **Rewrite**: the developer pasted back the agent's prose in their own words, or told the agent how to reword it. Set the agent's draft beside the version the developer wrote into the session and name each difference: a cut hedge, a split sentence, a word swapped, an example added, a list turned to prose.
- **Rejection**: the developer struck a passage, or refused a draft without saying how to fix it. Name what the struck text had that the kept text lacks.
- **Stated rule**: a preference the developer articulated. Scan their turns for "I prefer", "never", "always", "don't say", "sounds like an AI", or a correction of a phrase the agent proposed.
- **Broken rule**: a draft that broke a line the style sheets already hold, which the developer then fixed. It goes in as a sharpened line, not a new one.
- **Addition**: the developer added or cut content the spec never held: a fact, a verdict, what they rely on, a before and after, which facts go first. Name the question that would have drawn it out during the grill.

**Weight repeated corrections heavily.** The same fix made twice is a habit the agent's default voice brings to every draft, and the strongest case for a rule.

In your own session you saw the developer's edits. In another's you infer them, from:

- a developer turn that quotes or pastes prose back;
- a developer turn that names a word, a phrase or a habit;
- the agent's next draft changing in a way no turn explains, after a developer turn you skipped.

Tag each item `observed` or `inferred`, and rank `inferred` lower. If a ruling sounds situational ("for this Doc", "here"), quote the developer's words and do not generalize it; you cannot tell whether it was meant as a rule.

**In pair mode**, hunt the paired list from setup. Each changed paragraph is a Rewrite, a struck one a Rejection, an added one an Addition, and a fix of a line the style sheets hold a Broken rule; a Stated rule counts only where an attributing transcript holds one. Tag each item `diffed`, upgraded to `observed` where a transcript states the developer's reason. The same fix made in several places in one Piece is a repeated correction. Drop an edit the diff can't tell apart as voice or fact as `ambiguous`; a fact correction never becomes a style rule.

**Code-style rulings are not yours.** A ruling on code, comments, commits, PRs, agent docs or READMEs goes to `/to-code-style`; drop it here with that reason. A ruling on a chat reply or a Doc meant only for the developer goes to neither; drop it as out of scope.

Done when every rewrite, rejection, stated rule, broken rule and addition is either carried to step 2 or dismissed with a stated reason.

## 2. Keep what passes all four tests

- **Beforehand**: could a style sheet have stated this before the draft was written? (A fact the piece got wrong fails here. A ruling on voice passes.) An addition fails for the style sheets but passes for the grilling doc when a question asked before the draft would have drawn it out.
- **Ownership**: is it already in a style sheet or the grilling doc now, or assigned to an issue? Leave it there and say so; do not write it twice.
- **Style, not rubric**: is it how the prose should read, not a constraint of this one piece's venue (a word limit, a template, an assignment's required headings)? A venue constraint fails.
- **Separates**: would the agent's draft (in pair mode, the Agent draft) have broken the proposed rule? A rule the draft already follows fails: it does not tell the draft from the developer's edit.

## 3. Route and rank

Route each ruling to one of three sheets. The **Craft test** splits the first two: would a good writer with a different voice still follow it? Yes sends it to Craft; no keeps it in Voice.

- **`docs/writing-voice.md`**: how the developer sounds, for every kind of reader-facing prose. A ruling lands here when it fails the Craft test and is not an academic convention. One voice: never add a section per medium.
- **`docs/writing-craft.md`**: what any skilled writer does, whatever their voice: a garden path, an undefined term, new before given, a clashing idiom. A ruling lands here when it passes the Craft test and is not an academic convention.
- **`docs/academic-writing-style.md`**: citations, academic register, academic structure. A ruling lands here only if it applies to academic work and would be wrong in a blog post or in-app text. A ruling that overrides a Voice or Craft line for academic work goes here, and says which line it overrides.
- **The rule line** goes under the style sheet's existing section that fits, in its shape: one bolded line, the rule only, plus at most a short clause of scope or its one exception ([rules file](../../../docs/agents/prose-files.md#terms)).
- **The instance** goes in the reasoning file whose row in the style sheet's "When | File" table matches the rule's topic, under a `##` heading named for the rule. Match the file's bullets, `- "<quote>" — <source>`: for a rewrite, one bullet `- Agent: "<draft>" Developer: "<version>" — session <short id>, <date>`. A pair-mode instance ends `— <repo>#<n> Agent draft, <date>` instead, `<date>` being the Agent draft commit's date; mined from two Docs, it names the agent's Doc in place of `Agent draft`. Close a new heading with `- No count was recorded; from a session.` (in pair mode, `from an Agent draft.`), and leave `docs/writing-voice/sources.md` and every "Seen in" count alone: those describe the Drive samples, not sessions.

- **A grilling question** goes in the grilling doc's `## Questions` list, in its shape: a bolded label, what to ask, and the session's instance as `(<Piece letter>: "<quote>")`, by the letter the doc's Questions lead gives the Piece, or the next free letter for a new one. The quote is the real wording, with each name, institution, amount and spec number replaced by a neutral stand-in, as the doc's examples are (`Sam`, `Example Credit Union`, `$N`). A change to the calibration step edits `/grill-piece`'s step 4 instead, through `/writing-for-agents`.

Rank by how often the correction recurred, and say so. A ranked list lets the developer take the top three and stop.

## 4. Present, then wait

One block per item, most valuable first, numbered so the developer can answer "1, 3, skip 2":

```
🪤 **W1** - **<title>** (rewrite | rejection | stated rule | broken rule | addition; observed | inferred | diffed): the agent wrote "<draft>"; the developer changed it to "<version>" (or struck it, or said "<their words>"). (session ab12, 22:53)

📝 `docs/<sheet>.md`, "<section>": **<the exact rule line>**

📝 `docs/<sheet>/<file>.md`: <the instance to add, in a code block>

---

🪤 **W2** - ...
```

Number grilling-doc items `G1`, `G2`, … in the same shape, after the `W` items, with the 📝 half naming `docs/pieces/grilling.md`.

- The 🪤 half quotes what the agent wrote and what the developer did, with no fix in it. The 📝 half says what to write, with no story in it. Either half should read alone.
- Give the wording, not a description of it. The developer is approving the edit, not the idea.
- The `(session ab12, 22:53)` pointer is for another agent's session: the short session ID and the timestamp of the turn, so the developer can check it. A pair-mode item cites `(<Piece>, <Section>, ¶<n>)` instead.
- A `diffed` item's 🪤 half gives your reading of the developer's reason as "likely because…", and says when the change was a reviewer fix the developer approved.
- End with one line for what you dropped: `Dropped: <item> (situational), <item> (code style: /to-code-style), <item> (already in writing-voice.md)`.
- In pair mode, close with an `Upstream:` line naming each skill or step that added text the developer struck, and what it added, or `Upstream: none found.` File and edit nothing for it; the developer decides whether to follow up.

Then stop. Do not edit until the developer approves; an agent running this skill does not approve for itself.

## 5. On approval of items

The Agent draft stays as `/implement-piece` committed it, and the edited Deliverable stays in its Doc, in both modes.

Write only the approved items, then `npx prettier --check` the touched files and `npm run lint`. Then ask whether to commit, and on which branch in each repo touched: the reviewed session may have left work in flight, and a docs-only commit should not ride along with it.
