# Magnet pipeline：来源、缺陷与实现边界

## 正确性结论

MP-01 目录被当作 `download -o` 文件路径、失败回退 cwd；MP-02 任意 ID 即可打印清理、缺状态/收据；MP-03 `--name` 静默无效；MP-04/账户边界是响应包络、目录与账号归属不能靠猜。已修正为单资源持久状态、明确输出文件、失败非零且不回退、清理绑定同一 ID/本地大小与 SHA-256/人工确认；删除无效 `--name`，并对 account scope/响应冲突 fail closed。仍未通过真实 PikPak JSON、下载源一致性和删除语义验收，不报高分，不宣称已完成成熟云产品。

## 逐项深读候选与决定

### rclone/rclone — 活跃成熟 backend

固定提交 `d369079a1448c487d09d85bfe11382e16ea4e345`：
- [addURL L1618-L1635](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/pikpak.go#L1618-L1635)：离线创建独立返回 task；其无效目录 fallback 属 rclone 实现，不是官方 CLI 保证。
- [requestNewTask L111-L126](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/helper.go#L111-L126)、[getTask/waitTask L186-L215](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/helper.go#L186-L215)：按确切任务 ID 观察完成，错误明确返回。
- [shouldRetry L420-L490](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/pikpak.go#L420-L490)：取消、每日限额与空间不足有不同处理。
- **采纳**：创建→ID→核验分离；错误不是成功；配额失败不无限重试；未知 schema fail closed。
- **不采纳**：不直接复制上游 POST 重试、API 凭据处理、全量删除或目录 fallback；官方 CLI 无服务端幂等键。本地先写 submitting，结果未知就阻断再创建，宁可人工对账，不伪造 exactly-once。

### CJReinforce/PikPakAutoOfflineDownloadBot — 全链路对照，不是安全模板

固定提交 `473735baa88ec74aeb03b2702449f3fe8db0741d`，API 元数据 pushed_at 为 2024-12-05（显著陈旧，不因 stars=511 宣称仍活跃）：
- [README L8-L22](https://github.com/CJReinforce/PikPakAutoOfflineDownloadBot/blob/473735baa88ec74aeb03b2702449f3fe8db0741d/README.md#L8-L22)：云离线→aria2→删除，并警告强劲删除可能误删。
- [README L45-L47](https://github.com/CJReinforce/PikPakAutoOfflineDownloadBot/blob/473735baa88ec74aeb03b2702449f3fe8db0741d/README.md#L45-L47)：未配置默认自动删除。
- [README L168-L171](https://github.com/CJReinforce/PikPakAutoOfflineDownloadBot/blob/473735baa88ec74aeb03b2702449f3fe8db0741d/README.md#L168-L171)：逐个资源完整链路、清理避免和下载并行。
- **采纳**：一个资源一份状态；任务/文件/本地落盘明确关联；清理不能与下载混为成功。
- **不采纳**：默认自动删除、清空账号、TG 密码多账户、aria2 RPC 密钥及无人值守清理；本脚本不执行任何云删除，不读第三方账号，不安装 bot。

## 公开候选准入证据（取证 2026-10-16）

| candidate | source | license | release_or_explicit_unverified |
|---|---|---|---|
| rclone/rclone | [固定 getTask/waitTask](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/helper.go#L186-L215) | MIT；[固定 COPYING](https://raw.githubusercontent.com/rclone/rclone/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING) | [v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，published_at `2026-10-09T11:03:19Z`；固定快照与 tag 祖先关系未核验 |
| CJReinforce/PikPakAutoOfflineDownloadBot | [固定 README](https://github.com/CJReinforce/PikPakAutoOfflineDownloadBot/blob/473735baa88ec74aeb03b2702449f3fe8db0741d/README.md) | 未确认；固定完整 tree 端点 `GET /repos/CJReinforce/PikPakAutoOfflineDownloadBot/git/trees/473735baa88ec74aeb03b2702449f3fe8db0741d?recursive=1` 未列出 LICENSE，不能据此认定不存在其他许可 | 发行未核验；端点 `GET /repos/CJReinforce/PikPakAutoOfflineDownloadBot/releases/latest` 本次返回 404，仅说明该 endpoint 无 latest，不证明不存在其他发行 |

rclone 许可证原文及端点 `GET /repos/rclone/rclone/releases/latest` 已公开读取，该发行 `draft=false`、`prerelease=false`；不把固定研读快照称作发行代码，不以 pushed_at/stars 替代发行或兼容性验收。Bot **许可未确认，仅作行为对照，不复制代码、不安装运行**；README 可读不构成代码移植许可。两者都只借鉴机制，没有安装、执行上游程序。

以上 GitHub API 端点均以纯文本形式记录，文档不包含可点击的外部 API 链接，也不在运行时按这些端点发起请求；它们是取证时人工读取的地址记录。

### 官方 CLI — 真实参数边界

仅执行 v0.5.3 version 与 `task add/get/ls/watch/rm`、`download/get/rm` 帮助。`download -o` 明确是单文件路径；去掉 `-o` 默认写 cwd。`rm` 帮助没保证回收站/恢复/释放配额。`task rm --delete-files` 明确附加删文件，本管道不用。

上述 v0.5.3 是先前本地帮助证据，本轮未运行任何真实 PikPak 账号命令；官方 CLI 的 GitHub 源码、许可证与发行对应关系未核验，不借其他项目的 MIT 或版本背书。

## 落地机制与证据

- 状态原子 replace（临时文件同目录、flush/fsync、0600）；CLI `.lock` 独占，死锁人工核对后处理；同一来源原文+folder 的 SHA-256 指纹。不存原始资源 URL；状态还记录显式 account scope 别名与 `account_scope_binding=operator_declared_unverified`，该别名是操作者声明，不是官方身份验证。
- 同 state 已有 task ID 不重新 add；创建响应缺 ID/创建超时保留 submitting；不同链接/目录/账号 scope 拒绝复用。不按 task ls 第一条或名字匹配；缺 scope 或 `account_scope_binding` 的旧收据不静默迁移。
- step2/3/4 均先校验完整来源指纹、目录、account scope 与有效 task ID；CLI main 在 `auth status` 前先做 scope 门禁；无 ID 的 submitting 在 task get 前拒绝，不通过查询认领。只有人工对账后保留原指纹和同一 scope，并补确切 ID 才可继续。
- 精确收集外层/嵌套 task/file ID；规范 `status`/`phase` 后拒绝冲突，complete 必须有 file ID；`ok=false`/`success=false`/`error` 或畸形包络不产生成功下一步。错误只保留分类，不回显正文；记录 `latest_task_status`，一次查询可取消等待，error 保留本地收据但记 failed、退出 2。目录响应字段若存在必须与请求一致，多字段冲突拒绝；指定 folder 且无可验证字段只记 unknown，不给清理资格。
- `-o <dest>/<fileID>.part` 是完整文件；CLI 失败不回退。目标存在不覆盖，实际普通文件存在才落盘；记录本地大小、SHA-256、task ID/file ID/路径。再次查询同一 complete 不抹掉下载收据。
- downloaded 后观察到 pending/running，保留本地路径/大小/hash 与原 file ID，记 waiting 并撤清理资格。task get 超时由底层返回不含正文的退出分类 124，经 step2 记录 query_failure 并把旧 ready/downloaded 置 blocked、移除旧 complete；不通过全局捕获 SystemExit 来吞掉其他门禁。再次同一任务 complete、同一 file ID 且本地大小/hash 复核通过才恢复 downloaded，无需重下；新 file ID 不继承旧本地收据。
- step3/4 要求最近有效观察为 complete；CLI main 的 step4 先只读 `auth status -F json` 核对当前身份摘要，再只接受完整来源收据同一 ID，重算本地 hash，需 `--verified-local`；所有 ID 验证完才打印安全引用命令。**不查询 task/file、不回读云对象、不删除**；读取身份同样需要当前本人账号授权，`--help` 不访问账号。
- TDD `dev/test_maturity_entry.py`：已观察 MP-01 的 2 次错误调用、重复 add、缺 ID、错任务、陌生状态、命令注入、同长度篡改、无收据清理与状态回查退化的红测；本轮新增 MP-03/MP-04/ENTRY-SAVE-01 的外层/嵌套 ID 与 status/phase 冲突、失败包络、account scope、目录绑定和旧资格撤销红测，再以临时中性假 CLI 执行完整四步、重复提交与不调用 rm 的断言。私人报告保留首次红测及最终输出。

## 未验证与非承诺

本地 SHA-256 仅防下载后字节变化，不是远端源哈希核验；用户必须确认来源/内容。未访问任何真实账号，官方 auth/task JSON 的真实 schema 尚未验收；字段未知就停止。account scope 与 `account_scope_binding=operator_declared_unverified` 只是操作者声明的防混用标签，不是身份验证。CLI main 每步另从白名单稳定 ID 生成域隔离身份摘要并与收据比较，缺失/冲突/切换即拒绝；这项身份变更拒绝仅在受支持字段的中性 fixture 合同内验证，没有官方稳定 ID 字段的实盘证据，也不把 `logged_in` 当身份保证。只支持单文件，不支持目录型 BT/递归下载、自动续传、跨机/跨 state 去重、恶意本地并发替换、跨设备持续身份监测、自动重试、真实删除/容量释放。CLI 0 不是完整性证明，mock 绿不是平台验收。
