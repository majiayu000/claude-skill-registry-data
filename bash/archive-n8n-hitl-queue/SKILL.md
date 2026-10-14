---
name: n8n-hitl-queue
version: 1.0.0
description: |
  n8n人工审查队列机制 - 管理工作流失败项的人工审查流程
  核心价值：自动队列管理、审查通知、审批工作流
  适用：工作流异常处理、人工审批、质量控制
author: OpenClaw
tags:
  - n8n
  - hitl
  - queue
  - review
requires:
  - model: "kimi-coding/k2p5"
  - local_tools: ["python3"]
  - cron: true
---

# n8n HITL审查队列 Skill V1.0.0

## 标准1-5: 5标准满足

1. **全局**: 全失败类型覆盖
2. **系统**: 入队 → 通知 → 审查 → 处理闭环
3. **迭代**: PDCA优化审查流程
4. **Skill化**: 标准结构 + CLI接口
5. **自动化**: 自动队列管理 + 定时提醒

## 定时任务

```bash
# 每小时处理队列
0 * * * * ./scripts/process_queue.py

# 每日队列报告
0 18 * * * ./scripts/daily_report.py
```

---

*5标准全部满足*
