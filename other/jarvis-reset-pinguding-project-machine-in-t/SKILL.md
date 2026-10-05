---
name: jarvis-reset
description: jarvis 워치의 로컬 상태(.jarvis/baseline·args·status·stopped)를 삭제해 완전 초기화하고, 확인을 받은 뒤 계획/체크리스트(.jarvis/plan.md·checklist.md)도 삭제한다. 다음 /loop /jarvis는 최초 부팅(배너·계획 옵트인·강도 질문)부터 새로 시작한다. 루프 자체를 멈추는 게 아니라 누적 추적·저장된 설정을 비우는 독립 명령이다. "jarvis 초기화", "jarvis reset", "워치 상태 비우기", "처음부터 다시" 요청 시 사용.
---

# jarvis-reset

`jarvis` 워치의 **로컬 상태를 초기화**한다. `.jarvis/`의 상태 파일(`baseline`·`args`)을 지워 **누적 변경 추적과 저장된 설정을 전부 버리고**, 확인을 받은 뒤에만 **계획/체크리스트**(`plan.md`·`checklist.md`)도 지운다. 다음에 `/loop /jarvis`를 띄우면 최초 부팅처럼(시작 배너 + 계획 옵트인 + 강도 질문) 새로 시작한다.

> ⚠️ **이건 루프를 멈추는 명령이 아니다.** 돌고 있는 워치를 멈추려면 `/loop` 자체를 인터럽트한다(Esc). `jarvis-reset`은 그와 **독립**적으로 *상태만* 비운다. 멈춘 뒤 깨끗하게 다시 시작하고 싶을 때 쓴다.

## 왜 독립 명령인가

`/loop /jarvis`는 `.jarvis/baseline`·`args`가 남아 있으면 **그 상태에서 이어서** 감시한다(그게 곧 재개다). 그래서 "처음부터 새로"를 원하면 그 상태를 명시적으로 비워야 한다 — 그 일을 하는 게 이 스킬이다. 루프 종료(Esc)에는 teardown 훅이 없으므로, 초기화는 이렇게 **별도 명령**으로만 일어난다.

## 절차

1. **워치 상태 파일 일괄 삭제** (매 tick짜리, 항상 지워도 안전):

   ```bash
   rm -f .jarvis/baseline .jarvis/args .jarvis/status .jarvis/stopped .jarvis/paused
   ```

   - `.jarvis/status`는 생존 신호용 상태 파일이다. 지우면 statusline이 즉시 비워진다(워치 미가동 표시).
   - `.jarvis/stopped`는 Stop 훅이 남기는 이벤트 멈춤 플래그다. 함께 지운다(없으면 무해).
   - `.jarvis/paused`는 구버전 잔재일 수 있어 함께 지운다(없으면 무해).
   - `.jarvis/` 디렉토리 자체는 남겨도 무방하다(다른 캐시가 있을 수 있음). 비어 있어도 굳이 지우지 않는다.

2. **계획 & 체크리스트 — 지우기 전에 확인.** 한 줄짜리 상태 파일과 달리 `.jarvis/plan.md`·`.jarvis/checklist.md`는 사람이 저작·승인한 **지속 작업물**이다. 둘 중 하나라도 있으면 **먼저 묻는다**(`AskUserQuestion` 또는 단순 확인): *"계획과 체크리스트도 지울까요? 되돌릴 수 없습니다."*
   - **예** → `rm -f .jarvis/plan.md .jarvis/checklist.md` (다음 시작에 계획 옵트인을 다시 물음).
   - **아니오** → 남긴다. 다음 `/loop /jarvis`는 기존 체크리스트를 기준으로 계획 모드를 재개한다(baseline은 비워졌으니 처음부터 재측정하지만, 계획/체크리스트는 유지).
   - 둘 다 없으면 이 단계는 조용히 건너뛴다.

3. **보고** (한 줄): `🧹 Jarvis 상태 초기화 완료. 다시 켜려면 /loop /jarvis (배너·계획 옵트인·강도 질문부터 새로 시작).`

## 자연어 트리거

"jarvis 초기화", "jarvis reset", "워치 상태 비워", "처음부터 다시" 같은 초기화 의사를 이 스킬로 처리한다. "그냥 멈춰"·"잠깐 중지" 처럼 *멈춤*만 원하는 뉘앙스면 루프를 인터럽트(Esc)하라고 안내한다 — 상태는 그대로 두면 `/loop /jarvis`로 이어서 재개된다.

## 하지 않는 것

- 돌고 있는 `/loop`을 직접 멈추지 않는다(그건 Esc의 일).
- 사용자 워킹 트리의 코드/변경은 건드리지 않는다 — 지우는 건 `.jarvis/` 제어 파일뿐이다.

## 참조
- 워치 본체: `.claude/skills/jarvis/SKILL.md` ("제어 상태 파일" 표, 시작 시 재개·자가보정)
