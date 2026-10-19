---
name: pikpak-share-manager
description: |
  审计 PikPak 分享列表的已知过期/临期/零访问字段，输出只读报告；提供需人工授权的分享管理指引，不自动创建或撤销分享。
  用于分享管理、分享过期检查、share audit。
  Use when auditing PikPak share links for expiry, near-expiry or zero-visit status. Read-only report; never creates or revokes shares automatically.
---

# PikPak 分享审计与人工管理

脚本只有 `share ls` 读取能力，不创建、续期、恢复或撤销分享。先确认用户授权访问账号；测试只用 fixture/mock。

运行前提：若通过 `PIKPAK_BIN` 覆写 CLI，它必须由可信本地操作者设置并指向受信执行文件；`PATH`、解释器、脚本及父目录同样必须可信，子进程默认继承环境。不要在不可信 CI、多租户或提权服务中直接运行；仓库不假称未验证的 `permissions` / `allowed-tools` 字段会被宿主强制执行。

```bash
python3 scripts/share_audit.py --json ./report.json
# 固定 UTC 审计时点，可重复复核，不依赖“今天”
python3 scripts/share_audit.py --from-fixture dev/fixtures/shares.json --now 2026-10-16T00:00:00Z --json -
```

## 完整性与时间约定

- 自动跟随 `--token`；token 耗尽才 complete=true。重复 token、重复/缺失 share_id、20 页仍未耗尽均非零退出，不返回貌似完整的报告。
- `audited_at` 是判断基准，`generated_at` 是生成时刻，统一 UTC；接受 ISO 和数字 epoch，拒绝 NaN/Infinity/布尔值及范围溢出。`--epoch-unit auto|seconds|milliseconds` 作用于无前缀的 now/expiration/created，`s:`/`ms:` 前缀优先。auto 优先能表示的 UTC 秒，仅秒超出 datetime 范围才尝试毫秒；同时适合两种单位的数字有歧义，应显式指定单位，不按 1e9/1e12 阈值猜测。0、早期 epoch 和精确阈值均有回归；小于微秒的部分截断。
- expiration≤基准为过期；基准<expiration≤基准+7天为临期，精确比较，不向下取整。
- 只有适配器显式 -1 表示长期；expiration 缺失/无法解析标未知，未知不是永久。零访问只在 views 是非布尔非负整数0且 created 可解析、至少30天时标记；布尔值、字符串、负值及坏类型均为未知（JSON null），不从缺值猜测。
- 报告按白名单保留 share_id/title/status/views/expiration_raw/expiration_parsed/created/files/flags，不输出密码或分享链接。files 只接受非布尔非负原生整数计数，其他类型为未知（JSON null）；嵌套文件对象与敏感字段绝不透传。其他可选字段也不透传嵌套对象。
- 只输出人工复核 ID，不生成可复制 shell 撤销命令，避免远端 ID/标题命令注入。未知或零访问均不是自动删除理由。

## 响应与失败边界

- 原始 CLI 页必须是对象并显式包含 shares 数组和字符串 next_page_token；每项必须有非空字符串 share_id、字符串 title，且 ID 不重复。错误包络、缺字段或未知结构以 schema_error 非零中止。
- fixture 是明确的完整 snapshot，可省略空 token，但带非空 token 时拒绝；CLI 未提供 `--from-fixture` 时才由内部专用未设置哨兵进入线上路径，显式空字符串、不可读/坏 JSON、`null` 或非对象根节点，以及显式传入的 `None` 均以 `schema_error` 非零拒绝且不回退 live；与原始 CLI 分页契约区分。
- CLI 失败只报告稳定分类与 exit_code；缺失/超时/启动失败标记 127/124/126，不复述 stdout/stderr、异常正文或可执行路径。

报告包含私密元数据，输出目标由用户指定。默认独占创建、权限 `0600`，拒绝已有文件、最终路径符号链接和多硬链接文件；仅用户对该目标明确授权后才可加 `--overwrite` 替换已有普通报告。不提供报告写入事务或恶意并发修改防护。

## 手工管理（必须另获具体授权）

先检查本机 `pikpak share --help` 及对应子命令帮助，再决定是否使用 `create/get/rm`。创建必须逐项确认文件 ID、接收人/用途、有效期、密码策略和转存上限；不得依赖“永久无密码”默认值。撤销必须先展示精确 share IDs 与影响，再取得确认，执行后读回验证；本审计脚本不会执行这些动作。

公开第三方源码没有证明官方 owner 分享列表的 expiration/views/created 字段；当前 schema 是本适配器的 fixture 契约，不是线上实测。有效期哨兵、访问统计、创建/撤销闭环都未验证。回归使用固定 now；audited_at/expiration_parsed 保留实际毫秒到微秒精度，不把判断时点截成整秒；不要修改系统时钟或放宽断言。

[上游源码、许可证、采纳与真实边界](references/upstream-design.md)。报告包含私密元数据，勿公开。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
