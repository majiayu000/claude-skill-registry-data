---
name: bid-landscape-and-win-rate
description: Read the bid landscape and the win-rate-by-bid curve to find the efficient bid, the point where one more dollar of bid stops buying enough extra volume to be worth it. Use when the user asks about the bid landscape, win rate by bid, the efficient bid, marginal CPA vs marginal volume, "should I raise my bid", first-price bidding and how it changes the bid-to-win relationship, supply path optimization effects on win rate, bid shading, or deciding by dimension where to lean in versus cap the bid.
---

# Bid landscape and win rate

Every bid sits on a curve: raise it and you win more impressions but pay more for the ones you were already winning; lower it and you save on each win but lose volume. The efficient bid is the point where the next dollar of bid stops paying for itself. This skill is the method for finding that point: read the win-rate-by-bid relationship, weigh marginal cost against marginal volume, account for a first-price clearing environment where the bid is the price, and decide per dimension where to push and where to cap.

This skill operationalizes the auction foundations. For how the RTB auction runs and why open auction is first-price, see the `programmatic-foundations` skill; that skill explains the mechanics conceptually, this one turns them into bid decisions. For choosing and configuring the bid strategy that will execute these decisions on DV360, see the `dv360-bid-strategy` skill. For a line item that is not delivering at all (zero spend, disapproved creative, broken targeting), start in `dv360-troubleshooting`.

## When to use this skill

- "Should I raise my bid?" / "Is my bid too low or too high?"
- "How do I read the bid landscape / the win-rate curve?"
- "What is the efficient bid?" / "Where is the point of diminishing returns?"
- "Marginal CPA vs marginal volume, how do I trade them off?"
- "How does first-price change how I bid?" / "What about bid shading?"
- "Supply path optimization, and why is my win rate low on one exchange?"
- "Win rate by exchange / domain / format, where should I lean in or cap?"

Boundaries with sibling skills:
- The auction mechanics and first-price vs second-price concept itself: `programmatic-foundations`.
- Selecting the bid strategy (fixed, maximize, target CPA or ROAS, custom) that carries out these bid decisions: `dv360-bid-strategy`.
- A line item that is not serving for non-auction reasons (creative, targeting, pacing, eligibility): `dv360-troubleshooting`.
- Scoring impressions on a custom value before bidding: `dv360-custom-bidding`.

## Quick reference

The win-rate-by-bid curve is S-shaped. Where you are on it tells you what a bid change buys.

| Where the bid sits | Symptom | Move |
| --- | --- | --- |
| Low on the curve | Very low win rate, losing most auctions on price | Raising the bid buys a lot of volume cheaply per extra impression |
| Middle (steep part) | Win rate rising fast with bid | Each dollar still buys meaningful volume; tune toward goal |
| High (flat top) | High win rate, curve flattening | Raising the bid mostly raises cost on wins you already had; cap or hold |
| At the wall | Win rate near ceiling, CPA climbing | Stop bidding up; you are paying more for almost no new volume |

Two facts this encodes:
- Win rate is impressions won divided by bid responses, not over requests seen. A high win rate on few bids is not scale; check bid volume alongside it.
- The decision is always marginal. Judge a bid increase by the cost and volume of the next impressions it buys, not the average across all impressions.

## Core process

1. Pull the win-rate curve, not a single number. Get win rate and cost across a range of bids (a bid landscape report, a target/bid simulator where available, or your own bid-vs-win-rate data from logs). One win-rate figure hides where you sit on the curve.
2. Locate your position. Low win rate on the steep part means cheap volume is available above you; high win rate on the flat top means you are near the ceiling and paying up for little.
3. Compute the marginal trade, not the average. For a candidate bid increase, estimate the extra impressions won and the extra total cost (remember you pay more on impressions you were already winning, see First-price below). Divide the extra cost by the extra conversions or value to get the marginal CPA or marginal ROAS of that step.
4. Compare marginal CPA to your goal, not average CPA. Keep bidding up while the marginal CPA of the next step is at or below your target. Stop when the marginal CPA of the next step exceeds the goal, even if average CPA still looks fine.
5. Adjust for the clearing environment. In first-price you pay your bid, so the cost of bidding up is steeper than second-price intuition suggests; modern stacks apply bid shading to avoid overpaying (see First-price below).
6. Decide by dimension. Read win rate by exchange, supply path, domain, format, and device, then lean into paths where you win efficiently and cap or exclude paths where you overpay or cannot win (see Win rate by dimension below).
7. Hold and remeasure. After a bid change, let delivery restabilize before reading the new curve; a strategy mid-learning gives a noisy landscape (learning periods are in `dv360-bid-strategy`).

## The efficient bid: marginal CPA vs marginal volume

The efficient bid maximizes profitable volume, which is not the same as maximizing win rate or minimizing CPA.

- Marginal volume is the extra impressions (and downstream conversions or value) the next bid increment wins. It is large on the steep part of the curve and shrinks toward the flat top.
- Marginal cost is the extra total spend that increment causes. It includes paying more for impressions you were already winning, not just the price of the newly won ones, which is why marginal cost rises faster than it first appears.
- Marginal CPA is marginal cost divided by marginal conversions for that step. The efficient bid is where marginal CPA equals your target CPA (or marginal ROAS equals your target ROAS). Below that bid you are leaving profitable volume on the table; above it you are buying volume that loses money even though the average still looks healthy.
- Worked logic: if raising the bid from 4.00 to 4.50 wins 1,000 more impressions that yield 5 more conversions but adds 600 in total cost (including the uplift on previously won impressions), the marginal CPA of that step is 120. If your target CPA is 80, that step is unprofitable, hold at 4.00 even if your blended CPA at 4.50 is still under 80. Always test the step, not the average.

The trap is optimizing to a blended average. A blended CPA under target can hide a marginal CPA far over target on the impressions the last bid increase bought. Decisions live at the margin.

## First-price clearing and the bid-to-win relationship

Open auction is first-price: the winner pays exactly what it bids (the concept is covered in `programmatic-foundations`). That single fact reshapes the bid landscape relative to old second-price intuition.

- The bid is the price, not a ceiling. In second-price you could bid high and usually pay the runner-up price plus a cent, so overbidding was cheap. In first-price, every increment you add to your bid is paid in full on every win. Bidding up to chase win rate raises your clearing price on all wins, not only the marginal ones.
- This makes the marginal cost of bidding up steeper. The flat top of the win-rate curve is expensive in first-price, because you keep paying your full higher bid for diminishing extra volume.
- Bid shading exists to solve exactly this. A shading layer estimates the lowest bid likely to still win and submits that, so you capture the impression without paying your full max bid when you do not need to. If your DSP or the exchange applies shading, your realized clearing price sits below your nominal bid, and the effective curve is gentler than the nominal one. Know whether shading is active, because it changes what raising the nominal bid actually does.
- Practical consequence: in first-price, find the bid that wins the impressions you want at an efficient price, rather than bidding high "to be safe". Safety is not cheap when you pay your bid. Use win-rate data and shading, not a padded max bid, to control clearing price.

## Supply path optimization and win rate

The same impression is often available through several exchanges and resellers. Supply path optimization (SPO) is choosing the paths that deliver the impression most efficiently and cutting the rest, and it shows up directly in win rate.

- Duplicate paths split your bids and depress win rate. If you bid for the same inventory through three exchanges, you compete with yourself and win a smaller share on each path; consolidating onto the cleaner, cheaper path raises win rate and lowers cost.
- Path quality differs. A direct or shorter path typically has a lower take rate and a higher effective win rate for the same spend than a long reseller chain that marks the impression up. Read win rate and effective CPM by path to see which paths actually deliver.
- Low win rate on one exchange is often a path problem, not a bid problem. Before bidding up to fix a low win rate on an exchange, check whether you are reaching the same inventory more efficiently elsewhere, or whether that path has high floors or heavy reselling. Bidding up a bad path overpays; rerouting fixes it.
- The SPO lever interacts with the bid lever: prune paths first so your bids concentrate where you win efficiently, then tune the bid on the surviving paths. Tuning the bid before pruning optimizes against a polluted landscape.

## Win rate by dimension: where to lean in versus cap

Win rate is most useful disaggregated. The aggregate hides that you dominate some slices and cannot win others.

- Read win rate (and the matching CPA or value) by exchange, supply path, domain or app, ad format, device, and geo. Each slice has its own curve.
- Lean in where you win efficiently: a slice with a healthy win rate at or below target CPA is one to bid up or expand, because the marginal economics there are favorable.
- Cap or exclude where you overpay or cannot win: a slice with a very low win rate despite a high bid is either priced out (high floors, fierce competition) or a bad path, both of which waste spend if you keep bidding up. Cap the bid there or exclude it and redeploy to slices that convert.
- Watch a high win rate paired with weak downstream performance. Winning nearly everything on a slice can mean you are the only serious bidder because the inventory underperforms; high win rate is not automatically good. Pair every win-rate read with its CPA or value.
- Turn the read into action: concentrate bid and budget on efficient, winnable slices; cap or cut the rest. That reallocation usually moves blended performance more than a global bid change, because it fixes the mix rather than the average.

## Decision rules and thresholds

- Always evaluate a bid change at the margin. Raise the bid while the next step's marginal CPA is at or under target; stop when it crosses target, regardless of blended CPA.
- Never read win rate without bid volume and the downstream KPI. Win rate is wins over bid responses; high win rate on thin bids is not scale, and high win rate on poor inventory is not quality.
- In first-price, do not pad the bid for safety. You pay your bid on every win. Set the bid to the efficient clearing point and rely on shading, if active, to avoid overpaying.
- Fix the supply path before bidding up a low-win-rate exchange. Confirm you are not self-competing across duplicate paths or stuck on a high-take reseller chain.
- Disaggregate before you act. A global bid move treats a good mix and a bad mix the same; reallocating across slices by win rate and CPA usually beats a blanket change.
- After any bid or path change, let delivery restabilize before rereading the landscape; learning-period noise distorts the curve (see `dv360-bid-strategy`).

## Templates and examples

- Low win rate, want scale: pull the win-rate curve, confirm you sit on the steep low part, and step the bid up while the marginal CPA of each step stays under target. Stop at the first step whose marginal CPA exceeds target, not where blended CPA does.
- High win rate, CPA creeping up: you are on the flat top paying your first-price bid for little new volume. Hold or lower the bid; the cheap volume is already won, and extra bid is mostly clearing-price inflation on existing wins.
- One exchange shows a stubborn low win rate: before bidding it up, check for duplicate paths to the same inventory and the path's take rate. Reroute to the cleaner path or cap the bid there; only bid up if that path is genuinely the efficient route.
- Win rate strong on one format, weak on another at the same bid: lean budget and bid into the efficient format, cap or exclude the inefficient one, and remeasure blended CPA, which usually improves from the mix shift alone.
- A slice with near-100% win rate but poor conversion: do not celebrate the win rate. You are likely the only real bidder on weak inventory; cap or exclude and move spend to contested, converting slices.

## Common pitfalls

- Optimizing to win rate as if higher is always better. Win rate is a means, not a goal; a high win rate on cheap or poor inventory, or on thin bid volume, is not value. Pair it with CPA or value and bid volume.
- Deciding on blended CPA instead of marginal CPA. A healthy average can hide that the last bid increase bought money-losing impressions. Test the step, not the average.
- Carrying second-price intuition into first-price. Bidding high "to be safe" is expensive when you pay your bid on every win. Find the efficient clearing bid and use shading, not a padded max.
- Bidding up a low win rate that is really a supply-path problem. Self-competition across duplicate paths and high-take reseller chains depress win rate; bidding up overpays. Prune the path first.
- Reading win rate only in aggregate. The aggregate hides slices you dominate and slices you cannot win. Disaggregate by exchange, path, domain, format, device, and geo before acting.
- Rereading the curve mid-learning. A strategy that just changed gives a noisy, unrepresentative landscape. Let it restabilize, then read.

## Sources

- [Estimate your results with bid, budget, and target simulators (Google Ads)](https://support.google.com/google-ads/answer/9634060) (as of June 2026)
- [Metrics in reports, Win Rate definition (Display & Video 360)](https://support.google.com/displayvideo/table/3187025) (as of June 2026)
- [Troubleshoot your deals and line items (Display & Video 360)](https://support.google.com/displayvideo/answer/6292894) (as of June 2026)
