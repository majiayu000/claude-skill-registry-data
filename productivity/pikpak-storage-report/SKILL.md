---
name: pikpak-storage-report
description: |
  只读统计 PikPak 目录体积、文件数与大文件 TOP，适用于空间体检、容量报告、哪些文件占地方、storage full、largest files。
  明确扫描完整性与未知大小；不自动删除，不把扫描字节数伪装为账号配额。
  Use when checking what is filling up a PikPak drive: folder sizes, file counts, largest files, storage full, space usage. Read-only; never deletes and never reports scanned bytes as account quota.
  Triggers: PikPak 容量不足, ストレージ不足, 容量がいっぱい, PikPak 용량 부족, 저장 공간 부족, 空間不足, 大文件, 大きいファイル.
---

# PikPak 空间报告

只读目录扫描，不做删除、不查重内容、不自动查询账号总览。

## 范围和运行

先确认用户明确授权的目录 ID。开发/回归只使用中性 fixture，不接入真实账号。实际云端扫描须单独授权：

```bash
python3 scripts/storage_report.py --folder '<folderID>' --depth 2 --top 30 --json ./pikpak-storage.json
```

离线验证（仓库根目录）：

```bash
python3 skills/pikpak-storage-report/scripts/storage_report.py --from-fixture dev/fixtures/sample_tree.json --top 5 --json -
```

**`--depth` 只控制目录树展示层数，仍扫描全树；不能用浅展示声称扫描成本降低。** 缩小扫描范围用 `--folder`。`--top 0` 关闭榜单，JSON 中 `top_files=[]`。

## 报告字段与诚实解释

- `complete` / `truncated` / `errors`：目录枚举是否完成、是否触发预算、失败原因。
- `total_files` / `total_size` / `tree`：按云端 ID 去重后的文件数和已知字节数；父目录包含子目录，不能再次把所有层级相加。
- `unknown_size_files` / `total_size_is_lower_bound`：缺失、负数、带单位文本等无法识别的大小不会被当成已知 0。未知大小文件保留 `size=null`；存在未知值时总量只是下界，目录也标 `size_complete=false`。这与目录枚举 complete 是两种独立完整性。
- `top_files`：按已知字节数降序，包含 ID、path、size、modified；未知大小排后，不能据此保证已识别真正最大的未知文件。
- `account_overview=null` / `account_overview_status=not_queried`：脚本没有抓取账号总量/已用/回收站/会员。不得将此字段说成“已检查账号”。如用户另行授权并提供独立可信官方结果，可人工并列呈现，但不要偷偷扩展脚本访问。

`--json -` 的 stdout 只放 JSON。重复 token、目录环、缺失 fixture 页、坏 schema 或 CLI 失败非零退出 2，并用明确 incomplete 状态覆盖旧报告，不能继续发布完整树/排行。

默认文件上限 50000（`--max-items` 可调）；另有 5000 文件夹、10000 页、100 活动目录深度安全限制。预算触顶 `complete=false,truncated=true`。文件与目录共用 ID 身份索引，仅 kind/name/size/hash/params/时间证据一致的同 ID 合并；冲突会 `complete=false,error_code=IDENTITY_CONFLICT`，不发布半棵树或排行。云端并发变更仍可能影响快照，不等于原子服务端视图。

显式 fixture 顶层必须为 UTF-8 JSON 对象，null/坏文件/空路径绝不回退 live。可选时间缺失/null 归一为空字符串，非空值须为有效 ISO 字符串。`--max-items` 须为正整数，`--depth/--top` 非负，`PIKPAK_TIMEOUT` 为 1–86400 整数秒。输入、配置或展示失败统一退出 2，`--json -` 仍输出失败 JSON；只给安全错误分类/CLI 退出码，不回显原 stdout/stderr。目标不可写时失败 JSON 改送 stdout、标 `REPORT_WRITE_FAILED`，不得使用旧报告。

## 使用建议与安全边界

大目录/大文件只是人工整理入口，不代表可以删除。疑似多版本转到 `pikpak-dedup`；广告候选转到 `pikpak-ad-cleaner`，继续保留分级确认。候选体积、回收站体积和实际配额变化必须区分；没有官方契约与读回证据就不承诺软删立即释放容量，也不建议自动永久清空回收站。

报告可能含私密路径，应保存在受控目录。报告输出已强制 0600 并拒绝 symlink/非普通文件/多硬链接；当前原子写、全局墙钟期限/取消及恢复检查点尚未实现。

## 验证和证据

`python3 dev/test_maturity_cleanup.py`（同次设置 `TMPDIR` 为受控临时目录、`PYTHONDONTWRITEBYTECODE=1`；独立入口和 unittest 加载均自动进入 offline_environment，额外硬拒绝子进程/网络/通知） 覆盖聚合/重复 ID/未知值/TOP/失败完整性；真实 CLI JSON、配额计费、回收站、受限目录和大库性能未实盘验收。源码/文档证据与采纳/拒绝见 [upstream-design.md](references/upstream-design.md)。

## 输入、报告权限与资源边界

输入文件（fixture；ad-cleaner/dedup 另含冻结报告）使用 `O_NONBLOCK | O_NOFOLLOW` 打开，再以 fstat 拒绝非普通文件、非当前有效用户所有、多个硬链接和组/其他用户可写的文件；最终路径 symlink、FIFO、设备、目录均拒绝，不修改输入权限。普通中性 `0644` 与私有 `0600` 输入均可用，不强制输入 0600；真实私密数据仍应放入受控私有目录。父目录 symlink/恶意本地竞态不在隔离保证内。文件读入上限 **16 MiB（16777216 字节）**，按描述符有界读取；fixture、单次 live CLI JSON、冻结报告解析前均限制对象/数组容器嵌套深度 **64**（含根，忽略字符串内括号/转义）。超限/坏 JSON 安全分类为 `INVALID_FIXTURE` / `INVALID_CLI_JSON` / `INVALID_REPORT`，退出 2；扫描失败使可写目标 `complete=false`，冻结批准失败不输出命令、不扩大批准。

报告输出已在成功/失败路径拒绝 symlink、非普通文件和多个硬链接，截断前强制 `0600`；这不等于原子替换或生产验收。尚无原子写、全局墙钟期限/取消或恢复检查点。CLI stdout/stderr 仍先完整捕获，再检查单页 JSON 字节数；无 CLI 捕获期总字节/RSS 上限、展示输出字节上限或全任务累计输入预算。普通文件系统 I/O 没有墙钟截止；O_NONBLOCK 不承诺慢磁盘/网络文件系统不阻塞。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
