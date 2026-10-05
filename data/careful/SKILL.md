---
name: careful
version: 0.1.0
description: |
  面向破坏性命令的安全护栏。在执行 rm -rf、DROP TABLE、force-push、
  git reset --hard、kubectl delete 等操作前先给出警告。用户可逐次覆盖。
  适用于生产环境、在线调试或共享环境。 (gstack)
allowed-tools:
  - Bash
  - Read
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/bin/check-careful.sh"
          statusMessage: "Checking for destructive commands..."
---
<!-- 中文参考译文。 -->

# /careful

启用后，所有 Bash 命令都会先经过破坏性操作检查。命中高风险模式时，先警告，再由用户决定是否继续。

## 保护范围

- 递归删除：`rm -rf`、`rm -r`、`rm --recursive`
- 高风险 SQL：`DROP TABLE`、`DROP DATABASE`、`TRUNCATE`
- 改写历史：`git push --force`、`git reset --hard`
- 丢失工作区：`git checkout .`、`git restore .`
- 生产级删除：`kubectl delete`、`docker rm -f`、`docker system prune`

## 白名单例外

以下常见构建产物清理默认允许，不弹警告：

- `node_modules`
- `.next`
- `dist`
- `__pycache__`
- `.cache`
- `build`
- `.turbo`
- `coverage`

## 工作方式

- hook 从 Bash 工具输入里读命令。
- 一旦匹配危险模式，就返回 `permissionDecision: "ask"`。
- 用户可以覆盖继续，也可以取消。
- 该模式是会话级的，换新会话即可关闭。
