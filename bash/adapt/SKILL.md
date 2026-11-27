---
name: dsh-plugin-adapt
description: plugin-fast-adapt 的升级适配车道。查 DeepSeek 官方最新版本，取该版本官方 upgrade-guide，扫描插件代码匹配破坏性变更锚点，报出踩了哪几条并给官方修法；seams 查包名或 API 符号在指南与本机宿主里的双源结论；改完秒验并做四维性能架构体检；官方指南覆盖不到的老版本转七阶段迁移 SOP。宿主环境本身有问题（覆盖层残留、悬空软链、插件装了没生效）不走这里，转 dsh-plugin-diagnose。触发词：适配 DSH 插件、升级插件、插件不兼容、dsh 升级后报错、插件用了废弃 API、接缝查询、这个 API 还在不在、扫描窗口、破坏性变更、老版本 DSH 适配、历史走廊迁移、插件性能审计、peer 修补。
---

# 适配升级车道

把「插件适配到新版 DSH」拆成四步，每步一个脚本，每步都能单独跑；另有两个可选步骤补全「修完即验、升级顺带优化」。以下命令都相对工具根目录执行，工具根即本文件真实路径往上两级、含 `scripts/` 的那一层。脚本用自身文件的绝对路径定位，不必先 cd，从任何目录直接 `node <工具根>/scripts/<脚本>.mjs` 同样可行。本目录常以软链别名加载，shell 的 `cd ../..` 会按软链走错地方，确实要 cd 时用 `cd "$(realpath <本文件所在目录>)/../.."`。`<插件目录>` 指被查插件的仓库根。

环境本身有问题（覆盖层旧包、悬空软链、客户端半死链）先转 `../diagnose/SKILL.md`，别在坏环境上做适配判断。

## 第一步：看清本机环境

```sh
node scripts/env-doctor.mjs <插件目录> --brief
```

`--brief` 只影响输出体积（本机实测 80.5KB → 4.5KB，约省 2.1 万 token）：`installedPlugins` 的 patch 行原文换成计数、进程命令截断到 120 字符。要查具体挂载行时去掉 `--brief` 拿全量。

本车道只取四段：

- `globalDsh`：全局安装的 DSH 版本和位置，后面定目标版本要用
- `target.peerWindows`：待查插件自己声明的 peer 版本窗口，决定扫描走廊起点
- `ghostHost`：磁盘代码已换新、宿主进程还在跑旧代码时判 `stale`（进程启动时间早于磁盘变更超过 120 秒）。先重启宿主再做适配判断，否则改完也验不到；`ok` / `no-running-host` / `unknown` 看 `reason`，不猜
- `falseGreen`：`tsconfig` 的 `paths` 指向不存在的 checkout（M1）。此时 TypeScript 静默回落到 `node_modules` 的已发布类型，本地 `typecheck` 可能全绿而实际类型是旧的；`findings` 非空先修路径或删 alias，再信 typecheck 结果

`overlayFindings`、`sharedFarmFindings`、`activation` 非空，或 `ghostHost.verdict` 为 `stale`，说明环境本身要修，转 `../diagnose/SKILL.md`。

## 第二步：定目标版本

```sh
node scripts/guide-sync.mjs <本机版本>
```

它读 npm 的 `dist-tags`（`latest` / `next` / `alpha`），判断本机在官方通道里的位置：

| 判定 | 含义 | 下一步 |
| --- | --- | --- |
| `upgrade-available` | 有通道版本高于本机 | 取 `target`（官方所有通道的最高版本）继续 |
| `up-to-date-on-channel` | 本机已是某通道最新版 | 无需适配，收工 |
| `ahead-of-upstream` | 本机比官方所有通道都新 | 无需适配，收工 |
| `unknown-local` | 没检测到本机版本 | 默认跟 `latest`，但要人工确认 |

**不要盲目取 `latest`。** 本机完全可能跑在 `next` 线上，比 `latest` 还新一版，这时报「建议升级到 latest」是倒退。

**上游盯哨（--check）**：`node scripts/guide-sync.mjs --check` 零参数可直接接 cron、launchd 或 agent 轮询，自动探测本机宿主版本，退出码语义化（1=上游有新版，0=无需动作，2=判定失败），有新版时顺手把该版官方指南预取进缓存，下次 `run.mjs` 零等待。工具不自带定时器。

有 `target` 时取目标版本的官方升级指南：

```sh
node scripts/guide-sync.mjs <本机版本> --target <扫描目标> --clone
```

指南来源按优先级：本机已有 harness clone（只读，自动发现 `~/Documents/*/deepseek-harness` 或 `DSH_HARNESS_CLONE`）→ 默认分支的受管快照（`~/.cache/dsh-plugin-fast-adapt/harness-guides-branch/`，按 1 小时 TTL 刷新；冷拉约 4.8 秒，刷新约 1 秒）→ 发版 tag 缓存/clone（标 `frozen`）。tag 是冻结切片，官方会在发版后把同版本指南补全到默认分支，实测 `dsh-v0.2.1-rc.3` tag 里 `v0.2.1-rc.2` 只有 1 条变更，默认分支同一目录 23 条。

`--target` 必须传扫描窗口终点，不要留空跟官方最新：npm 发版常早于上游打 tag（实测 rc.4 上 npm 23 小时仍无 tag），跟着最新会去拉一个不存在的 tag，整段扫描跳过，而本机明明有覆盖到目标版本的指南。

**覆盖度（`scan.coverage`）**：`coveredUpTo` 是本轮指南实际覆盖到的最高版本，`complete=false` 表示目标版本的变更还没有官方文档。`run.mjs` 会在屏幕上明说「只覆盖到 X，不能当查干净」；`--strict` 把它当失败（退出码 2）。指南来自 tag 冻结快照时另标 `guides.frozen`，提示命中数可能偏低。

**取版锚点（2026-10-25 实测复盘）**：本机已是官方通道最新版时 `resolution.target` 为 `null`，旧实现因此拿不到指南语料、`run.mjs` 的 scan 阶段静默跳过（扫描走廊 `(peerFloor, hostVersion]` 明明有内容却报「无指南根或无窗口」）。现在取版锚点按 `--target || resolution.target || localVersion || dist-tags.latest` 依次回退，走廊照常扫。

**窗口起点只认宿主包（2026-10-25 dsh-image-gen 实录）**：起点取插件在宿主包（`@deepseek-ai/dsh` 及 `dsh-*` 套件子包）上声明的 peer 下限；同 scope 的 `@deepseek-ai/cordis`（4.x）、`@deepseek-ai/schemastery`（3.x）是独立版本线的库，不算宿主包。混入会把起点顶到 3.18.4 一类高位，窗口倒挂后扫描静默跳过。现在倒挂（起点大于终点）会回退宿主版本并在 `window.fallback` 留痕、`window.source` 记起点来源（flag/peer/host），stderr 同步告警。

## 第三步：查插件踩了哪些变更

```sh
node scripts/code-scan.mjs <插件目录> <upgrade-guide 目录> <本机版本> <目标版本>
```

`<upgrade-guide 目录>` 是官方指南根，例如 `~/layerfs-lab/deepseek-harness/docs/upgrade-guide`，或上一步 clone 出来的 `~/.cache/dsh-plugin-fast-adapt/harness-dsh-v<version>/docs/upgrade-guide`。

输出三段：

- `findingsByGuide`：按官方变更条目分组的命中，每条带 `guide`、`title`、`migration`
- `migration`：官方给的修法原文（从该指南的 Migration 段抽出的相关步骤）
- `findingCount` / `guidesConsidered`：命中数与参考的指南条数

每条命中带出处锚点 `guideFile`/`guideLine`（指南内相对路径加标题行号），结论可回溯到官方原文位置，不用在指南目录里再搜标题。

命中分三类并带 `severity`：`package`（import 了已移除或已改名的包，critical，装载必炸）、`member`（调用了已移除的方法或字段，high，运行时炸）、`code`（字符串里出现已变更的错误码或事件名，medium，最可能撞同名）。findings 先按 severity 排再按文件行号，每条带 `evidence`（命中行原文）。包名锚点有语义门：只在与移除或改名动词同句时才成为锚点，语境引用不算。

**扫描根（2026-10-25 实测复盘）**：`pickScanRoots` 取源码根并集，`src`（client/web 常嵌在 src 内部）与同级的 `client`/`web`/`ui` 一并扫；`lib`/`dist` 是构建产物、与 src 同义，只在没有任何源码根时才退回，否则同一处命中会按两份文件重复报。

## 接缝查询

```sh
node scripts/seams.mjs <包名或符号> [--guide <guide-root>] [--host <版本>]
```

回答「这个接缝在我的目标宿主还在不在」，双源合成：指南源（锚点表全走廊，哪个版本声称移除或改名了它、原文在哪一行、官方修法）乘宿主源（包看 node_modules 实测，符号看宿主套件源码文本命中，弱证据如实标注）。裸 `dsh-*` 名自动归一到 `@deepseek-ai/` scope 再查。诚实三态：双源都说没有才下「已移除」；指南说没有但宿主里有，报分歧不替人拍板；双源都无记录时明说「指南未提及不代表 API 不存在」。不走网络，指南根走缓存。

宿主实测的路径解析（`scripts/lib/host-scope.mjs`，与 `code-scan` 的宿主核查共用）：套件子包的真实位置是宿主主包内部的 `node_modules/@deepseek-ai/dsh-*`，不是全局 `node_modules` 的下一级。两个候选作用域都探（主包内部优先，全局 `@deepseek-ai` 兜住平铺安装形态），`checkedWhere` 记实际解析到的位置——结论可回溯到磁盘。包名收裸名与 `@scope/name` 全写两种写法，全写会先剥掉 scope 前缀再拼路径。

## 一键编排与运行日志

```sh
node scripts/run.mjs <插件目录> [--target <版本>] [--from <版本>] [--no-clone] [--no-smoke] [--no-typecheck] [--no-log] [--real-smoke] [--strict]
```

按上面四步依次跑环境、定版、指南、扫描、体检、冒烟、typecheck（执行插件自有的 typecheck script，与冒烟同信任级），输出一份统一 JSON 报告；扫描窗口自动取「插件在宿主包上声明的 peer 下限 → 宿主版本」的走廊（`--from`/`--target` 可覆盖，倒挂自动回退并留痕）。指南步骤会把窗口终点作为 `--target` 传给 `guide-sync`，按分支快照取语料，不再跟官方最新版本走。

typecheck 的两种跳过要分清：**工具链缺失**（runner 不在 PATH，按 PATH 预检判定）与**形态不适用**（目标不含 `tsconfig.json`，安装副本常见——`package.json` 的 `files` 白名单不含 tsconfig，`tsc -p tsconfig.json` 必报 TS5058）。两者都判 `skipped` 并给补法，都不算构建失败；只有 runner 在 PATH 上且构建确实失败才判 `fail`（退出码 2）。判据是纯机械的，不匹配错误文本。

`scan.coverage` 记本轮指南实际覆盖到哪一版（`coveredUpTo` / `complete`）。没扫或覆盖不全时屏幕明说「不能当查干净」，不再只打「命中 0 处」；`--strict` 让这两种未知态退出 2，供 CI 用，默认退出码语义不变。未知开关会直接报错（`--no-smoek` 这类拼写错误不再静默照跑）。

`--real-smoke` 默认关，显式启用后桥接原仓库 plugin-upgrade 的 `verify-runtime.mjs`：干净 profile 安装→启动→四类归因（插件代码、依赖解析、profile 配置、宿主运行时），fail 计入退出码 2。脚本不在本机（探测兄弟仓 `dsh-plugin-upgrade-skill`，或 `PFA_VERIFY_RUNTIME` 指路径）时诚实跳过给补法，Windows 按 POSIX-only 声明跳过。退出码：0 干净，2 有 critical/high 命中、typecheck 红、真冷启动失败，或 `--strict` 下扫描未知。

每次运行写本地日志（`~/.local/state/dsh-plugin-fast-adapt/runs/`，一次一个自包含 JSON 加 index.jsonl 一行摘要；旧 `~/.cache/dsh-plugin-fast-adapt/runs/` 有数据时首次运行自动整体搬迁，台账是要留存的运行史，放 `~/.cache` 会被本机清理工具整目录扫掉，可再生的 dist-tags 缓存与指南快照仍走 `~/.cache`）。记录工具版本与 commit：2026-10-25 实测教训是跑了一份滞后拷贝产出 4 个本已修复的误报，没有日志这类「跑的是哪版工具」完全不可观测。索引摘要带 `phases` 三态（scan/smoke/typecheck/realSmoke 各 ok|skipped|fail|error）与 `toolDirty` 星标（工具仓当时有未提交改动，版本号与 commit 可能拆对），扫描没跑不再与「体检满分」在同一行里混淆。

```sh
node scripts/run-log.mjs list [--limit 20]                    # 最近运行一览（含工具版本@commit）
node scripts/run-log.mjs show <id|--latest>                   # 单次全文
node scripts/run-log.mjs sanitize <id|--latest> [--out 文件]  # 脱敏后才可外发
node scripts/run-log.mjs doctor [--logs <目录>]               # 运行日志 × 宿主启动日志交叉核对
```

`doctor` 的判定：宿主日志干净且最近一次 run 扫描跑过，则状态一致；宿主日志干净但扫描没跑（`host-log-clean-scan-unknown`），代码侧未核查，看 `scan.reason`；宿主报了它而最近一次扫描干净，嫌疑在装载/挂载/环境侧，转 `../diagnose/SKILL.md` 看 activation 双半；两边都有问题先按运行日志的命中清代码。日志不出本机，对外反馈前必须先 `sanitize`（home 前缀转 `~`、用户名转 `<user>`、机器名转 `<host>`、邮箱转 `<email>`，目录结构保留）。`--offline` 跳过 guide-sync 供自检零网络用。

## 第五步（可选）：修完秒验

```sh
node scripts/quick-smoke.mjs <插件目录>
```

纯内存模拟 Cordis 上下文，动态载入插件入口，毫秒到秒级验证模块能加载、`apply` 契约能执行、工具能注册。改完代码先跑它，挂了立刻回改，不用等真宿主冷启动。

契约怎么判、Mock 缺口怎么读、边界在哪，见 `../build/SKILL.md` 的秒验段。一句话：冒烟通过不等于宿主兼容。

## 第六步（可选）：升级时顺带做性能与架构体检

```sh
node scripts/plugin-audit.mjs <插件目录>                                # 纯四维审计
node scripts/plugin-audit.mjs <插件目录> --guide <guide-root> <本机版本> <目标版本>   # 叠加官方指南交叉
```

四个维度从 100 分扣：性能（同步 I/O、无上限读取）、弹性（强依赖已移除包）、上下文预算（工具 Schema 体积）、生命周期（监听器与定时器清理）。检测走 scanner 状态机，注释和字符串里的同名词不算命中。报告带 `targetForm`（plugin/tool）：目标是不是 DSH 插件看生态信号（package.json 的 `dsh` 命名空间、`@deepseek-ai/*` 依赖），工具仓跳过生命周期维度，对普通 Node 脚本建议 `ctx.effect` 属形态错配的噪音（2026-10-25 自审实录）。

三条 INFO 级提示不扣分：import type 引用已移除包（编译期风险非运行时）、peer 窗口按严格 semver 不含目标宿主（本生态 bundle 安装不强制 peer，是声明性约定，建议先经 satisfiesRange 自验证再输出）、工具描述里的宿主路径约定在宿主代码零命中（可能旧版约定已消亡，如 `.dsh-filess`，需人工确认）。

带 `--guide` 时与 code-scan 同源交叉：package 命中先经宿主实测核查（包仍在目标宿主则降级 info 证伪；确实不存在则 HIGH 扣分附官方修法）。命中清零前不建议先做性能优化。新版本引入的接缝（弱依赖 `ctx.get()` 替代强 import、peer 范围写法）就是「按新依赖做架构调整」的依据。

**peer 修补建议**：对不含目标宿主的 peer 范围，`peerPatch` 给「与目标同三元组的 caret 线」替换写法，每条都先用 `satisfiesRange` 自验证覆盖目标，验证不过的写法不给。只对 `@deepseek-ai/dsh` 及其 `dsh-*` 套件子包生成；同 scope 的库（`@deepseek-ai/schemastery`、`@deepseek-ai/cordis`）有自己的版本线，拿宿主版本套它们的 peer 会给出错到离谱的建议。只生成不自动改包：改用户 `package.json` 是不可逆写，`--peer-patch` 打印后人工确认再落。

## 升级顺带查常设规则（可选）

```sh
node scripts/standards-scan.mjs <插件目录>        # 7 条机械可判的常设规则，带回溯出处
node scripts/standards-scan.mjs --rules           # 只看规则表与各自的机械判据
```

升级适配查的是「随版本变的破坏性变更」，这一条查的是「不随版本变的硬要求」（上游 `docs/defensive-patterns/`）。两者互不覆盖：一份插件可以通过全部升级指南扫描，仍然违反常设要求。同样的规则也作为第五维进了 `plugin-audit`，所以 `run.mjs` 已经带上，这里只是单跑入口。

批量把宿主核心包从 `dependencies` 挪进 `peerDependencies`（上游常设规则：写进 dependencies 会产生 vendored 多实例污染）：

```sh
node scripts/fix-peer-deps.mjs --installed          # dry-run，只打印计划
node scripts/fix-peer-deps.mjs --installed --apply  # 落盘，先备份到 <插件>/.pfa-backup/<时间戳>/
```

默认 dry-run。敢批量做是因为判据纯机械、且搬错位置会让 `npm install` 直接报错而不是静默改坏。

## 老插件：官方指南覆盖不到时

官方 upgrade-guide 最早只到 dsh-v0.1.7-rc.2。插件更老、目标版本更老，或跨大段历史走廊时，`code-scan` 会报 `guidesConsidered = 0`，这时转 [老插件迁移 SOP](../../references/legacy-migration-sop.md)：用原仓库 [plugin-upgrade skill](https://github.com/oh-my-dsh/dsh-plugin-upgrade-skill/tree/main/skills/plugin-upgrade) 的人工卡片走廊（dsh-v0.1.0-rc.8 起 19 条边加跳版卡）当差异来源，按八阶段 checklist 走：定模式 → 只读准备 → 幽灵宿主检查 → 组装走廊 → 七类触点 → 计划确认 → 实施 → 六层验证。两套工具的分工速查也在 SOP 里：有 guide 的段用本技能的 `code-scan`，没 guide 的段用原版的 `plan-migration.mjs` 和卡片，运行时验证用原版的 `verify-runtime.mjs`。

## 怎么读结果

- **命中为零不代表没问题**，只代表「在指南覆盖的范围内没踩到」。
- **命中先验误报**：同名符号会撞车，看命中位置上下文确认来源。
- **`member` 命中里若是指南的迁移目标就不会出现**，报了是噪音。
- **`guidesConsidered = 0` 说明这一段没有官方指南**，不是「查干净了」。
