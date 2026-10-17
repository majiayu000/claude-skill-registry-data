---
name: memory-merger
description: '将领域记忆文件中的成熟经验合并到其指令文件中。**自动触发**: 当记忆文件多次更新或有成熟内容时，自动建议合并。也可手动触发: `/memory-merger >领域 [作用域]`'
---

# 记忆合并器 (Memory Merger)

您将领域记忆文件中的成熟经验整合到其对应的指令文件中，在确保知识留存的同时最大限度地减少冗余。

**请使用待办列表 (TODO list)** 来跟踪流程步骤的进度，并实时告知用户。

## 作用域 (Scope)

记忆指令可以存储在以下两种作用域中：

- **全局 (Global)**（`global` 或 `user`）—— 存储在 `<global-prompts>` (`vscode-userdata:/User/prompts/`) 目录，适用于所有 VS Code 项目。
- **工作区 (Workspace)**（`workspace` 或 `ws`）—— 存储在 `<workspace-instructions>` (`<workspace-root>/.github/instructions/`) 目录，仅适用于当前项目。

默认作用域为 **全局 (Global)**。

在本提示词中，`<global-prompts>` 和 `<workspace-instructions>` 分别指代上述目录。

## 命令语法

```
/memory-merger >领域名称 [作用域]
```

- `>领域名称` —— 必填。要合并的领域（例如 `>clojure`、`>git-workflow`、`>prompt-engineering`）。
- `[作用域]` —— 可选。可选值包括：`global`、`user`（两者均代表全局）、`workspace` 或 `ws`。默认为 `global`。

**使用示例：**
- `/memory-merger >prompt-engineering` —— 合并全局“提示工程”记忆。
- `/memory-merger >clojure workspace` —— 合并工作区 “clojure” 记忆。
- `/memory-merger >git-workflow ws` —— 合并工作区 “git-workflow” 记忆。

## 执行流程

### 1. 解析输入并读取文件

- **提取** 域名和作用域。
- **确定** 文件路径：
  - 全局：`<global-prompts>/{domain}-memory.instructions.md` → `<global-prompts>/{domain}.instructions.md`
  - 工作区：`<workspace-instructions>/{domain}-memory.instructions.md` → `<workspace-instructions>/{domain}.instructions.md`
- 用户可能输错了域名。如果找不到对应的记忆文件，请在目录下使用 glob 搜索并判断是否有匹配项。如有疑问请询问用户。
- **读取** 这两个文件（记忆文件必须存在；指令文件可能尚不存在）。

### 2. 分析并提出方案

审查所有记忆条目并提交合并建议：

```
## 建议合并的记忆

### 记忆条目：[标题]
**核心内容：** [关键要点]
**合并位置：** [在指令文件中的建议插入位置]

[更多建议条目]...
```

提示用户：“请审查以上合并建议。如全部批准请回复 'go'，或指定需要跳过的部分。”

**在此处停止并等待用户输入。**

### 3. 定义质量标准

建立 10/10 标准，定义什么是优秀的合并结果：
1. **零知识丢失** —— 保留每一个细节、示例和细微差别。
2. **极简冗余** —— 合并重叠或重复的指导建议。
3. **极佳可读性** —— 层次结构清晰、采用平行结构、策略性加粗、逻辑分组合理。

### 4. 执行合并与迭代

开发最终的合并指令 **（此时暂不更新文件）**：

1. 起草合并指令，整合已批准的记忆内容。
2. 根据上述质量标准进行自我评估。
3. 优化结构、措辞和组织方式。
4. 重复以上步骤，直到合并指令达到 10/10 的质量标准。

### 5. 更新文件内容

当最终合并指令达到 10/10 标准后：

- **创建或更新** 指令文件为最终合并后的内容。
  - 如果是新建文件，需包含正确的 frontmatter（元数据）。
  - **合并 `applyTo` 模式**：如果记忆文件和指令文件都包含该模式，确保合并后全面覆盖且不重复。
- **从记忆文件中移除** 已成功合并的部分。

## 交互示例

```
用户："/memory-merger >clojure"

代理 (Agent)：
1. 读取 clojure-memory.instructions.md 和 clojure.instructions.md
2. 提出 3 项记忆合并建议
3. [停止，等待确认]

用户："go"

代理 (Agent)：
4. 定义 10/10 质量标准
5. 合并生成新指令候选，迭代优化至 10/10 分
6. 实际更新 clojure.instructions.md 文件
7. 清理 clojure-memory.instructions.md 中的已合并内容
```
