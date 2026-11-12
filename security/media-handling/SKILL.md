---
name: media-handling
description: "미디어 자산 처리 — presigned URL 직접 업로드, 변환 파이프라인, CDN 배포, EXIF·SSRF·transcoding DoS 방어, 만료 관리. Use when 이미지·영상·문서 UGC 업로드와 저장·배포 구조를 설계할 때."
license: MIT
---

# Media Handling — 미디어 자산 업로드/변환/배포

이미지·영상·문서 등 **사용자 제출 자산(UGC) + 시스템 생성 자산**의 업로드, 변환, 저장, CDN 배포, 만료 관리. SaaS 부트스트랩에서 의외로 큰 attack surface — SSRF, EXIF GPS 유출, transcoding DoS, hot-link 비용 폭탄, 한국 정통망법 미이행이 한꺼번에 터진다.

> **이 skill은 미디어 파이프라인 hub.** 결제는 `payment-integration.md`, 사용량 과금은 `credit-system.md`. 이 문서는 **자산 메타데이터 + 변환 파이프라인 + CDN 배치 + 보안 + 한국 규제**의 도메인 모델과 함정에 집중.

## When to Use

- UGC 업로드 (프로필 이미지, 게시물 첨부, 동영상)
- 시스템 생성 자산 (PDF 영수증, OG 이미지, 썸네일)
- 라이브/VOD 스트리밍 (HLS/DASH)
- 이미지·영상 on-the-fly 변환 (`?w=300&q=80`)
- 한국 시장 진출 시 정통망법 차단 의무 / 망내 CDN 결정
- "S3 + CloudFront로 시작했는데 egress가 월 $5,000 나옴" 비용 분석
- 사용자 1명이 4K mp4 100개 업로드해서 DoS 발생

**관련 skill (cross-link)**:
- `business/payment-integration.md` — 충전·결제 (storage 비용 추적은 `credit-system`)
- `business/credit-system.md` — 사용량 모네타이징 (저장/변환 단가 차감)
- `business/audit-log.md` — 자산 업로드/삭제 immutable 로그
- `business/multi-tenancy.md` — tenant 단위 storage quota
- `business/rate-limiting.md` — 업로드 RPS / 동시 transcoding 제한
- `business/notification-multichannel.md` — 변환 완료 webhook
- `security/owasp-top10.md` §A05/A07/A10 — SSRF / Identification / Server-side
- `infrastructure/aws-s3-cloudfront.md` — S3/CloudFront 운영
- `cicd/cdn-purge-strategies.md` — variant 갱신/무효화

**관련 agent**: `tech-lead` (Provider/CDN ADR), `cost-analyzer` (egress/storage 추적), `security-scanner` (SSRF/EXIF 검증)
**관련 skill**: `/infra:postgresql-operations` (asset 테이블 파티셔닝), `/messaging:broker-troubleshooting` (transcoding 큐)

---

## 1. 패턴 결정 매트릭스

| 차원 | 옵션 A | 옵션 B | 권장 |
|---|---|---|---|
| 업로드 경로 | **Direct (presigned URL)** | App proxy (multipart→S3) | A — 앱 서버 메모리/대역 절감, 동시성 ∞ |
| 변환 시점 | **Async (queue + worker)** | Sync (요청 시 변환) | A — 4K 영상 30초 transcoding 동기 호출 금지 |
| URL 모델 | **Signed URL (만료)** | Public bucket | A — hot-link 차단, 토큰 만료 정책 |
| 변환 트리거 | **On-the-fly (CDN 통과)** | Pre-bake (워커가 모든 variant 생성) | 혼합 — 핵심 variant pre-bake + 나머지 lazy |
| 영상 인코딩 | **HLS/DASH adaptive** | Single mp4 progressive | A 모바일 가변 망 (3G→5G→Wi-Fi) |
| 메타 추출 | **외부 워커 (libvips/ffprobe)** | DB 트리거 | A — RDS CPU 보호, 비동기 |

**원칙**:
- **Direct upload + presigned URL**이 2026 표준. App proxy는 50MB+ 영상에서 메모리 폭발/타임아웃
- Sync 변환은 **이미지 < 1MB만** (썸네일). 영상/RAW는 무조건 async
- **모든 자산은 immutable** (URL = `assets/{id}/{variant}.{ext}`). 갱신 = 새 ID 발급, CDN purge 불필요

---

## 2. Provider 비교 (2026-Q2 기준)

| 항목 | AWS S3 + CloudFront | Cloudflare R2 | GCS + Cloud CDN | Naver Cloud CDN+ | KT Cloud / 토스 CDN |
|---|---|---|---|---|---|
| Storage (Standard) | $0.023/GB | **$0.015/GB** | $0.020/GB | ₩30/GB (~$0.022) | KT: ₩28/GB |
| Egress (~10TB/월) | $0.085/GB | **$0** | $0.12/GB | 망내 무료 / 글로벌 별도 | 망내 무료 |
| Operations | PUT $0.005/1k | PUT $0.36/M | $0.005/1k | 별도 정액 | 별도 정액 |
| Cold storage | **Glacier Deep $0.00099/GB** | 15× R2 Std | Coldline $0.004/GB | 미지원 | 미지원 |
| 한국 망내 latency | 글로벌 PoP, ~30ms | ~25ms (서울 PoP) | 글로벌 PoP | **<10ms (KT/SKT/LGU+ 망내)** | <10ms |
| S3 호환 API | 100% | **100%** | XML API 일부 | 부분 | 부분 |
| 정통망법 이미지 차단 (2026-07) | 직접 구현 | 직접 구현 | 직접 구현 | **Naver SafeStream 결합 가능** | 자체 필터 |

**결정 가이드**:
- Egress 폭탄 위협 (10TB+/월) → **R2** ($0 egress가 본질적 차이)
- 글로벌 cold archive (사진 백업 SaaS) → **S3 Glacier Deep Archive** (15× 저렴)
- 한국 트래픽 80%+ → **Naver Cloud CDN+ 또는 KT/토스 망내** (latency + egress 비용)
- 비용 폭탄 사례: 10TB 저장 + 50TB egress = R2 $150/월 vs S3 $4,730/월

---

## 3. StorageGateway 추상화

`subscription-billing.md` SubscriptionGateway / `credit-system.md` CreditGateway와 짝이 되는 패턴.

```
StorageGateway (interface)
  ├─ presign_upload(asset_id, content_type, max_bytes, ttl_sec) → PresignedUrl
  ├─ presign_download(asset_key, ttl_sec, ip_lock?) → SignedUrl
  ├─ head(asset_key) → AssetMeta{size, etag, content_type, custom_metadata}
  ├─ delete(asset_key)
  ├─ copy(src_key, dst_key)             # variant 생성, immutable 보장
  └─ list_by_prefix(prefix, page_token) → list[AssetMeta]

Adapters:
  ├─ S3Adapter           # boto3 / aws-sdk
  ├─ R2Adapter           # S3 호환 (endpoint=https://<account>.r2.cloudflarestorage.com)
  ├─ GCSAdapter          # google-cloud-storage
  ├─ NaverObjectAdapter  # S3 호환 (endpoint=kr.object.ncloudstorage.com)
  └─ HybridAdapter       # 한국 트래픽 → Naver, 글로벌 → R2 (region 라우팅)
```

**원칙**: 도메인 코드는 `StorageGateway`만 의존. R2/Naver 전환 시 어댑터만 교체. **YAGNI 경고**: 단일 Provider면 추상화 보류 — 두 번째 region/provider 도입 직전이 최적 시점.

---

## 4. 도메인 모델

```
Asset (immutable, append-only)
  ├─ id                    (ULID, 시간순 정렬)
  ├─ tenant_id             (multi-tenancy 격리)
  ├─ owner_id              (uploader user)
  ├─ kind                  (image / video / audio / document)
  ├─ original_key          (S3 key, immutable)
  ├─ original_bytes
  ├─ original_mime         (서버 검증된 값, 클라이언트 신뢰 X)
  ├─ checksum_sha256       (중복 검출, 변조 감지)
  ├─ width, height         (image/video)
  ├─ duration_ms           (video/audio)
  ├─ exif_stripped_at      (GPS/카메라 메타 제거 시점)
  ├─ status                (uploading / processing / ready / quarantined / deleted)
  ├─ created_at, deleted_at
  └─ retention_until       (정통망법/GDPR 보존 기한)

Variant (Asset → 1:N, immutable)
  ├─ id
  ├─ asset_id
  ├─ kind                  (thumbnail / hls_720p / pdf_preview)
  ├─ key
  ├─ params                (JSON: {w:300, q:80, format:avif})
  ├─ bytes, mime
  └─ created_at

UploadIntent (presigned URL 발급 시점)
  ├─ id
  ├─ asset_id              (선할당)
  ├─ presigned_url
  ├─ max_bytes, allowed_mime[]
  ├─ expires_at            (TTL 5~15분)
  └─ completed_at          (S3 ObjectCreated 이벤트 수신 시점)
```

**핵심 원칙**:
- **immutable** — Asset/Variant 콘텐츠 변경 금지. "수정"은 새 Asset 발급. URL 캐시 무한
- **selected MIME = 서버 검증값** — 클라이언트 `Content-Type` 절대 신뢰 금지 (MIME sniffing)
- **checksum_sha256** — 중복 자산 dedup + 변조 감지 + GDPR 삭제 추적
- **retention_until** — 정통망법(불법촬영물 7일 차단), GDPR 우회 금지

---

## 5. Direct Upload — Presigned URL 의사코드

```python
# upload_intent.py
def create_upload_intent(
    user: User,
    tenant: Tenant,
    content_type: str,
    declared_bytes: int,
    purpose: str,                    # avatar / post_attach / video
) -> UploadIntent:
    # 1) 정책 검증 (사용자 신뢰 X)
    if content_type not in ALLOWED_MIME[purpose]:
        raise ValidationError(f"unsupported mime {content_type}")
    max_bytes = QUOTA[purpose][tenant.plan]      # avatar 5MB, video 500MB
    if declared_bytes > max_bytes:
        raise QuotaExceeded(...)

    # 2) Tenant storage quota 확인 (rate-limiting + multi-tenancy 결합)
    if tenant.storage_used + declared_bytes > tenant.storage_limit:
        raise QuotaExceeded("tenant storage")

    # 3) Asset 선할당 (status=uploading)
    asset = Asset.create(
        tenant_id=tenant.id, owner_id=user.id,
        kind=KIND_FROM_MIME[content_type],
        original_mime=content_type,         # 임시값, 업로드 후 서버 검증
        status="uploading",
    )

    # 4) Presigned URL 발급 (Conditions로 강제 제약)
    presigned = storage.presign_upload(
        key=f"raw/{tenant.id}/{asset.id}",
        content_type=content_type,
        content_length_range=(1, max_bytes),  # S3 PUT-style, R2도 동일
        ttl_sec=600,                          # 10분
        sse="AES256",
        conditions={
            "x-amz-meta-tenant-id": tenant.id,
            "x-amz-meta-asset-id":  asset.id,
        },
    )
    return UploadIntent(asset.id, presigned, expires_at=now()+600)


# webhook_s3_object_created.py — S3/R2 ObjectCreated 이벤트
def on_object_created(event: S3Event):
    asset_id = event.metadata["asset-id"]
    asset = Asset.get(asset_id)
    if asset.status != "uploading":
        return     # idempotent: 재전송 무시

    # 5) 서버 측 검증 (클라이언트 신뢰 0)
    head = storage.head(event.key)
    real_mime = sniff_mime(head)          # libmagic/file 명령으로 실제 시그니처 확인
    if real_mime != asset.original_mime:
        asset.update(status="quarantined")     # MIME sniffing 공격 차단
        return

    # 6) async 처리 큐 적재 (transcoding/EXIF 제거/AV 스캔)
    asset.update(status="processing", original_bytes=head.size, checksum=head.etag)
    queue.publish("media.process", {"asset_id": asset.id})
```

**핵심 함정**:
- `Content-Length` 검증 — 클라이언트 declared_bytes만 믿으면 50GB 업로드 가능 → S3 `content-length-range` Condition 필수
- TTL 5~15분 — 너무 길면 토큰 탈취·재사용 위협
- `x-amz-meta-*` 메타 — 신뢰 가능한 사용자 식별자 (Pre-signed에 서명 포함)
- `quarantined` 상태 — 삭제 X, 보안팀 검토용 보관 (정통망법 차단 대상은 별도 격리 버킷)

---

## 6. 변환 파이프라인 의사코드

```python
# media_processor.py — async worker (Kafka/SQS consumer)
def process_asset(asset_id: str):
    asset = Asset.get_for_update(asset_id)
    if asset.status != "processing":
        return     # idempotent

    # 1) 다운로드 (워커 격리 환경, 임시 디스크)
    src = storage.get(asset.original_key, max_bytes=ABSOLUTE_LIMIT)

    # 2) AV 스캔 (ClamAV / cloudmersive) — 정통망법 핵심
    if not antivirus.scan(src):
        asset.update(status="quarantined")
        audit_log("asset.quarantined", asset_id, reason="av_positive")
        return

    # 3) EXIF/메타 제거 — GPS 좌표 유출 차단
    if asset.kind == "image":
        src = libvips.copy(src).remove_exif()    # 또는 sharp().rotate().withMetadata({})
        asset.exif_stripped_at = now()

    # 4) 정통망법 2026-07 — 불법촬영물 hash DB 매칭 (이미지 + 동영상)
    if perceptual_hash_match(src, kisa_blocklist):
        asset.update(status="quarantined", retention_until=now()+7*DAY)
        notify_kisa_compliance(asset_id)
        return

    # 5) Variant 생성 (immutable, key = key=variants/{asset_id}/{kind})
    variants = []
    if asset.kind == "image":
        for spec in [VariantSpec(w=300, q=80, fmt="avif"),
                     VariantSpec(w=1200, q=85, fmt="webp"),
                     VariantSpec(w=300, q=85, fmt="jpeg")]:    # AVIF 미지원 폴백
            v = libvips.thumbnail(src, spec).save_buffer()
            key = f"variants/{asset.id}/{spec.kind_str()}"
            storage.put(key, v, content_type=spec.mime, immutable_cache=True)
            variants.append(Variant.create(asset.id, spec, key, len(v)))
    elif asset.kind == "video":
        # ffmpeg HLS adaptive bitrate (240p/480p/720p/1080p)
        hls_dir = ffmpeg_hls_abr(src, profiles=[HLS_240, HLS_480, HLS_720, HLS_1080])
        upload_directory_to_storage(hls_dir, prefix=f"variants/{asset.id}/hls/")
        variants.append(Variant.create(asset.id, kind="hls_master", key=...))

    # 6) 상태 ready + webhook
    asset.update(status="ready", width=src.width, height=src.height)
    Variant.bulk_create(variants)
    webhook.publish("asset.ready", asset_id)
```

**핵심 함정**:
- **EXIF 제거는 image kind만 충분치 않음** — mp4 GPS 메타도 제거 (`ffmpeg -map_metadata -1`)
- **AV 스캔 실패 fallback** — ClamAV 다운 시 fail-close (quarantine) vs fail-open (정책 결정)
- **AVIF 폴백** — Safari < 16, IE 미지원. 항상 jpeg/webp 동시 생성
- **HLS 재인코딩 비용** — 4K 30초 영상이 1080p로 4× CPU 소모. 동시성 cap + transcoding queue

---

## 7. CDN 배치 — 한국 시장 깊이

### Provider별 배치 전략

| 시나리오 | 권장 |
|---|---|
| 한국 트래픽 70%+ | **Naver CDN+ (망내) + Global CDN (해외용)** — 망내 latency <10ms, 망내 egress 무료 |
| 글로벌 SaaS | **Cloudflare R2 + Cloudflare CDN** — egress $0, 200+ PoP |
| KT/SKT/LGU+ 모바일 트래픽 | **KT Cloud CDN 또는 토스 CDN** — 망내 라우팅 비용 절감 |
| 공공/금융 (망분리) | **Naver Cloud Public Sector** — 정부 클라우드 보안 인증 |

### Naver CDN+ 통합 패턴

- Object Storage(`kr.object.ncloudstorage.com`, S3 호환) → CDN+ origin 자동 연동
- **Image Optimizer** — Naver 자체 on-the-fly 변환 (`?type=w300_q80`), libvips 직접 운영 회피
- **SafeStream** — 정통망법 불법촬영물 hash 매칭 ASP (자체 hash DB 운영 비용 회피)
- 비용 예시: 1TB 망내 egress = ₩40,000~80,000 (CloudFront $85 대비 1/3)

### Cache Key & Hot-link 차단

- 캐시 키에 `?w=300&q=80` 포함 — variant 폭발 방지 위해 화이트리스트 (`w∈{300,800,1200}`만 허용)
- `Referer` 검사로 hot-link 차단 (간단), `Signed URL + ip_lock`으로 결정적 차단 (강함)
- TTL: variant `Cache-Control: immutable, max-age=31536000`, master는 `s-maxage=300`

---

## 8. 보안 (필수)

### SSRF (Server-Side Request Forgery)

- 사용자 제출 URL 다운로드(예: "이 URL의 이미지를 가져와 변환")는 SSRF 무덤
- **Whitelist 도메인만 허용** + DNS 재바인딩 방어 (해석된 IP가 사설 대역(`10.0.0.0/8`, `169.254.0.0/16`, IPv6 link-local)이면 거부)
- AWS: `IMDSv2` enforce (`HttpTokens=required`, `HttpPutResponseHopLimit=1`) — IMDS 토큰 탈취 차단
- 워커는 **별도 VPC + outbound NAT 화이트리스트**로 격리

### Presigned URL 보안

- TTL 5~15분 — 토큰 탈취 시 노출 시간 최소화
- `Content-Length-Range`, `Content-Type` Condition 필수 — 50GB 업로드/jpeg 위장 mp4 차단
- VPC endpoint 우회 가능성 — Presigned URL은 IP 기반 정책을 우회. **bucket policy로 `aws:VpcSourceIp` 추가 검증**
- 다운로드용 Signed URL은 IP lock + Referer 검증 (특히 결제 영수증 등 민감 자산)

### MIME Sniffing

- 클라이언트 `Content-Type` **절대 신뢰 금지** — 업로드 후 `libmagic`/`file` 명령으로 시그니처 확인 (의사코드 §5)
- 응답 헤더 `X-Content-Type-Options: nosniff` 필수 (브라우저 자체 sniffing 차단)
- SVG 업로드 → XSS — `<script>` 포함 가능. 별도 sanitize (DOMPurify) 후 저장

### EXIF GPS / 메타데이터

- 이미지: `libvips.remove_exif()` 또는 `sharp().withMetadata({})` (rotate orientation은 보존)
- 영상: `ffmpeg -map_metadata -1`
- PDF: `qpdf --remove-metadata` (작성자/수정 이력)
- **DM 보낸 사진의 GPS로 사용자 위치 탈취** 사례 다수 — 기본 ON

### Anti-Virus / 격리

- ClamAV (오픈소스) 또는 Cloudmersive ASP — 워커 단계에서 스캔
- Quarantine 버킷은 **public 접근 절대 차단** + 별도 KMS 키
- 정책: `quarantined → 7일 후 자동 삭제 + 보안팀 알림`

### Hot-link / 비용 폭탄

- 4chan/Reddit에 1MB 이미지 링크 노출 → 일 100k 다운로드 → S3 egress $9 → 한 달 $270/이미지
- 방어: Signed URL + 짧은 TTL(1시간) + Referer 화이트리스트 + CDN 비용 알림 (월 임계치)

---

## 9. 한국 시장 깊이 (정통망법·개인정보보호법)

### 2026-07-01 — 불법촬영물 차단 의무 이미지 확대 ⚠️

- **전기통신사업법 §22-5②** 기술적·관리적 조치 대상이 동영상 → **이미지까지 확대**
- 모든 사용자 업로드 이미지를 **공개 이전 사전 검열** (perceptual hash DB 매칭)
- KISA 운영 hash DB 또는 SafeStream(Naver) 같은 ASP 활용
- 미이행 시 시정명령 + **2,000만 원 이하 과태료** + 부가통신사업자 등록 제재
- 적용 대상: 일정 규모 이상 SNS·UGC·온라인 스토어. 실질적으로 **모든 한국 향 SaaS 영향**

### 청소년 보호법 (청소년유해매체물)

- 청소년유해매체물 표시·포장 의무 (성인 인증 게이트)
- 본인인증(PASS/카카오/네이버) 결합 — `auth-oauth-social.md` 참조

### 개인정보보호법 — 위치정보·EXIF

- EXIF GPS는 개인정보(위치정보보호법 §2). 무단 수집·제3자 노출 시 과태료
- 자동 strip이 사실상 의무 (사용자 명시적 동의 외에는)

### 망 내 CDN (정책적 가성비)

- 한국 ISP는 **상호접속료(망 사용료)** 정책 — 외부 CDN egress 비용이 높음
- Naver/KT/SKT 망내 CDN은 ISP와 직접 협약 → 망내 트래픽 사실상 무료
- **B2C 한국 트래픽 80%+면 망내 CDN 필수 검토**

### 데이터 보존 / 삭제 의무

- 정통망법: 불법촬영물 차단 후 **7일 보존** (수사기관 협조 목적)
- 개보법: 사용자 탈퇴 시 즉시 파기 — **soft delete 후 N일 hard delete 워커**

---

## 10. 메트릭 / SLO

### 핵심 지표

| 지표 | 측정 | SLO 예시 |
|---|---|---|
| Upload success rate | `assets WHERE status IN (ready, processing) / total` | ≥ 99.5% |
| p95 transcoding latency (영상 1분) | worker span | ≤ 90s |
| CDN cache hit ratio | edge logs | ≥ 90% |
| Storage growth | `SUM(bytes) GROUP BY day` | 예측 곡선 ±20% |
| Egress / GB-month | 비용 알림 | 예산 80% 시 경고 |
| Quarantine rate | `WHERE status=quarantined / day` | < 0.1% (이상치 모니터) |

### 사용량 메트릭 SQL (`credit-system-metrics.md` 패턴 확장)

```sql
-- tenant별 일 평균 storage 사용량 (variant 포함)
SELECT
  tenant_id,
  date_trunc('day', created_at) AS day,
  SUM(original_bytes) FILTER (WHERE kind='image') AS image_bytes,
  SUM(original_bytes) FILTER (WHERE kind='video') AS video_bytes,
  COUNT(*) FILTER (WHERE status='quarantined') AS quarantine_cnt
FROM assets
WHERE deleted_at IS NULL
GROUP BY 1, 2;
```

CDN cost dashboard: Provider별 egress $/GB × 트래픽 합산 → 월 예측 곡선. R2 마이그레이션 ROI 자동 계산.

---

## 11. 안티패턴 (실제 사고 모음)

1. **클라이언트 MIME 신뢰** — `Content-Type: image/jpeg` 위장 mp4 → SVG XSS
2. **Public bucket 기본값** — 영수증 PDF 구글 검색 노출 사례 다수
3. **Presigned URL TTL 24시간** — 토큰 탈취 후 하루 종일 악용
4. **EXIF 보존** — DM 사진 GPS로 사용자 집 위치 노출
5. **Sync transcoding** — 4K 영상 업로드 1건이 API 서버 30초 점유 → 카스케이드 장애
6. **변환 결과 mutable 저장** — variant 키 재사용 → CDN purge 지옥
7. **AV 스캔 생략** — 멀웨어 .exe를 .jpg로 위장 배포
8. **정통망법 무시** — "글로벌 서비스니까 상관없어" → 한국 사용자 차단 + 과태료
9. **`?w=*&h=*` 무제한 variant** — 봇이 1만 가지 크기 요청 → 변환 비용 폭발
10. **Cold storage 미사용** — 1년 이상 미접근 자산도 Standard 보관 → 비용 5×
11. **Hot-link 미차단** — 4chan 트래픽 폭탄 → 월 egress $10,000
12. **Quarantine 자동 삭제** — 보안팀 검토 전 증거 인멸 / 정통망법 7일 위반

---

## 12. ADR 템플릿 (필수 결정)

- **Provider 선택**: S3 vs R2 vs Naver — egress 트래픽 패턴 + cold storage 필요성 + 한국 비중
- **변환 위치**: imgproxy 자체 운영 vs Naver Image Optimizer / Cloudflare Images / Mux
- **CDN 단일 vs 멀티**: 한국+글로벌 분리 라우팅 ROI vs 운영 복잡도
- **AV 스캔 fail 정책**: open vs close (사고 시 영향 vs 사용자 경험)
- **Variant 전략**: pre-bake all vs on-the-fly + cache vs 혼합
- **정통망법 ASP**: SafeStream 위탁 vs 자체 hash DB 운영
- **EXIF 정책**: 무조건 strip vs 사용자 동의 시 보존
- **Retention**: 사용자 탈퇴 시 즉시 hard delete vs N일 soft delete

각 ADR에 대안 비교표 + 정량 근거 (`rules/process/documentation.md` ADR 검증 규칙).

---

## 13. Quick Start

- [ ] StorageGateway 인터페이스 + S3Adapter 1개 (다른 어댑터는 두 번째 region 도입 시)
- [ ] `assets`, `variants`, `upload_intents` 테이블 + ULID
- [ ] Presigned URL 엔드포인트 — `content-length-range` Condition 필수
- [ ] S3 ObjectCreated 이벤트 → SQS/Kafka → worker
- [ ] worker: AV 스캔 → EXIF strip → 정통망법 hash 매칭 → variant 생성 → status=ready
- [ ] CDN 배치 + Cache-Control immutable + variant 화이트리스트
- [ ] Quarantine 격리 버킷 + 7일 자동 삭제 워커
- [ ] 메트릭: upload success / transcoding p95 / cache hit / storage growth / quarantine rate
- [ ] Cost 알림: 월 egress 예산의 80% 임계치
- [ ] 한국 트래픽 비중 측정 → 망내 CDN 도입 결정
- [ ] 정통망법 2026-07 시행 전 hash 매칭 ASP 통합
- [ ] EXIF strip 기본 ON 정책 + 사용자 안내
- [ ] Audit log: asset.created / quarantined / deleted (`audit-log.md` 패턴)
- [ ] DR: original_bytes는 Cross-Region Replication / R2 Replication 활성화

---

## 다음 단계

- 변환 큐가 폭주하면 → `messaging/kafka-patterns.md` (consumer lag/back-pressure)
- variant 키 정책 표준화 → `infrastructure/aws-s3-cloudfront.md`
- 사용량 청구 결합 → `business/credit-system.md` §1 Hybrid 모델 (저장/변환 단가 차감)
- 정통망법 hash DB 운영 deep-dive → 별도 `security/kr-content-compliance.md` 후보 (P2-D)
- Live streaming (LL-HLS, WebRTC ingest) → 별도 `media-streaming.md` 후보
