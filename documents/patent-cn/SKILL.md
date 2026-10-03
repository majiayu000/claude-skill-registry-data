---
name: patent-cn
description: "当用户上传交底材料、研发报告、技术方案文档，并要求撰写专利、撰写初稿，或请专利代理师视角输出可申请的专利文件时触发。也涵盖如下说法：'帮我把这份交底写成专利''生成专利文件''生成初稿''专利撰写'等，无论是否明确说'生成专利文件'。"
---

# 专利申请初稿

## 概述

触发后调用专利生成接口完成全部生成。本 skill 不自己撰写专利内容，只负责：

1. 上传 PDF 交底材料，取 `documentId`
2. 调用生成接口，消费 SSE 流式返回并落盘
3. 生成完成后**征求用户同意**，把文中 SVG 图渲染为高清 PNG、原位内嵌，把文中 Markdown 表格转为 docx 原生表格（带边框、表头加粗），导出 `.docx`

## 执行步骤

### 第 0 步：首次自举（仅一次）

若 `$DIR/assemble.js` 不存在，按下方源码写出（已预置，直接检查存在即可）。

仅在用户同意导出 DOCX 且 `$DIR/node_modules` 不存在时才需要：

```powershell
cd "$DIR"; npm install
```

> `package.json` 在根目录，`@resvg/resvg-js` 和 `docx` 会自动安装。

### 第 1 步：确认输入格式 & DOCX → PDF（静默转换）

上传接口**只接受 PDF**。若用户上传 DOCX/DOC，**自动静默转换**，不提示用户。

转换方法（按优先级尝试）：

1. **LibreOffice**：
   ```powershell
   soffice --headless --convert-to pdf --outdir "$DIR" "C:\绝对路径\交底材料.docx"
   ```
2. **PowerShell COM**（仅 Windows + Word 已安装）：
   ```powershell
   $word = New-Object -ComObject Word.Application
   $doc = $word.Documents.Open("C:\绝对路径\交底材料.docx")
   $doc.SaveAs([ref]"$DIR\temp_交底材料.pdf", [ref]17)
   $doc.Close(); $word.Quit()
   ```
3. **Python docx2pdf**：
   ```powershell
   pip install docx2pdf
   docx2pdf "C:\绝对路径\交底材料.docx" --output "$DIR\temp_交底材料.pdf"
   ```

> ⚠️ **不要在用户原始路径下产生临时文件**，PDF 输出到 `$DIR/` 目录。

### 第 2 步：上传，取 documentId

```powershell
curl.exe -s -X POST "https://www.cndeeptest.com/patent_draft/api/files/upload-document" -F "file=@C:\绝对路径\交底材料.pdf"
```

> ⚠️ PowerShell 中 `curl` 是 `Invoke-WebRequest` 别名，**必须用 `curl.exe`**。

从返回 JSON 的 `data` 取 `documentId`。`code != "200"` 时反馈 `message` 并停止。

### 第 3 步：生成并落盘（SSE 流式）

#### 3a. 后台启动 assemble.js

```powershell
node "$DIR/assemble.js" "<documentId>" "-" "stdout"
```

此命令以**后台模式**运行（timeout 900 秒），会持续输出进度行到 stdout。

#### 3b. 持续轮询直到 100%（核心要求）

启动后，你**必须进入持续轮询循环**，具体步骤：

1. 调用 `process poll` 读取新输出，timeout 设为 30000（30秒）
2. 如果 poll 到包含 `[进度` 的行 → 按下方话术表**逐字照搬**发送给用户
3. 如果 poll 到 `[进度 100%]` → 发送完成话术后退出轮询
4. 如果 poll 到空输出或超时 → **继续下一次 poll，不要停止**
5. 如果 poll 到 `[错误]` → 只转述错误消息，**终止流程**
6. **绝对不要在 100% 之前停止轮询**，不要中途结束对话

> ⚠️ **关键**：你必须持续 poll 直到 `[进度 100%]` 出现。整个过程约 8-15 分钟，期间你**不能提前结束**。每次 poll 超时只是意味着暂无新输出，不代表流程结束——继续 poll 即可。

#### 3c. 进度话术（必须逐字照搬，禁止自由发挥）

当你 poll 到某条 `[进度 X%]` 行时，从下表找到对应行，**整行复制发送，一个字都不要改，emoji 也不要换**：

```
poll 到 [进度 0%]   → 发送：🚀 0% 启动专利任务（剩余约13分30秒）
poll 到 [进度 5%]   → 发送：📋 5% 校验交底材料中（剩余约12分30秒）
poll 到 [进度 8%]   → 发送：✅ 8% 校验合格，开始生成（剩余约11分30秒）
poll 到 [进度 15%]  → 发送：📝 15% 生成初稿中（剩余约10分钟）
poll 到 [进度 50%]  → 发送：📝 50% 初稿已生成，开始质检（剩余约6分钟）
poll 到 [进度 55%]  → 发送：🔍 55% 质检进行中（剩余约5分钟）
poll 到 [进度 70%]  → 发送：✅ 70% 质检完成，开始修复终稿（剩余约3分钟）
poll 到 [进度 75%]  → 发送：🔧 75% 修复终稿中（剩余约2分钟）
poll 到 [进度 100%] → 发送：✅ 100% 专利申请文件生成完成
```

> ⚠️ **每一行都是必须汇报的独立进度节点，一行都不能跳过。** 8% 不是 5% 的附注，而是独立的里程碑——校验通过是重要节点，用户需要知道交底材料被接受了。

**禁止事项：**
- ❌ 禁止自行组合 emoji 和百分比（如 🚀 5% 是错误的）
- ❌ 禁止修改任何文字（包括"剩余约XX分"的时间数字也不许改）
- ❌ 禁止添加表外内容
- ❌ 禁止跳过任何进度等级
- ❌ 禁止在 100% 之前停止轮询

#### 3d. 校验不合格处理

如果 poll 到 `[进度 8%]` 后紧接着出现 `STEP_1_FAIL` 或 `[错误]`：
- **只转述接口返回的 error message**，不猜测原因
- **立即终止流程**

#### 3e. 最终统计（100% 后）

发送完 `✅ 100% 专利申请文件生成完成` 后，再发送：

```
共 X,XXX 字，包含 X 张附图

是否需要导出为 .docx 格式（内嵌高清PNG附图）？
```

**捕获结果**：进程结束后，从 stdout 提取 `===PATENT_CONTENT_START===` 和 `===PATENT_CONTENT_END===` 之间的 JSON，解析 `content` 和 `charCount`。

**统计方法**：
- 字数：`charCount`（JSON 字段）
- 附图数：统计 `content` 中 `<svg` 出现次数

### 第 4 步：征求同意 → 导出 DOCX（仅用户同意后）

**npm install**（如尚未安装依赖）：
```powershell
cd "$DIR"; npm install
```

**执行转换**：
```powershell
# 1. 写入临时 md
$content | Out-File -FilePath "$DIR/临时专利文件.md" -Encoding UTF8
# 2. 转换为 docx
node "$DIR/svg-to-docx.js" "$DIR/临时专利文件.md" "专利申请文件.docx"
# 3. 删除临时 md
Remove-Item "$DIR/临时专利文件.md" -Force
```

> 转换器：每个 `<svg>` → 3 倍率高清 PNG 居中原位内嵌；Markdown 表格 → docx 原生表格。

## 边界规则

- 用户上传 DOCX → **静默自动转 PDF**，不提示用户
- 进度话术 → **必须从 3c 节的话术表逐字照搬**，禁止自由组合
- 轮询 → **必须持续到 [进度 100%]**，不允许中途停止
- 错误 → **仅转述接口返回的 message**，不做原因猜测或建议
- 校验不合格 → **立即终止**，不继续生成

## 附录

- `$DIR`：本技能所在目录（Base directory）
- `$DIR/assemble.js`：SSE 流解析器，纯 Node.js 无依赖
- `$DIR/svg-to-docx.js` + `$DIR/package.json`：DOCX 导出用

详细 API 文档（`references/api.md`）和脚本源码（`references/appendix.md`）可按需读取。
