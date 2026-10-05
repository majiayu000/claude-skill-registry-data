---
name: environment-bootstrap
description: 从源仓库向其他设备或用户级 Skill 目录恢复已登记的 Codex Skill，提供只读审计、显式应用、SHA-256 校验，并且不删除目标端额外文件。用于复现 Codex 工作环境、比较已安装 Skill 与备份仓库，或准备安全的跨设备恢复。
---

# 环境恢复

## 适用范围

只负责把仓库中的已登记 Skill 恢复到明确的用户级或设备级目的地。源仓库是权威源；仓库审计和包质量检查分别由 `skill-repository-maintainer` 与 `skill-quality-gate` 负责。

## 工作流程

1. 确认源仓库存在 `skills.json` 和已登记包。
2. 运行源端严格校验：

   ```bash
   python3 scripts/validate_repo.py --strict
   ```

3. 明确目的地。Windows 常见路径是 `C:\Users\<user>\.codex\skills`，不得猜测其他用户的目录。
4. 先做只读差异检查：

   ```bash
   python3 scripts/sync_skills.py --destination "<destination>" --profile core --check
   ```

5. 用户明确要求恢复时，选择 `--profile core`、`--profile full` 或窄范围 `--skill`，运行 `--apply`，再对同一个目的地运行 `--check`。

## 安全边界

- 永不通过恢复删除目的地额外文件；旧的未登记 Skill 应单独审查。
- 不隐式安装插件、MCP、包、hooks 或全局配置。
- 不用旧目的地文件、stdout 或 apply exit code 单独报告成功。
- 源端校验失败时停止恢复并保留原始错误。
- 回滚应从已知稳定提交或备份重新复制，不使用递归删除。

## 输出契约

报告源端、目的地、模式（`check` 或 `apply`）、profile/包数量、missing/different/extra、SHA-256 结果和剩余风险。只有 post-apply 检查干净时才报告 `PASS`；有明确的非阻塞目的地差异时报告 `PARTIAL`。

## 验证

成功恢复的最低证据：

```text
strict source validation: PASS
apply: completed
post-apply hash check: PASS
destination-only files: preserved and reported
```

跨设备清单见 [restore-profile.md](references/restore-profile.md)。
