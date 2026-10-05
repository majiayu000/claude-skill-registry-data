---
name: skill-cleanup
description: 系统性清理本地 skills — 识别无用/低使用率 skill，分类禁用或删除
category: devops
---

# Skill 清理工作流

系统性清理本地 skills：识别无用/低使用率 skill → 分类 → 禁用。

## 触发条件

- 用户说"清理 skills""整理 skills""禁用没用 skill""skills 太多了"
- 上下文 token 消耗过大，需要精简 available_skills

## 清理流程

### 1. 全面摸底

```bash
# 列出所有本地 skills（按目录结构）
find ~/.hermes/skills -name "SKILL.md" -maxdepth 5 | wc -l

# 按修改时间排序 — 最近修改的通常是活跃使用的
find ~/.hermes/skills -name "SKILL.md" -maxdepth 5 -printf "%T+ %p\n" | sort -r | head -40

# 最老的 — 可能从未使用
find ~/.hermes/skills -name "SKILL.md" -maxdepth 5 -printf "%T+ %p\n" | sort | head -40
```

### 2. 分类判断

将 skills 分为四类：

| 类别 | 处理 | 判断依据 |
|------|------|----------|
| 🗑️ 可删除 | `rm -rf` | _archive/ 中已有、明确标记 duplicate、功能已被替代 |
| 🚫 禁用到坟场 | `mv → _archive/` | 领域不相关、3 个月未修改、无对应工具/环境 |
| ⚠️ 需确认 | 询问用户 | 边界情况：学生可能用到、工具类但未确认 |
| ✅ 保留 | 不动 | 日常开发/运维/项目相关、最近修改过 |

### 3. 判断原则

**明确该禁的：**
- 用户领域完全用不到的（如生物/化学/医药/物理/量子计算对前端+AI开发者）
- 依赖不存在工具的（如 Garden skills 依赖 Garden 环境、OpenCLI 依赖 opencli CLI — 除非用户装了）
- 功能已被新版替代的（如旧版 taste-skill 被 open-design 替代）
- 修改时间超过 2 个月且领域不相关的

**需确认的边界：**
- 学生身份可能用到的（latex-posters, market-research-reports, infographics）
- 工具类但不清楚是否有对应环境（matlab, modal）
- 娱乐性质但可能有趣（consciousness-council）

**明确保留的：**
- 最近修改过的（说明在使用）
- 核心工作流相关（软件工程、Git、运维、部署）
- 项目直接相关的（homepage、QQ bot、A2A、ComfyUI）
- 用户明确要求保留的

### 4. 呈现方案

给用户一个清晰的分类表格，每类标注数量和原因，让用户一次性确认。不要一个一个问。

### 5. 批量执行

```bash
# 禁用：移入坟场
mkdir -p ~/.hermes/skills/_archive/<category>/
mv ~/.hermes/skills/<skill-name> ~/.hermes/skills/_archive/<category>/

# 恢复：从坟场移回
mv ~/.hermes/skills/_archive/<category>/<skill-name> ~/.hermes/skills/
```

### 6. 验证

```bash
# 确认已移走
[ -d ~/.hermes/skills/<skill-name> ] && echo "还在" || echo "已移走"

# 坟场概览
find ~/.hermes/skills/_archive -maxdepth 1 -type d | sort
```

## 坟场约定

- `_archive/` 是永久坟场，不删除
- 移入后如需恢复，直接 `mv` 回原位置即可
- 分类存放：scientific/、garden-skills/ 等子目录
- 已有替代品的可放根目录（如 `_archive/codex-duplicate-of-claude-code`）

## 注意事项

- 飞书/Lark skills 不要禁 — 用户已接入飞书消息渠道
- OpenCLI skills 不要禁 — 用户认为很有用
- Nuwa 人物 perspective skills — 等要用时再启用，先留着不删
- 设计类 skills (taste-skill, open-design, creative) — 用户明确要求保留
- 操作不可逆时（如 rm -rf）优先用 mv 到 _archive 代替