---
name: writing-skills
description: 当你要创建新 skill、编辑已有 skill，或在部署前验证 skill 是否有效时使用
---

# 编写 Skills

## 概览

**编写 skill，本质上就是把测试驱动开发（TDD）应用到流程文档上。**

**个人 skills 存放在 agent 专属目录中**（Claude Code 用 `~/.claude/skills`，Codex 用 `~/.agents/skills/`）。

你要先写测试场景（给 subagent 的压力场景），观察它在**没有 skill** 时如何失败（baseline），再写 skill 文档，重新验证它是否能正确遵循，最后不断补漏洞、关死合理化空间。

**核心原则：**如果你没亲眼看到 agent 在没有 skill 时失败，就不知道这个 skill 是否真的教会了正确的东西。

**必需背景：**在使用本 skill 前，你必须理解 `superpowers:test-driven-development`。它定义了 RED-GREEN-REFACTOR 的基本循环，而本 skill 只是把这个循环迁移到文档上。

**官方参考：**Anthropic 的 skill 编写最佳实践见 `anthropic-best-practices.md`。它补充了这里的 TDD 视角。

## 什么是 Skill？

Skill 是一份关于已验证技巧、模式或工具的参考指南，帮助未来的 agent 快速发现并复用有效做法。

**Skill 是：**可复用技巧、模式、工具、参考指南  
**Skill 不是：**“我上次是怎么解决这个问题的”那类叙事性回顾

## Skill 与 TDD 的对应关系

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test case** | 带压力的 subagent 场景 |
| **Production code** | `SKILL.md` 文档 |
| **Test fails (RED)** | 没有 skill 时 agent 违反规则 |
| **Test passes (GREEN)** | 有了 skill 后 agent 开始遵循 |
| **Refactor** | 不断堵住新出现的漏洞 |
| **Write test first** | 先跑 baseline，再写 skill |
| **Watch it fail** | 记录 agent 的原始错误和合理化措辞 |
| **Minimal code** | 只写能修正这些失败的最小 skill |
| **Watch it pass** | 用同样场景验证 skill 生效 |
| **Refactor cycle** | 新借口出现 -> 补规则 -> 再验证 |

整个 skill 创建流程都应遵循 RED-GREEN-REFACTOR。

## 何时创建 Skill

**适合创建 skill：**
- 这个技巧对你来说并不显然
- 你以后还会重复用到
- 它适用面广，不是单项目私货
- 其他人也会受益

**不适合创建 skill：**
- 一次性解决方案
- 已经被广泛标准化的常识
- 明显属于某个项目约定（应写进 CLAUDE.md / AGENTS.md）
- 可以靠正则、校验脚本、自动化规则硬性约束的东西

## Skill 类型

### Technique
一个可以按步骤执行的具体方法，例如 `condition-based-waiting`、`root-cause-tracing`

### Pattern
一种思考问题的方式，例如 `flatten-with-flags`、`test-invariants`

### Reference
API 文档、命令参考、库使用指南等资料型内容

## 目录结构

```text
skills/
  skill-name/
    SKILL.md              # 主入口（必需）
    supporting-file.*     # 只有在确实需要时才添加
```

**平面命名空间。** 所有 skill 都应该处于统一、可搜索的平面命名空间中。

**单独文件适合放：**
1. **重型参考资料**（100+ 行），例如 API docs
2. **可复用工具**，例如脚本、模板、辅助代码

**适合直接写在 SKILL.md 内：**
- 原则和概念
- 短代码模式（< 50 行）
- 其他大多数正文

## SKILL.md 结构

### Frontmatter
必需字段是 `name` 和 `description`；其他受支持字段请参考 [agentskills.io/specification](https://agentskills.io/specification)

- 总长度建议不超过 1024 字符
- `name`：只用字母、数字、连字符
- `description`：第三人称，只描述**何时使用**，不要描述它**怎么做**
  - 以 `Use when...` 开头
  - 写清触发条件、症状、上下文
  - **不要**在 description 里总结完整 workflow
  - 尽量控制在 500 字以内

### 推荐结构

```markdown
---
name: skill-name
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
核心原则 + 1-2 句说明

## When to Use
说明适用和不适用场景；如果判断不显然，可以加小流程图

## Core Pattern
对 technique / pattern 类 skill，展示前后对比

## Quick Reference
表格或项目符号，方便扫描

## Implementation
短代码直接内联；重资料放到单独文件

## Common Mistakes
常见误用与修复方式

## Real-World Impact (optional)
说明它在真实环境里的价值
```

## Claude Search Optimization（CSO）

未来的 Claude / agent 能不能发现你的 skill，很大程度上取决于 description 和关键词布局。

### 1. 丰富而克制的 Description

description 的目的不是总结 skill 流程，而是帮助模型判断：
**“我现在应该读这个 skill 吗？”**

**关键规则：Description = 何时使用，不是如何执行。**

为什么这么重要：测试表明，一旦 description 里偷塞了 workflow 摘要，模型会直接照着 description 走，而不去认真读 skill 正文。结果就是 skill body 被跳过。

**坏例子：**
```yaml
description: Use when executing plans - dispatches subagent per task with code review between tasks
```

**好例子：**
```yaml
description: Use when executing implementation plans with independent tasks in the current session
```

**写 description 时要做到：**
- 用具体触发条件和症状
- 优先描述问题，而不是描述实现过程
- 除非 skill 本身就是技术栈专用，否则尽量技术无关
- 如果确实是技术专用 skill，就把那门技术明确写进触发条件
- 保持第三人称
- 不总结 workflow

### 2. 关键词覆盖

把模型真正可能搜索的词放进去：
- 错误消息
- 症状描述（如 flaky / hanging / timeout）
- 同义词
- 实际工具名、命令名、文件类型

### 3. 命名要具备动作语义

优先用主动、动词驱动的名字：
- `creating-skills` 优于 `skill-creation`
- `condition-based-waiting` 优于 `async-test-helpers`

Gerund（`-ing`）通常对过程类 skill 很友好：
- `creating-skills`
- `testing-skills`
- `debugging-with-logs`

### 4. Token 效率

一些 skill 会在很多会话里频繁被加载，所以 token 很宝贵。

**建议目标：**
- getting-started 类：<150 词
- 高频 skill：<200 词
- 其他 skill：尽量 <500 词，但仍以清晰为先

**减 token 的方法：**
- 把命令细节留给 `--help`
- 多做 skill 之间的交叉引用，少重复解释
- 例子只留最好的 1 个
- 删除重复话术

## 交叉引用其他 Skills

引用其他 skill 时，用 skill 名称 + 明确的强制标记：
- ✅ `**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development`
- ✅ `**REQUIRED BACKGROUND:** You MUST understand superpowers:systematic-debugging`
- ❌ `See skills/testing/test-driven-development`
- ❌ `@skills/testing/test-driven-development/SKILL.md`

**为什么不要用 `@` 强制加载：**它会立即把整个文件灌进上下文，代价太大。

## 流程图使用原则

只在这些场景使用 flowchart：
- 非显然的判断点
- 容易过早停止的循环流程
- A / B 选择不明显的时候

不要用流程图表示：
- 纯参考资料
- 代码示例
- 线性步骤
- 没语义的通用标签

## 代码示例原则

一个优秀示例胜过一堆平庸示例。

好示例应当：
- 完整、可运行
- 注释解释“为什么”
- 来自真实场景
- 清楚展现模式
- 能直接迁移

不要：
- 给同一个点写 5 种语言版本
- 写 fill-in-the-blank 模板
- 写脱离真实场景的玩具例子

## 文件组织模式

### Self-Contained Skill
```text
defense-in-depth/
  SKILL.md
```
当全部内容都可直接塞进主文档时使用。

### Skill with Reusable Tool
```text
condition-based-waiting/
  SKILL.md
  example.ts
```
当你需要复用工具代码，而不仅仅是叙述时使用。

### Skill with Heavy Reference
```text
pptx/
  SKILL.md
  pptxgenjs.md
  ooxml.md
  scripts/
```
当参考资料太大，不适合塞进主文档时使用。

## 铁律（与 TDD 相同）

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

这条规则既适用于新 skill，也适用于对旧 skill 的编辑。

先写 skill 再测？删掉，重来。  
先改 skill、不做测试？同样违规。

**没有例外：**
- 不是因为“只是补一小节”就可以跳过
- 不是因为“只是文档更新”就可以跳过
- 不要把未测试的改动留作参考
- Delete means delete

## 如何测试不同类型的 Skill

### Discipline-Enforcing Skills
例如 TDD、verification-before-completion

**测试方式：**
- 学术型问答：是否理解规则
- 高压场景：在时间压力、沉没成本、疲惫下是否仍遵守
- 组合压力：多种压力同时施加
- 记录它的合理化话术，再把这些话术写回 skill

**成功标准：**在高压场景下依然遵守规则。

### Technique Skills
例如 `condition-based-waiting`

**测试方式：**
- 新场景迁移
- 变体场景
- 缺信息场景

**成功标准：**能把技术正确迁移到新问题上。

### Pattern Skills
例如复杂度控制、信息隐藏

**测试方式：**
- 是否能识别何时适用
- 是否能正确使用模式
- 是否知道何时不该用

### Reference Skills
例如 API 文档、命令参考

**测试方式：**
- 能否正确检索信息
- 能否正确应用检索结果
- 常见场景是否覆盖完整

## 跳过测试的常见借口

| Excuse | Reality |
|--------|---------|
| "Skill is obviously clear" | 你觉得清楚，不代表其他 agent 也会用对。 |
| "It's just a reference" | Reference 也会缺漏、也会误导，照样要测。 |
| "Testing is overkill" | 未测试 skill 几乎一定会出问题。 |
| "I'll test if problems emerge" | 那时已经是在生产环境里踩坑了。 |
| "Too tedious to test" | 测 skill 远比之后 debug 错误 skill 更省事。 |
| "I'm confident it's good" | 过度自信是 skill 失效的重要来源。 |
| "Academic review is enough" | 阅读 ≠ 实战使用。 |
| "No time to test" | 部署未测试 skill，后面会浪费更多时间。 |

## 如何把 Skill 写得更抗合理化

纪律型 skill（如 TDD）必须主动防御合理化。agent 很聪明，也很会钻空子。

### 把所有漏洞写死

不要只写原则，还要把常见绕法明确禁止掉。

<Bad>
```markdown
Write code before test? Delete it.
```
</Bad>

<Good>
```markdown
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```
</Good>

### 显式处理“精神 vs 字面”论证

在 skill 前部直接写：

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

### 建立合理化对照表

把 baseline 测试里出现的每一种借口都写进表里，逐项回击。

### 增加 Red Flags 清单

让 agent 一旦说出某些典型话术，就能立刻自检并停下。

## RED-GREEN-REFACTOR for Skills

### RED：先跑失败基线

在**没有 skill** 的情况下，用 subagent 跑压力场景，并记录：
- 它做了什么错误决策
- 它说了哪些原话
- 是什么压力触发了错误

### GREEN：写最小 Skill

只针对这些具体失败写最小 skill，不要先写一堆假想规则。

然后用同样场景重新测试，看它是否遵守。

### REFACTOR：不断补洞

一旦又出现新的合理化说法，就把它补进 skill，然后再测。一直测到足够稳固。

完整方法见：`@testing-skills-with-subagents.md`

## 反模式

### ❌ 叙事性故事
“在 2025-10-03 那次会话里，我们发现……”

坏处：太具体，不可迁移。

### ❌ 多语言稀释
同一个例子写 JS / Python / Go 三份。

坏处：维护成本高，质量通常都不高。

### ❌ 把代码写进流程图

坏处：无法复制粘贴，也不利于阅读。

### ❌ 通用占位标签
比如 `helper1`、`step3`、`pattern4`

坏处：没有语义，不利于检索和理解。

## 停止点：写完一个 Skill 后必须做什么

写完任意 skill 后，**必须停下来完成该 skill 的部署流程**。

**不要：**
- 一口气批量写多个 skill，却不逐个测试
- 当前 skill 还没验证，就跳去写下一个
- 以“批处理更高效”为由跳过验证

## Skill 创建检查清单

**RED：**
- [ ] 为该 skill 设计压力场景
- [ ] 在没有 skill 的情况下跑基线，记录原始失败
- [ ] 整理出常见合理化模式

**GREEN：**
- [ ] `name` 只用字母、数字、连字符
- [ ] YAML frontmatter 至少包含必需的 `name` 与 `description` 字段（总长度建议不超过 1024 字符）
- [ ] `description` 以 `Use when...` 开头
- [ ] `description` 只写触发条件，不写 workflow
- [ ] skill 内有清晰的 Overview
- [ ] skill 直接针对 baseline 失败点写规则
- [ ] 有至少一个高质量示例
- [ ] 在有 skill 的情况下重新跑测试

**REFACTOR：**
- [ ] 找出新出现的合理化话术
- [ ] 把这些话术写回 skill
- [ ] 补充 rationalization table
- [ ] 补充 red flags
- [ ] 重测，直到足够稳固

**质量检查：**
- [ ] 只有在必要时才加小流程图
- [ ] 有 quick reference
- [ ] 有 common mistakes
- [ ] 没有叙事性流水账
- [ ] supporting files 只在真的需要时才建

**部署：**
- [ ] 把 skill 提交到 git
- [ ] 如果足够通用，考虑回馈上游

## Discovery Workflow

未来的 Claude / agent 通常会这样发现你的 skill：

1. 遇到问题（例如“tests are flaky”）
2. 搜索相关词
3. 找到你的 SKILL（description / 关键词匹配）
4. 扫 Overview 判断是否相关
5. 看 Quick Reference 抓住用法
6. 真正实现时再去读详细示例

**所以要为这个发现流程写 skill。**

## 最终结论

**创建 skill，就是把 TDD 用在流程文档上。**

同样的铁律：没有 failing test，就不该有 skill。  
同样的循环：RED（基线失败）-> GREEN（写 skill）-> REFACTOR（补漏洞）。

如果你愿意对代码坚持 TDD，就应该对 skill 也坚持一样的纪律。
