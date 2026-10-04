---
name: stylework-yunxiao-requirement-sync
description: "StyleWork 云效需求同步 / 云效导出到钉钉表格：当用户要把云效某个月或某批需求导出为 Excel，并复制到已有钉钉在线表格的新 Sheet，按迭代排序、分组留空、设置黄色加粗表头、冻结首行和置顶时使用。也适用于登录过期后扫码继续、用户直接提供本地 Excel、或检查本次同步结果。V1 只做云效到钉钉，不用于需求排期判断、钉钉反向写回云效、创建新的钉钉文件或修改已有 Sheet。"
---

# StyleWork 云效需求同步

## Overview

把用户指定的云效需求视图通过界面导出，转换成固定字段和迭代分组，再写入已有钉钉表格的一个新 Sheet。这个 Skill 有外部写入副作用，必须先完成本地预检，再创建 Sheet；不得覆盖或修改旧 Sheet。

## Hard Boundaries

- V1 只执行“云效 -> 钉钉”，不把钉钉内容写回云效。
- 内置浏览器只负责云效页面、登录和 Excel 导出；不得自行抓取云效分页接口或私有 API 替代导出。
- 钉钉文档探测、新建 Sheet、写入、设样式、冻结和置顶只能使用 `dws`。
- DWS 缺能力或失败时不得改用浏览器、`curl`、HTTP API、人工复制粘贴或其他写入方式绕过。
- 不创建新的钉钉文件，只在用户给定的现有在线表格中新增 Sheet。
- 用户未明确要求执行同步时，只给预检或说明，不产生外部写入。

## Context Intake

按以下优先级取得云效视图 URL 和钉钉表格 URL：

1. 当前用户消息中的明确 URL；
2. `$HOME/Documents/Codex/stylework-yunxiao-requirement-sync.local.json` 的 `yunxiao_view_url` 与 `dingtalk_sheet_url`；
3. 缺少时各问一次，不猜测、不搜索历史浏览记录。

月份优先取用户明确指定的目标月份；否则从导出数据的迭代字段推断。存在多个月份且用户未指定时，在写入前询问一次。浏览器导出不可用时，接受用户给出的本地 Excel。

## Fixed Field Contract

读取 `references/field-contract.md`。最终列顺序严格为：

`标题、负责人、创建者、迭代、技术难度、优先级、客户名称、URL`

- 不包含 `父ID`。
- 不包含 `描述`。
- `创建者` 不得改成 `创建人`。
- 不得去重、合并相似标题或擅自过滤行。
- 缺失非关键值保持空白，不补造描述、难度、优先级、客户或负责人。

## Workflow

### 1. Load tool contracts

执行前读取当前运行时的 `browser:control-in-app-browser`、`spreadsheets` 和 `dws` Skill。实际浏览器自动化前必须读取内置浏览器的实时工具文档；不要依赖过期 selector 或截图坐标。

### 2. Export from Yunxiao

1. 在内置浏览器打开目标视图并确认当前筛选范围与目标月份一致。
2. 若登录失效，暂停并请用户在内置浏览器扫码；用户确认完成后继续当前步骤，不重启整套流程。
3. 通过云效界面打开导出，选择固定 8 个字段并下载 Excel。
4. 浏览器导出失败时报告原因，并切换为等待用户提供本地 Excel；不得私自调用云效 API。

### 3. Preflight and transform locally

用 Spreadsheets 能力读取 Excel，按 `references/field-contract.md` 生成一个只含 8 列的 CSV 中间文件：

1. 校验表头、原始数据行数、空标题、空迭代、空 URL 和迭代格式。
2. 解析 `YY.M.W`，按年份、月份、周次升序排序；同迭代内保持原始顺序。
3. 不同迭代之间插入恰好 3 个空行。
4. 未知迭代、目标月份外迭代或关键字段缺失时，不得静默放到末尾；先输出异常报告并等待用户决定。
5. 输出写入预览：目标月份、8 个表头、源数据行数、各迭代数量、空行数量、预计写入范围和异常数。

只有预检无阻塞异常时才进入钉钉写入。

### 4. Probe DingTalk and select a new name

读取 `references/sync-playbook.md` 并严格使用其中的 DWS 命令。

1. 对原始 `/i/nodes/` URL 先运行 `dws doc info`，确认类型为在线表格（`ALIDOC/axls`）。
2. 运行 `dws sheet list` 获取现有名称。
3. 基础名为 `智能体{M}月需求-MMDD`。
4. 同名时改为 `智能体{M}月需求-MMDD-HHmm`；若仍冲突则停止，不覆盖、不删除旧 Sheet。

所有 DWS 调用必须带 `--format json`。命令失败时只允许增加 `--verbose` 原样重试一次；第二次仍失败即停止并报告。

### 5. Create, write, and style

按顺序执行：

1. 新建选定名称的 Sheet，并记录返回的稳定 Sheet ID。
2. 用 `dws sheet csv-put` 从 `A1` 写入完整 CSV。
3. 对 `A1:H1` 设置背景色 `#FCC102` 和加粗。
4. 用一次 `dws sheet update` 设置冻结首行并把 Sheet 移到最前。

若新建后某一步失败，不删除 Sheet。报告成功步骤、失败步骤、Sheet 名称与 ID；经用户再次明确要求后才继续修复半成品。

### 6. Read back and verify

至少验证：

- `dws sheet info` 返回预期名称、`frozenRowCount=1` 和 `index=0` 或等价字段；
- `dws sheet range read` 返回 8 个正确表头；
- 读回数据行数、迭代顺序和 3 个空行分隔与本地预览一致；
- 样式命令成功返回，表头范围是 `A1:H1`。

不能取得读回证据时，不得声称同步完成。

## Output Contract

完成时报告：

- 来源：云效导出或本地 Excel；
- 目标 Sheet 名称与 ID；
- 8 个字段；
- 原始需求行数、写入总行数、迭代分组计数；
- 排序、3 个空行、表头色、加粗、冻结和置顶的验证结果；
- 被保留的空值、异常和未完成步骤。

阻塞时只报告已完成到哪一步、阻塞原因、需要用户做的一个动作和可恢复点。

## Future Reverse Sync

未来可在同一操作型 Skill 中扩展“钉钉 -> 云效”，但必须通过 URL 定位需求、先展示逐字段差异并获得明确确认后写回。V1 不提供该能力，也不得暗示已经支持。

## Definition of Done

- 来源范围和目标月份已确认。
- 固定 8 列与源数据行数通过预检，无静默去重或字段改名。
- Sheet 使用不覆盖旧数据的唯一名称创建。
- 数据、迭代排序和 3 个空行已读回验证。
- 表头 `#FCC102`、加粗、冻结首行和移到最前均有命令证据。
- 全程遵守浏览器、Spreadsheets、DWS 的工具边界。

## Resource Guide

- `references/field-contract.md`：字段、排序、空行和异常处理规则。
- `references/sync-playbook.md`：DWS 命令顺序、重试和读回验证。
- `evals/evals.json`：触发、非触发与历史失败回归场景。
