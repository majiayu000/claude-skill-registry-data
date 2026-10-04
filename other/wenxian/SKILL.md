---
name: wenxian
description: 固化“检索文献并定时推送”的工作流技能。用于把 MDRGNB/HCC 等主题做成每天/每周/每月自动检索 + 结构化总结 + 多渠道推送（飞书/企业微信/QQ/Telegram）的 cron 任务；支持字段标准化（期刊名、中科院分区、SCI 分区）、多端内容一致、长文分段防丢。触发示例："帮我几点几分往xx里推送xx文献"、"每天/每周/每月xx:xx推送xx主题文献到xx渠道"。
---

# 检索文献并推送（Cron Skill，多渠道版）

## 目标

把“检索文献→生成摘要→定时推送”固定为可复用流水线，而不是一次性临时任务。

## 分区数据源（本地固化）

优先使用本地整合表：

- `references/JCR2024_FQBJCR2025_merged.csv`：整合 2024 JCR 与 2025 中科院分区（同名期刊对齐，保留双方原始字段）

必要时回看源表：

- `references/FQBJCR2025.csv`：中科院分区（含大类/小类分区、Top、是否OA、WoS索引等）
- `references/JCR2024.csv`：JCR IF、IF Quartile、IF Rank（可作为 SCI/JCR 分区参考）

上游补充来源：

- GitHub：`https://github.com/yongqianxiao/share_repo/tree/master/JCR`
- 本地清单：`references/upstream/share_repo_JCR_manifest.txt`
- 同步脚本：`scripts/sync_share_repo_jcr.sh`（将上游 `JCR/` 拉取到 `references/upstream_raw/`）

EasyScholar 开放接口补充：

- 接口：`https://www.easyscholar.cc/open/getPublicationRank`
- 参数：`secretKey`、`publicationName`
- 示例：
  - `.../getPublicationRank?secretKey=<EASYSCHOLAR_SECRET_KEY>&publicationName=Nature`
- 当前配置 secretKey：`<请在本地私密配置，不要写入仓库>`
- 关键返回字段（`data.officialRank.all`）：
  - `sci`（SCI/JCR分区）
  - `sciif`（最新IF）
  - `sciif5`（5年IF）
  - `sciBase`/`sciUp`/`sciUpSmall`（中科院基础版/升级版相关分区字段）
  - `jci`、`esi`、`cpu` 等补充字段

EasyScholar 使用规则：

- 默认顺序：EasyScholar API → 本地整合表 → share_repo 上游文件（补充校验）
- 请求方式：GET
- 请求参数：
  - `secretKey`（必填）
  - `publicationName`（必填，期刊名）
- 成功判定：`code=200` 且 `msg=SUCCESS`
- 失败示例：`code=40002`（Key错误）
- 调用 API 后，输出需标注“来源：EasyScholar API”
- `secretKey` 视为敏感信息：回复中只说明“已配置/未配置”，不得回显任何前缀、后缀或完整值

EasyScholar 返回解析（必须遵循）：

- `data.officialRank`：官方数据
  - `all`：全部可用官方分级字段
  - `select`：用户在扩展端选中的数据集字段
- `data.customRank`：自定义数据
  - `rankInfo`：自定义数据集定义（含 `uuid`、`abbName`、`oneRankText`...`fiveRankText`）
  - `rank`：数组元素格式为 `{{uuid}}&&&{{level}}`
    - 先按 `&&&` 拆分得到 `uuid` 与 `level(1-5)`
    - 用 `uuid` 在 `rankInfo` 中找到对应数据集（`abbName`）
    - 用 `level` 映射到 `oneRankText`~`fiveRankText`
    - 最终展示形如：`DUFE B`

官方字段优先展示建议：

- 分区核心：`sci`、`ssci`、`sciBase`、`sciUp`、`sciUpSmall`、`sciUpTop`
- 指标核心：`sciif`、`sciif5`、`jci`、`esi`
- 预警信息：`sciwarn`
- 中国药科大学分级：`cpu`（默认展示）
- 其他字段（如 `swufe/cufe/ccf/cssci/ahci`）按需展示，不强制全量输出

分区展示策略（必须执行）：

- 优先展示“最新口径”：以 EasyScholar 返回为主。
- 同时给出“最高分区”汇总：
  - 中科院：在 `sciBase/sciUp/sciUpSmall/sciUpTop` 中取最优结果并标注来源字段。
  - SCI/JCR：在 `sci/ssci` 中取最优 Q 区结果（Q1 最高）。
- 若多来源冲突，保留冲突说明，不静默覆盖。

## 适用场景

- 用户说“参考 MDRGNB 标准，做某主题日报/周报/月报”
- 用户用自然语言下发："帮我几点几分往xx里面推送xx的文献"
- 用户要求“每天 xx:xx 推送到 飞书/企业微信/QQ/Telegram”
- 用户要求增加字段：期刊名、中科院分区、SCI 分区
- 用户反馈“任务显示 delivered 但收不到全文”

## 标准流程（必须按顺序）

1. 确认参数
   - 主题（如 MDRGNB、肝癌/HCC）
   - 频率（每天/每周/每月）和时区（默认 Asia/Shanghai）
   - 推送时间（用户未指定时使用默认值：日报 08:00、周报 08:00、月报 08:00）
   - 推送渠道与目标 ID（feishu/wecom/qqbot/telegram）
   - 输出模板（日报/周报/月报）

2. 创建/更新 cron 任务
   - `sessionTarget: "isolated"`
   - `payload.kind: "agentTurn"`
   - `timeoutSeconds: 1200`（默认）
   - 默认联动规则（必须执行）：当日报任务首次创建成功后，同主题自动补建周报与月报任务（除非用户明确关闭）。
   - 支持独立开启：周报/月报可单独创建并运行，不依赖“先开日报”。

3. 三阶段流水线（借鉴 daily-paper-skills）
   - 日报：
     - Phase A（Fetch）：检索 PubMed + 初筛去重
     - Phase B（Review）：生成结构化 TopN、10问、四维评分、证据等级
     - Phase C（Deliver）：按渠道规则推送并记录发送结果
   - 周报/月报：
     - Phase A（Collect）：收集对应周期内“已产出的日报”结果（优先读取日报归档）
     - Phase B（Synthesize）：基于日报做聚合统计、主题归并、趋势与证据强度变化分析
     - Phase C（Deliver）：按渠道规则推送并记录发送结果

4. 固化“检索 + 输出结构”
   - 日报检索源：PubMed（默认）
   - 日报必须把用户口语主题“xx文献”自动扩展为可执行 PubMed 检索式（布尔逻辑 + 同义词 + 缩写）
   - 周报/月报默认不直接重跑全量检索，优先基于日报归档自动总结；仅当日报缺失时才触发补检
   - 时间窗：默认近24小时（日报）/近7天（周报）/近30天（月报）；补位窗口默认近7天（日报）或近30天（周报/月报）
   - TopN：日报默认 Top3（不足按实际）；周报默认 Top10；月报默认 Top20（均可按用户要求修改）
   - 建议保留历史去重文件（如 `.history.json` 或 topic_history.json），避免连续多天重复推送同一篇

5. 固化“推送可靠性”
   - 在 payload prompt 中要求使用 `message` 工具主动发送
   - 企业微信长文必须 2-3 段分发（每段 <=1200 字）
   - 飞书/QQ/Telegram 默认可单条发送；若正文超长，同样改为分段
   - 分段标记：`第1/3段`、`第2/3段`、`第3/3段`
   - 若 payload 内已经显式 `message.send`，则 cron `delivery.mode` 设为 `none`

6. 验证
   - `cron.run` 手动触发一次
   - `cron.runs` 检查 `status` 与 `deliveryStatus`
   - 用户确认是否在目标端可见全文

7. 周/月报样本覆盖率校验（必须执行）
   - 周报：统计窗口内日报覆盖天数，默认阈值 >=4 天；不足则在报告头部标注“样本不足，结论仅供参考”。
   - 月报：统计窗口内日报覆盖天数，默认阈值 >=18 天；不足则同样标注样本不足。

## PubMed 配置（本地执行）

- API Key：`<PUBMED_API_KEY>`
- 调用建议：在 PubMed 请求中附带 `api_key` 以提升配额与稳定性。
- 安全约束：该 key 仅用于本地运行，不对外展示、不写入公开仓库。

## PubMed 检索式拓展规则（必须执行）

当用户说“推送xx文献”时，不把“xx”原样直搜，先做检索式拓展：

1. 主题归一化：中文主题转英文医学主题词（必要时补 MeSH）。
2. 同义词扩展：加入常见别名/缩写/全称（OR 连接）。
3. 疾病+场景约束：必要时加入研究场景词（如 resistance、therapy、prognosis）。
4. 时间约束：日报默认近24小时；周报默认聚合近7天日报；月报默认聚合近30天日报。
5. 结果质量优先：优先临床相关和证据等级更高文献。

检索式结构示例：
- `(主主题同义词1 OR 同义词2 OR 缩写) AND (研究场景词1 OR 场景词2)`

输出时需在首段附一行“本次检索式：...”。

## 强化规则（从 dailypaper 流水线迁移）

1. 最低数量补位
   - 当日高质量新增不足 TopN（默认3）时，自动从近7天窗口补位，直到凑满 TopN 或候选耗尽。
   - 补位文献必须与当日已选不重复。

2. 质量优先排序
   - 候选排序优先级：证据等级 > 临床相关性 > 方法创新度 > 新近性。
   - 同分时优先期刊分区更高者（SCI/Q 与中科院分区综合判断）。

3. 历史回填与防断更
   - 若当期（天/周/月）检索结果极少，允许从历史候选池回填，保证日报/周报/月报不断更。
   - 回填文献要显式标注“回填/补位”，避免与“当日新增”混淆。

4. 归档结构标准化（建议强制）
   - 每次日报输出后落盘一条结构化记录（JSON）：`topic/date/pmid/title/journal/sci/cas/cpu/evidence/score/summary/url`。
   - 周报/月报优先读取该结构化归档，不直接解析自然语言文本。

## 推荐输出模板（MDRGNB/HCC 通用）

- 本期新增数量（日报=今日，周报=本周，月报=本月）
- TopN（日报默认3 / 周报默认10 / 月报默认20；不足按实际）
- 每篇包含：
  - 标题
  - 期刊名（Journal）
  - PMID
  - 链接
  - 中科院分区（最新口径 + 最高分区；查不到写“待核实”）
  - SCI/JCR 分区（最新口径 + 最高分区；查不到写“待核实”）
  - 中国药科大学分级（CPU）
  - 80-120字中文摘要
  - 一句话临床/研究价值
  - 10问要点（1-10）
  - 四维评分（工程应用价值/架构创新/理论贡献/结果可靠性，1-10）+ 总评
  - 证据等级（Meta/RCT/观察/体外/综述/其他）
- 本期结论
- 下期建议（1-2条）

## 渠道映射（默认）

- 飞书：`channel=feishu`，`target=chat:<chatId>` 或 `user:<openId>`
- 企业微信：`channel=wecom`，`target=<userId|groupId>`
- QQ：`channel=qqbot`，`target=qqbot:c2c:<openid>` 或 `qqbot:group:<groupid>`
- Telegram：`channel=telegram`，`target=<chat_id>`

## Cron 模板（多渠道通用）

```json
{
  "action": "add",
  "job": {
    "name": "<daily|weekly|monthly>-<topic>-<channel>-<HHMM>",
    "schedule": { "kind": "cron", "expr": "<m> <h> * * *", "tz": "Asia/Shanghai" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "model": "openai-codex/gpt-5.3-codex",
      "timeoutSeconds": 1200,
      "message": "先检索文献并生成结构化快报，再使用 message 工具发送到指定渠道/目标（channel=<feishu|wecom|qqbot|telegram>, target=<ID>）。若正文过长则按2-3段发送（每段<=1200字），最后仅输出固定完成语。"
    },
    "delivery": { "mode": "none" }
  }
}
```

常用表达式（默认推送时间均为 08:00，可修改）：
- 日报：`0 8 * * *`
- 周报（本周最后一天）：`0 8 * * 0`（周日早8点）
- 月报（本月最后一天）：`0 8 28-31 * *` + 任务内校验“次日是否跨月，仅在跨月前一天发送”

默认联动创建策略：
- 创建日报时，同时创建同主题周报与月报。
- 若用户未指定时间：日报/周报/月报都默认 08:00；若用户指定时间，按用户时间覆盖默认值。
- 周报默认“本周最后一天 08:00”，月报默认“本月最后一天 08:00”；两者都允许单独修改并可独立启停。
- 若对应周报/月报已存在，则跳过创建并仅更新配置（避免重复任务）。
- 月报“月末发送”必须做二次校验：仅在“明天跨月”时真正发送，避免 28-31 多次触发。

## 故障处理

- 现象：`delivered` 但用户看不到全文
  - 强制改为 payload 内 `message.send` 分段发送
  - 先发一条短测试消息验证 target 可达
  - 再 `cron.run` 复测全文

- 现象：发送失败或超时
  - 降级顺序：全文分段 → 短摘要（Top3+链接）→ 告警消息（含失败原因与重试建议）
  - 每次失败都写入 run summary（便于追踪）

- 现象：QQ 与企业微信内容不一致
  - 使用同一“内容生成模板”，仅替换 `channel/target`

## 约束

- 不得只输出单个占位词（如 `mdrgnb`）
- 分区信息不确定时必须标 `待核实`，不得臆造
- 10问要点、四维评分、证据等级为固定输出项，不得省略
- 周报/月报必须优先基于已发布日报自动总结生成（聚合/归纳/趋势），不得默认改为重新检索替代
- 用户要求“保持一致”时，QQ 与企业微信正文结构必须一致
- 周报 Top10、月报 Top20 的每篇入选都应给出 1 行“入选理由”（如证据等级高/分区高/临床价值高）
