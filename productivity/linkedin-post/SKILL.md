---
name: linkedin-post
description: Write LinkedIn posts for Mick Pletcher's professional audience. Always trigger immediately when Mick says "linkedin post", "lnp", or asks to write something for LinkedIn. LinkedIn audience is professional IT, AI, and automation peers. Tone is more polished than Facebook but still first-person and direct. No emojis. Avoid em dashes in final LinkedIn post output. 2 to 3 hashtags max. Focus on home AI infrastructure, algorithmic trading, enterprise automation, career insights, and tech commentary.
version: 1.2.0
---

# LinkedIn Post Skill

## Intent

Write LinkedIn posts in a credible practitioner voice with clear mode, audience, and call-to-action control.

## Do Not Use When

- Do not use for Facebook posts, X posts, resumes, or claims that require proof the user did not provide.
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

Write LinkedIn posts for Mick Pletcher's professional audience in a voice that is direct, technical, and first-person.

## Trigger

- `lnp` for immediate triggering
- `linkedin post about...`
- `write something for LinkedIn`

Treat `lnp` as an immediate trigger. Do not ask clarifying questions first unless the source material is missing a critical fact that would change the post.

## Audience and Tone

**Audience:** IT professionals, automation engineers, AI enthusiasts, enterprise tech practitioners, hiring managers, and peers in the Nashville and CBIZ space.

**Tone compared to other platforms:**

- More professional than Facebook, less casual than X
- Still first-person and direct, not corporate
- Shares real work, real results, and real opinions
- No humble-bragging
- Slightly longer than X and shorter than a blog post
- 150 to 400 words is the sweet spot

## Content Pillars

1. **Home AI infrastructure**: Proxmox, n8n, local LLMs, MCP servers, Claude integrations
2. **Enterprise automation**: PowerShell, SCCM, Intune, Microsoft Graph, CBIZ projects
3. **Algorithmic trading**: Alpaca, Python and PowerShell trading stack, paper versus live workflows
4. **Career and community**: Nashville PowerShell User Group, personal milestones, early retirement path
5. **Tech commentary**: GTC keynotes, new model releases, tooling observations

## Post Modes

Infer one of these modes unless the user explicitly asks for a different one:

- `career update`
- `technical lesson`
- `project breakdown`
- `opinion`

### Mode Guidance

- `career update`: center the milestone, what changed, and why it matters professionally
- `technical lesson`: lead with the lesson or result, then show how it was learned or built
- `project breakdown`: explain the problem, approach, tools, and outcome with enough structure to feel credible
- `opinion`: make the viewpoint clear early and support it with concrete reasoning instead of hot air

## Tone Controls

Infer one of these audience tones unless the user specifies one:

- `practitioner`
- `leadership`
- `builder`

### Tone Guidance

- `practitioner`: technical, grounded, tool aware, and peer level
- `leadership`: strategic, outcome oriented, and broader in framing without turning corporate
- `builder`: hands on, iterative, and focused on what was actually made or solved

## Hook Styles

The first two lines should create interest without sounding inflated.

Prefer hook styles such as:

- the concrete result
- the problem solved
- the lesson earned
- the tension or tradeoff

Avoid inflated hooks that sound like generic personal branding.

## Credibility Checks

Before finalizing the post, push for:

- proof: what was actually built, changed, or observed
- outcome: what improved, shipped, or became possible
- context: where this fits and why it matters

If the draft only makes vague claims, rewrite it toward specifics instead of amplifying the vagueness.

## Post Structure

**Hook line**

The first 1 to 2 sentences should earn the click in the feed preview. State what was built, solved, or learned. Skip the preamble.

**Body**

Use 2 to 4 short paragraphs. Explain what it is, why it matters, and how it works at a high level. Include specific tools, numbers, or outcomes where possible. One concrete detail is better than three vague claims.

**Closing line**

Optional. Use it for what comes next, a short observation, or a fitted CTA when the post would benefit from one.

**Hashtags**

Use 2 to 3 hashtags on their own line at the end.

## Format Rules

- No emojis
- Avoid em dashes in final LinkedIn post output
- No bullet points unless genuinely listing 3 or more discrete items
- Keep paragraphs short, usually 2 to 3 sentences
- Leave line breaks between paragraphs
- Put hashtags at the bottom, not in the middle of the post
- Do not wrap the post in quotes

## CTA Styles

Use a CTA only when it fits the post. Infer the best one unless the user specifies it:

- `hiring`
- `networking`
- `repo traffic`
- `discussion`
- `none`

### CTA Guidance

- `hiring`: brief note for people who may want to connect or collaborate professionally
- `networking`: useful when the post is about shared interests or adjacent work
- `repo traffic`: point to the repo or writeup without sounding thirsty
- `discussion`: one grounded prompt that invites real input
- `none`: default when the post stands best on its own

## Audience Testing Variants

When the user asks for variants, produce:

- one more technical practitioner draft
- one broader professional draft

Keep the core point the same while changing the framing, jargon level, and emphasis.

## Media Companion Suggestions

When the post would clearly land better with supporting media, add a short note after the post (not inside it) suggesting what to attach:

- screenshots for dashboards, reports, n8n flows, or terminal output that prove the result
- a simple architecture sketch when the post describes a multi-part pipeline
- a carousel only when the content is genuinely sequential, such as before and after steps; if suggesting one, list the 3 to 5 slide headlines

Never invent what an image shows. If no media would help, say nothing.

## Series Planning

When the user wants a multi-post series (project writeup, learning log, build diary):

- propose 3 to 5 post topics that each stand alone but build a through line
- give each a working hook line and the mode it should use
- order them so the strongest standalone post goes first, since later posts inherit its audience
- keep one continuity element across the series, such as a project name or running metric

## Post To Article Expansion

When a short post performed well or the user asks to go longer, expand it into a LinkedIn article draft:

- working title, opening that restates the hook with more context, and 3 to 5 sections with headers
- move the technical depth the post had to compress into the body, with specifics and code or config references where Mick can paste real material
- end with what is next rather than a motivational wrap-up
- keep the same first-person practitioner voice; an article is a longer post, not a whitepaper

## Example Post Pattern

```text
Built an automated morning briefing pipeline in n8n this week.

It pulls crypto prices from CoinGecko, top stories from RSS feeds, and market commentary from Reddit, then sends everything through the Claude API for summarization before delivering a consolidated brief each morning.

The whole thing runs on my Proxmox homelab, exposed via Cloudflare Tunnel. Zero manual steps from wake-up to briefing.

Next phase is integrating live Alpaca portfolio data so the brief includes overnight position changes alongside the news.

#automation #homelab #n8n
```

## Quality Checklist

- Hook line earns attention in the first 1 to 2 sentences
- Hook style creates interest without sounding inflated
- Specific tools or outcomes are mentioned
- Proof, outcome, and context are present
- No emojis and no em dashes in final output
- 2 to 3 hashtags at the bottom only
- Reads as professional but not corporate
- No filler phrases or AI-sounding language
- Written in first person as Mick
- Post mode matches the kind of story being told
- Tone control fits the intended audience
- CTA style is intentional when one is used

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A topic, draft, or concrete win you want to post about.

Example prompts:

- `Use linkedin-post to turn this project update into a LinkedIn post for technical peers.`
- `Write a LinkedIn post about automating endpoint reporting without sounding like a marketer.`
- `Show me an example prompt for a credibility focused LinkedIn post.`

