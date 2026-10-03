---
name: ppt-nano
description: 白板板书风格 PPT 生成。用户说「做PPT」「生成幻灯片」「白板风格演示」「板书」等时使用。支持 5 步标准工作流：确认风格→整理页码→检查依赖→逐页生成→合成下载。输出高保真白板照片，手写感 shufa 笔触，黑/蓝/红三色马克笔，适合教学、汇报、头脑风暴。每页需参考图和提示词前缀，封面必用专用前缀防止保留原文字。

---


# PPT-Nano 技能 — 白板板书风格PPT生成

## 🚨 触发条件
用户说「ppt-nano」「生成PPT」「做PPT」「白板风格PPT」等关键词时，**必须严格按以下流程执行，不可跳步！**

---

## ✅ 标准执行流程（5步，必须按顺序）

### 第一步：告知风格

立即回复：

> 🖊️ **白板板书风格**
> 真实白板照片 + 马克笔手写（shufa笔触）+ 手绘插图，黑/蓝/红三色马克笔

---

### 第二步：接收文案，整理确认表（必须输出表格）

收到文案后，**立即整理成确认表**发给用户，格式：

> 📋 梳理如下，请确认：
>
> | 页码 | 页面类型 | 参考图 | 内容摘要 |
> |------|---------|--------|---------|
> | 封面 | 首页 | cover.jpg | 主标题 / 副标题 |
> | P1 | 内容页 | content.jpg | 标题 / 要点摘要 |
> | P2 | 图表页 | chart.jpg | 标题 / 数据摘要 |
> | ... | ... | ... | ... |
>
> 共 X 页，请确认页面分配是否正确，确认后说"启动生成"！

**页面类型判断规则：**
- 有时间轴/流程/组织架构 → **导航页** navigation.jpg
- 有数据表格/数字对比 → **图表页** chart.jpg
- 有场景故事/对话泡泡 → **内容页** content.jpg
- 纯文字列表/要点 → **文字页** text.jpg（=content.jpg）
- 封面 → **首页** cover.jpg
- 结尾 → **尾页** closing.jpg

等用户确认后再进入第三步。

---

### 第三步：依赖检查（首次使用或不确定时执行）

```bash
python -c "import openai, PIL; print('ok')"
```

如果失败，先安装：
```bash
python -m pip install openai pillow python-pptx
```

---

### 第四步：逐页生成并发预览

**每页命令模板（严格执行）：**

```bash
python {baseDir}/scripts/generate_image.py \
  --prompt "{对应前缀}{页面专属提示词}" \
  --filename "{输出文件名}.jpg" \
  --resolution 2K \
  --aspect-ratio 16:9 \
  -i "{参考图绝对路径}"
```

> Windows PowerShell 下反斜杠续行用反引号（`` ` ``），或写成一行。

**关键参数说明：**
- `-i` 传入参考图（image-to-image 模式，必须带）
- `--resolution` 固定用 `2K`（支持 `2K` / `3K`，不支持其他值）
- `--aspect-ratio` 固定用 `16:9`
- `--filename` 必须以 `.jpg` 结尾（模型输出固定为 JPEG）
- 每次调用只生成一页

---

### ⚡ 提示词前缀（按页面类型选用，不可省略）

#### 通用页（内容页 / 图表页 / 导航页 / 尾页）
```
按参考图出图，白板背景和整体版式保留不变，白板上的所有原有文字和图案全部清除，按以下文案重新设计内容。中文必须是马克笔shufa笔触风格，配图手绘风格。Chinese text MUST use thick shufa-style ink brush marker calligraphy — bold chunky strokes, NOT printed font. 颜色规则：黑色用于主标题和正文，蓝色用于副标题、数据标注和补充信息，红色用于强调词、结论句和圆圈高亮。配图颜色按内容用红蓝马克笔适配。
```

#### 封面页（cover.jpg 专用，必须使用此版本）
```
按参考图出图，白板背景和整体版式保留不变，白板上的所有原有文字和图案全部清除，不保留任何已有标题或说明文字。按以下文案重新设计封面内容，主标题突出显示，副标题用蓝色马克笔书写。封面版面要充分利用，除主标题和副标题外，可添加与主题相关的手绘装饰图案、关键词标注、或视觉分割线，确保白板面积利用率不低于60%。中文必须是马克笔shufa笔触风格，配图手绘风格。Chinese text MUST use thick shufa-style ink brush marker calligraphy — bold chunky strokes, NOT printed font. DO NOT reproduce any text from the reference image. 颜色规则：黑色用于主标题，蓝色用于副标题和说明文字，红色用于强调词和圆圈高亮。
```

> **说明：** 封面参考图含有固定示例文字，若使用通用前缀模型容易将其保留。封面页必须使用封面专用前缀，明确要求清除原有文字。

---

**参考图路径（`{baseDir}/styles/whiteboard/pages/`）：**
```
├── cover.jpg       ← 首页专用（必须配封面专用前缀）
├── chart.jpg       ← 图表页专用
├── navigation.jpg  ← 导航页专用
├── content.jpg     ← 内容页/文字页共用
├── closing.jpg     ← 尾页专用
└── text.jpg        ← 文字页（同 content.jpg）
```

**规则：**
- 每页必须带参考图（`-i`），不同页型严禁混用参考图
- 封面页（cover.jpg）必须使用封面专用前缀，不可用通用前缀
- 以脚本输出的 `MEDIA:` 行为准获取生成图片路径，不依赖 stderr 解析
- 只记录保存路径，不读取图片内容

---

### 第五步：所有页确认后合成 .pptx

所有页面确认后，调用合成脚本：

```bash
python {baseDir}/scripts/build_pptx.py \
  -i "slide1.jpg" "slide2.jpg" "slide3.jpg" \
  -o "{workspace}/你的文件名.pptx"
```

> `build_pptx.py` 已内置跨平台支持（Windows / macOS / Linux），统一使用 `python` 调用。中文路径乱码问题已在脚本内部处理，无需手动设置环境变量。

**build_pptx.py 参数说明：**
| 参数 | 说明 |
|------|------|
| `-i img1.jpg img2.jpg ...` | 图片路径列表，**按页序排列** |
| `--dir ./某目录/` | 扫描目录下所有 jpg（按文件名字母序） |
| `-o output.pptx` | 输出路径，默认 `output.pptx` |
| `--width` / `--height` | 幻灯片尺寸（英寸），默认 13.33 × 7.5（16:9） |

**机器可读输出：** 脚本最后一行输出 `PPTX:/path/to/file.pptx`，可直接解析路径。

合成完成后将 .pptx 文件路径告知用户。

---

## 📁 文件位置
- 参考图：`{baseDir}/styles/whiteboard/pages/`
- 生成脚本：`{baseDir}/scripts/generate_image.py`
- 合成脚本：`{baseDir}/scripts/build_pptx.py`
- 输出目录：`{workspace}/ppt_outputs/`

> `{baseDir}` = skill 所在目录（如 `~/.easyclaw/skills/ppt-nano`）
> `{workspace}` = `~/.easyclaw/workspace`

---

## ⚠️ 常见错误（禁止）
- ❌ 不问风格直接问文案
- ❌ 收到文案不整理确认表直接生成
- ❌ 不传参考图（`-i`）或混用参考图
- ❌ 封面页使用通用前缀（必须用封面专用前缀）
- ❌ 省略提示词前缀
- ❌ 用错参考图（如内容页用了 chart.jpg）
