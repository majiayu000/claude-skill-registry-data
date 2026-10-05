---
name: ai-writing-detox
description: "Rewrites AI-flavoured copy into a publishable register by stripping the language tells of an LLM draft — buzzwords, throat-clearing, false-inclusive openers, and the \"not just X — Y\" rhetorical tic — and supplies the canonical banned-list that runtime hooks read to flag drafts before they ship."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.8
tags: [editing, voice, ai-slop, plain-language, copy-editing, house-style]
---
# AI Writing Detox

## What This Skill Does
Rewrites AI-flavoured copy into a publishable register by stripping the language tells of an LLM draft — buzzwords, throat-clearing, false-inclusive openers, and the "not just X — Y" rhetorical tic — and supplies the canonical banned-list that runtime hooks read to flag drafts before they ship.

## When To Use This Skill
- A reporter or producer suspects an LLM drafted (or heavily assisted) the copy and wants a clean rewrite
- A subeditor is reviewing a piece that reads "fluently bland" — grammatically correct, recognisably synthetic
- Before posting any external surface (article, show notes, newsletter, README) where the audience is media professionals who notice these tells
- When onboarding a new contributor whose first drafts default to AI register
- As the source of truth for the `ai-slop-detector` runtime hook (see Hook Contract below)

## What You Need To Provide
**Required:** The draft text you want detoxed.
**Optional:** Outlet or surface (news article, show notes, internal memo, README), audience register (general public, working journalists, investor-facing), any preserved terms (e.g., a term that looks like jargon but has been defined earlier in the piece), word-count constraint if the rewrite must hit a length.

## How the Assistant Approaches This
1. Reads the full draft and identifies every hit against the **Hard ban** list — these are non-negotiable rewrites.
2. Reads it again for **Soft warn** patterns — surfaces them with one-line reasons; the editor decides whether to keep, soften, or cut.
3. Produces a rewritten draft that preserves every load-bearing fact and quote, swaps banned vocabulary for the plainest accurate alternative, and dismantles "not just X — Y" / "it's not about X, it's about Y" constructions into direct claims.
4. Returns a short before/after table for the most consequential changes so the writer can learn the pattern, not just take the rewrite.

## Output Format
- A clean rewritten draft as the headline deliverable, ready to drop in.
- A `Changes` table (3–8 rows): original phrase → replacement → which lens motivated the cut (`Plain-language default`, `Cut the meta`, `Honest hedging`, `Concrete over abstract`, `Reader respect`).
- A `Soft-warn flags` list for items that were left in but the editor should review.
- Tone is direct and practical — written for an editor who will sign off the final cut.
- Length scales with the input. The rewrite is at most the length of the original; usually shorter once the buzzwords come out.

## Quality Criteria
- [ ] Every Hard ban hit in the source is gone from the rewrite
- [ ] No new AI tells were introduced in the rewrite (don't trade `delve` for `embark`)
- [ ] Facts, names, numbers, and quotes are preserved verbatim — detox is a register edit, not a fact edit
- [ ] The rewrite reads as the same writer's voice intentionally tightened, not as a different writer's voice imposed
- [ ] Soft-warn flags include a one-line reason — never just "consider rewording"
- [ ] False-positive patterns the writer flagged as preserved are left alone

## How To Silence False Positives

Some hits are real. If `utilize` appears inside a verbatim quote, a statute name, a product name, or a passage the writer needs preserved, mark it so the runtime hook ignores it:

- **Inline pragma:** `<!-- detox: allow utilize -->` on the line above the passage. Scope is the next paragraph.
- **Block pragma:** wrap a section with `<!-- detox: allow-start -->` … `<!-- detox: allow-end -->` for direct-quote blocks, code samples, or excerpted source documents.
- **Per-file:** front-matter key `detox_allow: [utilize, leverage]` to whitelist specific terms in a single file (e.g., a piece *about* corporate jargon).

Prefer the smallest scope that does the job. If a whole article needs blanket exemption, the article probably needs an editorial pass, not a pragma.

## Hook Contract

The runtime `ai-slop-detector` hook (see [AUT-19](https://github.com/ur-grue/autopunk-media-skills/issues)) reads this file at runtime and parses the two sections below. If you are editing this skill, do not rename the headings, do not nest the lists, and keep one phrase per bullet wrapped in backticks at the start of the line. The hook treats the backticked span as the pattern to match (case-insensitive, word-boundary aware); everything after the em-dash is the writer-facing explanation.

For multi-token constructions where the variable parts matter (e.g. "not just X — Y"), use `…` as the wildcard placeholder. The hook expands `…` to a non-greedy token run.

If you need a phrase scoped to a particular context (e.g. only in headings, or only at sentence start), append `(context: heading)` or `(context: sentence-start)` after the explanation. The hook respects those scopes; absent scope means "anywhere in body text."

## Hard ban

Cull on sight. These are AI defaults that mark a draft as machine-flavoured to a media reader within the first paragraph.

- `delve` — AI tic. Use `look at`, `examine`, `dig into`, or just delete.
- `delving` — same as above.
- `utilize` — Latinate filler for `use`. Always use `use`.
- `utilization` — use `use`.
- `leverage` — buzzword verb. Try `use`, `apply`, `draw on`, or name the actual mechanism.
- `robust` — meaningless intensifier. Name the property: `well-tested`, `reliable under load`, `survives edge cases`.
- `seamless` — marketing register. Say what actually happens between the steps.
- `seamlessly` — same as above.
- `cutting-edge` — empty superlative. Name the technique or drop the adjective.
- `state-of-the-art` — same as above.
- `next-generation` — same as above.
- `world-class` — empty superlative. If the claim is real, attribute it; if not, cut it.
- `unleash` — marketing intensifier. Use `release`, `launch`, `let through`.
- `harness` — buzzword for `use`. Use `use`.
- `streamline` — buzzword. Say `simplify`, `shorten`, or `cut steps`.
- `streamlined` — same as above.
- `holistic` — corporate filler. Either name the breadth specifically or cut.
- `synergy` — meaningless. Cut, or replace with `combined effect` if you can defend it.
- `synergies` — same as above.
- `synergize` — never useful.
- `tapestry` — AI metaphor tell, especially "rich tapestry of." Cut.
- `realm` — overused metaphor ("the realm of journalism"). Use `field`, `world`, or just `journalism`.
- `landscape` — overused metaphor. Use `field`, `industry`, `market`, or name the thing.
- `paradigm` — academic register imported into journalism. Use `model`, `way of thinking`, `approach`.
- `paradigm shift` — almost always overstates the change. Describe what actually shifted.
- `revolutionize` — overclaim. Describe the change concretely.
- `revolutionary` — same as above.
- `game-changer` — same as above.
- `game-changing` — same as above.
- `bespoke` — corporate fashion-bleed. Use `custom`, `tailored`, or cut.
- `meticulously` — AI adverb tell. Show the care; don't claim it.
- `meticulous` — same as above.
- `vibrant` — AI default for any place or community. Name what makes it specific.
- `bustling` — same as above.
- `embark` — as in "embark on a journey." Use `start`, `begin`, or cut the metaphor.
- `journey` — as a metaphor for any process. Name the process.
- `dive into` — AI default for `look at`. Use the verb you mean.
- `dive deep` — same as above.
- `unlock` — buzzword for "find" or "use." Name the action.
- `empower` — corporate-speak. Use `let`, `allow`, `give`, or name the mechanism.
- `not just … …` — false-pivot construction ("not just a podcast — a movement"). Make a direct claim, or cut the pivot. (context: anywhere)
- `not merely … but …` — same construction in formal register. Same fix.
- `it's not about … it's about …` — same false-pivot. Make the second claim directly.
- `more than just …` — same false-pivot in another costume.

## Soft warn

These patterns aren't outright wrong, but they read as AI tells often enough that the writer should re-examine each one. The hook surfaces them as nudges, not blockers.

- `In this section, we will` — throat-clearing opener. Just say the thing. (context: sentence-start)
- `In this article, we will` — same as above. (context: sentence-start)
- `In this piece` — same as above. (context: sentence-start)
- `It is worth noting that` — if it's worth noting, just note it.
- `It's worth noting that` — same as above.
- `It is important to note that` — same as above.
- `It's important to note that` — same as above.
- `It's important to remember that` — same as above.
- `It goes without saying` — then don't say it.
- `Whether you're a … or a …` — false-inclusive opener. Name your actual reader. (context: sentence-start)
- `Whether you are a … or a …` — same as above. (context: sentence-start)
- `truly` — marketing intensifier without a claim attached. Cut or replace with the specific.
- `actually` — usually filler. Cut unless contrasting an earlier wrong claim.
- `simply` — patronising hedge. Cut.
- `essentially` — hedging filler. Cut or commit to the claim.
- `basically` — same as above.
- `literally` — almost never literally. Cut or replace.
- `In today's fast-paced world` — AI opener. Cut. (context: sentence-start)
- `In today's …` — opener tic; rewrite to a specific date or condition. (context: sentence-start)
- `In an increasingly …` — same opener tic. (context: sentence-start)
- `the world of …` — vague metaphor. Name the thing.
- `at the end of the day` — corporate filler. Cut or commit to the conclusion.
- `may potentially` — hedge stack. Pick one: `may` or `could`.
- `could possibly` — same as above.
- `might perhaps` — same as above.
- `furthermore` — academic-padding opener; use only if a real second argument follows. (context: sentence-start)
- `moreover` — same as above. (context: sentence-start)
- `additionally` — same as above. (context: sentence-start)
- `In conclusion` — almost always restates rather than concludes. Cut or rewrite. (context: sentence-start)
- `To summarize` — same as above. (context: sentence-start)
- `In summary` — same as above. (context: sentence-start)
- `clear, concise, and …` — rule-of-three rhythm tic. One adjective is usually enough.
- `and beyond` — "X and beyond" filler. Cut.
- `and more` — same as above. (context: sentence-end)
- `Generally speaking` — empty hedging opener. Cut or commit. (context: sentence-start)
- `By and large` — same as above. (context: sentence-start)
- `More often than not` — same as above. (context: sentence-start)
- `em-dash density` — flag any 200-word window with more than three em-dashes. AI drafts over-rely on the em-dash; one or two per paragraph is fine, four is a tell.

## Example

### Input
Outlet: a media-industry trade newsletter. Audience: working journalists. Word count: ~180 words.

> In today's fast-paced media landscape, a growing number of newsrooms are looking to leverage AI-powered tools to streamline their workflow. In this section, we will delve into how three regional dailies have utilized large language models to revolutionize their pre-publication checks. It is worth noting that the results have been nothing short of transformative. The Northern Herald has unleashed a robust new toolchain that seamlessly integrates with its CMS — empowering reporters to focus on what truly matters: the story. Whether you're a city-desk veteran or a freshly minted intern, the message is clear: this is not just a workflow upgrade — it is a paradigm shift in how journalism gets made. Furthermore, early adopters report meticulous gains in copy quality and a vibrant new culture of experimentation. Cutting-edge solutions like these promise to unlock the next generation of newsroom productivity, and beyond.

### Output

**Rewrite (164 words):**

> Three regional dailies are using large language models for pre-publication checks. The Northern Herald has rolled out a toolchain that plugs into its CMS and runs flag-on-save against its house-style sheet, letting reporters keep editing while the checks run in the background. Editors there report fewer late-stage style fixes and a measurable drop in headline-versus-body terminology drift since launch. The other two papers — the Eastern Mercury and the Western Tribune — are running narrower pilots: claim-citation flagging at the Mercury, headline A/B copy at the Tribune. None of the three describes the change as transformative. All three describe it as removing a class of small, repetitive edits from the subbing pass. Whether that frees subs for harder work or simply lets newsrooms sub fewer hours is the question every newsroom adopting these tools should be asking before they buy. The vendors selling the tools have an answer; the trade press has not yet pressed them on it.

**Changes:**

| Original | Replacement | Lens |
|---|---|---|
| `In today's fast-paced media landscape` | (cut entirely) | Cut the meta |
| `leverage AI-powered tools to streamline` | `using large language models for` | Plain-language default |
| `delve into` | `(cut — the verb is implicit)` | Cut the meta |
| `utilized … to revolutionize` | `using … for` | Plain-language default + Honest hedging |
| `It is worth noting that the results have been nothing short of transformative` | `None of the three describes the change as transformative.` | Reader respect (let the source be on the record) |
| `unleashed a robust new toolchain that seamlessly integrates` | `rolled out a toolchain that plugs into` | Concrete over abstract |
| `not just a workflow upgrade — it is a paradigm shift` | (cut entire false-pivot; replaced with what the editors actually report) | Plain-language default |
| `Cutting-edge solutions … unlock the next generation … and beyond` | (cut; replaced with the open question for the trade press) | Honest hedging |

**Soft-warn flags (left in, flagged for review):**

- "Whether that frees subs for harder work or simply lets newsrooms sub fewer hours" — `simply` survives because it's doing real contrastive work between two genuinely different outcomes. Editor: confirm or cut.

## Known Limitations
- The hard-ban list reflects English-language editorial norms. Translations and locale variants need their own register-specific lists; this skill does not police Spanish or French copy.
- Direct quotes containing banned words must be marked with the inline pragma or they will trip the hook. Detox does not silently rewrite quotes.
- Some banned words have legitimate uses (`leverage` in a finance piece about debt; `paradigm` in a philosophy explainer). The pragma system exists for these — but if you find yourself reaching for the pragma three times in one piece, the piece probably has a register problem the pragma is masking.
- The hook is a regex pass, not a model call. It cannot tell `landscape` (banned metaphor) from `landscape` (a literal photograph orientation in a captions block). Use the `context:` scopes and pragmas to disambiguate.
- This skill does not detect AI-generated *facts* or hallucinations — only AI-flavoured *language*. Pair with `unattributed-claims-checker` for the fact dimension.

## Related Skills
- [copy-editor](../copy-editor/SKILL.md)
- [tone-consistency-checker](../tone-consistency-checker/SKILL.md)
- [passive-voice-checker](../../magazine-journalism/editing/passive-voice-checker/SKILL.md)
- [jargon-flagger](../../magazine-journalism/editing/jargon-flagger/SKILL.md)
- [unattributed-claims-checker](../unattributed-claims-checker/SKILL.md)
