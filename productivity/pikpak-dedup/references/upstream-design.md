# 上游机制核验与本次落地

## 已核验来源

只读公开 GitHub，不安装依赖或运行上游二进制；不访问 PikPak 真实账号。

### qarmin/czkawka

固定快照 `eb8b91dbb4d25dff416202674ee0de84ee4b5e5c`；API 当次 34279 stars、pushed_at `2026-09-16T17:34:11Z`。

- [核心说明 37–47 行](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/instructions/Instruction_Core.md#L37-L47)：name、size、size+name 都不是可靠内容重复；hash 模式先按 size 分组，再预哈希筛选，最后完整内容哈希。
- [实际源码 Name/SizeName/Size 路径](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/czkawka_core/src/tools/duplicate/core.rs#L41-L208)：独立 checking method，不把名称匹配伪装为完整哈希匹配。
- [prehash 到 full hashing](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/czkawka_core/src/tools/duplicate/core.rs#L361-L460) 与 [hash 模式入口](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/czkawka_core/src/tools/duplicate/core.rs#L679-L695)：预筛选不是最后证据。

**采纳**：证据等级隔离、同内容证据必须兼容字节大小、人工候选与精确重复明确区分。

**拒绝**：不把本地 Czkawka 宣称为直接支持 PikPak；不为查重下载真实内容，不加入挂载/预哈希/内容哈希执行引擎或新增依赖。跨名称的完整内容查重尚未实现。

### rclone/rclone

快照 `d369079a1448c487d09d85bfe11382e16ea4e345`；API 当次 60328 stars、pushed_at `2026-10-15T16:41:49Z`。

- [CheckHashes](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/fs/operations/operations.go#L48-L122)：选择共同支持的 hash 类型；空 hash 返回 HashNone。注意其同步逻辑中的 equal=true + HashNone 是回退信号，不是内容重复证明，不能照搬为删除判据。
- [lsjson 类型与 hash 填充](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/fs/operations/lsjson.go#L221-L230)：hash 按算法命名且可缺失。

**采纳**：原始 opaque `hash` 仅作元数据线索，不因字符串相同就声称“完全重复”。**拒绝** rclone checksum 不足时回退 size-only 的同步策略用于清理判断；不改用 rclone backend 接入账号。

## 许可与发行边界

- **rclone**：固定快照的 [COPYING](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING) 已核验为 MIT 许可文本，要求在副本或实质部分保留版权及许可声明；不是仅凭仓库热度猜许可。
- **Czkawka 的 core 机制**：固定 [czkawka_core/Cargo.toml:8](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/czkawka_core/Cargo.toml#L8) 明示 `license = "MIT"`；固定 [README 许可说明](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/README.md#L197-L203) 将 core/CLI/GTK 列为 MIT，图像/声音为 CC BY 4.0，Krokiet/Cedinia 因 Slint 为 GPL-3.0-only。这里采纳的是 core 的证据分级思路，不将组件许可扩大成“整个仓库一律 MIT”；未纳入的 GUI/资源也未复制或执行。
- 本技能只借鉴机制、独立实现，未引入或运行上游程序、未复制其源码或图音资源。以后复用实质代码/资源必须按实际组件许可保留相应声明/署名，并重新审查依赖，不能将引用当作无限制复用授权。
- 公开发行已核验：rclone [v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，发布于 `2026-10-09T11:03:19Z`；Czkawka [12.0.2](https://github.com/qarmin/czkawka/releases/tag/12.0.2)，发布于 `2026-09-09T19:48:14Z`。这是 2026-10-16 的发行元数据核对，不是运行验收；研读快照与发行 tag 的祖先关系未验证，不宣称 snapshot 等于 release。

## 本次代码落地

- 修复 DD-01：先按视频/音频兼容家族隔离，PDF/ZIP/字幕/未知类型不参与版本候选；相同归一名称的文档不能成为影片清理项。
- 每组明确 `match_type=name_candidate`、`exact=false`；记录 `same_size`、`remote_hash_match`、`hash_algorithm_verified=false`。远端 hash 相同但大小不同不算匹配；大小和 opaque hash 都相同仍不升级精确重复。
- highest-res 统一比较长边，再按大小/时间排序，不只比宽度；width/height 仅接受 1–2147483647 的整数或纯 ASCII 十进制数字串（允许前导零）。零/负数/浮点/布尔/单位/空白/容器/超范围和缺失值保留未知；两维均有效才输出分辨率，绝不抽取字符串片段造像素。组内任一项未知（包括已知与未知混合）就放入 unassessed_groups，reason=unknown_resolution、keeper=null、trash_candidates=[]、analysis_complete=false；该组 ID 不在冻结批准候选内。newest/largest 不隐式改策略，只依照其自身指标。它仍是元数据启发式，不保证真实画质。
- token/目录环终止；文件/目录共用身份索引，仅一致重复合并，身份/关键证据冲突使整份报告 incomplete、禁止命令。null/非对象 fixture 不回退 live；时间/配置/输入/展示失败从统一出口给失败 JSON，能写入时覆盖旧报告，不可写时明确禁用旧目标。CLI 错误只给分类/退出码、不回显原 stdout/stderr。保留页/目录深度/文件/文件夹预算与 `--json -` 纯 JSON。
- 字节解析仅接受非负整数或纯数字串；未知保留 null 与独立 size_complete/analysis_complete，不由 0 或坏字符串数字伪造证据。未知文件放 unassessed_files，同名组含未知大小放 unassessed_groups，不给 keeper 或清理候选；三个策略均不对其作确定性选择。
- SHA-256 绑定冻结报告与逐 ID 批准；keeper 永不进入批准清理范围；报告变化、非候选、非安全 ID 均整批拒绝；仅打印命令，不扫描后扩大授权，也不执行删除。

## 输入与资源边界

可选时间缺失/null 归一为空串，其他值必须为有效 ISO 字符串；PIKPAK_TIMEOUT 只接受 1–86400 整数秒。独立测试入口和 unittest 加载入口均进入 offline_environment，并硬阻断底层 subprocess/Popen/socket/urlopen/通知入口；测试仅使用中性 fixture、临时文件和底层模拟响应，无真实 CLI 进程。计数预算不等于内存或总墙钟预算。

输入文件（fixture；ad-cleaner/dedup 另含冻结报告）使用 `O_NONBLOCK | O_NOFOLLOW` 打开，再以 fstat 拒绝非普通文件、非当前有效用户所有、多个硬链接和组/其他用户可写的文件；最终路径 symlink、FIFO、设备、目录均拒绝，不修改输入权限。普通中性 `0644` 与私有 `0600` 输入均可用，不强制输入 0600；真实私密数据仍应放入受控私有目录。父目录 symlink/恶意本地竞态不在隔离保证内。文件读入上限 **16 MiB（16777216 字节）**，按描述符有界读取；fixture、单次 live CLI JSON、冻结报告解析前均限制对象/数组容器嵌套深度 **64**（含根，忽略字符串内括号/转义）。超限/坏 JSON 安全分类为 `INVALID_FIXTURE` / `INVALID_CLI_JSON` / `INVALID_REPORT`，退出 2；扫描失败使可写目标 `complete=false`，冻结批准失败不输出命令、不扩大批准。

报告输出已在成功/失败路径拒绝 symlink、非普通文件和多个硬链接，截断前强制 `0600`；这不等于原子替换或生产验收。尚无原子写、全局墙钟期限/取消或恢复检查点。CLI stdout/stderr 仍先完整捕获，再检查单页 JSON 字节数；无 CLI 捕获期总字节/RSS 上限、展示输出字节上限或全任务累计输入预算。普通文件系统 I/O 没有墙钟截止；O_NONBLOCK 不承诺慢磁盘/网络文件系统不阻塞。

## 验证与剩余

独立离线测试 `python3 dev/test_maturity_cleanup.py`：跨类型、opaque hash 与大小冲突、竖屏长边、冻结报告变更/越界、命令注入、完整性、分页/目录环等。

未验收：真实 hash 算法/CLI JSON、实际命名误报率、跨名称内容重复、真实删除/恢复/容量、报告原子写、总任务期限与恢复检查点；已实现的 0600/目标类型保护不替代这些能力。输出是待人工确认的名称/版本候选，不是自动去重器。
