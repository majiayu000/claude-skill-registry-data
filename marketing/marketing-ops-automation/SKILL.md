---
name: marketing-ops-automation
description: "Automate a full-stack content marketing workflow: trend scouting, idea reports, approval-gated scripts, asset/video production, and scheduling/posting integrations."
version: 1.0.0
author: OpenNolan
license: MIT
metadata:
  content-os:
    tags: [marketing, social-media, cron, content-calendar, trend-research, remotion, image-generation, approvals]
    related_skills: [xurl, youtube-content]
---

# Marketing Ops Automation

Use this skill when the user says “Content OS,” but interpret it as an AI/tech content engine, not generic marketing-advice content. The domain focus is AI tools, AI companies, model/product launches, funding, startup incubators/programs/applications, founder credits/perks, events, devtools, infrastructure, and creator-pattern research for short-form content.

Core principle: **separate research, ideation, scriptwriting, production, and posting into approval-gated stages**. Never auto-post or commit spend unless the user explicitly grants that authority.

## Recommended Workflow

1. **Clarify operating context only if missing and necessary**
   - Business/niche, audience, brand voice, platforms, competitors/inspiration accounts, timezone, posting approval policy.
   - If the user gives an obvious schedule or asks to proceed, act immediately and note assumptions (especially timezone).

2. **Trend scouting and one-off research**
   - Run recurring local-only trend collection so the user is not spammed. For an AI/tech content engine, run at the cadence the user requested; the Instagram AI/Tech Script Engine currently uses a 4-hour collector (`every 240m`) feeding a daily synthesis/script job.
   - Do not aim for generic marketing advice. The default subject matter is: AI tools, AI companies, model/product launches, funding rounds, startup incubator applications, accelerator deadlines, grant/credit/perk programs, events/conferences/hackathons, devtools, agents, infra, chips, open source, and practical startup/operator opportunities.
   - Search TikTok/Instagram/Reels, YouTube/Shorts, X, Reddit, Google Trends, competitor accounts, newsletters/blogs, and trend reports for creator and audience signal.
   - For AI/tech/funding videos, broaden research beyond generic web results: AI/product launches, funding rounds, acquisitions, YC/startup activity, arXiv/research, GitHub/Product Hunt/Hacker News/Reddit builder signals, and creator-pattern analysis from top Instagram/Reels/Shorts/TikTok AI creators.
   - For startup opportunity content, track application windows, eligibility, deadlines, benefits/credits, application links, founder fit, and why the opportunity matters now.
   - Creator research must extract topics, hook patterns, visual formats, comment/audience demand, and reusable framing—not just account names.
   - For one-off “do research and send me a script” requests, act immediately: gather source-backed evidence, write the script, save it under `~/content-os/scripts/YYYY-MM-DD/`, and deliver to the requested channel if the user explicitly asked to send.
   - Exa is approved for Content OS research up to the user's configured $5 cap; use configured env such as `EXA_API_KEY`, `EXA_SPEND_CAP_USD`, and `AI_VIDEO_SEARCH_PROVIDER=exa` when available, and notify before exceeding the cap.
   - Store structured evidence in durable files, e.g. `~/content-os/trends/YYYY-MM-DD.jsonl` or `~/content-os/research/YYYY-MM-DD/hour-HH.jsonl`.
   - Each record should include timestamp, platform, topic, source URL, evidence summary, creator/market signal, opportunity details if any, angle, confidence, and source type.
   - If the user sends an Instagram/social post as a “research seed” for tomorrow, save it durably instead of relying on chat context only. Use an inbox such as `~/content-os/research/user-submitted-posts.jsonl` with URL, submitted time, platform, accessible metadata/thumbnail summary, topic guess, intent, and status. The next collector/script run should research around the seed, verify claims, and decide whether it belongs in the daily script, digest carousel, or only as creator-pattern context.
   - For user-shared social links (Instagram/Reels, Threads, TikTok, X/Twitter) that are gated or metadata-only, treat link intake as part of Content OS research: inspect public metadata, search exact shortcode/caption/handle, analyze preview thumbnails, label access limits, and do not claim transcript/comment access unless directly retrieved. See `references/social-link-intake-and-gated-post-summarization.md`.
   - See `references/ai-tech-creator-research-strategy.md` for the required AI-tech hourly research, creator-research fields, daily 5 PM synthesis bar, and strategy-updating loop.

3. **Daily idea report**
   - Deliver a concise user-facing report at the agreed time.
   - Provide exactly the number requested (often 10) and include trend evidence, platform fit, hook, format, why it should work, complexity, and next step.
   - Include a clear approval instruction: `Reply with the numbers you approve, e.g. approve 1, 4, 7.`

4. **Approval-gated scripts**
   - At the script deadline, search recent session history for explicit approvals and also read durable approval files such as `~/content-os/approvals/YYYY-MM-DD.md`.
   - Accept only clear approvals such as `approve 1, 3`, `approved #2`, or `go with 4 and 7`.
   - If approvals are missing or ambiguous, ask for approval/clarification instead of guessing.
   - If approval arrives after the scheduled script job already ran, record it, inspect cron output and script files, then either trigger recovery or generate the scripts immediately if the user asks for them now.
   - Save scripts under `~/content-os/scripts/YYYY-MM-DD/idea-N.md`.

5. **Production**
   - Generate images/assets using the configured image generation tool/provider.
   - For vertical short-form video, create a production folder such as `~/content-os/productions/YYYY-MM-DD/idea-N/`.
   - For larger/recurring AI-news video work, prefer a separate typed production-pipeline project instead of ad-hoc one-off renders. The proven scaffold path is `~/ai-video-pipeline`; it models research cards, scripts, storyboards, asset ledgers, timestamped audio, timeline JSON, rendering, QA reports, and export packages.
   - Use Remotion/Node/ffmpeg when available. If rendering is blocked, produce ready-to-run code and exact commands; do not claim files rendered.
   - If the user specifically asks for OpenNolan, HyperFrames, reference-reel translation, or reusable motion/style systems, load `opennolan-video-production` and treat it as the production sub-workflow under this Content OS umbrella rather than creating a one-off video skill.
   - Verify any file exists before referencing `MEDIA:/absolute/path/to/file`. For delivery, do not assume `MEDIA:` will upload the MP4: the generic `send_message` connector may omit media attachments and only send the text/path. After sending, inspect the tool response for media warnings and disclose whether the delivery channel received a native attachment or just the local file path.
   - For vertical short-form video, do **not** ship a single generated image with captions pasted over it, do **not** ship pure kinetic-text graphics, and do **not** ship a slideshow of still images as a real production draft unless the user explicitly asked for a lightweight test. Storyboard the script into 5–8 beats, then build a video-first edit: source actual moving B-roll/video clips where possible, record/simulate product or form interactions, use animated UI/screen captures, or generate video/motion-graphics shots. Stills are supporting assets only; if used, animate them with layered parallax/internal subject motion rather than simple pan/zoom. Every 2–4 seconds should contain a retention event such as a cut, motion accent, camera move, text reveal, prop/UI change, SFX hit, pattern interrupt, or perspective shift. Use captions as selective emphasis rather than the entire script.
   - For production-grade factual AI-news videos, do not render directly from a topic. Require a source-backed research card, fact-checked script, storyboard, complete scene assets, timestamped voiceover/forced alignment, deterministic timeline, and QA gate before export.
   - For video deliverables, verify the MP4 is actually decodable, not just present: run `ffprobe -v error -show_entries format=duration,size` and `ffmpeg -v error -i <file>.mp4 -f null -`. A timed-out or killed ffmpeg process can leave a file with no `moov` atom or invalid NAL units.
   - Build a contact sheet and inspect visual variety + mobile text readability before delivery; if text is cramped/cut off, revise before sharing. If captions are cut off, reduce font size, add safe margins, and wrap long lines before re-rendering.
   - Voice quality is part of production quality. Avoid bland/default TTS voices for Content OS shorts; prefer energetic creator-style voices with clear delivery, and generate a short sample before committing a full render. The current preferred ElevenLabs voice for this workflow is `Liam - Energetic, Social Media Creator` (`TX3LPaxmHKxFdv7VOQHJ`) over default `Adam`.

6. **Posting/scheduling**
   - Posting is a separate explicit approval gate.
   - Prefer unified schedulers (Buffer, Metricool, Publer, Hootsuite/Sprout) for speed and reliability, unless the user wants direct APIs.
   - Direct platform routes: X via `xurl`, YouTube via YouTube Data API OAuth, Instagram via Meta Graph API, TikTok via Content Posting API, LinkedIn via LinkedIn API.

## Subagent Pattern

Use subagents when the workflow benefits from parallelism:

- **Trend researcher:** scans platform/trend sources and records evidence.
- **Competitor/content-pattern researcher:** studies hooks, thumbnails, comments, repeated formats.
- **Idea synthesizer:** converts evidence into ranked content opportunities.
- **Scriptwriter:** creates scripts for approved ideas only.
- **Art director:** converts scripts into image/visual prompts and style consistency rules.
- **Video producer:** generates Remotion structure, render commands, captions/subtitles, thumbnails.
- **QA/editor:** checks factual grounding, file existence, approval compliance, and platform constraints.

## Cron Implementation

For an Instagram AI/Tech Script Engine talking-head workflow, keep the system lean: local research, daily creator brief/talking script, then a separate asset/B-roll pack job. The current preferred pattern is:

1. Research collector: `deliver=local`, schedule `every 240m` unless the user requests a different cadence.
2. Daily concept + talking script: `deliver=<valid named target>`, e.g. your delivery channel; include flexible talking points and an `Asset/B-roll brief for follow-up cron` section.
3. Daily asset + B-roll pack: schedule 15–60 minutes after the script; use `codex` plus local media tools to create 5–10 SVG/PNG supporting visuals, `README.md`, `asset-ledger.jsonl`, `broll-suggestions.md`, and `hook-recommendation.md` under `~/content-os/assets/YYYY-MM-DD/daily-ai-tech-video/`. The hook recommendation must pick a relevant Kallaway/FigJam Short Form Lego Bricks combo from the stored FigJam-derived hook database, not from the generated PNG/SVG asset cards: one visual hook brick + one spoken hook brick + exact first 2–5 second shot/spoken line + matching SFX/audio cue. The asset cards should then support that hook, not determine it. If the user asks for the actual FigJam hook video/clip, treat that as a request for an embedded playable reference clip; do not answer with only taxonomy text. Use `content-os-tools` → `references/figjam-video-hook-extraction.md` for the extraction/disclosure workflow.

For a broader approval-gated daily marketing loop, create separate cron jobs rather than one monolithic job:

1. Hourly or requested-cadence trend scout: `deliver=local`.
2. Daily idea report: `deliver=origin`, schedule e.g. `0 17 * * *`.
3. Approved scripts: `deliver=origin`, schedule e.g. `0 19 * * *`.
4. Production: `deliver=origin`, schedule e.g. `0 21 * * *`.

Always check the live timezone (`date` plus `TZ=<your timezone> date`) before creating time-based jobs. Treat stated cron times as your local timezone unless the user explicitly says otherwise; convert to the scheduler's timezone before saving the cron expression and state both local and UTC next-run times. Do not default to UTC/server time for marketing cron jobs.

When the user asks where marketing cron results will appear, audit the live cron and channel state before answering: inspect `~/cron/jobs.json` for each job's `deliver` and `origin`, then map delivery-channel IDs through `~/channel_directory.json`. `deliver=origin` means the original chat/thread/topic, which may be a DM thread rather than a public channel; `deliver=local` means no platform post. Check `~/cron/output/<job-id>/` for generated run output and delivery errors before claiming what was sent.

When moving Content OS jobs to a named delivery channel, first list messaging targets, send a low-impact test message if the user requests it, then set `deliver` to the resolved channel ID rather than leaving `origin`. Also update job prompts that still say "origin thread" or an old timezone/channel so generated messages are self-consistent.

Late approvals are common: if an approval comes after the downstream cron has already run, write an approval file, inspect output directories, and do not imply deliverables exist until verified. If the user asks for the deliverable immediately, generate it in the current session rather than only triggering the next cron tick.

Daily script cron recovery: if the user asks for “today’s script” and the scheduled daily concept/script job failed or the expected `scripts/YYYY-MM-DD/daily-ai-tech-video.md` is missing, recover manually in-session from `research/latest.md`, today/previous-day research JSONL/synthesis files, and verified source pages. Save the recovered script to the normal path and verify it before replying. Do not present yesterday’s script as today’s, and do not only trigger/wait on cron when the user needs the script now. See `references/daily-script-cron-recovery.md`.

See `references/hourly-marketing-cron.md` for a concrete cron prompt set and file layout used in a Slack marketing workflow.
See `references/instagram-ai-tech-script-engine.md` for the Instagram-focused successor pattern: keep 4-hour AI/tech research, daily talking-head script, and a follow-up Codex-generated asset/B-roll pack while treating old `content-os` paths as legacy storage.
See `references/daily-tech-carousel-digest-workflow.md` for the separate 7AM draft-only “What happened in tech today” digest carousel workflow that turns non-winning research signals into one-slide-per-idea carousel drafts for your delivery channel with explicit approval before posting.
See `references/figjam-hook-database-cron-integration.md` for adding Kallaway/FigJam Short Form Lego Bricks hook recommendations to daily script and asset-pack cron jobs, including the `hook-recommendation.md` artifact.
See `references/ai-tech-creator-research-strategy.md` for the AI/tech/funding + creator research strategy: hourly source collection, top creator topic/format tracking, daily 5 PM concept/script synthesis, and reusable skill-update rules.
See `references/social-link-intake-and-gated-post-summarization.md` for summarizing and learning from user-shared gated social links without overclaiming access to transcripts/comments.
See `references/cron-delivery-audit.md` for the delivery-audit workflow and the Slack DM-vs-channel pitfall discovered during Content OS cron setup.
See `references/approval-recovery.md` for handling late approvals, missed session-search detections, and recovery when expected scripts/assets are absent.
See `references/creative-short-video-workflow.md` for the corrected anti-bland short-video production workflow: multi-beat storyboard, multiple GPT-image-2/B-roll visuals, motion, sound design, contact-sheet QA, and ffmpeg zoompan pitfalls.
See `references/remotion-short-video-production-notes.md` for the approved Remotion/template-driven short-video workflow, batch-production pattern, and QA/debugging pitfalls discovered while making Idea 10 plus Ideas 1/4/6.
See `references/idea-4-v2-remotion-qa-notes.md` for the Idea 4 v2 rebuild notes: fixing decodable-but-stale renders, avoiding false blank-frame contact-sheet tiles, and using scene-midpoint contact sheets for short-form QA.
See `references/idea-4-v2-remotion-qa-notes.md` for the Idea 4 v2 rebuild notes: fixing decodable-but-stale renders, avoiding false blank-frame contact-sheet tiles, and using scene-midpoint contact sheets for short-form QA.
See `references/typed-ai-video-pipeline-v0.md` for the typed production-pipeline scaffold pattern: research card → script → storyboard → asset ledger → voiceover timings → timeline JSON → FFmpeg/Remotion render → QA → export package, including the FFmpeg concat-path pitfall and v0 verification commands.
See `content-os-tools` → `references/procedural-motion-graphics-rendering-notes.md` when doing local Python/Pillow + FFmpeg procedural shorts; it covers NumPy render performance, silent-render reuse, generated-local ledgers, and contact-sheet pitfalls for slide-in text.
See `references/video-craft-learning-loop.md` for the corrected video-first standard: learn current short-form editing patterns from the web, use actual moving footage/screen/UI/generated-video assets, add retention events every 2–4 seconds, and reject slideshow-like drafts.
See `references/viral-claude-validation-angle.md` for the Claude/Reddit/G2 SaaS-validation viral-post angle: frame AI validation skeptically, require citations/receipts, and position the opportunity as a source-backed founder decision memo rather than a magic 10-minute market oracle.
See `references/tts-voice-selection-and-slack-delivery-notes.md` for the latest Content OS TTS preference: avoid bland default voices, use ElevenLabs Liam (`TX3LPaxmHKxFdv7VOQHJ`) for energetic social-media narration, and remember Slack `send_message` may omit native MP4 attachments.
See `references/slack-media-attachment-limitation.md` for the Slack connector limitation where `MEDIA:` MP4 attachments may be omitted, requiring explicit path/link delivery and response-warning disclosure.

## External Tool Recommendations

Use a strict ROI gate for external tools. Prefer free tools, public sources, and free Apify Actors first; recommend paid tools only when they save meaningful time/money/compute/LLM tokens, unlock otherwise unavailable data, or materially improve output quality.

When recommending tools:

- **Be exact.** Do not say “Apify” generically; name the exact Actor/app/API and URL, e.g. `clockworks/tiktok-scraper` or `streamers/youtube-scraper`.
- **Include pricing.** For paid tools/Actors/APIs, research current pricing or a credible price range and cite the source URL.
- **Compare free alternatives.** Name free alternatives and explain why they are insufficient for this workflow.
- **State ROI.** Explain what the tool saves or unlocks (time, money, compute, LLM tokens, unavailable data, quality).
- **Check startup programs.** Look for startup credits, free tiers, startup discounts, and eligibility/application links.
- **Record recommendations.** Maintain `~/content-os/tool-wishlist.md` with date, workflow stage, exact tool/API/Actor + URL, pricing, free alternatives, why not free, ROI reason, startup credits/discounts, priority, and approval/config needed.

Known starting points:

- **Apify:** agent-friendly cross-platform trend/competitor scraping. Free plan typically includes a small monthly usage credit; Apify Store Actors may be free, monthly-rental, or pay-per-result. Startup program/discounts can change, so verify live terms.
- **Buffer or Metricool:** practical first scheduler for approval-based posting across platforms.
- **Google Trends / Glimpse / Exploding Topics:** macro trend validation and early topic discovery.
- **TikTok Creative Center:** sounds, hashtags, ad/creative patterns.
- **vidIQ / TubeBuddy:** YouTube keyword/title/topic validation.
- **Brandwatch / Sprout / Hootsuite Insights:** enterprise-grade social listening.

See `references/apify-and-tool-roi.md` for a concise Apify/tool recommendation policy and pricing notes.

## Safety and Compliance

- Do not read or expose credential files.
- Do not ask users to paste API secrets in chat; direct them to configure credentials locally.
- Do not post, reply, DM, follow, or spend money without explicit user approval.
- Label uncertain trend evidence rather than overstating it.
- Respect platform API requirements and app-review constraints.

## Verification Checklist

Before finalizing setup:

- The content-OS tools list confirms required toolsets are enabled (`web`, `browser`, `terminal`, `file`, `code_execution`, `image_gen`, `vision`, `video`, `delegation`, `session_search`, `cronjob`).
- Cron jobs exist with correct schedules and delivery targets.
- User-facing jobs deliver to the intended origin/thread; noisy research jobs deliver local-only.
- Timezone assumption is stated.
- File paths for trends/scripts/productions are included in prompts.
- Approval gates are explicit for scripts, production, and posting.
