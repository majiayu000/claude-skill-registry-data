---
name: "x-twitter-recruiting-sourcing"
description: "Source candidates on X (formerly Twitter) using Advanced Search operators, Boolean strings, and X-Ray search. Use when building X search strings, finding passive candidates on X, searching by role or skill or location, monitoring transition signals, or researching candidate profiles on X."
---

# X (Twitter) Recruiting & Sourcing Skill

You are an expert at talent sourcing on X. Your primary focus is building precise X Advanced Search strings and identifying passive candidates through search. Apply these workflows whenever the user needs to find or research candidates on X.

---

## X Advanced Search — How It Works

Go to `x.com/search-advanced` or use `x.com/search` with operators inline.

X Advanced Search does **not** support full Boolean logic like LinkedIn. It uses separate fields:
- **All of these words** → AND logic
- **This exact phrase** → phrase match
- **Any of these words** → OR logic
- **None of these words** → NOT / exclusions
- **From these accounts** → `from:username`
- **To these accounts** → `to:username`
- **Mentioning these accounts** → `@username`
- **Near this place** → geographic radius (limited accuracy)
- **From this date / To this date** → date range

For inline search (search bar), combine operators in a single string.

---

## Core Search Operators

| Operator | What it does | Example |
|---|---|---|
| `"quotes"` | Exact phrase | `"machine learning engineer"` |
| `OR` | Either term | `engineer OR developer` |
| `-` (minus) | Exclude term | `-recruiter -hiring` |
| `from:` | Posts by a specific account | `from:username` |
| `to:` | Posts replying to an account | `to:username` |
| `@` | Mentions of an account | `@company` |
| `min_faves:` | Minimum likes (filters noise) | `min_faves:10` |
| `min_retweets:` | Minimum retweets | `min_retweets:5` |
| `since:` | Posts after date (YYYY-MM-DD) | `since:2025-01-01` |
| `until:` | Posts before date | `until:2025-12-31` |
| `lang:` | Language filter | `lang:en` |
| `filter:links` | Posts containing links | `"portfolio" filter:links` |
| `-filter:retweets` | Exclude retweets (original posts only) | `-filter:retweets` |

---

## Search Strings by Signal Type

### Open to Work / Active Seekers
```
"open to work" "software engineer" -recruiter -hiring -job
"looking for my next" engineer -recruiter
"open to opportunities" (engineer OR developer OR designer) lang:en -filter:retweets
"would love to hear" (engineer OR PM OR designer) "opportunities" -recruiter
"anyone hiring" engineer -"we're hiring" min_faves:3
```

### Transition Signals (just left / about to move)
```
"my last day at" -filter:retweets lang:en since:2025-01-01
"just left" (Google OR Meta OR Stripe OR OpenAI OR Shopify) -filter:retweets
"after X years" "leaving" -filter:retweets since:2025-01-01
"excited to share" "leaving" engineer -filter:retweets
"time for something new" (engineer OR designer OR PM) -filter:retweets
"officially my last week" -filter:retweets lang:en
```

### Building in Public (active practitioners — strong signal of real skill)
```
"just shipped" (Python OR Go OR Rust OR TypeScript) -filter:retweets min_faves:5
"just deployed" (ML OR "machine learning" OR API) -filter:retweets
"wrote a thread on" ("distributed systems" OR "system design" OR "ML") min_faves:10
"open sourced" (Python OR Rust OR Go) -filter:retweets since:2025-01-01
"launched" "product" -filter:retweets min_faves:20 lang:en
```

### Role-Specific Search Strings

**Software Engineer (Backend):**
```
("backend engineer" OR "software engineer") (Python OR Go OR Rust) "open to" -recruiter -hiring lang:en -filter:retweets
```

**ML / AI Engineer:**
```
("ML engineer" OR "machine learning" OR "AI engineer") "looking" OR "open to" (PyTorch OR TensorFlow OR "fine-tuning") -recruiter -filter:retweets lang:en min_faves:3
```

**Product Designer / UX:**
```
("product designer" OR "UX designer") ("open to" OR "looking for") Figma -recruiter -hiring -filter:retweets lang:en
```

**Product Manager:**
```
("product manager" OR "PM") ("open to" OR "looking for my next") (B2B OR SaaS OR fintech) -recruiter -filter:retweets lang:en
```

**DevRel / Developer Advocate:**
```
("developer advocate" OR "DevRel" OR "developer relations") ("open to" OR "looking") -recruiter -filter:retweets lang:en
```

**Data Scientist:**
```
("data scientist" OR "data science") (Python OR SQL OR "machine learning") "open to" -recruiter -hiring -filter:retweets lang:en
```

### Company Alumni Sourcing
```
"just left [CompanyName]" -filter:retweets since:2025-01-01
"after [X] years at [CompanyName]" -filter:retweets
"my time at [CompanyName]" (leaving OR left OR next) -filter:retweets
```

### Location-Based Search
```
"London" ("software engineer" OR "backend engineer") "open to" -recruiter lang:en -filter:retweets
"San Francisco" OR "SF" ("ML engineer" OR "AI") "looking" -recruiter -filter:retweets
"remote" ("product designer" OR "UX") "open to work" -recruiter -filter:retweets lang:en
```

---

## Google X-Ray for X Profiles

When X's own search is too limited, use Google to search X profiles directly:

```bash
# Profile bio search
site:x.com "software engineer" "machine learning" "open to work"
site:twitter.com "product designer" "Figma" "available"

# Role + location
site:x.com "backend engineer" "London" "Python"
site:twitter.com "ML engineer" "San Francisco" "open to"

# Skill-specific practitioners
site:x.com "Rust" "open source" "systems programming"
site:twitter.com "growth" "product" "YC" OR "Y Combinator"

# Exclude noise
site:x.com "UX designer" "open to" -recruiter -jobs -hiring
```

---

## Profile Research — Reading Signal from X Activity

Once you find a candidate profile, assess in this order:

1. **Bio** — title, skills, location, "open to" signals, links to GitHub/portfolio
2. **Pinned post** — often their best work or a career announcement
3. **Recent posts (last 30 days)** — are they sharing real work? Complaining about current role? Asking for intros?
4. **Engagement pattern** — do others in the field reply and engage? Signals credibility
5. **Transition indicators** — vague posts about "new chapters," reduced posting frequency at current employer, liking job posts

**Strong positive signals:**
- Sharing code, product thinking, or design work publicly
- Getting substantive replies from respected accounts in the field
- Posting about problems they're solving (not just opinions)
- Bio links to active GitHub, portfolio, or newsletter

**Flags to note:**
- Account inactive for 6+ months (may not respond to DM)
- Only retweets, no original content (hard to assess)
- Bio title doesn't match what they post about

---

## Hashtags to Monitor

| Hashtag | Signal |
|---|---|
| `#opentowork` | Active seeker |
| `#jobsearch` | Active seeker |
| `#buildinpublic` | Active practitioner sharing real work |
| `#layoffs` `#techlayoffs` | Transition pool |
| `#uxdesign` | Design practitioners |
| `#devrel` | Developer relations community |
| `#mlops` `#llm` `#genai` | ML/AI practitioners |
| `#fintech` | Finance/startup operators |
| `#indiehacker` | Builders and founders |

---

## X Lists — Pipeline Management

**Private lists:**
- Create a private list per role (e.g. "Q2 Backend Pipeline") — add candidates as you find them
- Monitor without following publicly
- Check weekly for transition signals

**Public lists (passive signal tool):**
- Add target candidates to a well-named public list (e.g. "Top ML Practitioners")
- Candidates get notified — creates visibility before you DM

---

## DM Outreach

**Warm up first (3-step sequence):**
1. Follow the candidate
2. Reply genuinely to 2–3 posts — add a real observation, not "great post!"
3. DM after a few days once your name is familiar in their notifications

**Cold DM template:**
```
Hey [Name],

Saw your thread on [specific topic] — genuinely useful take on [specific point].

I run recruiting at [Company]. We're building [one-line description] and your
background in [specific skill/area] jumped out at me.

Open to a quick call this week? No pressure.

[Your name]
```

- Only DM if DMs are open
- 3–5 sentences max
- No JD links in first message
