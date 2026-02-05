---
name: summarize-to-apple-notes
description: Summarize conversation content and save to Apple Notes app using HTML format. Use when user asks to "总结并保存到备忘录", "summarize and save to Notes". Handles both summarization and saving in one step. Can save to custom folder if user specifies.
allowed-tools: Bash
---

# 总结并保存到 Apple Notes

总结对话内容并保存到 macOS Apple Notes 应用，使用 HTML 格式显示。

## 职责

- ✅ 根据上下文总结对话内容
- ✅ 转换为 HTML 格式
- ✅ 保存到 Apple Notes（支持自定义文件夹）

## 触发场景

- "总结并保存到备忘录"
- "把内容保存到 Notes"
- "整理一下保存到备忘录"
- "总结到备忘录，放到 ABC 文件夹下"
- "summarize and save to Apple Notes"

**注意**：
- 具体总结哪些内容，由 Claude 根据对话上下文自动判断
- 如果用户指定了文件夹名称（如"放到 ABC 文件夹"），使用指定的文件夹
- 否则使用默认文件夹：`"AI Notes"`

## 操作流程

1. **分析上下文** - 识别需要总结的内容范围
2. **识别目标文件夹** - 检查用户是否指定了文件夹名称
3. **生成总结** - 提取关键要点、结论、代码等
4. **转换为 HTML** - 使用 Apple Notes 支持的标签
5. **保存** - 执行 osascript 命令写入指定文件夹

### 保存命令（关键）

**正确的创建方式**：

```bash
osascript <<'EOF'
set noteContent to "<h1>标题</h1>
<p>内容...</p>"
set folderName to "AI Notes"

tell application "Notes"
    -- 检查文件夹是否存在，不存在则创建
    if not (exists folder folderName) then
        make new folder with properties {name:folderName}
    end if

    -- 创建笔记（不提供 name，让 Notes 自动从内容提取标题）
    make new note at folder folderName with properties {body:noteContent}
end tell
EOF
```

**使用自定义文件夹**：
```bash
osascript <<'EOF'
set noteContent to "<h1>标题</h1>
<p>内容...</p>"
set folderName to "用户指定的文件夹名"

tell application "Notes"
    if not (exists folder folderName) then
        make new folder with properties {name:folderName}
    end if

    make new note at folder folderName with properties {body:noteContent}
end tell
EOF
```

**重要说明**：
- ⚠️ **必须先检查文件夹是否存在**，不存在则创建，否则会报错
- ⚠️ **不要提供 name 参数**，让 Apple Notes 自动从内容第一行（h1）提取笔记名称
- 如果提供 name 参数，会导致标题重复显示（name 显示一次，h1 又显示一次）
- 文件夹名称区分大小写
- 默认文件夹为 `"AI Notes"`，用于存放 AI 对话相关的笔记

## Apple Notes 支持的 HTML 标签

### ✅ 支持

| 标签 | 用途 |
|------|------|
| `<h1>` `<h2>` `<h3>` | 标题（三级） |
| `<p>` | 段落 |
| `<br>` | 换行/空行 |
| `<ul>` `<li>` | 无序列表 |
| `<ol>` `<li>` | 有序列表 |
| `<pre>` | 代码块 |
| `<table>` `<tr>` `<th>` `<td>` | 表格 |
| `<b>` `<i>` `<u>` `<s>` | 加粗/斜体/下划线/删除线 |

### ❌ 不支持

- `<blockquote>` - 块引用
- `<code>` - 行内代码（用 `<b>` 代替）
- `<hr>` - 分隔线（用 `<p>---</p>` 代替）
- Markdown 语法

## 间距和排版规则

为了获得良好的阅读体验，推荐使用以下间距规则：

**方案 E：密集内容 + 稀疏章节**

| 位置 | 规则 | 说明 |
|------|------|------|
| h2/h3 标题后 | 加 `<br>` | 标题与内容之间留白 |
| 段落之间 | 不加 `<br>` | 保持段落紧凑 |
| 章节之间 | 加 `<br>` | 在下一个 h2/h3 前留白 |
| 代码块前后 | 加 `<br>` | 代码块需要明确分隔 |
| 表格前后 | 加 `<br>` | 表格需要明确分隔 |
| 列表前后 | 加 `<br>` | 列表需要明确分隔 |

**效果**：章节分明，段落紧凑，层次清晰

## 输出格式示例

```html
<h1>技术讨论：XXX 方案选择</h1>
<p>日期：2025-12-11</p>
<br>
<h2>背景</h2>
<br>
<p>问题描述第一段...</p>
<p>问题描述第二段...</p>
<br>
<h2>关键结论</h2>
<br>
<ul>
<li>结论一</li>
<li>结论二</li>
<li>结论三</li>
</ul>
<br>
<h2>代码示例</h2>
<br>
<pre>function example() {
  return true;
}</pre>
<br>
<h2>对比分析</h2>
<br>
<table>
<tr><th>方案</th><th>优点</th></tr>
<tr><td>方案 A</td><td>简单</td></tr>
<tr><td>方案 B</td><td>灵活</td></tr>
</table>
<br>
<p>---</p>
<p><i>由 Claude Code 生成</i></p>
```

## 文件夹使用示例

### 示例 1：使用默认文件夹
```
用户："把我们刚才讨论的 Vue 问题总结一下保存到备忘录"
→ 保存到 "AI Notes" 文件夹（不存在会自动创建）
```

### 示例 2：指定文件夹
```
用户："总结到备忘录，放到'技术调研'文件夹"
→ 保存到 "技术调研" 文件夹（不存在会自动创建）
```

## 注意事项

- **HTML 实体转义（重要）**：在 HTML 内容中必须使用 HTML 实体，否则会导致 osascript 解析失败

  | 字符 | HTML 实体 | 使用场景 |
  |------|-----------|----------|
  | `"` | `&quot;` | 错误信息、代码中的字符串 |
  | `'` | `&apos;` 或 `&#39;` | 代码中的字符串 |
  | `<` | `&lt;` | 代码块中的泛型、比较符号 |
  | `>` | `&gt;` | 代码块中的泛型、比较符号 |
  | `&` | `&amp;` | URL 参数、特殊符号 |

  **示例**：
  ```html
  <!-- 错误（会导致 osascript 失败）-->
  <pre>const msg = "Hello World";</pre>

  <!-- 正确 -->
  <pre>const msg = &quot;Hello World&quot;;</pre>
  ```

- **换行**：`<br>` 可叠加使用创建多个空行
- **权限**：首次运行需授予终端访问 Notes 的权限
- **文件夹检查**：必须先检查文件夹是否存在，不存在则创建
- **文件夹名称**：区分大小写，建议使用有意义的名称
