---
name: agent-fleet
description: 使用本机 fleet 分派 Codex GPT-6、Gemini、Grok 或 JEV 任务，或调用 Kollab 图片/视频/音频/多模态能力时使用；包括用户点名 agent-fleet、Nano Banana、nanobanana、香蕉、便宜模型、多模型并行，用户说“让 Codex 或 GPT-6 做某事”的编码、调研与 review 派单，以及按全局 CLAUDE.md §2 路由任务。只做单一模型的直接任务且无需 fleet 时不触发；用户明确要直接操作 Codex CLI 原生命令（自选 sandbox、codex review、apply、resume）时用 codex Skill；普通生成图片也可用 imagegen。
---

# agent-fleet

本机多模型任务入口：使用 `fleet` 运行 brief，结束后按实际产物验收。先核对目标模型当前配置、真实 Key 是否存在、工作目录信任边界和任务归属；密钥只看状态，不打印值。

## 命令速查

| 命令 | 用途 |
|---|---|
| `fleet copy brief.md` | Gemini 文案、翻译 |
| `fleet grok brief.md` | Grok 调研 |
| `fleet web start/say/close/list`；兼容 `fleet web "问题" [--followup "追问" ...] [--close]` | 网页版 ChatGPT，少量串行问答 |
| `fleet bulk brief.md` | Gemini 批量处理 |
| `fleet gpt brief.md` | 托管 GPT 任务 |
| `fleet code brief.md [--low] [--cwd dir]` | 本机 Codex GPT-6：默认入口 |
| `fleet code brief.md --review` | 本机 Codex 只读审查 |
| `fleet judge state.txt questions.json` | JEV 结构化判断 |
| `fleet run --model name --prompt "任务"` | 旧的完整模型入口 |
| `fleet run-many --config batch.json` | 批量任务 |
| `fleet status` / `fleet tail [--follow]` | 看任务和日志 |
| `fleet say latest "消息"` | 向运行中的任务插话 |
| `fleet stop latest` / `fleet resume latest` | 收尾或续跑 |
| `fleet list-models` / `fleet help` | 看配置或用法 |
| `fleet media list` | 看 Kollab 当前托管的图片、视频、音频、视觉工具与必填参数 |
| `fleet media run <tool> --model <id> --prompt "..." [--input-json '{}'] [--out dir]` | 调用托管多模态工具并落盘 |
| `fleet media models [--source openrouter] [--search text]` | 查 Kollab 模型目录 |

`brief` 若是现存文件路径就读取内容，否则作为任务文本。短命令和 `run` 默认当前目录、不限轮数、安静写日志；`--verbose` 输出进度。`--cwd`、`--max-turns`、`--system-prompt` 等可显式指定。旧的 `agent-fleet run ...` 写法仍可用。完整结果在 `~/.agent-fleet/runs/*.result.md`，过程在同名 `.log`；stdout 默认只给简报。

多模态认证优先用 `KOLLAB_API_KEY` 或 `KOLLAB_STANDALONE_API_KEY`（`kollab api-key create` 获取），其次用进程级 `KOLLAB_API_TOKEN` 或 `kollab login` 会话；TEST 必须显式设置 `KOLLAB_API_URL`，不要复用生产 profile。先运行 `fleet media list` 看实时支持清单和模型 id，再用 `fleet media run generate_image --model <id> --prompt "一只猫"`；默认文件写入当前目录 `fleet-media/`。其他工具按清单传 `--input-json` 的必填字段，详见 [多模态用法](references/media.md)。普通配图也可用 imagegen。

## 启动方式（硬性，派单人自检）

`fleet` 任务一律这样启动：**一条 Bash 调用，只放 `fleet ...` 这一条命令，用工具参数 `run_in_background: true`、`timeout: 7200000`**，输出用 `> 文件 2>&1` 重定向。**命令里绝不写结尾的 `&`、`nohup`、`disown`。**

```text
Bash(command="fleet code brief.md --cwd <目录> > /tmp/<名>.out 2>&1", run_in_background=true, timeout=7200000)
```

原因：命令自己再加 `&`，外层 shell 立刻退出，harness 马上发「后台命令已完成」的假通知，真正的 fleet/codex 进程变成无人认领的孤儿，**之后不会有真实完成通知**，主线程只能靠轮询或补 Monitor（2026-10-04 hotellobby 的 P0a/P0b 就这样出过错）。不套 `&` 时，fleet 进程退出才会触发完成通知。

- 一个任务一次 Bash 调用；多个独立任务同一条消息里并行发多个 Bash 调用，不要在一条命令里串 `&`。
- 核对：启动后 `pgrep -fl 'agent-fleet.mjs code'` 能看到进程，且 Bash 任务状态仍是 running。
- 万一已经误套了 `&`：不要杀进程，用 Monitor 补一个带硬超时的 until 循环等报告文件；pgrep 的模式必须写成 `'[p]0a-xxx'` 这种括号形式，否则会匹配到 Monitor 自己的命令行，永远等不到结束。
- 重派进同一个 worktree 前先 `pgrep -fl 'codex exec.*<worktree>'`，杀 fleet 外壳不等于杀掉 codex。

## 模型路由与任务边界

写文案必须使用 `/marketing-psychology`、`/marketing-ideas`、`/write` 的原则并遵守 [references/copy-voice.md](references/copy-voice.md)，`fleet copy` 自动注入；写文案 brief 仍要给事实清单和禁止项。仅纯机械改写可用 `--no-voice` 跳过。

大部分任务（编码、修 bug、补测试、调研、技术文档、报告、数据整理）优先 `fleet code`：本机 Codex `gpt-6.1-sol`，默认 medium，单文件且边界明确时用 `--low`。页面、营销和产品文案、翻译、多语言及母语校对一律 `fleet copy`，写能做什么和带来什么好处，不贬低竞品或用恐吓式对比。Grok 可分担擦边题材、其他调研或作为 GPT-6 备选；JEV 只做结构化判断。Claude 只做全局 CLAUDE.md §2 明确归它的任务。

GPT-6 只做 brief 点名的事。除非逐项要求，不写测试或测试脚本、不先写测试、不加安全校验/防御代码/权限边界/输入校验/异常兜底、不重构或抽象封装、不加配置项、文档或注释、不改无关文件、不装依赖、不提交/推送/部署/发布、不调用外部写接口。已有测试和构建只在 brief 要求时运行；拿不准的事不做，最终回复用一行列「建议但未做」。未点名的产物算越界。brief 必须逐字包含：「只做本 brief 列出的事。不写测试、不加安全防护或边界校验、不重构、不做任何未点名的额外工作或 action；拿不准就不做，在回复里列一行建议。」

GPT-6 走 ChatGPT 会员额度，按现有账号约定不额外花钱；其 brief 必须限定最终回复只给结论、改动路径和验证结果，约 15 行内，长内容写入文件。面向读者的文案交 Gemini。

| 短名 | 实际模型 | 适合 |
|---|---|---|
| `copy` | `kollab-gateway-copy`（Gemini） | 文案、翻译（必须走这里，正面写） |
| `grok` | `kollab-gateway-research` | 擦边题材、其他调研、GPT-6 备选 |
| `bulk` | `kollab-gateway-bulk` | 批量转换 |
| `gpt` | `kollab-gateway-gpt-sol` | GPT 托管任务 |
| `code` | 本机 Codex `gpt-6.1-sol` | **默认执行者**：编码、调研、报告、通用任务；默认 medium，`--low` 为 low |
| `judge` | `jev` | 分类、选择、打分 |
| `web` | 网页版 ChatGPT（`chatgpt-web-ask.mjs`） | 联网调研、综述、对比、选题发散、竞品功能核对 |

`code` 在本机 Codex 缺失、登录失效或模型明确不支持时，自动改走 `kollab-gateway-gpt-sol`；其他失败不自动重试。选择以当前配置和实际结果为准；查看其他模型用 `fleet list-models`。Codex 审查范围见 [编程与 review](references/codex-coding.md)。

## 网页版 ChatGPT 通道

与 Rankup 探针共用网页驱动，适合少量串行调研、综述与对比；每轮约 30–110 秒。不适合读本地文件、执行命令、改代码或批量任务。

```bash
fleet web start "问题" --name research-signatures
fleet web say chatgpt-web-research-signatures "追问"
fleet web list
fleet web close chatgpt-web-research-signatures
fleet web "问题" --followup "追问1" --followup "追问2" --out answer.md --json
```

- 不设轮次上限，不会自动关页；用完请 `close`。兼容问答命令加 `--close` 在结束后关闭；失败、报错或中断也关闭，页面文字保留在输出中。追问间至少隔 8 秒。
- 常驻临时聊天占一个窗口池位（池容量 10），默认 dedicated，副屏优先、自动铺开；`AI_PROBE_WEB_WINDOW` 可覆盖。常驻对话打开时使用 `--keep-alive`，不自动回收，需显式 `fleet web close`；一次性问答（无追问且带 `--close`）仍默认 10 分钟空闲回收；旧 CLI 不认识该参数时提示并退回原 env 保活方案；页面丢失须重新 start，临时聊天无法找回。
- 不产生 API token 费用，但消耗订阅额度；高频可能触发验证或限流（探针遇过一次，原因未确认）。限流、验证码或登录失效立即停，保存 pageText 和 pageUrl 后关闭会话，供人工核查。
- 须用户确认账号已关闭记忆；脚本发送前读取临时页「不使用记忆」声明及页首模式；若是「个性化」会自动切到「不个性化」（该选择对后续新临时聊天持续生效）并回读确认，无法确认就停止并保存 pageText/pageUrl。已开路径已验证；自动切换路径未做真实切换实测。
- 内容发给 OpenAI，不放密钥或未公开资料；答案当线索，域名与数字需核对来源。输出 DOM 引用域名，未做 payload 核验。
- `start/say` 支持 `--json`、`--out file`；会话名、回答和引用一起输出。直接调用脚本与 `fleet web` 等价。窗口机制见 [opencli Skill](../../opencli/SKILL.md)。

## 行动范围（方向锁定，适用于所有被派出的模型）

执行者会自己找方向、顺手做没点名的事、做不成就绕路凑数。派单时把范围写死，一单只一个方向、一个目标：

1. **一个目标，围绕它做事。** brief 第一段写清要做的事和交付物；目标所必需的相关改动执行者可以做，不必逐项点名；不自己新增或切换方向，无关线索只在最终回复里用一行列出。
2. **办法由执行者定，只在四种情况停：** 小分叉（浏览器崩溃、弹窗遮挡、残留同名分支、验收条件现实中做不到等）选最保守方案继续，记在报告「偏差」里；要改生产或线上数据、要碰任务明显之外的系统、要花钱或用未授权凭据、缺权限或缺输入导致目标无法交付，才停下并如实写明已完成什么、卡在哪，不降低目标凑数。
3. **边界写大致范围即可**：主要涉及的路径、明确禁止项（生产、数据、花钱、凭据）、完成标准；不必穷举每个文件，范围内相关的改动执行者自行判断。需要多个方向就拆成多个 brief，不在一个 brief 里并列。验收条件写成结果并给备用办法（例如「测不了深色就只测浅色」），不要把测量办法写死。
4. **自动兜底**：`fleet code` 在 brief 前自动加上下面这段，网关模型则追加进默认执行者系统提示（`src/scope.mjs` 的 `SCOPE_LOCK`，文字与此逐字一致；改一处必须同步另一处）。brief 里仍要写自己的边界，兜底只防漏写：

> 【行动范围】你有 brief 指定的这一个任务目标：围绕它做事，目标所必需的相关改动（相邻文件、同类键、配置、让验收通过所需的小修）可以做，不必逐项点名；不要节外生枝：不自己新增或切换方向，不主动加测试、安全防护、重构，不做与目标无关的事；发现的无关线索只在最终回复里用一行列出，不执行。怎么做、怎么测、怎么验证由你自己决定：遇到办法、测量方式、环境小障碍（浏览器崩溃、弹窗遮挡、残留的同名分支或工作区、验收条件在现实中做不到等），选最保守的可行方案继续，把选择和理由记在报告的「偏差」里，不要停；验收条件做不到时先用 brief 给的备用办法，没有备用就做最接近的版本并如实写明差距。只有这几种情况才立刻停止并如实报告：需要改动生产环境或线上数据；需要碰任务明显之外的系统；需要花钱或使用未授权的凭据；缺权限或缺输入导致目标本身无法交付。停止时写明已完成什么、卡在哪里，不降低目标凑数。brief 已列出多条路径时，单条路径不可用就改用 brief 列出的其他路径。

验收时，执行者做了 brief 之外的事、改了方向、或做不到却用替代品交差，都算越界，按 CLAUDE.md §4.3 先向用户报告，不自行掩盖。

## 简报与验收

| verdict | 含义与处理 |
|---|---|
| `ok` | 正常结束；按任务核对产物和测试 |
| `partial` | 到轮数上限但已有改动；验收现有产物或 `resume` |
| `suspect` | 疑似假成功或要求改动却零改动；核对结果和 diff |
| `needs-review` | JEV 置信度不足；人工核对 |
| `fail` | 执行失败、空结果或裸控制 token；看错误后修复 |
| `stopped` | 已收尾中断；检查已完成部分 |

`ok` 只说明进程结果，不能代替任务验收；空结果、裸 tool-call 控制 token、`suspect` 或 `fail` 都不能算成功。核对 brief、产物和要求的检查；`dirty` 和 `commits` 也可能包含同一工作树里其他人的改动。细节见 [README](../README.md)。

## brief 写法

开头说明目标、真实交付物、允许改的文件、不可碰的范围、并行工作边界、必须跑的检查和完成标准；方向只写一个，写法见上文「行动范围」。

**派单前先核实路径，再写进 brief。** 允许读写清单里的每个路径都用 `ls` 或 `test -e` 确认：已有文件确认存在；新文件确认上级目录存在，并明确写成「新建，路径为……」，不要写「放在已有的脚本目录」这类要执行者自己去猜的说法。执行者遇到路径对不上会按「行动范围」直接停止、不会自行换路径，一处路径写错就白跑一轮。各 Skill 的布局并不统一（例如 agent-fleet 的说明在 `agent-fleet/skill/SKILL.md`、可执行脚本在 `bin/`；rankup 与 opencli 的说明在各自根目录的 `SKILL.md`、脚本在 `scripts/`），以派单时的实际 `ls` 为准，不凭记忆。需要改文件时加 `--expect-changes`；涉及浏览器时写明用 opencli（`opencli browser <会话名>`），禁止 Playwright/agent-browser。最终回复列改动与验证结果，不能只说“已完成”。 取证类 brief（打开外站、查 DNS/RDAP、批量读页面）还要写**重试与降级规则**：打开失败先同 URL 重开或刷新，间隔约 5 秒，最多 5 次；单项仍取不到记「无法验证」继续后面的项，只有站点整体不可达、验证码、限流、登录墙才整体停；否则执行者会因一次瞬时失败按「做不到就停」整单收工。

**brief 里带上已知坑清单（避免白跑一轮）**：浏览器自动化 Chromium 在重页面会崩，直接写 firefox.launch({headless:true}) 并每页独立实例（用的是 Playwright 自带的 Firefox，装在 ~/Library/Caches/ms-playwright/firefox-*，本机不需要安装 Firefox 应用，也不会弹窗）；页面有 Cookie 提示时先点「拒绝」或预置 localStorage 再测量；创建 worktree 前先 git worktree remove --force 并 git branch -D 清掉同名旧工作区；指定模型前先 `fleet list-models` 确认真有（gemini-3.1-pro 当前不在配置里，默认用 gemini-3.8-flash）；`fleet code` 整条命令放 Bash 后台，不套 &；pull --rebase 超时重试一次；macOS 的 sed 用 `sed -i ''`。


## 安全边界

把 `--cwd` 指向的目录及其项目配置当作不可信输入核对；网关路径使用 Claude Agent SDK 的 `bypassPermissions`，执行者可读写文件和运行命令，没有工具调用沙箱。只对可信目录派单，保护他人改动，不打印密钥。默认执行者系统提示禁止调用 Agent/Task 工具或再次转派，额外 `--system-prompt` 会追加其后。`fleet code` 默认 `danger-full-access`（可读写任意路径、可联网，含本机代理），`--review` 使用 `read-only`；详见 [README 的安全边界](../README.md#安全边界)。

## JEV judge

`fleet judge state.txt questions.json [--json]`：state 为文本或 `.json` 文件；questions 是 `{ "key": { "type": "noul"|"choice"|"score", "instructions": "..." } }`。`choice` 和 `score` 必须带 `criteria`。JEV 只做结构化判断，不生成自由文本，也不能用 `run`。旧写法 `fleet judge --model jev --state-file state.txt --questions-file questions.json` 仍可用。

`questions.json` 可按需选用其中一种或组合使用：

```json
{
  "is_urgent": { "type": "noul", "instructions": "这条消息是否紧急？" },
  "team": { "type": "choice", "instructions": "该由哪个团队处理？", "criteria": { "billing": "付款或退款", "technical": "故障或集成" } },
  "frustration": { "type": "score", "instructions": "客户有多沮丧？", "criteria": ["平静", "沮丧", "愤怒"] }
}
```
