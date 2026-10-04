---
name: wechat-theme-extractor-cn
description: 当用户需要从微信公众号文章提取视觉样式，并生成 markdown-wechat-converter 主题时使用。
---

# 微信文章主题提取器

## Overview

从微信公众号文章中提取正文样式，生成可用于 `markdown-wechat-converter` 的主题配置，并在目标工具文件中自动落盘。流程会从文章中分析字体、颜色、间距和区块样式，把新主题写入 `markdown-to-wechat.html`，并支持写入后的预览。

## 何时使用

当用户有以下需求时使用本技能：
- 提供微信公众号文章链接，要求提取排版和样式
- 希望基于现有微信文章生成新的主题配置
- 需要把主题自动写入 `markdown-to-wechat.html`
- 需要在写入完成后直接打开目标 HTML 预览

## 不要使用

以下场景不应使用本技能：
- 非微信公众号文章链接
- 用户只要提取纯文本内容，不需要分析主题样式
- 目标项目中不存在 `markdown-wechat-converter` 或对应 HTML 配置文件

## 使用说明

1. 先运行 `scripts/extract.py`，只负责抓取文章 HTML、提取标题和 `js_content`。
2. 读取生成的 `.extracted_content.html`，由 AI 自行分析颜色、字号、间距、标题层级、引用块、分隔元素等样式特征。
3. 基于分析结果生成适配 `markdown-wechat-converter` 的主题配置。
4. 在当前工作区内定位并修改 `markdown-to-wechat.html`，将新主题追加到已有主题配置中，避免破坏现有结构。
5. 修改后再次检查目标文件，确认主题配置已成功写入。
6. 如果写入成功，使用系统浏览器打开 `markdown-to-wechat.html` 进行预览。

## 执行流程

```text
用户提供链接
  -> 运行提取脚本
  -> 生成 .extracted_content.html
  -> AI 分析样式
  -> 生成主题配置
  -> 写入 markdown-to-wechat.html
  -> 校验写入结果
  -> 打开 HTML 预览
```

## 运行脚本

```bash
python3 scripts/extract.py "https://mp.weixin.qq.com/s/xxxxx"
```

## 脚本职责边界

Python 脚本只做以下事情：
- 获取微信文章 HTML
- 提取文章标题
- 提取 `js_content` 正文片段
- 保存为 `.extracted_content.html`

以下工作由 AI 完成：
- 样式特征分析
- 主题结构生成
- 写入目标工具配置
- 写入结果校验
- 预览打开

## 写入 `markdown-to-wechat.html` 规则

更新 `markdown-to-wechat.html` 时，必须遵守以下规则：

1. 先定位真实主题配置区域。
   - 先搜索主题相关的对象、数组、映射或 `const` 定义，再决定修改位置。
   - 不要假设固定变量名，必须以文件现有结构为准。

2. 保持原有代码风格。
   - 延续文件当前的缩进、引号风格、逗号风格和对象结构。
   - 不要顺手重排或格式化无关代码。

3. 优先追加或定点更新。
   - 如果主题名不存在，在现有主题集合中追加新条目。
   - 如果同名主题已存在，只更新该主题条目，不重复插入。

4. 限制修改范围。
   - 只修改主题定义区域，以及让主题可被选择所必须的最小注册代码。
   - 除非文件结构强制要求，否则不要改动渲染逻辑、事件处理或其他 UI 代码。

5. 写入后必须复检。
   - 重新读取修改后的片段，确认主题键名、显示名和核心样式字段都已存在。
   - 如果无法安全定位主题区块，停止自动写入并明确说明需要人工确认目标结构。

## 示例主题片段

生成主题时，优先产出与目标文件现有结构一致的对象。下面是一个可参考的最小示例：

```js
{
  id: "wechat-clean-blue",
  name: "微信清爽蓝",
  styles: {
    body: {
      fontFamily: "\"PingFang SC\", \"Helvetica Neue\", sans-serif",
      fontSize: "16px",
      color: "#2b2b2b",
      lineHeight: "1.75",
      backgroundColor: "#ffffff"
    },
    h1: {
      fontSize: "24px",
      fontWeight: "700",
      textAlign: "center",
      color: "#1f3a5f"
    },
    h2: {
      fontSize: "20px",
      fontWeight: "700",
      color: "#1f3a5f",
      borderBottom: "2px solid #9ec1ff"
    },
    blockquote: {
      color: "#4a5568",
      backgroundColor: "#f7fbff",
      borderLeft: "4px solid #7fb3ff",
      padding: "12px 16px"
    }
  }
}
```

实际写入时：
- 字段名必须以 `markdown-to-wechat.html` 现有主题结构为准
- 如果目标文件使用数组项、映射值或嵌套注册格式，应按原结构改写此示例
- 至少包含主题标识、显示名和核心排版样式

## 输出文件

- `scripts/.extracted_content.html`：提取出的正文 HTML，首部包含标题和原始 URL 注释

## 校验清单

- 能成功抓取文章 HTML
- `.extracted_content.html` 已生成且内容非空
- 已提取到标题和 `js_content`
- 新主题已写入 `markdown-to-wechat.html`
- `markdown-to-wechat.html` 打开后可正常预览
