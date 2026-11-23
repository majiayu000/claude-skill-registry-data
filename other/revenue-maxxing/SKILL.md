---
name: revenue-maxxing
description: Use when the user wants to raise what a YouTube channel or niche earns, from RPM and buyer intent to a newsletter, its own products and sponsors, scored layer by layer against peers. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "6.6"
  requires: tubelab-mcp
---

# Revenue Maxxing

## Overview

Top-earning channels stack five layers: sponsors, buyer intent (videos promising a result), a list to upsell, own products, and ad revenue, the least important. Score each against peers.

**Without TubeLab:** no audience, RPM, revenue or income-method data, so peers are guesses.

## Workflow

1. No channel? Score what a newcomer should build.
2. Read the channel's About, top and newest videos, descriptions, thumbnails and two transcripts (reads are often spoken). Note each offer, list and sponsor.
3. Look up the channel and the peer that earns in the most ways by handle, one per search, no other filter, not even `publishedAtFrom`. Find peers selling to the same viewers in any format: ones the user names or you know, read for free; one or two searches seeded with the channel, with `publishedAtFrom` and `classificationQuality` `"neutral"` or above; and one with niche words and `detectionsMonetization` course, product, community and services, for sellers and prices. Drop hits whose audience estimate differs.
4. Open peers' offers and sponsor reads: what, price, link. Read that peer's top transcript.
5. Mine comments on the top five to ten videos for pains: questions, complaints, "how do I", "I wish", favouring the richest viewers.
6. Score each layer ✅ 100, 🟡 50, ❌ 0.
   - Sponsors: ✅ for regular reads, 🟡 for occasional reads or affiliate links only. Also ✅ when its own products fill that slot. A read against the channel's message counts as none.
   - Buyer intent: ✅ when most top videos promise a result a product could deliver, 🟡 for some. Also ✅ when its average views beat peers earning well without promising results.
   - Audience capture: ✅ for a newsletter or community in most descriptions, with a free download to join. 🟡 when rarely linked or with nothing to join for.
   - Own products: ✅ for a linked product solving the problem the videos promise. 🟡 when it misses that problem or is not linked, ❌ when both.
   - Ad revenue: ✅ when videos average 8 minutes or more, 🟡 when some do.
7. The stack score is their average, ad revenue counting half.
8. Order actions: fast wins needing no other layer and deadlines first; then what another layer needs, like a list before a product; then the biggest win.
9. Each product idea sells a transformation viewers cannot get free from videos or social media, like "your first AI automation at work in 30 days", never information like a catch-up. Each solves a pain many viewers share or a top video's promise. Where jobs, money or health are at stake, one answers the fear behind the views, priced from a step 3 seller to the same viewers with a close problem. Price the rest from offers to these viewers, or "price untested".

## Output Format

One HTML page from this template, style block unchanged.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Revenue Maxxing: {channel}</title>
<style>
:root{--bg:#fff;--fg:#1c1c1c;--mut:#666;--line:#e3e3e3;--low:#d42a2a;--med:#c26a00;--high:#0c8a4d}
@media(prefers-color-scheme:dark){:root{--bg:#0f0f0f;--fg:#f1f1f1;--mut:#9a9a9a;--line:#2b2b2b;--low:#ff4e42;--med:#ffa400;--high:#3ddc97}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
main{max-width:920px;margin:auto;padding:32px 16px 72px}
a{color:inherit}
h1{font-size:24px;margin:0}
h2{font-size:19px;margin:44px 0 6px}
.mut{color:var(--mut)}
.center{text-align:center}
.low{--c:var(--low)}.med{--c:var(--med)}.high{--c:var(--high)}
.hero{display:flex;justify-content:center;align-items:center;gap:48px;flex-wrap:wrap;margin:40px 0 24px}
.gauge{position:relative;width:200px;font-weight:600;text-align:center}
.gauge svg{display:block;width:132px;margin:0 auto 8px;transform:rotate(-90deg)}
.gauge circle{fill:none;stroke:var(--line);stroke-width:8}
.gauge .arc{stroke:var(--c);fill:color-mix(in srgb,var(--c) 12%,transparent)}
.gauge b{position:absolute;top:0;left:0;width:100%;line-height:132px;font-size:44px;color:var(--c)}
.stack{display:flex;flex-direction:column;gap:6px;width:300px}
.layer{display:flex;justify-content:space-between;padding:10px 14px;border-radius:8px;border-left:6px solid var(--c);background:color-mix(in srgb,var(--c) 12%,transparent);font-weight:600}
.layer b{color:var(--c)}
.legend{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;font-size:13px}
.legend i,.row i{flex:none;display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--c)}
.big{font-size:19px;max-width:660px;margin:24px auto 8px}
.row{border-bottom:1px solid var(--line)}
.row>summary{display:flex;align-items:center;gap:12px;padding:13px 0;cursor:pointer;list-style:none}
.row>summary::-webkit-details-marker{display:none}
.row>summary::after{content:"+";color:var(--mut);width:12px;text-align:center}
.row[open]>summary::after{content:"\2212"}
.row span{flex:1}
.row b{color:var(--c)}
.row small{display:block;font-size:13px;color:var(--mut)}
.proof{padding:0 24px 18px 22px}
.proof p{margin:6px 0}
.proof ul{margin:6px 0;padding-left:20px}
.proof li{margin:4px 0}
.vids{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0}
.vids a{width:200px;font-size:13px;line-height:1.35;text-decoration:none}
.vids img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:8px;margin-bottom:6px;background:var(--line)}
blockquote{margin:10px 0;padding-left:12px;border-left:3px solid var(--line);color:var(--mut)}
ol{padding-left:22px}
li{margin:12px 0}
table{border-collapse:collapse;width:100%;margin-top:12px;font-size:15px}
td,th{text-align:left;vertical-align:top;padding:10px 12px 10px 0;border-bottom:1px solid var(--line)}
</style>
</head>
<body>
<main>
<h1>Revenue Maxxing: <a href="{url}">{channel}</a></h1>
<p class="mut">{run date} · {subscribers} subscribers · {monthly views} views a month · {revenue band} a month from ads · {n} peers compared · RPM, revenue and audience are estimates</p>
{No band for the channel: write "ad revenue not in the search hits", and never work one out from a peer's RPM. Ads turned on within the last month: add "ads turned on {date}, so it has not earned this yet".}

<div class="hero">
  <div class="gauge {low, med or high}"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="54"/><circle class="arc" cx="60" cy="60" r="54" pathLength="100" stroke-dasharray="{n} 100"/></svg><b>{n}</b>Stack score</div>
  <div class="stack">
    {The five layers, top to bottom: Own products, Audience capture, Buyer intent, Sponsors, Ad revenue. The class is high for ✅, med for 🟡, low for ❌.}
    <div class="layer {band}">{layer}<b>{✅ Strong, 🟡 Partial or ❌ Missing}</b></div>
  </div>
</div>
<div class="legend"><span class="low"><i></i> 0–39 weak</span><span class="med"><i></i> 40–69 partial</span><span class="high"><i></i> 70–100 strong</span></div>
<p class="big center">{biggest gap, one sentence with numbers}</p>
{Channel under a year old: add <p class="mut center">The score is low because the channel is new, not because it was neglected.</p>}

<h2>Actions, in order</h2>
{Up to five, in the order from step 8, one short sentence each. Only real gaps, never one the channel already does. The proof lives in the layers below.}
<ol>
  <li>{action}</li>
</ol>

<h2>Product ideas</h2>
{Three to five, strongest proof first. Only the name, type and price show; the rest sits in the collapsible.}
<details class="row">
  <summary><span>{product}<small>{app or SaaS, service, merch, tool, pack, course or community} · {price band}</small></span></summary>
  <div class="proof">
    <ul>
      <li><strong>Pain:</strong> {one sentence}</li>
      <li><strong>Proof:</strong> {a peer's offer, linked with its price, or a video on this problem with its views and ratio}</li>
      <li><strong>First test:</strong> {one cheap thing to try this week, such as a pinned comment or a first-line link to the offer}</li>
    </ul>
    <blockquote>"{a viewer's words}" · <a href="{comment's video url}">{video title}</a></blockquote> {one or two quotes; name the channel when the comment is on a peer's video}
  </div>
</details>

<h2>The stack, layer by layer</h2>
{One block per layer, weakest first, Ad revenue always last.}
<details class="row {band}">
  <summary><i></i><span>{layer}<small>{what this channel has, in a few words}</small></span><b>{✅, 🟡 or ❌}</b></summary>
  <div class="proof">
    <p><strong>Action:</strong> {one plain thing to try, or "Nothing to change" for a ✅ layer}</p>
    <ul>
      <li>{Found: what the channel does today, with links. Up to three bullets, one fact each}</li>
      <li>{Peers: what the best peers do, with links. Up to two bullets}</li>
    </ul>
    {Ad revenue only: a table with one row for the channel and one per peer, up to four, with the columns Channel, RPM band, Average length, Audience, Average views. The RPM band is context, never a gap. Write "not in the search hits" where a channel has no band.}
    <div class="vids">
      <a href="{video url}"><img src="{320px mqdefault.jpg}" alt="">{title} · {views, ratio, date}</a> {up to three videos that prove it}
    </div>
  </div>
</details>

<h2>More detail</h2>
<details class="row">
  <summary><span>All monetization methods<small>{n} checked, {gaps} not done yet</small></span></summary>
  <div class="proof">
    <p class="mut">❌ not done yet · ✅ already done · Money potential is an estimate.</p>
    {❌ rows first, highest potential on top. Up to twelve rows.}
    <table>
      <tr><th>Method</th><th>Inspiration</th><th>Money potential</th></tr>
      <tr><td>{❌ or ✅} {method}</td><td><a href="{offer link}">{offer}</a> on <a href="{url}">{channel}</a>, {price}</td><td>{High, Medium or Low}</td></tr>
    </table>
  </div>
</details>
<details class="row">
  <summary><span>Sponsors on channels like this<small>{n} brands</small></span></summary>
  <div class="proof">
    {Up to eight, the brand on the most peers first. Label an affiliate program as one, not as a sponsor. ✅ when this channel already works with the brand.}
    <ul>
      <li><a href="{the link the peer gives}">{brand}</a> {✅} · <a href="{url}">{channel}</a> (<a href="{video or moment url}">{sponsor read, or link in description}</a>)</li>
    </ul>
  </div>
</details>
</main>
</body>
</html>
```

- File: `revenue-maxxing-{handle}.html`, or an artifact.
- Chat: the score, biggest gap, first action and file.
- Product ideas: specific and plain: "RV park buying checklist", not "a course" or "chronotype plan". Apps when software fits.

## Common Pitfalls

- Suggest only sponsors the channel would recommend anyway, never one selling what it could sell or what its videos argue against.
- Do not over-maximize: strong channels get fewer actions.
- Under 10K subscribers, start with a free download, then a cheap product; sponsors wait; courses start as small groups. Affiliate links only when videos name costly things viewers buy, or peers link them.
- Monetize the content as it is: beyond buyer intent, never change visuals, voice, topics or format.
