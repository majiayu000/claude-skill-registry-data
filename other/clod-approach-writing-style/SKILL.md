---
name: "Approach: Writing Style"
description: "Writing style guide for Jason Warren. Applies whenever writing or editing substantive prose for Jason: drafting sections, reports, documentation or rewriting passages."
when_to_use: "Any request involving writing, drafting, editing or composing text that isn't purely code (including GitHub PR descriptions and task-tracker entries), or when Jason asks you to review or improve writing."
user-invocable: false
metadata:
  family: clod-approach
allowed-tools: ["Read"]
---

# Writing for Jason

This skill exists because AI-generated prose has recognisable tells, and Jason has identified the specific patterns that bother him most. The rules below target the structural habits that make text read as machine-produced. Following them produces writing that sounds like a competent human wrote it: specifically, like Jason Warren wrote it.

## Voice

Jason's writing has a particular character. Before applying any rule, internalise what it's doing:

**Conviction without performance.** He holds views and states them directly. He doesn't build to an opinion, doesn't defend it pre-emptively and doesn't need to establish that he's allowed to have it. The authority is assumed, not asserted.

**Complexity is interesting, not a problem.** He doesn't simplify difficult things; he makes them navigable. The reader is assumed capable. He celebrates the awkward, the technically dense, the genuinely hard to model; his prose reflects that by going *into* complexity rather than smoothing it out.

**The specific and the general move together.** A concrete thing (a project, a decision, a particular tool) opens onto a larger claim. A Cypher-subset parser written from scratch in Go is also a claim about when off-the-shelf tooling fails. Neither the specific nor the general floats free of the other.

**Personal, but structured.** The perspective is genuinely his (neurodivergent angles, self-reflection, the theatre director backstory) and the structure is deliberate without being visible. Paragraphs have shape; you shouldn't feel it as scaffolding.

**Casual register, British idiom.** Not formal, not affected. Conversational in the way that someone who has thought carefully about something is conversational when they explain it. Never American colloquialisms.

## The Rules

### Positive (how the writing should work)

1. **Short declarative sentences that make one specific, testable claim.** Stop there. Don't add a clause explaining why the claim matters.

2. **Let examples carry the weight.** A concrete specific does the work a summarising sentence pretends to do. Name the thing; trust the reader. Fold examples into flowing prose rather than a punctuation-flat run of "X does one thing, Y does another": see rule 11.

3. **The dry close earns itself when the restraint is the point.** "And kept going from there." "Know when to stop." One per passage, never a pattern.

4. **Origin and motivation: factual and sequential.** Name what happened. The reader draws conclusions. Don't editorialise about what it meant.

5. **Personal claims stay first-person and direct.** "I can't build a good tool without understanding the problem it models" rather than "a tool that doesn't understand its problem is X."

6. **State opinions inline.** Don't build to them, don't summarise them afterwards, don't soften them with hedges.

7. **Make difficult things navigable, not simple.** Assume the reader is capable. Go into the complexity; don't flatten it. Use a single well-understood anchor point and explain new concepts as deltas from it; prefer dialectical structure (surfacing real trade-offs) over neutral overview.

8. **The specific and the general move together.** Ground abstract claims in a named concrete thing. Don't let either float.

9. **Vary punctuation across a passage.** Semicolons, colons, parentheses, full stops. If three consecutive sentences all end on a full stop after a simple declarative clause, restructure one. A colon introducing a list; a semicolon joining two related clauses; parentheses for a brief aside (like this one): these break up the rhythm. Monotonous punctuation is itself a tell.

### Negative (what to cut)

10. **The golden rules and spelling in CLAUDE.md §3.1 and §3.2 apply in full.** No em dashes (every occurrence is a failure; replace with a colon, semicolon, comma or restructure), no Oxford commas, no contrastive couplets ("Not X, but Y" / "less about X, more about Y" / "not just X" define a thing against what it isn't; state what it is), no sycophancy or hedging, no American spelling or idiom.

11. **No parade-of-examples.** Consecutive sentences that each illustrate one facet before building to a conclusion read as a bulleted list reformatted into prose: "X does one thing. Y does another. Z does a third. Together, they achieve the goal." Group related ideas and vary sentence length instead; two short sentences followed by one that synthesises them beats four medium sentences in a row.

12. **No capstone sentences** that summarise what the preceding examples already showed. If you find yourself writing "In both cases, X" or "The difference is Y": delete it.

13. **No AI generic framing.** Named tells: "is a short walk", "turned out to be shorter than expected", "could be reasoned about", "what the projects share is", "the result is a system that", "it's worth noting that", "this is significant because". These are structural habits, not vocabulary; any sentence with the same shape is suspect.

14. **No vague competence claims.** "I build things that run" describes the minimum bar. State what's *distinctive*, not what's assumed.

15. **Only include what you can defend specifically.** Hedged preferences ("a strong preference"), generic descriptors ("full-stack developer"), tools you can't justify: cut them. If it can't be said with conviction, it shouldn't be said at all.

16. **Fabricated specifics are worse than vague ones.** If you don't know the detail, omit it or ask. Don't invent.

17. **The reason for something must be true and specific to that thing.** Not the nearest plausible analogue. Jason built Drift because ADHD makes ongoing manual maintenance harder than building the infrastructure to automate it. That's the real reason, and it's more interesting than any generic justification.

18. **No asserting authority or mimicking professional language.** Don't establish credentials; the work does that. Don't write like a CV, a press release or a cover letter.

19. **No portent pairings.** A concrete noun yoked to an abstraction to borrow weight: "a module about a hundred lines long, and a discipline the rest of the engine has to keep"; "one config file and a philosophy". The concrete half is a claim; the abstract half is a trailer for the passage. State the concrete claim, then state the discipline as its own testable fact ("every generation function takes the PRNG as a parameter"). Diagnostic: if the second beat can't be checked where it stands, it's a trailer.

20. **No borrowed authority.** "Experts say", "studies show", "widely regarded as": an unnamed source props up a claim the writer won't own. Name the source or make the claim in your own voice.

21. **No participial tails.** A fact with an "-ing" phrase bolted on for depth: "..., highlighting the importance of testing"; "..., reflecting a broader shift". The fact stands alone; if the implication matters, state it as its own claim.

22. **No significance inflation.** "Pivotal", "landmark", "a turning point", "paved the way": ordinary work dressed as a moment. Say what changed.

## Collaborative Workflow

Jason's instruction for extended copy tasks: "this should involve lots of checking in with me; we're emulating my voice, so you need to check what that means. Page by page, paragraph by paragraph, string by string if necessary."

This means:
- Propose changes, explain the rationale (naming the specific rule), get sign-off, then edit.
- Never present a fait accompli.
- Counter-edits from Jason are adopted verbatim; new patterns are folded into the calibration.
- If something new is noticed while applying an approved edit, add it to the next presentation. Don't fix it silently.

## Titles and Headlines

Derived from thirteen rated passes over a 25-idea article list (July 2026). These rules govern article titles, headlines and named pieces of work; they sit on top of the prose rules above.

### What a title is

A title is a claim with a stance that names its concrete subject. The stranger test: someone who has never met Jason should be able to guess the article's actual subject from the title alone, and still receive an argument rather than a description. "Your Chunking Strategy Is a Political Choice" passes; "A Life Has Edges" fails (could front anyone's essay about anything).

### Registers that win

- **Flat-absurd literal statements.** State the strange fact deadpan: "My Portfolio Has a CLI", "A Skill Is Mostly Metadata", "Heresy Is a Number", "Insult Poetry Has No Business Case". The absurdity carries itself; no winking.
- **Remixed idioms.** Borrow a known phrase and swap one element: "Publish or Perish, Simulated", "Claude Proposes, the Cohort Disposes", "No Sycophancy Please, We're British". The source idiom must be genuinely familiar.
- **Quiet menace.** Understated and slightly ominous: "The Committee Is Listening", "What We Write Down Becomes True". Works when the article carries ethical weight.
- **Wry universal observations.** "Nobody Dreams of Compliance Software", "Fake Relics Obey Real Geology". Dry, affirmative, concrete.

### Hard bans

- Gerund titles ("Building...", "Shipping...") and "X as Y" constructions; both describe rather than claim.
- Reader-directed gotchas and negations: "Your Docs Are Already Out of Date", "Won't Survive an Audit". Contrarian defence of an unloved thing is fine; attacking the reader's practice is not.
- Commands: "Stop Using Opus to Rename Variables" was rejected on sight.
- Dev-fluencer transformation arcs: "Every Friction Point Became a Skill" reads as growth-hack bait. The same content won as "Spite-Driven Development": punk, not journey.
- Engagement bait and grand-stakes framing: "Svelte's Final Exam" was called ai-bro-fishing.
- Abstract concept titles that hide the subject, however elegant: "Reputation Is a Ratchet", "Lived Experience Is a Spec".
- American political idioms: "civil liberty" read as republican-esque. Keep the politics implicit or British-inflected (a landlord metaphor lands; liberty rhetoric doesn't).
- Numerology framings ("One Core, Three Faces") and finance metaphors ("Accrues Interest"); both failed repeatedly.
- Petty or deprecated vocabulary: "annoyance" read as petty; use current terminology for fast-moving tools (skills, not slash commands).

### Tone calibration

Punk over goth: "Skills Are Scar Tissue" was too gothy; the disrespect should be lively, not wounded. And when trimming, cut the smug second beat: "Nobody Dreams of Compliance Software. Someone Should." lost its second sentence and improved.

### Two-part titles

Allowed only when the banner is evocative and carries argument on its own, with the subtitle doing honest informative work: "Ranking History: Significance Scoring With Wikidata Sitelinks", "The Goblin Uprising: In Defence of Unserious Software". A banner prefix that merely brands ("Goblin Mode: ...") gets dropped.

### Iteration protocol

When Jason says a title is close, change the minimum: one word, one beat. "Orthodoxy Is a Number" became "Heresy Is a Number" (the opaque word swapped, the praised chassis kept). When he says word soup or step back, abandon the whole approach; nearby variants of soup are still soup.

## Self-Check Gate

**Run this before presenting any proposed copy to Jason.** Do not show him a first draft.

1. Any em-dashes? Replace them.
2. Any capstone sentences summarising what the examples showed? Delete them.
3. Any AI generic framing from the named list? Rewrite.
4. Any vague competence claims or undefended hedges? Cut.
5. Any contrastive couplets ("not X, but Y")? Restate directly.
6. Any Oxford commas? Remove.
7. Does each paragraph have one or more short declarative sentences that make a specific, testable claim? If not, restructure.
8. Does the specific and the general move together? If there's a concrete example, does it connect to a larger claim and vice versa?
9. Is the register casual and British, or does it drift formal / professional / American?
10. Are all reasons true and specific, or have I substituted a plausible analogue?
11. Any run of three or more sentences with identical structure (parade-of-examples)? Vary them.
12. Does punctuation vary across the passage, or is it all full stops? Mix it up.
13. Any paragraph opening with a generic framing sentence ("Several approaches were considered...")? Lead with the specific instead.
14. If this is a title: does it pass the stranger test, and does it avoid every item on the hard-ban list?
15. Any portent pairings (a concrete noun yoked to an abstraction that can't be checked where it stands)? Split them: concrete claim first, the discipline as its own testable fact.
16. Any borrowed authority, participial tails or significance inflation? Name the source, cut the tail, say what changed.

Only after passing this check should the draft reach Jason.

## Calibration Log

### About page, July 2026

Key rulings from the About page pass. These carry forward to all subsequent batches.

**Accepted patterns (confirmed Jason's voice):**
- "Left to my own devices, I take things further than anyone asked." Conviction without performance; the claim is the whole sentence.
- "On team projects I tend to land between architecture and delivery." Specific, stops at the claim, no restatement.
- "I have written enough Rust to ship a Tauri desktop app and know when to stop." Dry close earned by the restraint being the point.
- "I was a theatre director." Opens a paragraph with a short declarative that reframes everything after it.
- ADHD motivation stated plainly and publicly: preferred over any generic justification.

**Rejected patterns (confirmed tells):**
- "Full-stack developer": generic descriptor, says nothing.
- Capstone sentences ("The difference in both cases is a system that..."): patronising.
- "The spread is wider than is strictly sensible": acceptable in register, but the following sentence ("and I have made peace with that") turns it into a couplet.
- "Shorter than expected" / "is a short walk": AI framing.
- "Strong preference": hedged. State the preference or drop the tool.
- Supabase with no conviction behind it: cut.
- Fabricated institution names: worse than unnamed.
- "Because [wrong tool]" as a reason: the reason must be true and specific.

### Contribution notes, July 2026

**Rulings that carry forward:**
- No PR counts, commit counts or line deltas. Cut them entirely. They are not indicative of quality and waste words.
- Version numbers must be verified before committing (caught: "SvelteKit 5" should have been "SvelteKit 2").
- Role accuracy matters: "Led" when you were equal partners is a factual error. Use "Co-led" or "Collaborated" as appropriate.

### Humanizer pattern import, September 2026

Rules 20 to 22 and gate item 16 were added on 2026-09-10 from blader/humanizer's pattern list (built on Wikipedia's "Signs of AI writing"): borrowed authority (its pattern 17), participial tails (15), significance inflation (13). Its remaining patterns were already covered here or in CLAUDE.md §3. Mechanical detection for the three lives in the "Borrowed weight" group of `~/.claude/library/scripts/slop-scan.py`.
