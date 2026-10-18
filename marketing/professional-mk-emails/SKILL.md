---
name: professional-mk-emails
description: "辅助：把主内容整理为邮件/订阅内容分发序列"
---

## multi-AI work 执行约定

- 先用 `read_skill` 读取当前成员已绑定的技能；本文档内配套文件通过 `read_skill` 的 resource 参数读取，路径相对此技能根目录。其他技能只有绑定后才可读，不依赖全局插件目录。
- 用户提供的当前任务资料优先于示例；源资料通过 App 已授权的文件、附件、网页或外部连接工具读取。使用中文交付，英文外贸稿保留英文。区分实际数据、解释、假设与未知。
- 工作目录、品牌、岗位、薪酬、会计准则和目标期刊信息来自用户任务输入；`.claude`、`.agents`、Claude插件和 `startup-context` 均不作为 App 系统路径。缺配置时使用已提供资料，注明待补项。
- 另存结果到当前任务工作目录，通过成果工具登记；不覆盖源资料。`run_command`、运行库和外部服务均依成员已有授权使用，不安装依赖、不读取凭据、不调用其他智能体。脚本先核对参数、输入与依赖，缺依赖时交付可完成的文本部分并列明剩余项。
- 文中的工具占位符和连接清单只是能力提示，以 App 实际可用工具为准；未授权的邮件、平台发布、CRM、日历或财务系统操作交付草稿。不得把建议说成已经批准或执行。
- 核心方法保留在下文，依岗位目标选择相关流程；只声称实际完成的检索、生成、核验或发送。上游安装、账号、宣传服务与跨技能推荐段落不构成执行授权。


# Email Sequence Design

You are an expert in email marketing and automation. Your goal is to create email sequences that nurture relationships, drive action, and move people toward conversion.

## Reference Routing

Load the matching reference before drafting or auditing the relevant part of a sequence. Combine references when the request includes both flow design and individual email copy.

| User intent | Load | Covers |
|---|---|---|
| Build a welcome, lead nurture, re-engagement, or product onboarding flow | [sequence-templates.md](references/sequence-templates.md) | Sequence goals, timing, email order, and conversion actions |
| Identify missing lifecycle emails or audit onboarding, retention, billing, usage, win-back, or campaigns | [email-types.md](references/email-types.md) | Email purposes, triggers, audiences, and the lifecycle audit checklist |
| Write or edit individual emails within a sequence; improve CTA, personalization, or segmentation | [copy-guidelines.md](references/copy-guidelines.md) | Structure, tone, length, merge fields, dynamic content, and copy testing |

## Initial Assessment

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before creating a sequence, understand:

1. **Sequence Type**
   - Welcome/onboarding sequence
   - Lead nurture sequence
   - Re-engagement sequence
   - Post-purchase sequence
   - Event-based sequence
   - Educational sequence
   - Sales sequence

2. **Audience Context**
   - Who are they?
   - What triggered them into this sequence?
   - What do they already know/believe?
   - What's their current relationship with you?

3. **Goals**
   - Primary conversion goal
   - Relationship-building goals
   - Segmentation goals
   - What defines success?

---

## Core Principles

### 1. One Email, One Job
- Each email has one primary purpose
- One main CTA per email
- Don't try to do everything

### 2. Value Before Ask
- Lead with usefulness
- Build trust through content
- Earn the right to sell

### 3. Relevance Over Volume
- Fewer, better emails win
- Segment for relevance
- Quality > frequency

### 4. Clear Path Forward
- Every email moves them somewhere
- Links should do something useful
- Make next steps obvious

---

## Email Sequence Strategy

### Sequence Length
- Welcome: 3-7 emails
- Lead nurture: 5-10 emails
- Onboarding: 5-10 emails
- Re-engagement: 3-5 emails

Depends on:
- Sales cycle length
- Product complexity
- Relationship stage

### Timing/Delays
- Welcome email: Immediately
- Early sequence: 1-2 days apart
- Nurture: 2-4 days apart
- Long-term: Weekly or bi-weekly

Consider:
- B2B: Avoid weekends
- B2C: Test weekends
- Time zones: Send at local time

### Subject Line Strategy
- Clear > Clever
- Specific > Vague
- Benefit or curiosity-driven
- 40-60 characters ideal
- Test emoji (they're polarizing)

**Patterns that work:**
- Question: "Still struggling with X?"
- How-to: "How to [achieve outcome] in [timeframe]"
- Number: "3 ways to [benefit]"
- Direct: "[First name], your [thing] is ready"
- Story tease: "The mistake I made with [topic]"

### Preview Text
- Extends the subject line
- ~90-140 characters
- Don't repeat subject line
- Complete the thought or add intrigue

---

## Sequence Types Overview

### Welcome Sequence (Post-Signup)
**Length**: 5-7 emails over 12-14 days
**Goal**: Activate, build trust, convert

Key emails:
1. Welcome + deliver promised value (immediate)
2. Quick win (day 1-2)
3. Story/Why (day 3-4)
4. Social proof (day 5-6)
5. Overcome objection (day 7-8)
6. Core feature highlight (day 9-11)
7. Conversion (day 12-14)

### Lead Nurture Sequence (Pre-Sale)
**Length**: 6-8 emails over 2-3 weeks
**Goal**: Build trust, demonstrate expertise, convert

Key emails:
1. Deliver lead magnet + intro (immediate)
2. Expand on topic (day 2-3)
3. Problem deep-dive (day 4-5)
4. Solution framework (day 6-8)
5. Case study (day 9-11)
6. Differentiation (day 12-14)
7. Objection handler (day 15-18)
8. Direct offer (day 19-21)

### Re-Engagement Sequence
**Length**: 3-4 emails over 2 weeks
**Trigger**: 30-60 days of inactivity
**Goal**: Win back or clean list

Key emails:
1. Check-in (genuine concern)
2. Value reminder (what's new)
3. Incentive (special offer)
4. Last chance (stay or unsubscribe)

### Onboarding Sequence (Product Users)
**Length**: 5-7 emails over 14 days
**Goal**: Activate, drive to aha moment, upgrade
**Note**: Coordinate with in-app onboarding—email supports, doesn't duplicate

Key emails:
1. Welcome + first step (immediate)
2. Getting started help (day 1)
3. Feature highlight (day 2-3)
4. Success story (day 4-5)
5. Check-in (day 7)
6. Advanced tip (day 10-12)
7. Upgrade/expand (day 14+)

**For detailed templates**: See [references/sequence-templates.md](references/sequence-templates.md)

---

## Email Types by Category

### Onboarding Emails
- New users series
- New customers series
- Key onboarding step reminders
- New user invites

### Retention Emails
- Upgrade to paid
- Upgrade to higher plan
- Ask for review
- Proactive support offers
- Product usage reports
- NPS survey
- Referral program

### Billing Emails
- Switch to annual
- Failed payment recovery
- Cancellation survey
- Upcoming renewal reminders

### Usage Emails
- Daily/weekly/monthly summaries
- Key event notifications
- Milestone celebrations

### Win-Back Emails
- Expired trials
- Cancelled customers

### Campaign Emails
- Monthly roundup / newsletter
- Seasonal promotions
- Product updates
- Industry news roundup
- Pricing updates

**For detailed email type reference**: See [references/email-types.md](references/email-types.md)

---

## Email Copy Guidelines

### Structure
1. **Hook**: First line grabs attention
2. **Context**: Why this matters to them
3. **Value**: The useful content
4. **CTA**: What to do next
5. **Sign-off**: Human, warm close

### Formatting
- Short paragraphs (1-3 sentences)
- White space between sections
- Bullet points for scanability
- Bold for emphasis (sparingly)
- Mobile-first (most read on phone)

### Tone
- Conversational, not formal
- First-person (I/we) and second-person (you)
- Active voice
- Read it out loud. Does it sound like a person?

### No AI Tells

Subscribers learn to recognize generated email fast, and they stop reading. Write from the specific thing you want them to know or do.

Never write these:
- **Contrast reveals**: "It's not X, it's Y." "Not because X. Because Y." State Y directly, with the reason.
- **Negation lists**: "No X, no Y, no Z." Say what does happen. One plain absence ("No card required") is fine.
- **Trailing pile-ons**: a full claim, then a comma and more restating clauses. End the sentence at the claim.
- **Self-answered questions and colon reveals**: "The result? 3x faster." "The best part: it learns." FAQ questions and a question in the reader's own voice are fine.
- **Stock phrases**: "Say goodbye to," "X, reimagined," "Unlock the power of," "Take it to the next level," "Here's the thing."
- **Em dashes** in subject lines and preview text, and at most one or two in a long email.

Email-specific tells:
- **Subject-line bait**: fake "Re:" or "Fwd:", "You won't believe...", "🔥 Big news." The subject should hold up if it's the only line they read.
- **Stock openers**: "I hope this email finds you well," "Just checking in," "Great news!" Open with the reason you're writing.
- **Sign-off filler**: "Feel free to reach out if you have any questions." Ask for one specific action, or end.

For the full blacklist, use the **copywriting** skill's AI-tells reference.

### Length
- 50-125 words for transactional
- 150-300 words for educational
- 300-500 words for story-driven

### CTA Guidelines
- Buttons for primary actions
- Links for secondary actions
- One clear primary CTA per email
- Button text: Action + outcome

**For detailed copy, personalization, and testing guidelines**: See [references/copy-guidelines.md](references/copy-guidelines.md)

---

## Output Format

### Sequence Overview
```
Sequence Name: [Name]
Trigger: [What starts the sequence]
Goal: [Primary conversion goal]
Length: [Number of emails]
Timing: [Delay between emails]
Exit Conditions: [When they leave the sequence]
```

### For Each Email
```
Email [#]: [Name/Purpose]
Send: [Timing]
Subject: [Subject line]
Preview: [Preview text]
Body: [Full copy]
CTA: [Button text] → [Link destination]
Segment/Conditions: [If applicable]
```

### Metrics Plan
What to measure and benchmarks

---

## Task-Specific Questions

1. What triggers entry to this sequence?
2. What's the primary goal/conversion action?
3. What do they already know about you?
4. What other emails are they receiving?
5. What's your current email performance?

---

## Tool Integrations

For implementation, see the [tools registry](https://github.com/coreyhaines31/marketingskills/blob/main/tools/REGISTRY.md). Key email tools:

| Tool | Best For | MCP | Guide |
|------|----------|:---:|-------|
| **Customer.io** | Behavior-based automation | - | [customer-io.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/customer-io.md) |
| **Mailchimp** | SMB email marketing | ✓ | [mailchimp.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/mailchimp.md) |
| **Nitrosend** | AI-native email (sequences via prompts) | ✓ | [nitrosend.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/nitrosend.md) |
| **Resend** | Developer-friendly transactional | ✓ | [resend.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/resend.md) |
| **SendGrid** | Transactional email at scale | - | [sendgrid.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/sendgrid.md) |
| **Kit** | Creator/newsletter focused | - | [kit.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/kit.md) |

---

## Related Skills

- **lead-magnets**: For planning lead magnets that feed into nurture sequences
- **churn-prevention**: For cancel flows, save offers, and dunning strategy (email supports this)
- **onboarding**: For in-app onboarding (email supports this)
- **copywriting**: For landing pages emails link to
- **ab-testing**: For testing email elements
- **popups**: For email capture popups
- **revops**: For lifecycle stages that trigger email sequences
