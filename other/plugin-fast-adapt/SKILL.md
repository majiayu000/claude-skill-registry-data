---
name: plugin-fast-adapt
description: DSH 插件升级适配与代码审查主入口。查 DeepSeek 官方最新版本与升级指南，扫描插件破坏性变更；支持四条车道（适配升级/造插件/启动排障/代码审查与防御性架构审核）及 DSH 原生插件与子 Agent 隔离委派协议，输出 P0/P1 紧凑报告。触发词：适配 DSH 插件、升级插件、插件不兼容、dsh 升级后报错、代码审查、代码审核、code review、生命周期检查、单例泄漏、Peer污染、紧凑报告、批量巡检。
---

# plugin-fast-adapt

DSH 插件升级适配与防御性审核的主入口。四条车道各管一件事，先判意图再动手：

| 车道 | 什么时候走这条 | 读哪一份 |
| --- | --- | --- |
| 适配升级 | 宿主发了新版、插件报错、要核某个包或 API 还在不在、要给插件做性能体检 | `sub-skills/adapt/SKILL.md` |
| 造插件 | 没有插件要从零写一个，或给刚写完的插件过体检门 | `sub-skills/build/SKILL.md` |
| 环境与启动故障 | 插件装了没生效、客户端卡 loading、宿主起不来 | `sub-skills/diagnose/SKILL.md` |
| 代码审查与架构审核 | 深度审查 Cordis 生命周期、单例泄漏、Peer 依赖污染、模板变量；常设规则的机械可判部分已升级为扫描 | `sub-skills/review/SKILL.md` |

**不要一次把四份都读进来。** 按上表判断走哪条，只读那一份；跨车道时（比如升级完顺手补个出生证）再补第二份。以下命令都在技能根目录执行；脚本用自身文件的绝对路径定位，从任何目录直接 `node <技能根>/scripts/<脚本>.mjs` 也可以，不必先 cd。

**权威来源只有四类，全在上游仓库与 registry**：不依赖人工维护的升级卡片，也不镜像官方全量文档。

| 来源 | 回答什么问题 | 出处 | 检测方式 |
| --- | --- | --- | --- |
| npm registry `dist-tags` | 本机在官方通道的哪个位置、目标版本是谁 | `@deepseek-ai/dsh` | `guide-sync` |
| 仓库 `docs/upgrade-guide/` | **这一版到那一版之间**坏了什么、官方修法是什么 | 每个版本目录一条条目 | `code-scan` |
| 仓库 `docs/defensive-patterns/` | **任何时候都成立**的硬要求（不随版本变） | 五篇：package-surface / general / client-components / conversation-and-session / remote-and-api | 机械可判的 7 条 `standards-scan`（规则 id：top-level-await、loader-entry-shape、shared-state-no-owner、cross-package-relative-import、lifecycle-unpaired-resource、vendor-rescope-unscoped、waterfall-missing-next），其余人工 |
| 仓库 `docs/persistence-changes/` | 落盘格式变了什么、**旧数据还能不能读** | 每份一条变更 | 暂为人工（缺真实故障样本） |

常设规则那层已经不再全靠人工：`scripts/lib/standards.mjs` 里那张表把**照原文读必然得出同一结论**的七条做成了机器检出（模块顶层 await、入口导出面、共享状态无所有者、跨包相对 import、外部生命周期资源未配对注销、裸引用未收归 `@deepseek-ai/` 作用域、waterfall 监听器未透传 `next`），每条都带 `defensive-patterns` 的原文出处，规则 id 以来源表那行为准并与规则表双向对账（自检兜着）；需要意图判断的（dispose 是否真等停稳、回调异常是否隔离、slot 注册物是否稳定）**故意不进**自动扫描，留在 review 车道人工核对——把裁量题伪装成判定题比不判更坏。确定性违规可由 `codemod.mjs` 一键修复。

前两类管「时间轴上的破坏性变更」，后两类管「不随版本变的常设契约」。二者不可互替：一份插件通过了全部升级指南扫描，仍可能违反常设要求；反过来，一条常设要求也不会出现在任何一版的 upgrade-guide 里。**只扫升级指南，等于只查了一半。**

三类上游文档由 `guide-sync` 的稀疏克隆一并取到缓存快照（`SPARSE_DOC_PATHS`），取完可直接在自己的工具根下点开：`node -e "console.log(require('os').homedir())"` 拼上 `/.cache/dsh-plugin-fast-adapt/harness-guides-branch/docs/` 即是。**稀疏面少一个目录，文档里的出处就变成死链**——2026-11-05 的实录：技能引了 `defensive-patterns` 与 `persistence-changes`，而稀疏面只有 `upgrade-guide`，出处点不开了一个月没人发现。自检里有一条断言把这个面钉住。

指南取仓库默认分支的受管快照（发版后官方还会补全同版本条目），发版 tag 只是冻结切片，仅在拿不到分支快照时兜底并标 `frozen`。那类知识快照必滞后（上游预发布节奏 1.7 到 2.8 天一个），而「某个包还在不在」用宿主 node_modules 实测更硬。

## 一键编排（推荐入口）

```sh
node scripts/run.mjs <插件目录> [--check-upstream] [--target <版本>] [--from <版本>] [--profile <web|desktop>] [--run-tests] [--no-clone] [--no-smoke] [--no-typecheck] [--no-log] [--real-smoke] [--strict]
```

环境→定版→指南→签名差分→扫描→体检→冒烟→typecheck 一条命令跑完，出一份统一 JSON 报告并写本地运行日志。退出码：0 干净，2 有 critical/high 命中、typecheck 红或真冷启动失败；加 `--strict` 时「扫描没跑」和「指南没覆盖到目标版本」也按 2 退出。报告里的 `scan.coverage` 写明本轮指南覆盖到哪一版：没扫或覆盖不全时屏幕会明说「不能当查干净」，不再用「命中 0 处」冒充干净。签名差分阶段每次都留存当前宿主签名快照，窗口起点的基线签名在缓存里才算差分并把包面删除合成虚拟指南落盘（基线缺失就如实记 skipped，本次先留快照、下次运行自愈，不需要用户记任何纪律）。合成指南由 `code-scan` 按窗口基线精确消费，其中官方指南没记的命中单独走 doc-gap 账（`scan.docGapCount`，来源标 `types-diff`）——官方文档滞后或漏记（#5816 类）不是噪音，是要显式呈现的事实。扫描窗口、`--real-smoke`、运行日志（`run-log.mjs list/show/sanitize/doctor`）的细节见 `sub-skills/adapt/SKILL.md`。「插件报错 / 装了没生效」的第一站是 `node scripts/run-log.mjs doctor`，它把运行日志和宿主启动日志并排核对。

## 技能面同步（可选）

本仓默认不盯任何下游。要把技能面镜像到另一个技能目录时显式给它：

```sh
node scripts/sync-skill.mjs --dest <下游技能目录> --check   # 只查漂移（退出码 1 = 有漂移）
node scripts/sync-skill.mjs --dest <下游技能目录>            # 同步
```

同步面固定为技能读者真正会用的文件：`SKILL.md`、`README.md`、`README.zh-CN.md`、`README.ja.md`、`references/**`、`scripts/**`、`sub-skills/**`，`package.json` 不入技能面。`--dry-run` 只打印不落盘；同步完成后打印建议的下游提交命令（只 add 同步路径防夹带），不自动提交。

## 跨车道纪律

- **命中为零不代表没问题**，只代表「在官方指南覆盖的范围内没踩到」。指南只记官方认为需要通知的破坏性变更，不覆盖所有可能性。先看 `scan.coverage.complete`：没扫或没覆盖到目标版本时，零命中是未知，不是干净。
- **命中先看是不是误报**。锚点匹配做了几层降噪（规则与实测依据见 `references/heuristics.md`），但同名符号仍会撞车，比如插件里的 `path.resolve()` 和指南里的 `runtime.resolve()`。判断方法：看命中位置的代码上下文，确认符号是不是真来自宿主 API。
- **`member` 命中里，指南的「迁移目标」与「延续句符号」不会出现**（2026-11-21 收口：成员锚点只从 Change 段非延续子句抽，Migration 新写法与 keeps its form/unchanged 句里的符号不再是待报锚点，判据见 `references/heuristics.md` 规则 5）。仍会出现的两类是触碰点级信号、要人工过一眼：同名符号撞车（插件里的 `path.resolve()` 与指南里的 `runtime.resolve()`），以及同名 API 语义变更（guide 写「`register(definition, { when })` adds a condition」——API 没改名、旧用法坏了，插件是否已带新选项只有看调用现场才知道）。
- **声明与实际调用要分开查**。版本号格式合法、peer 范围写得漂亮，都不等于宿主里能跑。上游生态给出的判据是「拿代码实际调用的 API 去比对它声明的兼容版本，不一致就算错」（Obsidian 官方 lint 的做法）。本技能的对应位置是 `code-scan` 的窗口走廊加 `seams` 双源结论，别用「peer 范围看起来对」替代实测。
- **远程依赖的结论一律标待审计**。宿主/插件共享模块、bundle 遮蔽、peer 解析这几类问题，构建期与安装期都可能全绿，只在浏览器或真实冷启动里炸（上游同类项目里这类 issue 的形态高度一致：构建通过、运行时两个实例互相不认识）。所以任何不经过真冷启动的结论都要标明「未在真宿主验证」。
- **自动化只吃机械可判的部分**。常设规则的自动化边界写死在 `standards-scan --rules` 的输出里：每条规则的「机械判据」一栏说清机器看什么、没看什么。判据收窄过三轮（第一版把模块级 `new Set()` 与 `Symbol.for` 全报成违规，实测在 dsh-image-gen 上 35 处命中全是常量表与编译产物），现在宁少不滥：**误报一次，使用者就不再信第二次**。
- **批量修补的失败方向必须是报错而不是静默改坏**。`fix-peer-deps` 敢批量做，是因为「宿主核心包写进 dependencies」判据纯机械，且搬错位置会让 `npm install` 直接报缺依赖，不会变成看不见的运行时异常；默认 dry-run、`--apply` 才落盘且先备份。
- **起子进程与删路径是本工具仅有的两类危险动作**。前者要净化环境（宿主的子进程凭证擦除会摘掉 `GIT_CONFIG_KEY_n` 却留下 `GIT_CONFIG_COUNT`，git 读到残缺配置组直接 fatal，本工具每条 git 调用都会静默失败）；后者要不跟随链接（`rmSync(recursive)` 删软链/junction 会删到目标里去）。两条都由 `scripts/lib/proc-env.mjs` 收口，新写的脚本一律走它，不要各自 `execFileSync` / `rmSync`。
- **目标宿主版本按平台分派**。桌面 APP 跑的是自己捆的那份宿主，不是 npm 全局那份；两者错开时（2026-11-05 实测：APP `0.2.2-rc.1` vs npm `0.2.1-rc.5`），拿 npm 版本判 APP 插件会把两端都判错，而报告看起来和正常的一样。`fleet-sweep` 每项按平台取目标版本，摘要里同时给出 `desktopHostVersion` 与 `targetVersionByPlatform`；APP 插件的套件存在性按 `app.asar` 内真实捆绑的 `@deepseek-ai/*` 包判定（`lib/desktop-app.mjs` 只读 asar 头，不解包），不再错用 npm 树那一份。
- **集群治理与单兵深度结合**。宿主刚升级、要把整批插件过一遍时，先用 `node scripts/fleet-sweep.mjs` 做集群广度筛查与矩阵看板诊断，筛出有问题的插件再逐个回到适配车道深查。工作区里的分组目录（形如 `Deepseek/`）会被下钻一层找插件；发现面不止 patch 条目一张网——宿主日志点名、patch 条目里没有的插件（装在 node_modules 却从未挂载的，如 2026-11-21 实录的 @linxin666/dsh-agents）按解析目录同一性去重后补成 HOST-LOG 项上榜；`~/.dsh/logs` 的宿主启动失败与未激活条目按包名与目录双键关联进看板，健康态从 healthy 降为 warning，不静默略过。
- **向外部仓提 PR 前过基线守卫**。本地副本过期还建分支，推上去就是分叉。`run-log.mjs sanitize --pr-draft` 与 `fleet-sweep.mjs --pr-ready` 先核对 `origin/HEAD`、npm 最新版与工作区干净度，落后或脏就拦；判定与拦截原因写在报告里（`ready` / `behind-upstream` / `dirty` / `npm-ahead` / `no-remote` / `remote-unreachable`）。
- **工具不自带定时器**。上游盯哨 `guide-sync --check` 的退出码是语义化的（1 有新版、0 无需动作、2 判定失败），接 cron、launchd 还是 agent 轮询由用户定。

## 安全边界

- **只读为主**：`env-doctor`、`code-scan`、`plugin-audit`、`seams`、`log-doctor` 完全不写文件；`run-log` 默认只读，只有 `sanitize --out <文件>` 会写脱敏结果到指定路径。
- **`quick-smoke` 与 `write-gate` 会执行插件代码**（动态 import 入口模块）。只对自己或审过的代码跑，不要对来路不明的目录跑。执行面限于 Node 进程内，但插件代码理论上能做任何 Node 能做的事。
- **自愈默认 dry-run**：`env-heal` 不加 `--apply` 只报告，加了也是移动不删除（进 `~/.dsh/.trash/<日期>/`）。
- **不改 DSH 本体**，不动 `~/.dsh` 下的配置和 profile 声明。
- **自动修补只限判据纯机械的三类，先备份后落盘**：`codemod`（Loader 入口导出面、顶层 await）、`fix-peer-deps`（宿主核心包 peer 挪位）与 `fleet-sweep --apply-compat`（批量写 `package.json` 兼容账本与 Peer 范围）默认 dry-run 或不带 `--apply` 只报，`--apply`/`--apply-compat` 才落盘，且原文件先备份到 `<插件目录>/.pfa-backup/<时间戳>/`（三个入口共用 `scripts/lib/backup.mjs` 的同一形状）。`.pfa-backup/` 已进 `release-rules` 的 `FORBIDDEN_PACK` 与 scaffold 生成的 `.gitignore`——实测 `npm pack` 会把它打进包，而备份里是改动前的 `package.json`。除此之外一律只报命中和官方修法；`plugin-audit --peer-patch` 也只打印建议，不写 `package.json`。
- **网络只用在「取官方源」这一步**：定版本读 npm 的 dist-tags，取指南 clone 官方仓库。两处都有超时，失败明确报错而非静默跳过；dist-tags 有 1 小时缓存，网络失败降级用旧缓存并标 stale；上游 tag 未打导致的 clone 失败记 1 小时否定缓存（dist-tags 一变即作废），期间不重复拉取；指南优先复用本机已有 clone，`--no-clone` 可跳过。
- **日志只落本机**，含本地路径与用户名，外发前必须 `sanitize`。`sanitize` 同时替换 home 的字面量与 realpath 两种形态（macOS 上 `/var` 与 `/private/var` 是同一目录的两种写法，只替换一种会漏掉另一种）。向外部仓库提交适配 PR 前必须过基线守卫（`run-log.mjs sanitize --pr-draft` 与 `fleet-sweep.mjs --pr-ready`）：先核对 `origin/HEAD` 与 npm 最新版，本地落后或有未提交改动时拦截，防止基于过期副本建分支导致分叉。
- **缓存根可注入**：`DSH_PFA_CACHE_DIR` > `DSH_CACHE_DIR` > `XDG_CACHE_HOME` > `~/.cache`，由 `scripts/lib/cache-root.mjs` 统一求值。自检启动即把缓存根指向临时目录，不写真实用户缓存。

## 判据回写纪律

修一次误报或漏报，三件一起做，缺一不可：

1. **写回判据**：`references/heuristics.md`（扫描降噪）或对应 `scripts/lib/*.mjs` 的注释（机器判据），说清「为什么这条判据是对的」。
2. **沉淀夹具**：`fixtures/<id>/input/` 放最小复现，`fixtures/<id>/expected.json` 写正确判定与 fingerprint。自检启动时全量回归，判据写松了（该报的不报）或写紧了（不该报的报了）都会红。
3. **登记账本**：`references/incident-ledger.md` 一行一条，带来源与夹具 id。

只做第 1 步不做第 2 步，下次换台机器重跑就没了；只做第 2 步不做第 3 步，夹具与判据会各自漂移。三条夹具一起才封住改动：`waterfall-real-break`（该报的报）、`waterfall-far-next` 与 `waterfall-object-literal-body`（不该报的不报）。

## 按需读取（车道之外）

| 场景 | 读什么 |
| --- | --- |
| 完整使用指南与集群多维治理实战 | `references/user-guide.md` |
| 官方指南覆盖不到的老插件 | `references/legacy-migration-sop.md` |
| 扫描降噪规则与实测依据 | `references/heuristics.md` |
| 事故账本（真实误报/漏报的最小复现索引） | `references/incident-ledger.md` |
| 给插件自己的仓库加提交时门禁 | `references/ci-snippet.md` |

## 自检

```sh
npm test
```

自检套件（313 项断言），覆盖扫描器不误报（注释和字符串里的同名词不算命中）、不漏报、版本窗口与 real semver 判定、目标形态判定、指南出处锚点、指南分支快照与覆盖度未知态、三元版本账本直通与变更嗅探、本地宿主接缝契约核对与未构建硬拦截、跨平台与工作区自适应（Termux/Linux/环境变量/祖先依赖）、上游经验吸纳（退出码 143 停机判定/Bundle 遮蔽阴影/准入账本 compatPatch/提示词 {{cwd}} 拦截/全局前缀分裂检测/集群治理 Web-APP 与运行态生命周期多维看板）、Cordis 深度防御性审查（核心 peer 依赖 vendored 污染 P0 拦截/顶层单例状态泄漏 P2 预警/run 与 audit --compact 紧凑模式/DSH 原生插件服务）、Release Note 破坏性变更虚拟指南提取与双语去重、接缝查询双源结论、运行日志与宿主日志交叉核对、一键编排各档位（含 --strict）、冒烟验证（含 Config 默认值解析、宿主 node_modules 兜底、未声明 inject 契约拦截与 exports-only 入口）、四维审计（含 peer 与 compat 准入账本修补）、启用诊断（宿主半与客户端半）、幽灵宿主四态与磁盘时间来源、tsconfig paths 假绿（含 extends 与 JSONC）、环境层三处盲区、创作脚手架与体检门、日志诊断、下游同步、发布预检规则（版本一致/tag/包内容/npm 状态）、跨平台模拟、诊断输出瘦身、CLI 帮助与未知参数、宿主凭证擦除留下的残缺 GIT_CONFIG 配置组净化（真实 git 子进程回归）、链接形态路径的安全删除、文档断言数与技能面 description 长度门禁、扫描性能回归、生命周期配对检查、确定性 Codemod 自动修补、Types-Diff 类型差分自动接缝与 SKILL.md 常设规则枚举双向对账、合成指南目录参数链（第五个参数不再被静默忽略）、工具链缺失按 PATH 预检确定性判定（runner 在场时内层命令缺失判 fail 不吞成 skipped）、脱敏覆盖 home 全部形态（realpath 与 Windows 8.3 短名）、事故夹具全量回归（`fixtures/` 与 `references/incident-ledger.md` 双向对账，判据收窄的两侧都钉住；含 2026-11-09 fleet 场测修出的正则字面量掩码根因）、状态词表单点真源对账（`scripts/lib/run-states.mjs`：阶段/类型检查/冒烟/真冷启动/构建/生命周期/健康/包探测/宿主在场/检查结论/符号文本证据共 12 张词表（26 个状态值），门禁扫描面是全 `scripts/**/*.mjs`，按值域判——值不落任何一面即为手写新状态）、直通记录形状对账（`phasesOf` 与索引投影都认 fast-pass 的顶层 `phases`/`findings`/`auditScore`，防直通记录被 list 显示成「?」、被 doctor 判成「代码侧未核查」）、账本直通基线必须自带结论（`auditScore`/`findings` 缺失时回退全量，防 null 在直通链上自我复制）、形态判定（目标不含 `tsconfig.json` 时 typecheck 判 skipped 而非 fail——安装副本的 `files` 白名单不含 tsconfig，判 fail 是假失败）、锚点抽取降噪（成员/裸调用锚点只从 Change 段非延续子句抽——Migration 迁移目标与「keeps its form/unchanged」延续句不进待报锚点，替换对旧符号补锚含 or 同伴与 instead of 方向判定，包路径尾点半角点剥离）、main 守卫软链安全（`lib/main-entry.mjs` isMainEntry 两侧 realpath 整类收口——17 个脚本的 argv[1] 守卫在软链技能根下曾静默 no-op exit 0，附源码门防新增裸比较）、fleet 卸载残留不再假绿（profile 已声明但目录缺失降 WARNING 并写明原因，不再硬造 overallScore:100）、文档分层对账（过程报告归档 `docs-local/archive/`，不进技能面）。自检零网络、零外部依赖，任何机器上都能跑。

提交前门禁：`git config core.hooksPath .githooks`（一次性）启用 pre-commit 钩子，commit 时自动跑本自检，改完真源忘了同步在这一刻被拦。

## 脚本清单

脚本是四条车道共用的工具箱，全部在技能根的 `scripts/` 下，不随车道分家。

| 脚本 | 职责 |
| --- | --- |
| `run.mjs` | 一键编排全流程 + 写本地运行日志 |
| `fleet-sweep.mjs` | 集群批量治理与巡检：扫描工作区（含分组目录下钻）或已安装整批插件，按平台取目标版本，APP 插件按 `app.asar` 捆绑包核查套件，并关联 `~/.dsh/logs` 的启动失败；输出矩阵看板与 JSON 报告；`--pr-ready` 筛出可安全提 PR 的目标 |
| `run-log.mjs` | 运行日志查看（list/show）与脱敏导出（sanitize，`--pr-draft` 附带 PR 基线守卫）、日志交叉核对（doctor） |
| `env-doctor.mjs` | 探测本机 DSH 环境：版本、覆盖层、共享农场悬空软链、两层 patch、插件、进程、幽灵宿主（进程代际）、tsconfig paths 假绿、宿主半与客户端半启用就绪度；`--brief` 省略 patch 行原文（约降 94% 体积） |
| `env-heal.mjs` | 覆盖层旧包自愈（默认 dry-run） |
| `guide-sync.mjs` | 定目标版本 + 取官方升级指南：默认分支受管快照按 1 小时 TTL 刷新，tag 快照仅在离线兜底并标 frozen |
| `code-scan.mjs` | 扫描插件代码，匹配官方变更锚点（带指南文件与行号出处）；第五个参数给合成指南目录时并入包面差分的虚拟指南，官方没记的命中来源标 `types-diff` 并单独计 doc-gap |
| `standards-scan.mjs` | 上游常设规则检出（7 条机械可判项，带 defensive-patterns 出处，id 清单见上方来源表）；`--rules` 出规则表 |
| `codemod.mjs` | 确定性代码与包面自动修补：修复 Loader 入口导出面、宿主核心包 peer 依赖、顶层 await；默认 dry-run，`--apply` 才落盘并备份 |
| `types-diff.mjs` | 宿主 .d.ts 与导出面差分（包面真源）：比对前后两版符号指纹，提取破坏性删除并按基线版本合成虚拟指南落盘；`run.mjs` 自动编排留存签名快照，`code-scan` 按窗口基线消费 |
| `fix-peer-deps.mjs` | 批量把宿主核心包从 dependencies 挪进 peerDependencies；默认 dry-run，`--apply` 才落盘并备份 |
| `seams.mjs` | 接缝查询：包名或 API 符号在指南锚点表与本机宿主里的双源结论；无显式指南根时优先默认分支受管快照，再退宿主版本缓存 |
| `quick-smoke.mjs` | 内存级 Cordis 冒烟，含 Mock 兜底披露 |
| `plugin-audit.mjs` | 四维性能架构体检，可叠加官方指南交叉 |
| `log-doctor.mjs` | 解析 `~/.dsh/logs/` 的宿主故障 |
| `scaffold.mjs` | 五形态插件脚手架 |
| `write-gate.mjs` | 创作体检门：硬门禁自动判，软指标透传待裁量 |
| `sync-skill.mjs` | 技能面同步与漂移检查 |
| `release-check.mjs` | 发布前预检：版本一致、`v<版本>` tag、npm 是否已发布、`npm pack` 必需文件与夹带、自检、工作区；只读，不自动打 tag 或发布 |
| `cli.mjs` | npm bin 入口（`npx plugin-fast-adapt doctor\|fleet\|check\|new`），兼容 `<插件目录>` 转发到 run.mjs |
| `self-test.mjs` | 自检 |
| `scripts/lib/` | 扫描器、指南解析、运行日志、客户端半判定、宿主发现与宿主模块探测、桌面 APP 与 asar 包面、PR 基线守卫、发布规则、`package.json` 读取、缓存根、备份约定（各层为独立模块，CLI 入口只 re-export，不反向依赖） |
