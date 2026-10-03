---
name: ui-sweep
description: "在 SOP 截图前把全站可交互元素系统性点一遍、改完一批 UI 后做回归扫描、用户说“把所有按钮点一遍”、或需要一次交互冒烟测试时触发。用 agent-browser 驱动 + 通用化遍历引擎,逐屏逐元素点击观察并八分类记账,产出 JSONL 台账、每屏截图与报告。"
argument-hint: "[站点URL] [登录态说明,可选]"
---

# ui-sweep — UI 全量交互遍历

SOP 截图前先把界面系统性点一遍,揪出「点了没反应」「点了报错」这类暗坑,再产 SOP 或回归验收——比人工肉眼过一遍快,比随机 monkey 测试有确定性覆盖保证。驱动是 [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)(★40.5k,Apache-2.0,专为 AI agent 造的 Rust CLI:a11y 快照带元素引用、点击自带遮挡检测、`console`/`errors` 采集、confirm/prompt 显式接管、`state save/load` 登录态注入),外加自研 ~350 行遍历编排(`scripts/sweep.mjs`,自己接管 agent-browser 会话生命周期 + 逐击域名校验,见下方「域名边界是两层」)。2026-08-13 在某内部 SPA 项目实跑验证:10 屏 218 条结果记录(205 次实际点击),0 页面异常、0 console 报错,揪出 1 个真缺陷(某「添加」类按钮在空输入时完全静默——既无提示也无变化)。

## 环境要求

- `npm i -g agent-browser`——自带 Chrome for Testing,无 Playwright 依赖(Apache-2.0)。本 skill 按 0.27.0 实测(headless Chrome for Testing 152)编写,其他版本行为可能有出入。
- Node.js(跑 `scripts/sweep.mjs` 与 `scripts/export-state.mjs`);`scripts/export-state.mjs` 额外依赖 `playwright-core`(`scripts/package.json` 已声明,`npm i` 一次即可)。

## 流程六步

1. **依赖自检**:确认 `agent-browser --version` 能跑通;确认目标是自家或已获授权的站点(见下方安全边界)。
2. **登录态注入**:用 `scripts/export-state.mjs --cdp <CDP地址> --out <state.json> --origin <origin>...` 从一个已登录的真实浏览器(通过 CDP 连接)导出 cookies + 各 origin 的 localStorage,拼成 `{cookies, origins}` 结构;**把这个 state.json 的路径填进 `sweep.config.mjs` 的 `STATE_FILE` 字段,不要自己手动跑 `agent-browser state load`**——引擎会在自己建好的受限会话里自动加载(见步骤 4「跑引擎」;手动预载会在引擎接管会话之前把会话建起来,导致引擎的 `--allowed-domains` 对这个会话失效,0.27.0 实测)。**绝不碰口令明文**(整个流程不涉及输入密码,只搬运已登录浏览器的态);**登录态文件用完即删,绝不把它入 git**。
3. **屏清单编制**(唯一需要项目定制的部分):先手动或用 `agent-browser open <ROOT>` + `snapshot -i` 抓首屏快照摸清结构,再把每个"屏"写进项目自己的 `sweep.config.mjs`。"屏" = 从 `ROOT` 出发的一条确定性恢复路径(`{id, path: [{css}|{text}], settleMs?}`,`path` 是从根到达该屏依次要点的元素);SPA 的浮层/抽屉/页签各种展开态,每个算一个独立屏,不要漏。**需要孤儿功能对账时**:同一步里按下方「孤儿功能对账(可选)」一节生成 `INVENTORY`,填进 `sweep.config.mjs`(不生成则该功能整体静默关闭)。
4. **跑引擎**:`node scripts/sweep.mjs <path>/sweep.config.mjs`。先跑一次 `--check-config` 确认 config 合法(缺 `ROOT`/`SCREENS` 会立即报错退出,不会静默空跑;`--check-config` 的输出会打印引擎实际生效的 `ALLOWED_DOMAINS`/`STATE_FILE` 值,便于跑真站点前核对);全量遍历跑默认模式(不带 `--strict`,见下方取舍说明)。引擎会**自己接管 `agent-browser` 会话生命周期**:启动时先 close 掉自己专用的隔离会话名(`--session ui-sweep`,不碰你自己在用的其他会话),再用带 `--allowed-domains <ALLOWED_DOMAINS>` 的命令重新建一个——这一步是必须的,因为 `--allowed-domains` 只在浏览器进程**启动那一刻**生效,已经在跑的会话不会因为后面命令换了值而重新生效(0.27.0 实测);`sweep.config.mjs` 配了 `STATE_FILE` 时,引擎会在这个新会话建好之后自己 `state load`。`sweep.config.mjs` 不填 `ALLOWED_DOMAINS` 时,引擎自动从 `ROOT` 的 hostname 推导;需要放行多个子域名/上游域名时,显式在 config 里写 `ALLOWED_DOMAINS = 'a.example.com,b.example.com'`(逗号分隔)。**`--allowed-domains` 的真实边界见下方「域名边界是两层」——它挡不住点击触发的跳转,可靠的边界是引擎自己的逐击域名校验。**
   **会话收尾**:引擎跑完(含失败退出、收到 SIGINT/SIGTERM/SIGHUP)会自动关掉自己的 `ui-sweep` 会话,不用手动 close;关闭失败时会往 stderr 打一行提示,照提示手动执行 `agent-browser --session ui-sweep close`。会话名固定为 `ui-sweep`,同一台机器同一时间只跑一个 ui-sweep,同时跑两个会互相关掉对方的会话;人工复核真缺陷时另起一个自己起名的会话(`agent-browser --session <名字> ...`),复核完执行 `agent-browser --session <名字> close`。
5. **结果判读**:引擎把每次点击归到八类之一——`ok-changed`(指纹变化,含 checkbox 勾选态)、`dead`(无任何反应)、`dialog-dismissed`(弹窗被驳回)、`click-error`(点击命令本身出错)、`page-error`(页面抛未捕获异常)、`skipped-denylist`(命中拦截名单未点)、`miss-not-found`(按 role+name 定位不到目标,回落按位仍找不到)、`left-domain`(点击后跑出了 `ALLOWED_DOMAINS`,引擎已当场强制拉回现场——见下方「域名边界是两层」)。另有 `note-relocated-by-index`——**这是一条附注,不是独立分类**:当按 role+name 定位不到时,引擎回落到「同角色序列里的同位置」重新命中并记这条附注(带上实际命中的元素名),回落命中后该次点击仍会正常归入上述八类之一,不单独计数。**假阳性定性法**(来自实跑复盘,先按这几条筛,再决定是否需要真浏览器复核):
   - `click-error` 先查 `dialog` 台账——同步 `window.prompt`/`confirm` 会堵塞点击命令直到超时,这类"报错"往往是按钮本身正常、只是弹窗同步阻塞;台账里能看到 prompt 内容和驳回记录即可排除。
   - `dead` 先想"同屏状态累积":引擎默认不追加恢复现场(见 `--strict` 说明),前序点击留下的展开态/提示可能掩盖了本次点击的效果,导致误判 dead——先用 `--strict` 对可疑 `dead` 清单重点复跑一次再下结论。
   - `miss-not-found` 先想「定位丢失」:多半是前序点击改变了面板态(目标元素被隐藏/移出可见区域/整体重排)、或语言/主题切换令元素名漂移,导致按 role+name 直接命中失败、按位回落也落空;不必然是产品缺陷,但若同一个元素在多次跑里稳定丢失,值得人工确认它是否真的被误删,或者角色/名字确实变了(需要更新 `sweep.config.mjs` 的屏清单)。
   - `left-domain` 不需要"定性"——它是安全边界事件,不是产品缺陷判读的对象;台账里每一条 `left-domain` 都已经被引擎当场恢复现场,不影响后续点击。如果一个元素稳定出现 `left-domain`(比如站内跳转到一个上游域名的正常链接),这是预期行为,不是缺陷,把该域名加进 `ALLOWED_DOMAINS` 即可让它正常参与遍历。
   - 当前态导航钮(已经在当前页的导航项)、被浮层盖住的报头/页面副本判 `dead` 属正常行为,不是缺陷。
   - headless 环境下全屏 API、原生日期选择器等浏览器 API 可能空转不生效,这是环境限制,不是产品问题。
   - 真缺陷(判定为产品问题的 `dead`/`click-error`/`page-error`)必须逐条用真浏览器手动复核坐实后才能定罪,不能只凭台账下结论。
6. **产报告**:照 `references/report-template.md` 的骨架产出——总量、真缺陷(已复核坐实)、假阳性定性(逐条说明排除依据)、观察级(不定罪但值得留意)、孤儿功能对账(见下方「孤儿功能对账(可选)」一节,未配 INVENTORY 时删除本节)、覆盖缺口(诚实记账哪些没点、为什么没点)六节。**孤儿功能对账一节必须逐字段点名对账**,台账里 `type: 'orphan-audit'` 那条记录有几个字段就在报告里落几处:`unreachable`(疑似真孤儿清单,逐条判读)、`broken`(打不通的入口,逐条带状态码)、`exempt_hits`(命中 exempt 的条目,只计数)、`inventory_hit_count`/`inventory_auditable_count`(覆盖率的分子/分母——分母已扣掉 exempt,天然不可达的条目不参与覆盖率;`seen_count` 是另一个字段,代表全部观测条目总数,含未列入 INVENTORY 的,仅供诊断,不是覆盖率分子)、`coverage_note`(覆盖缺口说明——**必须原样转述进报告的「对账覆盖缺口」一节,不得省略、不得改写成摘要**;采集失灵或整轮零采集时这个字段会带警告文字,报告里同样要如实带出,不能因为它读起来"扫兴"就悄悄压下去)。

## `--strict` 模式取舍

默认(不带 `--strict`):每屏内只在上一次点击改变了状态时才恢复现场,连续多次"无反应"的点击不重复恢复——跑得快(约为 `--strict` 的一半时间),代价是同屏状态可能累积掩盖后续点击的真实效果,产生上面提到的 `dead` 假阳性。

`--strict`:每次点击后无条件恢复现场(重新 `restore(screen)`)再点下一个——治状态累积假阳性,代价是全量跑慢约一倍。**建议**:初跑用默认模式覆盖全站,再对 `dead` 清单里可疑的条目用 `--strict` 重点复跑定性,不必对全站强制 `--strict`。

## 孤儿功能对账(可选)

现有流程是**遍历视角**:点遍 UI 上存在的元素,查「点了没反应」。它是黑盒的,天然查不到「功能实现了但 UI 上根本没有入口」——因为没入口的东西不会出现在 a11y 快照里。本节加一个**对账视角**:代码侧清单(INVENTORY)∩ 遍历侧实际到达(`network requests`)→ 求差集,两个视角互补。**不配 `INVENTORY` 时本节功能整体静默关闭,行为与不启用本节完全一致,零副作用。**

### 三类结论

| 结论 | 判据 | 含义 |
|---|---|---|
| `unreachable` | 在 INVENTORY 里、整轮遍历零触发、不在 exempt、且未被拦截名单间接跳过 | 疑似无 UI 入口(真孤儿候选) |
| `broken-entry` | 遍历触发了,但响应状态 ≥400 | 入口存在但打不通 |
| `exempt` | 命中 `sweep.config.mjs` 里的 exempt 正则 | 预期就没有 UI 入口(webhook/健康检查/内部调度),只计数不报警 |

覆盖不全时(某屏 restore-failed / miss-not-found 等原因没走完)相关条目单独标「note-partial-coverage」——**覆盖不全的部分不得判 unreachable**,这是诚实记账,和报告模板「覆盖缺口」一节同源。

### 怎么生成 INVENTORY

引擎(`scripts/sweep.mjs`)不懂任何技术栈,清单必须由 Claude 现场按项目实际用的技术栈生成,填进 `sweep.config.mjs` 的 `INVENTORY` 字段:

```js
export const INVENTORY = {
  apis: ['GET /api/projects', 'POST /api/projects/:id/archive'],  // 方法 + 路径模式,:id 代表变量段
  routes: ['/dashboard', '/projects/:id'],                        // 前端路由模式
  exempt: [/^POST \/api\/webhooks/, /^GET \/health$/],            // 预期无 UI 入口,不计入 unreachable
}
```

常见栈的提取手法(找路由/接口注册代码,不是找业务逻辑代码):

- **Go chi/gin**:搜 `r.Get(`/`r.Post(`(chi)或 `router.GET(`/`router.POST(`(gin)一类的路由注册调用,路径字面量就是 API 清单条目,`:id`/`{id}` 段统一记成 `:id`。
- **Express**:搜 `router.get(`/`app.post(` 等 `router.<method>(路径, ...)` 调用,同上取路径字面量。
- **FastAPI**:搜 `@app.get(`/`@router.post(` 等装饰器,路径写在装饰器参数里。
- **React Router**:搜 `<Route path="...">` 或 `createBrowserRouter([{ path: "..." }])` 里的 `path` 字段,拼成 routes 清单。
- **Vue Router**:搜 `routes` 数组里每个对象的 `path` 字段。

**生成后必须抽样核对真实文件**:随机抽 INVENTORY 里 3~5 条,打开对应源文件确认路径字符串确实存在、方法确实对——不许凭空列或凭记忆列,清单本身若是编的,后面的差集结论全部作废。

### 四类判读指南(与 dead click 假阳性经验对称)

拿到 `unreachable`/`broken-entry` 清单后先按这几类筛,再决定是否真的是产品缺陷:

1. **权限相关**——管理员/高权限入口,在普通账号身份遍历时必然 `unreachable`(压根没登录态看不到那个按钮)→ 换更高权限的登录态复跑一轮,或者把这类条目列进 `exempt`。
2. **数据状态相关**——依赖特定数据状态才出现的入口(例如列表为空时没有「编辑」按钮)→ 遍历前先造好触发数据,或在报告里标注为「条件入口」而非孤儿。
3. **拦截名单相关**——破坏性按钮本轮只记不点(`skipped-denylist`),其对应 API 自然零触发,不是没入口,是本轮没点→ 对照台账里 `skipped-denylist` 记录的具体元素名(报告模板「覆盖缺口」一节列出的「拦截未点 <N> 项(<按钮名列表>)」),逐条比对 unreachable 清单里的条目是否只可能由这些元素触发,能对上的先排除掉,剩下的才进入下一步判读。
4. **覆盖不全相关**——某屏因 restore-failed / miss-not-found 等原因没走完 → 该屏相关的条目不得判 `unreachable`,只能标 `note-partial-coverage`,建议补跑覆盖到再复核。

### 真孤儿的三条件(同时成立才定罪)

1. 代码里确实有这个功能(INVENTORY 条目对应的真实路由/接口代码存在,已抽样核对);
2. 前端源码全文搜不到任何调用该接口/路由的地方(不是"遍历没点到",是"代码里根本没人引用");
3. 遍历整轮零触发,且已排除上面四类判读指南里的情形。

三条同时成立才能写进报告「真孤儿」结论;只满足遍历零触发这一条,只能算 `unreachable` 候选,不能定罪。

**安全边界不变**:对账只读 `network requests` 记录做归一化与差集比对,不新增任何写操作,不改变遍历本身的拦截名单与 confirm/prompt 驳回规则。

## 安全边界(硬规则)

- **破坏性按钮只记不点**:引擎内置默认拦截名单(吊销/解散/删除/退出/logout/sign out/revoke/dissolve/delete/remove/discard/drop/归档/archive/清除/clear/重置/reset/发送/send/保存/save/上传/upload 等中英正则——2026-08-13 补:此前英文 UI 的 `<button>Delete item</button>` 实测会被真点、POST 真发出,旧正则只有中文「删除」没有英文 delete,现补齐 delete/remove/dissolve/discard/drop 五个英文破坏性词),命中的元素只记入台账(`skipped-denylist`),绝不点击。项目可以通过 `sweep.config.mjs` 的 `DENY_EXTRA`(正则)**叠加**拦截范围,但没有任何配置路径能削减或覆盖这份默认名单——安全底线不可配置弱化。站点专属的噪音钮(例如某个非破坏性、但希望常年跳过的入口按钮)不进默认名单,用项目自己的 `DENY_EXTRA` 增补。
- **confirm/prompt 一律驳回**:每次点击后台账检查弹窗状态,只要检测到 `confirm`/`prompt`/`alert` 一律 `dismiss`,不产生真实写入。
- **域名边界是两层**(0.27.0 实测,如实两层表述,不做单层的"圈死"承诺):
  1. `--allowed-domains <ALLOWED_DOMAINS>` 只约束 `agent-browser` 的**显式导航**(`open`/`back`/`forward` 这类命令直接指定 URL 的场景)。**点击跳转拦不住**——页面里 `<a href>` 默认行为、`location.href` 这类点击触发的同窗口跳转,不受这个 flag 约束,实测里点了就真跳走了。这个 flag 还只在浏览器进程**启动那一刻**生效:`state` 预载(先 `state load` 再跑遍历)、复用一个已经在跑的旧会话,都会让它对当前会话失效,因为后续命令换的值不会让已经启动的浏览器进程重新读取配置。
  2. 可靠的边界在引擎自己身上:每次点击后,引擎解析 `urlAfter` 的 hostname,不在 `ALLOWED_DOMAINS` 集合内就记 `left-domain` 并**当场强制恢复现场**,不等到下一次循环。这一层不依赖 `agent-browser` 的 flag 语义,是本 skill 实际能兑现的域名边界承诺。`ALLOWED_DOMAINS` 缺省从 `sweep.config.mjs` 的 `ROOT` 推导 hostname,需要放行多个域名时可在 config 里显式覆盖(逗号分隔)。
  为了让 `--allowed-domains` 至少在"显式导航"这层上生效,引擎会自己接管会话生命周期(见「跑引擎」步骤):启动时先 close 掉自己专用的隔离会话(`--session ui-sweep`),再带着这个 flag 重新建会话,不依赖用户手动预先做任何事。
- **只扫自家或已获授权的站点**:不对未获授权的第三方站点跑本 skill。
- **登录态文件用完即删**:`export-state.mjs` 产出的 state 文件含 cookies/localStorage,属敏感凭据,用完立即删除,绝不提交进 git、绝不上传;`sweep-out/`(截图与台账)同样不入 git——目录下没有 `.gitignore` 时引擎会自动写入一份(内容为 `*`);已存在则保留你自己的规则,请自行确认它确实忽略了截图与台账。

## 已知局限(诚实声明)

- **checkbox 翻转仅指纹级验证**:指纹里补了 `input:checked`/`[aria-checked="true"]` 计数,能捕捉"勾选状态变了"的信号,但没有对每个 checkbox 的语义(勾上代表什么)做二次验证——不确定的场景仍建议人工复核一次。
- **headless 环境部分浏览器 API 空转**:全屏 API、原生日期/颜色选择器等在 headless Chrome 下可能不产生真实效果,对应的 `dead` 判定不代表产品缺陷。
- **canvas/自绘 UI 不在覆盖范围**:a11y 快照只认可被无障碍树感知的元素,canvas 画布或纯自绘(非标准 DOM 控件)的交互不会出现在遍历计划里,本 skill 覆盖不到,需要额外的专项验证。

## 出处

- 实跑数据(出处:实跑台账 ledger.jsonl):2026-08-13 某内部 SPA 项目实跑,10 屏 218 条结果记录(205 次实际点击,即 218 减去 11 条 skipped-denylist、减去 2 条 miss-not-found——这两类都没有真的发出点击)—— ok-changed 106 / dead 97 / dialog-dismissed 0 / click-error 2 / page-error 0 / skipped-denylist(拦截未点)11 / miss-not-found(定位丢失)2;其中 2 次命中 note-relocated-by-index(按位回落,附注不是独立分类,已计入以上对应分类)。当时的实跑版本还没有 `left-domain` 分类(本轮才补上,见「域名边界是两层」),因此实跑数据没有这一类的样本。0 页面异常、0 console 报错,揪出真缺陷 1 个(某「添加」类按钮空输入时完全静默)。
- 驱动:[vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser),0.27.0(headless Chrome for Testing 152)实测。
- 调研依据:内部工具链调研(GitHub 候选对比:agent-browser vs playwright-mcp/chrome-devtools-mcp(MCP 形态,全量遍历下 token/时延成本不成立)vs browser-use(非确定性)vs crawlee(URL 爬虫,SPA 屏内状态逻辑仍需自写)vs gremlins.js(随机 monkey 测试,已停维护))。
