---
name: trello
description: "Boards, lists, and cards via the REST API."
version: 1.0.0
author: External Agent contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
required_environment_variables:
  - name: TRELLO_API_KEY
    prompt: "Trello API key from https://trello.com/app-key"
    help: "Get your API key at https://trello.com/app-key"
  - name: TRELLO_TOKEN
    prompt: "Trello API token (the Token link on https://trello.com/app-key)"
    help: "Generate a token from the Token link on https://trello.com/app-key"
metadata:
  hermes:
    tags: [trello, boards, cards, kanban, api, curl, jq]
    category: productivity
    related_skills: []
---

# Trello Skill

Manage Trello boards, lists, and cards directly via the Trello REST API, with `curl` through `terminal` and `jq` for shaping output. Ported from External Agent `skills/trello/SKILL.md`. Pairs with Hermes' kanban tools for local task boards; this skill talks to Trello itself.

## When to Use

- Listing Trello boards, lists, or cards.
- Creating, moving, commenting on, or archiving cards.
- Do not use for Hermes' local kanban boards — use the kanban tools for those.

## Prerequisites

- `curl` and `jq` on the host. Run commands through `terminal`.
- `TRELLO_API_KEY` and `TRELLO_TOKEN`, supplied by the user at runtime; never hardcode or embed them.
  1. Get your API key: https://trello.com/app-key
  2. Generate a token (click the "Token" link on that page)
  3. Set the environment variables:
     ```
     export TRELLO_API_KEY="your-api-key"
     export TRELLO_TOKEN="your-token"
     ```

## How to Run

All commands use `curl` to hit `https://api.trello.com/1/...`, authenticating with `key=$TRELLO_API_KEY&token=$TRELLO_TOKEN` query parameters. Pipe through `jq` to shape the JSON.

## Quick Reference

| Need | Call |
|---|---|
| List boards | `GET /1/members/me/boards` |
| List lists in a board | `GET /1/boards/{boardId}/lists` |
| List cards in a list | `GET /1/lists/{listId}/cards` |
| Create a card | `POST /1/cards` with `idList`, `name`, `desc` |
| Move a card | `PUT /1/cards/{cardId}` with `idList` |
| Comment on a card | `POST /1/cards/{cardId}/actions/comments` with `text` |
| Archive a card | `PUT /1/cards/{cardId}` with `closed=true` |

## Procedure

### List boards

```
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

### List lists in a board

```
curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

### List cards in a list

```
curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, desc}'
```

### Create a card

```
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={listId}" \
  -d "name=Card Title" \
  -d "desc=Card description"
```

### Move a card to another list

```
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={newListId}"
```

### Add a comment to a card

```
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "text=Your comment here"
```

### Archive a card

```
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"
```

## Examples

```
# Get all boards
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id" | jq

# Find a specific board by name
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | select(.name | contains("Work"))'

# Get all cards on a board
curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, list: .idList}'
```

## Pitfalls

- Board/List/Card IDs can be found in the Trello URL or via the list commands above. Replace the `{boardId}`, `{listId}`, and `{cardId}` placeholders — they are not literal.
- The API key and token provide full access to your Trello account — keep them secret, never paste them into a card or a message, and never commit them.
- Rate limits: 300 requests per 10 seconds per API key; 100 requests per 10 seconds per token; `/1/members` endpoints are limited to 100 requests per 900 seconds.

## Verification

- The list-boards call returns JSON with your boards' names and IDs; a 401 means the key or token is wrong or missing, not that the skill is broken.
- Live check on the host: `curl` + `jq` plus user-supplied `TRELLO_API_KEY`/`TRELLO_TOKEN` are present, and the list-boards call returns a board list. The credentials are host-side prerequisites; without them the skill reports the missing setup instead of working around it.
