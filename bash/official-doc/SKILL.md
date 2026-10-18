---
name: official-doc
description: 公文生成器 skill. Official Doc skill from the marketing-official-document-writing-team
  expert package.
---

# 公文生成器

支持公文生成、格式检查、语气规范检查、模板库。

## Usage

```bash
scripts/official.sh notice "标题" "内容"              # 通知
scripts/official.sh request "事由" "请示"              # 请示
scripts/official.sh report "主题" "内容"               # 报告
scripts/official.sh reply "原请示" "批复"              # 批复
scripts/official.sh format-check "文本"                # 格式检查
scripts/official.sh tone "文本"                        # 语气/用语检查
scripts/official.sh template "类型"                    # 模板库
scripts/official.sh help                               # 帮助
```

## Examples

```bash
# 生成通知
bash scripts/official.sh notice "关于开展安全检查的通知" "安全生产大检查"

# 格式检查
bash scripts/official.sh format-check "关于购置办公设备的请示，我觉得需要买10台电脑"

# 语气检查（检测口语化表达）
bash scripts/official.sh tone "我觉得这个方案差不多可以搞一下"

# 查看所有模板
bash scripts/official.sh template "all"

# 查看特定模板
bash scripts/official.sh template "请示"
```

## Template Types

通知 | 报告 | 请示 | 批复 | 会议纪要 | 工作总结

## Requirements

- Python 3.6+
- No external dependencies
---
💬 Feedback & Feature Requests: https://bytesagain.com/feedback
Powered by BytesAgain | bytesagain.com
