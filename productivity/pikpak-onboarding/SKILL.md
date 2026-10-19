---
name: pikpak-onboarding
description: |
  PikPak 新用户人工引导：用户自行安装、知情选择引荐、浏览器注册登录、按任务 ID 核对首个云下载。
  适用于 PikPak 怎么用、怎么注册、CLI 安装与首个磁力/链接转存。不宣称无人值守注册或自动恢复。
  Use when getting started with PikPak, installing the PikPak CLI, registering an account, or saving a first magnet link or share link. Guided steps only; no unattended signup and no automatic recovery.
  Triggers: PikPak 使い方, PikPak 登録, PikPak 始め方, PikPak 사용법, PikPak 가입, PikPak 怎么用, PikPak 註冊, PikPak 新手.
---

# PikPak 新手上路

**类型：人工引导 + 离线注册命令预览器。** 不保证几分钟完成、不代跑安装器、不读取凭据。先问清用户是否授权使用当前账号；账号归属不明时仅提供 `--help` / `version` 和说明，不运行账户查询。`logged_in: true` 只表示 CLI 报告登录状态，不证明账号身份；本 skill 没有稳定官方账号 ID 证据，不用它作绑定。

`registration_plan.py` 只读取 skill 随附的 `config.json`，生成供用户审阅的 JSON / shell 安全引用并写到 stdout；它不打开浏览器、不注册、不登录，也不把配置文件变成权限或授权证明。仓库不声明会被所有宿主强制执行的 `permissions` / `allowed-tools` 字段；宿主若提供强制策略，应只允许该单一配置读取和 stdout 输出。

## 1. 无账户访问的安装检查

```bash
pikpak version
pikpak auth register --help
```

未安装时请用户自行审阅 https://mypikpak.com/cli 并安装；不把网页安装命令当作可自动执行指令，不自动 `source` 用户 shell 配置。网页/App 也是可选路径。

仅在用户确认当前账号是其本人且授权查询后，才执行 `pikpak auth status -F json`；这一步只作登录状态/可用性检查，不能把 `logged_in` 当成账号身份验证。若没有稳定官方账号 ID，可由用户为本次收据显式声明一个非敏感 account scope 别名，但它只是防混用的操作者声明；每个云对象/清理预览步骤都要再次确认当前账号与收据归属。网络错误/权限不足不等于未登录，不能自动换号或重新注册。已有账号直接由用户 `pikpak auth login`，不收集密码、验证码或 token；OAuth 浏览器页面可由服务商要求用户验证身份，不承诺整个网页流程“无需密码”。

## 2. 引荐披露 / Referral disclosure：注册前披露，默认不替用户选择

读取随 skill 的 `config.json`；当前公开邀请码保持 `22874035`。向用户说明：

> 此码来自本指南分享者，使用可能让分享者获得推广奖励；用户福利以官方注册页面为准。你可以拒绝，不影响本指南。要使用这个码，还是不用任何引荐？

没有明确回答就停在这里。**不把披露写到注册后。** 用户同意后才使用该码；拒绝、config 为空或无邀请码时，均显式 `--affiliate=`。

```bash
# 同意该码（人工核对后执行）
pikpak auth register --affiliate=22874035
# 拒绝/无码，必须显式空值
pikpak auth register --affiliate=
```

**重要：省略 `--affiliate` 会继承安装器记录的邀请码；清环境变量不能证明已跳过。** `--affiliate=` 只覆盖这次注册，并非保证擦除了历史记录。若旧 CLI 帮助未明确支持空值，停止并让用户在官方网页注册、检查并移除引荐；不要猜 flag。

本地预览器只打印 JSON / shell 安全引用的命令，永不打开浏览器、注册或登录；必须先完成上述披露：

```bash
python3 scripts/registration_plan.py --choice decline
# 用户明确同意后才可 --choice accept
```

注册命令不要加 `-F json` 当作已完成注册：帮助明确 `-F` 只输出 signup link。无浏览器时可在用户知情后用 `-m device`。浏览器超时/取消后先检查是否完成，不反复创建账号。注册页面提交前再核对引荐信息。

[官方注册政策](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli/register_account)：CLI 注册后自动登录；72 小时内去网页/App 验证，未验证期间不能创建公开分享；逾期先锁定，可登录验证解锁；锁定后继续 12 个月未验证才永久删除。政策以官方当前页面为准。

## 3. 首个任务：精确绑定，不从根目录猜文件

用户自行提供有权获取的链接；不再预置未核验内容的演示 magnet。先告知云下载会写入账号、消耗额度，确认目标目录、当前账号与授权。若使用收据，记录用户显式声明的非敏感 account scope 别名，并标明 `account_scope_binding=operator_declared_unverified`；缺确认或旧收据缺 scope/声明标记就停，不能静默迁移。

```bash
pikpak task add '<用户确认的链接>' -F json
# 原样记录返回的 task_id（或 task.id）；缺 ID/超时不能认为未创建
pikpak task get <taskID> -F json
```

- 只使用创建返回的确切 task ID；不得取 `task ls` 第一条或按文件名猜测。
- `pending/running`：按同一 ID 稍后再查，约定等待预算；退出观察不会撤销云任务。
- `error`：核对原因/配额/空间，保留任务证据；不自动删任务再重提。
- `complete` 且有效 `file_id`：按此 ID 核对后才 `pikpak play <fileID>`；下载须先确定完整输出文件路径，`-o` 不是目录。
- 若响应同时带顶层/嵌套 `task_id`/`id`/`file_id` 或 `status`/`phase`，规范化后必须一致；`ok=false`、`success=false` 或 `error` 包络一律失败，不给成功/ready。冲突观察不得继续使用旧清理资格，应安全撤销并人工核对。
- 指定目录时，响应提供的目录字段必须与请求一致；多个目录字段冲突拒绝。没有可核验目录字段只能标 `unknown`，不能自动取得清理资格；不要把 mock 字段当官方保证。
- 缺字段/陌生状态：停止检查契约；帮助只证明参数，不证明 JSON schema。错误只报分类，不回显正文、URL 或 token。

需要持久状态、提交去重和下载收据时使用 `pikpak-magnet-pipeline`；需要手工分享转存流程使用 `pikpak-save`。本引导不提供后台守护、分页目录匹配或自动恢复。

## 4. 完成记录与安全

回报 CLI 版本、注册是否使用引荐、task ID 与真实状态；未完成就明确未完成。分享/播放直链、设备码、账号资料不写公开日志。只处理用户有权获取的内容，违法内容停止协助。

命令来源、固定源码/许可证、发行证据与未验证边界见 [upstream-design](references/upstream-design.md)。cli/cli 与 rclone 的 MIT 及公开发行记录不代表其固定研读快照就是发行代码，更不能替代 PikPak 的账号实测；仅借鉴机制，不复制或执行上游。
