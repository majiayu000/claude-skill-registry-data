---
name: slack-skill
description: Slack 앱 개발 및 API 통합 스킬. Bolt 프레임워크, Block Kit UI, 이벤트 처리, 슬래시 커맨드 지원. "Slack", "슬랙", "봇", "webhook" 키워드로 활성화.
trigger-keywords: slack, 슬랙, slack bot, 슬랙 봇, bolt, block kit, webhook, 웹훅, slack api, 채널 메시지, slash command, 슬래시 커맨드, slack app, 슬랙 앱
allowed-tools: Read, Write, Edit, Bash, WebFetch
priority: medium
tags: [slack, api, bot, messaging, integration, webhook, block-kit]
---

# Slack Development Skill

## Overview

Slack 플랫폼 개발을 위한 포괄적인 스킬입니다.
Bolt 프레임워크 기반 앱 개발, Web API 통합, Block Kit UI, 이벤트 처리, 배포까지 전체 워크플로우를 지원합니다.

## Purpose

- **Slack 앱 개발**: Bolt 프레임워크 기반 앱 구축
- **메시지 및 봇**: 메시지 전송, 봇 개발, 자동화
- **Block Kit UI**: 리치 메시지 레이아웃, 인터랙티브 컴포넌트
- **이벤트 처리**: 메시지, 리액션, 멘션 등 이벤트 핸들링
- **인증 및 배포**: OAuth 2.0, 멀티 워크스페이스, 프로덕션 배포

## When to Use

**명시적 요청:**
- "Slack 봇 만들어줘"
- "슬랙 앱 개발해줘"
- "Slack으로 메시지 보내줘"
- "Block Kit으로 버튼 만들어줘"
- "슬래시 커맨드 구현해줘"
- "Slack webhook 설정해줘"

**자동 활성화:**
- "slack", "슬랙", "bolt", "block kit" 키워드 언급 시
- 메시지 봇/자동화 요청 시
- webhook 설정 요청 시

## Prerequisites

### 환경 변수

```bash
# 필수
SLACK_BOT_TOKEN=xoxb-...         # Bot User OAuth Token
SLACK_SIGNING_SECRET=...         # Signing Secret

# OAuth용 (선택)
SLACK_CLIENT_ID=...              # Client ID
SLACK_CLIENT_SECRET=...          # Client Secret

# Socket Mode용 (선택)
SLACK_APP_TOKEN=xapp-...         # App-level token
```

### 의존성

```bash
# JavaScript (Node.js)
npm install @slack/bolt @slack/web-api

# Python
pip install slack-bolt slack-sdk
```

## Quick Start

### JavaScript (Bolt)

```javascript
const { App } = require('@slack/bolt');

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET
});

// 메시지 핸들러
app.message('hello', async ({ message, say }) => {
  await say(`Hello, <@${message.user}>!`);
});

// 슬래시 커맨드
app.command('/hello', async ({ command, ack, respond }) => {
  await ack();
  await respond(`Hello, <@${command.user_id}>!`);
});

app.start(3000);
```

### Python (Bolt)

```python
from slack_bolt import App
import os

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

@app.message("hello")
def hello_message(message, say):
    say(f"Hello, <@{message['user']}>!")

@app.command("/hello")
def hello_command(ack, respond, command):
    ack()
    respond(f"Hello, <@{command['user_id']}>!")

if __name__ == "__main__":
    app.start(3000)
```

## Core Features

### 1. Web API

```javascript
// 메시지 전송
await app.client.chat.postMessage({
  channel: 'C12345678',
  text: 'Hello, world!'
});

// 파일 업로드
await app.client.files.uploadV2({
  channel: 'C12345678',
  file: './document.pdf',
  title: 'Important Document'
});

// 유저 정보 조회
const result = await app.client.users.info({
  user: 'U12345678'
});
```

### 2. Block Kit UI

```javascript
// 버튼이 있는 메시지
await say({
  blocks: [
    {
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: 'Would you like to proceed?'
      }
    },
    {
      type: 'actions',
      elements: [
        {
          type: 'button',
          text: { type: 'plain_text', text: 'Yes' },
          action_id: 'yes',
          style: 'primary'
        },
        {
          type: 'button',
          text: { type: 'plain_text', text: 'No' },
          action_id: 'no',
          style: 'danger'
        }
      ]
    }
  ]
});
```

### 3. 이벤트 핸들링

```javascript
// App Home 열기
app.event('app_home_opened', async ({ event, client }) => {
  await client.views.publish({
    user_id: event.user,
    view: {
      type: 'home',
      blocks: [
        {
          type: 'section',
          text: { type: 'mrkdwn', text: 'Welcome!' }
        }
      ]
    }
  });
});

// 리액션 추가
app.event('reaction_added', async ({ event, client }) => {
  if (event.reaction === 'white_check_mark') {
    await client.chat.postMessage({
      channel: event.item.channel,
      text: 'Task complete!'
    });
  }
});
```

### 4. 인터랙티브 컴포넌트

```javascript
// 버튼 클릭
app.action('button_click', async ({ body, ack, client }) => {
  await ack();
  await client.chat.postMessage({
    channel: body.channel.id,
    text: 'Button clicked!'
  });
});

// 모달 제출
app.view('modal_submit', async ({ ack, body, view, client }) => {
  await ack();
  const title = view.state.values.title.title_input.value;
  // 데이터 처리
});
```

## Common OAuth Scopes

```
app_mentions:read     # 멘션 읽기
channels:history      # 채널 히스토리
channels:read         # 채널 정보
chat:write            # 메시지 전송
commands              # 슬래시 커맨드
files:write           # 파일 업로드
im:read               # DM 읽기
users:read            # 유저 정보
views:write           # 모달 및 홈 탭
```

## Deployment

### Local Development

```bash
# ngrok으로 터널링
ngrok http 3000

# Request URL에 ngrok URL 설정
# https://xxxxx.ngrok.io/slack/events
```

### Production

- Vercel, Heroku, AWS Lambda
- Google Cloud Functions, Azure Functions
- Docker 컨테이너

## Security Checklist

- [ ] 환경 변수로 시크릿 관리
- [ ] 요청 서명 검증
- [ ] 입력 값 검증 및 새니타이즈
- [ ] Rate limiting 구현
- [ ] HTTPS 사용
- [ ] 보안 이벤트 로깅

## Common Errors

| 에러 | 원인 | 해결 |
|------|------|------|
| `invalid_auth` | 토큰 무효 | 토큰 재발급 |
| `not_in_channel` | 봇이 채널에 없음 | `/invite @bot` |
| `request_timeout` | 3초 초과 | 비동기 응답 사용 |
| `action_no_longer_valid` | 액션 만료 | 메시지 갱신 |

## Rate Limits

- 메시지: 채널당 1 msg/sec
- 파일 업로드: 20 files/min
- 메시지 크기: 4000자
- 블록 수: 100 blocks/message

## Reference Documentation

- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 빠른 참조
- [SLACK_SKILL_GUIDE.md](SLACK_SKILL_GUIDE.md) - 상세 가이드
- [docs/BLOCK_KIT_COMPONENTS.md](docs/BLOCK_KIT_COMPONENTS.md) - Block Kit
- [docs/SECURITY_BEST_PRACTICES.md](docs/SECURITY_BEST_PRACTICES.md) - 보안

## External Resources

- **Slack API**: https://api.slack.com
- **Block Kit Builder**: https://api.slack.com/tools/block-kit-builder
- **Bolt Framework**: https://slack.dev/bolt/
- **Community**: https://slackcommunity.com/

---

## Workflow

### Step 1: 환경 설정 확인

```bash
# 환경 변수 확인
echo $SLACK_BOT_TOKEN | head -c 10
echo $SLACK_SIGNING_SECRET | head -c 10
```

### Step 2: 작업 유형별 분기

**메시지 전송:**
1. 대상 채널 ID 확인
2. `chat.postMessage` API 호출
3. 결과 확인

**앱 개발:**
1. Bolt 앱 초기화
2. 이벤트/커맨드 핸들러 구현
3. 로컬 테스트 (ngrok)
4. 프로덕션 배포

**Block Kit UI:**
1. 컴포넌트 설계
2. Block Kit Builder로 미리보기
3. 코드에 적용

---

## Examples

### 예시 1: 간단한 메시지 전송

```
사용자: "슬랙 #general 채널에 '안녕하세요' 메시지 보내줘"

Claude:
const { WebClient } = require('@slack/web-api');
const client = new WebClient(process.env.SLACK_BOT_TOKEN);

await client.chat.postMessage({
  channel: 'general',
  text: '안녕하세요'
});

→ 메시지 전송 완료
```

### 예시 2: 버튼이 있는 메시지

```
사용자: "확인/취소 버튼이 있는 메시지 보내줘"

Claude:
await client.chat.postMessage({
  channel: 'C12345',
  blocks: [
    {
      type: 'section',
      text: { type: 'mrkdwn', text: '진행하시겠습니까?' }
    },
    {
      type: 'actions',
      elements: [
        { type: 'button', text: { type: 'plain_text', text: '확인' }, action_id: 'confirm', style: 'primary' },
        { type: 'button', text: { type: 'plain_text', text: '취소' }, action_id: 'cancel', style: 'danger' }
      ]
    }
  ]
});
```

### 예시 3: 슬래시 커맨드 구현

```
사용자: "/hello 슬래시 커맨드 만들어줘"

Claude:
app.command('/hello', async ({ command, ack, respond }) => {
  await ack();
  await respond(`Hello, <@${command.user_id}>! 👋`);
});

→ /hello 커맨드 핸들러 구현 완료
  Slack 앱 설정에서 Slash Command URL 등록 필요
```

---

## Best Practices

**DO:**
- 환경 변수로 토큰/시크릿 관리
- `ack()`를 3초 내에 호출
- 긴 작업은 비동기로 처리 후 `respond()` 사용
- Block Kit Builder로 UI 미리보기
- Rate limit 준수 (1 msg/sec/channel)

**DON'T:**
- 토큰을 코드에 하드코딩하지 않기
- 동기 작업으로 3초 초과하지 않기
- 메시지당 100개 이상 블록 사용하지 않기
- 4000자 초과 메시지 전송하지 않기
- 사용자 입력값 검증 없이 사용하지 않기

---

## Troubleshooting

### invalid_auth
- SLACK_BOT_TOKEN 확인
- 토큰이 `xoxb-`로 시작하는지 확인

### not_in_channel
- 봇이 채널에 초대되었는지 확인
- `/invite @botname` 실행

### request_timeout
- `ack()`를 3초 내에 호출했는지 확인
- 긴 작업은 비동기로 처리

### action_no_longer_valid
- 인터랙티브 컴포넌트가 만료됨
- 새 메시지로 갱신 필요

---

**Version**: 1.0.0
**Last Updated**: December 2025
