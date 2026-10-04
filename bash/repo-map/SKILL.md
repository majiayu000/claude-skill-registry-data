---
name: repo-map
description: |
  Local repository map for multi-repo development: scan every local git repo into an incremental, self-healing index (name, path, read/write role, purpose); a UserPromptSubmit hook auto-injects the path and role whenever a repo name is mentioned, so cross-repo references and edits never need hand-pasted paths; optional macOS launchd scheduled sync keeps new repos in the map. Use when the user works across multiple local repositories or says 仓库地图, repo-map, repo map, 全局项目索引, 跨仓库引用, 找不到本地仓库, 仓库地图定时更新.

---

# repo-map：本地仓库地图

## 机制概览（三层识别链路）

| 层 | 载体 | 覆盖场景 | 可靠性 |
|----|------|---------|--------|
| L1 | UserPromptSubmit hook 字符串匹配 | 用户提到明确仓库名 | 确定性 100% |
| L2 | 项目 CLAUDE.md「## 关联仓库」节 | 确认过的结构性老关系（选择性沉淀） | 常驻上下文 |
| L3 | 全局 CLAUDE.md 一行规则 + `resolve` 命令 | 模糊指代（"那个缺陷分级服务"） | 尽力而为兜底 |

核心不变量：**缓存是纯产物，人永远不维护**。每次 resolve/list/sync 先做低成本一致性检查（find .git 清单 vs 缓存路径集），差集增量分析、死路径自动剪枝。

自愈由谁触发，决定了"新仓库多久进地图"：

| 触发方式 | 时机 | 覆盖 |
|---------|------|------|
| `resolve`/`list` 内置同步 | 用户手动跑命令那一刻 | 被动，不跑就不更新 |
| launchd 定时 `sync`（可选，冷启动询问） | 每 N 秒自动 | 主动，新仓库无需任何动作 |

`sync` 比 `list` 的增量多做一件事：**重析未成型仓库**（无 remote 或无提交）。刚 `git init` 的仓库会被记成"本地·可写"且无摘要，等它配好远端、有了首次提交，必须复查才能修正角色——纯增量永远不会回头看已存在路径，这是定时任务存在的真正理由。

组件：`scripts/repo_map.py`（scan/resolve/list/sync/schedule）+ `scripts/prompt_hook.py`（hook）。脚本就地运行于 skill 目录，不复制副本（单一事实源）。

## 安装步骤（幂等，可重复执行）

### 1. 前置检查
`python3 --version`、`git --version`、`~/.claude/settings.json` 存在。任一缺失即停下说明，不带病安装。

### 2. 探测扫描根，与用户确认
- 从历史 session 反推：`ls ~/.claude/projects/` 的目录名即历史 cwd（`-` 分隔），统计高频路径前缀。
- 辅助验证：对候选前缀 `find <root> -maxdepth 6 -name .git | head` 确认确实有仓库群。
- 把探测结果（根目录 + 预计仓库数）报给用户确认后再写配置。扫描根是配置不是数据——一年变不了一次，手工列出最诚实。

### 3. 身份引导，写配置 `~/.claude/repo-map.config.json`
配置含个人邮箱与组织域名，是机器级私密文件：**绝不提交进任何仓库**（本仓库 .gitignore 已设防线），只存在于 `~/.claude/`。

首次安装（配置不存在）时不要让用户手打邮箱，先探测候选、再让用户选择（选择优于输入）：
- 候选邮箱来源：`git config --global user.email`，再抽 3-5 个扫描根内仓库统计高频作者（`git log --format=%ae | sort | uniq -c | sort -rn | head`）。
- 候选 host 来源：对扫描根内仓库的 remote host 做频次统计。
- 用选择题（AskUserQuestion，多选 + 其他手动输入出口）确认：哪些邮箱是"你本人"（含开源身份如 GitHub noreply 邮箱——漏了会导致自己的开源仓库被误判为第三方只读）；哪个 host 是组织内部的。

```json
{"scan_roots": ["~/code"],
 "self_emails": ["a@x.com", "you@users.noreply.github.com"],
 "trusted_hosts": ["gitlab.your-org.com"]}
```
- 角色判定证据链：有本人 commit → 自研·可写；无 remote → 本地·可写（不存在上游，谈不上第三方）；host 可信 → 协作·可写；其余 → 第三方·只读。

### 4. 首次全量扫描
`python3 <skill目录>/scripts/repo_map.py scan`，报告仓库总数、自研/第三方比例、耗时。

### 5. 注册 hook（修改 settings.json 前先备份）
- `cp ~/.claude/settings.json ~/.claude/settings.json.bak-<日期>`
- 向 `hooks.UserPromptSubmit` **合并追加**（绝不覆盖已有条目）：
```json
{"matcher": "*", "hooks": [{"type": "command", "command": "python3 <skill绝对路径>/scripts/prompt_hook.py"}]}
```
- 用 python json 读改写，不用文本替换；改完 `python3 -m json.tool` 校验合法性。

### 6. 定时增量更新（冷启动必问一次，之后幂等跳过）

先探测状态，**已开启就直接跳过本步、不要重复打扰**：

```bash
python3 <skill目录>/scripts/repo_map.py schedule status   # exit 3 = 未开启
```

未开启时用 AskUserQuestion 问用户（不要替用户决定，这会往系统里装一个常驻后台任务）：

> 是否开启定时增量更新？开启后新建的仓库会自动进地图，无需手动跑命令。
> - **开启·每小时**（推荐）：`schedule on`。增量同步实测亚秒级，开销可忽略。
> - **开启·每天一次**：`schedule on 86400`。新仓库最长隔一天才进地图。
> - **不开启**：靠 `resolve`/`list` 被动同步；新建仓库后需手动跑一次 `list`。

选择开启则执行 `schedule on [间隔秒]`，它会写 `~/Library/LaunchAgents/com.claude-code.repo-map-sync.plist` 并 `launchctl bootstrap` 加载（`RunAtLoad` 注册即跑一次，可立刻验证）。plist 里的解释器固定为 `/usr/bin/python3`——launchd 不继承 shell PATH，更不跑 pyenv 初始化，写 `python3` 必然找不到。

仅 macOS。非 darwin 平台 `schedule` 会明确报错并提示改用 cron 调 `sync` 子命令，不做静默降级。

### 7. 全局 CLAUDE.md 追加规则节（已存在则跳过）
定位真实文件（注意软链：`readlink` 确认目标），追加：

```markdown
## 跨仓库协作（repo-map）
- 任务涉及其他本地仓库时，用 `python3 <skill绝对路径>/scripts/repo_map.py resolve <名称>` 解析路径与读写角色；"第三方·只读"仓库禁止写入。
- 为 A 仓库任务修改 B 仓库时，改动在 B 仓库独立成 commit、独立授权，不与 A 仓库改动混杂。
- 关联沉淀遵循"宁可漏掉，不能沉淀错"：仅当本次真实读取/修改了该仓库、且关系会复发（依赖/对接/上下游）时，才向用户一句话确认后幂等追加到当前项目 CLAUDE.md 的「## 关联仓库」节（名称、路径、角色、一句话关系）；仅提及、误提及、一次性查询、cwd 为全局配置目录一律不沉淀——漏掉的成本≈0（hook 每次都会重新命中），沉淀错会长期误导决策。
```

### 8. 验证（铁律：不验证不得称完成）
全部真跑并收集输出：

1. **resolve 命中**：挑一个真实仓库名 `resolve <名>`，返回路径与角色。
2. **resolve 未命中**：`resolve 不存在的名字`，exit code 2 + 提示语。
3. **增量自愈**：`git init` 一个临时新仓库到扫描根内 → `list` 应出现；删除它 → `list` 应剪枝消失。
4. **hook 命中**：构造 stdin JSON 模拟真实输入（`echo '{"prompt": "参考一下 <真实仓库名>", "cwd": "/tmp"}' | python3 .../prompt_hook.py`），应输出 additionalContext。
5. **hook 中英相邻**：`"跟<仓库名>对接"`（无空格）应命中。
6. **hook 误报**：泛词（如 "kubernetes" 不应命中 kube 类短名仓库）、以及不含仓库名的普通输入，应零输出。
7. **hook 自身排除**：cwd 在某仓库内且 prompt 提到该仓库，不注入。
8. **性能**：`time ... list`（增量路径）应在秒级；hook 单次应在 1s 内（含 python 解释器启动）。
9. **判定抽查**：抽 ≥10 个仓库人工核对自研/第三方判定，报告准确率与误判原因。

开启定时任务时，追加三项**由 launchd 真实触发**的端到端验证（用 `launchctl kickstart gui/$(id -u)/com.claude-code.repo-map-sync` 立即触发，不要手跑脚本冒充）：

10. **自动纳入**：扫描根内新建裸仓库 → kickstart → 缓存出现该仓库。
11. **定型刷新**：给它配 remote + 首次提交 → kickstart → 角色/摘要/活跃日期被修正（这一项证明"未成型重析"生效，纯增量会在此失败）。
12. **自动剪枝**：删除该仓库 → kickstart → 缓存中消失；全过程日志见 `~/.claude/logs/repo-map-sync.log`。

### 9. 汇报
仓库数与角色比例、各验证项结果、日志位置（hook `~/.claude/logs/repo-map-hook.jsonl`、定时 `~/.claude/logs/repo-map-sync.log`）、定时任务开关状态、误判仓库清单（如有）。

## 日常使用

- 自动：直接在输入里提仓库名，hook 注入解析结果，无需任何命令。
- 手动：`resolve <关键词>` / `list` / `scan`（仅在怀疑缓存脏时才需要 scan）。
- **检出状态标注（防跨仓库读到任务分支残留）**：目标仓库非 master/main 检出时，hook 在命中行打【⚠️ 检出在 \<分支\>】标（纯文件读 `.git/HEAD`，零 subprocess，不破毫秒级契约），resolve 额外给 ahead/behind 与脏净全量状态；两处都附读取建议——用 `git -C <路径> show origin/master:<相对路径>` 读主分支内容，或先在该仓库归位（repo-tidy）。
- 定时任务：`schedule status` 查状态与最近一次同步；`schedule off` 关闭；`schedule on [间隔秒]` 改间隔（幂等重装）。
- 换机器/新根目录：编辑 config 的 `scan_roots` 后跑一次 `scan`。

## 卸载

先 `schedule off`（注销 launchd 任务并删 plist），再删除 settings.json 中对应 hook 条目、全局 CLAUDE.md 的「跨仓库协作」节、`~/.claude/repo-map.config.json`、`~/.claude/repo-map-cache.json`、`~/.claude/logs/repo-map-{hook.jsonl,sync.log}`，最后删 skill 目录。

注意顺序：先注销定时任务再删 skill 目录，否则 launchd 会按分钟级重试一个已不存在的脚本，在日志里刷错误。

## 已知边界

- 仅支持 macOS/Linux（依赖 git 与 POSIX 路径约定）；`schedule` 子命令仅 macOS（launchd），Linux 需自行用 cron 调 `sync`。
- 定时 `sync` 只重析"未成型仓库"（无 remote 或无提交）。**已定型仓库**后来换了 remote、改了 README 首行或转手他人，不会自动刷新——这类变更靠手动 `scan`（全量约 25s/191 个仓库）。这是刻意的成本权衡：定时全量意味着每次上千次 git 调用，而定型后的元信息几乎不变。
- launchd `StartInterval` 在机器睡眠期间不触发；唤醒后补跑一次，不累积。合盖一周再打开，地图会在唤醒后数秒内追平。
- hook 匹配的是封闭名字集合；模糊指代走 L3 兜底，漏了退回手贴路径一次。
- 只读硬闸（PreToolUse 拦截写只读仓库）为可选增强，本 skill 不默认安装——误写第三方仓库可用 git 恢复，成本中等。
- hook 注入的仓库职责摘要取自各仓库 README 首行（截断 80 字符）。第三方仓库的 README 首行会进入对话上下文，理论上存在提示注入面；克隆来源不可信的仓库时留意其 README 首行内容。
