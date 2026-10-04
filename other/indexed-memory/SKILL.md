---
name: indexed-memory
description: 索引化记忆检索系统，支持按主题、日期、效用分类检索知识，避免重复学习，提高检索效率。
model: haiku
tools:
  - Read
  - Write
  - Glob
  - Grep
color: "#3498DB"
---

# Indexed Memory - 索引化记忆检索

基于 Memex(RL) 论文的索引化记忆系统，支持高效检索和复用历史知识。

## 核心理念

> 人类记忆系统支持高效检索，AI 也应该如此。

索引化记忆解决以下问题：
- 知识库越来越大，难以快速定位
- 重复学习相同内容
- 重要知识被淹没在海量信息中

---

## 索引结构

```
knowledge/
├── index.md              # 主索引
├── arxiv/               # arXiv 论文学习
│   └── index.json       # 论文索引（arXiv ID → 文件路径）
├── skills/              # 技能库
│   └── index.json       # 技能索引（技能名 → 文件路径）
└── daily/               # 日常记录
    └── index.json       # 日期索引
```

---

## 索引文件格式

### 论文索引 (arxiv/index.json)

```json
{
  "2602.14697": {
    "title": "E-SPL",
    "file": "self-evolution-2026-03-06.md",
    "keywords": ["self-evolution", "system-prompt", "RL"],
    "utility": 0.9,
    "lastAccessed": "2026-03-07"
  },
  "2505.22954": {
    "title": "Darwin Gödel Machine",
    "file": "self-evolution-2026-03-06.md",
    "keywords": ["self-evolution", "open-ended"],
    "utility": 0.85,
    "lastAccessed": "2026-03-07"
  }
}
```

### 技能索引 (skills/index.json)

```json
{
  "ice-review": {
    "file": "learned-skills.md",
    "source": "arXiv:2401.13996",
    "utility": 0.9,
    "usageCount": 5,
    "lastUsed": "2026-03-06"
  },
  "memory-retrieval": {
    "file": "learned-skills.md",
    "source": "arXiv:2601.03192",
    "utility": 0.85,
    "usageCount": 3,
    "lastUsed": "2026-03-05"
  }
}
```

---

## 检索流程

### 1. 论文检索

```bash
# 检查是否已学习某论文
grep "arXiv:XXXX.XXXXX" knowledge/arxiv/index.json

# 按关键词检索
grep -i "self-evolution" knowledge/arxiv/index.json
```

### 2. 技能检索

```bash
# 查找技能
grep "skill-name" knowledge/skills/index.json

# 按效用排序
jq 'to_entries | sort_by(.value.utility) | reverse' knowledge/skills/index.json
```

### 3. 日期检索

```bash
# 查找特定日期的学习内容
ls knowledge/arxiv/self-evolution-2026-03-*.md
```

---

## 效用评分机制

### 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 使用频率 | 30% | 被引用/使用的次数 |
| 成功率 | 40% | 应用成功的比例 |
| 时效性 | 30% | 最近使用时间 |

### 评分公式

```
utility = (usageScore * 0.3) + (successScore * 0.4) + (recencyScore * 0.3)
```

### 更新时机

1. **使用时** - 增加 usageCount
2. **成功应用时** - 更新 successRate
3. **定期审查** - 每周重新评估

---

## 去重机制

### 论文去重

```bash
# 学习新论文前检查
arxiv_id="2602.14697"
if grep -q "$arxiv_id" knowledge/arxiv/index.json; then
    echo "已学习过此论文"
    exit 0
fi
```

### 技能去重

```bash
# 创建新技能前检查
skill_name="new-skill"
if grep -q "\"$skill_name\"" knowledge/skills/index.json; then
    echo "技能已存在，考虑更新而非创建"
    exit 0
fi
```

---

## 维护操作

### 更新索引

```bash
# 添加新论文到索引
jq '. + {"new_arxiv_id": {"title": "...", "file": "..."}}' knowledge/arxiv/index.json > tmp.json && mv tmp.json knowledge/arxiv/index.json

# 更新效用评分
jq '.skill_name.utility = 0.95' knowledge/skills/index.json > tmp.json && mv tmp.json knowledge/skills/index.json
```

### 清理低效用内容

```bash
# 列出效用低于 0.5 的条目
jq 'to_entries | map(select(.value.utility < 0.5))' knowledge/skills/index.json
```

---

## 最佳实践

1. **学习前检索** - 避免重复学习
2. **定期更新效用** - 保持评分准确
3. **清理过时内容** - 保持知识库精简
4. **关联相关知识** - 建立知识图谱

---

## 输出格式

当用户需要检索知识时：

```markdown
## 检索结果

### 相关论文
| arXiv ID | 标题 | 效用 | 文件 |
|----------|------|------|------|
| 2602.14697 | E-SPL | 0.9 | self-evolution-2026-03-06.md |

### 相关技能
| 技能名 | 来源 | 效用 | 使用次数 |
|--------|------|------|---------|
| ice-review | arXiv:2401.13996 | 0.9 | 5 |

### 建议操作
- [ ] 应用 ice-review 技能
- [ ] 参考 E-SPL 论文优化系统提示
```
## Activation Keywords

- `indexed-memory`
- `indexed-memory`
- `indexed memory`

## Tools Used

- `exec`
- `read`
- `write`
- `edit`

## Instructions for Agents

1. Read the task description carefully
2. Follow the step-by-step process
3. Use the appropriate tools
4. Verify the results

## Examples

### Example 1: Basic Usage

**User:** <example user request>

**Agent:** <example agent response>

### Example 2: Advanced Usage

**User:** <example user request>

**Agent:** <example agent response>
