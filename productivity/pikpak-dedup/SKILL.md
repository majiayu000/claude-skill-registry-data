---
name: pikpak-dedup
description: |
  只读分析 PikPak 重复/多版本媒体候选，适用于查重、重复文件、保留最新/最高清、find duplicates、compare versions。
  名称候选不等于精确内容重复；先人工确认，按冻结报告逐 ID 批准，只打印命令，绝不自动删除。
  Use when finding duplicate or multiple releases of the same movie or episode in PikPak: same title, different resolution, keep newest or highest quality. Name similarity is not proof of identical content; you approve each ID from a frozen report and commands are only printed, never executed.
---

# PikPak 重复候选分析

**只读分析 + 人工逐项核对 + 冻结批准。不是自动去重器。**

## 1. 范围、策略与扫描

先取得明确授权的目录 ID；不默认获准访问整个账号。真实账号登录/扫描需要独立授权；开发/回归只用中性 fixture。`pikpak version` 和 `pikpak ls --help` 可检查安装/参数，不证明 JSON 契约。

```bash
python3 scripts/analyze_dupes.py --folder '<folderID>' --policy newest --json ./pikpak-dup-report.json
```

离线验证（仓库根目录）：

```bash
python3 skills/pikpak-dedup/scripts/analyze_dupes.py --from-fixture dev/fixtures/sample_tree.json --json -
```

策略只决定**候选组中建议保留的项**，不表示其他项应删除：

| 策略 | 指标 |
|---|---|
| `newest` | 最新修改时间，再比大小 |
| `largest` | 最大字节数，再比时间；不保证实际画质 |
| `highest-res` | 元数据分辨率长边，再比大小/时间；不保证真实画质 |

默认忽略小于 100 KB 的文件，可通过 `--min-size` 调整。先隔离视频/音频家族；PDF、ZIP、字幕和未知类型不参与版本组，避免同名文档成为影片清理项。归一名称会剔除常见清晰度/编码/来源词、保留集数/语言等，但仍是启发式，不能承诺语义不同一定不误合并。

## 2. 证据和完整性

所有组都标 `match_type=name_candidate`、`exact=false`。`evidence.same_size` 和 `remote_hash_match` 只是元数据线索；opaque `hash` 未核验算法/完整内容语义，即使与大小都相同也**不称为完全重复**。跨名称内容查重尚未实现。

先检查 `complete=true`、`truncated=false`。文件/目录共用 ID 身份索引，仅身份及 kind/name/size/hash/params/时间证据一致时去重；冲突报 `IDENTITY_CONFLICT`，整份报告不发布候选、禁止命令。重复 token、目录环、缺页、坏响应和 CLI 失败退出 2，写入 incomplete 状态而非伪完整候选。默认文件上限 50000（`--max-items`），另有 5000 文件夹、10000 页、100 活动目录深度预算；触顶另标 `truncated=true`。`--json -` 只输出 JSON。

size 只接受非负整数或纯十进制数字串；缺失/负数/布尔值/浮点数/单位文本保留 `null`，不抓取其中数字、不当作 0。`unknown_size_files` / `size_complete` 与枚举 complete 分开；未知项保存在 `unassessed_files`，同名组若含未知大小则放入 `unassessed_groups`（`keeper=null,trash_candidates=[]`），不以三种策略产生确定性保留建议、不用于阈值或 same_size/hash 证据；`analysis_complete=false` 不是“没有重复”。

width/height 分别只接受 1–2147483647 的整数或纯 ASCII 十进制整数串（允许前导零），这是本地元数据支持范围，不是画质保证。缺失、零、负数、符号/单位/空白、浮点数、布尔值、容器及超范围值均为未知，绝不抽取其中数字；任一维未知则 `resolution=""`，不制造单边分辨率。`highest-res` 只在组内每项宽高均有效时按长边比较。一项已知、一项未知或 `params` 缺失/部分维度时不能确定最高分辨率；若 `params` 明确提供了 `width`/`height` 而任一值非法，三个策略一律把整组放入 `unassessed_groups`，`reason=unknown_resolution`、`keeper=null`、`trash_candidates=[]`、`analysis_complete=false`，不生成排序、keeper、重复/清理建议，也不回显原始嵌套值。仅缺失/部分维度且选择 `newest`/`largest` 时仍可按明确的时间/大小指标处理；证据不足的组 ID 不能从冻结报告批准清理。枚举 `complete` 和 `size_complete` 可仍为 true。

显式 fixture 必须为 UTF-8 JSON 对象，null/坏文件/空路径不回退 live。可选时间缺失/null 归一为空字符串，非空时间须为有效 ISO 字符串；`--max-items` 为正整数，`--min-size` 非负，`PIKPAK_TIMEOUT` 为 1–86400 整数秒。输入/配置/展示失败统一退出 2，`--json -` 仍输出失败 JSON；CLI 原 stdout/stderr 不进入错误报告，仅保留安全分类及退出码。目标不可写时失败 JSON 改送 stdout 并标 `REPORT_WRITE_FAILED`，禁止使用旧目标。

展示组内所有 ID/路径/大小/时间/分辨率，保留项与候选项分别核对。`trash_candidates` 只是兼容字段名，不代表已批准。候选体积仅加已知 size、另报未知项，不是已释放或保证可释放容量；不同合集、音轨、版本仍需人工判断。

## 3. 冻结批准后仅打印

审核同一报告，记录原始字节摘要与批准 ID：

```bash
shasum -a 256 ./pikpak-dup-report.json
python3 scripts/analyze_dupes.py --from-report ./pikpak-dup-report.json \
  --report-sha256 '<审核时记录的64位SHA256>' --approve-id '<明确批准的候选ID>' \
  --emit-trash-cmd
```

多项重复 `--approve-id`。不允许重新扫描时直接生成命令。报告变更、未完成报告、非候选 ID、keeper、危险 ID 整批拒绝；ID 不做修复。每 30 项一批，**只打印，不执行**。

`rm` 帮助未独立证明可恢复语义，不承诺移入回收站或立即释放空间。只有另行核验当前官方的可恢复契约、用户明确授权对象与动作后，外部执行者才可考虑操作；未证实可恢复时止于清单，绝不使用永久删除。执行后如有授权须逐批准 ID 对账，不凭抽查宣称完成。

## 维护

`python3 dev/test_maturity_cleanup.py`（同次设置 `TMPDIR` 为受控临时目录、`PYTHONDONTWRITEBYTECODE=1`；独立入口和 unittest 加载均自动进入 offline_environment，额外硬拒绝子进程/网络/通知） 独立离线覆盖；父级 runner 单独整合。上游证据、采纳/拒绝、未实现内容见 [upstream-design.md](references/upstream-design.md)。未验收真实 CLI/schema/hash、命名误报率、删除恢复与配额；报告输出已强制 0600 并拒绝 symlink/非普通文件/多硬链接；尚未做原子写、总期限和恢复检查点。

## 输入、报告权限与资源边界

输入文件（fixture；ad-cleaner/dedup 另含冻结报告）使用 `O_NONBLOCK | O_NOFOLLOW` 打开，再以 fstat 拒绝非普通文件、非当前有效用户所有、多个硬链接和组/其他用户可写的文件；最终路径 symlink、FIFO、设备、目录均拒绝，不修改输入权限。普通中性 `0644` 与私有 `0600` 输入均可用，不强制输入 0600；真实私密数据仍应放入受控私有目录。父目录 symlink/恶意本地竞态不在隔离保证内。文件读入上限 **16 MiB（16777216 字节）**，按描述符有界读取；fixture、单次 live CLI JSON、冻结报告解析前均限制对象/数组容器嵌套深度 **64**（含根，忽略字符串内括号/转义）。超限/坏 JSON 安全分类为 `INVALID_FIXTURE` / `INVALID_CLI_JSON` / `INVALID_REPORT`，退出 2；扫描失败使可写目标 `complete=false`，冻结批准失败不输出命令、不扩大批准。

报告输出已在成功/失败路径拒绝 symlink、非普通文件和多个硬链接，截断前强制 `0600`；这不等于原子替换或生产验收。尚无原子写、全局墙钟期限/取消或恢复检查点。CLI stdout/stderr 仍先完整捕获，再检查单页 JSON 字节数；无 CLI 捕获期总字节/RSS 上限、展示输出字节上限或全任务累计输入预算。普通文件系统 I/O 没有墙钟截止；O_NONBLOCK 不承诺慢磁盘/网络文件系统不阻塞。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
