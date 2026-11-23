---
name: reverse-engineer-niche
description: Use when the user wants to reverse engineer a YouTube niche, or a channel's competitors, into a guidelines report of its outliers, winning titles, thumbnails, hooks and scripts, the versions that flop, and video ideas. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "4.1"
  requires: tubelab-mcp
---

# Reverse Engineer Niche

## Overview

A niche taken apart through 12 to 20 channels, emerging ones first, as a niche guidelines book. Five lenses:

- **Working formats:** a new video must fit the format and length viewers already watch.
- **New and specific:** new enough to stop a scroll, specific enough to feel real: a price, a job, a place.
- **Anchors:** names, brands, tools or terms that tell YouTube which viewers to send.
- **Dead versions:** a winner's promise that flopped.
- **Who can copy it:** anyone, or only someone with its asset: experience, trust, credentials, a skill, fame or budget.

Not for last month's winners (`trend-report`), one channel (`reverse-engineer-channel`) or whether to enter (`niche-validator`).

**Without TubeLab:** no search for new or similar channels, no audience, income, lost-ads or terminated-channel data. The report covers only channels you already know.

## Workflow

1. Ask once, with any scope question: end with video ideas, for their channel or a new one here?
2. Run the searches below, up to 15, never paging one.
3. Verify each channel with a free read (it gives the avatar): on topic, long videos, the user's language. English titles can hide Hindi audio; the hit's audience region shows it. Keep 12 to 20.
4. Median each channel's last three months of long videos. Winners: its top three at twice that or more. Flops: under half, older than a month, trailing their neighbours. One set of totals everywhere.
5. Fill the audience and income page from channel hits only; video hits carry just ads and RPM.
6. View every winner's and every flop's thumbnail on contact sheets.
7. Group winners into three to five patterns, each on three or more channels, each winner explained against its channel's normal videos.
8. Count title formulas and thumbnail compositions across winners and flops. Rising: also in the trending search.
9. Read the opening 30 seconds of ten or more winners on different channels. A hook formula is a beat order, named to fit any video, shared by two or more channels.
10. Read four to six full winning transcripts from different patterns. Mark each beat and its time. A video formula is a layout two or more share.
11. Pair dead versions with their winners, same channel when you can, with the reason.
12. Count topics, sub-topics and power words: winning titles against flops. Worn out: as common in flops.
13. Run the risk searches and fill the risk page.
14. Blend two patterns into a new angle no sampled video has filmed.
15. Given a channel, find up to three gaps: patterns its competitors win with that it skips.
16. If wanted, run `video-ideation` on these findings for the last chapter. Unanswered: offer it in the closing line.

```jsonc
// One search per line. {niche}: one to three phrasings of one niche. {code}: the user's language.
// Keep publishedAtFrom and classificationQuality as written. Only the risk searches leave quality out.
// 10 searches as written. Spend the spare five on a second phrasing, a wider date range, or handle lookups
// ({ "query": ["@handle"] }, nothing else) for big sampled channels found only by video, so the audience page covers them.

// Channels created this year, then emerging channels.
{ "query": ["{niche}"], "language": ["{code}"], "publishedAtFrom": "trimester", "classificationQuality": "neutral", "joinedDateFrom": "year", "medianViewsFrom": 1000 }
{ "query": ["{niche}"], "language": ["{code}"], "publishedAtFrom": "trimester", "classificationQuality": "neutral", "subscribersFrom": 3000, "subscribersTo": 300000, "avgViewsToSubscribersRatioFrom": 1 }

// Outliers: small channels' breakouts, breakouts on channels with 30 videos or fewer, then established channels' breakouts.
{ "query": ["{niche}"], "language": ["{code}"], "type": "video", "publishedAtFrom": "trimester", "classificationQuality": "neutral", "averageViewsRatioFrom": 2, "subscribersCountFrom": 3000, "subscribersCountTo": 300000, "size": 40 }
{ "query": ["{niche}"], "language": ["{code}"], "type": "video", "publishedAtFrom": "trimester", "classificationQuality": "neutral", "averageViewsRatioFrom": 2, "channelVideoCountTo": 30, "subscribersCountFrom": 1000, "size": 40 }
{ "query": ["{niche}"], "language": ["{code}"], "type": "video", "publishedAtFrom": "trimester", "classificationQuality": "neutral", "averageViewsRatioFrom": 1.5, "subscribersCountFrom": 300000, "size": 40 }

// Similar channels, one seed per search: the best breakout, or the given channel. Several seeds blur into a generic set,
// and the hits are mostly small, recently found channels: established ones come from the outlier search above.
{ "relatedChannelId": ["<channelId>"], "language": ["{code}"], "publishedAtFrom": "trimester", "classificationQuality": "neutral", "subscribersFrom": 3000, "size": 40 }

// Outliers of similar channels, same seed.
{ "relatedChannelId": ["<channelId>"], "type": "video", "publishedAtFrom": "trimester", "classificationQuality": "neutral", "averageViewsRatioFrom": 2, "size": 40 }

// Trending title formulas whose use grew 10% or more over the previous period. English only: pass no language.
// Keep only formulas whose example titles fit the niche; the rest are generic.
{ "query": ["{niche}"], "lastVideosCountChangePercentageFrom": 10 }

// Risk, seeded with the three strongest emerging channels (live seeds work): similar channels terminated, then that lost ads.
{ "relatedChannelId": ["<channelId>", "<channelId>", "<channelId>"], "terminated": true, "publishedAtFrom": "year", "size": 40 }
{ "relatedChannelId": ["<channelId>", "<channelId>", "<channelId>"], "monetizationChanged": true, "monetizationAdsense": false, "publishedAtFrom": "year", "size": 40 }

// AI-made channels: count detections.madeWithAI on the channel hits above. A search filtered on it returns AI films, off topic.
```

## Output Format

One HTML book from this template, style and script unchanged. Repeat or drop page types as the data allows.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{Niche}: Niche Guidelines</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&amp;display=swap" rel="stylesheet">
<style>
:root{--paper:#000;--bg:#0e0e0e;--card:#1a1a1a;--fg:#f4f4f4;--mut:#9d9d9d;--line:#2e2e2e;--red:#ff4e42;--pw:min(100vw,177.78vh);--u:calc(var(--pw)/100);color-scheme:dark}
@media(prefers-color-scheme:light){:root{--paper:#e2e2e2;--bg:#fff;--card:#f1f1f1;--fg:#141414;--mut:#666;--line:#e0e0e0;--red:#e3241b;color-scheme:light}}
*{box-sizing:border-box;margin:0;padding:0}
html{background:var(--paper);scroll-snap-type:y mandatory;scrollbar-width:none}
body{background:var(--paper);color:var(--fg);font-family:Archivo,system-ui,sans-serif;display:flex;flex-direction:column;align-items:center;counter-reset:pg;-webkit-print-color-adjust:exact;print-color-adjust:exact}
a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}
.chapter{display:contents}
.page{position:relative;overflow:hidden;width:var(--pw);height:calc(var(--pw)*.5625);margin-block:calc((100vh - var(--pw)*.5625)/2);padding:calc(var(--u)*3.6) calc(var(--u)*5) calc(var(--u)*5);background:var(--bg);display:flex;flex-direction:column;gap:calc(var(--u)*1.8);scroll-snap-align:center;scroll-snap-stop:always;counter-increment:pg;font-size:calc(var(--u)*1.3);line-height:1.4}
.page::before,.page::after{position:absolute;bottom:calc(var(--u)*1.9);font-size:calc(var(--u)*.85);color:var(--mut);letter-spacing:.04em}
.page::before{content:var(--book) "  ·  " var(--ch);left:calc(var(--u)*5)}
.page::after{content:counter(pg);right:calc(var(--u)*5)}
.k{font-size:calc(var(--u)*.95);font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
h1{font-size:calc(var(--u)*6.4);font-weight:800;line-height:1;letter-spacing:-.02em}
h2{font-size:calc(var(--u)*2.7);font-weight:800;line-height:1.1;letter-spacing:-.01em}
.lead{font-size:calc(var(--u)*1.9);font-weight:600;line-height:1.3}
.big{font-size:calc(var(--u)*4.6);font-weight:800;line-height:1}
.mut{color:var(--mut)}
small{font-size:calc(var(--u)*.95)}
.f{font-size:calc(var(--u)*3.1);font-weight:800;line-height:1.3;letter-spacing:-.01em}
mark{background:var(--red);color:#fff;padding:0 .25em;border-radius:.25em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.fill{flex:1;min-height:0;align-content:space-evenly}
.col.fill{justify-content:space-evenly}
.split{flex:1;min-height:0;display:grid;grid-template-columns:1.2fr 1fr;gap:calc(var(--u)*4);align-items:center}
.col{display:flex;flex-direction:column;gap:calc(var(--u)*1.4);min-width:0}
.g2,.g3{display:grid;gap:calc(var(--u)*1.6);align-content:start}
.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}
.kv{display:grid;grid-template-columns:auto 1fr;gap:calc(var(--u)*.9) calc(var(--u)*2);align-content:start}
.kv dt{color:var(--mut);font-size:calc(var(--u)*1);font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding-top:.3em}
.v{display:flex;flex-direction:column;gap:calc(var(--u)*.4);font-size:calc(var(--u)*1.05);line-height:1.3;min-width:0;background:var(--card);border-radius:calc(var(--u)*.9);padding:calc(var(--u)*.65)}
.v img,.wall img,.anno img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:calc(var(--u)*.6);background:var(--line)}
.v b,.r{align-self:flex-start;display:inline-block;width:fit-content;background:var(--red);color:#fff;font-weight:800;line-height:1;padding:.2em .4em;border-radius:.35em;white-space:nowrap}
.v b{font-size:calc(var(--u)*1.4)}
.r{font-size:.9em}
.x+b,.x+div>b,.no b,.r.lo{background:var(--bg);color:var(--mut);box-shadow:inset 0 0 0 1px var(--line)}
.v span{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.v small{color:var(--mut)}
.one .v span{-webkit-line-clamp:1}
.tight .col{gap:calc(var(--u)*.8)}.tight .legend,.tight .kv{font-size:calc(var(--u)*1.15)}.tight .legend{gap:calc(var(--u)*.5)}.tight .kv{gap:calc(var(--u)*.6) calc(var(--u)*2)}.one small{font-size:calc(var(--u)*.85)}
.v.h{display:grid;grid-template-columns:calc(var(--u)*14) 1fr;gap:calc(var(--u)*1);align-items:start}
.v.h>div{display:flex;flex-direction:column;gap:calc(var(--u)*.35)}
.v p{font-size:calc(var(--u)*1.05);line-height:1.35}
.vs{flex:1;min-height:0;display:grid;grid-template-columns:repeat(2,minmax(0,calc(var(--u)*36)));justify-content:space-around;align-content:center;gap:calc(var(--u)*5)}
.vs .v{gap:calc(var(--u)*.8);font-size:calc(var(--u)*1.2);padding:calc(var(--u)*1.4)}
.vs .v>div:first-child{display:flex;justify-content:space-between;align-items:center}
.vs .v b{align-self:center;font-size:calc(var(--u)*3.4)}
.x{position:relative;display:block}
.x::after{content:"";position:absolute;inset:0;border-radius:calc(var(--u)*.6);box-shadow:inset 0 0 0 calc(var(--u)*.22) var(--red);background:linear-gradient(to top right,transparent 49.4%,var(--red) 49.4% 50.6%,transparent 50.6%),linear-gradient(to top left,transparent 49.4%,var(--red) 49.4% 50.6%,transparent 50.6%)}
.anno{position:relative}
.anno i{position:absolute;border:calc(var(--u)*.22) solid var(--red);border-radius:calc(var(--u)*.5)}
.anno i::before{content:attr(data-n);position:absolute;left:calc(var(--u)*-.22);top:calc(var(--u)*-.22);background:var(--red);color:#fff;font:800 calc(var(--u)*1)/1 Archivo,system-ui,sans-serif;padding:calc(var(--u)*.35) calc(var(--u)*.55);border-radius:calc(var(--u)*.4) 0 calc(var(--u)*.4) 0}
.legend{list-style:none;counter-reset:n;display:flex;flex-direction:column;gap:calc(var(--u)*1)}
.legend li{counter-increment:n;display:flex;gap:calc(var(--u)*1);align-items:baseline}
.legend li::before{content:counter(n);flex:none;background:var(--red);color:#fff;font-weight:800;font-size:calc(var(--u)*.9);width:calc(var(--u)*1.8);height:calc(var(--u)*1.8);border-radius:50%;display:grid;place-items:center;transform:translateY(-.1em)}
.beats{display:flex;flex-wrap:wrap;gap:calc(var(--u)*1) calc(var(--u)*3)}
.beats span{position:relative;border:calc(var(--u)*.14) solid var(--line);border-radius:calc(var(--u)*.6);padding:calc(var(--u)*.7) calc(var(--u)*1.2);font-size:calc(var(--u)*1.7);font-weight:700}
.beats span+span::before{content:"→";position:absolute;left:calc(var(--u)*-2.3);color:var(--mut)}
.q{border-left:calc(var(--u)*.2) solid var(--line);padding-left:calc(var(--u)*1.4);display:flex;flex-direction:column;gap:calc(var(--u)*.5)}
.q p{font-size:calc(var(--u)*1.45)}
.q p>b{color:var(--mut);font-size:calc(var(--u)*.85);letter-spacing:.1em;text-transform:uppercase;margin-right:.6em}
.gantt{display:grid;grid-template-columns:auto 1fr;gap:calc(var(--u)*.7) calc(var(--u)*1.6);align-items:center;font-size:calc(var(--u)*1.15)}
.gantt div{position:relative;height:calc(var(--u)*1.5);background:var(--card);border-radius:calc(var(--u)*.3)}
.gantt div i{position:absolute;inset-block:0;left:calc(var(--a)*1%);width:max(calc(var(--u)*.6),calc((var(--b) - var(--a))*1%));background:var(--fg);border-radius:calc(var(--u)*.3)}
.gantt .pay i{background:var(--red)}
.chips{display:flex;flex-wrap:wrap;gap:calc(var(--u)*.8);align-content:start}
.chip{border:calc(var(--u)*.12) solid var(--line);border-radius:calc(var(--u)*.8);padding:calc(var(--u)*.6) calc(var(--u)*1.1);font-size:calc(var(--u)*1.15)}
div.chip>b{background:var(--red);color:#fff;padding:0 .35em;border-radius:.3em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.chip.worn>b{background:var(--card);color:var(--mut);text-decoration:line-through;box-shadow:inset 0 0 0 1px var(--line)}
.tag{font-size:calc(var(--u)*1.05);font-weight:800;letter-spacing:.14em;text-transform:uppercase}
.no .tag{color:var(--red)}
.t{width:100%;border-collapse:collapse;font-size:calc(var(--u)*1.15)}
.t td,.t th{text-align:left;padding:calc(var(--u)*.65) calc(var(--u)*1.2) calc(var(--u)*.65) 0;border-bottom:calc(var(--u)*.08) solid var(--line);vertical-align:top}
.t th{color:var(--mut);font-size:calc(var(--u)*.85);letter-spacing:.1em;text-transform:uppercase}
.chans{display:grid;grid-template-columns:repeat(4,1fr);gap:calc(var(--u)*.9);align-content:start}
.chans a{background:var(--card);border-radius:calc(var(--u)*.6);padding:calc(var(--u)*.8) calc(var(--u)*1.1);font-size:calc(var(--u)*1);line-height:1.35}
.chans b{display:block;font-size:calc(var(--u)*1.15)}
.chans .av{float:left;margin:calc(var(--u)*.15) calc(var(--u)*.8) 0 0;width:calc(var(--u)*2.6);height:calc(var(--u)*2.6);border-radius:50%;object-fit:cover;background:var(--line)}
.chans .me{box-shadow:inset 0 0 0 calc(var(--u)*.15) var(--fg)}
.cover{justify-content:flex-end}
.cover::before{display:none}
.wall{position:absolute;inset:-12% -6% -12% 22%;display:grid;grid-template-columns:repeat(4,1fr);gap:calc(var(--u)*.8);transform:rotate(-8deg);opacity:.75}
.cover .shade{position:absolute;inset:0;background:linear-gradient(90deg,var(--bg) 34%,transparent 75%),linear-gradient(0deg,var(--bg) 4%,transparent 40%)}
.cover>div:last-child{position:relative;display:flex;flex-direction:column;gap:calc(var(--u)*1.4);max-width:60%}
.divider{justify-content:center}
.divider .n{font-size:calc(var(--u)*13);font-weight:800;line-height:.9;color:transparent;-webkit-text-stroke:calc(var(--u)*.12) var(--mut)}
.divider h1{font-size:calc(var(--u)*7)}
code{font-family:ui-monospace,Menlo,monospace;font-size:.9em;background:var(--card);padding:.1em .4em;border-radius:.3em}
@media screen and (max-width:760px){
:root{--pw:100vw;--u:11px}
html{scroll-snap-type:none}
.page{width:100%;height:auto;min-height:0;margin:0 0 10px;padding:28px 16px 48px}
.page::before{left:16px;bottom:16px}.page::after{right:16px;bottom:16px}
.split,.g2,.g3,.vs{grid-template-columns:1fr}.chans{grid-template-columns:1fr 1fr}.vs{gap:16px}
.cover{min-height:80vh}h1{font-size:42px}.divider h1{font-size:52px}.cover>div:last-child{max-width:none}.wall{inset:-10% -30% 40% -10%}.cover .shade{background:linear-gradient(0deg,var(--bg) 55%,transparent 90%)}
.divider{min-height:60vh}
.beats{padding-left:28px}
}
@page{size:16in 9in;margin:0}
.page{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 fill=%22none%22 viewBox=%220 0 22 22%22%3E%3Cmask id=%22tlm%22 width=%2222%22 height=%2222%22 x=%220%22 y=%220%22 maskUnits=%22userSpaceOnUse%22 style=%22mask-type:alpha%22%3E%3Cpath fill=%22%23E40000%22 d=%22M22 2.095C22 .938 21.105 0 20 0H2C.895 0 0 .938 0 2.095V22L11 3.143 22 22V2.095Z%22/%3E%3Cpath fill=%22url%28%23tlg%29%22 d=%22M0 2.095C0 .938.895 0 2 0h9v19.905C11 21.062 10.105 22 9 22H0V2.095Z%22/%3E%3C/mask%3E%3Cg mask=%22url%28%23tlm%29%22%3E%3Cellipse cx=%2211%22 cy=%2211.352%22 fill=%22%23E40000%22 rx=%2210.5%22 ry=%2211%22/%3E%3C/g%3E%3Cdefs%3E%3ClinearGradient id=%22tlg%22 x1=%2211%22 x2=%22-1.938%22 y1=%2222%22 y2=%221.894%22 gradientUnits=%22userSpaceOnUse%22%3E%3Cstop stop-color=%22%23FFCBCB%22 stop-opacity=%22.18%22/%3E%3Cstop offset=%221%22 stop-color=%22%23E40000%22/%3E%3C/linearGradient%3E%3C/defs%3E%3C/svg%3E");background-repeat:no-repeat;background-size:calc(var(--u)*1.1);background-position:left calc(var(--u)*5) bottom calc(var(--u)*1.75)}
.page::before{left:calc(var(--u)*6.6)}
.cover{background-image:none}
.tl{position:absolute;top:calc(var(--u)*3.6);left:calc(var(--u)*5);z-index:2;display:flex;align-items:center;gap:calc(var(--u)*.6);color:var(--fg)}
.tl svg:first-child{height:calc(var(--u)*2.2)}.tl svg:last-child{height:calc(var(--u)*1.5)}
@media print{:root{--pw:16in}html{scroll-snap-type:none}body{display:block}.page{margin:0;break-after:page}}
</style>
</head>
<body style="--book:'{Niche}: Niche Guidelines'">
{CARD: <div class="v"><a href="{video url}"><img src="https://i.ytimg.com/vi/{id}/hqdefault.jpg" alt=""></a><b>{ratio}×</b><a href="{video url}"><span>{title}</span></a><small><a href="{channel url}">{channel}</a> · {views} views · {date}</small></div>
{ratio}: views ÷ the channel's three-month median from step 4, the number that picks winners and flops, on every badge and ratio. Never print TubeLab's averageViewsRatio.
ROW CARD: the same with class="v h", everything after the image link in one <div>, and <p>{why, one line}</p> last when the page asks for it. FLOP: class="x" on the image link crosses it out.
Any other ratio, outside a card: <b class="r">{ratio}×</b>, class="r lo" for a flop's.
PAGE: <section class="page"><p class="k">{Chapter · section}</p><h2>{title}</h2>{body}</section>. Each body below is one page. A page that overflows becomes two pages.}
<div class="chapter" style="--ch:'Cover'">
<section class="page cover">
<a class="tl" href="https://tubelab.net" aria-label="TubeLab"><svg viewBox="0 0 22 22" fill="none"><mask id="tlm" width="22" height="22" x="0" y="0" maskUnits="userSpaceOnUse" style="mask-type:alpha"><path fill="#E40000" d="M22 2.095C22 .938 21.105 0 20 0H2C.895 0 0 .938 0 2.095V22L11 3.143 22 22V2.095Z"/><path fill="url(#tlg)" d="M0 2.095C0 .938.895 0 2 0h9v19.905C11 21.062 10.105 22 9 22H0V2.095Z"/></mask><g mask="url(#tlm)"><ellipse cx="11" cy="11.352" fill="#E40000" rx="10.5" ry="11"/></g><defs><linearGradient id="tlg" x1="11" x2="-1.938" y1="22" y2="1.894" gradientUnits="userSpaceOnUse"><stop stop-color="#FFCBCB" stop-opacity=".18"/><stop offset="1" stop-color="#E40000"/></linearGradient></defs></svg><svg viewBox="0 0 69 15" fill="none"><path fill="currentColor" d="M15.736 9.769V4.131h2.723v9.818h-2.614v-1.783h-.102a2.899 2.899 0 0 1-1.106 1.387c-.512.35-1.136.524-1.873.524-.656 0-1.234-.149-1.732-.447a3.076 3.076 0 0 1-1.17-1.272c-.277-.55-.418-1.208-.422-1.975V4.13h2.723v5.766c.004.58.16 1.037.467 1.374.306.337.718.505 1.233.505.328 0 .635-.074.92-.224.286-.153.516-.379.691-.677.18-.298.266-.667.262-1.106ZM20 13.95V.858h.723a2 2 0 0 1 2 2V5.78h.083a3.6 3.6 0 0 1 .518-.805 2.73 2.73 0 0 1 .895-.69c.37-.188.83-.282 1.38-.282a3.69 3.69 0 0 1 1.982.563c.605.37 1.089.931 1.451 1.681.362.746.543 1.681.543 2.806 0 1.095-.177 2.020-.53 2.774-.35.75-.827 1.32-1.432 1.707-.6.383-1.274.575-2.020.575-.528 0-.978-.087-1.349-.262a2.79 2.79 0 0 1-.901-.658 3.347 3.347 0 0 1-.537-.812h-.121v1.572H20Zm2.666-4.91c0 .584.08 1.093.242 1.528.162.435.397.774.703 1.016.307.239.68.358 1.12.358.442 0 .817-.121 1.124-.364.307-.247.54-.588.697-1.023.162-.439.243-.944.243-1.515 0-.566-.08-1.065-.237-1.495-.157-.43-.39-.767-.697-1.01-.306-.243-.683-.365-1.13-.365-.444 0-.82.118-1.126.352-.302.234-.535.567-.697.997-.162.43-.242.938-.242 1.521ZM35.795 14.141c-1.010 0-1.879-.204-2.608-.613a4.203 4.203 0 0 1-1.674-1.752c-.392-.758-.588-1.655-.588-2.69 0-1.010.196-1.897.588-2.66a4.347 4.347 0 0 1 1.655-1.783c.716-.427 1.556-.64 2.519-.64.648 0 1.25.105 1.809.314a4.013 4.013 0 0 1 1.47.926c.422.414.75.934.984 1.56.235.622.352 1.351.352 2.186a.748.748 0 0 1-.748.748l-5.938.006V8.14l4.123-.09c0-.391-.086-.739-.256-1.041a1.832 1.832 0 0 0-.71-.71 2.024 2.024 0 0 0-1.042-.262c-.413 0-.78.096-1.099.288a2.017 2.017 0 0 0-.741.76c-.18.316-.271.667-.275 1.055v1.604c0 .486.09.906.268 1.26.184.353.441.626.774.818.332.192.726.287 1.182.287.303 0 .58-.042.831-.127.252-.085.467-.213.646-.384.179-.17.315-.38.409-.626l2.518.166a3.438 3.438 0 0 1-.786 1.585c-.392.448-.9.797-1.521 1.049-.618.247-1.332.37-2.142.37ZM42 13.95V.858h.768a2 2 0 0 1 2 2v8.809h2.326c.281 0 .525.193.588.467.197.844.83 1.518 1.66 1.767l.158.047H42ZM51.97 14.135c-.626 0-1.184-.109-1.674-.326a2.696 2.696 0 0 1-1.163-.978c-.281-.435-.422-.976-.422-1.624 0-.545.1-1.003.3-1.374.2-.37.473-.67.819-.895a3.97 3.97 0 0 1 1.176-.511 8.967 8.967 0 0 1 1.393-.243c.571-.06 1.031-.115 1.38-.166.35-.056.604-.137.761-.243a.534.534 0 0 0 .237-.473v-.039c0-.404-.128-.718-.383-.94-.252-.22-.61-.332-1.074-.332-.49 0-.88.109-1.17.326a1.5 1.5 0 0 0-.575.806l-2.519-.205c.128-.596.38-1.112.754-1.547a3.62 3.62 0 0 1 1.451-1.010c.597-.238 1.287-.358 2.071-.358.546 0 1.068.064 1.566.192.503.128.949.326 1.336.595.392.268.701.613.927 1.035.226.418.339.918.339 1.502v6.622h-2.582v-1.361h-.077a2.77 2.77 0 0 1-.633.812 2.93 2.93 0 0 1-.952.543c-.371.128-.8.192-1.285.192Zm.78-1.88c.401 0 .755-.078 1.062-.236a1.88 1.88 0 0 0 .722-.652c.175-.273.262-.582.262-.927V9.398a1.46 1.46 0 0 1-.351.154 6.404 6.404 0 0 1-.493.121c-.183.034-.366.066-.55.096l-.498.07c-.32.047-.599.122-.837.224-.239.102-.424.24-.556.416-.132.17-.199.383-.199.639 0 .37.135.654.403.85.273.192.618.287 1.036.287ZM58.925 13.95V.858h.723a2 2 0 0 1 2 2V5.78h.083a3.6 3.6 0 0 1 .518-.805 2.73 2.73 0 0 1 .895-.69c.37-.188.83-.282 1.38-.282a3.69 3.69 0 0 1 1.982.563c.605.37 1.088.931 1.45 1.681.363.746.544 1.681.544 2.806 0 1.095-.177 2.020-.53 2.774-.35.75-.827 1.32-1.432 1.707-.601.383-1.275.575-2.020.575-.529 0-.978-.087-1.349-.262a2.79 2.79 0 0 1-.901-.658 3.345 3.345 0 0 1-.537-.812h-.122v1.572h-2.684Zm2.665-4.91c0 .584.081 1.093.243 1.528.162.435.396.774.703 1.016.307.239.68.358 1.119.358.443 0 .818-.121 1.125-.364.307-.247.539-.588.697-1.023.161-.439.242-.944.242-1.515 0-.566-.078-1.065-.236-1.495-.158-.43-.39-.767-.697-1.010-.307-.243-.684-.365-1.131-.365-.443 0-.818.118-1.125.352-.303.234-.535.567-.697.997-.162.43-.243.938-.243 1.521Z"/><path fill="currentColor" d="M11.605 1.753a3 3 0 0 1-2.296 1.068H6.596V14.24H4.079V2.82H0V.761h12.44l-.835.992Z"/></svg></a>
<div class="wall">{16 winners: <a href="{video url}"><img src="{hqdefault}" alt=""></a>}</div><div class="shade"></div>
<div><p class="k">{Competitors of <a href="{url}">{channel}</a> · }{run date}</p><h1>{Niche}:<br><span class="mut">Niche Guidelines</span></h1>
<p class="lead">What wins, what flops and how to make it, from {n} winners and {n} flops.</p>
<p class="mut">{n} channels: {n} emerging and {n} established · {n} videos cited</p></div>
</section>
</div>
<div class="chapter" style="--ch:'Research'">
<section class="page divider"><p class="n">01</p><h1>Research</h1><p class="lead mut">The niche · Working formats · The channels · Who watches, and how it pays · Outliers · What to avoid · What got similar channels in trouble · Patterns that work</p></section>
{The niche: <div class="split"><div class="col"><p class="lead">{what it is}</p><dl class="kv"><dt>Who watches</dt><dd>{the most common age, gender, income tier and region across the channel hits, as an estimate}</dd><dt>What wins</dt><dd>{with numbers}</dd><dt>Start with</dt><dd>{the pattern to make first, and why}</dd></dl></div><div class="col">{CARD}</div></div>}
{Working formats: the same split. kv: Format, Length, Faceless or on camera ({n} of {n} winners are on faceless channels, from the hits and checked on the thumbnails), Where to differ. Right: <div class="g2">{four CARDs}</div>}
{The channels, h2 "{n} channels: {n} emerging, {n} established": <div class="chans"><a{ class="me" for the given channel} href="{url}"><img class="av" src="{avatar url}" alt=""><b>{channel}</b>{emerging or established} · {subs} subscribers<br><span class="mut">median {views} views · {ratio} per subscriber</span></a></div><p class="mut"><small>Medians cover each channel's last three months of long videos. Left out: {channels and why}.</small></p>}
{Who watches and how it pays, h2 "Who watches, and how it pays": <div class="split"><div class="col"><p class="k">Who watches</p><dl class="kv"><dt>Age</dt><dd>{most common band} · {n} of {n} channels</dd><dt>Gender</dt><dd>{male, female or balanced} · {n} of {n}</dd><dt>Income</dt><dd>{low, middle, upper-middle or high} · {n} of {n}</dd><dt>Region</dt><dd>{region} · {n} of {n}</dd></dl></div><div class="col"><p class="k">How it pays</p><dl class="kv"><dt>Ads on</dt><dd>{n} of {n} channels</dd><dt>RPM</dt><dd>{band}</dd><dt>Also earn from</dt><dd><div class="chips">{one per detected method (sponsors, affiliate links, products, courses, newsletter, community, services, donations): <div class="chip"><b>{method}</b> · {n} channels</div>}</div></dd></dl></div></div><p class="mut"><small>Estimates from TubeLab's channel search, for {n} of the {n} channels. No estimate for: {channels found only through a video search}. {If the fields come back empty: "not available on this plan".}</small></p>}
{Outliers, two pages of six: <div class="g2 fill">{ROW CARDs with why}</div><p class="mut"><small>{n} of {n} are also outliers against their channel's whole list, by TubeLab's flag. The rest are recent wins only: {titles}.</small></p>}
{What to avoid: <p class="lead">{what the flops share}</p><div class="g2 fill">{six FLOP ROW CARDs with why}</div>}
{What got similar channels in trouble, from the risk searches. Keep only channels that share a sampled title formula or thumbnail style. If none is close, one line saying so: <p class="lead">{n} similar channels were terminated and {n} lost ads in the last year. {what their formats share}</p><div class="g2 fill">{one ROW CARD per channel, up to six, for the video it is cited by: <b class="r lo">{terminated | lost ads {Mon YYYY}}</b> in place of the ratio, a terminated channel's image from https://cdn.tubelab.net/vi/{id}.jpeg, <small> with the channel only, and <p>{its title formula, slots in [ ], and its look}</p> last. Four fit under the lead; the rest and the note go on a page headed "What got similar channels in trouble, continued"}</div><p class="mut"><small>The data shows what happened, never why. AI-made channels found in the niche: {n}, {n} of them classed low effort. They share: {format}.</small></p> Never print this note: a terminated channel's thumbnails load from https://cdn.tubelab.net/vi/{id}.jpeg.}
{One page per pattern, h2 = its name: <p class="mut">{n} winners on {n} channels</p><div class="split"><div class="col"><dl class="kv">{Angle, New and specific, Title (formula, slots in <mark>[ ]</mark>), Thumbnail (composition name), Hook (formula name), Script (video formula name, only when read), Who can copy}</dl></div><div class="col">{three ROW CARDs}</div></div>}
</div>
<div class="chapter" style="--ch:'Packaging'">
<section class="page divider"><p class="n">02</p><h1>Packaging</h1><p class="lead mut">Anatomy of an outlier · Title formulas · Winning words · Thumbnail design</p></section>
{Anatomy of an outlier: <div class="split"><div class="col">{ANNOTATED}</div><div class="col"><p class="f">{its title, the slots in <mark></mark>}</p><p class="mut">{channel · views · date · ratio}</p><dl class="kv">{In the title, In the picture, Always}</dl></div></div>}
{ANNOTATED, boxing what matters on one real thumbnail (face, payout screen, amount, arrow), in percent of the image: <a class="anno" href="{video url}"><img src="{hqdefault}" alt=""><i data-n="1" style="left:{x}%;top:{y}%;width:{w}%;height:{h}%"></i></a><ol class="legend"><li>{what box 1 holds, <strong>words on it</strong>}</li></ol>}
{One page per title formula, no h2: <p class="f">"{formula, slots in <mark>[ ]</mark>}"</p><div class="split"><div class="col"><p><span class="big">{n}</span> winners on {n} channels</p><p><span class="big">{n}</span> flops</p><p class="mut">{Rising across YouTube: {n} videos use it, {ratio}× on average, use up 10% or more · click triggers: {triggers} | Seen in this niche only}</p></div><div class="col">{three ROW CARDs}</div></div>}
{More formulas, four a page: <div class="g2 fill"><div class="col"><p class="lead">"{formula}"</p><p class="mut">{counts}</p>{ROW CARD}</div></div>}
{Worn out, two a page: <div class="col"><p class="lead">"{formula}"</p><p class="mut">{counts}</p><div class="g2">{winner ROW CARD}{FLOP ROW CARD}</div></div>}
{Winning words: <div class="g3 fill"><div class="col" style="grid-column:span 2"><p class="k">Win</p><div class="g2">{CHIPs}</div></div><div class="col"><p class="k">Worn out: as common in flops</p><div class="chips">{CHIPs with class="chip worn"}</div></div></div>
CHIP: <div class="chip"><b>{word or topic}</b> · {n} winners, {n} channels, {n} flops<br><small class="mut">e.g. <a href="{video url}">{title}</a> · <b class="r">{ratio}×</b></small></div>}
{One page per thumbnail composition, h2 = its name: <p class="mut">{n} winners on {n} channels · {n} flops</p><div class="split tight"><div class="col">{ANNOTATED, legend moved right}<small class="mut">{proof}</small></div><div class="col">{legend}<dl class="kv"><dt>Text and colour</dt><dd>..</dd><dt>Why it likely works</dt><dd>..</dd></dl><div class="g2 one">{two CARDs}</div></div></div>}
</div>
<div class="chapter" style="--ch:'Storytelling'">
<section class="page divider"><p class="n">03</p><h1>Storytelling</h1><p class="lead mut">Hook formulas · Video formulas</p></section>
{One page per hook formula, h2 = its name: <p class="mut">{n} of {n} openings read, on {n} channels · the first {n} seconds · Who can copy: {..}</p><div class="beats"><span>{beat}</span><span>{beat}</span></div><div class="g2 fill"><div class="q"><small><a href="{video url}&amp;t=0s">{title}</a> · {channel · views · date · ratio}</small><p><b>{Beat}</b>"{its words}"</p></div></div>}
{One page per video formula, h2 = its name: <p class="mut">{n} of {n} scripts read</p><div class="split"><div class="col"><div class="gantt"><span><strong>{Beat: Hook, Setup, Re-hook, Stakes increase, Peak, Twist or Payoff}</strong> <span class="mut">{what happens}</span></span><div{ class=pay on the main payoff}><i style="--a:{start %};--b:{end %}"></i></div><span></span><span class="mut" style="display:flex;justify-content:space-between;font-size:.8em"><span>0%</span><span>50%</span><span>100% of the runtime</span></span></div></div><div class="col"><dl class="kv">{Main payoff, What repeats, Example: linked title, its stats and length}</dl><div class="chips"><a class="chip" href="{video url}&amp;t={s}s"><b>{m:ss}</b> {beat}</a></div></div></div>}
</div>
<div class="chapter" style="--ch:'Learnings'">
<section class="page divider"><p class="n">04</p><h1>Learnings</h1><p class="lead mut">Do's and don'ts · New angles{ · Gaps to win}</p></section>
{One page per pair, h2 = the lesson: <div class="vs"><div class="v yes"><div><span class="tag">✓ Do</span><b>{ratio}×</b></div><a href="{video url}"><img src="{hqdefault}" alt=""></a><a href="{video url}"><span>{title}</span></a><small>{channel · views · date}</small></div><div class="v no">{the dead version, the same with ✕ Don't and class="x" on its image link}</div></div><p class="lead">{the reason}</p>}
{One page per new angle, two patterns blended, h2 = the angle: <div class="split"><div class="g2"><div class="col"><p class="k">{pattern}</p>{CARD}</div><div class="col"><p class="k">+ {pattern}</p>{CARD}</div></div><div class="col"><dl class="kv">{New angle, Why it should work, Filmed yet? (not in the {n} videos counted)}</dl></div></div>}
{Given a channel: one page per gap, h2 = the gap: <div class="split"><div class="g2">{two competitor CARDs}</div><div class="col"><dl class="kv">{Their proof, Why it fits}</dl></div></div>. Then a page "Overall": kv of Copy, Avoid, Position, each <span class="lead"></span>.}
</div>
<div class="chapter" style="--ch:'Video ideas'">
{Only after video-ideation ran.}
<section class="page divider"><p class="n">05</p><h1>Video ideas</h1><p class="lead mut">{how many ideas, for whom, from what}</p></section>
{Overview: <table class="t"><tr><th>#</th><th>Idea</th><th>From</th><th>Potential</th><th>Fit</th></tr></table>}
{One page per idea, h2 = "{title}". Each takes a title formula, composition and hook from this report: <div class="split"><div class="col"><dl class="kv">{From, Title formula, Thumbnail (composition: its parts for this video), Hook (formula: its beats for this video), Avoids (linked dead version, ratio, why), Potential · Fit}</dl></div><div class="col"><p class="k">Proof</p>{CARD}</div></div>}
<section class="page"><p class="k">Next steps</p><h2>What to run next</h2><div class="col fill"><div><p><code>{skill}</code> <strong>{what to do}</strong></p><p class="mut">"{a prompt to paste, [brackets] for what the user fills in}"</p></div></div><p class="mut"><small>Made with the YouTube research skills on the <a href="https://tubelab.net/youtube-mcp">TubeLab MCP</a> · Install: <code>npx skills add TubeLabHQ/youtube-research-skills</code></small></p></section>
</div>
<script>
const P=[...document.querySelectorAll('.page')];
addEventListener('keydown',e=>{const d={ArrowRight:1,ArrowDown:1,PageDown:1,ArrowLeft:-1,ArrowUp:-1,PageUp:-1}[e.key];if(!d||innerWidth<=760)return;e.preventDefault();const m=scrollY+innerHeight/2,i=P.findIndex(p=>p.offsetTop+p.offsetHeight>m);(P[i+d]||P[i]).scrollIntoView({behavior:'smooth',block:'center'})});
</script>
</body>
</html>
```

- File: `reverse-engineer-niche-{niche-slug or handle}.html`, or an artifact. Chat: the top finding and the file.
- Plain, short language, with causes stated as likely. One idea and a few lines per page.
- Link every video, channel and moment from the data.
- Spell formulas and compositions out where used, never by page number.

## Common Pitfalls

- Do not call one channel's hits a pattern. One viral video proves the idea, not the channel.
- Do not sell a pattern seen only on established channels to a new channel. It may ride on trust.
- Do not say why a channel was terminated or lost ads. The data does not show why.
