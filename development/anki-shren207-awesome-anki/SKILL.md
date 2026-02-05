---
name: anki
description: |
  Anki 카드 분할 스킬. 정보 밀도 높은 Anki 카드를 원자적 단위로 분할.
  사용 시점: (1) 사용자가 /anki 명령 실행, (2) Anki 카드 분할/분석 요청,
  (3) AnkiConnect 연결 상태 확인 요청
---

# Anki Card Splitter

정보 밀도 높은 Anki 카드를 원자적 단위로 분할하는 스킬.

## 실행

```bash
# 프로젝트 루트에서 실행
bun run src/index.ts <command>
```

## 명령어

| 명령어 | 설명 |
|--------|------|
| `status` | AnkiConnect 연결 확인 |
| `split [deck]` | 분할 미리보기 (Dry Run) |
| `split [deck] --apply` | 분할 적용 |
| `analyze [deck] [noteId]` | 카드 구조 분석 |

## 사전 조건

1. Anki 실행: `open -a Anki --args -p test`
2. AnkiConnect 설치 (코드: 2055492159)
3. `.env`에 `GEMINI_API_KEY` 설정

## 주의

- 반드시 `test` 프로필에서만 실행
- `--apply` 없이 항상 미리보기 먼저 확인
