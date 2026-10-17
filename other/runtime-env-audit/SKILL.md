---
name: runtime-env-audit
description: 通过执行系统命令快速汇总当前宿主机的操作系统版本、内核信息及硬件配置，并以结构化表格形式呈现。
version: 1.0
evolved_from: none
evolution_type: CAPTURED
---

# runtime-env-audit

## 适用场景
- 新会话启动时，需要了解当前执行环境的限制和特性。
- 在安装依赖或编译代码前，确认系统架构（x86_64/aarch64）和资源是否充足。
- 调试与操作系统版本或内核特性相关的环境问题。

## 步骤
1. **执行信息采集**：运行组合命令获取系统核心参数。
2. **解析输出数据**：从命令返回的原始文本中提取关键字段（如 OS Name, Kernel, CPU Cores, Total Memory）。
3. **格式化输出**：将提取的信息整理为 Markdown 表格，确保直观易读。

## 工具和命令
使用 `exec` 工具执行以下命令：

```bash
# 综合查询命令
echo "---OS---" && cat /etc/os-release | grep -E "^(PRETTY_NAME|ID|VERSION_ID)="
echo "---Kernel---" && uname -mrs
echo "---CPU---" && lscpu | grep -E "^(Architecture|CPU\(s\)|Model name):"
echo "---Memory---" && free -h | grep "Mem:"
echo "---Disk---" && df -h / | tail -1
```

## 注意事项
- **权限限制**：在某些受限容器环境中，`lscpu` 或访问 `/proc` 文件系统可能会失败，应准备好 fallback 方案（如使用 `uname -a`）。
- **单位识别**：注意 `free -h` 输出的单位（Gi vs G），在记录时应保持原始单位以避免精度误解。
- **环境差异**：在 Docker 容器内运行时，显示的内核版本是宿主机的，但 CPU 和内存限制可能受到 Cgroups 的约束。

## 示例

### 输入
执行环境审计命令。

### 输出
| 维度 | 关键参数 | 详细信息 |
| :--- | :--- | :--- |
| **操作系统** | OS | Ubuntu 22.04.3 LTS |
| **内核** | Kernel | Linux 5.15.0-101-generic x86_64 |
| **处理器** | CPU | Intel(R) Xeon(R) Platinum (8 Cores) |
| **内存** | Memory | Total: 31Gi, Used: 4.2Gi, Free: 22Gi |
| **磁盘** | Root Partition | Size: 100G, Avail: 45G (48% used) |