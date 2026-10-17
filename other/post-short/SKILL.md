---
name: post-short
description: Post a finished short to Facebook, Instagram, TikTok and/or YouTube in one batch. Use whenever the user wants to post, publish, upload or cross-post a short or reel.
---

# Post a short (all platforms, one batch)

## Inputs (infer before asking)
- **Drive link** for the video (FB/IG/TikTok download from Drive). For YouTube, the local file path.
- **Base caption.** Write it yourself from the short's hook if none is given, then run it past the `critic`.
- **Platforms.** Default to all four unless the user names some.

## Steps
1. **Write one caption per platform** from the base caption, saved as `posting-automation/<platform>-posting-automation/caption.txt` (`--caption-file` avoids shell quoting).
   - Hashtags: Facebook 1-3 (user rule); IG 3-5; TikTok 3-5.
   - No em dashes.
   - The pre-flight rejects anything else, so get it right the first time.
2. **Pick the cover once and reuse it.**
   - TikTok: `python upload_short.py --drive-link <L> --caption-file caption.txt --preview-covers`, then choose the frame with a sharp face and a strong reaction (wide eyes, direct look, not neutral).
   - FB/IG: use the same frame as `--cover-image`.
3. **Run each platform** from its folder (the pre-flight runs automatically and exits with code 2 on bad input; fix the input and re-run, never bypass it):
   - Facebook: `python upload_short.py --page-url https://www.facebook.com/SparkedThor --drive-link <L> --caption-file caption.txt --cover-image <png>`
   - Instagram: `python upload_short.py --drive-link <L> --caption-file caption.txt --cover-image <png>`
   - TikTok: `python upload_short.py --drive-link <L> --caption-file caption.txt --cover-timestamp-ms <ms>` (confirm first; `--yes` only after the user OKs the cover)
   - YouTube: `python upload_video.py --video <mp4> --title "<title>" --description "<desc>" --privacy private`
4. **The final Publish click stays with the user** (FB/IG never auto-publish). Report what's queued on each platform and where to click.

## Gotchas (keep this list updated)
- **FB cover picker:** the preview tiles aren't clickable. It's a hidden `<input type=range>` (0-1000) that has to be set through the native value setter plus input/change events. This is already handled in `upload_short.py`.
- **FB/IG Chrome sessions expire:** run `login_chrome_profile.py` once to fix.
- **TikTok privacy:** posts are `SELF_ONLY` until the app passes TikTok's audit (see the tiktok folder's claude.md).
