---
name: brand-voice
description: "Fires on any written output — emails, outreach, LinkedIn posts, business cases, follow-ups. Provides: voice rules, email formatting, vocabulary substitutions, banned phrases, sign-off, and 7-point voice check. Output contract: all written content matches the user's calibrated tone and style."
user-invocable: false
---

# Brand Voice — Communication Style Skill

> **Tier 3 — This entire file is regenerated during deep personalization Phase 4 based on the AE's communication preferences and writing samples.**

## Purpose

Defines the AE's personal communication voice for all written outputs. Contains voice rules, email formatting standards, vocabulary substitutions, banned phrases, and the 7-point voice check. Ensures every email, outreach, LinkedIn post, and follow-up sounds like the AE — not like generic AI.

## When Referenced

- **Writing emails to existing contacts** (write-email intent) — applies voice rules to contextual emails and follow-ups
- **Drafting prospecting outreach** (write-email intent, new relationship) — applies voice rules to cold and warm outreach emails
- **Creating LinkedIn content** (write-post intent) — applies voice rules to posts and thought leadership
- **Processing calls** (process-call intent) — applies voice rules to the follow-up email generated in Output 4
- **Building executive business cases** (build-case intent) — applies voice tone to POV documents and presentations

## Core Framework

### Voice Rules

**Communication style:** {{COMMUNICATION_STYLE}}

**Default voice (before deep personalization):**
- Direct and professional. No corporate fluff.
- Short sentences. Active voice. Say what you mean.
- Confident but not arrogant. Helpful but not subservient.
- Match formality to the relationship — warm with champions, professional with economic buyers, concise with technical evaluators.

*After deep personalization, these rules are rewritten based on the AE's actual communication preferences and writing samples.*

### Email Formatting

| Rule | Standard |
|------|----------|
| **Subject lines** | Lowercase unless proper nouns. Under 6 words. Specific, not clickbait. |
| **Length** | Under 200 words. If it's longer, it should be a document, not an email. |
| **Structure** | Context (1 sentence) → Purpose (1-2 sentences) → Ask (1 sentence) |
| **Sign-off** | {{EMAIL_SIGN_OFF}} |
| **Tone** | Varies by recipient — see Tone Matching below |
| **CTA** | One clear call-to-action per email. Never more than one. |

### Tone Matching

Match communication tone to the recipient's role and relationship:

| Audience | Tone | Example |
|----------|------|---------|
| **Champion** | Warm, collaborative, insider language | "Hey Sarah — quick update on the POC timeline..." |
| **Economic Buyer** | Professional, business-outcome focused | "Following up on our conversation about the projected ROI..." |
| **Technical Evaluator** | Concise, specific, data-driven | "Here are the integration specs you requested..." |
| **New Contact** | Respectful, value-first, no assumptions | "Reaching out because I noticed [specific observation]..." |
| **Internal (manager)** | Structured, metrics-focused, brief | "Pipeline update: 3 deals moved this week..." |

### Vocabulary Substitutions (10+ required)

*After deep personalization, this section contains the AE's specific vocabulary preferences.*

**Default substitutions (before deep personalization):**

| Instead of | Use |
|-----------|-----|
| "Reach out" | "Contact" or "get in touch" |
| "Circle back" | "Follow up" or "revisit" |
| "Touch base" | "Connect" or "check in" |
| "Synergy" | [delete — don't replace, just remove] |
| "Leverage" | "Use" or "apply" |
| "Bandwidth" | "Capacity" or "time" |
| "Deep dive" | "Detailed review" or "analysis" |
| "Ping" | "Message" or "email" |
| "Loop in" | "Include" or "add" |
| "Take offline" | "Discuss separately" |
| "Ideate" | "Brainstorm" or "think through" |
| "Socialize" | "Share" or "discuss" |

### Banned Phrases

These phrases are NEVER used in any communication, regardless of context:

**Default banned list (before deep personalization):**
- "Just checking in"
- "Per my last email"
- "Hope you're doing well"
- "Wanted to follow up"
- "At the end of the day"
- "Low-hanging fruit"
- "Move the needle"
- "I hope this email finds you well"
- "I wanted to reach out"
- "As per our conversation"

*After deep personalization, this list is customized with the AE's personal banned phrases and may add phrases they never want AI to generate.*

### 7-Point Voice Check

Run this check on every communication output before presenting:

| # | Check | Question |
|---|-------|----------|
| 1 | **Authenticity** | Does this sound like {{AE_NAME}} wrote it, or like a robot? |
| 2 | **Vocabulary** | Are all vocabulary substitutions applied? No banned phrases? |
| 3 | **Length** | Is the email under 200 words? Is the LinkedIn post 150-300 words? |
| 4 | **Structure** | One clear purpose? One clear CTA? |
| 5 | **Tone match** | Is the tone appropriate for the recipient and relationship? |
| 6 | **Sign-off** | Using {{EMAIL_SIGN_OFF}} (or appropriate LinkedIn close)? |
| 7 | **Filler check** | Zero filler phrases? No "I hope," "just wanted to," "I'd love to"? |

**Passing score:** 7/7 for emails and outreach. 5/7 acceptable for LinkedIn posts (length and sign-off rules differ).

### LinkedIn Voice (Specific)

LinkedIn voice differs from email voice:
- More conversational than email
- First-person is fine (and encouraged for Personal posts)
- Can be more opinionated
- Can use incomplete sentences for emphasis
- Emojis: sparingly, never more than 2 per post (unless AE prefers differently)
- Hashtags: 3-5 at the end, never in the body

## Personalization Notes

- **This entire file is Tier 3** — fully regenerated during deep personalization Phase 4 (Brand Voice)
- Deep personalization captures: communication samples, vocabulary preferences, banned phrases, sign-off, and style preferences
- Voice rules are built from actual writing samples the AE provides during deep personalization
- Vocabulary substitutions list grows over time as the AE identifies more words they don't use
- The 7-point voice check is structurally universal but the specific checks reference personalized content

### First-Use Calibration Storage (Outreach)

On the first run of outreach, the user is asked for their typical email tone and optionally provides a sample email. The calibration response is stored here as supplemental voice data:

- **Outreach tone notes:** [Populated on first outreach run — natural email tone observations, sample email analysis]
- **Outreach-specific adjustments:** [Any voice rules specific to prospecting emails vs. internal/existing-relationship emails]

This supplements the deep personalization voice profile. If outreach runs before deep personalization, calibration data is stored here and merged into the full voice profile when deep personalization completes.
