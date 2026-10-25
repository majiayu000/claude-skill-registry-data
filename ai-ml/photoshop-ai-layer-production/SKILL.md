---
name: photoshop-ai-layer-production
description: 将平面位图或 AI 拆分素材组装为可编辑 PSD/PSB，并在 Windows 上安全附着用户已打开的 Photoshop 完成图层、蒙版、文字、保存重开与视觉验收。用于 AI 拆图、语义切片、遮挡背景补全、文字重建和生产级分层交付；不用于普通裁剪、单层修图或未经授权的上传、覆盖与关闭。
---

# Photoshop AI 分层生产

交付可继续编辑、可追溯来源、默认视图正确的 PSD/PSB，而不是一叠外观近似的整图。本 Skill 自带可执行入口、固定的 ComfyUI 工作流、模型下载清单、环境自检、原尺寸图层恢复、Photoshop 组装、OCR/字体工具和验收脚本；模型权重因体积约 30GB 不随包分发，由 `scripts/bootstrap.ps1` 从清单中的官方地址下载并校验。

## 选择工作范围

- 只做素材拆分时，离线生成图层资产和清单，不启动 Photoshop。
- 只做现成资产组装时，先验证资产，再附着用户已打开的 Photoshop。
- 完整生产时，按“源图冻结 → 单图试点 → 分层资产 → Photoshop 组装 → 可编辑文字 → 另存 → 重开 → 视觉验收”推进。
- 普通裁剪、格式转换或单层调整不使用本 Skill；选择更轻量的文件处理方式。

## 生产入口

1. 首次搬运或环境未知时，完整阅读 [搬运与复现说明](PORTABLE_README.md)，运行 `scripts/bootstrap.ps1 -RuntimeRoot <目录> -DownloadModels`。下载可续传，结束后会按 `config/models.json` 校验文件名、字节数和 SHA-256。
2. 运行 `scripts/check_environment.py --comfy-root <ComfyUI目录>`。只有 Python、ComfyUI 固定版本、核心节点和三份模型都通过，才进入推断。
3. 冻结源文件完整路径、哈希、尺寸、DPI、色彩模式、输出路径及不覆盖边界。运行 `scripts/inventory_sources.py`，为每个任务复制 `examples/job.example.json`。
4. 把源图放入本机 ComfyUI，运行 `scripts/run_qwen_layered.py`。默认 FP8、1024 长边、8 层、20 步、CFG 2.5；高质量复核可用 50 步、CFG 4.0。源图始终只发往 `127.0.0.1`。
5. 运行 `scripts/make_contact_sheet.py` 并查看完整图、逐层 RGBA 与重新合成图。Qwen 不提供语义名称和 z-index；接收方 AI 必须按画面证据填写 `layer-map.json`，不可凭固定层号套用另一张图。
6. 运行 `scripts/restore_original_size_layers.py`，把 AI RGBA 放大回原画布；需要保留原像素色彩的前景层使用 `original_rgb_masked`，AI 补全背景使用 `ai_rgba` 并明确标注为推断内容。
7. 资产完成后运行 `scripts/validate_production_manifest.py`。需要写入 Photoshop 时先读 [实时控制与保存边界](references/live-control.md)，再运行 `scripts/assemble_photoshop_document.ps1 -JobJson <任务清单>`。只附着可见、响应正常、由用户打开的 Photoshop，且只另存新 PSD/PSB。
8. 需要真实文字层时，按 [可编辑文字重建](references/text-reconstruction.md) 使用 `scripts/text/` 中的 Windows OCR、字体清单、字体拟合和文字层写入链；OCR 与字体拟合置信度分别保留。
9. 完成后运行 `scripts/verify_delivery.py`，并以 Photoshop 保存—关闭—重开后的图层结构、尺寸、默认可见性和人工视觉检查为最终验收。

## 目录即合同

- `config/`：固定运行版本、模型官方地址、体积和哈希。
- `workflows/`：可审计的 Qwen-Image-Layered API 工作流说明；实际请求由脚本按参数生成。
- `scripts/`：从安装、自检、推断、复合检查、原尺寸恢复到 Photoshop 组装和交付验证的可执行链。
- `scripts/text/`：可选的本地 OCR、系统字体匹配和 Photoshop 真文字层链。
- `examples/`：任务、层映射和文字清单模板；复制后只改路径与任务特定语义。
- `licenses/`：本 Skill 和其固定第三方来源的许可说明。

## 不可跨越的边界

- 当前指令和当前活动文档是实时权威。历史授权不能替代本次上传、保存、覆盖、关闭或重启授权。
- 默认不上传源图，不覆盖原文件，不合并或扁平化原图层，不强制关闭 Photoshop。
- 下载脚本只访问 `config/models.json` 和 `config/runtime-lock.json` 中列出的官方来源；不得悄悄改用网盘、镜像或未知权重。
- AI 只生成推断像素或分割建议；它不能证明原字体、测绘内容或被遮挡背景的真实性。
- 连接成功、读取成功、写入成功、保存成功、重开成功和视觉通过分别报告，不能互相替代。
- 超时后只做一次有界只读核对；先确认文档、图层和输出状态，再决定是否重试，禁止盲目重复写入。

## 完成标准

- 源文件哈希未变化，尺寸、DPI 和色彩模式符合合同。
- 默认视图与源图在约定尺度下相符；关闭上层元素后，背景连续且无明显残边或孔洞。
- 必要元素能独立开关；AI 补全图层明确标注为推断内容。
- 文字保存重开后仍是 Photoshop 文字层，低置信度项可快速定位。
- PSD/PSB 在授权的新路径存在，关闭重开后图层结构、类型、可见性和保存状态通过；视觉验收另行成立。
- 搬运验收必须在一个新目录解压后运行：Skill 快速校验通过，示例任务清单通过，下载清单可解析，所有入口脚本的 `--help` 或参数绑定成功；没有真实模型和 Photoshop 时只能报告“包结构通过”，不能报告“完整生产通过”。
