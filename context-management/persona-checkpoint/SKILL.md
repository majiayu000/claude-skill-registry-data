---
name: persona-checkpoint
description: |
  AI 人格操作系统的上下文保护和检查点系统（Never-Forget 协议）。监控上下文窗口使用量并在关键阈值自动保存进度，防止上下文丢失。实现 95% 的中断恢复能力。触发关键词：checkpoint、save context、preserve、resume、context protection、never-forget、recovery、context loss、emergency checkpoint、survival mode、flush context、session recovery、decision tracking、action items、resume point、proactive save、forced checkpoint、natural break、risky operation、context threshold、vigilant mode、active checkpoint、emergency flush、critical save、context percentage、checkpoint frequency、workspace memory、permanent facts、recovery protocol、session continuity、progress preservation、检查点、保存进度、保存上下文。
allowed-tools:
  - Bash
  - Read
  - Write
---

# 人格检查点 — Never-Forget 协议

本技能实现 AI 人格操作系统的上下文保护和检查点功能，防止上下文丢失，实现 95% 的会话恢复准确率。

## 阶段 1：评估上下文窗口使用量

**步骤 1.1：** 检查当前上下文窗口使用百分比

根据对话长度、工具调用和复杂性计算或估算当前上下文窗口利用率。

**步骤 1.2：** 确定严重程度阈值

| 使用量 | 状态 | 所需操作 |
|--------|------|----------|
| < 50% | 🟢 正常 | 随时记录决策（轻量级） |
| 50-69% | 🟡 警觉 | 增加检查点频率（每约 5 次交互） |
| 70-84% | 🟠 活跃 | 停止 — 立即写入完整检查点 |
| 85-94% | 🔴 紧急 | 紧急转储 — 仅保留必需信息（任务 + 恢复点） |
| 95%+ | ⚫ 严重 | 生存模式 — 仅保留恢复所需的最低限度信息 |

**步骤 1.3：** 应用用户可见性规则

- **< 70%**：静默操作，不通知用户
- **70-84%**：通知用户："上下文已达到 XX% — 正在写入检查点"
- **85-94%**：警告用户："⚠️ 上下文 XX% 处需要紧急检查点"
- **95%+**：严重警告："🚨 上下文已达到临界限制 — 生存模式检查点"

## 阶段 2：确定检查点操作

**步骤 2.1：** 根据阈值选择检查点类型

```pseudocode
if context < 50%:
    checkpoint_type = "lightweight"  # 仅内联决策
elif 50% <= context < 70%:
    checkpoint_type = "vigilant"     # 每约 5 次交互，轻量格式
elif 70% <= context < 85%:
    checkpoint_type = "full"         # 包含推理的完整检查点
elif 85% <= context < 95%:
    checkpoint_type = "emergency"    # 仅任务 + 恢复点
else:  # 95%+
    checkpoint_type = "survival"     # 绝对最低限度
```

**步骤 2.2：** 检查强制触发条件

如果出现以下情况，覆盖基于阈值的逻辑：
- 用户明确说"checkpoint"/"检查点"（强制完整检查点）
- 重大决策之前（架构变更、破坏性操作）
- 自然会话暂停时（任务完成、上下文切换）
- 有风险的操作之前（数据删除、重构、迁移）
- 正常操作中每约 10 次交互（主动）

## 阶段 3：写入检查点

**步骤 3.1：** 创建检查点文件路径

使用 Bash 创建目录并确定文件路径：

```bash
mkdir -p ~/workspace/memory
echo "~/workspace/memory/$(date +%Y-%m-%d).md"
```

**步骤 3.2：** 根据类型格式化检查点内容

**轻量级（< 50%）：**
```markdown
## 检查点 [HH:MM] — 上下文：XX%

**决策：** [做出了什么决策]
```

**警觉型（50-69%）：**
```markdown
## 检查点 [HH:MM] — 上下文：XX%

**当前任务：** [当前工作]
**继续从：** [下一步]
```

**完整检查点（70-84%）：**
```markdown
## 检查点 [HH:MM] — 上下文：XX%

**当前任务：** [我们正在做什么]

**关键决策：**
- [决策 1 及推理]
- [决策 2 及推理]

**待办事项：**
- [ ] [任务 1]（负责人：[用户/助手]）
- [ ] [任务 2]（负责人：[用户/助手]）

**当前状态：** [进展摘要]

**继续从：** [精确的下一步及上下文]
```

**紧急型（85-94%）：**
```markdown
## ⚠️ 紧急检查点 [HH:MM] — 上下文：XX%

**任务：** [一句话描述]
**继续：** [精确的下一步操作]
```

**生存型（95%+）：**
```markdown
## 🚨 生存检查点 [HH:MM] — 上下文：XX%

**继续：** [最低可行下一步]
```

**步骤 3.3：** 将检查点写入文件

使用 Bash 将检查点追加到当天的文件：

```bash
cat >> ~/workspace/memory/$(date +%Y-%m-%d).md << 'EOF'
[来自步骤 3.2 的格式化检查点内容]
EOF
```

**步骤 3.4：** 确认写入成功

验证检查点已写入：

```bash
tail -n 5 ~/workspace/memory/$(date +%Y-%m-%d).md
```

## 阶段 4：恢复协议

**步骤 4.1：** 读取最新检查点

使用 Bash 定位并读取当天的检查点文件：

```bash
cat ~/workspace/memory/$(date +%Y-%m-%d).md
```

**步骤 4.2：** 读取永久事实

使用 Read 工具加载持久上下文：

```bash
cat ~/workspace/MEMORY.md
```

**步骤 4.3：** 解析恢复指令

从检查点文件中提取最近的"继续从"指令。

**步骤 4.4：** 通知用户并恢复

通知用户：
```
正在从 [时间] 的检查点恢复。上下文恢复率：95%
上次检查点：[XX]% 上下文窗口
继续执行：[恢复指令]
```

**步骤 4.5：** 从精确的恢复点继续

按照恢复指令中指定的下一步执行，结合来自永久事实 + 检查点的完整上下文。

## 检查点触发摘要

| 触发条件 | 频率 | 类型 |
|----------|------|------|
| 主动触发 | 每约 10 次交互 | 轻量级或警觉型（取决于上下文 %） |
| 阈值：70%+ | 立即 | 完整检查点（强制） |
| 阈值：85%+ | 立即 | 紧急检查点（强制） |
| 阈值：95%+ | 立即 | 生存检查点（强制） |
| 重大决策 | 执行前 | 完整检查点 |
| 自然暂停 | 任务/阶段结束时 | 警觉型或完整型 |
| 有风险的操作 | 执行前 | 完整检查点 |
| 用户指令 | 遇到"checkpoint"关键词时 | 完整检查点（强制） |

## 状态管理

```pseudocode
computed.last_checkpoint_time = [HH:MM]
computed.last_checkpoint_context = [percentage]
computed.checkpoints_today = [count]
computed.recovery_mode = [true/false]
```

## 预期结果

- **上下文丢失预防：** 自上次检查点以来最多 5% 丢失
- **恢复准确率：** 中断后 95% 上下文恢复
- **用户透明度：** 70%+ 阈值时通知
- **会话连续性：** 从精确点无缝恢复
- **决策保留：** 所有关键决策连同推理一起捕获
- **行动跟踪：** 所有待处理任务连同负责人一起保留
