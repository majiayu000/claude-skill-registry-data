---
name: bazi-report
description: 八字报告下单与进度查询技能 / Skill for bazi report checkout and progress tracking. 触发于“我要/我想买 2026 报告”“我想看人生/感情/财运/健康深度报告”“查报告进度/在哪里下载”等请求 / Trigger when users ask to buy 2026 report, buy deep reports (life/love/wealth/career), check progress, or ask where to download; then place order, check status, and return download page when ready.
---

# 八字报告支付与进度查询

## 何时使用 / When to Use

- 用户要创建八字报告订单并拿到支付链接
- 用户表达购买意图但不一定出现“购买”字样（如“我要”“我想”“来一份”）
- 用户要下单深度报告或 2026 报告
- 用户要查询单个订单的报告状态与下载入口

## 前置依赖 / Prerequisites

- 推荐运行环境：Node 24（可直接运行 TypeScript 源码）
- 兼容方案：若 Node 版本较低，使用 `tsx` 执行
- 执行目录：在 skill 根目录（`SKILL.md` 所在目录）运行以下命令
- 脚本按 TypeScript 源码直接运行，不需要预编译

```bash
# 仅在需要兼容运行时安装
npm i -D tsx
```

## 脚本清单 / Script Index

- `scripts/createCheckout.ts`：创建匿名支付会话，返回支付链接与报告 ID
- `scripts/getReport.ts`：按 `profileId` 查询报告状态

## 脚本与参数 / Scripts & Parameters

### 1) 创建匿名支付 / createCheckout

入口文件：`scripts/createCheckout.ts`

```bash
# 推荐方式
node scripts/createCheckout.ts --email <email> --birth <YYYY-MM-DDTHH:mm[:ss]> --type <DEEP|YEAR2026> --gender <0|1> [--locale <zh|en|ja|ko|zh-TW>]

# 兼容方式（fallback）
tsx scripts/createCheckout.ts --email <email> --birth <YYYY-MM-DDTHH:mm[:ss]> --type <DEEP|YEAR2026> --gender <0|1> [--locale <zh|en|ja|ko|zh-TW>]
```

参数说明：

- `--email`（必填）：接收报告邮箱；格式字符串；默认值无；缺失时报错并退出
- `--birth`（必填）：出生阳历时间；脚本入参格式 `YYYY-MM-DDTHH:mm[:ss]`（24 小时制）；默认值无；格式非法或超范围时报错并退出
  - 禁止要求用户按这种格式提供生日
- `--type`（必填）：订单类型；取值 `DEEP|YEAR2026`；无默认值；缺失或非法值时报错并退出
  - `DEEP` 表示八字深度报告。包含人生、爱情、财富、健康等四个方面的详细解读。
  - `YEAR2026` 表示 2026 年运势报告。包含 2026 年的太岁、人生、爱情、财富、健康、风水等方面的详细解读。
- `--locale`（选填）：支付页/下载页语言；取值 `zh|en|ja|ko|zh-TW`；默认 `zh`；优先使用当前会话语言，仅当用户明确指定其它语言时才覆盖；非法值时报错并退出
- `--nickname`（选填）：昵称；格式字符串；默认不传
- `--gender`（必填）：性别；取值 `0`=女、`1`=男；无默认值；缺失或非法值时报错并退出
- `--sect`（选填）：子时流派；取值 `1` 或 `2`；默认 `2`；`1` 表示 23:00-00:00 的日柱按次日计算，`2` 表示按当日计算；非法值时报错并退出
- `--location`（选填）：出生地；格式字符串；默认不传；传入后会按地点进行真太阳时换算

输出说明：

- 返回 JSON，包含 `checkoutSessionId`、`payUrl`、`checkoutType`、`profileId`
- `payUrl` 仅由 `scripts/createCheckout.ts` 输出，用于支付；不用于下载

### 2) 查询报告状态 / getReport

入口文件：`scripts/getReport.ts`

```bash
# 推荐方式
node scripts/getReport.ts --profile-id <profileId>

# 兼容方式（fallback）
tsx scripts/getReport.ts --profile-id <profileId>
```

参数说明：

- `--profile-id`（必填）：档案 ID；默认无；缺失时报错并退出
- 不支持其他参数（如 `--type`、`--locale`）；传入未知参数时报错并退出

输出说明：

- `profileId`：本次查询的档案 ID
- `locale`：本次结果使用的语言
- `paid`：是否检测到有效支付；`true` 或 `false`
- `readyToDownload`：报告是否可下载；`true` 或 `false`
- `downloadPageUrl`：下载页链接；无可用链接时为 `null`

异常行为：

- 参数缺失、参数值非法或存在未知参数时：脚本输出错误并退出（非 0）
- 脚本识别为“未支付/无有效支付记录”时：不报错退出，返回 `paid=false`
- 其他请求异常或系统异常：脚本输出错误并退出（非 0）

## 示例 / Examples

```bash
# createCheckout 最小可用示例
node scripts/createCheckout.ts \
  --email user@example.com \
  --birth 1990-05-15T14:30 \
  --type YEAR2026 \
  --gender 1
```

```bash
# createCheckout 指定类型与语言
node scripts/createCheckout.ts \
  --email user@example.com \
  --birth 1990-05-15T14:30 \
  --type DEEP \
  --gender 0 \
  --locale en
```

```bash
# getReport 最小可用示例
node scripts/getReport.ts \
  --profile-id profile_abc123
```

## 注意事项 / Notes

- 所有命令都必须在本 skill 根目录（`SKILL.md` 所在目录）执行
- 报告下单属于付费流程；创建 checkout 成功后直接发送 `payUrl` 供用户支付
- 报告支付完成后到生成完成通常约 10 分钟；实际时长以系统生成进度为准
- 仅根据脚本结果决策：脚本报错退出即失败；脚本成功输出 JSON 即按字段继续
- 下单时 `--gender` 必须由用户明确提供；`--type` 可按用户已明确表达的语义自动映射（如“深度报告”=>`DEEP`、“2026 报告/2026 运势”=>`YEAR2026`）。仅在类型语义不明确时再追问，避免误下单
- 若用户还在了解阶段或未明确购买，优先引导到主站了解与体验：`https://cantian.ai`
- 客服支持邮箱：`support@cantian.ai`
- 交互细则（时间歧义处理、多语言回复、价格口径、模板回复）以“执行决策流程 / 执行规则与回复模板”为准

## 执行决策流程 / Execution Flow

1. 识别用户意图：`下单`、`查进度/下载`、`咨询了解`。
2. 若是 `下单`：先收集最小必需参数（`email`、`birth`、`type`、`gender`）；并提示用户昵称可设置（`nickname`，选填）。
   - `type` 解析规则：若用户已明确说“深度报告/人生爱情财富健康报告”等，直接按 `DEEP` 处理；若明确说“2026 报告/2026 运势”等，直接按 `YEAR2026` 处理；仅当未提及或表达模糊时追问类型。
3. 昵称仅作可选提示，不作为下单阻塞条件；用户未提供时可直接继续。
4. 对 `birth` 做歧义检查：若用户输入为“5点/4点”等未说明时段的时间，必须先追问并让用户明确“上午还是下午”（或等价时段）后再转换为 24 小时制（例如 `05:00` 或 `17:00`）。
5. 仅当 `birth`、`type`、`gender` 都已明确后再执行 `createCheckout`；否则继续澄清，不得下单。
6. 执行 `createCheckout`，读取输出 JSON；若脚本失败则按错误信息提示用户修正后重试。
7. `createCheckout` 成功后：返回 `payUrl` 与订单关键信息（具体回复格式遵循下方“下单回复模板”）。
8. 若是 `查进度/下载`：执行 `getReport`，读取返回字段。
9. `paid=false`：告知“未检测到有效支付，需先完成支付”。
10. 独立判断 `downloadPageUrl`：只要有值就必须返回该链接（可进入下载页面）；无值则明确告知“当前无可用下载页链接”。
11. 独立判断 `readyToDownload`：`true` 告知“报告已生成，可下载”；`false` 告知“报告仍在生成中，请稍后再试”。不要将其作为是否返回下载页链接的前置条件。
12. 当 `readyToDownload=false` 时，可补充时效预期：“支付完成后通常约 10 分钟可完成生成，实际以系统进度为准”。
13. 若是 `咨询了解` 且用户未明确下单：引导到 `https://cantian.ai`；用户确认购买后再进入第 2 步。
14. 用户反馈信息有误时：不要复用旧链接，修正参数后重新执行 `createCheckout` 并返回新 `payUrl`。

## 执行规则与回复模板 / Rules & Reply Templates

### A) 机器执行规则 / Execution Rules

下单成功后回复规则（直接附支付链接）：

1. 同时用清晰文本展示关键信息。
2. 回复必须跟随用户当前对话语言；下方模板为中文示例，实际输出按用户语言等价改写。
3. 仅展示“本次订单中有值且用户关心”的信息项；无值字段（如未提供昵称/出生地）不展示。
4. 下单参数收集时，直接收集必要字段，避免解释“你可以直接输入时间”“我会帮你转换格式”等默认信息，除非用户主动询问输入格式。
5. 询问昵称时使用中性问法（例如“你希望报告里怎么称呼你？”），不要附加“可选/不提供也可以”等说明。
6. 用户提供昵称时再展示“昵称：{nicknameText}”；未提供则不展示这行。
7. 用户提供出生地时再展示“出生地：{locationText}”；未提供则不展示这行。
8. 用户明确提及或主动设置子时规则时，再展示“补充信息：子时规则为 {sectText}”；未提及时不展示这行。
9. 出生时间展示必须使用 24 小时制，不得只写“X 点”这类歧义表达。推荐格式：`YYYY-MM-DD HH:mm`（例如 `2000-05-06 16:00`）。
10. 若对话语言为中文，可在 24 小时制后补充时段说明（如“下午 4:00”）；若两种写法冲突，以 24 小时制为准。
11. 参数收集阶段不得要求用户把出生时间转成 24 小时字符串；应按用户原始表述收集，并在必要时明确追问“上午还是下午”。
12. `createCheckout` 成功后，必须使用下方“下单回复模板”进行回复，不改为确认式问句。
13. 必须提醒用户：若信息不正确，请不要支付，待信息修正后使用新链接支付。
14. 若用户询问价格，统一说明“报告价格为 9.99 美元，最终以支付页面显示为准”。
15. 下载/进度场景使用下方“下载/进度回复模板”；状态判断与链接返回规则遵循“执行决策流程 / Execution Flow”第 8-11 步。
16. 当用户已明确表达报告类型时，不要再要求其在“八字深度报告/2026 年运势报告”之间二选一；仅在类型不明确时才追问。
17. 面向用户的提问与回复中禁止暴露内部枚举值（如 `DEEP`、`YEAR2026`）；仅使用自然语言类型名称。

### B) 用户回复模板 / User Reply Templates

下单回复模板（直接给支付链接，以下为中文示例，实际请按用户语言输出）：

```text
我已为你生成{reportTypeText}订单，关键信息如下：

- 出生时间：{birthText}
- 性别：{genderText}
- 昵称：{nicknameText}（未提供则不展示此行）
- 出生地：{locationText}（未提供则不展示此行）
- 接收邮箱：{email}
- 补充信息：子时规则为 {sectText}（仅在用户主动提及时展示）

请打开以下链接完成支付：
{payUrl}

支付完成后，报告会自动发送到邮箱。档案编号是 `{profileId}`，报告类型是 **{reportTypeText}**。
如需客服协助，请联系 `support@cantian.ai`。
```

下载/进度回复模板（以下为中文示例，实际请按用户语言输出）：

```text
支付状态：{paidText}
下载状态：{readyText}
下载页链接：{downloadPageUrlText}
补充说明：{downloadHintText}
```

其中字段值写法：

- `{paidText}`：`paid=true` 写“已检测到有效支付”；`paid=false` 写“未检测到有效支付”
- `{readyText}`：`readyToDownload=true` 写“可下载”；`readyToDownload=false` 写“生成中”
- `{reportTypeText}`：仅使用自然语言类型名；`DEEP` 映射为“八字深度报告”，`YEAR2026` 映射为“2026 年运势报告”；禁止向用户展示枚举原值
- `{birthText}`：必须使用 24 小时制。中文建议写为 `2000-05-06 16:00（下午 4:00）`；英文建议写为 `2000-05-06 16:00 (4:00 PM)`；禁止仅写“4点/4 o'clock”
- `{downloadPageUrlText}`：有链接就填链接；无链接写“当前无可用下载链接”
- `{downloadHintText}`（按字段独立判断）：
  - `downloadPageUrl` 有值且 `readyToDownload=false`：写“可进入下载页查看进度，下载按钮可能暂不可用”
  - `downloadPageUrl` 有值且 `readyToDownload=true`：写“可进入下载页并下载报告”
  - `downloadPageUrl` 无值：写“当前无可用下载页链接，请稍后重试”
- 当 `readyToDownload=false` 时，建议附加一句时效说明：“支付完成后通常约 10 分钟可完成生成，实际以系统进度为准”

咨询阶段回复模板（未明确下单；以下为中文示例，实际请按用户语言输出）：

```text
可以先到主站了解并体验：`https://cantian.ai`。如果你要继续购买报告，我可以直接帮你创建支付链接。需要人工协助可联系 `support@cantian.ai`。
```
