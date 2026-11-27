---
name: social-team
description: "Use for posting, comments, DMs, the idea backlog, account setup, brand deals or a social media plan. Runs yskills' brand accounts as a team: Social Lead, Scout, Community, Partnerships, Analyst."
---

# Social team

yskills, 2026-10-12: "be my social media manager", "a real working company start up that generates
money". The `video-studio` team makes each video; this team decides what gets made, where and when
it goes out, answers the people who react, and measures what earns. Every post has a money job:
follow, profile tap, visit, install, sign-up or sale. Checked 2026-10-17 and 2026-10-18; sources in
`docs/research/2026-10-17-social-team.md` (`claude-setup/docs/research/2026-10-17-social-team.md`) and
`docs/research/2026-10-18-brand-deals.md` (`claude-setup/docs/research/2026-10-18-brand-deals.md`).

Every role reads [`learnings.md`](learnings.md) first. The order of work from idea to numbers, every role's hand-over and pass bar: [`pipeline.md`](pipeline.md).

## yskills' loop

| yskills says | The team does | Status |
|---|---|---|
| any idea, any time, one line | the Lead files it in `social/ideas.md` (date, brand, pillar, format) and reacts with 👍, nothing else | idea |
| "work them out" (all, named, or "the best N") | the Lead ranks, writes a brief, the studio's Producer makes it (`video-studio`), the Critic passes it | ready |
| "upload" (all ready, or named) | the Publisher (started by the Lead) schedules it or sends it to the account's drafts (Posting below) | posted |

Also: "show my ideas", "drop X", "change X". Questions and results go to the coordinator, which asks
yskills in the project chat (operator SKILL.md, Cards); yskills does not read threads.

## Roles

| Role | Does | Playbook | Runs as |
|---|---|---|---|
| Social Lead | owns a brand's channels: backlog, weekly plan, calendar, posting, profile, account setup; briefs the studio | [`roles/lead.md`](roles/lead.md) | the weekly routine (fresh session) and a thread `Social · <brand> week <n>` |
| Scout | trends, rising sounds, competitors' best posts, the hook library | [`roles/scout.md`](roles/scout.md) | subagent of the Lead |
| Community | comments and DMs: reply drafts, comment-to-DM flows, follower-only gifts, leads | [`roles/community.md`](roles/community.md) | the `social` Worker's webhook plus a daily subagent review |
| Partnerships | brand deals and sponsors: media kit, brand list, outreach drafts, offers, contract check, delivery, invoice line | [`roles/deals.md`](roles/deals.md) | subagent of the Lead; a thread `Deal · <brand> · <partner>` per real offer |
| Hook Checker | pre-film and cover hook gate: first 2 s, share trigger, burned hooks | [`roles/hook-check.md`](roles/hook-check.md) | fresh subagent of the Lead |
| Caption Writer | post text only: description, hashtags, pinned question, cover text, credit line, in his voice (on-screen caption options are the Writer's) | [`roles/copy.md`](roles/copy.md) | subagent of the Lead |
| Publisher | preflight, schedule, read-back, the `posts.md` row | [`roles/publisher.md`](roles/publisher.md) | subagent of the Lead |
| Analyst | numbers per post, what to repeat or drop, new lessons | [`roles/analyst.md`](roles/analyst.md) | subagent of the Lead in the daily sweep and the weekly routine |

Paid ads stay with the Marketer (`operator/roles/marketer.md`); the studio makes their creatives.
No own law or security team: Partnerships hands contracts to the operator's Legal role and
suspicious brand mail to its Security role (`operator/roles/legal.md`, `security.md`).
Thread titles follow the operator rule; team map and models in
`docs/TEAMS.md` (`claude-setup/docs/TEAMS.md`) (Social).

## Where things live

One project `social` (decided 2026-10-26, made by the `new-project` workflow, `docs/USING.md`) is
the ideas-to-posts app for every brand: `https://social.yverse.workers.dev`, Worker + D1.

| yskills sees | What it holds |
|---|---|
| Ideen | one text box plus a Stil (Real Talk, Erklär-Video, Großes Video) and an optional own clip (up to 300 MB, chunked into D1); links in the text are style examples to watch; checkboxes plus "Jetzt ausarbeiten" mark ideas queued |
| Entwürfe | per draft: script, player, caption, slot; buttons Freigeben, Ändern (one line why), Verwerfen, Jetzt hochladen |
| Plan | the next days' two slots per account, what fills them |
| Auto-Post | the switch per account (Posting below) |

- Login: a passkey on his phone (Face ID); the first passkey registered after the deploy is the owner, registration closes after it. No password, no secret anywhere.
- Claude reads `GET /api/feed` (ideas with preset and upload state, his taps; nothing private in it), fetches an attached clip at `GET /api/uploads/<id>/<n>` (chunks of 1.8 MB, `chunks` from the feed), and writes drafts by committing `content/drafts.json` + `public/media/` (contract: the repo's `docs/DRAFTS.md`; set `ideaId` and `uploadId`, which frees the clip's space); the merge deploys them. Posted state goes back the same way. No API key for Claude.
- Presets (yskills 2026-10-26, he never writes "cinematic" himself): real_talk = cut pauses, light grade, his white caption in the safe zone, loudness normalised; explainer = that plus punch-ins and B-roll from his own footage; big = full `video-studio`. The style profile (`/mnt/project-files/social/style/xyskillsx-style.md`) is the default for every idea.
- Install on the phone: the app is a PWA (`store` skill, free phone app); no store account.
- The daily round (scheduled task "Social daily round", 06:41 Berlin, once a day: yskills 2026-10-26 "no wasted tokens"; prompt: `/mnt/project-files/social/routine/daily-round-prompt.md`): first a bare feed check that stops before loading anything when nothing is queued, changed or approved; otherwise one thread works queued ideas by preset, reworks change notes, queues approved (or, with auto-post on, Critic-passed) drafts into Metricool, writes every tap, note and post number back to `learnings.md` and the style profile, and reports one line. "ausarbeiten" in the project chat runs the same brief at once.
- HQ (Company XY) gets one row with the link and today's count (`docs/hq-rows.md`), not a copy of the app.
- Until a slice of the app is live, ideas land in `/mnt/project-files/<project>/social/ideas.md` and finished videos are attached in the thread reply. Videos of a product's own campaign stay in its `video/<slug>/` (`video-studio`).

`social/posts.md` (one row per post, [`templates/posts.md`](templates/posts.md)) is written by the Publisher and Analyst from the first post. The comments and DMs webhook and the `brands.md`, `deals.md` notes join the same project when Community and Partnerships start.

## Daily lane and the full studio

2 videos a day cannot each go through the seven-role studio (research 2026-10-26,
`docs/research/2026-10-26-claude-video-autopost.md` (`claude-setup/docs/research/2026-10-26-claude-video-autopost.md`)).

- **Daily lane** (the slots): one of three templates, filled from a Writer script: real-photo or
  screenshot slideshow (the Larry format), screen-capture devlog (Playwright capture of the real
  product), explainer (`video-studio` `templates/explainer/`, new look per art direction). Then one
  fresh Critic pass on the cut. Minutes, not hours. Sound and cuts per preset (real_talk, explainer,
  big): [`../video-studio/sound-kit.md`](../video-studio/sound-kit.md). A template is used only after its first video passed the Critic.
- **Full studio** (`video-studio` pipeline): 1-2 flagship videos a week, ads, launches.
- **Empty slot:** when no idea of his is ready, the Lead fills it from a `Done:` line of any project
  (devlog or learning pillar only, real footage); never a bait, ad or crypto topic (yskills, 2026-10-26).

## Posting

Two kinds of account (yskills, 2026-10-18: "when i give you another account or you make one for
our projects you get full decision power, it's just my personal now, i want to be authentic and creative"):

- **His personal account (@xyskillsx):** yskills decides what goes up; the team makes each idea great
  in his taste (`roles/lead.md`, [`xyskillsx-style.md`](xyskillsx-style.md)). On his "upload" or "poste" for a named video
  the team posts it itself: Metricool with `autoPublish` on at the planned slot, the licensed-bed master
  (yskills, 2026-10-26: "why should I post it and not you?"). `final-nomusic.mp4` is kept for when he
  wants to add a trending sound himself and asks for it. Never a browser bot into TikTok Studio's
  drafts (`learnings.md`); under 30 days or 20 posts it stays a draft (below).
  - **Unattended slots** (no "upload" for that video) there only while yskills has switched auto-post on in the `social` app. The switch is his
    standing ok for posts under CLAUDE.md's ask rule; note the date in project memory. Only videos the
    Critic passed, only the devlog and learning pillars, at most 2 a day, and a daily one-line summary
    to the coordinator. He chose it on 2026-10-26 ("jeden Tag 2 Videos hochladen"); the switch starts
    off after a deploy and he flips it himself. Direct posts carry the licensed music bed, since an API
    post cannot add a trending sound.
- **Project accounts** (one he hands over, or one made for a project): the social team has full
  decision power over content, schedule, profile and strategy. That message is yskills' standing ok
  for posts on them; no switch needed. The Lead decides, the Publisher posts what the Critic passed, and the Lead sends a daily
  one-line summary to the coordinator.
- **Slots and language** for his English-speaking international audience: [`xyskillsx-style.md`](xyskillsx-style.md), International audience (the one home).
- **On every account:** never ads, prices or crypto promotion without yskills' ok; money, brand deals
  and signatures stay ask-first (`roles/deals.md`). At most 2 posts a day per account. An account
  younger than 30 days or with fewer than 20 posts gets drafts only (new accounts that direct-posted
  by API were shadowbanned, `learnings.md`); start at 1 a day, the second only while reach holds.
- **AI label:** yskills' call, off by default (2026-10-12); twin videos show "twin" in the preview;
  what the law asks for ads and realistic AI people is `market` §4. Never strip provenance data.
- **Official APIs only**, through an already-audited posting service. No browser bots, cookie
  uploaders, VPNs or emulators.
- **Accounts:** one real account per brand or project, set up with
  [`templates/account-setup.md`](templates/account-setup.md) (sign-up with phone and captcha is yskills'
  hands step); never bulk or fake persona accounts.
- **Crypto (Y-Coin):** posts about building it are fine; no promotion until `legal` cleared the
  coin (TikTok bans crypto promotion; EU MiCA wants a notified white paper first).

## Tools (one pick per job)

| Job | Pick | Notes |
|---|---|---|
| Schedule and post | **Metricool** (picked 2026-10-18; its claude.ai connector `createScheduledPost`, `getScheduledPosts`, `getBestTimeToPostByNetwork`) | setup below; fallback upload-post (free tier) or Ayrshare if the free plan's monthly cap is below 2 a day; a paid plan is a card |
| Media URL for a scheduled post | today: a temporary branch `media-<video>` holding only that file on claude-setup, linked as `raw.githubusercontent.com/...` (free, used 2026-10-26); later: the `social` Worker serves `final.mp4` from its D1 clip store at a short-lived URL (free, no card, not built yet) | `createScheduledPost` needs a public URL and copies the file on create. The branch stays until the post has gone out, then the `branch-cleanup` workflow archives it as a tag and deletes it (the first run's `media-brag-2026-10-26` is the coordinator's to clean after the post) |
| Instagram comments and DMs | Instagram Messaging API from the `social` Worker | private reply to a comment (one per comment, within 7 days), sent on its own only for keywords and gift texts yskills approved per brand in `social/brands.md`; replies only inside the 24-hour window; `is_user_follow_business` in the user profile gates follower-only gifts; needs a Business or Creator account and Meta app review, else ManyChat (Meta partner) by card |
| TikTok comments and DMs | no general DM API: Community drafts replies for yskills | partner tools that automate TikTok DMs only where TikTok allows it, by card |
| Hooks, captions, humanizer | `sergebulaev/tiktok-skills` references (MIT) | read first (install rule: `toolbox`) |
| Launch and devlog videos | `latent-spaces/brag` (MIT plugin, HyperFrames) through the studio's Motion role | read its scripts before install |
| Trends | TikTok Creative Center (free, web), vidIQ connector (trial) | |
| Brand voice | Anthropic's Marketing plugin | per project (`toolbox`) |
| Ads data (later) | TikTok for Business connector, Windsor.ai | Marketer |

## Every week

1. Analyst (also swept daily for posts whose 24 h or 7 d cells are due): last week's numbers per post into `social/posts.md`; three lines on what to repeat or drop.
2. Scout: rising sounds and formats in each brand's niche, five hook ideas.
3. Lead: 5-7 posts across the pillars (learning, programming and devlogs, ads for our games and
   sites) from the backlog and every new `Done:` with a live link; briefs to the studio's Producer.
4. Publisher, started by the Lead: queue the ready videos with caption and time; anything for yskills goes to the coordinator
   as one short list.
5. Community runs daily; leads (a buyer, a press ask) go to the coordinator the same day, brand
   and collab messages to Partnerships.
6. Partnerships, monthly: refresh the media kit, ten fitting partners in `social/deals.md`,
   outreach drafts for the best three as one ask to the coordinator.

## Metricool, once per person

yskills' hands, about 5 minutes; the thread sends exactly these three steps through the coordinator:

1. Account: `https://app.metricool.com/` → Sign up (free).
2. In Metricool, the brand → Connect at TikTok (or Instagram, YouTube) → log in with that account, allow.
3. `https://claude.ai/settings/connectors` → "Metricool Social Media Management" → Connect, same Metricool login.

Then the Lead checks `getBrandSettings` shows the account and writes the date into `social/brands.md`
(or the app). A new project account later only needs step 2. The free plan's limits on scheduled
posts are checked against the plan's slots before the first week; over the cap is a card.
