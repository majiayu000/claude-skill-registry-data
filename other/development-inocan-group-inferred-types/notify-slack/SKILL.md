---
name: notify-slack
description: |
  Slack 채널에 메시지 전송 (공통 Skill). Use when (1) 이슈/태스크 알림,
  (2) 릴리스 알림, (3) /SEMO:slack 커맨드, (4) 팀원 멘션 요청.
tools: [Bash, Read, mcp__semo-integrations__semo_get_slack_token]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: notify-slack 호출 - {알림 유형}` 시스템 메시지를 첫 줄에 출력하세요.

# notify-slack Skill

> Slack 채널에 다양한 유형의 메시지 전송 (SEMO 공통 Skill)

## Purpose

모든 SEMO 패키지에서 공통으로 사용하는 Slack 알림 Skill입니다.

### 지원 메시지 유형

| 유형 | 설명 | 트리거 |
|------|------|--------|
| **이슈 알림** | Issue/Task 생성 완료 알림 | Agent 완료 후 호출 |
| **릴리스 알림** | SEMO 패키지 버전 업데이트 | version-manager 완료 후 |
| **커스텀 메시지** | 자유 형식 메시지 전송 | /SEMO:slack 커맨드 |

## Execution Flow

```text
1. MCP에서 Slack Token 조회
   ↓
2. 채널 ID 확인 (기본: C09KNL91QBZ = #_협업)
   ↓
3. (필요시) 사용자 ID 조회 (curl로 Slack API 호출)
   ↓
4. 메시지 전송 (curl + heredoc)
```

### Step 1: Token 획득

```
mcp__semo-integrations__semo_get_slack_token()
```

응답에서 `token:` 접두사 뒤의 토큰 값을 추출합니다.

### Step 2: 사용자 ID 조회 (필요시)

> **⚠️ 중요**: 모든 사용자 멘션은 반드시 `<@SLACK_ID>` 형식 사용
> **🔴 NON-NEGOTIABLE**: curl 직접 호출 시 토큰 파싱 문제 발생 가능. **반드시 스크립트 파일로 실행**

#### 방법 1: 스크립트 파일 생성 후 실행 (권장)

```bash
# 1. 스크립트 파일 생성
cat << 'SCRIPT' > /tmp/slack_users.sh
#!/bin/bash
TOKEN="$1"
curl -s "https://slack.com/api/users.list?limit=200" -H "Authorization: Bearer $TOKEN"
SCRIPT
chmod +x /tmp/slack_users.sh

# 2. 실행 및 사용자 검색
/tmp/slack_users.sh "{TOKEN}" | jq -r '.members[] | select(.deleted==false) | select(.profile.display_name | test("{이름}"; "i")) | .id'
```

#### 방법 2: display_name 또는 real_name으로 검색

```bash
/tmp/slack_users.sh "{TOKEN}" | jq -r '
  .members[] |
  select(.deleted==false) |
  select(
    (.profile.display_name | test("{이름}"; "i")) or
    (.real_name | test("{이름}"; "i"))
  ) |
  "\(.profile.display_name // .real_name) | \(.id)"
'
```

#### 방법 3: 전체 사용자 목록 조회

```bash
/tmp/slack_users.sh "{TOKEN}" | jq -r '
  .members[] |
  select(.deleted==false) |
  select(.is_bot==false) |
  "\(.profile.display_name // .real_name) | \(.id)"
'
```

> **⚠️ 주의**: `curl -s 'url' -H 'header'` 형식의 직접 호출은 셸 환경에 따라
> `curl: option : blank argument` 에러가 발생할 수 있습니다.
> 항상 스크립트 파일 방식을 사용하세요.

### Step 3: 메시지 전송 (스크립트 + heredoc 방식)

> **🔴 권장**: 복잡한 JSON 메시지는 스크립트 파일로 전송

#### 방법 1: 스크립트 파일 + heredoc (권장)

```bash
# 토큰을 변수에 저장 후 heredoc 사용
TOKEN="xoxb-..."
curl -s -X POST 'https://slack.com/api/chat.postMessage' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d @- << 'EOF'
{
  "channel": "C09KNL91QBZ",
  "text": "{fallback_text}",
  "blocks": [...]
}
EOF
```

#### 방법 2: 메시지 전송 스크립트 생성

```bash
# 1. 전송 스크립트 생성
cat << 'SCRIPT' > /tmp/slack_send.sh
#!/bin/bash
TOKEN="$1"
CHANNEL="$2"
MESSAGE="$3"
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$MESSAGE"
SCRIPT
chmod +x /tmp/slack_send.sh

# 2. JSON 메시지 파일 생성
cat << 'EOF' > /tmp/slack_message.json
{
  "channel": "C09KNL91QBZ",
  "text": "메시지 내용",
  "blocks": [...]
}
EOF

# 3. 전송
/tmp/slack_send.sh "{TOKEN}" "C09KNL91QBZ" "$(cat /tmp/slack_message.json)"
```

> **⚠️ 주의**: 인라인 curl 호출 시 셸 환경에 따라 헤더 파싱 오류 발생 가능.
> `TOKEN` 변수를 먼저 선언하고 `$TOKEN` 형식으로 사용하세요.

## 채널 정보

| 채널 | ID | 용도 |
|------|-----|------|
| #_협업 | C09KNL91QBZ | 기본 알림 채널 |

### 프로젝트별 채널 동적 조회 (선택)

```bash
# 채널 목록에서 검색
curl -s 'https://slack.com/api/conversations.list?types=public_channel&limit=1000' \
  -H 'Authorization: Bearer {TOKEN}' | \
  jq -r '.channels[] | select(.name | contains("{프로젝트명}")) | "\(.name) (\(.id))"'
```

## Output

```markdown
[SEMO] Skill: notify-slack 완료

✅ Slack 알림 전송 완료

**채널**: #_협업
**유형**: {release|issue|custom}
```

## References

- [User Lookup](references/slack-id-mapping.md)
- [Message Templates](references/message-templates.md)
