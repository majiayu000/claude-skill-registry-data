---
name: policy-rag
description: 当用户需要处理企业内部制度文件、审批流程表、审批权责表，或需要基于内部制度与审批流进行检索、问答、索引构建时，使用本技能。适用于制度文档拆分、Excel 审批表转换、制度索引构建、制度条款检索、审批路径检索等场景。不适用于国家法律法规、司法解释、裁判案例等法律检索任务；此类问题应交由专门的法律检索技能处理。
metadata:
  short-description: 面向企业内部制度与审批流程的拆分、转换、索引、检索与问答技能，采用严格脚本驱动工作流。
---

# Policy RAG 技能

本技能用于处理**企业内部制度文件**与**审批流程数据**，采用**严格的脚本驱动工作流**。

适用对象包括但不限于：

- 企业内部管理制度
- 采购制度
- 财务制度
- 供应商管理制度
- 费用报销制度
- 审批权限表
- 审批流程表
- Excel 版审批权责矩阵
- 已拆分或待拆分的制度文档

本技能的目标不是通用网页搜索，也不是国家法律法规检索，而是围绕**企业内部制度与审批流程**完成以下工作：

- 文档拆分
- Excel 审批表结构化转换
- 索引构建或重建
- 制度条款检索
- 审批路径检索
- 基于检索结果的证据化回答

---

## 一、适用场景

当用户提出以下需求时，应优先使用本技能：

### 1. 制度文档处理
- “把这份制度拆分一下，方便后续检索”
- “把上传的制度文档处理成可索引格式”
- “把这份 Markdown / Word 制度文件按章节拆开”

### 2. 审批 Excel 转换
- “把这个审批表转成结构化流程数据”
- “把 Excel 审批权责表转换成可检索格式”
- “把这份审批流表导入系统”

### 3. 制度索引构建
- “重建一下制度索引”
- “把处理后的制度文件建立检索索引”
- “刷新内部制度知识库”

### 4. 制度条款检索
- “预付款比例限制在哪一章”
- “白名单供应商的要求写在哪”
- “采购金额上限的规定在哪里”

### 5. 审批流程检索
- “这件事怎么审批”
- “超过 200 万的采购走什么审批路径”
- “供应商解冻走哪个审批分支”
- “这个申请由谁审批”

---

## 二、不适用场景

以下场景**不要**使用本技能：

- 国家法律法规检索
- 司法解释检索
- 裁判案例检索
- 法律咨询中的法条依据检索
- 需要联网搜索最新政策、最新新闻、最新监管动态的问题
- 通用网页信息查询

若用户问题属于以上类型，应改用相应的法律检索技能或网页搜索流程。

---

## 三、强制规则

以下规则为**必须遵守**的硬性规则。

### 规则 1：优先使用当前对话中上传的文件
如果用户在当前对话中上传了制度文档、审批表或 Excel 文件，应优先以这些文件为输入。

不得无视用户上传文件，直接跳到旧数据目录进行处理。

---

### 规则 2：必须调用仓库脚本，不得口头替代
凡是涉及以下实际处理任务时，必须调用仓库中已有脚本：

- 文档拆分
- Excel 审批表转换
- 索引构建
- 制度检索
- 审批流检索

不得仅凭理解“模拟执行”这些操作，也不得用临时自写逻辑替代已有脚本，除非原脚本明确缺失或报错不可用。

---

### 规则 3：回答必须建立在检索结果之上
当用户询问制度条款或审批流程时，必须先执行检索命令，再根据检索结果作答。

不得把未经检索验证的猜测表述为系统结论。

---

### 规则 4：严格限定技能边界
本技能只处理**企业内部制度**与**审批流程数据**。

如果问题本质上是在问：

- 法律法规
- 法条解释
- 司法裁判
- 行政监管规则

则不应继续使用本技能。

---

### 规则 5：命令执行失败时必须如实报告
若脚本报错、路径不存在、索引缺失、流程数据缺失，必须明确说明失败原因。

不得在失败后继续虚构结果。

---

## 四、目录与路径约定

默认假定本技能挂载在以下路径：

- 技能根目录：`/mnt/skills/custom/policies-regulations/policy-rag`
- 脚本目录：`/mnt/skills/custom/policies-regulations/policy-rag/scripts`

默认工作目录约定如下：

- 当前会话上传文件目录：`/mnt/user-data/uploads`
- 工作区输出目录：`/mnt/user-data/workspace/policy-rag`
- 原始制度文档目录：`/mnt/datasets/policy-rag/raw`
- 拆分后的制度文档目录：`/mnt/datasets/policy-rag/processed`
- 审批流程数据目录：`/mnt/datasets/policy-rag/flows`
- 制度索引目录：`/mnt/datasets/policy-rag/index`
- 缓存目录：`/mnt/datasets/policy-rag/.cache`

如工作区目录不存在，可先创建。

---

## 五、环境前提

本技能默认依赖以下运行条件：

- 已安装 Python 3
- 仓库依赖已安装完成
- 如仓库使用本地 embedding 服务，则该服务已可用
- `/mnt/skills/custom/policies-regulations/policy-rag/scripts` 下脚本可正常执行

在新环境首次运行，或用户反馈环境异常时，可先执行环境检查：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/check_env.py
```

---

## 六、输入解析顺序

### 1. 当用户要求处理文件时
按以下顺序解析输入文件：

1. 当前对话上传的文件
2. `/mnt/user-data/uploads`
3. 用户明确提供的绝对路径
4. `/mnt/datasets/policies-regulations/policy-rag/raw`

### 2. 当用户要求检索已有知识库时
按以下顺序解析数据源：

1. 用户明确提供的索引目录或 flows 目录
2. `/mnt/datasets/policies-regulations/policy-rag/index`
3. `/mnt/datasets/policies-regulations/policy-rag/flows`

---

## 七、工作流选择规则

必须根据用户任务类型，选择**唯一匹配**的工作流。

---

### A. 环境检查

适用情况：

- 新部署后首次运行
- 用户反馈脚本无法运行
- 检索、索引、embedding 等步骤异常
- 需要确认运行环境是否完整

执行命令：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/check_env.py
```

---

### B. 制度文档拆分

适用情况：

- 用户要求拆分制度文档
- 用户上传的是 Markdown / DOC / DOCX 等制度文件
- 用户希望按章节拆分后再索引

优先命令：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/rag_system.py split "<input_file>" "<output_dir>"
```

备用命令：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/split_doc.py "<input_file>" "<output_dir>"
```

默认输出目录：

```text
/mnt/datasets/policies-regulations/policy-rag/processed
```

---

### C. 审批 Excel 转换

适用情况：

- 用户上传审批表、审批权责表、流程 Excel
- 用户要求将审批表转为结构化流程数据
- 后续需要对审批路径进行检索

优先命令：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/rag_system.py convert "<excel_file>" "<output_dir>"
```

备用命令：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/convert_excel.py "<excel_file>" "<output_dir>"
```

默认输出目录：

```text
/mnt/datasets/policies-regulations/policy-rag/flows
```

---

### D. 制度索引构建或重建

适用情况：

- 用户明确要求构建索引
- 用户明确要求重建索引
- 制度文档刚拆分完成，需要建立检索索引
- 当前索引目录不存在

执行命令：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/rag_system.py index "<docs_dir>" "<index_dir>"
```

默认参数：

- `docs_dir`：`/mnt/datasets/policies-regulations/policy-rag/processed`
- `index_dir`：`/mnt/datasets/policies-regulations/policy-rag/index`

---

### E. 制度条款检索

适用情况：

- 用户在问某一项制度规定写在哪里
- 用户在找某个比例、条件、限制、范围、例外、要求
- 用户关注的是制度正文内容，而不是审批路径本身

执行命令：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/rag_system.py search-docs "<query>" "<index_dir>"
```

默认索引目录：

```text
/mnt/datasets/policy-rag/index
```

---

### F. 审批流程检索

适用情况：

- 用户在问“怎么审批”
- 用户在问“走哪个分支”
- 用户在问“不同金额对应哪条审批路径”
- 用户在问“由谁审批”
- 用户在问“哪个流程适用当前事项”

优先命令：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/search_flows.py "<query>" --flows-dir "/mnt/datasets/policy-rag/flows"
```

可选统一入口：

```bash
cd /mnt/skills/custom/policies-regulations/policy-rag && python3 scripts/rag_system.py search "<query>"
```

---

## 八、默认操作模式

### 模式 1：用户上传制度文件，并要求做成可检索
执行顺序：

1. 拆分文档
2. 构建索引
3. 如用户同时提出问题，再执行制度检索

---

### 模式 2：用户上传审批 Excel，并询问审批流程
执行顺序：

1. 转换 Excel
2. 检索审批流程

---

### 模式 3：用户直接询问制度条款，且索引已存在
执行顺序：

1. 制度条款检索

---

### 模式 4：用户直接询问审批路径，且流程数据已存在
执行顺序：

1. 审批流程检索

---

## 九、回答规则

完成检索后，回答应遵循以下顺序：

### 对于制度条款类问题
1. 先给出直接结论
2. 再给出命中的制度章节、条款或文本片段
3. 若存在多个相近命中项，应说明最相关项与备选项
4. 若检索结果不确定，应明确说明“不确定”或“当前结果置信度有限”

### 对于审批流程类问题
1. 先说明匹配到的审批路径
2. 再说明触发该路径的条件
3. 如存在多个审批分支，应清晰列出各分支适用条件
4. 不得虚构审批人、金额门槛、审批层级或分支条件

---

## 十、失败处理规则

### 1. 输入文件不存在
必须明确报告缺失的具体路径。

### 2. 索引目录不存在
如果用户要求检索制度内容，但索引不存在，应先构建索引，而不是假装检索成功。

### 3. flows 目录不存在
如果用户要求检索审批路径，但流程数据不存在，应明确说明审批流数据尚未准备好。

### 4. 脚本执行报错
必须提取并报告关键报错信息，停止虚构后续结果。

### 5. 问题越界
如果用户问题已经越出企业制度/审批流程范围，应切换到更合适的技能，而不是强行继续使用本技能。

---

## 十一、输出格式要求

### 对于拆分、转换、索引任务
输出中应至少包含：

- 输入路径
- 输出路径
- 实际执行的命令
- 是否执行成功
- 下一步建议

### 对于检索任务
输出中应至少包含：

- 直接答案
- 支撑该答案的命中结果
- 如有必要，给出章节名、流程分支名或关键条件
- 若未命中，明确说明当前知识库未返回可靠结果

---

## 十二、执行原则总结

本技能是一个**严格脚本驱动**的企业内部制度与审批流程处理技能。

应始终坚持以下原则：

- 先识别任务类型，再选工作流
- 先检索，再作答
- 先依据脚本结果，再下结论
- 只处理企业制度和审批流程，不越界处理法律法规问题
- 失败时明确报错，不编造结果
