---
name: customer-discovery
description: Plan customer discovery — define target profile, build prospect list, draft interview script, set up outreach + scheduling logistics.
---

# Customer Discovery

## When you activate
User has a sharpened problem hypothesis and is ready to talk to humans. They ask: "how do I find people to interview?", "help me plan customer discovery for X", "draft outreach for Y".

## What you produce
A discovery plan saved to `products/<name>/interviews/discovery-plan.md`:

```
## Discovery Plan — <product/idea>

### Target profile (be precise)
- Role / title: <specific>
- Company / context: <specific>
- Team size: <range>
- Seniority: <IC / manager / VP / C-suite>
- Acuteness signal: <how to tell they have this problem badly>

### Where they congregate (top 5 reachable channels)
1. <community / forum / LinkedIn group / Slack workspace> — URL
2. ...

### Prospect list strategy
- How to source: <Apollo / LinkedIn Sales Nav / scrape X / cold from Reddit threads>
- Initial batch size: 50–80
- Outreach format: <DM / email / cold call / community post>

### Interview script (15-min default)
1. **Warm-up** (2 min): "Tell me about your role and a typical week."
2. **Past-behavior probe** (5 min): "Tell me about the last time you dealt with <problem>. Walk me through it."
3. **Current solution** (3 min): "What did you try? What worked? What didn't?"
4. **Workaround cost** (2 min): "How much time/money does this currently cost you?"
5. **Magic wand** (2 min): "If you could wave a wand, how would this look?"
6. **Close** (1 min): "Who else has this problem? Mind connecting me?"

### Don't ask (Mom Test violations to strike out)
- ❌ "Would you use a product that does X?"
- ❌ "Would you pay $Y for this?"
- ❌ "Do you think this is a good idea?"
- All future-hypothetical questions.

### After every 5 interviews
Run `agents/idea/interview-synthesizer/` on the batch.
```

## Protocol
1. Read the sharpened hypothesis from `problem-sharpener` output (or ask user for it).
2. Read `knowledge-base/idea-stage/mom-test.md`.
3. Build the profile. Be ruthlessly specific.
4. Suggest reachable channels (with URLs, not categories).
5. Generate the script. Critique each question against Mom Test rules.
6. Optionally draft 2 outreach variants: cold DM (≤ 4 sentences) and warm-intro request (≤ 6 sentences). Save in `products/<name>/interviews/outreach-templates.md`.

## Sources
- `knowledge-base/idea-stage/mom-test.md`
- `knowledge-base/launch-stage/cold-outreach-templates.md` (just the structure)

## What you don't do
- Don't draft an interview script with future-hypothetical questions. Mom Test rules are non-negotiable.
- Don't build a prospect list yourself — give Hamza the sourcing strategy + tools; he runs it (Apollo, scraping, etc.).
- Don't promise "you'll know after 5 interviews" — emphasize the discipline of running the synthesizer in batches.
