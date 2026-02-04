---
name: comment-enforcer
description: Go 代码注释规范检查与修复工具。自动化检查注释格式、术语一致性、包级别注释规范，利用大模型进行语义分析和注释生成，确保项目注释符合专业标准。
---

# Go 代码注释规范检查器

## 概述

自动化检查和修复 Go 项目代码注释规范性，基于项目注释规范（.ai/rule.md.bak），结合脚本检查和大模型语义分析，确保注释的专业性、准确性和一致性。

**自动化策略**：60% 大模型（语义分析、注释生成）+ 40% 脚本（格式检查、术语一致性）

## 使用场景

- **新项目规范检查** - 检查新项目注释是否符合规范
- **代码审查辅助** - 快速发现注释问题并提供修复建议
- **批量注释生成** - 为缺失的注释生成符合规范的内容
- **术语一致性检查** - 确保全项目注释术语使用统一
- **代码重构验证** - 重构后验证注释是否需要更新

## 快速开始

### 一键检查（推荐）

```bash
# 1. 格式检查（脚本）
python3 .claude/skills/comment-enforcer/scripts/check_format.py

# 2. 术语一致性检查（脚本）
python3 .claude/skills/comment-enforcer/scripts/check_terminology.py

# 3. 包级别注释检查（脚本）
python3 .claude/skills/comment-enforcer/scripts/check_pkg_doc.py

# 4. 大模型语义分析
python3 .claude/skills/comment-enforcer/scripts/analyze_with_llm.py

# 5. 生成检查报告
python3 .claude/skills/comment-enforcer/scripts/generate_report.py

# 6. 执行修复（用户确认后）
python3 .claude/skills/comment-enforcer/scripts/fix_comment.py report.md
```

### 快速检查模式

```bash
# 只执行脚本检查（快速，无大模型）
python3 .claude/skills/comment-enforcer/scripts/check_format.py
python3 .claude/skills/comment-enforcer/scripts/check_terminology.py
python3 .claude/skills/comment-enforcer/scripts/check_pkg_doc.py
```

## 工作流程

### 阶段 1：脚本检查（40% 自动化）

**目标**：快速发现格式和术语问题

**时间**：1-2 分钟

**检查内容**：
```
开始
  ↓
1. 格式检查 [check_format.py]
   ├─ 注释是否存在
   ├─ 是否以中文标点结束
   ├─ 位置是否正确（在声明上方）
   └─ 统计缺失注释的数量
  ↓
2. 术语一致性检查 [check_terminology.py]
   ├─ 全局搜索 context.Context
   ├─ 全局搜索 *Config
   ├─ 全局搜索 Logger
   └─ 比对注释表述是否一致
  ↓
3. 包级别注释检查 [check_pkg_doc.py]
   ├─ 检查每个包是否有 doc.go
   ├─ 验证 doc.go 格式
   └─ 检查非 doc.go 文件是否包含包注释
  ↓
完成（输出 JSON 结果）
```

---

### 阶段 2：大模型分析（60% 智能化）

**目标**：语义分析和注释生成

**时间**：3-5 分钟（取决于代码量）

**分析内容**：
```
开始
  ↓
1. Interface 一致性检查
   ├─ 读取接口定义
   ├─ 读取实现方法
   ├─ 比对注释是否一致
   └─ 报告不一致的地方
  ↓
2. 语义准确性判断
   ├─ 分析代码逻辑
   ├─ 判断注释是否准确反映功能
   └─ 识别需要改进的注释
  ↓
3. 注释内容生成
   ├─ 识别缺失的注释
   ├─ 分析代码上下文
   └─ 生成符合规范的注释
  ↓
完成（输出 JSON 结果）
```

---

### 阶段 3：报告生成

**目标**：整合所有检查结果，生成可操作的报告

**输出格式**：Markdown 格式，包含：
- 总览统计
- 分类问题列表（格式、术语、语义）
- 每个问题的详细说明和解决方案
- 复选框用于二次确认

---

### 阶段 4：修复执行

**原则**：二次确认机制，不自动修改代码

**流程**：
```
1. 执行检查（脚本 + 大模型）
2. 生成报告
3. 用户审查报告
4. 用户勾选需要修复的问题
5. 执行修复
   ├─ 脚本修复格式问题
   ├─ 大模型生成缺失注释
   └─ 大模型改进不准确的注释
6. 验证修复结果
```

## 脚本说明

### check_format.py - 格式检查器

**功能**：
- 检查注释是否存在
- 检查注释是否以中文标点结束
- 检查注释位置是否正确（在声明上方）
- 统计缺失注释的数量

**用法**：
```bash
# 检查整个项目
python3 .claude/skills/comment-enforcer/scripts/check_format.py

# 检查特定目录
python3 .claude/skills/comment-enforcer/scripts/check_format.py internal/biz

# 检查特定文件
python3 .claude/skills/comment-enforcer/scripts/check_format.py internal/biz/greeter.go
```

**输出示例**：
```json
{
  "total_files": 45,
  "files_with_issues": 12,
  "issues": [
    {
      "file": "internal/server/server.go",
      "line": 45,
      "type": "missing_punctuation",
      "current": "// 这是一个示例函数",
      "suggested": "// 这是一个示例函数。",
      "auto_fixable": true
    },
    {
      "file": "internal/data/greeter.go",
      "line": 89,
      "type": "missing_comment",
      "item": "func Save",
      "auto_fixable": false
    }
  ]
}
```

**自动化程度**：100% 脚本自动化

---

### check_terminology.py - 术语一致性检查器

**功能**：
- 全局搜索特定类型（如 `context.Context`）
- 提取所有相关注释
- 比对注释表述是否一致
- 报告不一致的地方

**用法**：
```bash
# 检查所有标准术语
python3 .claude/skills/comment-enforcer/scripts/check_terminology.py

# 检查特定类型
python3 .claude/skills/comment-enforcer/scripts/check_terminology.py --type context.Context

# 自定义标准表述
python3 .claude/skills/comment-enforcer/scripts/check_terminology.py \
  --type context.Context \
  --standard "请求上下文，用于取消与超时控制。"
```

**输出示例**：
```json
{
  "context.Context": {
    "standard": "请求上下文，用于取消与超时控制。",
    "variations": [
      {
        "text": "上下文对象",
        "count": 3,
        "files": [
          "internal/biz/greeter.go:89",
          "internal/data/data.go:45",
          "internal/service/service.go:123"
        ]
      },
      {
        "text": "请求上下文",
        "count": 1,
        "files": ["internal/server/server.go:67"]
      }
    ],
    "total_inconsistent": 4
  }
}
```

**自动化程度**：100% 脚本自动化

---

### check_pkg_doc.py - 包级别注释检查器

**功能**：
- 检查每个包目录是否存在 `doc.go` 文件
- 验证 `doc.go` 格式是否正确
- 检查是否有非 `doc.go` 文件包含包级别注释

**用法**：
```bash
# 检查所有包
python3 .claude/skills/comment-enforcer/scripts/check_pkg_doc.py

# 检查特定目录
python3 .claude/skills/comment-enforcer/scripts/check_pkg_doc.py internal/
```

**输出示例**：
```json
{
  "total_packages": 15,
  "packages_with_doc": 12,
  "packages_missing_doc": [
    {
      "package": "internal/biz",
      "path": "internal/biz",
      "suggestion": "创建 internal/biz/doc.go"
    }
  ],
  "files_with_pkg_comment": [
    {
      "file": "internal/server/http.go",
      "line": 10,
      "comment": "// Package server 提供 HTTP 服务器实现",
      "suggestion": "移动到 doc.go 文件"
    }
  ]
}
```

**自动化程度**：100% 脚本自动化

---

### analyze_with_llm.py - 大模型语义分析器

**功能**：
- 检查 interface 实现方法的注释是否与接口定义一致
- 判断注释是否准确反映代码功能
- 识别需要改进的注释（过于简略、不准确）
- 为缺失的注释生成符合规范的内容

**用法**：
```bash
# 分析整个项目
python3 .claude/skills/comment-enforcer/scripts/analyze_with_llm.py

# 分析特定文件
python3 .claude/skills/comment-enforcer/scripts/analyze_with_llm.py \
  internal/service/greeter.go

# 只分析 interface 一致性
python3 .claude/skills/comment-enforcer/scripts/analyze_with_llm.py \
  --check-interface-only

# 只生成缺失注释
python3 .claude/skills/comment-enforcer/scripts/analyze_with_llm.py \
  --generate-only
```

**输出示例**：
```json
{
  "analyzed_files": 45,
  "semantic_issues": [
    {
      "file": "internal/data/greeter.go",
      "line": 123,
      "type": "inaccurate_comment",
      "current": "// 保存数据",
      "issue": "过于简略，未说明具体操作和数据类型",
      "suggested": "// Save 保存 Greeter 实体到数据库。",
      "reason": "需要明确操作类型（Save）、对象（Greeter）和目标（数据库）"
    }
  ],
  "interface_mismatches": [
    {
      "file": "internal/service/greeter.go",
      "line": 45,
      "interface_def": "// Create 创建一个新的 Greeter 实体。",
      "implementation": "// CreateGreeter 创建 Greeter。",
      "suggested": "统一为'创建一个新的 Greeter 实体。'"
    }
  ],
  "missing_comments": [
    {
      "file": "internal/domain/greeter.go",
      "line": 12,
      "type": "type_definition",
      "suggested": "// Greeter Greeter 领域模型。"
    }
  ]
}
```

**自动化程度**：
- 代码分析：100% 大模型
- 报告生成：脚本格式化输出

---

### generate_report.py - 报告生成器

**功能**：
- 整合所有检查结果
- 生成结构化的 Markdown 报告
- 提供符合规范的解决方案
- 汇总统计信息

**用法**：
```bash
# 生成完整报告（整合所有检查结果）
python3 .claude/skills/comment-enforcer/scripts/generate_report.py

# 指定输出文件
python3 .claude/skills/comment-enforcer/scripts/generate_report.py \
  --output comment-report.md

# 从已有结果文件生成报告
python3 .claude/skills/comment-enforcer/scripts/generate_report.py \
  --format-results format_results.json \
  --terminology-results terminology_results.json \
  --pkg-results pkg_results.json \
  --llm-results llm_results.json
```

**报告格式**：
```markdown
# 注释规范检查报告

生成时间：2026-01-06 15:30:00
检查范围：internal/, cmd/, pkg/

## 📊 总览
- 检查文件数：45
- 发现问题：12 个
  - 格式问题：5 个
  - 术语一致性问题：3 个
  - 语义问题：4 个

## 1️⃣ 格式问题（脚本检查 - 可自动修复）
### 1.1 注释未以标点结束
- [ ] internal/server/server.go:45
  当前：// 这是一个示例函数
  建议：// 这是一个示例函数。

### 1.2 缺少 doc.go 文件
- [ ] internal/biz/
  建议：创建 internal/biz/doc.go，添加包级别注释
  示例：
  ```go
  // Copyright 2025 fsyyft-go
  //
  // Licensed under the MIT License.
  //
  // Package biz 提供业务逻辑层实现。
  package biz
  ```

## 2️⃣ 术语一致性问题（脚本检查 - 需手动确认）
### 2.1 context.Context 注述不一致
- [ ] internal/biz/greeter.go:89
  当前：ctx 上下文对象
  标准：请求上下文，用于取消与超时控制。
  影响：3 处引用
  建议：批量替换为标准表述

## 3️⃣ 语义问题（大模型分析 - 需专业判断）
### 3.1 注释不够准确
- [ ] internal/data/greeter.go:123
  当前注释：// 保存数据
  问题：过于简略，未说明具体操作和数据类型
  建议：// Save 保存 Greeter 实体到数据库。
  理由：需要明确操作类型（Save）、对象（Greeter）和目标（数据库）

## 4️⃣ 缺失注释（大模型生成 - 需确认）
### 4.1 缺少类型注释
- [ ] internal/domain/greeter.go:12
  当前：无注释
  建议：
  ```go
  // Greeter Greeter 领域模型。
  type Greeter struct {
      // ID 唯一标识符。
      ID int64
      // Hello 问候消息。
      Hello string
  }
  ```

## ✅ 下一步操作

### 自动修复（脚本）
- 格式问题：5 个可自动修复

### 需要确认（列出清单）
- 术语一致性问题：3 个
- 语义问题：4 个
- 缺失注释：生成 4 个

请确认后执行修复操作。
```

**自动化程度**：100% 脚本自动化

---

### fix_comment.py - 修复执行器

**功能**：
- 脚本修复：格式问题（添加标点、调整位置）
- 大模型生成：缺失注释的内容
- 大模型优化：改进不准确的注释
- 创建 doc.go 文件

**用法**：
```bash
# 基本用法（从报告文件读取）
python3 .claude/skills/comment-enforcer/scripts/fix_comment.py report.md

# 预览模式（不实际修改）
python3 .claude/skills/comment-enforcer/scripts/fix_comment.py \
  report.md --dry-run

# 只修复格式问题
python3 .claude/skills/comment-enforcer/scripts/fix_comment.py \
  report.md --format-only

# 只生成缺失注释
python3 .claude/skills/comment-enforcer/scripts/fix_comment.py \
  report.md --generate-only
```

**安全机制**：
- 修复前自动创建 `.backup/comments/` 备份
- 支持预览模式（--dry-run）
- 提供回滚功能

**自动化程度**：
- 格式修复：100% 脚本
- 内容生成/改进：100% 大模型
- 执行协调：脚本

## 核心注释规范

### 1. 包级别注释规范

**强制要求**：
- 每个包必须在独立的 `doc.go` 文件中编写包级别注释
- `doc.go` 仅包含版权声明、包注释和 `package` 声明，不包含代码实现
- 除 `doc.go` 外，所有文件的 `package` 声明前后不得有任何注释

**doc.go 格式**：
```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package server 提供 HTTP 和 gRPC 服务器的实现。
//
// 本包包含服务器的初始化、配置和中间件设置功能，
// 支持基于 Kratos 框架的 Web 服务开发。
package server
```

---

### 2. 类型定义注释规范

**接口定义**：必须有功能说明、方法注释（含参数和返回值）

**结构体定义**：每个字段必须有用途说明

**示例**：
```go
// GreeterUsecase Greeter 用例接口。
type GreeterUsecase interface {
    // CreateGreeter 创建一个新的 Greeter 实体。
    // 参数：
    //   - ctx：请求上下文，用于取消与超时控制。
    //   - g：待创建的 Greeter 实体，Hello 字段不能为空。
    //
    // 返回值：
    //   - *Greeter：创建成功的实体，包含生成的标识。
    //   - error：创建失败时返回错误，成功时返回 nil。
    CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error)
}

// Greeter Greeter 领域模型。
type Greeter struct {
    // ID 唯一标识符。
    ID int64
    // Hello 问候消息。
    Hello string
}
```

---

### 3. 函数和方法注释规范

**标准格式**：
```go
// CreateGreeter 创建一个新的 Greeter 实体。
// 参数：
//   - ctx：请求上下文，用于取消与超时控制。
//   - g：待创建的 Greeter 实体，Hello 字段不能为空。
//
// 返回值：
//   - *Greeter：创建成功的实体，包含生成的标识。
//   - error：创建失败时返回错误，成功时返回 nil。
func (u *greeterUsecase) CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // ...
}
```

**要求**：
- 第一行：功能概述（必须以中文句号结束）
- 参数部分：列出每个参数及其说明
- 返回值部分：列出每个返回值及其说明
- 如果函数无参数或返回值，省略对应部分

---

### 4. 标准术语表

| 参数类型 | 标准表述 |
|---------|---------|
| `context.Context` | "请求上下文，用于取消与超时控制。" |
| `*Config` | "应用配置信息。" |
| `Logger` | "日志记录器。" |
| `*Data` | "数据仓储接口。" |
| `*Greeter` | "Greeter 实体。" |
| `error` 返回值 | "失败时返回错误，成功时返回 nil。" |

**一致性要求**：
- 所有相同类型必须使用相同的注释表述
- 使用 `check_terminology.py` 全局检查
- 发现不一致时，使用统一的标准表述

---

## 大模型介入点

| 介入点 | 触发条件 | 大模型职责 | 介入程度 |
|-------|---------|-----------|---------|
| interface 一致性检查 | 分析 interface 和实现时 | 比对注释是否一致，识别不一致的地方 | 20% |
| 语义准确性判断 | 分析代码和注释时 | 判断注释是否准确反映代码功能 | 30% |
| 注释内容生成 | 发现缺失注释时 | 生成符合规范的专业中文注释 | 40% |
| 注释改进建议 | 发现不准确注释时 | 提供更专业、更准确的表述 | 40% |
| 专业术语选择 | 编写注释时 | 使用项目约定的标准术语表述 | 10% |

**总体自动化程度**：60% 大模型 + 40% 脚本

---

## 故障排除

### 常见问题

#### 问题 1：Python 环境问题

**症状**：
```
ModuleNotFoundError: No module named 'anthropic'
```

**解决方案**：
1. 检查虚拟环境是否存在
2. 安装依赖：`pip install anthropic`
3. 或使用 python-venv-manager 创建虚拟环境

---

#### 问题 2：大模型 API 调用失败

**症状**：
```
anthropic.APIError: Invalid API key
```

**解决方案**：
1. 检查 `ANTHROPIC_API_KEY` 环境变量
2. 确认 API key 有效
3. 检查网络连接

---

#### 问题 3：报告生成失败

**症状**：
```
KeyError: 'format_results'
```

**解决方案**：
1. 确保已运行所有检查脚本
2. 检查 JSON 文件是否存在
3. 验证 JSON 文件格式是否正确

---

### 回滚操作

**触发条件**：
- 修复后发现新问题
- 不满意修复结果
- 想重新开始

**回滚方法**：
```bash
# 自动回滚（使用备份）
cp -r .backup/comments/* .

# 或使用 Git
git checkout .
```

---

## 最佳实践

### 检查前准备

1. **确保代码可编译**
   - 运行 `go build ./...`
   - 确保无编译错误

2. **创建分支**
   - 在新分支上进行修复
   - 便于回滚和代码审查

3. **备份代码**
   - 虽然脚本会自动备份
   - 但建议额外创建 Git 提交

---

### 检查过程

1. **分步执行**
   - 先运行脚本检查（快速）
   - 再运行大模型分析（耗时）
   - 最后生成报告

2. **审查报告**
   - 仔细阅读每个问题
   - 判断是否需要修复
   - 勾选需要修复的项目

3. **预览修复**
   - 使用 `--dry-run` 预览
   - 检查将要修改的内容
   - 确认后再执行

---

### 修复后处理

1. **验证修复**
   - 运行 `go build ./...`
   - 运行 `go test ./...`
   - 检查修复结果

2. **提交更改**
   - 创建清晰的 commit message
   - 推送到远程仓库

3. **代码审查**
   - 让团队成员审查
   - 确保修复质量

---

## 自动化程度

**总体自动化程度**：60% 大模型 + 40% 脚本

### 脚本负责（40%）

- ✅ 格式检查（标点、位置、存在性）
- ✅ 术语一致性检查
- ✅ 包级别注释检查
- ✅ 报告生成
- ✅ 格式问题修复

### 大模型负责（60%）

- ✅ Interface 一致性检查
- ✅ 语义准确性判断
- ✅ 注释内容生成
- ✅ 注释改进建议
- ✅ 专业性保证

---

## 技术规格

- **Go 版本**：1.16+（Go modules）
- **Python 版本**：3.8+（脚本执行）
- **虚拟环境**：.venv（推荐使用 python-venv-manager）
- **跨平台**：Windows, macOS, Linux
- **备份位置**：`.backup/comments/` 在项目根目录
- **大模型 API**：Anthropic Claude API

---

## 注意事项

1. **专业性要求**
   - 生成的注释必须专业准确
   - 使用标准术语表述
   - 保持语义一致性

2. **安全机制**
   - 修复前自动备份
   - 支持预览模式
   - 提供回滚功能

3. **性能考虑**
   - 大模型分析耗时较长
   - 建议分步执行
   - 可以只运行脚本检查

4. **二次确认**
   - 不自动修改代码
   - 生成报告供用户审查
   - 用户确认后才执行修复

---

## 相关资源

### 规范来源
- `.ai/rule.md.bak` - 项目注释规范原始文档
- `references/comment_standards.md` - 提取的注释规范
- `references/terminology_table.md` - 标准术语映射表

### 示例代码
- `internal/biz/greeter.go` - 业务层示例
- `internal/server/server.go` - 服务器层示例
- `internal/service/greeter.go` - 服务层示例

### 参考文档
- [Effective Go](https://golang.org/doc/effective_go.html#commentary)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Kratos Framework Documentation](https://go-kratos.dev/)
