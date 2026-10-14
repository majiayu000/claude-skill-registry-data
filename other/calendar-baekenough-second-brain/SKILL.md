---
name: calendar
description: 실시간 Google Calendar 조회·일정 등록·수정. 캘린더, 일정, 면접, 예약 변경 요청 시 사용. Second-Brain 검색은 조회 전용이지만 이 도구는 쓰기 가능하며 브라우저가 필요 없다.
---

# Calendar

Google Calendar API에 직접 연결된 영속 클라이언트다. **일정 등록·수정은 지원된다.** 브라우저 활성화나 `hermes tools enable browser`가 필요하지 않다.

```bash
CAL="python ${HERMES_HOME:-$HOME/.hermes}/calendar_client.py"
$CAL now
$CAL calendars
$CAL list --start 2026-09-21T00:00:00+09:00 --end 2026-09-22T00:00:00+09:00
$CAL get --calendar primary --event-id EVENT_ID
```

- 오늘·내일·이번 주는 반드시 `now`의 Asia/Seoul 실제 시각으로 계산한다. 과거 대화/시스템 프롬프트에 적힌 날짜를 현재 날짜로 사용하지 않는다.
- 일정 조회는 이 실시간 API를 우선한다. Second-Brain calendar 검색 결과는 수집 주기만큼 늦을 수 있다.
- 등록/수정은 사용자 요청이 있으면 실행한다. 명확히 요청한 사항을 매번 재승인받지 않는다. 대상이 여러 개면 구분에 필요한 정보만 묻는다.
- 먼저 날짜 범위로 후보를 조회하고 **Google event ID**를 확보한다. Second-Brain document UUID는 Google event ID가 아니다.
- `calendars`의 accessRole이 owner/writer인 캘린더만 수정 가능하다. 기본은 primary.

## 수정

`get`으로 얻은 `etag`를 그대로 전달한다. 제공한 필드만 PATCH하므로 참석자·알림·링크 등은 보존된다. 시작/종료는 함께 지정하며 시간대 오프셋 필수.

```python
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(os.environ.get('HERMES_HOME', Path.home()/'.hermes'))))
import calendar_client as cal
old = cal.api(cal.event_path('primary', event_id))
updated = cal.update('primary', event_id, old['etag'],
    summary='회의', start='2026-09-22T17:00:00+09:00',
    end='2026-09-22T18:00:00+09:00', location='회의실',
    description='변경 사항')
verified = cal.api(cal.event_path('primary', event_id))
```

- 시작 전 도착 시각/사전 준비는 메모에 별도로 남긴다. 종료가 명시되지 않았다면 기존 종료 시각을 유지하고 그 사실을 알린다.
- 412/etag 충돌은 최신 내용을 다시 읽어 해결한다. 무조건 덮어쓰지 않는다.
- 반복 일정은 조회로 얻은 개별 occurrence ID만 수정한다. 시리즈 전체 수정과 종일→시간 일정 변환은 지원하지 않는다.
- 사용자에게 성공을 보고하기 전 `get`으로 실제 저장 결과를 확인한다.

## 등록

```python
import uuid
# 재시도 때는 반드시 같은 event_id를 재사용한다.
event_id = uuid.uuid4().hex
created = cal.create('primary', event_id, summary='회의',
    start='2026-09-22T17:00:00+09:00', end='2026-09-22T18:00:00+09:00')
```

먼저 해당 시간대에 같은 일정이 있는지 확인한다. 409는 같은 ID를 `get`으로 조회해 성공 여부를 확인한다. API/네트워크 실패 후 새 ID로 무작정 재등록하지 않는다. 참석자 초대·이메일 발송·삭제는 이 클라이언트 범위에 없다.

## 인증 오류

토큰과 OAuth client 파일은 영속 Hermes 홈에 저장되며 자동 갱신된다. 토큰 원문/키를 읽어 출력하거나 대화에 붙이지 않는다. 조회만 가능하다고 추측하지 말고 실제 오류를 확인한다. Google 401/403이면 재승인이 필요할 수 있다. `auth-url`로 승인 URL을 받고, 승인 뒤 전체 redirect URL을 비공개 파일에 저장하여 `auth-code --redirect-file PATH`로 교환한다. 인증 완료 뒤 임시 파일을 지운다.
