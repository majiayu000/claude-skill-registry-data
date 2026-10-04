---
name: ielts-buddy-skills-updater
description: 说明如何从固定 IELTS Buddy OSS 发行源检查并更新本机已安装的用户端 Skills；不规定何时更新或更新后的使用方式。
---

# IELTS Buddy Skills 更新接口

本 Skill 只说明本机发行更新命令和写入边界，不参与学习、分析或推荐。

## 命令

```sh
python3 scripts/update_skills.py check
python3 scripts/update_skills.py update
```

- `check` 只读取本机版本和发行清单。
- `update` 下载固定 OSS 发行包，并校验项目、版本、commit、文件大小、SHA-256、ZIP 路径和 Skills 清单后替换受管理文件。
- 固定发行地址由脚本内置；不接受聊天中临时提供的替换源。

## 边界

- 只有用户明确要求更新时才调用 `update`。
- 目标为 Git 仓库时停止，交给 GitHub 发布流程。
- 下载、校验、解压或替换失败时保留原版本。
- `workflows/` 是独立的可选推荐层，不属于本 Skill 的接口契约。
