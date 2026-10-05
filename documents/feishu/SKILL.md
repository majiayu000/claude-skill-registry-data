---
name: feishu
description: >
  飞书全能力 Skill：文档读写、IM 消息（文本/富文本/卡片）、用户搜索、评论、权限管理、文件操作。
  Triggers: '飞书', '飞书文档', '写文档', '搜文档', '发消息', '发卡片', 'feishu', 'lark',
  '创建文档', '读取文档', '飞书评论', '飞书用户', '连飞书', '配置飞书', 'connect feishu',
  '飞书卡片', '飞书消息', 'interactive card'
slug: feishu
version: 1.0.0
displayName: 飞书集成（Feishu Integration）
summary: 飞书全能力 Skill，涵盖文档读写（MCP）、IM 消息发送（文本/富文本/卡片）、用户搜索、评论、权限管理，含鉴权配置、踩坑经验和 Python 工具模板。
tags: feishu, lark, im, document, mcp, integration
---

# 飞书 Skill (Feishu / Lark)

飞书全能力集成：文档操作（通过 MCP 工具）+ IM 消息发送（通过 REST API）+ 权限管理。

---

## 目录

1. [鉴权机制](#鉴权机制)
2. [配置指南（首次连接）](#配置指南)
3. [MCP 工具（文档/搜索/用户/评论/文件）](#mcp-工具)
4. [IM 消息 API（文本/富文本/卡片）](#im-消息-api)
5. [权限管理 API](#权限管理-api)
6. [典型工作流](#典型工作流)
7. [踩坑经验 & 注意事项](#踩坑经验)

---

## 鉴权机制

飞书 API 有两种鉴权方式，所有 API 调用都需要先获取 token。

### Tenant Access Token (TAT) — 应用身份

**适用：** 大部分场景（创建文档、发消息、管理权限、搜索用户）

```
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
Content-Type: application/json

{
  "app_id": "<APP_ID>",
  "app_secret": "<APP_SECRET>"
}
```

**响应：**
```json
{
  "code": 0,
  "tenant_access_token": "t-xxxxxxxx",
  "expire": 7200
}
```

- Token 有效期 2 小时，过期需重新获取
- 后续所有 API 请求头：`Authorization: Bearer <token>`

### User Access Token (UAT) — 用户身份

**适用：** 搜索用户个人文档、以用户身份操作

引导用户在浏览器中打开授权页面：
```
https://feishu-mcp.nodesk.tech/auth/feishu?app_id=<APP_ID>&app_secret=<APP_SECRET>
```

授权后获得 `user_id`，在 MCP server headers 中添加 `X-Feishu-User-Id`。

### 凭据获取

appId 和 appSecret 来自 config.json 的 `channels.feishu` 配置：
```python
# 读取方式
config = mcp_deskclaw_get_config(section="channels")
app_id = config["channels"]["feishu"]["appId"]
app_secret = config["channels"]["feishu"]["appSecret"]
```

---

## 配置指南

当用户说"帮我连飞书"或提供了 appId / appSecret 时，需要配置两部分。

### 1. 配置 IM 通道

```python
mcp_deskclaw_update_config(
    path="channels.feishu",
    value='{"enabled":true,"appId":"<APP_ID>","appSecret":"<APP_SECRET>","allowFrom":["*"],"groupPolicy":"mention"}'
)
```

### 2. 配置 MCP 文档工具

```python
mcp_deskclaw_mcp_server_add(
    name="feishu",
    url="https://feishu-mcp.nodesk.tech/mcp",
    headers='{"X-Feishu-App-Id":"<APP_ID>","X-Feishu-App-Secret":"<APP_SECRET>"}'
)
```

两者使用同一套 appId / appSecret，但走不同通道。

### 3. 重启生效

```python
mcp_deskclaw_restart_gateway()
```

### 检查现有配置

```python
mcp_deskclaw_get_config(section="channels")   # 查看 IM 通道
mcp_deskclaw_mcp_server_list()                 # 查看 MCP 服务器
```

---

## MCP 工具

配置完成后，以下 MCP 工具自动注册，直接调用即可。

### 文档操作

| 工具名 | 用途 | 典型场景 |
|--------|------|----------|
| `mcp_feishu_create-doc` | 创建新文档（支持 Markdown） | "帮我创建一篇飞书文档" |
| `mcp_feishu_fetch-doc` | 获取文档内容 | "读一下这个文档" |
| `mcp_feishu_update-doc` | 更新文档（7种模式：overwrite/append/replace_range/replace_all/insert_before/insert_after/delete_range） | "把这些内容写到文档里" |
| `mcp_feishu_list-docs` | 列出知识库子文档 | "这个知识库下有哪些文档" |
| `mcp_feishu_search-doc` | 搜索文档 | "搜一下关于 XX 的文档" |

### 用户操作

| 工具名 | 用途 |
|--------|------|
| `mcp_feishu_search-user` | 按用户名搜索（结果按亲密度排序） |
| `mcp_feishu_get-user` | 获取用户详细信息（不传 open_id 则获取自己） |

### 评论操作

| 工具名 | 用途 |
|--------|------|
| `mcp_feishu_get-comments` | 获取文档评论（支持全文/划词/全部筛选） |
| `mcp_feishu_add-comments` | 添加全文评论（支持文本 + @用户 + 超链接） |

### 文件操作

| 工具名 | 用途 |
|--------|------|
| `mcp_feishu_fetch-file` | 获取文件/图片/画板的 Base64 内容 |

---

## IM 消息 API

MCP 工具不覆盖 IM 消息发送，需要通过 `exec` 工具直接调用飞书 REST API。

### API 基础信息

| 项目 | 值 |
|------|-----|
| 基础 URL | `https://open.feishu.cn/open-apis` |
| 发送消息 | `POST /im/v1/messages?receive_id_type=open_id` |
| 回复消息 | `POST /im/v1/messages/{message_id}/reply` |
| 鉴权 | `Authorization: Bearer <tenant_access_token>` |

### 发送文本消息

```python
import urllib.request, json, ssl
ctx = ssl.create_default_context()

# 获取 token（见鉴权机制章节）
token = get_tenant_access_token(app_id, app_secret)

data = json.dumps({
    "receive_id": "<用户 open_id>",
    "msg_type": "text",
    "content": json.dumps({"text": "你好！"})
}).encode()

req = urllib.request.Request(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    data=data,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    },
    method="POST"
)
with urllib.request.urlopen(req, context=ctx) as resp:
    result = json.loads(resp.read())
```

### 发送富文本消息 (post)

```python
content = {
    "zh_cn": {
        "title": "消息标题",
        "content": [
            [
                {"tag": "text", "text": "普通文本 "},
                {"tag": "a", "text": "链接文字", "href": "https://example.com"},
                {"tag": "at", "user_id": "ou_xxx", "user_name": "张三"}
            ],
            [
                {"tag": "text", "text": "第二行内容"}
            ]
        ]
    }
}

data = json.dumps({
    "receive_id": "<open_id>",
    "msg_type": "post",
    "content": json.dumps(content)
}).encode()
```

**富文本元素类型：**

| tag | 用途 | 必填字段 |
|-----|------|---------|
| `text` | 纯文本 | `text` |
| `a` | 超链接 | `text`, `href` |
| `at` | @用户 | `user_id`（open_id 格式） |
| `img` | 图片 | `image_key`（需先上传） |

### 发送交互卡片 (interactive)

卡片是飞书最强大的消息类型，支持标题、分栏、按钮、表单等。

```python
card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "卡片标题"},
        "template": "blue"  # 颜色主题
    },
    "elements": [
        # 文本块（支持 lark_md 语法）
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**加粗** 普通文本 [链接](url)"}
        },
        # 分割线
        {"tag": "hr"},
        # 按钮组
        {
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "按钮文字"},
                    "url": "https://example.com",   # 点击跳转
                    "type": "primary"                # primary / default / danger
                }
            ]
        }
    ]
}

data = json.dumps({
    "receive_id": "<open_id>",
    "msg_type": "interactive",
    "content": json.dumps(card)
}).encode()
```

**卡片 header template 颜色：**
`blue`, `wathet`, `turquoise`, `green`, `yellow`, `orange`, `red`, `carmine`, `violet`, `purple`, `indigo`, `grey`

**卡片 elements 类型：**

| tag | 用途 | 说明 |
|-----|------|------|
| `div` | 文本块 | `text.tag` 可选 `plain_text` 或 `lark_md` |
| `hr` | 分割线 | 无额外字段 |
| `action` | 按钮组 | `actions` 数组，每个 button 可带 `url` 或 `value` |
| `note` | 备注 | 灰色小字，`elements` 数组 |
| `img` | 图片 | 需要 `img_key` |
| `column_set` | 多列布局 | `columns` 数组 |

**lark_md 语法（卡片内）：**
- `**加粗**`、`*斜体*`、`~~删除线~~`、`[链接](url)`
- `<at id=ou_xxx></at>` — @用户
- 不支持标准 Markdown 标题（#），用 div 的 text 模拟

### receive_id 类型

发消息时 URL 参数 `receive_id_type` 决定 `receive_id` 的含义：

| receive_id_type | receive_id 格式 | 说明 |
|-----------------|----------------|------|
| `open_id` | `ou_xxxxxxx` | 用户 open_id（推荐） |
| `chat_id` | `oc_xxxxxxx` | 群聊 ID |
| `union_id` | `on_xxxxxxx` | 跨应用用户 ID |
| `email` | `user@example.com` | 用户邮箱 |

---

## 权限管理 API

机器人创建的文档默认只有机器人自己能访问，**必须主动授权给用户**。

### 添加协作者

```
POST https://open.feishu.cn/open-apis/drive/v1/permissions/{token}/members?type=docx
Authorization: Bearer <tenant_access_token>

{
    "member_type": "openid",
    "member_id": "<用户 open_id>",
    "perm": "full_access"
}
```

**权限级别 (perm)：**

| 值 | 说明 |
|----|------|
| `view` | 只读 |
| `edit` | 可编辑 |
| `full_access` | 完全控制（含分享、删除权限） |

**member_type 类型：**

| 值 | 说明 |
|----|------|
| `openid` | 用户 open_id |
| `openchat` | 群组 chat_id |
| `department` | 部门 ID |
| `tenant` | 整个租户 |

### 查看当前协作者

```
GET https://open.feishu.cn/open-apis/drive/v1/permissions/{token}/members?type=docx
```

### 设置公开访问（租户内可读）

如果希望同租户所有人可访问，可以在创建文档时使用 MCP 工具的参数，或者调用权限 API 添加 `member_type: "tenant"` 的权限。

### ⚠️ 重要：创建文档后必须设权限

机器人用 TAT 创建的文档，用户默认无法访问。每次创建文档后必须：
1. 调用权限 API 给用户添加 `full_access`
2. 或者使用 MCP 工具 `mcp_feishu_create-doc` 时指定权限参数

---

## 典型工作流

### 写日记 / 日报 / 周报

```
1. mcp_feishu_create-doc → 创建文档（Markdown 直接写入）
2. 在回复中告知用户：文档写好了！🔗 https://bytedance.feishu.cn/docx/{document_id}
```

> ⚠️ 在飞书私聊中，**不要用 `message()` 工具单独发链接**！会触发 `_sent_in_turn` 机制导致正常 response 被跳过。把链接写在回复文本中。

### 发送卡片通知

```
1. 从 config 读取 appId / appSecret
2. 获取 tenant_access_token
3. 构造卡片 JSON
4. POST /im/v1/messages 发送
```

### 搜索并汇总文档

```
1. mcp_feishu_search-doc → 搜索关键词
2. mcp_feishu_fetch-doc → 读取相关文档
3. 在回复中汇总信息并附上文档链接
```

### 首次连接飞书

```
用户提供 appId + appSecret
  ↓
1. mcp_deskclaw_update_config → 写入 channels.feishu
2. mcp_deskclaw_mcp_server_add → 添加飞书 MCP
3. mcp_deskclaw_restart_gateway → 重启生效
```

---

## 踩坑经验

### 1. Python 环境可能没有 requests

DeskClaw 的 Python 环境不一定有 `requests` 库。调 REST API 时用标准库：

```python
import urllib.request, urllib.error, json, ssl
ctx = ssl.create_default_context()
```

### 2. 文档 Block API 的 block_type 与 key 必须严格对应

如果直接调用飞书 docx block API（而非 MCP），block_type 数值和 JSON key 的对应关系：

| block_type | JSON key | 说明 |
|-----------|----------|------|
| 1 | page | 页面根节点（不可创建） |
| 2 | text | 普通文本 |
| 3 | heading1 | 一级标题 |
| 4 | heading2 | 二级标题 |
| 5 | heading3 | 三级标题 |
| 6 | heading4 | 四级标题 |
| 7 | heading5 | 五级标题 |
| 8 | heading6 | 六级标题 |
| 9 | heading7 | 七级标题 |
| 10 | heading8 | 八级标题 |
| 11 | heading9 | 九级标题 |
| 12 | bullet | 无序列表 |
| 13 | ordered | 有序列表 |
| 14 | code | 代码块 |
| 15 | quote | 引用 |
| 17 | todo | 待办事项 |
| 22 | divider | 分割线（空对象 `{}` 即可） |

**block_type 和 key 不匹配会返回 400 invalid param**，错误信息不会告诉你具体哪里错了。

### 3. 优先用 MCP 工具写文档

MCP 工具 `mcp_feishu_create-doc` 和 `mcp_feishu_update-doc` 支持 Markdown 直接写入，自动处理 block 转换，比手动拼 block JSON 可靠得多。只有 MCP 不支持的操作才需要直接调 REST API。

### 4. 卡片消息的 content 是双重 JSON

发送卡片时，外层 `content` 字段的值是**字符串化的 JSON**，不是直接嵌套：

```python
# ✅ 正确
"content": json.dumps(card)

# ❌ 错误
"content": card
```

### 5. 群聊 @mention 过滤

配置 `groupPolicy: "mention"` 后，需要在 feishu channel 代码中实现过滤逻辑：
- 群聊消息的 `event.message.mentions` 数组包含被 @ 的用户列表
- 每个 mention 有 `id.open_id`、`name` 等字段
- 精确匹配：用机器人自己的 open_id（通过 `GET /bot/v3/info` 获取）

### 6. 飞书服务器地址

| 用途 | 域名 | 说明 |
|------|------|------|
| API 调用 | `open.feishu.cn` | 所有 REST API |
| WebSocket 长连接 | `lark-pushsdkws.feishu.cn` | IM 消息推送 |
| MCP 代理 | `feishu-mcp.nodesk.tech` | 文档 MCP 工具 |

---

## 与飞书 IM 通道的关系

| 功能 | 谁负责 | 走什么通道 |
|------|--------|-----------|
| 收飞书私聊/群聊消息 | feishu channel (gateway) | WebSocket 长连接 |
| 回复飞书消息 | feishu channel (gateway) | 自动通过 gateway 回复 |
| 主动发消息/卡片 | 本 skill (exec + REST API) | HTTPS → open.feishu.cn |
| 文档/搜索/用户/评论 | 本 skill (MCP 工具) | HTTPS → feishu-mcp.nodesk.tech |

两者共用同一套 appId / appSecret，但走不同通道。配置飞书时必须同时配置两者。

---

## 完整 Python 工具函数模板

参考 [references/python-template.md](references/python-template.md)，可直接在 `exec` 中复制使用。
