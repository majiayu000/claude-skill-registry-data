---
name: tool-comfyui-image
description: Generate and edit AI images through the local ComfyUI API (FLUX) — txt2img, img2img variation, 4x upscale, AnimateDiff image-to-motion, outpaint/extend-canvas, and cover generation. Use when the user says "生成图片" / "generate image", "图片变体" / "image variation", "放大图片" / "upscale", "图片动起来" / "animate image", "扩展画布" / "outpaint", or "生成封面" / "generate cover". NOT for AI music-video scene generation (use creative-mv-generator).
---

# ComfyUI Image Generation Skill

通过 ComfyUI API 生成和处理 AI 图像。

## 触发词

| 用户说 | 动作 |
|--------|------|
| "生成图片" / "generate image" | txt2img |
| "图片变体" / "image variation" | img2img |
| "放大图片" / "upscale" | upscale 4x |
| "图片动起来" / "animate image" | AnimateDiff |
| "扩展画布" / "outpaint" / "extend canvas" | outpainting |
| "生成封面" / "generate cover" | 封面生成流程 |

## Prerequisites (前置条件)

- ComfyUI must be running on the Home PC (`http://{homepc}:8188`), reachable over Tailscale.
- Required models installed (FLUX / upscale / AnimateDiff, per the workflow you invoke).
- Generation scripts live in the vault, not this skill folder — see the paths in each workflow below.

**Probe ComfyUI first — if it is down, STOP and tell the user** (there is no local fallback):
```bash
curl -s "http://{homepc}:8188/system_stats" | head -c 100
```

## 可用功能

### 1. txt2img - 文生图

**脚本**: `30_Resources/Technology/AI-LLM/scripts/flux_generate.py`

```bash
python3 flux_generate.py "prompt" output.png
python3 flux_generate.py "prompt" output.png --model dev  # 高质量但非商用
python3 flux_generate.py "prompt" output.png --width 1792 --height 1024  # 自定义尺寸
python3 flux_generate.py "prompt" output.png --seed 42  # 可复现
```

**模型选择**:
- `schnell` (默认): Apache 2.0 可商用，4步，快速
- `dev`: Non-commercial，30步，高质量

### 2. img2img - 图生图

**脚本**: `30_Resources/Technology/AI-LLM/scripts/flux_img2img.py`

```bash
python3 flux_img2img.py input.png "style description" output.png
python3 flux_img2img.py input.png "cyberpunk neon" output.png --denoise 0.5
```

**参数**:
- `--denoise`: 0.0-1.0，越低越接近原图 (推荐 0.4-0.7)

### 3. upscale - AI 放大

**脚本**: `30_Resources/Technology/AI-LLM/scripts/flux_upscale.py`

```bash
python3 flux_upscale.py input.png output.png
python3 flux_upscale.py input.png output.png --model ultrasharp  # 照片
python3 flux_upscale.py input.png output.png --model nmkd        # 通用
python3 flux_upscale.py input.png output.png --model realesrgan  # 动漫
```

### 4. AnimateDiff - 图片转动画

**脚本**: `30_Resources/Technology/AI-LLM/scripts/animatediff_generate.py`

```bash
# img2vid
python3 animatediff_generate.py --image input.png --prompt "gentle camera pan" --output output.gif

# txt2vid
python3 animatediff_generate.py --prompt "city skyline, camera panning" --output output.gif

# 自定义帧数
python3 animatediff_generate.py --image input.png --prompt "zoom in" --output output.gif --frames 24
```

**注意**: AnimateDiff 使用 SD 1.5 (DreamShaper)，不是 FLUX

### 5. outpaint - 扩展画布

**脚本**: `30_Resources/Technology/AI-LLM/scripts/flux_outpaint.py`

```bash
# 扩展到 16:9 横版
python3 flux_outpaint.py input.png output.png --target 1792x1024

# 扩展到 9:16 竖版
python3 flux_outpaint.py input.png output.png --target 1024x1792

# 指定扩展方向
python3 flux_outpaint.py input.png output.png --left 256 --right 256

# 自定义扩展区域内容
python3 flux_outpaint.py input.png output.png --target 1792x1024 --prompt "sunset sky"
```

### 6. 封面生成 (YouTube 频道)

**脚本**: `10_Projects/YouTube-Music-Channel/scripts/generate_cover.py`

```bash
python3 generate_cover.py \
    --song "歌名" \
    --style "City pop, 95 BPM" \
    --mood "自信、温暖" \
    --lyrics "歌词片段" \
    --output 输出目录
```

**输出**: 2 竖版 (9:16) + 2 横版 (16:9)

## 脚本路径

所有脚本位于:
- 通用脚本: `30_Resources/Technology/AI-LLM/scripts/`
- 频道脚本: `10_Projects/YouTube-Music-Channel/scripts/`

## 已安装模型

### FLUX (txt2img, img2img)
| 模型 | 许可证 | 用途 |
|------|--------|------|
| flux1-schnell-fp8.safetensors | Apache 2.0 | 商用 |
| flux1-dev-fp8.safetensors | Non-commercial | 高质量 |

### Upscale (放大)
| 模型 | 适用 |
|------|------|
| 4xUltrasharp | 照片、写实 |
| 4xNMKDSuperscale | 通用 |
| 4xRealisticrescaler | 动漫 |

### AnimateDiff
| 模型 | 用途 |
|------|------|
| dreamshaper_8.safetensors | SD 1.5 基础模型 |
| mm_sd_v15_v2.ckpt | Motion module |

## 常见问题

### ComfyUI 连不上
1. 确认 PC 开机且 ComfyUI 在运行
2. 检查 Tailscale 连接: `tailscale status`
3. PC 上运行 `run_nvidia_gpu.bat` (包含 `--listen 0.0.0.0`)

### CUDA Out of Memory
修改 Windows 页面文件大小到 32GB

### 图片颜色问题 (RGBA)
安装 `masquerade-nodes-comfyui` 节点处理 RGBA 图片

## 相关笔记

- [[ComfyUI]] - 主工具笔记
- [[FLUX Image Models]] - FLUX 模型详情
- [[Stable Diffusion Models]] - SD 模型详情
- [[ComfyUI Custom Nodes]] - 已安装插件
