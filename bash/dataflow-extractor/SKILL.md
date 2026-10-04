---
name: dataflow-extractor
description: 通过静态分析代码片段，提取变量和模块之间的数据流转关系（Dataflow Edges）。
---

# 数据流提取器技能

## 概述

此技能使用 Python 原生的 `ast` 模块，通过静态分析代码片段，提取变量和模块之间的数据流转关系（Dataflow Edges）。它能够识别赋值操作和函数返回值，捕获代码中的数据流动迹象。

## 核心功能

- **AST 解析**：使用 Python 原生的 `ast` 模块解析代码
- **数据流提取**：提取变量和模块之间的数据流转关系
- **赋值操作分析**：分析普通赋值和带类型注解的赋值
- **函数调用分析**：分析函数调用中的数据流动
- **异常处理**：处理代码语法错误，确保工作流不会崩溃
- **轻量级实现**：不依赖外部库，使用纯 Python 实现

## 工作流程

### 步骤 1：接收代码输入

用户提供包含数据流动的 Python 代码片段。

### 步骤 2：解析代码

使用 `ast.parse()` 将代码解析为抽象语法树。

### 步骤 3：遍历 AST

使用 `DataflowVisitor` 遍历 AST，提取数据流关系。

### 步骤 4：生成数据流图

根据提取的数据流关系，生成数据流图数据。

### 步骤 5：输出结果

以 JSON 格式输出数据流图数据。

## 核心解析逻辑

1. **处理普通赋值**：重写 `visit_Assign` 方法，处理 `a = b` 或 `a = func(b)` 等赋值操作。
2. **处理带类型注解的赋值**：重写 `visit_AnnAssign` 方法，处理 `a: int = b` 等带类型注解的赋值。
3. **规则 1**：如果右值（RHS）是一个变量（Name），则提取 [RHS, LHS]。
4. **规则 2**：如果右值是一个函数调用（Call），则将调用的函数名或对象作为数据源，提取 [Function/Object, LHS]。
5. **规则 3**：忽略纯字面量（常量、数字、字符串）的赋值。

## 使用示例

### 基本使用

```python
from dataflow_extractor import ASTDataflowExtractor

extractor = ASTDataflowExtractor()
code = """
frame = cv2.imread('image.jpg')
results = model(frame)
tracks = tracker.update(results)
db.save(tracks)
"""
result = extractor.extract(code)
print(result)
```

**输出：**
```json
{
  "dataflow": [
    ["cv2", "frame"],
    ["frame", "results"],
    ["model", "results"],
    ["results", "tracks"],
    ["tracker", "tracks"],
    ["tracks", "db"]
  ]
}
```

### 命令行使用

```bash
python /mnt/skills/custom/program_snippet/dataflow-extractor/scripts/extract.py \
  --code "frame = cv2.imread('image.jpg')\nresults = model(frame)\ntracks = tracker.update(results)\ndb.save(tracks)"
```

## 参数

| 参数 | 描述 |
|------|------|
| `--code` | 要分析的 Python 代码字符串 |
| `--file` | 包含要分析的代码的文件路径 |
| `--output` | 保存输出结果的文件路径 |

## 支持的数据流类型

- **变量赋值**：如 `a = b`
- **函数调用**：如 `a = func(b)`
- **方法调用**：如 `a = obj.method(b)`
- **带类型注解的赋值**：如 `a: int = b`
- **表达式赋值**：如 `a = b + c`

## 输出格式

输出是一个包含数据流关系的 JSON 字典：

```json
{
  "dataflow": [
    ["frame", "model"],
    ["results", "tracker"],
    ["tracks", "db"]
  ]
}
```

## 依赖

- Python 3.7+
- 标准库 `ast`
- 标准库 `abc`

## 注意事项

- 此技能使用静态分析，只能提取显式的数据流动关系
- 对于动态数据流动（如 `getattr(obj, "attr")`），可能无法正确识别
- 对于导入的模块和函数，会记录完整的名称（如 `cv2.imread` 提取为 `cv2`）
- 如果代码存在语法错误，会返回空的数据流列表，而不是崩溃

## 示例

### 示例 1：简单变量赋值

**输入：**
```python
a = 1
b = a
c = b
```

**输出：**
```json
{
  "dataflow": [
    ["a", "b"],
    ["b", "c"]
  ]
}
```

### 示例 2：函数调用

**输入：**
```python
def add(a, b):
    return a + b

x = 1
y = 2
z = add(x, y)
```

**输出：**
```json
{
  "dataflow": [
    ["x", "z"],
    ["y", "z"],
    ["add", "z"]
  ]
}
```

### 示例 3：方法调用

**输入：**
```python
class MyClass:
    def method(self, value):
        return value * 2

obj = MyClass()
in_value = 10
out_value = obj.method(in_value)
```

**输出：**
```json
{
  "dataflow": [
    ["MyClass", "obj"],
    ["obj", "out_value"],
    ["in_value", "out_value"]
  ]
}
```

### 示例 4：处理语法错误

**输入：**
```python
def missing_parenthesis:
    a = 1
    b = a
```

**输出：**
```json
{
  "dataflow": []
}
```

## 集成到 DeerFlow

1. 将此技能添加到 DeerFlow 的技能列表中
2. 在需要分析代码数据流的地方调用此技能
3. 使用提取的数据流关系为 Agent 提供代码执行流的上下文
