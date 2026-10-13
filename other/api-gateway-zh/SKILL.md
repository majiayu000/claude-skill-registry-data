---
name: api-gateway-zh
description: |
  连接 100+ API（Google Workspace、Microsoft 365、GitHub、Notion、Slack、Airtable、HubSpot 等），支持托管 OAuth 认证。
  当用户需要与外部服务交互时使用此技能。
  安全说明：MATON_API_KEY 仅用于 Maton.ai 身份验证，本身不授予对第三方服务的访问权限。每个服务都需要用户通过 Maton 的连接流程进行明确的 OAuth 授权。访问权限严格限制在用户已授权的连接范围内。由 Maton 提供 (https://maton.ai)。
compatibility: 需要网络访问和有效的 Maton API 密钥
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# API 网关

由 [Maton](https://maton.ai) 提供的透传代理，可通过托管 OAuth 连接直接访问第三方 API。API 网关让您可以直接调用原生 API 端点。

## 快速开始

```bash
# 原生 Slack API 调用
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456', 'text': 'Hello from gateway!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```


## 基础 URL

```
https://gateway.maton.ai/{app}/{native-api-path}
```

将 `{app}` 替换为服务名称，将 `{native-api-path}` 替换为实际的 API 端点路径。

重要提示：URL 路径必须以连接的应用名称开头（例如 `/google-mail/...`）。此前缀告诉网关使用哪个应用连接。例如，原生 Gmail API 路径以 `gmail/v1/` 开头，因此完整路径类似于 `/google-mail/gmail/v1/users/me/messages`。

## 身份验证

所有请求都需要在 Authorization 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

API 网关会自动为目标服务注入适当的 OAuth 令牌。

**环境变量：** 您可以将 API 密钥设置为 `MATON_API_KEY` 环境变量：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## 获取 API 密钥

1. 登录或在 [maton.ai](https://maton.ai) 创建账户
2. 前往 [maton.ai/settings](https://maton.ai/settings)
3. 点击 API Key 部分右侧的复制按钮进行复制

## 连接管理

连接管理使用单独的基础 URL：`https://ctrl.maton.ai`

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=slack&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**查询参数（可选）：**
- `app` - 按服务名称过滤（例如 `slack`、`hubspot`、`salesforce`）
- `status` - 按连接状态过滤（`ACTIVE`、`PENDING`、`FAILED`）

**响应：**
```json
{
  "connections": [
    {
      "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
      "status": "ACTIVE",
      "creation_time": "2025-12-08T07:20:53.488460Z",
      "last_updated_time": "2026-01-31T20:03:32.593153Z",
      "url": "https://connect.maton.ai/?session_token=5e9...",
      "app": "slack",
      "method": "OAUTH2",
      "metadata": {}
    }
  ]
}
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'slack'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**请求体：**
- `app`（必需）- 服务名称（例如 `slack`、`notion`）
- `method`（可选）- 连接方式（`API_KEY`、`BASIC`、`OAUTH1`、`OAUTH2`、`MCP`）

### 获取连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=5e9...",
    "app": "slack",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 URL 以完成 OAuth 授权。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您对同一应用有多个连接，可以通过添加带有连接 ID 的 `Maton-Connection` 头来指定使用哪个连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456', 'text': 'Hello!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，网关将使用该应用的默认（最早）活动连接。

## 支持的服务

| 服务 | 应用名称 | 代理的基础 URL |
|---------|----------|------------------|
| ActiveCampaign | `active-campaign` | `{account}.api-us1.com` |
| Acuity Scheduling | `acuity-scheduling` | `acuityscheduling.com` |
| Airtable | `airtable` | `api.airtable.com` |
| Apollo | `apollo` | `api.apollo.io` |
| Asana | `asana` | `app.asana.com` |
| Attio | `attio` | `api.attio.com` |
| Basecamp | `basecamp` | `3.basecampapi.com` |
| Baserow | `baserow` | `api.baserow.io` |
| beehiiv | `beehiiv` | `api.beehiiv.com` |
| Box | `box` | `api.box.com` |
| Brevo | `brevo` | `api.brevo.com` |
| Calendly | `calendly` | `api.calendly.com` |
| Cal.com | `cal-com` | `api.cal.com` |
| CallRail | `callrail` | `api.callrail.com` |
| Chargebee | `chargebee` | `{subdomain}.chargebee.com` |
| ClickFunnels | `clickfunnels` | `{subdomain}.myclickfunnels.com` |
| ClickSend | `clicksend` | `rest.clicksend.com` |
| ClickUp | `clickup` | `api.clickup.com` |
| Clockify | `clockify` | `api.clockify.me` |
| Coda | `coda` | `coda.io` |
| Confluence | `confluence` | `api.atlassian.com` |
| CompanyCam | `companycam` | `api.companycam.com` |
| Cognito Forms | `cognito-forms` | `www.cognitoforms.com` |
| Constant Contact | `constant-contact` | `api.cc.email` |
| Dropbox | `dropbox` | `api.dropboxapi.com` |
| Dropbox Business | `dropbox-business` | `api.dropboxapi.com` |
| ElevenLabs | `elevenlabs` | `api.elevenlabs.io` |
| Eventbrite | `eventbrite` | `www.eventbriteapi.com` |
| Fathom | `fathom` | `api.fathom.ai` |
| Firebase | `firebase` | `firebase.googleapis.com` |
| Fireflies | `fireflies` | `api.fireflies.ai` |
| GetResponse | `getresponse` | `api.getresponse.com` |
| GitHub | `github` | `api.github.com` |
| Gumroad | `gumroad` | `api.gumroad.com` |
| Granola MCP | `granola` | `mcp.granola.ai` |
| Google Ads | `google-ads` | `googleads.googleapis.com` |
| Google BigQuery | `google-bigquery` | `bigquery.googleapis.com` |
| Google Analytics Admin | `google-analytics-admin` | `analyticsadmin.googleapis.com` |
| Google Analytics Data | `google-analytics-data` | `analyticsdata.googleapis.com` |
| Google Calendar | `google-calendar` | `www.googleapis.com` |
| Google Classroom | `google-classroom` | `classroom.googleapis.com` |
| Google Contacts | `google-contacts` | `people.googleapis.com` |
| Google Docs | `google-docs` | `docs.googleapis.com` |
| Google Drive | `google-drive` | `www.googleapis.com` |
| Google Forms | `google-forms` | `forms.googleapis.com` |
| Gmail | `google-mail` | `gmail.googleapis.com` |
| Google Merchant | `google-merchant` | `merchantapi.googleapis.com` |
| Google Meet | `google-meet` | `meet.googleapis.com` |
| Google Play | `google-play` | `androidpublisher.googleapis.com` |
| Google Search Console | `google-search-console` | `www.googleapis.com` |
| Google Sheets | `google-sheets` | `sheets.googleapis.com` |
| Google Slides | `google-slides` | `slides.googleapis.com` |
| Google Tasks | `google-tasks` | `tasks.googleapis.com` |
| Google Workspace Admin | `google-workspace-admin` | `admin.googleapis.com` |
| HubSpot | `hubspot` | `api.hubapi.com` |
| Instantly | `instantly` | `api.instantly.ai` |
| Jira | `jira` | `api.atlassian.com` |
| Jobber | `jobber` | `api.getjobber.com` |
| JotForm | `jotform` | `api.jotform.com` |
| Keap | `keap` | `api.infusionsoft.com` |
| Kit | `kit` | `api.kit.com` |
| Klaviyo | `klaviyo` | `a.klaviyo.com` |
| Lemlist | `lemlist` | `api.lemlist.com` |
| Linear | `linear` | `api.linear.app` |
| LinkedIn | `linkedin` | `api.linkedin.com` |
| Mailchimp | `mailchimp` | `{dc}.api.mailchimp.com` |
| MailerLite | `mailerlite` | `connect.mailerlite.com` |
| Mailgun | `mailgun` | `api.mailgun.net` |
| ManyChat | `manychat` | `api.manychat.com` |
| Manus | `manus` | `api.manus.ai` |
| Microsoft Excel | `microsoft-excel` | `graph.microsoft.com` |
| Microsoft Teams | `microsoft-teams` | `graph.microsoft.com` |
| Microsoft To Do | `microsoft-to-do` | `graph.microsoft.com` |
| Monday.com | `monday` | `api.monday.com` |
| Motion | `motion` | `api.usemotion.com` |
| Netlify | `netlify` | `api.netlify.com` |
| Notion | `notion` | `api.notion.com` |
| Notion MCP | `notion` | `mcp.notion.com` |
| OneDrive | `one-drive` | `graph.microsoft.com` |
| Outlook | `outlook` | `graph.microsoft.com` |
| PDF.co | `pdf-co` | `api.pdf.co` |
| Pipedrive | `pipedrive` | `api.pipedrive.com` |
| Podio | `podio` | `api.podio.com` |
| PostHog | `posthog` | `{subdomain}.posthog.com` |
| QuickBooks | `quickbooks` | `quickbooks.api.intuit.com` |
| Quo | `quo` | `api.openphone.com` |
| Reducto | `reducto` | `platform.reducto.ai` |
| Salesforce | `salesforce` | `{instance}.salesforce.com` |
| Sentry | `sentry` | `{subdomain}.sentry.io` |
| SignNow | `signnow` | `api.signnow.com` |
| Slack | `slack` | `slack.com` |
| Snapchat | `snapchat` | `adsapi.snapchat.com` |
| Square | `squareup` | `connect.squareup.com` |
| Squarespace | `squarespace` | `api.squarespace.com` |
| Sunsama MCP | `sunsama` | MCP server |
| Stripe | `stripe` | `api.stripe.com` |
| Systeme.io | `systeme` | `api.systeme.io` |
| Tally | `tally` | `api.tally.so` |
| Telegram | `telegram` | `api.telegram.org` |
| TickTick | `ticktick` | `api.ticktick.com` |
| Todoist | `todoist` | `api.todoist.com` |
| Toggl Track | `toggl-track` | `api.track.toggl.com` |
| Trello | `trello` | `api.trello.com` |
| Twilio | `twilio` | `api.twilio.com` |
| Typeform | `typeform` | `api.typeform.com` |
| Unbounce | `unbounce` | `api.unbounce.com` |
| Vimeo | `vimeo` | `api.vimeo.com` |
| WhatsApp Business | `whatsapp-business` | `graph.facebook.com` |
| WooCommerce | `woocommerce` | `{store-url}/wp-json/wc/v3` |
| WordPress.com | `wordpress` | `public-api.wordpress.com` |
| Xero | `xero` | `api.xero.com` |
| YouTube | `youtube` | `www.googleapis.com` |
| Zoho Bigin | `zoho-bigin` | `www.zohoapis.com` |
| Zoho Bookings | `zoho-bookings` | `www.zohoapis.com` |
| Zoho Books | `zoho-books` | `www.zohoapis.com` |
| Zoho Calendar | `zoho-calendar` | `calendar.zoho.com` |
| Zoho CRM | `zoho-crm` | `www.zohoapis.com` |
| Zoho Inventory | `zoho-inventory` | `www.zohoapis.com` |
| Zoho Mail | `zoho-mail` | `mail.zoho.com` |
| Zoho People | `zoho-people` | `people.zoho.com` |
| Zoho Projects | `zoho-projects` | `projectsapi.zoho.com` |
| Zoho Recruit | `zoho-recruit` | `recruit.zoho.com` |

查看 [references/](references/) 获取每个提供商的详细路由指南：
- [ActiveCampaign](references/active-campaign/README.md) - 联系人、交易、标签、列表、自动化、营销活动
- [Acuity Scheduling](references/acuity-scheduling/README.md) - 预约、日历、客户、可用性
- [Airtable](references/airtable/README.md) - 记录、基地、表格
- [Apollo](references/apollo/README.md) - 人员搜索、数据增强、联系人
- [Asana](references/asana/README.md) - 任务、项目、工作区、Webhook
- [Attio](references/attio/README.md) - 人员、公司、记录、任务
- [Basecamp](references/basecamp/README.md) - 项目、待办事项、消息、日程、文档
- [Baserow](references/baserow/README.md) - 数据库行、字段、表格、批量操作
- [beehiiv](references/beehiiv/README.md) - 出版物、订阅、帖子、自定义字段
- [Box](references/box/README.md) - 文件、文件夹、协作、共享链接
- [Brevo](references/brevo/README.md) - 联系人、邮件营销、事务性邮件、模板
- [Calendly](references/calendly/README.md) - 事件类型、已安排事件、可用性、Webhook
- [Cal.com](references/cal-com/README.md) - 事件类型、预订、日程、可用时段、Webhook
- [CallRail](references/callrail/README.md) - 通话、跟踪器、公司、标签、分析
- [Chargebee](references/chargebee/README.md) - 订阅、客户、发票
- [ClickFunnels](references/clickfunnels/README.md) - 联系人、产品、订单、课程、Webhook
- [ClickSend](references/clicksend/README.md) - 短信、彩信、语音消息、联系人、列表
- [ClickUp](references/clickup/README.md) - 任务、列表、文件夹、空间、Webhook
- [Clockify](references/clockify/README.md) - 时间跟踪、项目、客户、任务、工作区
- [Coda](references/coda/README.md) - 文档、页面、表格、行、公式、控件
- [Confluence](references/confluence/README.md) - 页面、空间、博客文章、评论、附件
- [CompanyCam](references/companycam/README.md) - 项目、照片、用户、标签、组、文档
- [Cognito Forms](references/cognito-forms/README.md) - 表单、条目、文档、文件
- [Constant Contact](references/constant-contact/README.md) - 联系人、邮件营销、列表、细分
- [Dropbox](references/dropbox/README.md) - 文件、文件夹、搜索、元数据、版本、标签
- [Dropbox Business](references/dropbox-business/README.md) - 团队成员、组、团队文件夹、设备、审计日志
- [ElevenLabs](references/elevenlabs/README.md) - 文本转语音、语音克隆、音效、音频处理
- [Eventbrite](references/eventbrite/README.md) - 活动、场地、门票、订单、参与者
- [Fathom](references/fathom/README.md) - 会议录音、转录、摘要、Webhook
- [Firebase](references/firebase/README.md) - 项目、Web应用、Android应用、iOS应用、配置
- [Fireflies](references/fireflies/README.md) - 会议转录、摘要、AskFred AI、频道
- [GetResponse](references/getresponse/README.md) - 营销活动、联系人、通讯、自动回复、标签、细分
- [GitHub](references/github/README.md) - 仓库、问题、拉取请求、提交
- [Gumroad](references/gumroad/README.md) - 产品、销售、订阅者、许可证、Webhook
- [Granola MCP](references/granola-mcp/README.md) - 基于 MCP 的会议笔记、转录、查询接口
- [Google Ads](references/google-ads/README.md) - 营销活动、广告组、GAQL 查询
- [Google Analytics Admin](references/google-analytics-admin/README.md) - 报告、维度、指标
- [Google Analytics Data](references/google-analytics-data/README.md) - 报告、维度、指标
- [Google BigQuery](references/google-bigquery/README.md) - 数据集、表、作业、SQL 查询
- [Google Calendar](references/google-calendar/README.md) - 事件、日历、忙碌/空闲
- [Google Classroom](references/google-classroom/README.md) - 课程、课程作业、学生、教师、公告
- [Google Contacts](references/google-contacts/README.md) - 联系人、联系人群组、人员搜索
- [Google Docs](references/google-docs/README.md) - 文档创建、批量更新
- [Google Drive](references/google-drive/README.md) - 文件、文件夹、权限
- [Google Forms](references/google-forms/README.md) - 表单、问题、回复
- [Gmail](references/google-mail/README.md) - 邮件、会话、标签
- [Google Meet](references/google-meet/README.md) - 空间、会议记录、参与者
- [Google Merchant](references/google-merchant/README.md) - 产品、库存、促销、报告
- [Google Play](references/google-play/README.md) - 应用内产品、订阅、评论
- [Google Search Console](references/google-search-console/README.md) - 搜索分析、站点地图
- [Google Sheets](references/google-sheets/README.md) - 值、范围、格式化
- [Google Slides](references/google-slides/README.md) - 演示文稿、幻灯片、格式化
- [Google Tasks](references/google-tasks/README.md) - 任务列表、任务、子任务
- [Google Workspace Admin](references/google-workspace-admin/README.md) - 用户、组、组织单元、域、角色
- [HubSpot](references/hubspot/README.md) - 联系人、公司、交易
- [Instantly](references/instantly/README.md) - 营销活动、潜在客户、账户、邮件外联
- [Jira](references/jira/README.md) - 问题、项目、JQL 查询
- [Jobber](references/jobber/README.md) - 客户、工作、发票、报价 (GraphQL)
- [JotForm](references/jotform/README.md) - 表单、提交、Webhook
- [Keap](references/keap/README.md) - 联系人、公司、标签、任务、机会、营销活动
- [Kit](references/kit/README.md) - 订阅者、标签、表单、序列、广播
- [Klaviyo](references/klaviyo/README.md) - 配置文件、列表、营销活动、流程、事件
- [Lemlist](references/lemlist/README.md) - 营销活动、潜在客户、活动、日程、退订
- [Linear](references/linear/README.md) - 问题、项目、团队、周期 (GraphQL)
- [LinkedIn](references/linkedin/README.md) - 个人资料、帖子、分享、媒体上传
- [Mailchimp](references/mailchimp/README.md) - 受众、营销活动、模板、自动化
- [MailerLite](references/mailerlite/README.md) - 订阅者、组、营销活动、自动化、表单
- [Mailgun](references/mailgun/README.md) - 邮件发送、域、路由、模板、邮件列表、退订
- [ManyChat](references/manychat/README.md) - 订阅者、标签、流程、消息
- [Manus](references/manus/README.md) - AI 代理任务、项目、文件、Webhook
- [Microsoft Excel](references/microsoft-excel/README.md) - 工作簿、工作表、范围、表格、图表
- [Microsoft Teams](references/microsoft-teams/README.md) - 团队、频道、消息、成员、聊天
- [Microsoft To Do](references/microsoft-to-do/README.md) - 任务列表、任务、检查项、链接资源
- [Monday.com](references/monday/README.md) - 看板、项目、列、组 (GraphQL)
- [Motion](references/motion/README.md) - 任务、项目、工作区、日程
- [Netlify](references/netlify/README.md) - 站点、部署、构建、DNS、环境变量
- [Notion](references/notion/README.md) - 页面、数据库、块
- [Notion MCP](references/notion-mcp/README.md) - 基于 MCP 的页面、数据库、评论、团队、用户接口
- [OneDrive](references/one-drive/README.md) - 文件、文件夹、驱动器、共享
- [Outlook](references/outlook/README.md) - 邮件、日历、联系人
- [PDF.co](references/pdf-co/README.md) - PDF 转换、合并、拆分、编辑、文本提取、条形码
- [Pipedrive](references/pipedrive/README.md) - 交易、人员、组织、活动
- [Podio](references/podio/README.md) - 组织、工作区、应用、项目、任务、评论
- [PostHog](references/posthog/README.md) - 产品分析、功能开关、会话录制、实验、HogQL 查询
- [QuickBooks](references/quickbooks/README.md) - 客户、发票、报告
- [Quo](references/quo/README.md) - 通话、消息、联系人、对话、Webhook
- [Reducto](references/reducto/README.md) - 文档解析、提取、拆分、编辑
- [Salesforce](references/salesforce/README.md) - SOQL、sObjects、CRUD
- [SignNow](references/signnow/README.md) - 文档、模板、邀请、电子签名
- [SendGrid](references/sendgrid/README.md) - 邮件发送、联系人、模板、退订、统计
- [Sentry](references/sentry/README.md) - 问题、事件、项目、团队、发布
- [Slack](references/slack/README.md) - 消息、频道、用户
- [Snapchat](references/snapchat/README.md) - 广告账户、营销活动、广告组、广告、创意、受众
- [Square](references/squareup/README.md) - 支付、客户、订单、目录、库存、发票
- [Squarespace](references/squarespace/README.md) - 产品、库存、订单、配置文件、交易
- [Sunsama MCP](references/sunsama-mcp/README.md) - 基于 MCP 的任务、日历、积压、目标、时间跟踪接口
- [Stripe](references/stripe/README.md) - 客户、订阅、支付
- [Systeme.io](references/systeme/README.md) - 联系人、标签、课程、社区、Webhook
- [Tally](references/tally/README.md) - 表单、提交、工作区、Webhook
- [Telegram](references/telegram/README.md) - 消息、聊天、机器人、更新、投票
- [TickTick](references/ticktick/README.md) - 任务、项目、任务列表
- [Todoist](references/todoist/README.md) - 任务、项目、分区、标签、评论
- [Toggl Track](references/toggl-track/README.md) - 时间条目、项目、客户、标签、工作区
- [Trello](references/trello/README.md) - 看板、列表、卡片、检查清单
- [Twilio](references/twilio/README.md) - 短信、语音通话、电话号码、消息
- [Typeform](references/typeform/README.md) - 表单、回复、洞察
- [Unbounce](references/unbounce/README.md) - 落地页、潜在客户、账户、子账户、域
- [Vimeo](references/vimeo/README.md) - 视频、文件夹、相册、评论、点赞
- [WhatsApp Business](references/whatsapp-business/README.md) - 消息、模板、媒体
- [WooCommerce](references/woocommerce/README.md) - 产品、订单、客户、优惠券
- [WordPress.com](references/wordpress/README.md) - 帖子、页面、站点、用户、设置
- [Xero](references/xero/README.md) - 联系人、发票、报告
- [YouTube](references/youtube/README.md) - 视频、播放列表、频道、订阅
- [Zoho Bigin](references/zoho-bigin/README.md) - 联系人、公司、管道、产品
- [Zoho Bookings](references/zoho-bookings/README.md) - 预约、服务、员工、工作区
- [Zoho Books](references/zoho-books/README.md) - 发票、联系人、账单、费用
- [Zoho Calendar](references/zoho-calendar/README.md) - 日历、事件、参与者、提醒
- [Zoho CRM](references/zoho-crm/README.md) - 线索、联系人、账户、交易、搜索
- [Zoho Inventory](references/zoho-inventory/README.md) - 项目、销售订单、发票、采购订单、账单
- [Zoho Mail](references/zoho-mail/README.md) - 消息、文件夹、标签、附件
- [Zoho People](references/zoho-people/README.md) - 员工、部门、职称、考勤、请假
- [Zoho Projects](references/zoho-projects/README.md) - 项目、任务、里程碑、任务列表、评论
- [Zoho Recruit](references/zoho-recruit/README.md) - 候选人、职位、面试、申请

## 示例

### Slack - 发送消息（原生 API）

```bash
# 原生 Slack API: POST https://slack.com/api/chat.postMessage
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456', 'text': 'Hello!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json; charset=utf-8')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### HubSpot - 创建联系人（原生 API）

```bash
# 原生 HubSpot API: POST https://api.hubapi.com/crm/v3/objects/contacts
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'properties': {'email': 'john@example.com', 'firstname': 'John', 'lastname': 'Doe'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/hubspot/crm/v3/objects/contacts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Google Sheets - 获取电子表格值（原生 API）

```bash
# 原生 Sheets API: GET https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{range}
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-sheets/v4/spreadsheets/122BS1sFN2RKL8AOUQjkLdubzOwgqzPT64KfZ2rvYI4M/values/Sheet1!A1:B2')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Salesforce - SOQL 查询（原生 API）

```bash
# 原生 Salesforce API: GET https://{instance}.salesforce.com/services/data/v64.0/query?q=...
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/salesforce/services/data/v64.0/query?q=SELECT+Id,Name+FROM+Contact+LIMIT+10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Airtable - 列出表格（原生 API）

```bash
# 原生 Airtable API: GET https://api.airtable.com/v0/meta/bases/{id}/tables
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/airtable/v0/meta/bases/appgqan2NzWGP5sBK/tables')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Notion - 查询数据库（原生 API）

```bash
# 原生 Notion API: POST https://api.notion.com/v1/data_sources/{id}/query
python <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/notion/v1/data_sources/23702dc5-9a3b-8001-9e1c-000b5af0a980/query', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Notion-Version', '2025-09-03')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Stripe - 列出客户（原生 API）

```bash
# 原生 Stripe API: GET https://api.stripe.com/v1/customers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/stripe/v1/customers?limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 代码示例

### JavaScript (Node.js)

```javascript
const response = await fetch('https://gateway.maton.ai/slack/api/chat.postMessage', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  },
  body: JSON.stringify({ channel: 'C0123456', text: 'Hello!' })
});
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/slack/api/chat.postMessage',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'channel': 'C0123456', 'text': 'Hello!'}
)
```

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 缺少请求应用的连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 限流（每账户每秒 10 个请求） |
| 500 | 内部服务器错误 |
| 4xx/5xx | 来自目标 API 的透传错误 |

来自目标 API 的错误会以其原始状态码和响应体透传。

### 故障排除：API 密钥问题

1. 检查 `MATON_API_KEY` 环境变量是否已设置：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：无效的应用名称

1. 验证您的 URL 路径以正确的应用名称开头。路径必须以 `/google-mail/` 开头。例如：

- 正确：`https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages`
- 错误：`https://gateway.maton.ai/gmail/v1/users/me/messages`

2. 确保您有该应用的活动连接。列出您的连接以验证：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：服务器错误

500 错误可能表示 OAuth 令牌已过期。尝试通过上面的连接管理部分创建新连接并完成 OAuth 授权。如果新连接状态为 "ACTIVE"，请删除旧连接以确保网关使用新连接。

## 速率限制

- 每账户每秒 10 个请求
- 目标 API 的速率限制同样适用

## 注意事项

- 使用 curl 处理包含括号的 URL（`fields[]`、`sort[]`、`records[]`）时，请使用 `-g` 标志禁用 glob 解析
- 将 curl 输出管道到 `jq` 时，环境变量可能在某些 shell 中无法正确展开，这可能导致"Invalid API key"错误

## 提示

1. **使用原生 API 文档**：参考每个服务的官方 API 文档了解端点路径和参数。

2. **请求头会被转发**：自定义请求头（除了 `Host` 和 `Authorization`）会被转发到目标 API。

3. **查询参数有效**：URL 查询参数会被透传到目标 API。

4. **支持所有 HTTP 方法**：GET、POST、PUT、PATCH、DELETE 均受支持。

5. **QuickBooks 特殊情况**：在路径中使用 `:realmId`，它将被替换为已连接的 realm ID。

## 可选资源

- [Github](https://github.com/maton-ai/api-gateway-skill)
- [API 参考](https://www.maton.ai/docs/api-reference)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)
