---
name: pipeline-reasoner
description: >-
  使用 DeerFlow CloudLLMReasoner 的本地图推理规则分析业务 DAG，
  并输出严格 JSON 格式的流水线类型、缺失模块和逻辑异常诊断结果。
---

# Pipeline Reasoner

## 目标

Skill 6 使用 `deerflow.pipeline.CloudLLMReasoner` 作为 DeerFlow Agentic RAG 的图逻辑推理引擎。该类保留 `CloudLLMReasoner` 名称以兼容既有调用方，但当前实现不再依赖 OpenAI 兼容 API key，而是由 DeerFlow 根据 pipeline-reasoner 方法论在本地完成推理诊断。

该推理器负责诊断：

- `pipeline_type`：推断出的智慧城市业务分类。
- `missing`：流水线中可能缺失的关键业务模块。
- `anomalies`：逻辑断层、反向依赖、数据流不连通或业务顺序异常。

## 模块位置

```text
backend/packages/harness/deerflow/pipeline/reasoner.py
```

推荐导入方式：

```python
from deerflow.pipeline import CloudLLMReasoner
```

## 使用方式

```python
import networkx as nx

from deerflow.pipeline import CloudLLMReasoner

graph = nx.DiGraph()
graph.add_node("camera.open", type="Camera")
graph.add_node("model.predict", type="Detection")
graph.add_edge("camera.open", "model.predict")

reasoner = CloudLLMReasoner()
diagnosis = reasoner.reason(graph)
```

期望输出结构：

```python
{
    "pipeline_type": "交通监控与存储",
    "missing": ["Decode", "Storage"],
    "anomalies": ["逻辑断层: Camera 与 Detection 之间没有数据流转路径"],
}
```

## 序列化约定

`_serialize_for_llm(graph)` 只提取两类信息，以保持 Prompt 极简：

1. 节点业务类型：优先读取每个节点的 `type` 属性。
2. 边的拓扑路径：渲染为 `SourceType -> TargetType`。

严禁序列化完整节点属性、边 payload、源码、元数据或原始 `networkx` 图对象。

序列化示例：

```text
NodeTypes:
Camera
Detection
Edges:
Camera -> Detection
```

## 本地推理约定

`CloudLLMReasoner.reason(graph)` 不会发起网络请求。它会基于以下信息进行确定性诊断：

- 节点业务类型，例如 `Camera`、`Decode`、`Detection`、`Tracking`、`Storage`。
- 边的拓扑方向，例如 `Camera -> Detection`。
- 智慧城市流水线常见阶段顺序，例如采集、解码、预处理、检测、跟踪、识别、分析、告警、存储、输出。

输出仍然严格保持 `pipeline_type`、`missing`、`anomalies` 三个字段，便于上游或下游模块继续按原 JSON 契约消费结果。

## 异常处理

以下情况会返回安全诊断结果：

- 空图会返回 `pipeline_type="unknown"`，并在 `anomalies` 中标记“空流水线”。
- 无法识别的节点类型不会中断推理，只会跳过对应阶段规则。
- 存在循环、反向依赖或关键路径缺失时，会写入 `anomalies`。

```python
{
    "pipeline_type": "unknown",
    "missing": [],
    "anomalies": ["空流水线: 未发现可诊断的业务节点"],
}
```

## 验证方式

修改后运行聚焦测试：

```powershell
pytest backend\tests\test_pipeline_reasoner.py
```
