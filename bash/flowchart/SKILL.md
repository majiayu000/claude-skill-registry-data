---
name: flowchart
description: 绘制或修改 Mermaid 流程图、代码流程和对象关系图，并始终在 https://mermaid.live/edit 打开带图表内容的可编辑预览。用于用户要求绘制或预览流程图；明确只要伪代码时不触发绘图。
---

# Flowchart

使用 Mermaid 表达流程，完成后总是在 `https://mermaid.live/edit` 打开当前图表的可编辑预览，不能只返回聊天里的代码块或空白编辑器。用户后续明确要求不打开浏览器时遵从该要求。

## 绘制与预览

- 按用户请求与实际代码区分已实现路径和拟议修改；节点写真实对象/方法名，边写数据或调用关系。必要时用虚线标识拟议路径并说明图例。
- 保存 UTF-8 Mermaid 源码到 `.mmd` 文件。临时预览放系统临时目录；用户要求保存到项目时遵循该项目的文档组织规则。
- 用随附脚本生成包含源码的编辑链接：

  ```bash
  python3 <本 skill 目录>/scripts/mermaid_url.py /path/to/diagram.mmd
  ```

  也可用 `-` 从 stdin 读取。脚本仅生成链接，不负责打开浏览器。
- 使用浏览器工具打开生成的完整 `https://mermaid.live/edit#pako:...` URL。遵循当前环境的浏览器优先级；Lights 环境优先 Chrome DevTools MCP。该工具不可用时简要说明，再使用系统默认浏览器打开（macOS 使用 `open`，Windows 使用 PowerShell `Start-Process`，Linux 使用 `xdg-open`，均以参数传递完整 URL）。不关闭用户浏览器或杀进程来解除配置占用。
- 浏览器可检查时确认图表已载入、没有 Mermaid 语法错误，再交付；发现错误就修正源码并重新打开预览。只有系统打开命令成功时，如实说明已发起打开，不声称已验证页面渲染。
- 最终提供可点击的“打开流程图”编辑链接；需要交付源码时附 `.mmd` 文件链接。聊天内图表可作为补充，不能代替 Mermaid Live 预览。

## 链接实现

脚本使用 UTF-8 JSON → zlib deflate → URL-safe Base64，按 Mermaid Live 的 `#pako:` 格式生成链接；状态中的 `mermaid` 是 JSON 字符串。图表内容在链接中，不要将凭据加入图表。

协议来源：[官方序列化实现](https://github.com/mermaid-js/mermaid-live-editor/blob/develop/src/lib/util/serde.ts)、[官方状态类型](https://github.com/mermaid-js/mermaid-live-editor/blob/develop/src/lib/types.d.ts)。页面格式变化时先核对这些来源，不猜测编码。
