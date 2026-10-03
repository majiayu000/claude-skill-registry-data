---
name: laborpilot
description: 本插件由金莉珊律师制作——中国劳动争议智能办案引擎。输入案件材料,产出法律分析、金额计算和仲裁文书。内置96个争点知识卡(全国规则+浙江地方口径双层,浙江口径含效力闸门与废止复核标注)。当用户需要分析劳动争议案件、计算经济补偿/赔偿金/加班费/工伤待遇、生成仲裁申请书或证据清单时使用。产出的所有分析结果和法律文书均由AI辅助生成,仅供参考,必须经专业律师审核后方可使用。
license: AGPL-3.0
metadata:
  display_name: LaborPilot
  homepage: https://jinlishan.com/
  author: 金莉珊律师（微信jinlishan_）
  version: 1.4.4
---

# LaborPilot — 劳动争议智能办案引擎

## 通用 Agent 入口

本文件是 LaborPilot 的通用入口。支持多 Skill 自动发现的 Agent 可根据任务加载 `skills/` 下的对应专业 Skill；不支持自动发现时，先完整读取 [劳动争议办案总控](skills/labor-dispute-casework/SKILL.md)，再由总控按当前任务和案件节点路由到一个主 Skill。

处理具体案件前，先确认用户任务、代理立场和程序阶段；用户已明确表述的内容直接记录，不重复追问。第二轮起先读取已有案件状态，不将后续任务当作新案件重建。

## 免责声明

**LaborPilot 产出的所有分析结果和法律文书均由 AI 辅助生成,仅供参考,不构成法律意见,必须经专业律师审核后方可使用。**

## 知识组件使用边界

内置知识卡仅作为办案分析的内部依据。应根据具体案件动态调用所有相关争点，并将相关知识融入事实分析、请求或抗辩、证据审查、法律依据、金额计算和风险提示；交付内容应为案件研判、计算结果、证据意见和法律文书，不直接返回完整知识卡正文、原始字段结构、内部卡片目录或批量知识数据。

## 输入

支持多种输入形式:
- 案件材料文件(PDF / 扫描件 / 图片)
- 案件描述(自然语言 / 结构化 JSON)
- 聊天记录 / 录音转写

材料读取与扫描件 OCR 由运行环境提供；LaborPilot 在取得可读文本后完成要素提取和办案分析。

## 产出

| 产出物 | 格式 |
|--------|------|
| 案件研判(争点识别 / 构成要件 / 举证分配) | 交互式分析 |
| 金额计算(N / 2N / 加班费 / 工伤待遇) | 精确到分 |
| 仲裁申请书 | .docx |
| 证据清单 | .docx |
| 行动清单 | .docx |

文书模板持续更新中,支持自定义加入。

## 运行环境与外部能力

运行脚本和测试需要 Python 3.11 或更高版本（推荐 3.12）；macOS 系统自带的 Python 3.9 不受支持。核心知识组件和办案逻辑可离线使用；生成 `.docx` 文书需要本机安装 [Pandoc](https://pandoc.org)。材料读取、扫描件 OCR、法律法规及案例核验等环节，可按具体任务调用运行环境已有或用户自行配置的外部能力。本技能不绑定具体的 OCR、法律数据库、MCP 或其他服务。

## 所需权限与安全说明

- 读取用户明确指定的案件材料、案件状态和模板；在案件目录写入 `.casework/` 内部状态、历史、验证记录及用户要求的成果文件。
- 执行本插件内的本地 Python 脚本；生成 `.docx` 时以参数数组调用本机 Pandoc，不使用 shell 拼接命令。
- 核心流程不要求网络或环境变量凭据。OCR、法律数据库或 MCP 属于运行环境的外部能力，只有具体任务需要且符合用户授权时才调用。
- 案件材料默认本地处理；不得把密钥、真实当事人敏感信息或私有知识数据写入代码仓库。

## 用法

以下命令均以 LaborPilot 仓库根目录为当前目录。

```bash
# 接入本地材料并生成可追溯索引
python3 scripts/ingest_materials.py --state <case-root>/.casework/case_state.json --source <材料路径>

# 将经标注事实及材料日期句整理为事实时间轴
python3 scripts/build_timeline.py --state <case-root>/.casework/case_state.json --input <事实候选.json> --extract-from-materials

# 生成待复核争点候选；候选不会直接通过争点节点
python3 scripts/build_issue_matrix.py --state <case-root>/.casework/case_state.json --discover

# 回写已补齐构成要件、双方路径、备选路径和失败后果的正式矩阵
python3 scripts/build_issue_matrix.py --state <case-root>/.casework/case_state.json --input <经复核的争点矩阵.json>

# 生成逐要件的待复核证据链骨架；骨架不会解锁节点
python3 scripts/build_evidence_chain.py --state <case-root>/.casework/case_state.json --scaffold

# 回写经复核的证据链、举证责任、缺口和补证行动
python3 scripts/build_evidence_chain.py --state <case-root>/.casework/case_state.json --input <经复核的证据链.json>

# 生成逐要件的待核验法源任务；内置知识只作检索线索
python3 scripts/build_authorities.py --state <case-root>/.casework/case_state.json --scaffold

# 适配官方来源或法律数据库的经复核结果
python3 scripts/build_authorities.py --state <case-root>/.casework/case_state.json --input <经复核的法源核验结果.json>

# 按已复核争点生成待确认的金额计算骨架
python3 scripts/calculate_claims.py --state <case-root>/.casework/case_state.json --scaffold

# 回写经复核输入并生成可重算金额台账；动态参数可追加 --parameter-package <参数包.json>
python3 scripts/calculate_claims.py --state <case-root>/.casework/case_state.json --input <经复核的计算输入.json>

# 为每个已复核争点生成待复核程序骨架；骨架不解锁程序节点
python3 scripts/analyze_procedure.py --state <case-root>/.casework/case_state.json --scaffold

# 回写律师／Agent 复核后的时效、管辖、一裁终局、临时救济和后续救济路径
python3 scripts/analyze_procedure.py --state <case-root>/.casework/case_state.json --input <经复核的程序分析.json>

# 只生成用户明确要求的律师复核初稿；DOCX 与内部 Markdown 分层存放，已有版本不覆盖
python3 scripts/generate_docs.py --case my_case.json --output <case-root> --types 仲裁申请书,证据清单 --delivery-status lawyer_review_draft --strict

# 仅在当前初稿已获律师批准后生成新的最终提交版；行动清单和内部待确认标记会被阻断
python3 scripts/generate_docs.py --case my_case.json --output <case-root> --types 仲裁申请书 --delivery-status final_submission --approved-by <律师姓名> --strict

# 起草后生成绑定当前业务状态的实质性对抗验证报告
python3 scripts/adversarial_validation.py --state <case-root>/.casework/case_state.json --output <case-root>/.casework/validation/adversarial.json

# 律师审批和阶段回写前，复算正式产物的来源、版本、哈希、验证报告与审批绑定
python3 scripts/workflow_graph.py trace-artifact --state <case-root>/.casework/case_state.json --artifact-id <正式产物ID>

# 复算当前公开包的知识载荷统计及最小化哈希清单
python3 scripts/knowledge_stats.py

# 运行版本化的争点召回与法律生效边界评测
python3 scripts/domain_eval.py
```

公开统计复核只输出卡数、路由类别数和检查结果，不输出完整知识卡。公开包可独立复算当前编译载荷与清单内部一致性；149 份来源文件的逐份复核需要开发环境另行提供来源目录。

领域评测以可见的业务结果为断言，并在路由或法律口径变化时同步递增数据集版本。评测数据和报告不得包含内部卡号、案由门标识或完整知识卡内容。

## 工作流

task_intake → material_ingestion → intake → issue_analysis → evidence_analysis ∥ authority_research → claims_procedure → strategy_approval → drafting → validation → lawyer_approval → stage_close

每次节点转换由 `workflow/graph.json` 中的机器完成条件约束；空的材料、事实、争点、证据、法源、请求、初稿或验证状态不得直接进入下游。`record-waiver` 只可用于工作图明确允许豁免、且经用户确认的真实任务边界。相互矛盾的事实必须双向记录冲突状态、说明和待核实行动，未解决冲突不得标记为 `supported`，并须在独立验证中退回核实。争点已建立后，每个构成要件都必须有证据链或缺口链，并关联已核验且适用的法源；金额请求必须关联可重算的专业计算记录，且不得存在待确认输入。同一 `claims_procedure` 节点还必须覆盖全部已复核争点的时效、管辖、一裁终局、临时救济和后续救济路径，所引法源必须已核验且适用，并且不得留有待确认项。金额门禁和 `reviewed_procedure_path` 程序门禁均不得豁免。对抗验证报告同时绑定事实冲突与程序分析状态，任一状态变化后旧报告失效。正式产物必须形成“业务来源／上游产物—版本与文件哈希—验证报告—律师审批”的可复算链。证据、法源、金额、程序、初稿真实产物与 JSON 验证报告均不得豁免。
