---
name: dyz-med-review
description: >-
  对接近投稿状态的医学稿件做五个视角的模拟审稿：证据、方法统计、伦理合规、临床领域与期刊编辑，并汇总
  为定位明确的 PASS、REVISE 或 REJECT 建议。当用户要求投稿前全面把关、模拟同行评议或评估拒稿风险时
  使用；这是决策支持，不是真实同行评议，也不会自动修改、导出或投稿。
  Use for simulated pre-submission peer review and located revision recommendations.
---

# 医学论文多视角模拟审稿

## 使用前说明

模拟审稿不能替代真实领域专家、统计师、伦理审查或期刊编辑。报告必须注明实际审阅范围、稿件版本、使用的
模型/运行方式以及局限。

默认按五个视角审阅，不虚构五位审稿人。同一模型逐视角审阅必须标注 `single-model multi-lens review`。
若实际使用多个上下文或模型，记录真实模型、上下文共享、先前意见可见性与运行限制；新开对话本身不保证
意见独立性，跨模型也不等于独立专家。补充首轮/续审仅在用户要求及环境允许时执行，不是导出的强制前提。

## 所需输入

- 完整稿件及表图、补充材料和参考文献；
- 研究方案、注册记录、结构化结果和分析说明；
- 论断—证据矩阵与报告规范核对结果（如已有）；
- 目标期刊当前作者须知；
- 审阅范围和稿件版本。

缺少某类材料时仍可审阅可见部分，但对应视角不得给出无保留 PASS。

## 五个审阅视角

### 1. 证据

核对核心论断、引用匹配、知识缺口、矛盾证据、摘要与正文一致性。区分已验证、部分支持和无法核实。

### 2. 方法与统计

核对设计与问题、样本来源、结局定义、偏倚控制、模型、协变量、缺失数据、效应量与不确定性、亚组和敏感性
分析。需要正式偏倚评估工具时，选择适合研究类型的工具，不混用。

### 3. 伦理与透明度

核对适用的伦理审批、知情同意、注册、方案偏离、利益冲突、资助者角色、作者贡献、数据共享和实际 AI 使用
披露。研究参与知情同意与患者发表同意分别核对；病例、可识别叙述或影像等的发表同意适用性需由有资质的
伦理/临床人员结合期刊要求复核。参与同意、伦理批准、去标识化都不能自动证明发表同意已取得或可豁免。
无法确认时标为待专业复核，不编造批准、同意或豁免。

### 4. 临床/领域

评估临床问题的重要性、结局相关性、生物学合理性、适用人群、替代解释和结论是否改变实践。不能访问领域
专门知识或全文证据时，降低判断强度。

### 5. 期刊编辑

评估稿件定位、结构、标题摘要、篇幅、图表经济性、期刊范围和明显退修/拒稿风险。期刊政策必须基于当前官方
说明，不能使用过时记忆。

## 每个视角的报告格式

每条意见包含：

- 稳定问题 ID、严重程度：`critical`、`major` 或 `minor`；非阻断建议另作备注，不新增严重度枚举；
- 稿件位置；
- 观察到的问题；
- 为什么重要；
- 最小可行修复；
- 需要作者确认的事实；
- 建议结论：`PASS`、`REVISE` 或 `REJECT`。

`REJECT` 只表示当前版本存在可能无法通过局部修订解决的根本问题，并非真实期刊决定。

## 汇总规则

1. 合并重复意见，但保留不同视角的理由。
2. 事实和数值冲突优先于风格问题。
3. 不用平均分掩盖单个关键风险。
4. 总体结论由最严重、证据最充分的问题决定，并列出达到下一状态的条件。
5. 只提供修订路线；用户要求后才交给 `dyz-med-revision` 执行。

## 版本绑定与交接

消费 R2 schema 1.1 工件合同：输入按稳定 `artifact_id/version/sha256` 绑定，路径相对于明确项目根目录；
有 passport 时使用其中的 `artifacts`，无 passport 时可交付同形独立记录，不强制安装或调用其他技能。
每次审阅新建唯一 `checks[].id`，记录完整相关 `inputs`、`scope.domain/description`、
`execution_status`、`applicability`、`domain_result`、`report:{path,sha256}` 和 `checked_at`。
执行状态为 `not_run / blocked / failed / completed`；适用性为 `applicable / not_applicable / unknown`，
后两者需理由。已完成的模拟审稿用 `domain_result:{namespace: mock_review, value: PASS|REVISE|REJECT}`；
未完成时领域结论为 null，blocked/failed 记 reason。先保存报告，再在独立记录中引用报告哈希，不自哈希。

逐条消费验证输出的 `freshness: current / stale / unverified`，不写入自称 current 的证据。current 只证明
声明的绑定可核对；校验器退出码 0 也可对应 REJECT，绝不转换成科学 PASS。按本次相关记录判断，不用总退出码
触发全流程。输入版本/字节变化使依赖检查 stale；缺材料、缺绑定、范围有限或未核实检查不能证明全文通过。
纯排版也默认使旧绑定失效；沿用科学判断须新建当前绑定记录，附内容等价性和定位重核依据，保留旧记录。
问题按 `open_items` 记录 `id/severity/status`；处理状态为 `open / in_progress / awaiting_verification / verified_closed`，
回应立场不作关闭证据。关闭须关联 `verification_check_id` 和 `evidence:{path,sha256}`，核对该检查 current、
completed、applicable 且其实际领域结论支持关闭；当前 REJECT 或重大未结问题必须传给下游。

## 外部审阅预检

外部服务或远程模型收到内容前，逐项记录内容类别（公开题录、未发表稿件、作者身份、患者相关内容等）、用途、
服务/接收方与目的地、允许发送的字段/文件/范围及当前人类授权。工具已连接、只要求审稿或已获本地导出授权
都不等于外传许可；目的地、范围或授权未知时不发送，改用已确认本地路径或仅交付本地审阅材料。
批准使用 R2 `human_approvals`：核对 state、targets 的 artifact_id/version/sha256、role、confirmed_at 和
source 的 human/actor_id/statement/reference/locator；结合当前请求与授权者权限人工核实，
`recorded_not_authenticated` 不能当身份或合法性证明。内容/用途/目的地/范围改变必须重新确认。
回执记录预检时间、上述最小授权信息、批准来源、实际发送字段/工件绑定、接收方、时间、执行状态、返回证据与限制；
无授权时写实际未发送及本地降级，不把期望输出写成结果，不在日志复制敏感正文或凭据。授权也不能豁免患者隐私复核。

## 输出

默认写入（沿用用户已有路径，登记实际工件，不推断文件名即身份）：

- `paper/review/01-evidence.md`
- `paper/review/02-methods-statistics.md`
- `paper/review/03-ethics-transparency.md`
- `paper/review/04-domain.md`
- `paper/review/05-journal-editor.md`
- `paper/review/00-aggregate-report.md`

如果只做单一模型审阅，所有文件和汇总页都应带同一运行方式标记。

## 验收标准

- 五个视角均有范围、证据和具体定位；
- 没有把单模型角色扮演描述为独立专家；
- 高优先级意见可操作且不要求编造新数据；
- 未改动稿件；
- 总体结论与最严重问题一致，限制清楚。

## 配套资源

- [模拟审稿记录模板](templates/mock-review-record.md)
- [虚构汇总示例](examples/worked-example-review-council.md)
- [补充审稿提示模板](templates/reviewer/)
- [参考规范](references/references.md)
