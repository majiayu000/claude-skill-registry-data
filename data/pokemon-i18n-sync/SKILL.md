---
name: pokemon-i18n-sync
description: "포켓몬 그린 스킬의 언어별 버전(ko/en) 간 구조 동기화 및 검증 도구. '포켓몬 싱크', 'pokemon sync', 'i18n sync', '언어 동기화', '스킬 싱크' 키워드로 활성화."
trigger-keywords: 포켓몬 싱크, pokemon sync, i18n sync, 언어 동기화, 스킬 싱크, 포켓몬 번역, pokemon translate
allowed-tools: Read, Bash, Glob, Grep
---

# Pokemon Green i18n Sync Tool

포켓몬 그린 스킬의 언어별 버전(pokemon-green-ko, pokemon-green-en) 간 구조 동기화 및 검증 도구입니다.

## 기능

### 1. 싱크 검사 (Sync Validation)
언어 스킬 간 파일 구조와 JSON 키 일치 여부를 검사합니다.

**명령어**: "포켓몬 스킬 싱크 검사" / "pokemon skill sync check"

**검사 항목**:
- 파일 존재 여부 비교 (ko에 있는 파일이 en에도 있는지)
- JSON 파일의 키 구조 비교
- SKILL.md 섹션 수 비교

### 2. 싱크 리포트 (Sync Report)
상세한 차이점 리포트를 생성합니다.

**명령어**: "포켓몬 스킬 싱크 리포트" / "pokemon skill sync report"

### 3. 구조 복사 (Structure Copy)
기준 언어의 구조를 다른 언어로 복사합니다 (값은 플레이스홀더).

**명령어**: "포켓몬 스킬 구조 복사 ko→en" / "pokemon skill copy structure ko to en"

### 4. Diff 보기 (Diff View)
특정 파일의 언어 간 차이를 보여줍니다.

**명령어**: "포켓몬 스킬 diff species.json" / "pokemon skill diff moves.json"

---

## 스킬 경로

| 스킬 | 경로 |
|------|------|
| 한국어 | `.claude/skills/pokemon-green-ko/` |
| 영어 | `.claude/skills/pokemon-green-en/` |

프로젝트 경로: `/Users/jelly/personal/pukiman/`

---

## 사용법

### 싱크 검사 실행

```bash
# 검증 스크립트 실행
bash skills/pokemon-i18n-sync/scripts/validate-sync.sh
```

### 수동 키 비교 (jq)

```bash
# ko 파일의 키 추출
jq -r '[paths(scalars) | join(".")] | sort | .[]' \
  .claude/skills/pokemon-green-ko/data/pokemon/species.json > /tmp/keys_ko.txt

# en 파일의 키 추출
jq -r '[paths(scalars) | join(".")] | sort | .[]' \
  .claude/skills/pokemon-green-en/data/pokemon/species.json > /tmp/keys_en.txt

# 차이 비교
diff /tmp/keys_ko.txt /tmp/keys_en.txt
```

---

## 검사 대상 파일

### 데이터 파일 (data/)
| 파일 | 설명 | 키 검사 |
|------|------|---------|
| `pokemon/species.json` | 151 포켓몬 | 포켓몬 ID 키 |
| `pokemon/learnsets.json` | 레벨업 기술 | 포켓몬 ID 키 |
| `pokemon/evolutions.json` | 진화 조건 | 포켓몬 ID 키 |
| `moves/moves.json` | 165 기술 | 기술명 키 |
| `world/locations.json` | 위치 데이터 | 위치 ID 키 |
| `world/trainers.json` | 트레이너 | 트레이너 ID 키 |
| `messages/battle.json` | 전투 메시지 | 메시지 키 |

### SKILL.md
- 섹션 수 일치 여부
- 주요 섹션 존재 여부

---

## 출력 예시

```
=== Pokemon Skill i18n Sync Report ===
Base: pokemon-green-ko
Target: pokemon-green-en

[파일 검사]
✓ data/pokemon/species.json - 양쪽 존재
✓ data/moves/moves.json - 양쪽 존재
✗ data/items/tm-hm.json - en에 누락

[구조 검사: species.json]
✓ 151개 포켓몬 키 일치

[구조 검사: moves.json]
✗ "swift.ef.type" - ko에만 존재

[SKILL.md 검사]
✓ 섹션 수 일치 (15개)

Summary: 2 errors, 0 warnings
```

---

## 새 언어 추가

새 언어(예: 일본어)를 추가하려면:

1. 기존 스킬 복사
```bash
cp -r .claude/skills/pokemon-green-ko .claude/skills/pokemon-green-ja
```

2. 데이터 파일 번역
- `SKILL.md` 번역
- `data/messages/battle.json` 번역
- `data/pokemon/species.json`의 이름 번역

3. 싱크 검사 실행
```bash
bash skills/pokemon-i18n-sync/scripts/validate-sync.sh ja
```

---

## 스크립트 목록

| 스크립트 | 용도 |
|----------|------|
| `scripts/validate-sync.sh` | 전체 구조 검증 |
| `scripts/compare-json-keys.sh` | 두 JSON 파일 키 비교 |
| `scripts/diff-languages.sh` | 언어 간 차이점 표시 |

---

## 주의사항

1. **기준 언어**: ko(한국어)를 기준으로 다른 언어와 비교
2. **키만 비교**: 값(번역 내용)은 비교하지 않음
3. **자동 수정 없음**: 리포트만 생성, 자동 수정은 하지 않음
