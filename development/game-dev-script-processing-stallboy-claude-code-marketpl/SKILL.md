---
name: game-dev-script-processing
description: 游戏开发剧本处理技能 - 指导Claude Code使用游戏开发剧本处理器插件将剧本文件转换为游戏配置文件
version: 1.0.0
---

# 游戏开发剧本处理技能

## 概述

本技能指导Claude Code使用游戏开发剧本处理器插件，将剧本文件转换为游戏配置文件。

## 核心功能

### 剧本到配置转换
- 读取剧本目录中的剧本文件
- 应用转换规则生成游戏配置文件
- 支持大型剧本文件的分块处理
- 验证生成配置的正确性

### 支持的配置文件类型
- video.cfg - 视频配置
- story.cfg - 故事配置
- prop.cfg - 道具配置
- role.cfg - 角色配置
- qte.cfg - QTE配置
- sceneexplore.cfg - 场景探索配置

## 使用方式

### 基本命令
```bash
/script-to-config --script-dir Doc/剧本_md_dir
```

### 完整参数
```bash
/script-to-config --script-dir Doc/剧本_md_dir --output-dir Main/AIWork --resume
```

## 最佳实践

1. **剧本格式**: 确保剧本文件格式统一
2. **分块策略**: 大型剧本使用分块处理
3. **验证检查**: 生成配置后进行完整性验证
4. **版本控制**: 保持配置文件的版本一致性

## 故障排除

### 常见问题
- 剧本格式不兼容
- 配置生成失败
- 内存使用过高

### 解决方案
- 检查剧本文件格式
- 调整分块大小
- 清理临时文件