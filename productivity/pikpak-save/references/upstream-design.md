# Save：来源、缺陷与产品取舍

## 正确性结论

baseline 只列手工命令，却宣称一键/自动批量；没有持久作业、超时对账或任务结果核验。已明确缩为**人工转存操作卡 + 离线 JSON 收据检查器**，不冒称持久自动化；检查器对外层/嵌套 ID、状态冲突和显式失败包络 fail closed，不回显错误正文。未做真实账号验收，不给 95 分或其他精确分数。

## 候选与固定证据

1. **rclone/rclone** 固定 `d369079a1448c487d09d85bfe11382e16ea4e345`：
   - [addURL 请求与目标目录](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/pikpak.go#L1618-L1635)：创建返回 task，目标目录找不到时有其自身 fallback 语义。
   - [requestNewTask](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/helper.go#L111-L126)、[getTask/waitTask](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/helper.go#L186-L215)：持有任务 ID，再核对完成；不是从 task list 首条猜测。
   - [shouldRetry](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/pikpak.go#L420-L490)：context 取消停止；每日任务限额、容量不足是 fatal，不盲目重试。
   - **采纳**：创建/观察分离，保留确切任务 ID，状态 unknown/error 显式停止；`inspect_task.py` 对外层/嵌套 `task_id`/`id`/`file_id` 和规范化 `status`/`phase` 冲突、错 ID/缺 file ID 不输出下一步；`ok=false`/`success=false`/`error` 失败包络分类拒绝且不回显正文。人工批次逐项记已提交/未知/失败。
   - **不采纳**：不把 rclone 的命名参数、目标 fallback、HTTP 重试直接搬成官方 CLI 参数；`task add --help` 只有 `-p/-w`。创建重试可能已生效，选择人工对账而非“rclone 重试了所以可重提”。不把第三方 API task schema 称作官方 CLI JSON。
2. **PikPak CLI v0.5.3 本地帮助**：逐项只读核验 `task add/get/ls/watch/rm`、`share get/restore/history`、`download/play`。
   - `task ls -s` 存在，默认一页，不代表没有其他任务；分享预览 `--token/-l/--parent`；restore `-f` 为空表示全部，`--parent` 指定目标。
   - `task rm --delete-files` 是额外破坏性选项，流程不使用。`download -o` 是单文件完整路径；不能失败后静默去掉参数。
   - **采纳**：分享先完整分页/子目录预览，未完整就不默认恢复全部，只恢复批准 ID；提取码处理留在用户本地，不公开。
3. **cli/cli** 固定 `3d7967df5a94052b0554898ffa02526f0f90b8c9`：[login flow](https://github.com/cli/cli/blob/3d7967df5a94052b0554898ffa02526f0f90b8c9/pkg/cmd/auth/shared/login_flow.go#L204-L210)。借鉴“安全降级必须透明”，用于对未知 JSON、未完整预览和创建结果未知的明示；不移植 token 登录，也不假设 PikPak 有相同凭据存储。

社区搜索（Linux.do）只提供 rclone/CLI 候选，不采纳加速承诺、自动邀请或临时邮箱流程。未安装、运行任何上游代码。

## 公开候选准入证据（取证 2026-10-16）

| candidate | source | license | release_or_explicit_unverified |
|---|---|---|---|
| rclone/rclone | [固定 getTask/waitTask](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/helper.go#L186-L215) | MIT；[固定 COPYING](https://raw.githubusercontent.com/rclone/rclone/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING) | [v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，published_at `2026-10-09T11:03:19Z`；固定快照与 tag 祖先关系未核验 |
| cli/cli | [固定 login flow](https://github.com/cli/cli/blob/3d7967df5a94052b0554898ffa02526f0f90b8c9/pkg/cmd/auth/shared/login_flow.go#L204-L210) | MIT；[固定 LICENSE](https://raw.githubusercontent.com/cli/cli/3d7967df5a94052b0554898ffa02526f0f90b8c9/LICENSE) | [v2.102.0](https://github.com/cli/cli/releases/tag/v2.102.0)，published_at `2026-09-30T02:40:02Z`；固定快照与 tag 祖先关系未核验 |

许可证原文已公开读取。发行字段来自只读 GitHub REST 端点 `GET /repos/rclone/rclone/releases/latest` 和 `GET /repos/cli/cli/releases/latest`（以纯文本记录，文档不含可点击的外部 API 链接，运行时也不发起该请求），均 `draft=false`、`prerelease=false`。发行记录不等于快照/tag 对应关系或真实恢复能力验收；仅借鉴机制，不复制代码、不安装运行上游。

PikPak CLI v0.5.3 是先前本地帮助证据；其 GitHub 源码、许可证与发行对应关系未核验。本轮没有运行真实账号查询、云下载或分享恢复；不能从 rclone 的 MIT 许可或发行记录推定官方 CLI 的许可或实盘语义。

## 验证与剩余范围

TDD：先见检查器缺失失败，再实现精确 task ID、file ID、外层/嵌套包络一致性和必需 file ID 校验；`dev/test_maturity_entry.py` 的真实 main/argparse、stdin/退出码及公开候选证据字段经共享 `offline_environment` 与额外底层拒绝桩验证。输入均中性；帮助不等于服务端字段合同。账号 scope 与 `account_scope_binding=operator_declared_unverified` 只作人工声明的防混用字段，`logged_in` 不构成身份验证。

未实现/不承诺：持久自动批量队列、自动通知、账号登录、服务端创建幂等、恢复 exactly-once、配额数值、分享是否免次数、恢复后云端内容。本 skill 的 inspect 仅本地检查，不联网，不持久台账；需要持久单资源执行器时转 `pikpak-magnet-pipeline`。
