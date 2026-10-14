---
name: clickmax-vturb
description: Use when the user asks about VSL / Vturb video performance — play rate, engagement, retention, A/B test winners, whether the video is converting, how many people are watching now, or how to connect the Vturb account.
---

## When this applies

Questions about the performance of a VSL hosted on **Vturb** (the video player Clickmax integrates with): plays, play rate, engagement, finishes, clicks, conversions tracked by the player, and near-real-time audience. Also the "how do I connect Vturb" question.

## Not this skill

- revenue/sales totals, top products, funnel steps -> `clickmax-analytics`
- payment/transaction cohorts -> `clickmax-payments-dashboard-analysis`
- building or editing the page that hosts the video -> `clickmax-funnels` (page building)

## Key assumptions

- Workspace-scoped and **read-only**. There is no tool to connect, disconnect, or change the Vturb account — that happens on the Integrations page (see below).
- One Vturb account per workspace.
- `vturb_status` is the mandatory first call — every metric tool returns a precondition error when no account is connected.
- `playerId` only comes from `vturb_players_list`. Never guess or accept an id from prose.
- **Rates are 0..1 fractions** (`0.42` = 42%). Multiply by 100 before showing.
- `vturb_player_stats` data is cached ~5 min upstream — it is not real-time.
- Vturb rate-limits: a `429` means back off, not that the integration is broken.

## Connecting the account (no tool for this)

If `vturb_status` returns `connected: false`, or `status: "invalid"` (key revoked at Vturb), **do not ask the user for the API key** — no tool accepts it, and a key pasted in chat would be exposed in the conversation history.

Tell them to connect on the **Integrations** page, which is where the connection is managed:

1. Go to _Integrações_ → _Explorar integrações_.
2. Open the **Vturb** card (section _Vídeo e VSL_).
3. Paste the key generated at Vturb under _Settings > Analytics API_ and connect.

Optional on that screen: pasting the embed code of any video from the account identifies which Vturb account it is, which is what enables picking videos from the page editor. It can also be done later, in the editor itself.

Shortcut while building a page: the **Vturb** block in the page editor (group _Mídia_/_Elementos_) offers the same connection in its right sidebar. Both places write the same connection — there is only one Vturb account per workspace.

`status: "invalid"` = the key was revoked or expired at Vturb. Replace it with a fresh key on the Integrations page; disconnecting first is not required.

## Thought process

1. `vturb_status` — connected? If not, give the connection steps above and stop.
2. `vturb_players_list` — resolve the video the user means into a `playerId`. If several match the prose, ask which one instead of guessing.
3. Pick the metric tool:
   - performance over a period ("está convertendo?", "como foi essa semana") -> `vturb_player_stats` with `startDate`/`endDate`
   - who is on the page right now ("tem gente assistindo?") -> `vturb_player_live_users`
   - comparing variants ("qual versão ganhou?") -> `vturb_ab_tests_list` then `vturb_ab_test_stats`
4. Interpret against `duration` and `pitchTime` from step 2 (see below) and answer with numbers, not adjectives.

## Reading the metrics

|Field|Meaning|Trap|
|-|-|-|
|`plays`|pressed play|not unique people — use `uniqueDevices` for that|
|`playRate`|plays ÷ page loads|low play rate is a **thumbnail/headline** problem, not a video problem|
|`engagementRate`|average watch time **up to `pitchTime`**|a late `pitchTime` mechanically lowers it — always read with `pitchTime`/`duration`|
|`finishes`|reached the end||
|`clicks`|clicked the CTA||
|`conversions` / `conversionRate`|tracked **by Vturb**, over plays|**can diverge from Clickmax sales** — never present them as the same number|

`pitchTime` is the second where the offer is made. Market reference: a pitch around 60–75% of `duration` is typical; much later means few viewers ever hear the offer.

For `vturb_player_live_users`: it counts people who **entered the page** in the last `minutes` (default 60). Say "entraram nos últimos N minutos" — not "estão assistindo agora", because it does not prove they stayed.

## Diagnosing a weak VSL

Read the funnel in order and name the first stage that breaks:

```
page loads -> playRate -> engagementRate (até o pitch) -> clicks -> conversions
```

- low `playRate` -> thumbnail, headline, or the video is below the fold
- decent `playRate` but low `engagementRate` -> the opening minutes lose people
- good `engagementRate` but few `clicks` -> the CTA is weak, or hidden when the pitch happens
- `clicks` but few `conversions` -> the problem moved past the video, to the checkout/offer

## A/B tests (comparison groups)

A Vturb A/B test enrolls 2+ players (variants of the same VSL) and splits traffic between them by percentage. `vturb_ab_tests_list` gives the tests; `vturb_ab_test_stats` compares up to **2 variants per call** (upstream limit — for a 3-variant test, compare in pairs).

**Declaring a winner:**

- **Decide by `revenuePerVisitor`, not `conversionRate`.** A variant can convert less and still make more money per visitor (higher ticket). This is the single most common misreading.
- If `running` is `true` the test is **still splitting traffic** — present numbers as a trend, never as a final verdict.
- Watch the sample size: with few `views` per variant, a difference of a few points means nothing. Say so instead of crowning a winner.
- `locked` on a variant means its traffic share is pinned in the Vturb panel.

**Fair window:** omit `startDate`/`endDate` so each variant uses its own `started_at` inside the test. Forcing a shared window penalises a variant that joined later. Only pass explicit dates when the user asks for a specific period.

`retentionCurve` (`{ second, viewers }[]`) comes with these stats — it is the only place we expose per-second retention today. Use it to locate the drop-off and to choose the progressive-reveal second (below).

## Progressive reveal (using the data to change the page)

The Clickmax Vturb block supports **"Revelação progressiva"**: reveal or hide page elements at a given second of the video (`data-vturb-timer`). When the user asks when to show the CTA, anchor the recommendation on `pitchTime` from `vturb_players_list` — revealing the button around the pitch instead of at page load is the common fix for "engaja mas não clica".

> Per-second data is only available for videos enrolled in an A/B test, via `retentionCurve` in `vturb_ab_test_stats`. For any other video do not claim to know the exact drop-off second — reason from `pitchTime`, `engagementRate` and `finishes`.

---

Clickmax skill revision: `b8294822a4d6`
