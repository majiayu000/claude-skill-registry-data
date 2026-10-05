---
name: spy-competitor-ads
metadata: {packVersion: 1.3.0}
description: >-
  Downloads a competitor's live ad creatives — the actual MP4s and JPEGs — from the Meta Ad
  Library into a local swipe folder, through the Novoads API. One sweep per competitor,
  priced by a live estimate before anything is charged, media pulled the moment the response
  lands because the CDN links expire, and every ad carried with its permanent Ad Library
  URL, the page running it, and how many audiences the creative is running against, closing
  with the three most established and why. Use when asked to spy on competitors, find what
  ads a brand is running, pull a competitor's video or static creatives, build or refresh a
  swipe file, check who is outspending you on Meta, or source a reference ad to recreate.
  It finds, ranks and files ads; it does not rebuild them — a static becomes your own ads,
  or a reusable template, via clone-image-ad. It writes no craft analysis and no creative
  brief. A sweep that finds nothing is a result, never an apology.
---

# Spy Competitor Ads

Find what a competitor is actually running, and put the files on disk. That is the whole job.

It ranks what it finds, on evidence the Ad Library actually publishes — how long a creative has
run and how many audiences it runs against. It does **not** judge craft, explain "why it's
winning", or write a brief; it has not watched these ads and neither have you. What you do with
them belongs to `clone-image-ad`, which turns a static into your own ads, a reusable template,
or both.

The mechanics are one HTTP call per competitor. Everything that makes a run good or bad is
judgement: which competitors, which media mode, and which of the returned ads are actually the
brand's rather than somebody else's.

## Before anything: this runs on a Novoads account

- **Base URL:** `https://api.novoads.ai/v1` (host overridable with `NOVOADS_BASE_URL` — host
  only, you append `/v1`).
- **Auth:** `Authorization: Bearer $NOVOADS_API_KEY`, read from `.env` at the repo root. The key
  is `novo_` plus 64 hex.
- **Check:** `./scripts/check-novoads-env.sh`
- **Never** print API keys, commit `.env`, or paste a key into `MASTER_CONTEXT.md`.

> **REST key required. A Novoads MCP connector is not a substitute.** If
> `NOVOADS_API_KEY` is missing or still the placeholder, stop before any
> generation work and tell the user: "Before continuing, create an API key at
> <https://novoads.ai/dashboard/settings?tab=api> and paste it into `.env`."
> That holds even when `mcp__novoads__*` tools are connected and authenticated in
> the session. Never call `mcp__novoads__*` tools from this repo's workflows: they
> are a different surface with different behavior, including the units they quote
> costs in. Repo installs verify with `./scripts/check-novoads-env.sh`; a solo
> install checks `NOVOADS_API_KEY` in the environment.

**Pack version.** Every `/v1` response carries `X-Novoads-Pack-Version`; mention a newer pack at <https://github.com/novoads/agent-skills> only when that header names a version NEWER than this file's `metadata.packVersion` — equal or older is nothing to say, and it is never a reason to stop.

A `401` means the key is wrong, revoked, or from another account. A `403` with
`error.details.reason` of `plan_required` or `subscription_inactive` means the key is fine and
the account has no live subscription. Different problems, different fixes — say which one it is.

No account yet? **<https://novoads.ai/?utm_source=claude-code&utm_medium=github&utm_campaign=skill-pack>**
There is no free tier and no trial: every plan is a paid monthly subscription,
published at novoads.ai/pricing. Never call it free.

**If this deployment does not offer sweeps yet.** The endpoint is behind a flag that is off by
default. With it off, `POST /v1/competitor-ads` and a `kind: "competitor-ads"` estimate both
answer **`400 invalid_input`**, and the message names what the API *does* offer — it is not a
`404`, and the path existing is not evidence it is enabled. Read that as "this deployment does not
sell sweeps yet", say so plainly, and stop. Do not retry it, do not work around it with a
browser, and do not treat the 400 as a body you got wrong.

`POST /v1/competitor-ads` is the only sweep this skill runs. Verified live 2026-08-08 against
spec `2.19.0`: `HTTP 200`, ads returned, `creditsCharged: 0.2`, matching a
`{"kind":"competitor-ads"}` estimate taken in the same session.

## Golden rules

1. **Price it live, every time.** Every credit number you say out loud came from a
   `POST /v1/estimates` call in this session. There are no rate tables in this file, in this
   repo, or in the logs, and a remembered fee is a lie waiting to happen.
2. **The fee is flat per sweep.** Never quote a per-ad price. Asking for 5 ads costs exactly
   what asking for 20 costs, because the vendor bills a ten-result minimum underneath. N
   competitors is N charges, and that multiplication is the only arithmetic you do out loud.
3. **Download before you write a word.** The response carries `urlsExpire: true` and Meta's own
   token-bound CDN links. A response filed away for later is a list of dead links. `curl` every
   media URL the moment the sweep returns; `adLibraryUrl` is the durable one and it is what you
   quote.
4. **Zero ads is a report, not an apology.** An empty sweep is a success, it is charged, and it
   is said in one line. See *Zero* below — this is the rule this skill exists to hold.
5. **The results are not filtered for you, and filtering them is your job.** A keyword search
   returns third-party pages running the brand's creatives, and sometimes an unrelated company
   trading under the same name. Both arrive as `200 OK`. See *Reading the result*.
6. **Ask in prose, one question at a time.** No option menus. Carry a default so silence is
   never a blocker, name an escape hatch, and never ask twice about the same thing.

## Step 1 — resolve the sweep

Four things decide a run. Take each in order, take it in one line, and only ask about the ones
you genuinely cannot resolve.

**Brand.** Named in the request, or obvious from the repo's `MASTER_CONTEXT.md` or the product
you have been working on → use it, and say which one you took. Otherwise ask once: *"Which
brand am I spying for?"* Do not guess the brand — every downstream judgement about what counts
as pollution depends on it.

**Media mode.** The API requires it and `sweep.py` requires it, so SOMETHING has to choose —
look for an explicit trigger first:

| They said | `mediaType` |
|---|---|
| "video ads", "their videos", "hooks", "UGC they're running" | `"video"` |
| "static ads", "image ads", "posters", "creatives to print" | `"image"` |
| "both", "everything", "the full swipe file" | `"all"` |

Silent → **take `"image"`, say you took it, and name the escape in the same line.** Do not ask;
a question the run can answer for itself is work handed back to the user.

> Sweeping their **static** ads — 20 slots each, all statics. Say "video" or "both" instead.

**Why statics rather than `"all"`, when `"all"` costs the same:** the FEE is flat, the SLOTS are
not. `count` maxes at 20 per sweep whatever mode you ask for, so `"all"` spends those 20 on a
mix the user did not choose. Measured on a real three-competitor run, 2026-08-10: `"all"`
returned **20 video and 0 static** for one brand and 13/6 for another. Someone who wanted a
static from the first brand got nothing, at the same price that would have bought twenty. And
the clone that follows is the expensive half — a static render costs a fraction of a video one,
so the cheaper next step is the better default.

Say the slot cost out loud when they ask for `"all"`, because it is the part the flat fee hides:
**one kind gets you 20 of that kind; "both" splits the 20.** That is the whole trade, and it is
not a reason to refuse them — just a reason they should hear it once.

**Competitors.** Named → use them exactly as given, including the ones you would not have
picked. Not named → find 3 to 5 with `WebSearch` (brands selling something similar to a similar
audience that plausibly run paid social), then put the shortlist in front of the user before
opening a single sweep, in prose:

> I'd sweep Arcads, Creatify and Icon — all three sell AI UGC ads to performance marketers.
> Three sweeps, three charges. Swap or add any before I start.

That confirmation is not politeness. Each sweep spends, and a list the user has never seen is a
list you invented.

**Count and country.** `count` defaults to **20**, and 20 is right almost always: the fee is
flat, so a smaller number buys less for the same money. Honor an explicit smaller number, and
say once that it does not save anything. `country` defaults to `"ALL"`; narrow it to an ISO
3166-1 alpha-2 code only when the question is genuinely about one market, and say that narrowing
can empty a sweep you still pay for.

## Step 2 — price it before you sweep

```bash
curl -sS -X POST https://api.novoads.ai/v1/estimates \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kind":"competitor-ads"}'
```

Returns `credits`, `balance` and `sufficient`; when the balance is short it also returns
`shortBy` and `topUpUrl`. It spends nothing and it runs the same access checks the paid call
runs, which is why it is worth calling every time rather than only when you are unsure.

The estimate body is strict and only takes fields that move the price. The fee is flat per
sweep, so `kind` is the whole body. If the arm asks for more, the `400` names what is missing —
send it and re-quote. **Never fall back to a number you remember.**

Then announce, in one line, and get a yes before the first sweep:

> 3 competitors × 1 sweep each = 3 charges at N credits, N total (balance: B). Starting?

Two cases change it. `sufficient: false` is a blocker, not a warning: stop, say exactly what is
short, and give `topUpUrl`. And if the balance covers this run but not a second one, say so in
one clause before firing — a user who knows that picks their competitors more carefully.

## Step 3 — sweep them all at once, and download as they land

```bash
./scripts/sweep.py --queries "arcads.ai,creatify.ai,icon.com" --media video --yes
```

One call, all competitors, **in parallel up to the API's ceiling of ten concurrent sweeps** —
a budget kept separate from renders precisely so sweeps cannot starve a caller's next clip.
Each competitor's creatives are downloaded inside its own unit of work, the moment that
response lands, so the CDN clock starts and stops per competitor instead of after the slowest
one. It writes `outputs/competitor-ads/<slug>/{sweep.json,swept.json}` plus the media, retries
a 429 once using **the server's own `Retry-After`**, and reconciles what landed against what
was promised by counting FILES ON DISK.

**`--yes` is required and the script refuses without it**, naming the estimate. It spends one
charge per competitor and it is called by an agent; a script that can spend when nobody said
yes is the one failure worth being rude about. Price it and get the yes first — that half is
judgement and stays with you.

Read its summary out. On a shortfall it says which competitor was short and where the failed
ids are; do not present a short set as the full one.

**This used to say "one competitor per call, sequentially."** That was wrong twice over: the
justification was a single probe's "about ten seconds" that a real three-competitor run
contradicted in minutes, and the habit itself came from the RETIRED browser version, which
serialised to avoid bot detection while driving Chrome at Meta. Apify does the scraping now.
Nine of the ten slots were idle.

**`query` is a keyword search, not a page lookup.** A domain (`arcads.ai`) or an `@handle` is a
sharper query than a bare word, for the same reason it was in the browser era: bare words collide
with unrelated companies. It takes 2 to 200 characters.

### What comes back

```
POST /v1/competitor-ads
  request   query       brand name or domain, 2..200 chars          required
            mediaType   "video" | "image" | "all"                   required, no default
            country     ISO 3166-1 alpha-2, or "ALL"                default "ALL"
            count       1..20                                       default 20

  response  ads[]       adArchiveId     the Ad Library's own id for this ad
                        pageName        the page RUNNING it — not necessarily the brand
                        pageId
                        adLibraryUrl    permanent, public, the durable record
                        bodyText        the ad's primary copy, or null
                        collationCount  how many audiences this creative runs against, or null
                        startDate       when it went live, or null
                        endDate         or null
                        isActive
                        platforms[]     FACEBOOK, INSTAGRAM, THREADS, …
                        media           { kind: "video" | "image",
                                          videoHdUrl?, videoSdUrl?,
                                          previewImageUrl?, imageUrl? }
            query, mediaType, country   echoed back, so a saved sweep.json is self-describing
            urlsExpire  always true     the media URLs are already dying. See step 4
            creditsCharged              what this sweep cost. Log this, never recompute it
```

Ads arrive **ranked**: `collationCount` descending, then most recent first, deduplicated,
truncated to `count`. That ordering is mechanical. There is no server-side "which ad is
winning" — that judgement is yours and it is step 5.

Two things the list will not contain, so you do not go looking for them: the same creative twice
(it is collapsed on Meta's ad id, on Meta's collation id, and — for ads Meta groups under nothing —
on the opening of the ad's own copy), and ads with no fetchable file. Carousels and dynamic
creative are often published without a video or image on the ad itself, and an entry you cannot
download is not a creative to study. So `ads` can be shorter than what the Ad Library shows in a
browser, and a brand whose whole live set is that shape comes back as `ads: []`.

## Step 4 — check what actually landed

`sweep.py` already downloaded everything and printed `landed/expected` per competitor, counted
from FILES ON DISK rather than from its own successes. Read that line before you write a word
of delivery.

**A shortfall is said out loud, in the first sentence, or not at all.** A partial set delivered
as complete looks exactly like a competitor who runs four ads — that is the failure this whole
step exists to prevent, and it was measured: a browser-era run reporting five successes produced
exactly one file.

On a shortfall you have two moves, and delivering quietly is neither: re-fetch the named ids
from the sweep.json you already have, or deliver with the count named and the `adLibraryUrl`s
for what is missing. `references/recovery.md` has the loop. **Never re-sweep to refresh a
link** — that is a second charge for ads already paid for.

**Never log a media URL.** It is a credential while it lives.

## Step 5 — read the result with judgement

### `pageName` is who is running the ad, not who makes the product

Nothing is filtered server-side, and that is deliberate. On the probe behind this endpoint
(query `arcads.ai`, video, 2026-08-08) ten live ads came back across **three** pages, and only
three of the ten sat on the brand's own page. The rest were affiliate and reseller pages running
the brand's creatives, one of them carrying more live ads than the brand itself.

That is signal, not noise. An affiliate outspending the brand on the brand's own creatives is
one of the more useful things a sweep can tell you, and a server-side brand filter would have
silently deleted it.

So read `pageName` and `bodyText` on every ad and sort them into three groups:

- **The brand's own page** — what they are running themselves.
- **Third parties running the brand's creatives** — affiliates, resellers, agencies. Keep these.
  Say who they are.
- **Same-name strangers** — a genuinely unrelated company trading under the same word. The
  canonical case is "Creatify" the AI tool versus "Creatify.mx" a sticker shop. Drop these.

**Name the groups in the delivery and say what you dropped and why.** A filter the user cannot
see is a filter they cannot correct, and the correction is usually one sharper query away.

### Rank it with the script, not by eye

```bash
./scripts/rank-ads.py "$DIR/sweep.json"                  # the words
./scripts/make-picker.py "$DIR/sweep.json"               # the page
```

The first prints the delivery's opening: what the sample is, the twelve picks with their
basis, who is running them, the metadata-not-craft line. Read it out; do not recompute it.

**Then get it in front of them, and pick the way by what the session can actually do.** A page
on disk is invisible in a remote sandbox, over SSH, and to anyone looking at a chat window
rather than a desktop. **Never say "it is open in your browser"** — you cannot verify that, and
when it is wrong the user is staring at a screen where nothing happened.

**If your harness can render an HTML file inline in the conversation** — Claude Code publishes
one as an artifact — **that is the best answer.** It works locally and remotely, and the cards
stay clickable. Build it with `--embed`, then publish that file:

```bash
./scripts/make-picker.py "$DIR/sweep.json" --embed --out "$DIR/artifact.html"
```

Publish it with a title naming the brand and the count, and tell the user plainly that the
creatives are uploaded to render: they are a competitor's copyrighted work, the page is private
to them, and the on-disk copy stays local either way. Say it once, not every run.

`--embed` is not optional there: an artifact's CSP blocks every external host, so a page that
references the files beside it renders as twelve broken frames. Videos embed as their **poster
frame** and say so — twelve mp4s as data URIs is roughly 47 MB against a 16 MB ceiling — and the
script drops the tail rather than exceeding it, saying which on the page.

**Otherwise fall back to the file on disk**, name its absolute path, and offer to open it. Either
way, **also put the top few creatives in the conversation** by reading the downloaded images.
That is the one thing that works in every environment, and it is what makes the page a richer
view rather than the only one:

> Top 3 of 12 below. Full sheet: `/abs/path/picker.html` — say the word and I'll open it.

The second writes a **contact sheet** beside the sweep: twelve creatives at real size, videos
playable in place, each card numbered and carrying its page, dates and Ad Library link.
Comparing twelve ads as filenames is not comparing them. Open it and say:

> 12 candidates, and `picker.html` is open. Click the ones you want, or say **"clone 3"** —
> or **"clone 1, 4, 7"** for several.

Cards toggle, nothing starts selected, and the bar copies `clone 1, 4, 7`. **Each number is a
separate clone run**, so selecting six is six priced runs, not one — the bar says so and the
estimate still gates every one of them. The ordinal is the contract and the click is the
convenience, so a blocked clipboard costs nothing. Both scripts share one sort and one default
— never renumber by hand. A page rather than an option prompt on purpose: a prompt blocks, and
this flow proposes and proceeds.

The sort is `collationCount` descending then longest-running, which is arithmetic, and the
script also decides the thing prose kept getting subtly wrong: **whether the audience-count
signal is alive at all.** Measured on a real sweep of this category, every row came back `1`
or `null`, so the field the ordering nominally leads on contributed nothing and run length
decided everything — while the delivery still recited both bases. The script detects that and
says "run length only" instead. `--top N` changes how many BOTH produce (12 by default — a
grid of twelve is one glance where a list of twelve is a scroll); `--json` gives you
`signalAlive` and the counts if you are formatting your own.

Three claims it carries that are easy to get wrong by hand:

- **The SAMPLE is the strongest thing you can say.** The Ad Library is queried with
  `sort_data[mode]=total_impressions` descending — the same "Impressions: high to low" a human
  gets in the UI — so every ad in a sweep is among Meta's highest-impression ads for that
  query. Lead with it.
- **There is no impressions NUMBER.** Meta publishes per-ad impressions only for political and
  issue ads, and in the EU. Never quote one, never infer one from position.
- **The ORDER is ours, not Meta's.** The API re-sorts by `collationCount` then recency before
  you see it, so position 1 is not Meta's #1. The impressions claim belongs to the sample, not
  to the order within it.

What stays yours is the only part no sort can decide: **which of the three is worth cloning**,
read against the product you are cloning for. And it never becomes a craft judgement — you
have not watched these ads. Reading one properly is `analyze_ad`, charged **per ad**, which
against a twenty-ad sweep is an order of magnitude more than the sweep cost. Offer it on the
top one to three as its own priced step; never quietly upgrade "rank these" into twenty reads.

### `collationCount` is recurrence, not spend

It is the closest thing to a spend signal the Ad Library exposes: one creative shown against
twelve audiences appears as `collationCount: 12`. High collation plus an old `startDate` is the
strongest available evidence that a creative is working, because nobody keeps paying to run a
loser for months.

Two honesties about it. `null` is common and means *not reported*, not zero. And it is not a
budget: never turn a collation count into a dollar figure or a "they're spending X" claim. The
Ad Library does not publish spend for commercial ads, and inventing the number is worse than
leaving it out.

### Zero

**An empty sweep is a result. It is charged, and it is correct.** The vendor underneath bills its
minimum whether or not the query matched anything, so `ads: []` arriving as a `200` means the Ad
Library genuinely has nothing live for that brand, in that media mode, in that country.

Say it in one line and move on:

> No live video ads for BrandX in ALL right now.

Then stop. Specifically:

- **Do not apologise for it.** It is often the most valuable line in the whole run — a
  competitor who has gone dark is a finding.
- **Do not re-run the same sweep** hoping for a different answer. It is the same query against
  the same index, and it is a second charge.
- **Do not quietly widen the country or switch the media mode** to manufacture a result. If a
  different question is worth asking, ask it out loud, say it is another charge, and get a yes.
- **Do not pad it** with older creatives, a different brand, or the other media mode.

This rule is the reason this skill survived its rewrite. The browser-driven version could not
tell an honest zero from a broken DOM heuristic, and reporting the second as "this brand runs no
ads" was its worst failure mode. That ambiguity is now gone: a scrape that fails is a
`provider_failed` (HTTP 502) with the credits refunded, and it never reaches you as an empty list.

One honest zero has a second cause worth naming when you see it: some ad formats — carousels and
dynamic creative — are published with no downloadable file on the ad itself, and those are left
out of `ads`. So a brand whose entire live set is that shape comes back as `ads: []` on a charged
call. It is still a finding ("nothing fetchable is running right now"), and `adLibraryUrl` on the
Ad Library search page is where a human can still look.

## Step 6 — deliver, then offer the clone once

Deliver per competitor: the files on disk with their paths, the `pageName` groups, and one line
of what is live versus dark.

**Say the count first, and say it from the reconciliation in step 4** — "9 of 10 creatives
downloaded", not "here is their swipe file". If files are missing, that goes in the same sentence
with the `adLibraryUrl`s for the ones that did not land. A set delivered without its count reads as
complete, and the user studies four ads believing they are the whole answer they paid for.

Then offer the next step **once**, in one line, naming a skill that exists in this checkout:

- A **static** you want rebuilt as your own ads, or turned into a reusable template, or both
  → `clone-image-ad`.
- A **video** you want rebuilt for a different product, delivered as a finished MP4
  → `clone-video-ad`. Hand over the downloaded file path; it reads the source itself.

Offer, do not start. Either one spends, and neither is what was asked for here. There is no
hook-only skill in this pack, so an opening on its own routes to `clone-video-ad` too — clone
the whole ad and cut.

**Skip the offer entirely when this skill was invoked as a sub-step of something else.** If
another skill or workflow asked for a swipe file, hand back the file paths **and the ranked top
three** and stop — the caller owns what happens next, and an offer injected into the middle of
its flow hijacks it.

## Step 7 — file the corpus so it is not re-bought

The sweep is the charge; the files are the asset. Record beside the downloads, in
`$DIR/sweep.json`'s own directory, what was swept and **when**:

```bash
jq -n --arg q "$QUERY" --arg m "$MEDIA" --arg c "$COUNTRY" --arg at "$(date -u +%FT%TZ)" \
  '{query:$q, mediaType:$m, country:$c, sweptAt:$at}' > "$DIR/swept.json"
```

`sweep.json` already echoes the query, media mode and country back, which is why a saved sweep
is self-describing. The scan **date** is the part it does not carry, and it is the part that
decides everything below.

**Before sweeping anything, look for an existing corpus for that brand and media mode.**

- **Under 7 days old** — reuse it. Do not sweep, do not charge. Say which stored sweep you are
  using and when it was taken.
- **7 days or older** — say the date and the age unprompted, offer a refresh **with its price**,
  and wait. Never refresh silently, and never present stored ads as what the brand is running
  now. The freshness number is not arbitrary: the other competitor corpus in this repo sat at
  eight days with no threshold at any age and presented itself as healthy while three filters
  hid a post the founder found by hand.
- **Absent** — sweep, after the estimate and the announced total. Reuse is an optimisation on
  top of the price gate, never a way around it.

A stored corpus is re-minable: "clone the second one too" costs nothing. The media URLs are dead
within the hour, but the downloaded files are not, and `adLibraryUrl` never expires.

## Errors

`references/errors.md` — every `error.code` this surface emits, what each means, and what to do.
**Branch on the code, never on the message.** Two that matter before you read anything:
`provider_failed` (502) is NOT an empty result — the scrape failed and the credits were
refunded — and a call that times out on your side was probably charged, so reconcile it before
retrying rather than paying twice.

## Background

`references/background.md` — installing this skill outside the pack, and where the retired
browser-driven version went. Neither is needed to run a sweep.

## Legal note

`references/legal.md` — the Meta Ad Library is public, this skill does **not** scrape it (the
Novoads API does, through a commercial vendor, the same shape as Foreplay or AdSpy), and the
creatives you download are somebody else's copyrighted work. Studying a swipe file and
rebuilding an idea is not re-running a competitor's ad.

## Hard rules

- Every credit number comes from a live estimate in this session. No rate tables, ever.
- Never quote a per-ad price. The fee is flat per sweep.
- Download the media before writing the delivery. `adLibraryUrl` is what you quote.
- One sweep per competitor, fanned out to the API's ceiling by `sweep.py`, against a list the
  user has seen and priced.
- Never ask twice about the same thing, and never with a menu. A question the run can answer
  for itself is not a question — media mode defaults to `image` and says so.
- An empty sweep is reported in one line and never retried.
- Never turn `collationCount` into a spend figure.
- Never invent an ad, pad a thin result, or deliver a group you filtered without saying so.
- Close with a ranked top three and the basis for it. Never rank on craft you have not paid
  to read.
- Check for a stored corpus before sweeping. Under 7 days, reuse it and charge nothing; older,
  say its age and price the refresh; absent, sweep after the estimate. Reuse never skips the
  price gate.
