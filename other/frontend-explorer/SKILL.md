---
name: frontend-explorer
version: 0.1.2
description: 探索型前端测试——派一个「第一次见这个产品」的探索者，用 playwright-cli 驱真浏览器走完一段旅程，回一份按挡路程度排序的「在哪卡住 / 哪里看不懂」清单，每条带屏幕原文与截图证据。触发：探索一遍 / 走一遍 / 踢踢轮胎 / UX pass / 找新用户会在哪迷路。不用于判据已知的验收探针、回归测试、性能、代码评审。
---

# frontend-explorer — 探索型前端测试

脚本化测试回答「我已经想到的那件事还好使吗」。这里回答另一个问题：**一个从没见过这个产品的人
打开它——在哪停住，在哪盯着屏幕不明白？** 这两种失败形态就是全部产出；其余一切只为让这份产出诚实。

本 skill 对你的项目一无所知：应用在哪跑、怎么拿登录态、屏幕上的词什么意思，全部来自一份配置
（`references/config.example.yaml`）。想改本 skill 的文件去适配项目 = 那个事实该进配置。

## 前置条件

1. **一份配置**：复制 `references/config.example.yaml` 填好；含本机路径就别进版本库。做任何事之前先读它。
2. **应用在跑且可达**：`base_url` 可访问、其 host 在 `allowed_origins` 里。没在跑就按配置 `auth.setup` 起，
   不要自己发明启动方式。
3. **浏览器驱动 = `playwright-cli`**（`@playwright/cli`，0.x 命令面会漂，项目钉版本）：探索者经 Bash 调它，
   每个 persona 一个命名会话 `-s=<persona.session>`，与项目自己的会话及彼此隔离。**`-s=` 只隔离浏览器，不隔离账号**：
   本版一份 `session_file` = 一个账号 = 两 persona **串行**（第一轮打通的账号第二轮无路可走）；并行不在承诺面。不用 Playwright MCP、
   不用别的驱动、不调外部 LLM API。工具选型与登录态原则与 cto-orchestration `references/frontend-verify.md`
   同向（可选阅读，非依赖）。

## 流程（五步）

**1 — 准备会话。** 配置有 `auth.setup.command` 就跑它：它负责把应用带起来、签一个新用户、写出
`auth.session_file`（含入口 URL 与 storageState 路径），并停在前台。脚本里起它要让它**独占一个进程组**（`setsid` 起、记下
那个 pgid），结束时给该组发 INT（`kill -INT -- -<pgid>`）；只给 wrapper PID 发不起作用——bash 等前台子进程结束才跑 trap。

**2 — 派发前先冒烟。** 对每个 persona 的会话起浏览器、载入登录态、亲眼确认：

```
playwright-cli -s=<会话> open <entry_url>
playwright-cli -s=<会话> state-load <storageState 文件>
playwright-cli -s=<会话> goto <entry_url>
playwright-cli -s=<会话> find "<signed_in_marker.visible_text>"
```

看到标记文本才算登录态生效。没亲眼看到会话有效就派探索者 = 它报的每条 finding 都是「没登录」的伪影。
派第二个 persona 前再证一件事：**它要走的失败 / 返工路径在这个栈上能触发**（例：一次故意不合格的提交会被打回）——
fake 判定永不打回的栈，rework 步结构上探不到，`steps_not_reached` 那一行就是整轮的结论，别浪费一轮。
**登录态只经文件路径进浏览器**（`state-load`）。禁止 `cookie-set / cookie-get / cookie-list /
localstorage-* / sessionstorage-*`，禁止在 `eval` 正文里碰 cookie / token / localStorage——值上了命令行
或 stdout 就进了 transcript——一次性 session token 正是这样泄漏的。`state-save` 只许落
gitignored 的输出目录。

**3 — 派发探索者。** 配置里每个 persona 派一个独立子代理，brief 按 `references/dispatch.md` 组装，
**自包含**——子代理看不到本对话。席位形态：宿主的**带 Bash 的子代理**（如 Claude Code 的 Agent 工具，通用类型），
**显式指定经济型模型**（如 `model: sonnet`——这是耐心观察不是重推理，别让它默认继承你的高级模型）；cwd 设为输出目录、
或独立 worktree 兜只读。探索者**只读**：驱动浏览器、只往 `output.dir` 写文件；不读不改不跑项目代码，不离开 `allowed_origins`。

**4 — 筛选。** 对原始产出按 `references/triage.md` 自己筛，在编排上下文里做——噪声在这里死掉；
别交回产出它的那个代理（作者是最差的裁判）。

**5 — 产出。** `findings.json`（按 `references/output-schema.json` 校验）与 `findings.md` 落 `output.dir`。

## 两轮法（产量几乎全在第二轮）

第一轮走通路（happy path），抓的多是命名与渲染不一致；第二轮**专攻返工、失败、权限切换**——
用户真正会撞的都在这里，机制测试结构上够不着。两轮 = 两个 persona：配置示例内置「首访者」与
「做错了怎么办」，各项目只改词，不必每次手写第二轮 brief。

## 输出契约（硬）

每条 finding 三格，缺任一格即**删除**、不补：

| 格 | 含义 |
|---|---|
| `step` | 旅程的哪一步，取自配置 `journey` 的 id |
| `kind` | `blocked`（走不下去）或 `confused`（走下去了但不明白） |
| `evidence` | URL、**屏幕原文逐字**、截图路径 |

- **只报真撞上的。** 没有「可以改进」「要是…更好」「用户可能」；探索者没在浏览器里撞到的不存在。
- **最多 10 条**，按挡住旅程的程度排序。
- finding 是观察不是工单：写发生了什么，不写该做什么。
- `steps_not_reached`（没走到的步）与筛选掉落表**必报**——不自报边界的探索报告不可消费。

## 产出之后（交接，不是本 skill 的动作）

本 skill 止于观察与筛选。修复归项目、另行授权；稳定可判定的行为并入项目**既有** E2E 的口径归 cto-orchestration
`references/frontend-verify.md`（可选阅读），不在此复制。探索侧只守三条：下轮 brief 只按改动区域生成；历史 finding /
标准答案不喂冷探索者（去重归主位）；已覆盖问题复发必须重开——脚本绿压不掉图证。

## 护栏

- 永远只读。探索者没有修任何东西的授权。
- 导航围栏 = `allowed_origins`：离开围栏的链接本身可报，但不跟。
- 截图会拍到凭证、邀请码、个人数据。遵守配置 `redact` 表：屏幕值命中就不截那块，引用旁边的标签并注明值已隐去。
- 产物天然非确定。**永不接进 CI 门**——接了只会教所有人忽略它。

## 接入与移植（三处改动）

1. **写配置**：复制 `references/config.example.yaml` 填好。这是唯一要编辑的文件；`journey` 与 `glossary`
   写对，其余机械。glossary 是本次能发现什么的**天花板**——写进去的每个词都是探索者被禁止困惑的词，
   只放真新用户确实被告知的。
2. **落一个 hold 用例**：把 `references/hold-spec.template.ts` 拷进项目 e2e 目录，指向项目已有的
   「拿到已登录页面」的办法（通常两行）；从必跑测试里排除它（无断言、不自行终止）。`auth.setup.command`
   指向它。应用已在跑且已有 state 文件 → 跳过，`auth.mode: storage_state`。
3. **gitignore 输出目录**：`output.dir` 一行。findings、截图、session 文件都落那里，都不该进仓库。

安装：`ln -s <evolab>/skills/frontend-explorer ~/.claude/skills/frontend-explorer`（或整目录复制）。
除 `playwright-cli` 外零依赖。

## 不做的事

不做门禁；不提修法（观察归它，决定归人）；不碰你的代码。

## References

- `references/dispatch.md` — 子代理 brief 模板。
- `references/persona.md` — 探索者是谁、什么算 finding。
- `references/triage.md` — 原始笔记到可执行清单之间的过滤器。
- `references/output-schema.json` — JSON 契约。
- `references/config.example.yaml` — 全部项目旋钮（填好的通用示例）。
- `references/hold-spec.template.ts` — 让已登录栈活到 pass 结束的 Playwright 用例模板。
