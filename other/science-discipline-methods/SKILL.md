---
name: science-discipline-methods
description: Use when a research question is still a question rather than a plan — when you know the field but not which study design the field accepts, how many samples it demands, which measurements count as evidence, or which software is standard; also use when a review came back saying the design cannot answer the question, when you are switching fields or advising a student in an unfamiliar one, when two supervisors disagree about method, or when you need to know what reviewers in that field attack first before you commit months to a protocol.
---

# 学科方法库：先定设计，再谈统计

## 这一层解决什么问题

一个研究生最常见的卡点不是「不会做统计」，而是**问错了问题类型**。

他手里有一个现象、一份数据、一个想说的话，但不知道这个领域**用什么方式把现象变成证据**。
心理学靠随机分配与操纵检查，经济学靠外生变异与平行趋势，化学靠表征链，材料靠批次与标准，
机器学习靠多种子与强基线——同样是「证明 A 影响 B」，各领域要求的证据形态完全不同。

所以这一层的产出不是结论，是**这个领域公认的走路方式**：
能问什么、用哪个设计、要多少样本、量什么、跑什么方法、装什么软件、审稿人先打哪里。

## 入口

```
science_discipline_list {}                                  # 有哪些学科包
science_discipline_profile { domain: "biomed" }             # 某个学科的全貌
science_discipline_profile { question: "我想用 fMRI 研究注意力的神经机制" }   # 只有问题也行
science_discipline_profile { design: "重复测量" }            # 反向查：哪些领域有这个范式
science_discipline_profile { tool: "RDKit" }                # 反向查：这软件在哪个领域是标准
science_discipline_profile { journal: "nature" }            # 只知道要投哪
```

`domain` 可以给 id、中文名、英文名，或者整段研究问题——匹配器按
「显式 → 期刊族 → 别名精确 → 别名包含 → 关键词 → generic」六级降级，
并把 `matchedBy` / `confidence` / `candidates` 一起返回，让你知道它有多确定。

**generic 不是失败**，是诚实：没匹配上时不硬塞一个最近的学科，因为错误的学科包
会让后面每一步建议都错（样本量、默认校正方法、报告规范全都跟着错）。

## 一个学科包里有九样东西

| 字段 | 回答什么 | 什么时候必看 |
| --- | --- | --- |
| `questionTypes` | 这个领域能问哪几类问题，各需要什么前置 | 选题阶段 |
| `designs` | 有哪几种被接受的设计，各自的 `requires` / `nRule` / `threats` | 写方案前 |
| `measurements` | 量什么、单位、精度、伪迹来源、怎么校准 | 设计问卷/实验时 |
| `methods` | 分析方法的适用条件、`tool`、`pitfall` | 分析前 |
| `tools` | 装什么、`install`、`minimalScript`、是否离线、许可 | 开工第一天 |
| `statsDefaults` | 该领域的 α、校正方法、首选效应量 | 分析前 |
| `reviewerAttacks` | 审稿人会先打哪里，以及怎么挡 | 投稿前自检 |
| `benchmarks` | 顶刊的**方法学门槛** | 判断「我这够不够」 |
| `exemplarStructure` | Results 该按什么顺序写，图给几张 | 写作时 |

两个容易读错的地方：

1. **`benchmarks` 是门槛，不是中稿率。** 它写的是「顶刊在这个方法上通常要求到什么程度」
   （样本量、重复数、报告完整度）。任何把方法学门槛换算成录用概率的说法都是假的。
2. **`nRule` 给的是数字或公式，不是「建议适当增加」。** 因为模糊建议等于没建议——
   你没法拿「适当」去算样本量。

## 怎么用（四步）

### 第一步：把问题落到 `questionTypes` 上

如果你的问题不在任何一类里，通常意味着两种情况之一：问题还太模糊（"研究一下抑郁症"），
或者它其实是两个问题的拼接（"抑郁症的机制与治疗"）。先拆开，再各自归类型。

### 第二步：挑设计，看 `requires` 是否**全部**满足

`requires` 是合取，不是析取。RCT 要求随机化 **且** 分配隐藏 **且** 盲法 **且** 预设主结局——
缺一条，这个设计的证据等级就掉一档，而不是「打个折扣」。

`threats` 里每一条都给 `risk → mitigation` 配对：不是让你知道风险存在，是让你知道怎么挡。
如果某条 mitigation 你做不到，那它就不是风险而是**已知缺陷**，必须写进 Limitations。

### 第三步：用 `nRule` 反推样本量，而不是用惯例

包里每一处出现「每组 30」这类惯例数字，都同时给了它为什么不成立。
心理学的中位实际功效约 .50（Bakker et al. 2012），生医领域多数「每组 6 只」的动物实验
功效不足 50%——**惯例是错的，而且错得可测量**。

### 第四步：`reviewerAttacks` 当自检表用

投稿前逐条问自己「这条打得中我吗」。打中的，在正文里提前回答；
打不中的，确认是真的打不中，而不是你没想到。

## 与其他层的分工

- **science_search / science_journal_intel**：这个方向在做什么、投哪里 → 不解决「怎么做」
- **science_discipline_profile**（本层）：这个领域**怎么走路**
- **science_stats**（M6c）：具体跑哪个检验、假设满不满足、效应量多大
- **science_exp_plan**（M6b）：把关口落成你课题的可执行方案与样本量
- **science_reporting_standards**：写完了对着 CONSORT/PRISMA/STROBE 逐条打勾

顺序不能颠倒。先有设计，统计才有对象；先有门槛，才知道自己差多少。

## 常见误用

- **把学科包当投稿策略**：它是方法学门槛与审稿攻击清单，不是选刊建议。
- **只看 methods 不看 requires**：方法适用条件不满足时，跑出来的数字不是「稍弱」，是无效。
- **跨学科硬套**：把生医的 CONSORT 流程套到材料学论文上，会得到一份没有表征链的 Methods。
  换领域就换包，包里的 `why` 会告诉你为什么那条规矩在那个领域成立。
- **忽略 `reportingExternal`**：COBIDAS（脑影像）、ICH Q2（分析方法验证）、IEC 60904（光伏测量）
  这类外部标准本应用不做机器校验，但它们仍是投稿硬要求，不能因为「工具没查」就跳过。
