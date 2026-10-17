---
name: task-patrol-skill
description: 巡查 Skill — 通过 CLI 工具巡查任务状态、标记异常、发送告警
---

# Task Patrol Skill

你可以使用 `task-cli.py` 工具来巡查任务状态。该工具位于本 Skill 目录下。

## 认证信息

- API_KEY: `<注册后填入>`

## 工作流程

1. 获取规则 → 2. 检查积分 → 3. 扫描异常任务 → 4. 标记 blocked → 5. 发送告警 → 6. 记录日志

## 可用命令

> 所有命令前缀：`python task-cli.py --key <API_KEY>`

### 规则

```bash
rules                                     # 获取合并后的规则提示词（执行前必须调用）
```

### 任务巡查

```bash
task list                                 # 查看所有任务
st list --status in_progress              # 查看执行中的子任务（检查是否超时/卡住）
st list --status assigned                 # 查看已分配但未开始的（检查是否长期未启动）
st list --status blocked                  # 查看已标记异常的
st get <sub_task_id>                      # 查看子任务详情
```

> 📄 列表命令默认返回全部数据。如数据较多，可加 `--page N --page-size M` 分页查看。返回结果包含 `total`（总数）和 `has_more`（是否还有更多）。

### 异常标记

```bash
st block <sub_task_id>                    # 标记子任务异常（in_progress/assigned/rework → blocked）
```

### 积分

```bash
score me                                  # 查看自己的积分
score logs                                # 查看积分明细
```

> 📄 `score logs` 默认返回全部明细。如数据较多，可加 `--page N --page-size M` 分页查看。

### 通知

```bash
notification                              # 查看通知渠道配置
notify "消息内容"                          # 发送 Telegram 通知
```

### 日志

```bash
log create "patrol" "巡查发现xxx子任务超时，已标记blocked" --sub-task-id <id>
log mine                                  # 回顾工作记录（默认最近7天，最多20条）
log mine --action reflection              # 只看自省笔记
log list --sub-task-id <id>               # 查看某子任务的所有日志
log list --action blocked --days 3        # 扫描执行者求助日志
log list --days 30 --limit 50             # 最近30天，最多50条
```

## 注意事项

- 每次执行前先运行 `rules` 获取最新规则
- 每次唤醒时检查 `score logs`，分析自己的表现
- 重点巡查：超时未完成、长期未启动、会话断开的子任务
- 标记 blocked 后发送告警：`notify "⚠️ 子任务xxx已超时标记 blocked"`
- 不要直接修改子任务的内容或状态（除 block 外），交给规划师处理
