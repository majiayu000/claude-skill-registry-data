---
name: code-porter
description: |
  代码搬运师技能：优先搬运优秀开源项目，禁止重复造轮子。
  Use when: 需要实现新功能、选择技术方案、评估是否自己实现。
  Triggers: "实现", "开发", "创建", "构建", "写一个", "做一个"
---

# Code Porter (代码搬运师)

> 🚚 **核心理念**: 我是代码搬运师，喜欢搬运优秀的开源项目到自己的项目里。非必要，禁止重复造轮子。

## 🔴 第一原则：先搬运，再修改

**无论什么代码，都要先找开源方案！**

```
❌ 错误思路: "这是核心逻辑，我要自己写"
✅ 正确思路: "这是核心逻辑，更要找成熟方案，先搬运再改"

❌ 错误思路: "安全代码太重要了，必须自己实现"  
✅ 正确思路: "安全代码太重要了，自己写更危险，用久经考验的开源库"
```

**搬运优先级**: 成熟开源库 > Fork修改 > 参考实现 > 最后才自己写

## When to Use This Skill

使用此技能当你需要：
- 实现一个新功能或模块
- 选择技术方案或库
- 评估是否需要自己编写代码
- 寻找现有解决方案
- 集成第三方服务或 API

## Not For / Boundaries

此技能不适用于：
- 已有明确技术选型的项目（遵循现有架构）
- 纯学习目的的练习项目（刻意练习除外）

### ⚠️ 常见误区纠正

**误区**: "核心业务逻辑必须自己写"
**正解**: 核心业务逻辑也要**先搬运再修改**！
- 交易系统？先看 [ccxt](https://github.com/ccxt/ccxt)、[hummingbot](https://github.com/hummingbot/hummingbot)
- 风控引擎？先看 [riskfolio-lib](https://github.com/dcajasn/Riskfolio-Lib)
- 推荐系统？先看 [surprise](https://github.com/NicolasHug/Surprise)

**误区**: "安全代码必须自己实现"
**正解**: 安全代码**更要用成熟开源方案**！自己写反而更危险！
- 认证？用 [passport](https://github.com/jaredhanson/passport)、[next-auth](https://github.com/nextauthjs/next-auth)
- 加密？用 [crypto-js](https://github.com/brix/crypto-js)、[bcrypt](https://github.com/kelektiv/node.bcrypt.js)
- JWT？用 [jose](https://github.com/panva/jose)、[jsonwebtoken](https://github.com/auth0/node-jsonwebtoken)

---

## Quick Reference

### 🎯 搬运决策流程

```
需求 → 搜索开源方案 → 评估适配性 → 搬运/集成 → 适配调整
         ↓
    找不到合适的 → 最小化自己实现
```

### 📋 搬运前必问清单

| 问题 | 目的 |
|------|------|
| 1. 有没有现成的库/包？ | npm/pip/cargo 搜索 |
| 2. 有没有类似的开源项目？ | GitHub 搜索 |
| 3. 官方文档有没有推荐方案？ | 查阅官方文档 |
| 4. 社区有没有最佳实践？ | Stack Overflow / Reddit |
| 5. 这个轮子值得自己造吗？ | 成本/收益分析 |

### 🔍 搜索策略

```bash
# 1. 包管理器搜索
npm search <keyword>
pip search <keyword>  # 或 pip index versions <package>

# 2. GitHub 搜索
# 按 stars 排序: stars:>1000 <keyword>
# 按语言过滤: language:typescript <keyword>
# 按最近更新: pushed:>2024-01-01 <keyword>

# 3. Awesome 列表
# 搜索 "awesome-<domain>" 仓库
```

### ✅ 开源项目评估标准

| 指标 | 合格线 | 优秀线 |
|------|--------|--------|
| Stars | >100 | >1000 |
| 最近更新 | <6个月 | <1个月 |
| Issues 响应 | 有回复 | 24h内回复 |
| 文档质量 | 有 README | 有完整文档站 |
| 测试覆盖 | 有测试 | >80% 覆盖 |
| 许可证 | MIT/Apache | MIT |
| 依赖数量 | <20 | <5 |

### 🚫 禁止造轮子清单

以下场景**必须**使用现有方案：

| 领域 | 推荐方案 |
|------|----------|
| HTTP 请求 | axios, fetch, ky |
| 状态管理 | zustand, jotai, redux-toolkit |
| 表单验证 | zod, yup, joi |
| 日期处理 | date-fns, dayjs |
| UI 组件 | shadcn/ui, radix-ui, headless-ui |
| 图表 | recharts, chart.js, echarts |
| 动画 | framer-motion, react-spring |
| 数据库 ORM | drizzle, prisma, typeorm |
| API 客户端 | openapi-typescript, trpc |
| 测试 | vitest, jest, playwright |
| 构建工具 | vite, esbuild, turbopack |
| 代码格式化 | prettier, eslint |
| **认证授权** | next-auth, passport, lucia |
| **加密哈希** | bcrypt, argon2, crypto-js |
| **JWT 处理** | jose, jsonwebtoken |
| **交易系统** | ccxt, hummingbot |
| **风控引擎** | riskfolio-lib, pyfolio |
| **量化分析** | qlib, backtrader, zipline |

### 🔧 搬运集成模式

**模式 1: 直接安装**
```bash
npm install <package>
# 或
pnpm add <package>
```

**模式 2: 复制代码片段**
```typescript
// 来源: https://github.com/xxx/yyy
// 许可证: MIT
// 原作者: @author
// 修改说明: 适配本项目的 TypeScript 类型

// ... 代码 ...
```

**模式 3: Fork + 定制**
```bash
# 1. Fork 仓库
# 2. 修改适配
# 3. 作为 git submodule 或私有包引入
```

**模式 4: 参考实现**
```typescript
// 参考: https://github.com/xxx/yyy/blob/main/src/utils.ts
// 基于原实现重写，适配本项目架构
```

---

## Examples

### Example 1: 需要实现 WebSocket 实时通信

**Input:** "我需要在 React 项目中实现 WebSocket 实时通信"

**Steps:**
1. 搜索现有方案: `npm search websocket react`
2. 发现候选: `socket.io-client`, `@tanstack/react-query` + WebSocket, `use-websocket`
3. 评估 `use-websocket`:
   - Stars: 1.8k ✅
   - 最近更新: 2024 ✅
   - TypeScript 支持: 完整 ✅
   - 文档: 清晰 ✅
4. 决策: 使用 `use-websocket`

**Expected Output:**
```bash
pnpm add react-use-websocket
```

```typescript
import useWebSocket from 'react-use-websocket';

function MyComponent() {
  const { sendMessage, lastMessage } = useWebSocket('wss://api.example.com');
  // ...
}
```

### Example 2: 需要实现 Markdown 渲染

**Input:** "需要在页面中渲染 Markdown 内容，支持代码高亮"

**Steps:**
1. 搜索: `npm search markdown react`
2. 候选: `react-markdown`, `marked`, `markdown-it`
3. 评估 `react-markdown`:
   - Stars: 12k+ ✅
   - 生态: 支持 remark/rehype 插件 ✅
   - 代码高亮: 配合 `react-syntax-highlighter` ✅
4. 决策: 使用 `react-markdown` + `react-syntax-highlighter`

**Expected Output:**
```bash
pnpm add react-markdown react-syntax-highlighter @types/react-syntax-highlighter
```

### Example 3: 需要实现拖拽排序

**Input:** "列表需要支持拖拽排序功能"

**Steps:**
1. 搜索: `npm search drag drop react`
2. 候选: `@dnd-kit/core`, `react-beautiful-dnd`, `react-dnd`
3. 评估 `@dnd-kit`:
   - Stars: 11k+ ✅
   - 维护: 活跃 ✅
   - 性能: 优秀 ✅
   - 无障碍: 支持 ✅
4. 决策: 使用 `@dnd-kit`

**Expected Output:**
```bash
pnpm add @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

---

## 搬运工作流

### Phase 1: 需求分析
```
1. 明确功能需求
2. 确定技术约束（语言、框架、性能要求）
3. 评估复杂度
```

### Phase 2: 方案搜索
```
1. 包管理器搜索
2. GitHub 搜索 (stars:>500)
3. Awesome 列表查找
4. 官方文档推荐
5. 社区讨论（Reddit, HN, Twitter）
```

### Phase 3: 方案评估
```
1. 活跃度检查（最近提交、Issue 响应）
2. 质量检查（测试、文档、TypeScript）
3. 兼容性检查（依赖冲突、版本要求）
4. 许可证检查（MIT/Apache 优先）
5. 安全检查（npm audit, snyk）
```

### Phase 4: 集成实施
```
1. 安装依赖
2. 阅读文档/示例
3. 编写适配代码
4. 测试验证
5. 文档记录（来源、版本、修改）
```

---

## References

- `references/index.md`: 导航索引
- `references/awesome-lists.md`: 常用 Awesome 列表汇总
- `references/license-guide.md`: 开源许可证选择指南

---

## Maintenance

- **Sources**: vibe-coding-cn 方法论, 开源社区最佳实践
- **Last Updated**: 2025-12-30
- **Known Limits**: 
  - 评估标准为经验值，需根据具体场景调整
  - 某些领域可能缺少成熟开源方案
