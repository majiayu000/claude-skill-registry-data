# Onboarding：来源、缺陷与产品取舍

## 正确性结论（先于评分）

原指南“config 无码就不带参数注册”错误：真实 `pikpak auth register --help` 明示省略会继承安装器邀请码。现已修复所有无码/拒绝路径显式 `--affiliate=`；公开码 `22874035` 未改。账号边界另行收紧：`logged_in` 只作登录状态检查，未核证稳定官方账号 ID 时只接受用户显式声明的非敏感 scope 别名，并在收据中标记 `account_scope_binding=operator_declared_unverified`，不能当身份验证；不做无实盘依据的数字评分。

## 候选与一手证据

1. **PikPak 官方 CLI v0.5.3**：本机仅执行 version 和 `auth register/login/status/task add/get --help`，未读账号或缓存。
   - 注册帮助原文：`Without --affiliate, the invitation code recorded by the installer is used.` / `Use --affiliate= to register without that code for this invocation.`
   - `-F` 仅输出 signup link；空值覆盖本次，不代表删除安装器记录。`-m device`、浏览器授权、无默认同意均按此契约说明。
   - [官方安装页](https://mypikpak.com/cli)；[注册政策](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli/register_account) 实际读取，证实浏览器自助、72 小时验证、锁定后 12 个月删除与提交前可移除/恢复引荐。不执行网页安装器。
2. **cli/cli（GitHub CLI）**，固定提交 `3d7967df5a94052b0554898ffa02526f0f90b8c9`：
   - [login.go L68-L72 / L127-L129](https://github.com/cli/cli/blob/3d7967df5a94052b0554898ffa02526f0f90b8c9/pkg/cmd/auth/login/login.go#L68-L72)：浏览器模式默认、交互能力判断、存储降级透明披露。
   - [login_flow.go L204-L210](https://github.com/cli/cli/blob/3d7967df5a94052b0554898ffa02526f0f90b8c9/pkg/cmd/auth/shared/login_flow.go#L204-L210)：凭据使用不安全存储时明确警告，而非沉默降级。
   - 采纳机制：**副作用前披露、选择必须显式、错误/降级不能伪装成功**。新增 `registration_plan.py` 仅生成计划，无默认 choice、不调用注册或子进程。不移植 gh 的 token 模式/存储策略；PikPak 的行为必须依据自己帮助，不能由别的 CLI 推断。
3. **rclone/rclone**，固定提交 `d369079a1448c487d09d85bfe11382e16ea4e345`：[addURL](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/pikpak.go#L1618-L1635)、[按任务 ID 获取](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/helper.go#L186-L215)。采纳“创建与核验分离、按 ID 查结果”，首任务不再从根目录挑同名文件。不直接用逆向 API/账号密码，不执行上游代码。

Linux.do 搜索仅作候选发现，不把自动邀请、临时邮箱或加速经验当证据，不采纳自动注册/邀新方案。

## 公开候选准入证据（取证 2026-10-16）

| candidate | source | license | release_or_explicit_unverified |
|---|---|---|---|
| cli/cli | [固定 login flow](https://github.com/cli/cli/blob/3d7967df5a94052b0554898ffa02526f0f90b8c9/pkg/cmd/auth/shared/login_flow.go#L204-L210) | MIT；[固定 LICENSE](https://raw.githubusercontent.com/cli/cli/3d7967df5a94052b0554898ffa02526f0f90b8c9/LICENSE) | [v2.102.0](https://github.com/cli/cli/releases/tag/v2.102.0)，published_at `2026-09-30T02:40:02Z`；固定快照与 tag 祖先关系未核验 |
| rclone/rclone | [固定 getTask/waitTask](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/helper.go#L186-L215) | MIT；[固定 COPYING](https://raw.githubusercontent.com/rclone/rclone/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING) | [v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，published_at `2026-10-09T11:03:19Z`；固定快照与 tag 祖先关系未核验 |

许可证原文已公开读取。发行字段来自只读 GitHub REST 端点 `GET /repos/cli/cli/releases/latest` 和 `GET /repos/rclone/rclone/releases/latest`（以纯文本记录，文档不含可点击的外部 API 链接，运行时也不发起该请求），两项均 `draft=false`、`prerelease=false`。这只证明取证时存在这些发行记录，不证明研读快照就是发行代码，也不证明本地兼容性或安全性。仅借鉴机制，不复制代码、不安装运行上游。

官方 PikPak CLI v0.5.3 指先前本地 version/help 证据，不是本轮重跑结果；其 GitHub 源码、许可证与发行对应关系未核验，不能借用上述其他项目的 MIT 许可或版本背书。本轮没有运行任何真实 PikPak 账号命令。

## 已落地与验证边界

- 注册前模板披露、明确 accept/decline、空配置也显式空参数；预览器不启动浏览器，不读取凭据。
- 去掉固定 5 分钟和未经核验的演示 magnet；账号未知先停，`logged_in` 不作为身份验证，必要时只用用户声明的非敏感 scope 并标记 `account_scope_binding=operator_declared_unverified` 防混用；首任务只认确切 task/file ID；给取消/超时/配额失败分支。
- 首任务响应若有顶层/嵌套 ID 或 status/phase 必须一致；显式失败包络、目录字段冲突和缺可核验目录字段都不能给成功/ready/清理资格；错误只给分类，不回显正文。
- 测试：`dev.test_maturity_entry` 经共享 `offline_environment` 和额外底层进程/网络/通知拒绝桩运行，覆盖中性输入、计划 argv、错误路径及公开候选证据字段；未安装依赖。
- **未验证**：实际注册/登录、邀请码归属与福利、跨平台安装、task JSON 的真实形状。官方网页是政策证据，不是本次账号实测。文档时效变化应重读官网。
