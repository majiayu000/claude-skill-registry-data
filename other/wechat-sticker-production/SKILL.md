---
name: wechat-sticker-production
description: Create and review a consistent WeChat sticker series, animate approved character references with LocalVideoGen, convert owned video into bounded GIFs, and upload singles or albums through an authorized WeChat Sticker Platform browser.
---

# WeChat Sticker Production

Use this for the WeChat Sticker Platform, not WeChat chat-message automation or social video publication.

## Design and review

Define a small series around common chat replies. Each sticker should work alone, while shared clothes, palette, character relationships, or a small daily-life arc connect the set. Prefer one or two clear subjects, a large expressive face, a simple backdrop, and one readable action. Learn from public sticker collections without copying their characters or assets.

For LALACHAN, inspect the canonical individual images first. Aya is the red panda in a navy sailor outfit; Lala is the black-and-white panda. Preserve the user's approved reference, including prior versions. Do not force every buddy or branded prop into every sticker.

Work one sticker at a time when requested: reference -> user/style acceptance -> local animation -> small-size/loop review -> upload. Planned stickers are not generated stickers. Later cute-angry interactions can form reply pairs such as 哼 / 给你 / 好吧 without becoming hurtful or requiring the full story to understand them.

If the user requests a whole first album, the pilot is a style checkpoint, not the deliverable. Establish a complete 8-24-sticker scope using the live platform limits, then finish that scope sequentially. User additions such as hugs, kisses, shyness and encouragement can extend the same album. Keep each GIF useful independently and do not force all four characters into every composition.

The first still must already communicate the emotion. Inspect at 240 px and chat-like 120 px, with audio absent. Check character identity, limb count, expression, text, crop, motion, and three repeated loops. A smooth global image wobble is not a substitute for a character acting.

## Local animation

Discover the current LocalVideoGen API and its resource policy from the installed repository. Use its validated image upload and render API, keep the accepted reference as first frame, optionally as final frame for a loop, and save the job ID immediately. Submit once, monitor that same ID, download its observed output, and fully decode/sample it. Do not automatically regenerate or start a batch after a weak result.

Check RAM, swap, GPU and queue before rendering. Small output dimensions do not eliminate model-loading memory. Keep the normal resource gates; clean up only verified owned idle runtimes. Never close an active VM or another project's service just to fit a render. Stop the render services you launched when finished, while preserving a browser or image viewer needed for user review.

Bundled `scripts/render_wechat_sticker.py` supports the local H3 API contract used by this workflow. It records submission intent and receipt, fingerprints inputs, and resumes the same job after interruption. An ambiguous POST is blocked from automatic retry. An explicit preflight rejection is not a completed GPU attempt; preserve that evidence and correct the actual prompt/contract before resubmitting. Do not disable a guard just to get past it.

## GIF packaging

Bundled helper: `scripts/video_to_wechat_gif.py`. Requires Python 3.11+, Pillow, FFmpeg, and an explicitly supplied CJK font when text is used.

```bash
python3 scripts/video_to_wechat_gif.py INPUT.mp4 OUTPUT.gif \
  --duration 5.125 --speed 1.25 --fps 15 --label 哈哈 --font "$CJK_FONT"
```

It creates a GIF, preview PNG and provenance JSON without overwriting earlier versions. Recheck quality after palette/fps reduction. Flat backgrounds often look cleaner with no dithering; this is an aesthetic choice, not a universal rule. Keep the native source MP4, even though GIF carries no sound.

For a wording-only revision, reuse that MP4 and export a new labeled GIF. Preserve both alternatives, ask for selection when requested, and keep just one in the album's numbered GIF folder. Changing `靠山` to `撑腰` does not require a video rerender or a 25th album item.

Read the current [WeChat official specifications](https://sticker.weixin.qq.com/cgi-bin/mmemoticon-bin/readtemplate?t=guide/index.html#/makingSpecifications#specifications_stickers). On 2026-10-04 a dynamic single used 240 x 240 GIF, looping, <=500 KB. This helper conservatively targets 500,000 bytes. The meaning word allowed four Chinese characters. Albums required 8-24 images. LINE APNG and WeChat effect frame limits are not GIF requirements.

For a complete album, use `scripts/audit_wechat_album.py ALBUM --expected 24` (or the actual planned count). Set `--title` for subsequent series; `--partial` permits progress previews but is not final acceptance. It writes a portable gallery and checks GIF dimensions, loop, byte limit, duplicate content, transparent cover/icon and banner. The layout expects `gifs/*.gif`, `cover.png` (240 square), `icon.png` (50 square), and `banner.jpg` (750 x 400). Full-size originals stay preserved. A high-quality JPEG can fit the banner limit when its PNG is too large.

For a second series, preserve accepted identities while filling new everyday reply needs. A loose day-together arc can connect the set, but each sticker must work independently. Record the actual model profile and steps rather than equating a "better model" with better results. Preparing an album locally does not authorize submitting it; keep the first work and the unpublished successor separate.

## Browser upload and receipts

Reuse the user's specified authorized Chrome/CDP profile. Use available browser controls, or the installed `lalachan-xyq-browser-video` helper as a general CDP transport. Discover page IDs and observed controls rather than hard-coding a live account's identifiers.

1. Open `https://sticker.weixin.qq.com/`; user handles QR login if needed.
2. Choose 提交作品 -> 表情单品 for a pilot. Inspect the actual form.
3. Bring it to the front; attach the GIF with the real file input. Wait for remote preview and thumbnail, then fill 含义词 and relevant tags.
4. Verify the thumbnail/chat preview. Save a private screenshot and durable edit URL.
5. Save or submit according to the user's authorization. Report saved, submitted for review, approved, and live as distinct states; never retry a successful submission merely because approval is pending.
6. For 创建形象, inspect eligible works first. Do not associate unrelated old work. The observed form imposed six-month limits on changes to name/avatar/icon/description.

For albums choose 表情专辑 and 动态表情 instead of the single route. Upload sorted GIFs into one form, append only missing files when staging uploads, and verify remote order and meaning words. Banner, cover and icon have separate file inputs. Re-read checked values after each reactive form update. Use a name within eight Chinese characters, a short viewer-facing description, and the appropriate daily/cute classification. Confirm the complete count and thumbnails before one submission; retain the durable work URL and review status. Do not resubmit an already pending pilot single.

A blank upload route after login can be a failed static-resource request. Inspect loading evidence; revisit the dashboard and reopen the same route before replacing the browser or asking for another login.

## Appreciation settings

The LALACHAN owner requests `接受赞赏` enabled by default for future sticker works wherever available, unless explicitly overridden. This is an owner preference, not consent to monetize another user's work. Before submission, complete the appreciation message, guide image and thank-you image, using approved series artwork when possible. Re-read the checked state and verify it persists on the saved work's settings page.

On 2026-10-04 the album form accepted a 5-15-character message, a 750 x 560 guide image and a 750 x 750 thank-you image. A valid 240-square sticker GIF exceeded 500 KB after the platform enlarged it for appreciation. Reusing that sticker's PNG preview worked; pad the landscape guide instead of letting the platform crop ears or lettering. Inspect both uploaded previews. Keep the original animated album files unchanged.

For a pending work, inspect available editing first. Do not withdraw or create a duplicate to change this option without authorization. When the owner has withdrawn it for editing, complete and resubmit the same work once, then verify both review status and appreciation. Appreciation is distinct from a red-packet-cover distribution link; enabling it does not prove payout verification or platform approval.

## Records

See [the album production runbook](references/album-production.md) for the full sequential workflow, resume rules, upload ordering and resource lessons.

Keep private upload handles, account screenshots, cookies, paths and generated artifacts outside public Git. A portable handoff should name input/output roles, dimensions, hashes, generation settings, actual review result and platform status. Copy chosen deliverables to the configured sync folder and compare hashes; distinguish copying from confirmed cloud synchronization.

Design reference: [LINE animation guide](https://creator.line.me/en/guideline/animationsticker/detail/) emphasizes readable first frames and everyday communication. Borrow the design principles, not its different export limits.
