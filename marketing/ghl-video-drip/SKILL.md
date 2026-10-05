---
name: ghl-video-drip
version: 1.0.0
description: |
  Schedule N already-uploaded GHL videos as a one-per-day, multi-platform drip
  via a GoHighLevel Social Planner CSV. You give the CDN MP4 links (videos already
  in GHL Media Library) + a start date + time + captions; this builds a validated
  39-column / 2-header-row Social Planner CSV that posts each clip to
  TikTok + Instagram Reel + YouTube Short + LinkedIn (+ a pinned lead-magnet comment),
  one video per day.

  Distilled from batch7 (2026-05-30): 10 reels → 06-01→06-10 @ 7PM ET.

  Hard-won rules baked in:
    - Video URL MUST sit in videoUrls (col 6), NOT gifUrl (col 5) — the col-misalignment
      trap that makes GHL render a clip as a broken GIF.
    - GHL location timezone must be America/New_York (auto-DST), NOT America/Cancun
      (fixed GMT-05, 1h off in summer). CSV clock-time = location TZ.
    - 39 columns, 2 header rows (row1 platform groups, row2 field names).
    - Validate with .NET TextFieldParser (Import-Csv FAILS — duplicate "type" header).
    - Always test row 1 in GHL before trusting the full drip.

  Trigger when user says: "ghl video drip", "/ghl-video-drip", "schedule these videos
  one per day", "new GHL drip like batch7", or pastes N GHL CDN video links and a
  start date asking to schedule them.
---

# GHL Video Drip

Turn N pre-uploaded GHL videos into a one-per-day multi-platform Social Planner CSV.

## Prereqs (confirm with user)

1. Videos already uploaded to **GHL Media Library** → user has the CDN links
   (`https://assets.cdn.filesafe.space/<loc>/media/<id>.mp4`).
2. **GHL location timezone = `America/New_York (EDT)`** so CSV times = true ET.
   Set at: sub-account → Settings → Business Profile → Timezone.
   ⚠️ NOT `America/Cancun` (no DST → 1h off June–Nov). Changing TZ is global for the
   sub-account — warn it shifts any other queued posts/calendars; check the queue first.

## Inputs to collect (use AskUserQuestion if not given)

- **CDN links** (ordered) + a short caption/title per video.
- **Start date** (`YYYY-MM-DD`), **daily time** (default `19:00` = 7PM ET, best US window),
  **platforms** (default all 4: TikTok + IG Reel + YT Short + LinkedIn).
- Optional per-video: tags, category, pinned `followUpComment` (lead-magnet PDF url).

## Build

1. Write an input JSON (see `reference/sample_input.json`).
2. Run the builder:

   ```powershell
   # python = your Python 3.11 interpreter
   python ~/.claude/skills/ghl-video-drip/scripts/build_drip_csv.py <input.json> <out.csv>
   ```

   - Increments date +1 day per video from `start_date` at `time`.
   - Emits 39-col / 2-header CSV, all fields quoted, video in **col 6**.

3. Validate (asserts every record = 39 fields + prints date→video→title map):
   ```powershell
   powershell -File ~/.claude/skills/ghl-video-drip/scripts/validate_csv.ps1 <out.csv>
   ```
4. Hand the CSV path to the user → **upload to GHL Social Planner → test row 1 first**
   (confirm the video plays on all platforms, not a GIF/broken) → let the rest run.

## Notes

- One CSV row = one video posted to all selected platforms simultaneously (All-Social
  covers FB/IG/LinkedIn as `reel`; dedicated YouTube cols = `short`; TikTok cols set).
- Platform selection is also gated by which social accounts are connected/picked at
  upload time in Social Planner.
- Brand rules still apply: `@yourhandle` handle, client SAVINGS only (never your fees),
  no fake metrics.

## Column map (39)

1 postAtSpecificTime · 2 content · 3 OGmetaUrl · 4 imageUrls · 5 gifUrl ·
**6 videoUrls** · 7 mediaOptimization(TRUE) · 8 applyWatermark(FALSE) · 9 tags ·
10 category · 11 followUpComment · 12-13 type=reel,reel(FB,IG) · 14-15 pdfTitle,postAsPdf ·
16-25 Google GBP (empty ×10) · 26 YT title · 27 YT privacy(public) · 28 YT type(short) ·
29 TikTok privacy(everyone) · 30 promoteOtherBrand(FALSE) · 31-33 enableComment/Duet/Stitch(TRUE) ·
34 videoDisclosure(FALSE) · 35 promoteYourBrand(FALSE) · 36-37 Community title,notify ·
38-39 Pinterest title,link.
