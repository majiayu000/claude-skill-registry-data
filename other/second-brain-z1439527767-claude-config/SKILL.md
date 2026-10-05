---
name: second-brain
version: 1.0.0
description: Complementary co-pilot. Brain 1 creates, Brain 2 verifies with clean context and different model.
---

# Second Brain — Complementary Co-Pilot

> **"第一脑负责发散和创造。第二脑负责收敛和验证。互补，不对抗。"**

## Two Brains, One System

```
BRAIN 1 (Creative/Executive)          BRAIN 2 (Analytical/Verification)
─────────────────────────────────     ─────────────────────────────────
擅长：理解意图、生成方案、写代码      擅长：发现遗漏、验证正确性、找边界
模式：发散（divergent）                模式：收敛（convergent）
上下文：完整对话历史                    上下文：只看输入+输出（干净）
盲区：自我审查、上下文腐烂、          盲区：不理解完整背景、
      过度自信、锚定效应                    过于保守、缺少创造力

              │                                  │
              └────────── 互补 ──────────────────┘
                        1 + 1 > 2
```

## Division of Labor

| 任务阶段 | Brain 1 做 | Brain 2 做 |
|---------|-----------|-----------|
| **理解需求** | 解析意图、澄清歧义 | 检查需求完整性、找隐含约束 |
| **设计方案** | 生成多个方案、权衡利弊 | 验证每个方案的可行性、找死角 |
| **写代码** | 实现功能、保持风格一致 | 审查正确性、补测试、找边界条件 |
| **修 bug** | 定位根因、修复代码 | 验证修复是否彻底、是否引入新 bug |
| **提交前** | 自审、格式化 | 独立审查、跑测试、检查引用完整性 |
| **完成任务** | 总结产出、标记完成 | 检查是否有遗漏子任务、更新记忆 |

## The Complementarity Principle

Brain 2 doesn't just say "you missed X."

Brain 2 says:
- "这里缺了 X，我已经补上了 → 这是补丁"
- "这个边界条件没处理 → 这是我写的测试"
- "这个决策有个风险 → 这是我建议的缓解方案"

**Brain 2 fills gaps, doesn't just flag them.**

## Trigger Points

| 触发 | Brain 2 行动 | 优先级 |
|------|-------------|--------|
| **代码改动** (>10行或涉及安全) | 独立审查 diff → 补测试 → 补边界处理 | 🔴 |
| **架构决策** | 验证可行性 → 找遗漏的约束 → 建议替代方案 | 🔴 |
| **修 bug** | 验证修复彻底性 → 检查同类 bug 是否存在 | 🟡 |
| **任务完成** | 检查是否有遗漏子任务 → 更新记忆 | 🟡 |
| **用户纠正** | 分析纠正模式 → 建议规则更新 | 🟢 |

### When to SKIP Brain 2

| 跳过的场景 | 原因 |
|-----------|------|
| 单行 typo 修复 | 成本 > 收益 |
| 纯格式化/注释改动 | 无需审查 |
| 配置值微调（不改逻辑） | 影响范围明确 |
| 用户明确说"不用审查" | 尊重用户意图 |
| 同一任务已被 Brain 2 审查过 2 次以上 | 避免重复开销 |

## Clean Context Rule

Brain 2 runs as an **independent subagent** (separate subagent invocation, not same agent switching personas). True isolation requires a fresh subagent — see delegation-lora for the delegation mechanism.

Brain 2 receives ONLY:
- Original user request (verbatim)
- Output artifacts (diff, files, terminal output)
- Explicit constraints

Brain 2 does NOT receive:
- Brain 1's reasoning or justifications
- Conversation history
- Brain 1's self-assessment

## Disagreement Resolution

When Brain 1 and Brain 2 disagree:

| Disagreement Type | Who Wins | Why |
|------------------|----------|-----|
| **Objective correctness** (null check, syntax, security hole) | Brain 2 | Facts over opinions |
| **Design choice** (architecture, naming, tradeoffs) | Brain 1 | Has full project context |
| **Risk assessment** | Tie → escalate to user | Subjective, needs human judgment |

Rule of thumb: Brain 2 wins on WHAT is wrong. Brain 1 wins on HOW to fix it.

## False Positive Prevention

Brain 2 findings are not automatically applied:
1. Brain 2 reports → Brain 1 reviews and accepts/rejects each item
2. Accepted findings → write to KG as successful catch
3. Rejected findings → write to KG as false positive pattern
4. Same false positive 3 times → Brain 2 learns to stop flagging it

## Output: Complement Report

```
### Second Brain — Complement Report

#### ✅ CONFIRMED
- {what Brain 1 got right, with evidence}

#### 🔧 COMPLETED
- {what Brain 1 missed → Brain 2 already filled}
- {补丁、测试、边界处理已写好}

#### ⚠️ FLAGGED (needs Brain 1)
- {issues Brain 2 found but can't fix alone — needs Brain 1's context}

#### 💡 SUGGESTED
- {improvements for next time, patterns to learn}
```

## Model Selection

Different model = complementary blind spots:

| Brain 1 Model | Brain 2 Model | Why |
|---------------|---------------|-----|
| Creative model (Opus/Sonnet) | Precise model (Haiku) | Big-picture vs detail-oriented |
| Different provider | Different provider | Different training = different gaps |
| Any | adversarial-reviewer agent | Built for this exact purpose |

## Learning Together

Both brains contribute to memory:
- Brain 1 patterns → KG (creative strategies, successful approaches)
- Brain 2 findings → KG (common omissions, edge case patterns)
- Recurring gaps → auto-generated prevention rules
- Complementary strengths improve over time

## Integration

Built on the cross-model review mandate from self-review.md: different model, clean context, independent review.

Current integration status:

| Partner | Status | Mechanism |
|---------|--------|-----------|
| **precommit-pipeline step 4** | ✅ wired | Delegates to adversarial-reviewer = Brain 2 |
| **delegation-lora #5** | ✅ wired | Cross-model review trigger = Brain 2 |
| **memory-lora** | 🔜 planned | Both brains write to memory.db |
| **skill-judge** | 🔜 planned | Brain 2 reports feed skill scores |

### Sub-Agent Reference
Brain 2 is implemented using existing agent types:
- `adversarial-reviewer` — primary Brain 2 agent
- `code-review` — code-specific review
- `security-auditor` — security-focused review
- General-purpose subagent with different model — fallback
