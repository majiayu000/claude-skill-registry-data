---
name: template-skill-cn
description: Skill 模板（中文增强版）：演示如何编写自定义 Skill（YAML frontmatter + SKILL.md 主体 + scripts/reference 资源），用于学习 Progressive Disclosure 的工作方式。
---

# Skill 模板（template-skill）

这个 Skill 不是为了“解决业务问题”，而是为了教学：让你快速理解 Skill 的目录结构、写法，以及 Agent 什么时候会加载它。

## 什么时候使用这个 Skill？

- 你要创建一个新的 Skill
- 你希望把某个团队/项目的“固定流程”沉淀为可复用的指令
- 你希望 Skill 带上脚本/参考文档，并且按需读取（渐进式加载）

## Skill 基本结构

```
template-skill/
├── SKILL.md
├── reference/
│   └── guide.md
└── scripts/
    └── demo.ts
```

## 建议写法（强烈建议）

1. **frontmatter 必须写好**：`name` 和 `description` 决定“模型是否会想到用这个 Skill”
2. **SKILL.md 主体写流程**：以“步骤/检查清单”的形式写，便于模型执行
3. **把长内容放到 reference/**：例如 API 文档、规范、FAQ；需要时再让模型 read_file
4. **把确定性操作放到 scripts/**：例如代码生成、格式化、校验；需要时再让模型 bash 执行脚本

## 参考资料（按需读取）

阅读 [Guide](./reference/guide.md) 了解更详细的写作建议与示例。

## 可执行脚本（按需执行）

当你需要演示“Skill 引用脚本 + Agent 运行脚本”的链路时，运行：

```bash
node scripts/demo.ts
```
