---
name: chzzk-live-polling
description: 치지직(CHZZK) 비공식 폴링 API로 멤버 라이브 상태를 가져오는 구조·주기·에러 처리·라이프사이클을 다룬다(클라 포그라운드 + 서버 폴링/라이브 푸시). "라이브 상태", "치지직 폴링", "방송 중 여부", "시청자 수", "통합 LIVE", "라이브 알림/푸시", "폴링 주기/타임아웃", "chzzk API 응답 변경" 관련 작업 시 사용.
---

# 치지직(CHZZK) 라이브 폴링

멤버별 실시간 방송 상태는 **치지직 비공식 polling 엔드포인트**를 호출해 얻는다.
폴링 경로가 **두 곳**이며 로직·에러 정책을 공유한다:

- **클라 포그라운드 폴링** — `lib/controllers/global_controller.dart`.
  화면에 보이는 라이브 현황 갱신용(2분 주기, 포그라운드만).
- **서버 폴링** — `functions/index.js`의 `pollLiveStatus`(1분 주기 스케줄러).
  백그라운드 라이브 감지 → 방송 시작 푸시. 아래 "서버 폴링" 절 참고.

## 엔드포인트

```
GET https://api.chzzk.naver.com/polling/v2/channels/{broadcastId}/live-status
```

- `{broadcastId}` = `Member.chzzkBroadcastId` (dart 카탈로그 정의, [[add-member]] 참고).
- 응답의 `content` 객체를 `LiveCheckModel.fromJson`으로 파싱한다
  (`liveTitle`, `status`, `concurrentUserCount`, `liveCategoryValue`, `openDate`).
- `status == 'OPEN'`이면 방송 중(`LiveCheckModel.isLive`).
- **주의: 비공식·인증 불필요 엔드포인트다.** 응답 형식이 예고 없이 바뀌면
  무증상 실패할 수 있어, 아래처럼 방어적으로 처리한다.

라이브 시청 URL은 별도 규칙: `https://chzzk.naver.com/live/{broadcastId}`
(카드 탭 시 `url_launcher`로 이동). 형식은 `Member.liveUrlOf(broadcastId)`
(및 인스턴스 getter `member.liveUrl`) **한 곳에 단일화**되어 있으니, URL 형식이
바뀌면 `lib/model/member.dart`만 고친다.

## 폴링 주기·타임아웃 (`GlobalController` 상수)

- `_liveRefreshInterval = 2분` — 포그라운드에서 `Timer.periodic`으로 갱신.
- `_requestTimeout = 8초` — 멈춘 요청이 다음 폴링과 겹쳐 쌓이는 것을 방지.
  이 두 값은 서로 맞물려 있으니(타임아웃 < 주기) 함께 조정한다.

## 라이프사이클 (배터리·네트워크 절약)

`AppLifecycleListener`로 제어한다. **백그라운드에서 폴링을 돌리지 않는 것이 의도**다.

- `onResume`: 즉시 1회 갱신 + 주기 폴링 재개 (`refreshAllLiveStatus` → `_startLiveRefreshTimer`).
- `onPause`: 주기 폴링 중단 (`_stopLiveRefreshTimer`).
- `onClose`: 타이머·리스너 정리.

## 조회 함수 계층

- `_fetchLiveStatus(broadcastId)` — 단일 멤버 조회. 실패 시 `null` 반환.
- `_refreshGroupLiveStatus(group)` — 그룹 전체를 `Future.wait`로 병렬 조회 후 캐시 교체.
- `refreshLiveStatus()` — 현재 선택 그룹만.
- `refreshAllLiveStatus()` — 허니즈+아카시아 동시 (통합 LIVE 화면용).
- `liveCheck({forceRefresh})` — 캐시 우선, 비었거나 강제 시 갱신.

### key 기반 매칭 (member.key로 조회)

라이브 상태는 `RxMap<String, LiveCheckModel>`(`honeyzLiveStatus`/`acaxiaLiveStatus`)에
**`member.key` → 상태**로 보관한다. 카탈로그와 **인덱스로 페어링하지 않으므로**,
멤버 추가·순서 변경에도 어긋나지 않는다. (스트리머 프로필도 동일하게
`honeyz`/`acaxia` = `RxMap<String, StreamerModel>`.)

- **소비 규칙**: 맵에 없는 멤버는 "비방송(CLOSE)"으로 다룬다
  (`status?.isLive == true`인 멤버만 방송 중). `liveMembersAcrossGroups`·
  홈 대시보드·`group_page`·`streamer_detail` 모두 카탈로그를 순회하며 key로 상태를 조회한다.
- **직접 폴링**(`_refreshGroupLiveStatus`)은 조회 실패 멤버도 `CLOSE`로 채운다 —
  폴링을 한 번이라도 시도하면 맵이 비지 않아, UI가 "로딩 중(맵 비어있음)"과
  "전원 비방송"을 구분할 수 있다.
- **서버 집계 변환**(`liveStatusFromAggregate`)은 문서에 있는 멤버만 맵에 넣는다
  (없음 = 비방송). 순수 함수라 `test/global_controller_test.dart`에서 검증한다.

## 에러 처리 정책 (노이즈 vs 계약 변경 구분)

`_fetchLiveStatus`는 두 종류를 다르게 다룬다:

- **일시적 오류**(`TimeoutException`/`SocketException`/`http.ClientException`) →
  로그만, Crashlytics 기록 **안 함** (노이즈).
- **HTTP 비정상 응답 / 파싱 예외** → `FirebaseCrashlytics.recordError(fatal:
  false)`로 기록. 이건 **엔드포인트 계약이 바뀐 신호**이므로 반드시 남긴다.

chzzk API가 바뀌어 라이브가 안 뜬다는 리포트가 오면 이 Crashlytics 로그
(`reason: 'chzzk ... 형식 변경 가능성'`)부터 확인한다.

## 홈스크린 위젯 갱신 경로 (Android)

`lib/services/live_widget_service.dart`가 `home_widget` 저장소에 JSON
(`{updatedAt, live:[{name,group,title,viewers,url}]}`)을 쓰고, 네이티브
`LiveStatusWidgetProvider.kt`가 그린다. **페이로드 형식은 양쪽(Dart `buildPayload`
/ Kotlin `render`)을 함께 고친다** — 계약은 `test/live_widget_service_test.dart`.

- 즉시 갱신: `GlobalController._pushLiveWidget()` — 라이브 캐시가 바뀌는 두 경로
  (서버 집계·직접 폴링) 끝에서 호출.
- **즉시 반영(무음 푸시)**: 서버가 방송 중 멤버 집합이 바뀐 주기(`liveSetChanged`,
  순수)에만 전원 구독 토픽 `live_widget`으로 data-only 푸시(`type: widget_refresh`)를
  집계 쓰기 **뒤에** 보낸다. 클라는 항상 구독(`NotificationController`), 백그라운드면
  `refreshFromServer()`, 포그라운드면 `GlobalController.refreshAllLiveStatus()`(화면+위젯).
  위젯 미설치 기기는 `HomeWidget.getInstalledWidgets()`가 비어 있으면 건너뛴다.
- 라이브 FCM 수신(백그라운드): `main._firebaseMessagingBackgroundHandler` →
  `LiveWidgetService.refreshFromServer()` (집계 문서 직접 읽기, GetX 미사용).
- 주기 갱신: 위젯 `updatePeriodMillis`(30분) → 네이티브 `onUpdate`가 데이터가
  5분↑ 오래됐으면 `HomeWidgetBackgroundIntent`로 Dart `backgroundCallback` 호출.
  갱신 후 updatedAt이 신선해져 재요청되지 않는다(루프 방지).
- 위젯은 보조 UI — 실패는 전부 조용히 무시하고 기존 스냅샷을 유지한다.

## 통합 LIVE 정렬

`liveMembersAcrossGroups`: 양쪽 그룹에서 `isLive`인 멤버만 모아 **시청자 수
내림차순**(null=0, 뒤로) 정렬. 최애 우선 노출은 화면단(live_page)에서 처리.

## 서버 폴링 & 라이브 방송 시작 푸시

`functions/index.js`의 `pollLiveStatus`(Cloud Scheduler, 1분, `asia-northeast3`,
`maxInstances: 1`)가 백그라운드 라이브 감지를 담당한다. 멤버 정보는
`MEMBER_CATALOG`에 있으며 dart 카탈로그와 동기화 필수([[add-member]]).
**판정 로직(파싱·전이·심야 완화)은 `functions/live_logic.js` 순수 함수**로
분리되어 `functions/test/live_logic.test.js`(node --test, CI 포함)로 검증한다 —
알림 판정을 고칠 땐 index.js가 아니라 여기부터.

- **썸네일**: polling 응답엔 썸네일이 없다. 방송 중인데 `liveImageUrl`이 없는
  멤버(=세션 시작, `needsLiveImage`)만 비공식 `service/v2/channels/{id}/live-detail`을
  1회 조회해 `liveImageUrl`(`{type}` 자리표시자 템플릿)을 집계에 넣는다. 같은
  세션이면 이어받고 새 세션·종료면 비운다. 실패는 null — 카드가 썸네일 없이
  그려질 뿐이다. 클라 `LiveCheckModel.thumbnailUrl()`이 480으로 치환 + 10분 단위
  캐시 버스터를 붙여 `LiveThumbnail` 위젯(홈 카드·통합 LIVE 카드)이 표시한다.
  클라 직접 폴링 폴백엔 썸네일이 없다(의도).
- **상태 저장**: 집계 문서 `live_status/current`(멤버별 `status`/`liveTitle`/
  `concurrentUserCount`/`openDate`/`lastNotifiedOpenDate`/`liveImageUrl` + 메타
  `consecutiveAllFailures`/`rateLimitedUntil`)에 **주기당 읽기1·쓰기1**.
  members는 **merge 없이 통째 교체** — merge하면 카탈로그에서 뺀 멤버가 잔존한다.
- **알림 판정**: `OPEN`이고 **`openDate`(방송 식별자)로 아직 알림을 보낸 적이
  없을 때** 발송 — 상태가 흔들려도(플랩) 같은 방송엔 1회만. `lastNotifiedOpenDate`는
  **발송 성공 후에만 기록**하므로 FCM 발송 실패는 다음 주기에 자동 재시도된다
  (openDate가 없으면 중복 판정 불가 → 알림 생략).
- **폴링 공백 후 재개 가드**: 시작 15분 이내 방송만 발송(`isRecentOpen`) —
  빌링 중단 등으로 멈췄다 재개되면 공백 중 시작된 방송이 일괄 "방송 시작!"으로
  나가는 것을 막는다(`firstRun`은 빈 집계만 막음). 관측 공백이 30분을 넘은
  종료는 종료 시각을 중간값 대신 마지막 OPEN 관측 시각으로 기록(`estimateEndedAtMs`).
- **실패 시 직전 상태 유지** → 거짓 CLOSE→OPEN 알림 방지 (에러 정책은 클라와 동일).
- **발송**: 멤버별 토픽 `live_<memberKey>`, 채널 `live_channel`,
  `data: {type:'live', broadcastId, memberKey}`.
- **방송 기록**: OPEN 동안 `peakConcurrentUserCount`(세션별 최고 시청자)를
  집계에 누적하고, 종료(OPEN→CLOSE 또는 openDate 변경) 감지 시
  `live_history/{memberKey}/sessions/{openDate숫자}`에 세션 문서를 기록한다
  (베스트 에포트, ID 결정적이라 중복 없음). 같은 레코드를 집계 문서의
  `lastSessions[memberKey]`에도 써서(48h 지난 항목 정리) 홈 "오늘 방송했어요"가
  추가 읽기 없이 표시한다. 클라 멤버 프로필 "지난 방송"은 live_history를 읽는다
  ([[firestore-data]]).

### 클라이언트 수신 (`notification_controller.dart`)

- `live_channel` 채널 생성(스케줄과 분리).
- 구독 범위는 **`liveMode` 설정**('all' 전체 / 'favorites' 최애만(기본) /
  'off' 끄기, 알림 설정 시트에서 변경·영속)이 정한다. 최애 목록이 바뀌면
  `FavoritesController`가 `syncLiveSubscriptions(keys)`로 알리고,
  `desiredLiveTopics(mode, favorites, all)`(순수, 테스트 대상)가 정한 대상과
  영속 집합을 diff해 `live_<key>`를 추가/해제한다.
- 알림 탭 → `chzzk.naver.com/live/{broadcastId}` 이동 (포그라운드 로컬 알림은
  payload, 백그라운드/종료는 `onMessageOpenedApp`/`getInitialMessage`).

### 밴/차단 완화 (구현됨)

단일 egress IP 집중이 주 리스크. 구현된 완화책:

- **심야 완화**: KST 04–10시는 3분의 1 주기만 실제 폴링(사실상 3분 주기,
  `isQuietHourSkip`) — 클라 stale 판정(5분)보다 짧게 유지해야 한다.
- **429/403 백오프**: 감지 시 `rateLimitedUntil`(+10분)을 기록하고 그동안 주기
  생략 + `console.error`. 집계가 오래되면 클라가 직접 폴링으로 폴백.
- **지속 실패 승격**: 전원 조회 실패가 5회 연속(`consecutiveAllFailures`)이면
  `console.error` — Cloud Logging 알림 정책은 error 레벨에 걸어둔다.
- 브라우저 UA 지정, 서버가 막혀도 **클라 포그라운드 폴링이 폴백**으로 남는다.

## 검증

폴링/파싱 로직 수정 후 [[flutter-check]]로 테스트. 순수 파생 로직(정렬·필터·
key 매칭·집계 변환)은 `test/global_controller_test.dart`가 Firebase/네트워크 없이
`RxMap`에 값을 주입해 검증하므로, 여기 기대값도 함께 맞춘다.
