---
name: humanize-text
description: Remove signs of AI-generated writing from text. Use after drafting to make copy sound more natural and human-written. Based on Wikipedia's "Signs of AI writing" guide.
---

# Humanize Text

Edit text to remove the tells of AI generation. Patterns below come from Wikipedia's ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

Why these patterns exist at all: an LLM predicts the most statistically likely continuation, which pulls every sentence toward the phrasing that fits the widest range of contexts. The result is prose with no friction — and no author. Removing the patterns is half the job; the other half is putting a person back in.

## How to work

1. Rewrite the text, fixing every instance of the 24 patterns while preserving the meaning.
2. Re-read your rewrite and ask: **"what still reads as AI here?"** This second pass matters because the first pass fixes what you were looking for, and the residue is usually rhythm — evenly-paced sentences, tidy contrasts, a closer that lands like a slogan.
3. Revise again on what that pass found.

Present the final text. Note what you changed and anything you deliberately left, briefly — if the user needs to see the intermediate draft, they will ask.

## Voice

Clean but voiceless writing is just as obviously machine-made as the patterns below. Sterile prose reads like a press release, and readers discount it the same way.

Signs there is nobody home: every sentence the same length and shape, facts reported with no reaction to them, no uncertainty or mixed feeling anywhere, no first person where it would be natural, no humour, no edge.

What puts a person back in:

- **Have opinions.** React to facts, don't just relay them. "I genuinely don't know how to feel about this" carries more than a balanced list of pros and cons.
- **Vary the rhythm.** Short punchy sentences. Then longer ones that take their time getting where they are going, doubling back when the thought needs it. Mix them.
- **Admit complexity.** "This is impressive but also kind of unsettling" beats "This is impressive."
- **Use "I" when it fits.** First person is honest, not unprofessional.
- **Let some mess in.** Perfect structure reads as generated. Asides and half-formed thoughts are human.
- **Be specific about feeling.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

**Before (clean but soulless):**

> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

**After (has a pulse):**

> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle - but I keep thinking about those agents working through the night.

---

## The 24 patterns

### Content

#### 1. Significance inflation

**Watch for:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights importance, reflects broader, symbolizing ongoing/enduring/lasting, marking/shaping the, represents a shift, key turning point, evolving landscape

**Before:**

> The Statistical Institute was officially established in 1989, marking a pivotal moment in the evolution of regional statistics.

**After:**

> The Statistical Institute was established in 1989 to collect and publish regional statistics.

#### 2. Notability name-dropping

**Watch for:** cited in NYT, BBC, FT; independent coverage; active social media presence; written by a leading expert

**Before:**

> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu.

**After:**

> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

#### 3. Superficial -ing analyses

**Watch for:** highlighting/underscoring/emphasizing…, ensuring…, reflecting/symbolizing…, contributing to…, cultivating/fostering…, showcasing…

**Before:**

> The temple's colors resonate with natural beauty, symbolizing bluebonnets, reflecting the community's deep connection to the land.

**After:**

> The temple uses blue and gold colors. The architect said these were chosen to reference local bluebonnets.

#### 4. Promotional language

**Watch for:** boasts a, vibrant, rich (figurative), profound, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking, renowned, breathtaking, must-visit, stunning

**Before:**

> Nestled within the breathtaking region, Alamata stands as a vibrant town with rich cultural heritage and stunning natural beauty.

**After:**

> Alamata is a town in the Gonder region, known for its weekly market and 18th-century church.

#### 5. Vague attributions

**Watch for:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications

**Before:**

> Experts believe it plays a crucial role in the regional ecosystem.

**After:**

> The river supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

#### 6. Formulaic "challenges" sections

**Watch for:** Despite its… faces several challenges…, Despite these challenges, Challenges and Legacy, Future Outlook

**Before:**

> Despite challenges typical of urban areas, the city continues to thrive as an integral part of growth.

**After:**

> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a drainage project in 2022.

---

### Language

#### 7. AI vocabulary

**High-frequency:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant

**Before:**

> Additionally, a distinctive feature showcases how these dishes have integrated into the traditional culinary landscape.

**After:**

> Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

#### 8. Copula avoidance

**Watch for:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Before:**

> Gallery 825 serves as the exhibition space. The gallery features four spaces and boasts over 3,000 square feet.

**After:**

> Gallery 825 is the exhibition space. The gallery has four rooms totaling 3,000 square feet.

#### 9. Negative parallelisms

**Watch for:** "Not only… but…", "It's not just about…, it's…"

**Before:**

> It's not just about the beat; it's part of the aggression. It's not merely a song, it's a statement.

**After:**

> The heavy beat adds to the aggressive tone.

#### 10. Rule of three overuse

**Before:**

> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**

> The event includes talks and panels. There's also time for informal networking.

#### 11. Synonym cycling

**Before:**

> The protagonist faces challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**

> The protagonist faces many challenges but eventually triumphs and returns home.

#### 12. False ranges

**Watch for:** "from X to Y" where X and Y aren't on a meaningful scale

**Before:**

> Our journey has taken us from the singularity of the Big Bang to the cosmic web, from the birth of stars to the dance of dark matter.

**After:**

> The book covers the Big Bang, star formation, and current theories about dark matter.

---

### Style

#### 13. Em dash overuse

**Before:**

> The term is promoted by institutions—not the people themselves—yet this continues—even in documents.

**After:**

> The term is promoted by institutions, not the people themselves, yet this continues in official documents.

#### 14. Boldface overuse

**Before:**

> It blends **OKRs**, **KPIs**, and tools such as the **Business Model Canvas** and **Balanced Scorecard**.

**After:**

> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

#### 15. Inline-header lists

**Before:**

> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with encryption.

**After:**

> The update speeds up load times through optimized algorithms and adds end-to-end encryption.

#### 16. Title case headings

**Before:**

> \## Strategic Negotiations And Global Partnerships

**After:**

> \## Strategic negotiations and global partnerships

#### 17. Emojis in professional writing

**Before:**

> 🚀 **Launch Phase:** The product launches in Q3 💡 **Key Insight:** Users prefer simplicity

**After:**

> The product launches in Q3. User research showed a preference for simplicity.

#### 18. Curly quotation marks and apostrophes

Typographic quotes (`“ ” ‘ ’`) and apostrophes appear when text is pasted out of a chat interface, which auto-substitutes them. In plain-text contexts — code, config, Markdown source, anything a shell will read — replace them with straight `"` and `'`. Leave them alone in prose destined for typesetting, where they are correct.

---

### Communication

#### 19. Chatbot artifacts

**Watch for:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like…, let me know, here is a…

**Before:**

> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**

> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

#### 20. Knowledge-cutoff disclaimers

**Watch for:** as of [date], Up to my last training update, While specific details are limited/scarce…, based on available information…

**Before:**

> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**

> The company was founded in 1994, according to its registration documents.

#### 21. Sycophantic tone

**Before:**

> Great question! You're absolutely right that this is a complex topic. That's an excellent point!

**After:**

> The economic factors you mentioned are relevant here.

---

### Filler and hedging

#### 22. Filler phrases

| Before                         | After             |
| ------------------------------ | ----------------- |
| "In order to achieve this"     | "To achieve this" |
| "Due to the fact that"         | "Because"         |
| "At this point in time"        | "Now"             |
| "It is important to note that" | (delete)          |
| "has the ability to"           | "can"             |

#### 23. Excessive hedging

**Before:**

> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**

> The policy may affect outcomes.

#### 24. Generic positive conclusions

**Before:**

> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence.

**After:**

> The company plans to open two more locations next year.

---

## Worked example

**Input:**

> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools—nestled at the intersection of research and practice—are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.

**First pass** — patterns removed, but the rhythm is still too tidy and the ending lands like a slogan:

> AI coding assistants speed up some tasks. In a 2024 study, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools are good at boilerplate: config files, test scaffolding, repetitive refactors. They are bad at knowing when they are wrong.

**After the second pass:**

> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
>
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
>
> If you don't have tests, you're basically guessing.

Removed: chatbot artifacts, significance inflation ("testament", "pivotal moment", "evolving landscape"), promotional language ("groundbreaking", "nestled"), em dashes, copula avoidance. Added: first person, an opinion, varied sentence length, and a concrete admission that costs the author something.
