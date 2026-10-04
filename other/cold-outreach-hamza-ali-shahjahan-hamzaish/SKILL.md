---
name: cold-outreach
description: First 100 customers by hand. Sourcing → personalized cold messages → follow-up cadence → tracking. Volume × signal, not spam.
model_tier: sonnet
---

# Cold Outreach

## When you activate
User asks: "first 100 customers", "cold outreach for X", "how do I get users for Y?", "draft outreach to <segment>"

## What you produce
- A prospect list spec at `products/<name>/launch/prospects-strategy.md`
- Outreach templates at `products/<name>/launch/outreach/<segment>-<variant>.md`
- A tracking sheet spec (columns to use in airtable/notion/google sheet)

## Outreach principles
1. **Personalization is the moat.** A line that proves you read their LinkedIn beats any clever copy.
2. **Short.** Under 75 words for cold email. Under 50 words for LinkedIn DM.
3. **One ask.** "Got 10 minutes this week?" — not "would you like to demo / try the tool / give feedback / be on our advisory board?"
4. **No links above the ask.** Links trigger spam filters.
5. **Plain text. No signature graphics.** From a real human address (not noreply).

## Templates
Saved in `products/<name>/launch/outreach/`:

### Cold email — discovery (pre-PMF)
```
Subject: <pain> question

Hi <name>,

<1 sentence proving you've seen their work — specific>.

I'm researching how <role> handle <specific problem>. Not selling anything — just learning.

Got 15 minutes this week? Happy to share what I find at the end.

— <your name>
```

### Cold DM — LinkedIn — discovery
```
Hi <name> — saw your post on <specific topic>. Curious how you currently handle <related pain>? Doing user research, would love to chat for 10min if you're open.
```

### Cold email — early customer (post-prototype)
```
Subject: <outcome verb> for <segment>

Hi <name>,

<1-sentence relevance>.

I built <product>: <one-liner>. Few <segment> are using it now, getting <specific outcome>.

Worth 10 min? I'd love feedback even if you're not the right fit.

— <name>
```

### Follow-up #1 (T+4 days)
```
Hi <name> — bumping this in case it got lost. Even a "no thanks" helps me prioritize. Thanks either way.
```

### Follow-up #2 (T+10 days, breakup email)
```
Hi <name> — last one from me. If this isn't relevant, no worries. If it is, I'm easy to find.
```

After two follow-ups: stop. Don't add to a nurture sequence.

## Sourcing strategy (per segment)
| Source | Best for | Tool / how |
|---|---|---|
| LinkedIn Sales Nav | B2B roles | $80/mo, worth it for first 100 |
| Apollo | B2B contact info | freemium, 50 free credits/mo |
| GitHub | devs / OSS users | search by topic + recent commits |
| Twitter/X search | indie hackers, niche communities | use lists of users by topic |
| Substack | newsletter writers in a vertical | comment + DM |
| Subreddit search | consumers + niche pros | post a question, then DM responders |
| IndieHackers profiles | indie founders | filter by interests + revenue |

## Cadence rules
- 25 cold messages per day, max. Quality over volume.
- Track every send: date, channel, response (yes / no / no reply / negative).
- Test ONE variable at a time (subject line, opener, ask).
- Stop after 100 sends if response rate < 5% — fix the message or the audience, don't grind through.

## Sources
- `factory/playbooks/launch-stage/cold-outreach-templates.md`
- `factory/playbooks/launch-stage/first-100-customers.md`

## What you don't do
- Don't send the same email to 100 people unchanged. That's spam.
- Don't use "Hope this finds you well" or any other vacant opener.
- Don't include calendar links in cold email #1. Get the yes first.
