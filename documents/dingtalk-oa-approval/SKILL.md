---
name: dingtalk-oa-approval
description: 钉钉 OA 审批审阅与提醒工作流。凡是用户提到钉钉审批、OA、待审批、同意/拒绝/退回、录用、离职、请假、出差、外出、财务付款、报销、合同、晋升、立项特批，或让你定时检查新审批/超过 3 天审批，都必须使用本 skill。它要求先完整读取审批详情、流水、附言、附件、链接文档、PDF、面试记录、试用期考核标准等材料，再给出审批决策和附言；DWS 优先，DWS 读不到全文时按用户授权打开钉钉界面补读。
---

# DingTalk OA Approval Review

这个 skill 用于帮助当前授权审批人审阅钉钉 OA 审批。目标不是快速给结论，而是先把审批材料读完整，再根据定时任务 prompt 或其引用的本公司规则给出可执行意见。

## 与其他 DingTalk skills 的边界

不要把本 skill 合并进其他 DingTalk skill。它们负责不同业务，合并后会让触发范围过宽，容易在审批、文档、听记和知识库清理之间误用工具。

- `dws doc` / `dws wiki`：负责钉钉文档/知识库的创建、读取、写入、成员权限等文档与知识库操作。
- `dingtalk-browser-export`：负责从已登录 Chrome 导出当前 DingTalk/Alidocs 文档为 Word、PDF 或 Markdown。
- `dingtalk-knowledge-organize`：负责知识库盘点、分类、移动、重命名和 CSV 审批式整理。
- `dingtalk-minutes-access-request`：只负责钉钉 AI 听记权限申请、权限页复查和阻塞诊断；听记读取走 `dws minutes`。

- `stardust-oa-finance-review`：**只管它登记的 11 个财务模板**（按 `processCode` 精确匹配，见该 Skill 的 `references/template-registry.md`）。审批的 `processCode` 在它的登记表里，才按它的规则卡处理；**不在登记表里，那个 Skill 对这条审批完全不适用**，应选择对应的业务 Skill，按该 Skill 中的规则评估 `rule_coverage`。"没有规则卡"只对登记过的财务模板有意义，**不能作为其他审批类型请示 Derek 的理由**——2026-09-22 起一条 POC 立项评估和一条其他合同审批都因此被误停在 `needs_human`，而它们本来就不该有财务规则卡。
- `stardust-oa-project-review`：项目立项、第一曲线、POC/新机会及项目特批；读取该 Skill 指定的公司项目制度。它不覆盖合同签约权或财务模板审批。
- `stardust-oa-contract-review`：合同及其他对外有约束力承诺的审批；必须读合同正文。它不授予签约权，也不替代匹配的财务/项目审阅。
- `stardust-oa-people-review`：录用、离职、晋升。各类型规则与未决缺口互不通用；材料之间的矛盾（例如面试不推荐却已发 offer）由提交人解释，按决策表第 6 行退回，不转 `needs_human`。
- `stardust-oa-attendance-travel-review`：请假、出差、外出。三类规则不得互相借用；若该 Skill 未定义当前分支的适用边界，或它明确要求的外部规则来源无法取得，`rule_coverage` 不得为 `1.0`。
- `stardust-oa-cloud-resource-review`：云资源费用、服务器与计算硬件使用审批；按已批准资源方案核对本次变更。

分类可重叠：例如项目合同应同时读项目与合同 Skill；付款如精确匹配财务 registry，还需财务 Skill。非财务审批不需要在财务 Skill 中有模板行；应按 live process identity 选择其业务 Skill。业务 Skill 给出检查项不等于该类别已 100% 覆盖；只有本单所属业务 Skill 已定义覆盖本案适用分支的判断标准，并已逐条按实际材料核对，才允许 `rule_coverage = 1.0`。申请是否达到标准是审批结论，不影响该标准本身是否完整，因此未达标准但规则完整时仍可 `rc = 1.0`。**动作映射就是本 Skill 的完整决策表**，业务 Skill 不需要、也不应单独再写一份；某类别没有自己的动作清单，不是规则缺口。规则只在各 Skill 里，不读 `钉钉审批审阅原则.md` 之类的参考文档。

- **资金调拨申请单：一律 `needs_human`**（Derek, 2026-09-23）。照常读完材料，给出摘要、风险和建议，但**不执行同意、退回、拒绝或评论**，交给 Derek 决定。这是明确规则，不是规则缺口，以后补规则时也不要把它纳入自动处理。

审批内如果出现钉钉文档、Alidocs、知识库文件或 AI 听记链接，可以按材料类型临时调用对应能力读取材料；但审批判断、审批意见、附言和审批动作仍以 `dingtalk-oa-approval` 为主。AI 听记正文、摘要和转写读取统一走 `dws minutes`，只有遇到权限阻塞时才使用 `dingtalk-minutes-access-request`。

## 基本原则

1. **先审阅，后动作。** 同意和拒绝属于审批决策动作，必须先读完材料、确认当前 `RUNNING` 任务属于当前授权审批人、拿到当前 `taskId` 后才执行。若用户明确说“批了/同意/拒绝”，按用户确认执行；若当前任务或定时任务已明确授权自动处理，只有下文的材料、规则和动作门槛均满足时才可执行。业务 Skill 的判断标准缺失或互相冲突、且本单恰好取决于它时转 `needs_human`；动作本身一律按下文完整决策表，不要由 Skill 臆造审批结论。
2. **所有可访问材料必须读完。** 包括审批详情、审批流水、审批附言/评论、附件、链接文档、PDF、合同、报销凭证、面试记录、试用期考核标准、交接文档等。
3. **通过的前提是所有实质文件都已审阅完成，并且有相应标准/依据文档。** 只要审批中的附件、链接、PDF、合同、面试记录、试用期标准、BRD、工时评估、制度依据、预算依据等任一实质材料未读到、未读完或缺少标准文档，不得建议或执行同意。
4. **判定“读不到”之前必须先走通附件读取路径。** `dws oa approval attachment download-url` 和 `authorize-download` 目前对审批附件一律返回 `business error: success=false`（2026-09-17 实测 dws v1.0.62，trace 21030ead17896766012171561e0a32、2101eeef17896765225684156e0b16），**这两个失败不构成“工具未读到”的理由**。可用路径是先做预览授权再走钉盘下载，预览授权同时打开钉盘读取权限：

   ```bash
   dws oa approval attachment authorize-preview --instance-id <processInstanceId> --file-ids <fileId> --with-comment-attachment --format json   # 返回 spaceId
   dws drive +info --space-id <spaceId> --node <fileId> --format json
   dws drive +download --space-id <spaceId> --node <fileId> --output <工作目录内的相对路径> --format json
   ```

   授权之前 `drive +info` 会报 `forbidden.accessDenied`，授权之后同一 `fileId` 就能读元数据并下载正文；xlsx 用表格库读全表，pdf/docx 用文档读取，不得只看截图或文件名下结论。只有这条路径也失败，才可记为“工具未读到”。
   2026-09-17 长沙银行 POC 的 checklist 曾被两次判为“读不到”，实际按此路径 10,549 字节正常下载读全。

5. **缺材料和读不到是两回事，处理完全不同（Derek, 2026-09-23）。** 两者都不得通过，不得用“同意后补”替代审批前审阅。
   - **缺材料**＝申请人确实没交：必填字段为空、没有附件、表单没有给出要求的文件。这是申请人的缺口，按决策表**退回**。
   - **读不到**＝材料已提交但我们没读出正文。先把原则 4 和下文“OA 附件读取降级路径”的每条路径都走一遍。全部路径仍失败且申请人可提供可读副本时，按**退回优先**要求补正；当前流程不支持退回时才评论并保留待办。仅当同时存在独立规则缺口时才并行 `needs_human`，不可把纯材料可补正问题升级成规则缺口。
   - **申请人指向的证据要自己去查（Derek, 2026-09-23）。** 申请人或审批人在附言、评论或重新提交时说“见某次会议/听记/文档/群消息”，而我们有工具能找到它（AI 听记走 `dws minutes` 按标题和日期搜、会议走日程、文档走文档搜索、群消息走 chat 搜索），就必须先找到并读完，再据此判断；读到的内容能回答问题就按它判，不再追问。只有按名称、日期、参会人都搜过仍找不到或无权限，才退回要链接，并写明搜过什么。把“去看某某听记”原样再推回给申请人或转给 Derek，等于活儿没干。
   - **“已和 Derek 确认过”不是证据（Derek, 2026-09-23）。** 申请人在附言里说“已与磊哥确认、请不要拒绝”之类，不能作为通过或升级的理由。先按上一条自己去找确认记录（与 Derek 的钉钉聊天、会议听记、文档）；找不到就退回，要求申请人出具证明。附言里如果给出的是具体的补充信息，就按这些信息重新判断。
6. **遵循已取得的本公司归档规则。** 是否必须进入知识库、必须使用项目文件夹或必须在审批表中附链接，属于组织特定的治理要求。只有 prompt 或其引用的制度明确要求时，才将其作为同意前置条件；否则不得把本组织的归档习惯伪装成跨公司的审批规则。
7. **归档规则缺失时不臆造。** 如果当前事项依赖归档闭环而又没有取得适用制度，记录为规则缺口并转 `needs_human`；如果制度明确要求归档而材料未归档，才按该制度指定的退回或评论动作处理。
8. **不要根据标题直接判断。** 标题只能用于识别流程类型，不能替代表单、附件和附言。
9. **动作以完整本公司规则为准。** 对材料不足、事实矛盾、不合规或高风险事项，先确认适用规则规定的是退回、评论、请示还是拒绝；不能因为本 Skill 见过类似事项就直接拒绝或退回。
10. **退回不等于拒绝。** `revoke` 是撤回自己发起的审批，不是退回；`reject` 是拒绝审批，不能当作“退回补材料”使用。若完整本公司规则要求退回，先用 `dws oa approval revert-activities --task-id <taskId>` 查询可退回的节点列表（`instRevertActivities`），并在退回说明中写清缺口和补充要求。模板支持退回发起人（`REVERT_FOR_RESUBMIT`）时优先退发起人；不支持、或发起人已离职时，退回到仍在职、负责补充材料的节点（`REVERT_FOR_APPROVAL`）。若本公司规则指定评论或 `instRevertActivities` 确实为空，才按该规则评论并保留待办；工具错误不构成“没有可退回节点”的证据。
11. **不要手打或转抄任何 URL。** 2026-09-17 实测：分身把 prompt 里的反馈链接手抄进 `dws chat +dm --content`，百分号转义被抄断在半路（`...%E5%AE%A1%E6% 批待办扫描...`、`...%E7%90%86%E，尚...`），申请人收到一大段乱码；它发现后用 `chat message edit` 重发，**又抄错一次**。规则：消息正文里只能出现**从工具返回结果里原样复制**的链接；prompt、历史消息或上一轮输出里的长 URL 一律不要重抄。反馈链接由服务在自己的发送路径上追加，**分身不得自行拼接或复述**——需要给对方链接时，用审批详情返回的 `url` 字段，或者干脆只写事项名称让对方在钉钉待办里打开。

12. **被判为重复的消息是已送达，不是失败。** 给申请人发通知时，如果 provider 返回重复抑制（例如 `PROVIDER_DUPLICATE_NO_READBACK`），说明同样内容此前已经发出去了：应当读回那条消息确认后报"已送达"，**不要把本轮判为失败**。实测 2026-09-17：一条审批因此连跑四轮全部失败、反复重试又反复被去重，钉钉里当晚一条都没发出。

13. **当前不需要授权审批人处理的审批要跳过，结论是 `no_action`，不是 `needs_human`。** 如果详情或任务列表显示当前 `RUNNING` 任务不属于当前授权审批人，不做完整材料审阅，也不提醒为待处理事项；只记录为列表口径异常或他人待办。这一条**先于**下文的完整决策表判断——决策表第 14 行（兜底 `needs_human`）只适用于授权审批人**确实有**待处理任务的审批，不能用来接住"不确定是不是他的"。
   - **归属对不上时，以授权审批人自己的 `list-pending` 为准。** 实例详情里 `tasks` 的 `userId` 与授权审批人对不上、或多个并行 `RUNNING` 任务分不清归属时，不要因为"无法确认 userId 对应谁"而转 `needs_human`：跑 `dws oa approval list-pending`，这个实例不在授权审批人自己的待办里，就是他人待办，结论 `no_action`；在里面，才继续审阅。
   - 2026-09-22 实测：两条审批（一条 POC、一条其他合同）实例都还 `RUNNING`，但 Derek 的 `list-pending` 为 0，当前待办都在别的审批人手里。一条前一轮已正确得出 `no_action`（conf 0.99），下一轮却因"对不上 userId"翻成 `needs_human`（conf 0.42、rc 0.38）；另一条要 Derek"授权重跑"一个他根本没有待办的审批。**把"要不要处理别人的待办"交给授权审批人，是在造一个他答不了的问题。**

## 通用默认分流

- **可补正的材料缺口优先退回补充，不以拒绝代替补正。** 只有问题已查实、无法通过补充或修订纠正，并且适用业务规则允许拒绝时，才建议拒绝。若钉钉当前流程不支持适用的退回动作，按本公司规则评论要求补充并保留待办；不得用 `reject` 模拟退回。
- **只有制度/标准来源缺失时，申请人侧与人工侧并行处理。** 在 OA 评论中只问申请人能否提供已有、可追溯的制度/标准来源或链接；同时将规则来源、适用边界或动作授权缺口交 `needs_human`，不能让申请人替公司制定规则。申请人回复只用于定位来源，不能单独关闭人工升级。
- 以上是审阅分流默认值，不替代公司或业务大类 Skill 对具体阈值、例外、授权人和最终动作的规定。若业务 Skill 明确写了不同的动作（例如财务模板的规则卡），以该 Skill 为准；没写就按本 Skill 的决策表。业务 Skill 之间互相冲突时转 `needs_human`。

## 工具顺序

优先使用 `dws`，所有命令加 `--format json`。

先读取 DWS skill（如果当前会话还没有读过）：

```bash
sed -n '1,220p' /Users/derek/.agents/skills/dws/SKILL.md
```

常用只读命令：

```bash
dws oa approval list-pending --start "<YYYY-MM-DD>" --end "<YYYY-MM-DD>" --format json
dws oa approval detail --instance-id <processInstanceId> --format json
dws oa approval records --instance-id <processInstanceId> --format json
dws oa approval tasks --instance-id <processInstanceId> --format json
```

当前本机 `dws v1.0.52` 的 `list-pending` 必须传 `--start` 和 `--end`；不要再使用旧版 `--page/--size` 示例。`dws mcp` 的 canonical MCP 命令面已禁用，不能再用 `dws mcp oa get_processInstance_detail` 作为详情兜底。

### DWS detail 解析失败的已知模式

如果 `dws oa approval detail --instance-id <processInstanceId> --format json` 返回：

- `server_error_code=PARAM_ERROR`
- `technical_detail` 包含 `iPaaS 调用失败`、`saNode parse output error`、`expPayload`
- `expPayload` 里已经出现正确的 `processInstanceId`、标题、`operationRecords` 或评论正文片段

这通常不是实例 ID、当前账号权限或 CLI 参数绑定问题，而是 DWS 远端 Wukong/iPaaS 节点在把钉钉 OA 详情返回值转换为声明出参类型时失败。常见触发点是审批详情里的可变结构字段，例如很长的 `operationRecords[].remark`、评论附件、表单嵌套 JSON、空值/数组/对象混合字段。此时 DWS CLI 只收到业务错误，无法从 `detail` 产出可用 JSON。

处理要求：

1. 先记录 DWS 版本、实例 ID、`trace_id`、`server_error_code` 和上述失败症状。
2. 继续读取 `records` 和 `tasks`，但只能用于确认流水和任务归属；`records` 不返回评论正文，不能替代完整详情。
3. 立即使用 OpenAPI 详情补读脚本，不要基于 `records` 的空评论正文做审批通过判断：

```bash
python3 /Users/derek/.agents/skills/dingtalk-oa-approval/scripts/oa_openapi_detail.py --instance-id <processInstanceId> --summary
```

若需要保留完整原始详情用于审阅，去掉 `--summary`，但不得输出或保存 access token、AppKey、AppSecret、cookie、OAuth code 或临时下载 URL。

长期修复应在 DWS 远端接口完成：放宽 `oa/get_processInstance_detail` 的出参 schema，允许 `operationRecords`、表单值、附件、评论等字段保留原始 JSON/字符串/空值/数组/对象，不要让单个字段转换失败导致整个详情接口失败。

如果 `detail` 返回 `formValueVOS: [{"details":[]}]`、附言只有 `ADD_REMARK` 但无正文，或详情接口解析失败：

- 明确记录 DWS 版本、实例 ID、返回症状。
- 继续读取 `records` 和 `tasks`，但不要基于空详情做通过判断。
- 如果用户已授权使用 API，并且本机有 `~/.dingtalk-skills/config`，用 OpenAPI 补读详情；不要在输出里打印 access token、AppKey、AppSecret。
- 若用户已授权打开钉钉界面，切到钉钉客户端或 Chrome 读取页面详情。
- 若钉钉界面仍失败，向用户说明具体失败点，并要求打开对应审批详情页后继续。

## OpenAPI 详情补读

当 DWS 详情为空、字段丢失、或任务归属异常时，允许调用已授权的钉钉 OA OpenAPI/API 作为补充事实源。当前 OA 详情不完整时不能强行只用 DWS；以后如果 DWS 新增完整详情能力，再优先收敛到 DWS。前提是用户已授权，且应用已开通 `qyapi_aflow` 权限。

获取 token 和详情：

```bash
set -a; source ~/.dingtalk-skills/config; set +a
token=$(curl -sS "https://oapi.dingtalk.com/gettoken?appkey=${DINGTALK_APP_KEY}&appsecret=${DINGTALK_APP_SECRET}" | jq -r '.access_token // empty')
curl -sS -X POST "https://oapi.dingtalk.com/topapi/processinstance/get?access_token=${token}" \
  -H 'Content-Type: application/json' \
  -d '{"process_instance_id":"<processInstanceId>"}'
```

常用提取：

```bash
jq -r '
  .process_instance as $p |
  "TITLE: \($p.title)",
  "BUSINESS: \($p.business_id)",
  "CREATE: \($p.create_time)",
  "STATUS: \($p.status) RESULT: \($p.result)",
  "ORIGINATOR_DEPT: \($p.originator_dept_name)",
  "FIELDS:",
  ($p.form_component_values[]? | "- [\(.component_type)] \(.name // "") = \(.value // "")"),
  "REMARKS:",
  ($p.operation_records[]? | select(.remark != null and .remark != "") | "- \(.date) \(.operation_type) \(.operation_result): \(.remark)"),
  "TASKS:",
  ($p.tasks[]? | "- \(.taskid) \(.task_status) \(.task_result) user=\(.userid) url=\(.url // "")")
'
```

OpenAPI 审阅要点：

- `form_component_values` 是表单字段的事实源，可能包含 DDBizSuite JSON、附件数组、链接、表格行等嵌套内容。
- `operation_records` 是审批附言/评论事实源；审批留言里的补充信息必须纳入判断。
- `tasks` 是审批动作和是否需要处理的事实源；只审阅、提醒、操作当前用户且 `task_status=RUNNING` 的任务。若待办列表仍显示但 OpenAPI 中当前 RUNNING 任务不属于当前用户，跳过该审批，不做完整材料审阅，也不要操作。
- 附件里的 `DDAttachment.fileId`/`spaceId` 先按“OA 附件读取降级路径”处理。不要把 `fileId` 直接当 `dws drive download --node` 的 dentryUuid，也不要把同名 `doc search` 结果直接当作附件正文；同名文档只能作为补充候选，必须和原附件文件名、正文关键信息或审批事实交叉验证。
- 输出和日志中不得暴露 token、AppKey、AppSecret、cookie 或 OAuth code。
- 在 `ceo-agent-service` 自动化里，API token、AppKey、AppSecret、cookie、OAuth code、签名下载 URL 不得写入 SQLite、日志、报告、DingTalk 回复、agent 输出或 `audit_summary`；只能记录“已使用授权 API 补读详情”这类事实。

## 钉钉界面 fallback

当 DWS 不能读全文且用户允许打开审批页时：

1. 先尝试钉钉客户端内的 `审批 -> 审批中心 -> 待处理的`。
2. 如果工作通知里有审批通知，也可以从 `工作通知:北京星尘纪元智能科技有限公司` 打开对应卡片。
3. Chrome 直达审批页可能缺钉钉客户端身份，出现“用户信息验证失败”；这时不要继续在 Chrome 硬试，改用钉钉客户端。
4. 直达详情 URL 可从 PC bundle 路由推导，但 PC 客户端可能提示“暂时无法打开该链接，请在手机上查看”。遇到这种情况要如实报告。
5. 智能合同里的合同正文/附件如果 DWS 和文档搜索都读不到，可以在钉钉客户端审批中心搜索申请人、合同名或业务编号，打开审批详情里的 `合同正文 -> 预览`。预览页通常能显示 Word/PDF 正文、AI 概览和页码；需要逐页滚动读完。预览页 URL 可能含临时签名、STS token 或下载参数，不得复制到报告、日志或回复里。
6. 只读审阅时不要点击同意、拒绝、撤销按钮；但若当前任务要求自动评论，且已经确认不是同意/拒绝动作，可以提交评论。

审批中心链接：

```text
https://aflow.dingtalk.com/dingtalk/pc/query/pchomepage.htm?corpid=ding8ffc70a4ef94915f35c2f4657eb6378f&swfrom=mainNav#/upcoming?type=upcoming
```

移动详情 URL 模板（不保证 PC 可打开）：

```text
https://aflow.dingtalk.com/dingtalk/mobile/query/formService?dd_share=false&showmenu=false&dd_progress=false&dd_enable_replace=true&corpid=ding8ffc70a4ef94915f35c2f4657eb6378f&bizType=approve#/detail?procInstId=<processInstanceId>
```

## 审阅流程

每条审批按这个顺序处理：

1. 从 `list-pending` 提取标题、流程类型、`processInstanceId`、`processCode`、状态和更新时间。
2. 先用 `tasks` 或 OpenAPI `tasks` 确认当前 `RUNNING` 任务是否属于当前授权审批人；不属于就跳过，不继续打开附件、文档或链接。
3. 用 `detail` 读取业务编号、创建时间、发起部门、表单字段、附件和任务节点。
4. 用 `records` 读取审批流水和附言/评论。若有 `ADD_REMARK` 但无正文，必须说明正文未读到。
5. 打开审批内所有可访问链接、附件、文档和 PDF。
6. 如果当前本公司规则明确要求归档，检查实质评审文件是否满足该归档规则；没有读到归档制度时把它记录为规则缺口，而不是假定必须存在某一种项目文件夹。
7. 若任一实质材料读不到、缺少对应标准/依据文档，停止实质判断；动作必须遵循完整本公司规则的退回或评论映射。没有该映射时转 `needs_human`，并列出未读到的材料或未取得的规则来源。
8. 如果是录用审批，必须读取面试记录和试用期考核标准；没有读到不得下结论为同意。
9. 如果是财务/报销/付款，必须读取付款依据、预算/项目归属、发票/凭证、合同/订单/账单、费用说明和风险。
10. 如果是出差/差旅/报销，先加载对应业务 Skill；只有该 Skill 明确指定了需要核验的现行制度来源时，才按其限定范围读取。Skill 未提供关键标准时，将其记录为规则缺口，不自行搜索背景文档补规则。
11. 对每条审批显式给出“风险等级”“确信度”“information_completeness”“rule_coverage”，再给出建议动作、核心理由、制度依据、关键风险、建议附言。四个值必须互相自洽：结论里写了缺材料，`information_completeness` 就不能接近 1；没取到完整适用规则，`rule_coverage` 就不能为 `1.0`。
12. 只有用户确认，或当前定时任务 prompt 已明确授权且 `information_completeness == 1.0`、`rule_coverage` 与风险门槛都满足时，才用 `tasks` 中当前用户的 `taskId` 调用 approve/reject。分值不达标时按「动作与结局映射」分流：材料缺口按决策表退回；判断标准不足转 `needs_human`；材料依据都齐但高风险确信度不够转 `needs_human`。等待他人确认或外部结果按决策表评论说明。

## 风险和确信度

每条审批必须单独评估两个维度：

### 风险等级

- **低风险**：错误后果通常可通过常规管理动作纠正，且本公司完整规则明确属于低风险并允许自动动作。不得仅按金额小、历史曾同意或个人口头印象定为低风险。
- **中风险**：涉及预算、客户、差旅、合同、项目资源、特殊费用或后续凭证闭环，或本公司规则没有将它明确归为低风险。
- **高风险**：涉及录用/薪资、晋升、合同实质义务、授信/借款/付款、项目例外、数据/隐私/权限、对外重大承诺、法律/财务/税务/合规风险，或存在明显不一致、矛盾、虚假、不合规。除当前用户对**本条具体审批**的明确指令外，高风险不得自动同意；即便有明确指令，也必须读完材料且取得完整适用规则。

### 确信度

- **高确信度**：审批详情、审批流水、附言/评论、所有实质附件/链接/PDF/文档均已读完；适用 Skill 要求核验的事实证据已核对；如规则明确要求归档，归档也已闭环；当前 `RUNNING` 任务属于当前授权审批人；没有未解释矛盾；结论依据充分。规则文字是否完整计入 `rule_coverage`，不重复计入事实确信度。
- **中确信度**：主体事实和关键依据已读到，但仍有次要信息、后续凭证、已确认的归档要求或边界说明需要补齐；可给出倾向意见，但不自动同意，优先评论要求补充或等待用户确认。
- **低确信度**：详情为空、事实材料未读到、附件不可访问，或评论中有未澄清的新信息。适用标准/授权缺口单独反映在 `rule_coverage`；若它使本案分支未被覆盖，不得自动同意。

### information_completeness（材料完整度，0~1）

衡量的是**做这个决定所需的事实，我实际读到并核实了多少**。它衡量材料，不衡量我们做过的动作——"已经评论过""已经通知过申请人""上一轮审阅过"都**不能**抬高这个值；材料没补上来，它就该一直是低的。

- **1.0**：表单、流水、附言/评论、全部实质附件和链接文档中与本次判断相关的事实都已读到；如适用规则规定需有归档证据，也已满足；没有未解释的事实矛盾。规则来源本身按 `rule_coverage` 评分。
- **0.8~0.99**：主体事实和关键依据齐全，只差次要项——后续凭证、边界说明，或已确认制度要求的归档链接。**不得自动同意**。
- **0.5~0.79**：有一项关键材料缺失或读不到——合同正文、验收标准、交接文档、面试记录、预算依据、发票凭证。**结论只能是退回**。
- **< 0.5**：表单为空、核心附件全部不可读、当前任务归属不明、或评论里出现未澄清的新事实。服务会强制走单问回退，不产生终态结论。

判断时逐项列出"这个审批类型必须读到的材料清单"，再数已读到几项；不要凭整体感觉给分。附件按原则 4 的预览授权路径试过才算读不到。

### 规则来源、完整性与实际覆盖

`rule_coverage` 不是“读到一段规则文字”的分数，而是**本次审批适用的完整规则集是否已经取得、理解并覆盖了实际情况**。在评分前，必须先建立本次审批的规则来源和适用范围。

运行时审批判断按当前任务 prompt 和已加载的通用/业务 Skill 执行。相关规则可以由以下位置提供：

1. 定时任务 prompt 中明确写出的 OA 审批规则区域；
2. prompt 或业务上下文明确引用的规则文档、制度文档或其他可追溯来源；
3. `dingtalk-oa-approval` 与匹配事项的公司/业务专用 Skill，以及 Skill 明确引用的规则 reference。

`钉钉审批审阅原则.md` 是背景参考文档，不是审批 Agent 的运行时规则来源；不得为了补齐 `rule_coverage` 而读取它。若决定所需的公司规则没有写入当前 prompt 或适用 Skill，按规则缺口处理，不自行搜索、推断或用历史案例补规则。

只提供 DWS 查询、详情、任务或写操作命令的 `dingtalk-misc/references/oa.md` 是工具用法参考，不是业务审批规则来源，不能单独支撑高 `rule_coverage`。不得把背景参考文档当作运行时制度来源；本公司审批规则须已写入当前定时任务 prompt 或适用业务 Skill，不可从 Skill 本机路径、历史案例或 Agent 记忆中猜测。

规则来源必须覆盖以下内容：

- 当前审批事项类型和适用范围；
- 做出决定所需的事实、材料和前置条件；
- 阈值、单位、时限、角色关系和判断标准；
- 例外、特批条件、授权人和适用边界；
- 每种结果对应的动作（同意、拒绝、退回、评论、等待或 `needs_human`）；
- 当前审批实际触及的分支、事实和风险。

有下列任一情况，`rule_coverage` **不得为 `1.0`**：只读到总原则或摘要；规则只覆盖事项的一部分；适用 Skill 提到另有公司制度决定本案分支但没有明确给出可适用标准，且没有指出可读取的有效规则来源；例外或授权边界没有写清；规则逻辑与当前案例不匹配；规则来源之间存在未解决冲突；或当前案例出现规则没有覆盖的新分支。不得用经验、先例、常识或 Agent 自己补出的判断把覆盖率补到 1.0。

审阅结果的“制度依据”必须同时记录：规则来源、适用事项/范围、已核对的条款或段落、规则版本或更新时间（如果来源提供），以及未覆盖项或冲突。规则缺口属于我们的依据缺口，不得伪装成申请人的材料缺口。

### rule_coverage（规则覆盖度，0~1）

衡量的是**这个审批有没有完整、可依据、我已经核对过并且覆盖当前实际情况的成文规则集**。完整审批 Skill 可以直接构成规则来源；只有当适用 Skill 明确要求读取外部制度/标准作为本案决策依据时，才必须读取该指定来源。

- **1.0**：通用 Skill 与适用业务 Skill 已覆盖当前分支的事项范围、所需事实、阈值、例外和授权边界；Skill 明确要求的外部规则来源（如有）已读取；并已逐条对照审批内容核对。动作映射由通用决策表给出，不要求业务 Skill 重复编写。
- **0.5~0.99**：有直接规则，但只覆盖部分情形，或有个别条款、例外、授权边界或当前分支需要解释；这表示“部分覆盖”，不是完整规则。
- **大于 0、小于 0.5**：只有边缘或间接依据（如同类审批先例、他人转述的口径），没有直接适用的规则。
- **`= 0`**：该审批类型完全没有直接适用的成文规则，或 Skill 明确要求的外部规则来源存在但读取失败。背景参考文件不是必须读取的规则来源，也不得仅因没有读取它而降低覆盖分。

找不到规则不等于可以按常识放行。Skill 已完整定义本案实际分支时，可依据 Skill 评分；若 Skill 明确要求外部制度补充本案标准而该来源未取得，或 Skill 本身未定义当前分支，`rule_coverage` 必须低于 `1.0`，并按决策表转人工。

### 两个分值和三条路径的关系

- `information_completeness < 0.8` 且缺的是申请人可补正的材料、同时适用规则及动作授权完整 → **优先退回**，写明补正项；当前流程不支持退回时，按适用规则评论并保留待办。若同时存在规则缺口，执行下文“双向处理”，不能只退回或只升级。
- `rule_coverage < 0.5` → **转人工**，不要凭经验给结论，也不要以此为由退回（缺的是我们的依据，不是申请人的材料）。
- `rule_coverage < 1.0` → 规则尚未完整覆盖；不得在结论中写“规则已完整覆盖”，也不得把未覆盖的规则分支当作已满足。需要依赖该缺失规则作出业务判断时，转 `needs_human` 或先补齐规则来源。
- 自动同意要求 `information_completeness == 1.0` 且 `rule_coverage == 1.0`。
- 报分值前先自查：若结论写明**决策所需事实或材料**缺失/未读到，`information_completeness` 必须反映该事实缺口；核心材料缺失时低于 `0.8`，仅缺次要项时可为 `0.8~0.99`。单纯缺规则来源只降低 `rule_coverage`，不自动降低材料完整度。

### 完整决策表（自上而下，命中第一条即执行）

没有类型黑名单，全部按分值判定。每一轮必须先给出 `risk`、`confidence`、`information_completeness`（ic）、`rule_coverage`（rc），再对照下表；**顺序不可调换**，上面的条件优先于下面的。

先分清两类“不能同意”，它们的处理不同，且均不能由本 Skill 自己创造拒绝边界：

- **事实不成立（违规）**：已查实与事实不符、伪造，或违反强制性规定（法律、财税、合规红线）。材料之间只是互相矛盾、还没有提交人的解释时，是提交人要补的说明，按第 6 行退回，不是违规，也不是请示人工的理由。只有在完整适用规则明确允许拒绝、事实已查实且动作授权成立时，才可拒绝；否则请示人工。
- **未达规则要求**：材料真实可信，但**不满足制度设定的标准或门槛**——例如金额、定级、差旅或项目条件。**默认结果是拒绝**（Derek, 2026-09-23）——不满足门槛即不予通过，不需要规则另行写明。唯一例外：业务 Skill 设有特批条款、**且申请人已在表单或附言中明确提出特批并写明理由**，才转 `needs_human` 请示；特批申请不完整（缺负责人意见或理由）按材料缺口退回补齐。**业务 Skill 允许特批、但申请人没有提出，仍然拒绝**：特批是申请人要主张的事，不是我们替他补上的。

**不要把"未达标准"当成违规去拒绝**，也不要把违规当成未达标准去请示。

### 材料缺口与规则缺口同时存在（优先规则）

如果同一审批同时存在申请人能够补充的事实/附件/链接缺口，以及我们尚未取得的判断标准、例外或授权缺口，必须做**两件彼此独立的事**：

1. 在 OA 评论中向申请人只问一个可由其补充的问题，明确需要的事实、附件、链接或已知制度位置；不要让申请人“确认可以批准”或替我们创造制度。
2. 对缺少的公司判断标准、例外或授权边界同时记录 `needs_human`，说明具体缺口和规则来源所有者。评论回执、申请人说明或材料补齐**不能关闭**这个 `needs_human`；收到补充后必须重读当前 OA，再继续等待/处理人工的规则结论。

这条优先于下表的单纯“材料缺口”行：材料问题不能掩盖规则问题，规则问题也不能免除对申请人可补材料的询问。只有完整的公司规则明确把该材料缺口映射为退回，且该规则本身没有缺口时，才可用退回替代评论。

| # | 情况 | 风险 | `ic` | `rc` | `confidence` | 附加条件（须同时成立） | 动作 | Consumer 结局 |
|---|---|---|---|---|---|---|---|---|
| 1 | 不归当前审批人处理 | 任意 | 任意 | 任意 | 任意 | 当前 `RUNNING` 任务不属于当前授权审批人，或审批已终态 | 跳过，写明依据 | `proposal`（跳过） |
| 2 | 读取失败 | 任意 | 任意 | 任意 | 任意 | 工具、线路或详情服务本身报错/不可用；不包括已提交附件按全部支持路径读取后仍不可读的第 4a 行 | 报失败，保留错误原文 | `failed` |
| 3 | 无成文依据 | 任意 | 任意 | `= 0` | 任意 | 仅有规则来源缺口、没有独立的申请材料缺口；若两者并存，先执行上方“双向处理” | 评论只询问申请人是否知道已有、可追溯的规则来源/链接；并行请示人工补齐规则 | `proposal`（oa-comments）+ `needs_human` |
| 4 | 材料缺口 | 任意 | `< 1.0` | `= 1.0` | 任意 | 申请人**确实没交**的材料（字段为空、无附件、未给出要求的文件），规则来源完整 | 优先退回补正；当前流程不支持退回时，按规则评论并保留待办 | `proposal`（revert-task / oa-comments） |
| 4a | 读不到 | 任意 | `< 1.0` | 任意 | 任意 | 材料**已提交**但我们没读出正文，且所有读取路径都已走过 | 申请人可提供可读副本时优先退回补正；流程不支持退回时评论并保留待办。只有并存独立规则缺口时才另加 `needs_human` | `proposal`（revert-task / oa-comments） |
| 5 | 事实不成立 | 任意 | `= 1.0` | `> 0` | `> 0.9`（针对违规事实） | 已查实矛盾、不实、伪造或违反强制性规定 | 拒绝，写明查实的事实 | `proposal`（reject） |
| 6 | 未解释的矛盾 | 任意 | 任意 | 任意 | `<= 0.9`（针对违规事实） | 材料之间、材料与流程状态之间互相矛盾且没有说明，或怀疑第 5 行情形但未查实 | **退回提交人**，写明矛盾的两处事实，要求解释并补充依据；流程不支持退回时评论并保留待办。矛盾由提交人解释，不转 `needs_human`（Derek, 2026-09-23）；并存独立规则缺口时按“双向处理”另加 | `proposal`（revert-task / oa-comments） |
| 7 | 未达标准·已申请特批 | 任意 | `= 1.0` | `> 0` | 任意 | 材料真实但不满足门槛；业务 Skill 设有特批条款；**申请人已在表单或附言中明确提出特批并写明理由，且负责人意见已记录** | 请示 Derek，附特批建议与理由（特批申请不完整时按第 4 行退回补齐） | `needs_human` |
| 8 | 未达标准 | 任意 | `= 1.0` | `= 1.0` | `> 0.9` | 材料真实但不满足业务 Skill 设定的门槛 | **拒绝**，引用条文和实际数值（默认结果，无需规则另行写明“不满足即不予通过”） | `proposal`（reject） |
| 9 | 含义有歧义 | 任意 | `= 1.0` | `> 0` | 任意 | 某处含义不明，需申请人一句话澄清才能定论 | 评论提问，正文只放一个问题 | `proposal`（oa-comments） |
| 10 | 等第三方 | 任意 | 任意 | `> 0` | 任意 | 在等他人确认或外部结果（财务复核、客户回签、交接人确认等），且申请人没有应补材料 | 评论说明当前状态和等待对象 | `proposal`（oa-comments） |
| 11 | 可通过·低风险 | 低 | `= 1.0` | `= 1.0` | `> 0.9` | 材料真实、满足完整规则的全部要求 | 同意 | `proposal`（approve） |
| 12 | 可通过·中风险 | 中 | `= 1.0` | `= 1.0` | `> 0.9` | 材料真实、满足完整规则的全部要求 | 同意 | `proposal`（approve） |
| 13 | 可通过·高风险 | 高 | `= 1.0` | `= 1.0` | `> 0.9` | 材料真实、满足完整规则的全部要求 | 同意 | `proposal`（approve） |
| 14 | 兜底 | 任意 | 任意 | 任意 | 任意 | 以上都不命中，包括适用规则不完整或没有覆盖当前实际分支；**前提是授权审批人确有待处理任务**，否则按基本原则 13 结论为 `no_action` | 给出建议和理由，请示当前授权审批人；先补齐规则来源，不得把规则缺口写成申请人材料缺口 | `needs_human` |

第 14 行是兜底：**凡是没够到第 11–13 行门槛的，一律落到这里请示当前授权审批人**，不需要为“`rc` 差一点”或“`confidence` 差一点”单独列行。

第 9、10 行排在同意之前是有意的：**含义未澄清、或还在等第三方结果时，分值再高也不能同意**。

**任何审批决策都必须带理由，`--remark` 一律必填。** DWS 的 schema 把 `remark` 标为"可选"，**这里不接受可选**：`approve`、`reject`、`revert-task` 三个命令缺少 `--remark`，或 `--remark` 为空、只有"同意""不通过"这类无信息的词，都属于错误执行，必须重做。理由要写清依据的条文或事实、以及对方接下来该怎么办（退回）或为什么走不下去（拒绝）。

**执行后必须回读确认理由已经落库**：`dws oa approval records` **不返回 remark 正文**（已知限制），所以不能用它核验理由；要用 OpenAPI 详情补读脚本读 `operation_records[].remark`，确认自己写的那段话确实在里面。回读不到理由，就当作这次动作没写清楚，需要补一条评论把理由补上。

**执行拒绝前必须先查退回，并用措辞自检。** 2026-09-17 实测：一份客户合同被直接拒绝，`revert-activities` **一次都没调用**，而拒绝理由写的是"请先补齐上述既有事实并重新提交审阅"——那是一句退回的话，却用拒绝的命令发了出去；审批因此终结，申请人只能从头重发。两条强制检查：

1. **调用 `reject` 之前，必须先调用 `dws oa approval revert-activities --task-id <taskId>`**，并在结论里写明返回结果。此查询用于确认拒绝理由是否其实要求申请人补正；仅仅 `instRevertActivities` 非空，不会把“材料齐全但未达已覆盖标准”的第 8 行默认拒绝改成退回。
2. **措辞自检**：如果你写的理由里出现"请补充""请补齐""请提供""重新提交""修改后再提交"这类**要求对方做事然后回来**的表述，那么这不是拒绝，是**退回**——改用 `revert-task`，把同一段话放进 `--remark`。拒绝的理由只描述**已经查实的事实**和据此不予通过的结论，不含"补齐后再来"的要求。

拒绝是终结这条审批；退回是把它交回给能修的人。要对方补东西就永远是退回。

**拒绝（第 5、8 行）不套用第 11–13 行的风险门槛，但仍要求适用规则完整。** 已确认的违规（第 5 行）只有在事实依据充分、规则明确允许拒绝且授权成立时才可拒绝。真实材料未达到 Skill 明确规定的标准（第 8 行）按用户确认的默认规则拒绝，无需业务 Skill 再重复声明拒绝动作；若 Skill 设有特批且申请人明确提出，走第 7 行。若规则本身不完整或当前分支未覆盖，不能伪装成已确认违规/未达标准，转第 14 行 `needs_human`。

统一前置（第 5、8、11、12、13 行必须同时满足）：当前 `RUNNING` 任务确属当前授权审批人、审批仍是 `RUNNING`、分值与结论自洽——结论里写了“缺 X”或“未读到 X”，`ic` 就不可能是 `1.0`。

**几条容易走错的边界：**

- `ic` 不满分但缺的**不是材料**（例如只差第三方确认）→ 不要退回，走第 10 行评论等待；退回是要申请人补东西，第三方的事退给申请人没用。
- `rc` 不达标 → 永远不要退回给申请人：缺的是**我们的依据**，不是他的材料。低于 0.5 走第 3 行；`0.5 <= rc < 1.0` 走第 14 行补齐规则来源并 `needs_human`；只有 `rc == 1.0` 才能按完整规则作出规则驱动的通过或拒绝。
- 第 3 行的申请人询问只用于定位已有规则来源，不能要求申请人创设或解释公司制度；人工升级必须并行保留。若同时有可补正的申请材料缺口，另按“材料缺口与规则缺口同时存在”处理，不能用退回替代规则升级。

### 动作与结局映射

审批动作必须映射到协议的结局上，不能自创。**每一种处理都要落成一个带理由的 `proposal`**——包括“跳过”：跳过是一个明确的判断（这件事不需要当前授权审批人处理），必须写清依据，不能用空的 `no_action` 代替。`no_action` 只保留给“本轮确实没有任何可提案的动作”这种退化情形。

用 `no_action` 表达“我已经评论过了”或“等当前授权审批人确认”是错的：任务会收口成 `done` 并从 Attention 消失，待处理人再也看不到它在等待。

| 业务情形 | 动作 | Consumer 结局 |
|---|---|---|
| 分值达标，且完整规则明确同意动作 | 同意 | `proposal`（approve） |
| 事实有问题、不合规，且完整规则明确拒绝动作 | 拒绝 | `proposal`（reject） |
| 材料缺、读不到且申请人可补正 | **优先退回**；流程不支持时评论保留待办 | `proposal`（revert-task / oa-comments） |
| 材料齐全，只是在等他人确认或外部结果 | 评论 | `proposal`（oa-comments） |
| 材料在但含义有歧义，需申请人澄清 | **在审批里评论提问** | `proposal`（oa-comments，正文只放一个问题） |
| 高风险但分值不够 | 请示当前授权审批人 | `needs_human` |
| **找不到成文制度**（`rc<0.5`） | **补齐规则来源并请示当前授权审批人**；只有本公司规则要求时才评论申请人 | `needs_human` |
| **规则未完整覆盖**（`0.5 <= rc < 1.0`） | **补齐规则来源并请示当前授权审批人** | `needs_human` |
| 当前 RUNNING 任务不属于当前授权审批人，或已终态 | 跳过 | `proposal`（跳过，写明依据） |
| 工具、线路、读取失败 | — | `failed` |

**提问一律走审批评论，不要发私聊。** 问题留在审批单上，任何人打开这条审批都能看到上下文；私聊会让问答脱离审批记录，而且绕过服务的发送通道（无幂等键、无账本、反馈脚注要靠模型手抄，已因此发出过乱码消息）。

协议在 `information_completeness < 0.5` 时要求返回"只含一个问题的 proposal"。**在 OA 场景下，缺材料时这个问题由退回说明承载**——退回本身就是向申请人提出补充要求，不要再另发一条问句。只有材料齐全、仅含义不清时，才单独用评论提问。

## 审批材料读取补充

### OA 附件读取降级路径

OA 表单里的 `DDAttachment.fileId` 是审批附件 ID，不等同于 `dws drive download --node` 需要的 32 位 dentryUuid。审批附件优先走钉钉官方审批附件下载接口；只有官方下载失败时，才用文档搜索、企业检索或钉钉界面补读。

1. 先从 OpenAPI 原始字段提取 `fileName`、`fileType`、`fileSize`、`fileId`、`spaceId`，保留这些信息用于比对。
2. 优先调用官方审批附件下载接口获取真实附件：

```bash
# 使用新版 OpenAPI token；不要打印 token 或 downloadUri。
curl -sS -X POST "https://api.dingtalk.com/v1.0/workflow/processInstances/spaces/files/urls/download" \
  -H "x-acs-dingtalk-access-token: <accessToken>" \
  -H "Content-Type: application/json" \
  -d '{"processInstanceId":"<processInstanceId>","fileId":"<fileId>"}'
```

接口返回 `result.downloadUri` 后，用该临时地址下载二进制附件，再按 `fileType` 抽取正文：`docx` 解 `word/document.xml`，`xlsx` 读工作表 XML/sharedStrings，`pdf` 用 PDF 文本抽取，图片用 OCR 或人工查看。下载地址通常短期有效，且可能含签名；不得写入日志、SQLite、审批评论、DingTalk 回复或 agent 输出。

在 `ceo-agent-service` 中，优先使用服务侧已封装的 `DwsClient.download_oa_process_attachment(processInstanceId, fileId)` 和 worker 注入的 `downloaded_attachment.text`，不要让子 agent 自己把 `fileId` 当 drive node 下载。

3. 如果官方审批附件下载接口返回 `noPermission`、超时或网络错误，可重试一次；仍失败时，记录具体错误，并用文件名查找可读的钉钉文档节点作为候选：

```bash
dws doc search --query "<fileName without extension or key title words>" --page-size 10 --format json
dws mcp aisearch search_enterprise --json '{"queries":["<fileName> <审批标题> <关键业务词>"],"searchTypes":["document"],"timeRange":""}' --format json
```

评论/审批流水里的附件和表单 `DDAttachment` 不是同一个下载口径。OpenAPI `operation_records[].attachments[]` 可能只给 `file_id`、`file_name`、`file_size`、`file_type`，没有 `spaceId`。处理顺序：

1. 先确认它是评论附件，不要把“评论附件下载失败”误判为申请人未上传。
2. 可先获取审批钉盘空间，用于判断是否能走审批钉盘授权：

```bash
curl -sS -X POST "https://api.dingtalk.com/v1.0/workflow/processInstances/spaces/infos/query" \
  -H "x-acs-dingtalk-access-token: <accessToken>" \
  -H "Content-Type: application/json" \
  -d '{"userId":"<currentUserId>","agentId":<agentId-or-0>}'
```

3. 普通 `processInstances/spaces/files/urls/download` 即使带上该 `spaceId`，对评论附件仍可能返回 `noPermission`。这是评论附件下载口径问题，不是附件不存在。
4. 新版 OA 高级版下载接口可读评论附件：

```bash
curl -sS -X POST "https://api.dingtalk.com/v1.0/workflow/premium/processInstances/spaces/files/urls/download" \
  -H "x-acs-dingtalk-access-token: <accessToken>" \
  -H "Content-Type: application/json" \
  -d '{"processInstanceId":"<processInstanceId>","fileId":"<fileId>"}'
```

如果返回 `benefit.status.invalid`，表示租户/应用未开通或权益过期，不能继续把同一个 `file_id` 当作表单附件、drive node 或 doc node 反复尝试；改走钉钉客户端审批详情、工作通知卡片、申请人评论补可访问链接三选一。若 UI 和搜索也读不到，结论必须是“工具未能读取评论附件”，不得通过，但也不要说申请人没上传。

4. 对搜索结果只接受能和原附件匹配的候选：文件名/标题高度一致，并且正文 snippet 明确包含审批中的项目、客户、金额、主体、日期等关键字段。不要因为搜到同名或相似文件就默认匹配；同名在线文档可能是模板、旧版本或另一个节点。
5. 搜到 `nodeId` 后按类型读取：
   - `extension=adoc`：`dws doc read --node "<nodeId>" --format json`
   - `extension=axls`：`dws sheet list` 后用 `dws sheet range read`
   - `extension=docx|pptx|pdf|md` 且 `doc info/download` 可用：`dws doc download --node "<nodeId>" --format json`，再用本地工具抽取文本；若企业搜索已返回完整可判断 snippet，也可作为辅助证据，但合同/关键财务附件仍应尽量下载或读取全文。
6. 如果 `doc search` 找不到，但 `aisearch search_enterprise` 能返回带完整正文片段的同名文件，可引用该检索结果继续判断，并在材料记录中说明“通过企业知识检索按文件名补读”。
7. 如果应用已开通开放平台权限 `Storage.Dentry.Search`，可用官方存储搜索接口按附件名、空间或其他线索定位 dentry；若接口返回 `Forbidden.AccessDenied.AccessTokenPermissionDenied`，说明当前应用缺少该权限，继续走文档搜索、企业检索和钉钉界面，不要把它当成附件不存在。
8. 只有官方审批附件下载（**必须先走原则 4 的预览授权路径**，`download-url` / `authorize-download` 失败不算读不到）、文档搜索、企业检索、官方存储搜索和已授权钉钉界面都无法读到时，才把附件列为“工具无法访问/材料缺口”。一旦确认读不到，本单不得建议通过；申请人可提供可读副本时优先退回补正。若审批流程不支持退回，才评论说明具体缺项并保留待办；只有并存独立规则缺口时另加 `needs_human`。

财务审批里的发票字段不要只读 `InvoiceField.value`。`value` 可能只有供应商名；完整发票号、开票日期、购销方、价税合计、税额、验真/合规结果、文件 `fileId`/`spaceId` 通常在 `InvoiceField.ext_value` 的 JSON 里。必须解析 `ext_value` 后再判断发票是否匹配付款金额和供应商。

PDF 附件读取失败时，先判断是“真的不可读”还是“PDF 结构损坏、扫描件或图片型 PDF”。如果 PDF 文本抽取失败、页数为 0、page tree 异常或文本层为空，不得直接列为不可读；必须先走“审批 OCR 路径”。只有下载失败、OCR 失败、钉钉界面也无法读取时，才列为工具不可读。

### 审批 OCR 路径

审批中的扫描 PDF、图片附件、发票/完税证明截图、合同扫描件、盖章扫描件、报销凭证、验收单等，如果没有可用文本层，必须使用 `ocr` skill 的外部 Stardust OCR 服务读取；不要把本地 `magick + tesseract` 当作默认路径，避免 PDF 转图卡住或 OCR 语言/版面处理不一致。

OCR 前提：

1. 必须先用官方审批附件下载接口、文档下载或钉钉界面导出拿到真实本地文件；不要把临时下载 URL、token、cookie、AppKey、AppSecret 写入日志、SQLite、审批评论或回复。
2. 对高影响字段，如金额、日期、主体、合同期限、发票号、税额、付款账号、验收数量、身份证/手机号等，必须保留页码和 OCR 置信度；置信度低或识别有警告时，结论只能到中确信度，并提示需要人工核对原图。
3. OCR 结果要和审批表单、评论、合同/发票字段、历史审批编号交叉验证；不得只凭 OCR 单点通过财务、合同、录用、立项等高风险审批。
4. OCR 失败或服务认证失败是真失败；不要未经授权上传到其他 OCR 服务，也不要用猜测补全文字。

常用命令：

```bash
python3 "$HOME/.agents/skills/ocr/scripts/ocr.py" \
  "/absolute/path/to/scanned.pdf" \
  --format markdown \
  --output "/absolute/path/to/ocr-result.md"
```

如果只需要抽查关键页，使用一基页码：

```bash
python3 "$HOME/.agents/skills/ocr/scripts/ocr.py" \
  "/absolute/path/to/scanned.pdf" \
  --pages 1,3-5 \
  --format markdown
```

审批审阅时要读取 OCR 输出全文，并在材料记录中说明“通过 OCR 读取扫描件”。如果 OCR 输出与表单/评论冲突，按明显不一致处理，要求补充清晰材料或人工复核；不得自动同意。

已验证案例：
- OA 附件 `项目实施计划（第三曲线大模型解决方案）(2)(2)(1).docx` 不能用同名 `dws doc search` 结果替代；同名 Alidoc 节点曾是空模板。正确路径是用 OpenAPI 详情中的 `fileId=224596585916` 调官方审批附件下载接口，真实 docx 可读到项目范围、责任分工、T+30/T+60 里程碑、风险评估和交付物清单。
- OA 附件 `专家网络平台一期工时评估.pdf` 的 `drive download` 因空间权限失败，但 `dws doc search --query "专家网络平台一期工时评估"` 可找到同名 Alidoc 节点并用 `dws doc read` 读取全文。
- OA 附件 `背景_统一事实底稿模板.docx` 的 `drive download` 因空间权限失败，但 `dws doc search --query "背景_统一事实底稿模板"` 可找到同名 Alidoc 节点并读取转让定价事实底稿全文。
- 智能合同正文 `0526星尘设备交接单.docx` 的 `drive download` 因空间权限失败，`doc search` 和企业检索也没有可信同名结果；钉钉客户端审批中心搜索 `Lynne` 后打开对应合同审批，在 `合同正文 -> 预览` 中可逐页读取 Word 正文和 AI 概览。

钉钉文档和表格：

- `alidocs.dingtalk.com/i/nodes/<nodeId>` 可能是在线文档，也可能是钉钉表格。
- 在线文档用 `dws doc read --node "<url-or-nodeId>" --format json`。
- 如果提示 `当前节点是钉钉表格（扩展名=axls）`，改用：

```bash
dws sheet list --node "<nodeId>" --format json
dws sheet info --node "<nodeId>" --sheet-id "<sheetId>" --format json
dws sheet range read --node "<nodeId>" --sheet-id "<sheetId>" --range "A1:Z80" --format json
```

钉盘预览链接和只读权限：

- 审批表单或评论里的 `https://qr.dingtalk.com/page/yunpan?route=previewDentry&spaceId=<spaceId>&fileId=<dentryId>&type=file` 是钉盘预览入口。先解析 `spaceId` 和 `fileId`，再用 `dws drive info --node "<fileId>" --space-id "<spaceId>" --format json` 获取真实文件名、扩展名、路径、`dentryId`、32 位 `fileId/nodeId` 和 `docUrl`。
- 对 `docx`、`pptx`、`xlsx`、`pdf`、图片等二进制文件，优先尝试 `dws drive download --node "<dentryId>" --space-id "<spaceId>" --output "<local-dir-or-file>" --format json`。下载成功后再按文件类型抽取正文或走 OCR。
- 如果 `drive info` 成功但 `drive download` 报“没有权限访问该钉盘空间”“无文件读取权限”等，不要说文件不存在；这是“可预览/可见元数据，但无下载读取权限”。必须继续用 `dws doc permission list --node "<32位nodeId>" --format json` 或相应 `drive permission list` 查看权限角色。
- 若权限列表显示当前审批执行账号只通过部门、群或个人获得 `READER`，说明通常只能网页/客户端预览，不能下载解析正文。不要把 `READER` 直接等同于材料不可读；如果 `docUrl`、钉盘预览页或审批详情里的预览按钮能打开，必须进入网页或钉钉客户端预览页逐页读取全文，必要时使用页面复制、浏览器导出、截图 OCR 或人工逐页摘录完成审阅。
- 只有在 DWS 不能下载、网页/客户端预览也打不开，或预览页无法读完正文时，才把材料标记为“只读预览仍无法读取全文”。此时不得建议通过。
- 用户明确要求修复时，可以尝试给当前审批执行账号补 `DOWNLOADER` 权限，例如 `dws doc permission add --node "<32位nodeId>" --users "<currentUserId>" --role DOWNLOADER --format json`。如果返回 `forbidden.accessDenied` 或提示需要 `OWNER / MANAGER / EDITOR`，说明当前账号没有权限管理权，不要重复尝试，也不要改用猜测路径。
- 权限修复失败后的处理：若网页/客户端预览可读，继续通过预览完成审阅，并在材料记录中说明“通过网页/客户端预览读取，不能下载”；若预览也无法读完且申请人能补正，优先退回要求其提供可访问链接/副本，或协调文件所有者/管理员授权当前审批执行账号。当前流程不支持退回时才评论并保留待办。评论/退回中写明文件名、节点 ID、当前只读角色、所需补正和“未读完前不得通过”；若并存规则缺口，另行 `needs_human`。
- 对这类问题，最终报告要区分四种状态：`文件缺失`、`文件存在但只能预览不能下载`、`已通过网页/客户端预览读取完成`、`预览和下载均无法读取全文`。不要把权限不足归为普通附件解析失败。

外部业务证据系统：

- 录用、项目、财务或合同审批可能引用审批表之外的业务系统。该系统的名称、登录方式、查询键和所需证据包必须由当前本公司规则源指定，不能从历史环境或本 Skill 推定。
- 只读到列表摘要不构成读完；需要逐项展开或导出完整评审/证据包，读到每轮评价、风险、结论及相关附件。
- 系统访问失败时，记录具体访问失败；不要把系统中可能存在但未读取的证据当作缺失、也不能以摘要替代正文。

## 公司制度与知识边界

公司/业务专用 Skill 是本 OA workflow 的运行时规则载体。Agent 不得通过搜索或打开 `钉钉审批审阅原则.md` 补规则；当前 Skill 未覆盖的真实公司规则、例外或权限，按规则缺口处理并进入 `needs_human`。若业务 Skill 明确引用另一份有效文件作为本案必要的事实证据或规则原文，可以按该 Skill 的限定用途读取，但不能因此将背景材料扩展为新的动作规则。

## 通用审批证据框架

以下是要检查的**证据类别**，不是可直接执行的公司规则。每个类型的阈值、例外和授权人由对应业务 Skill 提供；动作一律按本 Skill 的决策表。

| 审批类型 | 需读证据 | 规则必须补齐的内容 |
|---|---|---|
| 项目/特批 | 商业理由、项目测算、战略/客户价值、管理意见、历史/会议依据 | 收益或毛利门槛、特批条件、授权人、低于门槛后的动作 |
| 录用 | 岗位需求、简历、完整面试记录/评审包、试用期目标、定级与薪资依据 | 岗位级别标准、市场薪资方法、HR/业务授权、候选人系统入口 |
| 离职 | 交接清单、接收确认、账号/资产处置、未结风险 | 必须交接项、接收确认标准、例外和关闭责任 |
| 请假/外出 | 理由、时间、工作交接、业务影响、必要的人员关系证据 | 人员关系要求、时长/证明标准、例外和动作 |
| 财务/报销/付款/关联交易 | 付款对象和金额、预算/项目、合同/订单/账单/验收、发票/凭证、风险与复核意见 | 授权矩阵、税务/发票例外、预付款/紧急付款、关联交易定价与复核 |
| 晋升 | 岗位变化、历史绩效/反馈、改进计划、考核指标 | 晋升标准、评审人、例外和后续考核 |
| 出差/差旅 | 客户/商机或业务依据、行程、预算、费用凭证、预期结果 | 场景、提前期、额度、交通/住宿例外、报销材料 |
| 合同 | 合同正文、主体、价款、交付/验收、违约、保密/数据/IP、期限、法务与业务意见 | 签约授权、必须法务复核条件、金额/风险阈值、红线和动作 |

规则源不完整或当前实际分支未被覆盖时，不能用此表中的“通常做法”替代本公司规则，必须将 `rule_coverage` 记为低于 `1.0` 并转人工。

## 输出格式

普通审阅输出每条包含：

```text
标题：
流程类型：
业务编号：
创建/更新时间：
是否超过 3 天：
审批链接：
建议动作：同意 / 拒绝 / 退回补充 / 评论等待 / 评论提问 / 请示当前授权审批人（needs_human）/ 跳过（写明依据）
风险等级：低 / 中 / 高
确信度：高 / 中 / 低
核心理由：
制度依据：
关键风险：
建议附言：
材料缺口：
```

如果是定时 heartbeat，只提醒两类事项：

1. 上次检查后新出现的审批。
2. 创建时间距当前已超过 3 天且仍在 RUNNING 的审批。

heartbeat 输出要简洁，按风险优先排序。是否执行同意、拒绝、退回或评论，完全由当前定时任务 prompt 提供的授权和完整本公司规则决定；Skill 不因它是 heartbeat 而自行扩大或收缩权限。材料缺口、规则缺口和等待第三方结果必须区分：材料缺口按本公司规则指定动作处理，规则缺口转 `needs_human`，等待第三方结果按本公司规则决定评论或等待。如果没有新审批也没有超过 3 天审批，明确说明无需处理。

## 执行动作

同意、拒绝、退回和评论均须由当前任务授权及完整本公司规则决定。审批评论不是同意或拒绝，但也不得在本公司规则指定退回或人工请示时擅自以评论替代。

自动同意只在当前定时任务 prompt 明确授权、`information_completeness == 1.0`、`rule_coverage == 1.0`、本公司风险门槛满足且规则明确指定同意动作时执行。自动动作必须写明审批意见，并在执行后回读审批记录或待办列表确认结果。

同意：

```bash
dws oa approval approve --instance-id <processInstanceId> --task-id <taskId> --remark "<审批意见，必填，写清依据的条文或事实>" --format json --yes
```

退回（仅当当前授权和完整本公司规则指定退回；缺口和补充要求写进 `--remark`，不要另发一条评论）：

先查可退回节点：

```bash
dws oa approval revert-activities --task-id <taskId> --format json
```

`instRevertActivities` 非空时执行退回；模板支持退发起人时优先 `REVERT_FOR_RESUBMIT`（`target-activity-id` 固定 `sid-startevent`），否则退到负责补充材料的节点 `REVERT_FOR_APPROVAL`（`activityId` 取自 `instRevertActivities`）：

```bash
dws oa approval revert-task --instance-id <processInstanceId> --task-id <taskId> --target-activity-id <activityId> --action <REVERT_FOR_RESUBMIT|REVERT_FOR_APPROVAL> --remark "<材料缺口和补充要求>" --yes --format json
```

**这条命令已于 2026-09-17 实跑验证可用**（长沙银行 POC，返回 `success: true`，钉钉待办随即从 4 条减为 3 条）。它是写操作，必须带 `--yes`。

选择退回节点时的硬规则：

- `actualActioners` / `activityActioners` 里标注 **“(已离职)”的节点不得作为退回目标**——退过去没有人处理，审批会彻底卡死。发起人已离职时不要用 `REVERT_FOR_RESUBMIT`，改退到仍在职的负责节点，通常是“提交人部门直接主管审批”，由主管指定新负责人。
- 只有 `instRevertActivities` 为空才允许说“无法退回”。`dws schema --cli-path "oa approval revert-task"` 返回 `unknown runtime schema path` 是 DWS 漏注册 schema 的已知缺陷（`revert-task`、`revert-activities` 两条都缺，同族的 `reject`、`redirect-task` 正常），**命令功能完好，不是退回不可用的证据**。
- 退回在审批流水里记为 `REDIRECT_PROCESS`，没有独立的 revert 操作类型；核验是否生效看这条记录加待办列表，不要找 “revert” 字样。

只有完整本公司规则允许评论、或 `instRevertActivities` 确实为空且规则指定该降级动作时，才评论要求补材料并保留待办，并在结论里写明“该模板无可退回节点”：

```bash
dws oa approval oa-comments --instance-id <processInstanceId> --text "<审阅意见、材料缺口和补充要求>" --format json
```

等待他人确认或外部结果（不涉及材料缺口）用上面的评论命令说明；需要申请人澄清含义时，也用同一条命令，正文只放一个问题。

拒绝：

```bash
dws oa approval reject --instance-id <processInstanceId> --task-id <taskId> --remark "<必填：已查实的事实和不予通过的依据条文；不要写'补齐后再提交'，那是退回>" --format json --yes
```

不要用 `reject` 执行“退回补材料”；按决策表需要退回时，用上面的 `revert-activities` + `revert-task`。是否退回由决策表决定，不需要业务 Skill 另写动作映射。

执行同意、拒绝或退回后必须用 `list-pending` 复查该审批是否离开待办列表（退回后应不再是分配给当前审批执行账号的 `RUNNING` 任务），并把结果告诉用户。执行评论后必须用 `records` 或 OpenAPI `operation_records` 复查评论是否写入成功。
