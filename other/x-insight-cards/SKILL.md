---
name: x-insight-cards
description: Run scheduled or manual creator curation that turns recent high-quality X posts into verified image-and-caption packs for Douyin and Xiaohongshu review, with optional private delivery to a pinned WeChat iLink bot review chat or confirmed File Transfer Assistant self-chat. Use when Codex needs to discover, verify, rank, deduplicate, translate, render, quality-check, resume, or privately deliver posts about wealth, life, goals, habits, attention, freedom, or long-term thinking while keeping sources auditable, Chinese typography accurate, recipient-safe, and platform publishing manual.
---

# X Insight Cards

Automate the preparation of Douyin and Xiaohongshu content packs from public X posts. Produce a small, source-auditable set of post images and copy-ready Chinese captions. Optimize for insight quality, faithful attribution, natural Chinese typography, and human review—not volume.

## Workflow

1. Read [references/workflow.md](references/workflow.md) before running a daily curation job.
2. For a scheduled daily job, first apply the catch-up policy in [references/workflow.md](references/workflow.md): when the scheduled time has passed and the daily completion record or final assets are missing, run the missed preparation immediately once network access is available. The catch-up mechanism must be independent of opening the Codex app.
3. Check the user's history file and existing output folders. Deduplicate by canonical URL and normalized English-text SHA-256.
4. Discover posts from the last 24 hours. Expand to 72 hours only when necessary; then use unused evergreen posts.
5. Verify each candidate's URL, author, handle, real profile avatar URL, exact English text, publication date, and views when views are material to selection. A candidate without a verified real author avatar is incomplete.
6. Reject politics, stock tips, medical advice, course sales, unattributed reposts, pure motivational filler, and unverifiable content.
7. Score candidates using [references/scoring.md](references/scoring.md). Select no more than five, sorted by score. Never pad below 75/100.
8. Translate faithfully. Preserve paragraphs, quotation marks, dashes, parentheses, and tone.
9. Render one card per selected post with the verified real author avatar. Initials, generated portraits, and generic placeholders are not acceptable fallbacks. For an English source, first estimate the full bilingual card at 1200 px width: keep both languages when the estimated height is at most 1200 px; when it exceeds 1200 px, omit the English body and show only the faithful Chinese translation with a small `译自英文原帖` label. Never shrink type to force a long post into bilingual mode. Use `scripts/render_card.py` for reconstructed cards and label the record `rearranged-render`.
10. Write one concise Chinese caption per card: normally one sentence, at most two, followed by 3–5 relevant hashtags. Do not copy the translation.
11. Run the checks in [references/qa-checklist.md](references/qa-checklist.md) and mark accepted items `READY_FOR_REVIEW`.
12. When the user has configured private delivery, read [references/private-delivery.md](references/private-delivery.md). For a fresh macOS installation, use the one-time `setup` binding and `wechat_ilink_listener_service.sh` flow documented there. Prefer the pinned iLink robot helper for unattended delivery when configured: its headless listener accepts only the exact command `发今日素材` from the pinned user, replies with safe usage guidance for other nonempty text from that same user, derives the current review-ready manifest from private history, preflights the fresh context, then sends each PNG and matching caption with checkpointed, stable message IDs. Use the verified integrated-main-window helper only for a separately configured File Transfer Assistant destination. Never upload or publish to a content platform.

## Rendering

The card renderer is deterministic Pillow layout code, not a generative-image model. Its default `render_mode` is `auto`: short English posts render bilingually, while long posts switch to translation-only according to the 1200 px estimated bilingual-height threshold.

Install Pillow, then run:

```bash
python scripts/render_card.py \
  --input assets/demo-post.json \
  --output ./output/demo-card.png
```

The English post style is the fixed reference. Match Chinese to the English text's visual size, stroke darkness, line height, and color. On macOS, prefer PingFang SC Regular for Chinese regular text. Read [references/typography.md](references/typography.md) whenever typography or punctuation is in scope.

## Ranking and deduplication

After assigning evidence-based score components, run:

```bash
python scripts/score_candidates.py \
  --input candidates.json \
  --history history.jsonl \
  --output ranked.json
```

Read [references/candidate-schema.md](references/candidate-schema.md) when preparing input data or consuming the output.

## Output contract

Default deliverables:

- One source-attributed PNG per selected post, prepared as Douyin/Xiaohongshu creator material.
- One copy-ready Chinese caption per post in the response or a user-requested structured file.
- A private/auditable history record outside the public deliverable folder.
- When explicitly configured, private delivery of each PNG and matching caption to the user's pinned iLink robot review chat or confirmed WeChat File Transfer Assistant self-chat.

Do not add poster backgrounds, ratings, Chinese titles, commentary, decorative AI art, platform watermarks, or captions inside the card.

## Safety and rights

- Use public, read-only content sources. Never read, export, print, or copy cookies, passwords, bot tokens, or context tokens into prompts, logs, manifests, history, or deliverables. A private delivery helper may open its pinned local `0600` credential and context files internally without emitting their contents.
- Do not bypass login challenges, rate limits, CAPTCHAs, or platform restrictions.
- Do not imply endorsement by X or any quoted author.
- Keep source links and attribution. Do not redistribute third-party media unless the user has the necessary rights.
- Never publish automatically. Private review delivery is not publication and requires a pinned recipient plus any just-in-time confirmation required by the active transport.
- A separate, explicit user request and platform-specific workflow is required for any social-platform upload.
