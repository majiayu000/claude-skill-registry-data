# 批量备份：不覆盖、分阶段发布与校验等级

## 正式发行与研读快照边界

截至 2026-10-16，经公开 GitHub `releases/latest` 元数据核验，下列正式发行均非 draft/prerelease；这里只核验 tag、公开 release URL 与发布时间（UTC），不证明该发行源码或实际运行兼容。

- **rclone/rclone**：[v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，发布于 `2026-10-09T11:03:19Z`。
- **restic/restic**：[v0.19.1](https://github.com/restic/restic/releases/tag/v0.19.1)，发布于 `2026-07-05T08:13:33Z`。
- **52funny/pikpakcli**：[v0.23](https://github.com/52funny/pikpakcli/releases/tag/v0.23)，发布于 `2026-07-06T05:32:49Z`。

下文固定 commit 仅是研读快照；与上述 release tag 的祖先关系未核验，不能称为稳定发行源码。许可证依据仍以列出的具体快照文件为准，不把 release 元数据等同源码、许可或线上行为认证。

## 一手源码与许可

1. **rclone/rclone**，MIT，60,328 stars，2026-10-15 活跃：
   - [check.go](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/fs/operations/check.go#L274-L295) 区分大小比较和共同 hash；无可比 hash 不是已验证内容。
   - [PikPak Hashes/Object.Hash](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/pikpak.go#L1873-L1878) 支持的是 `md5_checksum`；[File.Hash](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/api/types.go#L188-L215) 注释为自定义 GCID 形式。不能拿看似 SHA-1 的 `hash` 直接与本地 SHA-1 比较。
   - [copy.go](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/cmd/copy/copy.go) 是复制语义，不是快照/版本化备份或全树事务；[许可证](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING)。
2. **restic/restic**，BSD-2-Clause，36,607 stars，2026-10-11 活跃：
   - [fileswriter.openFile](https://github.com/restic/restic/blob/9da3b87b07706956e8dc5fd5cb259b99ec940f51/internal/restorer/fileswriter.go#L90-L149) 使用 O_NOFOLLOW、fstat 常规文件检查、O_EXCL；说明仅清洗字符串不是路径安全。
   - [Restorer 覆盖策略](https://github.com/restic/restic/blob/9da3b87b07706956e8dc5fd5cb259b99ec940f51/internal/restorer/restorer.go#L50-L75) 将 never/changed 等策略显式化；[verifyFile 调用](https://github.com/restic/restic/blob/9da3b87b07706956e8dc5fd5cb259b99ec940f51/internal/restorer/restorer.go#L564-L582) 说明恢复前匹配需内容验证。
   - [许可证](https://github.com/restic/restic/blob/9da3b87b07706956e8dc5fd5cb259b99ec940f51/LICENSE)。restic 有意允许部分覆盖/替换，本脚本不复制此行为，也不宣称实现 restic 的内容寻址、快照恢复或全树原子性。
3. **52funny/pikpakcli**，MIT：[下载实现](https://github.com/52funny/pikpakcli/blob/560f263661fc55e40e508fe8e0d4b151c855dcbd/internal/api/download.go#L78-L185) 确实有 Range/206、416、服务器忽略 Range 时重启和预期大小检查。但这是另一个 CLI，不证明官方 `pikpak download` 实现续传；本脚本不以该证据宣称支持续传。[许可证](https://github.com/52funny/pikpakcli/blob/560f263661fc55e40e508fe8e0d4b151c855dcbd/LICENSE)。

## 本次落地与取舍

- 下载前完整规划，检测清洗、NFC/大小写、文件/目录前缀碰撞，保留 backup_manifest.json；碰撞拒绝而非悄悄改名造成来源混淆。
- 拒绝已有目标（含同长文件）及清单，不覆盖或按大小跳过。现有脚本无可信来源绑定，宁可要求新目录，也不假装增量/幂等恢复。
- 下载到目标根中的私有临时目录，以 O_NONBLOCK|O_NOFOLLOW 打开暂存文件，fstat 先拒 FIFO/设备/目录等非普通文件，验证精确大小后在安全 fd 上 `fchmod(0600)`，再计算本地 SHA-256，最后用硬链接原子发布；若目标在下载期间出现，link 失败，不覆盖，umask 不会放宽最终模式。
- 清单同样以 O_EXCL|O_NOFOLLOW 安全 fd 暂存、fchmod(0600)、fsync、不可覆盖发布；失败退出非零，短文件不进入最终名称。仅清理本次私有临时数据，不删除用户文件或云端内容。
- 清单明确 `remote_integrity=unverified`、`verification=size_only`；本地 SHA-256 是后续损坏检测基线，不证明远端字节等同。未实现远端 MD5/GCID 核验、字节续传、检查点恢复、增量对比或版本化备份；已删除相关宣传。

## 验证与未认证边界

离线测试真实落中性临时文件，CLI 仅 mock：符号链接外写拒绝、名称碰撞、保留清单名、短下载非零、不覆盖已有文件、成功文件 SHA-256、umask=022 下下载文件和清单仍为 0600、显式空 fixture/dry-run 不回退 live。补充严格页 schema、失败分类不复述 CLI 原文、全树页数/扫描时间预算和 1 秒硬边界非普通暂存文件回归。没有真实网络下载/故障恢复认证。POSIX/同文件系统 hardlink 是当前实现前提；FAT/exFAT 等不支持 hardlink 时会安全失败，不承诺跨平台。无总树事务、崩溃恢复、磁盘配额预估、并发目录恶意重命名防护或完整目录空树恢复，不能称为成熟可靠备份系统。
## 证据与法律边界

本次仅通过未认证的公开 GitHub HTTPS 读取源码和许可证；未安装、执行上游代码，未访问 PikPak 账号。GitHub 源码可证明其自身实现，不能证明本项目所调用的官方 `pikpak` CLI 与这些第三方项目的 JSON/下载行为兼容。fixture 是离线回归，不是线上兼容认证。只借鉴机制，未复制上游实现；将来复制代码须保留对应版权与许可证。
