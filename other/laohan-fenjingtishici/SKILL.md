---
name: laohan-fenjingtishici
version: 1.0
description: 生成专业分镜图片提示词，适配扩散模型（FLUX/SDXL/Gemini）。校验质量后拆分为独立文件，或直接生成带产品描述的 Gemini 提示词模板。Use when 用户说"生成分镜提示词""校验分镜""拆分镜""分镜""分镜图"或提到视频分镜/镜头提示词/产品分镜模板。
---

# 分镜提示词生成与校验

为产品带货/短视频生成分镜图片提示词，并校验输出质量。

## 不适用场景

- 生成视频本身 → 这是分镜图片提示词，不是视频生成
- 生成封面图 → 用 laohan-fengmianqiuzhi
- 生成口播稿 → 用 laohan-chuangzuo
- 没有产品描述 → 模式1必须提供产品视觉描述才能生成

## 使用

```
# 模式1：生成 Gemini 提示词模板
/laohan-fenjingtishici <视频秒数> <产品视觉描述>

# 模式2：校验并拆分 Gemini 返回的分镜
/laohan-fenjingtishici <用户粘贴的 Gemini 输出>
```

## 模式1：生成提示词模板

输入视频秒数和产品描述，输出可直接粘贴到 Gemini 的提示词（内嵌所有规则）。

提示词模板内容见 `references/prompt_template.md`。

模板中需要替换的变量：
- `{VIDEO_LENGTH}` → 实际视频秒数
- `{FRAME_COUNT}` → 向上取整(视频秒数 ÷ 5)
- `{PRODUCT_DESCRIPTION}` → 产品的视觉特征（颜色、材质、形状）

## 模式2：校验并拆分

用户把 Gemini 返回的分镜结果粘贴过来，按检查清单逐项验证，通过后拆分为独立文件。

### 检查清单

校验以下 8 项，每项通过/失败+具体问题：

| # | 检查项 | 通过标准 |
|---|--------|---------|
| 1 | 帧数正确 | 帧数 = 向上取整(视频秒数 ÷ 5) |
| 2 | 产品占位符一致 | 所有帧中产品位置都使用 [PRODUCT] 占位符（除非物理状态变化） |
| 3 | 动势预设 | 每帧都有 mid-action / 动态姿势描述 |
| 4 | 正负分离 | Positive Prompt 和 Negative Prompt 已分离 |
| 5 | 无填充词 | 没有 "Generate an image..."、"HIGH RESOLUTION" 等对话式指令 |
| 6 | 无 meta-tags | 没有 "(Product reference: ...)" 标签，产品用 [PRODUCT] 占位 |
| 7 | 摄影术语 | 包含景别、角度、f值、焦距、光源方向、色温K值、照明技法 |
| 8 | 场景一致性 | 所有帧的 [SCENE] 描述完全相同（背景/环境/氛围不可跳变），只允许机位和光位变化 |

### 校验失败处理

- 项 1（帧数错误）：自动修正帧数，提示用户重新生成
- 项 2（占位符不一致）：标出差异帧，建议统一替换为 [PRODUCT]
- 项 3-8：标出具体问题帧和修改建议，不自动修改（保持 Gemini 原始输出）

### 拆分规则

校验通过后，每帧拆为一个文件：

```
{输出目录}/frame_1_prompt.txt
{输出目录}/frame_2_prompt.txt
...
{输出目录}/frame_N_prompt.txt
```

输出目录默认为当前项目目录，可由用户指定。

### 文件格式

每个文件包含帧标题 + Positive Prompt + Negative Prompt，和 Gemini 输出格式一致：

```
Frame N [timestamp - storytelling purpose]:

Positive Prompt:
[完整提示词]

Negative Prompt:
[negative 内容]
```

## 提示词工程规则

这些规则同时嵌入模板和用于校验：

1. **5秒分段**：每帧对应一个 5 秒视频片段（Wan 2.2 的 81 帧 ÷ 16fps）
2. **余数向上取整**：32 秒视频 → 7 帧（35 秒），最后一帧按完整 5 秒节奏描述，后期裁剪
3. **单一节拍**：每帧只描述一个动作/时刻
4. **纯视觉描述**：适配扩散模型，不含对话式指令，分辨率由工具控制
5. **[PRODUCT] 占位符**：产品外观用 [PRODUCT] 占位，生图时由上传的产品参考图决定外观，不写具体产品描述
6. **动作适配（CRITICAL）**：彻底根除参考视频中绑定原产品的专属交互（套硅胶壳、穿挂绳、塞入耳塞），替换为通用高级商业交互（"adjusting outer textures"、"arranging items gracefully"、"presenting side-by-side"）
7. **环境强制隔离**：剥离参考视频的特定背景/风格，强制用 "real commercial photography style"
8. **场景一致性锁定**：所有帧的 [SCENE] 必须完全相同（同一背景/环境/氛围），只允许机位和光位变化
9. **动势预设**：每帧描述 mid-action 姿态，为 I2V 提供运动张力
10. **正面/负面分离**：可直接复制到 ComfyUI 的两个 CLIPTextEncode 节点
11. **负面提示词语义**：`floating objects` 压制的是无因漂浮噪声，不与 positive 中的手部受因悬停矛盾
12. **负面基线**：每帧 Negative Prompt 默认包含 "CG, glowing effects, over-saturation"

## 前置依赖

- 无特殊依赖，纯文本处理
