---
name: trello-zh
description: 通过 Trello REST API 管理 Trello 看板、列表和卡片。
homepage: https://developer.atlassian.com/cloud/trello/rest/
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["jq"],"env":["TRELLO_API_KEY","TRELLO_TOKEN"]}}}
---

# Trello 技能

直接从 Clawdbot 管理 Trello 看板、列表和卡片。

## 设置

1. 获取 API 密钥：https://trello.com/app-key
2. 生成令牌（点击该页面上的 "Token" 链接）
3. 设置环境变量：
   ```bash
   export TRELLO_API_KEY="你的-api-密钥"
   export TRELLO_TOKEN="你的-令牌"
   ```

## 使用方法

所有命令都使用 curl 调用 Trello REST API。

### 列出看板
```bash
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

### 列出看板中的列表
```bash
curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

### 列出列表中的卡片
```bash
curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, desc}'
```

### 创建卡片
```bash
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={listId}" \
  -d "name=卡片标题" \
  -d "desc=卡片描述"
```

### 将卡片移动到另一个列表
```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={newListId}"
```

### 为卡片添加评论
```bash
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "text=你的评论内容"
```

### 归档卡片
```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"
```

## 注意事项

- 看板/列表/卡片 ID 可以在 Trello URL 中找到，或通过列表命令获取
- API 密钥和令牌提供对你 Trello 账户的完全访问权限 - 请保密！
- 速率限制：每个 API 密钥每 10 秒 300 次请求；每个令牌每 10 秒 100 次请求；`/1/members` 端点限制为每 900 秒 100 次请求

## 示例

```bash
# 获取所有看板
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id" | jq

# 按名称查找特定看板
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | select(.name | contains("Work"))'

# 获取看板上的所有卡片
curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, list: .idList}'
```
