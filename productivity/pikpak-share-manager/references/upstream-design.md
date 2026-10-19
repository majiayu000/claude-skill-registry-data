# 分享审计：完整性、时间与字段边界

## 正式发行与研读快照边界

截至 2026-10-16，经公开 GitHub `releases/latest` 元数据核验，下列正式发行均非 draft/prerelease；这里只核验 tag、公开 release URL 与发布时间（UTC），不证明该发行源码或实际运行兼容。

- **rclone/rclone**：[v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，发布于 `2026-10-09T11:03:19Z`。
- **52funny/pikpakcli**：[v0.23](https://github.com/52funny/pikpakcli/releases/tag/v0.23)，发布于 `2026-07-06T05:32:49Z`。
- **Quan666/PikPakAPI**：[0.1.11](https://github.com/Quan666/PikPakAPI/releases/tag/0.1.11)，发布于 `2025-02-11T12:42:10Z`。

下文固定 commit 仅是研读快照；与上述 release tag 的祖先关系未核验，不能称为稳定发行源码。许可证依据仍以列出的具体快照文件为准，不把 release 元数据等同源码、许可或线上行为认证。

## 一手来源（固定修订）

1. **rclone/rclone**（MIT，60,328 stars）：[RequestShare](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/api/types.go#L485-L491) 的 `expiration_days=-1` 是**创建请求**中的永久语义，`pass_code_option` 为独立字段；[许可证](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING)。不能据此把分享列表缺 `expiration` 推断为永久，也不能从上传凭据 ResumableParams 的 `expiration` 推导分享审计 schema。
2. **52funny/pikpakcli**（MIT，257 stars）：[share 命令](https://github.com/52funny/pikpakcli/blob/560f263661fc55e40e508fe8e0d4b151c855dcbd/cli/share/share.go#L14-L68) 是按路径分享链接输出，并没有本项目 `share ls -F json` 审计接口；[许可证](https://github.com/52funny/pikpakcli/blob/560f263661fc55e40e508fe8e0d4b151c855dcbd/LICENSE)。直接替换 CLI 会错误理解 ID/路径，不采用。
3. **Quan666/PikPakAPI**：[file_batch_share](https://github.com/Quan666/PikPakAPI/blob/c233bd3db99ecd49fe2e42ec8a2d83072e3a9432/pikpakapi/__init__.py#L854-L885) 与 [get_share_info](https://github.com/Quan666/PikPakAPI/blob/c233bd3db99ecd49fe2e42ec8a2d83072e3a9432/pikpakapi/__init__.py#L952-L978) 可交叉核验创建/读取是不同响应。[pyproject.toml](https://github.com/Quan666/PikPakAPI/blob/c233bd3db99ecd49fe2e42ec8a2d83072e3a9432/pyproject.toml) 明确声明 **GPL-3.0-only**，虽然 GitHub license API 返回 null、树中没有 LICENSE；不能据 API null 推断“无许可证”。220 stars、最后更新 2025-02-11，已陈旧；本次只阅读、不复制或依赖，避免混入本项目未评估的 GPL 分发义务。其创建结果文档并不能证明 owner 的分享列表存在 `views/created/expiration`。

## 采用的设计

1. 只有 token 耗尽才返回成功。重复 token、重复/缺失 ID、20 页后仍有 token 都退出非零，不输出貌似完整的报告或撤销建议；不把页数上限当完成条件。
2. UTC 时间解析 ISO 和显式秒/毫秒：`s:`/`ms:` 优先，`--epoch-unit` 作用于无前缀数值；auto 优先可表示的秒，否则尝试毫秒。两种单位都可表示时必须告知歧义，不能用 1e9/1e12 阈值猜测；覆盖 0、早期和阈值两侧，范围/Decimal 溢出为未知，拒绝 NaN/Infinity/布尔值。`expiration <= now` 为过期，临期用精确 timedelta(7天)，不再用 `.days` 向下取整成“接近8天”。`audit(now=...)` 可注入固定时钟，新增测试不依赖今天。
3. 缺失 expiration 标未知；只有本适配器显式 -1 才解释为长期有效。views/files 仅接受非布尔非负原生整数，其余为 JSON null；嵌套 JSON 不透传。原始页/完整 fixture 分别验证 schema，显式空 fixture 与坏路径/坏 JSON/null/坏根结构均拒绝且不回退 live；CLI 失败不转发原文，报告默认 0600/独占创建，--overwrite 需额外授权。未知统计不等于零访问；真实 CLI 字段未认证必须告知用户。CLI `--now` 与报告 `audited_at` 保留精确判断基准。
4. 脚本保持 share ls 只读；不执行 create/rm/restore，也不生成 shell 撤销命令，标题与 ID 以 JSON 转义展示，防止远端换行/命令片段污染建议。自动清理、续期、批量撤销不是本产品能力。

## 验证与剩余

新 unittest 用固定 UTC 时间、mock 分页，验证边界和超限 fail-closed；旧测试保留。官方 CLI help 只能证明 flags，不证明 raw JSON 字段，故真实分享列表 schema、永久哨兵、浏览计数含义、创建/撤销生效仍未验证；不得把 fixture 宣传为线上闭环。
## 证据与法律边界

本次仅通过未认证的公开 GitHub HTTPS 读取源码和许可证；未安装、执行上游代码，未访问 PikPak 账号。GitHub 源码可证明其自身实现，不能证明本项目所调用的官方 `pikpak` CLI 与这些第三方项目的 JSON/下载行为兼容。fixture 是离线回归，不是线上兼容认证。只借鉴机制，未复制上游实现；将来复制代码须保留对应版权与许可证。
