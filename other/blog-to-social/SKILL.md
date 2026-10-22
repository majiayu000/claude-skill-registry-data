---
name: blog-to-social
description: Convert a finished blog post into three ready-to-post social media versions in one pass for Facebook, X, and LinkedIn. Always trigger immediately when the user's message starts with "bts". Also trigger on "blog to social", "social posts for this", "promote this post", or when the user pastes or links a blog post and asks to share it, promote it, or turn it into social content.
version: 1.1.0
---

# Blog To Social

## Do Not Use When

- Do not use to write the source blog post from scratch, invent missing claims, or publish directly.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

Use this skill when the user wants one finished blog post converted into Facebook, X, and LinkedIn posts in a single pass.

## Trigger When

- The user says `bts`, `blog to social`, `social posts for this`, or `promote this post`
- The user pastes a blog post and wants social versions of it
- The user links to a blog post and wants platform-ready copy for multiple social channels

## Intent

Read the blog post once, extract the strongest raw material, and produce platform-native Facebook, X, and LinkedIn posts without back-and-forth.

## Workflow

1. Read the blog post or linked content.
2. Extract the core point, strongest specifics, likely audience, and the best hook.
3. Write Facebook, X, and LinkedIn posts in that order.
4. Make each post native to its platform instead of compressing the same wording three times.
5. End with a short note about anything that should be verified before posting, such as the final URL.

## Platform Rules

### Facebook

- Casual and direct
- 1 to 2 short paragraphs
- Include the actual blog URL
- Use 6 relevant hashtags
- Lead with a specific detail, result, number, or tool

### X

- 280 characters maximum including hashtags
- Lead with the strongest detail first
- Use 2 to 3 hashtags
- Include the URL only if it fits cleanly
- Keep it tight and specific

### LinkedIn

- 3 to 5 short paragraphs
- Hook first, then problem, approach, and result
- Include the blog URL before hashtags
- Use 3 to 5 relevant hashtags
- Keep it structured but still in Mick's voice

## Voice Rules

- No emojis
- Avoid em dashes in final post output
- Avoid quotation marks when they are not needed
- Lead with specifics instead of a vague setup sentence
- Avoid corporate buzzwords and AI filler phrases
- Each post must stand on its own

## Content Rules

- Produce all three posts in one pass
- Do not ask which platform to start with
- Do not summarize the blog post into generic copy
- Lead with the most concrete result, number, tool, or takeaway from the post
- Do not reuse the same wording across Facebook, X, and LinkedIn
- Always include the actual blog URL in Facebook and LinkedIn

## LinkedIn Guidance

LinkedIn should follow this order:

1. Hook
2. Problem
3. Approach
4. Result
5. Call to read or a real question for comments

Avoid opening with `I` as the first word. Avoid phrases like `excited to share`, `game-changer`, or `diving deep`.

## Length Controls

Default lengths follow the platform rules above. Adjust when the user asks or when the source clearly calls for it:

- `short`: one tight paragraph for Facebook and LinkedIn, the leanest X version
- `medium`: the platform defaults
- `thread`: for X only, when the post has 3 or more distinct takeaways worth separate posts; write a strong standalone opener plus numbered follow-up posts, each under 280 characters

The user can mix, such as `bts short facebook, thread x`.

## CTA Selection

Pick one CTA intent per platform based on what the blog post actually offers:

- `click through`: the post is a teaser and the value lives in the blog; end on the gap the link fills
- `discussion`: the post takes a position or shares a tradeoff; end with one grounded question
- `save for later`: the post is reference material such as a script or checklist; say plainly what the reader will come back for

Do not stack CTAs, and skip the CTA entirely when the post stands alone.

## Hook Quality Pass

Before writing the three posts, pull the 2 to 3 strongest hook candidates from the blog post: the best number, the sharpest result, the most surprising finding. Pick a different lead for each platform when the material supports it, so the three posts read as siblings rather than copies. If the blog post buries its best detail in the middle, that detail is the hook.

## Output Format

Use this layout:

```text
## Facebook

[post text]

---

## X
[X / 280 characters]

[post text]

---

## LinkedIn

[post text]
```

After all three posts, add a one-line note for anything that should be verified before posting.

## Constraints

- Do not sound like an AI-generated press release
- Do not use the same wording across all three platforms
- Do not leave out the blog URL from Facebook or LinkedIn
- Do not flatten the post into vague promotional language

## Validation Checklist

- [ ] All three posts are produced in one pass
- [ ] Each platform version stands on its own
- [ ] Each post leads with a concrete detail
- [ ] X stays within 280 characters
- [ ] Facebook and LinkedIn include the actual blog URL
- [ ] Final copy avoids emojis and em dashes

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A finished or mostly finished blog post, plus any preferred platform emphasis.

Example prompts:

- `Use blog-to-social to turn this finished blog post into Facebook, X, and LinkedIn drafts.`
- `Convert my latest post about Azure automation into short social posts for each platform.`
- `Show me an example prompt for repurposing a technical blog post into social content.`

