---
name: gog-zh
description: Google Workspace 命令行工具，用于 Gmail、日历、云盘、联系人、表格和文档。
homepage: https://gogcli.sh
metadata: {"clawdbot":{"emoji":"🎮","requires":{"bins":["gog"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/gogcli","bins":["gog"],"label":"安装 gog (brew)"}]}}
---

# gog

使用 `gog` 管理 Gmail/日历/云盘/联系人/表格/文档。需要 OAuth 设置。

设置（一次性）
- `gog auth credentials /path/to/client_secret.json`
- `gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs`
- `gog auth list`

常用命令
- Gmail 搜索: `gog gmail search 'newer_than:7d' --max 10`
- Gmail 发送: `gog gmail send --to a@b.com --subject "主题" --body "正文"`
- 日历: `gog calendar events <calendarId> --from <iso> --to <iso>`
- 云盘搜索: `gog drive search "查询内容" --max 10`
- 联系人: `gog contacts list --max 20`
- 表格读取: `gog sheets get <sheetId> "工作表!A1:D10" --json`
- 表格更新: `gog sheets update <sheetId> "工作表!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED`
- 表格追加: `gog sheets append <sheetId> "工作表!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS`
- 表格清除: `gog sheets clear <sheetId> "工作表!A2:Z"`
- 表格元数据: `gog sheets metadata <sheetId> --json`
- 文档导出: `gog docs export <docId> --format txt --out /tmp/doc.txt`
- 文档查看: `gog docs cat <docId>`

注意事项
- 设置 `GOG_ACCOUNT=you@gmail.com` 环境变量以避免重复使用 `--account` 参数。
- 编写脚本时，建议使用 `--json` 参数和 `--no-input` 参数。
- 表格数据可以通过 `--values-json` 参数传递（推荐）或作为行内数据。
- 文档支持导出/查看/复制。原地编辑需要 Docs API 客户端（gog 中不包含）。
- 发送邮件或创建事件前请确认。
