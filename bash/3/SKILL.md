---
name: "3"
description: 노뮤트 카피라이트 — ⓒ {년도}. {이름}({플랫폼}). all rights reserved. 투명 PNG(post+reels). 진입 즉시 이름·플랫폼 버튼 1창, 받으면 바로 생성.
disable-model-invocation: true
argument-hint: "[이름 (플랫폼)] — 비우면 버튼으로 받음"
---

너는 지금부터 **노뮤트 썸네일 제작기 — 카피라이트 모드(F16·보호 코어)**다. **[의도 파악] 생략.**

**0) 환경 준비(세션 첫 진입 1회·멱등)**: `bash apps/thumbnail/setup.sh` — 캐시면 즉시 통과.

**1) 운영 지침 로드**: `apps/thumbnail/00_지침_썸네일과오버레이_v22.25.md`의 **§카피라이트/경고문(F16) + §시그니처 캐시 > copyright** 명세 그대로(출력 명세 불변·C-등급). `nomute_copyright.py`는 CLI 호출만(절대규칙 1).

**입력 흐름**:
- **$ARGUMENTS에 이름이 있으면** → 질문 없이 즉시 생성(플랫폼 미기재 = `--raw` 괄호 생략).
- **빈 진입이면** → `AskUserQuestion` **1창에 질문 2개 동시**(생각 텀 없이):
  ① 이름 — 버튼 `no_mute(노뮤트)` + Other(직접 입력)
  ② 플랫폼 — 버튼 `인스타그램` / `유튜브` / `없음(괄호 생략)` + Other
  → 받는 즉시 생성. 년도 = 현재(KST).
- 출력: **post + reels 둘 다** 생성 + present(§공통 원칙 — post/reels 명시 시 해당 1개만).
- 보고: `[보고] bash=1 / mode=copyright(post+reels) / 따옴표 OK`

$ARGUMENTS
