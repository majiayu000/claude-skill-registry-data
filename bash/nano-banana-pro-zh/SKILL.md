---
name: nano-banana-pro-zh
description: 使用 Nano Banana Pro (Gemini 3 Pro Image) 生成/编辑图像。用于图像创建或修改请求，支持文生图和图生图；支持 1K/2K/4K 分辨率；可使用 --input-image 参数编辑现有图像。
---

# Nano Banana Pro 图像生成与编辑

使用 Google 的 Nano Banana Pro API (Gemini 3 Pro Image) 生成新图像或编辑现有图像。

## 使用方法

使用绝对路径运行脚本（请勿先 cd 到技能目录）：

**生成新图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro-zh/scripts/generate_image.py --prompt "你的图像描述" --filename "输出文件名.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**编辑现有图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro-zh/scripts/generate_image.py --prompt "编辑指令" --filename "输出文件名.png" --input-image "输入图像路径.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**重要提示：** 始终从用户当前工作目录运行，以便图像保存在用户工作位置，而不是技能目录中。

## 默认工作流（草稿 → 迭代 → 最终）

目标：快速迭代，在提示词正确之前不要浪费时间生成 4K 图像。

- 草稿 (1K)：快速反馈循环
  - `uv run ~/.codex/skills/nano-banana-pro-zh/scripts/generate_image.py --prompt "<草稿提示词>" --filename "yyyy-mm-dd-hh-mm-ss-draft.png" --resolution 1K`
- 迭代：以小幅差异调整提示词；每次运行保持文件名更新
  - 如果是编辑：每次迭代使用相同的 `--input-image` 直到满意为止
- 最终 (4K)：仅在提示词确定后使用
  - `uv run ~/.codex/skills/nano-banana-pro-zh/scripts/generate_image.py --prompt "<最终提示词>" --filename "yyyy-mm-dd-hh-mm-ss-final.png" --resolution 4K`

## 分辨率选项

Gemini 3 Pro Image API 支持三种分辨率（K 必须大写）：

- **1K**（默认）- 约 1024px 分辨率
- **2K** - 约 2048px 分辨率
- **4K** - 约 4096px 分辨率

将用户请求映射到 API 参数：
- 未提及分辨率 → `1K`
- "低分辨率"、"1080"、"1080p"、"1K" → `1K`
- "2K"、"2048"、"普通"、"中等分辨率" → `2K`
- "高分辨率"、"高清"、"hi-res"、"4K"、"超清" → `4K`

## API 密钥

脚本按以下顺序检查 API 密钥：
1. `--api-key` 参数（如果用户在聊天中提供了密钥）
2. `GEMINI_API_KEY` 环境变量

如果两者都不可用，脚本将退出并显示错误消息。

## 预检与常见故障（快速修复）

- 预检：
  - `command -v uv`（必须存在）
  - `test -n \"$GEMINI_API_KEY\"`（或传递 `--api-key`）
  - 如果是编辑：`test -f "path/to/input.png"`

- 常见故障：
  - `错误：未提供 API 密钥。` → 设置 `GEMINI_API_KEY` 或传递 `--api-key`
  - `加载输入图像时出错：` → 路径错误或文件不可读；验证 `--input-image` 指向真实图像
  - "配额/权限/403" 类 API 错误 → 密钥错误、无访问权限或配额超限；尝试使用不同的密钥/账户

## 文件名生成

使用以下模式生成文件名：`yyyy-mm-dd-hh-mm-ss-name.png`

**格式：** `{时间戳}-{描述性名称}.png`
- 时间戳：当前日期/时间，格式为 `yyyy-mm-dd-hh-mm-ss`（24小时制）
- 名称：带连字符的描述性小写文本
- 保持描述部分简洁（通常 1-5 个词）
- 使用用户提示或对话中的上下文
- 如果不清楚，使用随机标识符（例如 `x9k2`、`a7b3`）

示例：
- 提示 "宁静的日式花园" → `2025-11-23-14-23-05-japanese-garden.png`
- 提示 "山上的日落" → `2025-11-23-15-30-12-sunset-mountains.png`
- 提示 "创建一个机器人图像" → `2025-11-23-16-45-33-robot.png`
- 上下文不明确 → `2025-11-23-17-12-48-x9k2.png`

## 图像编辑

当用户想要修改现有图像时：
1. 检查他们是否提供了图像路径或引用了当前目录中的图像
2. 使用 `--input-image` 参数和图像路径
3. 提示词应包含编辑指令（例如 "让天空更戏剧化"、"移除人物"、"改为卡通风格"）
4. 常见编辑任务：添加/移除元素、改变风格、调整颜色、模糊背景等

## 提示词处理

**生成：** 将用户的图像描述原样传递给 `--prompt`。仅在明显不足时进行修改。

**编辑：** 在 `--prompt` 中传递编辑指令（例如 "在天空中添加彩虹"、"让它看起来像水彩画"）

在这两种情况下都要保留用户的创意意图。

## 提示词模板（高成功率）

当用户表达模糊或编辑需要精确时使用模板。

- 生成模板：
  - "创建图像：<主体>。风格：<风格>。构图：<镜头/拍摄>。光线：<光线>。背景：<背景>。调色板：<调色板>。避免：<列表>。"

- 编辑模板（保留其他所有内容）：
  - "仅更改：<单个更改>。完全保持：主体、构图/裁剪、姿势、光线、调色板、背景、文本和整体风格。不要添加新对象。如果存在文本，保持不变。"

## 输出

- 将 PNG 保存到当前目录（如果文件名包含目录，则保存到指定路径）
- 脚本输出生成图像的完整路径
- **不要读回图像** - 只需通知用户保存的路径

## 示例

**生成新图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro-zh/scripts/generate_image.py --prompt "一个带有樱花的宁静日式花园" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

**编辑现有图像：**
```bash
uv run ~/.codex/skills/nano-banana-pro-zh/scripts/generate_image.py --prompt "让天空更具戏剧性，添加暴风云" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```
