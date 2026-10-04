---
name: mac-software-storage-cleanup-cn
description: 当用户需要审计 macOS 软件占用、清理优先缓存或获取可回收空间建议时使用。
---

# Mac Software Storage Cleanup

## Overview

审计 macOS 软件安装与磁盘占用，输出可执行的分级清理建议，并在用户确认后执行低风险清理。流程会区分应用清单、缓存、模拟器数据和中风险应用数据，避免在没有确认的情况下删除业务数据。

## 何时使用

当用户有以下需求时使用本技能：
- 检查 `/Applications`、`~/Applications`、Homebrew Formula、Homebrew Cask 安装了哪些软件
- 统计软件和常见缓存目录的空间占用，并按大小排序
- 清理 `~/Library/Caches`、`~/Library/Developer/CoreSimulator` 等低风险目录
- 给出磁盘空间治理建议，并区分低风险与中风险清理项

## 不要使用

以下场景不应使用本技能：
- 用户想卸载某个具体应用，而不是做磁盘治理盘点
- 用户要求直接删除业务数据目录，但没有明确确认
- 任务环境不是 macOS，或目标路径不适用当前系统

## 使用说明

1. 先执行 `scripts/report_sizes.sh`，盘点软件来源与主要占用目录。
2. 基于报告区分清理优先级：
   - 优先级 1：缓存和模拟器数据，默认低风险。
   - 优先级 2：应用业务数据目录，仅列出候选，不直接删除。
   - 优先级 3：收益较低的小型缓存或日志。
3. 输出结论时，必须展示目录类别、数量、总占用和 Top N 大户。
4. 如需扫描优先级 2 候选，执行 `scripts/list_priority2_candidates.sh [目标目录] [TopN]`。
5. 只有在用户明确确认后，才执行 `scripts/cleanup_priority1.sh` 或等价清理动作。
6. 清理完成后，重新核算并输出“清理前 -> 清理后 -> 释放空间”的对比结果。

## 标准流程

```text
盘点安装来源与空间占用
  -> 识别高价值可清理目录
  -> 给出分级建议
  -> 等待用户确认
  -> 执行低风险清理
  -> 复核释放结果
```

## 执行命令

```bash
bash scripts/report_sizes.sh
bash scripts/list_priority2_candidates.sh ~/Library/Application\\ Support 20
bash scripts/cleanup_priority1.sh
```

## 输出要求

- 明确展示每类路径的数量和总占用
- 列出 Top N 大户，便于用户快速决策
- 任何清理动作都必须包含清理前后对比
- 没有用户确认时，不主动删除优先级 2 目录

## 边界

- 不使用破坏性 git 命令
- 不删除用户未确认的应用业务数据
- 若脚本失败，改用更稳妥的只读排查或最小范围清理方式
