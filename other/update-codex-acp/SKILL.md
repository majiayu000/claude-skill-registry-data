---
name: update-codex-acp
description: 更新内置 Codex ACP agent fork（vendor/codex-acp，自维护 git submodule），合并上游 agentclientprotocol/codex-acp 新提交并重建发布产物。当用户说更新 codex-acp / 合并上游修改 / 同步 codex agent / 升级内置 codex agent 时使用。注意真上游是 agentclientprotocol，zed-industries 已废弃。
disable-model-invocation: true
---

# 更新 codex-acp（合并上游 + 重建产物）

`vendor/codex-acp` 是我们自维护的 fork，**git submodule，不在 pnpm workspace 内，用自带 npm 工具链独立构建**（见根 CLAUDE.md）。上游是 `https://github.com/agentclientprotocol/codex-acp.git`（npm 包 `@agentclientprotocol/codex-acp`）。我们在某个上游 release 之上叠了若干自定义提交（费用计算、Claude 式 skills/memory、git 工作树会话匹配、跨平台路径比较、AI 会话标题持久化、ESM 标记、回放 shell 解析修复、rewind/fork、重连失败处理、transcriptPath 暴露等，共约 16 个）。

> ⚠️ **真上游踩坑（务必先确认）**：Codex ACP 有**两个**同名仓库。老的 `zed-industries/codex-acp` **已废弃**（README 明确写着开发已迁移），且其 `main` 被回退重写到较旧点、**与我们 fork 无共同祖先**（`git merge-base` 返回空）。**真正的上游是 `agentclientprotocol/codex-acp`**（基于新 Codex App Server）。若误把 upstream 设成 zed-industries，会出现「merge-base 为空 / 代码大幅倒退」的假象。判据：正确上游下 `merge-base` 命中我们的基线、`compare` 显示 **N ahead / M behind** 与我方自定义提交数吻合。

核心套路：**确认真上游 + 分叉点 → 与用户敲定推送范围 → 备份当前 HEAD → rebase 自定义提交到上游最新 → 按已知套路解决冲突 → 重新装依赖 + 构建 + typecheck + 测试 → 后处理改动 fixup 并入 → push fork → 主仓库 `pnpm agent:build` + `pnpm check` → 开分支提交 submodule 指针并 push**。

> **合并方式固定用 rebase**（用户已明确要求，不用再问）：历史线性、自定义提交清晰留顶、下次再合更省事；代价是重写历史需 `--force-with-lease` push fork。只需就“推送范围”征询用户。

> ⚠️ 第一原则：**fork 的自定义提交必须完整保留在历史顶部，且其承载的功能（费用累计上报、Claude 式 skills/memory、AI 标题持久化等）不能被上游同名实现覆盖掉**。主仓库 renderer 端依赖这些行为；合并时优先“两条路并存”，而不是二选一。

## 流程

### 0. 摸清现状（只读）
全程用 `git ls-remote` / `gh api` / 只读 git 命令探查，**不要**在 plan/调查阶段改动 submodule：
```bash
cd vendor/codex-acp
git remote -v                 # 通常只有 origin = 我们的 fork(lovebirdsx/codex-acp)，无 upstream
git log --oneline -12         # 顶部 N 个是我们的自定义提交（作者 lovebird），其下是某个上游 release（基线）
grep -A3 -i repository package.json   # 确认上游仓库 URL（应为 agentclientprotocol，别信 zed-industries）
git rev-parse main HEAD origin/main   # ⚠️ submodule 常是 detached HEAD；本地 main 可能已过时，别用它做基线
```
确认真上游并测分叉（这步决定工作量，也是排除 zed-industries 陷阱的关键）：
```bash
git remote add upstream https://github.com/agentclientprotocol/codex-acp.git
git fetch upstream
mb=$(git merge-base HEAD upstream/main) && git log --oneline -1 $mb   # 应命中我们的基线；空=上游选错了
git log --oneline $mb..HEAD           # 我方自定义提交（ahead）
git rev-list --count $mb..upstream/main   # 上游新提交数（behind）
git log --oneline $mb..upstream/main  # 上游新提交列表，预判影响面（codex 版本升级、SDK 升级等）
git diff --stat $mb..HEAD             # 我们改了哪些文件 → 预判冲突面
```
> 注：package.json 内部 `version` 与上游 git **tag** 不是一回事，对不上正常，不影响合并。GitHub 仓库页显示的 “N commits ahead / M behind” 是最快的真上游校验（应与上面 ahead/behind 吻合）。

### 1. 与用户敲定推送范围（AskUserQuestion）
- **合并方式**：固定 **rebase**，不用再问。
- **推送范围**：默认推荐**全部推送**（push fork + 主仓库提交 submodule 指针）。CLAUDE.md 规定提交/推送只在用户要求时做，必须先确认。选“仅本地不推送”时，跳过 push fork 与提交 submodule 指针，只到本地 `main` 指向合并结果 + 主仓库 `agent:build`/`pnpm check` 验证为止。

### 2. 备份 + rebase
submodule 常是 detached HEAD，rebase 会重写历史，**先落一个备份分支**再动手：
```bash
cd vendor/codex-acp
git branch backup-before-rebase-<短sha> <当前HEAD sha>   # 出事可 git reset --hard 回来
git branch -f main <当前HEAD sha> && git switch main       # 让 main 指向我们最新的 8 提交 HEAD
git rebase upstream/main                                    # 把 基线..HEAD 的自定义提交重放到上游最新
```
逐个提交解决冲突（见下「冲突套路」），每次 `git add <file>` 后 `git -c core.editor=true rebase --continue`。

### 3. 重新装依赖 + 构建 + typecheck + 测试
上游常升级 codex 版本 / ACP SDK / vscode-jsonrpc，rebase 后必须重装依赖再验证：
```bash
npm ci                 # 上游可能升级了 SDK/依赖（本次含 ACP SDK 1.1、vscode-jsonrpc v9）
npx tsc --noEmit       # 类型检查（必跑安全网，rebase 零冲突≠语义正确，见案例 5 精神）
node build.mjs         # esbuild → dist/index.js（+ dist/package.json 标 ESM）
npm test               # vitest；仅截错误。已知 Windows 路径测试会失败（见案例 1），非回归
```
把“后处理改动”（更新的快照等）用 **fixup + autosquash** 并入逻辑所属提交（保持历史干净）：
```bash
git add <改过的快照/测试文件> && git commit --fixup=<对应功能提交sha>
GIT_SEQUENCE_EDITOR=true git -c core.editor=true rebase -i --autosquash upstream/main
```

### 4. push fork
```bash
git push --force-with-lease origin main
git branch -d backup-before-rebase-<短sha>   # 确认无误后再删备份
# 收尾核对：git rev-parse HEAD main 相等；git rev-list --count upstream/main..main == 我方提交数
```

### 5. 主仓库重建产物 + 验证
```bash
cd <repoRoot>
pnpm agent:build      # = vendor-install(npm ci 生产依赖) + 两个 fork 各自 npm run build；重建 vendor/codex-acp/{dist,node_modules}
pnpm check            # lint + typecheck + test，仅截错误
```
> `agent:build` **同时构建 claude-agent-acp 和 codex-acp 两个 fork**，并把 fork 的 `node_modules` prune 成**生产依赖**，之后想再在 fork 跑 `npm test` 需先 `npm ci` 重装 devDeps。
> `pnpm check` 偶发的 FileWatcher / DiffEditor / `Channel closed`(IPC) 失败是主仓库既有环境 flake，与本次无关——单独 `pnpm --filter @universe-editor/editor run test` 重跑即绿。

### 6. 提交主仓库 submodule 指针
```bash
git switch -c chore/update-codex-acp     # 当前多在 main（默认分支），先开分支
git diff --submodule=log vendor/codex-acp   # 核对：顶部我方提交 + 其下上游新提交
git add vendor/codex-acp
git commit   # chore(agent): 更新 codex-acp 至上游 <版本>（codex <x.y.z> / ACP SDK <a.b>），正文记冲突处理 + Co-Authored-By
git push -u origin chore/update-codex-acp
```

## 冲突套路（按文件）

- **`package-lock.json`**：**不要手动解**。rebase 中冲突时 `git checkout --ours package-lock.json && git add`（rebase 里 `--ours`=上游侧），rebase 全部完成后 `npm ci`/`npm install` 一次性重生成。
- **`package.json`**：`version` 与 codex/SDK/依赖版本取上游；我方特有改动（如 build 脚本、devDep）保留。⚠️ Edit 解冲突当心**重复 key**（冲突标记外的公共行别在 new_string 里重写）。
- **`src/index.ts`**：agent 注册入口，双方常同改（见案例 2）。
- **`src/CodexEventHandler.ts` / `src/CodexAcpServer.ts`**：费用/token 上报，我方改了语义，注意与上游 token-usage 演进的冲突（见案例 3）。
- **`src/CodexAcpClient.ts`**：skills/memory 注入 + session config，我方大改（见案例 4）。
- 我方新增、上游无的文件（如 `src/PathUtils.ts`、`CLAUDE.md`、set-session-title 测试）→ 一般无冲突，直接保留。

## 案例库

> 每条：现象 → 根因 → 解法 → 锚点。新经验往下追加。

### 案例 1：fork `npm test` 若干路径测试在 Windows 必失败（非回归）
- **现象**：Windows 本地跑 `npm test`，约 4 个测试失败：`CodexAcpClient.test.ts` 的 skills additional-directories 两条 + `should map events from dump`（报 `Invalid request: AbsolutePathBuf deserialized without a base path`），以及 `load-session.test.ts` 的 history-fallback 一条。diff 全是 `\test\...` vs `/test/...`（反斜杠 vs 正斜杠）。
- **根因**：测试 fixture 用假 cwd `/test/cwd`。Windows 上 `path.join("/test/cwd", ...)` 产出 `\test\cwd\...`——非盘符绝对路径，真 codex 二进制反序列化 `AbsolutePathBuf` 时拒绝（→ 那条 AbsolutePathBuf 错误）；其余是快照里分隔符不匹配。Linux/Mac CI 上 `/test/cwd/...` 是合法绝对路径，全过。
- **判别**：**三方验证非回归**——① 纯 `upstream/main` 新建 worktree 跑同样测试也失败；② rebase 前的 `backup-before-rebase-*` 分支跑也失败。两者都失败 ⇒ 与本次 rebase 无关，是既有 Windows 环境差异。
- **解法**：**直接忽略**，不改测试/不改上游逻辑（改了会破坏 Linux CI）。不影响主仓库 `pnpm check`（vendor 不在 workspace）。与记忆 `codex-claude-skills-memory-parity` 记录的“3 个测试 Windows 反斜杠失败 CI 过”一致。
- **锚点**：`vendor/codex-acp/src/__tests__/CodexACPAgent/{CodexAcpClient.test.ts,load-session.test.ts}`、`src/app-server/AbsolutePathBuf.ts`、fixture `src/__tests__/acp-test-utils.ts`（`cwd: "/test/cwd"`）。

### 案例 2：`src/index.ts` — 我方表驱动扩展方法注册 撞 上游 prompt 取消支持
- **现象**：rebase 到「支持持久化 AI 会话标题」提交时 `src/index.ts` 冲突。HEAD（上游）侧把手写的 `.onRequest("authentication/status"...)` 等逐条注册保留、且给 prompt 加了 `ctx.signal`（来自上游取消支持）；我方侧把这些手写注册重构成表驱动的 `EXTENSION_METHOD_REGISTRATIONS` for 循环、但 prompt 还是旧的 `getAgent().prompt(ctx.params)`（无 signal）。
- **根因**：两边改同一段 agent builder——上游改控制流（加取消 signal），我方改结构（手写→表驱动）。
- **解法**：**两者都要**。采用我方 `const agentBuilder = ...` + 表驱动 for 循环结构，同时把 prompt 改成上游的 `getAgent().prompt(ctx.params, ctx.signal)`。先确认我方 `EXTENSION_METHOD_REGISTRATIONS`（在 `AcpExtensions.ts`）已完整覆盖上游那几个手写方法（authentication/status、authentication/logout、legacy set_model，且多了 set_session_title），确认后删掉上游的逐条 `.onRequest(...)` 手写注册与旧 `z`/parser import 残留即可。
- **锚点**：`src/index.ts`（`startAcpServer` 的 agent builder 链）、`src/AcpExtensions.ts`（`EXTENSION_METHOD_REGISTRATIONS`）。

### 案例 3：费用补丁的 totalTokenUsage 累计语义 撞 上游 token-usage 快照（更新快照）
- **现象**：rebase 后 `npm test`，`token-usage-events.test.ts` 6 个 `toMatchFileSnapshot` 失败。diff 显示我方输出 `totalTokens: 5000` 而快照期望 `2500`（测试输入里 `total=5000, last=2500`）。
- **根因**：我方「优化通知以支持 session 的费用计算」提交**刻意**把 `_meta.quota` 上报从 `lastTokenUsage`（最后一次调用）改成 `totalTokenUsage`（会话累计），以便客户端从单次快照给整个会话计价。上游后来（#107 等）增强了 token-usage 测试，会断言 `_meta.quota` 的具体值 → 与我方语义冲突暴露。旧基线时这些测试还不碰 `_meta.quota`（`grep -c _meta 旧快照` = 0），所以当年没冲突。
- **判别**：确认输出 `5000` = 测试输入的 `total` = 我方累计语义的**正确结果**（不是 bug），才更新快照。
- **解法**：`npx vitest run -u src/__tests__/CodexACPAgent/token-usage-events.test.ts` 更新这 6 个 `data/token-usage-*.json` 快照，用 `git commit --fixup=<费用计算提交sha>` 并入费用补丁（让该提交自洽=行为改动+对应快照在一起）。⚠️ `-u` 不带过滤会更新**全部**失败快照——若它顺手更新了案例 1 的 Windows 路径快照（如 `load-session-response-item-history-fallback.json`），要 `git checkout` **还原**掉（那些是环境差异，改了破坏 Linux CI）。
- **教训**：更新快照前先分清「我方有意的语义差异」（该更新）vs「Windows 环境差异」（该还原）vs「真回归」（该修代码）。
- **锚点**：`src/CodexEventHandler.ts`（`usage_update` 的 `_meta.quota`）、`src/CodexAcpServer.ts`（`buildQuotaMeta`，`totalTokenUsage` vs `lastTokenUsage`）、`src/__tests__/CodexACPAgent/data/token-usage-*.json`。

### 案例 4：skills/memory 注入（Claude 兼容）— 我方大改 CodexAcpClient（一般能自动合并，但注意路径构造）
- **现象**：「支持 Claude 兼容的 skills 和 memory」提交改 `src/CodexAcpClient.ts`：threadStart/threadResume 加 `...buildMemoryInstructions(cwd)`（读 `cwd/.claude/memory/MEMORY.md` 作 developerInstructions）、`refreshSkills` 把 skillExtraRoots 扩成 `.agents/skills` + `cwd/.claude/skills` + `additionalRoots/.claude/skills`。
- **根因/风险**：上游也在演进 skills（`support-skills-from-additionalRoots` 等分支/PR），两边都动 skills 发现逻辑，可能冲突或语义重叠。
- **解法**：合并时保留我方的 `.claude/skills` + memory 注入（这是 fork 命脉，主仓库依赖，见记忆 `codex-claude-skills-memory-parity`），与上游的 `.agents/skills` 处理**并存**。注意：我方对 skill root 故意不做存在性检查（保持与上游 `.agents/skills` 对称、最小化 diff），这会在 Windows 假 cwd 测试下触发案例 1 的 AbsolutePathBuf——那是测试环境问题，不是这里的 bug。
- **锚点**：`src/CodexAcpClient.ts`（`buildMemoryInstructions`、`refreshSkills` 的 `skillExtraRoots`）、`src/AcpExtensions.ts`（`SET_SESSION_TITLE_METHOD`）、记忆 `codex-claude-skills-memory-parity`。

### 案例 5：「两者都要」式解冲突丢块 + 语义适配三类（v1.1.7 合并实战）
- **现象**：rebase 到上游 v1.1.7（steering #309 / goal control #293 / 可配置 provider #272）时，冲突几乎全是「同一位置双方各加各的」（ext-method 类型 union、`isExtMethodRequest`、`EXTENSION_METHOD_REGISTRATIONS`、import 列表、方法块）。手工「两者都要」合并时**把上游 HEAD 侧的 `SessionSteerRequest`/`SessionSteeringResponse`/`SessionSteeringExtRequest` 三个类型定义整块丢了**（new_string 只保留了函数没保留类型），rebase 能完成但 `npx tsc --noEmit` 立刻报一串 TS2304。
- **解法**：① 丢的块补回去，**fixup 进当时解冲突的那个提交**（保持每个提交自洽可编译）；② 解冲突时优先用「只删标记行」的小步 Edit，别整块重写——整块重写最容易丢内容。
- **语义适配**（rebase 零冲突/标记解完 ≠ 完事，tsc + test 抓出来的三类）：
  1. **上游给接口加必填字段**：`SessionMetadata` 新增必填 `collaborationMode`，我方 `forkSession` 的返回字面量缺它（TS2741）→ 照上游其他返回点补 `collaborationMode: this.getCollaborationMode(thread.id)`，fixup 进 rewind/fork 提交。
  2. **上游改了测试 helper 签名**：`runPromptWithError` 返回值从 `unknown` 变 `{result, updates}`（上游要断言 session updates），我方新增测试 `fails the turn on a terminal stream disconnect` 还按旧签名用 → 调用处改 `const {result: error} = await ...`，fixup 进「重连失败当成错误」提交。
  3. **上游注册方式演进撞我方表驱动**：上游把 steering/goal_control 两个新 ext-method 的 parser（`sessionSteerParamsParser`/`goalControlParamsParser`）定义在 `index.ts` 并手写 `.onRequest` 注册——按案例 2 套路搬进 `AcpExtensions.ts` 并加进 `EXTENSION_METHOD_REGISTRATIONS` 表，`index.ts` 里删掉（连带 `import {z} from "zod"` 变成多余）。
- **锚点**：`src/AcpExtensions.ts`（类型 union / parser / 注册表）、`src/CodexAcpClient.ts`（`forkSession` 的 `collaborationMode`）、`src/__tests__/CodexACPAgent/auth-error-events.test.ts`（`{result: error}` 解构）。

### 案例 6：上游反向删除我方依赖的行为（v1.1.9 合并实战：#358 删 notifyConversationInterrupted）
- **现象**：rebase 到 v1.1.9 时，我方「修复取消未开始 turn 时缺少中断通知」提交在 `src/CodexAcpServer.ts` 出 3 处冲突。根因是上游 #358「Stop emitting "Conversation interrupted" message」**故意删掉**了 `notifyConversationInterrupted`（定义 + 3 处调用点），而我方提交反其道行之——把通知**收拢进** `cancelledPromptResponse` 让每次 cancel 都发（editor 依赖它渲染中断态，否则只显示 `[cancelled]` 而 agent 还在跑）。
- **根因**：同一行为双方意图直接相反（上游 JetBrains 客户端自己渲染中断 UI；我方 renderer 依赖该通知）。属「第一原则」场景：我方自定义行为不能被上游同名演进覆盖。
- **解法**：**保留我方语义**，三层处理——① 调用点冲突取我方 `return await this.cancelledPromptResponse(...)`（含上游新增的 `await eventHandler.flushPendingPlanUpdates()` 行，两者都要）；② 方法定义冲突保留上游新增的 `requestPlanImplementationPermission` + 我方 async 版 `cancelledPromptResponse`；③ 上游删除 `notifyConversationInterrupted` 定义是**自动合入**的（不在冲突块里！），须手动补回该方法并加注释说明为何保留。另外上游 #351 plan review 新流程引入的 3 处 `return this.cancelledPromptResponse(...)`（无 await）要统一改 `return await`，保证中断通知先于响应发出。
- **教训**：上游「删除函数」若与我方「调用该函数」不落在同一 hunk，删除会静默生效——解完冲突后务必 `grep` 我方提交引入的每个符号，确认其定义仍存在于最终文件。
- **锚点**：`src/CodexAcpServer.ts`（`cancelledPromptResponse`、`notifyConversationInterrupted`、`requestPlanImplementationPermission`）、上游提交 `efa3789`、我方提交「修复取消未开始 turn 时缺少中断通知」。

## 检查清单要点
1. 调查阶段全程只读（`git ls-remote` / `gh api` / 只读 git），别在 plan mode 改 submodule。
2. **真上游是 `agentclientprotocol/codex-acp`，不是已废弃的 `zed-industries/codex-acp`**。设错会出现 merge-base 为空 / 代码倒退的假象；用 `merge-base 命中基线` + `ahead/behind 与我方提交数吻合` 校验。
3. submodule 是 detached HEAD；**本地 `main` 常已过时**，基线用 `merge-base HEAD upstream/main` 的真实 sha，别信本地 main。**rebase 前先落 `backup-before-rebase-<sha>` 分支**。
4. rebase 里 `--ours` = 被 rebase 到的上游侧、`--theirs` = 正在重放的我方提交（与平时相反）。`package-lock.json` 取 `--ours` 后 `npm ci` 重生成。
5. `src/index.ts` 冲突：我方表驱动注册 + 上游 prompt `ctx.signal` **两者都要**（案例 2）；先确认 `EXTENSION_METHOD_REGISTRATIONS` 覆盖上游手写方法。
6. 费用补丁是 fork 命脉：`_meta.quota` 走 **totalTokenUsage 累计**语义。撞上游 token-usage 快照时**更新快照**并 fixup 进费用提交（案例 3）；别把它改回 lastTokenUsage。
7. package.json 解冲突当心**重复 key**；version/codex/SDK 依赖取上游。
8. 后处理改动（更新的快照、适配的测试）用 `git commit --fixup=<sha>` + `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash` 并入逻辑所属提交。
9. **rebase 零冲突 ≠ 语义正确**：`npx tsc --noEmit` **和** `npm test` 都是必跑安全网，别因 rebase 顺利就跳过。
10. fork 测试已知约 4 个 Windows 路径失败（案例 1）非回归——用「纯 upstream worktree + rebase 前备份分支」两处都失败来判别，别误判为回归，别改测试（会破坏 Linux CI）。
11. `pnpm agent:build` **同时**构建 claude-agent-acp + codex-acp 两个 fork，并 prune 到生产依赖；之后要再跑 fork 测试先 `npm ci`。
12. 全流程末尾用 `git diff --submodule=log vendor/codex-acp` 核对“我方提交在顶 + 上游新提交在下”，再提交主仓库指针。
13. **合并方式固定 rebase，不用再问用户**；只需就“推送范围”征询。选“仅本地不推送”时到本地 `main` 指向合并结果 + 主仓库 `agent:build`/`pnpm check` 验证为止，不 push fork、不提交 submodule 指针。

## 关键参考路径
- 根 `CLAUDE.md`「内置 ACP agent」段 + `scripts/release/{vendor-install.mjs,runtime-resources.mjs}`、`package.json` 的 `agent:build`（含两个 fork）
- `vendor/codex-acp/src/{index.ts,CodexAcpClient.ts,CodexEventHandler.ts,CodexAcpServer.ts,AcpExtensions.ts,PathUtils.ts}`
- codex-acp 构建：`vendor/codex-acp/build.mjs`（esbuild → dist/index.js，external `@openai/codex`），非 bun
- 主仓库 `apps/editor/src/renderer/services/acp/`（codex 会话/费用/标题消费端）、`scripts/sync-codex-skill-policy.mjs`（codex skills policy 同步）
- 记忆 `codex-claude-skills-memory-parity`、`codex-ai-title-persistence-parity`、`session-cost-feature`、`session-timer-feature`

## 其它
- 姊妹 skill `update-claude-agent-acp` 是 claude-agent-acp fork 的同类流程，套路互通、案例可互相参考。
- 后续用本 skill，发现新经验，需同步更新本文件。
