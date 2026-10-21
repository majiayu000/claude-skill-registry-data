---
name: website-positioning-check
description: >
  Give an existing website a fast, fresh-eyes positioning check: can the right
  visitor tell what is on offer, for whom, and why to believe it? Read-only and
  concise — a one-screen Clear / Blurred / Broken verdict, the single biggest
  blur, and the three highest-leverage fixes. Use whenever someone asks if a
  site's offer is clear, differentiated, outcome-led, too technical, or
  consistent between homepage and offer pages — even without the word
  "positioning". Trigger phrases: "is our positioning clear", "fresh eyes
  on the homepage", "what are we actually selling", "is it obvious who this is
  for", "we sound too technical", "homepage and services page disagree",
  "positioning sanity check", "does the site make sense to a stranger". Do not
  use for developing positioning from scratch (website-positioning), a full
  copy rewrite (copywriting), an SEO audit, or the pre-launch website-review.
---

# Website positioning check

Answer one question: **can the right visitor quickly tell this is for them, what
they get, and why to believe it?**

This is a diagnostic, not a workshop. Keep the answer to about 300 words — one
screen; the bold labels do not count. The cap exists so the owner reads the whole
thing: when a finding needs its evidence sentence, keep the sentence and cut
elsewhere. Do not edit files unless the user explicitly asks for implementation.

## Inspect

Read like an unfamiliar visitor before adopting the site's internal vocabulary.
Inspect, in this order:

1. **The rendered homepage.** A live URL if the user gives one. Otherwise build
   the site and read the built homepage (`dist/index.html` on a kit-built site;
   there `npm run build` writes only gitignored output). Confirm with
   `git status` that the tree is still clean afterwards; if it is not, say so.
   If you cannot build, read the homepage source (`src/pages/` on a kit site).
   Do not trust a build you did not just make — it may be stale.
2. **The primary offer page** — the services, product, or offer page the
   homepage's main CTA leads to. Follow it even when it leaves the site (a
   repo, an app store, a booking tool): the offer is wherever the CTA goes. If
   the target is missing or unreachable, the visitor has no next step — make
   that the Primary blur and carry on with the pages you have.
3. **`POSITIONING.md`, `CONTENT_GUIDE.md` and `STORY.md`**, when present (repo root or
   `docs/`) — last, so the site
   is judged by what a visitor sees and only then compared with what it meant
   to say.

Stop there. Missing proof on the pages you inspected is a finding, not a reason
to open more pages. Open one more only when two surfaces contradict each other
and that page settles which one the site means. Do not turn a quick check into
a site-wide audit or competitor study.

## Check

After the hero and first offer section, can the visitor it is for answer:

1. **Is this for me?** The audience or situation is recognizable.
2. **What do I get?** The change for the visitor leads; features, methods,
   credentials, process, and deliverables support it rather than replace it.
3. **Why this instead of the current alternative?** The difference is concrete,
   not an adjective or a generic claim every competitor could make.
4. **Why believe it?** Proof, experience, a mechanism, or an honest constraint
   supports the promise.
5. **What happens next?** The offer and CTA continue the same promise.

Then check consistency: title, description, H1, hero, offer names, and CTA should
sell the same category and outcome. On a site with a `STORY.md`, also judge the header
by its grunt test (what you do, how it makes life better, how to get it, in five
seconds) and check that the direct CTA repeats with the same label. Offer options should map to distinct visitor
starting situations, not read like an overlapping capability list. Where the
promise is a change in how the visitor's own team, practice, or life works
(training, enablement, a habit, a community), the site should show what that
looks like afterwards — not only what the provider does.

Do not score with fake precision. Use these verdicts:

- **Clear**: the five answers are immediate and the surfaces agree.
- **Blurred**: a credible offer exists, but the visitor must decode it.
- **Broken**: surfaces sell different things, the mechanism has replaced the
  visitor's outcome, or the main CTA leads nowhere.

Distinguish observation from inference where it changes the advice; do not label
every sentence. Flag missing evidence; never invent it. Bold copy may be good.
Unsupported certainty is not.

## Return this shape

**Verdict:** Clear / Blurred / Broken

**Current position:** One plain sentence describing what the site actually says,
not what its strategy document intended to say.

**Strongest element:** The one thing to preserve.

**Primary blur:** The single issue doing the most damage.

**Three fixes:** Three ranked, specific changes. For each, name the page and
section; add the file path when you know it. If a fix contradicts
`POSITIONING.md`, `CONTENT_GUIDE.md` or `STORY.md`, say so in the fix — the document
changes first, then the page (and `STORY.md` yields to `POSITIONING.md`).

**Core line:** One replacement positioning line only when the existing line is
part of the problem. Keep it faithful to available evidence.

Omit the Core line when no replacement is needed. Do not append a long checklist,
page-by-page inventory, or generic marketing advice.

## Handoff

If the site has an `analytics/` folder kept off GitHub (in the site folder, for each file you will write, `git check-ignore -q --no-index analytics/<file>` succeeds and `git ls-files -- analytics/<file>` succeeds and prints nothing),
save the verdict to `analytics/<date>_positioning-check/verdict.md`: first line "The assistant's
judgment, not a measurement", and at the end the pages judged and the full list of the site's
pages, so the next check can tell which pages are new.

If the user asks to fix the findings, update the positioning source of truth with
`website-positioning`, then use `copywriting` for page copy. Run the site's normal
tests and `website-review` after consequential changes.
