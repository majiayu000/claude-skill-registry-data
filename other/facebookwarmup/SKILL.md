---
name: facebookWarmup
description: "The Facebook part of warmup: the five Facebook warm-up activities (feed, Marketplace browse, create-page check, Selling, Messages), what each step must answer, `log facebook warmup stages`, the like and unmute details, and the Reels persona run. Read with its shared counterpart, skills/warmup/SKILL.md (the flows guide), when warming up a Facebook account."
---

# facebookWarmup

How a warm-up is recorded and run (activities as flows in one open browser,
the stage log, the hard boundaries) is `skills/warmup/SKILL.md`. This is what
only applies on Facebook.

## The five activities

The feed, Marketplace browse, the create-page check, Selling and Messages.
All five are flows since 2026-10-22 (Bethlehem: recorded, then run 27/27 steps):
`src/browser/flow/definitions/warmup*.json`, docs in
`docs/platforms/facebook/flows/warmup*.md`.

```bash
log facebook warmup stages plan                                        # the five scripts, recorded or not
log facebook warmup stages record --account <a> --now                  # one headed session: each script, then each flow
log facebook warmup stages run --account <a> --now                     # watched run: the machine runs each flow in turn, 10 s apart
log facebook warmup stages log --account <a> --follow                 # the stage log, live
```

`--only feedBrowse,sellingVisit` limits it. After recording, rebuild the
request docs: `log capture docs`.

Doc: `docs/lifecycle.md` (the warm-up section); scripts:
`src/facebook/warmup/stages/helpers/scripts.ts`.

## Likes on Facebook

`clickAny button ^Like$` only runs with `--likes`, when the owner asks. A like
passes on Facebook's answer, not on the "Remove Like" button: the step waits
for `CometUFIFeedbackReactMutation` and passes only when it answers 2xx with
the reaction we sent saved.

## What each step must answer

- the create page: `marketplace_new_seller_can_post_item` true (else
  `marketplaceMayNotPost`), and `sell_location`'s country and city the
  account's home (else `marketplaceLocationWrong`);
- Marketplace: `buy_location.display_name` names the home city (else
  `marketplaceLocationWrong`);
- the home feed: `FeedComposerCometRootQuery` answers this account's id;
- a scroll that pages: `CometNewsFeedPaginationQuery` or
  `MarketplaceCometBrowseFeedLightPaginationQuery` answers more;
- a listing: `MarketplacePDPContainerQuery` answers its details page;
- Selling and Messages: the page answers 2xx (Selling's
  `current_marketplace`).

The Reels and feed activities do the same (`openReels`, `openFeed`,
`readFeed`, `openMarketplace`, `openListings`, and the likes).

## Wrong pages

Erie, 2026-10-19, scrolled a checkpoint page for a minute before
`pageProblem` checked every step's landing page.

## Reels play with the sound on, every time a reel loads

Reels start muted, and coming back from the creator's profile loads the reel
again, muted (the owner, 2026-10-23: the run after the profile watched with
the audio off). So `unmute` follows every `backToReel`, in the drawn session
and the persona plan, and it presses nothing when `button "Mute"` already
shows (`already`), so it never mutes.

## Facebook Reels, for a persona

```bash
bun scripts/datasets/buildReelViewers.ts                        # once: 980 real viewers from KuaiRand-1K (~/.logCli/datasets)
bun scripts/datasets/buildInterestEffect.ts                     # once: the interest effect, from KuaiRand-Pure's random log
log facebook warmup persona --account <a>              # the persona, its real viewer and its pack (every dataset a trait)
log proxy balance                                      # each provider's traffic left, before a run
log facebook warmup reel run --account <a> --persona --live [--likes] [--trafficMb 1024]
```

- Each reel, the moment it lands, is read by SubQ from its frame (theirs or
  not, what it is, the one action they'd pick); the orderer (`planReel`)
  plans the watch from the real viewer's plays (their kind from their median
  up, the rest from it down, scaled by the measured effect) and at most one
  action. Watch every line live (rule 26): `= reel N: THEIRS|not theirs; watch …`.
- Reels streams video through the proxy: about 4.5 MB a reel (2026-10-20).
  A run is refused when the account used its `--trafficMb` (default 1 GB) in
  the last 24 hours, checks every 5 reels and stops at it; each run's use goes
  to the `ledger` table in `~/.logCli/log.db` (kind `proxyTraffic`).
- The creator's profile opens in its own tab: back to the reel closes it
  (`closeTab`). Stop a run with the browser left open (rule 35); if a session
  dies, close its AdsPower profile and clear its proxy, then log the close.
