---
name: design-an-interface
description: 设计接口契约 — 来自 superpowers 体系。本 skill 是桥接层,完整纪律见 <SUPERPOWERS_SKILL_ROOT>/design-an-interface/。
version: 4.0.0

---

# Design-an-Interface(桥接到 superpowers)

## Contract

- Inputs: design spec, domain constraints, integration points
- Outputs: interface contract document
- Gates: interface is testable and accepted by caller/implementer
- Required disciplines: `stage-gate`
- Next: `/domain-modeling` or `/writing-plans`

> **本仓库不维护此 skill 的内容**。完整纪律请读:
> `<SUPERPOWERS_SKILL_ROOT>/design-an-interface/SKILL.md`

## 何时调

- brainstorming 之后,writing-plans 之前
- 需要把功能拆成可测试的接口

## 衔接点

- **产出**:接口契约文档
- **下一步**:`/domain-modeling` 或 `/writing-plans`
- **门控**:`disciplines/stage-gate` 第 2 层

## 降级方案(superpowers 未装时)

如果 `<SUPERPOWERS_SKILL_ROOT>/design-an-interface/` 不存在,按以下 4 步产出接口契约:

### 1. 列举调用方与实现方

- **调用方**是谁?(controller / 巴枪 / 第三方系统)
- **实现方**是谁?(哪个 service / 模块)
- **触发场景**有哪些?(主动调用 / 事件回调 / 定时)

### 2. 写接口契约表

每个接口必须含 5 列:

| 列 | 含义 | 例子 |
|---|---|---|
| Name | 方法/路径名 | `POST /api/v1/asn/receive` |
| Input | 入参 schema | `{tcAsnId, lpnList[]}` |
| Output | 出参 schema | `{receivedQty, exceptionList[]}` |
| Errors | 错误码字典 | `E_ASN_NOT_FOUND(40401)` |
| Pre/Post | 前置/后置条件 | 前置:ASN 状态=10;后置:状态=30 |

### 3. 验收契约

- **可测试性**:每个契约都对应 1 个测试用例(契约层用)
- **错误码对齐**:与全局 `09-QA审计报告` 的错误码字典一致
- **联调**:与调用方对齐字段名 / 类型,**字段名严禁猜测**(走 `disciplines/no-field-guessing`)

### 4. 输出 + 签字

写到 `docs/superpowers/specs/<topic>-interface.md`,末尾 `## Sign-off` 等用户白名单签字(4 句之一)。

### 最小纪律摘要

- **契约是合同**:写下来就不准改,改了要重新签字
- **错误码全局唯一**:不复用业务字段名当错误码
- **Pre/Post 必须**:只写 Input/Output = 验收没边界
- **联调不靠人脑**:调用方拿到契约文档就能写 Mock

### 安装提示

```bash
npx skills@latest add obra/superpowers-design-an-interface
```
