---
name: fundflow-investor-meeting
description: Use this skill for Stardust/FundFlow investor meeting preparation, investor style analysis, post-meeting transcript review, follow-up recommendations, and DingTalk financing-group updates. Trigger whenever the user mentions 融资会议, 投资人会议, 会前准备, 会后总结, 投资人问题, 投资人风格, 融管通, FundFlow, NDA, DataPack, 资料室, demo口径, or asks to send financing meeting insights to 融资支持群/融资群/Friday群.
---

# FundFlow Investor Meeting Workflow

This skill standardizes how to prepare for investor meetings, analyze the meeting afterward, and close the loop in FundFlow and DingTalk.

## Core Principle

Treat FundFlow / 融管通 as the financing business source of truth.

Use live FundFlow data before reconstructing status from local notes, DingTalk chat, calendar entries, or memory. Public research is supporting evidence for investor style and market context, not the source of truth for our financing stage.

## Required Tool Order

1. Read `/Users/derek/.agents/AGENT.md` first.
2. Use FundFlow MCP for financing facts:
   - `get_financing_dashboard` for overall process, risks, and active project context.
   - `search_investors` for investor profile, stage, owner, BP/NDA/DD/TS status, latest follow-up.
   - `list_recent_meetings` for meeting ids, status, timing, contact, and whether a meeting note exists.
   - `get_project_context` for recent follow-ups, stage distribution, and risk signals.
   - `get_meeting_detail` when available for one meeting's original transcript, AI note fields, and archived follow-up.
3. Use DingTalk DWS only after FundFlow:
   - Read `dws-shared` before any DWS command.
   - Read the product skill for the action: `dingtalk-chat`, `dingtalk-minutes`, `dingtalk-doc`, `dingtalk-calendar`, or `dingtalk-drive`.
   - Use `dws schema "<command>" --compact --format json` and `dws <command> --help` before writing/sending.
4. Use public web search for current investor background, portfolio, recent AI investments, and mentioned companies. Cite source links when reporting externally.
5. Use local materials only when the user points to a file, or when FundFlow lacks the needed content and local docs are clearly the relevant source.

## Fact Source Rules

- If the user says a transcript or meeting record is in 融管通, do not keep searching DingTalk minutes. Query FundFlow first.
- If FundFlow MCP returns only summaries but the UI/system is known to contain original transcript, report the MCP capability gap clearly. Do not pretend the transcript was read.
- If a capability gap blocks the work and the user asks to fix it, inspect `/Users/derek/Documents/Projects/FundFlow`, implement a narrow MCP/tooling fix, test it, push it, and state that线上部署/刷新 is still required before the live MCP can expose the new field.
- When public company/investor information may have changed, browse and use current sources.
- Separate facts from inference: say "FundFlow显示..." for system facts, "我的判断是..." for analysis.

## Meeting Prep Workflow

Use this for prompts like "帮我准备和某投资人的会议", "这个投资人现在怎么聊", or "给某基金会议建议".

1. Identify the target:
   - Investor company name.
   - Meeting time/title if provided.
   - Project, usually `B轮股权融资`.
   - Current objective, e.g. sign NDA, enter DataPack, schedule second meeting, get TS interest.
2. Pull FundFlow context:
   - Search investor by name.
   - List recent meetings filtered by investor when possible.
   - Pull project context and dashboard risks.
   - Record exact status: BP, NDA, DD, TS, investment status, latest follow-up, owner, next action.
3. Research investor:
   - Investment style: government/央国资, market-oriented VC/PE, strategic investor, industry fund, insurance/corporate investor.
   - Recent AI or enterprise software cases.
   - Their likely decision frame: financial return, policy alignment, industrial landing, security/compliance, product moat, customer quality, revenue certainty.
4. Build the meeting strategy:
   - Meeting objective: one concrete stage movement.
   - Main story: 3-5 sentences, not a full BP walkthrough.
   - Likely objections/questions.
   - Recommended answer structure.
   - Demo focus, if needed.
   - Materials to prepare.
5. Produce a concise internal prep note:
   - `当前状态`
   - `本次目标`
   - `投资人判断`
   - `建议主线`
   - `销售/收入口径`
   - `技术/产品口径`
   - `可能追问与回答`
   - `下一步动作`

## Post-Meeting Workflow

Use this for prompts like "根据会议听记总结关键点", "会后总结发群", "分析投资人问题/风格/跟进建议".

1. Locate the transcript:
   - Start with FundFlow `list_recent_meetings`.
   - Use `get_meeting_detail` by meeting id when available.
   - If no FundFlow transcript is exposed, check DingTalk minutes only if the meeting likely came from DingTalk/腾讯会议 and the user has not corrected the source to FundFlow.
   - If neither source exposes the original transcript, say exactly what was checked and ask the owner to补原文/入口. Do not write a final "based on transcript" analysis.
2. Read every available transcript/note carefully:
   - Extract investor's actual questions and wording.
   - Extract our replies by speaker when available: CEO/Derek, CFO/Shawn, product owner/ET, or others.
   - Track mentioned companies, competitors, customers, metrics, and requested materials.
3. Analyze:
   - `会议关键点位`: what moved the investor forward or blocked them.
   - `投资人核心问题`: explicit questions and implicit concerns.
   - `投资人风格`: decision frame and risk preference.
   - `我方回答质量`: what worked, what was vague, what should be tightened.
   - `后续推进`: target state, owner, deadline, next message/call/demo/material.
4. Keep the conclusion operational:
   - Which stage should FundFlow move to?
   - What material should be sent?
   - Who owns it?
   - What is the next meeting/demo objective?

## Company / Competitor Analysis

When the investor mentions companies such as 奇点智源 or 知满科技:

1. Research official/public sources.
2. Classify what kind of question the investor is really asking:
   - Security/compliance/control infrastructure.
   - Vertical AI / industry agent depth.
   - Data/model/evaluation moat.
   - Revenue quality and customer proof.
   - Differentiation from large model companies or labeling vendors.
3. Connect the company back to Stardust/Friday:
   - What the example validates.
   - What our difference is.
   - What proof we need to show.
4. Avoid broad competitor tables unless the user asks. Focus on why the investor mentioned them.

## DingTalk Group Routing

Only send when the user explicitly asks to send/update a group, or has clearly delegated that action in the current workflow.

- Financing strategy, investor logic, follow-up actions, FundFlow status: send to `融资支持群` or the named financing group.
- Demo problems, demo optimization, Friday product standard talk tracks, ET/product-owner advice: send to `Friday群`.
- If both are requested, split messages by audience. Do not send product-demo criticism to the financing group unless the user asks.
- Before sending:
  - Search/verify the target group by name unless the conversation already has a freshly verified `openConversationId`.
  - Use `dws chat message send` with a stable `--uuid`.
  - After sending, read recent group messages to verify it landed.
  - If message formatting collapses bullets, send a shorter corrected follow-up or move long content into a document.

## Message Templates

### Financing Group Update

```text
【[投资人]会议复盘｜[事实源]】

1. 当前状态
[FundFlow显示的阶段、BP/NDA/DD/TS、会议轮次、联系人、下一步]

2. 投资人核心关注
[3-5条，优先用投资人原话或接近原话]

3. 我的判断
[投资人风格、真实问题、我们应如何定位]

4. 后续动作
- [动作]：[负责人]，[时间/条件]
- [动作]：[负责人]，[时间/条件]

如果需要，我会在拿到/读完原始听记后补一版逐段复盘。
```

### Internal Meeting Prep

```text
【[投资人]会议准备】

当前状态：
[FundFlow facts]

本次目标：
[one stage movement]

建议主线：
[one paragraph]

对方可能追问：
- [question]： [answer direction]

材料/演示准备：
- [item]
```

### Transcript Gap Update

```text
【[投资人]会议听记读取进展】

刚核实：[where the transcript is expected to be]。
当前我能通过 [tool/source] 读到 [available facts]，但还没有读到 [missing field/content]。

需要补充：
1. 投资人原话问题和真实关注点。
2. 提到 [company/topic] 时的上下文。
3. 下一步材料、负责人、时间。
```

## Quality Bar

- Do not summarize a meeting as if you read the transcript unless you actually read the original transcript or full note.
- Do not let the BP narrative drown the investor's actual concerns.
- Do not use vague phrases like "继续推进" without a concrete next state and owner.
- Use exact dates and times for today's/yesterday's meetings.
- Keep group messages short enough for DingTalk. Put long analysis in a doc when needed.
- Make the output useful for a CEO/CFO/product owner to act on immediately.

