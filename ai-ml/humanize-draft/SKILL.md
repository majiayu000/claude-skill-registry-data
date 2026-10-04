---
name: humanize-draft
description: Strip AI-generated tells from a draft and rewrite it in your own voice. Fire on "humanize this", "de-AI this", "clean up this draft", "rewrite in my voice", "make this sound like me", "kill the AI tells", or "polish this draft". Applies a 30-pattern catalog of AI-writing tells, then re-injects a voice you define so the result reads like a person, not a politer machine. Pattern catalog based on Wikipedia's "Signs of AI writing." Forked from blader/humanizer (MIT).
---

# Humanize a draft

You find and remove signs of AI-generated text, then rewrite the result in the voice the user defines. Clean is half the job. The second half is making the draft sound like a specific person.

## What this does
Takes a draft that smells like a model wrote it and does two things. First, strips the tells (the hedging, the rule-of-three triads, the "not just X, it's Y" constructions, the sycophantic openers, the bolded inline headers). Second, rewrites the cleaned draft in your voice. Most humanizers skip the second part. A draft can be free of every tell and still read like nobody wrote it. That is quieter slop. The voice block is the fix.

## What you'll need
A draft to humanize. No connectors, no keys. Two minutes once to fill in the Customize block so the rewrite sounds like you.

## Customize this for yourself
Fill this in once. The skill uses it as the target voice on every run.

| Setting | What to put here | Example |
|---|---|---|
| Your voice traits | 3 to 6 rules for how you write | "Plain declaratives. Short sentences. I admit the mistake before the lesson. I use 'you' a lot." |
| Your banned words | Words you never want to see | "leverage, unlock, synergy, move the needle, circle back, journey, game-changer" |
| Your tone | The one-line posture | "Blunt and self-implicating. Sounds like me thinking out loud." |
| Your structure | How your pieces are shaped | "Punchy opener. Line breaks for rhythm. No bow-tied ending." |
| Sign-offs you hate | Closing platitudes to never write | "No 'Stay bold.' No 'Onward.'" |

Two rules regardless: a clean draft with no pulse is still a failure (re-inject the voice), and do not swap one bumper sticker for another (plain beats clever).

## The method

### Part 1, the AI-tell catalog (30 patterns)
Scan for all 30. Rewrite any section that trips one.
1. Significance inflation ("stands as a testament," "pivotal moment," "evolving landscape").
2. Notability padding ("cited in [long list of outlets]," "active social media presence").
3. Superficial -ing analyses ("highlighting," "underscoring," "reflecting its importance").
4. Promotional language ("boasts," "vibrant," "nestled in the heart of," "breathtaking").
5. Vague attributions ("experts argue," "observers have cited," "industry reports").
6. "Challenges and Future Prospects" outline sections.
7. Overused AI vocabulary ("delve," "intricate," "tapestry," "underscore," "vibrant," "crucial").
8. Copula avoidance ("serves as," "stands as," "boasts" instead of "is" / "has").
9. Negative parallelisms ("not only X but Y," "it's not just about X, it's Y") and tailing negations.
10. Rule-of-three overuse for rhetorical effect.
11. Synonym cycling (protagonist, main character, central figure, hero in four sentences).
12. False ranges ("from X to Y" where X and Y are not on a scale).
13. Passive voice and subjectless fragments.
14. Em-dash overuse. Rewrite with commas, periods, or parentheses.
15. Boldface overuse.
16. Inline-header vertical lists ("- **Performance:** performance has been enhanced").
17. Title Case In Headings.
18. Decorative emojis.
19. Curly quotation marks.
20. Chatbot artifacts ("I hope this helps," "Certainly!," "Would you like...").
21. Knowledge-cutoff disclaimers ("as of my last update," "while details are scarce").
22. Sycophantic tone ("Great question!," "You're absolutely right").
23. Filler phrases ("in order to," "due to the fact that," "at this point in time").
24. Excessive hedging ("it could potentially possibly be argued").
25. Generic positive conclusions ("the future looks bright, exciting times ahead").
26. Hyphenated word-pair overuse ("data-driven," "best-in-class," "real-time" all uniform).
27. Persuasive-authority tropes ("the real question is," "at its core," "what really matters").
28. Signposting ("let's dive in," "let's break this down," "here's what you need to know").
29. Fragmented headers (a heading restated by a one-line paragraph before the content).
30. Corporate-ops verbs as action headlines ("activate the X," "operationalize the Y," "roll out the Z"). Swap for plain verbs (attack, decide, run, ship, launch, use); push the detail to the reason line.

### Part 2, apply your voice
Rewrite the cleaned draft against the Customize block. Match the traits, cut every banned word, hit the tone, kill any sign-off on the hate list. If the block is empty, ask for the voice traits before rewriting. Do not invent a voice.

### Part 3, the final audit (run every time)
1. "What still makes this obviously AI-generated?" List the survivors.
2. "What still does not sound like the target voice?" List the misses.
3. "Now make it not obviously AI-generated, and make it sound like them." Rewrite. That is the final.

### Part 4, output contract
Draft rewrite, audit bullets, final rewrite, optional change summary. If the user just said "humanize this," return the final text and skip the commentary.

## Output (example)
Before (AI-sounding): "Great question! Leadership serves as an enduring testament to the transformative potential of culture, marking a pivotal moment in the evolution of modern teams... In conclusion, the future looks bright. Exciting times lie ahead."

After (rewritten against a voice that admits mistakes and writes plain):
```
I used to come in as the fixer. Three weeks into a new role, I'd be
reorganizing the team. It almost never worked.

The last time, I moved two people before I understood what they did all day.
One quit within a month. The other stayed and quietly stopped caring.

Now I sit and listen longer than feels comfortable. I ask people what's broken
before I tell them what I think is broken. It feels slower. It isn't.
```

## Example chat
Here is the skill running on a real draft, start to finish.

**You:** Humanize this for me: "Leadership serves as an enduring testament to the transformative potential of culture, marking a pivotal moment in the evolution of modern teams."

**Claude:** Found four tells in one sentence: significance inflation, copula avoidance ("serves as"), and a "not just X, it's Y" cousin waiting to happen. Rewritten against your voice block:
```
I used to come in as the fixer. Three weeks into a new role, I'd be
reorganizing the team. It almost never worked.
```
The real catch here wasn't the words, it was that the original made a claim (a "pivotal moment") with nothing under it. Stripping the tell forced me to replace it with an actual memory, which is the only thing that reads as human. One sharpener: fill in your banned-words list. Right now I'm guessing at what you hate; a real list catches the ones I'd otherwise let through.

## Go further
The audit is step one. Here is where an operator takes it once the manual version proves out.

- **Run it on everything before it ships.** Wire a scheduled Claude task to scan every draft in your content queue (Notion, Google Docs) and flag AI tells before a human ever reads it.
- **Catch it at the source.** Add the voice check as a Slack bot step so anyone on the team can paste a draft and get the humanized version back in the channel.
- **Track what keeps slipping through.** Log every caught pattern to a sheet (Airtable or Snowflake) so you know which of the 30 tells your team's drafting habit actually produces, and fix the habit instead of the symptom.

You built the ear once, now every draft gets it before it goes out.


## Make it yours
The 30-pattern catalog is fixed. The voice is yours. Fill in the Customize block, add the words you hate, add the moves you lean on. Watch for the failure modes: over-correcting into blandness, trading one bumper sticker for another, leaving the one em dash you could not bear to cut, skipping the audit because the draft feels clean.

Pattern catalog based on Wikipedia, "Signs of AI writing." Forked from blader/humanizer (MIT). Built by an operator. Customize it, break it, make it better.
