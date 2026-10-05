---
name: perplexity-skill-schema
description: "Load when the user is creating, refactoring, auditing, or fixing an Agent Skill. Provides structural audits, content analysis, and interactive auto-fixes based on Perplexity's Skill engineering guide."
version: "1.0.0"
last_updated: "2026-05-15"
depends: []
metadata:
  author: "yinyo"
  category: "skill-engineering"
---

# Yinyo Skill Craft — Skill 工匠

Skill 工程审计与**交互式修复**工具。基于 Perplexity Agents Team 官方指南 + Karpathy CLAUDE.md 编码规范 + yinyo 系列实战经验。

**新增能力**：支持自动修复 + 用户确认模式。

## 核心规则

### 1. Skill 是目录，不是文件

- 单文件 > 50KB → 必须拆分为 hub-and-spoke 结构
- 标准结构：SKILL.md + README.md + docs/ + examples/ + subskills/
- 多级嵌套：300 主题 → 20 领域 → 15 主题/领域

### 2. Description 是路由触发器

- 必须用 `Load when...` 开头
- 说明触发条件，不是功能列表
- 控制在 50 字以内

### 3. 三级渐进式加载

| 层级 | Token 预算 | 内容 | 付费频率 |
|------|-----------|------|----------|
| Index | ~100 | name + description | 每会话 |
| Body | ~5000 | 核心规则 + 快速参考 | 加载后到 compaction |
| Runtime | 无上限 | docs/ + examples/ + subskills/ | 用到时 |

### 4. 删除模型已知内容

- 解释基础概念 → 删除
- 通用编程原则 → 删除
- "If it's easy to explain, the model already knows it. Delete it."

### 5. Karpathy 编码四原则

- Think Before Coding：不确定就问
- Simplicity First：200 行能写完不写 500 行
- Surgical Changes：只碰必须碰的
- Goal-Driven Execution：定义可验证目标

## 交互式修复流程（新增）

### 修复原则

1. **低风险**（结构、格式、版本）→ 自动执行，事后汇报
2. **中风险**（描述重写）→ 展示修改前后对比，用户确认
3. **高风险**（内容删除）→ 列出删除清单，逐项确认

### 修复范围

| 修复类型 | 示例 | 风险等级 |
|----------|------|----------|
| 结构调整 | 单文件拆分为目录 | 低 |
| 描述重写 | 改为 `Load when...` | 中 |
| 内容删除 | 删除模型已知内容 | 高 |
| 版本同步 | 更新 version/last_updated | 低 |
| 格式规范化 | frontmatter 补全 | 低 |

### 修复流程

```
审计 → 列出问题 → 分类风险 → 用户确认 → 自动修复 → 二次审计 → 报告结果
```

### 修复后验证

- 自动执行二次审计
- 对比修复前后分数
- 生成修复报告（改了什么、为什么改、分数变化）

## 审计流程

### 输入

用户提供：
- Skill 目录路径，或
- SKILL.md 内容

### 输出

生成审计报告：

```
## 审计报告：{skill-name}

### 结构审计
- [PASS/WARN/FAIL] 目录结构
- [PASS/WARN/FAIL] 文件大小
- [PASS/WARN/FAIL] 层级深度

### 内容审计
- [PASS/WARN/FAIL] Description 写法
- [PASS/WARN/FAIL] 模型已知内容检测
- [PASS/WARN/FAIL] 信号密度

### 版本管理
- [PASS/WARN/FAIL] 版本号格式
- [PASS/WARN/FAIL] 同步状态

### 总分：{X}/100
### 建议：{priority actions}
```

## 反模式检测清单

### 结构反模式
- [ ] 单文件膨胀（> 50KB）
- [ ] 描述过长（> 100 tokens）
- [ ] 无层级（> 50 个主题平铺）
- [ ] 无版本管理

### 内容反模式
- [ ] 模型已知内容（基础概念解释）
- [ ] 过度工程（抽象层 > 实际需求）
- [ ] 流程表演（约束执行合规而非成品质量）
- [ ] 无验证标准

### yinyo 特有毒点
- [ ] 版本回退犹豫（质量下降不立即回退）
- [ ] 流程越完整质量越差（yinyo-writer 教训）
- [ ] 单文件 277KB（yinyo-liuyao 教训）

## 修复建议模板

### 单文件膨胀 → 拆分

```
原：SKILL.md (277KB)
新：
├── SKILL.md (5KB: 核心规则)
├── docs/
│   ├── rules.md (50KB: 120条规则)
│   ├── examples.md (100KB: 412卦例)
│   └── reference.md (30KB: 64卦纳甲表)
└── subskills/
    ├── edge-case-1.md
    └── edge-case-2.md
```

### Description 错误 → 修正

```
❌ "This Skill helps you write articles."
✅ "Load when the user needs to write a WeChat public account article."
```

## 快速参考

### Skill 命名
```
yinyo-{domain}-{action}
```

### 文件大小
- Index: < 1KB
- Body: < 50KB
- Runtime: 无上限

### 版本管理
- SemVer: MAJOR.MINOR.PATCH
- 每次更新同步：SKILL.md + README.md + Git commit + memory

### 修复触发词
- "修复这个Skill" → 进入交互式修复模式
- "自动修复" → 执行低风险修复
- "帮我改" → 展示修改建议，等待确认
