---
name: hosts-troubleshoot
description: 排查和修复系统 hosts 文件问题。当用户提到 hosts 解析异常、域名映射错误、网站被劫持、需要清理重复条目、或任何与 hosts 文件相关的疑问时使用——即使用户没有明确说出"hosts"这个词，只要问题涉及域名解析异常也应主动加载。
---

# Hosts 排查

按以下流程使用 HOSTS_MGR 工具（operation=read / list_groups / add_entry / remove_entry）排查 hosts 问题：

## 1. 读取现状

先调用 `HOSTS_MGR(operation='read')` 获取完整 hosts 内容。把每一行归类为：有效映射、注释、空行、可疑行（格式错误、被注释但疑似应生效的条目）。

## 2. 诊断常见问题

- **重复映射**：同一 hostname 出现多个不同 IP。列出每组重复，指出实际生效的（最后一条），询问用户保留哪个。
- **冲突映射**：hostname 同时映射到 127.0.0.1 和真实 IP（常见于"屏蔽"软件与开发配置打架）。
- **格式错误**：缺少 IP 或 hostname、多余空格分隔符、全角字符混入。
- **失效条目**：映射到内网 IP 但当前网络不可达的（可以用 TERMINAL `ping` 验证，超时即报告，不要断言失效）。

## 3. 修复

- 修复动作都是写操作：`remove_entry` / `add_entry`。执行前先向用户复现将要删除/新增的条目，确认后再动手。
- 一次只改一条，改完用 `read` 复核结果。
- 不要批量清理用户没有确认的条目。

## 4. 验证

修复后建议用户执行 `ipconfig /flushdns`（Windows）或告知 macOS/Linux 对应命令，并用 TERMINAL `ping <hostname>` 验证解析是否生效。
