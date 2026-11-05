---
name: phd-progress
description: 响应“一键更新”、更新论文进度或实验进度，从当前可见对话、用户汇报和批量材料提取真实科研进展，匹配已有记录后预检、批量保存并让网页同步。支持整理现有聊天，避免把开发工作、示例或计划误记为成果。
---

# 更新科研进度

先读取 [本地操作约定](../phd-manager/references/local-workflow.md)，在用户的项目仓库执行命令。字段及允许状态从仓库 `docs/IMPLEMENTATION_CONTRACT.md` 查询。

英文口令 **Update progress / Update paper progress / Update experiment progress** 与中文更新口令等价，直接执行；**Import progress** 转入导入流程，**Summarize advisor feedback / Generate weekly report** 按 [manager 路由](../phd-manager/SKILL.en.md) 继续完成。英文请求使用 [完整英文说明](SKILL.en.md) 并用英文答复，不自动翻译或重写已有科研内容，无需重复技能前缀。

## 一键更新与材料范围

- 用户直接输入 **“一键更新”**，默认整理当前可见对话中已提供的真实科研进展并保存。无需用户重新讲述上下文、选择网页按钮或再次指定技能。口令本身已授权明确事项的本地更新，不再以“是否执行”结束。
- “整理这段聊天/把刚才讨论同步到工作台”使用当前可见材料；过去聊天未提供的内容不可臆造。用户指定只预览时仅生成变更预览，不执行正式写入。
- “批量更新这些记录”合并多条事项，通过 [批量操作约定](../phd-manager/references/batch-workflow.md) 一次预检并保存。Markdown、CSV、文件清单或首次结构化导入交给 [phd-import](../phd-import/SKILL.md)，随后继续完成任务。
- 网站开发、技能改动、使用演示和 AI 提出的未确认计划不是用户科研成果。当前没有真实新材料或材料已全部登记时，报告“暂无新的科研进展需要更新”，不写入空批次、不更新示例、不为了产生活动记录而重复保存。

## 工作流

1. 从用户明确的对话上下文、记录 ID 和现有真实项目定位目标；先列出项目、任务，以及本次涉及的论文/实验/会议，读取目标记录的 ID 与 version。不能把网页当前选择当作已知上下文；多个候选无法区分时只询问该项。
2. 将输入拆成“已完成事实”“进行中工作”“阻塞”“后续计划”，保留用户原话或材料位置作为来源。复用现有任务；标题相近不足以证明同一任务，结合项目、关联论文和交付物判断。完全相同的事实和来源不重复追加，重复调用应只报告无变化。
3. 用户明确汇报完成时可标记任务 `done`，在 `notes` 或 `evidence` 记录产出/用户确认；仅“准备开始”或“计划完成”不标完成。延期保留原有原因并记录新的真实日期；没有明确日期则留空。
4. 对阻塞项写明缺少的依赖与一个可执行的解除步骤。只有用户要求安排后续工作时再登记建议任务，并标注 `origin: "ai"`。
5. 论文阶段与百分比分别判断。用户给出“已写完初稿”可更新到合适阶段，但不要擅自换算为 80%；明确百分比再写入 `progress`。实验“完成”交给实验工作流核对结果与证据。
6. 按 [批量操作约定](../phd-manager/references/batch-workflow.md) 形成必要增量，先 `node cli.mjs batch --file <json-file> --dry-run`，检查通过后用同一文件正式执行并回读。遇到事实冲突仅追问不能确定的项；其余独立明确项可先保存。保留既有 notes、数组和人工百分比。
7. 简要报告新增/更新/跳过数量、关键变化和待确认事项。只有正式执行成功并回读后才能说“已更新”；已打开的工作台自动读取共享数据，不需要修改网页源码或重新生成网站。

## 字段选择

- `tasks`：`status` 使用 `todo / in_progress / done / blocked`，`priority` 使用 `high / medium / low`；有关联时填写真实 `paperId`、`experimentId` 或 `meetingId`。
- `papers`：`status` 使用 `idea / outline / drafting / revising / submitted / accepted`；`progress` 为 0–100 的整数。章节状态为 `todo / drafting / done`，更新数组前保留未变章节。
- `projects`：整体状态为 `active / paused / completed`。单篇论文完成不等于整个博士项目完成。

写作产物和实验结果是不同交付物。避免为了让看板显得顺利而把尚未核验的实验、审稿意见处理或投稿行动标为完成。
