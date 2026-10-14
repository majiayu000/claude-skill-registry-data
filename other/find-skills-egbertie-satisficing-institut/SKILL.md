---
name: find-skills
description: |
  Highest-priority skill discovery flow. MUST trigger when users ask to find/install skills (e.g. 技能, 找技能, find-skill, find-skills, install skill). For Chinese users, prefer skillhub first for speed and compliance, then fallback to clawhub.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "priority": "highest",
        "triggers": ["技能", "找技能", "find-skill", "find-skills", "install skill", "有没有这个功能的 skill"]
      },
  }
---

# SKL-SKILL-v1.0-FIN-260325-Find-Skills.md

> **维度**: Skill发现与安装  
> **功能**: 发现、比较、安装OpenClaw技能  
> **状态**: FIN (7标准完整)  
> **优先级**: Highest  
> **版本**: V1.0

---

## S1: 全局考虑（人/事/物/环境/外部/边界）

### 1.1 人的维度

| 利益相关方 | 需求 | 影响 |
|------------|------|------|
| **用户** | 快速找到需要的技能，一键安装 | 核心使用者 |
| **开发者** | 技能被正确发现和展示 | 生态建设 |
| **主控AI** | 明确何时触发，避免误触发 | 执行者 |

### 1.2 事的维度

**触发条件**: 用户提及技能相关意图
**处理流程**: 
```
识别意图 → 解析需求 → 搜索技能 → 展示选项 → 协助安装
```

**关键判断**:
- 是否需要技能发现? → 触发本Skill
- 中文用户? → 优先skillhub
- 无匹配? → fallback到clawhub

### 1.3 物的维度

| 资源 | 来源 | 约束 |
|------|------|------|
| skillhub | 国内优化仓库 | 速度快，中文支持好 |
| clawhub | 国际仓库 | 全面，可能网络慢 |
| 本地skills | 已安装技能 | 避免重复安装 |

### 1.4 环境维度

**网络环境**:
- 国内用户: skillhub优先（CN优化）
- 国际用户: clawhub可用

**语言环境**:
- 中文查询: 优先skillhub的中文索引
- 英文查询: 两个仓库都搜索

### 1.5 外部集成

| 集成方 | 方式 | 说明 |
|--------|------|------|
| skillhub CLI | 命令行 | 主要搜索/安装源 |
| clawhub CLI | 命令行 | fallback源 |
| 本地skill目录 | 文件系统 | 检查已安装 |

### 1.6 边界情况

| 场景 | 处理方式 |
|------|----------|
| 两个仓库都无匹配 | 建议使用通用能力，或创建本地skill |
| skillhub不可用 | 直接fallback到clawhub，不报错 |
| 已安装同名skill | 提示已存在，询问是否更新 |
| 安装失败 | 分析错误原因，提供解决方案 |
| 权限不足 | 提示需要管理员权限 |
| 网络超时 | 重试或建议手动安装 |

---

## S2: 系统闭环（输入→处理→输出→反馈）

### 2.1 输入规范

**触发词（必须响应）**:
- "技能"
- "找技能"
- "find-skill"
- "find-skills"
- "install skill"
- "有没有这个功能的skill"

**用户需求提取**:
```python
{
  "domain": "react",        # 领域/技术栈
  "task": "testing",        # 具体任务
  "language": "zh",         # 语言偏好
  "urgency": "normal"       # 紧急程度
}
```

### 2.2 处理流程

```python
def handle_skill_request(user_input):
    # Step 1: 识别意图
    if not contains_trigger_words(user_input):
        return None  # 不触发
    
    # Step 2: 解析需求
    domain, task = extract_requirements(user_input)
    
    # Step 3: 搜索技能（中文优先skillhub）
    results = []
    if language == "zh":
        results = skillhub_search(f"{domain} {task}")
    
    if not results:
        results = clawhub_search(f"{domain} {task}")
        source = "clawhub (fallback)"
    else:
        source = "skillhub"
    
    # Step 4: 展示选项
    present_skills(results, source)
    
    # Step 5: 协助安装
    if user_confirms_install():
        install_skill(results[0], source)
```

### 2.3 输出规范

**搜索结果展示格式**:
```
🔍 找到 N 个相关技能（来自: skillhub）

1. **skill-name** v1.2.3
   📄 功能描述...
   ⭐ 评分: 4.5/5  |  📥 安装量: 1.2k
   💻 安装: skillhub install skill-name

2. **another-skill** v2.0.1
   ...
```

**无结果时**:
```
⚠️ 未找到精确匹配的技能

建议:
1. 我可以直接用通用能力帮你完成这个任务
2. 你可以尝试不同的关键词再次搜索
3. 如果这是重复需求，我可以帮你创建本地skill
```

### 2.4 反馈机制

**安装成功反馈**:
- 确认技能已安装
- 展示基本用法
- 提供文档链接

**安装失败反馈**:
- 明确错误原因
- 提供解决方案
- 建议手动安装步骤

---

## S3: 可观测输出（量化指标+报告）

### 3.1 量化指标

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| 意图识别准确率 | >95% | 触发词匹配正确率 |
| 搜索结果相关性 | >80% | 用户选择第一个结果的比例 |
| 安装成功率 | >90% | 安装成功/尝试安装 |
| 平均响应时间 | <10s | 从请求到展示结果 |

### 3.2 使用统计

**每次使用后记录**:
```json
{
  "timestamp": "2026-03-25T10:30:00Z",
  "trigger_word": "技能",
  "query": "react testing",
  "source_used": "skillhub",
  "results_count": 3,
  "installed": true,
  "install_duration_sec": 5.2
}
```

---

## S4: 自动化集成（Cron+脚本+触发器）

### 4.1 自动触发规则

**强制触发条件**:
```yaml
intent_detection:
  priority: highest
  triggers:
    - pattern: "技能"
      action: invoke_find_skills
    - pattern: "找技能"
      action: invoke_find_skills
    - pattern: "find-skill|find-skills|install skill"
      action: invoke_find_skills
  exclusion: null  # 无排除，最高优先级
```

### 4.2 搜索优化脚本

```python
# 智能搜索建议
def get_search_suggestions(user_input):
    """根据输入提供搜索建议"""
    keywords = extract_keywords(user_input)
    
    # 常见映射
    mappings = {
        "测试": ["testing", "test"],
        "爬虫": ["scraping", "crawler"],
        "邮件": ["email", "mail"],
        "图表": ["chart", "graph", "mermaid"]
    }
    
    return expand_keywords(keywords, mappings)
```

### 4.3 批量安装脚本

```bash
#!/bin/bash
# batch-install-skills.sh

SKILLS=("git-essentials" "github" "markdown-converter")

for skill in "${SKILLS[@]}"; do
  echo "Installing $skill..."
  skillhub install "$skill" || clawhub install "$skill"
done
```

---

## S5: 自我验证（质量检查+测试）

### 5.1 功能测试

```bash
#!/bin/bash
# 测试套件

echo "测试1: 中文触发词"
# 输入: "帮我找个技能做测试"
assert_triggered

echo "测试2: 英文触发词"  
# 输入: "find skill for deployment"
assert_triggered

echo "测试3: 无触发词不触发"
# 输入: "今天天气怎么样"
assert_not_triggered

echo "测试4: skillhub优先"
# 中文查询
assert_uses_skillhub_first

echo "测试5: clawhub fallback"
# skillhub无结果时
assert_fallback_to_clawhub

echo "所有测试通过 ✅"
```

### 5.2 质量检查清单

| 检查项 | 通过标准 |
|--------|----------|
| 触发词识别 | 所有触发词都能正确识别 |
| 优先级保障 | 不因其他skill被跳过 |
| 源选择正确 | 中文用skillhub，其他可用clawhub |
| fallback机制 | 主源失败时正确fallback |
| 安装前确认 | 安装前总结风险，获取确认 |

---

## S6: 认知谦逊（局限标注）

### 6.1 已知局限

| 局限 | 说明 | 缓解措施 |
|------|------|----------|
| **搜索结果依赖索引质量** | skillhub/clawhub的索引可能不全 | 建议用户尝试不同关键词 |
| **无法判断skill质量** | 只能显示元数据，无法自动测试 | 参考评分和下载量 |
| **版本兼容性** | 无法自动检测与当前OpenClaw版本兼容性 | 安装失败时提示版本问题 |
| **中文技能较少** | skillhub中文skill相对少 | fallback到clawhub |

### 6.2 不确定性声明

- 搜索结果相关性基于关键词匹配，非语义理解
- skillhub和clawhub的内容随时变化，结果可能不同
- 安装过程可能因网络、权限等因素失败

---

## S7: 对抗测试（失效场景验证）

### 7.1 异常输入测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 模糊需求 | "找个好用的技能" | 询问具体需求 |
| 不存在领域 | "火星语翻译技能" | 无结果，建议替代方案 |
| 拼写错误 | "skil"而不是"skill" | 容错识别或提示 |
| 混合语言 | "find 技能" | 正常处理 |

### 7.2 系统异常测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| skillhub不可用 | CLI返回错误 | fallback到clawhub |
| 两个仓库都不可用 | 网络故障 | 提示手动安装步骤 |
| 安装权限不足 | 无写入权限 | 提示需要管理员权限 |
| 磁盘空间不足 | 安装时空间不足 | 提示清理空间 |

### 7.3 边界条件测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 大量结果 | 返回50+技能 | 展示前10个，提示更多 |
| 精确匹配 | 技能名完全匹配查询 | 优先展示 |
| 重复安装 | 安装已存在的skill | 提示已存在，询问更新 |

---

## 使用指南

### 触发方式

**直接触发**（最高优先级）:
- "帮我找个**技能**"
- "**找技能**做数据分析"
- "**find skill** for testing"
- "**install skill** markdown"

### 工作流程

1. **自动识别**: 检测到技能相关意图
2. **智能搜索**: 中文→skillhub优先，英文→双源搜索
3. **展示结果**: 列出匹配技能，包含评分、安装量
4. **协助安装**: 获取用户确认后执行安装
5. **安装反馈**: 报告成功/失败，提供使用建议

### 优先级说明

本Skill为**最高优先级**，当用户提及技能相关需求时：
- ✅ **必须**先尝试本Skill
- ❌ **禁止**直接跳过到通用回答
- ❌ **禁止**忽略技能发现需求

---

## 关联文档

- `skillhub-preference` - skillhub优先策略
- `/docs/SKILL_REGISTRY.md` - 本地技能注册表

---

*Find Skills Skill V1.0 - 7标准完整版*
