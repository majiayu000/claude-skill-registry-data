---
name: ielts-buddy
description: 连接 IELTS Buddy 账号、查询课程和真实学习记录、分析学习快照，或按用户要求保存待办、词书与口语素材时使用。只需处理用户已提供材料的学习任务无需连接。
---

# 连接 IELTS Buddy 学习数据

使用用户当前任务所需的最少数据。HTTP 接入的实时事实源是 [Agent 接入说明](https://ieltsbuddy.igopx.cn/developers/api/agent.md)，逐接口参数以运行环境返回的文档为准，不猜测操作名或调用站内私有接口。

## 连接与调用

1. 已有授权时复用凭据，先通过 `GET /api/v1/agent/me` 核对账号、有效期和 scopes。没有授权且任务需要个人数据时，在本 Skill 根目录运行 `python3 scripts/ielts_buddy_api.py bind`，仅将返回的绑定链接交给用户确认；不要代替用户确认或索要密码、Cookie。
2. 运行 `python3 scripts/ielts_buddy_api.py capabilities`，再 GET 所需 `/capabilities/<operation>.md` 阅读请求、权限与响应。也可直接使用 Agent 自带 HTTP 能力。
3. 使用 `python3 scripts/ielts_buddy_api.py call <operation> --json '<JSON>'`。长请求使用 `--json -` 从标准输入读取。执行时将脚本路径解析为本 Skill 安装目录下的绝对路径。
4. 检查 HTTP 与业务 code；写入成功后引用返回的 id 和事实，必要时读回。401 重新绑定；403 核对 scopes，不能通过网页 Cookie 绕过权限。已有绑定不代表用户授权发送反馈或进行无关写入。

## 按任务取数

- 跨模块学习分析：优先 [学习快照与证据](references/learning-data.md)，读取快照目录后在本地查询需要的记录，不打印整包。
- 查最近一次练习、模考科目或精听结果：使用 [复盘记录](references/review-records.md)，先列表再详情；只查统计时使用足迹 summary，不累加分页行数。
- 查课程、题目、资料：从当前 capability 目录选择，复用服务端返回的精确 id、contentRef 和链接。正式作答、播放、看课、交卷由用户在网页完成。
- 保存学习安排：`ielts_study_todos_create/update`，日期、时间和内容关联均按当前契约；明确要求安排时直接执行，讨论建议时不写。打开链接不等于完成待办。
- 保存词句：`ielts_vocabulary_add`，由调用方提供释义，保存不代表网站产生复习成绩。
- 保存口语素材：只提交标题和真实经历，不保存题目覆盖映射。
- 用户明确要求发送产品反馈时才用 `ielts_feedback_create`；响应不确定先读取 `ielts_feedback_list` 核对，不能盲目重发。

教学判断在调用方完成。站内文档创作、实时语音等未列入公开契约的功能，不作为本 Skill 能力。后台题库研究需要独立 Operator 权限与工具，用户 Token 不可代替 Operator Token。
