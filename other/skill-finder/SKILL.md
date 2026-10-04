---
name: skill-finder
description: 벤더링된 android/kotlin/compose 스킬을 자연어로 검색해 적재적소 스킬을 찾는다. spec/plan 작성이나 TEAMYG-Android 구현 중 "어떤 스킬 써야 하지", "recomposition 관련 스킬 찾아", "이 주제 스킬 검색"이 필요할 때 사용. SKILL.md frontmatter를 키워드 가중 랭킹해 상위 후보를 돌려준다.
---

# skill-finder

`.claude/skills/`의 벤더 스킬을 쿼리로 랭킹한다(이름>description>제목 가중). 로직은 `parfait/script/search.py`.

## 사용
`python3 parfait/script/search.py "<자연어 쿼리>" [--top N]`

예: `python3 parfait/script/search.py "lazy list scroll jank" --top 5`

## 언제
- **spec/plan 작성 시**(워크플로 A): 다룰 주제(recomposition·stability·navigation·coroutines·testing·gradle 등)를 쿼리해 관련 벤더 스킬을 찾은 뒤, 그 스킬을 네이티브 `Skill`로 호출해 설계·계획에 반영.
- 구현 중 특정 문제(성능·안정성·마이그레이션)에 맞는 스킬을 모를 때.

## 참고
- 전체 목차는 `.claude/skills-vendor/CATALOG.md`.
- 검색은 후보 랭킹만 — 실제 지침은 해당 스킬을 `Skill`로 호출해 로드.
- 벤더 스킬 갱신은 [[update-injected-skills]].
