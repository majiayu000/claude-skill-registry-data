---
name: domain-modeling
description: 梳理领域模型 — 来自 superpowers 体系。本 skill 是桥接层,完整纪律见 <SUPERPOWERS_SKILL_ROOT>/domain-modeling/。
version: 4.0.0

---

# Domain-Modeling(桥接到 superpowers)

## Contract

- Inputs: design spec, terminology, entities, business rules
- Outputs: domain model diagram and entity list
- Gates: user agrees canonical terms and relationships
- Required disciplines: `stage-gate`
- Next: `/writing-plans`

> **本仓库不维护此 skill 的内容**。完整纪律请读:
> `<SUPERPOWERS_SKILL_ROOT>/domain-modeling/SKILL.md`

## 何时调

- brainstorming / design-an-interface 之后
- 需要定义实体、值对象、聚合根

## 衔接点

- **产出**:领域模型图 + 实体清单
- **下一步**:`/writing-plans`
- **门控**:`disciplines/stage-gate` 第 2 层

## 降级方案(superpowers 未装时)

如果 `<SUPERPOWERS_SKILL_ROOT>/domain-modeling/` 不存在,按以下 4 步产出领域模型:

### 1. 列实体

从 brainstorming 设计稿提取名词,过滤出**实体**(有生命周期、有 ID)与**值对象**(无 ID、不可变):

| 类型 | 例子 | 判别 |
|---|---|---|
| 实体 | ASN / LPN / 波次 | 有 `*_ID`,状态会变 |
| 值对象 | 收货地址 / 计量单位 | 无 ID,只描述属性 |
| 聚合根 | ASN(含 LPN 列表) | 一致性边界 |

### 2. 画 ASCII 关系图

参考 `disciplines/ascii-flowchart` 用 ASCII 画实体关系图,严禁 Mermaid:

```
[ASN] -- 1..N --> [ASN_DTL] -- 1..N --> [LPN]
   |                                       |
   +-- 1..1 --> [收货地址(值对象)]
```

### 3. 字段对齐验证

每个实体字段必须与知识库核对(`disciplines/no-field-guessing`):

- 已有表 → 直接用现有字段(走 `field-alignment-check.py`)
- 新增字段 → 标记 `EXTEND` 且写扩展理由

### 4. 输出 + 签字

写到 `docs/superpowers/specs/<topic>-domain.md`,末尾 `## Sign-off` 等用户白名单签字(4 句之一)。

### 最小纪律摘要

- **名词 ≠ 实体**:不是所有名词都是实体,看 ID 与状态
- **ASCII 不用 Mermaid**:与全局 `ascii-flowchart` 纪律冲突
- **字段不靠记忆**:严禁自创字段名(`no-field-guessing` + `no-self-invent`)
- **聚合根边界 = 事务边界**:不能跨聚合根强一致

### 安装提示

```bash
npx skills@latest add obra/superpowers-domain-modeling
```
