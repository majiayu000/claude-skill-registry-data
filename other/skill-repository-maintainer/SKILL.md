---
name: skill-repository-maintainer
description: 审计、验证并安全同步 Codex Skill 仓库：检查包结构、manifest 和元数据，识别私有或运行时文件，审查目录组织，并将已登记的包显式同步到其他设备。用于维护 Skill 备份仓库、检查 Skill 是否完整、准备发布，或比较源仓库与已安装 Skill 目录。
---

# Skill 仓库维护

## 适用范围

把本仓库当作 Skill 源仓库，负责注册表、包边界、结构校验、发布前审计和目的地差异检查。本 Skill 不负责修改 Skill 的行为质量；行为质量交给 `skill-quality-gate`。

## 工作流程

1. 确认仓库根目录和目的地；没有明确目的地时不要猜测写入路径。
2. 清点 `skills.json`、根目录注册包、`SKILL.md`、`agents/openai.yaml`、examples、references、scripts、assets 和被忽略的运行时状态。
3. 运行严格校验：

   ```bash
   python3 scripts/validate_repo.py --strict
   ```

4. 审查差异和发布边界，隔离私有记忆、缓存、依赖树、机器路径、临时文件和生成报告。
5. 对目标设备做只读检查：

   ```bash
   python3 scripts/sync_skills.py --destination "<destination>" --profile core --check
   ```

6. 只有用户明确要求同步时才使用 `--apply`，应用后立即再次 `--check`。永远不通过同步脚本删除目的地额外文件。

仓库已有 validator 时优先使用它；包内 `scripts/audit.py` 仅作为独立安装或外部仓库没有 validator 时的便携 fallback。

## 架构边界

- `skills.json` 是注册表，根目录注册包是发布源。
- `tier` 和 `profiles` 只描述安装集合，不授权自动安装或执行。
- `skill-quality-gate` 负责触发、流程、输出和行为质量；本 Skill 负责结构、边界和同步。
- 运行时状态可以被审计，但不能进入已发布包。

## 输出契约

报告 `PASS`、`PARTIAL` 或 `BLOCKED`，并包含仓库路径、目的地、命令、包数量、missing/different/extra、哈希结果、改动文件、残余风险和是否只读。

不要把旧目的地文件、旧 stdout 或单次 apply 当作同步成功证据；只有 post-apply 检查通过才可报告同步完成。

## 验证

最低验证集：严格仓库校验、相关 Skill smoke test、质量门禁和目标设备只读差异检查。应用操作必须保留目的地额外文件并完成第二次检查。
