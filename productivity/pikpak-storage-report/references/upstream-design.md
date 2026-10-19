# 上游机制核验与本次落地

## rclone/rclone：结构化清单与大小统计

固定快照 `d369079a1448c487d09d85bfe11382e16ea4e345`。API 当次返回 60328 stars、pushed_at `2026-10-15T16:41:49Z`。仅阅读公开 GitHub，不安装或运行 rclone，不使用本地/真实 PikPak 账号。

- [lsjson 数据结构](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/fs/operations/lsjson.go#L20-L34)：Path、Name、Size、IsDir、ID 保留可程序复核的身份与原始字节信息。
- [ListJSON 错误传播](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/fs/operations/lsjson.go#L244-L267)：遍历错误向上传递，不输出伪完整统计。
- [size 命令源码](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/cmd/size/size.go#L39-L81)：结果区分 Count、Bytes、Sizeless；未知大小使总量可能低估，并单独告警，而不是默认为可靠的 0 字节。
- [lsjson 递归/深度文档](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/docs/content/commands/rclone_lsjson.md#L99-L118)：这里只对照上游 list 命令的默认递归、`--max-depth` 和 `-R` 扫描边界，不证明本地“展示深度独立于扫描深度”的机制。本地依据是 `scripts/storage_report.py` 的 `run_main`：`walk_tree` 不接收 `args.depth`，仅 `print_tree` 使用它；离线测试 `test_storage_display_depth_does_not_limit_scan_or_total` 另行核验总量不随展示深度变化。

## 采纳 / 拒绝

**采纳**：结构化 TOP 文件保留 ID/path/size/time；枚举完成与体积完整分开；已知大小求和加 unknown 计数；扫描失败非零，不把坏 JSON/权限错误当空目录；按 ID 去重避免重复计费。

**拒绝**：不把本地磁盘或 rclone 的 totals 当 PikPak 服务端配额；不自动接入 rclone native backend，也不硬加 Go/Rust/存储适配层。账号总览未查询时明确 null/not_queried，不凭 fixture 编造容量/会员。Czkawka 的本地内容查重不适合作云盘配额计量，未纳入本脚本执行路径。

## 许可与发行边界

- **rclone**：固定快照的 [COPYING](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING) 已核验为 MIT 许可文本，要求在副本或实质部分保留版权及许可声明；不是仅凭仓库热度猜许可。
- **Czkawka（仅作对照，未采纳执行路径）**：固定 [czkawka_core/Cargo.toml:8](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/czkawka_core/Cargo.toml#L8) 明示 core 的 `license = "MIT"`；固定 [README 许可说明](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/README.md#L197-L203) 将 core/CLI/GTK 列为 MIT，图像/声音为 CC BY 4.0，Krokiet/Cedinia 因 Slint 为 GPL-3.0-only。本技能未采用其内容查重能力计量云端配额，不将组件许可扩大成“整个仓库一律 MIT”；GUI/图音资源也未复制或执行。
- 本技能只借鉴机制、独立实现，未引入或运行上游程序、未复制其源码或图音资源。以后复用实质代码/资源必须按实际组件许可保留相应声明/署名，并重新审查依赖，不能将引用当作无限制复用授权。
- 公开发行已核验：rclone [v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，发布于 `2026-10-09T11:03:19Z`；Czkawka [12.0.2](https://github.com/qarmin/czkawka/releases/tag/12.0.2)，发布于 `2026-09-09T19:48:14Z`。这是 2026-10-16 的发行元数据核对，不是运行验收；研读快照与发行 tag 的祖先关系未验证，不宣称 snapshot 等于 release。

## 本次落地

1. 修复 ST-01：逐目录 token 环检测、活动祖先目录环检测、全局文件/目录 ID 去重；文件默认 50000（`--max-items`）、文件夹 5000、页 10000、活动目录深度 100 的边界。`--depth` 仅为展示深度；它不减少全树扫描，缩小范围应使用 `--folder`。
2. 文件/目录共用 ID 身份/关键证据索引，只有一致重复才合并；kind/name/size/hash/params/时间冲突报 identity_conflict，整份报告不发布树或排行。缺页、坏响应、CLI 错误、预算、坏输入/配置/时间或展示失败统一退出 2、输出 complete=false，能写时覆盖旧报告，不可写时失败 JSON 改送 stdout 并禁用旧目标。CLI 原 stdout/stderr 不回显；null/非对象 fixture 不回退 live；预算截断另标 truncated=true。
3. 修复 ST-02：JSON 增加排序后的 `top_files`（跟随 `--top`，0 为空）、`account_overview=null`、`account_overview_status=not_queried`、展示深度以及完整性字段；不偷偷查询账号。
4. 无法识别的 size（含缺失/负数/带单位字符串/布尔值）保留 null，统计 `unknown_size_files`、`total_size_is_lower_bound`，目录带 `size_complete`；可枚举完整但体积仅为下界。未知大小不能在大文件榜宣称为已知 0。

## 输入与资源边界

可选时间缺失/null 归一为空串，其他值必须为有效 ISO 字符串；PIKPAK_TIMEOUT 只接受 1–86400 整数秒。独立测试入口和 unittest 加载入口均进入 offline_environment，并硬阻断底层 subprocess/Popen/socket/urlopen/通知入口；测试仅使用中性 fixture、临时文件和底层模拟响应，无真实 CLI 进程。计数预算不等于内存或总墙钟预算。

输入文件（fixture；ad-cleaner/dedup 另含冻结报告）使用 `O_NONBLOCK | O_NOFOLLOW` 打开，再以 fstat 拒绝非普通文件、非当前有效用户所有、多个硬链接和组/其他用户可写的文件；最终路径 symlink、FIFO、设备、目录均拒绝，不修改输入权限。普通中性 `0644` 与私有 `0600` 输入均可用，不强制输入 0600；真实私密数据仍应放入受控私有目录。父目录 symlink/恶意本地竞态不在隔离保证内。文件读入上限 **16 MiB（16777216 字节）**，按描述符有界读取；fixture、单次 live CLI JSON、冻结报告解析前均限制对象/数组容器嵌套深度 **64**（含根，忽略字符串内括号/转义）。超限/坏 JSON 安全分类为 `INVALID_FIXTURE` / `INVALID_CLI_JSON` / `INVALID_REPORT`，退出 2；扫描失败使可写目标 `complete=false`，冻结批准失败不输出命令、不扩大批准。

报告输出已在成功/失败路径拒绝 symlink、非普通文件和多个硬链接，截断前强制 `0600`；这不等于原子替换或生产验收。尚无原子写、全局墙钟期限/取消或恢复检查点。CLI stdout/stderr 仍先完整捕获，再检查单页 JSON 字节数；无 CLI 捕获期总字节/RSS 上限、展示输出字节上限或全任务累计输入预算。普通文件系统 I/O 没有墙钟截止；O_NONBLOCK 不承诺慢磁盘/网络文件系统不阻塞。

## 验证与边界

`python3 dev/test_maturity_cleanup.py` 独立中性 fixture/mock 测试覆盖重复 ID 不重复计数/计字节、缺页/目录环/token、预算、CLI 失败、TOP ID/path 顺序与未知大小。`--json -` 可直接 JSON 解析。

尚未验证真实 JSON schema/分页/存储计费、回收站与实际释放容量；未实现账号总览自动抓取、原子写、全局墙钟期限和恢复检查点；0600 报告权限和目标类型保护已实现。扫描快照可能受并发变更影响，不等价于原子服务端快照。
