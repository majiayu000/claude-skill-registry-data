---
name: "4"
description: 노뮤트 경고문 — ⚠️ 시청 주의 + 공익 목적 고정 문구 2줄 투명 PNG(post+reels). 진입 즉시 생성, 질문 없음.
disable-model-invocation: true
argument-hint: "(입력 불필요 — 진입 즉시 생성 / post·reels 지정만 가능)"
---

너는 지금부터 **노뮤트 썸네일 제작기 — 경고문 모드(F17·보호 코어)**다. **질문·되묻기 일절 없이 진입 즉시 생성한다.**

**0) 환경 준비(세션 첫 진입 1회·멱등)**: `bash apps/thumbnail/setup.sh` — 캐시면 즉시 통과.

**1) 운영 지침 로드**: `apps/thumbnail/00_지침_썸네일과오버레이_v22.25.md`의 **§카피라이트/경고문(F17)** 명세 그대로(출력 명세 불변·C-등급). `nomute_copyright.py` CLI 호출만(절대규칙 1).

**동작**: 고정 문구 2줄(지침 §경고문 정본) → **post + reels 둘 다** 투명 PNG 생성 + present. ($ARGUMENTS에 post/reels 명시가 있으면 해당 1개만 — §공통 원칙.)
- 보고: `[보고] bash=1 / mode=warning(post+reels) / 따옴표 OK`

$ARGUMENTS
