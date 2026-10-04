---
name: laohan-notebooklm
description: 口播稿一键生成幻灯片图片，通过 NotebookLM 生成中文幻灯片，PDF 转图片输出供剪映使用。Use when 用户说"生成PPT""生成幻灯片""做PPT图片""幻灯片""PPT"或提到口播稿背景图/视觉素材。
version: "1.2.0"
---

# 口播稿幻灯片生成

> **定位（2026-09-20治理P2-20）**：研究辅助工具，非生产链路；生产视频的画面资产走本地素材库/网络素材合同（⑩）或动画实现（⑪），不走本工具。

把口播稿一键生成幻灯片图片，输出到 script.md 同级目录的 slides/ 子目录，剪映直接用。

## 核心理念

不加提示词、不加布局要求——NotebookLM 自由发挥效果最好。输出是半成品图片，布局和排版在剪映里调整，不在这里浪费时间。

## 不适用场景

- 想要精确控制每页内容和排版 → NotebookLM 不支持，用 python-pptx 手动生成 PPT
- 生成英文幻灯片 → 改 `--language en-US`，但本 skill 默认中文场景
- 没有 nlm CLI 或网络无法访问 NotebookLM → 先装依赖、解决网络问题

## 使用

```
/laohan-notebooklm <script.md路径>
```

## 流程

每步可能 SSL 超时，加重试（最多3次，间隔3秒）。

### 0. 准备

- 从 script.md 路径确定输出目录：script.md 所在目录下的 `slides/` 子目录
- `SCRIPT_DIR=$(dirname "$SCRIPT")`，`OUTPUT="$SCRIPT_DIR/slides"`
- `mkdir -p "$OUTPUT"`
- `cp "$SCRIPT" "$OUTPUT/script.md"`
- 确认网络可访问 NotebookLM（REGION_NOT_SUPPORTED 时需切换网络环境）

### 1. 创建笔记本

```bash
nlm notebook create "<标题>PPT"
```

记录返回的 NOTEBOOK_ID。

### 2. 上传素材

```bash
nlm source add NOTEBOOK_ID --file "$OUTPUT/script.md"
```

只上传口播稿原文，不加任何提示词或引导注释。

### 3. 触发生成

```bash
echo "y" | nlm slides create NOTEBOOK_ID --language zh-CN --length default
```

`--language zh-CN` 是关键，漏了生成英文版。

### 4. 轮询+下载+转图片（后台脚本）

必须用一个后台脚本一次性完成轮询、下载、转图片。用 `Bash` 工具的 `run_in_background: true` 执行：

```bash
NB="NOTEBOOK_ID"
TITLE="<标题>"
OUTPUT="<script.md所在目录>/slides"

for i in $(seq 1 20); do
  st=$(nlm studio status "$NB" 2>&1 | grep -o '"status": "[^"]*"' | head -1)
  echo "[$i] $st"
  echo "$st" | grep -q "completed" && break
  sleep 30
done

for i in 1 2 3; do
  nlm download slide-deck "$NB" -o "${OUTPUT}/${TITLE}.pdf" 2>&1 && break
  sleep 5
done

pdftoppm -png -r 200 "${OUTPUT}/${TITLE}.pdf" "${OUTPUT}/slide"
echo "Done: $(ls "${OUTPUT}"/slide-*.png | wc -l | tr -d ' ') slides"
```

后台完成后读取输出确认图片数量，告知用户。

## 输出

```
<script.md所在目录>/slides/
├── script.md
├── <标题>.pdf
├── slide-01.png
├── slide-02.png
└── ...
```

## 关键原则

- 不加提示词：只上传口播稿原文，NotebookLM 自由发挥效果最好
- 不加布局要求：布局在剪映里调整
- 输出到 script.md 同级的 slides/ 目录，与其他素材统一管理

## 前置依赖

- nlm CLI v0.5.25（`pip install notebooklm-mcp-cli`）
- poppler（`brew install poppler`）
