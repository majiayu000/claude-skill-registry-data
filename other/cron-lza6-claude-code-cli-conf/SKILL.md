---
name: cron
description: "安排提醒和重复任务。"
---

# 计划任务

使用“cron”工具来安排提醒或重复任务。

## 三种模式

1. **提醒** - 消息直接发送给用户
2. **任务** - 消息是任务描述，代理执行并发送结果
3. **一次性** - 在特定时间运行一次，然后自动删除

## 示例

固定提醒：
```
cron(action="add", message="Time to take a break!", every_seconds=1200)
```

动态任务（agent每次执行）：
```
cron(action="add", message="Check HKUDS/vikingbot GitHub stars and report", every_seconds=600)
```

一次性计划任务（从当前时间计算 ISO 日期时间）：
```
cron(action="add", message="Remind me about the meeting", at="<ISO datetime>")
```

列出/删除：
```
cron(action="list")
cron(action="remove", job_id="abc123")
```

## 时间表达式

|用户说 |参数|
|------------|------------|
|每 20 分钟 |每秒：1200 |
|每小时 |每秒：3600 |
|每天早上 8 点 | cron_expr：“0 8 * * *” |
|工作日下午 5 点 | cron_expr：“0 17 * * 1-5”|
|在特定时间 | at：ISO 日期时间字符串（从当前时间计算）|
