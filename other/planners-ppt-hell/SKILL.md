---
name: planners-ppt-hell
description: 制作与持续修改 SVG 视觉工作台（默认直接打开审阅工作台交付给人看），按需导出可编辑 PPTX 或视频静态关键帧 SVG，并支持参考快提与模板包维护入库。
---

# Planner's PPT Hell

> 来源：阿祖不看 TVC · [demyth.info](https://demyth.info) · `Lawyif@163.com`。署名保留在 Skill 与审阅工作台，不写入客户最终 PPTX、导出 SVG 或 PNG。

本 Skill 的**核心交付物是持久化 SVG 视觉工作台 (`Workbench`)**——它本身就是给人浏览、编辑、调序与演示的交互终端。用户直改与模型候选共用版本库（`workbench_store.py`），`.pptx` 与冻结快照仅在按需外发时生成。核心术语见 [GLOSSARY.md](GLOSSARY.md)，架构裁决见 [docs/adr/](docs/adr/)。

## 同一主线下的任务切入（`Non-linear Playbook`）

所有任务共享**「1. 接收 → 2. 定方向与模板 → 3. 工作台制作与审阅交付（默认终点）」**同一条主线，按当前任务与已有半成品切入：

| 当前任务 | 执行路径 | 按需加载的模块 (Disclosed References) |
|---|---|---|
| **从零 / 从 Bypage 做幻灯片** | `1 → 2 → 3（打开 Workbench 即完成）` | [02_content_stage.md](references/workflow/02_content_stage.md) → [01_template_intake.md](references/workflow/01_template_intake.md) → [04_svg_stage.md](references/workflow/04_svg_stage.md) + [svg_to_ppt_rules.md](references/domain/svg_to_ppt_rules.md) |
| **做视频静态关键帧 SVG** | `1 → 2 → 3（保存 SVG 并交付 Craft）` | [03_video_route.md](references/workflow/03_video_route.md) → [04_svg_stage.md](references/workflow/04_svg_stage.md) + [svg_rules.md](references/domain/svg_rules.md) |
| **处理工作台返修 / 换模板与版式** | 直接进 `3`（`workbench_store.py --state` 读任务） | [04_svg_stage.md](references/workflow/04_svg_stage.md) + [07_visual_review.md](references/workflow/07_visual_review.md) |
| **提炼外部参考 / 维护库模板包** | 走 `2` 的参考快提或模板入库链 | [01_template_intake.md](references/workflow/01_template_intake.md) + [template_package.md](references/contracts/template_package.md)（视频风格沉淀归 `video-craft`） |
| **按需外发：导出可编辑 PPTX / 冻结快照** | 仅在用户明确要求导出或网页点选导出唤醒时执行 | [project_contract.md](references/contracts/project_contract.md) |

## 核心深模块 CLI（`Deep-module Tools`）

在 Skill 根目录运行，路径用绝对路径，具体参数以 `--help` 为准：

| 工具 CLI | 职责与调用时机 (Seam) |
|---|---|
| `python3 scripts/init_svg_project.py` | 初始化项目画布与目录（`--source <稿件> --route slides\|video [--width W --height H]`，或 `--assets <dir> --plan <visual-plan.json>`）。已有项目直接恢复原目录。 |
| `python3 scripts/workbench_store.py --root <project>` | 页面版本与任务唯一入口：`--state` 查页序、当前修订版与待办 `tasks`；`--command-json` 经 JSON stdin 提交 `get`、`checkout`、`save`（保护用户直改文字与坐标 `guards`，支持记录 `layout_id`）、`add_page`、`delete_page`、`order`、`task`、`resolve`。 |
| `python3 scripts/orchestrate/ppt_pipeline.py <project> <cmd>` | 无状态编排 CLI：`frames`（测图片槽位）、`check --summary`（渲染 PNG + 几何防线校验 + 文案对表）、`review [--surface-only]`（生成并打开/刷新 `Workbench`）、`export [--snapshot <path>]`（按需冻结快照并转 PPTX）、`template-select` / `template-review`。 |
| `python3 scripts/template/template_library.py` | 模板库管理：`list`、`apply <project> --template-id <id>`、`publish`、`refresh <template_id>`（直接修改包文件后重算 `manifest.json` 哈希与原语列表）、`verify`（全库完整性门禁）。配合 `extract_template_pack.py`、`scaffold_template_pack.py`、`apply_layout_selection.py`、`layout_index.py` 使用。 |
| `python3 scripts/resolve_video_vault.py --style <style_id>` | 解析视频风格包（优先挂载 `~/.config/planners/video-vault/styles/<style_id>/`，无私有库自动降级为 `default-clean`）。 |

---

## 1. 接收（`Intake & Resume`）

- **恢复或新建**：已有项目直接跑 `workbench_store.py --root <project> --state` 恢复当前页序、修订版与待办任务；新项目按输入源运行 `init_svg_project.py`（Bypage 衔接见 [02_content_stage.md](references/workflow/02_content_stage.md)）：
  - **Bypage 逐页稿**：现行 `planners-doc/2` 交付（`.planners/by-page.md` + `by-page.assets.json` + `fact-audit.json`）用 `--source <Project>/.planners/by-page.md --route slides` 初始化，整理正文、制作说明与登记图片进 `_internal/01_content/page_content.json`，沿用同一 `project-memory.md`、权威 `source-index.json` 与 `fact-audit.json`；旧版 `bypage-production/1` JSON 包用 `import_bypage.py`。
  - **直接材料**：按复杂度整理进 `page_content.json`，或多源研究时先委派 `planners-bypage`。
  - **视频关键帧**：有 `visual-plan.json` 用 `--assets` + `--plan` 初始化并保留 `screen_id`；仅有已定稿上屏稿用 `--source <上屏稿.md> --route video`（未定稿新片回 `video-idea-system`）。详见 [03_video_route.md](references/workflow/03_video_route.md)。
- **Completion Criterion**：来源与画幅可读，每页拥有稳定 `page_key` 与 `page_content.json` 记录，全部源图片已登记且零静默遗漏。

## 2. 定方向与模板（`Direction & Template`）

- **确认秩序与密度基调**：一次确认画幅与视觉来源（用户已指明则直接执行），将本次选择写入 `_internal/01_content/design_direction.md`。
- **角色分工（`Template Pack vs. Page Composition`）**：
  - **模板管皮肤与参考骨架**：已选 `Template Pack`（或视频风格 `page.md`）时，色彩、字体、容器形式（发丝线 vs. 卡片/色条）与现成原语（`primitives/*.svg`）100% 服从模板；
  - **页面构图力学管层级、双密度与原型**：开画前结合 [page_composition.md](references/domain/page_composition.md)，由模型按每页内容体量动态适配**高密咨询台账（`High-Density Consulting Ledger & Grid`）**或**低密聚光灯留白（`Low-Density Spotlight & Manifesto`）**，并按需选用 9 大拓扑原型。
- **选用、快提或入库模板**：见 [01_template_intake.md](references/workflow/01_template_intake.md)。开画前必须实际查看所选模板/风格的 `SPEC.md` 与样张（或 `extract_template_pack.py` 生成的 `contact_sheet.png`）。
- **Completion Criterion**：`design_direction.md` 已落盘，所选模板/风格的规范文档与参考样张已实际查看。

## 3. 工作台制作与审阅交付（`Workbench & Review` — 默认终点）

按 [04_svg_stage.md](references/workflow/04_svg_stage.md) 与 [svg_rules.md](references/domain/svg_rules.md)（幻灯片另读 [svg_to_ppt_rules.md](references/domain/svg_to_ppt_rules.md)）逐页制作、返修并交付工作台：

1. **Checkout → 编辑候选 → Save**：通过 `workbench_store.py` 执行 `checkout` 获取候选路径、基版与 `protected` 守卫（用户改过的文字与坐标几何均受保护，生成器重建整页时按 `human_edits_lost` 返回的 `guards` 原位保留），编辑候选 SVG 后 `save`（附 `author="model"`、`base_revision`，参考了版式时附 `layout_id`）。
2. **版式与反馈任务**：工作台提交的框选意见、整套模板（`template_id`）与逐页参考版式（`layout_id`）均作为 pending task 存入 Store。按参考版式组织该页（版式是起点而非死锁层，内容冲突时优先保住主张与证据，并在回执说明偏离），保存后调用 `resolve` 绑定结果 revision。
3. **Check → 多模态看图自检**：运行 `ppt_pipeline.py <project> check --pages ... --summary` 检查技术防线（切字、重叠、越界、未定义 CSS 变量、Emoji、文案对表），**直接打开渲染出的逐页 PNG 大图（`check` 返回的 `png` 路径，位于 `_internal/03_png_preview/pages/<page_key>.png`）目检阅读层级、换行与图片裁切**，有缺陷立即修候选重跑。
4. **打开审阅工作台并交给人看（默认停止点）**：按 [07_visual_review.md](references/workflow/07_visual_review.md) 打开或刷新工作台——DSH 环境跑 `ppt_pipeline.py <project> review --surface-only` 后交 `review_open` 挂入侧栏；非 DSH 跑 `ppt_pipeline.py <project> review` 启动 `planners-review-core` 本地宿主。**至此直接向用户交付工作台，停下等待审阅，禁止主动运行 `export`。**
   - *视频路线收尾*：若本任务为视频静态关键帧（`video`），保存、技术检查与看图通过后，直接按 Store `order` 交付 `get_page` 返回的已保存 SVG、关联素材与 `notes` 给 `video-craft`，同样无需运行 `export`。

- **Completion Criterion**：本轮所有变更均取得 Store 保存回执（非 `no_change`），`check` 零硬错误，已实际目检最新 PNG 大图，待办 `task_id` 已 `resolve`，且 `Workbench` 已打开或刷新（`video` 路线已交出 SVG 与素材清单）。

---

## 按需外发分支：导出可编辑 PPTX / 冻结快照（仅显式触发）

**仅当**用户在工作台点击导出（唤醒携带 `snapshot.path`）或明确指示导出 `.pptx` / 固定版本快照时执行（细节见 [project_contract.md](references/contracts/project_contract.md)）：

- 运行 `python3 scripts/orchestrate/ppt_pipeline.py <project> export [--snapshot <snapshot.json绝对路径>]`，产物写入 `_internal/06_ppt_output/<snapshot_id>/`（根目录 `final_deck.pptx` 为最新兼容副本）。
- 如实报告输出路径、技术转换报告与复核限制；导出后工作台继续保持可编辑。

---

## 协同能力与工程维护

- **同行 Skill 协同**：修改页面文案表达调 `slide-copy`；补充论证视角调 `planners-method-wiki`；页面改写改变了数字、主体、时间、单位或限定条件时，在交付前按 [02_content_stage.md](references/workflow/02_content_stage.md) 调用 `planners-fact-check` 复核受影响页。
- **架构与升级**：模块唯一主人、接口契约与测试门禁见 [references/architecture.md](references/architecture.md)。升级或维护本 Skill 时遵循 `planning-before-create-skill`，候选问题记入 [GOTCHAS.md](GOTCHAS.md)，正式变更记入 [references/maintenance-history.md](references/maintenance-history.md)。
