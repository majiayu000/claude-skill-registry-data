---
name: update-injected-skills
description: 벤더링한 android/kotlin/compose 스킬을 upstream과 동기화한다. 사용자가 "스킬 업데이트", "벤더 스킬 갱신", "update-injected-skills", "스킬 최신화"라고 할 때 사용. baseline.json의 마지막 SHA 대비 delta(추가·수정·삭제)만 재벤더한다.
---

# update-injected-skills

`.claude/skills-vendor/`의 4개 소스 repo를 baseline SHA 대비 diff로 업데이트한다. 로직은 `parfait/script/vendor.py`.

## 절차
1. **dry-run 먼저**: `python3 parfait/script/vendor.py --update --dry-run`
   - 출력 `+추가 ~수정 -삭제`와 스킬 목록 확인.
2. delta 있으면 실제 적용: `python3 parfait/script/vendor.py --update`
3. 변경 요약을 사용자에게 보고(추가/수정/삭제 스킬명 + baseline SHA 갱신분).
4. `.claude/skills/`·`.claude/skills-vendor/{baseline,manifest,MANIFEST,CATALOG}` 변경을 **사용자 확인 후** 커밋(CLAUDE.md Git 규율: 브랜치→PR→merge).

## 주의
- baseline SoT = `.claude/skills-vendor/baseline.json`. `baseline.md`는 렌더 산출물.
- 전량 재설치가 필요하면 `--full`(초기 설치 전용).
- 스킬 원본은 편집 금지(순수 벤더).
