# 上游机制核验与本次落地

## 证据边界

仅只读检索公开 GitHub 源码/文档；未安装或运行上游工具，未访问真实 PikPak 账号。上游设计证据不等于本项目已验证真实 CLI JSON、回收站或配额契约。

## rclone/rclone

核验快照：`d369079a1448c487d09d85bfe11382e16ea4e345`；GitHub API 当次返回 60328 stars、pushed_at `2026-10-15T16:41:49Z`。活跃成熟项目，但热度不是正确性证明。

- [lsjson 源码](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/fs/operations/lsjson.go#L20-L34)：结构化保留 Path、Name、Size、IsDir、ID、按算法命名的 Hashes，而不是解析人类表格。
- [ListJSON 错误传播](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/fs/operations/lsjson.go#L244-L267)：walk/list/callback 错误返回调用方；不能把失败当空目录。
- [lsjson 文档](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/docs/content/commands/rclone_lsjson.md#L48-L50)：hash 可选，不能把缺失字段当已经检查过。

**采纳**：ID 身份去重、结构校验、完整性独立于候选数组、机器输出只放 JSON。逐目录 token 集合、目录祖先环检测、全局文件/目录 ID 去重以及扫描预算是结合本项目分页协议的本地落地，不声称直接复制 rclone 内部实现。

**拒绝**：不把 rclone 当广告识别器，不引入其同步/删除/去重执行；本次不替换 CLI，也不增加账号接入。

## qarmin/czkawka

快照：`eb8b91dbb4d25dff416202674ee0de84ee4b5e5c`；当次 34279 stars、pushed_at `2026-09-16T17:34:11Z`。

- [核心工具说明](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/instructions/Instruction_Core.md#L37-L47)：名称/大小/内容哈希是不同证据级别；未读取内容就不能给内容级保证。

**有限采纳**：保留 high/review/protected 人工分级，不把“可疑扩展名”写成已确认恶意内容；不自动删除。

**拒绝**：Czkawka 是本地文件扫描器，不直接支持 PikPak 的云端元数据遍历；本次不挂载、不下载资源、不做全文或二维码识别，不加入 Rust/图像/FFmpeg 依赖。

## 许可与发行边界

- **rclone**：固定快照的 [COPYING](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING) 已核验为 MIT 许可文本，要求在副本或实质部分保留版权及许可声明；不是仅凭仓库热度猜许可。
- **Czkawka 的 core 机制**：固定 [czkawka_core/Cargo.toml:8](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/czkawka_core/Cargo.toml#L8) 明示 `license = "MIT"`；固定 [README 许可说明](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/README.md#L197-L203) 将 core/CLI/GTK 列为 MIT，图像/声音为 CC BY 4.0，Krokiet/Cedinia 因 Slint 为 GPL-3.0-only。这里采纳的是 core 的证据分级思路，不将组件许可扩大成“整个仓库一律 MIT”；未纳入的 GUI/资源也未复制或执行。
- 本技能只借鉴机制、独立实现，未引入或运行上游程序、未复制其源码或图音资源。以后复用实质代码/资源必须按实际组件许可保留相应声明/署名，并重新审查依赖，不能将引用当作无限制复用授权。
- 公开发行已核验：rclone [v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，发布于 `2026-10-09T11:03:19Z`；Czkawka [12.0.2](https://github.com/qarmin/czkawka/releases/tag/12.0.2)，发布于 `2026-09-09T19:48:14Z`。这是 2026-10-16 的发行元数据核对，不是运行验收；研读快照与发行 tag 的祖先关系未验证，不宣称 snapshot 等于 release。

## 已落地

1. 重复 token、目录环、缺失 fixture 页、无效响应停止；文件 50000（可调）、目录 5000、页 10000、活动目录深度 100 的上限触发 `complete=false`，预算截断另标 `truncated=true`，退出码 2。
2. 文件/目录共用 ID→身份/关键证据索引，仅一致重复合并；kind/name/size/hash/params/时间冲突使整份报告 incomplete/identity_conflict，不保留半份候选。CLI 错误不回显原 stdout/stderr，仅安全分类和退出码；fixture null/非对象绝不回退 live。输入/时间/配置/展示失败使用同一失败出口，能写入时覆盖旧完整报告；不可写时改送失败 JSON 到 stdout 并明确禁止使用旧目标。
3. `--json -` 只输出 JSON。大小只接受非负整数或纯十进制数字串；非法/缺失值保留 `size=null,size_known=false`，单列 unknown_size_files/size_complete，不从坏字符串抽数字证明短片。规则层仍优先保护字幕/密码文本，压缩包不进入广告候选。
4. 命令只允许读取冻结报告：SHA-256 绑定原始字节、逐个 `--approve-id` 且必须属于指定分级；不接受扫描时直接生成命令。整批先校验 ID，只接受 `[A-Za-z0-9][A-Za-z0-9_-]{0,255}`，拒绝而不修复异常标识；去重后每 30 项仅打印，不执行。

## 输入与资源边界

可选时间缺失/null 归一为空串，其他值必须为有效 ISO 字符串；PIKPAK_TIMEOUT 只接受 1–86400 整数秒。独立测试入口和 unittest 加载入口均进入 offline_environment，并硬阻断底层 subprocess/Popen/socket/urlopen/通知入口；测试仅使用中性 fixture、临时文件和底层模拟响应，无真实 CLI 进程。计数预算不等于内存或总墙钟预算。

输入文件（fixture；ad-cleaner/dedup 另含冻结报告）使用 `O_NONBLOCK | O_NOFOLLOW` 打开，再以 fstat 拒绝非普通文件、非当前有效用户所有、多个硬链接和组/其他用户可写的文件；最终路径 symlink、FIFO、设备、目录均拒绝，不修改输入权限。普通中性 `0644` 与私有 `0600` 输入均可用，不强制输入 0600；真实私密数据仍应放入受控私有目录。父目录 symlink/恶意本地竞态不在隔离保证内。文件读入上限 **16 MiB（16777216 字节）**，按描述符有界读取；fixture、单次 live CLI JSON、冻结报告解析前均限制对象/数组容器嵌套深度 **64**（含根，忽略字符串内括号/转义）。超限/坏 JSON 安全分类为 `INVALID_FIXTURE` / `INVALID_CLI_JSON` / `INVALID_REPORT`，退出 2；扫描失败使可写目标 `complete=false`，冻结批准失败不输出命令、不扩大批准。

报告输出已在成功/失败路径拒绝 symlink、非普通文件和多个硬链接，截断前强制 `0600`；这不等于原子替换或生产验收。尚无原子写、全局墙钟期限/取消或恢复检查点。CLI stdout/stderr 仍先完整捕获，再检查单页 JSON 字节数；无 CLI 捕获期总字节/RSS 上限、展示输出字节上限或全任务累计输入预算。普通文件系统 I/O 没有墙钟截止；O_NONBLOCK 不承诺慢磁盘/网络文件系统不阻塞。

## 验证与剩余

`python3 dev/test_maturity_cleanup.py` 覆盖上述机制；所有数据均为中性 fixture/mock。尚未验证真实 CLI schema/分页契约、分类误报率、回收站可恢复性或实际容量变化。报告已强制 0600 并拒绝不安全目标；原子写、总墙钟期限/取消、恢复检查点尚未实现；本次无自动删除。
