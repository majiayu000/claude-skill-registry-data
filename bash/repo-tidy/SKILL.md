---
name: repo-tidy
description: "Prepare safe task branches/worktrees, preserve active or unverified work, and keep session working directories in sync. Use for new repository-changing tasks or requested cleanup; not for read-only audits, continued tasks, or status checks."
---

# repo-tidy

把本地仓库恢复到「默认分支与远端一致、无可安全回收的遗留分支/worktree」的基线状态。默认分支优先读取 origin/HEAD，缺少该引用时才兼容 master/main。归位发生在**下一个任务开始时**（push 完 MR 未合，任务结束时无收尾时机）。

组件（脚本就地运行于 skill 目录，不复制副本）：
- `scripts/repo_tidy.py` —— 核心：tidy / `--all` / `--new`
- `scripts/git-repo-status.sh` —— SessionStart hook：注入 `[repo-status]`（分支/ahead-behind/脏净）+ `[tasks]` 菜单（各 worktree 的分支与状态：已合并可回收 / 已推送 MR 待合 / 未推送 / 工作区脏），供判断续任务还是开新任务
- `scripts/session-cwd.sh` —— 把本 session 的 cwd 写到 `~/.claude/session-cwd/<iTerm 会话 id>`。用户的编辑器快捷键按前台标签页 id 读它，于是打开的永远是 AI 当前所在目录——**子进程改不了父 shell 的 cwd，所以不能靠 shell 的当前目录**。静默输出（挂在 SessionStart/UserPromptSubmit 上，stdout 会被注入上下文）
- `scripts/worktree-fetch.sh` —— PreToolUse(EnterWorktree) 先 `fetch --prune`，保证新任务分支从最新的 origin/<默认分支> 切出
- `scripts/install.sh` —— 一键注册上面几个 hook 到 `~/.claude/settings.json`；幂等、改前备份、只增不删
- `scripts/editor-here.sh` —— 绑到编辑器快捷键：按前台标签页 id 读位置文件，打开 AI 当前所在目录；读不到再回退到终端路径
- `scripts/task-here.sh` —— 声明「本 session 当前在做哪个任务目录」，给运行中不能切 cwd 的 agent（Codex）用；Claude Code 不需要
- `tests/` —— `test_repo_tidy.sh`、`test_session_cwd.sh`、`test_install.sh`（另有 `scripts/test_git_repo_status.sh`），改脚本后必须跑

## 安装

前置：`python3`、`git`、可写的 `~/.claude/`。缺任一项先停下说明，不带病安装。

私人配置（`settings.json` / `CLAUDE.md`）不进版本库，所以用脚本改——幂等、改前备份、只增不删，不碰用户已有的其它 hook：

```bash
bash "$SKILL_DIR/scripts/install.sh"             # 安装（可反复跑）
bash "$SKILL_DIR/scripts/install.sh" status      # 体检：依赖 / 核心层 / 增强层 / hook 注册
bash "$SKILL_DIR/scripts/install.sh" --uninstall # 只移除本 skill 注册的 hook
```

**Claude Code 与 Codex 都装**，检测到哪个装哪个（`CLAUDE_HOME` / `CODEX_HOME` 可覆盖路径，测试用）。两边的 hook 事件名与 stdin 格式一致（都是 `{"cwd":...,"hook_event_name":...}`），所以脚本是同一份。

| 事件 | matcher | 脚本 | Claude Code | Codex |
|---|---|---|---|---|
| SessionStart | `*` | `git-repo-status.sh`、`session-cwd.sh` | ✓ | ✓ |
| UserPromptSubmit | `*` | `session-cwd.sh` | ✓ | ✓ |
| PostToolUse | `EnterWorktree\|ExitWorktree` | `session-cwd.sh` | ✓ | — |
| PreToolUse | `EnterWorktree` | `worktree-fetch.sh` | ✓ | — |

后两条只给 Claude Code：Codex 没有 `EnterWorktree` 工具，它用原生的 `codex --worktree`（启动时就进 worktree）和 `-C/--cd`。

hook 热生效，装完不用重启 session。**Codex 首次运行会要求确认信任新 hook**。

### Codex：对话中决定任务目录，不必启动前就想好

Codex 运行中不能切工作目录，但**能用绝对路径在别的目录里干活**（已实测）。所以流程和 Claude Code 一样是「先聊、再决定」，只是多一步声明：

1. 在项目主路径启动 `codex`，照常对话
2. 判断是新任务且需要独立目录 → **先问用户**，同意后：
   ```bash
   python3 "$SKILL_DIR/scripts/repo_tidy.py" . --new <task>
   ```
   主检出空闲就原地切分支（此时 cwd 就是任务目录，第 3 步可跳过）；被占用则建 worktree 并输出路径
3. 若拿到的是 worktree 路径，声明它，好让用户的编辑器快捷键跟过去：
   ```bash
   bash "$SKILL_DIR/scripts/task-here.sh" <worktree 路径>
   ```
   之后用绝对路径在那个 worktree 里读写、跑 `git -C <路径> ...`
4. 任务结束 `task-here.sh --clear`

**不要让用户用 `codex --worktree` 或 `-C` 启动**——那等于逼人在开口之前就想清楚要做什么，和「先聊再决定」是相反的。这两个参数只在用户主动要求时才提。

声明存在 `<键>.task`，优先级高于 hook 写的 `<键>`：后者每轮对话都会被刷新成 cwd，不分开存会被冲掉。Claude Code 不需要声明——`EnterWorktree` 真的改了 cwd，hook 自动就写对了。

Codex 侧拿不到 tty（hook 父进程无控制终端），只走 `TERM_SESSION_ID` 键——iTerm2 / Terminal.app 都设这个变量，够用。

### 两层能力，各自独立可用

**核心层**（仓库归位、任务 worktree、开工前 fetch、`[tasks]` 菜单）是纯 git 操作，**与平台和终端无关**，任何环境都能用。

**增强层**（编辑器快捷键打开 AI 当前所在目录）需要「能报出当前是哪个终端标签页」，只有这层有环境要求。没有它不影响前面任何功能。

### 增强层：绑编辑器快捷键

把 `scripts/editor-here.sh` 绑到快捷键（iTerm2 用 Preferences → Keys 的 Send Text / Run Coprocess，或 Hammerspoon / Karabiner 调用）。

**不能直接绑 `code .`**：claude 运行期间终端的当前目录冻结在启动目录，子进程改不了父 shell 的 cwd，AI 切进 worktree 后 `code .` 打开的还是旧目录。

| 环境 | 状态 |
|---|---|
| macOS + iTerm2 | 已实测 |
| macOS + Terminal.app | 已写支持（按 tty 匹配），**未实测** |
| 其它终端（WezTerm / Alacritty / tmux / VS Code 内置） | 需设 `SESSION_KEY_CMD`，**未实测** |
| Linux / WSL | 核心层可用；增强层需 `SESSION_KEY_CMD` + `EDITOR_HERE_CMD`，**未实测** |

标「未实测」的是照着 API 文档写的，作者手上没有那些环境。能跑通或需要改，欢迎开 issue / PR。

`session-cwd.sh` 按两个键各写一份位置文件，就是为了让不同终端各取所需：

- `<UUID>` —— `TERM_SESSION_ID` 的 UUID 段，iTerm2 与 Terminal.app 都设这个变量
- `tty-<name>` —— 控制终端名，POSIX 通用回退

其它终端设 `SESSION_KEY_CMD` 指定一条输出「当前标签页唯一键」的命令，`editor-here.sh` 会拿它去查同名或 `tty-` 前缀的位置文件。例如 tmux：

```bash
export SESSION_KEY_CMD="tmux display-message -p '#{pane_id}'"
```

环境变量：`EDITOR_HERE_APP`（macOS 上要打开的应用，默认 VS Code）、`EDITOR_HERE_CMD`（直接指定打开命令，如 `cursor` / `zed`）、`EDITOR_HERE_DRY=1`（只打印路径不打开，排错用）。

### 排错

先跑 `install.sh status`，它会分层告诉你卡在哪一环：hook 没注册、终端认不出、位置文件不新鲜（hook 没在跑）、`editor-here.sh` 不可执行。

快捷键打开了错目录 → `EDITOR_HERE_DRY=1 bash scripts/editor-here.sh` 看它解析到什么，再看 `$TMPDIR/editor-here.log` 最后一行的来源标签（`ai-session` 走的是位置文件，`terminal-path` 说明回退了）。

### 卸载

```bash
bash "$SKILL_DIR/scripts/install.sh" --uninstall   # 移除 hook（备份已自动留下）
rm -rf ~/.claude/session-cwd                        # 位置文件
```

再解绑编辑器快捷键、删除 skill 目录即可。`settings.json` 的备份在 `~/.claude/settings.json.bak-*`。

## 何时用

- 用户说「归位」「整理仓库」「清理分支/worktree」
- 需要修改仓库的新任务开工前；只读审计、问答、续任务不归位，`[repo-status]` 本身不触发动作
- 显式调用 do-something 时遵循该 skill 的 do/main 续做规则，不额外开普通任务分支
- 用户明确要求提交后的仓库整理

## 执行步骤

### 1. Dry-run 出清单

`SKILL_DIR` 指本 SKILL.md 所在目录（全局安装、项目级安装、plugin 缓存目录均适用，按实际安装位置解析，不要硬编码）。

```bash
# 单仓库（默认当前目录）
python3 "$SKILL_DIR/scripts/repo_tidy.py" <repo-path>

# 全部仓库（扫描 ~/Desktop/Works/code）
python3 "$SKILL_DIR/scripts/repo_tidy.py" --all
```

### 2. 核对范围后执行

核对 dry-run 清单与授权范围。已授权的单仓库清理或按项目规则启动新任务，可直接处理已核实安全的对象，不因换轮次重复询问。未推送、未合并、脏工作区、活跃任务或归属不明的对象保留；范围扩大或存在数据丢失风险时说明影响并确认。

`upstream 已删除` 本身不能证明工作已合并。脚本只自动清理已证实为默认分支祖先的分支；未证实合并的 gone 分支保留并报告；其关联 worktree 同样保留，但不单独列出目录。不阻塞 `--new` 创建新任务。squash 等不能由祖先关系证实的情况，也不自动删除；需要另行核实内容保留证据和清理授权。

```bash
python3 "$SKILL_DIR/scripts/repo_tidy.py" <repo-path> --apply
```

### 3. 开新任务（已有范围授权时直接执行）

**Claude Code 里走 `EnterWorktree`，不要用 `--new`。**读 SessionStart 注入的 `[tasks]` 菜单判断：

- 续某个任务 → `EnterWorktree(path=<该 worktree 路径>)`
- 新任务 → `EnterWorktree(name=<task>)`
- 两个 session 共用一个 worktree（一个写、一个 review）→ 同样用 `path`
- 已有任务范围授权时直接进入工作树，不重复确认；只有工作位置会改变目标、范围或重大后果时才确认。用户明确要求留在主检出时遵循。session 中途换新任务：`ExitWorktree(keep)` 再 `EnterWorktree(name=...)`，同样复用已有授权

配套 hook 保证两件事：进门前已 fetch（新分支基于最新远端默认分支），进门后位置文件已更新（用户快捷键看到的就是这里）。主检出因此恒定停在默认分支，只作阅读窗口——**默认不在主检出上开工，用户明确要求时除外**，否则第一个任务就会把它占走，后续任务被迫绕到 worktree，而没人再把它还回来。

没有 `EnterWorktree` 的环境（如其他 CLI）才用回退命令：

```bash
python3 "$SKILL_DIR/scripts/repo_tidy.py" <repo-path> --new <task>
```

- 先对该仓库执行一次归位（等价 `--apply`，安全边界相同）
- 主检出空闲（在默认分支且无 tracked 改动）→ 原地 `switch -c task/<task> origin/<默认分支>`，**这会占用主检出**
- 主检出被占用 → 创建 sibling worktree `<仓库>--<task>`（基于最新 origin/<默认分支>）并输出 `cd` 路径
- 若占用主检出的分支**已经合并进默认分支**（任务做完没归位的僵尸），会明确报出来并给归位命令，而不是默默绕开——绕开正是主检出被长期霸占的原因：每个新任务都躲去 worktree，没人回来收拾
- `<task>` 含 `/` 时按原样作分支名，否则加 `task/` 前缀

## 脚本行为（安全边界）

| 对象 | 条件 | 动作 |
|------|------|------|
| 本地分支 | 已合并进 origin/<默认分支> | 删除 |
| 本地分支 | upstream 已删除 | 已证实合并则按上一行清理，否则保留并报告 |
| 本地分支 | 有未推提交 / 从未推送 / MR 进行中 | **保留并报告** |
| 本地分支 | 与 origin/<默认分支> 同点且未推送过（刚切出的空任务分支） | **保留**（并行 session 可能正要用） |
| 本地分支 | 空且已落后 origin/<默认分支>（切出后从未动过） | 删除（无内容可丢，重切才是正确归位） |
| 当前分支 | 可清理且工作区无 tracked 改动 | 切回默认分支再删 |
| 默认分支 | 落后远端 | ff-only 前进 |
| 默认分支 | 与远端分叉 | **不动，报告** |
| worktree | 分支可清理且工作区干净 | 移除 |
| worktree | 工作区脏 / detached | **保留并报告** |

脚本自身永远可以 dry-run；一切「✋ 保留」项需要人工决策，不要替用户强清。

## 不做的事

- 不删除整目录的克隆分身（如 `xxx-mr199/` 这类完整 clone）——发现时报告给用户，删目录是危险操作需单独确认
- 不 force push、不改写历史、不碰远端分支
