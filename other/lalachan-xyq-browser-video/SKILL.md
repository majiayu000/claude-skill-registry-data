---
name: lalachan-xyq-browser-video
description: Use when generating, preparing, monitoring, downloading, or publishing LALACHAN Xiaoyunque videos through a logged-in Chrome/CDP web UI, especially requests mentioning Lala Xia, Aya Chan, Sasa Kun, Xiaoyunque, XYQ, Seedance, 沉浸式短片, Agent 模式, reference images, reference video, Nutstore copying, low-credit generation, or avoiding the Xiaoyunque API.
---

# LALACHAN Xiaoyunque Browser Video

## Core Rule

Prefer the logged-in Xiaoyunque browser UI over the Xiaoyunque API unless the user explicitly asks for API usage. Validate visible page state before submitting: mode, model, duration, ratio, prompt, attachments, and credit estimate.

On Lachlan's workstation, `$HOME/.cache/xyq-chrome` is the canonical shared
Chrome profile for Xiaoyunque, JLC/JLCEDA web workflows, and downloads. When a
visible virtual desktop is requested, preserve that profile on display `:98`,
CDP `9344`, and noVNC `6099`. Do not launch a fresh profile or substitute the
book-only embedded-browser profile.

For portable docs/examples, use an ignored local config instead of personal
absolute paths:

```bash
cp .config/lazyskills.env.example .config/lazyskills.local.env
$EDITOR .config/lazyskills.local.env
set -a
. .config/lazyskills.local.env
set +a
```

Use the bundled scripts first:

```text
scripts/xyq_cdp_browser.py
scripts/xyq_chrome/watch_thread_dom_download.py
scripts/xyq_chrome/launch_chrome.sh
```

Load detailed references only when needed:

```text
references/xyq-browser-video-generation-skill.md
references/uploaded-images-no-path-workflow.md
references/xyq-browser-automation-workflow.md
references/smooth-video-generation-runbook.md
references/continue-confirm-download-runbook.md
references/30s-agent-workflow.md
references/words-card-30s-default.md
references/lala-studio-end-to-end-runbook.md
```

For a complete WeChat/operator handoff covering story writing, prompt saving,
browser generation, download, and LazyEdit publishing, see:

```text
$LALACHAN_ROOT/references/lalachan-story-video-handoff-for-wechat.md
$LAZYSKILLS_ROOT/docs/lalachan-story-video-generation-handoff.md
```

## LALACHAN Defaults

Default uploaded image order in the LALACHAN project:

```text
words-card.jpg
LazyingArtRobot.png
display.png
patchwork-leather-notebook-luxury-clean-v2.png
raraxia.jpeg
ayachan.png
sasakun.jpeg
Trio.png
```

Prompt labels after upload:

- 图1: words card / 小白屏学习卡.
- 图2: `LazyingArtRobot.png`, robot `庄子`; keep the LazyingArt logo on chest.
- 图3: LightMind AI glasses.
- 图4: handmade patchwork notebook.
- 图5: `raraxia.jpeg`, individual 啦啦侠 / Rara Xia reference.
- 图6: `ayachan.png`, individual 阿芽酱 / Aya Chan reference.
- 图7: `sasakun.jpeg`, individual 飒飒君 / Sasa Kun reference.
- 图8: `Trio.png`, three-character group identity reference.

No-Trio variant:

- If the user says not to upload `Trio.png`, skip only `Trio.png`.
- Still upload supporting assets unless separately excluded: `words-card.jpg`,
  `LazyingArtRobot.png`, `display.png`, and
  `patchwork-leather-notebook-luxury-clean-v2.png`.
- Still upload the three individual character references: `raraxia.jpeg`,
  `ayachan.png`, and `sasakun.jpeg`.
- In that case labels stop at 图7 and the prompt must not mention 图8 or a
  group-reference image. "No Trio" does not mean "only character photos" unless
  the user explicitly says only to upload character photos.

Characters:

- `啦啦侠 / Lala Xia`: use `raraxia.jpeg` as the primary individual reference.
- `阿芽酱 / Aya Chan`: use `ayachan.png` as the primary individual reference.
- `飒飒君 / Sasa Kun`: use `sasakun.jpeg` as the primary individual reference.
- `Trio.png`: optional group identity/reference image when uploaded; omit it
  when the user requests no Trio.
- `words-card.jpg`: words card / 小白屏学习卡 style reference.
- `LazyingArtRobot.png`: robot `庄子`; preserve the LazyingArt chest logo.
- `display.png`: LightMind AI glasses.
- `patchwork-leather-notebook-luxury-clean-v2.png`: handmade patchwork notebook/tool prop.
- `raraxia.jpeg`: individual 啦啦侠 / Rara Xia reference.
- `ayachan.png`: individual 阿芽酱 / Aya Chan reference.
- `sasakun.jpeg`: individual 飒飒君 / Sasa Kun reference.

Main-cast identity is a paid-submit blocker:

- The generated prompt must clearly anchor `啦啦侠 / Lala Xia`, `阿芽酱 / Aya Chan`, `飒飒君 / Sasa Kun`, and `庄子机器人 / Zhuangzi Robot` to the uploaded reference images.
- Extra villains, crowds, workers, animals, or fantasy characters are allowed, but they must not replace or redesign the four main characters as unrelated humans, unrelated figurines, or new faces.
- If the visible preview/prompt setup suggests the main cast may be redesigned instead of referenced, stop before paid submission and fix the prompt or attachments.

Words-card rule:

- Treat `图1` as the visual style reference for the physical learning card.
- Use `$LALACHAN_ROOT/words-card.jpg` as the design reference for Codex image generation. Before Xiaoyunque upload, generate a fresh episode-specific PNG with the imagegen skill and pass the reference image to that generation call.
- For every new video, create a fresh story-relevant word card; do not reuse the previous word unless the user asks.
- Default card metadata includes English, Japanese, Japanese furigana, and one short target-language meaning. Use another target language when the episode requests it.
- Before image generation, verify that every value expresses the same intended word and is correctly written in its own language or script. Apply the same accuracy standard to every line.
- The physical card face contains only the values, one line each. Do not render language names, field labels such as `English:` or `Japanese:`, colons, bullets, numbering, or explanatory text.
- Use the in-scene prompt pattern: `图1 是已经制作好的实体学习卡，只显示上传图片中的四行正文，不加语言名称、字段标签、冒号、项目符号或编号。保持每一行文字准确清楚。它只是场景里的真实道具，不是字幕。`
- Choose a word that matches the episode theme, for example battle/courage scenes can use `courage / 勇気 / ゆうき / 勇气`.
- Default method: use Codex imagegen with `words-card.jpg` as the referenced image, render the exact unlabeled value block, save the generated PNG under the current run, compare every line character-by-character, and upload that PNG as `图1`.
- After generating any words card, key-scene image, character reference, or other still asset, preserve the selected result at a stable project path and open it in a detached local viewer with the `persistent-image-preview` skill. A preview rendered only in chat does not count as opened. Keep the viewer open while the asset is reviewed or uploaded.
- Treat an unreadable, mislabeled, misspelled, semantically inconsistent, missing, duplicated, or unverified generated card as a paid-submit blocker. Regenerate the card before Xiaoyunque; do not spend video credits hoping Xiaoyunque will repair it.
- Asking Xiaoyunque to render a new card from the base style image is only a fallback when the user explicitly accepts it or Codex image generation is unavailable and no paid submission will occur yet.
- The card is a real prop in the scene, not a subtitle overlay.

Story writing rule:

- Write stories in natural, understandable Chinese first. The viewer should understand the action, joke, and emotion without reading production notes.
- Keep one clear cause-and-effect chain per short video: problem, response, twist, payoff.
- Dialogue should sound like friends talking. Avoid pseudo-code, abstract slogans, machine-like phrases, over-explained lore, and strange translated wording.
- Use simple concrete nouns and actions. Prefer "培养皿在显微镜下慢慢亮起来" over vague phrases like "生命数据完成同步".
- If a concept is educational or technical, show it through a visible action and one plain sentence, not a lecture.
- For lab scenes, keep the lab clean and believable: gloves, sterile bench, incubator, microscope, pipette, petri dish, and careful movement. Dance can happen as small safe steps, shoulder moves, or rhythm while working, not reckless lab behavior.
- Before turning a new story into a Xiaoyunque prompt, run a critic pass using `lalachan-story-critic` when available. Fix exact awkward lines first, then write the final prompt.

Never paste local filesystem paths into the Xiaoyunque prompt. Paths are only
for the browser file upload command. The prompt should refer only to actually
uploaded labels: normally `图1` through `图8`, or `图1` through `图7` when
`Trio.png` is intentionally omitted. Explicitly ask not to draw file names or
paths into the video.

Always upload the actual reference image files before generation. Do not treat
typed local paths, pasted filenames, or prompt-only image descriptions as a
substitute for upload. Before any paid submit, verify visible attachment
evidence for every required reference image. If image upload fails or cannot be
proved, stop and fix/report the blocker instead of submitting.

Default video setup:

```text
Mode: 创作 Agent by default for normal LALACHAN video generation
Model: Seedance 2.0 Mini 体验版 / cheapest visible suitable model by default
Duration target: 30s by default
Ratio: 4:3 unless the user requests otherwise
Prompt language: mainly Chinese
Always include: 不要字幕，不要生成任何字幕、说明文字、下三分之一文字或画面文字。
Post-generation: always auto-download the finished MP4, verify it, copy it to Videos/, and send it back to the requesting chat. Submit to LazyEdit only when the current request explicitly asks for LazyEdit/import/process or public publishing.
```

For default work, target `30秒` and use `创作 Agent` / integrated-agent with
`Seedance 2.0 Mini 体验版` / the cheapest visible suitable model. Use
`沉浸式短片` when the user explicitly requests `15秒` or another duration that
the short-film controls support. Before any Agent/long-video paid action,
inspect the visible credit estimate. If it is not clearly the cheapest
available path, or if it is a high-cost render, pause and ask for approval
instead of continuing. If a generation fails, continue in the same current
thread by sending a short corrective message; do not start a new session or new
thread just to retry unless the current thread is unusable and the user accepts
that cost/risk.

For a requested video longer than 15 seconds, select `创作 Agent` (or another
explicit long-video workflow) and make sure the `沉浸式短片` chip is not active.
Do not split the story into 15-second clips or compress it merely because the
short-film workflow is capped. `Seedance 2.0 Mini 体验版` can still be selected
inside Agent mode when the visible UI offers it; validate the actual selected
model and credit preview before submitting.

## Credit-Budget Rule

- Default to `Seedance 2.0 Mini 体验版` / `vipnew` when the UI shows it, especially when it shows a cheap rate such as `单秒限时低至4积分`.
- If Mini体验版/vipnew is unavailable, choose the cheapest visible suitable Seedance row. Do not silently upgrade to a high-credit long-video/Agent render.
- Treat visible high credit estimates, non-Mini paid long renders, recharge/payment approval, insufficient credits, disabled submit, login, CAPTCHA, or explicit user budget limits as blockers that require reporting before paid submission.
- Use normal `Seedance 2.0`, Fast VIP, Agent long-video, or other more expensive routes only when the user explicitly asks for that quality/duration/capability or confirms the visible cost.
- If the user asks for cheapest, Mini体验版 is the target. If the requested duration cannot be made with Mini, offer a shorter Mini version or ask before using Agent.
- If the UI shows Mini 体验版 / cheapest trial but another model is selected, do not submit. Select the cheap model first or stop and report the blocker.
- Do not continue an `智能长视频` / Agent render when it requests a large point spend unless the user has explicitly approved that exact high-cost render.
- For `4:3`, verify the opened ratio menu checkmark or screenshot because the compact toolbar may still show only `比例`.
- Never waste credits on avoidable retries: do not click `生成视频`, `提交`, or
  any paid action twice unless the page proves the first attempt failed without
  charging. If points drop or the task shows queued/running, monitor only.

## Paid Submit Contract And Acceptance Gate

Every render click spends a limited user resource. Keep automatic generation
countdowns off and require visible evidence of mode, actual model/tier,
duration, ratio, uploaded previews, prompt, cost, and balance before one
deliberate click. Prompt text and agent claims are not UI evidence.

After download, verify media integrity and inspect a contact sheet before
another paid clip or publication. A rejected result is evidence, not a publish
candidate. Retry only with user approval after reporting the charge, balance,
failure evidence, and least-cost recovery. For multi-clip recovery, validate the
first paid clip before spending on later clips.

Read [references/paid-generation-quality-gate.md](references/paid-generation-quality-gate.md)
before a paid submit, Agent storyboard render, retry, or multi-clip recovery.

## Browser Workflow

Before manipulating the page, prove that CDP and noVNC expose the same logged-in
Chrome profile and X display. On the canonical workstation this is normally CDP
`9344`, display `:98`, noVNC `6099`, and profile `~/.cache/xyq-chrome`. A healthy
legacy port such as `9222` may belong to an unrelated browser. Check the Chrome
process arguments, page URL, and visible noVNC tab together; do not trust a
responsive port alone. Explicit `LALA_STUDIO_XYQ_*` values take precedence over
stale generic `XYQ_*` settings.

1. Attach to an existing logged-in Chrome CDP endpoint, usually `$XYQ_CDP_URL` or another active port:

```bash
scripts/xyq_cdp_browser.py --cdp-url "$XYQ_CDP_URL" list-pages
```

2. Bring the Xiaoyunque page forward and inspect visible controls:

```bash
scripts/xyq_cdp_browser.py --cdp-url "$XYQ_CDP_URL" bring-to-front PAGE_ID
scripts/xyq_cdp_browser.py --cdp-url "$XYQ_CDP_URL" visible PAGE_ID
```

3. Select mode/model/duration/ratio by browser UI. For long work, click the exact
   top-level Agent mode and verify the short-film chip is inactive. Verify the
   requested mode, selected model row, duration, ratio, upload success, and any
   visible point cost/VIP/vipnew state. If the selected model, tier, or price
   cannot be proved from the visible UI, do not submit.

4. Upload and verify reference images:

```bash
scripts/xyq_cdp_browser.py --cdp-url "$XYQ_CDP_URL" upload-images-verify PAGE_ID \
  words-card.jpg \
  LazyingArtRobot.png display.png patchwork-leather-notebook-luxury-clean-v2.png \
  raraxia.jpeg ayachan.png sasakun.jpeg Trio.png \
  --timeout 180 \
  --screenshot outputs/xyq-run/after-upload.png
```

5. Fill the saved prompt:

```bash
scripts/xyq_cdp_browser.py --cdp-url "$XYQ_CDP_URL" type-prompt PAGE_ID references/prompts/example.md --wait 2
```

6. If the submit button stays disabled, inspect upload item classes. Wait until every uploaded file item is `success`; a single `uploading` reference blocks submission.

7. If the current thread pauses, fails, or needs a correction, first send a
   short message in the same thread. Avoid new sessions because they can waste
   credits and confuse the user. Use `创作` / new-session only when the current
   thread is truly unusable or the user explicitly asks.

8. Confirm the automatic generation countdown is disabled, save a preflight
   screenshot, and submit exactly once only when the user asked for generation
   and every field in the paid submit contract is satisfied.

## Agent Confirmation Pauses

Long-video / Agent workflows may stop after storyboard or reference-material
creation and ask the user to confirm before generating video. If the page asks
for continuation, reply in the same thread with a short message such as
`继续生成视频。`; do not start a new generation. Use `type-prompt` or real browser
keystrokes so the chat input enables the send button.

```bash
scripts/xyq_cdp_browser.py type-prompt PAGE_ID outputs/xyq-run/continue.md --wait 0.3
scripts/xyq_cdp_browser.py click PAGE_ID SEND_BUTTON_X SEND_BUTTON_Y
```

## Watch, Download, Copy

Prefer the official watermark-free export, using included membership benefits
when available. Verify the downloaded pixels: premium membership alone is not
proof of a clean export, and an `AI-generated` label may have separate rules
from a branding watermark. Preserve the original and report unavailable export
options; this preference does not authorize paid regeneration, cropping, blur,
or inpainting. Keep separately requested publication logos unchanged.

Monitor the submitted thread through the browser page:

```bash
scripts/xyq_chrome/watch_thread_dom_download.py \
  --cdp-url "$XYQ_CDP_URL" \
  --page-id PAGE_ID \
  --thread-url "THREAD_URL" \
  --output-dir outputs/xyq-run \
  --filename result_30s.mp4 \
  --expected-duration 30 \
  --copy-to Videos \
  --copy-to "$NUTSTORE_AUTOPUBLISH"
```

After every successful Xiaoyunque generation, do not stop at the browser result.
Download the final MP4 automatically, verify it with `ffprobe`, apply the
5-second duration tolerance unless exact duration was requested, copy it to
`Videos/`, and send it back to the requesting chat. Only submit it to LazyEdit
when the current request explicitly asks for LazyEdit/import/process or public
publishing. Direct LazyEdit CLI upload is preferred when available; Nutstore
AutoPublish import is an acceptable fallback. For LazyEdit-only requests, use
`--no-publish`; for public publish requests, publish exactly once to the
requested platforms.

Before copy or publish, run a complete decode and inspect a contact sheet. For
LALACHAN, reject generic replacement people/mascots, duplicate leads, incorrect
character-image mapping, missing required main characters, or a visual style
that contradicts the accepted references. Keep the rejected file as evidence,
but do not place it in an AutoPublish folder or public queue.

Do not scan every page-level `video` element and accept the first downloadable
file. Xiaoyunque pages can contain promotional media and stale results. Scope
discovery to the current result card or visible preview, pass
`--expected-duration`, and reject a candidate whose probed duration falls
outside the requested tolerance. Hash the accepted download and copied outputs
when exact identity matters.

Direct LazyEdit handoff pattern:

```bash
cd "$LAZYEDIT_ROOT"
python scripts/lazyedit_publish.py \
  --video "$LALACHAN_ROOT/Videos/VIDEO.mp4" \
  --title VIDEO_COMPLETED \
  --use-current-settings \
  --correction-prompt-file "$LALACHAN_ROOT/references/prompts/PROMPT.md" \
  --metadata-prompt-file temp/METADATA_BRIEF.md \
  --correct-subtitles \
  --correction-source polished \
  --no-publish \
  --wait \
  --poll-seconds 10
```

Nutstore fallback pattern:

```bash
cp -f "$LALACHAN_ROOT/Videos/VIDEO.mp4" \
  "$NUTSTORE_AUTOPUBLISH/VIDEO_COMPLETED.mp4"
```

Protected `everphoto` URLs may fail from unauthenticated direct HTTP. First test browser-context fetch with `--await-promise`; if it returns `200 video/mp4`, pull the active `video.currentSrc` from the page and download with browser-like `Referer` and `User-Agent` headers.
The bundled watcher can now use this same browser-context path by triggering an
in-page blob download and copying the downloaded MP4 from `~/Downloads`.
If protected URL download still fails but the page is complete and has a visible
top-right `下载` button, click the page button and then copy the newest MP4 from
`~/Downloads`. Quote the file path or use null-delimited `find -print0` patterns
because Xiaoyunque may save names such as `final_video (5).mp4`. See
`references/continue-confirm-download-runbook.md` for the full fallback
sequence.

## Completion Check

Before final response, report only verified facts:

- prompt/reference files saved;
- mode/model/duration/ratio seen on page;
- attachment filenames verified;
- prompt verified to contain no local image paths;
- credit charge or blocker observed;
- local MP4 path, `ffprobe` dimensions/duration, and copy targets.
- LazyEdit handoff status: video id for direct CLI upload, or Nutstore
  `_COMPLETED` path/import evidence for folder handoff.
