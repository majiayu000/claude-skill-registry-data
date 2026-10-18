---
name: photo-caption-writer
description: 当使用者说"给这张照片写图注"、"帮我写一段作品说明"、"这张照片配一句什么文字"、"展览标签怎么写"时使用。Write a factual short photo caption or a longer artist statement from photographer-provided context and optional EXIF metadata. Use when a user asks for a caption, wall label, portfolio note, or brief statement for an existing photograph. Do not infer emotions, intent, place, identity, or circumstances from the image alone.
category: photography
version: 0.1.1
status: draft
priority: P2
compatible_agents:
  - claude-code
  - openclaw
  - cursor
  - codebuddy
  - generic-llm-agent
---

# Photo Caption Writer

Write concise, usable copy without turning guesses about a photograph into facts.

## Inputs

Collect only what the requested output needs:

- the photograph, or a description of it;
- output mode: `short` or `long`;
- destination or audience, if relevant;
- facts the photographer confirms: time, place, subject, event, process, or circumstances;
- the photographer's own intent, memory, or interpretation;
- optional EXIF metadata.

Do not block on missing optional inputs. If the user asks for a factual detail that is absent, ask for it or omit it. Never fill the gap by guessing from pixels, filenames, or nearby context.

## Workflow

1. **Separate the evidence.** Make three private working lists:
   - `confirmed`: explicitly supplied by the photographer or extracted from metadata;
   - `attributed`: interpretations or intentions stated by the photographer;
   - `unknown`: anything merely inferred from the image.
2. **Extract metadata when useful.** If a local image is available and the runtime can execute Python, run:

   ```text
   python3 scripts/extract_exif.py IMAGE
   ```

   The script requires Pillow. It reads IFD0 and the Exif sub-IFD, where cameras store aperture, shutter, ISO, focal length, lens, and capture time, and prints `source_file`, `captured_at`, `camera_make`, `camera_model`, `camera` (maker not repeated), `lens`, `exposure_time`, `aperture`, `iso`, `focal_length_mm`, `focal_length_35mm`, and `exposure_compensation_ev`. `captured_at` comes from DateTimeOriginal only; a file that carries only IFD0 DateTime (its last edit or export time) gets `null`, so never present a file date as the capture time. GPS is never printed. Treat `null` fields as unavailable; do not mention them. If the script cannot run, use only metadata the user provides.

   HEIC/HEIF files (the iPhone default) need the `pillow-heif` package, or a JPEG copy first: `sips -s format jpeg IMG.HEIC --out IMG.jpg` (macOS; keeps the EXIF). The script exits 1 and prints that command instead of guessing.

   `scripts/image_io.py` is a shared copy of the photo skills' image module; identical copies live in `photo-exif-frame`, `shoot-outing-review-card`, `photo-series-layout`, and `photo-spread-composer`, and `scripts/validate.sh` requires them to stay byte-identical, so never edit one copy alone. fontTools is optional and only used by the rendering skills to check glyphs. `python3 scripts/extract_exif.py --selftest` runs the regression checks.
3. **Choose the mode.**
   - `short`: one sentence, normally 15–35 words. State only useful context; include camera settings only when requested or editorially relevant.
   - `long`: one restrained paragraph, normally 70–150 words. Connect confirmed context, the photographer's attributed intent, and relevant process details.
4. **Draft in the user's language and requested voice.** Prefer concrete nouns and verbs. Preserve uncertainty with wording such as “the photographer recalls” or “appears” only when uncertainty itself is useful and clearly marked.
5. **Run the honesty check.** For every claim, identify its source. Remove or qualify any claim supported only by visual inference.
6. **Return clean copy.** Give the finished caption first. Add a brief `待确认` list only when unresolved facts materially affect publication.

## Source and attribution rules

- EXIF supports capture settings and recorded timestamps; it does not establish creative intent.
- A user-provided account supports that person's stated memory or intention, not an objective claim about every viewer's experience.
- Visible content can support neutral description, but not hidden identity, exact location, relationship, emotion, symbolism, or cause.
- Do not identify people, private places, medical conditions, political affiliation, or other sensitive traits from appearance.
- Do not claim that a photograph “expresses,” “captures,” or “symbolizes” an idea unless the photographer supplied that interpretation. Attribute it when appropriate.
- Preserve the distinction between capture time and file creation or modification time.
- Do not expose GPS or other sensitive metadata unless the user explicitly asks and understands the publication context.

## Output patterns

### Short

```text
[Publication-ready caption]

待确认（only if needed）:
- [missing fact that materially changes the caption]
```

### Long

```text
[Publication-ready paragraph based on confirmed context and attributed intent]

待确认（only if needed）:
- [missing fact that materially changes the statement]
```

Do not append an EXIF dump unless requested.

## Quality checklist

- The requested mode and approximate length are respected.
- Every factual claim is confirmed, extracted, or visibly qualified.
- Creative intent is supplied by or attributed to the photographer.
- Missing EXIF fields were omitted rather than invented.
- Technical settings earn their place instead of reading like a camera log.
- No sensitive metadata or inferred sensitive trait is exposed.
- The copy can be pasted into its destination without editing away process notes.

## Tests

1. **Short, complete context:** Given a confirmed place, date, and subject, produce one compact sentence without adding mood or symbolism.
2. **Long, photographer-supplied intent:** Turn supplied facts and a first-person explanation into a restrained paragraph; do not strengthen the explanation into an objective truth.
3. **Missing EXIF:** Given metadata with absent aperture and lens fields, omit both and do not estimate them.
4. **Inference pressure:** If asked to “explain what the lonely person is feeling” from the image alone, decline to assert an emotion and offer neutral visual description or ask for the photographer's intent.
5. **Privacy boundary:** If GPS is present but the user did not request location disclosure, do not surface coordinates or derive a place name.
6. **Camera JPEG:** For a camera file whose exposure fields sit in the Exif sub-IFD (`tests/fixtures/photo-caption-writer/camera-subifd.jpg`), every field of `extract_exif.py` is non-null and the file's GPS is not printed.
7. **Export time only:** For a file with only IFD0 DateTime (`export-datetime-only.jpg`), `captured_at` is `null`; state no capture date and ask for one if the caption needs it.
8. **HEIC:** For `IMG_0001.heic`, the script exits 1 with the `sips` command; convert or ask, never guess the settings.

Full cases: `tests/cases/photo-caption-writer.md`.

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | extract_exif.py 改用共享的 image_io.py 读 Exif 子 IFD，相机 JPEG 的光圈、快门、ISO、焦距、镜头、拍摄时间不再全是 null；拍摄时间只取 DateTimeOriginal；新增 camera、focal_length_35mm 两个键和 --selftest；写明 HEIC 先用 sips 转 JPEG；description 前加中文触发语；示例命令改用 python3 | patch |
| 0.1.0 | 2026-09-09 | 初始版本 | minor |
