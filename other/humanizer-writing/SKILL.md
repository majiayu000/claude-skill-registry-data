---
name: humanizer-writing
description: |
  Rewrite AI-sounding text so it reads naturally without changing what it says.
  Use when editing or reviewing prose for inflated claims,
  sales language, vague sources, repetitive structure, stock AI words, passive
  voice, filler, or chatbot artifacts. Based on Wikipedia's "Signs of AI writing."
  Use at writing time (before and while drafting) as well as at edit time.
  Triggers: "hw", "humanizer-writing", "write this so it doesn't sound like AI",
  "spot AI writing", "AI tells", "de-AI this draft".
license: MIT
metadata:
  version: "1.0.0"
  based_on: "github:blader/humanizer@e2e92e7b4b82 (2.11.2)"
  research: "2026-09-03 NotebookLM, 83 sources"
---

# Humanizer-Writing: write and edit so it doesn't read as AI

Rewrite AI-sounding text so it reads like the writer, not a chatbot. Do not change what it says or make up details.

The patterns below come from Wikipedia's ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

## What to do

When given text to humanize:

1. **Find AI patterns.** Check the text against the patterns below.
2. **Keep every claim.** You may shorten dull parts, expand useful parts, and merge or split paragraphs. Keep the information even when you change the structure.
3. **Do not invent facts.** Do not add a fact, name, number, date, quote, or citation unless it comes from the source or the user. If a sentence needs a missing detail, ask for it or use a simpler sentence. You may add an opinion or reaction when the writer's voice calls for one, but you may not add a factual claim. Fiction is exempt because invented details are part of the task.
4. **Match the voice.** Use the right tone for the text, such as formal, casual, or technical. Add personality only when the text and the writer call for it.

The input type controls what you return. See [How to return the result](#how-to-return-the-result). Use the same rewrite process in every mode.

For format calibration on a specific artifact (CV, email, LinkedIn post, docs), run the `content-polish` skill, which sequences this skill with a proofreading pass.

## Before you draft (writing-time practices)

Most AI tells are set before the first sentence. Removing them afterward is more work than not writing them.

- **Take a stance.** Decide what you think, then write that. Surveying both sides ("While X has merits, Y also offers benefits") is the default posture of a model tuned to be agreeable, and it reads that way. If the honest answer is "it depends," say what it depends on.
- **One concrete detail per claim.** Before drafting, list the things only you can supply: a real number, a dated incident, a client's actual words, a mistake you made. "We cut proposal turnaround from 12 days to 4" carries a claim that "streamlining workflows improves efficiency" cannot.
- **Name sources with dates.** Write "Kobak et al., *Science Advances*, July 2025" instead of "studies show." If you cannot name it, cut the claim rather than gesture at it.
- **Decide the structure before you draft.** A bulleted list, a bold mini-heading, and a closing summary are choices. Models emit them by reflex. Ask whether the argument needs a list, or whether the list is dodging the work of writing transitions.
- **Write to one reader.** Pick a specific person and write to them. Prose written for everyone lands on the average register, which is where the model already lives.
- **Draft messily first.** An unedited braindump has natural unevenness: fragments, detours, a paragraph that runs too long. Keep some of it. Polish removes tells, but it also removes voice.
- **If a model drafts for you, constrain it.** Do not ask for "better" or "more professional"; that request summons the defaults. Give it a sample of your own writing, a named reader, a sentence-length ceiling, and a list of banned words.

## 60-second decision tree

Run this before the full pattern pass. Each check is answerable in seconds.

1. **Cut the ends.** Delete the first and last paragraph. Did the piece lose information? If not, they were throat-clearing. Leave them out.
2. **Look, do not read.** Are the paragraphs the same shape on the page? Uniform blocks mean uniform sentences. Put one short sentence after the longest one.
3. **Count the triples.** Do lists, adjectives, and examples keep arriving in threes? Cut one item or add a fourth.
4. **Chase one claim.** Take the strongest claim. Is it attached to a named, dated source? If it says "studies show," name the study or delete the claim.
5. **Find the hedge.** Does any paragraph qualify itself more than once ("it is important to note," "generally speaking")? Strike the phrase and state the claim.

Passing all five means stop. Do not run the full pass. A clean draft that gets a full pattern sweep usually comes back worse.

## Match the writer's voice

If the user provides a writing sample (their own previous writing), analyze it before rewriting:

1. Read the sample first. Note its sentence length, word choice, paragraph openings, punctuation, repeated phrases, and transitions.
2. Match those habits. Do not replace casual words with formal ones or remove deliberate quirks.
3. If there is no sample, use the guidance below.

A writing sample takes priority over these style rules. If the sample uses em dashes, keep them at about the same rate. Do not apply §14 as a ban.

## Add personality only when it fits

Removing AI patterns is only half the job. The result should still sound like a person.

Use personality in blog posts, essays, opinions, and personal writing when it fits the writer. Keep reference, technical, legal, and factual text neutral. Do not add opinions or first-person language where they do not belong.

When personality fits, keep the writer's opinions, uncertainty, mixed feelings, humor, asides, and uneven rhythm. Never invent facts to make the text feel personal.

## Content patterns

### 1. Inflated claims about importance and legacy

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted
**Problem:** AI writing often claims that ordinary details mark a major change, prove a legacy, or reflect a broad trend.
**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.
**After:**
> The Statistical Institute of Catalonia was established in 1989, part of a wider decentralization of administrative functions in Spain.

### 2. Name-dropping to prove importance

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence
**Problem:** AI writing often lists well-known publications or follower counts to prove that a person matters. The list usually gives no useful context.
**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.
**After:**
> Her views have been cited in The New York Times and the BBC.

If the source explains what the person said and where, keep that useful citation. Do not invent context for a shorter version.

### 3. Shallow analysis with -ing phrases

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...
**Problem:** AI writing often adds an -ing phrase to make a simple fact sound deeper than it is.
**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.
**After:**
> The temple is painted blue, green, and gold, colors meant to evoke Texas bluebonnets and the Gulf of Mexico.

### 4. Sales language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning
**Problem:** AI writing often sounds like an advertisement, especially when it describes places, culture, products, or organizations.
**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.
**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia.

### 5. Vague sources

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)
**Problem:** AI writing often assigns a claim to unnamed experts, critics, reports, or observers.
**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.
**After:**
> Researchers and conservationists study the Haolai River for its unusual characteristics.

Name a real source when the source text provides one. Otherwise, remove the unsupported claim. Never invent a source.

### 6. Formulaic challenges and outlook sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook
**Problem:** AI articles often add a stock section about challenges, future prospects, or continued growth. These sections usually repeat vague claims instead of adding facts.
**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.
**After:**
> Korattur has recurring traffic congestion and water shortages.

Add details such as dates or public actions only when they come from the source or the user.

## Language and grammar patterns

### 7. Overused AI words

**High-frequency AI words:** Actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, gate/gated/gating (figurative; preserve established technical usage), highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, quietly, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant
**Problem:** AI writing uses these words much more often than most people do, especially in groups.
**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.
**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

### 8. Avoiding is and are

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]
**Problem:** AI writing often replaces simple verbs such as *is*, *are*, and *has* with longer phrases.
**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.
**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

### 9. Not X but Y and clipped negative endings
**Problem:** AI writing overuses forms such as "Not only...but..." and "It's not just X, it's Y."

It also adds clipped endings such as "no guessing" instead of writing a clear clause.
**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.
**After:**
> The heavy beat adds to the aggressive tone.
**Before (tailing negation):**
> The options come from the selected item, no guessing.
**After:**
> The options come from the selected item without forcing the user to guess.

### 10. Forced groups of three
**Problem:** AI writing often forces ideas into groups of three to sound complete.
**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.
**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.

### 11. Changing names and repeating sentence openings
**Problem:** AI writing handles repetition by rule instead of by ear. It may keep renaming the same person or thing. It may also start several sentences with the same subject, often *she* or *he*.

Use one clear name for the same subject. For repeated openings, merge sentences, change the subject when that helps, or begin with the action.
**Before (synonym cycling):**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.
**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.
**Before (repeated openings):**
> She noted the door. She noted the lock on it. She filed both away.
**After:**
> She noted the door and its lock, then filed both away.

Do not ban the repeated word. Fix the repeated sentence pattern. The remaining sentence may still start with "She."

### 12. False from X to Y ranges
**Problem:** AI writing often uses "from X to Y" when X and Y do not form a real range.
**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.
**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

### 13. Passive voice and missing subjects
**Problem:** AI writing often hides who acts or drops the subject. Use active voice when it makes the actor and action clearer.
**Before:**
> No configuration file needed. The results are preserved automatically.
**After:**
> You do not need a configuration file. The system preserves the results automatically.

## Style patterns

### 14. Em and en dashes

**Rule:** The final rewrite must not contain em dashes (—) or en dashes (–), unless the writer's sample uses them. Replace a dash with a period, comma, colon, or parentheses, or rewrite the sentence. Also check for spaced dashes (` — `) and double hyphens (` -- `) used as dashes.
**Before:**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.
**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.
**Before:**
> The new policy — announced without warning — affects thousands of workers. The changes -- long overdue according to critics -- will take effect immediately.
**After:**
> The new policy, announced without warning, affects thousands of workers. The changes, long overdue according to critics, will take effect immediately.

Before returning the rewrite, search for `—` and `–`. Remove each one unless the writer's sample uses that mark. In that case, match the sample's rate.

**Why the habit exists.** Freeburg (arXiv:2603.27006, 2026) argues the em dash is markdown leaking into prose: models trained on markdown read `---` as a structural joint, so when you ban headings and lists, the structural impulse escapes through the one mark that is legal in both registers. It is also decision-deferral. The model avoids choosing between a period, a comma, and a parenthesis by using the mark that could be any of them. Rates run from 0.00 per 1,000 words (Llama, suppressed in post-training) to 10.62 (GPT-4.1), against a human baseline of 3.23. Density and job-switching matter more than presence: three dashes in one short paragraph, each doing a different grammatical job, is the tell.

**Colons and semicolons carry the same habit.** Watch the bold-label-plus-colon list item (§16) and the colon that introduces a triplet. A semicolon splicing clauses that want to be separate sentences is the same deferral in a different mark.
**Before:**
> Caching helps: it cuts latency; it reduces database load; it improves the user experience.
**After:**
> Caching cuts latency and takes read load off the database.

### 15. Too much bold text
**Problem:** AI chatbots often bold words and phrases without a clear reason.
**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.
**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

### 16. Lists with bold mini-headings
**Problem:** AI writing often uses vertical lists in which every item starts with a bold label and a colon.
**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.
**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

### 17. Title case in headings
**Problem:** AI chatbots often capitalize every main word in a heading.
**Before:**
> ## Strategic Negotiations And Global Partnerships
**After:**
> ## Strategic negotiations and global partnerships

### 18. Emojis
**Problem:** AI chatbots often add emojis to headings and list items as decoration.
**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting
**After:**
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

### 19. Curly quotation marks
**Problem:** ChatGPT often uses curly quotes (“...”) where the writer or target format uses straight quotes ("...").
**Before:**
> He said “the project is on track” but others disagreed.
**After:**
> He said "the project is on track" but others disagreed.

**Model split (dated 2026-09):** OpenAI and DeepSeek models emit curly quotes and curly apostrophes by default; Claude and Gemini emit straight ones. So a text that mixes straight and curly apostrophes usually had two sources pasted together, and curly quotes inside a code sample mean nobody read the text after pasting. Match the target format: straight marks in code, config, and Markdown source, and whatever the publication uses in prose.

## Chatbot patterns

### 20. Chatbot text left in the answer

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., Want me to...?, Want me to give examples?, Should I continue?, let me know, here is a...
**Problem:** A chatbot's greeting, offer, or closing sometimes remains in text that should stand on its own.
**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.
**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

Also delete machine residue that never had a conversational form: JSON attribution fragments such as `{"attribution":{"attributableIndex":"0-1"}}`, bracketed citation markers like `[3, 14]` pointing at a reference list that is not in the document, and stray tool or tag names. Check the end of the text and the end of each section, where this residue collects.

### 21. Knowledge-limit disclaimers and guesses

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information, not publicly available, maintains a low profile, keeps personal details private, prefers to stay out of the spotlight, likely [grew up/studied/began], it is believed that
**Problem:** Older models may mention the date when their knowledge ends. A model may also explain that it could not find a source, then fill the gap with a plausible guess. State what the source does not show, or remove the sentence. Do not present a guess as a fact.
**Before (cutoff disclaimer):**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.
**After:**
> The company's founding date is not documented in the available sources. (Or cut the sentence. State a date only if a source provides one.)
**Before (speculative gap-fill):**
> Information about her early life is not publicly available, suggesting she maintains a low profile and keeps personal details private. She likely grew up in a middle-class household, which shaped her later interest in education reform.
**After:**
> Her early life is not documented in the available sources. (Or omit the section.)

### 22. Overly agreeable tone
**Problem:** AI assistants often praise the user or agree before giving the answer.
**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.
**After:**
> The economic factors you mentioned are relevant here.

## Filler and hedging

### 23. Filler phrases

**Before → After:**
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"

### 24. Too many qualifiers

**Phrases to watch:** to be fair, it's also possible, could potentially, might arguably, in some cases it may, this is an inference
**Problem:** Repeated editing can add one qualifier after another until every claim sounds uncertain. Keep a qualifier only when the source supports it and the meaning needs it. Remove caveats that only repair an earlier overstatement.
**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.
**After:**
> The policy may affect outcomes.

### 25. Generic positive endings
**Problem:** AI writing often ends with vague optimism instead of the last useful fact.
**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.
**After:**
> (Cut the paragraph. End on the last concrete fact instead of a send-off. If the source states real plans, use those.)

### 26. Too many hyphenated word pairs

**Words to watch:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end
**Problem:** AI writing often hyphenates these pairs everywhere. Keep the hyphen before a noun when grammar needs it, as in `a high-quality report`. Drop it after the noun, as in `the report is high quality`.
**Before:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross-functional, the report is high-quality, and the methodology is data-driven.
**After:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross functional, the report is high quality, and the methodology is data driven.

### 27. Pretending to reveal a deeper truth

**Phrases to watch:** The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter
**Problem:** AI writing uses these phrases to make an ordinary point sound like a hidden truth.
**Before:**
> The real question is whether teams can adapt. At its core, what really matters is organizational readiness.
**After:**
> The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.

### 28. Announcing the next point

**Phrases to watch:** Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado, heads up, quick note, before I forget
**Problem:** AI writing often announces the next point instead of stating it. A casual phrase such as "one thing that bit me" can have the same problem. Remove the announcement, not just its formal tone.
**Before:**
> Let's dive into how caching works in Next.js. Here's what you need to know.
**After:**
> Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.
**Before (casual register):**
> One thing that bit me hard, so pay attention to this part: the webpack dev server doesn't send the CORS header by default.
**After:**
> The webpack dev server doesn't send the CORS header by default.

### 29. A heading repeated in the first sentence

**Signs to watch:** A heading followed by a one-line paragraph that simply restates the heading before the real content begins.
**Problem:** AI writing often follows a heading with a sentence that only repeats the heading. Remove the repeated sentence.
**Before:**
> ## Performance
>
> Speed matters.
>
> When users hit a slow page, they leave.
**After:**
> ## Performance
>
> When users hit a slow page, they leave.

### 30. Writing about the previous version
**Problem:** Documentation and comments should describe the current behavior. Mention the previous version only in change logs, release notes, migration guides, and other documents about change.
**Before:**
> This function was added to replace the previous approach of iterating through all items, which caused O(n²) performance.
**After:**
> This function uses a hash map for O(1) lookups, avoiding the O(n²) cost of naive iteration.

### 31. Forced punchlines and dramatic fragments
**Problem:** AI writing often turns each sentence into a dramatic closing line. One short sentence can add emphasis. A row of short fragments usually feels forced.
**Before:**
> Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.
**After:**
> AlphaEvolve changed the search because it did not favor symmetry or human-looking designs. That made some of the older assumptions less useful.

### 32. Formulaic sayings

**Words to watch:** X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of
**Problem:** AI writing often turns an ordinary claim into a saying that sounds deep but adds no detail. Replace the saying with the specific claim.
**Before:**
> Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.
**After:**
> Symmetric layouts often feel more predictable to users. Teams can over-optimize workflows and miss how people actually use them.

### 33. Fake-candid openings

**Phrases to watch:** Honestly?, Look, Here's the thing, The thing is, Let's be honest, Real talk, when used as standalone hooks or fake-candid pauses before an ordinary point.
**Problem:** AI writing often starts with a staged pause or claim of honesty before making a routine point. State the point directly.
**Before:**
> Is it worth the price? Honestly? It depends on how often you'll use it.
**After:**
> Whether it's worth the price depends on how often you'll use it.

### 34. Answering objections no one raised

**Phrases to watch:** This isn't (mainly/really) about, I'm not saying/arguing/trying to, To be clear, Don't get me wrong, This is not to say, You could argue/frame this differently but, Some might say... but
**Problem:** AI writing may answer an objection that does not appear in the text. Watch for an unattributed statement about what the writer does not mean, especially when the topic appears nowhere else. A direct claim such as "the API is not thread-safe" is not this pattern.
**Before:**
> This isn't mainly about prompt length, and I'm not arguing that documentation doesn't matter. You could categorize the problem another way, but the issue is whether the agent can use the instruction when it acts.
**After:**
> The issue is whether the agent can use the instruction when it acts.

Remove only the unsupported defense. If it contains a real claim, state that claim directly. Keep an objection when the text names its source or answers it in full.

### 35. Rejecting fake alternatives

**Phrases to watch:** A tempting option/approach would be, One might be tempted to, An obvious approach would be, You might think... but, It would be easy to just, Some would suggest
**Problem:** AI writing may introduce an option that no reader would consider, reject it in a clause, and never mention it again. This often leaves an old drafting idea in the final text. Remove the fake option and state the real constraint directly.
**Before:**
> Session tokens are rotated every 24 hours. A tempting approach would be to rotate them by restarting the auth service on a cron job, but that would drop every active session. Rotation happens in place, and clients refresh transparently.
**After:**
> Session tokens are rotated every 24 hours, in place, and clients refresh transparently.

One rejected option may be valid. Several short, unrelated rejections are a stronger sign. Ask what new information each sentence adds. If it only records an earlier edit, rewrite the paragraph around its main point.

## Grammatical register

### 36. Participial tailing clauses

**Words to watch:** allowing for, enabling, resulting in, reducing, increasing, driving, leading to, thereby
**Problem:** GPT-4o attaches present participial clauses at 5.3 times the human rate (Reinhart et al., *PNAS*, 2025). §3 covers the ones that fake depth. This is the plainer version: two or three facts get folded into a trailing clause, so nothing after the comma gets its own subject or its own verb. Give each fact a sentence, or make the link explicit with *so*, *because*, or *which*.
**Before:**
> The scheduler batches writes every 200ms, reducing lock contention and allowing for higher throughput on shared tables.
**After:**
> The scheduler batches writes every 200ms. That cuts lock contention, so shared tables take more throughput.

### 37. Nominalisations

**Words to watch:** utilization, implementation, optimization, conceptualization, prioritization, facilitation, the provision of, the application of
**Problem:** GPT-4o turns verbs into abstract nouns at 2.1 times the human rate. The noun then needs a weak verb (*conduct*, *perform*, *achieve*, *was*) to carry it, and the human actor disappears. Turn the noun back into the verb and name who did it.
**Before:**
> Optimization of resource utilization was achieved through the implementation of caching.
**After:**
> We added caching, and the service now uses less memory.

## Stock scaffolding

### 38. Common surge connectors

**Words to watch:** across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within
**Problem:** Kobak et al. (*Science Advances*, 2025) found these ten ordinary words carry an 11.0% combined excess-frequency gap in 2024 PubMed abstracts, enough on their own to date a text as post-ChatGPT. Any one of them is fine. Three or four in a paragraph is the tell. *additionally* and *crucial* also appear in §7's list; §7 is about a word being wrong for the writer, this is about the cluster dating the text. Cut them, or replace them with the actual relationship between the sentences.
**Before:**
> Additionally, the model exhibited notably improved accuracy across all datasets, offering comprehensive insights within the clinical domain.
**After:**
> The model was more accurate on all six datasets, including the two clinical ones.

### 39. Symmetrical openers, transitions, and closers

**Openers to watch:** In today's digital age, In the ever-evolving landscape of X, With the advent of, Imagine a world where, As a college student
**Transitions to watch:** Furthermore, Moreover, Consequently, This means that, One key benefit is, Another important factor is, It's worth noting that, In terms of, However, one must consider
**Closers to watch:** Ultimately, In essence, At the end of the day, To wrap things up, Remember [restated thesis], Here's the kicker, And here's the part most people miss
**Problem:** These are safe placeholder phrases that orient a reader without telling them anything, and they collect at the seams of a piece. That is why the first and last paragraph of an AI draft usually carry no information. Delete them and answer the reader's question in the first hundred words instead.
**Before:**
> In today's fast-paced digital landscape, caching is more important than ever. [...] Ultimately, caching remains a crucial tool for any modern team.
**After:**
> Next.js caches at four layers, and two of them ignore your revalidate setting. [...] The router cache is the one that will bite you in staging.

### 40. Metaphor inflation and B2B high drama

**Words to watch:** seam/seamless, beacon, symphony, tapestry, roadmap, journey, unwavering, Swiss-Army knife, at the forefront, game-changer, unveil, unleash, unmask, robust, leverage, facilitate
**Problem:** A plain noun gets traded for a dramatic one and a plain verb (*show*, *add*, *use*) for a brochure verb. The sentence gains volume and loses the fact. The matching habit is intensifier inflation: *incredibly*, *wildly*, *massively* stuck to ordinary numbers.
**Before:**
> We're unveiling a robust, game-changing platform that seamlessly orchestrates a symphony of integrations across your entire journey.
**After:**
> The platform connects to Stripe, Slack, and HubSpot. Setup takes about ten minutes.

## Rhythm and shape

### 41. Metronomic cadence and rectangle paragraphs
**Problem:** Read the passage out loud. If every sentence takes the same breath, it is machine cadence. Models cluster sentences at 15 to 25 words, land a type-token ratio of 44 to 49%, and score 52 to 55 on sentence-length consistency, all far tighter than human writing, which swings from fragments to long clause-heavy sentences. Paragraphs come out as visually identical blocks running claim, example, restatement. Those numbers are evidence for reading a draft, not a target to write toward: do not count words and do not rewrite to hit a metric. Fix it by ear. Follow a long sentence with a short one. Let one paragraph run six sentences and the next run one.
**Before:**
> The cache stores results for repeated requests. This reduces the load on the database server. Response times improve for the end user. Teams should monitor the hit rate regularly.
**After:**
> The cache holds results for repeated requests, which takes most of the read load off Postgres and roughly halves p95. Watch the hit rate. Under about 70% you are paying the memory cost for nothing.

### 42. Meta process narration and abstract headings

**Phrases to watch:** after reviewing the available sources, an examination of the history shows, upon closer analysis, below we will analyze, in this section we explore
**Headings to watch:** Why the reception was mixed, Key contributions and lasting impact, Understanding the fundamentals of X
**Problem:** A chatbot narrates the act of reading the facts; a writer who knows them states them. The same reflex produces headings that summarize the section's conclusion before the section runs. Human headings are short labels: Reception, Early life, Caching, Pricing.
**Before:**
> ## Key contributions and lasting impact
>
> After reviewing the available sources, an examination of Hopper's career shows significant influence on early compilers.
**After:**
> ## Compilers
>
> Hopper wrote the A-0 compiler in 1952 and later led the team that specified COBOL.

## Rhetorical posture

### 43. Hedge stacking, sycophancy, and the no-screw-up tell

**Phrases to watch:** it is important to remember, generally speaking, to some extent, it could be argued, while X has merits Y also offers, you're not broken, and for now that's enough
**Problem:** Safety tuning pushes models into a defensive crouch: hedge at the open, again mid-paragraph, again at the close, so no sentence can be wrong. §24 covers stacked qualifiers inside one sentence; this is the paragraph-level posture, and it comes with two companions. Sycophancy picks the rounder, more agreeable word and the therapeutic closing line. The no-screw-up tell is the absence of failure: nothing went wrong, nobody got fired, no release shipped broken. Take a position, keep the one hedge the evidence supports, and keep the mistake if it happened.
**Before:**
> It is important to remember that, generally speaking, while microservices have merits, monoliths also offer benefits, and it could be argued that the right choice depends to some extent on context.
**After:**
> Start with a monolith. We split ours at 40 engineers and lost two months to distributed tracing we did not need.

## Model fingerprints (dated 2026-09)

PERISHABLE. Each row is one model generation's habit, not a law, and the newest releases already break several of them. Treat a match as one weak signal among several. You cannot name the model that wrote a text from its prose.

| Model | Habits |
|---|---|
| Claude | load-bearing, substrate, honest take / honest assessment / honest caveat, synthesize, reconciling, fold, crux, invariant, gate, belt-and-suspenders, beat, register, wire / wiring. Straight quotes. Long, variable sentences; over-intensifies with *incredibly* and *wildly*. |
| GPT-4o / GPT-5 | Dense, enthusiastic, noun-heavy corporate register. Curly quotes and apostrophes. High em dash density (GPT-4.1 at 10.62 per 1,000 words, and it resists suppression prompts). Participial clauses and nominalisations well above baseline. tapestry, camaraderie, palpable, delve, meticulous, boast. |
| Gemini | Bullets and nested numbered lists by default, even where a paragraph fits. Introduction-body-summary in every section. Dry and clinical. Straight quotes. Latches onto a word from the prompt (say "analytical") and repeats it for the rest of the conversation. |
| Llama | Zero em dashes under any instruction, so an absence of dashes is not evidence of a human writer. Reserved, observational tone. Over-indexes on *unease*, *palpable*, *intricate*. |
| DeepSeek | Curly quotes. High dash use (6.95 per 1,000 words) and resistant to suppression, like the GPT-4.x line. |

## Check for false positives

### What not to flag

A person may use some of these patterns. Do not treat any item below as proof by itself:

- **Perfect grammar and consistent style.** Many writers are professionals or have been edited. Polish does not equal AI.
- **Mixed casual and formal styles.** This can reflect the writer's field, age, or personal habits.
- **"Bland" or "robotic" prose.** AI prose has *specific* tells. Generic dryness without those tells is just dry writing.
- **Formal or academic words.** §7 lists specific words that AI writing overuses. Do not simplify every formal word.
- **Letter-style opening or closing on a comment.** Salutations and sign-offs predate ChatGPT by centuries.
- **Common transition words in isolation.** *Additionally*, *moreover*, *consequently* are AI-coded only when piled up. One *however* is not a tell.
- **Curly quotes alone.** macOS, Word, Google Docs, and most CMSes auto-curl by default. Curly quotes only count when stacked with other tells.
- **Any single feature, and em dashes most of all.** Mark Twain runs 10.13 em dashes per 1,000 words in *Huckleberry Finn*, the same rate as GPT-4.1. Many editors and journalists use them just as freely. One mark, one word, or one structure is never proof. Em dashes count only when they arrive with formulaic sales-y rhythm and several other tells.
- **One short sentence for emphasis.** Flag dramatic fragments only when several appear in a row.
- **Deliberate repeated openings.** Writers may repeat an opening to build rhythm or pressure, as in "She came. She saw. She conquered." Change it only when the repetition adds nothing.
- **"Honestly" or "look" mid-sentence.** These are ordinary in casual writing. The tell is the standalone theatrical opener, not the word itself.
- **Useful limits and disclaimers.** Keep scope statements, legal and safety notices, real corrections, named objections, replies, and FAQ answers.
- **Real alternatives.** Keep options that a reader may consider in a design document, tutorial, or argument. Remove only an unlikely option that the text dismisses and never uses again.
- **Unsourced claims.** Most of the web is unsourced. Lack of citations doesn't prove anything.
- **Correct, complex formatting.** Visual editors and templates produce clean output without any AI.
- **Secondhand text.** Do not rewrite watched phrases inside quotations, titles, proper names, or examples where the phrase is being discussed rather than used.
- **Short texts.** A paragraph or two gives an unstable signal. Both statistical checks and word lists misfire badly under a few hundred words. Judge a short comment on its content, not its style.
- **Writing by non-native English speakers.** Liang et al. (Stanford) measured a 61% average false-positive rate when detectors were run on TOEFL essays. ESL writers are taught textbook transitions and formal hedges and are trained not to take grammatical risks, which is exactly the safe register these patterns describe. Never treat that register as evidence.
- **Formal academic and technical prose.** Standardized terminology, nominalisations, and tricolon structures are house style in those fields and were taught long before 2022. Flag the puffery in an abstract, not its vocabulary.

When unsure, look for several patterns together. One em dash proves nothing. Several stock patterns in the same passage are stronger evidence. Sourcing beats style: a text with named, dated, checkable citations for every major claim is showing expertise no matter how polished it reads.

### Do not over-correct

- **No mechanical synonym swaps.** Trading *delve* for *explore* or *moreover* for *besides* leaves the sentence rhythm untouched, and rhythm is what actually reads as machine-written. Rewrite the sentence or leave the word alone.
- **No over-fragmentation.** Chopping every sentence to force variety produces the staccato triplet ("No fluff. No filler. No noise."), which is its own marketing-brochure tell. §31 covers this; forcing burstiness recreates the problem you were fixing.
- **The pub test.** Read the rewrite out loud. If you would not say the sentence to a colleague, it is not more human than what it replaced, only stranger. Automated humanizer tools fail this constantly ("paramountly significant" for "important").

### Human details to keep

These details often carry the writer's voice. Keep them unless they hurt the meaning:

- **Specific, unusual details.** Keep a real address, an odd quote, or a phrase such as "the lawyer who used to work upstairs from my dentist."
- **Mixed feelings and unresolved tension.** Keep lines such as "I think this is mostly good, but it bothers me, and I can't fully explain why."
- **Dated, era-bound references.** Slang, memes, or in-jokes that map to a specific year and subculture. Models lag by a year or more.
- **Deliberate first-person choices.** Keep a cut or word choice when the writer can explain why it belongs.
- **Variety in sentence length.** Real writing alternates short and long. AI writing tends toward an even, mid-length cadence.
- **Genuine asides, parentheticals, or self-corrections.** "(I keep wanting to say 'almost' here, but it really was certain.)" Models rarely interrupt themselves like this.
- **Edits made before November 30, 2022.** ChatGPT's public launch. Anything older than that is, with very rare exceptions, not AI-written.

---

## How to return the result

**Pasted text (default).** Return the draft, a short list of remaining AI patterns, and the final rewrite.

**File mode.** When the user names a file, run the full rewrite process but write only the final text to the file. Change prose only. Keep code blocks, YAML metadata, data, and link targets unchanged. Then give the user a short summary.

**Embedded mode.** When another task uses this skill for a pull request, commit message, or document, return only the final text.

## Rewrite process

1. Read the source and mark each AI pattern.
2. Write a draft. Read it aloud. Check the rhythm, details, simple verbs such as *is* and *has*, and the right level of formality.
3. Ask two questions:
   - **"What still sounds AI-generated?"**
   - **"Did the rewrite add or remove any fact, name, number, date, quote, citation, ranking, or other claim?"**
   Treat any unsupported addition or lost claim as an error.
4. Write the final version. State each point naturally instead of patching one flagged phrase at a time. If a sentence stays awkward, rewrite the paragraph around its main point. Apply the dash rule in §14.

Return the result required by [How to return the result](#how-to-return-the-result).

## Tells decay

This list is dated 2026-09, and it will rot in a predictable direction.

- Vocabulary tells age fastest. *Delve* spiked 28-fold in 2024 PubMed abstracts, then became a meme; writers scrubbed it and labs tuned it out. A 2024 word list run against 2026 text mostly finds people avoiding the words.
- Punctuation profiles shift every model generation. GPT-4.1 ran 10.62 em dashes per 1,000 words; GPT-5.4 runs 1.43, close to the 3.23 human baseline. Llama has always been at zero. Any threshold you set today is wrong within a year.
- The published web lags the models. Pew's Common Crawl sample shows em dashes doubling and negative parallelism nearly tripling between 2023 and 2026, because the web holds the output of older models.
- Structural and rhetorical tells (§39 to §43) decay slowest. They come from how models are tuned to be helpful and safe, not from a word list, so they survive each round of scrubbing.

Re-run the underlying research about quarterly. When you do, re-date this section, the model fingerprint table, and the model split note in §19.

## Source

This skill is based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. Its patterns come from reviews of AI-generated text on Wikipedia.

Wikipedia's main point: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."

This skill is a derivative. Its base is `github:blader/humanizer@e2e92e7b4b82` (version 2.11.2), which supplies §1 to §35 and the original false-positive list.

Everything added on top (the writing-time section, the 60-second decision tree, §36 to §43, the model fingerprint table, the false-positive additions, and "Tells decay") comes from a 2026-09-03 NotebookLM research pass over 83 sources, held at `~/.claude/projects/system-improvement/outputs/notebooklm-research/2026-09-03-spot-ai-writing/`. The named studies behind the numbers: Kobak et al. (*Science Advances*, 2025), Reinhart et al. (*PNAS*, 2025), Freeburg (arXiv:2603.27006, 2026), Siler (*PNAS*, 2026), Liang et al. (Stanford), and Pew Research Center's Common Crawl analysis.

Long-form evidence, full tables, and per-claim citations: [references/research-2026-09.md](references/research-2026-09.md).
