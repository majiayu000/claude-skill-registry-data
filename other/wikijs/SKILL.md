---
name: wikijs
description: |
  Wiki.js 文档中心管理助手。通过 GraphQL API 管理公司 AI 应用文档中心。
  支持项目文档的自动维护、读取、搜索和组织。每个项目拥有独立的文档空间（基于路径前缀）。

  使用场景：
  - 创建/更新/删除项目文档
  - 搜索和读取文档内容
  - 同步代码库文档（README、CHANGELOG等）到 Wiki.js
  - 管理项目文档结构和导航
  - 查看文档修改历史

  触发关键词：wiki、文档中心、项目文档、wikijs、文档同步
---

# Wiki.js 文档中心管理助手

## 概述

Wiki.js 是公司的 AI 应用文档中心，基于 GraphQL API 进行文档管理。每个项目在 Wiki.js 中拥有独立的文档空间，通过路径前缀区分（如 `/projects/wuji-stat/`）。

## 环境配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| Wiki.js URL | `http://localhost:3000` | 本地开发环境 |
| GraphQL 端点 | `http://localhost:3000/graphql` | API 入口 |
| 认证方式 | Bearer Token | 需要 API Key |

### 获取 API Token

1. 登录 Wiki.js 管理后台
2. 进入 **管理区域** → **API Access**
3. 点击 **New API Key** 创建新密钥
4. 复制生成的 Token

Token 存储位置：`~/.claude/skills/wikijs/.env`
```
WIKIJS_URL=http://localhost:3000
WIKIJS_TOKEN=your_api_token_here
```

## 项目文档空间规范

### 路径结构
```
/projects/{project-name}/           # 项目根目录
├── index                           # 项目首页（必须）
├── getting-started                 # 快速开始
├── architecture                    # 架构说明
├── api/                            # API 文档目录
│   ├── index                       # API 概览
│   └── {endpoint-name}             # 各端点文档
├── guides/                         # 使用指南目录
│   └── {guide-name}                # 各指南文档
└── changelog                       # 更新日志
```

### 命名规范
- 路径使用小写字母和连字符：`my-project-name`
- 页面路径不含扩展名：`/projects/my-project/api/users`
- 项目名与代码仓库名保持一致

## GraphQL API 操作

### 认证请求格式
```bash
curl -X POST http://localhost:3000/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query": "YOUR_GRAPHQL_QUERY"}'
```

### 核心操作

#### 1. 列出所有页面
```graphql
query {
  pages {
    list(orderBy: PATH) {
      id
      path
      title
      description
      updatedAt
    }
  }
}
```

#### 2. 获取页面内容
```graphql
query {
  pages {
    single(id: PAGE_ID) {
      id
      path
      title
      description
      content
      contentType
      createdAt
      updatedAt
    }
  }
}
```

#### 3. 搜索页面
```graphql
query {
  pages {
    search(query: "搜索关键词") {
      results {
        id
        title
        description
        path
      }
      totalHits
    }
  }
}
```

#### 4. 创建页面（Markdown）
```graphql
mutation {
  pages {
    create(
      title: "页面标题"
      description: "页面描述"
      content: "# 标题\n\n页面内容..."
      editor: "markdown"
      isPublished: true
      isPrivate: false
      locale: "zh"
      path: "projects/my-project/page-name"
      tags: ["project-name", "category"]
    ) {
      responseResult {
        succeeded
        errorCode
        message
      }
      page {
        id
        path
        title
      }
    }
  }
}
```

#### 5. 更新页面
```graphql
mutation {
  pages {
    update(
      id: PAGE_ID
      title: "新标题"
      description: "新描述"
      content: "# 新内容\n\n更新后的内容..."
      tags: ["tag1", "tag2"]
    ) {
      responseResult {
        succeeded
        errorCode
        message
      }
      page {
        id
        path
        updatedAt
      }
    }
  }
}
```

#### 6. 删除页面
```graphql
mutation {
  pages {
    delete(id: PAGE_ID) {
      responseResult {
        succeeded
        errorCode
        message
      }
    }
  }
}
```

#### 7. 渲染页面（更新后刷新）
```graphql
mutation {
  pages {
    render(id: PAGE_ID) {
      responseResult {
        succeeded
        errorCode
        message
      }
    }
  }
}
```

## 使用 Python 脚本操作

Wiki.js 操作脚本位于 `scripts/wikijs_api.py`，提供便捷的命令行接口。

### 基本用法
```bash
# 列出项目文档
python scripts/wikijs_api.py list --project wuji-stat

# 获取页面内容
python scripts/wikijs_api.py get --id 123

# 搜索文档
python scripts/wikijs_api.py search --query "API"

# 创建文档
python scripts/wikijs_api.py create \
  --project wuji-stat \
  --path getting-started \
  --title "快速开始" \
  --content "# 快速开始\n\n..."

# 更新文档
python scripts/wikijs_api.py update \
  --id 123 \
  --content "# 更新内容\n\n..."

# 删除文档
python scripts/wikijs_api.py delete --id 123

# 同步 README
python scripts/wikijs_api.py sync-readme \
  --project wuji-stat \
  --file /path/to/README.md
```

## 文档同步工作流

### 从代码库同步文档

1. **识别需同步的文件**
   - `README.md` → `/projects/{project}/index`
   - `CHANGELOG.md` → `/projects/{project}/changelog`
   - `docs/*.md` → `/projects/{project}/guides/*`

2. **同步命令**
```bash
# 同步单个文件
python scripts/wikijs_api.py sync-file \
  --project wuji-stat \
  --source /path/to/README.md \
  --target index

# 同步整个 docs 目录
python scripts/wikijs_api.py sync-dir \
  --project wuji-stat \
  --source /path/to/docs \
  --target guides
```

3. **自动同步（Git Hook）**
   - 可配置 post-commit hook 自动同步文档变更

## 编辑器类型

| 编辑器 | 说明 | 使用场景 |
|--------|------|----------|
| `markdown` | Markdown 编辑器 | **推荐**，适合大多数文档 |
| `code` | HTML 代码编辑器 | 需要自定义 HTML |
| `ckeditor` | 富文本编辑器 | 非技术用户 |
| `asciidoc` | AsciiDoc 编辑器 | 复杂技术文档 |

## 标签规范

每个文档应包含以下标签：
- 项目名：`project:{project-name}`
- 文档类型：`type:guide` / `type:api` / `type:reference`
- 状态：`status:draft` / `status:published`

## 数据库直连（备用）

当 API 不可用时，可直接操作数据库：

```bash
# 连接数据库
docker exec -it wikijs-db psql -U wikijs -d wiki

# 查询页面
SELECT id, path, title FROM pages WHERE path LIKE 'projects/wuji-stat/%';

# 获取页面内容
SELECT content FROM pages WHERE id = 123;
```

**注意**：直接操作数据库后需通过 API 调用 `render` mutation 刷新渲染缓存。

## 常见问题

### Markdown 渲染问题
创建页面时必须设置 `editor: "markdown"`，否则内容会显示为纯文本。

### 页面更新后显示旧内容
调用 `render` mutation 刷新页面渲染缓存。

### 路径冲突
Wiki.js 使用虚拟目录，同一路径不能同时存在文件和文件夹入口。建议每个目录都创建 `index` 页面作为目录入口。

## 参考文档

- [GraphQL API 完整参考](references/api.md)
- [Wiki.js 官方文档](https://docs.requarks.io/)
