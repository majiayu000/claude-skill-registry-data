---
name: painpoint-research
description: Run structured social-media painpoint research for a sharply-defined ideal customer profile, returning direct quotes with source URLs grouped by theme, ranked by emotional intensity and frequency. Use when the user says "find me painpoints for [ICP]," "research what [audience] is complaining about," "pull customer language from Reddit/Twitter/forums," or similar.
---

# Painpoint Research

Surface direct quotes from places your customers already talk, organized so you can use them in copy and validation.

## When to trigger this skill

The user wants any of:

- "Find me painpoints for [ICP]"
- "Research what [audience] is complaining about"
- "Pull customer language from social media for [segment]"
- "What are [persona] saying about [problem]?"

Do NOT trigger this skill when:

- The user wants generic web research (use a web search directly)
- The ICP is vague ("small business owners" — too broad). Ask for sharpness first.
- The user wants competitive intel about specific vendors (use a different workflow)

## Inputs you need

**Required:**
- A sharply-defined ICP. Examples: "Family caregivers in the sandwich generation taking care of elderly parents." "Solo founders building their first SaaS without a technical background." "YouTube creators with under 10K subscribers trying to monetize."

If the user gives a vague ICP, ask them to narrow it before researching. Bad: "marketing managers." Good: "growth marketing managers at 20-50 person B2B SaaS startups who report to the CEO and have no agency budget."

**Optional but useful:**
- The problem space you're focused on (saves time vs. open-ended research)
- Any platforms to exclude (e.g. "skip Reddit, my customers aren't there")

## Workflow

### 1. Sharpen the ICP

If the ICP is too broad, ask one question to sharpen it. Then proceed.

### 2. Run the research

Search across the platforms where the ICP actually talks. Default platforms:

- **Reddit** — search relevant subreddits for the ICP. Pull from the comments, not just top-level posts.
- **Twitter / X** — search the exact phrases the ICP would use to describe their pain.
- **Forums and niche communities** — Indie Hackers, Hacker News, Stack Exchange, professional subreddits.
- **Facebook Groups** (rarely searchable directly, often skipped).
- **LinkedIn** — pull from comments on posts about the problem space, not from profile bios.
- **Product review sites** — G2, Capterra, TrustRadius for the "what I hate about my current tool" reviews.

For each painpoint you find:

- **Capture verbatim.** Don't paraphrase. The customer's exact language is what's valuable.
- **Tag emotional intensity.** Mild / moderate / strong, based on emotion words and intensifiers.
- **Note source URL.** Always. No quote goes in without a source.
- **Group by theme.** Cluster related painpoints. Five to seven themes is usually right.

### 3. Generate the research artifact

Use `template/research-output.md`. Fill every section.

Save to `~/painpoint-research/<icp-slug>/painpoints.md`.

### 4. QA check

Before reporting done, verify:

- At least 15 direct quotes total
- Every quote has a source URL
- Themes are clustered (not 15 standalone quotes with no grouping)
- At least one quote with strong emotional intensity per major theme
- No fabricated quotes. If you can't find something, say so.

### 5. Present

Tell the user:

- The themes you found, ranked by signal strength
- Two or three quotes worth using directly in copy or outreach
- Any themes that surprised you, with what they might mean
- The platforms that yielded the most signal (helps with channel planning)

## What to look for, not just collect

- **Repeated language.** When five different people describe the same pain in similar words, that's the copy you want on your landing page.
- **Emotional intensifiers.** "I literally," "I hate," "every single time," "I can't even." These mark strong painpoints worth leading with.
- **What they've tried.** Workarounds are gold. They tell you which adjacent solutions to compare against and where the solution space already failed them.
- **What they're afraid of.** Painpoints + fear of trying again is a buying signal.

## What to flag as caveats

- A quote from a single thread isn't a pattern. Need at least 3 independent sources.
- Highly upvoted posts can be selection bias. The loudest pain isn't always the most common.
- Some ICPs don't post about their pain publicly (regulated industries, senior executives). Don't force a research artifact when the ICP isn't online about it. Recommend interviews instead.
