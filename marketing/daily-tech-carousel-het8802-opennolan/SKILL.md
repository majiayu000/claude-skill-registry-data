---
name: daily-tech-carousel
description: Use when creating or scheduling a daily "What happened in tech today" Instagram carousel from unused AI/tech research collector signals.
---

# Daily Tech Carousel

## Core principle
This is a **daily digest carousel**, not the main selected-idea carousel. Use the AI/Tech Script Engine's broad research pool to turn several non-winning signals into one premium Instagram carousel: one clear tech idea per slide.

## Relationship to existing workflows
- Keep the main workflow unchanged: 4-hour research collector → daily selected concept/script → selected idea carousel.
- This workflow runs separately after the main script/carousel jobs.
- It should use the same research files but exclude or de-emphasize the selected daily winner unless needed as context.
- Never auto-post a carousel draft. Approval is required before posting or scheduling.

## Inputs
Read these first:
1. `~/content-os/research/latest.md`
2. `~/content-os/research/YYYY-MM-DD/*.jsonl` for today and previous day
3. `~/content-os/research/YYYY-MM-DD/daily-5pm-synthesis.md` if present
4. `~/content-os/scripts/YYYY-MM-DD/daily-ai-tech-video.md` if present
5. Existing approval/status file for the same date if rerunning

## Topic selection
Select 5-8 research records that are source-backed and distinct. Prefer:
- AI product launches, devtools, agent infrastructure, funding/acquisition signals, startup opportunities, benchmarks, and builder-market signals.
- Founder/operator relevance over generic tech news.
- High or medium evidence strength.
- One-sentence implications that can stand alone.

Avoid:
- Duplicating the main selected daily concept unless the post needs a recap slide.
- Low-confidence Instagram/search snippets as primary slides; use them only as creator-pattern support.
- Overloading the carousel with multiple variants of the same agent/tool story.

## Carousel structure
Recommended 8-slide structure:
1. Cover: `What happened in tech today` + date + sharp subheading.
2-7. One signal per slide: title, why it matters, source tag, and one founder/operator implication.
8. Save/CTA slide: the meta-pattern tying the day's signals together.

If the day has more strong signals, use up to 10 slides. Do not exceed 10 without explicit user request.

## Copy rules
Each topic slide must include:
- A punchy headline under 9 words.
- One plain-English explanation.
- One `Why it matters` or `Founder takeaway` line.
- A small source tag/domain.

The carousel should feel like a premium editorial tech briefing, not a link dump.

## Visual rules
Follow `instagram-carousel` visual quality standards:
- 1080x1350 PNG slides.
- Use Codex CLI native image generation (`$imagegen`) as the preferred generation path for aesthetic slide imagery when available; avoid HTML/card screenshots and only use programmatic rendering as a transparent fallback.
- Default to the Anthropic-inspired AI/tech visual system: warm ivory/cream paper, charcoal ink, clay/orange accents, sand/tan cards, muted olive approval states, simple line icons, tactile collage/sticky notes, workflow cards, connector diagrams, grain, and soft shadows.
- Mobile-readable type with generous margins.
- Premium editorial/social design: collage, paper depth, screenshots/mock UI fragments, annotation marks, diagrams, source labels.
- One coherent palette and typography system across slides.
- No generic robot imagery, tiny paragraphs, flat HTML-card grids, or cramped citations.
- Do not add repeated headers, footers, slide numbers, date bars, brand bars, or template chrome. These make the carousel look like a deck instead of an Instagram post.

## Codex generation pattern
Create a detailed design brief and per-slide prompt file before generating images. Then use Codex/local tooling to generate deterministic PNGs and a contact sheet.

Expected output folder:
`~/content-os/daily-carousels/YYYY-MM-DD/what-happened-in-tech/`

Required files:
- `README.md` — overview, selected topics, source files, status, usage notes.
- `research-selection.md` — chosen records, why selected, why excluded selected winner.
- `carousel-copy.md` — slide-by-slide copy.
- `codex-prompts.md` — generation prompt(s) for Codex/local rendering.
- `caption.md` — caption, CTA, hashtags.
- `approval-status.json` — status object.
- `asset-ledger.jsonl` — one generated asset record per slide/contact sheet.
- `contact-sheet.png` — visual review sheet.
- `slide-01.png`, `slide-02.png`, ... — final PNG slides.

## Approval-to-post workflow
When the user replies in the relevant delivery thread with `post it`, `approve carousel`, `approved`, or equivalent, treat it as explicit approval for that package.

If the baseline posting time has already passed, do not only mark approval and wait for the 30-minute checker if the user asked to post now. Post immediately via the Instagram carousel pattern from your Instagram API integration, then verify the published media/permalink and update `approval-status.json` to `status: posted`.

If Instagram verification fails before media creation (for example `INSTAGRAM_GET_USER_INFO` returns top-level `HTTP 401 Unauthorized`), do **not** create child or parent containers and do not imply the post went live. Update `approval-status.json` to a blocked-approved state such as `status: approved_posting_blocked`, preserve `approved_at`/`approved_by`, add `last_post_attempt` with the exact error summary, write a short attempt log in the package directory, and tell the user to re-link/refresh your Instagram API integration before retrying.

Before publishing, clean the public caption: remove internal approval/revision commands, local file paths, and workflow notes. Keep only viewer-facing copy, CTA, and hashtags.

## Approval status
Use this status schema:
```json
{
  "status": "pending_approval",
  "approved_at": null,
  "approved_by": null,
  "scheduled_for": null,
  "posted_at": null,
  "posting_mode": "manual_or_integration_pending",
  "notes": []
}
```

Only set `approved` after explicit user approval such as `approve carousel`, `approve today's carousel`, `approved`, `post this`, or `schedule this` in the relevant delivery context or a durable approval file.

If the user asks to schedule for a specific/custom future time, `scheduled_for` is authoritative. The posting checker must not use the default weekday baseline while `scheduled_for` is in the future; it should only post when the current local time is within the due window for `scheduled_for`. If creating an additional one-shot cron job, also make sure the generic approved-posting checker cannot post the same package earlier at its baseline time.

## Posting-time baseline
Use your local timezone unless the user says otherwise.

### Saved Instagram timing reference
A high-performing creator reference recommended three candidate posting windows per day:
- Monday: 7:30 AM, 12:15 PM, 8:00 PM PT
- Tuesday: 8:15 AM, 1:00 PM, 7:30 PM PT
- Wednesday: 9:00 AM, 2:00 PM, 9:15 PM PT
- Thursday: 8:45 AM, 1:45 PM, 8:30 PM PT
- Friday: 7:00 AM, 11:45 AM, 6:15 PM PT
- Saturday: 10:30 AM, 3:00 PM, 8:00 PM PT
- Sunday: 9:45 AM, 1:30 PM, 7:45 PM PT

Interpretation:
- Treat these as a creator-sourced posting-time hypothesis, not as your account-specific Instagram Insights.
- The pattern clusters around morning activation, lunch/early-afternoon breaks, and evening scrolling windows.
- For scheduled daily carousel posting, prefer the lunch/early-afternoon slot when approval is ready; use the evening slot as a same-day fallback if approval lands late. Morning slots are useful for pre-scheduled content, but the current carousel approval workflow often needs post-draft review first.

### Primary scheduling targets for this workflow
Until your own Instagram Insights override them, use these practical daily-carousel targets:
- Monday: 12:15 PM PT; fallback 8:00 PM PT
- Tuesday: 1:00 PM PT; fallback 7:30 PM PT
- Wednesday: 2:00 PM PT; fallback 9:15 PM PT
- Thursday: 1:45 PM PT; fallback 8:30 PM PT
- Friday: 11:45 AM PT; fallback 6:15 PM PT
- Saturday: 3:00 PM PT; fallback 8:00 PM PT
- Sunday: 1:30 PM PT; fallback 7:45 PM PT

Treat these as a starting baseline; update based on your Instagram Insights when available.

## Delivery
Draft delivery goes to your delivery channel when available. The message must say status is pending approval and must include individual slide images in exact posting order (`slide-01.png`, `slide-02.png`, ...), followed by the contact sheet, caption path, and exact approval/revision commands. Do not send only a zip folder; archives are optional secondary backups only.

## Cron architecture
For implementation/audit details, use `references/cron-setup.md`. The proven pattern is two jobs: a 7AM draft generator to your delivery channel, plus a separate 30-minute posting checker that only acts after explicit approval and at the weekday posting-time baseline. Keep this separate from the selected-idea 6AM carousel job.

## Common mistakes
- Creating another full carousel for the selected daily script instead of unused research ideas.
- Combining generation and posting into one cron job, which weakens the approval gate.
- Posting automatically after generation.
- Treating weak creator snippets as factual tech news.
- Sending only text without generated slide files/contact sheet.
- Sending only a zip archive instead of ordered individual slide images.
- Assuming delivery-channel media attached successfully. If the message tool warns that `MEDIA` attachments were omitted, do not claim the images were delivered; send ordered absolute paths and/or attach the ordered slide images in the active user thread where native media upload is supported.
- Forgetting to write `approval-status.json`, which breaks later scheduling/posting checks.
