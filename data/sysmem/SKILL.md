---
name: sysmem
description: 项目架构链条化初始化和管理技能包，用于自动化项目文档维护、架构分析和代码结构优化。当需要维护项目文档一致性、分析架构风险、检查重复代码或更新模块说明时使用此技能。
---

# Sysmem

## Overview

Sysmem提供项目架构链条化管理，通过自动化扫描、文档更新、架构分析和清理建议，确保项目文档结构的一致性和完整性。支持自动化项目初始化、模块化管理和持续架构健康监控。

## Core Capabilities

### 1. 项目扫描和结构分析
使用`scripts/scan_project.py`扫描整个项目结构：
- 自动发现所有模块目录和readme文件
- 提取模块功能摘要和文件组织结构
- 生成标准化的项目结构JSON文件
- 识别未在readme中记录的新文件

**使用场景**：
- 项目初始化时建立基线结构
- 定期检查项目结构变化
- 为其他功能提供数据基础

**执行命令**：
```bash
python3 /path/to/skill/scripts/scan_project.py /path/to/project
```

**重要**: 所有脚本都会在**目标项目的 .claude/skill/sysmem/ 目录**中生成数据文件，不会污染项目根目录或skill目录。

### 2. 智能数据收集和文档更新
使用数据收集 + Claude智能处理的组合方式：

**第一步：数据收集**
```bash
python3 /path/to/skill/scripts/collect_data.py /path/to/project
```
收集器负责：
- 扫描项目结构，提取模块信息
- 分析现有文档，识别变化
- 检测架构问题和重复代码
- 生成结构化的分析数据

**第二步：Claude智能更新**
将收集到的数据交给Claude处理：
- 基于现有CLAUDE.md内容进行增量更新，而非覆盖
- 保持用户自定义的内容和格式
- 智能判断更新内容，避免误修改
- 利用Claude的理解能力优化文档结构

**正确使用方式**：
1. 运行数据收集脚本：`python3 scripts/collect_data.py`
2. 将生成的`project_data.json`内容提供给Claude
3. 要求Claude基于数据进行智能更新：`基于project_data.json，请更新我的CLAUDE.md和各模块README，保持现有内容不变，只更新需要变化的部分`

**优势**：
- ✅ 保护用户自定义内容
- ✅ 智能增量更新，避免覆盖
- ✅ 利用Claude的理解能力
- ✅ 保持文档格式和风格一致

### 3. 架构风险分析和重复代码检测
使用`scripts/analyze_architecture.py`进行深度分析：
- 检测文件重复（同名文件、相似内容）
- 分析函数重复（Python代码的函数签名和逻辑相似度）
- 识别实现不一致（配置文件结构、API接口格式）
- 评估架构复杂度和文档完整性
- 生成详细的分析报告和改进建议

**使用场景**：
- 代码重构前的风险评估
- 定期架构健康检查
- 新模块加入的一致性验证
- 技术债务评估和优化规划

**分析标准**：参考`references/analysis_criteria.md`中的详细规则

### 4. 文件清理建议
基于项目扫描结果提供清理建议：
- 列出未在readme中记录的文件
- 标识可能是临时文件或废弃代码
- 提供模块级别的清理建议
- 支持用户决策和批量清理操作

**使用场景**：
- 项目整理和优化
- 移除不再需要的代码文件
- 保持项目结构清洁

### 5. 模块readme结构化管理
基于`references/readme_template.md`维护标准化文档：
- 第一行必须包含结构化功能描述
- 标准化的文件功能说明格式
- 重要定义的Ground Truth标记
- 代码变更历史记录

**使用场景**：
- 新模块创建时的文档初始化
- 现有模块文档的标准化改造
- 维护文档格式一致性

### 6. 双重环境支持和同步
新增的双重环境管理功能：
- **Claude Code集成**：在Claude环境中进行数据收集和初步分析
- **Codex集成**：在Codex环境中进行深度分析和代理协作
- **跨环境同步**：自动同步数据文件和文档变更
- **统一管理**：提供统一的配置和工具接口

**双重环境工作流程**：
```bash
# Claude Code环境（主环境）
python3 /path/to/skill/scripts/collect_data.py /path/to/project

# 同步到Codex环境
python3 scripts/sync-env.sh --to-codex

# Codex环境中使用代理
from agents.sync_agent import SyncAgent
agent = SyncAgent()
agent.sync_with_claude("/path/to/project")
```

**同步机制**：
- 数据文件自动同步：`.claude/skill/sysmem/` ↔ `.codex/sysmem/`
- 文档一致性检查：CLAUDE.md ↔ AGENTS.md
- 配置文件统一：双重环境共享配置
- 冲突解决策略：Claude Code优先级

## Workflow Decision Tree

### 首次使用Sysmem
```
用户请求: "初始化sysmem来管理我的项目架构"
↓
1. 执行数据收集: python3 scripts/collect_data.py
2. Claude分析收集到的project_data.json
3. 检查现有CLAUDE.md和readme文件状态
4. Claude基于数据进行智能文档更新（增量更新，不覆盖）
5. 提供架构分析和改进建议
```

### 定期维护流程
```
用户请求: "用sysmem更新项目文档"
↓
1. 执行数据收集: python3 scripts/collect_data.py
2. 将project_data.json提供给Claude
3. Claude对比分析，识别变化和需要更新的部分
4. 进行智能增量更新，保护用户自定义内容
5. 生成更新报告和建议
```

### 架构分析流程
```
用户请求: "分析payment模块的架构风险"
↓
1. 执行数据收集: python3 scripts/collect_data.py
2. Claude分析project_data.json中的架构问题
3. 检查重复代码、配置不一致等问题
4. 提供详细的风险评估和解决建议
5. 用户根据建议进行代码优化
```

## Resources

### scripts/
**collect_data.py** - 智能数据收集器，收集项目结构、文档状态和架构问题
**scan_project.py** - 基础项目扫描器，遍历项目结构并收集文件信息
**analyze_architecture.py** - 架构分析器，检测风险和重复代码

**注意**: 推荐使用 `collect_data.py` + Claude智能处理的组合方式，避免直接修改文件。

### references/
**readme_template.md** - 标准readme模板，确保文档格式一致性
**claude_md_template.md** - CLAUDE.md结构模板和示例
**analysis_criteria.md** - 架构分析标准和规则定义

### assets/
**project_structure_example.json** - 项目结构数据格式示例
