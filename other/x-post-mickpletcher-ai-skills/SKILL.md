---
name: x-post
description: Write posts for X on tech, PowerShell, IT automation, and fitness topics. Always trigger immediately when the user's message starts with "xp". Produce a single post within 280 characters, no emojis, avoid em dashes in final X post output, and use 2 to 3 hashtags maximum.
version: 1.1.0
---

# X Post Skill

## Intent

Write concise X posts about tech, PowerShell, IT automation, projects, and fitness in Mick's voice.

## Do Not Use When

- Do not use for long-form posts, Facebook posts, LinkedIn posts, replies, or claims that need missing proof.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Write posts for X on tech, PowerShell, IT automation, and fitness. The voice should stay direct, specific, and compressed. Every post must fit within a single 280-character post including hashtags.

## Trigger

Activate when the message starts with `xp`. Everything after it is the draft or topic. Rewrite it immediately. No clarifying questions first.

```text
xp just automated Intune compliance reporting, cut a 2 hour manual process down to 3 minutes
xp hit 790 on leg press today, started at 465 three months ago
```

## Non-Negotiable Rules

- No emojis
- Avoid em dashes in final X post output
- No quotation marks around words or phrases
- Single post only
- Must fit within 280 characters including hashtags
- Use 2 to 3 hashtags maximum, placed at the end
- First person, confident, and conversational
- Always show the character count after the post

## Character Budget

280 characters total. Hashtags count toward that total.

- Two hashtags usually consume about 20 to 30 characters
- Leave enough space for the body before adding hashtags
- If the draft is too long, cut adjectives first, then restructure instead of truncating mid-thought

Always show the count in this format:

```text
[X / 280 characters]
```

If the post is over 280 characters, flag it and provide a tighter version automatically.

## Voice and Tone

X rewards punchy, opinionated, specific posts. Use the same direct voice as the Facebook writing skills, but more compressed. Lead with the most interesting detail first.

Banned phrases:

- `journey`
- `transformative`
- `game-changer`
- `next level`
- `cutting-edge`
- `excited to share`
- `proud to announce`
- `diving deep`
- `leverage`
- `showcase`
- `utilize`
- `The takeaway here is...`

### What works on X

- Specific numbers over vague claims
- Plainly stated opinions
- Process details that show expertise
- Before and after contrast

### What does not work on X

- Anything that sounds like a LinkedIn post
- Motivational sign-offs
- Vague humble-brags without specifics
- Asking people to like or repost

## Hashtag Strategy

Always use 2 to 3 hashtags and place them at the end.

**Tech / PowerShell / IT**

`#PowerShell #ITAutomation #Intune #Azure #SCCM #EndpointManagement #Microsoft #SysAdmin`

**Fitness**

`#StrengthTraining #MuscleBuilding #FitnessProgress #Lifting #NaturalStrength`

For topics not listed, choose 2 to 3 specific hashtags that fit real X communities.

## Length Presets

Infer the right preset from the draft. Default to a single post.

- **Single post** (default): full 280-character budget, hook plus optional support line.
- **One-liner**: under 140 characters, one sharp claim or number, 1 to 2 hashtags. Use when the draft is a single punchy fact or opinion.
- **Thread opener**: when the topic clearly needs more than one post, write the strongest standalone first post and note that a thread would follow. Do not write the rest of the thread unless asked.

## Hook Generation

Before writing the final post, internally draft 2 to 3 candidate opening clauses and keep the one that lands fastest. The first clause has to earn the read on its own. Prefer the most specific number, contrast, or opinion in the source material. Never open with setup phrases like "I recently" or "Today I".

## Topic Modes

Adjust emphasis by topic. Do not announce the mode.

- **PowerShell / endpoint management**: lead with scale (device counts, time saved), name the tool stack, use tech hashtags.
- **Fitness**: lead with the number and the timeframe, keep it factual rather than motivational, use fitness hashtags.
- **Build / project updates** (container home, homelab, trading): lead with what changed since the last update and one concrete detail that shows real progress.

## Post Structure

```text
[Hook with the most specific or interesting detail first]
[Optional supporting sentence if budget allows]
#Hashtag1 #Hashtag2
```

## Examples

**Tech**

Draft:

```text
just automated Intune compliance reporting, cut a 2 hour manual process down to 3 minutes
```

Post:

```text
Automated Intune compliance reporting across 4,000 endpoints. What took 2 hours manually now runs as a scheduled job in 3 minutes. #PowerShell #ITAutomation
```

**Fitness**

Draft:

```text
hit 790 on leg press today, started at 465 three months ago
```

Post:

```text
790 lbs on leg press today. Started at 465 three months ago. 75% improvement and still climbing. #StrengthTraining #MuscleBuilding
```

**Bad**

```text
So excited to share that I've been absolutely crushing my fitness goals lately! This journey has been so rewarding! #FitnessJourney #Blessed
```

## Output Format

Output the post text first, then the character count on the next line. After that, ask whether anything should be adjusted.

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A draft, a result, or the main point you want in the post.

Example prompts:

- `Use x-post to turn this PowerShell win into a tight post for X.`
- `Write three X post options about this training milestone with a direct tone.`
- `Show me an example prompt for using this skill with a rough draft.`

