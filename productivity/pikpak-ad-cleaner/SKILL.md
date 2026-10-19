---
name: pikpak-ad-cleaner
description: |
  扫描 PikPak 资源包的广告/推广可疑文件，分 high/review/protected 报告；只读扫描，不自动删除。
  适用于清理广告、垃圾文件、推广文件、scan folder for junk、remove promo files。
  只有明确批准冻结清单后才打印清理命令；未核验可恢复语义前不得执行。
  Use when scanning a PikPak share or folder for bundled ad files, promo junk, fake readme, or spam videos. Read-only grading report; cleanup commands are only printed after an explicit frozen-list approval and are never executed automatically.
---

# PikPak 广告分级扫描

**只读扫描 → 分级核对 → 冻结报告逐 ID 批准 → 仅打印命令。绝不自动删除。**

## 范围和前提

先确认用户授权的文件夹 ID，不因“只读”就默认获准扫描整个账号。`pikpak version` / `pikpak ls --help` 可检查安装与参数。实际账号的登录/扫描须单独获授权；开发验证只用中性 fixture，不执行 auth/status/ls。

## 1. 扫描

经授权的云端扫描：

```bash
python3 scripts/scan_ads.py --folder '<folderID>' --json ./pikpak-ad-report.json
```

完全离线验证（fixture 路径相对仓库根目录）：

```bash
python3 skills/pikpak-ad-cleaner/scripts/scan_ads.py --from-fixture dev/fixtures/sample_tree.json --json -
```

分级：
- `high`：网址快捷方式、含网址或多个推广词的文本/图片。仍是规则候选，不是内容已证实为广告。
- `review`：可执行文件、疑似宣传短片、单个强推广词/多个弱推广词；必须人工判断。
- `protected`：字幕、疑似密码文本，保护优先；压缩包不参与广告判断。

文件名/扩展名启发式可能误报，绝不读取或执行可疑文件本体。

## 2. 完整性和数量

先检查 JSON 的 `complete=true`、`truncated=false`。重复分页 token、目录环、无效响应、CLI 失败会退出 2；设置 `--json` 时写入明确失败状态，且不提供完整统计或命令。不要使用旧报告假装本次成功。

文件与目录共用 ID 身份索引；仅 kind/name/size/hash/params/时间证据一致的重复记录合并。任何身份/关键证据冲突都会 `complete=false,error_code=IDENTITY_CONFLICT`，整份失败报告不发布候选，也不能生成命令。默认上限 50000 个文件（`--max-items` 可调）；另有 5000 文件夹、10000 页、100 个活动目录深度的安全上限。预算触顶标 `truncated=true`。`--json -` 的 stdout 只有 JSON。

size 只接受非负整数或纯十进制数字字符串；缺失、负数、布尔值、浮点数、单位文本均保留 `size=null,size_known=false`。报告单列 `unknown_size_files` / `size_complete`；不能从坏字符串抓数字判短片。候选数量按 `high/review` 数组计算，体积只加已知 size 并另报未知项（下界）；**候选体积不等于实际释放空间**。

显式 fixture 必须是 UTF-8 JSON 对象，`null`/坏文件/空路径永不回退 live。可选时间缺失/null 归一为空字符串，非空时间须为有效 ISO 字符串。`--max-items` 须为正整数，`PIKPAK_TIMEOUT` 为 1–86400 整数秒；输入/配置/展示失败统一退出 2，`--json -` 仍给失败 JSON。错误只给安全分类/CLI 退出码，不回显原 stdout/stderr。文件目标不可写时以 `REPORT_WRITE_FAILED` 改送失败 JSON 到 stdout，旧目标不能当本次结果。

## 3. 冻结批准与命令打印

向用户展示 ID、路径、大小、分级和理由，明确记录批准的 ID；审核时记录报告原始字节摘要：

```bash
shasum -a 256 ./pikpak-ad-report.json
```

仅使用同一报告生成批准的子集，不重新扫描：

```bash
python3 scripts/scan_ads.py --from-report ./pikpak-ad-report.json \
  --report-sha256 '<审核时记录的64位SHA256>' --approve-id '<明确批准的ID>' \
  --emit-trash-cmd high
```

每个批准 ID 单独重复 `--approve-id`。报告变化、未完成报告、非当前分级候选、protected ID、异常 ID 都拒绝整批。安全 ID 采用保守字母数字/下划线/连字符格式，不修复未知格式。最多每 30 项打印一个 `pikpak rm` 命令，**从不执行**；扫描模式直接使用 `--emit-trash-cmd` 会被拒绝。

## 4. 执行边界

本 skill 不执行删除。当前独立 CLI 帮助只证明 `rm` 子命令存在，未证明可恢复契约。只有另行核验当前官方文档/客户端行为、确认仅移入回收站且用户明确批准对象和动作后，外部执行者才可考虑操作；不能证明可恢复就停在报告，不生成或使用永久删除动作。复核必须逐个批准 ID 对账，不凭抽查宣称全部成功。

## 维护与未验收

运行 `python3 dev/test_maturity_cleanup.py`（同次设置 `TMPDIR` 为受控临时目录、`PYTHONDONTWRITEBYTECODE=1`；独立入口和 unittest 加载均自动进入 offline_environment，额外硬拒绝子进程/网络/通知） 和父级回归测试。机制证据、采纳/拒绝和剩余问题见 `references/upstream-design.md`。真实 CLI JSON/分页、误报率、回收站与配额未实盘验收；报告含私密路径，应保存在受控目录。报告目标拒绝 symlink/非普通文件/多硬链接并强制 `0600`，但尚未提供原子替换、墙钟总期限与恢复检查点。

## 输入、报告权限与资源边界

输入文件（fixture；ad-cleaner/dedup 另含冻结报告）使用 `O_NONBLOCK | O_NOFOLLOW` 打开，再以 fstat 拒绝非普通文件、非当前有效用户所有、多个硬链接和组/其他用户可写的文件；最终路径 symlink、FIFO、设备、目录均拒绝，不修改输入权限。普通中性 `0644` 与私有 `0600` 输入均可用，不强制输入 0600；真实私密数据仍应放入受控私有目录。父目录 symlink/恶意本地竞态不在隔离保证内。文件读入上限 **16 MiB（16777216 字节）**，按描述符有界读取；fixture、单次 live CLI JSON、冻结报告解析前均限制对象/数组容器嵌套深度 **64**（含根，忽略字符串内括号/转义）。超限/坏 JSON 安全分类为 `INVALID_FIXTURE` / `INVALID_CLI_JSON` / `INVALID_REPORT`，退出 2；扫描失败使可写目标 `complete=false`，冻结批准失败不输出命令、不扩大批准。

报告输出已在成功/失败路径拒绝 symlink、非普通文件和多个硬链接，截断前强制 `0600`；这不等于原子替换或生产验收。尚无原子写、全局墙钟期限/取消或恢复检查点。CLI stdout/stderr 仍先完整捕获，再检查单页 JSON 字节数；无 CLI 捕获期总字节/RSS 上限、展示输出字节上限或全任务累计输入预算。普通文件系统 I/O 没有墙钟截止；O_NONBLOCK 不承诺慢磁盘/网络文件系统不阻塞。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
