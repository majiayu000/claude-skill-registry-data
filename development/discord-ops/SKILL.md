---
name: discord-ops
description: Discord 서버 운영 자동화 skill. MCP 서버를 통해 메시지 전송, 채널 관리, 역할 부여 등 수행. Discord 관련 작업, 서버 운영, 커뮤니티 관리 요청 시 사용.
---

# Discord Operations Skill

Discord 서버 운영을 자동화하는 skill입니다. MCP 서버(discord-mcp)를 통해 Discord API와 통신합니다.

## 사용 가능한 MCP 도구

### 서버 정보
- `get_server_info` - 서버 상세 정보 조회

### 메시지 관리
- `send_message` - 채널에 메시지 전송
- `read_messages` - 메시지 히스토리 조회
- `edit_message` - 메시지 수정
- `delete_message` - 메시지 삭제
- `add_reaction` / `remove_reaction` - 이모지 반응

### 채널 관리
- `create_text_channel` - 텍스트 채널 생성
- `delete_channel` - 채널 삭제
- `get_channel_list` - 채널 목록 조회

### 역할 관리
- `create_role` - 역할 생성
- `delete_role` - 역할 삭제
- `assign_role` / `remove_role` - 사용자 역할 부여/제거

### 사용자 관리
- `get_user_id_by_name` - 사용자명으로 ID 검색
- `send_private_message` - DM 전송
- `list_members` - 멤버 목록 조회

## 운영 지침

작업 수행 시 `tasks/` 폴더의 지침을 참조합니다:
- `tasks/connection-test.md` - 연결 테스트
- `tasks/welcome-member.md` - 새 멤버 환영
- `tasks/daily-announce.md` - 일일 공지

## 작업 수행 방식

1. 요청된 작업에 해당하는 지침 파일 확인
2. 지침에 따라 MCP 도구 호출
3. 결과 확인 및 보고

## 주의사항

- 메시지 전송 전 채널 ID 확인 필수
- 역할 부여 시 권한 계층 확인
- 대량 작업 시 rate limit 고려 (1초 간격 권장)
