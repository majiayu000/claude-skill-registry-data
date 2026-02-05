---
name: js-checker
description: "JavaScript 代码检查和修复工具。当需要执行 JavaScript 代码时，使用此技能进行：1) 检查本地 Node.js 版本是否支持代码语法，2) 自动修复全角符号等常见问题，3) 验证代码可执行性，4) 返回检查结果供主 Agent 使用 execute_shell_command 执行"
---

# JavaScript 代码检查工具

## 概述

此技能提供 JavaScript 代码的检查、修复和验证功能，确保代码可以在本地 Node.js 环境中成功执行。

## 核心功能

### 1. Node.js 版本检查
- 检查本地 Node.js 版本
- 验证代码语法是否与 Node.js 版本兼容
- 检查是否使用了不支持的语法特性

### 2. 代码修复
- 自动修复全角符号（中文标点符号）
- 修复常见的编码问题
- 修复常见的语法错误

### 3. 代码验证
- 使用 `node --check` 验证语法
- 尝试执行代码验证可执行性
- 检查依赖项是否可用

### 4. 执行准备
- 返回检查结果和建议
- 提供执行命令（供 `execute_shell_command` 使用）
- 标记需要修复的问题

## 工作流程

### 标准流程

1. **检查 Node.js 版本**
   ```
   使用 scripts/check_node_version.py 检查本地 Node.js 版本
   ```

2. **检查代码语法**
   ```
   使用 scripts/check_js_syntax.py 检查 JavaScript 代码语法
   ```

3. **修复代码问题**
   ```
   使用 scripts/fix_js_code.py 自动修复全角符号等问题
   ```

4. **验证代码可执行性**
   ```
   使用 scripts/validate_js.py 验证代码是否可以执行
   ```

5. **返回结果**
   ```
   返回检查结果、修复后的代码和执行命令
   ```

## 使用方法

### 方式 1: 完整检查流程

```python
# 1. 检查 Node.js 版本
node_version = check_node_version()

# 2. 检查代码语法
syntax_result = check_js_syntax(js_code, node_version)

# 3. 修复代码
fixed_code = fix_js_code(js_code)

# 4. 验证代码
validation_result = validate_js(fixed_code)

# 5. 返回结果
return {
    "node_version": node_version,
    "syntax_ok": syntax_result["valid"],
    "fixed_code": fixed_code,
    "validation_ok": validation_result["valid"],
    "execute_command": f"node -e \"{fixed_code}\""
}
```

### 方式 2: 快速检查

```python
# 一次性完成所有检查
result = check_and_fix_js(js_code)
```

## 脚本说明

### scripts/check_node_version.py

检查本地 Node.js 版本和兼容性。

**功能**:
- 检查 Node.js 是否安装
- 获取 Node.js 版本号
- 检查版本是否满足要求（>= 14.0.0）

**返回**:
```json
{
    "installed": true,
    "version": "18.17.0",
    "major": 18,
    "minor": 17,
    "patch": 0,
    "meets_requirement": true
}
```

### scripts/check_js_syntax.py

检查 JavaScript 代码语法。

**功能**:
- 使用 `node --check` 检查语法
- 检查是否使用了不支持的语法特性
- 检查代码糖（ES6+ 特性）兼容性

**参数**:
- `js_code`: JavaScript 代码字符串
- `node_version`: Node.js 版本（可选）

**返回**:
```json
{
    "valid": true,
    "errors": [],
    "warnings": [],
    "syntax_features": ["arrow-functions", "async-await"]
}
```

### scripts/fix_js_code.py

自动修复 JavaScript 代码中的常见问题。

**功能**:
- 修复全角符号（中文标点符号）
- 修复编码问题
- 修复常见的语法错误

**参数**:
- `js_code`: JavaScript 代码字符串

**返回**:
```json
{
    "fixed_code": "...",
    "fixes_applied": [
        {"type": "fullwidth_char", "line": 5, "original": "，", "fixed": ","},
        {"type": "encoding", "line": 10, "description": "Fixed UTF-8 encoding"}
    ]
}
```

### scripts/validate_js.py

验证 JavaScript 代码是否可以执行。

**功能**:
- 尝试执行代码（使用 `node -e`）
- 检查运行时错误
- 验证依赖项

**参数**:
- `js_code`: JavaScript 代码字符串

**返回**:
```json
{
    "valid": true,
    "executable": true,
    "errors": [],
    "output": "..."
}
```

## 集成到主 Agent

检查完成后，主 Agent 可以使用 AgentScope 的 `execute_shell_command` 工具执行代码：

```python
from agentscope.tool import execute_shell_command

# 1. 使用 js-checker 检查代码
check_result = check_and_fix_js(js_code)

# 2. 如果检查通过，执行代码
if check_result["validation_ok"]:
    execute_command = check_result["execute_command"]
    result = await execute_shell_command(execute_command)
```

## 示例

### 示例 1: 检查并修复全角符号

**输入代码**:
```javascript
console.log("Hello，World！");
```

**修复后**:
```javascript
console.log("Hello,World!");
```

### 示例 2: 检查语法兼容性

**输入代码**:
```javascript
const x = 1;
let y = 2;
```

**检查结果**:
- Node.js 版本: 18.17.0 ✅
- 语法检查: 通过 ✅
- 代码糖: ES6+ 特性，Node.js 18 支持 ✅

### 示例 3: 验证可执行性

**输入代码**:
```javascript
console.log("Test");
```

**验证结果**:
- 语法: 通过 ✅
- 执行: 成功 ✅
- 输出: "Test"

## 注意事项

1. **Node.js 版本要求**: 建议使用 Node.js >= 14.0.0
2. **代码执行**: 代码会在临时环境中执行，不会影响系统
3. **依赖项**: 如果代码使用了外部依赖，需要先安装
4. **安全性**: 代码执行前会进行基本的安全检查

## 相关工具

- AgentScope `execute_shell_command`: 执行修复后的代码
- Node.js: JavaScript 运行时环境

