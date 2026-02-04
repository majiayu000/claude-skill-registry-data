---
name: novel-generator
description: 智能小说生成器v2.0，支持长篇小说的断点续传、智能上下文管理、三层压缩机制、章节跳转、智能导入设定、AI辅助编辑和记忆管理。当用户需要创作长篇小说、管理复杂故事结构、从外部资源导入设定、或需要AI辅助进行持续性的创意写作时使用此技能。
---

# 小说生成器技能 v2.0

## 技能概述

这是一个专业的长篇小说AI创作辅助技能，具备完整的断点续传、智能上下文管理、分层压缩存储、智能导入和AI辅助编辑功能。

## 核心功能

### 1. 双模式操作系统
- **设定模式**: 引导式创建世界观、人物、环境、情节、风格、记忆设定
- **写作模式**: 基于设定进行持续创作，支持章节跳转和断点续传
- **导入模式**: 从外部目录智能导入设定和内容

### 2. 智能上下文管理
- 128k token上下文窗口，可配置
- 三层压缩策略：近期(2k)、中期(500token)、长期(100token)
- 记忆压缩独立处理，不占用主上下文

### 3. 项目结构管理
- 每个项目独立文件夹结构
- 章节独立存储，每章包含三层压缩数据
- 设定区、写作区、成品区三区分离

### 4. 智能导入功能 🔥 NEW
- **智能扫描**: 递归扫描指定目录下的所有文本文件
- **内容识别**: AI辅助识别和分类设定内容（人物、世界观、环境等）
- **智能合并**: 支持覆盖、追加、局部修改三种更新模式
- **批量导入**: 支持指定设定类型的定向导入

### 5. 增强编辑功能 🔥 NEW
- **智能章节编辑**: 支持本地和AI辅助的内容编辑
- **上下文感知**: 维护章节间的一致性和连贯性
- **多种编辑模式**: 替换、追加、前置、插入
- **AI集成**: 预留标准AI任务接口

### 6. 记忆管理系统 🔥 NEW
- **记忆片段管理**: 逐条插入和管理角色记忆
- **多维度显示**: 支持按类型、时间线、关联网络等展示
- **情感权重**: 支持记忆的重要性和情感强度标记
- **记忆压缩**: 智能压缩和长期记忆管理

## 使用指南

### 首次使用
1. 启动技能进入设定模式
2. 完成世界观、人物、环境、情节、风格设定
3. 可选添加记忆设定
4. 切换到写作模式开始创作

### 断点续传
- 技能自动保存会话状态
- 重新启动时恢复上次的工作状态
- 支持章节跳转和上下文重建

### 压缩管理
- 每10章自动触发压缩
- 失败时报告用户，支持手动重试
- 三层压缩结果独立存储

## 技能资源使用

### Scripts 使用方法

### 核心管理脚本

#### session_manager.py
会话管理和断点续传的核心脚本：
```bash
python scripts/session_manager.py --action save|load|resume --session-id <session_id>
```

#### mode_handler.py
模式切换脚本：
```bash
python scripts/mode_handler.py --mode setting|writing|import --project-path <path>
```

#### context_manager.py
上下文管理脚本：
```bash
python scripts/context_manager.py --action build|clean --chapter <N> --token-limit <128k>
```

#### compression_engine.py
压缩处理脚本：
```bash
python scripts/compression_engine.py --action compress|recompress --chapters <range>
```

### 🔥 新增功能脚本

#### unified_api.py 🔥 NEW
统一API接口，整合所有功能：
```bash
# 系统状态查看
python scripts/unified_api.py --request-json '{"action": "system.status"}'

# 导入设定（需要AI处理）
python scripts/unified_api.py --request-json '{
  "action": "import.from_directory",
  "target_directory": "./source_materials"
}'

# 显示设定
python scripts/unified_api.py --request-json '{
  "action": "display.setting",
  "setting_type": "worldview",
  "format_type": "readable"
}'

# 智能章节编辑
python scripts/unified_api.py --request-json '{
  "action": "chapter.intelligent_edit",
  "chapter_number": 1,
  "edit_request": {
    "content": "新内容...",
    "edit_mode": "append",
    "requires_ai": false
  }
}'
```

#### import_manager.py 🔥 ENHANCED
增强的导入管理器，支持智能扫描和AI分析：
```bash
# 扫描目录内容
python scripts/import_manager.py --action scan-directory --target-directory ./source_materials

# 从目录导入（返回AI任务）
python scripts/import_manager.py --action import-from-directory --target-directory ./source_materials

# 处理AI分析结果
python scripts/import_manager.py --action process-ai-result --project-path . [需要AI结果输入]
```

#### chapter_manager.py 🔥 ENHANCED
增强的章节管理器，支持智能编辑：
```bash
# 创建章节
python scripts/chapter_manager.py --action create --chapter 1 --title "第一章"

# 智能编辑（本地）
python scripts/chapter_manager.py --action intelligent-edit --chapter 1 --content "新内容" --edit-mode append

# 智能编辑（AI）
python scripts/chapter_manager.py --action intelligent-edit --chapter 1 --requires-ai --edit-instructions "请改进这段文字"

# 上下文更新
python scripts/chapter_manager.py --action context-update --chapter 1 --content "章节重点内容"
```

#### settings_display_manager.py 🔥 NEW
设定显示管理器：
```bash
# 显示世界观设定
python scripts/settings_display_manager.py --type worldview --format readable

# 显示特定角色
python scripts/settings_display_manager.py --type character --name "张三" --format json

# 显示记忆统计
python scripts/settings_display_manager.py --action list
```

#### memory_display_manager.py 🔥 NEW
记忆显示管理器：
```bash
# 显示角色所有记忆
python scripts/memory_display_manager.py --identifier "张三" --type character_all

# 显示记忆时间线
python scripts/memory_display_manager.py --identifier "张三" --type timeline

# 显示记忆统计
python scripts/memory_display_manager.py --action stats --identifier "张三"
```

### References 使用时机

#### data_schemas.md
在实现数据结构和验证时参考，包含所有数据模型的详细定义。

#### compression_rules.md
压缩触发时参考，定义三层压缩的具体规则和算法。

#### context_strategies.md
上下文管理策略参考，在不同章节位置时如何组装上下文。

### Assets 使用方法

#### templates/
包含项目模板、章节模板、设定模板，在创建新项目时使用。

#### examples/
包含优秀示例和演示数据，在用户需要参考时使用。

## 工作流程

### 设定模式流程
1. 检查现有项目状态
2. 引导用户完成六大设定
3. 验证设定完整性
4. 保存设定到settings/目录
5. 准备进入写作模式

### 写作模式流程
1. 加载项目设定和章节状态
2. 构建当前上下文窗口
3. 生成章节内容
4. 检查压缩触发条件
5. 更新进度和会话状态

### 章节跳转流程
1. 保存当前工作状态
2. 清理现有上下文
3. 加载目标章节及其前序章节
4. 重建压缩上下文
5. 恢复写作状态

## 错误处理

- 压缩失败时记录详细日志并提示用户
- 上下文超限时智能降级处理
- 文件损坏时支持备份恢复
- 网络中断时本地缓存保护

## AI集成工作流程 🔥 NEW

### AI任务处理流程
系统采用"本地处理+AI客户端"架构，当需要AI能力时会返回标准化的AI任务请求：

```python
# 示例：处理导入请求
result = api.process_request({
    "action": "import.from_directory",
    "target_directory": "./source_materials"
})

if result["status"] == "ai_task_required":
    # 获取AI任务
    ai_task = result["ai_task"]

    # 调用AI服务处理
    ai_result = your_ai_client.process_task(ai_task)

    # 应用AI结果
    final_result = api.process_request({
        "action": "import.process_ai_result",
        "ai_result": ai_result
    })
```

### 支持的AI任务类型
1. **content_analysis**: 分析文件内容并提取设定
2. **content_edit**: 智能编辑和改进内容
3. **generate_summary**: 生成内容摘要
4. **memory_analysis**: 分析记忆内容和关联

### AI任务请求格式
```json
{
  "status": "ai_task_required",
  "ai_task": {
    "task_type": "content_analysis",
    "files": [...],
    "analysis_instructions": "请识别世界观、人物、环境等设定",
    "supported_settings": ["worldview", "character", "environment"]
  }
}
```

## 性能优化

- 增量压缩减少重复计算
- 智能缓存机制提升响应速度
- 异步处理避免用户等待
- 分层存储优化内存使用
- AI任务队列管理，避免重复请求