---
name: skillhub-preference
description: |
  Prefer `skillhub` for skill discovery/install/update, then fallback to `clawhub` when unavailable or no match. Use when users ask about skills, 插件, or capability extension.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "policy": "skillhub_first",
        "fallback": "clawhub"
      },
  }
---

# SKL-SKILL-v1.0-FIN-260325-Skillhub-Preference.md

> **维度**: Skill源选择策略  
> **功能**: 定义skillhub优先、clawhub fallback的使用策略  
> **状态**: FIN (7标准完整)  
> **版本**: V1.0

---

## S1: 全局考虑（人/事/物/环境/外部/边界）

### 1.1 人的维度

| 利益相关方 | 需求 | 影响 |
|------------|------|------|
| **用户** | 快速获取技能，国内访问流畅 | 体验优先 |
| **开发者** | 技能分发渠道选择 | 生态策略 |
| **主控AI** | 明确的选择优先级 | 决策依据 |

### 1.2 事的维度

**策略核心**: skillhub优先，clawhub备用

**决策树**:
```
需要搜索/安装/更新skill?
    ↓
用户是中文用户?
    ├── 是 → 优先skillhub
    │        ↓
    │        skillhub可用且有结果?
    │            ├── 是 → 使用skillhub结果
    │            └── 否 → fallback到clawhub
    │
    └── 否 → 双源搜索，综合结果
```

### 1.3 物的维度

| 资源 | 特点 | 适用场景 |
|------|------|----------|
| **skillhub** | CN优化，速度快，中文支持 | 国内用户首选 |
| **clawhub** | 国际源，全面 | fallback，国际用户 |
| **两者** | 互补 | 无匹配时扩大搜索 |

### 1.4 环境维度

**网络环境**:
- 中国大陆: skillhub显著更快
- 国际网络: 两者均可

**语言环境**:
- 中文界面: skillhub中文内容更多
- 英文界面: clawhub内容更全面

### 1.5 外部集成

| 集成方 | 关系 | 策略 |
|--------|------|------|
| skillhub CLI | 主要源 | 优先调用 |
| clawhub CLI | 备用源 | 失败时调用 |
| find-skills | 上层封装 | 使用本策略 |

### 1.6 边界情况

| 场景 | 处理方式 |
|------|----------|
| skillhub CLI未安装 | 直接使用clawhub |
| skillhub返回空结果 | 明确告知fallback到clawhub |
| clawhub也无结果 | 建议替代方案 |
| 两者结果冲突 | 优先展示skillhub结果，标注clawhub备选 |
| skillhub临时不可用 | 自动fallback，不报错 |

---

## S2: 系统闭环（输入→处理→输出→反馈）

### 2.1 输入规范

**触发条件**: 涉及skill源选择的场景
- skill发现
- skill安装
- skill更新

**参数**:
```python
{
  "action": "search|install|update",
  "query": "markdown converter",
  "language": "zh",  # 用户语言偏好
  "strict": false    # 是否严格使用skillhub
}
```

### 2.2 处理流程

```python
def select_skill_source(action, query, language="zh"):
    """选择skill源的策略实现"""
    
    # Step 1: 优先尝试skillhub
    if language == "zh" or not strict_mode:
        result = try_skillhub(action, query)
        if result.success and result.has_matches:
            return {
                "source": "skillhub",
                "data": result.data,
                "fallback": False
            }
    
    # Step 2: fallback到clawhub
    result = try_clawhub(action, query)
    if result.success:
        return {
            "source": "clawhub (fallback)",
            "data": result.data,
            "fallback": True,
            "note": "skillhub无匹配，已fallback到clawhub"
        }
    
    # Step 3: 都失败
    return {
        "source": None,
        "error": "两个源都不可用或无匹配",
        "suggestion": "尝试其他关键词或手动安装"
    }
```

### 2.3 输出规范

**成功响应（skillhub）**:
```
🎯 来自 skillhub 的结果（CN优化源）

找到 3 个匹配技能：
1. markdown-converter v2.1.0
   ...
```

**成功响应（clawhub fallback）**:
```
⚠️ skillhub 无匹配结果，已自动切换到 clawhub

🎯 来自 clawhub (fallback) 的结果

找到 2 个匹配技能：
1. md-to-pdf v1.5.0
   ...
```

**失败响应**:
```
❌ 两个源都未找到匹配技能

建议：
1. 尝试不同的关键词（如 "markdown" 改为 "md"）
2. 我可以直接帮你完成这个任务
3. 访问 https://clawhub.com 浏览更多技能
```

### 2.4 反馈机制

**源选择透明度**:
- 明确告知用户使用的源
- fallback时明确说明原因
- 提供源切换选项（如果用户坚持）

**性能反馈**:
- 记录每个源的响应时间
- 源不可用时报错并fallback

---

## S3: 可观测输出（量化指标+报告）

### 3.1 量化指标

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| skillhub命中率 | >60% | skillhub成功/总请求 |
| fallback率 | <40% | clawhub使用/总请求 |
| fallback成功率 | >90% | clawhub找到结果/fallback次数 |
| 平均响应时间(skillhub) | <3s | 国内网络 |
| 平均响应时间(clawhub) | <5s | 国内网络 |

### 3.2 源使用统计

**周期性报告**:
```
📊 Skill源使用统计（过去30天）
━━━━━━━━━━━━━━━━━━━━
skillhub: 72% (命中率高 ✓)
clawhub: 28% (fallback)
━━━━━━━━━━━━━━━━━━━━
平均响应: skillhub 1.2s, clawhub 3.5s
建议: 当前策略合理，继续保持
```

---

## S4: 自动化集成（策略自动化）

### 4.1 自动源选择

```yaml
# 嵌入到find-skills的决策流程
source_selection:
  default: skillhub
  conditions:
    - if: language == "zh"
      then: skillhub_first
    - if: skillhub_unavailable
      then: clawhub_fallback
    - if: skillhub_no_match
      then: clawhub_fallback_with_notice
```

### 4.2 健康检查

```python
def check_source_health():
    """检查各源健康状态"""
    health = {}
    
    # 检查skillhub
    try:
        result = subprocess.run(["skillhub", "list"], timeout=5)
        health["skillhub"] = "healthy" if result.returncode == 0 else "unhealthy"
    except:
        health["skillhub"] = "unavailable"
    
    # 检查clawhub
    try:
        result = subprocess.run(["clawhub", "list"], timeout=5)
        health["clawhub"] = "healthy" if result.returncode == 0 else "unhealthy"
    except:
        health["clawhub"] = "unavailable"
    
    return health
```

### 4.3 自适应策略

```python
def adaptive_source_selection():
    """根据历史性能自适应调整"""
    stats = get_usage_stats(days=7)
    
    # 如果skillhub命中率持续低，调整策略
    if stats.skillhub_hit_rate < 0.3:
        logger.warning("skillhub命中率过低，建议检查索引质量")
    
    # 如果clawhub响应太慢，延长超时
    if stats.clawhub_avg_response > 10:
        config.clawhub_timeout = 15
```

---

## S5: 自我验证（策略验证+监控）

### 5.1 策略验证测试

```bash
#!/bin/bash
# 策略验证测试

echo "测试1: 中文查询优先skillhub"
result=$(find_skill "中文查询" --language zh)
assert_source "skillhub"

echo "测试2: skillhub无结果时fallback"
# 使用非常冷门的关键词
result=$(find_skill "xyzabc123" --language zh)
assert_fallback "clawhub"

echo "测试3: 明确告知fallback"
assert_contains "已自动切换到 clawhub"

echo "测试4: 两个源都无结果"
# 使用不可能存在的关键词
result=$(find_skill "this_skill_definitely_not_exist_12345")
assert_error "两个源都未找到"

echo "所有策略测试通过 ✅"
```

### 5.2 质量检查清单

| 检查项 | 通过标准 |
|--------|----------|
| 中文用户skillhub优先 | 中文查询先调用skillhub |
| fallback透明度 | fallback时明确告知用户 |
| 失败处理 | 两个源都失败时给出建议 |
| 性能差异 | skillhub响应时间 < clawhub |
| 用户选择权 | 用户可强制指定源（可选） |

---

## S6: 认知谦逊（局限标注）

### 6.1 已知局限

| 局限 | 说明 | 缓解措施 |
|------|------|----------|
| **skillhub内容相对较少** | 相比clawhub，skillhub收录的技能较少 | fallback机制补偿 |
| **skillhub更新延迟** | 新技能可能在skillhub上更新较慢 | 提示用户尝试clawhub |
| **网络环境影响大** | 国内访问clawhub可能很慢 | 明确优先skillhub的策略价值 |
| **无法判断内容质量** | 仅根据元数据选择，无法自动测试 | 依赖社区评分 |

### 6.2 策略不确定性

- skillhub和clawhub的内容随时变化，策略效果可能波动
- 国际用户可能更适合clawhub优先，但本策略以国内用户为主
- 源的健康状态变化可能影响用户体验

---

## S7: 对抗测试（策略失效场景）

### 7.1 源不可用测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| skillhub CLI不存在 | 未安装skillhub命令 | 直接使用clawhub，不报错 |
| skillhub网络超时 | 模拟网络故障 | 超时后fallback到clawhub |
| clawhub也不可用 | 两个源都故障 | 提示手动安装方案 |

### 7.2 结果质量测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| skillhub返回低质量结果 | 结果相关性差 | 尝试clawhub获取更好结果 |
| 结果冲突 | 同名skill在两个源都有 | 优先展示skillhub版本，标注差异 |
| 版本差异 | 两个源版本不同 | 提示版本差异，让用户选择 |

### 7.3 极端场景测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 连续fallback | 连续10次查询都fallback | 策略不变，但记录日志 |
| 快速切换 | 频繁切换源 | 保持策略稳定性 |
| 用户强制指定 | 用户说"用clawhub" | 尊重用户选择（如果实现） |

---

## 使用指南

### 策略原则

**核心原则**: **skillhub优先，clawhub备用**

**决策规则**:
1. 中文用户 → 先查skillhub
2. skillhub有结果 → 使用skillhub
3. skillhub无结果 → 明确告知，fallback到clawhub
4. 两个源都无结果 → 建议替代方案

### 透明沟通模板

**使用skillhub时**:
```
🎯 从 skillhub（国内优化源）搜索到以下技能...
```

**fallback到clawhub时**:
```
⚠️ skillhub 未找到匹配，已自动切换到 clawhub
🎯 从 clawhub (国际源) 搜索到以下技能...
```

---

## 关联文档

- `find-skills` - 上层封装，使用本策略
- `/docs/CLAWHUB_VS_SKILLHUB.md` - 两源详细对比

---

*Skillhub Preference Policy V1.0 - 7标准完整版*
