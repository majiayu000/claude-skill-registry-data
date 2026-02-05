---
name: discord-skill
description: Discord REST API 서버/채널 관리 스킬. 채널 CRUD, 권한 관리, 메시지 전송, 웹훅 지원. "Discord", "디스코드", "채널 관리", "discord bot" 키워드로 활성화.
trigger-keywords: discord, 디스코드, discord bot, 디스코드 봇, 채널 관리, channel management, discord api, 서버 관리, guild, 길드, webhook, 웹훅
allowed-tools: Read, Write, Edit, Bash, WebFetch
priority: medium
tags: [discord, api, bot, channel, guild, webhook, messaging]
---

# Discord Channel Management Skill

## Overview

Discord REST API를 활용하여 서버(길드)와 채널을 관리하는 스킬입니다.
Bot 토큰 기반 인증으로 채널 CRUD, 권한 관리, 메시지 전송, 웹훅 작업을 지원합니다.

## Purpose

- **채널 관리**: 텍스트/음성/카테고리 채널 생성, 수정, 삭제
- **권한 관리**: 역할 및 사용자별 채널 권한 설정
- **메시지 작업**: 메시지 전송, 조회, 삭제
- **웹훅 관리**: 웹훅 생성 및 메시지 전송
- **서버 정보**: 길드 정보 및 채널 목록 조회

## When to Use

**명시적 요청:**
- "Discord 채널 만들어줘"
- "디스코드 서버에 메시지 보내줘"
- "채널 권한 설정해줘"
- "Discord 웹훅으로 알림 보내줘"
- "디스코드 채널 목록 보여줘"
- "채널 삭제해줘"

**자동 활성화:**
- "discord", "디스코드" 키워드 언급 시
- 채널/서버/길드 관리 요청 시
- 웹훅 설정 요청 시

## Prerequisites

### 환경 변수

```bash
# 필수 - jelly-dotenv/.env에 설정
DISCORD_BOT_TOKEN=           # Bot Token (Developer Portal에서 발급)

# 선택
DISCORD_APPLICATION_ID=      # Application ID
DISCORD_GUILD_ID=            # 기본 서버(길드) ID
DISCORD_DEFAULT_CHANNEL_ID=  # 기본 채널 ID
```

### Discord Bot 설정

1. [Discord Developer Portal](https://discord.com/developers/applications)에서 애플리케이션 생성
2. Bot 섹션에서 봇 생성 및 토큰 복사
3. OAuth2 > URL Generator에서 봇 초대 링크 생성
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Manage Channels`, `Send Messages`, `Manage Messages`
4. 생성된 URL로 봇을 서버에 초대

## API Reference

### Base URL

```
https://discord.com/api/v10
```

### Authentication

```bash
Authorization: Bot YOUR_BOT_TOKEN
Content-Type: application/json
```

## Quick Start

### 채널 목록 조회

```bash
# 환경 변수 로드
source skills/jelly-dotenv/load-env.sh

# 길드의 채널 목록 조회
curl -s -X GET \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  "https://discord.com/api/v10/guilds/$DISCORD_GUILD_ID/channels" | jq
```

### 텍스트 채널 생성

```bash
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "new-channel",
    "type": 0,
    "topic": "채널 설명"
  }' \
  "https://discord.com/api/v10/guilds/$DISCORD_GUILD_ID/channels" | jq
```

### 메시지 전송

```bash
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello from Claude Code!"
  }' \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/messages" | jq
```

### 채널 삭제

```bash
curl -s -X DELETE \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  "https://discord.com/api/v10/channels/$CHANNEL_ID" | jq
```

## Channel Types

| Type | 값 | 설명 |
|------|-----|------|
| GUILD_TEXT | 0 | 텍스트 채널 |
| DM | 1 | DM 채널 |
| GUILD_VOICE | 2 | 음성 채널 |
| GROUP_DM | 3 | 그룹 DM |
| GUILD_CATEGORY | 4 | 카테고리 |
| GUILD_ANNOUNCEMENT | 5 | 공지 채널 |
| ANNOUNCEMENT_THREAD | 10 | 공지 스레드 |
| PUBLIC_THREAD | 11 | 공개 스레드 |
| PRIVATE_THREAD | 12 | 비공개 스레드 |
| GUILD_STAGE_VOICE | 13 | 스테이지 채널 |
| GUILD_DIRECTORY | 14 | 디렉토리 |
| GUILD_FORUM | 15 | 포럼 채널 |
| GUILD_MEDIA | 16 | 미디어 채널 |

## Permissions Bitfield

### 주요 권한

| 권한 | Hex | Decimal | 설명 |
|------|-----|---------|------|
| VIEW_CHANNEL | 0x400 | 1024 | 채널 보기 |
| MANAGE_CHANNELS | 0x10 | 16 | 채널 관리 |
| SEND_MESSAGES | 0x800 | 2048 | 메시지 전송 |
| MANAGE_MESSAGES | 0x2000 | 8192 | 메시지 관리 |
| MANAGE_ROLES | 0x10000000 | 268435456 | 역할/권한 관리 |
| ADMINISTRATOR | 0x8 | 8 | 관리자 (모든 권한) |

### 권한 계산

```javascript
// 여러 권한 조합
const permissions = VIEW_CHANNEL | SEND_MESSAGES | MANAGE_MESSAGES;
// 1024 | 2048 | 8192 = 11264
```

## Core Features

### 1. 채널 CRUD

```bash
# 채널 정보 조회
curl -s -X GET \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  "https://discord.com/api/v10/channels/$CHANNEL_ID" | jq

# 채널 수정
curl -s -X PATCH \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "updated-name",
    "topic": "새로운 설명"
  }' \
  "https://discord.com/api/v10/channels/$CHANNEL_ID" | jq

# 음성 채널 생성
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Voice Room",
    "type": 2,
    "user_limit": 10
  }' \
  "https://discord.com/api/v10/guilds/$DISCORD_GUILD_ID/channels" | jq

# 카테고리 생성
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Category",
    "type": 4
  }' \
  "https://discord.com/api/v10/guilds/$DISCORD_GUILD_ID/channels" | jq
```

### 2. 권한 관리

```bash
# 역할에 채널 권한 설정
curl -s -X PUT \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": 0,
    "allow": "3072",
    "deny": "0"
  }' \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/permissions/$ROLE_ID"

# type: 0 = 역할, 1 = 멤버
# allow/deny: 권한 비트필드 문자열
```

### 3. 메시지 작업

```bash
# 메시지 목록 조회 (최근 50개)
curl -s -X GET \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/messages?limit=50" | jq

# Embed 메시지 전송
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "embeds": [{
      "title": "알림",
      "description": "중요한 공지사항입니다.",
      "color": 5814783,
      "fields": [
        {"name": "항목 1", "value": "내용 1", "inline": true},
        {"name": "항목 2", "value": "내용 2", "inline": true}
      ]
    }]
  }' \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/messages" | jq

# 메시지 삭제
curl -s -X DELETE \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/messages/$MESSAGE_ID"

# 메시지 일괄 삭제 (2주 이내, 2-100개)
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": ["MESSAGE_ID_1", "MESSAGE_ID_2"]
  }' \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/messages/bulk-delete"
```

### 4. 웹훅 관리

```bash
# 웹훅 생성
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Webhook"
  }' \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/webhooks" | jq

# 웹훅으로 메시지 전송 (토큰 불필요)
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Webhook message!",
    "username": "Custom Bot Name"
  }' \
  "https://discord.com/api/v10/webhooks/$WEBHOOK_ID/$WEBHOOK_TOKEN"
```

### 5. 스레드 관리

```bash
# 메시지에서 스레드 생성
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Discussion Thread",
    "auto_archive_duration": 1440
  }' \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/messages/$MESSAGE_ID/threads" | jq

# 스레드 없이 생성 (포럼/미디어 채널용)
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Thread",
    "type": 11,
    "auto_archive_duration": 60
  }' \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/threads" | jq
```

## Rate Limits

| 범위 | 제한 |
|------|------|
| 전역 | 50 req/sec |
| 메시지 전송 | 5 msg/5sec/channel |
| 메시지 삭제 | 별도 높은 제한 |
| 채널 수정 | 2 req/10min/channel |

### Rate Limit 헤더

```
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 4
X-RateLimit-Reset: 1470173023.123
X-RateLimit-Reset-After: 1.456
X-RateLimit-Bucket: abc123
```

## Error Handling

### 일반적인 에러 코드

| 코드 | 의미 | 해결 방법 |
|------|------|----------|
| 401 | Unauthorized | 토큰 확인 |
| 403 | Forbidden | 봇 권한 확인 |
| 404 | Not Found | ID 확인 |
| 429 | Rate Limited | 재시도 대기 |
| 50001 | Missing Access | 채널 접근 권한 없음 |
| 50013 | Missing Permissions | 필요 권한 부족 |

### 에러 응답 처리

```bash
response=$(curl -s -w "\n%{http_code}" ...)
http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "429" ]; then
  retry_after=$(echo "$body" | jq -r '.retry_after')
  sleep "$retry_after"
fi
```

## Security Checklist

- [ ] 봇 토큰을 코드에 하드코딩하지 않기
- [ ] 환경 변수 또는 시크릿 매니저 사용
- [ ] 필요한 최소 권한만 부여
- [ ] Rate Limit 준수
- [ ] 민감한 채널에 대한 접근 제한

## Reference Documentation

- [references/api-endpoints.md](references/api-endpoints.md) - API 엔드포인트 전체 목록
- [references/permissions.md](references/permissions.md) - 권한 비트필드 상세
- [references/rate-limits.md](references/rate-limits.md) - Rate Limit 가이드

## External Resources

- **Discord Developer Portal**: https://discord.com/developers/docs
- **Discord.js Guide**: https://discordjs.guide/
- **Permission Calculator**: https://discordapi.com/permissions.html
- **Discord API Types**: https://discord-api-types.dev/

---

## Workflow

### Step 1: 환경 확인

```bash
# 환경 변수 로드
source skills/jelly-dotenv/load-env.sh

# 봇 연결 테스트
curl -s -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  "https://discord.com/api/v10/users/@me" | jq .username
```

### Step 2: 작업 유형별 분기

**채널 관리:**
1. 길드 채널 목록 조회
2. 채널 생성/수정/삭제 실행
3. 결과 확인

**메시지 전송:**
1. 대상 채널 ID 확인
2. 메시지 본문 구성 (텍스트/Embed)
3. POST 요청 실행

**웹훅 작업:**
1. 채널에 웹훅 생성
2. 웹훅 URL로 메시지 전송

---

## Examples

### 예시 1: 채널 목록 조회

```
사용자: "디스코드 서버의 채널 목록 보여줘"

Claude:
curl -s -X GET \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  "https://discord.com/api/v10/guilds/$DISCORD_GUILD_ID/channels" | jq

→ 채널 목록:
| 이름 | 타입 | ID |
|------|------|-----|
| general | 텍스트 | 123456789 |
| voice-chat | 음성 | 987654321 |
```

### 예시 2: 텍스트 채널 생성

```
사용자: "announcements라는 공지 채널 만들어줘"

Claude:
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "announcements", "type": 0, "topic": "공지사항"}' \
  "https://discord.com/api/v10/guilds/$DISCORD_GUILD_ID/channels"

→ 채널 "announcements" 생성 완료 (ID: 111222333)
```

### 예시 3: Embed 메시지 전송

```
사용자: "알림 채널에 배포 완료 메시지 보내줘"

Claude:
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "embeds": [{
      "title": "배포 완료",
      "description": "v1.2.3 배포가 완료되었습니다.",
      "color": 5763719
    }]
  }' \
  "https://discord.com/api/v10/channels/$CHANNEL_ID/messages"

→ 메시지 전송 완료
```

---

## Best Practices

**DO:**
- 봇 토큰은 환경 변수로 관리
- Rate limit 준수 (429 응답 시 대기)
- 필요한 최소 권한만 봇에 부여
- 채널 작업 전 권한 확인
- 대량 삭제 시 bulk-delete API 사용

**DON'T:**
- 토큰을 코드에 하드코딩하지 않기
- Rate limit 무시하고 연속 요청하지 않기
- 모든 권한을 가진 봇 사용하지 않기
- 2주 이상 된 메시지에 bulk-delete 시도하지 않기
- 사용자 DM에 무분별하게 메시지 보내지 않기

---

## Troubleshooting

### 401 Unauthorized
```bash
# 토큰 확인
echo $DISCORD_BOT_TOKEN | head -c 20
# 토큰 형식: Bot xxxxxxxxxxx
```

### 403 Forbidden
- 봇이 해당 채널/서버에 접근 권한이 있는지 확인
- 필요한 권한(Manage Channels 등)이 부여되었는지 확인

### 429 Rate Limited
```bash
# retry_after 값만큼 대기 후 재시도
sleep $retry_after
```

### 50001 Missing Access
- 봇이 서버에 초대되었는지 확인
- `/invite @bot` 명령으로 채널에 봇 추가

---

**Version**: 1.0.0
**Last Updated**: December 2025
