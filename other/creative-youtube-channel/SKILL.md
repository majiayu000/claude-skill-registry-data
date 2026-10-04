---
name: creative-youtube-channel
description: Manage the 3-30 Channel YouTube MUSIC channel — create song notes, check the release pipeline, generate videos, track releases. Use when the user says "3:30 channel", "song pipeline", "release status", or music-channel work. NOT for the AI-Engineering tutorial channel (use creative-youtube-ai-engineering) or making the MV itself (use creative-mv-director, the MV entry point).
---

# YouTube Music Channel Manager

This skill manages the **3:30 Channel (AI Music)** project for publishing Suno-generated songs.

## Reference files (read on demand)

`SKILL_DIR` = `{home}/.claude/skills/creative-youtube-channel/`. The harness loads only this file; read a sibling with the Read tool when you reach the step that needs it.

| File | Priority | Read when |
|---|---|---|
| `<SKILL_DIR>/templates.md` | Required | Creating a song note, writing YouTube Title/Description/Tags (SEO), or running the publish checklist |
| `<SKILL_DIR>/scripts.md` | Required | Generating an animated / multi-scene MV, a Shorts clip, or a cover image; Codex dispatch; AI voice conversion |

## Project Location

- **Main Plan**: `10_Projects/YouTube-Music-Channel/YouTube Music Channel Plan.md`
- **Songs**: `10_Projects/YouTube-Music-Channel/songs/YYYY-MM-DD__SongName/`
- **Assets**: `10_Projects/YouTube-Music-Channel/assets/`
- **Suno Guide**: `30_Resources/Technology/Suno AI 曲风参考.md` — 曲风、提示词技巧、中文歌词技巧

## Commands

### Status Check
When user asks about channel status, pipeline, or what songs are ready:
1. Read all song notes in `songs/` folder
2. Check 版权记录 section for each song
3. Report:
   - ✅ **Uploaded**: YouTube link checkbox checked
   - ⏳ **Ready**: Video generated, no YouTube link yet
   - 🔄 **In Progress**: Missing checklist items

### New Song
When user wants to create a new song note:
1. Ask for: 歌名, 曲风, BPM, 语言, 系列 (if not provided)
2. Create folder: `songs/YYYY-MM-DD__歌名/`
3. Create note using template from existing songs (copy structure from `One Step 就好.md`)
4. Include: 基本信息, Suno Prompt, 歌词, YouTube上传信息, 版权记录

### Generate Video (Static Background)
When user wants to create a video with static breathing background:
1. Locate song folder and read note
2. Check prerequisites exist: audio (.mp3), cover (.png), lyrics
3. Get BPM and style from note
4. Look up color scheme in main plan (配色方案 table)
5. Generate breathing background using Python script from plan
6. Run ffmpeg composite command from plan
7. Update note: check "生成横屏视频"

Animated MV / Multi-Scene MV / Shorts / Cover generation, Codex dispatch, AI voice conversion: `<SKILL_DIR>/scripts.md`.

### Upload Checklist
When user is uploading or has uploaded a song:
1. Read the song note
2. Verify all copyright items are documented
3. After upload, update: YouTube链接, 上传日期
4. Link to [[inner child healing songs]]

---

## 🚀 Complete Publishing SOP

**CRITICAL**: 每次发布前 Claude 必须按此流程执行，不可跳过任何步骤。

### Phase 1: Pre-Upload (每首歌)

#### Step 1.1: 创建歌曲笔记

如果歌曲笔记不存在，使用模板创建。Song-note template: `<SKILL_DIR>/templates.md`.

#### Step 1.2: 填写版权清单

确保以下项目已完成再上传：
- [x] Suno 截图已保存（必须包含账号名、日期、订阅标识）
- [x] Suno 链接已记录
- [x] 视频文件已生成 (.mp4)

#### Step 1.3: SEO 优化

Title 格式 / Description 结构 / Tags 策略: `<SKILL_DIR>/templates.md`.

### Phase 2: Upload

#### Step 2.1: 确认上传参数

**上传前必须确认**:
- [ ] 视频文件路径正确
- [ ] Title/Description/Tags 已优化
- [ ] 目标 Playlist ID 正确
- [ ] Privacy 设置正确 (public/private/unlisted)

**Playlist IDs 速查**:
在专辑笔记或主计划中查找 Playlist ID。

#### Step 2.2: 执行上传（2026-09-14 起的正式路径）

**脚本**: EmptyOS 仓库的 `scripts/youtube_push_song.py`。它读取 release 文件夹里的 `release-package.md`（标题、描述、标签、置顶留言）。旧的 `10_Projects/YouTube-Music-Channel/scripts/youtube_upload.py` 会直接 `--privacy public`，不要再用。

```bash
python scripts/youtube_push_song.py "<歌曲文件夹或 release 文件夹>"         # dry run：连频道、查重名、跑 QA，不上传
python scripts/youtube_push_song.py "<歌曲文件夹或 release 文件夹>" --yes   # 私享上传 + 缩略图 + 字幕
```

脚本的设计行为：
- 只允许 `private` / `unlisted`；**转公开只在 YouTube Studio 手动做**。
- 频道守卫：连到的频道名必须包含 `Unsaid Signal`（token profile `music`）。
- 频道上已有同名影片 → 直接 SKIP。
- 素材按文件夹自动挑选：排序后第一个非 teaser 的 `*.mp4`、第一个 `*.png` 缩略图、第一个 `*.srt` 字幕。

**注意**（《不可说》MV 发布时学到的）：
- 报 `invalid_grant` 表示 token 失效。请 Kevin 运行 `python scripts/youtube_auth.py --profile music`，在浏览器里选 Unsaid Signal；Claude 不能代为登录。
- 同一首歌换新版本（例如静态版 → MV）时，新建一个 release 文件夹（例如 `release-v2-mv/`），放新的 `release-package.md` 和母带（硬链接即可）。标题必须和旧影片不同，否则会被查重跳过。旧影片保持私享，删不删由 Kevin 决定。
- 歌词已烧进画面时，文件夹里不要放 `.srt`，否则字幕会重复。
- 缩略图只认 `.png`（不超过 2 MB，1280×720 足够）。
- 上传脚本本身不设置 AI 合成内容声明。上传后可以用 API `videos.update(part=status)` 设 `containsSyntheticMedia: true`（2026-09-15《换班》实测生效）；但读回时这个字段不会出现，必须打开 Studio 确认「AI use: Yes」。
- 播放清单：用 API 新建清单后马上加影片，可能返回 404（清单尚未生效）。先按标题重新列出、确认只有一个，再加入；不要重复创建。清单 ID 记到专辑笔记。
- 720p 母带上传前先做 1080p 版，做法见 creative-mv-generator 的 `references/imagery-mv-production-lessons.md`。

#### Step 2.3: 定时发布 (可选)

发布时间照频道计划：**周三或周六 20:00（Australia/Sydney）**。AEST 是 UTC+10；10 月第一个周日起到 4 月第一个周日是 AEDT（UTC+11）。

如需定时发布（Kevin 确认日期后）：
1. 上传时用 `--privacy private`
2. 用 API 设定（2026-09-15《换班》实测）：`videos.update(part="status")`，body 里 `privacyStatus: private`、`publishAt: <UTC ISO>`、`containsSyntheticMedia: true`，并把原有的 `license`、`embeddable`、`publicStatsViewable`、`selfDeclaredMadeForKids` 原值带上（`part=status` 会整体替换可写字段）。
3. API 读回确认 `publishAt`；再打开 Studio 该影片页，确认 Visibility 显示 Scheduled、AI use 为 Yes、没有未保存的修改。
4. 也可以手动：YouTube Studio → Content → 选择视频 → Visibility → Schedule。
5. 置顶留言要等影片公开后才能发。

**分享版（给朋友用微信等传）**：从字幕版母带另压 720p。CRF 22 约 41 MB；两遍 950 kbps 约 25 MB，字幕仍清楚。要传到手机端的文件控制在 30 MiB 以下。

### Phase 3: Post-Upload

#### Step 3.1: 更新歌曲笔记

上传成功后立即更新：

```markdown
# frontmatter 更新
status: published
published: YYYY-MM-DD
youtube_id: VIDEO_ID

# 正文更新
**YouTube**: https://www.youtube.com/watch?v=VIDEO_ID

# 版权清单勾选
- [x] YouTube链接: https://www.youtube.com/watch?v=VIDEO_ID
- [x] 上传日期: YYYY-MM-DD
```

#### Step 3.2: 更新发布日历

更新 `YouTube Music Channel Plan.md` 的发布日历：

```markdown
| 日期 | 星期 | 歌曲 | 系列 | 状态 |
|------|------|------|------|------|
| MM-DD | Day | 歌名 | 系列 | ✅ 已发布 `VIDEO_ID` |
```

#### Step 3.3: 更新周记录

更新当周的周计划 `50_Journal/2026/2026-WXX.md`：

在 **Review → 完成** 部分添加：
```markdown
- [x] 发布 [歌名] 到 YouTube ✅ YYYY-MM-DD
  - URL: https://www.youtube.com/watch?v=VIDEO_ID
```

#### Step 3.4: 更新专辑笔记 (如适用)

如果是专辑中的歌曲，更新专辑笔记的发布状态表。

### Phase 4: 批量发布

发布多首歌时：

1. **先创建所有歌曲笔记** (Phase 1.1)
2. **填写所有版权清单** (Phase 1.2)
3. **优化所有 SEO** (Phase 1.3)
4. **批量上传** (可并行执行多个上传命令)
5. **批量更新记录** (Phase 3)

Publishing Checklist (发布时打勾): `<SKILL_DIR>/templates.md`.

---

## Quality Standards

Before marking any song complete:
- [ ] All 版权记录 items checked
- [ ] YouTube description matches template
- [ ] Audio backed up to OneDrive/Suno/
- [ ] Linked to inner child healing songs note
