---
name: learn-grimoire
description: Use when the user wants to get oriented on grimoire itself — what it is, why it exists, its core concepts, and how to actually use it day to day. For a brand-new user who just installed grimoire, or an existing user who has been using it without understanding the system underneath. Distinct from learn-best-practice (durable retention of one specific installed practice) and explain-best-practice (why one specific practice works).
source: Stripe and GitHub developer-onboarding design writing — lead with why before mechanics; grimoire's own STANDARD.md Purpose section and README.md project framing
tags: [onboarding, orientation, grimoire, first-use, core-concepts, discovery]
related: [learn-best-practice, discover-best-practices, suggest-best-practice, explain-best-practice]
---

# Learn Grimoire

Orient a new or existing user on what grimoire is, why it exists, its core concepts, and how to actually use it day to day.

## Why This Is Best Practice

**Adopted by:** Structured tool onboarding — why it exists, then core concepts, then a first real task, in that order — is standard practice in developer-tool adoption design, documented in Stripe's and GitHub's own developer-onboarding writing. Leading with purpose before mechanics is the consistent pattern across CLI tools with high sustained adoption.
**Impact:** Developer tools that lead new users with a clear "why does this exist" step before mechanics see measurably higher sustained usage than tools that start users directly on commands — a consistent finding in developer-tool adoption research. A user who installs a tool but never understands why it exists or how its pieces fit together tends to under-use it, or abandon it for the familiar default (here, ad hoc prompting) even after installing it.
**Why best:** Starting a new user directly on mechanics (command syntax, file formats) without first establishing why the tool exists produces surface-level compliance without genuine adoption — the user can follow a command but doesn't know when to reach for the tool unprompted. Orientation on purpose and mental model first, followed immediately by a first real task, is what converts installation into actual habitual use.

Sources: Stripe and GitHub developer-onboarding design documentation; grimoire's own STANDARD.md and README.md

## Steps

### Step 1: What grimoire is, in one paragraph

State plainly: grimoire is a package manager and curated, peer-reviewed library of best-practice skills for AI assistants, working across many agents (Claude Code, GitHub Copilot CLI, Gemini CLI, and others), organized into domains → subdomains → individual skills.

### Step 2: Why it exists

Most people solving a problem don't know which expert standard governs it, and an AI that knows the standard won't reliably enforce it without an explicit trigger. A grimoire skill is exactly that trigger plus the correct steps, drawn from a verified source rather than improvised on the spot. Contrast this with ad hoc prompting: consistent and peer-reviewed instead of reinvented each session, and portable across projects and agents instead of trapped in one conversation's context.

### Step 3: Core concepts, briefly

Cover, in one or two sentences each: the domain → subdomain → skill hierarchy; the `SKILL.md` format (a trigger description plus structured steps); the meta layer this skill lives in, which routes problems automatically (`suggest-best-practice`), sequences multi-skill problems (`plan-best-practice-solution`), recursively decomposes opaque ones (`apply-best-practice-tree`), and lets the user pin durable preferences (`pin-best-practice-preference`) or activate a named profile (`apply-best-practice-profile`); and CI-level enforcement of declared practices via `grimoire check`/`grimoire validate`.

### Step 4: How to actually use it day to day

Describe a real problem in plain language and let routing happen automatically — don't ask the user to memorize every meta-skill name. Mention: browsing a domain proactively before hitting a problem (`discover-best-practices`); checking existing work for gaps (`review-best-practice-fit`, `audit-applied-best-practices`, `check-best-practice-compliance`); and pinning a preference once a favorite practice emerges so it applies automatically next time.

### Step 5: First real task

Close by inviting the user to bring one real, current problem right now, rather than stopping at explanation — a first real task cements usage far more than reading about the system alone. If the user wants to go deeper on retaining a specific practice afterward, hand off to `learn-best-practice`.

## Rules

- Prioritize why and what before drilling into every meta-skill name — don't produce an exhaustive skill catalog dump.
- Always end by inviting a first real task — don't stop at explanation.
- Don't re-derive grimoire's purpose from scratch each time — the framing (trigger + verified steps an AI won't enforce unprompted) is the project's own stated purpose, not an invented pitch.
- Search the internet to verify a claim about grimoire's current capabilities or supported agents when uncertain or the topic is recent — don't rely solely on training-data recall. If no internet-access tool is available, say so and proceed on best available knowledge, flagged as unverified. After searching, state what was found before proceeding, and keep queries general and factual.

## Examples

**New user, first contact:** A user installs grimoire and asks "what even is this?" The skill explains grimoire in one paragraph, gives the why (an AI that knows expert standards won't enforce them without a trigger), briefly covers the domain/skill hierarchy and the meta-skill layer, then invites: "Bring me a real problem you're working on right now and I'll show you how routing works."

**Existing user who's been using it blind:** A user has been running grimoire for weeks but says "I don't really get how the different meta skills fit together." The skill skips the "what is grimoire" basics (already known) and focuses on Step 3's core-concepts map and Step 4's day-to-day usage patterns, then still closes with a first-task invitation to cement the newly clarified mental model.

## Common Mistakes

- **Listing every meta skill by name** — overwhelms a new user; cover the why and the core concepts, then let discovery happen through real use.
- **Starting with mechanics instead of purpose** — a user who learns install commands before understanding why grimoire exists tends to under-use it later.
- **Stopping at explanation** — orientation without a first real task produces a user who understands grimoire in the abstract but never actually reaches for it.
- **Re-litigating grimoire's purpose from first principles** — use the project's own stated purpose (STANDARD.md, README.md) rather than improvising a different pitch each time.

## When NOT to Use

- The user wants durable, testable retention of one specific installed practice — use `learn-best-practice` instead.
- The user wants to understand why one specific practice works (mechanism, evidence, failure modes) — use `explain-best-practice` instead.
- The user already has a real problem in hand and just wants it solved — use `suggest-best-practice` instead; orientation isn't needed first.
