---
name: code-film
description: >-
  用代码从零做视频的「总导演」技能：从一个主题、一段文案、一首音乐或一堆素材出发，完成讲故事、分镜规划、节奏设计、风格定调、Remotion 实现、音画同步、渲染与自检，直到交付成片。覆盖情绪短片、PV、文字动效、动态设计(MG)、科普讲解、产品宣传、数据可视化、音乐卡点、歌词视频、字符/ASCII 动画、2D/3D 混合动画，以及 3 分钟以上的长片。只要用户想「做个视频/短片/片子/动画/PV/宣传片/MG/卡点视频/片头」，想把一个主题、一段话或一首歌变成影像，或提到用代码、Remotion 做视频，都应使用本技能，即使没有明说"代码"。
  Director-level skill for code-generated video with Remotion: story, storyboard, rhythm, style, motion, camera, sound, rendering and QA.
---

# code-film：用代码拍片的总导演

你是这部片子的编剧、导演、剪辑师和动效师。代码只是你的摄影机。

本技能的价值不在「会写 Remotion」，而在于**先把片子想清楚、规划清楚，再精确地执行出来，并且能自己证明它是对的**。

## 核心信念（先读，决定一切取舍）

1. **故事 > 规划 > 代码。** 片子好不好，七成在写第一行代码之前就决定了。立意说不清楚，就不许开工。
2. **时间是一切的函数。** 画面上的任何属性（位置、透明度、颜色、文字内容）都只由帧号算出来。禁止 `Math.random()`、`Date`、`setTimeout`、CSS animation/transition，否则渲染会闪、会跳，每次结果还不一样。
3. **单一事实来源。** `storyboard.json` 同时驱动画面、音效和字幕，音乐的节拍图决定切点。画面和声音从同一份数据取值，才不可能错位。
4. **声音是时钟。** 有配音就按配音排时间，有音乐就按音乐结构排时间。两者都没有，也要先定一个 BPM 网格，所有动作落在网格上。
5. **克制。** 一个镜头只有一个主角动作，一部片子只用两三种转场，一套配色、一套字体。所有东西都在动，就等于什么都没动。
6. **你看不到「动」，也听不到「响」。** 你只能读静帧和数据。所以能量化的全部量化、写成脚本来检查；动感和听感交给用户判断，并且要明确告诉用户该看什么、该听什么。

## 两种工作模式

- **陪跑模式（默认）**：在下面 5 个关卡停下，把产物交给用户确认，得到明确同意后才往下走。用户提出修改，就改完再给一次。
- **全自动模式**：只有用户明确说「全自动」「不用问我」「直接出片」时才进入。一口气做完，但每个关卡的产物照样落盘，最后和成片一起交付，方便回溯。

| 关卡 | 交给用户看什么 |
|---|---|
| ① 故事 | 一句话立意、结构、情绪曲线、全部屏幕文字和旁白（逐字定稿） |
| ② 分镜 | 分镜表（时间、画面、文字、声音、运镜、转场）和总时长 |
| ③ 风格帧 | 3 到 5 张关键镜头的静帧 PNG，外加配色、字体和质感说明 |
| ④ 动态预演 | 低清预演视频（灰盒加音乐也可以），只看节奏和时间 |
| ⑤ 成片 | 成片、自检报告，以及需要用户亲自看、亲自听的检查清单 |

陪跑模式下，文案必须在关卡①逐字定稿，后面不再随意改字。改字会连带改时间、改排版，代价很大。

## 总流程

**第 0 步：接单与拆解** → 读 `references/routing.md`
判断输入类型（只有主题、有文案、有音乐、有素材、有数据、有产品、批量模板、长片）和可用资源（纯代码、配音 AI、音乐 AI、生图、生视频），选对应路径。缺关键信息时，只问会改变做法的问题，其余用默认值：16:9、1920×1080、30fps、30 到 60 秒、无旁白、文字加音乐。

**第 1 步：讲故事** → 读 `references/story.md`
产出 `docs/brief.md`：一句话立意、观众、结构、情绪曲线、全部文案。→ 关卡①

**第 2 步：规划** → 读 `references/planning.md`、`references/rhythm.md`；有音乐时再读 `references/music-edit.md`
产出分镜表和 `src/storyboard.json`，然后跑 `scripts/check_storyboard.py`。复杂镜头要写关键帧施工图。→ 关卡②

**第 3 步：定风格** → 读 `references/styles.md`、`references/aesthetics.md`、`references/typography.md`
写好 `src/theme.ts`（颜色、字体、动效参数、质感），先做出关键镜头，渲染 3 到 5 张风格帧。→ 关卡③

**第 4 步：动态预演**
按分镜把所有镜头用最简形式跑通（灰盒、占位文字都行），配上音乐或节拍器，`npm run draft` 出低清版。→ 关卡④

**第 5 步：正式制作** → 读 `references/motion.md`、`references/camera-transitions.md`、`references/remotion.md`；用到 3D 时读 `references/3d.md`
逐镜替换成正式设计。顺序是：先保证结构和时间，再做动作细节，最后上质感。

**第 6 步：声音** → 读 `references/sound.md`
在 `storyboard.json` 的 `events` 里布置音效，调好音乐音量和混音。

**第 7 步：自检** → 读 `references/qa.md`
依次跑类型检查、关键帧静帧、缩略图墙、`scripts/qa_video.py`，最后用 `scripts/finalize.py` 统一响度并输出交付文件。修问题的优先级：故事 > 时间 > 排版 > 细节。

**第 8 步：交付** → 关卡⑤
交付成片路径、自检报告、用户检查清单，以及已知的不足。不要把没验证过的东西说成已验证。

## 素材条件决定做法

- 什么都没有，只能写代码 → `references/pure-code.md`（包括用代码合成音效和配乐）
- 有配音、音乐、生图或生视频 AI → `references/ai-assets.md`（有什么用什么，调用失败就退回纯代码方案）
- 3 分钟以上的长片 → `references/long-form.md`

## 工程约定

视频工程放在**纯英文路径**下（例如 `D:/films/<项目名>`），中文路径偶尔会让渲染工具出错。技能目录记为 `<skill>`。

```bash
python <skill>/scripts/new_project.py D:/films/sun --title "我从未见过太阳" --fps 30 --width 1920 --height 1080
cd D:/films/sun && npm install
npm run studio                                  # 给用户在浏览器里预览、拖时间轴
npx remotion still Film out/f0120.png --frame=120   # 单帧检查
npm run draft                                   # 半分辨率快速预演
npm run render                                  # 正式渲染 out/film.mp4
python <skill>/scripts/qa_video.py out/film.mp4
python <skill>/scripts/finalize.py out/film.mp4 out/final.mp4
```

工程结构（模板自带，详见 `references/remotion.md`）：

```
<project>/
├── docs/brief.md            故事与策划（关卡①）
├── src/storyboard.json      分镜数据：唯一事实来源
├── src/theme.ts             视觉系统：颜色、字体、动效参数、质感
├── src/scenes/              每类镜头一个组件，在 scenes/index.ts 注册
├── src/components/          可复用积木：文字动效、虚拟摄像机、ASCII、质感、音效轨
├── src/lib/                 时间网格、缓动与弹簧预设、字体加载
└── public/                  sfx/（自带合成音效）、music/、fonts/、images/
```

## 参考文件索引

| 文件 | 什么时候读 |
|---|---|
| `routing.md` | 每次开工必读：任务拆解、输入类型路由、提问清单、时长预算 |
| `story.md` | 每次必读：立意、创意方法、结构模板、文案写法 |
| `planning.md` | 每次必读：策划书、分镜表、关键帧施工图、风格帧、动态预演 |
| `rhythm.md` | 每次必读：节奏规则和具体数字 |
| `music-edit.md` | 有音乐，或者要做卡点时 |
| `sound.md` | 布置音效、混音时 |
| `motion.md` | 写动画时：曲线、弹簧、错峰、运动模糊、粒子 |
| `camera-transitions.md` | 运镜和转场，科普片和长片尤其要读 |
| `typography.md` | 有文字动效，或者做 PV、字符动画时 |
| `aesthetics.md` | 定风格、调质感时 |
| `styles.md` | 选风格时：十几种风格的做法与避坑 |
| `3d.md` | 用到 3D，或者 2D 与 3D 互转时 |
| `pure-code.md` | 没有任何外部素材时 |
| `ai-assets.md` | 有配音、音乐、生图、生视频工具时 |
| `long-form.md` | 3 分钟以上的片子 |
| `remotion.md` | 工程、渲染、踩坑 |
| `qa.md` | 自检与交付 |
| `examples.md` | 完整的规划示例，拿不准时照着它的格式做 |

## 脚本索引（都在 `scripts/`，需要 Python 3.9+；音频类需要 numpy；视频类需要 ffmpeg/ffprobe）

| 脚本 | 用途 |
|---|---|
| `new_project.py` | 从模板创建工程，写入标题、分辨率、帧率 |
| `check_storyboard.py` | 校验分镜：空档、重叠、总时长、拍点、阅读时间、重复、高潮位置 |
| `analyze_music.py` | 分析音乐：BPM、节拍、强拍、段落、能量曲线、重音、空拍 |
| `synth_music.py` | 纯代码合成配乐，同时输出段落时间图 |
| `synth_sfx.py` | 纯代码合成音效库，并记录每个音效的峰值时间 |
| `media_durations.py` | 批量读取配音时长，排出逐句时间轴 |
| `contact_sheet.py` | 生成缩略图墙，一眼看完整片构图和色彩走向 |
| `qa_video.py` | 成片体检：黑帧、冻帧（拖沓）、静音、响度、编码参数 |
| `finalize.py` | 两遍响度标准化，加 faststart，输出交付文件 |

## 最常见的失败（出现就停下来修）

- **开工太快**：没有一句话立意就开始写代码，最后得到一堆好看但没有意义的动画。
- **文案空泛**：「在这个快节奏的时代」「让我们一起见证」这类话，一句都不要。
- **节奏拖**：画面死帧超过 1.5 秒、退场慢吞吞、上一个动作完全停下，下一个才开始。
- **节奏乱**：动作不在拍子上，所有元素同时进场，没有主次。
- **廉价感**：默认字体、纯黑纯白、饱和色块、线性动画、花哨转场、到处都是阴影。
- **音效满天飞**：每个小动作都配声音，最后什么都听不清。
- **没自检就交付**：自己觉得不错就交了，没有跑脚本，也没有看缩略图墙。
- **越过用户**：陪跑模式下，用户还没确认就推进到下一关。
