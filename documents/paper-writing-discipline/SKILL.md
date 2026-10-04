---
name: paper-writing-discipline
description: |
  当用户在科研写作过程中踩到一个本系列 paper-* skill 没覆盖的新坑、
  并表示"以后...我都要这样做"、"下次记得..."、"这种情况要先..."、"加一条新规则"时，
  帮用户把这条新规则按 4 个判断题筛过，合格则按本 skill 提供的模板提炼成一个新的 paper-* skill 落盘。
  Use when 用户说"以后...都要..."、"下次记得..."、"这种情况要先..."、
  "帮我把这个习惯固化下来"、"加一条新规则"。
---

# paper-writing-discipline：怎么把新坑变成新 skill

## 核心理念

skill 不是知识，是**踩过坑后才悟出来的纪律**。
每次踩新坑，都是写一个新 skill 的机会——别让同一个坑再踩第二次。

> 知识可以查，纪律必须前置。

---

## 触发条件

用户出现以下任一信号 → 触发：

- 「以后...我都要...」
- 「下次记得...」
- 「这种情况要先...」
- 「这个教训我得记下来」
- 「帮我把这个习惯固化下来」
- 「再加一条新规则到 skill 里」
- 你识别到用户刚踩了一个坑、且这个坑可被规则化避免

---

## 4 个判断题（不全过 ≠ 写 skill）

判断这条新规则是否值得做成 skill：

```
Q1：不用会翻车？
  ├─ 不用没事 → 不是纪律，是偏好 → 不要 skill，写进 CLAUDE.md
  └─ 不用会翻车 → 进入 Q2

Q2：是反直觉的？
  ├─ "本来就该这么做"的常识 → 不要 skill（太弱）
  └─ 必须经历过才懂 → 进入 Q3

Q3：能在动手前就触发？
  ├─ 只能事后补救 → 不是 skill，是 hook
  └─ 能在用户提需求时就触发 → 进入 Q4

Q4：是 HOW 不是 WHAT？
  ├─ 是某个工具的用法 → 写文档 / 教程
  └─ 是"做事的方式" → 做 skill ✅
```

**4 个全过 → 写 skill。任何一个 No → 改用其他形式（CLAUDE.md / hook / 教程）。**

---

## SKILL.md 模板（直接复制改填）

```markdown
---
name: paper-<动词>-<对象>
description: |
  [一段中文，说清这个 skill 防什么灾]
  Use when [中文触发条件，列具体场景]。
---

# paper-<名字>：[一句话标题]

## 核心理念
[1-2 句，说清这条纪律的根本原因]
> [一句金句，让用户读到就记住]

## 触发条件
满足任一条 → 触发：
- [...]
- [...]

## 强制流程
\`\`\`
[简单流程图]
\`\`\`

## 标准回复模板
> [让 AI 能直接套用的话术]

## ❌ 反例（书 §X.X）
[具体翻车故事]

## Rationalization Table
| 念头 | 现实 |
|---|---|
| [...] | [...] |

## Red Flags
- [...]

## 来源
《Claude Code 科研手记》§X.X
```

---

## 命名规范

- 前缀统一 `paper-`（让所有 skill 在 `~/.claude/skills/` 里聚成一组）
- 动词开头：`paper-confirm-before-doing`、`paper-backup-before-word`
- 描述触发场景，不是描述功能
- 只用小写字母 + 数字 + 连字符（YAML 强制）

| ✅ 好名字 | ❌ 坏名字 |
|---|---|
| paper-backup-before-word | word-backup-system |
| paper-pilot-before-batch | batch-task-helper |
| paper-confirm-before-doing | task-confirmation |

---

## description 写法

**核心原则**：description 写"什么时候触发"，不要写"做什么"。

| ✅ 好 | ❌ 坏 |
|---|---|
| Use when 用户编辑 .docx 文件之前 | 这是一个 Word 备份工具 |
| Use when 用户给出模糊润色任务 | 用来润色论文段落 |
| Use when 拿到导师录音 / 便条 | 处理导师反馈的 skill |

为什么：description 进入 Claude 的 system prompt，决定它"要不要打开这个 skill"。
描述功能 → Claude 不知道何时调用 → 永远不会被触发。

---

## 必备 6 个栏目（缺一不可）

每个 paper-* skill 必须有：

1. **核心理念**（1-2 句 + 一句金句）
2. **触发条件**（list，要具体）
3. **强制流程**（流程图 / 步骤）
4. **标准回复模板**（能直接套）
5. **Rationalization Table**（封掉合理化借口）
6. **Red Flags**（自检停止信号）

可选：❌ 反例、例外情况、配套 skill、来源。

---

## 写完之后的检查清单

- [ ] 文件名为 `paper-<动词>-<对象>/SKILL.md`
- [ ] frontmatter 只有 `name` 和 `description`
- [ ] description 以 "Use when" 段为主
- [ ] 6 个必备栏目齐了
- [ ] Rationalization Table ≥ 4 条（少了不够辛辣）
- [ ] 有 1 个具体反例（来自书或用户经历）
- [ ] Red Flags 都是"念头/动作"级别，不是"情况"级别
- [ ] 用 Read 重新打开自检一遍是否能让一个不知情的 AI 看懂

---

## 落盘位置

写完后放到：

```
~/.claude/skills/paper-<新 skill 名>/SKILL.md
```

之后用户开新会话，这个 skill 就自动出现在系统提示的 skill 列表里。
本系列 skill 也可以集中放在 `~/.claude/skills/paper-pack/` 子目录里统一管理。

---

## ❌ 反例

用户："以后我让你改 .tex 文件时，你要先确认编译能过。"

**错误做法**：直接写一个 paper-check-latex-compile skill。
**正确做法**：先用 4 个判断题筛——

- Q1（不用会翻车）：✅
- Q2（反直觉）：⚠️ 偏弱，"改完编译"算半个常识
- Q3（动手前触发）：✅
- Q4（HOW 不是 WHAT）：✅

→ Q2 偏弱，建议先写进 CLAUDE.md 的"工作纪律"部分。如果用户后续两次都没这么做、又踩了坑，再升级为 skill。

---

## Rationalization Table

| 念头 | 现实 |
|---|---|
| "用户的需求很具体，直接照做就好" | 直接照做产出的是脚本，不是 skill |
| "4 个判断题太麻烦" | 不过这 4 题，写出来的是噪音，反而稀释整个体系 |
| "先写出来，不好用再删" | 删一个 skill 比加一个 skill 难——它已经污染了 system prompt |
| "用户说要的，肯定值得做" | 用户说要 ≠ 是 skill。可能是 CLAUDE.md，可能是 hook |
| "skill 越多越显得体系完整" | skill 多到一定程度互相冲突，反而每个都触发不准 |

---

## Red Flags

- 你跳过 4 个判断题就开始写 → 停
- 你写了一个不带 Rationalization Table 的 skill → 不合格，回去补
- 你的 description 写的是"做什么"不是"什么时候用" → 不会触发
- 你写了第 N 个 paper-* skill 但还没用过 → 先用一周再加新的

---

## 来源

参考 superpowers:writing-skills（适配中文科研写作场景）。
