---
name: caption-writer
description: "Writes platform-optimised social media captions for Instagram, LinkedIn, TikTok, or Twitter/X from a brief, article excerpt, or content description — matched to the platform's conventions and the account's voice."
status: stable
category: social-media
subcategory: content
version: 1.0
eval_score: 4.4
tags: [social-media, content, captions, copywriting, instagram, linkedin, tiktok]
---
# Caption Writer

## What This Skill Does
Writes platform-optimised social media captions for Instagram, LinkedIn, TikTok, or Twitter/X from a brief, article excerpt, or content description — matched to the platform's conventions and the account's voice.

## When To Use This Skill
- You need captions for a batch of posts and want consistent, platform-appropriate copy
- You have a piece of content (article, video, podcast episode, photograph) and need to adapt it for social
- Your existing captions feel generic and you want them to reflect a specific voice or tone
- You are posting across multiple platforms and need different versions of the same story

## What You Need To Provide
**Required:** The platform(s) you are writing for (Instagram, LinkedIn, TikTok, Twitter/X), what the post is about or what it shows/links to, the intended effect (inform, provoke discussion, drive to a link, build community, entertain).

**Optional:** Your account's voice or tone (formal, conversational, opinionated, dry, warm), any hashtag strategy or specific tags to include, the account type (personal brand, media outlet, documentary film, magazine, podcast), a character or word count limit.

## How the Assistant Approaches This
1. Identifies the platform's conventions and what performs well in that context — Instagram rewards visual storytelling and warmth, LinkedIn rewards insight and professional credibility, TikTok rewards immediacy and humour or raw authenticity, Twitter/X rewards brevity and opinion
2. Takes the core content and finds the single most engaging angle for the platform — not the most complete description of the content, but the one sentence or idea that makes someone stop scrolling
3. Writes to the platform's natural length and structural conventions: hook, body (or immediate impact), close (question, CTA, or punchline), then suggests hashtags or platform-specific elements if requested
4. After the captions, provides a "Next Step" note: which platform to post to first based on where the account's audience is most active, whether thread-writer or carousel-script-writer should be run to build out the content further, and the recommended posting time window for each platform

## Output Format
One caption per platform requested. Instagram: 125–200 words + hashtag suggestions (5–10 relevant tags). LinkedIn: 100–150 words, no hashtag padding. TikTok: 50–80 words, conversational, fast. Twitter/X: 240–280 characters, with an optional threaded follow-up. Each caption clearly labelled with the platform. Emojis used if appropriate to the voice and platform; omitted if the account is formal or serious. Output ends with a "Next Step" note: which caption to post first, whether to run thread-writer or carousel-script-writer to extend the content, and the recommended post scheduling action.

## Quality Criteria
- [ ] Each caption uses the specific conventions of its platform — not the same text reformatted
- [ ] Opening line works as a hook even in a preview/truncated view (Instagram's "more" fold)
- [ ] The intended effect (inform / provoke / drive / entertain) is evident in the caption's structure
- [ ] No generic filler phrases ("check this out," "so excited to share," "this one really hits different")
- [ ] Hashtags (where used) are relevant and not purely reach-padding with irrelevant tags
- [ ] Voice is consistent — if the account uses first person, all captions use first person
- [ ] Output includes at least one concrete next action the user can take immediately (schedule the highest-priority caption, run thread-writer or carousel-script-writer to extend the content)

## Example

### Input
Platform: Instagram and LinkedIn
Content: A new episode of an investigative documentary podcast just dropped. Episode 6 digs into how a legal provision designed to protect whistleblowers has been used repeatedly by corporations to suppress journalists. Three lawyers and two former journalists who had their stories killed are interviewed.
Account type: Documentary podcast
Voice: Serious, direct, a little dry
Intended effect: Drive listens, provoke discussion

### Output

---

**INSTAGRAM**

The law that's supposed to protect whistleblowers.

Episode 6 of [PODCAST NAME] looks at how a legal provision designed to shield people who speak out has quietly become one of the most effective tools corporations use to kill journalism instead.

Three lawyers. Two journalists whose stories never ran. And the documents that explain why.

Link in bio.

*#investigativejournalism #documentarypodcast #pressfreedoom #whistleblowers #mediaindustry #journalism #podcast #truecrime #medialaw*

---

**LINKEDIN**

Episode 6 of [PODCAST NAME] examines something that doesn't get enough attention: how whistleblower protection statutes — designed to encourage transparency — have been turned into litigation instruments that silence investigative reporting.

We interviewed three legal practitioners and two journalists whose stories were suppressed using these mechanisms. What they describe is a pattern, not a series of isolated incidents.

For anyone working in media law, investigative journalism, or press freedom — this episode is worth your time.

Listen at [link].

## Known Limitations
- Caption quality depends heavily on the quality and specificity of the input. Vague briefs ("write a caption about our documentary") produce generic output — the more specific the content and the intended effect, the better the caption.
- This skill does not have access to platform analytics. Recommendations about what "performs well" are based on general platform conventions, not data from your specific account. Your own account's historical performance is the most reliable guide.
- Hashtag suggestions are based on relevance to the topic, not current algorithm performance. Hashtag effectiveness shifts frequently on Instagram and TikTok; treat suggestions as a starting point and supplement with your own research.

## Related Skills
- [thread-writer](../thread-writer/SKILL.md)
- [carousel-script-writer](../carousel-script-writer/SKILL.md)
- [short-form-video-brief](../short-form-video-brief/SKILL.md)
- [platform-strategy-brief](../../strategy/platform-strategy-brief/SKILL.md)
