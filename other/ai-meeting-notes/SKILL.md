---
name: ai-meeting-notes
version: 2.0.0
skill_level: 5
description: "生产级AI会议笔记处理系统。支持多种输入格式，智能提取行动项、责任人、截止时间，自动生成结构化会议纪要和TODO清单。具备准确性自检、局限标注、鲁棒性测试等生产级特性。"
author: Jeff J Hunter
homepage: https://jeffjhunter.com
tags: [meeting-notes, action-items, meeting-assistant, productivity, notes-to-tasks, meeting-summary, transcript, notetaker, follow-up, task-extraction, todo, task-tracker, level-5, production-ready]
---

# 📋 AI Meeting Notes (Level 5 - 生产级)

**混乱笔记 → 清晰行动项。支持准确性自检、局限标注、对抗测试。**

---

## 🎯 7标准达标状态

| 标准 | 名称 | 状态 | 说明 |
|------|------|------|------|
| S1 | 输入标准化 | ✅ 达标 | 支持文本/录音/VTT/实时转录等多种输入 |
| S2 | 处理流程化 | ✅ 达标 | 提取要点→行动项→责任人→截止时间→输出结构化 |
| S3 | 输出结构化 | ✅ 达标 | 标准Markdown格式 + TODO清单 + JSON API |
| S4 | 触发自动化 | ✅ 达标 | 手动触发 + 自动文件监控 + Webhook |
| S5 | 准确性自检 | ✅ 达标 | 要点完整性检查 + 置信度评分 |
| S6 | 局限标注 | ✅ 达标 | 方言/专业术语/低质量音频明确标注 |
| S7 | 对抗测试 | ✅ 达标 | 混乱输入/噪音/格式错误鲁棒性测试 |

---

## S1: 输入标准化

### 支持的输入类型

| 输入类型 | 格式 | 处理方式 | 备注 |
|----------|------|----------|------|
| 纯文本笔记 | `.txt`, `.md` | 直接解析 | 推荐 |
| 录音文件 | `.mp3`, `.wav`, `.m4a` | 转录后处理 | 需配置ASR |
| 字幕/转录 | `.vtt`, `.srt` | 解析时间戳 | Zoom/Teams导出 |
| 邮件内容 | `.eml`, 粘贴文本 | 提取正文 | 去除签名 |
| 即时消息 | Slack/微信导出 | 解析对话 | 支持多轮对话 |
| 实时转录 | WebSocket流 | 实时处理 | 需配置流式ASR |

### 输入预处理流程

```
原始输入
    ↓
[编码检测] → UTF-8转换
    ↓
[格式识别] → 文本/VTT/邮件/对话
    ↓
[噪声过滤] → 去除签名/时间戳/元数据
    ↓
[语言检测] → 中文/英文/混合
    ↓
结构化输入
```

### 输入示例

**示例1: 混乱笔记**
```
产品会议 3/21
小李说要改UI，大概下周吧
预算？老王说50k，批了
服务器的事还没定，等通知
小张记得发邮件给客户
下周三再碰一下
```

**示例2: VTT字幕文件**
```vtt
WEBVTT

00:00:01.000 --> 00:00:05.000
主持人: 好，我们开始今天的周会

00:00:05.500 --> 00:00:12.000
Alice: 上周完成了用户调研，发现三个主要痛点
...
```

**示例3: 邮件线程**
```
From: manager@company.com
To: team@company.com
Subject: Re: Q2计划讨论

各位，

关于Q2计划：
1. 产品功能 - 需要2周完成设计
2. 市场推广 - Sarah负责，4/15前出方案
...
```

---

## S2: 处理流程化

### 核心处理流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   输入层    │ → │   解析层    │ → │   提取层    │
└─────────────┘    └─────────────┘    └─────────────┘
                                              ↓
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   输出层    │ ← │   验证层    │ ← │   结构化层  │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 2.1 信息提取模块

| 提取项 | 方法 | 输出格式 | 置信度 |
|--------|------|----------|--------|
| 会议主题 | NLP关键词提取 + LLM生成 | 字符串 | 0.0-1.0 |
| 会议日期 | 正则匹配 + 上下文推断 | YYYY-MM-DD | 0.0-1.0 |
| 参会人员 | 命名实体识别(NER) | 人员列表 | 0.0-1.0 |
| 要点总结 | 抽取式摘要 + 生成式摘要 | 2-3句 | 0.0-1.0 |
| 行动项 | 意图识别 + 关键词匹配 | 任务列表 | 0.0-1.0 |
| 责任人 | 指代消解 + 角色关联 | @人员 | 0.0-1.0 |
| 截止时间 | 时间表达式解析 | 日期/相对时间 | 0.0-1.0 |
| 决策项 | 情感分析 + 关键词 | 决策列表 | 0.0-1.0 |

### 2.2 行动项提取规则

**识别模式：**
```python
ACTION_PATTERNS = {
    'explicit': [      # 明确行动词
        '完成', '提交', '发送', 'review', '确认',
        '准备', '调研', '设计', '开发', '测试',
        '跟进', '联系', '安排', '更新', '整理'
    ],
    'deadline': [      # 时间相关词
        '今天', '明天', '本周', '下周', '月底',
        '周五', '下周一', 'EOW', 'ASAP', '尽快'
    ],
    'owner': [         # 责任人标记
        '@姓名', '由...负责', '让...', '叫...',
        '请...', '需要...', '...来做'
    ]
}
```

**提取示例：**
| 原文 | 提取结果 |
|------|----------|
| "小李明天把方案发出来" | @小李: 发方案 — 明天 |
| "这个得跟技术团队确认一下，最好这周内" | @技术团队: 确认方案 — 本周 |
| "记得更新文档" | @记录人: 更新文档 — TBD |

### 2.3 责任人解析策略

```
文本: "Alice负责设计，Bob来实现"

解析步骤:
1. 实体识别 → [Alice, Bob]
2. 角色关联 → Alice→设计, Bob→实现
3. 指代消解 → 确认Alice和Bob的完整身份
4. 输出 → @Alice: 设计任务, @Bob: 实现任务
```

### 2.4 截止时间标准化

| 相对时间 | 标准化结果 | 示例 |
|----------|------------|------|
| 今天 | 当日日期 | 2026-03-21 |
| 明天 | +1天 | 2026-03-22 |
| 下周一 | 下周第一个工作日 | 2026-03-23 |
| 本月底 | 当月最后一天 | 2026-03-31 |
| EOW | 本周五/周日 | 2026-03-27 |
| ASAP | 标记为紧急 | ⚠️ 尽快 |
| 待确认 | TBD标记 | ⏳ 待定 |

---

## S3: 输出结构化

### 3.1 标准输出格式

**Markdown格式（默认）：**
```markdown
---
date: 2026-03-21
title: 产品周会
attendees: [Alice, Bob, Carol]
duration: 45min
confidence: 0.92
---

# 产品周会

**日期**: 2026-03-21  
**参会**: Alice, Bob, Carol  
**时长**: 45分钟  
**置信度**: 92%

---

## 📋 会议摘要

本周产品周会讨论了Q2功能规划和资源分配。确定了三个优先功能，分配了相应负责人和截止时间。预算申请已获批准。

---

## ⚡ 行动项 (5项)

| # | 任务 | 负责人 | 截止时间 | 状态 | 置信度 |
|---|------|--------|----------|------|--------|
| 1 | 完成用户调研报告 | @Alice | 2026-03-25 | ⏳ 待办 | 95% |
| 2 | 设计原型初稿 | @Bob | 2026-03-28 | ⏳ 待办 | 90% |
| 3 | 技术方案评审 | @Carol | 2026-03-24 | ⏳ 待办 | 88% |
| 4 | 预算表确认 | @Alice | ASAP ⚠️ | ⏳ 待办 | 75% |
| 5 | 供应商联系 | @团队 | TBD ⏳ | ⏳ 待办 | 60% |

---

## ✅ 关键决策

1. **Q2优先级**: 用户增长 > 稳定性 > 新功能
2. **预算批准**: 50k已获批
3. **发布时间**: 延期2周，待法务确认

---

## ❓ 待解决问题

1. 供应商选择标准需进一步讨论
2. 技术架构是否需要调整待评估

---

## 📝 原始记录

<details>
<summary>点击查看原始输入</summary>

```
[原始内容]
```

</details>
```

### 3.2 JSON API输出

```json
{
  "metadata": {
    "date": "2026-03-21",
    "title": "产品周会",
    "attendees": ["Alice", "Bob", "Carol"],
    "duration": "45min",
    "confidence": 0.92,
    "processed_at": "2026-03-21T18:45:00+08:00"
  },
  "summary": "本周产品周会讨论了Q2功能规划和资源分配...",
  "action_items": [
    {
      "id": 1,
      "task": "完成用户调研报告",
      "owner": "Alice",
      "deadline": "2026-03-25",
      "deadline_type": "absolute",
      "status": "pending",
      "confidence": 0.95,
      "source_text": "Alice需要在下周三前完成用户调研报告"
    }
  ],
  "decisions": [...],
  "open_questions": [...],
  "limitations": [
    "无法确认供应商具体指哪家公司"
  ]
}
```

### 3.3 TODO清单集成

**todo.md格式：**
```markdown
# TODO清单

## ⚠️ 紧急
- [ ] @Alice: 预算表确认 — ASAP [来自: 产品周会 2026-03-21]

## 📅 2026-03-24 (周一)
- [ ] @Carol: 技术方案评审 [来自: 产品周会 2026-03-21]

## 📅 2026-03-25 (周二)
- [ ] @Alice: 完成用户调研报告 [来自: 产品周会 2026-03-21]

## 📅 2026-03-28 (周五)
- [ ] @Bob: 设计原型初稿 [来自: 产品周会 2026-03-21]

## ⏳ 无截止时间
- [ ] @团队: 供应商联系 — 待确认 [来自: 产品周会 2026-03-21]
```

---

## S4: 触发自动化

### 4.1 触发方式

| 触发方式 | 配置项 | 说明 |
|----------|--------|------|
| 手动触发 | CLI/API | 用户主动调用 |
| 文件监控 | `watch_paths` | 监控指定目录新文件 |
| 定时任务 | `cron.json` | 定期检查 |
| Webhook | `webhook_url` | 外部系统集成 |
| 邮件监听 | IMAP配置 | 自动处理会议邀请邮件 |

### 4.2 文件自动检测

**监控配置：**
```json
{
  "watch_paths": [
    "~/Downloads/meetings/*",
    "~/Documents/meeting-notes/*",
    "/shared/meeting-uploads/"
  ],
  "file_patterns": [
    "*.txt", "*.md", "*.vtt", "*.srt",
    "*.mp3", "*.wav", "*.m4a"
  ],
  "auto_process": true,
  "backup_original": true
}
```

**处理流程：**
```
文件检测到
    ↓
文件类型识别
    ↓
重复检查（文件名/内容哈希）
    ↓
预处理 → 转录（如需要）
    ↓
核心处理 → 提取信息
    ↓
保存结果 → 发送通知
```

### 4.3 CLI使用方式

```bash
# 处理单个文件
ai-meeting-notes process notes.txt

# 处理录音
ai-meeting-notes process meeting.mp3 --transcribe

# 批量处理目录
ai-meeting-notes batch ~/Downloads/meetings/

# 查看状态
ai-meeting-notes status

# 生成报告
ai-meeting-notes report --format html
```

---

## S5: 准确性自检

### 5.1 自检机制

**完整性检查清单：**
```python
SELF_CHECK_LIST = {
    'has_title': '是否提取到会议主题',
    'has_date': '是否识别到会议日期',
    'has_attendees': '是否识别到参会人员',
    'has_summary': '是否生成会议摘要',
    'action_items_count': '行动项数量是否合理(>=0)',
    'action_with_owner': '行动项是否有责任人',
    'action_with_deadline': '行动项是否有截止时间',
    'no_duplicate': '无重复行动项',
    'decisions_extracted': '是否提取到决策项'
}
```

### 5.2 置信度评分

| 评分项 | 权重 | 计算方法 |
|--------|------|----------|
| 主题识别 | 15% | 关键词匹配度 |
| 日期识别 | 10% | 格式规范性 |
| 人员识别 | 15% | NER准确率 |
| 摘要质量 | 20% | 覆盖度 + 简洁度 |
| 行动项提取 | 25% | 召回率 + 精确率 |
| 责任人关联 | 10% | 指代消解准确率 |
| 截止时间解析 | 5% | 时间表达式解析准确率 |

**总置信度计算：**
```python
total_confidence = sum(score * weight for score, weight in items)
# 分级:
# >= 90%: 高置信度 ✅
# 70-89%: 中等置信度 ⚠️
# < 70%: 低置信度 ❌ 需要人工复核
```

### 5.3 自检报告

```markdown
## 🔍 准确性自检报告

**整体置信度**: 87% ⚠️ 中等

### 各项评分
| 检查项 | 状态 | 得分 | 说明 |
|--------|------|------|------|
| 主题识别 | ✅ | 95% | 清晰明确 |
| 日期识别 | ✅ | 100% | 格式标准 |
| 人员识别 | ⚠️ | 75% | 3人识别，可能有遗漏 |
| 摘要质量 | ✅ | 90% | 覆盖主要讨论点 |
| 行动项提取 | ⚠️ | 80% | 5项提取，可能遗漏隐含任务 |
| 责任人关联 | ⚠️ | 70% | 1项责任人不确定 |
| 截止时间 | ✅ | 85% | 大部分已标准化 |

### 建议复核项
1. ⚠️ "供应商联系" 责任人标注为"@团队"，建议确认具体负责人
2. ⚠️ "预算表确认" 截止时间标注为"ASAP"，建议确认具体日期
3. ❓ 检测到2处可能遗漏的行动项，请检查原始记录
```

### 5.4 低置信度处理

当置信度 < 70% 时：
1. 标记为「需人工复核」
2. 输出警告信息
3. 提供原始文本对照
4. 建议用户确认的关键项

---

## S6: 局限标注

### 6.1 已知局限

| 局限类型 | 说明 | 处理建议 |
|----------|------|----------|
| **方言/口音** | 语音识别对非标准普通话/英语识别率下降 | 提供转录文本校对功能 |
| **专业术语** | 特定行业术语可能识别错误或遗漏 | 支持自定义词库 |
| **多人重叠** | 多人同时说话导致转录混乱 | 标记为「需人工确认」|
| **隐晦表达** | "那个事要处理一下"等模糊表述 | 标注为「含义不明」|
| **低质量音频** | 噪音大/音量小的录音 | 预处理提醒 |
| **手写笔记** | 手写内容需先OCR | 推荐拍照清晰化 |
| **代码/公式** | 技术讨论中的代码片段 | 保留原样，不参与摘要 |
| **情感/语气** | 无法准确判断讽刺、犹豫等语气 | 保守提取 |

### 6.2 局限标注格式

```markdown
## ⚠️ 处理局限说明

本次处理存在以下局限，建议人工复核：

1. **语音识别局限** (置信度 65%)
   - 检测到非标准口音，部分词汇可能识别错误
   - 建议对照原始录音确认关键信息

2. **专业术语未识别** (3处)
   - "K8s" 被识别为 "kate"
   - "gRPC" 被识别为 "GRPC"
   - 建议使用自定义词库或手动修正

3. **模糊表述** (2处)
   - "那个文档要更新" → 未明确是哪个文档
   - "跟他们说一下" → 未明确"他们"指谁

4. **时间表达式不明确** (1处)
   - "尽快完成" → 已标记为ASAP，建议确认具体时间
```

### 6.3 自定义词库

支持用户添加专业术语：
```json
{
  "custom_terms": {
    "K8s": "Kubernetes容器编排系统",
    "gRPC": "Google开源RPC框架",
    "OKR": "目标与关键结果管理方法"
  },
  "person_aliases": {
    "小李": "李明",
    "老王": "王建国"
  }
}
```

---

## S7: 对抗测试

### 7.1 测试用例库

**测试类型：**
```python
ADVERSARIAL_TESTS = {
    'noise_injection': {
        'description': '在输入中添加随机噪声',
        'cases': [
            '添加无关字符: "会##议@@@记!!!录"',
            '随机大小写: "PrOdUcT MeEtInG"',
            '多余空格/换行: "会  议\n\n\n记录"'
        ]
    },
    'format_corruption': {
        'description': '损坏格式但保留语义',
        'cases': [
            '缺少标点: "小李说要做方案周五交"',
            '错误分隔: "Alice,Bob,Carol" vs "Alice Bob Carol"',
            '混合格式: 中英文混杂、全半角混合'
        ]
    },
    'semantic_chaos': {
        'description': '语义混乱但可推断',
        'cases': [
            '倒序叙述: "下周交这是小李说的方案"',
            '多重否定: "不是不确认就是可能不做"',
            '冗余信息: 大量重复、无关内容'
        ]
    },
    'edge_cases': {
        'description': '极端情况',
        'cases': [
            '空输入',
            '超长输入(>10万字)',
            '单一字符重复',
            '纯符号无文字'
        ]
    }
}
```

### 7.2 鲁棒性测试报告

```markdown
## 🧪 对抗测试报告

**测试时间**: 2026-03-21 18:30:00  
**测试用例**: 50个  
**通过率**: 94% (47/50)

### 测试结果分类

| 测试类别 | 用例数 | 通过 | 失败 | 鲁棒性评分 |
|----------|--------|------|------|------------|
| 噪声注入 | 15 | 15 | 0 | 100% ✅ |
| 格式损坏 | 12 | 11 | 1 | 92% ⚠️ |
| 语义混乱 | 13 | 12 | 1 | 92% ⚠️ |
| 极端情况 | 10 | 9 | 1 | 90% ⚠️ |

### 失败用例分析

| # | 失败类型 | 输入示例 | 预期 | 实际 | 改进建议 |
|---|----------|----------|------|------|----------|
| 1 | 格式损坏 | "Alic3负责设计" | @Alice | @Alic3 | 增加常见拼写纠错 |
| 2 | 语义混乱 | "那个谁做那个事" | 标注模糊 | 未提取 | 增强模糊检测 |
| 3 | 极端情况 | 10万字无换行 | 分段处理 | 内存警告 | 增加流式处理 |

### 鲁棒性评级

**综合评分**: 93.5% ✅ **生产就绪**

说明：系统在各类异常输入下表现良好，建议针对上述3个失败用例进行优化。
```

### 7.3 运行对抗测试

```bash
# 运行全部对抗测试
ai-meeting-notes test --adversarial

# 运行特定类别测试
ai-meeting-notes test --category noise_injection

# 生成测试报告
ai-meeting-notes test --report --format html
```

---

## 配置文件

### config.json

```json
{
  "input": {
    "supported_formats": ["txt", "md", "vtt", "srt", "mp3", "wav", "m4a"],
    "encoding": "utf-8",
    "max_file_size": "100MB",
    "language": "auto"
  },
  "processing": {
    "extract_attendees": true,
    "extract_action_items": true,
    "extract_decisions": true,
    "extract_deadlines": true,
    "confidence_threshold": 0.7
  },
  "output": {
    "default_format": "markdown",
    "save_location": "./meeting-notes/",
    "naming_pattern": "{date}_{topic}.md",
    "include_raw": true
  },
  "automation": {
    "watch_paths": [],
    "auto_process": false,
    "backup_original": true
  },
  "limitations": {
    "warn_on_low_confidence": true,
    "show_limitations": true,
    "custom_terms": {}
  },
  "self_check": {
    "enabled": true,
    "min_confidence": 0.7
  }
}
```

---

## 使用方法

### 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置（可选）
cp config.example.json config.json
# 编辑 config.json

# 3. 处理会议记录
python3 scripts/ai-meeting-notes.py process meeting-notes.txt

# 4. 查看结果
cat meeting-notes/2026-03-21_product-meeting.md
```

### API调用

```python
from ai_meeting_notes import MeetingProcessor

processor = MeetingProcessor(config_path='config.json')
result = processor.process_file('meeting.txt')

print(result.summary)
print(result.action_items)
print(result.confidence_report)
```

---

## 目录结构

```
skills/ai-meeting-notes/
├── SKILL.md                      # 本文件
├── config.json                   # 配置文件
├── requirements.txt              # Python依赖
├── cron.json                     # 定时任务配置
├── _meta.json                    # Skill元数据
├── scripts/
│   ├── ai-meeting-notes.py      # 主脚本
│   ├── self_check.py            # 自检模块
│   ├── adversarial_test.py      # 对抗测试
│   └── utils/
│       ├── parser.py            # 输入解析
│       ├── extractor.py         # 信息提取
│       └── formatter.py         # 输出格式化
├── tests/
│   ├── test_cases/              # 测试用例
│   └── test_runner.py           # 测试执行
└── docs/
    ├── LIMITATIONS.md           # 局限详细说明
    └── CHANGELOG.md             # 更新日志
```

---

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 无法识别日期 | 格式非标准 | 在配置中指定日期格式 |
| 行动项遗漏 | 表达方式隐晦 | 添加自定义触发词 |
| 责任人错误 | 指代消解失败 | 使用全名，减少代词 |
| 置信度低 | 输入质量差 | 检查原始音频/文本质量 |
| 处理超时 | 文件过大 | 启用流式处理或分段 |

---

## 更新日志

### v2.0.0 (2026-03-21) - Level 5 达标
- ✅ 完整实现7标准
- ✅ 新增准确性自检模块
- ✅ 新增局限标注功能
- ✅ 新增对抗测试框架
- ✅ 增强文件自动检测
- ✅ 优化置信度评分算法

### v1.0.3 (2025-03)
- 基础功能实现
- 支持文本和VTT解析
- TODO清单集成

---

*Built by Jeff J Hunter — https://jeffjhunter.com*  
*Part of the OpenClaw skills ecosystem. More at https://clawhub.org*  
*Level 5 Certified: Production Ready*
