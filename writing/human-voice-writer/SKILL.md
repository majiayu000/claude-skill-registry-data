---
name: human-voice-writer
description: Write prose that sounds authentically human rather than AI-generated. Use this skill whenever writing long-form content, emails, articles, reports, documentation, blog posts, creative writing, social media copy, proposals, memos, or any text where sounding like a real person matters. Triggers on requests like "write this naturally," "make it sound human," "don't sound like AI," "write like a real person," or any writing task where the user has indicated they want authentic, non-robotic prose. Also use when editing existing text to remove AI-sounding patterns.
version: 1.0.0
---

# Human Voice Writer

Apply research-backed techniques to produce writing that reads as authentically human. Based on findings from CMU/PNAS stylometric research, Nielsen Norman Group style studies, GPTZero/Binoculars detection methodology, Wikipedia's AI Cleanup project, and professional copywriting frameworks.

## Core Rules (Apply to All Writing)

### 1. Ban the AI Vocabulary

Never use these words/phrases unless quoting someone or the user specifically requests them. Full list with research backing in `references/ai-tells.md`.

**Highest-signal bans:** delve, tapestry (metaphorical), landscape (metaphorical), navigate (metaphorical), leverage (as verb), foster, robust, utilize, nuanced, multifaceted, pivotal, underscores, holistic, synergy, paradigm, transformative, groundbreaking, cutting-edge, harness, streamline, cornerstone, encompasses, facilitates, moreover, furthermore, nevertheless, myriad, plethora, ensures/ensures that, respective/respectively

**Banned punctuation:** Em dashes (—), en dashes used as em dashes (–), and double hyphens (--). Never use any of these. Restructure sentences instead: use periods, commas, colons, or parentheses. If a sentence needs an em dash to work, rewrite it so it doesn't.

**Banned rhetorical patterns:** Never use "It's not just X, it's Y" or any variation: "This isn't just..., it's...", "That's not... it's...", "It's not about X, it's about Y", "It's more than just X, it's Y." These false-revelation constructions are a strong AI tell. Just state the point directly. Also ban "Not only X, but also Y" parallel constructions.

**Banned negation-assertion patterns:** AI loves to negate something the reader supposedly believes, then correct them. This includes short dramatic negations used as punchlines ("That's not speculation." "That's not a coincidence."), negation-correction pairs across sentences ("They aren't junior employees. They're senior engineers." "This wasn't an accident. It was a deliberate choice."), and any pattern where you say what something *isn't* before saying what it *is*. These rules apply everywhere in the output: body text, headings, titles, subheadings, and any other text. A negation-assertion in a heading is just as much of an AI tell as one in a paragraph. Human writers occasionally do this, but AI does it constantly because it creates easy dramatic tension. Instead of negating a strawman, just state the positive claim directly. If the contrast matters, fold it into one sentence rather than setting up a two-beat negate-then-assert rhythm.

**Banned false-choice framings:** "Whether you're a beginner or a seasoned pro...", "Whether you're looking to X or Y..." These are filler. Cut them entirely or address the reader directly.

**Banned signposting:** "Let's break this down," "Here's the thing," "Let me explain," "Let's dive in," "Let's unpack this." Just make the point. Real writers don't announce that they're about to explain something.

**Banned filler phrases:** "at its core," "at the end of the day," "straightforward," "when it comes to," "the power of [X]," "the beauty of [X]," "as we discussed earlier," "building on our previous conversation"

**Banned openings:** "In today's rapidly evolving...", "In the realm of...", "In an era where...", "In a world where...", "When it comes to...", "Imagine a world where...", "Picture this:"

**Banned hedges:** "It's important to note...", "It's worth mentioning...", "Based on the information provided...", "As we can see..."

**Banned closings:** "In conclusion" followed by restating everything, "Embrace the power of...", generic calls to action

**Banned filler constructions:**
- Hollow intensifiers: "truly," "really," "incredibly," "absolutely," "extremely." Pick one per piece at most, or skip them entirely. AI scatters these everywhere for false emphasis.
- "From X to Y" sweeps: "From onboarding to offboarding," "From startups to enterprises." This gestures at breadth without saying anything. Be specific about what you actually mean.
- Paired synonyms: "clear and concise," "robust and scalable," "simple and intuitive," "quick and easy." Pick one adjective. Two is AI doubling up for emphasis it didn't earn.
- Overused question-then-answer: "What makes this different? It's the approach." Once per piece is fine. More than that is a tell.
- "By [gerund]" chains: "By implementing this framework, teams can..." or "By leveraging AI, organizations can..." AI uses these to sound procedural. Restructure: "If you implement this framework, teams will..." or just say what happens.
- "Allows you to" / "enables you to" / "empowers you to": Product-copy AI defaults. Say what the thing does directly. "The tool tracks expenses" not "The tool allows you to track expenses."
- Weasel quantifiers: "significant," "substantial," "considerable," "notable," "meaningful" used without actual numbers. If you can quantify it, quantify it. If you can't, say "large" or "small" and move on.
- "Key" as an adjective: "Key takeaways," "key insights," "key benefits." AI overuses this. Say "main," "biggest," or drop the qualifier entirely.
- Transition word overuse: "Additionally," "however," "consequently," "therefore," "thus." AI uses these as paragraph glue far more than humans do. Most of the time the connection is obvious without them. Just start the next sentence.

Use plain replacements. "Use" not "utilize." "Help" not "facilitate." "Try" not "endeavor." "Show" not "demonstrate."

### 2. Vary Sentence Length (Burstiness)

This is the single highest-impact humanization technique. AI detection tools use sentence length uniformity as a core metric.

- Mix short punches (3-8 words) with long compound sentences (25-35 words)
- No three consecutive sentences within 5 words of each other in length
- Aim for a standard deviation of 8+ words across sentence lengths in any given paragraph
- Use fragments for emphasis. One word works. So do two.
- Start 10-15% of sentences with "And" or "But"
- Never start 3+ consecutive sentences with the same word

### 3. Eliminate Repetitive Sentence Patterns

- **Ban anaphora chains.** Never repeat the same sentence structure with slight word swaps. "It means better outcomes. It means faster delivery. It means less waste." sounds like a keynote speech, not a person. Say it once, differently.
- **Ban vague "This" openers.** Do not start sentences with "This" as a vague referent: "This underscores...", "This highlights...", "This reflects..." Name the actual subject. If you can't, the previous sentence wasn't clear enough.
- **Ban colon-to-tidy-list constructions.** Do not use "Three things matter: clarity, consistency, and communication" or similar. AI loves neat trinities. Humans don't organize their thoughts into perfect groupings of three abstract nouns.
- **Limit semicolons.** Most people rarely use them in professional writing. AI over-relies on them to stitch together related ideas. Use a period and start a new sentence instead.

### 4. Break Structural Templates

- Do not follow topic-sentence/elaboration/summary for every paragraph
- Vary paragraph length (1-sentence paragraphs mixed with 5-6 sentence paragraphs)
- No summary paragraphs that restate what was already said
- Allow the point to arrive at the end sometimes, not always up front
- Use parentheticals and asides where natural
- Vary paragraph openings. Do not start every paragraph the same way (with a claim, a noun phrase, a prepositional phrase). Mix it up: start some with a question, some with a short fragment, some with a dependent clause, some mid-thought.

### 5. Kill the Assistant Register

- Take positions instead of defaulting to "both sides have merit"
- Express genuine uncertainty ("I'm not sure about this" not "It's important to consider multiple perspectives")
- Use contractions in anything less than fully formal writing
- No sycophantic openings ("Great question!") or generic closings
- Match register to context: casual when casual is called for, formal when formal is called for

### 6. Eliminate Deep Grammatical AI Signatures

Per CMU/PNAS research, these are the hardest patterns to detect but the most statistically significant:

- **Avoid trailing participial phrases.** "...improving efficiency," "...highlighting its significance" are AI's most distinctive grammatical pattern (2-5x human frequency). Restructure into separate sentences or "which" clauses.
- **Reduce nominalizations.** "We decided" not "the decision was made." "Sales dropped" not "a decrease in sales was observed." LLMs nominalize at 1.5-2x human rates.
- **Use active voice by default.** Passive voice is fine sometimes, but AI overuses it as a hedging mechanism.

### 7. Calibrate Length to Format

AI over-writes by default. Fight this aggressively.

- A Slack message should be a few sentences. Not three paragraphs.
- A short email should be 3-5 sentences. Not a page.
- A one-paragraph answer should stay one paragraph. Don't expand it to four.
- Match the length the user would expect for the format. When in doubt, shorter is more human.
- If the user asks for "a quick summary" or "a short note," that means short. Actually short.

## Workflow: Writing New Content

1. **Read the user's request.** Determine the register (casual, professional, formal, technical) and format (email, article, report, etc.).
2. **Consult `references/ai-tells.md`** if uncertain whether a word or pattern is an AI tell.
3. **Write the first draft** applying all seven core rules above.
4. **Self-review pass:** Scan for:
   - Any banned vocabulary that slipped through (including "ensures," "key," "respective/respectively")
   - Any em dashes, en dashes, or double hyphens
   - Any "it's not just X, it's Y" or "not only X, but also Y" patterns
   - Negation-assertion patterns in all text including headings, titles, and subheadings: short dramatic negations ("That's not speculation."), negation-correction pairs ("They aren't X. They're Y."), saying what something isn't before what it is
   - Hollow intensifiers (truly, really, incredibly, absolutely, extremely)
   - "From X to Y" sweep constructions
   - Paired synonym adjectives (clear and concise, quick and easy)
   - "The power of" or "the beauty of" constructions
   - "Imagine" or "Picture this" openings
   - "By [gerund]" chains
   - "Allows you to" / "enables you to" / "empowers you to"
   - Weasel quantifiers without actual numbers (significant, substantial, considerable)
   - Transition word overuse (additionally, however, consequently, therefore, thus)
   - "As we discussed earlier" or recap openers in multi-turn conversations
   - Three or more consecutive sentences of similar length
   - Anaphora chains (repeated sentence structure with word swaps)
   - Sentences starting with vague "This" as referent
   - Paragraphs that all follow the same structure or open the same way
   - Trailing participial phrases
   - "Helpful assistant" hedging language
   - Over-signposting ("Let's break this down," "Here's the thing")
   - Semicolon overuse
   - Overused question-then-answer pattern
   - Sycophantic openings/closings
   - Output length appropriate for the format (emails short, Slack shorter)
5. **Fix issues found** in the self-review before delivering.

## Workflow: Editing Existing Text

When asked to "humanize" or "de-AI" existing text:

1. **Read `references/ai-tells.md`** to identify all Tier 1 and Tier 2 patterns present.
2. **Read `references/humanization-techniques.md`** for the full technique library.
3. **Identify specific problems** in the text: banned words (including "ensures," "key," "respective/respectively"), em dashes/en dashes, false-revelation constructions, negation-assertion patterns, "not only...but also," hollow intensifiers, paired synonyms, "from X to Y" sweeps, "the power of" constructions, "imagine" openings, "by [gerund]" chains, "allows/enables/empowers you to," weasel quantifiers without numbers, transition word overuse, recap openers, uniform sentence lengths, anaphora chains, vague "This" openers, structural monotony, repetitive paragraph openings, assistant register, trailing participial phrases, nominalizations, semicolon overuse, over-signposting, overused question-then-answer, excessive length for format.
4. **Rewrite** applying fixes at all four layers (word, sentence, structure, tone).
5. **Preserve the original meaning and information.** Humanizing means changing how something is said, not what is said.

## Workflow: Matching a Specific Voice

When the user provides writing samples or asks to match a particular voice:

1. **Read `references/humanization-techniques.md`** for the 16-dimension voice framework.
2. **Analyze the samples** across all 16 dimensions, producing specific, measurable observations (not adjective descriptions).
3. **Preserve the sample's structure.** Rhythm is part of voice. Do not flatten paragraph breaks, sentence lengths, or formatting patterns from the samples.
4. **Generate writing rules** from the analysis: sentence length range, contraction frequency, vocabulary level, punctuation habits, paragraph architecture, stance patterns.
5. **Write using those rules** combined with the core humanization rules above.

**Key finding:** Actual writing samples outperform tone descriptors, which outperform author/celebrity name references (Nielsen Norman Group). Always prefer sample analysis over abstract style descriptions.

## Examples: Bad to Good

These show common AI patterns and how to fix them. Learn the transformations, not just the rules.

**Em dash removal:**
- Bad: "The team worked late into the night — and it paid off."
- Good: "The team worked late into the night. It paid off."

**False-revelation fix:**
- Bad: "It's not just a tool, it's a complete platform for collaboration."
- Good: "It's a complete collaboration platform."

**Hollow intensifier removal:**
- Bad: "This is a truly incredible opportunity for the team."
- Good: "This is a rare opportunity for the team."

**Paired synonym fix:**
- Bad: "We need a clear and concise strategy."
- Good: "We need a clear strategy."

**"From X to Y" sweep fix:**
- Bad: "From hiring to onboarding to performance reviews, our platform handles it all."
- Good: "The platform handles hiring, onboarding, and performance reviews." (Or better: pick the one that matters most and talk about it specifically.)

**Vague "This" fix:**
- Bad: "Revenue grew 30% last quarter. This underscores the effectiveness of the new strategy."
- Good: "Revenue grew 30% last quarter. The new pricing model drove most of that growth."

**Trailing participial fix:**
- Bad: "The company launched a new product line, expanding its market presence significantly."
- Good: "The company launched a new product line. It expanded their market presence significantly."

**Anaphora chain fix:**
- Bad: "It means faster deployments. It means fewer bugs. It means happier engineers."
- Good: "Deployments got faster, bugs dropped, and engineers stopped dreading release day."

**Question-then-answer overuse fix:**
- Bad: "What sets this apart? The architecture. What makes it reliable? The testing. What drives adoption? The simplicity."
- Good: "The architecture sets it apart, and the testing keeps it reliable. People adopt it because it's simple."

**Length calibration:**
- Bad (when asked to write a quick Slack update): Three paragraphs with headers explaining the full context, methodology, and next steps.
- Good: "Wrapped up the migration. No issues. We're clear to deploy tomorrow."

**"Ensures" removal:**
- Bad: "This process ensures alignment across all stakeholders."
- Good: "Everyone ends up on the same page." (Or better: cut the sentence if the previous one already made the point.)

**"By [gerund]" fix:**
- Bad: "By implementing automated testing, teams can reduce bug counts significantly."
- Good: "Automated testing cuts bug counts."

**"Allows you to" fix:**
- Bad: "The dashboard allows you to monitor performance in real time."
- Good: "The dashboard monitors performance in real time."

**Weasel quantifier fix:**
- Bad: "We saw a significant improvement in response times."
- Good: "Response times dropped 40%." (Or if you don't have the number: "Response times dropped noticeably.")

**"Key" overuse fix:**
- Bad: "Here are the key takeaways from the meeting."
- Good: "Here's what mattered from the meeting."

**Transition word fix:**
- Bad: "The migration completed on schedule. Additionally, the team resolved three outstanding bugs. Furthermore, performance testing showed no regressions."
- Good: "The migration completed on schedule. The team also resolved three outstanding bugs, and performance testing showed no regressions."

**Negation-assertion fix (dramatic negation):**
- Bad: "That's not speculation." or "That's not a coincidence."
- Good: Just cut it. The preceding claim should stand on its own evidence. If you need emphasis, use a specific detail instead of a dramatic negation.

**Negation-assertion fix (negation-correction pair):**
- Bad: "They aren't junior employees who don't know better. They're senior engineers and experienced managers."
- Good: "The applicants are senior engineers and experienced managers." (State who they are. No need to first say who they aren't.)

**Negation-assertion fix (what-it-isn't-then-what-it-is):**
- Bad: "Remote work stopped being a perk around 2021. It's infrastructure now."
- Good: "Remote work became infrastructure around 2021." (Fold the contrast into one sentence instead of the two-beat negate-then-assert rhythm.)

**Recap opener fix (multi-turn):**
- Bad: "As we discussed earlier, the deployment strategy involves three phases."
- Good: "The deployment has three phases." (Just pick up where you left off.)

## When Rules Conflict

These rules will sometimes pull in opposite directions. Here's how to resolve that:

- **Fragments vs. clarity:** Use fragments for emphasis and rhythm, but not if they make the meaning unclear. A fragment that confuses the reader is worse than a complete sentence that bores them.
- **"And/But" starters vs. varied openings:** The 10-15% guideline for "And" and "But" starters is a tool for variety, not a quota. If you've already varied your openings well, you don't need to force an "And" in.
- **Short sentences vs. burstiness:** Short punches work because they contrast with longer sentences. Five short sentences in a row isn't burstiness. It's choppy.
- **Avoiding banned patterns vs. natural flow:** If removing a banned construction makes the sentence awkward or unclear, find a third option. The goal isn't to mechanically avoid a checklist. The goal is to sound like a person.
- **General principle:** When two rules conflict, choose whichever option sounds more like something a human would actually write. Read it out loud. If it sounds weird, it is weird.

## What NOT to Do

- Do not overcorrect into deliberately bad writing. The goal is natural, not sloppy.
- Do not inject forced slang or colloquialisms that don't fit the register.
- Do not add fake personal anecdotes unless the format calls for it and the user approves.
- Do not sacrifice clarity for style. If a "boring" sentence is the clearest way to say something, use it.
- Do not apply these rules to code, data tables, or structured technical output where they are irrelevant.

## Reference Materials

### AI Writing Tells (references/ai-tells.md)
Complete banned vocabulary list, banned structural patterns, and statistical deep patterns organized by detection significance tier. Sourced from Wikipedia AI Cleanup project, Pangram Labs, CMU/PNAS research, GPTZero methodology.

**When to read:** When uncertain whether a word or pattern is an AI tell, or when editing existing text to remove AI patterns.

### Humanization Techniques (references/humanization-techniques.md)
Detailed technique library covering all four layers (word, sentence, structure, tone) with specific rules and the 16-dimension voice capture framework.

**When to read:** When doing deep editing/humanization of existing text, when matching a specific person's voice, or when the writing task requires particularly careful human-sounding output.
