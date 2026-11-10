---
name: dyz-med-revision
description: >-
  修订已有医学稿件或逐条回应编辑和审稿人意见，覆盖语言、结构、科学表述、改投适配和拒稿后恢复，并保留
  可追溯的修改记录。当用户明确要求修改稿件、回复审稿意见或按新期刊重整时使用；先给修订计划，文字和
  格式修改可在授权范围内执行，涉及新数据、重分析、伦理、作者或其他源事实时必须先获得确认。
  Use for manuscript revision, response to reviewers and journal resubmission preparation.
---

# 医学稿件修订与审稿回复

## 入口边界

只做中英互译用 `dyz-med-translate`；只做语言自然化用 `dyz-med-deai`；用户尚不清楚稿件问题时先用
`dyz-med-manuscript-diagnose`。本 Skill 负责实施已明确的修订。

## 核心原则

1. 保留原稿，输出新版本或明确的修订副本。
2. 修改前先说明范围、受保护内容和需要确认的事实。
3. 不编造数据、分析、伦理、注册、作者贡献、审稿人要求或引用。
4. 不把审稿人建议自动视为正确；评估后可采纳、部分采纳或有理有据地不采纳。
5. 每项修改都能追溯到评论、诊断问题、期刊要求或用户目标。

## 工作流

### 1. 读取并结构化输入

读取稿件、决定信和审稿意见。保留原始编号与原文，按编辑、Reviewer 1、Reviewer 2 等来源拆分。对文档
解析不完整处记录页码/位置和警告。

### 2. 分类每条问题

使用：

- `editorial`：语言、结构、格式；
- `interpretive`：结论强度、解释、适用性；
- `methodological`：设计、模型、偏倚控制；
- `data_or_analysis`：需要新数据、重分析或新表图；
- `ethics_or_authorship`：伦理、注册、署名、利益冲突；
- `journal_adaptation`：目标期刊格式和定位。

标记是否可直接处理、需要作者确认或当前无法完成。

### 3. 先交付修订计划

计划至少包含：

- 修订模式和目标；
- 涉及与不涉及的章节；
- 受保护的数字、事实、引用和声明；
- 每条问题的处理策略；
- 需要的新材料或确认；
- 可能引入的风险；
- 输出版本和验证方式。

只有真正依赖源事实的事项才暂停；已授权的文字、结构和格式修订可继续执行。

### 4. 执行最小修改

按章节修改，避免无关重写。科学内容变化必须来自用户提供的结果或实际重新分析输出。引用新增前先核实来源；
引用编号和交叉引用在最终阶段统一更新。

### 5. 写逐条回复

每条审稿意见包含：

- 原始评论；
- 作者回应；
- 实际修改内容；
- 准确位置；
- 回应立场 `response_stance`：`ACCEPT`、`PARTIAL`、`DISAGREE_WITH_REASON` 或 `NEEDS_AUTHOR_INPUT`；
- 独立的问题处理状态：`open / in_progress / awaiting_verification / verified_closed`；
- 稳定问题 ID、`critical / major / minor` 严重度，以及关闭所需的检查与证据。

ACCEPT 表示采纳立场，不证明修改已完成；不同意且理由完整也不自动关闭问题。明确区分已回应、已实施和已验证关闭。
三条均已回复、仅一条完成验证时必须写“回复 3/3，已验证关闭 1/3”，其余两条保持实际未结状态。

语气专业、具体。不同意时解释方法学或证据理由，不攻击审稿人，也不声称做过未完成的分析。

### 6. 验证受影响内容

重新核对：

- 数字、表图和摘要一致性；
- 方法与新分析是否一致；
- 新增或改写论断的证据；
- 因果和临床应用边界；
- 目标期刊要求；
- 所有审稿意见是否有回应，所有回应是否有对应修改或理由。

按 R2 schema 1.1 将修订输入与产出登记为稳定 artifact ID、path、version、sha256；保留原稿与旧检查。
有 passport 时逐条读取相关记录，无 passport 时可用同形独立记录及明确项目根目录，不强制兄弟技能依赖。
复核记录用唯一 `checks[].id`、完整 `inputs`（artifact_id/version/sha256）、scope.domain/description、
execution_status、applicability、domain_result、report:{path,sha256}、checked_at。执行状态为
`not_run / blocked / failed / completed`，未完成时 domain_result=null；blocked/failed 需 reason。
适用性为 `applicable / not_applicable / unknown`，后两者需理由。先保存报告，再由独立记录引用哈希。
消费逐条验证输出的 `freshness: current / stale / unverified`，不能自行存储 current 代替核验。
校验器退出码 0 不是科学 PASS；current 也不保证范围充分或领域结论支持关闭。

只有 `verification_check_id` 指向 current、completed、applicable 的检查，且审阅其领域结论确实支持解决、
`evidence:{path,sha256}` 可定位关闭依据时，才可写 `verified_closed`。部分检查不能关闭未覆盖部分。
结果、稿件或相关依据变化使依赖检查失效，旧关闭不能继续计入当前有效关闭数，应报告需重核并保留历史。
纯排版变更也默认 stale；需沿用科学判断时另建当前输入绑定记录，附等价性和页码/定位重核依据，不改旧哈希。
仅核对受影响范围，不自动串联分析、全面审稿、导出或投稿。

外部审稿/处理前，记录内容类别、用途、具体服务与目的地、允许发送范围和当前人类授权；未知则不发送，
采用已确认本地处理或交付本地待审材料。按 R2 human_approvals 核对 targets 的版本/哈希、role、confirmed_at、
source（human、actor_id、statement、reference、locator）及实际授权权限；recorded_not_authenticated 不证明有效同意。
回执记实际发送字段/工件绑定、目的地、时间、执行状态、结果证据及限制；未发送如实写未发送，不复制敏感正文。
研究参与同意与患者发表同意分开；适用性不明交有资质人员复核，不把伦理批准或去标识化推定为发表豁免。

## 输出

默认生成：

- 版本化修订稿；
- `paper/revisions/revision-plan.md`；
- `paper/revisions/response-letter.md`；
- `paper/revisions/traceability-matrix.md`；
- `paper/revisions/open-items.md`；
- 简明变更摘要。

## 验收标准

- 原稿可恢复，修订范围清楚；
- 每条评论有独立的回应立场、处理状态、回应和位置（未修改时写理由，不捏造定位）；
- 所有数字和声明保持或有已确认来源；
- 未完成分析没有被写成已完成；
- 分别报告受影响章节的复核结果、范围与 freshness；未通过、未核实或待作者输入时只交付标明限制的修订草稿，不声称全部关闭。

## 配套资源

- [审稿意见回应表](templates/reviewer-response-table-template.md)
- [虚构修回示例](examples/worked-example-reviewer-response.md)
- [参考规范](references/references.md)
