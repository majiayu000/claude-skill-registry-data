---
name: langgraph-development
description: 专业的LangGraph AI应用开发技能，提供从概念到生产的完整开发指导。基于Context7最新调研，涵盖StateGraph设计、多代理协作、RAG系统实现、生产部署等核心场景。使用此技能构建有状态、多参与者、长期运行的AI代理应用。
---

# LangGraph开发技能

本技能提供构建、管理和部署LangGraph AI应用的comprehensive指导，基于Context7对最新LangGraph生态系统的深度调研。

## 使用场景

在以下情况下使用此技能：
- 需要构建有状态的多代理AI应用
- 设计复杂的AI工作流和决策流程
- 实现RAG（检索增强生成）系统
- 构建多Agent协作系统（Supervisor、Swarm模式）
- 需要持久化执行和人机协作功能
- 从开发到生产的完整部署流程
- 性能优化和监控调试需求

## 核心概念和架构

### LangGraph核心特性
- **低级编排框架**：用于构建、管理和部署长期运行的有状态代理
- **持久化执行**：支持检查点、状态恢复、容错处理
- **综合内存管理**：短期记忆、长期记忆、上下文窗口优化
- **人机协作**：审批流程、干预机制、交互式决策
- **生产就绪部署**：企业级稳定性、可扩展性、监控能力

### 核心API组件
- **StateGraph**：状态驱动的图结构
- **MessageGraph**：消息传递图
- **CompiledGraph**：编译后的可执行图
- **CheckpointSaver**：状态持久化（支持MySQL、Redis、PostgreSQL）
- **节点类型**：LLM节点、工具节点、条件节点、自定义节点

### 开发工作流程

1. **设计阶段**
   - 使用`scripts/design_workflow.py`设计应用架构
   - 参考`references/architecture_patterns.md`选择合适的架构模式
   - 使用`assets/diagrams/`中的流程图模板进行可视化

2. **实现阶段**
   - 使用`scripts/generate_template.py`生成项目模板
   - 参考`references/api_reference.md`进行API调用
   - 遵循`references/best_practices.md`中的编码规范

3. **测试阶段**
   - 使用`scripts/test_agent.py`进行单元测试
   - 使用`langgraph-studio`进行本地调试
   - 集成LangSmith进行监控和评估

4. **部署阶段**
   - 使用`assets/templates/production_ready/`中的部署配置
   - 参考`references/deployment_guide.md`进行生产部署
   - 使用`scripts/monitor.py`进行性能监控

## 资源组件

### Scripts（可执行工具）
- `scripts/setup_environment.py`：环境配置和依赖安装
- `scripts/generate_template.py`：项目模板生成器
- `scripts/checkpoint_analyzer.py`：检查点分析和状态管理工具
- `scripts/performance_monitor.py`：性能监控和优化工具
- `scripts/test_agent.py`：代理测试和验证工具
- `scripts/deploy_helper.py`：部署辅助脚本

### References（参考资料）
- `references/architecture_patterns.md`：架构模式和设计模式参考
- `references/api_reference.md`：API速查手册和示例
- `references/best_practices.md`：最佳实践和编码规范
- `references/troubleshooting.md`：故障排查和问题解决指南
- `references/use_cases.md`：使用案例和实战项目分析
- `references/deployment_guide.md`：部署指南和生产环境配置

### Assets（资源文件）
- `assets/templates/`：完整的项目模板
  - `basic_agent/`：基础代理模板
  - `rag_system/`：RAG系统模板
  - `multi_agent/`：多代理系统模板
  - `production_ready/`：生产就绪模板
- `assets/diagrams/`：架构图和流程图
- `assets/config_files/`：配置文件模板
- `assets/example_projects/`：示例项目和演示代码

## 常见应用模式

### RAG系统实现
使用LangGraph构建增强型检索生成系统：
- 集成向量存储和文档检索
- 实现上下文管理和答案生成
- 支持多轮对话和状态保持

### 多Agent协作
实现复杂的代理协作模式：
- **Supervisor模式**：中央代理协调多个专业化代理
- **Swarm模式**：动态代理切换和控制交接
- **ReAct模式**：推理-行动循环代理

### 生产级应用
构建企业级AI应用：
- 容错处理和错误恢复
- 性能监控和日志管理
- 可扩展架构和负载均衡

## 技能使用流程

1. **需求分析**：明确应用场景和功能需求
2. **架构设计**：选择合适的架构模式和组件
3. **快速原型**：使用模板生成基础代码
4. **功能实现**：基于参考文档开发核心功能
5. **测试验证**：使用测试工具验证功能正确性
6. **性能优化**：使用监控工具优化性能
7. **生产部署**：使用部署工具进行生产环境配置

## 注意事项

- 确保Python 3.8+环境并安装必要的依赖
- 推荐使用虚拟环境进行项目隔离
- 生产环境需要考虑安全性和性能优化
- 定期更新LangGraph版本以获得最新功能
- 使用LangSmith进行生产环境的监控和调试
