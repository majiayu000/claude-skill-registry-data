---
name: tweet-crafter
description: |
  Craft tweets, threads, and long-form X posts optimized for the January 2026 algorithm.
  Use when creating individual posts for X/Twitter, adapting newsletter content for X,
  writing thread hooks, or optimizing post format (thread vs long-form). Includes current
  algorithm signals, Premium features, and Spanish-language patterns for LATAM audiences.
---

# Tweet Crafter Skill

## Algorithm Signals (January 2026)

| Signal | Weight | Notes |
|--------|--------|-------|
| First 30 min engagement | Critical | Make or break for distribution |
| Replies | Very High | 2x value of retweets |
| Reposts | High | Network expansion |
| Quotes | High | Conversation starter, shown to both audiences |
| Likes | Medium | Weakest engagement signal |
| Premium status | Modifier | 4x in-network, 2x out-of-network |
| Video | Very High | 5x engagement vs text (0.42% vs 0.08%) |
| Dwell time | High | Time spent reading > quick interactions |
| External links | Penalty | Zero median engagement for non-Premium (March 2026) |

**Key insight**: Focus on prompting replies and conversations, not likes. The algorithm heavily rewards content that generates discussion.

### 2026 Platform Changes
- Video content dominates X (~80% of user sessions)
- External links severely penalized for non-Premium accounts
- Unverified accounts need ~10x more engagement for same reach
- Threads now underperform long-form articles

## Format Selection

```
Long-form (preferred): Tutorials, essays, deep analysis, "X cosas que aprendí", narratives
Thread: Only when content naturally breaks into discrete numbered points

Performance benchmark:
- Long-form articles: Higher engagement, better reach, preferred by algorithm
- Threads: Lower performance, use sparingly for variety
```

**Default to long-form articles.** Threads are no longer the go-to format for educational content. Long-form articles consistently outperform threads on reach and engagement.

## Link Posts (NEW — October 2025)

Links are no longer penalized. New in-app browser keeps engagement buttons visible.

**Requirements for link posts:**
- Write a compelling standalone caption (not just "new post")
- Include interesting description or insight
- Add image when possible (150%+ engagement boost)

Per Elon: "posting a link with almost no description will get weak distribution"

## Content Templates

### Single Tweet (max 280 chars)

```
[Hook/insight/question]

[Optional: 1-2 supporting lines]

[Optional: 1 hashtag max]
```

### Thread Format (Use Sparingly)

```
1/🧵 [Standalone hook that works even without thread]

2/ [First point — strongest insight]

3-N/ [Supporting points]

N/ [CTA: follow, RT first tweet, link to newsletter]
```

Thread rules:
- 5-15 tweets optimal
- Self-reply immediately after posting (signals thread to algorithm)
- Hook must work standalone — most people only see tweet 1
- **Consider converting to long-form article instead** — better performance

### Long-Form Post (Premium)

```
[First 280 chars: Hook that appears in timeline — CRITICAL]

[Body: Up to 25,000 chars with bold/italic formatting]

[CTA at end]
```

Only first 280 characters show in timeline. Front-load the hook.

## Media Guidelines

| Type | Engagement Multiplier |
|------|----------------------|
| Video (native, <2:20) | 10x |
| Images | 2-3x |
| Polls | High engagement |
| Plain text | Baseline |

Video specs: Native upload, under 2:20, no external watermarks.

## Hook Formulas

The first line determines everything. Use these proven patterns:

**Curiosity:**
- "I used to think [common belief]..."
- "Here's what nobody tells you about [topic]..."
- "Everyone's doing [X] wrong. Here's why:"

**Value-Forward:**
- "5 ways to [achieve result]:"
- "The framework I use for [task]:"
- "[Number] tools that changed how I [outcome]:"

**Story:**
- "Last week, something unexpected happened..."
- "3 years ago, I made a decision that..."
- "I almost quit [X]. Then I discovered..."

**Data/Surprise:**
- "[Surprising statistic] — here's why it matters."
- "I analyzed [X] and found something interesting:"

**Spanish Hooks:**
- "[Número] cosas que aprendí sobre [tema]:"
- "El error más común en [tema]:"
- "Nadie te dice esto sobre [tema]:"

## Pre-Publish Checklist

Before posting, verify:

- [ ] Hook is in first 280 characters (critical for timeline preview)
- [ ] Content invites replies (questions, opinions, hot takes)
- [ ] 0-2 hashtags maximum
- [ ] Media attached if applicable (video = 5x engagement)
- [ ] No external links unless Premium (or put link in reply)
- [ ] Would I engage with this if I saw it?
- [ ] Posted during optimal hours (9-11 AM or 7-9 PM PST)

## Spanish-Language Patterns

### Thread Templates

**Tutorial Thread:**
```
1/🧵 Cómo [accomplish task] en [technology]:

Una guía paso a paso 👇

2/ Paso 1: [Action]
[Explanation]

...

N/ Eso es todo.

Guarda este hilo para cuando lo necesites.
Sígueme @tacosdedatos para más tutoriales en español.
```

**Insights Thread:**
```
1/🧵 [Number] cosas que aprendí sobre [topic] después de [experience]:

Un hilo corto 👇

2/ [Insight #1]
[Brief explanation]

...

N/ Si te fue útil:
• Sígueme para más contenido de [topic]
• RT el primer tweet para que llegue a más personas
```

### Newsletter Promotion

```
[Insight or hook from the newsletter]

Esto y más en el nuevo tacosdedatos:
[Link]

[Optional: What else is in the issue]
```

## Hashtag Strategy

- Maximum 1-2 hashtags (X algorithm doesn't favor heavy usage)
- Spanish hashtags for discoverability: #DataScience #Python #DatosAbiertos
- Skip hashtags entirely for conversational posts

## Timing

- Best times: 9-11 AM, 7-9 PM (PST)
- Best days: Tuesday-Thursday
- Post when followers are online (check analytics)

## Output Format

When crafting tweets, provide:

```markdown
## Tweet/Thread: [Topic]

### Content
[Full post content]

### Format
- **Type**: Single tweet / Thread (X tweets) / Long-form
- **Character count**: X/280 (or full length for long-form)
- **Media needed**: [Image description / Video spec / None]

### Algorithm Notes
- Hook strength: [Strong/Medium/Weak]
- Suggested posting time: [Day, Time]
```

## References

For deep algorithm research and source links, see [references/REFERENCES.md](references/REFERENCES.md).
