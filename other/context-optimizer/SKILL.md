---
name: context-optimizer
description: |
  上下文优化器 - 智能对话压缩与记忆分层管理
  
  核心功能:
  1. 智能摘要 - 自动识别关键决策，压缩冗余内容
  2. 分层记忆 - 短期/中期/长期自动归档
  3. Token预警 - 80%时主动建议压缩
  4. 上下文重建 - 从压缩状态恢复关键信息
  
  触发条件:
  - Token消耗达80%
  - 用户发送"/compact"
  - 对话超过50轮
  - 用户明确说"优化上下文"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "triggers": ["/compact", "优化上下文", "Token快用完了", "上下文太长"],
        "priority": "high"
      },
  }
---

# SKL-SKILL-v1.0-FIN-260326-Context-Optimizer.md

> **维度**: 对话上下文管理  
> **功能**: 智能压缩、分层记忆、Token预警  
> **状态**: FIN (7标准完整)  
> **版本**: V1.0  
> **创建时间**: 2026-03-26

---

## S1: 全局考虑（人/事/物/环境/外部/边界）

### 1.1 人的维度

| 利益相关方 | 需求 | 影响 |
|------------|------|------|
| **用户(Egbertie)** | 避免Token耗尽，保留关键信息 | 核心受益者 |
| **主控AI** | 知道何时压缩，如何恢复 | 执行者 |
| **未来会话** | 能从压缩状态恢复上下文 | 间接受益 |

### 1.2 事的维度

**触发条件**:
- Token消耗 ≥ 80%
- 对话轮数 ≥ 50
- 用户主动请求 `/compact`
- 系统检测到上下文膨胀

**处理流程**:
```
触发检测 → 信息分层 → 智能摘要 → 压缩归档 → 重建索引
```

### 1.3 物的维度

| 资源 | 类型 | 约束 |
|------|------|------|
| 对话历史 | 输入 | 需分析内容价值 |
| Token配额 | 限制 | 通常4K-128K不等 |
| 存储空间 | 输出 | 压缩后存memory/ |
| 计算时间 | 处理 | 摘要生成耗时 |

### 1.4 环境维度

**Token压力场景**:
- 长对话（>50轮）
- 代码/文档编辑（大量文本）
- 多文件分析（大量上下文）

**压缩策略**:
| 场景 | 策略 |
|------|------|
| 闲聊/问候 | 直接删除 |
| 任务执行过程 | 保留结果，删除中间步骤 |
| 关键决策 | 完整保留 |
| 代码/文档 | 保留最终版本，删除迭代过程 |

### 1.5 外部集成

| 集成方 | 方式 | 说明 |
|--------|------|------|
| 系统/compact | 命令触发 | 用户主动压缩 |
| Token监控 | 自动触发 | 80%时主动建议 |
| Memory系统 | 文件存储 | 压缩后存memory/ |

### 1.6 边界情况

| 场景 | 处理方式 |
|------|----------|
| Token已耗尽 | 无法压缩，提示/new创建新对话 |
| 全是对话无实质内容 | 建议直接/reset |
| 用户拒绝压缩 | 记录，继续直到硬性限制 |
| 压缩后信息丢失 | 保留完整版到文件，摘要供会话使用 |
| 压缩失败 | 回退，提示手动处理 |

---

## S2: 系统闭环（输入→处理→输出→反馈）

### 2.1 输入规范

**触发信号**:
```python
{
  "trigger_type": "auto|manual|system",
  "token_pct": 82,           # 当前Token百分比
  "turn_count": 55,          # 对话轮数
  "context_size_kb": 45      # 上下文大小
}
```

### 2.2 处理流程

```python
class ContextOptimizer:
    def optimize(self, context):
        # Step 1: 信息分层
        layers = self.classify_messages(context)
        #   - critical: 关键决策、TODO、用户偏好
        #   - important: 任务结果、配置变更
        #   - normal: 执行过程、尝试步骤
        #   - disposable: 闲聊、确认、重复内容
        
        # Step 2: 分层处理
        summary = {
            "critical": self.preserve_full(layers["critical"]),
            "important": self.summarize(layers["important"]),
            "normal": self.compress(layers["normal"]),
            "disposable": self.discard(layers["disposable"])
        }
        
        # Step 3: 生成压缩包
        compressed = self.generate_summary(summary)
        
        # Step 4: 持久化
        self.save_to_memory(compressed)
        
        return compressed
```

### 2.3 输出规范

**压缩报告**:
```markdown
## 上下文压缩完成

**压缩前**: 55轮 / 82% Token
**压缩后**: 5项关键信息 / 15% Token

### 保留的关键决策
1. [决策1] ...
2. [决策2] ...

### 已完成的任务
- [任务1] ✅ ...
- [任务2] ✅ ...

### 待办事项 (TODO)
- [ ] ...

### 用户偏好更新
- ...

### 完整记录
已保存至: memory/2026-03-26-compact-HHMM.md
```

### 2.4 反馈机制

**用户确认**:
- 展示压缩摘要
- 询问是否有遗漏
- 允许补充关键信息

**后续恢复**:
- 新会话可读取压缩文件
- 自动重建上下文

---

## S3: 可观测输出（量化指标+报告）

### 3.1 量化指标

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| 压缩率 | >60% | (原Token-压缩后)/原Token |
| 关键信息保留率 | 100% | 用户确认无遗漏 |
| 压缩耗时 | <5s | 从触发到完成 |
| 误删率 | <5% | 压缩后用户补充次数/总压缩次数 |

### 3.2 使用报告

**每次压缩后生成**:
```
🧠 上下文优化报告
━━━━━━━━━━━━━━━━━━━━
原始大小: 45KB (82% Token)
压缩大小: 12KB (18% Token)
压缩率: 73%
保留决策: 5项
保留TODO: 3项
耗时: 2.3s
━━━━━━━━━━━━━━━━━━━━
状态: ✅ 成功
```

---

## S4: 自动化集成（Cron+脚本+触发器）

### 4.1 Token预警机制

```python
# 嵌入到token-monitor中
def check_context_pressure():
    if token_pct >= 80:
        suggest_compact()
    if token_pct >= 90:
        strongly_recommend_compact()
    if token_pct >= 95:
        warn_imminent_overflow()
```

### 4.2 自动压缩脚本

```bash
#!/bin/bash
# auto-compact.sh - 定期自动压缩

TOKEN_PCT=$(get_current_token_pct)
if [ "$TOKEN_PCT" -ge 85 ]; then
  python3 /root/.openclaw/workspace/scripts/context_optimizer.py auto
fi
```

### 4.3 会话启动恢复

```python
def on_session_start():
    """会话启动时检查是否有压缩的上下文"""
    latest_compact = find_latest_compact()
    if latest_compact and is_recent(latest_compact, hours=24):
        return f"检测到近期压缩的上下文，发送 /restore 恢复"
```

---

## S5: 自我验证（质量检查+测试）

### 5.1 功能测试

```python
def test_compression():
    # 测试1: 正常压缩
    context = generate_test_context(turns=50, token_pct=85)
    result = optimizer.optimize(context)
    assert result.compression_ratio > 0.6
    assert result.critical_retained == 100%
    
    # 测试2: 无实质内容
    context = generate_chat_only_context(turns=30)
    result = optimizer.optimize(context)
    assert result.recommendation == "建议 /reset"
    
    # 测试3: Token已耗尽
    context = generate_test_context(token_pct=99)
    result = optimizer.optimize(context)
    assert result.error == "Token不足，无法压缩"
```

### 5.2 质量检查清单

| 检查项 | 通过标准 |
|--------|----------|
| 关键决策保留 | 所有标记为critical的内容保留 |
| TODO完整性 | 所有未完成TODO保留 |
| 用户偏好 | 所有偏好更新保留 |
| 压缩率达标 | ≥60% |
| 恢复可用 | 压缩文件可被后续会话读取 |

---

## S6: 认知谦逊（局限标注）

### 6.1 已知局限

| 局限 | 说明 | 缓解措施 |
|------|------|----------|
| **语义理解限制** | 可能误判某些内容为"可删除" | 用户确认环节 |
| **压缩不可逆** | 丢弃的内容无法自动恢复 | 完整版保存到文件 |
| **长文档处理** | 超长文档压缩可能耗时 | 分段处理 |
| **代码上下文** | 可能丢失调试过程的价值 | 保留关键错误信息 |

### 6.2 不确定性声明

- 压缩质量依赖于内容识别算法，可能有误判
- 不同模型的Token计算方式可能不同
- 极端情况下（Token=99%）可能无法完成压缩

---

## S7: 对抗测试（失效场景验证）

### 7.1 异常输入测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 空上下文 | 无任何对话 | 提示无需压缩 |
| 单轮对话 | 只有1轮 | 提示无需压缩 |
| 全是对话 | 无实质任务 | 建议/reset |
| 混合内容 | 任务+闲聊混合 | 正确分类处理 |

### 7.2 边界条件测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| Token=80% | 边界触发 | 建议压缩 |
| Token=95% | 紧急状态 | 强烈建议压缩 |
| Token=99% | 极限状态 | 提示/new |
| 超大上下文 | >100KB | 分段处理 |

### 7.3 恢复测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 正常恢复 | 从压缩文件重建 | 关键信息完整 |
| 文件损坏 | 压缩文件损坏 | 提示无法恢复 |
| 过期恢复 | >7天的压缩文件 | 提示可能过时 |

---

## 使用指南

### 触发方式

**自动触发**:
- Token ≥ 80% 时主动建议
- 对话轮数 ≥ 50 时提示

**手动触发**:
- 发送 `/compact`
- 说"优化上下文"

### 压缩级别

| 级别 | 压缩率 | 适用场景 |
|------|--------|----------|
| 轻度 | 30% | Token还够，仅清理闲聊 |
| 中度 | 60% | 标准压缩，平衡保留 |
| 深度 | 80% | Token告急，仅保留关键 |

### 恢复命令

```
/restore [日期]  # 恢复指定日期的压缩上下文
/restore-latest   # 恢复最近的压缩
```

---

## 关联文档

- `/scripts/context_optimizer.py` - 核心实现
- `/scripts/token_monitor_v21.py` - Token监控集成
- `memory/COMPACT_INDEX.md` - 压缩文件索引

---

*Context Optimizer Skill V1.0 - 7标准完整版*
