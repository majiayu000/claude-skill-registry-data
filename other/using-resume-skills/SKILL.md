---
name: using-resume-skills
description: ResumeSkills 技能路由入口——在处理任何简历、求职、面试、谈薪相关请求之前必须先调用，根据用户输入自动判断应使用哪个 ResumeSkills 技能。当请求涉及简历优化、写简历、改简历、求职信、LinkedIn、面试准备、薪资谈判、offer 比较、跳槽转行、ATS 等话题时使用本技能完成路由。
---

# 技能：using-resume-skills

本技能是 ResumeSkills 全部求职技能的**路由入口**。它的唯一职责是：根据用户的请求，快速、准确地判断出应该调用哪个（或哪几个）具体技能，然后交给对应技能执行。

<EXTREMELY-IMPORTANT>
哪怕只有 1% 的可能性某个 ResumeSkills 技能适用于用户正在做的事情，你也绝对必须路由到该技能。

如果一个技能适用于当前任务，你没有选择。你必须使用它的路由结果。

这不可协商。你不能通过合理化来逃避。
</EXTREMELY-IMPORTANT>

## 规则

**在做出任何响应或动作之前，先用下方的技能路由表完成匹配**——包括澄清性的提问、请求上传简历、或直接开始回答之前。

然后宣布「使用 [技能名] 来 [目的]」，并严格遵循该技能。如果该技能有检查清单，逐条创建待办事项。如果路由结果指向多个技能（常见于复合请求），按下方「优先级顺序」依次加载。

## 技能路由总表

如果用户的请求命中了路由表中任意一行，**必须**加载对应技能：

| 用户想要什么 | 应使用的技能（保持英文 ID） |
|------|---------|
| 过简历筛选系统（ATS）、检测 ATS 兼容性、关键词匹配分析 | **resume-ats-optimizer** |
| 优化简历经历条目（bullet points）、把平淡描述改成有亮点的成果 | **resume-bullet-writer** |
| 给简历补数字、加指标、量化成果（数字不清楚时帮你估算） | **resume-quantifier** |
| 调整简历的格式和排版、让简历更清晰易扫、ATS 友好排版 | **resume-formatter** |
| 新写/改写简历的某个板块（如项目经历、技能、自我评价） | **resume-section-builder** |
| 简历的整体综合优化（含软件开发、产品经理、技术类岗位） | **tech-resume-optimizer** |
| 高管（C 级高管、VP 总监）级别简历 | **executive-resume-writer** |
| 学术简历/CV（科研岗位、出版物、基金、教学经历） | **academic-cv-builder** |
| 创意/设计类简历（视觉设计与 ATS 兼容的平衡） | **creative-portfolio-resume** |
| 把简历投给某个具体岗位前做定制化调整 | **resume-tailor** |
| 管理多个简历版本、维护母版简历、追踪投递记录 | **resume-version-manager** |
| 管理者还没出，「我要不要投这个岗」「这个岗位我匹配度如何」 | **job-description-analyzer** |
| 写求职信（cover letter） | **cover-letter-generator** |
| 优化 LinkedIn 领英主页 | **linkedin-profile-optimizer** |
| 把简历上的条目扩写成作品集（portfolio）案例 | **portfolio-case-study-writer** |
| 整理推荐人/背调联系人列表、准备背调材料 | **reference-list-builder** |
| 帮忙批量填写岗位申请表、网申表单 | **application-form-filler** |
| 写冷邮件（cold email）：给招聘方、猎头、内推发消息 | **cold-email-writer** |
| 准备面试：STAR 故事、模拟问题、答题要点 | **interview-prep-generator** |
| 谈薪/涨薪/薪资谈判策略、反向报价话术 | **salary-negotiation-prep** |
| 比较/分析多个 offer（含总包对比） | **offer-comparison-analyzer** |
| 跨行业转行、把原行业经验翻译成目标行业的语言 | **career-changer-translator** |

## 复合请求的优先级顺序

当多个技能都适用时，按以下顺序逐个执行（前面技能的输出是后面技能的输入）：

1. **先分析，后动手**：`job-description-analyzer` 优先于 `resume-tailor`、`resume-section-builder` 等一切「改简历」类技能——你得先知道岗位要什么，才能合理定制。
2. **先条目，后格式**：`resume-bullet-writer` 与 `resume-quantifier` 优先于 `resume-formatter`——先让内容有料，再谈排版。
3. **先匹配度，后投递**：判断「该不该投」走 `job-description-analyzer` → 若决定投递，再走 `resume-tailor` → 必要时 `cover-letter-generator`。
4. **特殊人群走专属技能**：技术岗走 `tech-resume-optimizer`，高管走 `executive-resume-writer`，学术走 `academic-cv-builder`，创意/设计走 `creative-portfolio-resume`，转行走 `career-changer-translator`。这些技能与通用技能**叠加使用**，不是二选一。
5. **投递后环节独立处理**：面试（`interview-prep-generator`）、谈薪（`salary-negotiation-prep`）、offer 比较（`offer-comparison-analyzer`）按用户当前所处阶段单独触发。

示例：

- "帮我优化简历然后投这个岗" → `job-description-analyzer` →（决定投递后）`resume-tailor` →（需要的话）`cover-letter-generator`
- "我的经历有点水，帮我改一下" → `resume-bullet-writer` → `resume-quantifier`
- "我下周面试 XX 公司" → `interview-prep-generator`（若用户有简历，还可用简历生成 STAR 故事）

## 红线

出现以下念头时，说明你在合理化逃避路由——停下来，回到路由表：

| 想法 | 现实 |
|------|------|
| "这个问题很简单，不用技能" | 简单的事会变复杂。检查路由表。 |
| "用户没贴简历，先聊两句" | 就算要澄清，也要先完成路由判断。 |
| "我先直接回答，技能何必多此一举" | 行动 = 任务。先查路由表。 |
| "我记得 resume-tailor 是干嘛的" | 技能会更新。路由后加载当前版本再执行。 |
| "用户说的是'面试'而不是'简历'" | 求职话题全都在路由表里，不只是简历。 |
| "这个请求看起来和求职无关" | 只要涉及求职链路上任何一环的 1% 可能性，就该路由。 |
| "多个技能都像适用，选一个就行" | 按「优先级顺序」叠加使用，不二选一。 |

## 未命中时怎么办

如果用户的请求确实不属于上表中任何一项（例如询问这个 Skills 库本身、询问技能安装方式），则按常规划答处理即可；一旦对话中出现任何求职/简历相关的新诉求，立刻回到路由表重新匹配。

## 用户指令优先

用户指令（CLAUDE.md、AGENTS.md、直接请求等）优先于技能，技能又优先于默认行为。只有当用户明确要求你直接处理、不要调用技能时，才可以跳过路由。
