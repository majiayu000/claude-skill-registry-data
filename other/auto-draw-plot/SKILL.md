---
name: auto-draw-plot
description: 根据用户描述生成高质量绘图 prompt，并按通用、roadmap、schematic 模式通过 BenszAPI 直接完成 gpt-image-2.5-flare、gpt-image-2.5-sunburst、gpt-image-2 或 Nano Banana/Gemini 出图、编辑和多轮迭代；这是自包含的图片生成工作流，选中后不得调用或依赖 imagegen，除非用户明确要求同时使用 imagegen。
metadata:
  author: Bensz Conan
  short-description: 模式化需求理解 + multi-round image-to-image optimization + GPT 图片模型低成本 JPEG
  keywords:
    - auto-draw-plot
    - nano-banana
    - gemini
    - parallel-vibe
    - visual evaluation
    - 图像生成
---

# Auto Draw Plot

## 目标

- 以用户需求为起点，由宿主 AI 进行语义规划，再构造适用于当前图片 provider 的 prompt，通过 BenszAPI 直接完成“parallel-vibe 规划留痕 → prompt → 出图 → 视觉评估 → 继续/停止”的闭环；脚本默认不调用额外 Gemini 文本接口。
- 触发边界：默认模式是 `general`；用户明确要技术路线图/roadmap/flowchart 时使用 `roadmap`，明确要原理图/机制图/架构图时使用 `schematic`。后续新增类型应作为 `config.yaml:modes.presets` 扩展，不改主流程。
- `parallel-vibe` 是必选工作流的一部分，不是可选增强；默认通过 `scripts/run_draw_plot.py` 在独立隐藏工作区里完成整个闭环。
- `auto-draw-plot` 独立负责需求拆解、prompt 生成、图片 generation/edit、多轮保真微调、评估与交付；图片请求由本 skill 的脚本通过 BenszAPI 提交，不调用也不依赖 `imagegen` skill。完整的 `imagegen` 技能边界见「Skill 专属约束」。

## 流程

### 输入

- `user_need`（必需）：自然语言描述的图像需求、输出用途、必要的视觉语义与格式要求。
- `mode`（可选）：`general` / `roadmap` / `schematic`；默认 `general`。模式只改变 prompt preset、默认画布和评估口径，不引入 legacy draw.io 渲染器。三种模式的语义与文字策略：
  - `general`：通用绘图模式，适合普通信息图、封面图、概念图和自由描述。
  - `roadmap`：技术路线图模式，强调 3-5 阶段、阶段标题条、主链箭头、风险/备选虚线、A4 打印可读。
  - `schematic`：原理图/机制图模式，强调分组大框、圆角节点、机制链/模块关系、主链与辅助箭头分层。
  - `roadmap` / `schematic` 的文字策略：优先把标签自然换成 2-3 行，也不要横向压缩字形；默认使用现代黑体/思源黑体/Noto Sans CJK 风格的正常字宽、常规到半粗体。除非用户明确要求窄体标题或压缩排版，否则禁止窄体、长体、压缩体、condensed/narrow/compressed font、横向压缩和瘦长拉伸字体。
  - 不要把 `roadmap` / `schematic` 回退成 draw.io、SVG/PDF 或 TEX 强绑定流程；这些 legacy 能力只作为 prompt 和评估经验迁移。
- `api_config`（可选）：Codex 本机配置优先使用 `~/.codex/config.toml` 中当前 BenszAPI provider 的 `base_url` 与 `experimental_bearer_token`；`~/.codex/auth.json` 仅作为兼容认证来源，`~/.bensz-skills/config/remote.env` 只作为缺失字段的兜底。默认 `auto` 只在运行前按优先级选择连接与鉴权检查通过的 provider，真实生成资格以 Images submit 响应为准。
- `image_provider`（可选）：用户明确指定的图片模型/provider，如 `gpt-image-2.5-flare`、`gpt-image-2.5-sunburst`、`gpt-image-2` 或 `nano_banana`。显式指定后必须只用该 provider/model，失败时暂停并报告原因，不得切换到其他模型。
- `allow_provider_fallback`（可选）：只有用户明确说“失败可以换模型/可以回退到另一个 provider”时才为 true；该授权仅覆盖已确认未创建任务的 provider 故障，不覆盖订阅、余额、权限、overage、计费服务错误或 submit 空/非 JSON 等任务创建状态不确定的协议错误。
- `max_rounds`（可选）：最大优化轮数，默认 3；若用户另有指定，以用户为准。
- `visual_constraints`（可选）：比例、期望布局、色调、字体等硬约束。尺寸只作为 provider 原生尺寸选择参考，不承诺最终导出像素。
- `quality` / `provider_size` / `output_format` / `output_compression`（可选）：OpenAI 图片模型显式 provider 参数；默认模型为 `gpt-image-2.5-flare`，默认参数分别为 `low`、`1024x1024`、`jpeg`、`85`，均执行白名单或范围校验。
- `reference_images`（可选）：用于 prompt 引导的风格/布局图；第 2 轮起上一轮 `output.jpg` 会自动作为第一参考图，用户参考图排在其后。
- `workspace_base`（可选）：用户显式指定的隐藏工作区根目录；未指定时使用当前目录 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-draw-plot/`。

### 执行步骤

1. **理解需求与模式**：宿主 AI 先把用户需求拆成“主体 / 结构 / 风格 / 硬约束 / 禁止项”，并解析 `mode`；未指定时用 `general`。需要时参考 [references/prompt-guidelines.md](references/prompt-guidelines.md)。
2. **声明监督路径**：若用户传入 `workspace_base`，解析该路径；否则解析 `project_root/.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-draw-plot`。必须把解析后的绝对路径用可见消息在 API 检查、`init_workspace.py`、`run_draw_plot.py` 或任何图片生成调用之前告诉用户，例如：`本次 auto-draw-plot .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-draw-plot 工作区绝对路径：/abs/project/.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-draw-plot`。不要只把路径写进 `run-manifest.json`；初始化后可再补充实际 `run_dir`，但不能用 `run_dir` 补充替代启动前的根目录声明。
3. **检查 API**：运行 `scripts/nano_banana_check.py`。默认优先读取本地 Codex 配置：从 `~/.codex/config.toml` 当前 BenszAPI provider 获取 base URL 和 `experimental_bearer_token`（或 provider 内兼容 token 字段），再从 `~/.codex/auth.json` 获取兼容 key；环境变量与 `remote.env` 只作为缺失字段的兜底来源。Windows 同时兼容 `%USERPROFILE%`、`%HOMEDRIVE%%HOMEPATH%` 与 Git Bash/PowerShell 的 `HOME`。配置加载必须记录实际配置文件路径、来源和 API Key 不可逆短指纹；若 Codex 配置与 BenszAPI 环境变量同时存在且 Base URL/API Key 不一致，必须在发图前停止并报告冲突字段，不得静默使用旧配置；诊断证据不得写入完整密钥。`gpt-image-2.5-flare`、`gpt-image-2.5-sunburst` 与 `gpt-image-2` 共享 OpenAI Images provider，只能绑定 `benszresearch.com` 子域名 base URL；非 HTTPS、裸域、非白名单域名或缺少 key 时不得绕过校验。若配置只提供子域名根地址，客户端会在校验后统一规范为带 `/v1` 的 API 基址，避免 Images 请求落入站点 HTML fallback。
   - 若用户点名 `gpt-image-2.5-flare`、`gpt-image-2.5-sunburst`、`gpt-image-2`、`Nano Banana`、`Gemini` 或其他具体 provider/model，运行前检查和后续出图都必须固定在该 provider/model，并给主脚本传 `--provider <name>`；失败时输出可执行的配置/额度/端点错误，不自动切到另一个模型。
   - 默认 `auto` 会按 provider 优先级检查配置、连接和鉴权；`/v1/models` 成功只能表述为 `connectivity/authentication_ok`，不得写成“可生图”或 `generation_eligible=true`，真实 Images submit 才是当前请求的准入判断。此步骤不执行完整 Images 计费资格检查，不要把“指定模型失败”改写成“自动使用另一个模型”。
4. **初始化隐藏工作区**：运行 `scripts/init_workspace.py`，默认建立 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-draw-plot/{yyyy-mm-dd-hh-mm}/`，写出 `run-manifest.json`。
5. **生成 parallel-vibe 计划**：每一轮开始前，必须生成该轮的 `parallel-vibe` plan；即使宿主 AI 最终不真正启动 `parallel-vibe` CLI，也必须按它的 thread/workspace 协议为每一轮写出合法 `plan.json`，至少写出：
   - `parallel-vibe/parallel-plan.round-XX.json`
   - `parallel-vibe/parallel-plan.json`（latest）
   - `rounds/round-XX/parallel-plan.json`

   主入口 `scripts/run_draw_plot.py` 已经会为每一轮自动生成 parallel-vibe plan，用户无需额外手工执行；若宿主 AI 想把“下一轮 prompt 草案”真正交给独立线程处理，则直接复用该轮 `parallel-plan.round-XX.json`。`parallel-vibe` worker 当前仍只负责在隔离 workspace 里产出 prompt 草案与评估请求模板；真正的出图与评估继续由本 skill 的主脚本完成，避免跨 workspace 回写导致不稳定。
6. **生成第 1 轮 prompt**：
   - 优先由宿主 AI 在调用脚本前完成需求拆解与 prompt 规划；
   - `run_draw_plot.py` 只做本地模板拼装与护栏合并，不默认调用 Gemini / Nano Banana 等远端文本规划接口；
   - prompt 仍需忠实反映用户需求，不得暴露密钥或绝对路径。
7. **调用图片模型**：运行 `scripts/generate_image.py` 或主入口 `scripts/run_draw_plot.py`；OpenAI 图片模型默认使用 `gpt-image-2.5-flare`，也支持显式指定 `gpt-image-2.5-sunburst` 或 `gpt-image-2`。纯文本出图默认提交到 `/v1/images/jobs/generations`，存在参考图时默认提交到 `/v1/images/jobs/edits`。配置仅给出 BenszAPI 子域名根地址时，客户端会先规范为带 `/v1` 的 API 基址；同步端点只在 job endpoint 明确不支持时兼容回退。submit 在服务端尚无持久幂等契约时只提交一次；结构化 `retryable=false`（包括 `BILLING_PRICING_NOT_CONFIGURED`）立即停止，`2xx` 空/非 JSON 响应也不重试或跨 provider，poll/result 的暂时故障独立处理。默认请求 `quality=low`、最小匹配原生尺寸和 `output_format=jpeg`，输出扩展名、magic bytes、MIME 与 meta 必须一致；PNG/WebP 回退结果导出 JPEG 时以白色合成透明背景。参考图编辑会追加“只改明确要求、保留主体/构图/背景”的契约，并记录原始参考图 SHA-256。
   - 回退授权：只有用户主动要求允许回退时，才设置 `allow_provider_fallback=true` 或脚本参数 `--allow-provider-fallback`；回退路径使用 `~/.bensz-skills/config/remote.env` 中的 `GEMINI_BASE_URL`、`GEMINI_API | GEMINI_API_KEY`、`GEMINI_MODEL`。即使已授权，计费、订阅、余额、权限、overage、`BILLING_SERVICE_ERROR` 与 submit 空/非 JSON 等任务创建状态不确定的协议错误仍必须停在原 provider 并展示结构化错误。
8. **视觉评估**：
   - `scripts/evaluate_image.py` 默认只做启发式文件/分辨率检查并标记 `fallback_mode=heuristic`，不调用 Gemini 文本接口；
   - 宿主 AI 必须根据最终图片、用户需求与 `evaluation.json` 做语义把关，必要时人工触发下一轮。
9. **多轮优化**：上一轮若未通过，第 `n+1` 轮必须把第 `n` 轮 `output.jpg` 作为第一参考图传给可消费参考图的图片 provider，并把反馈拼进 prompt，要求模型保真微调而不是从零重画；首轮用户参考图也必须标记为 `image-to-image`，来源使用 `user_reference` / `previous_round` / `mixed`。
10. **交付**：输出至少 1 张最终 JPEG；隐藏目录里保留 `meta/result.json` 供追溯。

### 输出

- 至少 1 张合乎需求的图像；OpenAI 图片模型正式输出默认为 `jpeg`。
- 隐藏目录里的 `meta/analysis.json` / `meta/result.json`：记录每轮 prompt、模型参数、参考图策略、评估结果、最终选图和停止原因。
- 每轮图片 meta 必须区分 `requested_provider_size`、`native_size`、`output_size` 与 `postprocess_resize_applied`；默认 `postprocess_resize_applied=false`。
- `image-debug/gpt-image-2-error.json` 只保留错误类别、HTTP 状态和服务端安全返回的 `error.type` / `error.code` / `error.message`。JSON 与 multipart 请求发送安全 `X-Client-Request-ID`；`2xx` 空正文或非 JSON 正文分别记录 `PROVIDER_EMPTY_RESPONSE` / `PROVIDER_NON_JSON_RESPONSE`，附经白名单校验的 `request_id` / `client_request_id`、origin/path、响应类型、声明/实际长度、SHA-256、首字节类别和重定向布尔值；不得写入 query、Authorization、API Key、Cookie、prompt、原始正文、订阅明细或原始内部错误对象。
- 每轮目录：`rounds/round-XX/prompt.txt`、`rounds/round-XX/prompt-plan.json`、`rounds/round-XX/parallel-plan.json`、`rounds/round-XX/output.jpg`、`rounds/round-XX/evaluation.json` 以及 `image-debug/` / `evaluation-debug/`；OpenAI 图片模型默认主动使用 Sub2API image job endpoint，generation/edit 均显式发送 `quality=low`、原生尺寸和 `output_format=jpeg`，并在 debug meta 中保留参考图 SHA-256。
- run 级 `parallel-vibe/parallel-plan.json` 与 `parallel-vibe/parallel-plan.round-XX.json`：每轮必留痕的 parallel-vibe plan。

### 输出管理

- 默认工作区是当前目录下的 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-draw-plot/{yyyy-mm-dd-hh-mm}/`；所有中间文件必须留在隐藏目录里，正式交付物不写入该目录。
- 同一任务复用一个任务根目录；多 Skill 协作才创建 `shared/`，本 Skill 专属材料放入 `auto-draw-plot/` 的 `input/`、`output/`、`log/` 子目录。
- 轻量测试目录固定为 `./tests/draw-plot`，中间文件限定在 `tests/draw-plot/_artifacts/`（见「校验」）。

### 校验

- 轻量测试必须在 `tests/draw-plot` 下完成；每次执行都应该在该目录内生成 `TEST_PLAN.md`/`TEST_REPORT.md`，并把中间文件限定在 `tests/draw-plot/_artifacts/`。
- auto-test-skill 的 A/B 轮也只能操作 tests 目录，确保 `p0-p2` 问题均闭环。
- 视觉语义把关不可脚本化：宿主 AI 必须依据最终图片、用户需求与 `evaluation.json` 复核启发式评估结论后才可交付。

### 失败与恢复

- 配置冲突：Codex 配置与 BenszAPI 环境变量的 Base URL/API Key 不一致时，必须在发图前停止并报告冲突字段，不得静默使用旧配置。
- 域名校验失败：OpenAI 图片模型出现非 HTTPS、裸域、非白名单域名或缺少 key 时停止，不得绕过校验。
- 指定 provider 失败：暂停并报告原因，输出可执行的配置/额度/端点错误，不自动切到另一个模型；provider 回退仅按「执行步骤」第 7 步的授权边界执行，任务创建状态不确定的协议错误一律停在原 provider 并展示结构化错误。
- submit 失败：服务端尚无持久幂等契约时只提交一次；结构化 `retryable=false`（包括 `BILLING_PRICING_NOT_CONFIGURED`）立即停止，`2xx` 空/非 JSON 响应不重试、不跨 provider；poll/result 的暂时故障独立处理。
- 评估未通过：按「执行步骤」第 9 步进入多轮保真微调；达到 `max_rounds` 或得分平台期仍不达标时，交付当前最优结果并在 `meta/result.json` 记录停止原因。

## 约束

<!-- BEGIN COMMON CONSTRAINTS -->
<!-- Source-Hash: sha256:15120201e9e0c7569517261d57ecefb63ac279c26ed13876f8e95b6dc35854d3 -->
<!-- Template-ID: skill-common-constraints; Template-Version: 1; Sync-Policy: exact-block -->

### 公共硬约束

本块由 `docs/templates/skill-common-constraints.md` 统一维护；每个 `SKILL.md` 的 `## 约束` 必须逐字同步本块，不得在副本中改写公共规则。

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- `bensz-collect-bugs` 是一个 Agent Skill；仅将 Bensz Agent Skill 或 Bensz 基础设施本身的设计缺陷交给它。先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。

<!-- End of canonical common constraints. -->
<!-- END COMMON CONSTRAINTS -->

### Skill 专属约束

- `imagegen` 技能边界：用户要求用 `auto-draw-plot` 画图、改图或基于上一轮继续微调时，只使用本 skill 完成完整链路。不得把它表述或编排为“先生成 prompt，再交给 `imagegen` 出图/编辑”的前处理步骤；这种说法会错误暗示依赖关系，并可能造成重复生图与重复计费。
- 只有用户明确点名同时使用 `imagegen`，或明确要求其独有能力时，才允许额外调用 `imagegen`；调用前说明两者各自独立的职责，且不得将 `imagegen` 伪装成 `auto-draw-plot` 的内部依赖。默认用户可见说明应写明：`本次使用 auto-draw-plot，由其经 BenszAPI 完成 prompt、出图和后续编辑。` 不得默认承诺后续会调用 `imagegen`。
- `gpt-image-2.5-flare`、`gpt-image-2.5-sunburst` 与 `gpt-image-2` 只能绑定 `benszresearch.com` 子域名 base URL；非 HTTPS、裸域、非白名单域名或缺少 key 时不得绕过校验。
- 错误诊断与 `image-debug/gpt-image-2-error.json` 不得写入 query、Authorization、API Key、Cookie、prompt、原始正文、订阅明细或原始内部错误对象；诊断证据中的 API Key 只允许不可逆短指纹。
- 历史隐藏目录只允许显式兼容读取、迁移或清理，不做静默处理。
- 因本 skill 设计缺陷导致的 bug 先按公共约束记录到 `~/.bensz-skills/bugs/`；只在用户明确要求 “report bensz skills bugs” 时，才通过本地 `gh` 调用将新 bug 推送到 `huangwb8/bensz-bugs`，上传前必须先脱敏本地路径/用户名等隐私。
- prompt 结构模板与迭代策略见 [references/prompt-guidelines.md](references/prompt-guidelines.md)；合法的 `parallel-vibe` shell plan 模板见 [references/parallel-plan.md](references/parallel-plan.md)。
