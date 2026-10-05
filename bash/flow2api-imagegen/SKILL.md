---
name: flow2api-imagegen
description: 使用你本机配置好的 Flow2API 接口生成图片，默认优先走 http://localhost:38000/v1，不出网更稳定。适用于用户说“帮我生图”“生成一张图”“画一个封面”“做一张海报”“用我的本地 Flow2API 模型出图”这类场景，支持 square、landscape、portrait、four_three、three_four 五种预设，也支持手动指定模型。
---

# Flow2API Image Generation

当用户要生图时，优先使用这个 skill。

## 配置位置

本 skill 使用用户级配置文件：

```bash
~/.flow2api-imagegen/config.json
```

默认已配置：

- `base_url`：`http://localhost:38000/v1`
- `fallback_base_url`：`https://flow2api.mianhua.ggff.net/v1`
- `api_key`
- 常用模型预设

## 用法

脚本路径：

```bash
python3 ~/.codex/skills/flow2api-imagegen/scripts/flow2api_imagegen.py
```

基本用法：

```bash
python3 ~/.codex/skills/flow2api-imagegen/scripts/flow2api_imagegen.py \
  --prompt "一只戴宇航员头盔的橘猫，电影感，细节丰富" \
  --output /tmp/cat.png
```

横图：

```bash
python3 ~/.codex/skills/flow2api-imagegen/scripts/flow2api_imagegen.py \
  --prompt "赛博朋克城市夜景，霓虹灯，电影海报风格" \
  --preset landscape \
  --output /tmp/city.png
```

竖图：

```bash
python3 ~/.codex/skills/flow2api-imagegen/scripts/flow2api_imagegen.py \
  --prompt "小红书封面，极简，奶油色背景，产品居中" \
  --preset portrait \
  --output /tmp/cover.png
```

手动指定模型：

```bash
python3 ~/.codex/skills/flow2api-imagegen/scripts/flow2api_imagegen.py \
  --prompt "现代家居客厅渲染图" \
  --model gemini-3.0-pro-image-landscape-2k \
  --output /tmp/home.png
```

## 预设映射

- `square` -> `gemini-3.0-pro-image-square-2k`
- `landscape` -> `gemini-3.0-pro-image-landscape-2k`
- `portrait` -> `gemini-3.0-pro-image-portrait-2k`
- `four_three` -> `gemini-3.0-pro-image-four-three-2k`
- `three_four` -> `gemini-3.0-pro-image-three-four-2k`

## 输出规范

生成成功后：

1. 返回图片保存路径
2. 简要说明用了哪个模型
3. 如果用户要预览，直接引用本地图片路径

## 失败处理

如果失败，先检查：

1. `~/.flow2api-imagegen/config.json` 是否存在
2. `base_url` 和 `api_key` 是否有效
3. 模型名是否还存在

必要时可先查询模型列表：

```bash
curl -sS http://localhost:38000/v1/models \
  -H 'Authorization: Bearer <API_KEY>'
```

## 补充说明

- 现在这个 skill 先封装的是**生图**
- 你这个本地接口里也有 `veo` 系列视频模型，但目前还没有单独封装成 video skill
- 如果你后面要，我可以继续给你补一个 `flow2api-videogen`
