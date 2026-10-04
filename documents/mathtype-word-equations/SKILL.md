---
name: mathtype-word-equations
description: "在 Windows 上安全处理 Word/WPS DOCX 公式：把带编号公式或 Word 内置公式（OMML）转换、汇总为可编辑 MathType OLE（Equation.DSMT4），或在文档间复制已有 MathType 公式。适用于用户要求‘MathType 公式’‘内置公式转 MathType’‘提取/列出带编号公式’或‘批量转换公式’时；不适用于只有 PDF、未安装 MathType 或需要手工排版的任务。默认不启动或操控 Word/WPS，不原地修改源文件。"
---

# Word MathType 公式

在 DOCX 包层直接处理公式，默认不使用 computer-use，也不占用用户的 Word/WPS 窗口。所有公式必须成为可编辑的 `Equation.DSMT4` OLE 对象，不能只插入图片或把 OMML 改个标签。

## 必须遵守

- 把输入文档视为只读；输出到不同且尚不存在的 `.docx` 路径。
- 不关闭、不杀死 Word、WPS、MathType 或其他用户进程。文件被占用时停止并说明。
- 先生成候选文件，再验证。用户明确要求覆盖已有目标时，按 [workflow.md](references/workflow.md) 的发布流程创建唯一备份并复核源文件未变化。
- 只清理本次运行创建且已确认位于专用暂存根目录中的文件；失败时保留暂存目录并报告位置。
- 不上传用户文档、公式内容、绝对路径、暂存文件或生成的 OLE/WMF 资产。

## 选择处理路径

先只读检查 `word/document.xml`、`word/_rels/document.xml.rels`、嵌入对象和图片关系，然后分流：

1. **已有 MathType OLE**：优先逐字节复制对应 OLE 与 WMF 预览，重映射关系和所有标识符。带编号公式汇总时使用 `scripts/Copy-NumberedMathTypeEquations.ps1`。
2. **Word 内置公式（OMML）**：使用固定版本 XSLT 转 MathML，再通过本机 MathType OLE 服务顺序生成 OLE 与 WMF。使用 `scripts/Convert-OmmlDocxToMathType.ps1`。
3. **混合文档**：已有 MathType 对象走复制路径，其余 OMML 走转换路径；不得重复转换已有 MathType。

仅按对象大小判断空公式不可靠。必须用通用回读验证；只有回读确认“不含任何非空语义 token”时才跳过空占位对象，其他回读错误都应中止。

## 执行顺序

1. 阅读 [workflow.md](references/workflow.md)，解析绝对路径，确认源、目标不同且输出不存在。
2. 首次使用或 helper 缺失时运行 `scripts/Build-MathTypeHelpers.ps1`；helper 必须编译为 x86。
3. 在唯一暂存目录生成候选 DOCX。MathType OLE 本地服务调用必须串行，不能并发。
4. 运行 `scripts/Test-MathTypeDocx.ps1`，并按 [validation.md](references/validation.md) 完成结构、语义与预览资产验证。完整转换要求 OMML 数量为零；发布前给审计器传入 verifier，不能只做静态计数。
5. 交付候选文件及验证摘要；只有用户明确要求时才发布到既有目标路径。

OMML 路径使用随 skill 固定的 `references/third-party/OMML2MML.XSL`。需要转换 OMML 时先读 [SOURCE.md](references/third-party/SOURCE.md)，不得静默换用来源或许可证不明的 XSL 文件。

## 失败处理

任何一个公式生成、回读或关系校验失败，都不要发布部分成功的文件。保留只读源文件和候选/暂存证据，报告失败公式序号、阶段和可复现命令；不要尝试通过界面自动化补救，除非用户另行授权。
