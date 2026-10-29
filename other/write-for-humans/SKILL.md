---
name: write-for-humans
description: The seven anti-slop rules in order, voice preservation, and a prose-humanizer subagent for long rewrites.
disable-model-invocation: true
---

# Write for humans

Use this skill when writing or revising prose people will read: docs, READMEs, PRs, commit messages, issues, email, Slack, or long-form replies. Apply it while drafting and when cleaning up existing prose. For rewrites, identify the tells, judge whether they cluster, then cut or revise them while preserving the author's voice.

Skip code, configuration, structured data, direct quotations, and agent-facing instructions where bluntness matters more than humanization.

## The seven rules

Apply these in order. Earlier cuts make later edits smaller.

1. **Cut scaffolding.** Remove announcements, throat-clearing, signposts, moral wrappers, and closers that tell readers what the text is about to do or has just done. Cut stock openings such as “Great question” and “Let's dive in,” and endings such as “In conclusion” or “I hope this helps.” Remove section previews and summaries that repeat nearby text. Avoid defensive reassurance and unsolicited offers; state a useful offer once, plainly.

2. **State the claim directly.** Rewrite “not X, it's Y,” “not only X but Y,” and similar contrast setups as a positive claim. Avoid rhetorical Q&A and “the X? A Y” constructions. Keep a real contrast when the distinction carries meaning; remove the staged strawman.

   Before: “This isn't theoretical. It's practical.” After: “You can run this today on your laptop.”

3. **Name facts instead of inflating stakes.** Replace abstract significance with the specific event, evidence, or effect. Cut words such as “pivotal,” “crucial,” “testament,” and “transformative” when they add no fact. Replace inflated verbs such as “showcase,” “underscore,” “foster,” “leverage,” and figurative “navigate” with direct wording. The test: if removing the word changes nothing, remove it; if it changes the meaning, replace it with a concrete fact.

   Before: “The 1987 renovation marked a pivotal moment in the building's enduring legacy.” After: “The building was renovated in 1987 after the roof collapsed in a storm.”

4. **Use plain verbs.** Prefer “is,” “has,” and active verbs over “serves as,” “stands as,” “represents,” “embodies,” or “boasts.” Name the person or thing doing the action when the actor matters.

5. **End at the fact.** Remove trailing participial phrases that add commentary after a complete claim, such as “reflecting broader trends” or “highlighting its importance.” Keep an -ing phrase when it states a real action or necessary result.

   Before: “The population grew 12%, reflecting broader demographic trends.” After: “The population grew 12%.”

6. **Earn modifiers and punctuation.** Cut decorative adjectives unless a concrete detail earns them. Keep em-dashes to one or two per page in ordinary prose; rewrite default asides instead of swapping punctuation mechanically. Literary prose may use roughly three or four per 500 words when the author's rhythm calls for them. Remove decorative emoji and Unicode, bold-every-keyword bullets, title-case headings, and small tables that work better as prose. Watch the bold-label-em-dash bullet pattern (`**Option** — description`): it silently blows the em-dash budget once you have three or more bullets. Use `**Option**:` or a plain hyphen instead.

   Before: “The problem — and this is the part nobody talks about — is systemic.” After: “The problem is systemic, and nobody talks about it.”

7. **Vary rhythm; ration threes.** Mix sentence lengths, avoid three consecutive sentences with the same opening, and repeat the right noun instead of cycling through near-synonyms. Use at most one tricolon below 500 words and two above 500 words; never stack them. Prefer two or four items when the facts support that count, or move one item into its own sentence.

   The rule-3 / rule-7 collision is the most common way drafts fail this skill: listing concrete facts mechanically produces three-item lists. Convert before you write the tricolon, not after; counting afterwards fails under time pressure. When a three-item list forms:

   - Use two items and promote the third to its own sentence: “A and B. C is the one that changed.”
   - Use four items when the list is naturally four, not compressed to three.
   - Drop the weakest item and write prose.
   - Use a colon and a single item: “Only one thing moved the needle: X.”

## Tables and terminal readability

When output will be read in a terminal, TUI, chat transcript, or narrow pane, make tables physically readable before sending them: short columns, wide comparisons split into smaller tables, long URLs or notes moved outside the grid. In a Markdown file, README, or report that a viewer will render, normal tables are fine; still keep column names short and paragraphs out of cells.

## Preserve the author's voice

Make the text sound like a clearer version of its author. Keep their rhythm, opinions, contractions, first person, and rough edges. Do not add content or change technical meaning. Preserve lowercase, swearing, and other deliberate register choices. If two edits work, choose the shorter one. For fiction or essayistic prose, preserve distinctive punctuation and rhythm when the source genuinely uses them.

## Workflow

### Drafting

1. Draft with the seven rules in view, especially direct claims, earned modifiers, and varied rhythm.
2. Read the full draft once and use the checklist below to catch remaining patterns.
3. Return the prose without a preamble about the writing process.

### Revising

1. Read the whole draft, then scan the seven rule categories. For a long draft or dense pattern cluster, load [`REFERENCE.md`](REFERENCE.md) for the full catalog.
2. Judge the density: make a few surgical edits when only a handful of tells appear; revise paragraph by paragraph when patterns cluster.
3. Apply the rules in order, cutting before rewriting.
4. Compare the result with the source. Restore distinctive wording or roughness if the edit has made the voice generic. Keep facts and technical meaning intact.
5. Return the revised prose. Include a change list only when requested.

For a long, file-level rewrite or when the main context is tight, dispatch [`agents/prose-humanizer.md`](agents/prose-humanizer.md) with the draft. It edits in place and returns a short summary.

## Self-edit checklist

- Does the opening state a claim instead of announcing the topic? Announce means cut.
- Search “ not ”, “it's not”, and “isn't”. Kill any “not X, it's Y” / “not only X but Y” / “not X — Y”.
- Count em-dashes: more than two in the whole piece? Reduce.
- Scan for inflating vocabulary (delve, tapestry, landscape, robust, seamless, crucial, pivotal, testament, showcase, underscore, leverage, foster, figurative navigate, nestled, boasts, vibrant, meticulous, intricate); see REFERENCE.md for the full list. Replace with a fact or delete.
- Cut participial -ing tack-ons at the end of sentences.
- Cut signposted closers (“In conclusion”, “Ultimately”, “The future looks bright”).
- Count every “X, Y, and Z”. Hard cap is 1 per 500 words. Convert the weakest to prose, then audit every remaining tricolon: does the third item earn its spot?
- Convert bold-first bullet lists (`**Keyword:** content`) to prose or plain bullets.
- Break three consecutive sentences opening with the same subject.
- Does the last sentence restate the first? Cut it.

## More guidance

- [`REFERENCE.md`](REFERENCE.md) has the extended pattern catalog, vocabulary tables, and detection examples. Load it for dense or long rewrites, or when this skill lacks a specific tell.
- `writing-clearly-and-concisely` covers structural clarity. When both skills apply, make that structural pass first, then apply these register rules.
