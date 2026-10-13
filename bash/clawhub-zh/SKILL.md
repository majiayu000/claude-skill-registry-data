---
name: clawhub-zh
description: 使用 ClawHub CLI 从 clawhub.com 搜索、安装、更新和发布智能体技能。当您需要即时获取新技能、将已安装的技能同步到最新版本或特定版本，或发布新技能或更新技能文件夹时使用此技能。配合 npm 安装的 clawhub CLI 使用。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["clawhub"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "clawhub",
              "bins": ["clawhub"],
              "label": "安装 ClawHub CLI (npm)",
            },
          ],
      },
  }
---

# ClawHub CLI

安装

```bash
npm i -g clawhub
```

认证（发布用）

```bash
clawhub login
clawhub whoami
```

搜索

```bash
clawhub search "postgres backups"
```

安装

```bash
clawhub install my-skill
clawhub install my-skill --version 1.2.3
```

更新（基于哈希匹配 + 升级）

```bash
clawhub update my-skill
clawhub update my-skill --version 1.2.3
clawhub update --all
clawhub update my-skill --force
clawhub update --all --no-input --force
```

列表

```bash
clawhub list
```

发布

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

说明

- 默认注册表：https://clawhub.com（可通过 CLAWHUB_REGISTRY 或 --registry 覆盖）
- 默认工作目录：cwd（回退到 OpenClaw 工作区）；安装目录：./skills（可通过 --workdir / --dir / CLAWHUB_WORKDIR 覆盖）
- update 命令会对本地文件进行哈希计算，解析匹配的版本，并升级到最新版本（除非设置了 --version）
