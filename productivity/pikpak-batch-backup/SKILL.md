---
name: pikpak-batch-backup
description: |
  按 PikPak 文件夹树生成下载计划并安全复制到新的本地目录；不覆盖已有文件，校验大小，生成本地 SHA-256 清单。尚不支持增量、字节续传或远端内容校验。
  用于云盘备份到本地、批量下载、备份计划与完整性边界咨询。
  Use when backing up a PikPak folder to local disk in one pass: download plan, never overwrite existing files, verify size, write a local SHA-256 manifest. No resume, no incremental sync, no remote content verification.
---

# PikPak 批量下载到本地

**语言 / Language**: 本 skill 的说明、帮助文本与错误信息以简体中文为主，面向中文用户；这是有意的区域定位，不是强制。仓库同时提供英文 README（`README.en.md`）；脚本的 `--json` 输出与退出码不依赖语言，可直接被其他语言的调用方解析，请以机器可读输出作为程序接口。
This skill's docs, help text and errors are primarily Simplified Chinese and target a Chinese-speaking audience by design. English readers can use `README.en.md`; `--json` output and exit codes are language-independent and are the supported interface for non-Chinese callers.

当前是保守的单次复制工具，不是版本化备份或可恢复快照系统。

运行前提：`PIKPAK_BIN`、`PATH`、Python 解释器、脚本文件及其父目录必须由当前操作者控制；子进程默认继承环境。不要把环境变量交给远端输入、不可信 CI、多租户或提权服务。仓库不把未验证的 `permissions` / `allowed-tools` 字段当作宿主隔离证明；需要不可信部署时，应由宿主固定并核验可执行文件和环境后再运行。

## 先规划，再授权下载

```bash
# 在线只读列目录，不下载（需用户授权访问账号）
python3 scripts/batch_backup.py --folder "<folderID>" --dest ./pikpak-backup --dry-run

# 完全离线测试
python3 scripts/batch_backup.py --from-fixture dev/fixtures/sample_tree.json --dest ./new-backup --dry-run

# 用户确认范围/容量后，向已创建的新空目录下载
python3 scripts/batch_backup.py --folder "<folderID>" --dest ./pikpak-backup
```

单文件 CLI `-o` 是文件路径，例如 `pikpak download <fileID> -o ./neutral.mp4`，不是输出目录。flags 以用户所装 CLI 的 `--help` 为准。

## 现在真实提供的保护

- 遍历树并检查分页 token、目录 ID 环路、深度和数量上限。
- 下载前检查清洗后、大小写、NFC 归一化及文件/目录名称碰撞；保留 `backup_manifest.json`。
- 已有文件/清单全部拒绝，**同长也不跳过**；不覆盖用户数据。重跑请选新目录，当前没有增量/断点恢复。
- 拒绝符号链接路径组件，以 POSIX dir_fd/O_NOFOLLOW 打开目录。
- 在目标根的私有临时目录下载；暂存文件用 `O_NONBLOCK|O_NOFOLLOW` 打开，先 fstat 拒绝 FIFO/设备/目录等非普通文件，精确大小吻合后以安全 fd `fchmod(0600)` 再读取并计算 SHA-256，以不可覆盖 hardlink 原子发布；清单也以 `0600` 安全 fd 暂存后发布，失败内容不发布为最终名。
- 清单记录 id/path/size/status/local sha256；失败非零退出。`remote_integrity=unverified`、`verification=size_only`，本地 SHA-256 不是远端内容相等证明。
- 不删云端或用户已有本地文件，只清理本次私有临时目录。


## 响应与失败边界

- 原始列表页必须是对象，显式包含 `files` 数组与字符串 `next_page_token`；每项必须有非空字符串 id/name 和 `drive#file|drive#folder` kind。错误包络、缺字段、未知 kind 或元数据容器坏类型均以 `schema_error` 非零中止，不输出空成功。
- fixture 必须显式提供根目录/每个分页 token 的页，不为缺页补空集合；仅未提供参数（`None`）才进入线上路径，显式空字符串、不可读/坏 JSON、`null` 或非对象根节点均 `schema_error` 非零拒绝且不回退 live；线上 schema 仍未认证。
- CLI 失败只报告稳定分类与 `exit_code`，不复述 stdout/stderr、异常正文或可执行路径。缺失/超时/启动失败分别标记 127/124/126；非零 CLI 保留其退出码作为诊断信息。
- 全树列表预算 `--max-pages 10000`、`--scan-timeout 900` 秒；每次 CLI 超时不超过剩余预算。唯一 token 的空页也计数，触发预算非零标记 `incomplete`，不输出部分成功。时间预算不保护报告生成、下载或 Python 正则执行。

## 明确不提供的能力

不宣称官方 CLI 自带续传；第三方 pikpakcli 的 Range 源码不是官方 CLI 证据。没有远端 MD5/GCID 校验、检查点恢复、增量对比、跨文件事务、空目录恢复、空间预留、崩溃恢复或版本保留。目标须支持 POSIX nofollow、dir_fd 和同文件系统 hardlink；FAT/exFAT 等不支持时安全失败。禁止并发程序修改备份目录，不能抵御本地恶意进程并发重命名。

`--dry-run` 不下载，但未加 fixture 时会访问云端列表；fixture 不加 dry-run 会直接拒绝，显式空 fixture 不能绕过该限制。配额/限速取决于账号与平台当前规则，不承诺固定数值。清单含名称路径，需私密保存。

## 设计依据与验证

见 [上游源码、许可证、采纳与未实现边界](references/upstream-design.md)。离线回归：`python3 -m unittest dev.test_maturity_data -v`；mock 不是官方 API 兼容认证。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
