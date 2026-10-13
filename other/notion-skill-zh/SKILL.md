---
name: notion
description: 通过官方 Notion API 操作 Notion 页面和数据库。
homepage: https://developers.notion.com
metadata:
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - NOTION_API_KEY
    install:
      - id: node
        kind: note
        label: "需要 notion-cli (Node.js) 或 notion-cli-py (Python)。详见下方文档。"
---

# Notion

此技能让智能体能够使用官方 Notion API 操作 **Notion 页面和数据库**。

这是一个声明式技能：它记录了**安全、推荐的操作**，并假设有一个本地 CLI（`notion-cli`）实际执行 API 调用。

## 身份验证

- 在 https://www.notion.so/my-integrations 创建 Notion 集成
- 复制内部集成令牌（Internal Integration Token）
- 将其导出为环境变量：

```bash
export NOTION_API_KEY=secret_xxx
```

将集成与您想访问的页面或数据库共享。
未共享的内容对 API 不可见。

## 配置文件（个人/工作）

您可以通过环境变量或配置定义多个配置文件（例如：personal、work）。

默认配置文件：personal

通过以下方式覆盖：

```bash
export NOTION_PROFILE=work
```

## 页面操作

**读取页面：**

```bash
notion-cli page get <page_id>
```

**追加内容块：**

```bash
notion-cli block append <page_id> --markdown "..."
```

优先使用追加而非重写内容。

**创建页面：**

```bash
notion-cli page create --parent <page_id> --title "..."
```

## 数据库操作

**检查架构：**

```bash
notion-cli db get <database_id>
```

**查询数据库：**

```bash
notion-cli db query <database_id> --filter <json> --sort <json>
```

**创建行：**

```bash
notion-cli page create --database <database_id> --props <json>
```

**更新行：**

```bash
notion-cli page update <page_id> --props <json>
```

## 架构变更（高级）

在应用架构变更前，始终先检查差异。

未经明确确认，切勿修改数据库架构。

推荐流程：

```bash
notion-cli db schema diff <database_id> --desired <json>
notion-cli db schema apply <database_id> --desired <json>
```

## 安全注意事项

- Notion API 有速率限制；请谨慎批量操作
- 优先使用追加和更新操作，避免破坏性操作
- ID 是不透明的；请明确存储，不要从 URL 推断
