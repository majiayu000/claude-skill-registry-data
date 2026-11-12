---
name: anti-bot
description: "봇·매크로 방어 — 다층 방어 아키텍처, 행동 분석 기반 봇 탐지, Device/Browser Fingerprint, Headless 브라우저 탐지, JA3 TLS 지문, JS Challenge·Proof-of-Work, Nginx/AWS WAF 규칙, 탐지 메트릭·알림. Use when 티켓 매크로·크롤러·자동화 공격을 차단하거나 WAF 규칙을 설계할 때."
---

# 봇 / 매크로 방어

탐지(행동·지문) → 챌린지 → 차단(WAF)의 다층 구조.
요청량 제한 자체는 `/saas:rate-limiting` 이 다루며, 여기서는 **누가 봇인지 판별**하는 축을 다룬다.

## Multi-Layer Defense Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Layer Bot Defense                       │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: Edge (CDN/WAF)                                        │
│  ├─ IP Reputation, Geo Blocking, Known Bot Signatures           │
│              ↓                                                   │
│  Layer 2: Rate Limiting                                         │
│  ├─ Global / Per-IP / Per-User / Endpoint-specific              │
│              ↓                                                   │
│  Layer 3: Challenge                                             │
│  ├─ JS Challenge, CAPTCHA (suspicious), PoW (high load)        │
│              ↓                                                   │
│  Layer 4: Behavioral Analysis                                   │
│  ├─ Mouse/Touch, Timing, Session Behavior                       │
│              ↓                                                   │
│  Layer 5: Device Fingerprint                                    │
│  └─ Browser, TLS (JA3), Anomaly Detection                       │
└─────────────────────────────────────────────────────────────────┘
```

> 요청량 제한(Sliding Window / Token Bucket) 구현은 `/saas:rate-limiting` 참조 — 여기서 중복 기술하지 않는다.

## Behavioral Analysis

### Bot Detection Flags

| Flag | 조건 | 감점 |
|------|------|------|
| `CONSISTENT_TIMING` | 요청 간격 표준편차 < 50ms | -30 |
| `SUPERHUMAN_SPEED` | 평균 간격 < 100ms | -40 |
| `NO_MOUSE_MOVEMENT` | 마우스 이동 없음 | -20 |
| `LINEAR_MOVEMENT` | 직선 이동 비율 > 90% | -25 |
| `CENTERED_CLICKS` | 모든 클릭이 정확히 중앙 | -35 |
| `SHORT_DWELL_TIME` | 페이지 체류 < 0.5초 | -20 |
| `PROGRAMMATIC_TYPING` | 키 입력 간격 < 30ms | -35 |

**판정**: Score < 30 → Bot, Score < 60 → Suspicious

### Frontend Behavior Collection

```javascript
class BehaviorCollector {
    constructor() {
        this.mouseMovements = [];
        this.clickEvents = [];
        this.keystrokes = [];
        this.startTime = Date.now();
        this.init();
    }

    init() {
        // 마우스 이동 (50ms throttle, 최근 100개)
        document.addEventListener('mousemove', throttle((e) => {
            this.mouseMovements.push({ x: e.clientX, y: e.clientY, t: Date.now() - this.startTime });
        }, 50));

        // 클릭 (위치 + 오프셋)
        document.addEventListener('click', (e) => {
            this.clickEvents.push({ x: e.clientX, y: e.clientY, offsetX: e.offsetX, offsetY: e.offsetY });
        });

        // 키 입력 타이밍 (값은 수집 안함)
        document.addEventListener('keydown', () => {
            this.keystrokes.push({ t: Date.now() - this.startTime });
        });
    }

    attachToRequest(headers) {
        headers['X-Behavior-Data'] = btoa(JSON.stringify(this.getData()));
        return headers;
    }
}
```

## Device Fingerprinting

### Browser Fingerprint Components

| 항목 | 수집 방법 |
|------|----------|
| User-Agent | HTTP Header |
| Screen Resolution | `screen.width x screen.height` |
| Timezone | `Intl.DateTimeFormat().resolvedOptions().timeZone` |
| Canvas Hash | Canvas API 렌더링 결과 해시 |
| WebGL Renderer | `getParameter(UNMASKED_RENDERER_WEBGL)` |
| Plugins | `navigator.plugins` |

### Headless Browser Detection

```java
private boolean isHeadlessBrowser(FingerprintData data) {
    // SwiftShader = Headless Chrome
    if (data.getWebGLRenderer().contains("SwiftShader")) return true;
    // navigator.webdriver 플래그
    if (Boolean.TRUE.equals(data.getWebdriverFlag())) return true;
    // 플러그인 없음 + Chrome
    if (data.getPlugins().isEmpty() && data.getUserAgent().contains("Chrome")) return true;
    return false;
}
```

### TLS Fingerprint (JA3)

```java
// 알려진 봇 라이브러리 JA3 해시
Set<String> knownBotJA3 = Set.of(
    "e7d705a3286e19ea42f587b344ee6865",  // Python requests
    "6734f37431670b3ab4292b8f60f29984",  // curl
    "4d7a28d6f2263ed61de88ca66eb011e1"   // Go http client
);

// X-JA3-Hash 헤더 체크 (리버스 프록시에서 추가)
if (knownBotJA3.contains(request.getHeader("X-JA3-Hash"))) {
    return forbidden();
}
```

## Challenge Systems

### JavaScript Challenge

```java
// 서버: 간단한 연산 문제 생성
ChallengeToken createJsChallenge(String sessionId) {
    int a = random.nextInt(100), b = random.nextInt(100);
    String challenge = encrypt("return " + a + " + " + b, sessionId);
    redis.setex("challenge:" + sessionId, 30, String.valueOf(a + b));
    return new ChallengeToken(challenge, Instant.now().plusSeconds(30));
}

// 클라이언트: eval로 실행 후 정답 제출
```

### Proof-of-Work (High Load)

```java
// 서버: nonce + difficulty 발급
PoWChallenge issuePoW(String sessionId, int difficulty) {
    String nonce = UUID.randomUUID().toString();
    String prefix = "0".repeat(difficulty);  // 예: "0000"
    redis.setex("pow:" + sessionId, 120, nonce + ":" + difficulty);
    return new PoWChallenge(nonce, difficulty, prefix);
}

// 클라이언트: SHA256(nonce + solution)이 prefix로 시작하는 solution 찾기
// 검증: hash.startsWith(prefix)
```

## WAF Integration

### Nginx Rate Limiting

```nginx
http {
    limit_req_zone $binary_remote_addr zone=ip:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=conn:10m;

    map $http_user_agent $is_bot {
        default 0;
        ~*bot 1; ~*spider 1; ~*python 1; ~*curl 1; "" 1;
    }

    server {
        if ($is_bot) { return 403; }

        location /api/ {
            limit_req zone=ip burst=20 nodelay;
            limit_conn conn 10;
            limit_req_status 429;
        }
    }
}
```

### AWS WAF Rules (핵심)

```json
{
  "Rules": [
    { "Name": "RateLimit", "Statement": { "RateBasedStatement": { "Limit": 1000, "AggregateKeyType": "IP" }}},
    { "Name": "BlockKnownBots", "Statement": { "ByteMatchStatement": { "SearchString": "python-requests", "FieldToMatch": "user-agent" }}},
    { "Name": "BlockNoUA", "Statement": { "SizeConstraintStatement": { "FieldToMatch": "user-agent", "Size": 0 }}}
  ]
}
```

## Monitoring Metrics

```java
meterRegistry.counter("bot.detection", "type", detectionType, "blocked", String.valueOf(blocked));
meterRegistry.counter("rate_limit.hit", "type", limitType);
meterRegistry.summary("behavior.score").record(score);
```

### Alert Rules

```yaml
- alert: HighBotTraffic
  expr: sum(rate(bot_detection_total{blocked="true"}[5m])) / sum(rate(http_requests_total[5m])) > 0.3
  annotations:
    summary: "30% 이상의 트래픽이 봇으로 감지됨"

- alert: RateLimitSurge
  expr: sum(rate(rate_limit_hit_total[1m])) > 1000
  annotations:
    summary: "Rate limit 히트가 분당 1000회 초과"
```

## Defense Effectiveness

| 방어 계층 | 탐지율 | 오탐률 |
|----------|--------|--------|
| WAF/IP 기반 | 40% | 5% |
| Rate Limiting | 60% | 10% |
| JS Challenge | 75% | 3% |
| Behavioral Analysis | 85% | 8% |
| Device Fingerprint | 80% | 5% |
| **다층 조합** | **95%+** | **2%** |

## Anti-Patterns

| 패턴 | 문제 | 해결 |
|------|------|------|
| CAPTCHA만 의존 | AI 솔버로 우회 | 다층 방어 |
| IP만으로 차단 | Proxy/VPN 우회 | 핑거프린트 + 행동 분석 |
| 정적 Rate Limit | 정상 사용자도 차단 | 동적/적응형 제한 |
| 서버 사이드만 | 클라이언트 조작 못 탐지 | 프론트엔드 행동 수집 |


## 참조 스킬

- `/saas:rate-limiting` — 알고리즘 / 키 설계 / 429 응답
- `/saas:virtual-waiting-room` — 대기열 우회 시도 차단
- [`owasp-top10`](../owasp-top10/SKILL.md) — A04 Insecure Design, A07 인증 실패
- [`threat-modeling`](../threat-modeling/SKILL.md) — 공격자 관점 시나리오 도출
- `/architecture:high-traffic-design` — CDN/Edge 에서의 선차단
