---
name: marketingPage
description: Make a marketing page on log's site (log.listeningkit.com) for one play, the way /rea-looksmaxxing was made - the platform pages' own sections, the play's copy as data, a phone story with real clips, an agent session running the whole play, an embedded post, logo chips, a use case and an installable skill. Use when the owner asks for "a new page called <x>", "a page like the platform pages for <play>", or to turn a video or a play into a page.
---

# marketingPage

A marketing page sells one play. It is built from the same sections as the
platform pages (`/twitter`, `/discord`, …), so it looks like part of the site,
and only the copy, clips and session are new. The worked example is
`/rea-looksmaxxing` (`site/apps/web/src/landing/useCases/ReaLooksmaxxingPage.tsx`).

## Hard boundaries

- **Reuse the sections, never redraw them.** Every block below already exists
  in `UseCasesPage.tsx`, `platformStories.tsx`, `PlatformMoney.tsx`,
  `HowItWorks.tsx` and `Control.tsx`. When a page needs something a section
  can't do, give that section an optional prop (the way `PlatformMoney` got
  `embed`, `title` and `subline`, and `PromptCta` got `install`), so every
  other page stays the same.
- **A summary of the play, never the whole script.** The page says how it
  works in three steps. A step-by-step grid of every beat was tried on
  /rea-looksmaxxing and the owner took it out: the full script lives in the video.
- **Embeds sit on the page, not in a card.** A post is shown as itself, inside
  a section (the money section's `embed`), never boxed in a separate
  decorated card.
- **Every number is real or not there.** Views, counts and quotes come from
  the research (treg, the video's sources) and keep their source. A price
  nobody checked is written as "priced per call", never invented.
- **Funny, deadpan.** The headline says it straight; the sticker word and the
  aside carry the joke ("Your jawline is optional").
- Only what the owner asked for (rules 39-41), and nothing about any platform's
  rules (rule 38).

## The page, top to bottom

| # | Section | Component | What goes in |
| --- | --- | --- | --- |
| 1 | Header | `Header` (light tone, "Set up log") | nothing new |
| 2 | Hero | your own `Hero`, same blue band, `ClayClouds` and `DitherFade` | headline, a handwritten aside, a lede naming the tools as `LogoChip`s, the two buttons (`#play`), then `HowItWorks` with the play's `how` steps and rows |
| 3 | The stepper scroll | `PlatformScroll platformId="<page>"` | three `Slide`s in `platformStories.tsx` under `SLIDES_BY_PLATFORM["<page>"]`, each a lead, sticker, body and a phone `Story` |
| 4 | Why free | `Control` with `session={PLATFORM_SESSIONS["<page>"]}` | a title with a sticker word, a lede with `Dashed` words, and an agent session that runs the whole play in Claude Code and Codex |
| 5 | Money | `PlatformMoney platformId="<page>"` | a card wall in `WALLS["<page>"]` (the DMs people would send), and optionally `embed`, `title`, `subline` |
| 6 | The play | `ThreeSteps` | the `Play`'s three steps, its calls and its outcome rows |
| 7 | Prompt | `PromptCta` | the ask, and `install` set to the skill's install line |
| 8 | More plays | `MoreUseCases` | nothing new |
| 9 | Footer | `SiteFooter` | nothing new |

## Steps

1. **Data first.** Write the play in `useCases/<page>.ts` as a `Play`
   (`platformPages.ts`'s type): name, ask, calls, outcome, three steps and its
   `how` (moments and rows). The ask is how the owner says it.
2. **The page.** `useCases/<Page>Page.tsx` puts the sections above in order and
   sets `document.title`. Route it in `App.tsx` and add it to
   `public/sitemap.xml`.
3. **The stepper.** Three slides in `platformStories.tsx`. Posts take `video`
   or `image`, DMs take a `meme` item for a photo. Clips come from footage we
   already have (the video's project): cut a few seconds, silent, about 360 px
   wide, so each is a few hundred KB at most:
   `ffmpeg -ss 1 -t 6 -i <clip>.mp4 -an -vf "scale=360:-2,fps=24" -c:v libvpx-vp9 -b:v 0 -crf 40 -row-mt 1 public/video/<page>/<name>.webm`.
   Clips are webm, never mp4: `site/.gitignore` ignores every `.mp4`, so an
   mp4 never reaches the deploy (the /rea-looksmaxxing clips 404ed on the live
   site until they were re-encoded). Photos go to `public/images/<page>/` as
   webp.
4. **The session.** `platformSessions.ts`: a run of `user`, `tool` and
   `assistant` events that goes through the whole play with the real tool
   names. A tool from another MCP server sets `server` (treg's
   `catalog_search` and `call` set `server: 'treg'`), so it isn't shown as log.
5. **The money wall.** A `WALLS` entry with nine threads of what people would
   DM after seeing the content.
6. **Logo chips.** A tool named in running text is a `LogoChip` from the
   site's own logo files (`public/logos/stack`, `public/logos/tools`,
   `public/logo.svg`).
7. **The use case and the skill.** The play gets a use case page
   (`docs/useCases/<area>/<page>.md`, the README table, `useCaseCatalog.ts`,
   then `bun run docs:build`) and, when people outside the repo should run it,
   a published skill (`skills/published/<page>/SKILL.md`, then
   `bun run skills:build`), installed with
   `install.sh --skills <name>` or `npx skills add log.listeningkit.com`.
8. **Check it in the browser** (`log landing (log-cli checkout)` in
   `.claude/launch.json`, port 3010): desktop and 375 px wide, no sideways
   scroll, the stepper's phones play their clips, both agent tabs run, the
   embed loads. Then `npx tsc --noEmit -p site/apps/web`.

## Files from /rea-looksmaxxing

- `site/apps/web/src/landing/useCases/ReaLooksmaxxingPage.tsx`, `reaLooksmaxxing.ts`
- `platformStories.tsx` (`REA_SLIDES`), `platformSessions.ts` (`REA_LOOKSMAXXING`), `PlatformMoney.tsx` (`WALLS.reaLooksmaxxing`)
- `public/video/reaLooksmaxxing/`, `public/images/reaLooksmaxxing/`
- `docs/useCases/inbox/reaLooksmaxxing.md`, `skills/published/reaLooksmaxxing/SKILL.md`
