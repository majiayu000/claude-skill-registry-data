---
name: page-diagnose
description: Diagnose why a web page or a Paper design looks flat, cluttered or badly made. Measures it against well-regarded pages of the same type and writes each problem up as a short lesson with a marked picture. Use to diagnose a page or site, compare a design before and after, check a page against house design rules, or run the tool's evals.
---

`node ~/.claude/skills/page-diagnose/diagnose.mjs <url>` measures a page at 1440 and 390 in its own browser tab (read-only: it never clicks, types or submits) and compares it with reference pages **of the same page type**. A problem is something the page does that none of the references do. It launches its own headless Chrome and closes it when the run ends; it never drives the Synth app's browser (port 9300 is refused).

## Branches

- **A page**: `diagnose.mjs <url> --html report.html`. Prints one line per problem; the HTML is the lesson report. The type is detected (home, listing, detail, availability, cart, checkout, form, table, article, landing); pass `--type` when the first line says it guessed wrong.
- **A Paper frame**: the address is `paper:<fileId>/<frameId>`, measured at the frame's own width. Hover, press, focus and input checks are reported as not applicable to a design.
- **Several pages in one report**: run each with `--out <dir>`, then `diagnose.mjs report <dir>/run.json… --html report.html`.
- **Your own references**: `--against listing=<url> …` for one run, or `diagnose.mjs refs build <set> home=<url> listing=<url> …` then `--refs <set>`. The default set is `travel`. → [`PROFILES.md`](PROFILES.md)
- **House rules** (absolute limits, house wording for fixes): `--profile house.json`; exit code 2 when a rule fails. → [`PROFILES.md`](PROFILES.md)
- **Before and after**: `diagnose.mjs diff before/run.json after/run.json`; exit code 1 when it got worse.
- **A state behind a click** (a dialog, a drawer): `--inject open.js` runs your script in the page before measuring. Open only states that change nothing.
- **What a number means, or a check looks wrong** → [`METRICS.md`](METRICS.md). **Is the tool right?** → [`EVALS.md`](EVALS.md), `node eval.mjs all`.

## What a report must be

A run is done when its report meets every line. The collector and the report builder enforce the first four; the last is yours.

- **Every picture is a settled capture.** A page still showing skeletons, spinners or missing pictures, or one that renders blank, is not measured (exit 3, with the reason). Report that page as not captured; never show a loading state.
- **Every reference is the same kind of thing** as what it sits beside: a cart beside a cart. With no like-for-like reference the report shows none and says so.
- **Every finding is a lesson a junior designer could act on**: what we see with specifics, the picture with the problem boxed, the number in words, why it matters, what good looks like, how to fix it here, how sure we are. The words come from [`lib/lessons.mjs`](lib/lessons.mjs), one entry per check; a finding without an entry, specifics or a marked picture is left out and named on stderr.
- **Plain words only**: no scores, no check names, no term the reader has to look up.
- **You look through the finished report, every picture and every pairing, before showing it to anyone**, and say in your hand-off which pairings you looked at and which findings were left out.

## Limits

It measures what can be measured and cannot judge taste. Each finding stands on its own check's record (the report says it under "how sure we are"); the findings do not add up to a score, and pages or sites must not be ranked by them: on sites the tool was not tuned on, well-regarded and poor pages total about the same ([`EVALS.md`](EVALS.md)). Bot walls and logins stop it: it reports the page as blocked and never works around one. A reference set of a few sites is a small sample: a finding says "none of these do this", not "this is wrong".
