---
name: readability-report
description: 生成可读性报告。当用户请求为项目源代码生成可读性报告时，使用此功能。输出名为 readability-report.html 的单页 HTML 文件作为可读性报告，该报告集成了 Node.js 脚本和 HTML 模板。
license: Complete terms in LICENSE.txt
---

## 报告生成步骤

1. **确定路径和输出目录**

   - 确定源码文件夹路径（通常为 `src/`）
   - 确定报告输出文件夹：默认为项目根目录下的 `.cqm/readability/`
   - 如果输出文件夹不存在，则创建该目录

2. **初始化文件结构数据**

   - 执行脚本：`node .claude/skills/readability-report/script/generate-file-structure.js <源码文件夹路径> .cqm/readability/readability.json`
   - 脚本会在输出文件夹（`.cqm/readability/`）下生成 `readability.json` 文件
   - 该 JSON 文件包含源码目录结构，每个代码文件的 `readability` 字段初始值为 `0`

3. **评估代码可读性**

   - 读取 `.claude/skills/readability-report/code-readability.md` 作为可读性评估标准
   - 读取 `.cqm/readability/readability.json` 获取所有代码文件列表
   - 对于 JSON 中的每个代码文件：
     - 读取文件内容
     - 根据 `code-readability.md` 的标准，运用 AI 能力评估其可读性
     - 将评估结果（0-100 的分数）更新到该文件对应的 `readability` 字段
   - 将更新后的数据写回 `readability.json`

4. **生成 HTML 报告**

   - 读取模板文件：`.claude/skills/readability-report/template/readability-report-template.html`
   - 读取最终的 `readability.json` 数据
   - 在模板文件中找到 `rawData` 变量（通常在 JavaScript 代码中）
   - 将 `readability.json` 的内容赋值给 `rawData` 变量
   - 将更新后的模板内容保存为 `.cqm/readability/readability-report.html`

5. **完成**
   - 最终报告文件位于：`.cqm/readability/readability-report.html`
