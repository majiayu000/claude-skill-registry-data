---
name: fix-ci-e2e-flake
description: 诊断并修复 CI 偶发、本地稳过的 Playwright e2e 失败（flake）。当用户提到 CI e2e 偶发失败 / flaky / 本地跑没问题但 CI 挂了 / e2e 不稳定，或贴出 toHaveCount / toBeVisible / timeout 报错、expect(locator) call log 时使用。
---

# 修复 CI 偶发 e2e 失败（flake）

本仓库 e2e 用 Playwright + `_electron` 启动真实 Electron，通过 `window.__E2E__` 探针调服务。CI 偶发、本地稳过的失败**绝大多数不是产品 bug，而是断言写法不够鲁棒，或 CI 环境噪音（extension host 崩溃、进程启动慢、定时器竞态）**。核心套路：**判定真回归 vs flake → 读 call log 的“失败形态” → 把断言收敛到“被测对象本身” → 本地验证 happy path 不破 → 经验追加到案例库**。

> ⚠️ 第一原则：**不要为了让 CI 变绿而削弱对被测行为的覆盖**。鲁棒化 = 排除背景噪音干扰，被测断言强度不变。只能靠放宽真正的被测断言才能过 → 它可能是真回归，别盖住。

## 判定流程

1. **真回归 vs flake**：本地 `--repeat-each=5` 能否复现（本地稳过+CI 偶发→flake；本地也挂→回归）；同 commit 重跑能过=flake，每次必挂=回归/结构性缺口；**retry 救得回=瞬时竞态（flake），救不回=结构性（test 超时击穿/真回归/产物缺口）**——分类第一信号；`git log -p` 看失败 spec 是否刚改过；怀疑回归时 `git stash` 纯净基线复跑（对比前两边都先 `pnpm build`）；核对 CI 堆栈绝对路径（`D:\a\...` 是 runner 路径）语义对得上你改的目录。
2. **读 call log 失败形态**：count **波动**=背景元素间歇出现（噪音污染全局 count）；count/received **稳定停错值**=被测对象自身没就位（真回归/定时器没触发/fire-once 空转）；`waiting for locator` 恒 0=渲染没发生/探针没触发/选择器错；timeout 且无元素=往前看前置步骤；**元素 visible 但 click 超时 + `... intercepts pointer events`=被兄弟元素遮挡**（hit-target 检查走 elementFromPoint，水平布局溢出时常见，见案例 42）。
3. **已知噪音源**：extension host 偶发崩溃（`ExtensionHostClientService._handleCrash` 发背景 toast + error 日志）；renderer 定时器竞态（auto-hide/auto-read 在 CI 晚几百 ms）。
4. **最小且鲁棒的修复**（优先对齐同文件已鲁棒化的兄弟断言——同文件内有的步骤已加固、有的还裸，后者是遗留薄弱点）：噪音污染**列表**→`.filter({hasText:'<被测唯一文案>'})` 收敛；噪音污染**全局单值/一次性状态**→从源头禁用无关子系统（先 grep 确认无 spec 依赖）；定时器/异步竞态→`expect.poll`/`toHaveCount({timeout})`，少用固定 `waitForTimeout`+硬断言；纯环境型→别强改产品，记录案例库。
5. **验证**：诊断前先确认产物链是新的（`pnpm build`；手跑单 LSP spec 还需 `pnpm ext:build`+`extension-host/dist`+`vendor/typescript-language-server`，缺→符号空/探针缺=产物问题非回归）。`UNIVERSE_E2E_NO_TAG_FILTER=1 pnpm --filter @universe-editor/editor exec playwright test e2e/specs/<spec>.ts [--repeat-each=5]`（cwd 落在 apps/editor，会命中该目录的转发 config 从而套用默认 tag 过滤——不带 `NO_TAG_FILTER` 时全 `@regression` 的 spec 会直接报 “No tests found”，看着像路径写错）；全量 `pnpm e2e`（输出多，只截错误）。本地无法复现 CI 噪音是常态——目标是“鲁棒化没破坏 happy path”。
6. **沉淀**：把“失败形态→根因→修法”追加到 `references/cases.md`（**信号行必填**），并在下方「案例索引」补一行。这是本 skill 长期价值所在。

## 案例索引（按失败信号速查，命中后去 `references/cases.md` 读详情）

- call log count **波动**=背景噪音 → 案例 1；全局单值/一次性状态同轮多挂=同一噪音源打一片 → 案例 2
- `Test timeout of 30000ms exceeded`（非 poll message）=test 天花板击穿 → 案例 3/10/32
- CI 每次必挂+本地稳过+received 恒空+retry 救不回=伪 flake（CI 缺产物）→ 案例 4
- `expect.poll` 里 `keyboard.press` 后 received 稳定错值=盲按污染被测对象 → 案例 5
- `Execution context was destroyed ... navigation`（fire 后页面 reload/导航再 evaluate）→ 案例 6；冷启动首个裸 evaluate、无任何导航/崩溃（utility world 销毁，挂 CDP 后不复现）→ 案例 58；`Resulting promise was garbage collected` 栈在 evaluateWhenRestored 内（同竞态第二种消息变体击穿只认 destroyed 的守卫，retry 救不回≠非瞬时竞态）→ 案例 78
- 冷启动首 poll 恒 `""`：局部硬编码 timeout 盖 CI 分档 / 首 poll 漏带大 timeout → 案例 7/25/31
- `EBUSY/EPERM rmdir` 栈在 teardown=Windows 文件锁 → 案例 8；`ENOTEMPTY`+`.json.tmp`=storage 原子写竞态 → 案例 17；EPERM/EBUSY 在 test body finally 删「app 打开/watch 的目录」+retry 救不回=app/daemon 还活着（fixture teardown 在 finally 之后），用 harness `scratchDir` 排到 closeApp 后 → 案例 77（本地 smoke.* 冷启那批已迁，判据与 shared fixture 例外见 77b）
- `runCommand`+`expect.poll` 分离、received 卡死初值=fire-once 在就位前空转 → 案例 9
- click 把状态切离默认后 received 恒卡默认值=mount 后 fire-and-forget reconcile 迟到覆盖 → 案例 27
- 上轮修完形态变了仍挂=只治了表象，复合根因继续剥 → 案例 11/30/40
- `Target page ... has been closed`+退出码 0xC0000005：单实例过、多实例崩=parcel watcher → 案例 12/16/44；sharedApp 下崩点飘忽受害者无辜 → 案例 26
- `Worker teardown timeout`+测试全过：有 fixture 名=quit 链 veto → 案例 13；无 fixture 名+事后有孤儿=孤儿子进程握 CDP pipe → 案例 45；无 fixture 名+事后无孤儿=多 shared app 串行 closeApp 超预算 → 案例 63
- 滚动采样 received 单调爬升、`--workers=1` 过 `--workers=4` 挂=测量瞬时值 → 案例 14
- 滚动恢复断言 frac 异常（RAF 过冲/虚拟双峰/像素中点落末条）→ 案例 15/34/41
- 仅 CI Windows 确定性挂+涉及 tmp 路径/git=8.3 短路径 → 案例 18；URI 字符串稳定差 `%7E`/`~` → 案例 29
- 新 spec `--repeat-each` 批量挂、received 恒他人写入值=多层叠加 → 案例 19
- `--workers=1` 确定性全挂+stash 回 HEAD 仍挂=既有脆弱点被激活，别当环境噪音 → 案例 20/30
- sharedApp 多 ghost tab / 跨 spec 状态泄漏=reload 不拆 main 态 → 案例 21/40
- 关闭编辑器后紧接 model 操作、修改静默丢失=dispose 竞态 → 案例 22
- 某提交后多 spec 同红形态各异=`git show` 看时序变更波及面 → 案例 23；补了 `.catch` 仍挂=永久 pending → 案例 24
- `extension host may only execute _workbench.* commands not "<ext.cmd>"`=激活竞态 → 案例 35
- 拖拽 spec received 恒 0（稳定卡值）=drop 在 Monaco 就位前 fire → 案例 36
- workspace 切换后紧接的命令 received 恒初值=host 异步 re-pin 窗口 → 案例 37；boot 后 `openWorkspace` 的 LSP spec provider poll 恒 0 / teardown 报 Disposable 泄漏（栈在 `_createProvider`）=双重启竞态，用 `workspaceSeeder` launch pin workspace → 案例 54
- 等满 timeout 恒 not found 且该时长==产品放弃点=根本没就位（产品 bug）→ 案例 38
- click 侧栏后 received 恒 explorer / 快照 `Explorer [pressed]`=后台逻辑抢容器 → 案例 39/40
- 元素 visible 但 click 超时+`intercepts pointer events`、本地全绿=en-US+1280 窗口溢出遮挡 → 案例 42；点击超高 Monaco `.view-lines` 容器中心、CI relayout 后中心滑出可见区被 Welcome/标签栏挡 → 案例 54
- 仅 CI Windows 确定性挂+断言基于行/列宽度（getBoundingClientRect/scrollWidth）+失败截图视口恒等于 runner 屏宽（1024x718）=runner 屏 1024x768 夹窄默认 1280 窗口，布局断言在 Windows 上测的是另一个场景 → 案例 92
- `toBeFocused` 恒 inactive+无 workspace 冷启动=bootstrap 一次性焦点恢复抢焦 → 案例 43；测试中途 openWorkspace 后编辑器区内焦点被抢=workspace restore 窗口 editor 分支裸抢 → 案例 53
- 纯黑页+probe 恒无+业务无关 spec 同轮随机挂=bootstrap RPC 被 gate 丢弃 → 案例 33
- 本机裸 `electron.launch` 报 `Process failed to launch!`（exitCode=9）、CI 正常=本机环境 → 案例 28；**CI Windows** 同报错+ICU 加载失败/文件被占用+同窗口多 worker 齐挂=runner 文件锁窗口，harness `launchElectron` 已内建重试 → 案例 72；**CI Linux** 报 `spawn ETXTBSY` 栈在 launchElectron 内=瞬时守卫正则不匹配新变体 / Windows 重试耗尽仍挂=锁窗口超预算（Defender 排除根治）/ Windows 报 `Electron failed to install correctly`=同族新变体（已并入守卫）→ 案例 72b；报错**无 `electron.launch:` 前缀**+trace error 条目早于重试留痕=playwright 内部游离 promise unhandledRejection 击穿守卫（已 pnpm patch playwright-core）→ 案例 72c
- 失败仅集中 DnD 类且重跑能过=headless 手势时序 → 案例 46；锁屏时剪贴板用例必败 → 案例 47
- 终端 spec 在 WSL 下 initial+retry 确定性挂、续行文本比预期多一个 `"`（CI 全绿）=把 pty 对输入的回显当成了 shell 输出（缓冲区含某段文本 ≠ shell 执行过；快 shell 赢 race、慢 `$SHELL` 必输），定位判据锚「行首」→ 案例 87
- 新写「重启后状态仍在」用例 initial 挂/retry 过、failed 在自建 poll 等持久化值、received 里混入别的类型条目（view）=renderer 的 debounce 写还没落盘就 `closeApp` + 对整份持久化容器严格相等 → 案例 88
- chord 用例卡 `defocusEditor` 等 focus 变 false+retry 秒过=defocus 时序噪声（观察中）→ 案例 48
- `Alt+<n>` 偶发等于没按（`element(s) not found` 恒 0 / received 恒初值）+ 失败现场 DOM `activeElement` 已在目标区内而 `when` 里的 `*Focus` 键读到反向值 = **焦点键陈旧**（逐 Part 键由 tracker 记账；同一次按的上下文不同会走不同代码路径——浮层开着走 React handler、关着走全局 binding）→ 案例 90（已修：键改 DOM 派生 + 原子读不变量断言）
- 列表相等断言 received 是 expected 前缀子集+采样点为固定 sleep=增量渲染截半，poll 到收敛 → 案例 49
- sash 拖拽/尺寸持久化 spec，reload 后目标 pane 高度稳定卡等分值=异步 reconcile 落后于 Allotment 首次布局、preferredSize 挂载后是 no-op → 案例 50；**修完同断言再挂**=等分值经 onChange→debounce 落盘污染磁盘，恢复路径修得再好读的也是脏值，须收窄落盘权到用户动作 → 案例 50b；**再挂且诊断现场 mem==DOM==贪心值**（磁盘干净）=mem 记账被 onChange 覆盖、storedSizesKey/target 读脏 mem 锁死，恢复目标必须读独立的 persisted 权威源（save 序列化也走它）+settle 窗口内持续校验 → 案例 50c
- ACP 配置写入后立即建 session、echo agent received 恒 `"[]"`=异步镜像池 stale 滤空 wire 列表 → 案例 51
- `[MonacoLoader] not initialized` 栈过同步探针=poll 回调抛异常击穿等待 → 案例 52（**已修又再发**时先核对 main 上修复真实存在：`git log -S`）
- openWorkspace 后立即外部写文件、等 watcher surface 的 treeitem 等满 timeout 恒不出现=watcher 跨进程 arm（spawn utility process+subscribe）窗口吞事件，seed 可见≠订阅生效 → 案例 55；同一条事实的**非树消费者**（会话改动兜底）变体：等行恒 0 且失败取证里连该通道的 `.log` 文件都不存在=工作区 watcher 还是 idle 相位才 arm（`WorkspaceWatchContribution`），树的 catch-up 重读只治树，别的 consumer 得自己等就位信号 → 案例 89
- teardown 泄漏栈 `MainThreadLanguages._createProvider` 但**断言全过**、bundle 变更提交后 CI 恒定挂、泄漏数=activate 注册批大小=host activate 赢了 Monaco dynamic import，注册抛 not-initialized 半建 store 成孤儿+provider 批静默丢失 → 案例 56（区分 54：那是 dying-host 帧打 **disposed** 对象）
- 「忙等+可信输入」spec 本地 `--repeat-each` 必现 flaky、双形态交替（poll 恒 0 / byType 实收单元素但非期望类型如 `["keyup"]`）=setTimeout 提前量赛跑 CDP 输入派发 + dedupe 只留最慢样本；修=console token 确认主线程已阻塞再按键 + 断言放宽到事件族 → 案例 57
- 焦点门控断言（如聚焦时应出现应用内 toast）恒不出现+host.log 是 `notify shown` 而非 `skipped`=并行 worker `win.show()` 偷前台，断言前 `page.bringToFront()` 钉焦点 → 案例 59
- `EPERM rename '<x>.json.<pid>.<ts>.tmp'` 经 reviveWireError 从 main 传回、retry 救得回=产品原子写 rename 撞 Windows 瞬时锁（并发读/AV），修产品加重试 → 案例 60
- beforeAll 起本地 server 报 `did not start on <url>`、retry 救得回=固定随机端口撞占用（上轮孤儿 server）+stdio ignore 无诊断 → 案例 61
- `tokenColor(<word>)` poll 恒 undefined 到 `Test timeout`=Monarch 合并 span 使 exact-text 在 TextMate takeover 前结构性匹配不到，补显式 takeover 门控+test.slow → 案例 62
- 图表 reveal 断言 received 恒 `_row_…`（行在、选中类稳定缺失）+retry 变 "Loading…" 行不出现=reveal 与初始 load 双发请求、晚到 load 清选中（产品竞态）→ 案例 64
- 自启动 spec `closeApp: graceful close still pending`→force-kill 后 `CDP pipe still open`→teardown 30s 超时、事后无孤儿=某进程握子端 pipe 句柄（wsl 探测/agent 孙进程/并发 spawn 继承泄漏），终解=closeApp 父端 stdio destroy 兜底 + seed 收敛 + 死父指纹清扫 → 案例 65
- takeover 门控过后 `tokenColor` 仍恒 undefined（整行单 mtk1 span）/ token 有色但错色（mtkN 呈 +1 位移查了残表）=TextMate 双产品竞态（grammar 注册竞速 Monarch 丢 resolve 不 fire + 主题快照乱序落盘残表）；探针门控用 getOrCreate 会替产品治病，须改只读 → 案例 66
- 探针抛 `[E2E] no durable active ACP session` / echo agent `session/load` 拒 `session not found`、失败点在「发送 prompt 后立刻依赖 durable id/agent 落账」=user 消息本地乐观上屏不等握手；就位信号=agent 回复进 timeline，poll `status==='idle'` 有假窗口不充分 → 案例 67
- 大 fixture 多次 print 往返+裸 toBeVisible 等满不出现、initial+retry 同形态=「纯慢 vs 静默 '' 误路由」双假设同修（失败结构化传播+断言先 poll 任一终态）；artifact `if-no-files-found: ignore` 把上传路径错位静默吞掉致无现场 → 案例 68（**真根因后来定案在案例 69**）
- 案例 68 修后同形态再挂、仅 CI Linux 偶发本地 Windows 全绿+失败截图恒黑+aria 快照只剩 alert 空壳=fake CLI 大 stdout 后 `process.exit()` 在 POSIX 截断 → 尺寸路由翻转 → providerless webview 静默超时；修=`process.exitCode` 自然退出+poll 终态补 custom-editor+失败自动收集 userData/logs → 案例 69
- `toBeFocused` 恒 `data-focused="false"`（稳定卡值）但 aria 快照树内容已正确、断言前一步刚触发异步数据推送=焦点交付后 payload 落地触发 keyed remount 换掉被聚焦节点；修=ChangesTree 同 commit 换树保焦（模块级 viewId 意图集+microtask 过期）→ 案例 70（与案例 64 同族互参）
- poll context key 恒 `""`+截图纯黑+aria 只剩 alert 空壳+bootstrap 日志完整走完后静默（探针活着）=workspace-swap restore 竞态擦掉 swap 窗口内新开的编辑器；修=restore 读期间新进 editor 先 detach 再 re-admit 永不擦；React 19 逃逸边界错误静默 unmount root 且被 isBenignError 吞掉零留痕，createRoot 须显式 onUncaughtError 落盘 → 案例 71（与案例 33/69 的黑屏形态区分见详情）
- toContainEqual 的 received 里消息 text 是期望的**前缀**（echo 回声同截断、retry 截断点漂移）+失败点前是 `keyboard.type` 直接 Enter 打 Monaco 输入框=EditContext 异步落字赛跑提交，type 后先 poll `getAcpPromptText()` 全文再 Enter → 案例 73
- palette `type→Enter` 后命令效果 poll 恒卡初值、焦点断言正常+**双平台同 run initial+retry 全灭**+插桩（type 与 Enter 间加 evaluate）后不复现=QuickInputPanel useDeferredValue 旧列表被 accept（产品竞态,慢机高概率）,修产品 accept 路径不改 spec → 案例 74
- 复制图片后剪贴板 poll 恒无图、`toPngBase64` 快路径剥前缀未校验 payload=echo fixture 发伪 PNG 字节，main nativeImage 解出空图静默跳过写（**多 worker 各自独立 app 时不复现，serial lane 共享 app 才现**）→ 案例 75；Ctrl+V 粘贴后 chip 恒不出现、仅 CI Linux=xvfb 剪贴板 ownership 翻转不同步，seed 后先 poll 剪贴板可读回图再粘 → 案例 75b
- `electronApplication.firstWindow: Timeout 30000ms` 栈在 harness fixtures（非 spec 体）+ 报错无 `electron.launch:` 前缀（launch 已成功）+ initial+retry 双挂 + 伴随无 fixture 名 `Worker teardown timeout`=post-launch→pre-window 相位被 runner 环境窗口拖死（72 家族守卫不覆盖此相位），harness `launchAppReady` 已内建整链重试+log dump+closeApp 防孤儿 → 案例 76
- webview/iframe 计数钩子 poll 恒 0+initial/retry 同形态+失败 commit 与被测链路无关=钩子以静态 HTML 标记为门控 `if(!obj) return` 静默空转（案例 9 iframe 变体）叠加单次写赛跑 createFileSystemWatcher arm 窗口（案例 55 exthost 变体）；修=poll 对象本身就位+钩子守卫改 throw+poll 内幂等重写 → 案例 79
- teardown 泄漏栈在 Monaco `bindDocumentChangeListeners`+断言全过+全 ts spec 恒定挂=provider 挂 `onDidChange` 后 model 级 `ModelSemanticColoring`（活到 teardown）把订阅存普通数组成孤儿 root（泄漏门误报）；修=proxy 侧包装 event 给订阅 `setParentOfDisposable(store)` 锚定 root 链（区分 54 dying-host/56 半建 store）→ 案例 80
- 自启动 spec 中途 openWorkspace 后 `getActiveEditorUri().toBeFalsy()` 恒停旧值（`a.json`）或 `release-notes:whatsNew`、`--repeat-each` 可复现=手写 state.json 漏了 harness `INITIAL_STATE` 的 `app.releaseNotes.lastVersion` pin，升级 "What's New" 标签异步打开既污染空 workspace 又触发 persist 跨通道赛跑把 A 写进 B；修=seed 合并 `INITIAL_STATE` → 案例 81
- output 过滤后写真实 logger 的高等级行 10s 不可见、仅 CI Windows 某 shard 双挂、本地大量复现失败=先把「写链路」与「过滤可见」断言分层并加失败 dump，再逐项证伪（文件落盘/mtime、等级解析、Monaco 可见性、teardown 顺序红鲱鱼）；「aria 只剩 alert 空壳」先查 teardown `expectNoLeaks` 先 unmount 再拍 snapshot → 案例 82
- `sideBarVisible` 恒 false **但同一时刻** treeitem 的 toBeVisible 已过（矛盾指纹）+ 侧栏宽度 0 而树行仍在 DOM=裸 fire 了 toggle 命令 `workbench.view.explorer`，一半概率把 Explorer 关掉；改走幂等 `WorkbenchPO.showExplorer()`（读状态再决定是否 fire）→ 案例 83
- 键盘 ContextMenu 键断言仅 CI Linux 确定性挂+`detail===0` 恒空+retry 同形态+Windows 全绿+新 spec 首跑=keyup 补充 contextmenu 是 Windows 专属 Chromium 契约，断言改平台感知（win32 精确/非 win32 0..1 且形状不变，非弱化）→ 案例 84
- 虚拟化行出窗断言 `not.toBeInViewport` 但 ratio=1 且 rect 真在窗外（矛盾指纹）=IO 采样到 transform 前瞬态帧；改 rect 判窗后又稳定停中间值=Tree reveal useLayoutEffect 被 watcher 初始 refresh 的 structureVersion 变化重跑、scrollIntoView 撤销 scrollTop=0；修=poll 内每次先重设 scrollTop=0 再读 getBoundingClientRect 判窗外 → 案例 85
- 键盘 ContextMenu 键开出的菜单 **count 恰 1 但缺行级项**（Rename…/Delete not found）+ 本地确定性复现=守卫判据失效致空白区菜单 last-wins 顶掉行级菜单；根因=keyup 补充事件坐标是**焦点元素中心不是 (0,0)**（上一轮按未实测的 (0,0) 收紧守卫），判据须换 `button === -1`（CDP 右键恒 `button: 2`）；改共享守卫判据后必须回查所有模拟该事件的单测否则假绿 → 案例 86
- 预填/选区类断言 received 是**光标默认位**的旧值（`#TestValue` 变 `#const`）+ 同文件同族 setup 早已 `expect.poll` 只有这一处裸 fire + 本机高概率挂/`git stash` 回基线同挂=探针 setup 丢掉了返回值，`openWorkspace` 后活动编辑器还没就位/选区被迟到 adopt 覆盖 → 案例 91

- 连续键盘 grow → shrink 恰差一个步长、启动窗口内真实 Allotment 单测稳定复现=onChange 启动恢复撤销键盘操作（产品竞态），键盘与拖动共用用户操作标记 → 案例 93
- focusedView 已到位但立即重开 Ctrl+Tab 首行仍是 Files、retry 恢复=FocusTracker 延迟 settle 而 picker 只取一次快照，打开前只读 poll MRU head（同查 Ctrl+P）→ 案例 94
- 子代理全文已到但 `live=false, sawLive=false`、展开 click 比末块观察窗更慢=采样错过流式阶段；仅延后封口又出现 `mdparse.calls=1`=展开前已发完，首块挂载握手 + 末块采样握手保留真实增量渲染 → 案例 95

- 非快捷键用例在切组前等 `editorFocus=false` 恒 true、还没按 chord 就超时=场景搭建耦合无关的移焦步骤，改走同一切组命令，保留活动组与业务断言 → 案例 96
- 反向断言「某日志为空」CI 偶发收到**一条逐文件窄查**=断言挂在一场赛跑上（该通道按设计在特定相位就是会响），改判**形态**（目录 spec `/...`/`/*`）；改完用 fake 故障档验信号仍在 → 案例 97
- `type`+`Enter` 盲打后 `waitForHidden` 超时、现场只有「对话框没关」=诊断黑洞；打字前 `input.focus()` + Enter 前断言落字，失败点前移（重跑即绿=环境噪音，只加门控不改产品）→ 案例 98

## 关键参考路径
- `apps/editor/e2e/specs/` —— 所有 e2e spec；`@p0` 阻塞 CI，`@p1` 次级
- `apps/editor/e2e/fixtures/electronApp.ts` —— `workbench` fixture、`runCommand`/`waitForRestored`/`statusBar` 封装、`closeApp`
- `apps/editor/src/renderer/e2e/probe.ts` —— `window.__E2E__` 探针
- `apps/editor/src/renderer/services/extensions/ExtensionHostClientService.ts` —— ext host 崩溃→通知（CI 噪音主源）

## 其它
- 后续用本 skill，发现新经验，按判定流程第 6 步同步更新案例库与索引
- 修复了某个e2e本身测试稳固性的问题，那么需要整体评估一下所有e2e是否也存在同样的问题，并一并修复
