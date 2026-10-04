---
name: c-support
description: C Language Support Library for OpenClaw skills. Provides AST parsing, CMake analysis, Unity test generation, and security rule checking for C projects.
tools:
  - read
  - write
  - exec
---

# C Support Library

C语言支持库，为OpenClaw技能提供C代码分析能力。

**Version**: 1.0  
**Features**: AST解析、CMake分析、Unity测试生成、安全规则库

## Purpose

这个库为其他技能（code-review, security, tdd等）提供共享的C语言基础设施：

- **AST解析** - tree-sitter/pycparser封装
- **CMake分析** - 解析CMakeLists.txt
- **Unity测试** - 生成Unity测试框架代码
- **安全规则** - CWE漏洞检测规则

## Usage

```python
from lib.c_parser import CParser, analyze_project
from lib.cmake_parser import CMakeParser, analyze_cmake_project
from lib.unity_templates import UnityTestGenerator
from lib.c_security_rules import CSecurityChecker

# Parse C file
parser = CParser()
info = parser.parse_file("src/main.c")
print(f"Found {len(info.functions)} functions")

# Analyze CMake project
cmake_info = analyze_cmake_project(".")
print(f"Targets: {[t.name for t in cmake_info.targets]}")

# Check security
checker = CSecurityChecker()
issues = checker.check_file("src/main.c")
print(f"Found {len(issues)} security issues")

# Generate Unity tests
generator = UnityTestGenerator()
test_code = generator.generate_test_file(info.functions, "myheader.h")
```

## Modules

### c_parser.py

C代码解析，提取：
- 函数定义和签名
- 宏定义
- 结构体/联合体/枚举
- 头文件依赖
- 危险函数调用

### cmake_parser.py

CMake分析，提取：
- 项目名称和版本
- 构建目标（可执行文件/库）
- 编译选项和定义
- 包含目录
- 测试定义
- 子目录

### unity_templates.py

Unity测试框架支持：
- 测试文件生成
- CMake集成模板
- Mock模板生成
- 断言参考

### c_security_rules.py

安全漏洞检测：
- 危险函数检测（strcpy, gets等）
- CWE规则库
- 格式化字符串漏洞
- 硬编码凭证检测
- 内存安全问题

## Installation

```bash
# Install dependencies
pip install tree-sitter tree-sitter-c pycparser

# Or use the requirements.txt
pip install -r requirements.txt
```

## Testing

```bash
cd skills/c-support
python -m pytest tests/
```

## Integration

其他技能可以通过以下方式使用：

```python
import sys
sys.path.insert(0, '/path/to/skills/c-support/lib')

from c_parser import CParser
from cmake_parser import CMakeParser
# ... etc
```

## License

MIT License
