---
name: pdfmd
description: 将 PDF 文件转换为结构化的中文 Markdown 文本。只在用户明确要求“把 PDF 转成 Markdown/MD/文档”时使用本技能。
allowed-tools: ["Bash", "Write"]
triggers:
  - type: keyword
    keywords:
      - "pdf 转 markdown"
      - "pdf 转 md"
      - "pdf 转 文本"
      - "把 pdf 变成 markdown"
      - "把 pdf 变成 md"
      - "从 pdf 中提取内容"
---

# PDF to Markdown 转换 Skill（示例）

## 何时使用

当出现以下任一情况时，可以考虑启用本 Skill：

- 用户说“把这个 PDF 转成 Markdown / MD / 文本 / 文档”
- 用户上传或引用 PDF 文件，并要求“提取里面的正文”“翻译成中文 Markdown”等

如果用户只是一般性阅读 / 总结 PDF，而不要求导出 Markdown，可以直接阅读 PDF 文本或使用其他技能。

## 工作目录结构

在当前示例项目中，本 Skill 所在目录如下：

```text
workspace/
  skills/
    pdfmd/
      SKILL.md
      pdf_extract.py
```

其中：

- `SKILL.md` 为本说明文件
- `pdf_extract.py` 是一个 Python 脚本，仅负责从 PDF 中提取纯文本（不调用任何大模型），
  再由当前 Agent 使用已有的大模型配置完成翻译和 Markdown 转换。

> 注意：本 Skill 假设在执行环境中已经安装了 Python 以及依赖:
>   - `pypdf`

## 给 Claude 的操作步骤（使用 SDK 内置能力）

当你判断应当使用本 Skill 时，请按以下顺序操作：

1. **确认 PDF 文件路径**

   - 如果用户提供了路径（例如 `docs/report.pdf`），先确认该路径在当前工作区内。
   - 如果用户上传了 PDF 文件，将其保存到本地工作目录（如 `./docs/`），并记住实际路径。

2. **选择输出路径**

   - 如果用户希望生成一个 Markdown 文件，可以选定输出路径，例如：
     - 输入：`docs/report.pdf`
     - 输出：`docs/report.md`

3. **使用 `Bash` 调用 Python 脚本提取 PDF 文本**

   使用 `Bash` 工具执行 Python 脚本来读取 PDF 内容，例如（注意：命令在沙箱工作目录 `workspace/` 下执行，因此路径从 `skills/` 开始）：

   ```bash
   python skills/pdfmd/pdf_extract.py \
     --input "<PDF 文件路径>" \
     --pages "<页码范围，可选，如 1-3,5>"
   ```

   说明：

   - `--input`：要读取的 PDF 文件路径（必填）
   - `--pages`：可选页码范围，例如 `"1-3,5"`
   - 脚本不会调用任何大模型，只会将提取出的纯文本打印到 stdout。

   `Bash` 工具的返回中：

   - `ok`: 命令是否执行成功（exit code 为 0）
   - `output`: 包含脚本的标准输出（即提取出的 PDF 文本）

4. **在当前对话中使用大模型进行转换**

   在拿到 `Bash` 的输出后，不需要在 Skill 或脚本中直接调用任何外部大模型 API。
   而是：

   - 将 `output` 字段中的内容视为原始 PDF 文本；
   - 在当前 Agent 的对话中，结合本 Skill 的说明，向大模型发出请求：
     - 将文本翻译成中文；
     - 调整结构为合理的标题、段落、列表等；
     - 输出为标准的 Markdown 格式。

   > 所有大模型调用由 SDK 的 provider/router 统一负责，自动使用当前 Agent 配置好的模型和路由策略，
   > Skill 不负责管理 API Key 或模型选择。

5. **使用 `Write` 将 Markdown 保存到文件（如用户有此需求）**

   如果用户明确要求生成 Markdown 文件，可以在得到最终 Markdown 文本后，调用 `Write` 工具写入文件：

   ```json
   {
     "path": "<输出 Markdown 文件路径>",
     "content": "<模型生成的中文 Markdown 文本>"
   }
   ```

   然后可以通过正常的文件系统操作（如下载或后续处理）使用该文件。

6. **根据用户需求做二次加工（可选）**

   - 如果用户还有额外要求（例如“只保留某几章”“简化为摘要”），在拿到 Markdown 后再用模型进行二次加工。
   - 对于特别长的 Markdown，可以按章节或段落拆分处理，避免超出上下文限制。

## 错误处理与限制

- 若 Python 脚本执行失败（`Bash` 返回 `ok == false` 或 exit code 非 0）：
  - 检查 PDF 路径是否正确；
  - 确认文件存在且为有效 PDF；
  - 检查是否已安装 `pypdf` 依赖。

- 若生成的 Markdown 明显缺失内容或大量乱码：
  - 向用户说明这是 PDF 原始排版 / 内嵌字体导致的限制。
  - 根据情况建议尝试只转换部分页面，或改用其它方式获取内容。

## 安全注意事项

- 本 Skill 通过 Python 脚本仅读取 PDF 文本，不执行其中任何代码，但仍建议只对可信来源的 PDF 使用本 Skill。
- 大模型调用由 SDK 内部统一管理，Skill 不直接处理任何 API Key。
