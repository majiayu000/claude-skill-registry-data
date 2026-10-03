---
name: writing-plans
description: 把 spec 拆成可执行计划(每个 ≤ 2h)— 来自 superpowers 体系。本 skill 是桥接层,完整纪律见 <SUPERPOWERS_SKILL_ROOT>/writing-plans/。
version: 4.0.0

---

# Writing-Plans(桥接到 superpowers)

## Contract

- Inputs: signed design spec, interface/domain model as available
- Outputs: `docs/superpowers/plans/YYYY-MM-DD-<topic>-plan.md`
- Gates: tasks are independently executable and each is no larger than 2 hours
- Required disciplines: `stage-gate`
- Next: `/tdd`

> **本仓库不维护此 skill 的内容**。完整纪律请读:
> `<SUPERPOWERS_SKILL_ROOT>/writing-plans/SKILL.md`

## 何时调

- brainstorming / design-an-interface / domain-modeling 之后
- 需要把 spec 拆成可逐步执行的计划

## 衔接点

- **产出**:`docs/superpowers/plans/YYYY-MM-DD-<topic>-plan.md`(含 ≤ 2h 子任务列表)
- **下一步**:`/tdd`(开始红绿循环)
- **门控**:`disciplines/stage-gate` 第 2 层 + 第 3 层(每个子任务)

## 降级方案(superpowers 未装时)

如果 `<SUPERPOWERS_SKILL_ROOT>/writing-plans/` 不存在,按以下 4 步产出可执行计划:

### 1. 拆任务(每个 ≤ 2h)

按以下规则拆:

- **可独立运行**(一个任务完不依赖另一个任务的产物)
- **可独立验证**(每个任务有明确的 PASS 标志)
- **可估时**(≤ 2h,超出则继续拆)
- **依赖关系显式**(用 `Blocked by:` 标注)

### 2. 每个任务写 7 件套

| 字段 | 例子 |
|---|---|
| Title | "实现 ASN 收货状态机 10→30" |
| Files | `service/AsnReceiveService.java` |
| Test | `AsnReceiveServiceTest#shouldTransitionFrom10To30` |
| Steps | 1. 写 RED 2. 跑确认失败 3. 写实现 4. GREEN 5. 提交 |
| Verify | `mvn test -Dtest=AsnReceiveServiceTest` |
| Blocked by | - |
| Estimate | 1.5h |

### 3. 顺序 + 依赖图

- **第 1 个任务**:数据模型 / 状态机先建(后面的都依赖)
- **中间任务**:业务逻辑 / 接口契约
- **最后任务**:联调 / E2E 测试

### 4. 输出 + 签字

写到 `docs/superpowers/plans/YYYY-MM-DD-<topic>-plan.md`,末尾 `## Sign-off` 等用户白名单签字(4 句之一)。

### 最小纪律摘要

- **每个任务 ≤ 2h**:超 2h 必须拆(否则 TDD 红绿循环失控)
- **7 件套不能少**:缺 Verify = 不知道什么时候算 PASS
- **依赖写显式**:不写 = 后续乱序执行
- **第 1 个任务不含集成**:先建地基,再在上面盖楼

### 安装提示

```bash
npx skills@latest add obra/superpowers-writing-plans
```
