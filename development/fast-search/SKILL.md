---
name: fast-search
description: 通过运用智能搜索策略，能够加速对大型代码库进行全文搜索——这些策略包括并行搜索、模式优化、文件过滤以及结果汇总。该系统经过优化，能够以最短的时间完成搜索任务，同时所需加载的上下文信息也最少。
---

# Fast Search - 极速代码搜索

⚡ **核心优化**: 最小化上下文加载,直接执行工具调用,并行搜索,快速响应

---

## 0. ⚡ SPEED OPTIMIZATION RULES (CRITICAL)

### 核心原则: **SEARCH FIRST, EXPLAIN LATER**

**执行流程**:
```
用户请求 → 立即并行执行搜索 → 返回结果 → (可选)简短说明
         ↓
    无需加载完整文档/示例
    无需解释搜索策略
    无需展示搜索过程
```

### 速度优化清单 (MUST FOLLOW)

| 优化项 | 实施规则 | 速度提升 |
|-------|---------|---------|
| ✅ **跳过文档加载** | 不读取 references/示例文件 | 节省 2-5s |
| ✅ **直接工具调用** | 识别意图后立即调用工具 | 节省 1-3s |
| ✅ **并行执行** | 所有独立搜索同时发起 | 3-5x 加速 |
| ✅ **最小输出** | 默认用 `files_with_matches` | 节省 50-80% token |
| ✅ **智能过滤** | 自动推断文件类型 | 减少 60-90% 搜索范围 |
| ✅ **避免重复** | 记住搜索结果,不重复搜索 | 节省 100% |

### 立即执行模式 (Instant Execution Mode)

**触发搜索请求时,按以下步骤操作**:

1. **推断搜索意图** (< 0.5s 思考)
   - 提取关键词
   - 推断文件类型 (根据仓库特征)
   - 确定 outputMode (默认 `files_with_matches`)

2. **立即并行调用** (无需等待)
   ```
   同时发起所有搜索 → 等待结果 → 直接返回
   ```

3. **精简输出** (只给必要信息)
   - ✅ 结果文件列表/匹配数
   - ✅ 关键代码位置
   - ❌ 搜索策略说明
   - ❌ 参数解释
   - ❌ 性能分析

### 禁止减速行为 (MUST NOT DO)

| ❌ 禁止操作 | 原因 | 替代方案 |
|-----------|------|---------|
| 读取示例文件 | 浪费 2-5s | 直接使用内置模式 |
| 解释搜索计划 | 用户只要结果 | 直接执行 |
| 展示工具调用过程 | 增加噪音 | 静默执行 |
| 使用 `content` mode | 输出过大 | 优先 `files_with_matches` |
| 串行搜索 | 等待时间累加 | 并行执行 |
| 重复搜索 | 浪费时间和 token | 记住已搜索内容 |

---

## 1. 🎯 WHEN TO USE

### Activation Triggers

| Trigger | Description |
|---------|-------------|
| 大规模搜索 | 需要在整个仓库中查找符号、字符串或模式 |
| 符号追踪 | 查找函数定义、类引用、变量使用 |
| 依赖分析 | 追踪 import/include 关系 |
| 重构准备 | 需要找到所有需要修改的位置 |
| 代码审计 | 搜索特定模式(如安全问题、TODO等) |
| 玩法/业务逻辑定位 | 想知道"某个玩法/活动/系统"的代码入口和链路 |

### Keyword Triggers
- "搜索" / "查找" / "search" / "find" / "grep"
- "帮我搜" / "搜一下" / "帮我查" / "查一下" / "全局搜"
- "在哪里使用" / "where is used" / "引用" / "ref"
- "入口在哪" / "在哪里实现" / "怎么触发" / "触发链路"
- "玩法" / "玩法逻辑" / "活动逻辑" / "业务逻辑" / "规则" / "机制" / "流程" / "系统" / "模块"
- "战斗" / "副本" / "招募" / "钓鱼" / "小游戏" / "匹配" / "排行榜"

---

## 2. ⚡ INSTANT EXECUTION PATTERNS

### Pattern 1: 单一符号搜索 (< 2s)

**用户**: "搜索 handleLogin 函数"

**执行** (立即并行):
```typescript
// 不解释,直接执行 ↓
search_content({ 
  pattern: "handleLogin\\(", 
  fileTypes: ".js,.ts,.jsx,.tsx,.py",  // 自动推断
  outputMode: "files_with_matches" 
})
```

**返回**: "找到 5 个文件包含 `handleLogin` 调用: src/auth.ts, src/login.js, ..."

---

### Pattern 2: 符号定位 (< 3s)

**用户**: "查找 UserService 定义和使用"

**执行** (并行 2 个搜索):
```typescript
// 同时发起
search_content({ pattern: "class UserService", outputMode: "files_with_matches" })
search_content({ pattern: "UserService\\(", outputMode: "files_with_matches" })
```

**返回**: 
- 定义: src/services/UserService.ts
- 使用: 8 个文件

---

### Pattern 3: 玩法入口定位 (< 4s)

**用户**: "战斗系统的代码入口"

**执行** (并行 3-4 个搜索):
```typescript
search_content({ pattern: "\\b(battle|combat|fight)\\w*", fileTypes: ".py,.java,.js", outputMode: "files_with_matches", caseSensitive: false })
search_content({ pattern: "class.*Battle", outputMode: "files_with_matches" })
search_content({ pattern: "def.*battle|function.*battle", outputMode: "files_with_matches" })
```

**返回**: 
- 核心类: game/BattleManager.py, game/BattleSystem.java
- 入口函数: initBattle, startBattle, ...

---

## 3. 🛠️ CORE TECHNIQUES

### Technique 1: 并行搜索 (Parallel Search)

**原则**: 同时发起所有独立搜索,不串行等待

```
✅ 并行执行 (3x 速度)
search_content("functionA")  ─┐
search_content("functionB")  ─┼─► 并行执行
search_content("functionC")  ─┘
执行时间 = max(A, B, C) ≈ 2s

❌ 串行执行 (慢)
search_content("functionA") → wait → search_content("functionB") → wait...
执行时间 = A + B + C ≈ 6s
```

**实践**:
- 搜索函数定义和使用 → 并行
- 搜索多个相关符号 → 并行
- 不同目录的搜索 → 并行

---

### Technique 2: 精确模式匹配 (Precise Pattern)

**使用正则边界减少噪音**:

| 目标 | 模式 | 说明 |
|------|------|------|
| 函数定义 | `def functionName\(` | 匹配 Python 函数定义 |
| 函数调用 | `functionName\(` | 匹配函数调用 |
| 类定义 | `class ClassName` | 匹配类定义 |
| 变量赋值 | `varName\s*=` | 匹配变量赋值 |
| 精确单词 | `\bword\b` | 单词边界匹配 |
| 导入语句 | `import.*moduleName` | 匹配导入 |

---

### Technique 3: 智能文件类型过滤 (Auto File Type)

**自动推断策略**:

```python
# 根据仓库特征自动推断 fileTypes (< 0.1s)
if 项目有 .py 文件 → fileTypes: ".py,.pyx,.pyi"
if 项目有 .java 文件 → fileTypes: ".java"
if 项目有 .ts/.tsx 文件 → fileTypes: ".ts,.tsx,.js,.jsx"
if 项目有 .proto 文件 → 搜索协议时用 ".proto"
if 项目有 .vue 文件 → 前端搜索用 ".vue,.js,.ts"
```

**常用过滤组合**:

| 场景 | fileTypes |
|------|-----------|
| Python 项目 | `.py,.pyx,.pyi` |
| JavaScript/TS | `.js,.ts,.jsx,.tsx` |
| Java 项目 | `.java` |
| C/C++ 项目 | `.c,.cpp,.h,.hpp` |
| 配置文件 | `.json,.yaml,.yml,.toml` |
| Proto 文件 | `.proto` |
| Web 前端 | `.vue,.html,.css,.scss` |

**效果**: 
- 减少 60-90% 搜索文件
- 避免二进制/无关文件
- 无需用户指定类型

---

### Technique 4: 智能输出模式 (Smart Output Mode)

**默认策略**: 优先使用 `files_with_matches` (最快,最省 token)

| outputMode | 用途 | 速度 | Token 消耗 |
|------------|------|------|-----------|
| `files_with_matches` ⭐ | **默认**: 定位文件 | ⚡⚡⚡ 最快 | 最少 (仅文件名) |
| `count` | 统计数量 | ⚡⚡ 快 | 少 |
| `content` | 需要看匹配行 | ⚡ 慢 | 大 (完整匹配内容) |

**自动选择规则**:
```
用户说"搜索/查找/在哪" → files_with_matches
用户说"有多少/统计" → count  
用户说"显示内容/具体代码" → content
```

**两步策略**: 
```
步骤1: files_with_matches 快速定位 (< 2s)
步骤2: read_file 精读关键文件 (按需)
```

---

### Technique 5: 目录范围限定 (Directory Scoping)

**从最可能的目录开始**:

```
优先级:
1. 已知相关目录 → 直接搜索
2. 项目源码目录 (src/, lib/, app/)
3. 排除无关目录 (node_modules/, vendor/, build/)
```

**自动排除规则**:
- node_modules/ (Node.js 依赖)
- vendor/ (第三方库)
- build/, dist/ (构建产物)
- .git/ (版本控制)
- venv/, env/ (Python 虚拟环境)

---

## 4. 📋 SEARCH WORKFLOWS

### Workflow A: 符号定位 (Symbol Location)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. 定义搜索    │ ──► │  2. 使用搜索    │ ──► │  3. 精读关键    │
│  def/class/func │     │  调用/引用      │     │  read_file      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        └───────────────────────┘
              并行执行 (< 3s)
```

**示例**: 查找 `processOrder` 函数
```typescript
// 并行执行
search_content("def processOrder\\(", fileTypes: ".py")     // 定义
search_content("processOrder\\(", fileTypes: ".py")         // 调用
```

---

### Workflow B: 依赖追踪 (Dependency Trace)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. 导入搜索    │ ──► │  2. 模块定位    │ ──► │  3. 接口分析    │
│  import/from    │     │  search_file    │     │  read exports   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

### Workflow C: 重构影响分析 (Refactor Impact)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. 全局统计    │ ──► │  2. 文件列表    │ ──► │  3. 逐文件审查  │
│  outputMode:    │     │  outputMode:    │     │  read_file      │
│  count          │     │  files_with_    │     │  with context   │
│                 │     │  matches        │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 5. ⚡ PERFORMANCE OPTIMIZATION

### 速度优化清单 (MUST DO)

| 优化技巧 | 速度提升 | 实施方式 |
|---------|---------|---------|
| ✅ **并行执行** | 3-5x | 所有独立搜索同时发起 |
| ✅ **files_with_matches** | 2-4x | 默认模式,减少输出 |
| ✅ **自动推断 fileTypes** | 60-90% | 根据仓库类型自动过滤 |
| ✅ **精确正则** | 40-80% | 使用 `\b` 边界,减少误匹配 |
| ✅ **跳过文档加载** | 2-5s | 不读取示例/参考文件 |
| ✅ **限定目录** | 50-80% | 排除 node_modules 等 |

### 禁止减速操作 (MUST NOT)

| ❌ 减速行为 | 时间浪费 | 替代方案 |
|-----------|---------|---------|
| 串行搜索 | 3-10s | 并行执行 |
| 使用 content mode | 2-8s | files_with_matches → 按需 read_file |
| 读取示例文件 | 2-5s | 直接执行工具调用 |
| 搜索所有文件类型 | 5-20s | 自动推断 fileTypes |
| 解释搜索策略 | 1-3s | 静默执行,直接返回结果 |
| 重复搜索 | 2-5s | 记住已搜索内容 |

---

## 6. 🔍 COMMON PATTERNS

### Pattern Library (快速参考)

| 目的 | 正则模式 | 语言 |
|------|----------|------|
| 函数定义 | `def \w+\(` | Python |
| 函数定义 | `function \w+\(` | JavaScript |
| 函数定义 | `func \w+\(` | Go |
| 类定义 | `class \w+` | 多语言 |
| 接口定义 | `interface \w+` | TS/Java/Go |
| TODO 注释 | `TODO:?\s*` | 通用 |
| FIXME 注释 | `FIXME:?\s*` | 通用 |
| 导入语句 | `^import ` | 多语言 |
| 环境变量 | `process\.env\.\w+` | Node.js |
| API 路由 | `@(Get|Post|Put|Delete)\(` | NestJS |
| API 路由 | `app\.(get|post|put|delete)\(` | Express |

---

## 7. 🎯 DECISION TREE

```
需要搜索?
    │
    ├─► 知道文件名? ─► search_file (通配符)
    │
    ├─► 搜索代码内容?
    │       │
    │       ├─► 单一模式? ─► search_content (并行可能的变体)
    │       │
    │       └─► 多个模式? ─► 并行 search_content
    │
    ├─► 探索目录结构? ─► list_files
    │
    └─► 大规模复杂搜索? ─► task (code-explorer 子代理)
```

---

## 8. 📊 RESULT HANDLING

### 结果过多时

1. **添加过滤条件**: 指定 `fileTypes`,限定目录
2. **使用更精确的模式**: 添加边界 `\b`,使用完整签名
3. **分批处理**: 先统计 (`count`),再按文件处理

### 结果为空时

1. **检查拼写**: 确认搜索词正确
2. **放宽模式**: 移除边界限制,使用部分匹配
3. **扩大范围**: 移除 `fileTypes` 限制,搜索更多目录
4. **尝试变体**: 驼峰/下划线,大小写变体

---

## 9. 🎓 SUCCESS CRITERIA

| 指标 | 目标 | 测量方式 |
|------|------|---------|
| **响应速度** | < 3s 返回结果 | 从接收请求到返回结果 |
| **搜索精度** | 相关性 > 85% | 匹配结果中相关文件占比 |
| **并行率** | 100% 独立搜索并行 | 无串行等待 |
| **Token 效率** | 优先 files_with_matches | 减少 70% 输出 token |
| **自动优化** | 智能推断 fileTypes | 减少 60-90% 搜索范围 |

### 速度基准

| 搜索类型 | 目标时间 | 实施标准 |
|---------|---------|---------|
| 单一符号 | < 2s | 1 个搜索 + files_with_matches + 自动 fileTypes |
| 符号定位 | < 3s | 2 个并行搜索 (定义+使用) |
| 多模式搜索 | < 4s | 3-4 个并行搜索 |
| 大规模探索 | < 5s | 使用 code-explorer 子代理 |

---

## 10. ⚡ INSTANT EXECUTION CHEATSHEET

### 快速执行模板

**单符号搜索**:
```typescript
// 立即执行,无需解释
search_content({ 
  pattern: "symbolName\\(",
  fileTypes: ".推断的类型",  // 自动推断
  outputMode: "files_with_matches"  // 默认最快
})
```

**符号定位** (定义+使用):
```typescript
// 并行执行
[
  search_content({ pattern: "class|def|function SymbolName", outputMode: "files_with_matches" }),
  search_content({ pattern: "SymbolName\\(", outputMode: "files_with_matches" })
]
```

**玩法入口定位**:
```typescript
// 并行 3 个模式
[
  search_content({ pattern: "\\b关键词\\w*", caseSensitive: false, outputMode: "files_with_matches" }),
  search_content({ pattern: "class.*关键词", outputMode: "files_with_matches" }),
  search_content({ pattern: "def.*关键词|function.*关键词", outputMode: "files_with_matches" })
]
```

### 自动 fileTypes 映射

| 仓库特征 | 自动使用 fileTypes |
|---------|-------------------|
| Python 项目 | `.py,.pyx,.pyi` |
| Node.js 项目 | `.js,.ts,.jsx,.tsx` |
| Java 项目 | `.java` |
| C/C++ 项目 | `.c,.cpp,.h,.hpp` |
| Proto 项目 | `.proto` |
| Web 前端 | `.vue,.html,.js,.ts,.css` |
| Go 项目 | `.go` |

### 执行流程 (< 3s)

```
1. 识别意图 (< 0.5s)
   ↓
2. 推断 fileTypes (< 0.1s)
   ↓
3. 并行执行搜索 (1-2s)
   ↓
4. 返回结果 (< 0.5s)
```

**关键**: 跳过文档加载、策略解释、过程展示

---

## 11. 📚 TOOLS REFERENCE

### 工具速查

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `search_content` | 内容搜索 | `pattern`, `directory`, `fileTypes`, `outputMode` |
| `search_file` | 文件名搜索 | `pattern`, `target_directory`, `recursive` |
| `list_files` | 目录列举 | `target_directory`, `depth`, `limit` |
| `task` (code-explorer) | 大规模探索 | `prompt`, `subagent_name` |

### 常用 fileTypes 组合

```
Python:     .py,.pyx,.pyi
JavaScript: .js,.jsx,.mjs
TypeScript: .ts,.tsx
Java:       .java
C/C++:      .c,.cpp,.h,.hpp
Go:         .go
Rust:       .rs
Proto:      .proto
Config:     .json,.yaml,.yml,.toml,.xml
Web:        .html,.css,.scss,.vue
Shell:      .sh,.bash
```
