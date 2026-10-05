---
name: reducing-aigc-detection
description: Systematically reduce AIGC detection rates in academic papers (Chinese/English). Analyzes detection reports, identifies high-impact sections, applies multi-layer rewriting strategies preserving formatting/footnotes, and verifies results. Supports 维普/知网/Turnitin platforms.
user-invocable: true
allowed-tools: Bash, Read, Write, Edit, Agent, WebSearch, WebFetch
argument-hint: <docx-path> [--report <pdf-path>] [--platform weipu|cnki|turnitin] [--target <percentage>]
aliases: reduce-aigc, aigc-fix, lower-aigc
---

# 降AIGC · reducing-aigc-detection

> 检测器追的是统计均匀性，反检测的本质是重新注入人类写作天然的 variance 和 imperfection。

## 何时使用

| 场景 | 使用 | 说明 |
|------|------|------|
| AIGC 检测报告显示高于红线 | YES | 核心场景 |
| 论文提交前预防性降 AI | YES | 不需要检测报告 |
| 已有 AI 辅助写作的论文需要人性化 | YES | 最佳实践 |
| 纯人工写作但误判率高 | YES | 可针对性微调 |
| 想批量处理多份文件 | NO | 每篇需要定制化处理 |

## 核心原理

### 检测器三板斧

| 指标 | 含义 | AI 文本特征 | 人类文本特征 |
|------|------|------------|------------|
| Perplexity（困惑度） | 文本可预测性 | 极低（<30） | 中高（60-120） |
| Burstiness（突发性） | 句长变化幅度 | 极低，句长均匀 | 高，长短交替 |
| Token 概率分布 | high-prob token 占比 | >85% | <70% |

### 平台差异

| 平台 | 特殊机制 | 关键应对 |
|------|---------|---------|
| **维普** | 章节加权（摘要 1.8x，引言/结论 1.5x）；拼接预警（风格断层 +10-15%） | 优先改摘要；全文风格一致 |
| **知网** | 3.0+ 分析论证深度曲线；4.0 标注"结构工整度过高" | 制造浅→深螺旋节奏 |
| **Turnitin** | 2025.8 可识别 humanizer 工具痕迹 | 不用洗稿工具，手动改写 |

## 执行流程

### Phase 0: 侦察

1. 读取检测报告 PDF（如有），提取各章节 AIGC 占比
2. 如无报告，通读全文预判高风险段落
3. 按 AIGC 率 x 章节权重 排序，确定改写优先级

```
优先级 = AIGC率 × 章节字数 × 平台权重系数
```

### Phase 1: 分级定策

| AIGC 率 | 策略 | 改动幅度 |
|---------|------|---------|
| >80% | 整段重写 | 保留核心论点，彻底换表达 |
| 40-80% | 重点改写 | 换骨架、注入个人经验、打碎并列 |
| 20-40% | 局部手术 | 替换 AI 特征词、打断过渡链、加短句 |
| <20% | 微调或不动 | 仅修复明显 AI 模板词 |

### Phase 2: 改写执行

#### 改写层级（按效果排序）

**第一层：结构层（降 60-70%，最高优先）**

- 消灭「N个方面：第一…第二…第三…」并列模板
- 打破「背景→分析→结论」标准三段论
- 制造论证深度不均匀：核心论点厚写，次要一笔带过
- 长短句交替：穿插 5-10 字短句与 30-40 字长句
- 加入自我修正轨迹：「最初以为…后来发现…」

**第二层：词汇层（降 10-15%，配合第一层）**

中文 AI 高频触发词黑名单（必须替换或删除）：

```
值得注意的是 / 综上所述 / 不可否认 / 首先…其次…最后
研究表明 / 结果显示 / 此外 / 总之 / 不仅…而且
主要体现在N个方面 / 具有重要意义 / 发挥着重要作用
在…方面 / 与此同时 / 一方面…另一方面
```

英文 AI 高频触发词黑名单：

```
delve(s) / furthermore / moreover / it is important to note
comprehensive / multifaceted / nuanced / landscape / underscores
in conclusion / this report hopes to / integrates...with
The X section explains/introduces/presents/summarizes (mechanical parallelism)
```

替换策略：不是换同义词，是**换句式**。「研究表明X」→ 引具体作者年份样本量。

**第三层：内容注入（最难被检测）**

- 加入个人研究细节、田野观察、实验意外
- 引用对立观点的具体文献
- 补充具体数据、数字、表格
- 增加口语化学术表达碎片

#### 技术执行注意事项

**docx 编辑策略**：

| 段落类型 | 编辑方式 | 理由 |
|---------|---------|------|
| 无脚注/无特殊格式 | `replace_full_para()` — 设 Run 0 新文本，清空其余 | 安全快速 |
| 含脚注引用 [N] | Run 级替换 — 仅改非 superscript runs | 保留脚注 |
| 含 bold/italic 段中格式 | Run 级替换或 XML 层编辑 | 保留格式标记 |
| 含图表引用 | 仅改文字 runs，不动图表 XML | 防止引用断裂 |

**python-docx 段落替换模板**：

```python
def replace_full_para(para, new_text):
    """整段替换，保留首 run 格式。仅用于无脚注段落。"""
    if not para.runs:
        return
    para.runs[0].text = new_text
    for r in para.runs[1:]:
        r.text = ''
```

**Run 级替换模板**（保留脚注）：

```python
# 先扫描确认哪些 runs 是脚注（superscript=True）
for j, r in enumerate(para.runs):
    if r.font.superscript:
        continue  # 不动
    if '目标文本片段' in r.text:
        r.text = r.text.replace('目标文本片段', '替换文本')
```

### Phase 3: 一致性检查

改写后必须检查：

1. **风格一致性** — 改过的段落与未改段落语气一致（维普拼接预警）
2. **脚注完整性** — 所有 [N] 引用保留且对应正确
3. **字数变化** — 改后总字数与原文偏差 <15%
4. **信息完整性** — 原文核心论点、数据、引用全部保留

### Phase 4: 验证

1. 提取改后文本，人工通读
2. 建议用户去检测平台复检
3. 如仍超标，进入第二轮精修（优先改权重最高的剩余段落）

## 反模式（明确不能做的事）

| 操作 | 为什么无效 |
|------|-----------|
| 仅做同义词替换 | 句式结构未变，知网 3.0 直接穿透，仅降 5-10% |
| 只改标红段落不管上下文 | 风格断层触发维普拼接预警，反而加分 |
| 用 humanizer/洗稿工具 | Turnitin 2025.8 已可识别工具痕迹 |
| AI 改 AI 不换 prompt 策略 | 输出仍在 AI 分布内，等于原地踏步 |
| 插入特殊 Unicode 字符 | 所有主流平台已修补 |
| 中→英→中互翻 | 仅降 15%，且翻译腔本身可能触发 |
| 越改越正式/书面 | 越规整越像 AI |
| 先降查重后降 AI | 顺序错误——查重修改会引入新 AI 特征 |

## 高校红线参考

| 层级 | 典型要求 |
|------|---------|
| C9 / 顶尖 985 | <10-15% |
| 211 院校 | 15-25% |
| 普通本科 | 20-30% |
| 硕博论文 | <=10% |

## 终极检查清单

- [ ] 全文句长分布有足够变化（不是均匀 15-25 字）
- [ ] AI 特征词已替换或删除（对照黑名单）
- [ ] 消灭了所有「N个方面：第一…第二…第三…」并列模板
- [ ] 摘要已改为非标准四段式（维普权重 1.8x）
- [ ] 注入了具体数据 / 真实案例 / 个人观察
- [ ] 全文风格一致（无拼接断层）
- [ ] 论证深度有自然的浅→深节奏变化
- [ ] 脚注引用完整保留
- [ ] 文档格式无损（字体、行距、页眉）
- [ ] 改后总字数偏差 <15%

## 输出骨架

```
【战场态势】各章节 AIGC 率 + 优先级排序
【改写方案】每章节策略（整段重写 / 局部手术 / 微调 / 不动）
【执行结果】改动清单 + 脚注保留确认
【预估效果】各章节预估改后 AIGC 率
【复检建议】下一步行动
```
