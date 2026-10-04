---
name: code-semantic-labeler
description: 使用责任链模式实现代码语义标注，将代码中的节点映射到城市业务语义。
---

# 代码语义标注器

## 基本信息
- **名称**: 代码语义标注器
- **描述**: 使用责任链模式实现代码语义标注，将代码中的节点映射到城市业务语义。
- **版本**: 1.1.0
- **标签**: 代码分析, 语义标注, 责任链模式

## 功能
- **责任链模式**：按顺序使用多个标注器，规则库优先，LLM 兜底
- **规则基于标注**：使用精确或模糊前缀匹配进行语义标注
- **LLM 兜底**：当规则未命中时，使用 LLM 进行语义标注
- **代码总结**：当 ontology_rules 中没有标注时，调用大模型对代码进行总结
- **AST 分析**：使用 code-to-ast-new 进行真实的 AST 分析
- **本体规则管理**：提供接口管理 ontology_rules，支持从文件加载和保存

## 工作流程
1. **代码切分**：将原始代码切分为可处理的块（模拟）
2. **AST 分析**：使用 code-to-ast-new 解析 AST，提取核心变量和函数调用
3. **语义标注**：使用责任链模式对节点进行语义标注
4. **代码总结**：当规则未命中时，调用大模型对代码进行总结
5. **结果输出**：将处理结果组装成统一的 JSON 结构返回

## 参数

### 输入参数
| 参数名 | 类型 | 描述 | 是否必填 | 默认值 |
|-------|------|------|---------|-------|
| code | string | 要分析的 Python 代码字符串 | 是 | 无 |
| rules_file | string | 本体规则文件路径 | 否 | ontology_rules.json |

### 输出参数
| 参数名 | 类型 | 描述 |
|-------|------|------|
| status | string | 处理状态，成功为 "success"，失败为 "error" |
| message | string | 错误信息，仅当 status 为 "error" 时存在 |
| pipeline_steps | array | 执行的管道步骤 |
| labeled_nodes | array | 标注后的节点列表，每个节点包含 "name" 和 "type" 字段 |
| code_summary | string | 代码总结，当规则未命中时生成 |

## 示例

### 输入示例
```json
{
  "code": "import cv2\n\n# 读取视频\ncap = cv2.VideoCapture(0)\n\n# 目标检测\nresults = model.predict(frame)\n\n# 目标跟踪\ntracks = tracker.update(results)\n\n# 保存结果\ndb.save(tracks)"
}
```

### 输出示例
```json
{
  "status": "success",
  "pipeline_steps": ["split", "ast_extract", "semantic_label", "code_summary"],
  "labeled_nodes": [
    {"name": "cv2.VideoCapture", "type": "Camera"},
    {"name": "model.predict", "type": "Detection"},
    {"name": "tracker.update", "type": "Tracking"},
    {"name": "db.save", "type": "Database"}
  ],
  "code_summary": "这是一段包含视频流读取和目标检测的 Python 代码。"
}
```

## 命令行使用

### 分析代码
```bash
python scripts/label.py \
  --code "import cv2\ncap = cv2.VideoCapture(0)\nresults = model.predict(frame)\ntracks = tracker.update(results)\ndb.save(tracks)"
```

### 分析代码文件
```bash
python scripts/label.py \
  --file input.py \
  --output output.json
```

### 添加本体规则
```bash
python scripts/label.py \
  --add-rule "cv2" "Camera"
```

### 指定本体规则文件
```bash
python scripts/label.py \
  --code "import cv2\ncap = cv2.VideoCapture(0)" \
  --rules-file custom_rules.json
```

## 依赖
- Python 3.7+
- 标准库 `abc`, `ast`, `json`, `os`, `sys`
- code-to-ast-new 技能

## 注意事项
- 此技能使用模拟的 LLM 调用，实际实现中应该调用真实的 LLM API
- 规则库的质量直接影响标注结果的准确性
- 对于复杂的代码，可能需要更复杂的 AST 分析逻辑
- 代码总结功能在规则未命中时触发，提供代码的整体语义理解
- 本体规则文件默认保存在技能目录下的 ontology_rules.json 文件中

## 扩展指南

### 添加新的标注器
1. 继承 `BaseLabeler` 类
2. 实现 `label` 方法
3. 将新标注器添加到 `SemanticLabelingPipeline` 中

### 修改本体规则
1. 编辑 ontology_rules.json 文件
2. 或使用命令行参数 `--add-rule` 添加规则
3. 或使用 `OntologyManager` 类的方法管理规则

### 集成真实的 LLM
1. 修改 `LLMFallbackLabeler._call_llm_api` 方法，调用真实的 LLM API
2. 修改 `CodeSummarizer._call_llm_api` 方法，调用真实的 LLM API

### 集成真实的代码切分
修改 `DeerFlowOrchestrator._mock_code_split` 方法，集成真实的代码切分技能
