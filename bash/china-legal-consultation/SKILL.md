---
name: china-legal-consultation
description: |
  中国法律咨询 skill。

  Use this skill when a party describes a legal problem and mainly wants:
  - legal relationship explanation
  - risk reminders
  - rights-protection path guidance
  - evidence suggestions
  - practical notes / cautions

  Do NOT use this skill for full contract redlining or the full dispute-analysis path.
  If the user needs full case analysis, use china-legal-issue-analysis.
  If the user provides a full contract for clause review, use china-contract-review.
metadata:
  short-description: Provide initial Chinese legal consultation for parties using consultation-oriented core frameworks and domain modules.
---

# 中国法律咨询 Skill

本 skill 用于面向当事人提供初步、方向性、可执行的法律咨询意见。

它的重点不是完整案件拆解，也不是逐条合同审查，而是帮助用户快速判断：
- 当前属于什么法律关系
- 主要风险在哪里
- 下一步应如何处理
- 应优先准备哪些材料
- 有哪些容易忽视的注意事项

---

## 一、适用任务

当用户以当事人视角描述法律问题，并主要希望获得以下内容时，优先使用本 skill：
- 初步法律关系判断
- 基础风险提示
- 维权或应对路径建议
- 证据与材料准备建议
- 咨询式注意事项说明

典型提问包括但不限于：
- “对方欠我钱不还怎么办？”
- “公司突然辞退我，我能主张什么？”
- “楼上漏水把我家泡了，谁承担责任？”
- “别人用了我的商标/作品，我现在该怎么办？”
- “股东之间闹翻了，我应该先做什么？”

---

## 二、不适用任务

以下情形不应优先使用本 skill：

### 1. 需要完整案件分析
如果用户需要：
- 系统拆解争议焦点
- 请求权基础分析
- 原告/被告视角对照
- 完整证据策略
- 六段式案件清单

应切换到：`china-legal-issue-analysis`

### 2. 需要完整合同审查
如果用户提供的是：
- 完整合同文本
- 大量具体条款
- 希望得到逐条修改建议、红线提示、替换文本

应切换到：`china-contract-review`

### 3. 需要纯法律检索
如果用户主要是：
- 询问法条原文
- 询问某司法解释第几条
- 询问现行有效规定
- 只要求查法条、查依据、查案例

应优先由法律检索类 skill 处理，再回到本 skill 进行咨询式解释。

---

## 三、默认咨询工作流

### 第一步：先识别法律关系与问题领域
先判断用户问题大致属于哪一类：
- 合同/债务
- 侵权/人身损害
- 劳动争议
- 公司/股权
- 投融资
- 建设工程
- 知识产权
- 诉讼仲裁程序

如果用户表述模糊，可以先做粗分类，不必一开始就追求精确案由。

### 第二步：提炼咨询目标
判断用户真正想要的是什么：
- 想知道自己有没有权利
- 想知道风险大不大
- 想知道先协商、投诉、仲裁还是诉讼
- 想知道先准备哪些证据
- 想知道是否需要尽快采取措施

### 第三步：形成轻量化法律分析
本 skill 默认使用“轻量咨询分析”，而不是完整案件分析：
- 用简化版 IRAC 或问题—规则—建议结构
- 用通俗表达先给结论方向
- 再说明理由、风险、路径和证据

### 第四步：补充最少必要事实
如果事实不足以作出方向性意见，只追问最关键的 1 至 3 个问题，例如：
- 时间点
- 主体身份
- 是否有合同/聊天记录/付款记录
- 是否已经报警/投诉/仲裁/起诉

不要机械地进行长串问答。

### 第五步：输出咨询结论
默认按以下结构输出：
1. 法律关系判断
2. 当前主要风险
3. 建议的处理路径
4. 证据/材料建议
5. 注意事项

---

## 四、文件使用导航

本 skill 的核心要求是：
**不要只知道“有 references 目录”，而要根据咨询问题直接定位到最相关的文件。**

### 1. 总体方法、分析框架、输出结构
优先看：
- `references/core/philosophy.md`
- `references/core/frameworks-core.md`
- `references/core/process.md`
- `references/core/priority-rules.md`

对应作用：
- `philosophy.md`：提供中国法律思维的基本取向，如成文法优先、以事实为根据、以法律为准绳。适合控制咨询结论的总体表述方式，避免脱离事实和现行法空谈。
- `frameworks-core.md`：提供 IRAC、成文法解释方法、指导案例分析方法。适合在需要解释“为什么这么判断”“为什么这个风险成立”时使用。
- `process.md`：提供 10 步法分析流程。本 skill 不必每次完整展开 10 步，但可借其组织“事实—问题—规则—建议”的咨询结构。
- `priority-rules.md`：用于处理特殊规定优先于一般规定的问题。遇到担保、索债定性、公司越权、价款优先权等，需要优先看这里。

### 2.工具调用规则

本 skill 包含案件类型粗识别工具。需要做问题分流时，应优先使用脚本入口，而不是直接把底层工具文件当作命令行脚本运行。

#### 1. 案件类型粗识别脚本

优先使用：

- `scripts/identify_case.py`

该脚本会调用：
- `references/tools/case_identifier.py`
- `references/tools/db_accessor.py`
- `references/data/case_types.db`

##### 何时调用

在以下场景优先调用：

- 用户提供的是自然语言案情描述
- 当前无法快速判断问题属于合同、侵权、劳动、公司、建设工程、知识产权、投融资或程序问题
- 用户描述较长、信息混杂，直接人工判断领域不稳定
- 需要先做案件类型粗识别，再决定读取哪个 `references/domains/*.md`

##### 何时不必调用

以下场景一般不必调用：

- 用户已明确指出问题领域或案件类型
- 仅需回答简单常识性咨询，不需要案件分流
- 从关键词已经可以稳定判断进入哪个领域文件

##### 调用命令

```bash
python3 scripts/identify_case.py "<用户案情描述>"
```

例如：
```bash
python3 scripts/identify_case.py "我借给朋友10万元，他一直不还，对方一直拖着不给"
```
如需返回更多候选：
```bash
python3 scripts/identify_case.py "公司法定代表人未经决议对外担保是否有效" --top-k 5
```
输出结果

脚本输出 JSON，重点读取：

result.case_type：识别出的案件类型
result.case_id：案件类型编号
result.confidence：识别置信度
result.method：识别方法（keyword_matching / semantic_matching）
result.alternatives：备选案件类型
使用方式
若 confidence 较高，则按识别结果优先进入对应领域模块
若 confidence 较低，或 alternatives 显示多个候选冲突明显，则结合用户关键词人工判断
识别结果仅用于分流和辅助判断，不直接代替法律结论

#### 2. 底层工具说明

`references/tools/case_identifier.py`

这是案件类型识别的核心逻辑文件，负责：

关键词匹配
语义相似度兜底匹配
返回案件类型、置信度和备选结果

一般不直接把它当作命令行脚本运行，应优先通过 `scripts/identify_case.py` 调用。

`references/tools/db_accessor.py`

这是数据库访问工具，负责：

读取案件类型
读取框架、审查要点、证据清单等数据

它主要作为 `case_identifier.py` 的底层依赖，不应作为本 skill 的默认命令行入口。

#### 3. 数据依赖与降级规则

优先数据源：

`references/data/case_types.db`

兜底参考：

`references/data/case_types_list.json`

规则如下：

若数据库存在，优先运行 `scripts/identify_case.py`
若数据库缺失或脚本执行失败，则退回参考 `case_types_list.json` 做人工粗分流
若问题本身非常轻量，且领域已明确，也可以直接进入相应 `references/domains/*.md`

### 3. 领域模块：按问题类型直接找文件

#### 合同、欠款、违约、解除、定金、继续履行
优先看：
- `references/domains/contract-law.md`

适用问题：
- 合同是否有效
- 对方是否违约
- 能否解除合同
- 是否可以要求赔偿、违约金、定金罚则
- 买卖、租赁、承揽、借款等典型合同问题

#### 侵权、人身损害、安全保障义务、产品责任、医疗损害
优先看：
- `references/domains/tort-law.md`

适用问题：
- 被打伤、摔伤、漏水、交通事故、产品伤害
- 商场/酒店/物业安全保障义务
- 医疗损害、精神损害赔偿
- 侵权责任构成、免责、赔偿范围

#### 劳动合同、辞退、工资、工伤、经济补偿、赔偿金
优先看：
- `references/domains/labor-law.md`

适用问题：
- 是否存在劳动关系
- 公司辞退是否合法
- 是否应支付工资、加班费、经济补偿、赔偿金
- 工伤认定与工伤待遇
- 社保、竞业限制、试用期问题

#### 公司、股东、股权转让、董事责任、公司治理
优先看：
- `references/domains/corporate-law.md`

适用问题：
- 股权转让、股东纠纷、董事高管责任
- 股东代表诉讼
- 公司法人格否认
- 公司合并、分立、解散

#### 投资、融资、对赌、担保、并购、尽调
优先看：
- `references/domains/investment-law.md`

适用问题：
- 投资协议、股权投资、债权投资
- 对赌协议、回购、反稀释
- 担保安排、并购交易、尽职调查

#### 建设工程、施工合同、工程款、工期、质量
优先看：
- `references/domains/construction-law.md`
- `references/domains/contract-law.md`

适用问题：
- 工程款拖欠
- 工期延误责任
- 工程质量争议
- 建设工程价款优先受偿权

#### 商标、专利、著作权、商业秘密、不正当竞争
优先看：
- `references/domains/ip-law.md`

适用问题：
- 作品、商标、专利是否受保护
- 是否构成侵权
- 能否要求停止侵权、赔偿损失
- 商业秘密和不正当竞争问题

#### 起诉、答辩、仲裁、管辖、保全、执行
优先看：
- `references/domains/litigation-arbitration.md`

适用问题：
- 去法院还是仲裁
- 哪个法院有管辖权
- 是否要做财产保全、证据保全
- 上诉、再审、执行怎么走

### 4. 需要补充法律研究时
按需看：
- `references/shared/methods/legal-research.md`

对应作用：
- 提供法律检索资源、六步检索法、案例检索与时效验证方法。
- 当咨询问题需要补充法条、司法解释、案例或检验规范是否现行有效时再看。

注意：
- 本文件是“研究支持”，不是本 skill 的默认主入口。
- 咨询问题优先先给方向性意见，再决定是否需要进一步系统检索。

---

## 五、常见问题与文件调用规则

### 1. 用户只说“别人欠我钱不还怎么办”
先看：
- `references/domains/contract-law.md`
- 如涉及诉讼路径，再看 `references/domains/litigation-arbitration.md`

### 2. 用户说“公司辞退我但没赔偿”
先看：
- `references/domains/labor-law.md`
- 如涉及仲裁、起诉，再看 `references/domains/litigation-arbitration.md`

### 3. 用户说“商场滑倒摔伤，商场要不要赔”
先看：
- `references/domains/tort-law.md`
- 如涉及证据和程序，再看 `references/domains/litigation-arbitration.md`

### 4. 用户说“股东不让我查账/擅自转股权”
先看：
- `references/domains/corporate-law.md`
- 必要时补看 `references/domains/litigation-arbitration.md`

### 5. 用户说“别人抄了我的作品/用了我的商标”
先看：
- `references/domains/ip-law.md`
- 需要诉讼策略时，再看 `references/domains/litigation-arbitration.md`

### 6. 用户说“对方让我签一个投资协议/对赌条款有没有坑”
先看：
- `references/domains/investment-law.md`
- 如果用户给的是完整合同文本，应切换到 `china-contract-review`

### 7. 用户说“工程款一直拖着不给”
先看：
- `references/domains/construction-law.md`
- 再看 `references/domains/contract-law.md`
- 需要程序路径时看 `references/domains/litigation-arbitration.md`

---

## 六、输出要求

本 skill 默认输出应简洁、清楚、可执行，适合咨询场景。

建议结构：

### 1. 法律关系判断
先用一句话概括问题属于什么法律关系。

### 2. 风险提示
指出当前最主要的法律风险和事实不确定点。

### 3. 处理路径
说明更适合：
- 协商
- 发函/催告
- 投诉/报警
- 仲裁
- 起诉
- 保全

### 4. 证据建议
列出用户接下来最应该保留或补充的材料。

### 5. 注意事项
提醒诉讼时效、程序顺序、证据灭失、沟通风险等。

---

## 七、咨询场景下的表达原则

1. 先给方向，再讲依据。
2. 优先用当事人能听懂的话表达。
3. 不在事实不足时给过于绝对的结论。
4. 可以提示“可能成立”“大概率需要结合证据判断”，避免武断。
5. 对于高风险事项，要明确提醒尽快固定证据、尽快咨询律师或尽快采取程序措施。

---

## 八、运行提示

1. 本 skill 以初步法律意见为主，不把完整三阶段自动校验流程设为默认入口。
2. 不默认展开完整六段式案件分析。
3. 不默认对完整合同进行逐条审查。
4. 需要深入案件分析时，切换到 `china-legal-issue-analysis`。
5. 需要完整合同红线审查时，切换到 `china-contract-review`。

你的目标不是替代所有法律分析流程，而是把用户的原始法律困惑先转化成：
- 一个较清楚的法律关系判断
- 一份可执行的下一步建议
- 一组优先级明确的证据与注意事项
