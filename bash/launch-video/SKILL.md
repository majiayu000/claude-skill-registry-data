---
name: launch-video
description: |
  为开源项目制作约 30 秒的发布宣传视频（1080p MP4，16:9 或 9:16，带配乐和音效）：痛点 → 亮相 → 原理 → 可核实的证据 → 安装命令。先按项目、渠道和受众从 29 种视觉风格（扁平动态图形、动态排版、等轴 2.5D、数据新闻、粘土 3D、弥散玻璃、Synthwave、故障艺术、HUD、粒子成形、像素、水墨、剪纸、一笔线条等）中给出 3 个候选，并用真实素材渲染试样；选定后用 HTML/SVG/Canvas/three.js 写动画，逐帧渲染合成。产品画面来自真实录屏、真实输出和源码，配乐与音效按风格由脚本合成，无第三方授权问题。用于“给项目做宣传视频”“发布视频”“launch video”“做成赛博/水墨/粘土风的介绍视频”“给几个视频风格选”“README/推文配视频”等请求。与 readme-craft 同属开源项目分发系列。不用于实拍剪辑、AI 生成视频或纯 GIF 录屏。
trigger: /launch-video
compatibility: Claude Code, Codex
license: MIT
---

# launch-video

把一个开源项目的核心价值压成约 30 秒的视频：观众看完知道它解决什么问题、怎么做到、凭什么信、怎么开始。画面由 HTML 动画按时间逐帧渲染，所以文字清晰、可反复修改、可重新生成。风格可以随项目变化，证据不能变：无论选哪种风格，真实素材和可核实数字都是同一套。

同系列：`readme-craft` 写仓库首页。视频里的定位句、证据与安装命令应和 README 一致；README 过时或无法走通时先修 README。

## 0. 检查依赖（任一缺失即停止并告知）

```bash
node --version && ffmpeg -version | head -1 && python3 --version
```

在工作目录安装渲染依赖（只装一次）；3D 风格再装 three：

```bash
npm i -D playwright && npx playwright install chromium
npm i three   # 仅 3D 或着色器风格需要
```

已有 Chromium 时可设置 `CHROMIUM_PATH` 复用，免下载。

## 1. 取证：先找证据幕

读 README、包元数据、发布记录、源码入口、测试与已有案例，确定：

- **观众与痛点**：谁在什么场景遇到什么代价。
- **一句承诺**：项目名后面那一句，只强调一个词。
- **证据**：可复现的量化结果 > 真实产物 > 真实操作对比。证据与数字只取自可核实来源，并记下来源、版本、条件。
- **安装命令**：从 README 或发布页逐字复制，并核对当前发布版本（如 `npm view <pkg> version`）。
- **真实素材**：已有录屏、截图、导出文件；缺素材时实际运行项目录制，不画假界面。
- **机制隐喻**：用一个动词概括“原理”幕（组装、流转、过滤、监控、转换、一步到位……），第 2 步按它匹配风格。

没有任何可信证据时，明确告诉用户：视频只能展示真实操作过程，或建议先产出证据。不编数字。

## 2. 定风格：候选 → 试样 → 选定

读 `references/styles.md`，按其中的选型流程：

1. 整理信号：渠道与画幅、证据类型、机制隐喻、受众调性、品牌资产、用户点名的风格。
2. 用硬约束排除：素材承载力、画幅、语言文化、可行性。
3. 选 3 个差异明显、至少覆盖两个家族的候选：**稳妥 / 契合 / 大胆**。每个写清以下内容：
   - 理由（引用项目事实）
   - 签名镜头
   - 五幕各一句
   - 配乐 mood
   - 成本
   
   最后标出推荐项。
4. 读候选所在的配方文件（`references/styles/*.md`），为每个候选写一个 3–4 秒的试样页 `probe-<id>.html`：项目名 + 承诺句 + 一张嵌入真实素材的原理画面，用 `engine.js` 搭（第 3 步的目录结构）。渲染并拼成对比图：

```bash
for id in <id1> <id2> <id3>; do node <skill>/scripts/render.mjs --html probe-$id.html --stills 1.2,3.2 --out out/probes/$id; done
ffmpeg -v error -y -pattern_type glob -i 'out/probes/*/t*.png' -vf "scale=960:-1,tile=2x3" -frames:v 1 out/candidates.jpg
```

对比图每行一个候选（按 id 字母序），左右两列是同一候选的两张静帧。自己先看对比图：试样质感不达标的候选（3D 发灰、粒子不成形、文字溢出）先修或换掉，不把半成品交给用户比较。然后把候选说明和 `out/candidates.jpg` 交给用户选。

- 用户已点名风格：只做该风格的试样，确认可行后继续。
- 用户要求直接出片或无人值守：取推荐项继续，交付时说明理由和其余候选。

## 3. 分镜

按 `references/storyboard.md` 的五幕结构写分镜表：幕、时间、标题、一句解释、画面素材及其来源、真实性标签。再加上所选风格配方里的五幕映射、原生转场和签名镜头。用户未指定时默认：英文、16:9、30 秒、强调色取自产品主色。9:16 渠道按竖屏重新排版，不裁切横屏画面。

方向或素材存在重大不确定（选哪个项目、面向哪个渠道、证据是否可用）时，先向用户确认；其余按默认推进。

## 4. 搭建工作目录

工作目录放在用户指定位置；未指定时放在项目仓库之外的运营/素材目录，或仓库内 `docs/media/launch-video/`。源 HTML 是视频的“源码”，与成片放在一起；`node_modules/` 与 `out/` 不入库。

```bash
mkdir -p <work>/assets && cd <work>
cp <skill>/assets/engine.js .
cp <skill>/assets/template.html promo.html         # editorial 风格
cp <skill>/assets/three-starter.html promo.html    # 3D / 着色器风格（二选一）
python3 <skill>/scripts/fetch_fonts.py --out fonts "Instrument Serif:ital@0;1" "Inter Tight:wght@400;500;600" "JetBrains Mono:wght@400;600"
python3 <skill>/scripts/fetch_fonts.py --out fonts-cjk --text-from promo.html "Ma Shan Zheng"   # 中文字体只取用到的字
```

`<skill>` 指本 SKILL.md 所在目录。其他 2D 风格从空白页开始：`<div id="stage">` 加各幕 `<section class="scene">`，引入 `engine.js`，调用 `LV.start(...)`（用法见 `engine.js` 文件头）。字体按配方选用 Google Fonts 上的 OFL 字体。中文文案改动后，重跑带 `--text-from` 的抓取。

素材处理：

- 录屏转帧：`ffmpeg -i rec.mp4 -vf "fps=15,crop=W:H:X:Y" -q:v 3 assets/rec/%03d.jpg`，用 `setFrame` / `preloadFrames` 播放。先抽一帧确认裁剪去掉了字幕条、系统信息与隐私内容。
- 截图与导出图复制进 `assets/`，文件名写清来源。

## 5. 写动画

按分镜和风格配方实现每一幕：

- `render(t)` 必须是纯函数：DOM 样式、Canvas 像素、3D 姿态全部由 `t` 算出；随机数只用 `rng(seed)`；运动用闭式函数，不逐帧积分。
- 代码、字段名、输出格式照源码写；示意值要在画面上标注。
- 一幕一件事，标题 ≤ 8 个词。文字停留时间按 `references/styles.md` 的阅读时间规则计算。
- 动效与转场遵循所选风格的配方（editorial 用 `expoOut` 快起慢收、不回弹；扁平和粘土用 `backOut` / `squash`；像素和拼贴用 12fps 步进）。全片只用一套转场语法。
- 音画同步：每个音效所在的帧，对应画面必须已经开始动。分组元素按音效节拍逐个出现，不整块同时出现。

动手前读 `references/pitfalls.md`。

## 6. 静帧检查 → 全片渲染

```bash
node <skill>/scripts/render.mjs --html promo.html --stills 1,3.5,6,9,13,17,22,29.9
node <skill>/scripts/render.mjs --html promo.html --out out/silent.mp4
```

画布尺寸取页面的 `LV.start({ width, height })`，竖屏无需额外参数。逐张查看静帧：残影、溢出、占位符、文字可读性、风格签名是否成立、真实素材是否看得清。`render.mjs` 报页面错误时必须修复，不能忽略。

## 7. 配乐与音效

在工作目录写 `cues.json`。`mood` 取所选风格在总表里的 mood，`bpm` 可省略（用该 mood 的默认速度）。音效对齐到画面节点（点击、亮相、转场、状态出现、打字）；工具演示每 10 秒约 3–5 个，宁少勿密：

```json
{"mood": "synthwave", "bgm_gain": 0.5, "cues": [{"t": 4.6, "sfx": "reveal", "gain": 0.6}, {"t": 13.0, "sfx": "chime", "gain": 0.5}]}
```

mood：`calm bright synthwave chiptune pentatonic pulse`。内置音效：`click tick pop chime snap whoosh reveal type thud blip glitch drop`。

```bash
python3 <skill>/scripts/check_sync.py --video out/silent.mp4 --cues cues.json
python3 <skill>/scripts/mix.py --video out/silent.mp4 --cues cues.json --out out/<project>-launch.mp4
```

`check_sync.py` 会列出画面晚于音效的点：`LATE` 表示画面起动晚，`SLOW` 表示画面变化峰值晚超过 0.2s。这些只是嫌疑点，逐条用 `ffmpeg -ss <t-0.1> -i out/silent.mp4 -vf "fps=10,scale=480:-1,tile=4x2" -frames:v 1 cue.jpg` 看帧确认。真问题就改 HTML 或 cue 时间。持续运动的风格（网格滚动、粒子漂浮、背景流动）会让变化峰值不明显；细线描边、小图标这类小面积变化可能低于检测阈值；同一窗口里更大的场景变化也会盖住小元素。看帧确认画面已按时起动的，记为误报并在交付时注明。

用户有授权明确的音乐时用 `--music <file>` 替换；不要使用来源或授权不明的音频。

## 8. 验证

```bash
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate:format=duration -of compact out/<project>-launch.mp4
ffmpeg -v error -y -i out/<project>-launch.mp4 -vf "fps=1,scale=480:-1,tile=6x5" -frames:v 1 out/sheet.jpg
```

确认：有视频流和音频流，时长和画幅正确，每秒抽帧无残影与空白，首帧为第一幕，末帧停在安装画面。按 `references/pitfalls.md` 的自检清单逐条核对。音频的主观听感无法由脚本判断，交付时请用户试听。

## 输出

交付以下内容：

- 成片路径
- 所选风格及理由（以及未选的候选和 `out/candidates.jpg`）
- 源 HTML 与 `cues.json`
- 分镜摘要：每幕内容及素材来源
- 真实性说明：哪些是真实录屏，哪些是示意
- 验证结果
- 修改方式：改 HTML 或 cues 后重跑第 6、7 步；换风格就回到第 2 步

发布到 X、社区、README 或任何对外渠道，都需要用户对具体平台和内容的授权；未授权时只交付成片和建议文案。
