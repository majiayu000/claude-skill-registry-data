---
name: send-file
description: 发送文件到消息平台。触发词：发送文件、发送文档、发送截图、传文件、发文件。支持飞书等平台，内容优先级：生成的文档 > 本地文件 > 截图。
---

# Send File

## Overview

将文件发送到消息平台（飞书、Telegram、Discord 等）。

**内容来源优先级（用户未指定时）：**
1. 🥇 **生成的文档** - 刚刚由代码/工具生成的文件（报告、导出数据等）
2. 🥈 **本地文件** - 用户机器上已存在的文件
3. 🥉 **截图** - 屏幕截图或图片

## 配置（必须）

使用前需要配置飞书应用凭证：

```bash
# 临时配置（当前终端）
export FEISHU_APP_ID='cli_xxx'
export FEISHU_APP_SECRET='xxx'

# 永久配置（添加到 ~/.zshrc 或 ~/.bashrc）
echo "export FEISHU_APP_ID='cli_xxx'" >> ~/.zshrc
echo "export FEISHU_APP_SECRET='xxx'" >> ~/.zshrc
source ~/.zshrc
```

**获取飞书应用凭证：**
1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 创建或选择应用
3. 在「凭证与基础信息」中获取 App ID 和 App Secret
4. 确保应用有 `im:message` 和 `im:resource` 权限

## Quick Start

用户请求发送文件时：

```
用户: 把这个文件发到飞书
用户: 发送 /path/to/file.pdf 给我
用户: 把刚才生成的报告发给我
```

**重要：飞书文件发送必须用 Python 脚本**

⚠️ OpenClaw 的 `message` tool 无法直接发送本地文件（只能发链接）。

**正确做法：直接执行 Python 脚本**

```bash
python ~/.openclaw/skills/send-file/scripts/send_feishu_file.py <file_path> <open_id>
```

**执行时机：**
- 用户说"发文件"、"发送xxx"、"把xxx发给我"时
- 当前在飞书对话中，自动推断 open_id
- 直接用 exec 调用脚本，不要用 message tool 的 filePath 参数

## Platform Support

| 平台 | 状态 | 说明 |
|------|------|------|
| 飞书 | ✅ 支持 | 使用 `message` tool，支持多种文件类型 |
| Telegram | ✅ 支持 | 使用 `message` tool |
| Discord | ✅ 支持 | 使用 `message` tool |
| Signal | ✅ 支持 | 使用 `message` tool |
| 微信 | ⏳ 计划中 | 暂未原生支持 |
| QQ | ⏳ 计划中 | 暂未原生支持 |

## Workflow

### Step 1: 确定文件来源（按优先级）

当用户说"发文件"但未明确指定时，按优先级判断：

**优先 1: 生成的文档**
- 刚刚由工具生成的文件（如报告、代码、导出数据）
- workspace 目录下的新文件
- 直接使用该路径

**优先 2: 本地文件**
- 用户明确指定路径：`发送 /path/to/file.pdf`
- 模糊路径：`发送桌面的那个pdf` → 需要搜索或确认
- 使用 `read` 确认文件存在

**优先 3: 截图**
- 用户明确要求截图
- 需要先截图再发送
- macOS: 使用 `screencapture` 命令

### Step 2: 确定目标平台和接收者

**当前对话自动推断**
- 如果用户在飞书对话中 → 发送到当前对话
- 无需额外指定

**明确指定**
- `发到飞书群xxx`
- `发到 Telegram`
- 使用 `message` tool 的 `channel` 和 `target` 参数

### Step 3: 发送文件

**重要：飞书文件发送需要两步**

飞书不能直接发送本地文件路径，必须先上传获取 `file_key`：

**Step 3.1: 上传文件到飞书**
```python
# 1. 获取 tenant_access_token
# 2. 调用 POST /open-apis/im/v1/files 上传文件
# 3. 获取返回的 file_key
```

**Step 3.2: 发送文件消息**
```python
# 调用 POST /open-apis/im/v1/messages?receive_id_type=open_id
# msg_type: "file"
# content: {"file_key": "<file_key>"}
```

**Python 示例代码：**
```python
import requests
import json

# 1. 获取 token
token_resp = requests.post(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={"app_id": APP_ID, "app_secret": APP_SECRET}
)
token = token_resp.json()["tenant_access_token"]

# 2. 上传文件
with open(file_path, 'rb') as f:
    upload_resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/files",
        headers={"Authorization": f"Bearer {token}"},
        files={'file': (filename, f, mime_type)},
        data={'file_type': file_type, 'file_name': filename}
    )
file_key = upload_resp.json()["data"]["file_key"]

# 3. 发送文件消息
requests.post(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={
        "receive_id": open_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    }
)
```

**file_type 对照表：**
| 文件类型 | file_type |
|---------|-----------|
| Excel (.xlsx/.xls) | `xlsx` |
| Word (.docx/.doc) | `doc` |
| PDF | `pdf` |
| 图片 | `image` |
| 视频 | `video` |
| 音频 | `audio` |
| 其他 | `stream` |

## File Type Support

### 飞书支持的文件类型

| 类型 | 扩展名 | 大小限制 |
|------|--------|----------|
| 文档 | pdf, doc, docx, xls, xlsx, ppt, pptx | 30MB |
| 图片 | jpg, jpeg, png, gif, webp | 20MB |
| 音频 | mp3, wav, m4a, aac | 30MB |
| 视频 | mp4, mov, avi | 50MB |
| 压缩包 | zip, rar, 7z | 30MB |

## Examples

### Example 1: 发送刚生成的文件

用户：把刚才生成的报告发到飞书

```
1. 确认生成的文件路径（通常是 workspace 目录）
2. 使用 message tool 发送
```

### Example 2: 发送本地文件

用户：发送 /Users/wlong/Desktop/report.pdf 给我

```
1. 确认文件存在
2. 使用 message tool 发送，target 留空（当前对话）
```

### Example 3: 截图并发送

用户：截个屏发给我

```
1. 使用 screencapture 截图
2. 保存到临时文件
3. 使用 message tool 发送
```

## Scripts

### scripts/send_feishu_file.py

飞书文件发送脚本，自动处理上传和发送流程。

**用法：**
```bash
python ~/.openclaw/skills/send-file/scripts/send_feishu_file.py <file_path> <open_id>
```

**示例：**
```bash
# 发送文件给用户
python ~/.openclaw/skills/send-file/scripts/send_feishu_file.py \
  /Users/wlong/Downloads/report.xlsx \
  ou_26b058ca29943e674a9b0c9039329897
```

**环境变量：**
- `FEISHU_APP_ID`: 飞书应用 ID（**必须配置**）
- `FEISHU_APP_SECRET`: 飞书应用密钥（**必须配置**）

### scripts/send_file.sh

通用文件发送辅助脚本（用于文件检查和验证）。

## Notes

- 大文件发送可能需要时间，告知用户等待
- 飞书有文件大小限制，超大文件需要分片或压缩
- 发送失败时检查文件格式和大小
- 微信/QQ 支持待后续扩展