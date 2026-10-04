---
name: handoff
description: Create a compact handoff document for another agent, machine, or fresh session. Supports temporary handoff files and persistent Obsidian `07_交接台` task handoffs with external large artifacts under iCloud `AgentArtifacts/`.
---

# Handoff

Write a concise Markdown handoff so a fresh agent can continue the work without re-reading the whole conversation. Match the user's current language by default; in Chinese conversations, write the handoff in Chinese while keeping commands, file paths, URLs, issue IDs, commit hashes, and skill names in their original form.

## 输出位置

根据用户意图选择落点:

- 临时交接: 默认保存到 OS 临时目录，不写入当前 workspace；文件名为 `handoff-YYYYMMDD-HHMMSS-<short-topic>.md`
- 项目制品: 只有当用户明确要求把 handoff 落到当前 workspace 时，才写入当前 workspace
- 多机器长期接力: 当用户提到不同机器、家里机器、远程 Codex/Claude Code、Obsidian、知识库交接台、接着在另一台机器做时，默认写入 Obsidian Vault 的 `07_交接台`

持久交接的标准结构:

```text
07_交接台/
  01_Inbox/
  02_Active/<category>/<task_id>/
    00_Task.md
    01_Assets.md
    YYYY-MM-DD-HHMM__<topic-slug>.md
  03_Blocked/<category>/<task_id>/
  04_Archive/YYYY-MM/<task_id>/
  90_Templates/
```

大型产物、视频、压缩包、下载物和中间处理文件不要放进 Obsidian Vault；统一放到 iCloud Drive 顶级目录 `AgentArtifacts/`，并在 `01_Assets.md` 中索引:

```text
iCloud Drive/AgentArtifacts/
  01_Active/<category>/<task_id>/
    raw/
    working/
    outputs/
    exports/
```

## 工作流程

1. 从用户请求中识别下一轮会话的重点；如果用户没给重点，就根据当前任务推断最可能的继续方向。
2. 判断 handoff 类型: 临时交接、当前 workspace 项目制品，或 `07_交接台` 持久接力。
3. 若是持久接力，选择分类并使用稳定 `task_id`:
   - `project`: repo、app、产品推进
   - `research`: 调研、教程、资料分析
   - `knowledge`: 最终要沉淀进知识库的内容整理
   - `ops`: 工具链、环境、同步、配置、自动化
   - `media`: 视频、图片、音频、素材处理
   - `task_id` 格式为 `<YYYY-MM-DD>-<english-slug>`
4. 只收集继续工作必需的上下文：
   - 当前目标和最新用户请求
   - 已做决定，以及仍然有效的约束
   - 相关文件、URL、issue ID、PRD、ADR、计划、commit、diff 或生成制品
   - 已运行命令、验证结果和已知失败
   - 阻塞点、待确认问题和下一步具体动作
5. 如果当前任务涉及 Git repo，只运行只读检查，例如 `git status --short` 和有针对性的 `git diff --stat`。不要 stage、commit、sync 或 push。
6. 脱敏 secrets、token、凭据、私有 API key 和敏感个人信息。如果某个值对下一步重要，用占位符替代，并说明下一位 agent 应从哪里获取。
7. 持久接力时更新 `00_Task.md` 的当前状态和最新 handoff，新增本次 `YYYY-MM-DD-HHMM__<topic-slug>.md`（`topic-slug` 为本次交接重点的英文短 slug；机器与 agent 写进 frontmatter 的 `machine` / `agent`，不进文件名）；旧 handoff 按 append-only 处理，不回写。
8. 如果写入 Obsidian Vault 中的 `.md`，最后执行 `touch "<file>"` 触发 Obsidian/iCloud 感知。
9. 汇报保存路径，并说明是否有敏感信息被有意脱敏。

## 临时 Handoff 模板

```markdown
# Handoff：<简短主题>

## 目标
<下一位 agent 或下一轮会话要完成什么。>

## 当前状态
<工作现在处于什么状态，包括已经完成了什么。>

## 关键上下文
<仍然重要的决定、约束、假设和用户偏好。>

## 相关制品
- <Path or URL>: <why it matters>

## 变更文件
<仅在相关时总结 repo 状态。引用 diff，不要粘贴大段 patch。>

## 验证结果
- <Command or check>: <result>

## 待确认问题
- <问题或阻塞点；如果没有，写“暂无”。>

## 建议技能
- <$skill-name>: <why the next agent should use it>

## 下一步
1. <第一个具体动作>
2. <第二个具体动作>
3. <如有必要，第三个具体动作>
```

## 持久接力模板

`00_Task.md`:

```markdown
---
type: handoff-task
status: active
category: media
task_id: 2026-06-29-openmontage-douyin-tutorial
owner_machine: home-mac
created: 2026-06-29
external_assets: iCloud Drive/AgentArtifacts/01_Active/media/2026-06-29-openmontage-douyin-tutorial/
---
# <任务名>

## 当前结论
## 当前状态
## 下一步
## 最新交接
## 关键文件
## 外部资产
## 未验证 / 风险
```

单次 handoff:

```markdown
---
type: handoff-session
task_id: 2026-06-29-openmontage-douyin-tutorial
machine: home-mac
agent: codex
created: 2026-06-29 14:51
---
# Handoff

## 一句话结论
## 本次完成
## 下一步可直接执行
## 关键路径
## 阻塞 / 待确认
## 给下一个 agent 的指令
```

## 规则

- 不重复已经沉淀在 PRD、计划、ADR、issue、commit 或 diff 里的内容；改用路径或 URL 引用。
- handoff 要足够短，方便快速阅读；优先给指针，不粘贴大段内容。
- 只要特定 skill 对下一位 agent 有帮助，就保留 `建议技能` 部分。
- `建议技能` 必须使用实际 skill 名称，并明确提示下一位 agent 通过 Skill tool 调用；不要把 skill 只写成普通参考资料。
- 如果用户给了 handoff 重点，围绕该重点写，不要总结所有事情。
- 持久接力按任务父目录组织，不按机器平铺；单次 handoff 文件名用 `<时间>__<topic-slug>`（体现这次交接关于什么），机器和 agent 只写进 frontmatter，不进文件名。
- 同一任务的 `00_Task.md` 是当前真相，最新 agent 接棒优先读它和最新一个 handoff。
- 大型产物只进 `AgentArtifacts/`，Obsidian 中只保存路径、清单和说明。
- 除非用户单独要求，不要 archive、close、sync、commit、push，也不要改变其他外部状态。
