---
name: light-consistency
description: 统一风格与一致性维护。在论文、PPT、图表、代码、项目文档之间保持术语一致、视觉风格一致、逻辑线索一致、创新点表述一致（常驻，所有任务后台生效）。避免同一项目在不同材料中出现说法不一致、指标名称不统一、图表风格混乱、创新点前后矛盾、方法名称变化、数据集名称不统一、论文与 PPT 逻辑不一致、软著与系统功能不一致。
user-invocable: false
---

# 跨材料一致性维护

## 工作方式（常驻）
在任何产出材料的任务中后台运行：每生成或修改一份材料，比对项目库 db09 的"统一定义"，发现偏差即纠正或提示。

## 单一事实源：项目术语与定义表（存 db09）
借鉴 content-strategy 的"先定义后生产"：所有材料从一份定义文件派生，禁止下游各写各的。

**事实源的两种形态（同一份真相，机读 ⊃ 人读）：**
- **人读真相（每个项目必有）**：`databases/db09-projects/projects/<项目>/terminology.md`——Markdown 术语表（类别/标准叫法/缩写/英文/备注），由 a02 维护，是 db09 项目卡固定组成。审计脚本读它做**覆盖缺口**检测。
- **机读增强（需严格校验时再生成）**：三份 YAML schema 模板（`assets/` 的 `db09_glossary.yaml`/`db09_method_lock.yaml`/`db09_metric_registry.yaml`），比 Markdown 多 `forbidden`/`confusable`/权威数值列，支撑受控术语替换与指标数值冲突检测；扩写后存回项目 db09 目录（与 terminology.md 并列）。字段清单见文件清单节。

> `assets/` 三份是空白模板；真实项目事实源永远落在 `databases/db09-projects/projects/<项目>/`，避免"db09 指两个地方"。

维护要点（锁定口径，配合下方「一致性检查维度」五维）：方法/数据集名称含缩写列入"禁改清单"（润色/翻译不得替换）；指标统一符号+单位+定义（F1 vs F-score）；3 条创新点标准措辞跨论文/PPT/软著/竞赛一字对齐；关键术语锁中英对照+大小写连字符（fine-tune 不写 finetune）；**视觉规范**：项目有 `databases/db09-projects/projects/<项目>/palette.json`（论文图 m11/PPT m16/前端 a05 共读的视觉 SSOT 实例）则"跨材料配色一致"直接**对照该文件逐项核**——四方取色须同源、谁都不另起色板；无 palette.json 时退回 db05 `design_tokens.template.json`（DTCG 色值锚点真相源），论文图(db07)/PPT(db06)/前端(db05)/海报同取一份值（**当前人工/清单对照，非脚本自动核**）。
- **变更广播**：定义一旦修改，立即触发对**所有已产出材料**的回扫，避免下游过期。"已产出材料"的权威清单 = orchestrator 维护的 `.light/passport.yaml` 各阶段 `artifacts:` 路径并集（§4 产物台账）；无 passport 的轻项目退回 db09 的 `version_history.md` 列出的产物。回扫即对这份清单逐项跑下方 `consistency_audit.py`，命中即按"现状→问题→建议"修。

## 审计脚本：consistency_audit.py
`scripts/consistency_audit.py` 读取上述 db09 三件套，扫描一组材料文本，自动检测并**定位到 `材料:行号`** 的六类不一致，按 ERROR/WARN/INFO 分级，每条带"现状→问题→建议"，报告末尾做"条数自检"。

六类检测：
- `SUBSTITUTION` 受控术语/方法名被同义改写或写错(大小写/连字符/近义词)。`forbidden` 项支持 `{text:.., placeholder: true}` 标记说明性占位（语义需人工判断，审计跳过，不再 literal 误命中）。
- `METRIC_NAME` 同一指标被换名(如把 F1 写成"准确率")。
- `METRIC_VALUE` 同一指标(同方法×数据集)跨材料数值不一致，或与 db09 权威值不符；位置感知，一行并列多指标/多方法也能就近配对，不串位；命名实体内嵌数字(YOLOv8 的 8、CrowdScene-2k 的 2)挖空不误读；`%` 指标分数/百分数(0.876↔87.6)自动归一化。
- `GROSS_MISMATCH` 数值偏差落在"超精度容差但仍同量级"区间(相对偏差 30%~300%)，单列严重错填告警，**不再静默丢弃**(取代旧 `>0.30 continue`)。
- `CONTRIBUTION_DRIFT` 创新点/贡献提法漂移：以 db09 `创新点N` 行(terminology.md，只读)为标准措辞，跨材料用 token 覆盖+句级相似度检测"同一贡献在 PPT/软著提法偏离"。
- `COVERAGE_GAP` 规范术语/指标只在部分材料出现，应出现处缺席。`must_cover: true`(贡献级)缺席报 WARN，普通术语降 INFO 降噪。

用法（在 `skills/light-consistency/` 下）：真实审计 `python scripts/consistency_audit.py --db09 assets --materials <文件...> [--json out.json]`；无参跑内置合成材料自测（六类检测全触发 + X-1/2/4/5 专项断言）。退出码：发现 ERROR 返回 1（可接 CI），否则 0。端到端实例见 `examples/worked_example.md`。

## 一致性审计流程（inventory → tag → gap → fix）
借内容审计四步法：① **盘点** 逐份材料抽关键主张（方法名/指标名+数值/创新点措辞/图表风格）成清单；② **打标** 每项标 一致/冲突/缺失，冲突指向具体位置(章节/页/行)；③ **差距** 量化覆盖率（哪些贡献点 PPT 缺席、哪个指标只在论文）；④ **修正** 每条给"现状→问题→统一建议→修正后文本"。**完整性强制**：逐条列全不用省略号，报告末尾自检"清单条数=实际处理条数"。

## 一致性检查维度（五维 + 逻辑线索）
①**术语**同一概念全程同一叫法；②**指标**名称/定义/数值各处相同(论文表=PPT 图=摘要数字)；③**创新点**摘要/引言/结论/PPT/申报书表述不矛盾；④**方法/数据集名称**不中途改名；⑤**视觉**论文图/PPT/前端/海报共用设计语言（**人工/清单对照**：项目有 `databases/db09-projects/projects/<项目>/palette.json` 则对照它逐项核四方取色是否同源，无则依 db05 `design_tokens.template.json` 核；脚本只核文本类，视觉靠 `assets/design_language_extract.template.md` 人工签字）；⑥**逻辑线索**论文叙事与 PPT 叙事、软著功能与系统实现对得上；⑦**B-fact 快照新鲜度**db09 卡内引用的 venue 计量/数据集许可/DOI 等带 `[snapshot…src=…]` 三件套快照,对照 source_pointer 核是否超期(计量 >90 天/许可 >365 天)——从 palette.json 推广到所有 db09 B-fact 引用,超期标 WARN 提示重核(`consistency_audit.py` 的 METRIC_VALUE 检测可顺带标记)。

## 触发检查的场景
论文↔PPT、论文↔软著、系统↔软著功能说明、多版本图表、竞赛材料↔论文、代码命名↔论文符号。

## 产出
一致性检查报告（不一致清单 + 统一建议 + 修正后文本/配置）+ 更新后的术语表(db09)。

## 工具视角（具体用法）
- **内容层**：distill/polish 改写最易制造不一致（受控术语换近义词、F1→准确率）——把 db09 受控词表当"禁改清单"传入，改完必过术语表回扫；audit/critique 走"分维度+具体证据"三段式（现状→问题→建议）。
- **风格层**：extract-design-system 从现有论文图/PPT/前端反推设计语言，走 `assets/design_language_extract.template.md` 的"采样→抽取→⚠人工签字"流程产视觉规范卡（截图取色受压缩影响，标 ⚠ 项须人工签字方可作 SSOT）；确认值写入 db05 `design_tokens.template.json`。
- 各工具（W3C DTCG Design Tokens、Style Dictionary v4、Prettier、EditorConfig、Mermaid）的真实配置项/命令/坑见 `references.md`。

## 衔接
服务 m07/m08/m09/m11/m15/m16/m17/a05；定义存 db09 并被所有技能读取。

## 文件清单
- `assets/db09_glossary.yaml` / `db09_method_lock.yaml` / `db09_metric_registry.yaml`：db09 单一事实源 schema 模板。
- `assets/design_language_extract.template.md`：视觉设计语言抽取模板(采样清单+原子属性抽取表+⚠人工确认核对栏+视觉规范卡)，配套 db05 的 `design_tokens.template.json`(DTCG 视觉 SSOT)。
- `scripts/consistency_audit.py`：跨材料一致性审计器(六类检测+定位+修正建议+JSON 导出+自测)。
- `examples/worked_example.md`：论文 vs PPT 指标名/数值冲突的端到端实例(定位→统一→修正→回归)。
- `examples/materials_paper.txt` / `materials_ppt.txt`：配套可运行材料。

---
工具实现细节、真实配置项与端点见 `references.md`（逐工具核查笔记）。
