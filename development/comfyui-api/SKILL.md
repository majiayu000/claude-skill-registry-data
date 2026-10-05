---
name: comfyui-api
description: ComfyUI API 调用、工作流构建、模型管理和提示词编写 — 针对实验室 4×A10 服务器
---

## ComfyUI GUI 故障诊断

### 用户说"点击运行没反应"

**现象：** GUI 上点 Queue Prompt/Add Queue 后，没有任何反馈，进度条不动。

**排查步骤（按优先级）：**

```bash
# 1. 检查队列——很可能已经在跑了（GUI 前端线程卡了，后端正常）
curl -s http://localhost:8188/queue | python3 -m json.tool

# 2. 检查 GPU 内存——如果 GPU 满载，任务在排队
nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader,nounits

# 3. 检查 API 是否响应
curl -s -o /dev/null -w '%{http_code}' http://localhost:8188/
```

**常见原因：**
| 原因 | 表现 | 解决 |
|------|------|------|
| GPU 满载（22+/23GB） | queue_running 有任务 + GPU memory.used 接近 total | 等当前任务跑完，queue_pending 会自动进入 |
| GUI 前端线程卡 | 浏览器无反馈但后端已在处理 | 刷新页面（F5），看队列增加任务 |
| 工作流特定节点报错 | queue 中任务状态异常 | 查 `history` API 看 error |

**注意：** ComfyUI 在加载大模型（Wan2.2 14B ~10GB+）时 GUI 线程可能短暂无响应，这不影响后端队列的正常运行。
- **SSH**: `ssh -p 35043 po@3722d01e5a6f.ofalias.com` (OpenFRP 隧道, 带宽有限, 少传文件)
- **⚠️ SSH 断连**: fish fastfetch banner 破坏非交互 SSH；需用 `bash -c` 包装或等 30s+ 后再连。详见 `lab-server-deploy` skill
- **本地 API 隧道**: 已建 `localhost:18188 → server:8188`（SSH 转发，非持久，可能需重建）
- **服务器管理**: 1Panel + OpenResty Docker 反向代理。公网仅开放 8080 端口。部署新服务见 `lab-server-deploy` skill
- **文件下载（推荐，绕过 fish greeting）**:
  ```bash
  # 远端先用 base64 编码，本地解码
  ssh -p PORT user@host 'base64 -w0 /path/to/file' | base64 -d > local_file
  ```
- **硬件**: 4×NVIDIA A10 (23GB 显存/卡) + 125GB RAM
- **Shell**: fish (远端, 启动时跑 fastfetch 打 system info banner, 会破坏 scp/sftp/scp 协议。本地已修复: `sed -i 's/^fastfetch/#fastfetch/' ~/.config/fish/config.fish`)
- **Python 环境**: venv 在 `/data/comfy/comfy-env/`
- **工作流目录**: `/data/comfy/ComfyUI/user/default/workflows/`
- **输出目录**: `/data/comfy/ComfyUI/output/`

## API 工具脚本
服务器上已有 `/data/comfy/comfy_api.py`，支持：
```
source /data/comfy/comfy-env/bin/activate
python3 /data/comfy/comfy_api.py queue              # 查看队列
python3 /data/comfy/comfy_api.py submit WF.json     # 提交
python3 /data/comfy/comfy_api.py status PROMPT_ID   # 状态
python3 /data/comfy/comfy_api.py image [关键词]      # 输出文件
python3 /data/comfy/comfy_api.py list-workflows     # 已有工作流
python3 /data/comfy/comfy_api.py list-models        # 模型列表
```

## 学习新模型/工作流的正确流程

当需要在服务器上学习一个未知的 ComfyUI 模型或工作流时，按以下顺序操作：

### 1. 查官方文档（第一优先级）
- **ComfyUI 内置节点文档**: `https://docs.comfy.org/built-in-nodes/{node_name}`
- **ComfyUI 教程/工作流模板**: `https://docs.comfy.org/tutorials/video/wan/`
- **HuggingFace 模型卡片**: 模型发布页通常有架构说明和推荐参数
- **ComfyUI 官方博客**: `https://blog.comfy.org/` — 新功能发布和最佳实践

### 2. 查社区资源（第二优先级）
- YouTube 教程（搜索 "ComfyUI {model_name} tutorial"）
- Reddit r/comfyui, r/StableDiffusion
- HuggingFace Discuss 论坛（prompt 技巧、常见问题）
- Kijai 的 HuggingFace 仓库（模型 fp8 转换 + README 说明）

### 3. 分析工作流 GUI JSON（第三优先级——验证已学知识）
- 工作流文件在 `/data/comfy/ComfyUI/user/default/workflows/`
- 格式是 ComfyUI 0.4 subgraph 格式：`{"nodes": [...], "links": [...], "widgets_values": [...]}`
- `widgets_values` 按序对应无 `link` 的 inputs
- `mode: 4` = bypassed（跨掉的子管线）
- `mode: 0` = 激活
- 数据连接通过 `links` 数组: `[id, src_id, src_slot, tgt_id, tgt_slot, type]`

### 4. 调试工具
- **节点参数查询**: `curl http://localhost:8188/object_info/{class_type}` 返回该节点的所有输入、输出、参数范围、默认值
- **队列状态**: `curl http://localhost:8188/queue`
- **历史记录**: `curl http://localhost:8188/history/{prompt_id}`
- **所有历史**: `curl http://localhost:8188/history`

### Anima 模型 + AstrBot promax 集成 pitfall(2026-07-08 root-caused)

AstrBot `astrbot_plugin_ComfyUI_promax` 的 `comfyui_txt2img` 路径(LLM tool 调)原本走 `_build_comfyui_prompt` 标准 T2I 路径,用 `CheckpointLoaderSimple` 直接加载 Anima ckpt。**Anima 不内嵌 CLIP/VAE**,这条路径会立即报 `clip input is invalid: None`。

**修法**: `comfyui_txt2img` 必须先检测 `eng.workflow_prefixes["anima"]`,有就走 `anima_t2i` workflow(`anima_t2i.json`),由 workflow 自带的独立 `CLIPLoader(qwen_3_06b_base.safetensors, type=stable_diffusion) + VAELoader + CheckpointLoaderSimple` 三节点解决;无 anima workflow 才回落到标准路径(只对内嵌 CLIP 的 SD/SDXL ckpt 工作)。

**坑 — 容易改错的地方**:
- 把 CLIPLoader 的 `type` 从 `stable_diffusion` 改成 `qwen_image` 看似更"准确",**但 8 次跑成功已验证 stable_diffusion 工作**——Anima ckpt 内部 checkpoint loader 会覆盖 type 字段,改 type 反而有引入新 bug 的风险
- promax schema 标 `enable_translation: "已弃用"`,但代码里 `_translate_cn_prompt` 仍自动调,LLM 翻译失败 fallback 原文 → 中文 prompt 进 Qwen3 出乱码。**不要靠 promax 翻译,LLM tool 路径直接传英文 Danbooru 标签**

`/home/po/astrbot/data/plugins/astrbot_plugin_ComfyUI_promax/workflow/anima_t2i.json` 的 node 11 硬编码 `"best quality, score_7, ..."` 仍是 workflow 兜底 starter,LLM tool 路径会覆盖它。

→ AstrBot 端 LLM 调 tool 失败的更多 pitfall 见 [astrbot-operations](../../astrbot-operations/SKILL.md) 的"LLM/Provider 端故障排查"段。

## Wan2.2 模型架构关键理解
Wan2.2 系列使用**双模型级联**架构（高噪 + 低噪），不同任务共享同一组模型：

| 任务 | 使用的模型 | 区别节点 | 有无独立 checkpoint |
|------|-----------|---------|-------------------|
| T2V (文生视频) | high_noise + low_noise | EmptyHunyuanLatentVideo | 有独立 T2V 模型 |
| I2V (图生视频) | high_noise + low_noise | WanImageToVideoLatent | **与 FLF2V 共用** |
| FLF2V (首尾帧) | high_noise + low_noise | **WanFirstLastFrameToVideo** | **无独立模型！复用 I2V 模型** |
| T2V Fun Camera | high_noise + low_noise | WanFunControl | 有独立模型 |

注意：Wan2.1 的 FLF2V 有独立 checkpoint (`wan2.1_flf2v_720p_14B_fp16`)，但 Wan2.2 FLF2V **没有**，用同一组 I2V 模型文件。

### 6. WAN 视频模型 Prompt 编写最佳实践（来自 HuggingFace 官方论坛）

```
框架：Cast & Count + Setting & Time + Camera & Framing + Action Timeline + Motion Boundaries + Visual Style
```

| 要素 | 说明 | 示例 |
|------|------|------|
| **Cast & Count** | 明确指出角色数量和身份 | "Exactly two people: one man and one woman in their 30s" |
| **Setting & Time** | 锚定环境和时间 | "Indoor restaurant, warm candlelit evening, wooden table" |
| **Camera & Framing** | 镜头语言 | "Static camera, eye-level, medium shot. No zoom, no pan." |
| **Action Timeline** | 按时间顺序描述动作演进 | "The man keeps his arm around her. They lean toward each other. They talk and smile." |
| **Motion Boundaries** | 正面约束限制动作 | "They remain seated. They do not stand up. Nobody else enters the frame." |
| **Visual Style** | 风格和氛围 | "Cinematic, naturalistic lighting, soft shallow depth of field" |

**关键陷阱**: CFG=1 时负面 prompt 基本无效。使用 WanVideoNAG 节点（NAG scale=11, alpha=0.25, tau=2.5）在 CFG=1 下恢复负面控制。

### 7. 视频质量验证
生成后必须验证输出：
```bash
file output.mp4           # 确认是有效 MP4
ffprobe -v quiet -show_streams output.mp4 | grep -E "codec_name|width|height|duration|nb_frames|r_frame_rate"
```
常见问题: 只有首帧后灰屏 → KSampler 参数错误（scheduler/step 分割/leftover_noise）

## 可用模型

### Diffusion Models
- `flux-2-klein-base-9b-fp8.safetensors` — Flux 2 Klein 文生图
- `z_image_turbo_bf16.safetensors` — Z Image Turbo (SD3架构, 快速)
- `qwen_image_edit_2509_fp8_e4m3fn.safetensors` — Qwen 图像编辑
- `wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` — Wan2.2 图生视频 (I2V/FLF2V共用)
- `wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors`
- `Wan21_SkyReelsV3-R2V_fp8_scaled_mixed.safetensors` — SkyReels V3 参考图生视频 (R2V)
- `ltx-2-19b-dev-fp8_transformer_only.safetensors` — LTX Video
- `MelBandRoformer_fp32.safetensors` — 音频分离
- `SkyReelsV3` 系列 — 视频生成

### LoRAs
- `wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors` — Wan2.2 I2V/FLF2V 4步 LoRA (高噪)
- `wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors` — Wan2.2 I2V/FLF2V 4步 LoRA (低噪)
- `wan2.1_i2v_lora_rank64_lightx2v_4step.safetensors` — SkyReels-V3/Wan2.1 4步 LoRA

### Checkpoints
- `hunyuan_3d_v2.1.safetensors` — 3D生成
- `ltx-2-19b-dev-fp8.safetensors` / `ltx-2-19b-distilled.safetensors`
- `miaomiao-harem.safetensors` — **SDXL Illustrious 动漫模型** (6.5GB, Civitai ⭐⭐⭐⭐⭐)。通过 `CheckpointLoaderSimple` 加载（自带 CLIP/VAE），**不需要额外 SDXL CLIP 模型**。已验证 1024×1024 完整生成 ✅。参数：30步, cfg=4, euler, scheduler=normal。路线评估参考 `ai-drama-pipeline-route-planning` skill
- `Anima/miaomiaoHarem_anima14.safetensors` — **Anima 动漫模型** (4GB, 2B 参数, flow matching 架构)。**不自带 CLIP/VAE**，需三个独立节点加载：CLIPLoader(`qwen_3_06b_base.safetensors`, type=stable_diffusion) + VAELoader(`ae.safetensors`) + CheckpointLoaderSimple(只加载扩散模型部分)。Qwen 0.6B 文本编码器**不支持中文 prompt**，中文会生成随机动漫少女而非预期内容。必须用英文 Danbooru 标签格式写 prompt（如 `1girl, cat ears, smoking`）。已给 AstrBot ComfyUI promax 插件 `handle_workflow` 加 `_translate_cn_prompt` 方法（通过 `self.context.get_using_provider().text_chat()` 调 DeepSeek 翻译），含 CJK 检测 + try/except fallback。参数：32步, cfg=4, euler_ancestral, scheduler=simple。
- `WAN/wan2.2-rapid-mega-aio-v1.safetensors` — **Wan2.2 Rapid All-in-One** (24.3GB, 放在 `checkpoints/WAN/` 子目录内，使用 `CheckpointLoaderSimple` 加载)。单文件合并了 WAN 2.2 + CLIP + VAE + 加速器，无需分开加载多个模型。

### Text Encoders
- `qwen_3_8b_fp8mixed.safetensors` — Flux2用的CLIP, type=`flux2`
- `qwen_3_4b.safetensors` — SD3/ZIT用的CLIP, type=`sd3`
- `umt5_xxl_fp8_e4m3fn_scaled.safetensors` — T5系列
- `gemma_3_12B_it_fp4_mixed.safetensors` — Gemma

### VAEs
- `flux2-vae.safetensors` — Flux VAE
- `ae.safetensors` — SD3/ZIT VAE
- `wan_2.1_vae.safetensors` — Wan2.2 I2V/FLF2V VAE (fp8)
- `Wan2_1_VAE_fp32.safetensors` — Wan2.1/SkyReels-V3 VAE (fp32, 精度更高)

## 工作流构建 (API 格式)

### Flux 2 Klein 文生图
关键节点: UNETLoader + CLIPLoader(type=flux2) + CLIPTextEncode + EmptyFlux2LatentImage + Flux2Scheduler + KSamplerSelect + CFGGuider + SamplerCustomAdvanced + RandomNoise + VAEDecode + VAELoader + SaveImage

已有预置工作流: `_hermes_flux_t2i.json`

### Qwen Image Edit (图像编辑)
关键节点: UNETLoader + LoraLoaderModelOnly + ModelSamplingAuraFlow + CFGNorm + CLIPLoader(type=qwen_image) + VAELoader(qwen_image_vae) + LoadImage + ImageScaleToTotalPixels + VAEEncode + TextEncodeQwenImageEditPlus + KSampler + VAEDecode + SaveImage

使用步骤:
1. 上传图片到 ComfyUI input/ 目录
2. 提交工作流 `_hermes_qwen_edit.json`，指定图片文件名和编辑指令
3. 获取编辑结果

提示词示例: "改为安全帽反光马甲背心", "angry expression, furrowed brows" (表情包编辑)

**经验总结（Qwen Image Edit 表情包批量生成）：**
- 一张小图(190×201) 通过改 prompt + seed 可以批量生成不同表情
- 6 张表情共耗时约 3 分钟（Qwen Lightning 4步+排队）
- 表情变化: 生气 ✅ 开心 ✅ 震惊 ✅ 哭 ✅ 得意 ✅ 委屈 ✅ 困 ✅
- 输出为 1024×? 放大图，每张 400-600KB
- 局限性: 主要是"微调"原图而非"重绘"，大幅表情变化效果有限；小图放大后细节不够

**关键细节:**
- `TextEncodeQwenImageEditPlus` 的输入字段名是 **`prompt`** (不是 `text`)！用错名会报 400
- `image2`/`image3` 等可选 IMAGE 输入，如果不使用必须**从 inputs 中删除**（不能设 null/None）
- 工作流需要先上传图片到 `/data/comfy/ComfyUI/input/`，用 `LoadImage` 节点加载
- 推荐使用 Lightning LoRA + 4步 + cfg=1 快速出图
- 调试 400 错误时用 `api/object_info/{class_type}` 检查节点输入字段名

### Z Image Turbo 文生图
关键节点: UNETLoader + CLIPLoader(type=sd3) + CLIPTextEncode + ConditioningZeroOut + EmptySD3LatentImage + KSampler(cfg=1) + VAEDecode + VAELoader + SaveImage

已有预置工作流: `_hermes_zit_t2i.json`

### MiaoMiao Harem (SDXL Illustrious) 文生图 — 动漫风格
已验证 ✅ 可工作。使用 CheckpointLoaderSimple（自动提取 MODEL + CLIP + VAE），无需单独加载 CLIP。

```python
WF = {
    "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "miaomiao-harem.safetensors"}},
    "2": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": ""}},        # 负prompt (空)
    "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": "prompt"}},   # 正prompt
    "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
    "5": {"class_type": "KSampler", "inputs": {
        "model": ["1", 0], "seed": 42, "steps": 30, "cfg": 4.0,
        "sampler_name": "euler", "scheduler": "normal",
        "positive": ["3", 0], "negative": ["2", 0],
        "latent_image": ["4", 0], "denoise": 1.0}},
    "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
    "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "miao"}},
}
```

**参数速查:**
| 参数 | 值 | 说明 |
|------|-----|------|
| Steps | 30 | Illustrious 模型推荐值 |
| CFG | 4.0 | 动漫风格推荐 3-5 |
| Sampler | euler | 稳定 |
| Scheduler | normal | SDXL 标准 |
| Resolution | 1024×1024 | SDXL 原生分辨率 |
| 耗时 | ~123s/张 | A10 实测 |

**Prompt 风格（SDXL/Illustrious 标签式，非 Flux 自然语言）:**
```text
masterpiece, best quality, anime style, [场景描述], [角色描述], [风格描述], highly detailed
```

### 提示词编写
- **Flux 2 Klein**: 自然语言描述, 不需要负面词。cfg=3-5
- **MiaoMiao Harem (SDXL)**: 标签式 prompt（`masterpiece, best quality, anime style`）
- **Z Image Turbo**: SD3架构, 4-6步出图, 快速迭代
- **Wan2.2 视频**: 需参考图+动作描述, lightx2v LoRAs 可4步出图。参考脚本: `/data/comfy/pipeline_flux2wan.py`

## ⚠️ Flux 2 Klein 已知限制 & 替代方案

### Flux2ProImageNode / Flux2MaxImageNode — 云端 API，不可靠

这两个节点调用 `api.comfy.org` 的云端 API，**不是本地推理**。当该服务不可达时会报：
```
The API server at https://api.comfy.org is currently unreachable
```
**不要依赖这两个节点**。需要本地生图时用 `UNETLoader` + `CLIPLoader(type=flux2)`。

### mmx 图像生成 — 更快更简单的替代方案

当 ComfyUI Flux 工作流出问题时，**`mmx image generate`** 是更快的替代方案：
```bash
mmx image generate "prompt text" --output output.png
```
输出是标准图片文件，无需经过工作流构建、队列等待、轮询的复杂流程。适合快速生成单张图片（如数字人肖像）。

### 1024×1024 系统性生成失败（历史记录，2026-05-11）
| 变体 | 生成方式 | 步骤 | 结果 |
|------|---------|------|------|
| Base FP8 | SamplerCustomAdvanced | 20步, cfg=5 | ❌ 底部 90-95% 灰色 |
| Base FP8 | KSampler | 20步, cfg=3.5 | ❌ 底部 90-95% 灰色 |
| Distilled GGUF Q4_K_S | UnetLoaderGGUF + KSampler | 4步, cfg=1 | ❌ 底部 90% 灰色 |
| Distilled GGUF Q4_K_S | 同上方但 640×640 | 4步, cfg=1 | ⚠️ 底部 45-50% 灰色（部分改善）|

**根因猜测：** 可能是 VAE 解码阶段显存不足导致 latent 只部分解码，或模型本身训练数据比例导致正方形分辨率下渲染不全。**非 prompt/工作流参数问题**（官方工作流和简化版都复现）。

**对策：** 如需完整 1024×1024 图片，使用 MiaoMiao Harem (SDXL) 替代。Flux 2 Klein 仅适用于可接受底部裁剪的场景。

## Flux → Wan I2V 端到端管线 (每镜耗时)

| 步骤 | 耗时 | 输出 | 说明 |
|------|------|------|------|
| Flux 2 Klein 关键帧 | ~70s | 1024×1024 PNG (~1.4MB) | cfg=3-5, 20步 |
| 图片上传到 ComfyUI | ~1s | — | POST /upload/image |
| Wan2.2 I2V 动画化 | ~170s | 720×720 MP4 (~340KB) | 41帧@16fps=2.6秒 |
| **单镜头总计** | **~4min** | **2.6秒视频** | 81帧≈5秒, 耗时~5min |

**视频参数与时长关系:**
| 帧数 | 16fps时长 | 预计耗时 |
|------|-----------|----------|
| 41 | 2.6秒 | ~3min |
| 81 | 5秒 | ~5min |

**Wan2.2 内存:** 24GB A10 可跑 720×720, fp8 模型 + 4步 LoRA。VRAM 余量约 172MB (torch_vram_free)，说明模型动态加载。A10 上 41 帧约 3 分钟。

## 工作流格式解析

服务器上的工作流 JSON 使用 **ComfyUI 0.4 subgraph 格式** (非 API 格式):
```json
{"definitions": {"subgraphs": [{"nodes": [...], "links": [...], ...}]}}
```

**Links 结构 (dict 格式):**
```json
{"id": N, "origin_id": src, "origin_slot": 0, "target_id": dst, "target_slot": 0, "type": "IMAGE"}
```
- `origin_id=-10` → 外部 widget 输入 (PrimitiveStringMultiline 等顶层节点)
- `target_id=-20` → 输出到顶层 (SaveImage 等)

**每个子图节点结构:**
```json
{"id": N, "type": "CLIPLoader", "inputs": [{"name": "clip_name", "type": "COMBO", "link": null, "widget": {"name": "clip_name"}}],
 "widgets_values": ["qwen_3_8b_fp8mixed.safetensors", "flux2", "default"]}
```
`widgets_values` 按序对应无 `link` 的 inputs 中的 widget 输入。

## 模型加载器映射

| 模型存放目录 | 对应的加载节点 |
|---|---|
| `checkpoints/` | `CheckpointLoaderSimple`, `easy fluxLoader`(仅扫描此目录) |
| `diffusion_models/` | `UNETLoader`, `DiffusionModelLoaderKJ` |
| `loras/` | 有多种 LoRA 加载节点 |
| `vae/` | `VAELoader` |
| `text_encoders/` / `clip/` | `CLIPLoader` / `DualCLIPLoader` |

Flux 2 Klein 模型在 `diffusion_models/` 下，**不能用 `easy fluxLoader`**（它只扫描 `checkpoints/`）。必须用 `UNETLoader` 加载模型，配合 `CLIPLoader(type="flux2")`。

## SSH 文件传输 (fish shell 坑)

远端 shell 是 fish，不支持 bash 风格的 heredoc。**huggingface.co 被墙，需用 hf-mirror.com 镜像下载大模型。**
```bash
# ❌ 这样不行 (fish 报错)
ssh host 'cat > file << "EOF" ... EOF'

# ✅ 方法1: 用 base64 管道绕过 (最通用，兼容 fish 有杂音的情况)
cat local_file.py | base64 -w0 | ssh host 'bash -c "base64 -d > /path/to/file && chmod +x /path/to/file"'

# ✅ 方法2: bash -c "cat > file" < local_file (需要 fish greeting 已禁用)
ssh -o StrictHostKeyChecking=no -p PORT user@host 'bash -c "cat > /remote/file"' < /local/file
```

### Fish 启动时打印大量 bass （fastfetch 系统信息）

`~/.config/fish/config.fish` 末尾有 `fastfetch -c examples/10.jsonc`，**每次 SSH 登录都会先输出系统信息 banner**。这会破坏 scp/sftp/sftp 协议握手（报 `Received message too long`）。

**修复：**
```bash
# 注释掉 fastfetch 行
ssh server "sed -i 's/^fastfetch/#fastfetch/' ~/.config/fish/config.fish"
```

**替代方案（不修改远端配置）：**
```bash
# 用 base64 中转（绕开 shell 输出干扰）
ssh -o StrictHostKeyChecking=no -p PORT user@host 'cat /remote/path/file.mp4 | base64 -w0' 2>/dev/null | base64 -d > /local/path/file.mp4
```
**关键：** `2>/dev/null` 丢弃 stderr 上的任何残留输出，`base64 -d` 从 stdin 解码。

## 漫剧自动生成系统 (Manhua Pipeline)

项目根目录: `/data/comfy/manhua/`

### 目录结构
```
manhua/
├── workflows/           # API 格式工作流 JSON
│   ├── flux_t2i.json    # Flux 2 Klein 文生图
│   ├── zit_t2i.json     # Z Image Turbo 文生图
│   ├── qwen_edit.json   # Qwen 图像编辑
│   ├── wan_i2v.json     # Wan2.2 图生视频 (双模型级联 I2V)
│   └── index_tts.json   # IndexTTS2 TTS
│                       # (GUI 格式工作流在 ComfyUI/user/default/workflows/ 下)
│                       #   video_wan2_2_14B_flf2v.json — 首尾帧 FLF2V
│                       #   SkyReels-V3双图参考.json — SkyReels V3 R2V
├── scripts/
│   ├── orchestrator.py  # 主编排器
│   ├── character_manager.py  # 角色管理
│   ├── storyboard_gen.py     # 分镜格式文档
│   └── cron_runner.py        # cron 定时执行
├── series/              # 生成结果
├── characters/          # 角色资产
├── pending/             # 待处理 storyboard
└── series_config.json   # 系列配置
```

### 工作流
1. 用户提供剧本文本
2. AI (LLM) 生成 storyboard JSON (使用分镜 prompt 模板)
3. 用户审核 storyboard
4. 编排器执行: 逐帧生成(Flux/Wan) → TTS(IndexTTS2) → 合成(ffmpeg)
5. 输出 sX-epY/final.mp4

### Wan2.2 I2V 工作流架构

**模型架构:**
- 双模型级联: high_noise(加噪4步) → low_noise(去噪4步)
- 各带 lightx2v 4步 LoRA (strength_model=1.0)
- WanImageToVideo 节点: 720×720, 81帧(≈5秒@16fps) 或 41帧(≈2.6秒)
- CLIP: umt5_xxl, type=wan
- VAE: wan_2.1_vae
- Sampler: euler, scheduler=simple, cfg=1.0
- ModelSamplingSD3: shift=5.0

**Subgraph 扁平化:**
原始工作流 (`03_video_wan2_2_14B_i2v_subgraphed.json`) 是 ComfyUI 0.4 subgraph 格式。节点 116 是子图包装器(`98e3bef8-...`)，内部包含 16 个节点(84-104)。API 格式需要展开成 16 个独立节点 + 额外 SaveVideo 节点。

**API 工作流节点清单（已扁平化的 `wan_i2v.json`）:**
```
┌─ 95  UNETLoader(high_noise)        ─┐
│  └→ 101 LoraLoaderModelOnly(high)    │
│      └→ 104 ModelSamplingSD3(shift)  │
│          └───┐                       │
├─ 96  UNETLoader(low_noise)         ─┤│
│  └→ 102 LoraLoaderModelOnly(low)     ││
│      └→ 103 ModelSamplingSD3(shift)  ││
│          └───┐                       ││
│               ├──┐                    ││
│  84 CLIPLoader ─→ 93 CLIPTextEncode(+p)    │
│                 └→ 89 CLIPTextEncode(-p)    │
│                        └──┐                 │
│  90 VAELoader ─────────────┤                 │
│  97 LoadImage ─────────────┤                 │
│                   ↓        │                 │
│  98 WanImageToVideo ───────┤                 │
│   ├→[0]positive ─→ 86 KSampler(high, ena)   │
│   ├→[1]negative ─→ 86                        │
│   └→[2]latent   ─→ 86                        │
│                  ↓ high latent                │
│                 85 KSampler(low, dis)          │
│                  ↓ low latent                  │
│                 87 VAEDecode                   │
│                  ↓ frames                      │
│                 94 CreateVideo(fps=16)          │
│                  ↓ VIDEO                        │
│                 [+id] SaveVideo(codec=h264)     │
```

**KSampler 步数设置（关键！参数错了视频只出首帧后灰屏）:**\n| 节点 | add_noise | start_at_step | end_at_step | return_with_leftover_noise | 用途 |\n|------|-----------|---------------|-------------|---------------------------|------|\n| 86 (high) | enable | 0 | 2 | enable | 高噪: 第1-2步(共4步), 加噪, 保留残噪供低噪精修 |\n| 85 (low)  | disable | 2 | 4 | disable | 低噪: 第3-4步(共4步), 不加噪, 从残噪精修到清晰 |\n注意: API JSON 中这些值是绝对整数（`end_at_step=2` 不是 `2/4`）。scheduler 必须用 `simple` 非 `normal`。cfg=1.0, sampler_name=euler。

**视频输出节点（2026-04-28 更新）：使用 VHS_VideoCombine**

`SaveVideo` 需要 `VIDEO` 类型输入，但工作流中只有 CreateVideo 输出 VIDEO。**改用 `VHS_VideoCombine`（VideoHelperSuite），它接受 IMAGE 类型，直接连接到 VAE Decode(87)。**

```python
# VHS_VideoCombine 节点配置（ID=105，已永久内置）
{
  "class_type": "VHS_VideoCombine",
  "inputs": {
    "images": ["87", 0],    # ← 直接连 VAE Decode！CreateVideo 已移除
    "frame_rate": 16,
    "loop_count": 0,
    "filename_prefix": "manhua-video",
    "format": "video/h264-mp4",
    "pix_fmt": "yuv420p",
    "crf": 19,
    "save_metadata": true,
    "pingpong": false,
    "save_output": true,
  }
}
```

**输出位置：`outputs["gifs"]`** — 每个条目含 `filename`、`subfolder`、`fullpath`、`format`、`frame_rate` 等字段。

**现在工作流结构：** `VAE Decode(87) → VHS_VideoCombine(105) → MP4`

**API 提交步骤:**
1. 上传首尾帧图片到 ComfyUI input 目录
2. 调用 `api/object_info/WanFirstLastFrameToVideo` 确认节点可用
3. 构建 API 格式工作流（见上），注意 KSampler 参数与 I2V 一致的坑
4. 提交到 `/prompt`
5. 从 `outputs["images"]` 提取视频文件

## Wan2.2 Rapid All-in-One（单文件合并模型）

### 概述

由社区创作者 **Phr00t** 开发的单文件合并模型，将 WAN 2.2 + CLIP + VAE + 加速器合并为一个 24.3GB 的 checkpoint。支持 T2V、I2V、首尾帧(FLF)全部模式。**比分开加载的双模型级联快 ~4 倍**。

### 下载

```bash
# ❌ huggingface.co 被墙，必须用国内镜像
cd /data/comfy/ComfyUI/models/checkpoints
mkdir -p WAN && cd WAN
wget -c -O wan2.2-rapid-mega-aio-v1.safetensors \
  'https://hf-mirror.com/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/Mega-v1/wan2.2-rapid-mega-aio-v1.safetensors'
```
下载后 ComfyUI 需要重启或等待自动扫描。验证：`CheckpointLoaderSimple` 的 `ckpt_name` 列表中会出现 `WAN/wan2.2-rapid-mega-aio-v1.safetensors`。

### 工作流文件

HF 仓库中有官方工作流 JSON：`Rapid-AIO-Mega.json`（加载后调整 prompt 和输入图片）

### 关键节点

| 节点 | 用途 |
|------|------|
| `CheckpointLoaderSimple` | 加载 checkpoint（路径 `WAN/wan2.2-rapid-mega-aio-v1.safetensors`）|
| `WanVaceToVideo` | 核心生成节点，输出 positive/negative conditioning + latent |
| `WanVideoVACEStartToEndFrame` | 首尾帧控制节点，生成首尾帧间的插值序列 |
| `ModelSamplingSD3` | 设置 shift（T2V=8.0） |
| `KSampler` | 4步采样，CFG=1，ipndm，sgm_uniform |

### 模式切换（通过 WanVaceToVideo.strength 控制）

| 模式 | strength | 需要的图像 | 说明 |
|------|----------|-----------|------|
| **T2V** | 0.0 | 无 | 纯文本生成，无需加载图片和 VACE 节点 |
| **I2V** | 1.0 | start_image | 参考图生成视频，需 VACE 节点控制 |
| **FLF** | 1.0 | start_image + end_image | 首尾帧插值，需 VACE 节点+两图 |
| **混合** | 0.0~1.0 | 可选 | 介于之间的控制强度 |

### API 工作流结构（T2V 模式，已验证通过）

```python
wf = {
    "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "WAN/wan2.2-rapid-mega-aio-v1.safetensors"}},
    # 注意：CheckpointLoaderSimple 输出索引: [0]=MODEL, [1]=CLIP, [2]=VAE
    "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
    "3": {"class_type": "CLIPTextEncode", "inputs": {"text": "", "clip": ["1", 1]}},  # CFG=1 时负prompt留空
    "4": {"class_type": "WanVaceToVideo", "inputs": {
        "positive": ["2", 0], "negative": ["3", 0],
        "vae": ["1", 2],
        "width": 512, "height": 512, "length": 81, "batch_size": 1,
        "strength": 0.0  # T2V模式
    }},
    "5": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["1", 0], "shift": 8.0}},
    "6": {"class_type": "KSampler", "inputs": {
        "model": ["5", 0], "positive": ["4", 0], "negative": ["4", 1],
        "latent_image": ["4", 2],
        "seed": 42001, "steps": 4, "cfg": 1.0,
        "sampler_name": "ipndm", "scheduler": "sgm_uniform", "denoise": 1.0
    }},
    "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
    "8": {"class_type": "VHS_VideoCombine", "inputs": {
        "images": ["7", 0], "frame_rate": 16, "loop_count": 0,
        "filename_prefix": "rapid_out", "format": "video/h264-mp4",
        "pingpong": False, "save_output": True
    }}
}
```

### API 工作流结构（I2V 模式）

相比 T2V 增加 LoadImage + VACE 节点，strength=1.0：

```python
# 先上传图片
start_name = upload_image_via_api("input.png")
int_node = "3"  # INTConstant(81)

wf = {
    # ... 同 T2V 的 CheckpointLoaderSimple + CLIPTextEncode ...
    "2": {"class_type": "LoadImage", "inputs": {"image": start_name, "upload": "image"}},
    "3": {"class_type": "INTConstant", "inputs": {"int": 81}},
    "4": {"class_type": "WanVideoVACEStartToEndFrame", "inputs": {
        "num_frames": [int_node, 0], "empty_frame_level": 0.5,
        "start_image": ["2", 0]
    }},
    # WanVaceToVideo: strength=1.0, control_video=["4", 0], control_masks=["4", 1]
    # ... 同 T2V 的 KSampler + VAEDecode + VHS_VideoCombine ...
}
```

### 参数速查

| 参数 | 值 | 说明 |
|------|-----|------|
| 分辨率 | 512×512 | 可用更高，但会显著增加显存和耗时 |
| 帧数 | 81（~5s @ 16fps） | 通过 INTConstant 节点设置 |
| 步数 | 4 | 这是加速后的最优值 |
| CFG | 1.0 | 留空负prompt |
| Sampler | ipndm | 配合 sgm_uniform scheduler |
| VACE strength | 0.5 | controls首尾帧的控制强度 |
| 模型 shift | 8.0 | 视频用的标准值 |

### 性能基准（A10 实测）

| 模式 | 分辨率 | 帧数 | 耗时 |
|------|--------|------|------|
| T2V, 4步 | 512×512 | 81 | **~5min** |
| I2V, 4步 | 512×512 | 81 | ~5-6min（含图片上传）|
| FLF, 4步 | 512×512 | 81 | ~6-7min（含两张图）|

对比 FLF2V Default 20步 640×640: **~20min**。Rapid AIO 快约 4 倍。

### 输出

使用 `VHS_VideoCombine`（而非 `SaveVideo`/`CreateVideo`），`outputs["gifs"]` 中获取 mp4 路径。
输出文件名示例: `rapid_out_00001_.mp4`

### 已知问题

- **不兼容 4 卡并行**：Wan2.2 14B 只使用单 GPU
- **512×512 分辨率限制**：A10 24GB 下 512×512 是稳妥选择，高于此可能有 OOM 风险
- **CFG=1 时负prompt无效**：这是 WAN 模型的特性，不要费时间写负prompt
- **视频质量不如 Default 20步**：4 步加速会有质量折损，但短剧场景一般够用

**工作流文件**: `video_wan2_2_14B_flf2v.json`（ComfyUI GUI 格式，含两个子管线）

### ⚠️ 关键设计原则

1. **首尾帧必须不同**：FLF2V 的核心价值是插值两张不同的图像。如果用同一张图做首尾帧，模型没有变化可生成，输出基本静止（同 loop 1 张图）。首帧和尾帧至少要有构图、角度、或场景元素的差异，FLF2V 才能产生有意义的运动。

2. **两帧差异要可过渡**：首尾帧差距不宜过大。Wan2.2 能处理风格转换（如油画→写实）和运镜变化（广角→近景），但不能凭空生成完全不存在的内容。设计时应确保两帧之间有视觉连续性。

3. **FLF2V 做镜头间过渡**：这是 FLF2V 的优势用法——用相邻镜头建立过渡：
   ```
   镜头N尾帧 ──FLF2V 1s──→ 镜头N+1首帧
   ```
   过渡手法包括：
   - **遮挡过渡**: 物体（手/路人/碎片）在镜头前经过，遮挡后露出新场景
   - **匹配剪辑**: 形状或构图匹配（瞳孔→数据流、乱码字符→树叶）
   - **视觉溶解**: 故障波纹扩散、燃烧灰烬重组、数据包裹画面
   - **快速缩放**: 推近到模糊再拉远出清晰

### FLF2V 分镜设计方法论

当用 FLF2V 构建完整的视频故事（而非单段特效）时，需要重新设计分镜结构，不能套用传统 T2I 分镜逻辑。

**核心结构**:
```
每镜 = [首帧图A] ──FLF2V 5s──→ [尾帧图B]      (主体内容)
            │
            ▼ 过渡 1s (FLF2V)
            │
每镜 = [首帧图C] ──FLF2V 5s──→ [尾帧图D]      (下一个镜头)
```

**设计流程**:
1. 先确定每镜的**首帧和尾帧各自的画面描述**（文字），而不是只写一个"镜头描述"
2. 首尾帧的设计需要体现出**可感知的变化**：视角移动、场景变化、表情演变、物体状态变化
3. 为每镜写 FLF2V prompt，描述从首帧到尾帧的**运镜+场景演变**
4. 为每对相邻镜头设计 **1秒过渡**——用一个单独的 FLF2V 跑，首帧=上一镜尾帧，尾帧=下一镜首帧
5. 过渡 FLF2V 的 prompt 专门描述过渡效果，不描述原始镜头内容

**生成顺序**:
1. 全部 48 张 Flux 图（24镜 × 2帧/镜）
2. 24 次 FLF2V 主体（首→尾，每镜 5 秒）
3. 23 次 FLF2V 过渡（尾→首，每镜 1 秒）
4. ffmpeg concat 拼接所有片段

**参数速查**:
| 类型 | 模式 | 帧数 | 时长 | 耗时估算 |
|------|------|------|------|----------|
| 主体(24镜) | Lightning 4步 | 81帧 | 5s | ~3min/镜 |
| 动效镜头(如建筑溶解) | Default 20步 | 81帧 | 5s | ~10min/镜 |
| 过渡(23次) | Lightning 4步 | 17帧 | 1s | ~1min/过渡 |
| 总耗时(24镜+23过渡) | - | - | ~2min23s | ~2-3h |

**过渡手法详解**:
- **遮挡过渡**: 主体从一侧进入画面，遮挡全部视野后离开，露出新场景。适合人物行走、车辆经过、数据流覆盖等场景
- **匹配剪辑**: 两帧有相似形状/构图的位置，FLF2V 自然做形状渐变。如圆形瞳孔→圆形数据流入口、矩形招牌→矩形树叶画面
- **场景自身变化**: 固定镜头，场景本身发生颠覆性变化（建筑融化、天空裂开、人消失）。适合展现"世界在变"的叙事
- **消散/汇聚**: 主体/画面碎成粒子散开→散去的粒子重新汇聚成新画面

**搭配 Flux 生成首尾帧的技巧**:
- 同一 prompt + 不同 noise_seed → 自然生成略微不同的构图（适合视角变化）
- 不同 prompt（广角 vs 近景）→ 大幅场景变化
- 首帧和尾帧的种子差异控制在 1~10 之间，确保画面风格一致

**核心节点**: `WanFirstLastFrameToVideo`（ComfyUI 0.3.48+ 内置，`comfy_extras.nodes_wan`）

**用途**: 给定首帧(start_image)和尾帧(end_image)，生成两帧之间的平滑过渡视频

**输入输出:**
```
Inputs:  positive(CONDITIONING), negative(CONDITIONING), vae(VAE),
         start_image(IMAGE, optional), end_image(IMAGE, optional),
         width(INT, 16-16384, step=16), height(INT, 16-16384, step=16),
         length(INT, 1-16384, step=4, default=81), batch_size(INT, 1-4096)
Outputs: positive(CONDITIONING, slot=0), negative(CONDITIONING, slot=1),
         latent(LATENT, slot=2)
```

**双管线架构**（工作流默认 Default 模式激活，Lightning 模式 bypassed）:

| 模式 | 激活方式 | steps | cfg | shift | sampler | scheduler | 高噪→低噪 | LoRA |
|------|---------|-------|-----|-------|---------|-----------|-----------|------|
| **Default (20步)** | 默认激活 ✅ | 20 | 4 | 8.0 | euler | simple | 0→10 / 10→10000 | 无 |
| **Lightning (4步)** | Ctrl+B 启用 | 4 | 1 | 5.0 | euler | simple | 0→2 / 2→10000 | lightx2v |

**API 格式关键节点清单（Default 模式，已验证 ✅ 输出 640×640, 81帧, 5s, H.264）:**

```python
wf = {
    "1": LoadImage(start_image),         # 如 "wan22_14B_flf2v_start_image.png"
    "2": LoadImage(end_image),           # 如 "wan22_14B_flf2v_end_image.png"
    "3": CLIPLoader("umt5_xxl_fp8_e4m3fn_scaled.safetensors", "wan", "default"),
    "4": CLIPTextEncode(clip="3", text=""),          # 正prompt
    "5": CLIPTextEncode(clip="3", text=neg_prompt),  # 负prompt
    "6": UNETLoader("wan2.2_i2v_high_noise_14B_fp8_scaled...", "default"),
    "7": ModelSamplingSD3(model="6", shift=8.0),
    "8": UNETLoader("wan2.2_i2v_low_noise_14B_fp8_scaled...", "default"),
    "9": ModelSamplingSD3(model="8", shift=8.0),
    "10": VAELoader("wan_2.1_vae.safetensors"),
    "11": WanFirstLastFrameToVideo(
        positive="4", negative="5", vae="10",
        start_image="1", end_image="2",
        width=640, height=640, length=81, batch_size=1),
    "12": KSamplerAdvanced(
        model="7", positive="11", negative="11", latent_image="11",
        add_noise="enable", steps=20, cfg=4,
        sampler_name="euler", scheduler="simple",
        start_at_step=0, end_at_step=10,
        return_with_leftover_noise="enable"),
    "13": KSamplerAdvanced(
        model="9", positive="11", negative="11", latent_image="12",
        add_noise="disable", steps=20, cfg=4,
        sampler_name="euler", scheduler="simple",
        start_at_step=10, end_at_step=10000,
        return_with_leftover_noise="disable"),
    "14": VAEDecode(samples="13", vae="10"),
    "15": CreateVideo(images="14", fps=16),
    "16": SaveVideo(video="15", filename_prefix="flf2v", format="mp4", codec="h264"),
}
```

**参数坑**（和 I2V 一致）:
- scheduler 必须用 `"simple"` 非 `"normal"`
- `start_at_step` / `end_at_step` 是绝对值（不是 `2/4` 这种分数）
- 高噪段 `return_with_leftover_noise="enable"`, 低噪段 `="disable"`
- cfg=1 时需配合 steps ≤4 (Lightning LoRA模式); cfg=4 适配长步数 (Default模式)

**Lightning 模式（4步）API 差异:**
- UNETLoader + LoraLoaderModelOnly(strength=1.0) 串联
- shift=5.0 (不是 8.0)
- KSampler: steps=4, cfg=1, 高噪 0→2, 低噪 2→10000
- 参考工作流: `video_wan2_2_14B_flf2v.json` 中 bypassed 组

**已知参考图:**
- `wan22_14B_flf2v_start_image.png` (2.1MB)
- `wan22_14B_flf2v_end_image.png` (1.7MB)
- `a1a42643e0d1f6f93b423952bac4be4b.jpg` (1.1MB, 旧默认首帧)
- `d2d66521a31cdbf7c4c1c2dd12680cda.jpg` (109KB, 旧默认尾帧)

## SkyReels-V3 双图参考 (Dual-Image Reference)

**工作流文件**: `SkyReels-V3双图参考.json`（ComfyUI GUI 格式）

**核心节点**: `WanPhantomSubjectToVideo`（`comfy_extras.nodes_wan`）

**模型**: `Wan21_SkyReelsV3-R2V_fp8_scaled_mixed.safetensors` (13.5GB)
**LoRA**: `wan2.1_i2v_lora_rank64_lightx2v_4step.safetensors` (705MB)
**VAE**: `Wan2_1_VAE_fp32.safetensors` (484MB)

**用途**: 参考图到视频（Reference to Video, R2V）。接受两张图像（ImageBatchMulti 合并），生成基于参考图的视频

**输入输出（WanPhantomSubjectToVideo）:**
```
Inputs:  positive(CONDITIONING, required), negative(CONDITIONING, required),
         vae(VAE, required),
         images(IMAGE, optional — 多帧参考图 batch),
         width(INT, 16-16384, step=16), height(INT, 16-16384, step=16),
         length(INT, 1-16384, step=4, default=81), batch_size(INT, 1-4096)
Outputs: positive(CONDITIONING, slot=0), negative_text(CONDITIONING, slot=1),
         negative_img_text(CONDITIONING, slot=2), latent(LATENT, slot=3)
```

**管线架构**:

```
Image 1 ──┐
          ├→ ImageBatchMulti(inputcount=2) → ImageScaleByAspectRatio V2(4:3, crop, lanczos) → images
Image 2 ──┘                                            
                                              WanPhantomSubjectToVideo
UNETLoader(SkyReelsV3) → PathchSageAttentionKJ(auto) → ModelPatchTorchSettings(enable_tf32)
  → LoraLoaderModelOnly(strength=1.0) → ModelSamplingSD3(shift=8)
  → [模型进入 WanPhantomSubjectToVideo]
                                              → KSampler(steps=8, cfg=1, euler, simple, denoise=1)
                                              → VAEDecode
                                              → easy cleanGpuUsed
                                              → VHS_VideoCombine(fps=24, h264-mp4, save_output=true)
```

**默认参数**: 832×480, 81帧, 8步, cfg=1, shift=8

**已验证** ✅: 历史记录显示已成功生成 `sky-v3_00001.mp4` ~ `sky-v3_00003.mp4` (通过 GUI 运行)

**⚠️ 注意**: 原始工作流中 `VHS_VideoCombine` 的 `save_output=false`（预览模式）。API 提交时需改为 `true`，否则视频存为 temp 会丢失。

**API 格式关键节点清单**:
```python
wf = {
    "1": LoadImage("z-image-turbo_00017_.png"),  # 参考图1
    "2": LoadImage("z-image-turbo_00018_.png"),  # 参考图2
    "3": ImageBatchMulti(image_1="1", image_2="2", inputcount=2),
    "4": LayerUtility: ImageScaleByAspectRatio V2(image="3", aspect="4:3", scale=1, ...),
    "5": CLIPLoader("umt5_xxl_fp8_e4m3fn_scaled.safetensors", "wan", "default"),
    "6": CLIPTextEncode(clip="5", text=positive_prompt),
    "7": CLIPTextEncode(clip="5", text=negative_prompt),
    "8": UNETLoader("Wan21_SkyReelsV3-R2V_fp8_scaled_mixed.safetensors", "default"),
    "9": PathchSageAttentionKJ(model="8", attention="auto", patch=False),
    "10": ModelPatchTorchSettings(model="9", enable_tf32=True),
    "11": LoraLoaderModelOnly(model="10", lora_name="wan2.1_i2v_lora_rank64_lightx2v_4step.safetensors", strength_model=1.0),
    "12": ModelSamplingSD3(model="11", shift=8.0),
    "13": VAELoader("Wan2_1_VAE_fp32.safetensors"),
    "14": WanPhantomSubjectToVideo(
        positive="6", negative="7", vae="13", images="4",
        width=832, height=480, length=81, batch_size=1),
    "15": KSampler(model="12", positive="14:0", negative="14:1", latent_image="14:3",
                   seed=..., steps=8, cfg=1, sampler_name="euler", scheduler="simple", denoise=1),
    "16": VAEDecode(samples="15", vae="13"),
    "17": easy cleanGpuUsed(anything="16"),
    "18": VHS_VideoCombine(images="17", frame_rate=24, format="video/h264-mp4",
                          filename_prefix="skyv3", save_output=True),
}
```

**注意**: WanPhantomSubjectToVideo 输出有 4 个 slot:
- slot 0: positive conditioning → KSampler.positive
- slot 1: negative_text conditioning → KSampler.negative
- slot 2: negative_img_text conditioning（可忽略）
- slot 3: latent → KSampler.latent_image

**已知参考图:**
- `z-image-turbo_00017_.png` (1.0MB)
- `z-image-turbo_00018_.png` (1.4MB)
4. 提交到 `/prompt`
5. 轮询 `/history/{prompt_id}` 直到完成
6. 从 `outputs["gifs"]` 提取视频路径，`fullpath` 字段可直接使用

### IndexTTS-2 语音克隆 & TTS (easy-use 版)

**模型位置**: `/data/comfy/ComfyUI/models/IndexTTS-2/` (3.5GB gpt.pth + 1.2GB s2mel.pth + campplus_cn_common.bin 声纹提取)

**节点清单**:
- `easy downloadIndexTTSAndLoadModel` — 加载模型
- `easy indexTTSGenerate` / `easy indexTTSGenerateSimple` — 生成 TTS
- `easy indexTTSEmotionVector` — 8维情感向量（Happy/Angry/Sad/Fear/Hate/Low/Surprise/Neutral）
- `easy indexTTSEmotionText` — 文本描述情感
- `easy indexTTSAudioMerge` — 合并多段音频
- `ReferenceTimbreAudio` — 声纹参考音频输入（5~15秒干净录音即可克隆）
- `IndexTTSEmotionOptionsNode` — 情感选项

**声音克隆 API 工作流（已验证 ✅）**:

```python
wf = {
    "1": {
        "class_type": "easy downloadIndexTTSAndLoadModel",
        "inputs": {"model": "IndexTTS-2", "download_from": "modelscope"}
    },
    "2": {
        "class_type": "LoadAudio",
        "inputs": {"audio": "reference.wav"}  # ⚠️ 必须 WAV！MP3 会报 Header missing
    },
    "3": {
        "class_type": "easy indexTTSGenerateSimple",
        "inputs": {
            "indextts_model": ["1", 0],
            "text": "目标文本...",
            "unload_model": False,
            "seed": 42,
            "reference_audio": ["2", 0]
        }
    },
    "4": {
        "class_type": "SaveAudioMP3",
        "inputs": {
            "audio": ["3", 0],
            "filename_prefix": "output_name",
            "quality": "320k"
        }
    }
}
# 提交: POST /prompt {"prompt": wf, "client_id": "..."}
# 轮询: GET /history/{prompt_id}
# 输出: /data/comfy/ComfyUI/output/output_name_00001_.mp3
```

**节点输入速查:**

| 节点 | required inputs | optional inputs |
|------|----------------|-----------------|
| `easy downloadIndexTTSAndLoadModel` | `model` (COMBO), `download_from` (COMBO) | `start` (*) |
| `easy indexTTSGenerateSimple` | `indextts_model`, `text`, `unload_model`, `seed` | `reference_audio`, `reference_audios`, `emotions` |
| `LoadAudio` | `audio` (COMBO, 从 input/ 目录选) | — |
| `SaveAudioMP3` | `audio`, `filename_prefix`, `quality` | — |

**坑点**:
- ⚠️ **参考音频必须 WAV**：MP3 格式在 ComfyUI 的 `LoadAudio` 节点会报 `Header missing` / `InvalidDataError`。用 `ffmpeg -i ref.mp3 -ar 16000 -ac 1 ref.wav` 转换
- ⚠️ **API 格式用 string-keyed nodes**：`{"1": {...}, "2": {...}}` 不是 `{"nodes": [...]}` GUI 格式
- ⚠️ **`SaveAudioMP3` 有 `quality` 参数**：可选 V0/128k/320k，是 required input（容易漏）
- ⚠️ **文本长度**：IndexTTS-2 朗读速度约 **104 wpm**（比人类 ~150 wpm 慢）。4000 字符 → ~4:30。如果有时长限制，先用 `len(text) / 104 * 60` 估算秒数再精简单词数

**性能参考（A10）**:
| 指标 | 值 |
|------|-----|
| 朗读速度 | ~104 wpm (265s / 460词) |
| 4000 字符生成耗时 | ~5 min |
| 输出质量 | 320k MP3, 5MB/4.5min |

**声音克隆工作流**:
1. 用户提供 5~15 秒参考录音（推荐中文，IndexTTS-2 用中文训练的声纹提取器）
2. `LoadAudio` 加载参考音频（**WAV 格式**） → 提取声纹
3. `easy indexTTSGenerateSimple` 输入目标文本 + 声纹 → 输出克隆语音
4. 支持跨语言：中文参考音频 → 英文 TTS 输出

**API 调用**: 通过 SSH 隧道 `localhost:18188` 直接调。用 `execute_code` + `terminal` 提交工作流。
**服务器端轮询**: 对长任务（>5min），用 `systemd-run --pipe --collect --wait` 在服务器后台执行轮询脚本，避免 SSH 超时。

**⚠️ execute_code 的 terminal() 不支持 `input` 参数**——不要写 `terminal("scp ...", input=payload)`，会报 `TypeError`。正确做法：先 `write_file` 写临时文件，再 `scp` 上传。

### ComfyUI_Sonic — 音频驱动数字人（Talking Head）

**模型位置**: `/data/comfy/ComfyUI/models/sonic/`（全部就绪 ✅）
- `unet.pth` — 主模型
- `yoloface_v5m.pt` — 人脸检测
- `audio2bucket.pth` + `audio2token.pth` — 音频特征提取
- `whisper-tiny/` — 语音转特征
- `RIFE/` — 帧插值（流畅度提升）

**核心节点**:
- `SONICTLoader` — 加载 Sonic 模型 + 人脸检测器
- `SONIC_PreData` — 预处理：输入图片 + 音频 → 驱动参数
- `SONICSampler` — 采样生成说话视频帧

**用途**: 给定一张肖像照 + 音频文件 → 生成说话数字人视频。适合口播、讲解类内容。

**⚠️ 前置依赖**: Sonic 需要 **SD/SDXL 系列 checkpoint** 作为基模型（通过 `SONICTLoader.model` 输入）。服务器上目前只有 3D 和视频模型（hunyuan3d, LTX, Wan），**没有 SD/SDXL 基模型**，因此 Sonic 无法直接使用。需要先下载 SD1.5 或 SDXL 模型（~7GB）。

**参考工作流**: `/data/comfy/ComfyUI/custom_nodes/ComfyUI_Sonic/examples/`

### 其他 TTS / 声音节点（服务器已具备）

| 节点组 | 关键节点 | 状态 |
|--------|---------|------|
| **ElevenLabs** | ElevenLabsTextToSpeech, ElevenLabsInstantVoiceClone, ElevenLabsSpeechToSpeech, ElevenLabsVoiceSelector | 节点已安装，需 API key |
| **ChatterBox** | ChatterBoxVoiceCapture, ChatterBoxAudioAnalyzer, ChatterBoxF5TTSEditOptions | zip 存在但**未解压安装** |
| **Qwen3 TTS** | Qwen3TTSVoiceDesignerNode | 节点已安装 |
| **通用 TTS** | SpeechSynthesis, SpeechRecognition, SenseVoiceNode | 节点已安装 |
| **MelBand RoFormer** | MelBandRoformer_fp32 模型已就绪 | 音频分离/增强 |

### 数字人 / Talking Head 能力总览

| 节点/方案 | 模型状态 | 用途 |
|-----------|---------|------|
| **ComfyUI_Sonic** | ✅ 模型全 | 音频驱动面部动画（最推荐） |
| **SadTalker** | ✅ 已安装+模型全 | 单图+音频→说话视频，3D 头部运动+口型。**已通过 ComfyUI API 验证 ✅** |
| **FantasyTalking** | ❌ 模型未下载 | 数字人说话 |
| **MultiTalk** | ❌ 模型未下载 | 多人数字人 |
| **WanInfiniteTalk** | ⚠️ patch 有 (`Wan2_1-InfiniTetalk-Single_fp16.safetensors`) | Wan 视频模型扩展 |
| **WanVideoImageToVideoMultiTalk** | ⚠️ 节点存在 | Wan 多说话人 I2V |
| **ChatterBox** | ❌ zip 未解压 | 声音克隆 + 表情编辑 |

通过 SSH 隧道 `localhost:18188` 直接调用 API。用 `execute_code` + `terminal` 提交工作流。
也可以在本地用 curl 直接调 `localhost:18188`。

### SadTalker — 单图+音频说话数字人

**ComfyUI 自定义节点**: `haomole/Comfyui-SadTalker`（GitHub）

**安装步骤**:
```bash
cd /data/comfy/ComfyUI/custom_nodes
git clone https://github.com/haomole/Comfyui-SadTalker.git

# ⚠️ 不要 touch nodes/__init__.py！空 __init__.py 会遮蔽父包的 NODE_CLASS_MAPPINGS
# nodes/ 目录应该作为 namespace package（无 __init__.py），让 ComfyUI 直接导入子模块
```

**Python 3.12 兼容性修复（必须！否则节点无法加载）**:

SadTalker 依赖 gfpgan → basicsr，而 basicsr 使用了 Python 3.12 中移除的 API：

```bash
# 1. 修复 basicsr 的 distutils 导入（Python 3.12 已移除 distutils）
sed -i 's/from distutils.version import LooseVersion/from packaging.version import Version as LooseVersion/' \
  /data/comfy/comfy-env/lib/python3.12/site-packages/basicsr/archs/arch_util.py

# 2. 修复 basicsr 的 torchvision API 变更
sed -i 's/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/' \
  /data/comfy/comfy-env/lib/python3.12/site-packages/basicsr/data/degradations.py

# 3. 安装 gfpgan（需走代理，huggingface 被墙）
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 \
  /data/comfy/comfy-env/bin/pip install gfpgan facexlib
```

**节点注册修复（关键！否则 ComfyUI 不加载 SadTalkerNode）**:

SadTalker 的 `__init__.py` 使用相对导入（`from .nodes.SadTalkerNode import ...`），但 ComfyUI 通过 `spec_from_file_location` 加载时 `__package__` 未正确设置，导致 `ImportError: attempted relative import with no known parent package`。

同时 `nodes/SadTalkerNode.py` 内部有 `from ..SadTalker.src.Pb import SadTalker` 也会失败。

**修复方案**：全部改为 `sys.path.insert` 绝对导入：

```python
# __init__.py（放在 Comfyui-SadTalker/ 根目录）
_base = os.path.dirname(__file__)
sys.path.insert(0, _base)
sys.path.insert(0, os.path.join(_base, "nodes"))
sys.path.append(os.path.join(_base, "SadTalker"))

from ShowText import ShowText
from ShowVideo import ShowVideo
# ...

# nodes/SadTalkerNode.py（修改第 12 行附近）
# 将: from ..SadTalker.src.Pb import SadTalker
# 改为:
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from SadTalker.src.Pb import SadTalker
```

**模型下载（~2.4GB, 8 个文件）**:

```bash
# SadTalker 主模型 → Comfyui-SadTalker/SadTalker/checkpoints/
# huggingface.co 被墙，用 hf-mirror.com 镜像
SD_CHECKPOINTS=/data/comfy/ComfyUI/custom_nodes/Comfyui-SadTalker/SadTalker/checkpoints

# 4 个 SadTalker 模型 (~1.7GB)
wget -O $SD_CHECKPOINTS/SadTalker_V0.0.2_256.safetensors \
  https://hf-mirror.com/vinthony/SadTalker-V002rc/resolve/main/SadTalker_V0.0.2_256.safetensors
wget -O $SD_CHECKPOINTS/SadTalker_V0.0.2_512.safetensors \
  https://hf-mirror.com/camenduru/SadTalker/resolve/main/new/checkpoints/SadTalker_V0.0.2_512.safetensors
wget -O $SD_CHECKPOINTS/mapping_00109-model.pth.tar \
  https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar
wget -O $SD_CHECKPOINTS/mapping_00229-model.pth.tar \
  https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/mapping_00229-model.pth.tar

# 4 个 GFPGAN 模型 → ComfyUI/gfpgan/weights/ (~700MB)
GFP_WEIGHTS=/data/comfy/ComfyUI/gfpgan/weights
wget -O $GFP_WEIGHTS/alignment_WFLW_4HG.pth \
  https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth
wget -O $GFP_WEIGHTS/detection_Resnet50_Final.pth \
  https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth
wget -O $GFP_WEIGHTS/GFPGANv1.4.pth \
  https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
wget -O $GFP_WEIGHTS/parsing_parsenet.pth \
  https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth
```

**节点**: `SadTalkerNode`（类别: "SadTalker"）

**输入**: `image`(IMAGE), `audio`(AUDIO), `poseStyle`(INT 0-46), `faceModelResolution`("256"/"512"), `preprocess`("crop"/"resize"/"full"/"extcrop"/"extfull"), `stillMode`(BOOL), `gfpganAsFaceEnhancer`(BOOL)

**输出**: `video_path`(STRING), `show_video_path`(STRING) — 视频文件路径

**工作流 (API 格式)**:

```python
wf = {
    "1": {"class_type": "LoadImage", "inputs": {"image": "portrait.jpg"}},
    "2": {"class_type": "LoadAudio", "inputs": {"audio": "narration.wav"}},
    "3": {
        "class_type": "SadTalkerNode",
        "inputs": {
            "image": ["1", 0],
            "audio": ["2", 0],
            "poseStyle": 0,
            "faceModelResolution": "256",  # 256 更快，512 更清晰
            "preprocess": "crop",
            "stillMode": True,
            "batchSizeInGeneration": 2,
            "gfpganAsFaceEnhancer": False,  # 设为 False（GFPGAN 不稳定）
            "useIdleMode": False,
            "idleModeTime": 5,
            "useRefVideo": False,
            "refInfo": "pose",  # ⚠️ 必填！pose/blink/pose+blink/all
            "useRefAudio": False,
        }
    },
    "4": {"class_type": "ShowVideo", "inputs": {"show_video_path": ["3", 1]}},
    # ⚠️ 必须加 ShowVideo 作为输出节点！SadTalkerNode 输出 STRING 不被 ComfyUI 识别为 output
}
```

**⚠️ 关键坑点**:
- `refInfo` 是 **required input**（容易漏），值：`pose / blink / pose+blink / all`，默认 `pose`。漏了会报 `prompt_outputs_failed_validation: required_input_missing: refInfo`
- `ShowVideo` 必须作为最终输出节点，否则提交报 `prompt_no_outputs`
- `gfpganAsFaceEnhancer` 设 False——GFPGAN 的 basicsr 依赖与 Python 3.12 不兼容
- **VRAM OOM**：SadTalker 峰值需要 ~21GB VRAM（256 分辨率, batch_size=1）。A10 23GB 勉强够用，但如果有其他进程占用 GPU（训练任务、其他 ComfyUI 模型），就会 `Allocation on device` OOM。**运行前用 `nvidia-smi` 检查目标 GPU 空闲 ≥21GB**。如果 VRAM 紧张：重启 ComfyUI 清空缓存、加 `--lowvram`、换 `CUDA_VISIBLE_DEVICES=N` 切换 GPU
- **batchSizeInGeneration 最小化**：OOM 时降到 1，不要用默认的 2
- **工作流提交模式**：长 JSON 用 `echo '...' > /tmp/st.json && scp && ssh 'curl -d @/tmp/st.json'` 避免 shell 转义地狱。**不要用 execute_code 的 terminal(input=...)——terminal() 不支持 input 参数**

**GPU VRAM 僵尸进程排查**：
```bash
# 查看 GPU 上所有进程（含已死但未释放 VRAM 的僵尸）
nvidia-smi --query-compute-apps=pid,name,used_memory,gpu_bus_id --format=csv

# [Not Found] = 进程已死但 VRAM 未释放
# fuser -v /dev/nvidia0 查看哪些 PID 持有 GPU 文件句柄

# 如果 GPU 重置被拒：先停掉所有使用该 GPU 的进程，再 sudo nvidia-smi --gpu-reset -i N
# 注意：僵尸 VRAM 通常无法通过 nvidia-smi --gpu-reset 清理（需要完全释放 CUDA context）
# 最可靠方案：换一张干净的 GPU（CUDA_VISIBLE_DEVICES=N）

**⚠️ 安装后需重启 ComfyUI** 才能加载节点。重启方式见下。

### ComfyUI 进程管理 (systemd-run 模式)

**⚠️ SSH 后台进程绝对不可靠**——`terminal(background=true)` 起 `ssh ... &` 会在 SSH 断开时杀死所有子进程。**唯一可靠的方式是 `systemd-run --user`**，它创建独立的 systemd 单元，不受 SSH 会话生命周期影响。

```bash
# 启动 ComfyUI（长期运行服务，用 -d detach）
ssh server 'systemd-run --user --unit=comfyui -d --working-directory=/data/comfy/ComfyUI \
  /data/comfy/comfy-env/bin/python3 main.py --listen 0.0.0.0 --port 8188'

# 切换 GPU（VRAM 紧张时换卡）
ssh server 'systemctl --user stop comfyui; CUDA_VISIBLE_DEVICES=1 systemd-run --user --unit=comfyui \
  --setenv=CUDA_VISIBLE_DEVICES=1 -d --working-directory=/data/comfy/ComfyUI \
  /data/comfy/comfy-env/bin/python3 main.py --listen 0.0.0.0 --port 8188 --lowvram'

# 重启（如安装新 custom node 后）
ssh server 'systemctl --user restart comfyui'

# 查看状态 / 日志
ssh server 'systemctl --user status comfyui'
ssh server 'journalctl --user -u comfyui -n 50 --no-pager'

# 运行一次性任务（如模型下载、轮询脚本）—— --pipe --collect --wait 会等任务结束
ssh server 'systemd-run --user --unit=my-task --pipe --collect --wait \
  /data/comfy/comfy-env/bin/python3 /tmp/my_script.py'

# 清理失效的 unit（同名 unit 再次启动会报 \"already loaded\"）
ssh server 'systemctl --user reset-failed'
```

**坑点**: 
- `--pipe --collect --wait` 适合有明确终点的任务（模型下载、脚本执行）。长运行服务用 `-d`（detach）
- 同名 unit 第二次启动会报 `already loaded`，需先 `systemctl --user stop` + `reset-failed`，或用不同名字（`comfyui-v2`, `comfyui-v3`...）
- 重启后等 30-40 秒让 ComfyUI 完全加载（模型扫描 + custom nodes 注册）
- **不要用 `pkill` 杀 ComfyUI**——pkill 会连带杀死 SSH 会话自身

**验证节点已加载**: `curl -s http://127.0.0.1:8188/api/object_info | python3 -c "import json,sys; d=json.load(sys.stdin); print('NodeName' in d)"`

## 首轮测试结果 (腐烂现实 / Rotten Reality)

### 2026-04-27 第 1 轮 — 24 镜头，SSH 超时，3 视频跳过

**全流程测试** — 24 镜头分镜表，写实电影风格，自动生成到 final.mp4

| 指标 | 实际值 | 说明 |
|---|---|---|
| 分镜数 | 24 镜头 | 6幕，含3个Wan I2V视频镜头（被跳过） |
| 成功生成 | 21/24 帧 | 3个视频镜头因无SaveVideo节点被跳过 |
| 最终视频时长 | 51 秒 | 计划1m54s（缺3个视频段） |
| 视频格式 | 1024×1024, H.264, 2.3MB | 无音频/字幕 |
| 总耗时 | ~25 分钟 | 含队列等待（服务器有其他用户任务） |
| 单帧 Flux 耗时 | ~30-60 秒 | 主要取决于队列排位 |
| 编排器寿命 | ~23 min 后被杀死 | SSH 600s 上限触发 |
| 视频合成 | 手动完成 | 编排器在合成阶段被杀 |

### 2026-04-28 第 3 轮 — 已修复 Wan I2V SaveVideo + get_output_files

重启全覆盖生成（tmux 后台运行），验证 fix 有效性。

| 指标 | 实际值 | 说明 |
|---|---|---|
| 24 镜头 | 运行中 | tmux send-keys 启动，非 SSH foreground |
| 修复点 | SaveVideo(105)永久加入工作流 + get_output_files 四key检查 | 编排器 `generate_wan_video` 补 `filename_prefix` patch |
| venv | 不需要 | 编排器只依赖 Python stdlib，fish 下 activate 失败不影响 |

### 最终产物
```
series/rotten-reality/s1-ep1/
├── frames/          # 21 张 Flux 生成的分镜图
├── seg_0000.mp4 ~ seg_0010.mp4  # 11 个视频片段
├── final.mp4        # 最终合成视频 (2.3MB)
├── concat.txt       # ffmpeg concat 清单
├── progress.json    # 执行进度
└── subtitles.srt    # 空文件（字幕未生成）
```

### 已知问题 & 修复方向

| 问题 | 原因 | 优先级 | 修复 |
|---|---|---|---|
| Wan I2V 视频镜头跳过（旧） | WanImageToVideo 的 LoadImage 路径不对（图没 cp 到 ComfyUI/input/） | 已修复✅ | `generate_wan_video()` 中已 `shutil.copy2(img, ComfyUI/input/)` |
| Wan I2V 视频返回 None（旧） | 工作流缺少 SaveVideo 节点 + `get_output_files` 只查 `images` 不查 `videos/files/gifs` | 已修复✅ | `_manhua_wan_i2v.json` 已永久添加 SaveVideo 节点(105)；`get_output_files()` 已改为检查四个 key |
| 字幕文件为空 | 编排器到字幕阶段时已被杀，没走到 TTS + SRT 生成 | **高** | 编排器增加 checkpoint 断点续跑 |
| 无音频轨 | IndexTTS2 节点没被调用 | **中** | 同上，TTS 在合成阶段之前 |
| 编排器中途被杀死 | SSH foreground timeout=600s 上限，~23min 后触发 | **方案 A（推荐）:** tmux 后台运行。**方案 B:** `terminal(background=true)` 起 SSH nohup |
| 编排器合成阶段中断 | 流程做到 ffmpeg concat 前被杀 | **中** | 分段 checkpoint: 每生成 5 帧写一次 progress.json |
| 缺少断点续跑 | orchestrator 没有 resume 逻辑 | **低** | progress.json 检查已生成帧，跳过已有帧继续后续 |

## 编排管道模式 (Multi-shot Pipeline)

### 架构分层
```
User Input → [Storyboard JSON] → Orchestrator → [Shot Loop] → ffmpeg Compose → MP4
                                         │
                                    ComfyUI API (Flux/Wan/TTS)
```

### 逐镜循环
```python
for shot in storyboard["shots"]:
    if shot["action_level"] == "action":
        # Wan2.2 I2V: 先出 Flux 参考图, 再喂 WanImageToVideo
    else:
        # Flux T2I: 直接提交
    submit → wait_for_completion() → copy output → save progress.json
```

### ⚡ 异步提交模式（推荐：避开 SSH timeout，不等人）

对于长耗时任务（FLF2V 20min, I2V, T2I 等），不要阻塞等待。使用 **submit → verify → cron poll → notify** 模式：

```
Step 1: 通过 SSH API 提交任务，拿到 prompt_id    (3s)
Step 2: 确认队列中有任务在跑                        (2s)
Step 3: 写 job 标记文件（记录 prompt_id + prefix）   (即时)
Step 4: 设 cron 每 5min 轮询一次                     (设置完就走)
Step 5: cron 查到完成 → 自动回复/通知                 (异步)
```

**关键脚本：`/tmp/flf2v_runner.py`**（参考 skill 同目录下的 `scripts/flf2v_runner.py`）

```bash
# 提交（快速返回）
/data/comfy/comfy-env/bin/python3 /tmp/flf2v_runner.py submit <prefix> <start_img> <end_img> "<prompt_text>"

# 轮询（检查是否有完成任务）
/data/comfy/comfy-env/bin/python3 /tmp/flf2v_runner.py poll
```

**poll 检测逻辑：** 不依赖 API history outputs（可能为空），直接扫描 output/ 和 output/video/ 目录查找文件名匹配 prefix 的 mp4 文件。找到即认为完成。

**配合 cron 使用（推荐）：**
```yaml
# cronjob 定义
- action: create
  name: "flf2v-poll"
  schedule: "every 5m"
  prompt: "Run /data/comfy/comfy-env/bin/python3 /tmp/flf2v_runner.py poll and report any DONE results"
  repeat: 10  # 最多跑 10 次 ≈ 50 分钟，足够覆盖 20min 任务
```

**坑点：**
- ComfyUI `SaveVideo` 的输出可能不在 `outputs["videos"]` 中，即使文件名以 prefix 开头。必须**直接扫磁盘**。
- 提交后立即检查 queue 可能为 0（ComfyUI 短暂延迟），等 3 秒再查。
- 任务完成但 queue_running=0 且 queue_pending=0 时，就是 done 了（无论 outputs 是否为空）。
- Cron job 的 prompt 必须自包含，不能依赖当前会话上下文。

### 后台运行 (避开 SSH 超时)

**方法 A — tmux send-keys（推荐 ✅ 已验证可跑完全程）**

远端 shell 是 fish，`source venv/bin/activate` 在 fish 下会报错（bash 语法不兼容）。但编排器只依赖 Python stdlib，**不需要 venv**。

```bash
ssh server 'bash -c "
cd /data/comfy/manhua
tmux new-session -d -s manhua -x 200 -y 50
tmux send-keys -t manhua \"cd /data/comfy/manhua\" Enter
tmux send-keys -t manhua \"python3 scripts/orchestrator.py storyboard.json --series s --season 1 --episode 1\" Enter
echo Started in tmux session manhua
"'

# 查看进度
ssh server 'bash -c "tmux capture-pane -t manhua -p -S -30"'

# 连接到会话（交互式）
ssh -t server 'tmux attach -t manhua'
```

**方法 B — SSH background=true**
```bash
# 在服务器上保存 runner3.sh:
cat > /tmp/runner3.sh << 'SCRIPT'
#!/bin/bash
cd /data/comfy/manhua
exec /data/comfy/comfy-env/bin/python3 scripts/orchestrator.py \"$@\"
SCRIPT

# 通过 background=true 运行:
ssh server /tmp/runner3.sh storyboard.json --series s --season 1 --episode 1
```

### 常见失败模式

| 症状 | 原因 | 修复 |
|---|---|---|
| 队列空但编排器在跑 | 工作流 JSON 不存在 | 检查 `_manhua_*` 文件 |
| 400 Bad Request | 节点输入字段名错了 | `api/object_info/{节点类型}` 对参数 |
| Wan I2V 跳过 | LoadImage 路径不对 | 图片先 cp 到 ComfyUI/input/ 用相对路径 |
| SSH 600s 超时 | 默认 foreground 上限 | 用 runner3.sh 脱离会话 |
| ffmpeg 字幕失败 | SRT 是相对路径 | 用绝对路径 `subtitles=/abs/path.srt` |
| scp/sftp 报 `Received message too long` | fish shell fastfetch greeting 破坏协议 | 注释掉 config.fish 中 `fastfetch` 行或用 base64 管道下载 |
| ffprobe 报空 JSON | 二进制文件被 fish banner 污染 | 文件头不是 MP4 → 重新用 base64 方式传输 |
| 编排器合成阶段中断 | SSH timeout 杀死进程 | 添加 checkpoint 断点续跑；不要依赖编排器完成合成，手动补全 |
| 合成阶段崩溃 `TypeError: expected str, not NoneType` | 视频镜头生成失败后 `shot["image"]=None`，传给 ffmpeg `-i None` 直接抛异常退出 | 用 `elif shot.get("image")` 判空 + else 分支生成纯色占位片段 `ffmpeg -f lavfi -i color=c=black:s=1024x1024:d={dur}` |
| Wan I2V 视频生成返回 None（但 API 成功）— 已修复 ✅ | 两大原因：(1) 工作流无 SaveVideo 节点；(2) 即使有，`get_output_files()` 只查 `images` 不查 `videos/gifs/files` | 修复：
(1) 工作流 `_manhua_wan_i2v.json` 已永久添加 SaveVideo 节点(105)
(2) `get_output_files()` 已验证修复：检查四个 key（`images`, `videos`, `files`, `gifs`）|
| Wan I2V 400 `codec: 'h264_nvenc' not in ['auto', 'h264']` | SaveVideo 节点参数允许值有限 | 用 `codec: 'h264'` 和 `format: 'mp4'` |
| 输出目录不包含 image_edit.png 等 | Qwen编辑工作流输出文件名被固定 | 修改工作流 JSON 中的 filename_prefix 为唯一值 |
| Wan I2V 400 `codec: 'h264_nvenc' not in ['auto', 'h264']` | SaveVideo 节点参数允许值有限 | 用 `codec: 'h264'` 和 `format: 'mp4'` |\n| Wan I2V 400 `format: 'video/h264-mp4' not in ['auto', 'mp4']` | 同上 | 用 `format: 'mp4'` |\n| Wan I2V 只出首帧后灰屏 | KSampler scheduler/steps/leftover_noise 参数错误 | 修复三处：(1) scheduler=`simple` 非 `normal` (2) 高噪0→2, 低噪2→4 (3) 高噪 `return_with_leftover_noise=enable` |

### 视频合成
```bash
# 静态图 → 视频段
ffmpeg -y -loop 1 -i image.png -c:v libx264 -t 5 seg_0000.mp4
# 拼接
ffmpeg -y -f concat -safe 0 -i concat.txt -c:v libx264 temp.mp4
# 烧录字幕 (需绝对路径)
ffmpeg -y -i temp.mp4 -vf "subtitles=/abs/path/subtitles.srt" final.mp4
```
