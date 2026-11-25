---
name: qwen-image
description: DSH 图像工作区：远程 Turbo 快速文生图用 image_mode=turbo，生图优先 qwen_generate_image，同步对话进度与图库；原生参考编辑用 reference_mode=edit；qwen_image_import 导入网址/本机文件/对话参考图，qwen_image_resources 查资源，qwen_image_presets 配置和保存整套预设，qwen_image_connection 实时切换本机/远程并设置空闲卸载；qwen_image_jobs 批量查队列、qwen_image_cancel 取消任务、qwen_image_gallery 只读检索图库、qwen_image_batch 批量提交、qwen_image_import_many 批量导入、qwen_image_export 复制导出、qwen_image_score 本地客观评分、qwen_image_reroll 按标记重投、`source_image_ids` 多图编辑。不改跑独立脚本。
whenToUse: 实际生图、搜索参考图后图生图、按指令改图或换画风、导入图片、参考变体、局部重绘、配置 LoRA/控制图/蒙版/采样、保存或加载图像预设、切换本机或远程生图、调整空闲卸载时间、批量提交或导入、批量查任务/取消任务、按提示词或种子检索图库、导出任务文件、查询资源或已有结果时加载。仅写提示词、讨论方案、搜索已有图片时不自动生成。
---

# 图像：生成与任务恢复

## 执行路由

用户要出图时，使用已注册的 `qwen_generate_image`。它统一管理任务、按需启动、会话进度、图片附件与图库；提示词类技能负责画面描述，执行仍走此工具。若本技能正文已经完整注入，不重复加载。

- 用户说“用 Turbo 快速打样”时，调用 `qwen_generate_image(prompt=完整画面描述, image_mode="turbo")`。该档加载 Qwen 2.1 Turbo 权重，固定 8 步，适用远程纯文生图。用户要求质量档时传 `image_mode="quality"`。省略档位沿用插件设置；单独改步数不会切换模型。
- 常规生图、参考变体、负向提示词、CFG 与支持的调度器，优先用工具当前公布的参数。
- 不用终端、Python/MFLUX CLI、旧生图工具、直接 HTTP 请求或手写图库文件代替插件；不用安装软件、修改插件、运行补丁或手动启动服务。
- 工具缺失、参数未支持或失败时，如实说明具体情况，保留任务 ID。不要静默改跑脚本或切到其他服务。只有用户明确要求使用独立 CLI/其他产品时才采用其指定路线，并说明它不具备本插件完整的会话进度同步。
- 以当前工具 schema 为准。MFLUX 库、独立脚本或其他技能里写过的能力，不代表当前插件已接入。网址、本机文件和会话图片附件先用 qwen_image_import 导入。参考变体与原生参考编辑是两种模式，不把强度式图生图承诺为指令编辑。原生编辑支持兼容 MFLUX 的完整视觉模型和更新后的远程 Qwen 网关，不能承诺任意局部像素精确保留。LoRA、图库控制图与蒙版按下节的限制使用。
- 仅要求提示词、解释原理、讨论画面或找已有图片时，不提交生图任务。

## 搜索参考图 → 导入 → 图生图

用户明确要求“上网找参考并生成”时，连续完成以下步骤，无需手动打开图库：

1. 使用当前会话可用的联网搜索/浏览器工具找图，查看原始来源与图片内容，取得 PNG/JPEG/WebP 的公开图片直链。插件负责导入，不自带搜索引擎；不要把搜索结果网页、预览页面或凭空编造的网址当图片。没有搜索工具时如实说明，可继续使用用户给的真实图片链接、文件或附件。
2. 调用 `qwen_image_import(url=真实图片直链, kind="source", name=简短名称)`。已有本机文件则传 path；用户上传的会话图片传完整 attachment（attachmentId、mediaType、bytes、width、height，可含 name）。只复制上下文实际提供的字段，不虚构。已有图库/资源 ID 无需重复导入。
3. 检查成功返回的 id、尺寸与 settings。用户要换画风、改颜色、按图中主体做编辑时，先查询资源工具，确认当前后端的 reference_edit.supported 为 true，调用 `qwen_generate_image(source_image_id=id, reference_mode="edit", scheduler="linear", prompt=明确的编辑要求)`；尺寸为32的倍数，不传 change_strength、控制图或蒙版，按完整步数采样。本机组件缺失或旧网关不支持时明确说明，不能自行切换或冒充原生编辑。用户只要保留照片做轻微变体，或明确指定变化幅度时，沿用 variation 默认模式和 change_strength（默认0.45）。
4. 继续通过插件显示真实进度、结果附件和图库记录。适当注明参考来源网页；导入失败只换可用直链或说明错误，不偷偷跑下载器/生图脚本。用户仅要求找图或导入时停在对应步骤，不额外生成。

公网 URL 不支持登录、Cookie 或内网/Tailscale 服务，重定向也会逐跳检查。图片限制与面板一致：PNG/JPEG/WebP、64MiB、最长边8192、3200万像素。HTML 页面需先浏览取得真实图片链接。导入时不启动模型或 SSH，也不改变本机/远程模式。

导入用途不会加工图片：control 必须本身就是线稿/姿态/边缘等有效结构图；mask 必须是用户需要的黑白蒙版，不会把普通照片自动变成姿态或蒙版。需要生成这些素材而工具未提供相应能力时明确说明。

## 配置与保存高级参数（不等于生成）

先区分用户意图：只问说明就解释；只想配置或保存就用资源/预设工具，不调用生成。只有明确要求出图才调用 `qwen_generate_image`。

| 需要完成的事 | 工具与操作 |
| --- | --- |
| 导入新参考图、控制图或蒙版 | `qwen_image_import`：url / path / attachment 三选一，返回真实 ID；不生图、不启动模型 |
| 查有哪些 LoRA、已导入图、蒙版 | `qwen_image_resources(kind, query)`；返回真实名称、来源、ID/路径，不加载模型 |
| 看有哪些预设 | `qwen_image_presets(action="list")`，获取真实 ID 与 revision |
| 取出某套参数继续调整 | `action="load", id`；检查 issues，取 settings，与用户要求合并 |
| 保存当前完成图的配置 | 先 list，再 `action="save", name, revision, from_job_id` |
| 保存新参数组合 | 先 list，再 `action="save", name, revision, settings` |
| 覆盖已有预设 | load 后合并完整 settings，save 时同时传真实 id、name、revision；用户未要求覆盖就新建 |
| 重命名、默认或删除 | list 后用 rename / set_default / clear_default / delete 与 revision；仅执行用户要求的操作 |
| 备份或导入 | export 返回可移植 JSON；import 用 document_json 和 revision，不写文件、不运行脚本 |
| 查询运行位置/卸载时间 | `qwen_image_connection(action="status")`，获取 mode、idle_minutes 与 revision；不建立 SSH |
| 用户要求切换本机/远程 | 先 status，再 `action="switch", mode="local"或"remote", revision`；复用已有连接配置，持久保存并立即生效，不需要重启 |
| 用户要求改空闲时间 | 先 status，再 `action="set_idle", idle_minutes, revision`；本地与配套远程网关共用，不改变预设 |

切换必须由用户要求，不能把失败任务自动转到别的后端。存在上传、排队或生成时工具会阻止切换，等待任务结束再操作。不要声称 connectionMode 只能手动修改或必须重启；用工具实际返回的状态确认。若宿主尚未注册该工具，才说明需要更新插件并重新加载一次，不能用 shell 修改配置代替。

**保存 settings 是整套替换，不是补丁。** 被省略的字段回到内置默认值。修改已有预设时先 load，把返回的完整 settings 与改动合并，再保存。settings 与生成工具使用相同参数名，但不含 prompt；不要把连接密钥、Python/模型/缓存目录塞进预设。

**加载不会自动出图，也不会替换用户正在编辑的面板草稿。** 会话中要按该预设出图：先 load，确认 issues 为空，将 settings 与完整 prompt 合并交给生成工具。保存和默认设置与面板共用同一个库；面板重新打开高级设置，或在「管理 → 刷新列表」读取。用户在面板选中预设后才替换那里的高级参数，画面描述始终保留。设默认仅影响首次空白草稿或主动恢复默认，不覆盖已有草稿和已提交任务。

### 资源选择与高级参数

- 先查资源，按名称、来源和用途选择。LoRA 用返回的 path，图片用返回的 32 位 id；不猜路径、图片 ID、ControlNet 权重或 LoRA 兼容性。图片名称不清楚其内容时，请用户指明用途。工具清单不展示图片内容，文件名不能证明它是有效蒙版。
- 新图片使用 `qwen_image_import` 导入，不要求用户手动去图库选文件。网址用 `url`，本机绝对路径或 `~/` 用 `path`，会话图片用真实完整 `attachment` 引用；三者只能选一个。`kind` 为 source / control / mask，默认 source。工具返回 `settings` 可合并到生成参数或预设；导入不覆盖面板草稿，也不会生成图库作品。不要猜附件字段或传裸附件哈希。
- `lora_paths` 与 `lora_scales` 顺序一一对应；UI 默认权重 0.8，工具省略权重默认 1.0，保存时请显式带上需要的权重。LoRA 与底模应兼容，最多 8 个。
- 结构控制用 `controlnet_image_id` / `controlnet_strength`（0–1，默认 1）。执行端必须已准备好 Qwen Image 2.1 Union 权重。只需要结构控制时不传 source_image_id；本机 MLX 与原图组合时需要蒙版；配套远程网关也支持无蒙版的原图 + 控制变体。
- 局部重绘：`source_image_id` 为原图，`mask_image_id` 为蒙版，白色重画、黑色保留。不要同时传 change_strength；保持原图尺寸才能保留原始像素。
- 参考变体：source_image_id + change_strength，不保证换画风或精准局部编辑；测试中即使换 prompt，也可能强烈重建照片。
- 原生参考编辑：source_image_id + reference_mode="edit" + linear。当前后端 reference_edit.supported 必须为 true；把图片同时送入视觉/文本条件与参考潜变量，完整步数从噪声生成。用于“转水彩、换颜色、按指令改图”，不使用 change_strength，不与 ControlNet/蒙版混用，支持同一 LoRA 通道。32倍数尺寸。本机使用 QwenImage21Edit，需要完整视觉编码器；纯文本导出不可用。不支持时说明返回的 reason，而非自动切换后端。旧预设未保存该字段时仍为 variation。保存和复用 edit 预设时保留 reference_mode，不补入 change_strength。
- negative_prompt / guidance / scheduler 在本机和配套 Qwen 远程网关支持。普通文生图的 CFG 只在负向词非空且值大于 1 时生效；结构控制/蒙版分支在 CFG > 1 时可使用空负向词。填写负向词且 guidance 为 1 时实际自动使用 2.5。CFG 不是通用质量旋钮。
- linear 为默认。结构控制或蒙版只能用 linear；另外两个调度器仅用于支持的普通文生图。先看资源查询或预设加载返回的 remote_capabilities：配套 Qwen 网关支持 LoRA、ControlNet、蒙版、参考变体和三个调度器；普通 OpenAI Images API 仍只有基础文生图。不得静默丢弃高级预设参数。
- 未指定 seed 表示随机；固定 seed 便于比较。步数更多不保证更好。保存完成图会保留其实际种子；若用户要随机种子预设，改用 settings 保存并省略 seed。
- 缺失资源时 load 返回 issues 且不提供可提交 settings，先重新选择或移除缺失项。冲突时重新 list 核对，不用旧 revision 循环重试。不要删用户图库或移动资源来解决预设错误。

### 远程使用与进度

- 资源和预设继续引用 客户端电脑上的真实 path / 32 位图片 id。插件按 SHA256 自动同步选中的文件到远程私有缓存，不需要修改现有预设或猜 Windows 路径；首次同步 LoRA 可能较慢。
- `lora_paths` 是插件工具的本机输入，并不是发送给 Windows 的路径。网络请求仅包含 LoRA 的内容 SHA256 与 scale，服务器用校验后的 `<sha>.safetensors` 加载；不会按原文件名猜测。不同内容同名不混用。资源被移动或删除时需在资源库重新选择。
- 按需 SSH 只在真正提交生图时连接，资源/预设/配置查询及检查不会唤醒连接。离线返回的 `remote_capabilities.verification="on_generation"` 是已配置协议的预期能力，提交时仍会实际握手，不能当成服务器在线证明。上传、排队、采样与保存都保持连接；最后一个任务结束后按设置计时，确认卸载才断开。Mac 休眠或进程异常退出时，服务器还有同一时长的独立空闲释放。
- 用 `qwen_image_resources` 查看 mode 与 remote_capabilities，不启动模型。配套网关的 features 包含 lora / controlnet / mask / img2img / progress；能力不足时明确说明，不换脚本。
- 上传、排队、加载、真实采样步数和保存结果会同步到会话卡片、创作页和图库；切换页面不会取消任务。不要把上传阶段或模型加载说成采样进度，也不要编造百分比。
- 服务器返回的图先保存回客户端图库，再显示对话附件。隐私分类只影响图库，绝不隐藏对话图片。
- 本机与 CUDA 的量化、随机数和计算实现不同，相同种子不保证像素一致。固定同一后端、模型精度、分辨率、步数、调度器、提示词和 LoRA/控制参数后，seed 才有可靠的复现意义。跨后端仍可对比质量/遵循度，但不能把同 seed 当成同一初始噪声或逐像素对照。预设字段沿用，优先用 linear；其他调度器按网关公布的 schedulers 使用。

### 简短操作例子

用户：“把刚才这张的参数存成产品摄影。” → list 获取 revision；save(name="产品摄影", from_job_id=刚才的完整任务ID, revision=返回值)。返回保存的名称/ID，不再生一张。

用户：“用产品摄影预设，换成绿色茶壶再画一张。” → list 找预设ID；load 检查 issues；保留返回的 settings，只把 prompt 写成完整的绿色茶壶目标描述，然后 qwen_generate_image。完成后直接展示插件附件，不运行独立脚本。

## 一次创作

1. 根据用户约束组成完整目标描述：主体、环境、构图、风格、光线及需逐字呈现的文字。中文可直接用，不添加无关主体或风格；关键缺失信息无法合理推断时再追问。
2. 调用 `qwen_generate_image`。默认 1024×1024、40 步；横图 1344×768、竖图 768×1344。只有用户明确要试稿/测试时使用 512×512 或低步数。
3. 工具执行期间，对话和左侧「图像」显示任务状态；本机和配套 Qwen 网关提供真实采样步数；普通远程 Images API 只能显示处理状态。不要编造百分比、耗时或实时半成品图片。
4. 成功后直接呈现工具图片附件，保留完整任务 ID 供后续迭代。无需再查找、复制、导入图片或把附件 JSON/文件路径当成图片展示。图库开启隐私模式时，未收藏结果进入隐私图库；对话中的图片与进度照常显示。

## 继续调整

- 重新构图或按新描述重画：使用完整 prompt，不传 `source_image_id`。
- 沿用上张图生成变体：传工具返回的 32 位任务 ID 为 `source_image_id`，配合 `change_strength`。默认 0.45；较低值更接近原图，较高值变化更大。描述完整目标，保留用户要求不变的主体和构图。
- source_image_id 单独使用是强度式图生图。换画风或按指令改图优先按上节检查当前后端原生编辑能力；蒙版精确保留走已有局部重绘分支。不要把“改提示词重画”说成参考编辑，也不编造任务 ID，不传文件路径或附件哈希充当 ID。
- 多轮“继续改这张”使用指代对应的结果；多个同等可能的版本才追问。固定尺寸、种子等参数有助于比较，但不保证不同运行环境逐像素一致。

## 查询与取回：qwen_image_status

收到提交回执或错误里的任务 ID 后，需要查进度、恢复结果或用户问“画好了吗/图在哪”时，调用 `qwen_image_status(id)`。它只读取任务；完成时直接返回同一张图的附件，不启动模型、不重新生成、不搜索文件。

- 任务仍在排队/加载/生成/保存：报告工具返回的状态，让现有进度卡片继续更新。不要紧密循环轮询，也不再提交同一请求。
- 任务已完成：直接展示返回图片；恢复结果不会创建第二张图库作品。
- 任务失败或已取消：说明具体错误；更正参数或明确重试前不自动再生一张。
- 任务不存在或已在回收站：说明状态，让用户在图库中核对；不要自行新建目录、改 job.json 或把独立脚本产物冒充原任务。
- 等待超时、网络中断或取消等待不等于取消后台生成。先查询已接受任务，避免重复开跑。

若一次变体没有达到画风要求，不用几乎相同参数连续抽卡、臆断“提示词未传”或自行升级调参。最多做一次有依据的调整；需要改模式或超出用户明确参数时先说明。只有核对任务请求、工作流条件连接与对照结果后才能判定接口缺陷。

## 默认路线：先文生图，再参考图

不要把所有需求都做成参考编辑。默认先用 `qwen_generate_image` 文生图探索姿势、构图、服装；只有以下情况才用参考图：

- 要指定某个人物的脸/身份
- 要把一件指定服装穿到人物身上（人物 + 服装两图）
- 要保留指定场景/机位做局部修改

生成耗时与模型、硬件、尺寸、步数和冷启动有关，不承诺固定秒数或质量保证。参考编辑可能继承原图构图与不需要的细节；应检查真实结果。

## 编辑模式的负向提示词

负向提示词按用户目标选择。非空负向且 guidance=1 时本插件会提高到 2.5，可能增加计算量；不要把其他模型的建议说成此工作流的保证，也不要凭空引用基准。

## 多图参考：source_image_ids

Qwen 2.1 原生支持多图编辑（远程网关 2.17+）。`qwen_generate_image` 传：
- `reference_mode: "edit"`
- `source_image_ids: [id1, id2, …]`（2–8 张已导入图片）
- prompt 里用 `<image1>`、`<image2>` 明确指代，例如：
  「保持 <image1> 的人物身份和脸，换成 <image2> 的服装；姿势与机位沿用 <image1>。」

不要同时传 `source_image_id`、`change_strength`、`mask_image_id` 或 `controlnet_image_id`。
本机 MFLUX 不支持多图，会直接报错，不会偷偷退化成单图。创作页与预设已支持多图：第一张是主图，其余作为附加参考；导出预设会清空本机 ID，导入时按资源指纹重挂。

通用多图操作示例见 [多图编辑](../../docs/recipes/garment-swap-v1.md)。不同参考图可能互相影响；先明确每张图负责的主体、物品或风格，并检查输出，不承诺固定成功率。参考图宽高比不同时可能中心裁切，注意边缘内容。

## 客观评分：qwen_image_score

`qwen_image_score({ids, write?})` 对已完成任务算本地指标：edge/detail、grain、饱和度、亮度、肤色占比、高光/阴影剪切，并给暂定 flags（heavy-grain / texture-overload）。它是**诊断报告，不是 pass/fail 门禁**；阈值要等人工 ground truth 校准。`write=true` 只在图片旁写 `qa.json`，不改图片、收藏或任务记录。评分不加载模型、不建 SSH。

命中 `heavy-grain` / `texture-overload` 时用 `qwen_image_reroll({ids})` 重投：同 prompt、同参数、seed+1，原图保留。它只重投命中标记的图，不重试未命中的；新图出来后再次评分。

## 批量提交、批量导入与导出

- 一次要出多张、或多个 seed 对比：`qwen_image_batch({jobs:[...], max_parallel?})`，1–10 个独立任务，返回真实 id，**不等待出图**。每个任务接受与 `qwen_generate_image` 相同的参数；后端只有 4 个准入位，工具会自动分波。失败按 index 报告，不自动重试已接受任务。
- 一次导入多张本机参考图：`qwen_image_import_many({paths, kind})`，1–20 个绝对路径或 `~/`。同内容同 kind 返回已有 id（`deduped: true`），不会重复占空间；单张失败不影响其余。
- 要把已完成任务交给外部图库/工具：`qwen_image_export({ids, out_dir})`，复制为 `<id>/image.png`、`<id>/job.json` 和 `manifest.json`，原图库不动、目标存在时拒绝覆盖。

## 队列、批量状态与只读检索

- 需要一次查多个任务或看整条队列：`qwen_image_jobs(ids?, status?, limit?)`。它有 `ids` 时批量返回，没有时返回活动队列、队列顺序和状态计数；只读，不启动模型。
- 需要取消排队/生成中的任务：`qwen_image_cancel(ids)`。已结束或不存在的 ID 会逐条报告，不影响其他 ID；取消不删除图片。远程任务只有当前 DSH 进程仍持有请求时才能取消。
- 需要按提示词、种子、收藏/归档、来源图或时间检索图库：`qwen_image_gallery(...)`。它只返回元数据与血缘字段（seed、source_image_id、reference_mode、lora_names、elapsed_seconds），不返回图片、附件或文件路径，也不改收藏。
- 单个结果的附件仍用 `qwen_image_status(id)`；不要用 gallery 工具替代取图。

工具遵循 DSH 权限；不自动公开图片、切换服务或改变调用模型的行为规则。图片由工具的附件/演示卡片显示；不要把宿主返回的本机 attachment 存储路径手写成 Markdown 图片链接，尤其是含空格的 Windows 路径。视觉质量依据实际返回结果判断，不声称看见尚未生成的图片。切换 LoRA 组合时由后端重新加载模型，避免残留；Agent 不手动卸载服务或改运行文件。

本机原生编辑保留当前模型目录和同一 LoRA 通道，但编辑与文生图使用不同模型实例，切换时卸载前一个实例。完整采样、不启用 step cache、Turbo 或自动重试；前缀 KV 复用不跳过采样步。参考输入按 1024 像素面积预算预处理；不要声称相同种子跨后端像素相同。

## 插件安装与维护边界（2.19.0）

新装、连接配置、更新或故障诊断时，先阅读包根目录的 AGENTS.md。所有服务器地址、SSH 别名、目录和密钥由用户自行提供/选择；不要复制作者部署或猜测路径。自动检查默认开、自动安装默认关；维护不等于生成，不启动模型或 SSH。升级、回滚前检查任务，安装完成后提示用户择时手动重启，不能终止现有会话。图库收藏记录损坏时停止写入，从设置中的收藏备份恢复；不要删 gallery.json 以“修复”。

## Windows 与远程依赖排错

远程模式的图片导入也需要客户端 Python/Pillow，评分需要 numpy。缺失时报告实际解释器路径和错误，按用户授权参考 AGENTS.md 与 docs/SETUP.md 的 setup-image-python.py 安装；不要把本机依赖错误归因于远程 GPU。Windows 路径使用实际返回值，保留空格和中文；不拼接 shell 命令。多图任务查询/重投应保留 source_image_ids 全部引用。
