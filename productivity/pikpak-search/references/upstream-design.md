# 搜索：上游设计审阅与落地

## 正式发行与研读快照边界

截至 2026-10-16，经公开 GitHub `releases/latest` 元数据核验，下列正式发行均非 draft/prerelease；这里只核验 tag、公开 release URL 与发布时间（UTC），不证明该发行源码或实际运行兼容。

- **rclone/rclone**：[v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，发布于 `2026-10-09T11:03:19Z`。
- **52funny/pikpakcli**：[v0.23](https://github.com/52funny/pikpakcli/releases/tag/v0.23)，发布于 `2026-07-06T05:32:49Z`。

下文固定 commit 仅是研读快照；与上述 release tag 的祖先关系未核验，不能称为稳定发行源码。许可证依据仍以列出的具体快照文件为准，不把 release 元数据等同源码、许可或线上行为认证。

## 一手来源（固定修订）

1. **rclone/rclone**：MIT，公开 API 核验 60,328 stars，2026-10-15 仍活跃。
   - [PikPak listAll](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/pikpak.go#L769-L823)：`parent_id`、`page_token` 和 `next_page_token` 串联目录列表，远端错误直接上抛；支持逐项回调。它在空 `files` 时停止，不能直接照搬为“空页等于遍历完成”。
   - [lsjson ListJSONItem](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/fs/operations/lsjson.go#L20-L39)：目录/文件有显式 `IsDir`，大小、ID、时间和可选 Hashes 分开；目录不是“没有大小的文件”。
   - [MIT 原文](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING)。
2. **52funny/pikpakcli**：MIT，257 stars，2026-08-03 更新；[list 命令源码](https://github.com/52funny/pikpakcli/blob/560f263661fc55e40e508fe8e0d4b151c855dcbd/cli/list/list.go)、[许可证](https://github.com/52funny/pikpakcli/blob/560f263661fc55e40e508fe8e0d4b151c855dcbd/LICENSE)。它按远端路径工作，命令名为 `pikpakcli`，不是本项目依赖的 `pikpak ls --raw`；不能直接替换可执行文件或继承其参数语义。

## 适配决策与实质变化

| 机制 | 采纳 | 原因与实现 |
|---|---|---|
| lsjson 的显式目录类型 | 是 | walk 现在同时收集目录；JSON 保留 `kind`；file/folder/any 逐类过滤，修复 folder 返回后代文件。 |
| token 驱动分页 | 是，增强 | 每目录记录已见 token；重复 token、重复目录 ID、深度超限退出非零，不把局部结果报为完整。空页仍遵守 token。 |
| 引入整个 rclone 后端 | 否 | 现有 CLI 已是认证适配层；不增加 Go、依赖和第二套凭据。 |
| 第三方 CLI 直接替代 | 否 | 命令/响应契约不同，未经许可不能测试真实账户。 |

正则现在在扫描前编译校验；regex 参数整体保留空格，不再拆成多个 OR 词。普通关键词仍按空格分 AND/OR；limit/max-items 必须为正数。文档删除“服务端 API 已下线”断言：当前 CLI 不提供 search 不足以证明服务端关闭。

## 验收与未覆盖

`dev/test_maturity_data.py` 覆盖 folder ID、含空格正则、空盘坏正则先拒绝、重复 token；保留旧测试。补充严格页 schema、大小未知、稳定失败分类、私密报告独占创建及全树页数/扫描时间预算；fixture 参数按 `None` 区分未提供，显式空路径、读取/JSON/根节点错误均 fail-closed，不得回退 live。Python `re` 仍可能灾难回溯，扫描预算不保护正则执行，没有安全正则引擎，禁止将不可信表达式当作安全输入；大库性能、真实 JSON 契约、限流重试尚未认证。多页扫描不是时间点一致快照。
## 证据与法律边界

本次仅通过未认证的公开 GitHub HTTPS 读取源码和许可证；未安装、执行上游代码，未访问 PikPak 账号。GitHub 源码可证明其自身实现，不能证明本项目所调用的官方 `pikpak` CLI 与这些第三方项目的 JSON/下载行为兼容。fixture 是离线回归，不是线上兼容认证。只借鉴机制，未复制上游实现；将来复制代码须保留对应版权与许可证。
