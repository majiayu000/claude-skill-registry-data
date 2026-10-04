---
name: content-atomizer
description: Multi-channel content cascade skill. Takes ANY raw source material (build log, architectural note, vault entry, campaign retro, podcast transcript, code snippet) and atomizes it into multi-channel marketing content (X threads, LinkedIn posts, newsletter segments, visual card concepts). Use when the user says "content atomizer", "atomize this", "social posts from this", "repurpose content", or "create content cascade".
metadata:
  version: 1.0.0
---

# Content Atomizer Skill

The **Content Atomizer** takes 1 piece of longform technical content or build log and cascades it into 5 distinct, high-signal marketing assets tailored for X/Twitter, LinkedIn, newsletters, and visual posts.

---

## The Atomization Cascade

Given a raw input (article, vault note, architecture design, or code file), generate:

### Asset 1: The Deep-Dive X/Twitter Thread (5-7 Posts)
- **Post 1 (Hook)**: Punchy insight or proof-of-work statement + visual screenshot prompt.
- **Posts 2-5**: High-signal breakdown steps with clean code/diagram blocks.
- **Final Post**: Clear call to action (GitHub link or project URL).

### Asset 2: The LinkedIn Thought-Leadership Post
- **Format**: First-person practitioner perspective.
- **Structure**:
  - **Hook**: Highlighting an industry misconception or engineering trade-off.
  - **Body**: 3 concise takeaways written with natural line spacing.
  - **CTA**: Direct question to drive comment engagement.

### Asset 3: The Newsletter Digest Section
- **Format**: 150-word crisp summary suitable for a weekly developer newsletter or product update email.
- Includes a key takeaway block and "Read Full Post / Try Demo" link.

### Asset 4: The Visual Screenshot / Code Card Concept
- Text prompt specifying exact code block or diagram layout for a social visual card (e.g. 1200x630 dark mode card with syntax highlighting).

### Asset 5: The Short Video Demo Script (30-60s)
- **0-5s**: Hook (Visual outcome on screen).
- **5-20s**: Explaining the problem & unique mechanism.
- **20-30s**: Call to action.

---

## Quality Rules
- **No Clichés**: Filter out AI buzzwords ("delve", "game-changer", "unleash", "in today's fast-paced world").
- **Voice Checked**: Maintain authentic developer practitioner tone.
- **Source First**: Every post is grounded strictly in facts from the input material.
