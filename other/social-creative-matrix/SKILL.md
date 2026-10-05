---
name: social-creative-matrix
description: 从一条创意自动生成国内社媒矩阵：8平台适配文案（抖音/快手/小红书/微博/知乎/头条/百家号/视频号）+ 9:16、1:1、16:9、3:4 四套AI配图，并规范交付与蚁小二草稿发布。用户提到一条创意全平台、多尺寸、矩阵分发、Canva式社媒、社媒配图加文案、全平台文案时使用。
---

<!-- NOVA-EXEC-BEGIN -->
## Nova Ai-Studio 集成（优先于下文通用路径）

- 所有交付物写入 **`<task-artifact-dir>/`**（系统注入 STDA，勿自建语义目录 social-matrix）。
- **禁止**首 turn `ask_user_question`；从 user goal 推断主题/受众/平台，缺信息用合理默认并正文说明。
- **文档类**可用中文主文件名（与活动主题一致），**须与 write_file 字符串完全一致**；pathHints 兼容英文 legacy：
  - `《{主题}》创意简报.md`（alias: `brief.md`）
  - `《{主题}》创意锚点.md`（alias: `creative-anchors.md`）
  - `《{主题}》社媒文案矩阵.md`（alias: `copywriting.md`）
- 机器文件保持英文：`manifest.json`；配图 `visuals/image-*.png`。
- en UI 会话可仍用英文 basename 主名；中文 UI 优先中文名。
<!-- NOVA-EXEC-END -->

# 社媒矩阵创作（Social Creative Matrix）

将「一条创意」转为**可发布的国内社媒矩阵包**：统一视觉、分平台文案、四套标准比例配图，并可交接蚁小二 `imageText` 草稿发布。

## 安全默认

- 用户**未明确**说「发布 / 上线 / 公开」时：**只落盘文件**，不调用 `publish`。
- 若用户要推送：默认**平台草稿**或蚁小二草稿，见 `references/yixiaoer-handoff.md`。
- 发布权威 DTO 以 **`read_skill yixiaoer`** + `yixiaoer_api` 为准；本技能只做编排与打包。

## 何时使用

- 一条主题/活动，要多平台同步发图文。
- 需要 9:16 / 1:1 / 16:9 / 3:4 多尺寸配图。
- 需要按平台改标题、正文、话题，而不是只给文件名。

## 不要单独用本技能的场景

- 只做单平台深度运营 → `read_skill yixiaoer` + 对应平台 doc。
- 只做文案策略/日历 → 可选 `read_skill mkt-social`（vendor：`skills/vendor/marketingskills/mkt-social`）。
- 只做网页/落地页 → `read_skill open-design`。
- 海外 LinkedIn/X 真发布 → 首版不支持；仅可手写海外文案占位。

## 必读索引（按阶段）

| 阶段 | 文档 |
|------|------|
| 全局 | `references/workflow-phases.md` |
| 1 | `references/creative-brief.md` |
| 2 | `references/creative-brief.md`（创意锚点节） |
| 3 | `references/copy-platform-matrix.md` + `assets/copy-matrix.template.md` |
| 4 | `references/visual-ratio-matrix.md` + `references/deliverables-spec.md` |
| 5 | `read_skill open-design` → `read_skill od-social-carousel` |
| 6 | `references/deliverables-spec.md` + `assets/manifest.template.json` |
| 7 | `references/yixiaoer-handoff.md` + `references/platform-deep-links.md` |
| 发布前 | `references/anti-patterns.md` |

---

## 工作流（7 阶段，按序执行）

### 阶段 1 — Brief 锁定

1. 从 user goal 推断主题、受众、语气、目标平台（8 平台中文名多选）；**勿** `ask_user_question` 挡首文件。
2. 生成 `<slug>`（英文短横线，仅内部引用）。
3. `write_file` → `<task-artifact-dir>/《{主题}》创意简报.md`（或 en：`brief.md`；模板见 `references/creative-brief.md`）。

### 阶段 2 — 创意锚点

1. 写一句话 **valueProp**。
2. 写 **visualPrompt**（给四次 `generate_image` 共用：主体、构图、光线、风格；避免每平台改 prompt）。
3. 写 **avoid**（禁用项）。
4. `write_file` → `<task-artifact-dir>/《{主题}》创意锚点.md`（alias: `creative-anchors.md`）。

**禁止**在未完成本阶段前调用 `generate_image`。

### 阶段 3 — 文案矩阵

1. 读 `references/copy-platform-matrix.md`。
2. 仅为 brief 中选中的平台生成：标题、正文、话题建议、推荐配图文件名、备注（超字策略）。
3. `write_file` → `<task-artifact-dir>/《{主题}》社媒文案矩阵.md`（alias: `copywriting.md`；结构见 `assets/copy-matrix.template.md`）。

### 阶段 4 — 四套配图（严格预算）

**硬限制**：全任务 **仅 4 次** `generate_image`（对应 visuals/ 下 4 个 basename），**禁止**额外 png、禁止 per-platform 配图、禁止 VAP/discover_visual_assets（尤其 fiction/IP 无官网 URL 时）。

1. 优先确认 `tools.image` 已配置；若未配置或失败：
   - 在 `visuals/` 写入 **4 个 SVG 占位**（文件名仍用 image-*.png 或同名 .svg 并在 manifest 标注 placeholder）
   - **不要**反复重试 generate_image；**不要**写根目录 `visual-*.png` 或 `img-*.png`
2. 生图可用时：对 `9:16`、`3:4`、`1:1`、`16:9` 各 **1 次** `generate_image`：

| aspect_ratio | output_path |
|--------------|-------------|
| `3:4` | `<task-artifact-dir>/visuals/image-3x4.png` |
| `9:16` | `<task-artifact-dir>/visuals/image-9x16.png` |
| `1:1` | `<task-artifact-dir>/visuals/image-1x1.png` |
| `16:9` | `<task-artifact-dir>/visuals/image-16x9.png` |

4. 用户只要部分比例时：按 `references/visual-ratio-matrix.md` 省略，并记入 manifest `skippedRatios`。

### 阶段 5 — 可选轮播（仅 brief 要求时）

1. `read_skill open-design`
2. `read_skill od-social-carousel`
3. 生成系列 HTML → `<task-artifact-dir>/optional/carousel.html`
4. 不替代阶段 4 的四张 PNG。

### 阶段 6 — 打包交付

1. 读 `assets/manifest.template.json`，生成 `manifest.json`（含 `platforms`、`copy`、`visuals`、`recommendedMapping`，映射见 `references/visual-ratio-matrix.md`）。
2. `status` 设为 `ready`（未发布）或 `draft`（仅文案图未完成）。
3. 在回复中列出：
   - 文件夹路径
   - 各平台推荐配图
   - 下一步：若要发布，说明需蚁小二 Key 与账号已绑定

### 阶段 7 — 发布交接（可选）

仅当 brief 勾选发布且用户确认：

1. `read_skill yixiaoer`
2. 严格执行 `references/yixiaoer-handoff.md`
3. 发布前对每个目标平台 `read_file` 对应 `references/platform-deep-links.md` 中的子文档
4. 完成后更新 `manifest.status` 为 `published` 或保留 `ready`（仅草稿）

---

## 工具速查

| 工具 | 用途 |
|------|------|
| `ask_user_question` | **禁用**（Nova 从 goal 推断；仅用户明确要求发布偏好时才澄清） |
| `write_file` | brief、文案、manifest、prompt.txt |
| `generate_image` | 阶段 4，四次同 prompt |
| `read_skill` | yixiaoer、open-design、od-social-carousel、mkt-social（可选） |
| `yixiaoer_api` | 阶段 7 accounts / upload / publish |
| `read_file` | 发布前读 yixiaoer 平台 md |

**禁止**：bash 搜索 `api.ts`；禁止外链图片 URL 填入蚁小二。

---

## 与其他技能协作

| 需求 | 技能 |
|------|------|
| 视觉/HTML 精修 | `open-design`、`od-poster-hero` |
| 小红书系列卡片 | `od-social-carousel` |
| 发布执行 | `yixiaoer` |
| 长期内容日历 | `mkt-social`（可选） |

---

## 交付验收

见 `references/workflow-phases.md` 检查表。最低交付：

- `manifest.json`
- `copy-matrix.md`
- `visuals/` 下至少用户要求的 ratio 对应 PNG

用户可复制例句见仓库 `docs/social-matrix-prompt-examples.md`。
