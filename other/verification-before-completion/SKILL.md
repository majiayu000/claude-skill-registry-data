---
name: verification-before-completion
description: 完成任务前验证(铁律)— 来自 superpowers 体系。本 skill 是桥接层,完整纪律见 <SUPERPOWERS_SKILL_ROOT>/verification-before-completion/。
version: 4.0.0

---

# Verification-Before-Completion(桥接到 superpowers)

## Contract

- Inputs: completion claim, verification commands, implementation/documentation outputs
- Outputs: verification report using IDENTIFY/RUN/READ/VERIFY/THEN
- Gates: full verification command succeeds and output supports the claim
- Required disciplines: `stage-gate`
- Next: commit, fix loop, or `/handoff`

> **本仓库不维护此 skill 的内容**。完整纪律请读:
> `<SUPERPOWERS_SKILL_ROOT>/verification-before-completion/SKILL.md`

## 何时调

- 每个子任务结束时(在 commit 之前)
- 整个开发冲刺结束时(在 HANDOVER 之前)

## 衔接点

- **产出**:验证报告(IDENTIFY → RUN → READ → VERIFY → THEN 5 步门控)
- **下一步**:commit(通过)或修复(失败)
- **门控**:`disciplines/stage-gate` 第 3 层(失败必须重新跑)

## 5 步门控

参考完整纪律:
1. **IDENTIFY** — 什么命令能证明这个声明?
2. **RUN** — 执行完整的验证命令
3. **READ** — 读完整输出,检查退出码
4. **VERIFY** — 输出是否确认了声明?
5. **THEN** — 才能做出声明

> **铁律:跳过任何一步 = 撒谎,不是验证。**

## 降级方案(superpowers 未装时)

如果 `<SUPERPOWERS_SKILL_ROOT>/verification-before-completion/` 不存在,严格按以下 5 步门控(铁律,不允许跳):

### 1. IDENTIFY — 什么命令能证明这个声明?

- 把"已完成 / 通过 / 成功"翻译成**可执行的命令**
- 例如:"已修复 ASN 收货 bug" → `mvn test -Dtest=AsnReceiveServiceTest`
- ❌ 没有命令 = 你不知道自己在声称什么

### 2. RUN — 执行完整命令

- 命令必须**完整执行**(不能只看 stdout 头几行就停)
- 包含退出码 / 错误输出
- 用 `; echo "exit=$?"` 拿退出码

### 3. READ — 读完整输出

- 读**全部**输出,不只是你期望的那部分
- 数失败数 / 数 PASS 数 / 检查退出码
- ❌ 看一半就跳 = 漏掉隐藏失败

### 4. VERIFY — 输出是否真的支持声明?

- 把命令输出对照你的声明
- 输出支持 → 进 THEN
- 输出**反对**你的声明 → 立刻如实汇报(不允许"应该可以了")
- ❌ "看起来是对的" 一律不算

### 5. THEN — 才能做出声明

- **经过前 4 步后**才能写"完成 / 通过 / 成功"
- 必须附证据:命令 + 退出码 + 关键输出片段
- ❌ 没跑就声明 = 撒谎

### 最小纪律摘要

- **IDENTIFY 写不出命令 = 这个声明不成立**
- **RUN 不完整 = 假装在验**
- **READ 跳着看 = 漏失败**
- **VERIFY 不严 = 给自己找借口**
- **THEN 没附证据 = 不可信**

### 安装提示

```bash
npx skills@latest add obra/superpowers-verification-before-completion
```
