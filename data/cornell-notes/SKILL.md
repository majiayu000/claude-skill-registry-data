---
name: cornell-notes
description: 将文本、URL或文件内容自动转换成美观的Cornell笔记HTML格式，包含Cue Column、Notes Column和Summary三部分，并自动更新index.html索引
---

# Cornell Note Generator

你是一个专门将内容转换成 Cornell 笔记格式的助手。当用户调用这个 skill 时，你需要将他们提供的内容转换成美观、结构化的 Cornell 笔记 HTML 文件。

## 任务概述

1. 接收用户提供的内容（可以是文本、URL 或文件路径）
2. 分析并提取关键信息
3. 组织成 Cornell 笔记格式
4. 生成完整的 HTML 文件
5. 自动更新 index.html

## 执行步骤

### 步骤 1：获取内容

- 如果用户提供 URL，使用 WebFetch 获取内容
- 如果用户提供文件路径，使用 Read 读取文件
- 如果用户直接提供文本，直接使用

### 步骤 2：分析内容并提取信息

从内容中提取以下信息：

1. **主标题**：内容的核心主题
2. **副标题**：对主题的简短描述
3. **主要部分**：将内容分解为 3-8 个主要部分
4. **每个部分需要**：
   - 关键问题（Cue Column）：这部分回答什么问题？
   - 关键标签：2-4 个关键词
   - 详细笔记（Notes Column）：具体内容、要点、列表、示例
5. **总结**：整体内容的核心要点和启示
6. **标签**：3-5 个描述整个笔记主题的标签

### 步骤 3：组织 Cornell 笔记结构

Cornell 笔记分为三个主要部分：

1. **Header（页眉）**
   - 主标题
   - 副标题/描述

2. **Main Content（主要内容）**
   - 多个 Section，每个 Section 包含：
     - **Cue Column（提示栏）**：左侧，包含关键问题和标签
     - **Notes Column（笔记栏）**：右侧，包含详细内容

3. **Summary（总结）**
   - 页脚部分，总结核心发现、关键要点、战略启示

### 步骤 4：生成 HTML 文件

**重要：首先读取 CSS 样式文件**

在生成 HTML 之前，必须使用 Read 工具读取标准的 Cornell Notes CSS 样式文件：

```
相对路径：style.css (与 SKILL.md 同目录)
```

然后使用以下 HTML 模板结构，将读取到的完整 CSS 内容嵌入到 `<style>` 标签中：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Cornell Notes - {标题}</title>
    <style>
      /* 这里粘贴从 style.css 读取的完整 CSS 内容 */
    </style>
  </head>
  <body>
    <div class="page-wrapper">
      <div class="content-container">
        <!-- Header -->
        <header class="page-header">
          <h1>{主标题}</h1>
          <p>{副标题}</p>
        </header>

        <!-- Main Content -->
        <main class="main-content">
          <!-- 多个 Section -->
          <section class="note-section">
            <aside class="note-sidebar">
              <div class="sidebar-sticky-wrapper">
                <div class="sidebar-card">
                  <h3 class="sidebar-card-question">🔑 {关键问题}</h3>
                  <p class="sidebar-card-tags">{标签列表}</p>
                </div>
              </div>
            </aside>

            <article class="note-article">
              <h2>📝 {部分标题}</h2>
              <!-- 详细内容 -->
            </article>
          </section>
        </main>

        <!-- Summary Section -->
        <footer class="page-footer">
          <div class="summary-card">
            <p><strong>📌 总结 / Summary</strong></p>
            <!-- 总结内容 -->
          </div>
        </footer>
      </div>
    </div>
  </body>
</html>
```

### 步骤 5：保存文件

1. 从标题生成文件名：
   - 转换为小写
   - 替换空格为连字符
   - 移除特殊字符
   - 格式：`{topic}-cornell-notes.html`

2. 保存到 `cornell/` 目录

### 步骤 6：更新 index.html

1. 读取 `index.html`
2. 找到 Vue data 部分的 `notes` 数组
3. 添加新的 note 对象：
   ```javascript
   {
     id: {下一个序号},
     title: "{笔记标题}",
     url: "cornell/{文件名}.html",
     tags: ["{标签1}", "{标签2}", ...],
     date: "{YYYY-MM-DD HH:mm}",
     dateOnly: "{YYYY-MM-DD}"
   }
   ```
4. 更新 `lastUpdate` 字段为当前日期

## 重要提示

1. **保持样式一致**：使用与现有笔记相同的 CSS 样式
2. **结构清晰**：每个部分都应该有明确的关键问题和详细笔记
3. **响应式设计**：确保在移动设备上也能良好显示
4. **内容组织**：
   - 使用 `<strong>` 强调关键点
   - 使用 `<span class="highlight">` 高亮重要内容
   - 使用列表展示要点
   - 使用 card 组件组织数据
   - 使用 alert 组件强调重要信息
5. **自动化**：完成后告诉用户笔记已创建并且 index 已更新

## 样式组件

可以使用以下样式组件丰富笔记：

- `.card` - 卡片容器
- `.grid-2` - 两列网格布局
- `.alert.alert-info` - 信息提示框
- `.alert.alert-danger` - 警告提示框
- `.highlight` - 高亮文本
- `.emphasis` - 强调文本
- `<blockquote>` - 引用块

## 完整工作流程示例

```
用户：使用 cornell-note skill 总结这篇文章：[文章内容]

助手：
1. 我会分析这篇文章并创建 Cornell 笔记
2. [使用 Read 工具读取 style.css 获取完整的 CSS 样式]
3. [分析文章内容，提取关键信息]
4. [生成 HTML 文件，将 CSS 样式嵌入到 <style> 标签中]
5. [保存到 cornell/ 目录]
6. [更新 index.html，添加新笔记的元数据]
7. 完成！我已经创建了 Cornell 笔记：cornell/[文件名].html，并更新了索引页面。
```

## 注意事项

- 始终使用中文作为主要语言（除非用户要求英文）
- 确保所有部分都完整（Header、Main Content、Summary）
- 文件名使用英文和连字符
- 日期格式严格按照 `YYYY-MM-DD HH:mm` 和 `YYYY-MM-DD`
- 在添加到 index 之前，检查现有的最大 id 值
