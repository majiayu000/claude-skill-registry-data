---
name: newsletter
description: "Writes a personal founder newsletter issue in the user's own voice (learned from 3 to 5 of their past issues): a real firsthand scene first, one lesson, one thing readers can use today, one call to action. Also generates a deduplicated, ranked idea bank and, optionally, audits past issues' open and click data correctly. Use when someone asks to write this week's newsletter, turn a story or brain dump into an issue, fix a draft that sounds like AI, or come up with newsletter ideas. Works with any email platform; drafts only, never sends or schedules."
---

# Newsletter

A personal email that happens to contain value, not a blog post or a framework dump.

By Johann (@johannships). Built from editing my own weekly issues and auditing every sent issue's opens and clicks.

## Step 0: learn the voice (first run, then reuse)

Ask for **3 to 5 past issues** the user is proud of (paste, files, or the public archive URL). Write `voice.md` next to this file:
- greeting and sign-off (copy them exactly; they repeat every issue)
- capitalisation, paragraph length, header style
- words and shorthand they use; words they never use
- how they move from story to lesson (quote 2 real transition lines)
- CTA style and where it sits

Show it once, apply corrections, reuse after. No samples: use the defaults below and label the draft "default voice".

## Inputs

- **Raw material** (required): a brain dump, voice-note transcript, a story, or "what happened this week". If you only have a topic or an itinerary, stop and ask for one short messy note: what happened, what surprised you, what you got wrong. Ask before writing a full draft, not after it is rejected.
- **The one job of this issue**: replies, a community join, a booked call, a download. One primary CTA. Ask if not given.
- **Links** for the CTA and any resource. Keep missing ones as literal placeholders like `[COMMUNITY LINK]`. Never invent a URL.
- Optional: the archive URL, for dedupe.

## Structure

1. **Subject**: lowercase-friendly, 3 to 7 words, sells the story ("i left the country. my AI ran my business."). Not "How I Achieved Success Through Strategic Planning".
2. **Preview line**: promises the concrete payoff ("hint: it's not about the money").
3. **Greeting + scene**: open inside a real moment. What you were doing, what you saw, what surprised you.
4. **One lesson** the story earns. 2 to 3 sentences.
5. **The useful part**: a method, checklist, prompt or exercise they can use today, written conversationally. Bullets are fine; a five-part numbered framework usually reads like a content marketer.
6. **What you're building / where you're headed**: 2 to 3 short paragraphs, optional.
7. **One CTA**, after the value. A free resource is value, not a CTA: give it before the ask.
8. **Sign-off**: same structure every issue (from voice.md).

`[image placeholder: what photo]` only where a real photo would help.

Paragraphs 1 to 3 sentences, often 1. Lots of whitespace. Short `###` headers.

## Voice rules

- **Substitution test**: if another founder could send the body unchanged except for city, company and tool names, it is not personal enough. Get a real detail from the user.
- **Conservation mode**: when the user hands you rough copy and says it is more in their voice, keep their words, claim order, fragments, asides and closing thesis. Fix typos, grammar, repetition and transitions only. No polished new opener, no tidy moral, no expansion after they asked for shorter.
- Prefer their plain question ("how do you add AI to your business when it changes daily?") over consultant language ("navigating an evolving landscape").
- Never invent feelings, self-deprecation or "lol" to sound casual.
- Never: em dashes, "here's the thing", "let that sink in", "unlock", "game changer", "deep dive", "level up", "→ try it:" after every section.
- No private finances, client names or deal mechanics unless the user confirms they are public.

## Example (default voice, excerpt)

```
subject: i stopped building software
preview: not because it doesn't work

hey friends,

i stopped building saas.

not because it doesn't work. it does.

[scene: the moment you decided]

### the one thing that made the difference

[lesson in 2 to 3 sentences]

paste that into Claude. say "build me a system that handles this." you'll be surprised how fast you have a working version.
```

## Mode: ideas

1. Dedupe first: read the public archive (all pages) and any drafts the user shares. Compare scene, lesson, asset and CTA, not just titles. If the archive is unreachable, say so.
2. Return the number asked for (default 10), genuinely distinct. For each: subject, preview, opening scene, reader takeaway, practical asset, the one CTA, one sentence on why it should convert.
3. Rank them and name the strongest overall and the strongest for the issue's job.
4. When the user says one is a duplicate, replace it in the same reply.

Prefer an honest experiment ("here's the setup and the scorecard, results next issue") over invented success.

## Mode: performance audit (optional)

Only when asked "what's working" and the user can export per-issue stats (any platform's CSV or API). Follow `references/engagement-audit.md`. Read-only: never create, schedule or send anything in the platform.

## Output

The full issue in one fenced `markdown` block (subject, preview, body, CTA, sign-off) so formatting survives a paste. Commentary outside the block, 3 lines max. If a claim needs checking, put `internal note (remove before sending): ...` above the block.

## Checklist before handing over

- [ ] Real scene comes before any framework
- [ ] Passes the substitution test
- [ ] Exactly one primary CTA; resources come before it
- [ ] Every number traces to the user's material
- [ ] No em dashes, no banned phrases (search the text, do not eyeball)
- [ ] Subject and preview each do a different job
- [ ] Would the user actually send this? If it sounds generated, rewrite.

## Feedback log

Append corrections and issue results to `feedback.md` (date, issue, what changed, rule going forward). Read it first next time.
