---
name: update-claude-agent-acp
description: 更新内置 ACP agent fork（vendor/claude-agent-acp，自维护 git submodule），合并上游 agentclientprotocol/claude-agent-acp 新提交并重建发布产物。当用户说更新 claude-agent-acp / 合并上游修改 / 同步 acp agent / 升级内置 agent / 升级 claude-agent-sdk 时使用。
disable-model-invocation: true
---

# 更新 claude-agent-acp（合并上游 + 重建产物）

`vendor/claude-agent-acp` 是我们自维护的 fork，**git submodule，不在 pnpm workspace 内，用自带 npm 工具链独立构建**（见根 CLAUDE.md）。上游是 `https://github.com/agentclientprotocol/claude-agent-acp.git`（npm 包 `@agentclientprotocol/claude-agent-acp`，作者 Zed Industries）。我们在某个上游 release 之上叠了若干自定义提交（esbuild 单文件打包、AskUserQuestion extMethod、工具错误上下文、listSessions 时间戳、electron-builder ESM 修复、上下文计算修复等）。

核心套路：**确认分叉点 → 与用户敲定推送范围 → 在工作分支 rebase 自定义提交到上游最新 → 按已知套路解决冲突 → 重新生成 lock + 构建 + 测试 fork → push fork → 主仓库 `pnpm agent:build` + `pnpm check` → 开分支提交 submodule 指针并 push**。

> **合并方式固定用 rebase**（用户已明确要求，不用再问）：历史线性、自定义提交清晰留顶、下次再合更省事；代价是重写历史需 `--force-with-lease` push fork。只需就“推送范围”征询用户。

> ⚠️ 第一原则：**fork 的自定义提交必须完整保留在历史顶部，且其承载的功能（尤其 AskUserQuestion 走 extMethod）不能被上游同名实现覆盖掉**。主仓库 renderer 端依赖这些行为；合并时优先“两条路并存”，而不是二选一。

## 流程

### 0. 摸清现状（只读）
全部用 `git ls-remote` / `gh api` 探查，**不要**在 plan/调查阶段改动 submodule：
```bash
cd vendor/claude-agent-acp
git remote -v                 # 通常只有 origin = 我们的 fork(lovebirdsx/...)，无 upstream
git log --oneline -8          # 顶部 N 个是我们的自定义提交，其下是某个上游 release（基线）
grep -A3 -i repository package.json   # 确认上游仓库 URL
git rev-parse main HEAD origin/main   # ⚠️ submodule 常是 detached HEAD；本地 main 分支可能已过时，别用它做基线
```
用 `gh` 确认上游含我们的基线、以及基线后有多少新提交（这步决定工作量）：
```bash
gh api repos/agentclientprotocol/claude-agent-acp/commits/<基线sha> --jq '.commit.message'   # 确认线性分叉
gh api 'repos/agentclientprotocol/claude-agent-acp/compare/<基线>...<上游HEAD或main>' --jq '.ahead_by,.behind_by,.total_commits'
git diff --stat <基线>..<我们的HEAD>   # 我们改了哪些文件 → 预判冲突面
```
> 注：package.json 内部 `version`（如 0.46.0）与上游 git **tag**（可能是 v0.x 旧体系）不是一回事，版本号对不上是正常的，不影响合并。

### 1. 与用户敲定推送范围（AskUserQuestion）
- **合并方式**：固定 **rebase**，不用再问（用户已明确要求）。
- **推送范围**：默认推荐**全部推送提交**（push fork + 主仓库提交 submodule 指针）。CLAUDE.md 规定提交/推送只在用户要求时做，所以必须先确认。选“仅本地不推送”时，跳过 push fork 与提交 submodule 指针，只到本地 `main` 指向合并结果 + 主仓库 `agent:build`/`pnpm check` 验证为止。

### 2. 配置 upstream 并 rebase
```bash
cd vendor/claude-agent-acp
git remote add upstream https://github.com/agentclientprotocol/claude-agent-acp.git
git fetch upstream
git switch -C update-upstream <我们最新的HEAD/origin-main的sha>   # 基于最新 fork 提交，不是过时的本地 main
git rebase --onto upstream/main <基线sha>                        # 把 基线..HEAD 的自定义提交重放到上游最新
```
逐个提交解决冲突（见下「冲突套路」），每次 `git add <file>` 后 `GIT_EDITOR=true git rebase --continue`。

### 3. 重新生成 lock + 构建 + 测试 fork
rebase 时 `package-lock.json` 冲突按下面套路取上游侧；rebase 完成后必须重新生成以纳入我们的依赖：
```bash
npm install            # 重新生成 package-lock.json（纳入 esbuild 等我方 devDep）
npm run build          # esbuild → dist/index.js（确认末行打印 SDK 版本）
npm run typecheck      # tsc --noEmit
npm test               # vitest；仅截错误。已知 2 个 Windows 路径测试会失败（见案例 1），非回归
```
把这些“后处理改动”用 **fixup + autosquash** 并入逻辑所属提交（保持历史干净）：
```bash
git add package-lock.json && git commit --fixup=<esbuild提交sha>
git add <改过的测试文件> && git commit --fixup=<对应功能提交sha>
GIT_SEQUENCE_EDITOR=: GIT_EDITOR=true git rebase -i --autosquash <上游HEAD sha>
```

### 4. 同步 main 并 push fork
```bash
git branch -f main update-upstream    # 可能报 worktree 警告，但若随后 rev-parse 确认 main==HEAD==目标 即成功
git switch main
git push --force-with-lease origin main
git branch -d update-upstream         # 清理临时分支
# 收尾核对：git rev-parse HEAD main origin/main 应全相等
```

### 5. 主仓库重建产物 + 验证
```bash
cd <repoRoot>
pnpm agent:build      # = vendor-install(npm ci 生产依赖) + npm run build；重建 vendor/.../{dist,node_modules}
pnpm check            # lint + typecheck + test，仅截错误
```
> `agent:build` 会把 fork 的 `node_modules` prune 成**生产依赖**，之后想再在 fork 跑 `npm test` 需先 `npm install` 重装 devDeps。
> `pnpm check` 偶发的 `FileWatcherMainService` debounce / `DiffEditor getPosition` 失败是主仓库既有环境 flake，与本次无关——重跑即绿（可单独 `pnpm -w run test` 复核）。

### 6. 提交主仓库 submodule 指针
```bash
git switch -c chore/update-claude-agent-acp     # 当前多在 main（默认分支），先开分支
git diff --submodule=log vendor/claude-agent-acp   # 核对：顶部我方提交 + 其下上游新提交
git add vendor/claude-agent-acp
git commit   # chore(agent): 更新 claude-agent-acp 至上游 <版本> (sdk <x.y.z>)，正文记冲突处理 + Co-Authored-By
git push -u origin chore/update-claude-agent-acp
```

## 冲突套路（按文件）

- **`package-lock.json`**：**不要手动解**。rebase 中冲突时 `git checkout --ours package-lock.json && git add`（rebase 里 `--ours`=上游侧），rebase 全部完成后 `npm install` 一次性重生成。⚠️ 在 `vendor/*` 重新生成 lock 一律带 `--registry=https://registry.npmjs.org`，否则本机镜像 URL 会写进 `resolved` 字段污染 CI（案例 10）。
- **`package.json`**：保留我们的改动（`build` 改成 `node esbuild.config.mjs`、新增 `typecheck`、devDep 加 `esbuild`），`version` 与 SDK/依赖版本取上游。⚠️ Edit 解冲突时**当心重复 key**：冲突标记外的公共行（如 `@eslint/js`）别在 new_string 里再写一遍，否则产生重复键（esbuild 会 warn，`npm install`/typecheck 不报错，易漏）。
- **`esbuild.config.mjs` / `src/interactive.ts`**：我们新增、上游无 → 一般无冲突，直接保留。
- **`src/acp-agent.ts` / `src/tools.ts`**：双方都大改，需语义合并（见案例 2、3）。

## 案例索引（命中后去 `references/cases.md` 读详情）

> 每条：现象 → 根因 → 解法 → 锚点，全部在 `references/cases.md`。新经验追加到该文件并在此补一行。

- **案例 1**：fork `npm test` toDisplayPath 系列在 Windows 必失败（`src\x` vs `src/x`），上游 `path.relative` 平台分隔符缺陷，非回归 → 直接忽略（当前已知 6 个，含案例 9 扩展）。
- **案例 2**：AskUserQuestion 上游 elicitation 实现撞我方 extMethod → **两路并存**（form 优先、extMethod 兜底），主仓库不声明 elicitation 能力，绝不让上游 form-only 逻辑禁用它。
- **案例 3**：`withToolUseContext` 撞上游新 `failActive(...); break;` 控制流 → 上游控制流包住我方错误信息参数，注意括号配平。
- **案例 4**：自定义测试用不存在的 `cwd: "/test"` 被上游新增 `validateCwd` 拦截 → 改 `process.cwd()` + elicitation 断言反转为 `not.toContain`。
- **案例 5**：上游 #790 把 client 抽象成窄接口 `AcpClient` → 三方合并保住调用点但 `extMethod` 接口/实现被整体顶替，**typecheck 才暴露**；补回接口声明 + `ClientConnection` 实现。
- **案例 6**：上游 #835 idle-without-result 校验撞我方 compact_boundary 测试的人为 trailing idle 构造 → 删 trailing idle（真实 compaction turn 总有 result），**npm test 才暴露**。
- **案例 7**（0.55.0→0.58.1）：SDK 0.3.205 收紧类型（`CanUseTool` 加 `|null`、`AsyncGenerator`）+ 上游新 mock 缺 `getSettings` → 三类纯测试适配（`result?.behavior`、`async function*`、补 mock 字段），含同文件混改的 sed 分离 fixup 技巧。
- **案例 8**：上游 #848 把阻塞 CLI 往返（`getContextUsage`/`setModel`）塞进 resume 关键路径，恢复 2s→20s+ → 我方 `getAvailableModels` resume 零往返 + `reconcileResumedSessionModel` 后台纠偏。**原则：任何 CLI 控制请求都不得回到 session/load 关键路径**。
- **案例 9**（0.58.1→0.62.0）：上游 #894 contextWindow seeding 也进 resume 关键路径，与案例 8 正面冲突 → 语义合并（以我方零往返为准）；含 5 类坑：dogfood env 污染测试、git 对齐吞噬闭合行、extNotification 旁路 sendUpdate 副作用、autosquash 时序陷阱、rebase 中途 git 操作禁忌。
- **案例 10**：vendor submodule `npm ci` 报 `Missing ... from lock file`（peer 无祖先链节点，上游依赖链演进致老 lock 失效）→ `npm install --package-lock-only --registry=https://registry.npmjs.org` 重生成，`npm ci --dry-run` 验证。与要点 8 是同一 lock 环节的两个坑。
- **案例 11**（0.62.0→0.64.2）：上游 #881 给「丢弃子代理 text」分支加 forwardSubagentText 门控 → 我方挂分支上的副作用（用量累积）必须提升到分支决策前，否则新路径丢失；replay 强类型辅助撞 union 类型 → 补接口字段；测试尾部相邻 append 冲突在 `=======` 处补闭合括号。

## 要点速记

1. 调查阶段全程只读（`git ls-remote` / `gh api`），别在 plan mode 改 submodule。
2. submodule 是 detached HEAD；**本地 `main` 分支常已过时**，rebase 基线和工作分支都用 `origin/main`/当前 HEAD 的真实 sha，别信本地 main。
3. rebase 里 `--ours` = 被 rebase 到的上游侧、`--theirs` = 正在重放的我方提交（与平时相反）。`package-lock.json` 取 `--ours` 后用 `npm install` 重生成。
4. AskUserQuestion 是本 fork 的命脉：主仓库走 extMethod、不支持 elicitation。合并时**两路并存**，绝不让上游的 form-only 逻辑禁用它（案例 2）。
5. package.json 解冲突当心**重复 key**（公共行别在 new_string 重写）；version/依赖取上游、build/esbuild 取我方。
6. 后处理改动（重生成的 lock、适配的测试）用 `git commit --fixup=<sha>` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash` 并入逻辑所属提交。
7. fork 测试已知 **6 个** Windows 路径分隔符失败是上游缺陷（案例 1 家族，2 个 toDisplayPath + 4 个 #867 refine 测试），别误判为回归；主仓库 `pnpm check` 的 FileWatcher/DiffEditor/`Channel closed`(IPC) 偶发失败是既有 flake，单独 `pnpm --filter @universe-editor/editor run test` 重跑即绿。
8. `pnpm agent:build` 会 prune fork 到生产依赖；之后要再跑 fork 测试先 `npm install`。⚠️ 这次 `npm install` 可能把 `package-lock.json` 弄脏（本机 npmmirror registry 元数据更新后重解析 optional devDep，如 `@emnapi/wasi-threads` 小版本漂移 + 补上之前缺失的 `@emnapi/core` 条目）。**别急着丢弃**：npm 对 optional 依赖解析失败会静默省略 lock 条目，rebase 当天生成的 lock 可能因缓存元数据过期而缺条目，当天 `npm ci` 靠同样的缓存蒙混过关，隔天后 `npm ci` 就会报 `Invalid/Missing ... EUSAGE`（`agent:build`/打包必挂）。判别法：`npm ci --dry-run` 能过才算噪音可丢弃；报错就说明脏 lock 才是同步态，必须 commit（fixup 进 esbuild 提交 + autosquash，lock-only 重放无冲突）。
9. 全流程末尾用 `git diff --submodule=log vendor/claude-agent-acp` 核对“我方提交在顶 + 上游新提交在下”，再提交主仓库指针。
10. **rebase 零冲突 ≠ 语义正确**：上游做接口/抽象层重构时，我方挂在旧结构上的接口声明+实现可能被整体顶替而只留调用点（案例 5）；上游新增运行时校验时，我方旧测试的人为构造序列会失效（案例 6）。第 3 步 `npm run typecheck` **和** `npm test` 都是必跑安全网，别因 rebase 顺利就跳过。
11. **合并方式固定 rebase，不用再问用户**；只需就“推送范围”征询。选“仅本地不推送”时到本地 `main` 指向合并结果 + 主仓库 `agent:build`/`pnpm check` 验证为止，不 push fork、不提交 submodule 指针。

## 关键参考路径
- 根 `CLAUDE.md`「内置 ACP agent」段 + `scripts/release/{vendor-install.mjs,runtime-resources.mjs}`、`package.json` 的 `agent:build`
- `vendor/claude-agent-acp/src/{acp-agent.ts,tools.ts,interactive.ts,elicitation.ts}`
- 主仓库 `apps/editor/src/renderer/services/acp/{acpClientService.ts,acpSessionService.ts,acpSession.ts}`、`workbench/agents/QuestionCard.tsx`
- 记忆 `acp-fork-windows-path-test-flake`

## 其它
- 后续用本 skill，发现新经验，需同步更新本文件