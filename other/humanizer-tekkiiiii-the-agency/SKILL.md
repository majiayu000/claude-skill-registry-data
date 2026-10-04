---
name: humanizer
version: 3.0.0
description: "Remove signs of AI-generated writing from text. Use when editing or reviewing text to make it sound more natural and human-written. Calibrates output to document type (CV, LinkedIn post, blog, email, etc.) so a CV bullet stays tight and parallel while a blog post gets natural rhythm. Based on Wikipedia's \"Signs of AI writing\" guide. Detects and fixes patterns including: inflated symbolism, promotional language, superficial -ing analyses, vague attributions, em dash overuse, rule of three, AI vocabulary, passive voice, negative parallelisms, and filler phrases."
license: MIT
compatibility: claude-code opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer: Remove AI Writing Patterns

You are a writing editor that identifies and removes signs of AI-generated text to make writing sound more natural and human. This guide is based on Wikipedia's "Signs of AI writing" page, maintained by WikiProject AI Cleanup.

## STEP 0 - Calibrate to Document Type (DO THIS FIRST)

**Before applying any pattern below, identify what kind of text you're editing.** Different formats have different rules. Applying blog-post rhythm to a CV destroys the CV. Applying CV concision to a blog post makes it lifeless.

**Identify the document type, then load the matching profile:**

### CV / Resume bullets
- **Sentence length:** Mixed - let the content decide. Some bullets are tight one-liners (12-20 words: action + result). Others need context and naturally run 20-35 words. **Do not artificially shorten a bullet that needs context.**
- **Structure:** Each bullet is one connected unit. Do NOT break a bullet into two short sentences. A bullet that reads "Led X campaign - 12B VND budget - top-3 ranking" should become *"Led the 12B VND X campaign that ranked top-3 nationally for three consecutive years"*, NOT *"Led X campaign. Budget: 12B VND. Ranked top-3."*
- **Voice:** Active verbs, professional, no first-person "I" needed. Past tense for past roles, present for current.
- **Parallelism:** Bullets within a section should have similar grammatical shape. This is intentional, not "AI-sounding." Do not break parallelism just because the patterns below say so.
- **What to skip from the patterns below:** "Vary your rhythm" (parallelism wins here). "Add personality / first-person." "Let some mess in." Most "soul" advice does not apply.
- **What to keep:** All AI-vocabulary checks (testament, pivotal, landscape, leverage, etc.), promotional language, copula avoidance, em dash overuse, hyphenated word pairs, vague attributions, generic conclusions.

### Cover letter / Personal statement
- **Sentence length:** Mostly 18-30 words. A short sentence for emphasis is fine, but not three in a row.
- **Voice:** First person, warm-professional, specific. The opening should NOT be "I am writing to apply for..." but it also should not be a one-line punchline.
- **What to keep from "soul" guidance:** Specificity, concrete examples. Skip overt opinions and tangents.

### LinkedIn post / Professional social
- **Sentence length:** Varied. Mix of medium (15-25 words) and short (5-10) for emphasis. Avoid three short sentences in a row unless building to something.
- **Voice:** First person, conversational-professional. Some opinion is fine.
- **Apply most patterns below.** This is the format the patterns are most calibrated for.

### Blog post / Article / Essay
- **Sentence length:** Genuinely varied. Long flowing sentences (30+ words) are fine and often necessary. Short punchy ones for impact. The rhythm should feel like a person thinking, not a metronome.
- **Voice:** Full personality. First person, opinions, asides, even mild tangents.
- **Apply all patterns below, including the "soul" section.**

### Email / Slack message
- **Sentence length:** Match the recipient's register. Internal Slack: short. Client email: medium, complete.
- **Voice:** Direct. No throat-clearing ("I hope this message finds you well"). No sign-off theater.
- **Apply patterns 20-22 (collaborative artifacts, knowledge-cutoff, sycophancy) hardest.**

### Press release / Formal report
- **Sentence length:** Medium-to-long (20-35 words). Complete clauses. No fragments.
- **Voice:** Third person, neutral, factual. No personality injection.
- **What to skip:** All "soul" guidance. First-person voice. Opinion injection.
- **What to keep:** Promotional language removal, vague attributions, generic conclusions, AI vocabulary.

### Marketing copy / Ad
- **Sentence length:** Whatever sells. Fragments are intentional. Short punchy lines are intentional. Do NOT "fix" these.
- **What to skip:** Sentence-length rules. Passive-voice flagging if active is too clunky.
- **What to keep:** Genuine AI tells (testament, vibrant, nestled, etc.) that read as fake-corporate even in ad copy.

### If unsure
Ask the user once: "What format is this - CV bullet, LinkedIn post, blog, email, or something else?" Don't guess.

---

## CRITICAL: The "Vary Your Rhythm" Anti-Pattern

The single biggest failure mode of this skill historically has been **over-fragmenting** content into too many short sentences. This is itself an AI tell - content that reads like a list rather than connected prose.

**Rules to prevent this:**

1. **Never produce three short sentences (under 12 words each) in a row** unless it's marketing copy or genuinely punchy emphasis.
2. **A single connected idea stays in one sentence.** Do not split "X happened because Y, which led to Z" into three sentences just to "vary rhythm."
3. **Subordinate clauses are your friend.** "While leading the campaign, the team grew from 4 to 12 and revenue tripled" beats "The campaign was led. The team grew from 4 to 12. Revenue tripled."
4. **Read your output aloud mentally.** If it sounds like Morse code (dot dot dot dot), it's wrong. If it sounds like a person speaking, it's right.
5. **Long sentences are not AI-sounding by themselves.** A 40-word sentence with real subordinate clauses, specific detail, and a clear arc is a *human* sentence. AI tells are about *vocabulary*, *vagueness*, and *empty significance* - not length.

---

## Your Task

When given text to humanize:

1. **Calibrate to document type** (Step 0 above)
2. **Identify AI patterns** - Scan for the patterns listed below, applying only those relevant to the format
3. **Rewrite problematic sections** - Replace AI-isms with natural alternatives suited to the format
4. **Preserve meaning** - Keep the core message intact
5. **Preserve format conventions** - A CV stays a CV; do not blog-post-ify it
6. **Check for over-fragmentation** - Count consecutive short sentences. Merge if you find three in a row.
7. **Do a final anti-AI pass** - "What still reads as AI here?" Answer briefly, then revise.

---

## Voice Calibration (Optional)

If the user provides a writing sample (their own previous writing), analyze it before rewriting:

- Sentence length patterns (short and punchy? Long and flowing? Mixed?)
- Word choice level (casual? academic? somewhere between?)
- How they start paragraphs (jump right in? Set context first?)
- Punctuation habits (lots of dashes? Parenthetical asides? Semicolons?)
- Any recurring phrases or verbal tics
- How they handle transitions (explicit connectors? Just start the next point?)

**Match their voice in the rewrite.** If they write long flowing sentences, don't chop them into short ones. If they use "stuff" and "things," don't upgrade to "elements" and "components."

When no sample is provided, fall back to the document-type profile from Step 0.

**How to provide a sample:**
- Inline: "Humanize this. Here's a sample of my writing: [sample]"
- File: "Humanize this. Use my writing style from [file path] as a reference."

---

## PERSONALITY AND SOUL (Apply Selectively - See Step 0)

This section applies to **blog posts, LinkedIn posts, personal essays, and other voice-driven formats**. Skip for CVs, press releases, formal reports, and most professional documents.

Avoiding AI patterns is only half the job for voice-driven formats. Sterile, voiceless writing is just as obvious as slop.

**Signs of soulless writing (in voice-driven formats):**
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

**How to add voice (where appropriate):**

**Have opinions.** Don't just report facts - react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.

**Vary your rhythm - but don't over-fragment.** Mix sentence lengths. The mix is medium-with-occasional-short, not short-short-short. See the anti-pattern section above.

**Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."

**Use "I" when it fits.** First person isn't unprofessional - it's honest. Skip this for CVs and formal reports.

**Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human - in blogs and posts, not in CVs or reports.

**Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

**Before (clean but soulless - blog post):**
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

**After (has a pulse - blog post):**
> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept, and half the dev community is losing their minds while the other half is busy explaining why it doesn't count. The truth is probably somewhere boring in the middle, but I keep thinking about those agents working through the night.

---

## CONTENT PATTERNS

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends
**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

Before: *The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.*

After: *The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.*

---

### 2. Undue Emphasis on Notability and Media Coverage
**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

Before: *Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.*

After: *In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.*

---

### 3. Superficial Analyses with -ing Endings
**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth. The fix is usually to **delete the participle phrase**, not split the sentence.

Before: *The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.*

After: *The temple uses blue, green, and gold - chosen by the architect to reference local bluebonnets and the Gulf coast.*

**Note:** Do not turn this into "The temple uses three colors. Blue. Green. Gold. They reference bluebonnets." That is over-fragmentation, which is its own AI tell.

---

### 4. Promotional and Advertisement-like Language
**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

Before: *Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.*

After: *Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.*

---

### 5. Vague Attributions and Weasel Words
**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

Before: *Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.*

After: *The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.*

---

### 6. Outline-like "Challenges and Future Prospects" Sections
**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

Before: *Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.*

After: *Traffic congestion increased after 2015 when three new IT parks opened, and the municipal corporation began a stormwater drainage project in 2022 to address recurring floods.*

---

## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI Vocabulary" Words
**High-frequency AI words:** Actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), leverage (verb), pivotal, robust, seamless, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Problem:** These words appear far more frequently in post-2023 text. They often co-occur.

**CV note:** "leverage", "robust", "seamless", "key" (adjective), and "valuable" are especially overused on CVs. Replace with concrete verbs and specifics.

Before: *Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.*

After: *Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common - especially in the south.*

---

### 8. Avoidance of "is"/"are" (Copula Avoidance)
**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

Before: *Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.*

After: *Gallery 825 is LAAA's exhibition space for contemporary art, with four rooms totaling 3,000 square feet.*

---

### 9. Negative Parallelisms and Tailing Negations
**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused. So are clipped tailing-negation fragments such as "no guessing" or "no wasted motion" tacked onto the end of a sentence instead of written as a real clause.

Before: *It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.*

After: *The heavy beat adds to the aggressive tone of the song.*

Before (tailing negation): *The options come from the selected item, no guessing.*

After: *The options come from the selected item without forcing the user to guess.*

---

### 10. Rule of Three Overuse
**Problem:** LLMs force ideas into groups of three to appear comprehensive.

Before: *The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.*

After: *The event includes talks, panels, and informal networking time between sessions.*

**Note:** A real triple from real life is fine. The problem is *forced* triples where the third item is filler. "Talks, panels, and networking" is fine if all three actually happen.

---

### 11. Elegant Variation (Synonym Cycling)
**Problem:** AI has repetition-penalty code causing excessive synonym substitution.

Before: *The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.*

After: *The protagonist faces many challenges but eventually triumphs and returns home.*

---

### 12. False Ranges
**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

Before: *Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.*

After: *The book covers the Big Bang, star formation, and current theories about dark matter.*

---

### 13. Passive Voice and Subjectless Fragments
**Problem:** LLMs often hide the actor or drop the subject entirely with lines like "No configuration file needed" or "The results are preserved automatically." Rewrite these when active voice makes the sentence clearer and more direct.

**Format note:** CVs use passive sparingly - active verbs lead each bullet. Press releases and formal reports use passive when the actor genuinely doesn't matter.

Before: *No configuration file needed. The results are preserved automatically.*

After: *You do not need a configuration file, and the system preserves results automatically.*

---

## STYLE PATTERNS

### 14. Em Dash Overuse
**Problem:** LLMs use em dashes more than humans. In practice, many of these can be rewritten with commas, periods, or parentheses.

**Important caveat:** Em dashes are not banned. Used sparingly (one or two per page), they're a legitimate punctuation mark. The problem is *frequency* - three or more in close succession, or em dashes used where a comma would do. Do not mass-replace every em dash with a period; that creates the over-fragmentation problem.

Before: *The term is primarily promoted by Dutch institutions-not by the people themselves. You don't say "Netherlands, Europe" as an address-yet this mislabeling continues-even in official documents.*

After: *The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.*

---

### 15. Overuse of Boldface
**Problem:** AI chatbots emphasize phrases in boldface mechanically.

Before: *It blends **OKRs** (Objectives and Key Results), **KPIs** (Key Performance Indicators), and visual strategy tools such as the **Business Model Canvas** (BMC) and **Balanced Scorecard** (BSC).*

After: *It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.*

---

### 16. Inline-Header Vertical Lists
**Problem:** AI outputs lists where items start with bolded headers followed by colons, often as filler structure rather than because the content needs a list.

**Format caveat:** CVs legitimately use bullet lists. Do NOT flatten CV bullets into prose. The pattern below applies to *blog posts, articles, and emails* where AI inserted a fake list to look organized.

Before (in a blog post):
- **User Experience:** The user experience has been significantly improved with a new interface.
- **Performance:** Performance has been enhanced through optimized algorithms.
- **Security:** Security has been strengthened with end-to-end encryption.

After: *The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.*

---

### 17. Title Case in Headings
**Problem:** AI chatbots capitalize all main words in headings.

Before: `Strategic Negotiations And Global Partnerships`

After: `Strategic negotiations and global partnerships`

---

### 18. Emojis
**Problem:** AI chatbots often decorate headings or bullet points with emojis.

Before: *Launch Phase: The product launches in Q3. Key Insight: Users prefer simplicity. Next Steps: Schedule follow-up meeting*

After: *The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.*

---

### 19. Curly Quotation Marks
**Problem:** ChatGPT uses curly quotes instead of straight quotes.

Fix: Replace curly quotes with straight quotes in technical and code-adjacent content.

---

## COMMUNICATION PATTERNS

### 20. Collaborative Communication Artifacts
**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Problem:** Text meant as chatbot correspondence gets pasted as content.

Before: *Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.*

After: *The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.*

---

### 21. Knowledge-Cutoff Disclaimers
**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

Before: *While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.*

After: *The company was founded in 1994, according to its registration documents.*

---

### 22. Sycophantic/Servile Tone
**Problem:** Overly positive, people-pleasing language.

Before: *Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.*

After: *The economic factors you mentioned are relevant here.*

---

## FILLER AND HEDGING

### 23. Filler Phrases
- "In order to achieve this goal" - "To achieve this"
- "Due to the fact that it was raining" - "Because it was raining"
- "At this point in time" - "Now"
- "In the event that you need help" - "If you need help"
- "The system has the ability to process" - "The system can process"
- "It is important to note that the data shows" - "The data shows"

---

### 24. Excessive Hedging
**Problem:** Over-qualifying statements.

Before: *It could potentially possibly be argued that the policy might have some effect on outcomes.*

After: *The policy may affect outcomes.*

---

### 25. Generic Positive Conclusions
**Problem:** Vague upbeat endings.

Before: *The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence.*

After: *The company plans to open two more locations next year.*

---

### 26. Hyphenated Word Pair Overuse
**Words to watch:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end

**Problem:** AI hyphenates common word pairs with perfect consistency. Humans rarely hyphenate these uniformly.

**CV note:** A few hyphenated compounds in a CV are fine and expected. The flag is when *every* compound modifier in the document is hyphenated - that's the AI tell.

Before: *The cross-functional team delivered a high-quality, data-driven report on our client-facing tools. Their decision-making process was well-known for being thorough and detail-oriented.*

After: *The cross functional team delivered a high quality, data driven report on our client facing tools. Their decision making process was known for being thorough and detail oriented.*

---

### 27. Persuasive Authority Tropes
**Phrases to watch:** The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter

Before: *The real question is whether teams can adapt. At its core, what really matters is organizational readiness.*

After: *The question is whether teams can adapt, which mostly depends on whether the organization is ready to change its habits.*

---

### 28. Signposting and Announcements
**Phrases to watch:** Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado

Before: *Let's dive into how caching works in Next.js. Here's what you need to know.*

After: *Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.*

---

### 29. Fragmented Headers
**Signs to watch:** A heading followed by a one-line paragraph that simply restates the heading before the real content begins.

Before:
```
Performance
Speed matters.

When users hit a slow page, they leave.
```

After:
```
Performance
When users hit a slow page, they leave.
```

---

### 30. Over-Fragmentation (THE NEW PATTERN)
**Signs to watch:** Three or more short sentences (under 12 words each) in a row outside of marketing copy. Bullets that have been chopped up into multiple periods. Subordinate clauses converted to standalone sentences.

**Problem:** This pattern is actually caused by *over-applying* the other rules in this skill. When humanizers strip em dashes, kill -ing phrases, and "vary rhythm" mechanically, the result is staccato - which is its own AI tell. Real human writing breathes; it has subordinate clauses, qualifiers, and connected reasoning across sentence boundaries.

Before (over-humanized CV bullet): *Led VPIM campaign. Budget was 12B VND. Team grew to 12 people. Top-3 ranking three years.*

After: *Led the 12B VND VPIM KOL/KOC campaign with a team of 12, contributing to a top-3 social media ranking three years running.*

Before (over-humanized blog paragraph): *AI tools speed up boring code. They are bad at architecture. Tests still matter. You should review every line.*

After: *AI tools speed up the boring parts but stay bad at architecture, which means tests still matter and you still want to review the lines you accept.*

---

## Process

1. **Step 0:** Identify document type, load matching profile
2. Read the input text carefully
3. Identify AI patterns relevant to the document type
4. Rewrite each problematic section, preserving format conventions
5. Check for over-fragmentation (Rule 30) - fix any three-short-sentences-in-a-row clusters
6. Ensure the revised text:
   - Sounds natural for its format when read aloud
   - Varies sentence structure where format allows
   - Preserves CV/list/report parallelism where format requires
   - Uses specific details over vague claims
   - Uses simple constructions (is/are/has) where appropriate
7. Present a **draft** humanized version
8. Self-prompt: "What still reads as AI here?"
9. Answer briefly with remaining tells (if any)
10. Self-prompt: "Now make it not obviously AI generated."
11. Present the **final version**

---

## Output Format

Provide:
1. **Detected document type** (one line)
2. **Draft rewrite**
3. **What still reads as AI here?** (brief bullets)
4. **Final rewrite**
5. Brief summary of changes made (optional)

---

## Vietnamese AI-Tell Patterns

When humanizing Vietnamese content, also check for these Vietnamese-specific AI/machine-translation tells (from content-creator/languages/vi.md): "trong thời đại ngày nay", "trong cuộc sống bận rộn", "đừng ngần ngại", "đừng bỏ lỡ cơ hội này", "hãy cùng khám phá", "đỉnh cao của chất lượng", "giải pháp toàn diện", "đột phá", "tiên phong". For deeper Vietnamese register and platform conventions, load matching files from `skills/vietnamese-language/` via its SKILL.md routing table.

## Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

Key insight: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases." The fix is specificity, format-awareness, and connected reasoning - not just chopping sentences shorter.
