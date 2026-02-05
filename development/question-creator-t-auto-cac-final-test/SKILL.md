---
name: question-creator
description: 创建符合 CAC 评测系统规范的标准化测试题目。当用户需要添加新题目、创建测试题、或提到"创建题目"、"新建题目"、"添加题目"、"add question"、"create question"时使用此 Skill。支持代码、数理、逻辑、综合四类题库。
---

# Question Creator - 题目创建助手

创建符合 CAC 评测系统规范的标准化测试题目。

## 快速开始

### 必需信息

创建题目前，请提供：
1. **题目内容** - 完整的题目描述
2. **标准答案** - 正确答案和解题过程
3. **难度级别** - base / advanced / final / final+
4. **题库类别** - 代码 / 数理 / 逻辑 / 综合

### 创建流程

1. 确定编号 → 查看目标目录，找下一个可用编号
2. 创建目录 → `NNN-problem-name` 格式
3. 创建文件 → meta.yaml, prompt.md, reference.md, README.md
4. 验证格式 → `python scripts/validate_questions.py`

## 目录结构

```
{题库名}/{difficulty}-test/NNN-problem-name/
├── README.md       # 人类阅读的完整文档
├── meta.yaml       # 机器读取的元数据
├── prompt.md       # 发给被测模型的 prompt
├── reference.md    # 标准答案/评判依据
└── test-results/   # 测试结果目录
```

## 文件格式

详细格式规范见 [question_format_guide.md](references/question_format_guide.md)。
编号规则见 [numbering_rules.md](references/numbering_rules.md)。
文件模板见 [templates/](templates/) 目录。

### meta.yaml 模板

```yaml
id: {category}-{difficulty}-{number}
brief: 题目简短描述
category: math | code | logic | comprehensive
difficulty: base | advanced | final | final+
scoring_std:
  max_score: 10
  indicators:
    - accuracy      # 准确性
    - completeness  # 完整性
```

### 评分指标速查

| 类型 | 可用指标 |
|------|----------|
| 代码题 | `ans_correct`, `code_quality`, `efficiency`, `robustness` |
| 理论题 | `completeness`, `accuracy`, `clarity`, `depth` |
| 设计题 | `ans_correct`, `example_quality`, `completeness`, `practicality` |

### prompt.md

纯净的题目文本，直接发给被测模型，不含元数据。

### reference.md

标准答案和评判依据，供评判模型参考。

## 题库路径

| 类别 | 路径 | category |
|------|------|----------|
| 代码 | `代码能力基准测试题库/` | code |
| 数理 | `数理能力基准测试题库/` | math |
| 逻辑 | `自然语言与逻辑能力基准测试题库/` | logic |
| 综合 | `综合能力测评/` | comprehensive |

## 示例

参考现有题目：
- 数理：`数理能力基准测试题库/base-test/001-chicken-rabbit-cage/`
- 代码：`代码能力基准测试题库/base-test/001-simple-calculator/`
- 逻辑：`自然语言与逻辑能力基准测试题库/base-test/001-age-multiple-reasoning/`

## 注意事项

1. 编号必须三位数字，连续递增
2. 目录名用小写英文和连字符
3. 所有必需文件不能为空
4. meta.yaml 必须符合 YAML 语法
