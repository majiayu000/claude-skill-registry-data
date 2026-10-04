---
name: trade-negotiation
description: This skill should be used when the user says "they countered", "how should I respond to their counter", "make a counteroffer", "negotiate this trade", "they said no, what now", "how do I get this deal done", or is mid-conversation with another manager about an offer. Provides counteroffer reasoning - anchoring, concession laddering, framing, and walk-away discipline. Not for the initial verdict on an offer (trade-evaluation), finding a partner from scratch (trade-finder), or sending the final offer in the browser (roster-ops propose-trade).
---

# Trade Negotiation: The Back-and-Forth

Turn a stalled or countered trade into a closed deal — or a clean walk-away. This skill manages the *sequence* of offers; use trade-evaluation for the underlying math whenever a new construction appears.

## Step 1: Establish the negotiation state

Gather: the offer history so far (every version, in order), the current offer on the table, what the other manager has *said* (their words carry their priorities), and both teams' standings. Read `leagues.md` from the project root for the trade deadline, playoff weeks, and trade-review method — the deadline is the clock every negotiation runs on. If the file is missing or those fields are blank, ask for them directly and suggest running the `fantasy-league-setup:league-config` skill to persist the answers. If `leagues.md` defines more than one league, use the one marked `(default)` unless the user names another.

State the advice **as of** a concrete date/time, and refresh any stale injuries, role changes, or deadline context before treating the current counter as live. If an injury update is what moved the price, require **both** the official team/game status and a second credible source before repricing around it.

**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

**This skill is read-only.** Reading a page needs no confirmation, but never click anything that changes a roster, files a claim, or sends an offer from here — that is what the `roster-ops` skills and their confirmation gates exist for.

## Step 2: Set the walk-away before countering

Before drafting any counter, compute (with trade-evaluation logic) the **minimum acceptable version**: the weakest construction the user should still accept, by lineup delta. Write it down in the response. Every counter is then measured against it — this is what prevents "winning the negotiation, losing the trade."

## Step 3: Read the counter

- **What they changed reveals what they value.** If they swapped out one player but kept the structure, they're in — haggling over price. If they restructured entirely, the original framing missed their need; re-diagnose (their deficit may not be what trade-finder assumed).
- **Anchor check**: if their counter is far below the user's opener, don't split the difference — that rewards extreme anchoring. Move a small step and re-justify, or hold and re-frame.
- **Every changed construction requires a fresh evaluation.** Re-run the trade-evaluation logic every time the pieces, pick/FAAB sweeteners, or roster counts change. A counter that adds a bench throw-in can still flip the deal once forced cuts, waiver replacements, legality, or timing are accounted for.
- Classify momentum: converging (versions getting closer → close it), circling (same gap restated → change the *pieces*, not the price), or diverging (walk-away is near).

## Step 4: Concession laddering

- **Concede smallest legal pieces first**: bench depth, a throw-in, or FAAB/claim priority only when the league and platform explicitly allow that asset to be traded — never the headline player in the first concession.
- **One concession per round**, and always attach a condition: "I'll add Sandoval if we swap your Pruitt in for the backup TE." Free concessions teach the partner to keep waiting.
- **Change the shape when price-stuck**: expand 1-for-1 into 2-for-2 (lets both sides win a lineup slot), or move the surplus piece — a different player of similar value may fit their roster better and cost the user less.
- In any 2-for-1 or 3-for-2 revision, recalculate who gets cut, who replaces that cut from waivers, and whether the platform/legal rules allow every asset in the package.
- **Deadline lever**: name a real expiry tied to a real event ("before Sunday's games — after that Fontaine's price changes"). Never bluff an expiry; leagues remember.
- **Develop a second partner before negotiating hard.** Having a genuine alternative for the same roster hole is the strongest legitimate leverage in fantasy trading — it makes the walk-away credible because it *is* credible. Build it before you need it, and never fabricate one.

## Step 5: Frame every message as their win

The counter-message the user sends should lead with what the other side gains ("this fixes your RB2 for the playoff run"), state the change plainly, and skip the lecture about fairness. Draft the actual message text for the user. Keep leverage private: never reveal the walk-away, desperation ("I have to fix TE this week"), or a rival negotiation unless it's real and strategically deployed.

## Step 6: Close or walk

- Close when the current version ≥ the minimum acceptable version and momentum is converging — accept promptly; extracting the last 2% risks the whole deal.
- **In veto-vote leagues, optics are a closing condition.** A genuinely fair deal that *looks* lopsided gets vetoed anyway. Once terms are agreed, consider restructuring toward apparent balance — a token piece each direction changes nothing materially and removes the pretext. Check `leagues.md` for whether the league uses league votes or commissioner review.
- Walk when two consecutive rounds circle below the walk-away line. Exit warmly ("can't make this one work — flag me if your RB situation changes") — preserved rapport is the option value on every future trade.
- Then suggest `roster-ops:propose-trade` to submit the final agreed version. If that plugin isn't installed, tell the user the clicks instead.

## Worked example (fictional)

**As of Friday 6:00 PM ET**, the platform still shows the same players, deadline, and legal trade assets, with no unresolved injury change. "Turf Burns" countered the user's Fontaine-for-Vasquez offer: they want Fontaine **plus** WR Jalen Moss for Vasquez. User's walk-away (from a fresh trade-evaluation pass): giving Fontaine + any startable WR loses more lineup points than the elite TE adds — Moss is over the line, a bench piece is not.

> They kept the structure — they want this trade; it's a price haggle. Counter (one concession, conditioned, smallest piece): "Can't do Moss — he starts for me. I can do **Fontaine + Dewey Sandoval for Vasquez** *if* you include your backup TE so I'm not streaming the position while Vasquez is on bye. Sandoval's been getting goal-line looks. Good until Sunday — after this week I'm just streaming TE and keeping the RBs."
>
> That concedes a bench RB (the smallest piece), holds the headline player, **attaches a condition to the concession** rather than giving it away, sets a soft but real deadline, and frames their gain. If they circle back to Moss again: walk, warmly.
