---
name: dyz-med-submit
description: >-
  根据目标期刊当前要求准备医学论文投稿包，包括投稿信、题名页、作者贡献、利益冲突、数据可用性及其他
  指定附件。当用户要求准备投稿材料、cover letter 或投稿前清单时使用；默认只生成本地文件，绝不自动
  上传、发送、点击提交或创建外部数据仓库，任何外部提交动作都需要用户另行明确授权并最终确认。
  Use to prepare local cover letters and journal submission packages; external submission needs authorization.
---

# 医学论文投稿包准备

## 安全边界

本 Skill 的默认终点是“本地投稿包已准备并可供作者审阅”，不是“已投稿”。未经用户明确要求和最终确认，
不得登录投稿系统、上传文件、发送邮件、创建公开仓库或代表作者作出声明。

## 所需输入

- 已确认的目标期刊及当前作者须知；
- 最终或指定版本稿件和导出报告；
- 稿件编号（修回时）、文章类型和投稿语言；
- 作者姓名、单位、顺序、通讯信息和 ORCID（按需）；
- 每位作者确认的贡献、署名资格、终稿批准和责任承担；
- 伦理、注册、资助、利益冲突、数据/代码可用性；
- 实际使用的 AI 工具、版本、用途和作者复核方式；
- 期刊要求的声明、表单和附加文件。

缺少行政或事实信息时，可以生成带清晰待填项的内部草稿，但不能称为可直接提交版本。

## 工作流

### 1. 核实期刊材料清单

从期刊官方当前要求建立清单：主稿、匿名稿、题名页、投稿信、亮点、图表、补充材料、报告规范清单、伦理/
注册文件、利益冲突表、作者贡献、数据声明等。不要预设固定“六份”或“七份”文件。

### 2. 准备投稿信

投稿信应简洁说明：

- 稿件标题与文章类型；
- 研究问题、主要发现和对该期刊读者的价值；
- 原创性、非一稿多投和全体作者批准（仅在作者已确认时）；
- 期刊要求的伦理、注册、利益冲突或 AI 使用说明；
- 通讯作者信息。

不夸大新颖性，不写无法证明的“首次”，不虚构编辑姓名或稿件历史。

### 3. 核对作者与贡献

依据目标期刊和适用的 ICMJE/CRediT 要求整理贡献。工具只能发现信息缺口，不能替作者决定署名资格、顺序或
贡献。每位作者的终稿批准和责任承担必须由人类确认。

### 4. 生成真实声明

- 利益冲突：区分“已确认无”与“尚未询问”；
- 数据可用性：按实际隐私、伦理、协议和仓库状态描述；
- 资助：如实说明资助方角色；
- AI 使用：仅依据实际使用，按目标期刊当前政策确定位置和措辞；
- 伦理与注册：复制已核实信息，不补造编号或日期；
- 同意：研究参与知情同意、患者发表同意分别记录。有资质的伦理/临床人员需结合病例、可识别叙述/影像及
  期刊要求判断发表同意适用性；不把参与同意、伦理批准或去标识化自动当作发表同意或豁免。缺来源或适用性
  未知时标为待专业复核，不自行填写“已获同意”“不适用”或“已豁免”。

“合理请求后提供”在某些受限数据场景可能是诚实表述；应补充实际访问条件，而不是强迫公开。

### 5. 生成并核对本地文件

按期刊清单生成所需格式。逐份检查占位符、姓名顺序、单位映射、字数、图表数量、稿件版本和声明一致性。
需要签字、盖章或在线表单的项目标为人工步骤。

### 6. 提交就绪评估

必须分三栏输出，不合并为一个含混的 ready：

1. `package_completeness`：`complete / incomplete / unknown`，仅表示当前期刊清单下文件和行政材料齐备性。
2. `scientific_review`：逐条列相关 check ID、scope、execution_status、applicability、原始 domain_result、
   freshness 和限制，并报告 `supported_for_declared_scope / not_ready / unverified`，不冒充医学认证。
3. `external_authorization`：按目的地/动作分别列 `not_confirmed / confirmed / declined`、当前有效性、范围与
   人类来源；本地包完成不授予登录、转换、上传、发送、公开或最终提交权限。

本地候选包另可给 `readiness: ready / ready_with_manual_steps / not_ready`，但该标签不是执行授权：
仅在必需材料齐全、源事实确认、所需科学检查对当前相关版本有效且范围足够、无 critical/major 未结问题时
才可 ready；只剩已列明的机械性签署/在线步骤可为 ready_with_manual_steps。未确认作者/伦理事实/利益冲突/
声明、当前 REJECT 或 REVISE、重大问题未结、缺检查或 stale/unverified/未执行/范围有限，都不能无保留 ready；
缺乏判断依据写 unverified 并将 readiness 记 not_ready。不得选取另一个 PASS 掩盖仍有效的相反意见。
仍可在用户请求范围内准备显著标记“内部审阅包／非提交终版”的本地草稿，列明限制，不强制自动重跑所有技能。

按 R2 schema 1.1 消费 artifacts 的稳定 ID/path/version/sha256 和检查的完整相关 inputs
（artifact_id/version/sha256）、scope.domain/description、execution_status、applicability、domain_result、
report:{path,sha256}、checked_at；逐条使用验证输出的 `freshness: current / stale / unverified`，不接受
存储的 current 自证。current 不等于 PASS；校验器退出码 0 即使对应 REJECT 也合法，不作为科学门禁。
仅相关记录影响本次决策，无 passport 可用同形独立记录及明确根目录，不强制兄弟技能依赖。
输入版本或字节改变使依赖记录 stale；排版变更要沿用科学判断也需新建当前绑定记录，附内容等价性和定位重核
依据，不能改旧哈希。open_items 的 severity 为 critical/major/minor；status 为
open/in_progress/awaiting_verification/verified_closed。关闭计数必须核实 verification_check_id 指向
current、completed、applicable 的检查，其领域结论支持关闭且 evidence:{path,sha256} 可追溯；
回复覆盖数与验证关闭数分列，不能用“已全部回应”消除重大未结风险。

### 7. 外部动作前的授权与回执

任何外部转换、审稿或提交前，先记录内容类别、用途、具体服务/接收方与目的地、允许发送的字段/文件/范围和
当前人类授权；目的地、范围或权限未知即不发送，采用已确认本地路径或本地草稿。已连接工具、本地导出授权、
材料齐备或科学 PASS 均不是外传许可，审阅草稿也不例外。
按 R2 human_approvals 核对 state、targets 的 artifact_id/version/sha256、role、confirmed_at 及
source（human、actor_id、statement、reference、locator），人工核实角色权限、动作及当前请求；
recorded_not_authenticated 不能证明身份或有效同意。内容/用途/目的地/范围改变必须重新确认。
上传/发送与最终提交分开授权；最终提交前再次让用户确认实际文件清单、版本与声明，未授权的动作不得执行。
回执记录预检时间、授权来源/范围、实际发送字段/工件绑定、目的地、动作时间、执行状态、返回证据和限制；
未执行写未发送/未提交，不捏造回执，不在日志复制患者内容、敏感正文或凭据。

## 输出

默认保存到 `paper/submissions/package/`：

- 期刊要求的本地附件；
- `submission-checklist.md`；
- `submission-readiness.md`；
- `manual-actions.md`；
- `package-manifest.yaml`。

## 验收标准

- 文件清单来自期刊当前要求；
- 作者、伦理、注册、利益冲突、数据和 AI 使用信息均有真实来源；
- 无未标注占位符；
- 所有人工签署/盖章/在线步骤明确；
- 没有执行任何未经授权的外部提交动作。

## 配套资源

- [投稿前检查清单](templates/投稿前检查清单.md)
- [虚构投稿包示例](examples/虚构课题投稿材料生成示例.md)
- [作者与投稿规范](references/投稿与作者身份相关规范清单.md)
