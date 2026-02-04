---
name: python-code-reviewer
description: 审查 Python 代码，提供改进建议，确保代码质量和最佳实践
---

# Python Code Reviewer Skill

当用户请求代码审查或询问 Python 代码质量时，使用此技能进行全面评估。

## 审查清单

### 1. 代码风格 (PEP 8)
- [ ] 缩进使用 4 个空格
- [ ] 行长度不超过 79 字符（或 99 字符）
- [ ] 导入语句分组排序
- [ ] 命名规范（snake_case 函数/变量，PascalCase 类）

### 2. 类型提示
- [ ] 函数参数有类型注解
- [ ] 返回值有类型注解
- [ ] 复杂类型使用 `typing` 模块

### 3. 文档
- [ ] 模块有 docstring
- [ ] 公共函数有 docstring
- [ ] 复杂逻辑有注释

### 4. 错误处理
- [ ] 使用具体的异常类型
- [ ] 不要裸露的 `except:`
- [ ] 适当使用 `try/except/finally`

### 5. 性能考虑
- [ ] 避免在循环中重复计算
- [ ] 使用生成器处理大数据
- [ ] 合理使用列表推导式

## 审查报告格式

```markdown
## 代码审查报告

### 优点
- ...

### 需要改进
- **[严重]** ...
- **[建议]** ...

### 重构建议
- ...
```

## 常见问题示例

### 不推荐
```python
def process(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
```

### 推荐
```python
def process(data: list[int]) -> list[int]:
    """过滤正数并翻倍。"""
    return [item * 2 for item in data if item > 0]
```
