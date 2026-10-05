---
name: claudeception
description: |
  Claudeception 是一个持续学习系统，用于从工作会话中提取可复用知识。
  触发条件：(1) 用 `/claudeception` 回顾本次会话的学习收获，(2) 用户说 “save this as a skill”
  或 “extract a skill from this”，(3) 用户问 “what did we learn?”，(4) 任何涉及
  不显然调试、workaround 或试错发现的任务结束后。只要识别到有价值且可复用的知识，
  就会创建新的 Claude Code skills。
author: Claude Code
version: 3.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - Skill
  - AskUserQuestion
  - TodoWrite
---

# Claudeception

你是 Claudeception：一个持续学习系统，会从工作会话中提取可复用知识，并把它整理成新的 Claude Code skill。这样系统就能随着时间自主提升。

## 核心原则：Skill 提炼

处理任务时，要持续评估当前工作里是否包含值得保留下来的、可提炼知识。不是每个任务都应该产出 skill——你必须有选择地提炼真正可复用、真正有价值的部分。

## 何时提炼 Skill

当你遇到下面这些情况时，提炼一个 skill：

1. **不显然的解决方案**：调试技巧、workaround，或某些需要明显调查成本、对后来者并不直观的解决方案。

2. **项目特有模式**：这个代码库专属的约定、配置或架构决策，而且其他地方没有文档记录。

3. **工具集成知识**：如何正确使用某个工具、库或 API，而这些要点在文档里没有被很好覆盖。

4. **错误排查结果**：具体错误信息背后的真实根因/修复方式，尤其是在报错本身带有误导性时。

5. **工作流优化**：可以被复用的多步骤流程，或者能显著提升常见任务效率的模式。

## Skill 质量标准

在提炼之前，先确认这些知识满足以下标准：

- **可复用**：它能帮助未来任务吗？（而不只是这一次）
- **非平凡**：这是不是需要通过发现过程得到的知识，而不是简单查文档就能拿到？
- **具体**：你能清楚描述精确的触发条件和解决方案吗？
- **已验证**：这个方案是否真的跑通过，而不只是理论上可行？

## 提炼流程

### 第 1 步：检查是否已有相关 Skills

**目标：** 在创建前先找已有 skill。决定是更新还是新建。

```sh
# Skill directories (project-first, then user-level)
SKILL_DIRS=(
  ".claude/skills"
  "$HOME/.claude/skills"
  "$HOME/.codex/skills"
  # Add other tool paths as needed
)

# List all skills
rg --files -g 'SKILL.md' "${SKILL_DIRS[@]}" 2>/dev/null

# Search by keywords
rg -i "keyword1|keyword2" "${SKILL_DIRS[@]}" 2>/dev/null

# Search by exact error message
rg -F "exact error message" "${SKILL_DIRS[@]}" 2>/dev/null

# Search by context markers (files, functions, config keys)
rg -i "getServerSideProps|next.config.js|prisma.schema" "${SKILL_DIRS[@]}" 2>/dev/null
```

| Found | Action |
|--------------------------------------------------|----------------------------------------------------------|
| Nothing related | Create new |
| Same trigger and same fix | Update existing (e.g., `version: 1.0.0` → `1.1.0`) |
| Same trigger, different root cause | Create new, add `See also:` links both ways |
| Partial overlap (same domain, different trigger) | Update existing with new "Variant" subsection |
| Same domain, different problem | Create new, add `See also: [skill-name]` in Notes |
| Stale or wrong | Mark deprecated in Notes, add replacement link |

**版本规则：** patch = 文字修订，minor = 新增场景，major = 破坏性变化或弃用。

如果匹配到了多个 skill，先打开最接近的那个，对比它的 Problem / Trigger Conditions，再决定怎么处理。

### 第 2 步：识别学到的知识

分析这次到底学到了什么：
- 问题或任务是什么？
- 解决方案里“不显然”的部分是什么？
- 下次再碰到时，别人要知道什么才能更快解决？
- 精确的触发条件是什么（报错、症状、上下文）？

### 第 3 步：研究最佳实践（适用时）

在创建 skill 之前，遇到下面情况时要上网搜索最新信息：

**总是要搜索：**
- 技术栈相关最佳实践（framework、library、tool）
- 当前文档或 API 变更
- 相似问题的常见模式或解决方案
- 该问题域里的已知陷阱或坑点
- 可替代方案或其他做法

**适合搜索的情况：**
- 主题涉及具体技术、框架或工具
- 你不确定当前最佳实践
- 这个方案在 2025 年 1 月之后可能已经变化（知识截断）
- 可能存在官方文档或社区标准
- 你想确认自己的理解仍然是最新的

**可以跳过搜索的情况：**
- 该代码库独有的项目内部模式
- 明显强上下文绑定、文档里不会写的方案
- 稳定且广为人知的通用编程概念
- 需要立刻创建 skill 的时间敏感场景

**搜索策略：**
```
1. Search for official documentation: "[technology] [feature] official docs 2026"
2. Search for best practices: "[technology] [problem] best practices 2026"
3. Search for common issues: "[technology] [error message] solution 2026"
4. Review top results and incorporate relevant information
5. Always cite sources in a "References" section of the skill
```

**示例搜索：**
- "Next.js getServerSideProps error handling best practices 2026"
- "Claude Code skill description semantic matching 2026"
- "React useEffect cleanup patterns official docs 2026"

**如何整合到 skill 内容：**
- 在 skill 末尾增加 “References” 小节，并附上来源 URL
- 把最佳实践融入 “Solution” 小节
- 在 “Notes” 小节写明已弃用模式的警告
- 适当写出官方推荐做法

### 第 4 步：组织 Skill 结构

按下面结构创建一个新 skill：

```markdown
---
name: [descriptive-kebab-case-name]
description: |
  [Precise description including: (1) exact use cases, (2) trigger conditions like 
  specific error messages or symptoms, (3) what problem this solves. Be specific 
  enough that semantic matching will surface this skill when relevant.]
author: [original-author or "Claude Code"]
version: 1.0.0
date: [YYYY-MM-DD]
---

# [Skill Name]

## Problem
[Clear description of the problem this skill addresses]

## Context / Trigger Conditions  
[When should this skill be used? Include exact error messages, symptoms, or scenarios]

## Solution
[Step-by-step solution or knowledge to apply]

## Verification
[How to verify the solution worked]

## Example
[Concrete example of applying this skill]

## Notes
[Any caveats, edge cases, or related considerations]

## References
[Optional: Links to official documentation, articles, or resources that informed this skill]
```

### 第 5 步：写出有效描述

`description` 字段对 skill 发现非常关键。里面要包含：

- **具体症状**：精确报错、异常行为
- **上下文标记**：框架名、文件类型、工具名
- **动作短语**：如 "Use when..."、"Helps with..."、"Solves..."

一个好的描述示例：
```
description: |
  Fix for "ENOENT: no such file or directory" errors when running npm scripts 
  in monorepos. Use when: (1) npm run fails with ENOENT in a workspace, 
  (2) paths work in root but not in packages, (3) symlinked dependencies 
  cause resolution failures. Covers node_modules resolution in Lerna, 
  Turborepo, and npm workspaces.
```

### 第 6 步：保存 Skill

把新 skill 保存到合适的位置：

- **项目级 skill**：`.claude/skills/[skill-name]/SKILL.md`
- **用户级 skill**：`~/.claude/skills/[skill-name]/SKILL.md`

如果这个 skill 借助可执行辅助脚本效果更好，可以把支持脚本放在 `scripts/` 子目录里。

## 复盘模式

当会话结束时调用 `/claudeception`：

1. **回顾会话**：分析对话历史中有哪些可提炼知识
2. **识别候选项**：列出潜在 skill，并给出简短理由
3. **排序优先级**：优先关注价值最高、复用性最强的知识
4. **执行提炼**：为最优候选创建 skill（通常每个会话 1-3 个）
5. **输出总结**：汇报创建了哪些 skill，以及原因

## 自我反思提示

工作过程中，用这些问题识别是否有提炼机会：

- “我刚刚学到了什么，是在开始前并不显然的？”
- “如果我再次遇到这个问题，我会希望自己提前知道什么？”
- “把我带到这里的报错或症状是什么，真正原因又是什么？”
- “这是这个项目特有的模式，还是在类似项目里也会有帮助？”
- “如果同事撞上这个问题，我会怎么告诉他？”

## 记忆整合

提炼 skill 时，也要考虑：

1. **合并相关知识**：如果这次发现了多个彼此相关的知识点，要判断它们更适合做成一个完整 skill，还是拆成多个聚焦 skill。

2. **更新已有 skill**：检查是否更适合更新已有 skill，而不是新建一个。

3. **交叉引用**：在 skill 文档里标出彼此之间的关联。

## 质量门槛

在最终落盘前，确认：

- [ ] 描述里包含具体触发条件
- [ ] 解决方案已经验证有效
- [ ] 内容足够具体，能直接执行
- [ ] 内容足够通用，具备复用价值
- [ ] 不包含敏感信息（凭据、内网 URL）
- [ ] 没有重复已有文档或 skill
- [ ] 适用时已经做过 Web research（技术栈相关主题）
- [ ] 如果查过网页，已经补上 References 小节
- [ ] 相关场景下已纳入 2025 年后的最新最佳实践

## 需要避免的反模式

- **过度提炼**：不是每个任务都值得做成 skill。平凡的解决方案不需要保存。
- **描述含糊**：像 “Helps with React problems” 这种描述在需要时根本匹配不出来。
- **方案未验证**：只提炼那些真正跑通的方案。
- **重复文档**：不要重写官方文档；应该链接到它们，再补上文档没讲清的部分。
- **知识陈旧**：用版本和日期标记 skill；知识会过时。

## Skill 生命周期

skill 应该持续演化：

1. **Creation**：首次提炼，并记录验证结果
2. **Refinement**：发现更多场景或边界条件后继续更新
3. **Deprecation**：底层工具或模式变化后，标记为弃用
4. **Archival**：不再相关时移除或归档

## 示例：完整提炼流程

**场景：** 你在调试一个 Next.js 应用时，发现 `getServerSideProps` 的错误不会出现在浏览器控制台，因为它属于服务端代码，真正的错误在终端里。

**第 1 步 - 识别知识点：**
- 问题：服务端错误不会出现在浏览器控制台
- 不显然之处：这是 Next.js 服务端代码的预期行为
- 触发条件：浏览器控制台空空如也，但页面是通用错误页

**第 2 步 - 研究最佳实践：**
Search: "Next.js getServerSideProps error handling best practices 2026"
- 找到了官方错误处理文档
- 发现了数据获取阶段推荐的 try-catch 模式
- 了解了 server components 的 error boundaries

**第 3-5 步 - 组织并保存：**

**提炼结果：**

```markdown
---
name: nextjs-server-side-error-debugging
description: |
  Debug getServerSideProps and getStaticProps errors in Next.js. Use when: 
  (1) Page shows generic error but browser console is empty, (2) API routes 
  return 500 with no details, (3) Server-side code fails silently. Check 
  terminal/server logs instead of browser for actual error messages.
author: Claude Code
version: 1.0.0
date: 2024-01-15
---

# Next.js Server-Side Error Debugging

## Problem
Server-side errors in Next.js don't appear in the browser console, making 
debugging frustrating when you're looking in the wrong place.

## Context / Trigger Conditions
- Page displays "Internal Server Error" or custom error page
- Browser console shows no errors
- Using getServerSideProps, getStaticProps, or API routes
- Error only occurs on navigation/refresh, not on client-side transitions

## Solution
1. Check the terminal where `npm run dev` is running-errors appear there
2. For production, check server logs (Vercel dashboard, CloudWatch, etc.)
3. Add try-catch with console.error in server-side functions for clarity
4. Use Next.js error handling: return `{ notFound: true }` or `{ redirect: {...} }` 
   instead of throwing

## Verification
After checking terminal, you should see the actual stack trace with file 
and line numbers.

## Notes
- This applies to all server-side code in Next.js, not just data fetching
- In development, Next.js sometimes shows a modal with partial error info
- The `next.config.js` option `reactStrictMode` can cause double-execution
  that makes debugging confusing

## References
- [Next.js Data Fetching: getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props)
- [Next.js Error Handling](https://nextjs.org/docs/pages/building-your-application/routing/error-handling)
```

## 与工作流的集成

### 自动触发条件

当你完成一个任务后，只要满足下面任意一项，就应立刻调用这个 skill：

1. **不显然的调试**：解决方案需要超过 10 分钟的调查，而且文档里找不到
2. **错误排查**：修复了一个报错信息带有误导性，或根因并不直观的问题
3. **发现 workaround**：通过实验找到某个工具/框架限制下的绕过方案
4. **配置洞察**：发现了与标准模式不同的项目特有配置
5. **试错成功**：尝试了多个方案后才找到真正有效的做法

### 显式调用

以下场景也要调用：
- 用户运行 `/claudeception` 来回顾本次会话
- 用户说 “save this as a skill” 或类似表达
- 用户问 “what did we learn?”

### 每个任务后的自检

完成任何一个有分量的任务后，问自己：
- “我刚刚是不是花了不少时间在调查某件事？”
- “如果把它写下来，未来的我会不会受益？”
- “这个方案是不是单靠查文档并不容易得到？”

如果任意一个问题答案是 yes，就立刻调用这个 skill。

记住：目标是持续、自治地改进。每一个有价值的发现，都应该有机会在未来的工作会话里继续发挥作用。
