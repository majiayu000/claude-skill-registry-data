---
name: diagram-creator
description: Create technical diagrams using diagramming languages like Mermaid, PlantUML, GraphViz, and others. Use when users request diagrams, flowcharts, sequence diagrams, architecture diagrams, ER diagrams, Gantt charts, mind maps, or any visual representation of systems, processes, or data structures. Trigger examples:"画一个系统架构图"、"创建一个流程图"、"生成一个时序图"、"帮我做个甘特图"。
---

# Diagram Creator

## Quick Start

Use **Mermaid** as the default choice - it's versatile, well-supported, and handles most diagram types:

```mermaid
graph LR
    A[开始] --> B{判断}
    B -->|是| C[执行]
    B -->|否| D[结束]
```

## Tool Selection Guide

**Default:** Use Mermaid for most cases (flowcharts, sequence diagrams, Gantt charts, ER diagrams)

**Alternative tools for specific needs:**
- **Complex UML/C4:** PlantUML
- **Network/Architecture:** GraphViz (DOT)
- **ASCII art style:** Ditaa
- **Timeline/Waveforms:** WaveDrom
- **Full list:** See [TOOLS.md](TOOLS.md)

## Recommended Colors

Apply these colors for professional, consistent diagrams:

| 用途 | 颜色 | HEX | 场景 |
| :--- | :--- | :--- | :--- |
| **主色** | 深海蓝 | `#0052CC` | 核心系统、主要服务 |
| **辅色** | 天空蓝 | `#4C9AFF` | 子系统、API 网关 |
| **中性** | 浅灰 | `#EBECF0` | 背景、分组、边界 |
| **强调** | 活力橙 | `#FF991F` | 重点模块、第三方依赖 |
| **线条** | 深炭灰 | `#172B4D` | 连接线、文字、边框 |

## Example

```mermaid
graph TD
    %% 定义样式
    classDef core fill:#0052CC,stroke:#172B4D,stroke-width:2px,color:#fff;
    classDef sub fill:#4C9AFF,stroke:#172B4D,stroke-width:1px,color:#fff;
    classDef container fill:#EBECF0,stroke:#172B4D,stroke-width:1px,stroke-dasharray: 5 5,color:#172B4D;
    classDef warn fill:#FF991F,stroke:#172B4D,stroke-width:2px,color:#fff;

    %% 图表内容
    subgraph VPC [云私有网络 VPC]
        LB(负载均衡 LB):::sub
        
        subgraph AppLayer [应用层 Group]
            API(API 网关):::sub --> Auth(认证服务):::core
            Auth --> Core(核心业务系统):::core
        end
        
        subgraph DataLayer [数据层 Group]
            DB[(主数据库)]:::core
            Redis(缓存 Redis):::warn
        end
    end
    
    User((用户)) --> LB
    LB --> API
    Core --> DB
    Core -.-> Redis

    %% 应用样式
    class VPC,AppLayer,DataLayer container;
```

## Workflow

1. Understand the diagram requirements and type needed
2. Select appropriate tool (default: Mermaid)
3. Design structure and layout
4. Apply recommended colors for visual clarity
5. Generate clean diagram code
6. Validate syntax and readability

Output only the diagram code - no XML tags, no extra explanations.
