---
name: workpm
description: >
  다이달로스(Daedalus) — 설계 없이 바로 구현할 때 사용하는 5단계 PM. 리서치, 제안, 도면,
  구현, 검증을 자체 진행하며 Claude, Codex, Antigravity, Grok의 내장 탐색자·작업자를 우선 사용한다.
  Antigravity의 일반 장기 팀 작업은 /teamwork-preview를 우선하고, 이 스킬은 5단계 장부와 산출물이 필요할 때 사용한다.
  /workpm 또는 /daedalus로 실행한다.
---

# Daedalus (다이달로스) — 현장감독 PM

> **다이달로스(Daedalus)**: 미노타우로스의 미궁을 지은 그리스 전설의 건축가.
> 설계 도면 없이도 직접 리서치하고, 제안하고, 도면을 그린 뒤 시공합니다.

**공식 호출명:** `/workpm` (별칭: `/daedalus`, `다이달로스`)

## 언제 사용하나?

| 상황 | 사용할 도구 |
|------|-----------|
| **젭마인 없이** 바로 구현 시작 | **다이달로스** (`/daedalus`) |
| **젭마인 산출물**(sections/) 기반 구현 | **포세이돈** (`/agent-team`) |

다이달로스는 **설계 산출물이 없을 때** 스스로 리서치 → 제안 → 도면 작성 → 구현까지 전체를 관리합니다.
젭마인 산출물이 이미 있다면 `/agent-team`이 더 적합합니다 (섹션 파싱 + Wave 정렬 + 전문가 매칭).

## 네이티브 기능과의 경계

- 작은 직접 구현은 현재 Antigravity 메인 컨텍스트가 그대로 수행합니다. 구현 전 계획만 필요하면 네이티브
  `/plan`, 요구사항 누락을 집중 질문으로 좁히는 일만 필요하면 `/grill-me`가 우선입니다.
- 일반적인 장기·다중 에이전트 실행은 현재 플랜과 런타임에서 가용한 Antigravity
  `/teamwork-preview`가 우선입니다. 이미 그 팀 문맥이 활성화돼 있으면 실행 엔진으로 재사용하고 중첩 PM을 만들지 않습니다.
- WorkPM의 고유 범위는 설계 없이 시작한 요청을 **리서치→제안→도면→구현→검증** 5단계 장부와
  완료 증거까지 끌고 가는 것입니다. 이 산출물 계약이 필요할 때만 네이티브 엔진 위에 얹습니다.
- slash command는 사용자/TUI 진입점입니다. 스킬이 `/plan`, `/grill-me`, `/teamwork-preview`를
  프로그램적으로 호출하거나 플랜 제한을 우회한다고 가정하지 않습니다.

## 실행 경로

> **native-first 원칙** (learned/020): 워크플로우(5단계)는 공통, 실행 프리미티브만 CLI별 네이티브로 교체.

| CLI | 실행 경로 | 기준 파일 |
|-----|----------|----------|
| Claude Code | 내장 subagent; 실험 Agent Teams가 활성화되면 named teammate | `${orchestrator_root}/commands/workpm.md` |
| Codex | 내장 `explorer`/`worker`/`default` | `${orchestrator_root}/commands/workpm.md` + 아래 역할 표 |
| Antigravity | 활성 `/teamwork-preview` 팀 또는 내장 `research` + 메인/사용자 정의 쓰기 서브에이전트 | `${orchestrator_root}/commands/workpm.md` + 아래 역할 표 |
| Grok | 내장 `explore`/`general-purpose`/`plan` | `${orchestrator_root}/commands/workpm.md` + 아래 역할 표 |
| (폴백) | Orchestrator MCP PM/Worker — 네이티브 도구로 요구 계약을 충족할 수 없을 때만 | `${orchestrator_root}/commands/workpm-mcp.md` |

## Source-only internal module resolution (mandatory)

`orchestrator`와 조건부 `domain-dictionary`는 다이달로스가 내부 계약으로 읽는 source-only
모듈입니다. 등록된 스킬이나 slash command로 호출하지 않습니다.

각 모듈을 다음 순서로 해석하고 처음 확인된 exact `SKILL.md` 파일 하나를 읽습니다.

1. 현재 프로젝트의 `skills/{name}/SKILL.md`가 실제로 있으면 그 exact 파일.
2. 없으면 현재 런타임 active root의 exact 파일: Claude/Grok은
   `~/.claude/skills/{name}/SKILL.md`, Codex는 `~/.codex/skills/{name}/SKILL.md`, Antigravity는
   `~/.gemini/antigravity-cli/skills/{name}/SKILL.md` (명시 opt-in 설치 지원).
3. 둘 다 없으면 현재 런타임 전역 카탈로그(Claude/Grok
   `~/.claude/SKILLS-CATALOG.md`, Codex `~/.codex/SKILLS-CATALOG.md`, Antigravity
   `~/.gemini/antigravity-cli/SKILLS-CATALOG.md`)에서 정확한 모듈명 행을 찾습니다. 행이 하나일 때만
   `읽을 경로`의 절대 `SKILL.md`를 읽고, 누락·중복 행은 fail-closed입니다. 기본 설치에서
   보통 `.olympus/source-skills`를 가리켜도 경로를 추측하거나 조합하지 않습니다.
4. `module_root`는 읽은 `SKILL.md`의 부모입니다. `references/`, `scripts/`, `commands/`는
   모두 그 루트에서 해석합니다.

이 exact 파일 읽기는 내부 모듈 로드입니다. 런타임 Skill 목록/레지스트리를 근거로 호출하거나
모듈 이름을 slash command로 실행하지 않습니다.

5단계 네이티브/순차 경로를 선택한 뒤 `orchestrator`를 해석하여 `orchestrator_root`를 만들고
`${orchestrator_root}/commands/workpm.md`를 읽습니다. 이 계약은 필수이므로 행·경로·파일을
읽지 못하면 `BLOCKED: workpm source contract unavailable`을 보고하고 워크플로우 완료를
주장하지 않습니다. MCP 경로는 hard lock, 외부 ledger, 장시간 크로스-CLI 혼합이 실제로
필요하다고 판정한 뒤에만 `${orchestrator_root}/commands/workpm-mcp.md`를 추가로 읽습니다.
MCP 파일을 읽지 못하면 안전하게 직렬화 가능한 작업만 메인 순차 경로로 축소하고
`MCP: NOT RUN`을 기록합니다. hard lock 자체가 필수이면 `BLOCKED`입니다.

`domain-dictionary`는 Phase 1에서 사전이 없고 작업이 trivial하지 않을 때만 지연 로드합니다.
성공하면 `domain_dictionary_root`를 만들고 모듈 및 필요한
`${domain_dictionary_root}/references/*` 계약을 따릅니다. 모듈이 없으면 아래 5~10개 용어
추출만 bounded native fallback으로 수행하고 `dictionary-module: NOT RUN (native fallback)`을
기록합니다. fallback이나 미실행을 모듈 PASS로 표시하지 않습니다.

**CLI별 네이티브 역할** (agent-team [wave-executor.md](../agent-team/references/wave-executor.md)와 동일 — CLI별 설치본에 agent-team이 없을 수 있어 여기 내장, 수정 시 양쪽 함께):

| CLI | 읽기 전용 탐색·검토 | 구현·명령 실행 | 상태·정리 |
|-----|--------------------|----------------|-----------|
| **Claude** | `Explore` | `general-purpose`; Agent Teams 활성 시 named background `Agent` | shared task list/메시지; implicit team 자동 정리 |
| **Codex** | `explorer` | `worker` (`default` 폴백) | 현재 spawn/message/wait/interrupt 기능 |
| **Antigravity** | `research` | 메인 또는 쓰기 도구를 명시한 사용자 정의 서브에이전트 | 호출 반환을 Lead가 검증 |
| **Grok** | `explore` | `general-purpose` | 호출 반환을 Lead가 검증 |

읽기 전용 역할에는 파일 생성을 지시하지 않습니다. 구현 역할은 고유 파일 범위와 검증 계약을 받습니다. 위임이 없거나 실패하면 메인 컨텍스트에서 순차 실행하고, hard lock·외부 ledger·크로스-CLI 혼합이 필요할 때만 MCP로 전환합니다.

`pmworker`는 레거시 호출명입니다. 별도 스킬로 보지 말고 이 다이달로스/오케스트레이터 경로로 라우팅합니다.

## 추론 강도 선택 전략

각 CLI의 현재 모델·effort·sandbox 설정을 상속합니다. 판단·비교·최종 검증에는 높은 추론 강도를, 구현에는 균형형 실행을, 반복 테스트에는 빠른 실행을 요청하되 특정 vendor 모델을 강제하지 않습니다.

## 도메인사전 통합

다이달로스는 설계 산출물 없이 즉흥 시공하기 때문에 **용어 일관성이 더 중요**합니다. 사전이 없으면 첫 시공부터 용어가 어긋납니다.

### Phase 1 끝: 사전 존재 확인 + 자동 생성

리서치 직후 다음을 자동 수행:

1. **사전 존재 확인**: `docs/domain-dictionary.md` 탐색
2. **있으면**: 컨텍스트로 로드, 모든 후속 Phase에 전달
3. **없고 trivial하지 않으면 source module 로드**: 위 resolver로 `domain-dictionary`의 정확한
   `SKILL.md`와 필요한 module-root reference를 읽어 코드베이스/컨텍스트 계약 수행
4. **모듈 미가용 시 즉석 생성** (bounded native fallback):
   - 글로벌 사전(`~/.agent-memory/domain-dictionaries/{도메인}.md`, `AGENT_DOMAIN_DICTIONARY_HOME` override 가능) 후보 용어를 번호 목록으로 시드 (있으면)
   - 사용자 지시문에서 핵심 용어 5~10개 추출
   - 사용자 1회 확인 후 마스터 사전 v1 생성
   - 이후 시공 중 새 용어 발견 시 사전 자동 갱신 (델타 없이 마스터 직접)
   - 상태를 `dictionary-module: NOT RUN (native fallback)`으로 기록
5. **비적용 조건**: 사용자 지시가 5줄 미만의 trivial 작업이면 `NOT APPLICABLE: trivial task`로 기록

### Phase 4 (구현): teammate에게 사전 전달

모든 구현 teammate 프롬프트에 사전 컨텍스트와 준수 규칙을 포함합니다. 자세한 형식은 `agent-team` 스킬의 [teammate-context-template.md](../agent-team/references/teammate-context-template.md) "도메인사전 강제 사용 지침" 섹션 참조 — 동일하게 적용. (Codex 설치본에는 agent-team이 없음 — `agent-team-codex`의 [prompt-templates.md](../agent-team-codex/references/prompt-templates.md)를 쓰되, 사전 컨텍스트+준수 규칙+금지 표현을 팀원 프롬프트에 포함한다는 원칙은 동일)

### Phase 5 (공정 점검): 사전 준수 검증

도면 vs 코드 대조 시 사전 준수도 함께 검사:
- 코드 식별자가 사전 영문 식별자를 따르는가
- 금지 표현 사용 여부
- UI 라벨이 사전 한글 표기를 따르는가
- 위반 발견 시 해당 teammate에게 재시공 지시 (rename은 자동 수정 가능)

## 워크플로우

경로에 따라 단계 수가 다릅니다.

| 경로 | 단계 | 차이 |
|-----|------|------|
| 네이티브 (Claude/Codex/Antigravity/Grok) | 5단계 | Phase 3에 영향도 분석 포함 |
| 폴백 (orchestrator MCP) | 4단계 | 영향도 분석을 별도 Phase로 두지 않고 구현 계획에 흡수 |

## Start

1. **네이티브 경로** (기본): 경로 선택 후 source-only resolver로
   `${orchestrator_root}/commands/workpm.md`를 읽고 5단계 워크플로우를 따릅니다.
   각 CLI는 위 역할 표와 현재 런타임 도구를 사용합니다.
2. **순차 폴백**: 네이티브 위임이 없거나 독립 작업이 하나뿐이면 로드한 같은 5단계를 메인 컨텍스트에서 순차 실행합니다.
3. **MCP 폴백**: hard file lock, 외부 task ledger, 장시간 크로스-CLI 혼합이 필요하다고
   판정한 뒤에만 `${orchestrator_root}/commands/workpm-mcp.md`를 읽습니다. 선택 전에는 MCP
   계약이나 서버를 로드하지 않습니다.
