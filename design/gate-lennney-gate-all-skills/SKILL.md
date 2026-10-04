---
name: gate
description: "技能路由入口 / Entry router. 根据用户输入路由到对应技能。Use when the user isn't sure what they need, says '帮我做个网站', '我想优化一下', or any general request that could map to multiple skills. Routes to gate-discuss / gate-frontend / gate-seo / gate-optimize / design / engineering / AI / product skills."

trigger: 用户不确定使用哪个技能
input: 用户需求
output: 路由到对应技能
next: 所有技能
dependencies: 无
---

# AI 技能路由系统

当用户提出需求时，根据以下规则路由到对应的技能。

## 路由决策规则

### 规则 1：识别用户意图

分析用户输入，识别以下意图类型：

| 意图类型 | 关键词示例 | 路由目标 |
|----------|------------|----------|
| 建站 | 搭建、新建、从零开始 | `/gate-discuss` |
| 前端开发 | 页面、组件、样式、UI | `/gate-frontend` |
| SEO | 搜索引擎、SEO、优化 | `/gate-seo` |
| UI 设计 | 设计、界面、原型、UX | `/ui-ux-pro-max` |
| 组件设计 | 组件、复用、组件库 | `/component-design` |
| 样式 | Tailwind、CSS、样式 | `/styling-tailwind` |
| 代码审查 | 审查、review、检查代码 | `/code-review` |
| 调试 | bug、调试、问题、错误 | `/diagnosing-bugs` |
| 测试 | 测试、TDD、单元测试 | `/tdd` |
| 重构 | 重构、优化代码、代码结构 | `/ai-refactoring` |
| 产品 | PRD、需求、用户故事 | `/prd-development` |
| 优化 | 优化、性能、速度 | `/gate-optimize` |

### 规则 2：检查项目状态

在路由前，检查当前项目状态：

```bash
# 检查是否存在项目
ls package.json 2>/dev/null    # Node.js 项目
ls pyproject.toml 2>/dev/null  # Python 项目
ls Cargo.toml 2>/dev/null      # Rust 项目

# 检查是否有 Git 仓库
git status 2>/dev/null

# 检查是否有部署配置
ls vercel.json 2>/dev/null     # Vercel 部署
ls netlify.toml 2>/dev/null    # Netlify 部署
```

**状态判断**：
- 无项目 → 新建项目流程（`/gate-discuss`）
- 有项目但未完成 → 继续开发流程
- 项目已上线 → 优化流程（`/gate-optimize`）

### 规则 3：路由优先级

当多个技能匹配时，按以下优先级选择：

1. **用户明确指定的技能** → 直接调用
2. **当前阶段最相关的技能** → 根据项目状态 + `next` 字段选择
3. **用户意图最匹配的技能** → 根据关键词匹配
4. **默认路由** → 询问用户具体需求

### 规则 4：推荐下一步

调用完一个 skill 后，读取它的 `next` 字段，自动推荐给用户。

> 每个 skill 的完整路由信息（trigger / next / dependencies）在其自身的 SKILL.md 的 frontmatter 中。不需要在这里维护副本。

## 路由决策流程

```
用户输入
    ↓
分析意图（关键词匹配）
    ↓
检查项目状态
    ↓
选择最匹配的技能
    ↓
调用技能
    ↓
执行任务
    ↓
更新项目状态
    ↓
推荐下一个技能
```

## 使用示例

### 示例 1：新用户想建站
```
用户：我想搭建一个个人网站
AI：分析意图 → 建站
AI：检查项目状态 → 无项目
AI：路由到 → /gate-discuss
```

### 示例 2：用户有项目需要优化
```
用户：我的网站加载太慢了
AI：分析意图 → 性能优化
AI：检查项目状态 → 项目已部署
AI：路由到 → /gate-perf
```

### 示例 3：用户需要设计帮助
```
用户：我想设计一个登录页面
AI：分析意图 → UI 设计
AI：检查项目状态 → 有项目
AI：路由到 → /ui-ux-pro-max
```

## 注意事项

1. **优先使用 gate-* 技能**：建站流程和优化流程优先使用对应的 gate 技能
2. **直接调用技能**：设计、工程、AI、产品类技能可以直接调用
3. **检查依赖**：调用技能前检查是否有依赖技能
4. **更新状态**：完成技能后更新项目状态
5. **推荐下一步**：完成后推荐下一个相关技能
