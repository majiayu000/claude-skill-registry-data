---
name: review-piece
description: "Review a writing Piece's Deliverable as it is now, in four parallel sub-agents: Spec (facts, Outline, length, copied wording), Voice (the Voice sheet and the spec's overrides), Craft (the Craft sheet: rules and garden paths) and Reader (what it says to someone without the spec). Reports them side by side. Invoked as /review-piece <repo> <n>."
argument-hint: "<repo> <n>"
disable-model-invocation: true
---

Four-axis review of a Piece's Deliverable, read as it is now. There is no diff and no fixed point.

- **Spec**: does the text hold to the spec's facts, Outline and length limit, and copy no wording from what its drafter read?
- **Voice**: does it follow the Voice sheet and the spec's overrides?
- **Craft**: does the text keep the Craft sheet's rules, and can a reader parse each sentence on the first pass?
- **Reader**: what does it say to a reader who never saw the spec?

Each axis runs in a **fresh-context sub-agent** that never wrote the Piece, so the axes judge the text rather than the author's intent. The Piece rules live in the root's `docs/pieces/`: [`rules.md`](../../../docs/pieces/rules.md) (its "Implementing a piece spec" and "Done checks" sections) and [`GLOSSARY.md`](../../../docs/pieces/GLOSSARY.md). Point the sub-agents there; never restate them here.

## 1. Pin the issue and its scope

The input is `/review-piece <repo> <n>`, an issue in `<repo>`. Fetch it with `npm run issue:read -- <repo> <n> --body --comments` and state its title. If the reference is ambiguous, or the issue is Research rather than a Piece, stop and say so.

Run `gh api repos/<owner>/<repo>/issues/<n>/parent`, resolving `<repo>` to `<owner>/<repo>`; a 404 means no parent. Fetch a parent when there is one, since its facts join the fact list. Then set the **scope**:

- **Sections**: the issue has a parent and is not the final pass. The scope is the Sections it names, matched by their exact heading text in the Deliverable.
- **Whole**: the issue has no parent, or it carries the `final-pass` label. The scope is the whole Deliverable.

Done when the title is stated, the scope is one of the two, and for Sections every named heading is found in the Deliverable. A heading that isn't found fails here, before any sub-agent runs.

## 2. Gather the inputs

**Every source is a Drive file**, read by the ID the spec lists; `/grill-piece` saved each web page to Drive, and no input here is read from the web.

Write each to its own file in the scratchpad, so each sub-agent gets only its own files:

- **Deliverable**: the Google Doc the spec names, read now as Markdown with the gworkspace tools.
- **Reader**: the spec's Reader field, verbatim, and nothing else. With no Reader field, use the spec's lines on who the Piece is for and mark them a stand-in.
- **Fact list**: the closed list the implementer had: the issue's facts, the parent's facts, the facts of any Research comment the spec links, never its `## Unverified` section, and any of the developer's own text the spec names as given.
- **Unverified**: each linked Research comment's `## Unverified` section, verbatim; facts set aside, outside the fact list.
- **Outline**: the spec's Outline field, verbatim.
- **Length limit**: the spec's, verbatim.
- **Read passages**: a folder with one file per passage: each short Supporting Material file's text, read from Drive by the file ID the spec lists; for one too long to read whole, the passages the spec lists by page range. A long PDF is downloaded by [`docs/pdf-pages.md`](../../../docs/pdf-pages.md), each listed range written to its own file with the page-range command, then the download deleted. For each fact the fact list takes from a Research comment, add the range its locator cites, which stands for the References the drafter read. Match the locator's file name to its source in the Research spec's Supporting Material, and read that source by its Drive ID: a cited page range written to its own file from its source's PDF by the page-range command the same way, or for a source with no pages, the text under the cited heading.
- **Overlap**: the output of `npm run overlap -- --deliverable <Deliverable file> --passages <Read passages folder> --allow <file>`, its allow file listing the proper names and fixed terms the Piece can't reword.
- **Style**: the spec's Evidence and Formality values, whether the Piece is Academic, and its Style field's overrides, Form and Order sections, verbatim, in the Style file shape in [the Jev agent doc](../../../docs/agents/jev.md#the-style-check).

Done when every file exists, or the spec has no such field and you say so. A missing Drive ID or Supporting Material file is asked for, never guessed. Note each **gap**: an input that is missing, a stand-in, or only partly loaded.

## 3. Spawn the four sub-agents in parallel

Issue all four Agent calls together, in the foreground. Each prompt names the scope: the Section headings or "the whole Deliverable".

**Spec** sub-agent, the session's model. Its prompt gives the Deliverable, fact list, Unverified, Outline, length limit, Read passages and Overlap files, points at done checks 1, 2 and 4 in `docs/pieces/rules.md`, and the brief: "For the in-scope text only, report every factual claim that doesn't trace to the fact list. Judge each in-scope Overlap hit, keeping it as copied wording or dismissing it with a one-line reason, and add any sentence structure copied from the Read passages, which the Overlap list can't see. Report each in-scope Section that doesn't make its Outline claim or set out the facts the Outline assigns it. Report whether the whole Deliverable meets the length limit. Quote the spec line or the copied passage for each finding. Label hard only a claim missing from the fact list, a claim drafted from the Unverified file, which is outside the fact list, a claim that contradicts a fact or another part of the Deliverable (a table, a gate, an earlier Section), a fact the Outline assigns a Section that it leaves out, a Section that doesn't make its Outline claim at all or makes a different one, copied wording or a missed length limit; label how the text describes a source (overstated, narrowed, misattributed) and a claim made only weakly or implicitly a judgement call. Under 400 words."

**Voice** sub-agent, the session's model. Its prompt gives the Deliverable and Style files, points at the style rules under "Implementing a piece spec" in `docs/pieces/rules.md`, plus `docs/academic-writing-style.md` for an Academic Piece, and the brief: "For the in-scope text only, report every place it breaks `docs/writing-voice.md`'s rules, read in full and applied with the rules tagged for these Evidence and Formality values, or the spec's overrides, which win where they conflict. Leave `docs/writing-craft.md` to the Craft axis. Cite the rule for each finding and quote the sentence. Every finding is a judgement call. Under 400 words."

**Craft** sub-agent, the session's model. Its prompt gives the Deliverable and Style files, plus `docs/academic-writing-style.md` for an Academic Piece, and the brief: "Read `docs/writing-craft.md` in full. Then, for the in-scope text only, report every sentence that breaks one of its rules, or that reads one way on the first pass and turns out to mean another (a garden path). The spec's overrides and the academic sheet win where they conflict with a Craft rule. Quote the sentence and cite the rule for each finding. Every finding is a judgement call. Under 400 words."

**Reader** sub-agent, the session's model. Its prompt gives only the Deliverable and Reader files. Never give it the facts, the Read passages, the style sheets or the spec. The brief: "You are the reader described. Read the whole Deliverable, then for the in-scope part only report: (a) what you took it to say, in a few sentences; (b) each place you got lost, quoting it; (c) what you would ask the author. Under 400 words."

## 4. Aggregate

Present the four reports under `## Spec`, `## Voice`, `## Craft` and `## Reader`, verbatim or lightly cleaned. Open each with that axis's gaps from step 2 and the check each one weakened. Keep the axes unmerged and unranked: one axis's findings must never bury another's.

End with one line per axis: its finding count and its worst finding. Pick no winner across axes.
