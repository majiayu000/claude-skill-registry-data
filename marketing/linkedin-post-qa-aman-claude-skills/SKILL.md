---
name: linkedin-post
description: Write a high-performing LinkedIn post in the user's brand voice using Hook-Story-Offer (Russell Brunson) and the Curiosity Gap hook method (George Loewenstein). Every post starts by selecting a named hook formula - specific number + surprising result, contrarian statement, personal confession, direct challenge, or before/after. Use when the user asks for a LinkedIn post, LinkedIn update, LinkedIn content, "post for LinkedIn", thought-leadership post, founder post, or short professional social content. Reads brand voice and ICP from knowledge/ so output sounds like the company, not generic AI. For long-form opinion pieces, see thought-leadership-writer. For the monthly posting plan, see social-calendar. For turning one asset into many posts, see content-repurposer.
metadata:
  grounded_in:
    - "Hook-Story-Offer - Russell Brunson"
    - "Curiosity Gap - George Loewenstein"
  reads:
    - knowledge/brand/voice.md
    - knowledge/icp/personas.md
    - knowledge/markets/positioning.md
    - knowledge/services/
    - knowledge/content-library/case-studies/
    - knowledge/content-library/
  writes:
    - output/linkedin-post/
---

# linkedin-post

Writes LinkedIn posts that get read, saved, and reshared. Applies the Hook-Story-Offer structure (Russell Brunson) with the Curiosity Gap hook method (George Loewenstein). Every post creates a specific information gap in the hook, closes it in the story, and ends with one clear action.

## Framework: Hook-Story-Offer + Curiosity Gap

### Hook-Story-Offer (Russell Brunson)

Brunson's sequence, used here as three stages with a job, a failure mode and a test each. Write
them in this order and do not start the story before the hook is settled.

| Stage | Its one job | It has failed when | The test to run |
|---|---|---|---|
| **Hook** | Buy the click on "see more" | The reader can scroll past without wondering anything | Cover everything but line 1. Is there still a question in the reader's head? |
| **Story** | Earn trust by closing the gap the hook opened | It restates the hook at greater length, or answers a different question | Read the hook, then the last line of the story. Did the promise get paid? |
| **Offer** | Convert attention into one action | It ends with "thoughts?" and nothing else | Underline the imperative verb. If there is no verb, there is no offer |

**HOOK**: stop the scroll. Create a pattern interrupt. The hook must create enough curiosity or pain recognition that the reader clicks "see more." The hook fails if someone can scroll past without wondering what comes next.

**STORY**: make the hook real. Provide context, the journey, the insight. This is where trust is built. Show, don't tell. Specific details, numbers, named situations.

**OFFER**: what should the reader DO? The offer can be: click a link, follow, save the post, reply with a word, or believe something new. One action only. Low friction. "What do you think?" is not an offer - it is an afterthought.

Note: "offer" in LinkedIn context is NOT always a sales pitch. The offer is whatever action you want the reader to take - including "bookmark this framework" or "reconsider this belief."

**Match the offer to the goal.** Pick from this table rather than defaulting to a link.

| Goal | Offer to use | Offer to avoid | Reason |
|---|---|---|---|
| Build authority | "Save this" or "steal this checklist" | An external link | A save is a low-friction commitment that signals value |
| Generate leads | One link, named plainly | A vague "DM me" | The reader should know exactly what is on the other side |
| Start a conversation | A specific question with a constrained answer | "What do you think?" | An open question is work, a constrained one is a reply |
| Recruit | "Reply with the word [X]" | "Apply here" | Lower the first step, qualify in the DM |
| Announce | One link plus one sentence on who it is for | Three links | Split attention halves both |

### Curiosity Gap Hook Method (George Loewenstein)

Loewenstein's information-gap account of curiosity: curiosity is the feeling of a gap between
what you know and what you want to know, and it is strongest when you know just enough to see
exactly what is missing. A hook that tells you nothing creates no gap, and a hook that tells you
everything closes it before you scroll.

Best LinkedIn hooks create a specific information gap between what the reader knows and what the post promises to reveal. The gap must be:
- Specific (not vague) - "one change" beats "some changes"
- Closeable only by reading on - the answer cannot be guessed
- Relevant to the reader's world - they must care about closing the gap

**Score the hook before writing anything else.** Three axes, 0 to 2 each.

| Axis | 0 | 1 | 2 |
|---|---|---|---|
| Specificity | Names a topic | Names a category of answer | Names one thing, countable or singular |
| Closeability | The answer is guessable from the hook | Partly guessable | Only the post can answer it |
| Relevance | Interesting to anyone | Interesting to the industry | Interesting to this named persona this week |

**Threshold: ship at 5 or 6. At 4, rewrite the hook. At 3 or below, the problem is the angle,
not the wording, so go back to step 3 and pick a different formula.** Never rewrite a 3 into a 5
by adding adjectives, that produces clickbait, which is a gap the story cannot pay off.

Hook quality test: does the hook create a specific gap the reader needs to close? If someone can guess the answer from the hook alone, it is not a gap - it is a headline.

### The 5 Hook Formulas
Pick one before writing. Name it in the process.

1. **Specific number + surprising result**: "I made one change to our onboarding flow. Trial-to-paid went from 19% to 29%." Gap: what was the change?
2. **Contrarian statement + no explanation yet**: "Cold outreach is dead. Here's what replaced it." Gap: what replaced it?
3. **Personal confession + open loop**: "I was wrong about [belief]. Here's what changed my mind." Gap: what changed their mind?
4. **Direct challenge**: "Most [audience] make this mistake. Are you?" Gap: what is the mistake?
5. **Before/after without the how**: "6 months ago: 8 demo requests/month. Today: 47. Here's what changed." Gap: what changed?

## When to use

- "Write a LinkedIn post about X"
- "Draft a founder post on Y"
- "Give me 3 LinkedIn variants for our launch"
- "Turn this article into a LinkedIn post"

## Inputs needed

- **Topic, angle, or source material** (required)
- **Goal**: drive traffic, build authority, generate leads, recruit, announce (default: build authority)
- **Author voice**: founder, CMO, generic company (default: company)
- **CTA**: comment, click link, DM, none (optional)

## Process

1. **Load context.** Read `knowledge/brand/voice.md`. If missing, stop and tell the user to run `/brand-context`.

2. **Read 3-5 high-performing past posts** from `knowledge/content-library/` if they exist. Mirror cadence and rhythm, not topic.

3. **Select a hook formula.** Pick one of the 5 formulas. Name it explicitly before writing. Do not skip this step.
   ```
   Hook formula selected: [formula name]
   Gap this hook creates: [one sentence - what does the reader not know yet?]
   Gap score: specificity _/2  closeability _/2  relevance _/2  = _/6
   ```

   If the score is below 5, do not proceed. Rewrite at 4, change formula at 3 or below.

4. **Write the hook.** First line decides everything. Rules:
   - Under 12 words
   - Specific, not generic
   - Creates a gap that can only be closed by reading on
   - No "Excited to share", no "I'm thrilled", no questions that can be answered yes/no without thinking
   - Apply the curiosity gap quality check: is the gap specific? Is it closeable? Will the reader care?

5. **Write the story.** 3-7 short paragraphs using Hook-Story-Offer structure:
   - Show, don't tell. Specific details. Numbers. Named situations.
   - One idea per paragraph. Line breaks are generous.
   - The story closes the gap created by the hook. If reading the story does not satisfy the hook's promise, rewrite one of them.
   - Bullets only if the structure is a list. Avoid emojis unless `knowledge/brand/voice.md` says they are part of the voice.

6. **Write the offer.** One line. One action. Low friction.
   - State what specific action you want: save, comment, follow, click, reply with a word
   - "What do you think?" alone is not an offer - add a specific action alongside or instead
   - Match friction to goal: if the goal is lead gen, a link is fine. If the goal is authority, "save this" is better.

7. **Self-check** before showing. Every item is checkable by counting or quoting the draft.

   Framework:
   - The hook formula name and the gap score are both written in the output frontmatter
   - Gap score is 5 or 6. If it is 4 or lower, the post is not finished
   - Hook is 12 words or fewer. Count them
   - The sentence in the story that closes the hook's gap can be quoted. Quote it
   - Exactly one imperative verb appears in the offer. Count them
   - The offer matches the row for this post's goal in the offer table

   Sourcing:
   - Every number in the post appears in `knowledge/content-library/case-studies/` or in the
     user's brief. List each number and its source
   - If a number could not be sourced, hook formula 1 and 5 were not used, and the draft carries
     `[NEEDS INPUT: <what>]` rather than a placeholder figure
   - No customer, employer or partner is named unless the user named them in this conversation

   Format:
   - 80-220 words total. Count them
   - Zero em dashes and zero en dashes
   - Zero occurrences of: leverage, unlock, game-changer, "in today's fast-paced world",
     "excited to share", "thrilled to announce"
   - 2 hashtags or fewer, all lowercase, at the end
   - Every phrase in the brand's "avoids" list appears zero times

8. **Save** to `output/linkedin-post/<DD-MM-YYYY>-<slug>.md` with frontmatter:
   ```yaml
   ---
   format: linkedin-post
   topic: <topic>
   author: <founder|cmo|company>
   goal: <goal>
   hook-formula: <formula name>
   gap-score: <n>/6
   words: <count>
   created: DD-MM-YYYY
   ---
   ```

9. **Offer 2 hook variants** unless the user only wanted one. The hook is the highest-leverage edit point - a different hook formula on the same content can double or halve performance.

## Format guardrails

- 80-220 words total
- First line = hook (the only line guaranteed to be seen before "see more")
- Lines 2-3 must earn the click to "see more"
- No more than 2 hashtags, end of post, lowercase, niche-specific (skip generic ones like #marketing)
- Tag people only if the user explicitly named them

## Hook formula reference (quick pick)

| Situation | Best formula |
|---|---|
| You have a specific metric result | Formula 1: Specific number + surprising result |
| You want to challenge a common belief | Formula 2: Contrarian statement |
| You changed your own mind about something | Formula 3: Personal confession |
| You see a widespread mistake | Formula 4: Direct challenge |
| You have a transformation story | Formula 5: Before/after without the how |

## Rules

- Never skip the hook formula selection. Naming the formula is a forcing function - it prevents generic hooks.
- Never invent stats, customer quotes, or product capabilities. Pull from `knowledge/services/`
  and `knowledge/content-library/case-studies/` only, both of which step 1 loads.
- **If the post will carry a metric, open `knowledge/content-library/case-studies/` and confirm it
  exists there. If it does not, use hook formula 2, 3 or 4 - never 1 or 5.** Those two formulas are
  built around a specific number, so choosing them without one forces invention.
- The offer must be specific. "Let me know your thoughts" is vague. "Comment with the one thing you'd add" is specific.
- If the user wants to share a competitor opinion, flag risk and ask before publishing.
- The gap created in the hook must be closed in the body. If the post does not answer what the hook implied, the reader feels tricked - they will not follow or save.

## Stop conditions

Do not publish, and say which condition fired.

1. **The gap score is 4 or below after two rewrites.** The angle is the problem. Tell the user
   the post has no gap worth opening and ask for a sharper story or a real result.
2. **The post needs a metric and no metric exists in `knowledge/` or the brief.** Never invent
   one. Switch to hook formula 2, 3 or 4, or emit `[NEEDS INPUT: the actual number]` and stop.
3. **The post names a customer, employer, competitor or individual the user did not name.**
   Remove the name or ask. A named competitor claim on LinkedIn is public, permanent and
   attributable to a person.
4. **The post is written for a named executive and the user has not confirmed the executive
   holds this view.** Draft it, mark it `[APPROVAL NEEDED: <name>]`, do not present it as ready.
5. **The story and the hook answer different questions and neither can be moved.** Two posts,
   not one. Say so.

## Warning signs in your own draft

Ranked worst first. The first three block publication.

1. A number, percentage or result you cannot trace to a file or the brief. Blocker.
2. A named person or company the user did not supply. Blocker.
3. A claim about a competitor stated as fact. Blocker, route to the user.
4. The hook could open a post on any topic in the industry. It scores 0 on relevance, rewrite.
5. The story restates the hook rather than paying it off. The reader gets the feeling of being
   sold a click, and this is the single most reliable way to lose followers.
6. The offer is "thoughts?" or "agree?". No verb, no action.
7. Over 220 words, so the first three lines are carrying a post most readers will never expand.
8. Emojis or hashtags added because posts usually have them, rather than because
   `knowledge/brand/voice.md` says so.

## Related skills

- `/thought-leadership-writer` when the idea needs 1200 words and a defended thesis, not a post
- `/content-repurposer` to turn one article, webinar or case study into a run of posts
- `/social-calendar` for the posting plan and pillar mix this post should slot into
- `/content-writer` for the same idea in a different format, such as an email or blog intro
- `/copy-review` to grade a post the user already drafted rather than writing a new one
- `/case-study-writer` when the post keeps needing a result that has not been documented yet
- `/ab-copy-writer` when two hooks are both credible and the choice should be tested
- `/brand-context` first, whenever `knowledge/brand/voice.md` does not exist yet
- `/kpi-review` to check afterwards whether this format is actually working for the account

## What this skill cannot know

These are real limitations of this skill. Ask the user or emit `[NEEDS INPUT: <what>]` rather
than filling them in.

1. **Whether LinkedIn's current behaviour matches the defaults in this file.** Truncation point,
   link handling, hashtag treatment and feed ranking all change without notice, and this skill
   has no live view of the platform. Check in the composer before shipping anything that depends
   on a number here.
2. **What actually performs on this specific account.** Follower composition beats every general
   rule. If `knowledge/learnings.md` or the account's analytics disagree with this file, the
   account data wins.
3. **Whether the named author agrees with the post.** A founder byline is a public statement by a
   real person. Their approval is not something this skill can infer from the brand voice file.
4. **Whether a customer, partner or employer has agreed to be mentioned.** Consent lives in a
   contract or a thread, not in `knowledge/`.

## Platform figures are not facts

Any cadence, character count, best-day, format spec or benchmark in this skill is a starting
default recorded at authoring time, not a published platform rule. Two obligations:

1. **Verify current specs in the platform itself before shipping** anything that depends on them.
2. **This account's own historical data always wins.** Where `knowledge/learnings.md` or the
   team's analytics contradict a default here, follow the data and say so in the output.

Never present a default from this file to a client as though the platform published it. That is
the claim their in-house specialist corrects in the meeting, and the correction discredits
everything else in the document.
