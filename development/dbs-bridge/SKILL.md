---
name: dbs-bridge
description: |
  Agent 基建：把任意 skill 或 skill 集合目录桥接到 Claude Code（~/.claude/skills）、Codex（~/.codex/skills）、通用 Agents（~/.agents/skills，豆包 Mac App / Trae Solo / Codex 可读取）和 Grok（~/.grok/skills）。支持 dbskill 仓库内 skill，也支持外部 skill 绝对路径。Claude / Codex / 通用 Agents 使用软链，Grok 生成带 user_invocable: true 的薄 bridge。支持按 skill 名称、相对路径、绝对路径、skills 目录批量桥接，也支持拆桥和查看桥接状态。
  触发方式：/dbs-bridge、/bridge、「桥接这个 skill」「桥接整个 skills 目录」「把这个 skill 接到 Claude Code、Codex、豆包和 Grok」「让多个 Agent 都能调用这个 skill」「取消桥接」「查看桥接状态」
  Bridge any skill folder or directory of skill folders to Claude Code, Codex, generic Agents (~/.agents/skills), and Grok using symlinks plus Grok bridge files. Supports dbskill skills and external skill directories. Use when the user wants one or many skills callable from multiple agents, or wants to unlink/check bridge status.
  Trigger: /dbs-bridge, /bridge, "bridge this skill", "bridge this skills directory", "make this skill available to Claude Code, Codex, Doubao, and Grok", "unlink this skill", "check bridge status"
---


# dbs-bridge：多端 skill 桥接

把任意包含 `SKILL.md` 的 skill 源目录，或包含多个 skill 子目录的集合目录，用软链同时挂到：

- `~/.claude/skills/<skill-name>`
- `~/.codex/skills/<skill-name>`
- `~/.agents/skills/<skill-name>`

同时为 Grok 生成薄 bridge：

- `~/.grok/skills/<skill-name>/SKILL.md`

这样 Claude Code、Codex、豆包 Mac App、Trae Solo、Grok 等 Agent 都能通过同一个源目录调用该 skill。源目录改动后，各端自动同步。源目录可以在 dbskill 仓库内，也可以在外部项目、`~/.claude/skills` / `~/.codex/skills` / `~/.agents/skills` / `~/.grok/skills` 以外的本地目录、iCloud 目录或其他工作区。

---

## 核心原则

1. **Claude / Codex / 通用 Agents 只用软链。** 不复制 skill 文件，避免多端出现版本分叉。
2. **源目录可以在任何位置。** 桥接目录只指向源目录。
3. **绝不覆盖真实目录。** 如果目标位置已有同名真实目录，停下来报告，让用户手动处理。
4. **Grok 生成薄 bridge。** Grok bridge 必须包含 `user_invocable: true` 并指向真源。
5. **拆桥只删派生产物。** 取消桥接时只移除 `~/.claude/skills`、`~/.codex/skills`、`~/.agents/skills` 下的软链和 `~/.grok/skills` 下由本工具生成的 bridge，不删除源目录。
6. **优先用脚本执行。** 使用本 skill 自带脚本 `scripts/bridge-skill.sh`，不要临场重写桥接命令。

---

## 确定源 skill

用户可能给：

- skill 名称：`dbs-hook`
- 相对路径：`skills/dbs-hook`
- 绝对路径：`/Users/.../dbskill/skills/dbs-hook`
- 外部绝对路径：`/Users/.../.agents/skills/lark-doc`
- skill 集合目录：`/Users/.../dbskill/skills`
- 当前上下文刚创建或刚修改的 skill

按优先级判断：

1. 用户明确给了绝对路径，直接使用该路径。
2. 用户给了相对路径，先按当前工作目录解析，再按 dbskill 仓库根目录解析。
3. 用户只给 skill 名称，优先查当前工作目录下的同名目录，再查 dbskill 仓库 `skills/<name>`。
4. 用户只说“这个 skill”，使用当前对话里刚创建、刚改名或刚讨论的 skill。
5. 仍不确定时，查看当前工作目录和仓库 `skills/` 下最近修改的 skill。
6. 还是无法确定时，只问一句：`桥接哪个 skill？给我 skill 名称或路径。`

源目录必须满足其中一种条件：

- 目录本身包含 `SKILL.md`；
- 目录的一级子目录里包含多个 `SKILL.md`，用于批量桥接。

---

## 执行桥接

在 dbskill 仓库根目录运行：

```bash
skills/dbs-bridge/scripts/bridge-skill.sh link <skill-name-or-path>
```

例子：

```bash
skills/dbs-bridge/scripts/bridge-skill.sh link dbs-hook
skills/dbs-bridge/scripts/bridge-skill.sh link skills/dbs-beta-framework-builder
skills/dbs-bridge/scripts/bridge-skill.sh link skills
skills/dbs-bridge/scripts/bridge-skill.sh link "/absolute/path/to/skill"
skills/dbs-bridge/scripts/bridge-skill.sh link "/Users/me/external-skills/my-skill"
skills/dbs-bridge/scripts/bridge-skill.sh link "/Users/me/external-skills"
```

执行后把脚本输出里的各宿主桥接结果回给用户。

---

## 查看状态

用户问“桥好了没”“查看桥接状态”时运行：

```bash
skills/dbs-bridge/scripts/bridge-skill.sh status <skill-name-or-path>
```

输出应说明 Claude Code、Codex、通用 Agents 和 Grok 四个位置分别指向哪里。

---

## 取消桥接

用户说“取消桥接”“拆桥”“unlink”时运行：

```bash
skills/dbs-bridge/scripts/bridge-skill.sh unlink <skill-name-or-path>
```

拆桥完成后告诉用户：源 skill 没有被删除，只移除了各端派生产物。

---

## 输出规范

桥接完成后，简短回报：

```markdown
已桥接 `<skill-name>`：

- Claude Code：`~/.claude/skills/<skill-name>` -> `<source-path>`
- Codex：`~/.codex/skills/<skill-name>` -> `<source-path>`
- 通用 Agents：`~/.agents/skills/<skill-name>` -> `<source-path>`
- Grok：`~/.grok/skills/<skill-name>` -> `<source-path>/SKILL.md`
```

如果遇到同名真实目录：

```markdown
没有覆盖 `<target-path>`，因为那里已经是一个真实目录。需要你先手动确认这个目录能否移走。
```

---

## 自检

每次执行前确认：

- 源目录存在；
- 源目录含 `SKILL.md`，或其一级子目录包含 `SKILL.md`；
- 外部路径必须使用绝对路径，或能从当前工作目录解析；
- Claude / Codex / 通用 Agents 目标位置如果存在，必须是软链才允许更新；
- Grok 目标位置如果存在，必须是本工具生成的 Grok Bridge 才允许更新；
- 不能删除源目录；
- 不能把 `skills/dbs-bridge` 自身复制到各端；Grok 只能生成薄 bridge。

---

## 不知道下一步用哪个 Skill？

输入 `/dbs`。

它会读取刚才的具体结论，选择当前最值得处理的一个方向，并直接路由到对应 Skill。