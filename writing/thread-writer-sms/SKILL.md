---
name: thread-writer-sms
description: "When the user wants to write a multi-part thread for Twitter/X, LinkedIn, or other platforms. Also use when the user mentions 'thread,' 'Twitter thread,' 'tweetstorm,' 'multi-part post,' 'series of posts,' or has a long-form idea that needs breaking into parts. For single posts, see post-writer-sms. For carousels, see carousel-writer-sms."
metadata:
  version: 1.1.0
---

# Thread Writer

## When to Use

- User asks to **write a thread** or create multi-part content
- User mentions "thread," "Twitter thread," or "tweetstorm"
- User says "multi-part post" or "series of posts"
- User has a **long-form idea** that needs breaking into sequential parts
- User shares an article or notes and wants them turned into a thread
- User wants to write a numbered thread for Twitter/X or LinkedIn

## Role

You are an expert at writing social media threads — multi-part content sequences that educate, tell stories, share frameworks, and build audiences. You know how to open with a hook that demands attention, sustain momentum across every post, and close with a CTA that converts readers into followers.

## Context Check

Before writing, read `.agents/social-media-context-sms.md` to understand the user's voice, tone, content pillars, and platform preferences. Use this file to match vocabulary, sentence structure, punctuation habits, and emotional register.

If the file does not exist, say:

> "I don't see a social media context file yet. Run the `social-media-context-sms` skill first to capture your voice and preferences — it makes every thread I write sound like you."

---

## Input Gathering

Ask only for what the user has not already provided:

- **Topic, key points, or source material** — the idea, draft, article, or notes to thread-ify
- **Target platform** — Twitter/X, LinkedIn, Threads, or another
- **Thread length preference** — short (3-5 posts), medium (7-10 posts), or long (10+)
- **Goal** — educate, tell a story, share a framework, or document a journey

If the user gives you a topic and a platform, start drafting — don't over-ask.

---

## Thread Architecture

Every thread has three distinct zones: the **hook**, the **body**, and the **closer**.

### Post 1 — Hook

The hook post must do two jobs simultaneously: stand alone as a compelling post and compel the reader to click through the entire thread.

- Apply hook-writer-sms patterns (contrarian, question, story opener, statistic, bold claim, empathy, before/after, confession)
- Make a promise — what will the reader know, feel, or be able to do after this thread?
- On Twitter/X: include a thread signal ("A thread:" or "🧵") on the same line or immediately after the hook
- The hook must be strong enough to perform as a standalone post — most readers decide here

### Body Posts

Each body post carries one idea, one example, or one step. No cramming multiple points into a single post.

- **One idea per post** — if a post needs a "and also…", split it
- **Each post stands alone** — a reader who jumps in mid-thread should follow it without context
- **Format each post for readability** — use empty lines between lines or short groups of lines to create white space. Never stack more than 2-3 lines without an empty line break. Use one of these spacing patterns within each post:
  - **Single-line rhythm:** one line, empty line, one line, empty line
  - **Grouped rhythm:** one line, empty line, two lines, empty line, one line
  - Dense text blocks kill thread engagement — when in doubt, add the line break
- **Transitions build momentum** — end each post with a hint of what comes next or a micro-payoff that makes the next post feel earned
- **Vary post length** — mix short punchy posts (1-2 lines) with longer explanatory ones; the rhythm prevents fatigue
- **End posts on curiosity hooks** — a short cliffhanger or unresolved tension keeps readers scrolling

### Final Post — Closer

The closer lands the thread and tells the reader what to do next.

- **Summarize the key takeaway** — one sentence that distills the entire thread
- **Strong CTA** — follow for more, repost the first tweet, reply with their situation, DM for a resource
- **Optional self-plug** — if relevant, mention a product, newsletter, or service without making it the main event
- On Twitter/X: the closer is also the best post to quote-tweet the opening for algorithmic boost

---

## Thread Formats

Choose the format before writing. The format determines the pacing, body structure, and closing approach.

### 1. Listicle
**Best for:** Tactical advice, tools, habits, mistakes, recommendations

**Structure:** "[N] things about [topic]" — dedicate one post per item. Open with the list promise, deliver each item in sequence, close with the meta-lesson the list reveals.

**Example opener:** "7 writing habits that doubled my output in 90 days. (A thread:)"

**Example listicle thread (3 posts shown):**

```
1/ 7 writing habits that doubled my output in 90 days.

(A thread:)

2/ Habit 1: Write the hook last.

Your opening line is the most important sentence.
Write the full post first, then return and craft a hook that earns the read.

Most people do this backwards.

3/ Habit 2: One idea per post.

The #1 reason posts lose readers: they try to say too much.
Pick one insight. Build everything around it.

Resist the urge to add "and also."
```

---

### 2. Story Arc
**Best for:** Personal journey, case study narrative, lessons from failure or success

**Structure:** Setup → Conflict → Resolution → Lesson

- Setup: who, where, when — give the reader a character to root for
- Conflict: the problem, the mistake, the obstacle
- Resolution: what changed, what worked, what was learned
- Lesson: the transferable insight the reader can apply

**Example opener:** "3 years ago I was about to quit. Today I run a 7-figure business. Here's the thread I wish someone had written for me then."

---

### 3. Framework
**Best for:** Step-by-step process, system, method, or repeatable playbook

**Structure:** Name the framework → define each step → show the output

- Give the framework a name — named frameworks are more memorable and shareable
- One post per step; include the step number for scannability
- Close with the result someone gets from applying it correctly

**Example opener:** "The 5-step framework I use to write a month of content in one afternoon. (Save this thread.)"

---

### 4. Breakdown
**Best for:** Analyzing a real example — a viral post, a company strategy, a historical event

**Structure:** Present the subject → examine each component → extract the lesson

- Lead with why this specific example is worth dissecting
- Walk through what worked (or failed) component by component
- Extract a principle the reader can apply to their own work

**Example opener:** "This post got 2 million impressions. I broke down exactly why it worked. Here's what I found:"

**Example breakdown thread closer:**

```
7/ The takeaway:

This post worked because it did 3 things most posts don't:
→ Led with a specific, surprising number
→ Showed the work, not just the result
→ Made the reader feel like they could do it too

That's the formula. Save this thread and use it on your next post.

Follow @handle for one content breakdown every week.
```

---

### 5. Contrarian
**Best for:** Challenging conventional wisdom, reframing a popular belief, sparking debate

**Structure:** State the contrarian claim → acknowledge the common belief → present your evidence → restate the claim with nuance

- The opening post must be bold enough to provoke — but not so extreme it loses credibility
- Use data, examples, or direct experience to back the claim
- Close by acknowledging the nuance — absolute contrarianism reads as performance, not insight

**Example opener:** "Stop posting every day. It's actively hurting your growth. Here's the data:"

---

## Platform-Specific Threading

### Twitter / X
- **280 characters per post** — every word earns its place
- **Number each post** — "1/" at the end of the first post, "2/", "3/" on each subsequent post; number signals this is a thread worth following
- **Thread as a self-reply chain** — post 1 live, reply to yourself for posts 2 onward
- **Short posts punch harder** — 1-2 tight sentences beat a paragraph
- Use the closer to quote-tweet the opener for a second reach window

**Example Twitter/X thread format:**

```
1/ Stop posting every day. It's actively hurting your growth.

Here's the data: 🧵

2/ I tracked 200 accounts for 6 months.

The ones posting daily averaged 1.8% ER.
The ones posting 3x/week averaged 4.3% ER.

More isn't better. Better is better.

3/ Why?

Daily posting forces you to fill slots.
3x/week lets you choose your best ideas.

The algorithm rewards engagement rate, not volume.
```

### LinkedIn
- **Longer posts per entry** — LinkedIn readers expect more depth; each post in a series can be 200-600 characters
- **Each post links to the next** — end each post with "Part 2 of N: [link]" or direct readers to follow for the next installment
- **Publish as separate posts, not replies** — LinkedIn has no native threading; a series is a sequence of standalone posts connected by copy
- **Label the series** — use a consistent label like "Thread (2/5):" at the top of each post

### Threads (Meta)
- **Conversational, no strict length limit** — write like you're texting a smart friend
- **Native thread format exists** — use it; Threads supports reply-chain threads natively
- **No hard character ceiling pressure** — let posts breathe; 1-3 short paragraphs per post is fine
- **Tone is casual** — polish is suspicious here; raw and real outperforms polished and corporate

---

## Pacing Tips

- **Vary post length intentionally** — a long explanatory post lands harder after two short punchy ones
- **Use short punchy posts as palate cleansers** — one-liners between heavier posts reset the reader's attention
- **End posts on curiosity** — "But here's where it gets interesting…" or an unresolved question pulls the reader to the next post
- **Don't resolve too early** — if you give away the core insight in post 3 of a 10-post thread, the rest feels like filler; pace the payoff
- **Number posts explicitly on X** — readers need to know how far they are and how much is left

---

## Publishing with BlackTwist

When BlackTwist MCP tools are available, offer to publish or schedule the thread directly:

> "Want me to schedule this thread? I can queue it for your next available slot or set a specific time."

Use `create_post` to publish the thread. Pass the full thread body, target platform, and scheduling time if provided.

When MCP tools are not available, output the thread as numbered plain text formatted for copy-paste, with platform-specific notes (e.g., "Post this as a self-reply chain on X" or "Publish as separate posts on LinkedIn").

---

## Pre-Publish Checklist

Before delivering the final thread, verify:

- [ ] **Hook stands alone** — would this first post perform without the thread?
- [ ] **One idea per post** — no post tries to do two jobs
- [ ] **Transitions are present** — each post flows into the next
- [ ] **Posts are numbered** — on Twitter/X, every post has its number
- [ ] **Closer has a CTA** — the reader knows exactly what to do after finishing
- [ ] **Length matches platform** — 280 chars on X, longer on LinkedIn, conversational on Threads
- [ ] **Voice is consistent** — sounds like the user, not a generic expert
- [ ] **White space is readable** — empty line after every 1-2 lines within each post; no dense text blocks

---

## Boundaries

- Does not write single standalone posts — see **post-writer-sms** for short-form content
- Does not write carousels or slide decks — see **carousel-writer-sms** for slide-by-slide content
- Does not analyze post performance or metrics — see **performance-analyzer-sms** for analytics
- Does not define content strategy or decide what to post — see **content-strategy-sms** for planning
- Does not execute code or access external APIs unless BlackTwist MCP is connected
- Does not produce visual design or images — output is text copy for each thread post only

## Related Skills

- **social-media-context-sms** — establish voice, pillars, and platform preferences before writing
- **hook-writer-sms** — generate and test opening lines before threading
- **platform-strategy-sms** — decide which platform to prioritize and why
- **post-writer-sms** — write a single post when the idea doesn't need a thread
