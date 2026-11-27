---
name: dsh-plugin-diagnose
description: DSH 插件装了没生效、客户端卡 loading、宿主起不来的排障车道。log-doctor 解析 ~/.dsh/logs 的 startup 日志（StartupError、端口占用、未声明 inject、客户端入口死链）给根因与下一步动作；env-doctor 巡检 profiles 覆盖层旧包残留、共享 node_modules 农场悬空软链、两层 patch、宿主半与客户端半双面启用就绪度；env-heal 清理覆盖层默认 dry-run。触发词：插件装了没生效、插件不激活、客户端卡 loading、entry did not activate、web boot 失败、注入死链、宿主启动失败、StartupError、EADDRINUSE、日志诊断、覆盖层旧包、悬空软链、共享农场、环境体检、Silent Pending。
---

# 环境与启动故障车道

症状是「插件明明装了却不起作用」或「宿主根本起不来」时走这里。代码本身踩没踩破坏性变更不走这条车道，那是 `../adapt/SKILL.md` 的事；先确认环境干净，适配结论才可信。以下命令都相对工具根目录执行，工具根即本文件真实路径往上两级、含 `scripts/` 的那一层。脚本用自身文件的绝对路径定位，不必先 cd，从任何目录直接 `node <工具根>/scripts/<脚本>.mjs` 同样可行。本目录常以软链别名加载，shell 的 `cd ../..` 会按软链走错地方，确实要 cd 时用 `cd "$(realpath <本文件所在目录>)/../.."`。

## 第一步：看宿主日志怎么说

```sh
node scripts/log-doctor.mjs [--logs <目录>] [--limit 5] [--pattern '^startup-']
```

宿主启动失败（`StartupError`、端口占用、未声明 inject、客户端入口死链）此前要人工逐个 grep `~/.dsh/logs/startup-*.log`，再从 300 多行的 JS 字面量里抠 `failedPlugins` 与 `waitingForServices`。本脚本把这条排障路径固化：解析每份 startup 日志的头部元信息与多行 error 块、消息数组（容忍宿主的 `[length]: N` 伪数组标记），抽取预置信号，汇总成按根因分组的诊断并给可执行动作。

输出：`runs`（每份日志的 meta、failedPlugins、waitingForServices、inactiveEntries、signals）、`crashReports`（桌面 APP 崩溃报告）、`signalSummary`（按出现次数排序的信号加动作）、`verdict`（`clean`/`warnings`/`host-failure`）。非 startup 日志（dsh-web、maintain、env-sweeper、web-restart）全文扫信号，并抽出 `inactiveEntries`：宿主「N entries did not activate」警告下的每一条，带条目 id、包名和错误原文。错误是「already owned by process」一类时另报 `resource-locked`，那是 web 与 APP 同时开在抢同一份资源，不是插件代码缺陷。

**桌面 APP 的日志不在 `~/.dsh/logs/`。** APP 主进程的 stdout/stderr 接 `/dev/null`，宿主 stderr 只在内存留 64KB，唯一落盘的是致命错误时写的崩溃报告 `~/Library/Logs/DeepSeek Harness/crash-<时间>-<host|web-boot|renderer|main>.log`（只留最近 10 份）。log-doctor 默认一并读取（`--crash-dir` 可改），解析出来源、阶段、宿主诊断里的失败插件，以及渲染进程的报错尾巴。客户端半卡 loading 的证据主要在渲染进程那一段。APP 没崩就不会有报告，也就没有要追溯的故障。

**边界**：日志是宿主写的 JS 字面量而非 JSON，只做行级启发式解析，解析不到的字段留 `null` 不猜；信号是文本命中，动作是「怎么确认、怎么修」的第一步，不替用户拍板。

日志说插件装载失败时，先用运行日志 `node scripts/run-log.mjs doctor` 与代码侧状态并排：宿主报了它而最近一次扫描干净，嫌疑就在装载、挂载或环境侧，继续往下一步查。

## 第二步：巡检本机环境

```sh
node scripts/env-doctor.mjs <插件目录> --brief
```

`--brief` 把 `installedPlugins` 的 patch 行原文换成计数、进程命令截断到 120 字符，本机实测 80.5KB → 4.5KB（约省 2.1 万 token）。日常诊断八段结论都在；要逐条看挂载行或完整进程命令时去掉 `--brief`。输出 JSON，本车道重点看八段：

- `globalDsh`：全局安装的 DSH 版本和位置
- `desktopApp`：桌面 APP 自己捆的宿主版本（从 `app.asar` 只读取出）。APP 不用 npm 全局那份宿主，两者错开时带 `mismatch`：desktop profile 的结论以 APP 版本为准
- `ghostHost`：运行中的宿主进程是不是在跑旧代码。比进程启动时间与磁盘变更时间（安装目录/`package.json`/git 最后提交），超过 120 秒容差判 `stale`；`no-running-host` 只是没开宿主，`unknown`（Windows 无 `ps etime`、桌面 renderer）写明原因不猜。改完 Host 侧代码不重启就属于这一类
- `falseGreen`：插件 `tsconfig` 的 `paths` 指向不存在的 checkout（M1）。TypeScript 静默回落到 `node_modules` 的已发布类型，`typecheck` 全绿而实际类型是旧的；带 `findings`（alias、目标、解析后的绝对路径）与修复建议
- `overlayFindings`：profiles 覆盖层里与主安装脱节的包，带 severity 和原因
- `sharedFarmFindings`：共享 node_modules 农场（`~/.dsh/profiles/node_modules`）的悬空软链，带 `brokenCount` 与 `hostBackedBroken`（指向宿主安装树的是「宿主升级后包被移除」那一类，标 critical）
- `runningProcesses`：正在跑的 DSH 宿主进程（改 Host 侧代码后必须重启它）
- `activation`：插件启用就绪度。构建产物在不在、各 profile 挂没挂载、声明的 inject 服务在该 profile 有没有提供方特征（Cordis 静默 pending 风险）。目标不是插件形态（package.json 无 `dsh` 命名空间、无 `@deepseek-ai/*` 依赖）时记 `N/A` 不检查，否则按插件规则跑纯工具仓会把「无 main 入口」误报成 ERROR（2026-10-25 自审实录）。入口解析按 Node 语义，`exports['.']` 优先于 `main`，无 `main` 但入口写在 `exports` 的包不会再被误报
- `activation.client`：客户端半（dsh.client）三层判定，声明形状（合成器 boot 即 throw）、`./client` 产物（报 client bundles not found）、inject 目标名册死链（entry 卡 loading，整次 web boot 失败）。web profile 与桌面 APP 共用同一套 platform:web 前端，两端一视同仁。宿主 bundle 里按 profile 名开关的行（`disabled: !!js "ctx.get('profileContext')?.name !== 'desktop'"`，如 `ui-sidebar-browser`）只算进对应 profile 的名册，web 上 inject 它会如实报死链；其他判不了的 `!!js` 表达式按两端都有处理。名册证据分强弱：宿主内置、bundles 列名、overlay 挂载行为属强证据直过；包在依赖里但无行证据报 info 弱档让人确认（宿主是否自动挂载，静态分析判不了）。2026-10-25 实录：宿主半冒烟全绿、桌面 APP 起不来，真凶就是客户端半死注入

## 三类高频环境故障

**覆盖层旧包优先解析。** `overlayFindings` 非空时先处理覆盖层再谈别的。这是 issue #263 那一类事故：宿主升级后覆盖层里残留旧包，旧包优先解析导致运行时装载冲突，而且只换文件不重启宿主还会复现。上游已移除的包若被 overlay 显式补挂（`- insert:` 行）则降级 info，那是刻意保留的兼容垫片不是意外残留，直接拆会弄断还 require 它的旧插件，确认全部消费方改净后再清。

```sh
node scripts/env-heal.mjs           # dry-run，只报告
node scripts/env-heal.mjs --apply   # 真的移动（移到 ~/.dsh/.trash/<日期>/，不删除）
```

**共享农场悬空软链。** `overlayFindings` 只看各 profile 自己的覆盖层目录，共享农场是另一层。`~/.dsh/profiles/node_modules` 是指向宿主安装的软链农场（`@deepseek-ai/*` 加 react-dom、express 等传递依赖），宿主升级后包被移除就留下悬空软链，任何 require 它的插件都以 `ERR_MODULE_NOT_FOUND` 收场（2026-10-26 实测 209 条，宿主启动日志里 `client-runtime`、`orca-agent-hooks` 两行装载失败，而 `overlayFindings` 报 0 处）。这一层 `env-heal` 不处理，需手工清。

**两层 patch 都要看。** 除了各 profile 自己的 `cordis.patch.yml`，还有全局 `~/.dsh/cordis.patch.yml`，`dsh --dump-config` 显示它拼在每个 profile 的最后一层。只读前者会把它整个漏掉：本机全局层由 Orca 写入 `orca-agent-hooks` 行，引用的 `@deepseek-ai/dsh-hooks-claude-code` 没装，每次启动都报 `1 entry did not activate`，而工具报 0 处（2026-10-26 实测）。`installedPlugins[].patchEntries` 已把两层合并，`registered` 与 `disabled` 判定对两层都生效。

## 边界

- `env-doctor`、`log-doctor` 完全只读
- `env-heal` 默认 dry-run，真动手也是移动不删除
- 不改 DSH 本体，不动 `~/.dsh` 下的配置和 profile 声明
- 日志只落本机；解析结果含本地路径，对外反馈前先脱敏
