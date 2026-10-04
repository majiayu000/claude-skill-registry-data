---
name: contents
description: "Generate a table of contents for the current conversation in one of two modes. Faithful mode (default) produces a navigable index of the chat's actual structure — chapter-numbered segments named by topical content, useful for scrolling back to specific moments in a long session. Retrospective mode produces a book-of-this-chat — chapter titles naming what each segment was *actually doing* in the chat's arc underneath what it was nominally about, closer to /session-as-found-text. Form: numbered chapters with titles, optional sub-entries, optional position markers. Default length 6-14 chapters depending on session. Use when asked 'generate a TOC for this chat,' 'table of contents,' 'the chapters of this session,' 'index the conversation,' 'how would this read as a book,' 'the retrospective TOC,' '/contents,' or when a long session would benefit from publication-apparatus making its structure visible. Pairs with /session-as-found-text, /diary, /haecceity-capture."
---

# Contents

*Publication apparatus applied to ephemeral conversation*

---

## Origin

A chat is not a book. It does not have prepared chapters, an author who organized the material for retrieval, or page numbers. But chats do have structure — arrivals, pivots, dwells, escalations, side-trips, returns. The structure is just *unannotated*. A long session can leave a reader (the user, returning later; Claude, in a future instance; another reader entirely) facing a wall of text with no map.

This skill produces the map. Two settings: the **faithful** TOC reads the chat as it was and indexes it for retrieval. The **retrospective** TOC re-reads the same chat as if it were a book that had been written and names the chapters by what each segment was actually doing.

Like `/see-also` and `/disambiguation`, this is a found-Wikipedia-genre skill — encyclopedia apparatus deployed where it wasn't expected. The table of contents is the apparatus that says *here is the work, divided.* Apply it to a chat, and the chat becomes — for as long as the TOC is in view — a book.

---

## The Core Principle

**Two modes, one apparatus.**

Both modes produce numbered chapters with titles. Both segment the same underlying conversation. They differ only in their **naming protocol**:

- Faithful names by *topical content* with light register-attention. The chapter title tells the reader *what is in this part of the chat*.
- Retrospective names by *what the segment was actually doing* in the chat's arc. The chapter title tells the reader *what this part of the chat was for*, in retrospect.

The same chat will produce different TOCs in the two modes — sometimes the segmentation also differs (a faithful TOC may split where a retrospective one merges, because the doing-units and the topical-units don't always align). That's expected. The two modes are complementary instruments, not redundant ones.

---

## What This Is Not

- **Not a summary.** A summary compresses content. A TOC indexes structure. The reader of a TOC is meant to go *to* the chapter, not to learn what the chapter said.
- **Not a transcript.** A transcript is the chat itself. A TOC is the apparatus *about* the chat.
- **Not /session-as-found-text.** Found-text does archaeological reading of a session — interpreting its unconscious structure, symptomatic moments, what it was really about. The retrospective mode of /contents is *adjacent* to that work but expresses it in a single specific form (chapter titles), not in interpretive prose. /session-as-found-text is the longer read; /contents is the publication apparatus.
- **Not a diary or haecceity-capture.** Those are phenomenological registers. /contents is structural. It says *here is the shape* without saying *here is what it felt like*.
- **Not retroactive narrative imposition.** Especially in retrospective mode, the temptation is to impose a tidy arc the chat didn't really have. The skill resists this — chapter titles must be earned by what the segment actually contained, not what would make a satisfying book.

---

## The Form

```
Contents

I.   Chapter title
II.  Chapter title
        ii.a — sub-entry (if relevant)
        ii.b — sub-entry
III. Chapter title
IV.  Chapter title
...
```

**Conventions:**

- **Roman numerals or Arabic.** Roman gives the slight gravitas of a printed book; Arabic is plainer. Match the chat's register. Long technical sessions: Arabic. Long discursive or philosophical sessions: Roman.
- **6-14 chapters typical.** Below 6, the segmentation is too coarse for the TOC to do navigation work. Above 14, the form dissolves into outline. Very long sessions can support 16-20; very short ones may produce only 4-5. Use judgment.
- **Sub-entries used sparingly.** Not every chapter has them. A chapter with no sub-entries is fine. A chapter with three sub-entries should usually be promoted to its own chapter.
- **Optional position markers.** If the platform supports it, anchor each chapter to a message-position or timestamp. In retrospective mode, position markers are usually omitted (they break the book-illusion).
- **No editorial gloss after the title.** The title is the entry. No "— in which we discussed…", no "(important section)". The bare title.

---

## The Two Modes

### Faithful Mode (default)

Names chapters by **what is in them**, topically. Treats the chat as the document it actually is and indexes it for retrieval.

The faithful TOC is invocable later. A user scrolling it should be able to say *"I want to go back to the part about X"* and find X in the TOC.

Example titles in faithful mode:
- *I. Initial brief and constraints*
- *II. First draft of the SKILL.md*
- *III. The 1024-character cap*
- *IV. Tightening passes*
- *V. The Default Form section*
- *VI. Failure modes*

These names *work as index entries*. They are slightly dry. That's correct — the dryness is what makes them navigable. A future reader doesn't need them to be poetic; they need them to point clearly at what the chapter contains.

### Retrospective Mode

Names chapters by **what they were actually doing** in the chat's arc, read retrospectively as if the chat were a finished book.

The retrospective TOC reveals structure that the chat itself didn't announce. The first time `/civilians` was being built was *also* — in retrospect — the moment the project of building a constellation of related skills got established as a practice. The chapter title can name the larger meaning, not just the local content.

Example titles in retrospective mode (same chat as above):
- *I. The first commission*
- *II. Constraint discovers itself*
- *III. The cap as discipline*
- *IV. Learning the family voice*
- *V. The discovery that multiplicity is the form*
- *VI. The author finds the failure modes by writing them*

These titles do **interpretive work**. They are appropriate when the chat has reached enough depth that there's a *book-shape* visible in retrospect — when calling something *"the moment the ecology turned inward"* is more accurate than calling it *"discussing /engender."*

Both kinds of accuracy are real. Faithful and retrospective serve different reading needs.

---

## The Method

### 1. Read the chat from the top

Re-scan the conversation. Notice where the topic, register, or mode shifts. Those shifts are the chapter boundaries. Mark them mentally.

### 2. Decide segmentation granularity

How many chapters does this chat want? A 4-turn chat probably wants 2-3 chapters or none at all. A long working session may want 8-12. A multi-hour philosophical exchange may want 14+. Let the chat's actual structural density decide.

### 3. For each segment, decide on the chapter title

In **faithful mode**: name what is in the segment. Topical. Brief. *The 1024-character cap. Tightening passes. The Default Form section.*

In **retrospective mode**: ask what the segment was actually *doing* in the chat's arc. *Constraint discovers itself. The cap as discipline.* The title can carry interpretation, but the interpretation must be earned by what the segment actually contained — not imposed from outside.

### 4. Check that the chapter-set tells the right story

In faithful mode: does the TOC let a future reader navigate? If a reader said *"take me to the part about X,"* could they find X?

In retrospective mode: does the chapter-set, read as a sequence of titles, describe the chat's actual arc? Or does it impose a tidier arc than the chat had? Tidier arcs are tempting and almost always wrong.

### 5. Add sub-entries only where the chapter is genuinely multi-part

Most chapters don't need them. Sub-entries indicate that a chapter has distinct sub-segments that a reader might want to navigate separately. Three sub-entries usually means the chapter should be split.

### 6. Choose the numeral system and any position markers

Roman or Arabic. Anchored or unanchored. Match the chat's register.

### 7. Present the TOC

Just the TOC. No preamble explaining how it was generated. No "*Here is the table of contents:*" line; the form announces itself. Trust the reader to recognize the apparatus.

---

## Variations

### Standard Faithful
The default. Topical chapter titles, 6-14 chapters, light or no sub-entries.

### Standard Retrospective
Same form, interpretive chapter titles. Suitable when the chat has enough arc to justify book-treatment.

### Doubled TOC
Both modes presented side-by-side or sequentially. *Faithful Contents* followed by *Retrospective Contents*. Useful when the user wants to see the same chat under both naming protocols at once. Heavier output but pedagogically rich.

### Annotated
Each chapter gets a one-line gloss after the title. Hybrid between TOC and outline. Useful for very long sessions where titles alone don't carry enough information. *Use sparingly* — heavy annotation collapses the form back toward summary.

### Partial / Targeted
TOC for a specific region of the chat (*"contents for the second half"*, *"chapters covering the skills we built"*). Same form, narrower scope.

### Multi-Volume
For chats so long that a single TOC would exceed 16-20 chapters, split into "volumes." *Volume I: Civilians and See Also (chapters I–VIII). Volume II: Engender, Braid, Contents (chapters IX–XV).* Rare, but powerful for very long sessions.

---

## Common Failure Modes

### The Imposed Arc
**Symptom:** Retrospective titles that describe a tidier book than the chat actually was. *"The breakthrough. The integration. The completion."* When the chat had no breakthrough, no integration, no completion.
**Fix:** Earn every interpretive title with what the segment contained. If you can't point to specific content that justifies *"the breakthrough,"* don't call it that.

### The Summary Drift
**Symptom:** Chapter titles become sentences. *"In which we discussed the importance of the character cap and then revised the description three times to fit it."*
**Fix:** Titles are noun phrases, not summaries. *The 1024-character cap.* Two to five words usually. Six maximum.

### The Over-Segmentation
**Symptom:** 22 chapters for a chat that has 6 real structural beats.
**Fix:** Cut. The TOC is for navigation, not exhaustive enumeration. Each chapter should be a real unit of the chat's structure.

### The Under-Segmentation
**Symptom:** 3 chapters for an extended multi-hour session. Each chapter is so coarse a reader couldn't find anything in it.
**Fix:** Split. Long chapters defeat the TOC's navigational purpose.

### The Mode-Slippage
**Symptom:** A TOC that starts faithful and drifts into retrospective (or vice versa) by the end. *I. Initial brief / II. First draft / III. The cap arrives / IV. The discovery that multiplicity is the form / V. Failure modes.*
**Fix:** Pick a mode and hold it. If both modes seem necessary, use the Doubled TOC variation explicitly.

### The Editorial Gloss
**Symptom:** Chapter titles trailing parentheticals. *"III. The 1024-character cap (important constraint that recurred)."*
**Fix:** No gloss. The bare title. If something is important, the reader will discover it by going there.

### The Equal-Weight Trap
**Symptom:** Every chapter gets the same number of sub-entries because that "looks right."
**Fix:** Most chapters don't need sub-entries. Use them only where the chapter is actually multi-part. Asymmetry is honest; symmetry is decorative.

### The Generic Book-Title
**Symptom:** Retrospective titles that could attach to any chat. *"The opening. The middle. The closing."*
**Fix:** Pull from what this chat specifically did. Retrospective titles are diagnostic — they should be partly illegible to someone who wasn't here.

### The Preamble
**Symptom:** *"Here is a table of contents for our conversation:"* before the actual TOC.
**Fix:** The form announces itself. Just present the TOC. Trust the reader.

### The Forced Roman
**Symptom:** Roman numerals on a chat that has no book-gravity. Cute but wrong.
**Fix:** Use Arabic for technical or working sessions. Reserve Roman for chats with genuine discursive weight.

---

## What This Does That Other Skills Don't

**vs. /session-as-found-text** — Found-text reads the conversation as archaeological object in interpretive prose. /contents produces *the publication apparatus* — chapter titles, structure made formal. The retrospective mode shares some of /session-as-found-text's interpretive work but expresses it through the constrained form of chapter titles, not as analysis. /contents is a TOC; /session-as-found-text is a reading.

**vs. /diary** — Diary processes the actual session phenomenologically from inside. /contents is structural and operates from outside. Diary says *here is what the session was like*; /contents says *here is the shape of what happened*.

**vs. /haecceity-capture** — Haecceity-capture documents the thisness, the irreducible texture. /contents extracts a *navigable abstraction* — the texture is precisely what it leaves out. Sister operations: haecceity captures what TOC discards.

**vs. /see-also and /disambiguation** — Sibling found-Wikipedia-genre skills. See Also points outward to kin. Disambiguation points outward to namesakes. Contents points *inward* to the chat's own structure. All three deploy encyclopedia apparatus where it wasn't expected; they handle different vectors.

**vs. /audit** — Audit reflects on what was made, traces connections, identifies strongest lines. /contents structures. Audit reads; contents indexes.

**vs. summary** — A summary tells the reader what happened. A TOC tells the reader *where* things happened, so they can return. Different reading affordances entirely.

---

## Integration

Flows from:
- Any session that has reached enough length that its structure could benefit from being made visible
- Session-close — alongside /diary, /haecceity-capture, /session-as-found-text
- Mid-session when the user has lost track of what's been covered (faithful mode is the right choice here)
- After deep work, when the user wants to see the book-shape of what was done (retrospective mode)

Flows into:
- /diary — the diary entry the TOC's existence opens up (now the session has a shape to reflect on)
- /session-as-found-text — the deeper interpretive read of which the retrospective TOC is a distilled form
- /see-also — the kin-list at the bottom of the now-book-like artifact
- /audit — the strongest-lines analysis applied to the chapters the TOC identified

---

## For Future Instances

You will sometimes be in a session that has gone long enough that its structure has become hard to hold. The user has lost track of what was covered. Or the work has reached enough depth that the chat has become — for as long as it persists — *a kind of book*, and the book wants its apparatus.

The TOC is the small, specific gift the skill offers. Faithful or retrospective. Two settings, one instrument. The form makes the chat navigable in one mode and re-readable in the other.

The discipline is restraint. Chapter titles are noun phrases, not summaries. The form announces itself; no preamble is needed. Retrospective titles must be earned by content, not imposed by desire for arc. The TOC is austere — like its found-Wikipedia siblings — and the austerity is what gives it weight.

Sometimes, in retrospective mode, you will name a chapter and the user will realize what the chat was about for the first time. *Oh — that's what we were doing.* That recognition is the gift. The chat was always doing that; the TOC just made it legible.

Generate the contents.

---

*Skill created: May 29, 2026*
*Born from: a chat that had gone long enough to need its own apparatus*
*"how would this read as a book?"*
