---
name: speaker-guide
description: Create speaker guide documents for AI Builders Meetup. Use when asked to create or generate a speaker guide, speaker 가이드, 스피커 가이드, or when preparing materials for meetup speakers. Ensures no essential sections are missed through a structured 3-phase workflow.
---

# Speaker Guide Generator

3-phase workflow to create complete speaker guides.

## Phase 1: Collect Information

Use AskUserQuestion to gather:

1. **Basic Info**: 밋업 이름, 날짜/시간, 장소
2. **Format**: 발표 시간(분), 스피커 수, 패널토크 유무
3. **Audience**: 타겟 오디언스
4. **Deadlines**: 1:1콜 마감, 자료제출 마감, 질문지 전달일

## Phase 2: Generate Document

Create `speaker-guide.md` with ALL sections from template.

See [references/template.md](references/template.md) for full template.

Required sections checklist:
- [ ] 밋업 정보 (일시, 장소, 형식)
- [ ] 타겟 오디언스
- [ ] 준비 일정 테이블
- [ ] 발표 안내 (시간, 주제, 자료, 라이브데모)
- [ ] 패널 토크 (진행방식, 사전질문지)
- [ ] 호스트 1:1 콜
- [ ] 당일 안내 (사전모임, 타임라인)

## Phase 3: Review

Check for commonly missed items:

| 항목 | 확인 |
|------|------|
| PDF 버전 필수 안내 | |
| 공유 가능 버전 요청 | |
| 호스트 랩탑 사용 안내 | |
| 발표 사이 질문 없음 안내 | |
| 스피커 사전모임 시간 (30분 전) | |
| 라이브 데모 사전고지 요청 | |

If any missing, use AskUserQuestion to confirm before adding.

## Example

See [../../2-echo-delta/speaker-guide.md](../../2-echo-delta/speaker-guide.md)
