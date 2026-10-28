---
name: file-reader-wechat
description: 【微信机器人专用版】含 Python 代码：从微信 iLink 文件消息下载（CDN）、AES-128-ECB 解密、解析 PDF/Word/txt 正文。依赖微信 iLink 协议，只能用在微信 iLink 机器人上；别的平台用【通用版】file-reader。
---

# File Reader（微信机器人专用版）

**定位**：专为微信 iLink 机器人写的技能，带可运行的 Python 代码。
**与通用版的区别**：`file-reader` 是通用版（纯流程、无代码，任何 AI 助手可用）。
本技能的代码依赖微信 iLink 协议（文件消息结构、CDN、AES 密钥），换平台跑不起来。

## 协议要点

- 入站消息 `item_list[]` 的 `type`：1 文本 / 2 图片 / 3 语音 / **4 文件** / 5 视频
- 文件消息结构：`item.file_item.media` 含 `aes_key`（base64，两种编码：16 字节原文或 32 字符 hex）
  与 `full_url`（CDN 下载地址）；`item.file_item.file_name` / `len`
- CDN 文件用 **AES-128-ECB** 加密，PKCS7 填充

## 用法

```python
from file_reader import download_media_item, extract_file_text

# item 是入站消息 item_list 中的文件 item（type == 4）
raw_bytes = download_media_item(item)          # 下载并解密 -> 原始字节
text, pages = extract_file_text(raw_bytes, "讲义.pdf")  # 解析纯文本
```

## 支持的格式

| 格式 | 解析方式 |
|------|----------|
| PDF | pypdf，按页提取 |
| docx | python-docx，按段落提取 |
| txt / md / csv / json / log | UTF-8 解码 |

图片（type 2）、语音（type 3）暂不支持。

## 依赖

```
cryptography   # AES 解密
pypdf          # PDF 解析
python-docx    # Word 解析
requests       # CDN 下载
```
