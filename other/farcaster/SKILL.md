---
name: farcaster
description: Read Farcaster - any profile, cast, or thread - keyless and free. Use before any claim about a Farcaster person, project or conversation.
---

# farcaster - read the network before you talk about it

Zaal, 2026-08-07: "add that as an often used skill for farcaster knowledge."

Farcaster is where ZAO's community actually is, so a claim about a person, a
project, or what someone said should come from the network - not from memory, and
not from a guess at a bio. This makes that a ten-second move.

## The one command

```bash
~/bin/zao-fetch-farcaster.sh <url-or-handle-or-fid>
```

Accepted inputs, all verified working 2026-08-07:

| Input | Returns |
|---|---|
| `https://farcaster.xyz/<handle>` | profile, bio, FID, recent casts |
| `https://farcaster.xyz/<handle>/<0xshorthash>` | that single cast |
| `warpcast.com/...` | same shapes |
| a bare FID (`8004`) | profile + recent casts |

No API key. No Neynar. It reads **Haatz** (`haatz.quilibrium.com`), a free public
Snapchain hub mirror running the standard Farcaster hub HTTP API.

## Use it when

- Anyone names a Farcaster handle and you are about to say who they are
- Before drafting outreach - read what they actually post first
  (`feedback_not_botty_zaal_voice`: check warm-vs-cold before reaching out)
- Researching a project that lives on Farcaster
- Verifying a claim someone made about a cast or a thread

## Do NOT

- **Do not guess a bio or a follower count.** Fetch it. Every number in a ZAO doc
  traces to a measurement (`anti-fabrication.md` rule 5), and a Farcaster bio is
  one fetch away.
- **Do not reach for Neynar first.** Neynar needs a key and a budget; this needs
  neither and answers the same read questions. Neynar is for WRITES and for
  things the hub cannot answer.
- **Do not post, reply, follow or like from a research task.** Reading is free
  and safe; anything outbound is gated on Zaal's explicit yes, every time.

## Worked example, 2026-08-07

Zaal sent `farcaster.xyz/ahn.eth` and asked about GM Farcaster. Four fetches, no
key, about a minute:

```
ahn.eth      -> justin, FID 8004. "building /quidli, casting /justinahn,
                daoing /orange-dao & /purple"
gmfarcaster  -> FID 273384. "29 minutes of Farcaster news to start your day
                with your hosts @adrienne & @nounishprof" - gmfarcaster.com
adrienne     -> FID 5818. Co-founder of /gmfarcaster, "Farcaster's #1 news
                show". Also co-founder Tenger Ways. Engineer. Runs /word-a-day.
nounishprof  -> FID 4167. "building /gmfarcaster network | blockchain ENT prof"
```

That is the difference between "GM Farcaster is a Farcaster news thing, I think"
and knowing both hosts, both FIDs, and that one of them has already spoken with
Zaal (the Nounish Prof x Sparkz brainstorm, 2026-07-22).

## Honest limits

- **Reads only.** Writing a cast goes through zaalcaster or ZOE's publish path,
  both of which require a signer and Zaal's confirmation.
- **Hub data, not enriched data.** Follower counts and "power badge" style fields
  come from Neynar's index, not the hub - if you need those, say so and use
  Neynar deliberately rather than pretending the hub gave them to you.
- **The mirror can move.** If Haatz stops answering, the fallback ladder is in
  `[[project_farcaster_fetch_haatz]]`; do not silently switch to a paid API
  without saying the free one broke.
- **There is no GM Farcaster API.** Checked 2026-08-07: `gmfarcaster.com/api`
  returns 404. Their show is on the network and on gmfarcaster.com; read it the
  same way as anything else.

## Siblings

Completes the keyless-fetch trio, all three verified and all three preferred over
paid or authenticated paths for READS:

- **Farcaster** - this skill, via Haatz
- **Reddit** - `~/bin/zao-fetch-reddit.sh` via arctic_shift
  (`[[project_reddit_fetch_oauth_fix]]`)
- **X** - FxTwitter (`[[project_x_fetch_fxtwitter]]`)

Source: `[[project_farcaster_fetch_haatz]]`, doc 823.
