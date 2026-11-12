---
name: media-streaming
description: "라이브 스트리밍과 DRM — 프로토콜 선택, ingest, live transcoding·ABR, 콘텐츠 보호, CDN multi-tier, Live→VOD 변환, 비용. Use when 실시간 방송이나 보호 콘텐츠 전송을 구축할 때, 정적 업로드는 media-handling 을 쓴다."
license: MIT
---

# Media Streaming — 라이브 + DRM

라이브 방송 + 보호 콘텐츠 스트리밍 패턴. VOD/이미지/EXIF/SSRF는 [`business/media-handling.md`](../media-handling/SKILL.md) cover. 이 skill은 **실시간 라이브 + DRM**에 집중.

> 핵심 결정: (1) 프로토콜 (LL-HLS vs WebRTC), (2) Ingest (RTMP vs SRT vs WebRTC), (3) DRM 적용 여부, (4) Self-host (origin server) vs SaaS (Mux/Livepeer/AWS IVS).

## When to Use

- 실시간 강의/교육 (낮은 latency 필요, 채팅 동기화)
- 스포츠/게임 라이브 중계 (10K~1M 동시 시청)
- 비디오 컨퍼런싱 (1:1 ~ N:M)
- B2C 라이브 커머스 (한국 특화)
- 영상 콘텐츠 보호 (Premium/유료 영상 → DRM)
- Live → VOD 자동 변환 + replay
- CCTV / 모니터링 스트림

**관련 skill (cross-link)**:
- `business/media-handling.md` — VOD/이미지/문서 (이 skill의 짝)
- `business/subscription-billing.md` — premium 콘텐츠 구독
- `business/credit-system.md` — pay-per-view, 시청 시간 과금
- `business/rate-limiting.md` — concurrent stream cap
- `business/audit-log.md` — 시청 로그 (저작권 추적)
- `infrastructure/aws-cloudfront.md` (있을 시) — CDN
- `observability/observability-cost.md` — egress 비용 추적

---

## 프로토콜 선택 결정 트리

```
유즈케이스?
    │
    ├─ < 500ms latency 필수 ─────> WebRTC (1:1, 회의, 화상)
    │   - 또는 LL-HLS (글로벌 1:N, 2~5초 latency)
    │
    ├─ 1:N broadcast (10K+ 시청자) ─> LL-HLS (Apple) 또는 LL-DASH
    │   - HLS는 표준, iOS native 지원
    │   - DASH는 Android/web 우선
    │
    ├─ Legacy compatibility ──────> RTMP (Flash 시대 잔재, OBS 표준)
    │   - 송출자 입력 (Ingest) 용도. 시청자 직접 RTMP는 비권장
    │
    ├─ 손실 환경 (위성/장거리) ────> SRT (Secure Reliable Transport)
    │   - 방송사/프로 송출 표준
    │
    └─ 저비용 1:1 ─────────────────> WebRTC P2P (TURN 서버 비용만)
```

### Latency 비교

| 프로토콜 | latency | 시청자 규모 | 표준 |
|---|---|---|---|
| **WebRTC** | < 500ms | 1:1 ~ 1:100 | 회의, 인터랙티브 |
| **LL-HLS** | 2~5s | 1:1M+ | Apple HLS Low-Latency Extension |
| **LL-DASH** | 2~5s | 1:1M+ | MPEG-DASH CMAF |
| **HLS (legacy)** | 10~30s | 1:1M+ | 안정성 우선 시청 |
| **RTMP (ingest)** | 1~3s | 송출 입력만 | OBS/송출 도구 |
| **SRT** | 200ms~2s | 송출 + 분배 | 방송 프로 표준 |

---

## StreamingGateway 추상화 (Gateway 패턴 6번째)

```
interface StreamingGateway {
    createLiveStream(tenantId, opts) -> Stream(id, ingestUrl, playbackUrl, streamKey)
    startBroadcast(streamId)
    endBroadcast(streamId) -> Recording (Live → VOD)
    getViewerCount(streamId) -> int
    getSimulcastTargets(streamId) -> Target[]   // YouTube, Twitch 등 동시 송출
}

implementations:
    AWSIVSGateway          // AWS Interactive Video Service (관리형 LL-HLS)
    MuxGateway             // Mux.com (관리형 + analytics)
    LivepeerGateway        // 분산 transcoding
    SelfHostedGateway      // nginx-rtmp + ffmpeg + S3 + CloudFront
```

**부트스트랩**: AWS IVS / Mux로 시작 → 트래픽/비용 임계 도달 시 self-host.

---

## Ingest (송출자 입력)

### RTMP (가장 보편)

```
OBS Studio / FFmpeg 등 송출 도구
    │
    └─> rtmp://ingest.example.com/live/{stream_key}
            │
            └─> Origin server (nginx-rtmp 또는 AWS MediaLive)
                    │
                    └─> Transcode → LL-HLS / DASH 출력
```

- stream_key는 인증 토큰 역할 (URL에 노출되므로 단명 + scope)
- TLS 안 됨 (RTMPS는 RTMP over TLS, 권장)

### SRT (프로 방송)

- 손실 네트워크에서 reliable
- 비트레이트 보장 (FEC + 재전송)
- AWS MediaConnect, Wowza 지원

### WebRTC Ingest (WHIP)

- 새로운 표준 (RFC), 브라우저에서 직접 송출
- HTTPS POST로 SDP 교환 → 즉시 ingest
- OBS도 WHIP 지원 시작 (2026)

### Ingest 인증 패턴

```
1. UI에서 "방송 시작" 클릭
2. Backend: stream_key 생성 (TTL 24h, single-use)
3. Backend: rtmp_url + stream_key 반환
4. 송출 도구가 이 URL로 connect
5. Origin server: stream_key 검증 (Backend API 콜)
6. 만료된 key는 즉시 disconnect
```

stream_key는 평문 노출되므로 **single-use + 짧은 TTL** 필수.

---

## Live Transcoding + ABR

```
Original ingest (1080p60, 8Mbps H.264)
    │
    └─> ffmpeg/MediaLive/IVS encoder
            ├─> 1080p (5Mbps)
            ├─> 720p  (3Mbps)
            ├─> 480p  (1.5Mbps)
            └─> 240p  (500Kbps)

Player가 네트워크 상황에 따라 자동 switching (HLS 매니페스트가 모든 bitrate 알림)
```

### 인코딩 옵션

- **CPU**: ffmpeg libx264, AWS MediaLive standard
- **GPU**: NVIDIA NVENC (10x faster, 약간 quality 낮음)
- **AV1 (next-gen)**: 30% 압축률 ↑ but 인코딩 비용 ↑↑ (실시간 어려움, 2026 GPU 가속 도래)

### 코덱 호환성

| 코덱 | iOS | Android | Web | 비용 |
|---|---|---|---|---|
| **H.264** | ✅ | ✅ | ✅ | 표준, low |
| **H.265 / HEVC** | ✅ (iOS 11+) | ✅ (대부분) | ✅ Safari, 부분 Chrome | 라이센스 fee |
| **AV1** | ✅ (iOS 17+) | ✅ (신형) | ✅ Chrome 90+ | royalty-free, 인코딩 비싸 |
| **VP9** | ❌ | ✅ | ✅ Chrome | YouTube 표준 |

→ **부트스트랩은 H.264 only**. 트래픽 + cost 분석 후 H.265/AV1 추가.

---

## DRM (Premium 콘텐츠 보호)

```
3대 DRM 시스템 (단일 콘텐츠가 모두 지원해야 cross-platform)

           Widevine          PlayReady          FairPlay
플랫폼     Android, Chrome   Edge, Xbox         iOS, Safari, tvOS
공급자     Google            Microsoft          Apple
포맷       CENC (CBCS)       CENC (CBCS)        CBCS (only)

→ CMAF + CBCS encryption 으로 단일 manifest로 3 DRM 모두 처리 가능
```

### DRM 흐름

```
1. License server (자체 또는 SaaS):
   - JWT/session 검증
   - 시청 권한 확인 (구독, 결제 완료 등)
   - 콘텐츠 키 발급 (단명, IP/디바이스 제한)
2. Player (Shaka Player, Video.js, AVPlayer):
   - 매니페스트 fetch
   - 첫 segment에 DRM 정보 (PSSH box) → license server에 challenge
   - license + 콘텐츠 키 받아 복호화 + 재생
3. 시청 종료 또는 idle 시 키 폐기
```

### DRM Provider

- **Self-host**: Shaka Packager + 자체 license server (복잡, 노력 大)
- **AWS Elemental MediaPackage + DRM**
- **Google Widevine Cloud License**
- **EZDRM, BuyDRM** (전문 SaaS, $0.01~0.05/license)
- **Mux Stream**, **Vimeo OTT** (all-in-one)

### DRM 안 쓰는 보호

- HLS encryption AES-128 (간단, 키 노출 위험)
- Token-authenticated CDN URL (단명 signed URL)
- IP allowlist (corporate)

→ Premium ($/월) 콘텐츠 외엔 token-authenticated URL로 충분.

---

## CDN Multi-tier (Origin Shield)

```
Origin (transcoded segments)
    │
    └─> Origin Shield (regional cache, 1~3대)
            │
            └─> Edge POPs (글로벌 100+)
                    │
                    └─> 시청자
```

- **Origin Shield**: origin 부하 ↓ (cache hit 90%+ 회수)
- **Edge POPs**: 시청자 가장 가까운 위치
- **Hot-spot**: 동시 1M+ 시청 시 single edge가 폭발 — Multi-CDN 또는 P2P 보조

### Multi-CDN

- 한국: 네이버/KT + 글로벌 CloudFront/Fastly
- 망내 latency 최적화 + 글로벌 fallback
- 자세한 CDN 비교: [`business/media-handling.md`](../media-handling/SKILL.md) §Provider 매트릭스

### P2P Streaming (대규모 라이브)

- WebRTC datachannel로 시청자끼리 chunk 공유
- StreamRoot, Peer5 (Microsoft) — egress 비용 30~70% ↓
- 트래픽 1M+ 동시 시청 시 ROI 강함

---

## Live → VOD 자동 변환 (Archiving)

```
방송 종료 시점:
1. Origin server: stream segment 모두 S3로 flush
2. ffmpeg concat: HLS segments → mp4 (또는 HLS playlist 그대로)
3. media-handling Asset 테이블에 INSERT (recording_id)
4. Variant 생성 (1080p, 720p, 480p)
5. CDN URL 발급 (signed)
6. UI에 "다시보기" 버튼 활성화
```

`business/media-handling.md` Asset/Variant 모델 재사용. Live → VOD 흐름은 단순 archiving.

### 보관 정책

- 라이브 직후: 7일 무료 보관 (replay 핫)
- 7일 후: cold storage (Glacier / 네이버 Archive)
- 청소년 콘텐츠: PIPA 14세 미만 보관 제한 (`/security:child-data-protection`)

---

## 한국 시장 깊이

### 한국 라이브 시장 특수성

- **라이브 커머스 폭발** — 카카오쇼핑LIVE, 네이버 SHOPPING LIVE (2026 5조원 시장)
- **저지연 요구** — 라이브 채팅과 영상 sync (chat lag → UX 폭망). LL-HLS 2초 미만 필수
- **모바일 우선 시청** — iOS 50%+, 망내 latency 결정적
- **앱스토어 정책** — Apple In-App Purchase (콘텐츠 구독 30% 수수료)

### 한국 CDN

| Provider | 망내 latency | 가격 (1TB) | DRM 통합 |
|---|---|---|---|
| **Naver Cloud CDN+** | 네이버 < 30ms, KT < 50ms | ₩90~120K | ✅ |
| **KT Olleh CDN** | KT < 20ms | ₩80~110K | ✅ |
| **CloudFront** | 글로벌 평균 50~80ms | $85 | ✅ MediaPackage |
| **Cloudflare Stream** | 글로벌 50~70ms | $1/1K minutes | ✅ |

→ **국내 사용자 90%+ 시 네이버/KT, 글로벌 mix면 multi-CDN**.

### 망사용료 분쟁 (2024~)

- 한국 정부: 콘텐츠 사업자가 ISP에 망 사용료 지불 의무 검토
- 글로벌 CDN으로 우회 시 정부 규제 가능성 — 한국 트래픽은 한국 CDN 권장

### PIPA + 위치정보법

- 시청 로그 (IP/디바이스) PII 가능 → 마스킹 + 30일 retention
- 위치 기반 라이브 (예: GPS-trigger broadcast) → 위치 정보 처리 동의 의무
- 자세한 법령: `/security:kr-location-info-act`, `/security:data-subject-rights`

### 청소년 보호

- 19세 미만 콘텐츠는 본인인증 + 시청 시간 제한
- 라이브 송출자 검증 (실명 KYC)

---

## 비용 (egress 절대 강자)

```
1만 시청자 × 1080p 5Mbps × 1시간 라이브 =
  1만 × 5Mbps × 3600초 × 1/8 byte =
  22.5 TB egress
  
CloudFront:  $1,910 (한 시간 방송)
네이버 CDN:  ₩2,025K (~$1,500)
Cloudflare:  포함 (구독 모델)
```

### 비용 최적화

1. **AV1/H.265** — 30% bitrate ↓ (단 인코딩 비용 ↑)
2. **ABR 적극** — 모바일은 480p로 자동 (대부분 충분)
3. **Multi-CDN** — 한국 트래픽은 국내 CDN, 글로벌은 CloudFront
4. **P2P (StreamRoot)** — 30~70% egress ↓ (1M+ 시청 시 ROI)
5. **Replay 캐싱** — Live → VOD CDN cache 90%+ hit
6. **시청자 cap** — 무료 ≤ N명, premium 이상 추가

분기 비용 추적: `/observability:observability-cost`, `/dx:quarterly-review`.

---

## 안티패턴

| 안티패턴 | 왜 나쁜가 | 대신 |
|---|---|---|
| RTMP 시청자 directing | Flash 종료, mobile 미지원 | 시청은 LL-HLS / DASH |
| 단일 bitrate | 모바일 끊김 | ABR (4 ladder 이상) |
| Stream key 영구 발급 | 재사용 → 도용 | TTL 24h + single-use |
| TLS 없는 RTMP ingest | 네트워크 sniff | RTMPS / SRT / WHIP |
| DRM 없는 premium 콘텐츠 | 다운로드 → 유포 | 3 DRM (Widevine/PlayReady/FairPlay) + CMAF CBCS |
| Origin 직접 노출 | 부하 폭발 | CDN + Origin Shield 필수 |
| Single-CDN 글로벌 라이브 | 한 region 다운 시 전체 다운 | Multi-CDN failover |
| Live recording 동기 처리 | 방송 끝 → UI 멈춤 | async archiving worker |
| 시청 로그에 IP 풀로 저장 | PIPA / GDPR 위반 | 마스킹 + 30일 |
| HLS segment TTL 무한 | CDN 비용 폭발 | live segment 1분, archived 1년 |
| Hot-spot 무대응 | edge OOM, 시청 실패 | rate limit + autoscale + P2P |
| 단일 코덱 (AV1만) | iOS legacy 재생 불가 | H.264 fallback 의무 |
| License server 인증 단순 (token만) | 탈취 시 무한 시청 | device binding + IP rotation 감지 |
| Replay 영상도 라이브 CDN으로 | 단명 cache, 비용 ↑ | VOD CDN으로 분리 (다른 cache 정책) |
| 글로벌 CDN으로 한국 사용자 처리 | 망사용료 분쟁 + latency | 국내 CDN 우선 |

---

## ADR 템플릿 (Self-host vs SaaS)

```markdown
## Context
- 동시 시청자: N명 (peak)
- 방송 빈도: M/일
- 한국 vs 글로벌 비율: ...
- DRM 필요: yes/no
- 예산: $/월

## Options
A. AWS IVS (관리형 LL-HLS, $1~$3/시간 + viewer)
B. Mux Stream (analytics 우수, $0.04/min ingest + delivery)
C. Self-host (nginx-rtmp + ffmpeg + S3 + CloudFront, ops 大)
D. Cloudflare Stream (단순, $1/1K min)

## Decision
[선택] 이유: ...

## Consequences
- 운영 부담: ...
- DRM 비용: ...
- 한국 시청자 latency: ...
- migration cost: StreamingGateway 추상화로 ...

## Predicted Outcomes
- 시청 startup time < 3s
- buffering rate < 0.5%
- 비용 < $X/월 at N viewer
- LL-HLS p95 latency < 5s

## Review Schedule
- Tier 1, 6개월 (트래픽 5x 시 즉시)
```

`/dx:adr-retrospective` 참조.

---

## Quick Start (1주 부트스트랩)

```
1. AWS IVS 또는 Mux 가입 (관리형 시작)
2. StreamingGateway 인터페이스 정의
3. UI: "방송 시작" → API → ingestUrl + playbackUrl 발급
4. OBS 연결 (RTMP), 송출 테스트
5. Player 통합: Video.js / hls.js (LL-HLS 활성)
6. 시청 페이지: 채팅 (WebSocket) + 영상 sync
7. 방송 종료 시 자동 archiving → media-handling Asset
8. CDN signed URL (시청 권한 검증)
9. Grafana: 동시 시청자, ingest bitrate, error rate, egress 비용
10. 트래픽 100K+ 시 self-host 또는 multi-CDN 평가
```

---

## 다음 단계 (After Adoption)

- DRM 통합 (premium 콘텐츠) — Widevine/FairPlay 단계적
- Multi-CDN orchestration (한국 + 글로벌)
- 라이브 채팅 sync (Redis pub/sub + WebSocket)
- 시청자 분석 (CDN log → analytics warehouse)
- Simulcast (동시 송출 to YouTube/Twitch) — 마케팅 용
- WebRTC ingest (WHIP) — 브라우저 직접 송출
- AV1 / H.265 for cost reduction
- P2P streaming for hot events
- Live commerce 통합 (`business/payment-integration.md` + 라이브 결제)

---

## 관련 자원

- Apple HLS Authoring Spec — LL-HLS 표준
- W3C WebRTC standards
- "Streaming Systems" (O'Reilly) — 분산 미디어 처리
- AWS IVS / MediaPackage docs
- Mux blog — 운영 사례 (encoding, ABR ladder)
- 네이버 클라우드 미디어 streaming 가이드
- 카카오쇼핑LIVE 기술 블로그 — 한국 라이브 커머스 사례
- Shaka Player docs — DRM client 통합
