---
name: china-legal-issue-analysis
description: |
  中国法律问题分析 skill。

  Use this skill for concrete Chinese legal issues, dispute analysis,
  issue spotting, legal relationship analysis, risk assessment,
  litigation/arbitration positioning, and action planning.

  Core capabilities:
  - case type identification
  - six-part checklist generation
  - 10-step legal analysis process
  - IRAC / claim-right / issue-based analysis
  - domain-specific issue analysis
  - legal citation verification and revision

  Do NOT use this skill as a dedicated contract redlining skill.
  If the primary input is a full contract text that needs clause-by-clause review,
  use china-contract-review instead.

  If the user only needs a lightweight initial answer as a party to a dispute,
  use china-legal-consultation instead.
metadata:
  short-description: Analyze concrete Chinese legal issues with directed file selection, case typing, checklist generation, and legal verification.
---

# 中国法律问题分析 Skill

本 skill 用于处理**具体案件事实、争议经过、法律问题、法律依据适用、风险评估、诉讼/仲裁思路与行动建议**。

它不是一个“遍历整个 references/ 目录再慢慢找材料”的 skill，而是一个**按任务类型定向选择子目录和脚本**的 skill。

## 何时使用

当用户提供以下任一内容时，优先使用本 skill：
- 案件事实或争议经过
- 想判断法律关系、责任承担、请求权基础、抗辩空间
- 想识别案件类型，再进入进一步分析
- 想根据案件类型生成要件事实/审查清单
- 想判断某个观点是否引用了过期法律或错误版本
- 想按中国法方法做 IRAC、请求权基础、争议焦点分析

典型任务：
- 案件类型识别
- 法律关系梳理
- 争议焦点提炼
- 请求权基础与抗辩分析
- 要件事实匹配
- 法律风险评估
- 诉讼/仲裁行动建议
- 法律引用校验与修正

## 何时不要用

以下情况不应优先使用本 skill：
- 用户提供完整合同文本，要求逐条审查、标注风险、给出修改建议
- 用户只想获得面向当事人的轻量、快速、低结构化咨询答复
- 用户主要是要“检索法条原文/案例原文”，而不是在已有事实基础上做结构化分析

对应协作：
- 合同逐条审查 -> `china-contract-review`
- 轻量法律咨询 -> `china-legal-consultation`
- 专门法条/案例检索 -> 优先交给专门检索 skill

## 强制规则

1. **禁止无差别遍历 `references/`。**
   先判断任务类型，再只打开最少必要文件。

2. **先做路由，再读文件。**
   先判断当前任务属于：
   - 核心分析方法
   - 领域专题分析
   - 案件类型识别
   - 要件清单生成
   - 司法解释定位
   - 法律时效/版本校验

3. **优先读索引文件，再读实体文件。**
   例如：
   - 司法解释先看 `references/interpretations/metadata.json`
   - 案件类型先用数据库/清单，不要先翻各领域文档

4. **脚本调用必须用明确命令，不要只写“参考某个 .py”。**
   本 skill 中的若干脚本没有完善的 CLI 参数接口，
   因此应使用下面写明的 `python - <<'PY'` 方式调用类和方法，
   而不是直接运行其演示代码作为正式工作流。

5. **数据库优先于 JSON 清单。**
   当前包内已经存在：
   - `references/data/case_types.db`
   - `references/data/case_types_list.json`

   若需要案件类型识别、六段式框架、审查要点等结构化能力，优先使用 `case_types.db`。
   `case_types_list.json` 仅作为数据库不可用时的降级参考。

6. **遇到目录内文档的上游失效引用，不要被误导。**
   某些 README 里提到的上游文件在当前拆分包中并不存在；
   只使用当前 skill 实际存在的文件。

## 目录总览与定向选择规则

### 1. `references/core/` —— 核心方法文件

只在需要“法律分析方法”时读取，不要把它当成领域知识库通读。

- `references/core/philosophy.md`
  - 用途：总原则、成文法优先、以事实为根据、以法律为准绳
  - 适合：确定分析基调、控制结论表述、说明裁判/分析取向

- `references/core/frameworks-core.md`
  - 用途：IRAC、成文法解释、指导案例参照、论证结构
  - 适合：需要结构化分析、Issue/Rule/Application/Conclusion 输出时

- `references/core/process.md`
  - 用途：10 步法，从事实收集到行动建议
  - 适合：需要完整办案路径、分析流程、操作步骤时

- `references/core/priority-rules.md`
  - 用途：特别规定优先于一般规定、特殊规则优先适用
  - 适合：存在一般法/特别法冲突，或一般规则/专项司法解释冲突时

**核心文件选择规则：**
- 普通法律问题分析：`frameworks-core.md` + `process.md`
- 要强调中国法总原则：再加 `philosophy.md`
- 涉及特殊规则优先：再加 `priority-rules.md`
- 不要默认四个全读；至少先根据任务选 2 个，再按需要追加

### 2. `references/domains/` —— 领域模块

只根据争议主题定向读取一个或两个模块；不要把所有领域模块都打开。

- `contract-law.md`
  - 关键词：合同、协议、违约、解除、撤销、无效、可撤销、违约金、定金、赔偿损失

- `tort-law.md`
  - 关键词：侵权、损害赔偿、安全保障义务、产品责任、医疗损害、精神损害

- `construction-law.md`
  - 关键词：建设工程、施工合同、工程款、工期延误、工程质量、优先受偿权、竣工验收

- `corporate-law.md`
  - 关键词：公司、股东、股权转让、董事、监事、高管、股东会、董事会、公司治理

- `investment-law.md`
  - 关键词：投资、融资、对赌、担保、股权投资、债权投资、尽调、并购、IPO

- `labor-law.md`
  - 关键词：劳动合同、工资、辞退、解除、经济补偿、赔偿金、工伤、社保、加班

- `ip-law.md`
  - 关键词：著作权、商标、专利、商业秘密、不正当竞争、知识产权许可/转让

- `litigation-arbitration.md`
  - 关键词：诉讼、仲裁、管辖、证据、举证责任、起诉、答辩、保全、执行

**领域文件选择规则：**
- 只选最匹配的 1 个主领域文件
- 如问题天然跨领域，最多加 1 个辅助领域文件
- 常见组合：
  - 合同 + 担保/投资 -> `contract-law.md` + `investment-law.md`
  - 公司 + 对外担保/股东纠纷 -> `corporate-law.md` + `investment-law.md`
  - 工程款/质量争议 -> `construction-law.md` + `contract-law.md`
  - 劳动争议 + 程序问题 -> `labor-law.md` + `litigation-arbitration.md`
  - 知识产权侵权 + 合同许可 -> `ip-law.md` + `contract-law.md`

### 3. `references/interpretations/` —— 司法解释索引

先看总索引，再决定是否进入具体子目录。

- `references/interpretations/metadata.json`
  - 用途：当前有哪些司法解释索引、关键词映射、版本信息
  - 这是进入本目录的**第一入口**

当前可定向进入的子目录：
- `references/interpretations/contract-general-2023/`
  - 适用：预约合同、越权代表、违反强制性规定、无权处分、违约金调整、以物抵债等
  - 先读：`README.md`
  - 再读：`index.md`

- `references/interpretations/security-law-2020/`
  - 适用：保证、担保、公司对外担保决议、抵押财产转让、价款优先权 PMSI 等
  - 先读：`README.md`
  - 再读：`index.md`

**司法解释目录选择规则：**
1. 先读 `metadata.json` 看关键词映射和已有解释 ID
2. 再进入命中的具体解释目录
3. 先读对应 `README.md` 获取“该解释解决什么问题”
4. 需要条文索引时再读 `index.md`
5. 不要在两个解释目录之间反复来回，除非争点确实跨越

### 4. `references/shared/` —— 通用补充模块

- `references/shared/methods/legal-research.md`
  - 用途：法律、法规、案例、实务资源的检索路径与方法
  - 适合：需要说明“接下来该去哪里检索官方文本/案例/数据库”时

- `references/shared/verification/automated-checklist.md`
  - 用途：自动化法律校验的触发条件、流程、校验逻辑
  - 适合：需要检查法律是否更新、是否可能用错版本、是否要反思修正时

**shared 目录选择规则：**
- 需要“检索方法”时读 `legal-research.md`
- 需要“法律版本/时效/适用性校验”时读 `automated-checklist.md`
- 不是所有分析都要读 shared 目录

### 5. `references/data/` —— 结构化数据

- `references/data/case_types.db`
  - 用途：案件类型、六段式框架、审查要点等结构化数据
  - 适合：案件类型识别、清单生成、按 case_id 调框架和要点

- `references/data/case_types_list.json`
  - 用途：降级版案件类型清单
  - 适合：数据库脚本不可用时，人工查看可选案件类别

- `references/data/README.md`
  - 用途：上游说明
  - 注意：其“数据库可能不存在”的提示与当前包不一致；当前 zip 中数据库实际存在

### 6. `references/tools/` —— 可调用脚本与支持模块

区分“直接调用入口”和“仅供支持”。

**建议直接调用的入口：**
- `references/tools/case_identifier.py`
  - 用途：案件类型识别
- `references/tools/checklist_generator.py`
  - 用途：根据 case_id 和角色生成要件清单
- `references/tools/automated_verification.py`
  - 用途：对初步法律意见做引用提取、更新检查、适用性判断、修正建议

**支持模块，不要单独当主要入口使用：**
- `references/tools/db_accessor.py`
  - 用途：数据库访问封装
- `references/tools/checklist_framework.py`
  - 用途：角色与六段式框架定义

## 推荐任务路由

### 路由 A：用户给了事实，想做普通法律分析

按以下顺序选择：
1. `references/core/frameworks-core.md`
2. `references/core/process.md`
3. 选择 1 个最相关的 `references/domains/*.md`
4. 如存在特殊规则优先问题，再加 `references/core/priority-rules.md`
5. 如涉及特定司法解释争点，再进入 `references/interpretations/metadata.json` 后选解释目录

### 路由 B：用户先问“这是什么案件/属于什么纠纷”

按以下顺序：
1. 优先调用 `case_identifier.py`
2. 如识别结果置信度较高，用返回的 `case_id` 进入下一步分析
3. 如置信度较低，再人工参考 `case_types_list.json` 做补充判断
4. 之后再按领域读取相应 `domains/*.md`

### 路由 C：用户想要“要件、证据、争点、原告/被告应准备什么”

按以下顺序：
1. 先确认或识别 `case_id`
2. 调用 `checklist_generator.py`
3. 根据角色选择：`plaintiff` / `defendant` / `neutral`
4. 输出六段式或角色化审查清单
5. 如需分析方法补充，再读 `frameworks-core.md` 或 `process.md`

### 路由 D：用户争点明显落在合同编通则解释或担保制度解释

按以下顺序：
1. 先读 `references/interpretations/metadata.json`
2. 命中后进入对应子目录 `README.md`
3. 再读 `index.md`
4. 如需要再补 `contract-law.md` / `corporate-law.md` / `investment-law.md`

### 路由 E：用户已经写出法律分析意见，想检查是否引用过期法规

按以下顺序：
1. 读 `references/shared/verification/automated-checklist.md`
2. 读 `references/interpretations/metadata.json`
3. 调用 `automated_verification.py`
4. 根据输出中的 `issues_found` 和 `updated_opinion` 做修正说明

## 精确脚本调用命令

下面命令是本 skill 中建议写入并实际使用的**明确调用命令**。

### 1. 案件类型识别：`case_identifier.py`

**用途**：根据用户案情描述，返回 `case_type`、`case_id`、`confidence`、`method`。

**工作目录**：skill 根目录

**调用命令模板：**

```bash
cd /path/to/china-legal-issue-analysis && python - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path('references/tools').resolve()))
from case_identifier import CaseIdentifier

user_input = "我借给朋友10万元，他一直不还"
db_path = str(Path('references/data/case_types.db').resolve())

identifier = CaseIdentifier(db_path)
result = identifier.identify(user_input, top_k=3)
print(result)
PY
```

**使用规则：**
- 先用于“案件类型不明确”的输入
- 若 `confidence` 较高，可直接使用返回的 `case_id`
- 若 `confidence` 较低，再结合 `case_types_list.json` 和领域文档人工补判

### 2. 要件清单生成：`checklist_generator.py`

**用途**：根据已知 `case_id` 和角色生成结构化清单。

**工作目录**：skill 根目录

**调用命令模板：**

```bash
cd /path/to/china-legal-issue-analysis && python - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path('references/tools').resolve()))
from checklist_generator import ChecklistGenerator
from checklist_framework import UserRole

case_id = 7
user_role = UserRole.NEUTRAL  # 可改为 UserRole.PLAINTIFF / UserRole.DEFENDANT

db_path = str(Path('references/data/case_types.db').resolve())
generator = ChecklistGenerator(db_path)
checklist = generator.generate(case_id=case_id, user_role=user_role)
print(generator.format_markdown(checklist))
PY
```

**角色选择规则：**
- 原告视角：`UserRole.PLAINTIFF`
- 被告视角：`UserRole.DEFENDANT`
- 中立完整视角：`UserRole.NEUTRAL`

### 3. 数据库直接查询：`db_accessor.py`

**用途**：需要直接查看案件类型、框架、统计信息时使用。

**工作目录**：skill 根目录

**调用命令模板（查看案件类型详情）：**

```bash
cd /path/to/china-legal-issue-analysis && python - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path('references/tools').resolve()))
from db_accessor import get_db_accessor

db = get_db_accessor(str(Path('references/data/case_types.db').resolve()))
case_info = db.get_case_type(7)
print(case_info)
PY
```

**调用命令模板（搜索关键词对应案件类型）：**

```bash
cd /path/to/china-legal-issue-analysis && python - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path('references/tools').resolve()))
from db_accessor import get_db_accessor

db = get_db_accessor(str(Path('references/data/case_types.db').resolve()))
results = db.search_case_types_by_keyword("借贷")
print(results)
PY
```

### 4. 自动化法律校验：`automated_verification.py`

**用途**：对初步法律意见进行法规引用提取、更新检查、新旧法适用分析、修正输出。

**注意**：该脚本内部使用相对路径 `interpretations/metadata.json`，
因此建议在 **`references/` 目录下执行**。

**工作目录**：`references/`

**调用命令模板：**

```bash
cd /path/to/china-legal-issue-analysis/references && python - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path('tools').resolve()))
from automated_verification import AutomatedLegalVerification

legal_opinion = """
本案涉及《中华人民共和国公司法》(2018年修正)第二十条。
案件事实发生于2024年8月15日。
"""

verifier = AutomatedLegalVerification()
result = verifier.verify(legal_opinion=legal_opinion, fact_date="2024-08-15")
print(result['verification_report'])
print(result['issues_found'])
print(result['updated_opinion'])
PY
```

**使用规则：**
- 当分析中出现具体法律名称、年份、司法解释文号时优先考虑校验
- 尤其适用于公司法、民诉法、劳动合同法等存在版本更新风险的问题
- 如案件事实发生在新旧法切换附近，更应调用

## 实际工作顺序建议

### 模式 1：先识别，再分析
适用于案情模糊、案件类型不明的输入。

顺序：
1. 调 `case_identifier.py`
2. 必要时用 `db_accessor.py` 查看该 `case_id` 的详细信息
3. 读取对应领域文档
4. 用 `frameworks-core.md` + `process.md` 输出分析
5. 需要清单时再调 `checklist_generator.py`

### 模式 2：已知领域，直接分析
适用于用户已经明确说是合同、劳动、公司、侵权等争议。

顺序：
1. 读取 1 个最匹配的领域文档
2. 读取 `frameworks-core.md`
3. 需要完整办案路径时追加 `process.md`
4. 涉及司法解释时进入 `interpretations/`
5. 涉及时效/版本问题时做 `automated_verification.py`

### 模式 3：先出初步意见，再校验修正
适用于较长法律分析输出。

顺序：
1. 先用 core + domain 输出初步分析
2. 若引用了具体法规/司法解释，调用 `automated_verification.py`
3. 根据 `issues_found` 修正表述
4. 在最终答案中交代“已做版本与适用性复核”

## 输出要求

使用本 skill 输出时，应尽量包含以下结构：
- 事实与争议概括
- 案件类型或法律关系判断
- 争议焦点
- 适用规则
- 要件匹配/抗辩分析
- 风险判断
- 建议行动方案

若调用了脚本，可在内部工作流中使用脚本结果，但对用户输出时应转化为自然语言分析，不要只粘贴原始字典。

## 重要提醒

- `case_identifier.py`、`checklist_generator.py`、`automated_verification.py` 才是主要可调用入口
- `db_accessor.py` 和 `checklist_framework.py` 主要是支持模块
- 不要把 `python xxx.py` 的测试输出当作正式调用方式；应使用本文件中给出的明确命令模板
- 只根据当前任务读取必要子目录，不要扫描整个 skill
