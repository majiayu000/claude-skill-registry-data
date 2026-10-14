---
name: token-optimizer
description: |
  Token优化与休眠控制集成模块 V2.1
  
  优化点:
  1. 将休眠检测(每10分钟)整合到Token监控(每6小时)，节省144次/天 ≈ 2000 token
  2. 动态频率调整 - 根据Token状态自动调整监控频率
  3. 分级响应 - L5-L1不同策略
  4. 集成上下文优化建议 - 80%Token时建议压缩
  
  核心改进:
  - 原方案: 2个独立任务(监控+检测) = 每天168次运行
  - 新方案: 1个集成任务 = 每天4-12次运行
  - 节省: ~90% Token消耗
metadata:
  {
    "openclaw":
      {
        "emoji": "⚡",
        "version": "2.1",
        "optimization": "90% token savings vs v2.0"
      },
  }
---

# SKL-SKILL-v1.0-FIN-260326-Token-Optimizer.md

> **维度**: Token效率优化  
> **功能**: 监控+休眠检测集成，动态频率调整  
> **状态**: FIN (7标准完整)  
> **版本**: V2.1  
> **优化效果**: 节省90% Token (vs V2.0)  
> **创建时间**: 2026-03-26

---

## S1: 全局考虑（人/事/物/环境/外部/边界）

### 1.1 人的维度

| 利益相关方 | 需求 | 影响 |
|------------|------|------|
| **用户** | Token不被浪费，系统稳定运行 | 核心受益者 |
| **主控AI** | 明确何时降级、何时休眠 | 执行者 |
| **未来会话** | Token记录准确，可预测 | 间接影响 |

### 1.2 事的维度

**问题发现**: 原V2.0方案中，休眠检测每10分钟运行一次，每天144次，消耗约2000 Token。

**优化方案**: 将休眠检测逻辑整合到Token监控任务中。

**处理流程**:
```
Token监控运行
    ↓
检查当前Token百分比
    ↓
确定当前等级(L5-L1)
    ↓
如果等级变化:
    - 调整自身频率
    - 调整其他任务频率
    - 建议休眠(如果L1)
    ↓
如果Token ≥ 80%:
    - 建议上下文压缩
    ↓
记录状态，等待下次运行
```

### 1.3 物的维度

| 资源 | 原方案 | 新方案 | 节省 |
|------|--------|--------|------|
| 日运行次数 | 168次 | 4-12次 | 93% |
| 日Token消耗 | ~2400 | ~200 | 92% |
| 存储(状态文件) | 2个 | 1个 | 50% |

### 1.4 环境维度

**Token压力等级**:
| 等级 | Token范围 | 监控频率 | 日运行次数 |
|------|-----------|----------|------------|
| L5 | 100-70% | 每6小时 | 4次 |
| L4 | 70-50% | 每8小时 | 3次 |
| L3 | 50-30% | 每12小时 | 2次 |
| L2 | 30-15% | 每天6AM | 1次 |
| L1 | <15% | 暂停 | 0次 |

### 1.5 外部集成

| 集成方 | 方式 | 说明 |
|--------|------|------|
| Cron系统 | 任务调度 | 频率动态调整 |
| Context Optimizer | 调用 | Token≥80%时建议压缩 |
| Hibernate Control | 调用 | Token<15%时进入休眠 |
| Memory系统 | 文件记录 | 保存Token历史 |

### 1.6 边界情况

| 场景 | 处理方式 |
|------|----------|
| 首次运行无历史 | 默认L5配置 |
| Token跳跃式变化 | 按当前值处理，记录异常 |
| 调整失败 | 记录错误，下次重试 |
| 用户手动干预 | 尊重用户选择，暂停自动调整 |

---

## S2: 系统闭环（输入→处理→输出→反馈）

### 2.1 输入规范

**参数**:
```python
{
  "current_token_pct": 75,     # 当前Token百分比
  "session_duration_min": 120, # 会话时长
  "tasks_executed": 45,        # 已执行任务数
  "context_size_kb": 32        # 上下文大小
}
```

### 2.2 处理流程

```python
class TokenOptimizer:
    def run(self, token_pct):
        # Step 1: 确定等级
        level = self.get_level(token_pct)
        
        # Step 2: 检查等级变化
        if level != self.last_level:
            self.adjust_frequency(level)
            self.log_transition(self.last_level, level)
        
        # Step 3: 检查上下文压力
        if token_pct >= 80:
            self.suggest_context_compression()
        
        # Step 4: 检查休眠条件
        if level == "L1":
            self.suggest_hibernation()
        
        # Step 5: 生成报告
        return self.generate_report()
```

### 2.3 输出规范

**监控报告**:
```markdown
⚡ Token优化报告 (V2.1)
━━━━━━━━━━━━━━━━━━━━
当前Token: 75% (L5 - 正常运营)
等级变化: 无
下次监控: 6小时后

任务频率:
- morning-report: 09:07 每天 ✅
- token-monitor: 每6小时 ✅
- evening-totem: 18:00 每天 ✅
- weekly-check: 周日 03:17 ✅
- daily-backup: 03:00 每天 ✅

上下文状态: 正常 (32KB)
建议操作: 无
━━━━━━━━━━━━━━━━━━━━
```

### 2.4 反馈机制

**等级变化时**:
- 报告调整内容
- 说明调整原因
- 预告下次调整阈值

**预警时**:
- Token≥80%: 建议压缩上下文
- Token<30%: 预告即将进入节省模式
- Token<15%: 建议进入休眠

---

## S3: 可观测输出（量化指标+报告）

### 3.1 量化指标

| 指标 | 原V2.0 | 新V2.1 | 改进 |
|------|--------|--------|------|
| 日运行次数 | 168次 | 4-12次 | -93% |
| 日Token消耗 | ~2400 | ~200 | -92% |
| 响应延迟 | 10分钟 | 6-24小时 | +效率 |
| 准确性 | 高 | 高 | 持平 |

### 3.2 效率对比

```
📊 Token优化效果对比
━━━━━━━━━━━━━━━━━━━━
          V1.0    V2.0    V2.1
━━━━━━━━━━━━━━━━━━━━
任务数    6       6       5
日运行    168     168     4-12
日Token   ~11000  ~3000   ~200
节省率    -       73%     98%
━━━━━━━━━━━━━━━━━━━━
```

---

## S4: 自动化集成（Cron+脚本+触发器）

### 4.1 动态Cron调整

```python
def adjust_cron_schedule(level):
    """根据等级调整Cron频率"""
    schedules = {
        "L5": "0 */6 * * *",   # 每6小时
        "L4": "0 */8 * * *",   # 每8小时
        "L3": "0 */12 * * *",  # 每12小时
        "L2": "0 6 * * *",     # 每天6AM
        "L1": "disabled"       # 暂停
    }
    
    new_schedule = schedules[level]
    if new_schedule == "disabled":
        disable_cron_job("token-monitor")
    else:
        update_cron_schedule("token-monitor", new_schedule)
```

### 4.2 集成脚本

```python
#!/usr/bin/env python3
# token_optimizer.py - 主运行脚本

import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from token_monitor_v21 import TokenMonitor
from context_optimizer_client import suggest_compression
from hibernation_control_client import suggest_hibernation

def main():
    monitor = TokenMonitor()
    result = monitor.run()
    
    # 根据结果触发其他模块
    if result['token_pct'] >= 80:
        suggest_compression()
    
    if result['level'] == 'L1':
        suggest_hibernation()
    
    print(result['report'])

if __name__ == "__main__":
    main()
```

### 4.3 状态持久化

```json
{
  "version": "2.1",
  "last_check": "2026-03-26T06:00:00Z",
  "current_level": "L5",
  "token_pct": 75,
  "adjustments": [
    {
      "time": "2026-03-26T00:00:00Z",
      "from": "L4",
      "to": "L5",
      "reason": "Token恢复"
    }
  ]
}
```

---

## S5: 自我验证（质量检查+测试）

### 5.1 功能测试

```python
def test_token_optimizer():
    # 测试1: L5正常运行
    result = optimizer.run(token_pct=75)
    assert result['level'] == 'L5'
    assert result['next_check'] == '6h'
    
    # 测试2: L1休眠建议
    result = optimizer.run(token_pct=10)
    assert result['level'] == 'L1'
    assert result['suggestion'] == 'hibernate'
    
    # 测试3: 80%压缩建议
    result = optimizer.run(token_pct=82)
    assert result['suggestion'] == 'compress_context'
    
    # 测试4: 等级变化调整
    optimizer.last_level = 'L5'
    result = optimizer.run(token_pct=45)
    assert result['adjusted'] == True
```

### 5.2 质量检查清单

| 检查项 | 通过标准 |
|--------|----------|
| 等级判断准确 | 各阈值边界正确 |
| 频率调整生效 | Cron更新成功 |
| 建议触发正确 | 80%建议压缩，15%建议休眠 |
| 状态记录完整 | 历史调整可追溯 |
| Token节省达标 | 较V2.0节省>80% |

---

## S6: 认知谦逊（局限标注）

### 6.1 已知局限

| 局限 | 说明 | 缓解措施 |
|------|------|----------|
| **响应延迟增加** | 从10分钟到6小时，可能错过快速变化 | 关键操作触发即时检查 |
| **等级边界抖动** | Token在边界波动时频繁调整 | 增加滞后区间(±5%) |
| **无法精确预测** | 无法预知用户接下来的操作量 | 基于历史平均估算 |

### 6.2 不确定性声明

- Token计算可能因模型/平台差异而有偏差
- 频率调整需要Cron权限，可能失败
- 极端情况下（Token瞬间耗尽）无法及时响应

---

## S7: 对抗测试（失效场景验证）

### 7.1 异常输入测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| Token=0 | 完全耗尽 | 提示已进入休眠 |
| Token=100 | 刚重置 | 标准L5配置 |
| Token=边界值 | 正好70%,50%,30%,15% | 正确归属等级 |
| 负数/超100 | 非法值 | 报错，使用默认值 |

### 7.2 系统异常测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| Cron更新失败 | 权限不足 | 记录错误，下次重试 |
| 状态文件损坏 | JSON解析失败 | 重置为默认状态 |
| 时间跳跃 | 系统时间异常 | 基于当前时间重新计算 |

### 7.3 边界条件测试

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 连续降级 | L5→L4→L3→L2→L1 | 每级正确调整 |
| 连续升级 | L1→L2→L3→L4→L5 | 每级正确调整 |
| 快速波动 | 在边界反复跳动 | 滞后机制生效，减少调整 |

---

## 使用指南

### 部署方式

替换原有的token-monitor和hibernation-check：

```bash
# 1. 删除旧任务
openclaw cron delete <old-token-monitor-id>
openclaw cron delete <old-hibernation-check-id>

# 2. 创建优化版任务
openclaw cron create \
  --name token-optimizer \
  --cron "0 */6 * * *" \
  --session isolated \
  --message "Run token optimization and hibernation check" \
  --description "Token优化与休眠控制集成 V2.1"
```

### 监控命令

```bash
# 查看当前状态
python3 /root/.openclaw/workspace/scripts/token_optimizer.py status

# 手动触发
python3 /root/.openclaw/workspace/scripts/token_optimizer.py run
```

---

## 关联文档

- `/scripts/token_monitor_v21.py` - 监控核心
- `/scripts/token_optimizer.py` - 优化器主程序
- `skills/context-optimizer/SKILL.md` - 上下文优化
- `skills/hibernation-protocol/SKILL.md` - 休眠协议

---

*Token Optimizer V2.1 - 7标准完整版，90% Token节省*
