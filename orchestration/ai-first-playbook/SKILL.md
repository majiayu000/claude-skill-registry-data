---
name: ai-first-playbook
description: "AI-First 조직 전환 플레이북 — 파일럿(0-30일)→팀 확산→문화 정착 단계, ROI 측정 프레임워크, Claude Code 운영 전략. Use when 팀에 AI 도구를 도입하고 효과를 측정하는 로드맵을 세울 때."
---

# AI-First Engineering Playbook

AI-First 조직 전환, 워크플로우 재설계, ROI 측정, Claude Code 운영 전략

## Quick Reference (결정 트리)

```
AI 도입 단계?
    │
    ├─ 시작 (0-30일) ──────> Phase 1: 파일럿
    │       └─ 1-2개 워크플로우에 AI 적용, 효과 측정
    │
    ├─ 확장 (30-90일) ─────> Phase 2: 팀 확산
    │       └─ 성공 패턴 표준화, 팀 AI 리터러시 구축
    │
    └─ 정착 (90일-12개월) ─> Phase 3: AI-First 문화
            └─ 워크플로우 재설계, 역할 재정의, 거버넌스

가치의 원천?
    │
    ├─ 기술 (20%) ──────> AI 도구 도입 (Copilot, Claude Code)
    │
    └─ 워크플로우 (80%) ──> 일하는 방식 자체를 재설계
            │
            ├─ AI가 잘하는 것 → AI에게 위임
            ├─ 인간이 잘하는 것 → 인간에게 집중
            └─ 새로운 가능한 것 → AI로 처음 가능해진 작업

ROI 측정?
    │
    ├─ 잘못된 지표 ────────> LOC, PR 수, 커밋 수 (AI가 부풀림)
    │
    └─ 올바른 지표 ────────> 아래 "측정 프레임워크" 참조
```

---

## Phase 1: 파일럿 (0-30일)

### 목표

"AI가 뭘 할 수 있나?"가 아니라 **"AI가 우리한테 뭘 해줄 수 있나?"**

### 파일럿 워크플로우 선택

**높은 ROI 워크플로우** (먼저 시작):

| 워크플로우 | AI 역할 | 기대 효과 | 측정 방법 |
|-----------|---------|---------|---------|
| 코드 리뷰 | 1차 자동 리뷰 → 인간 최종 | 리뷰 시간 50%↓ | 리뷰 소요시간 |
| 테스트 작성 | 테스트 초안 생성 | 테스트 커버리지↑ | 커버리지 % |
| 버그 수정 | 진단 + 수정 제안 | MTTR↓ | 해결 시간 |
| 문서 작성 | API 문서, 코드 주석 | 문서화율↑ | 문서 커버리지 |
| 보일러플레이트 | CRUD, 설정 파일 | 반복 작업↓ | 생성 시간 |

**낮은 ROI** (나중에):
- 아키텍처 설계 (인간 판단 필수)
- 보안 민감 코드 (리스크 높음)
- 레거시 대규모 리팩토링 (컨텍스트 복잡)

### 30일 체크리스트

```
Week 1: 환경 설정
- [ ] Claude Code / Copilot 팀 라이선스 설정
- [ ] CLAUDE.md 프로젝트 규칙 작성
- [ ] 1-2명 얼리어답터와 파일럿 시작

Week 2-3: 실험
- [ ] 선택한 워크플로우에 AI 적용
- [ ] Before/After 데이터 수집 시작
- [ ] 효과 있는 패턴 기록

Week 4: 평가
- [ ] 파일럿 결과 정리 (정량 + 정성)
- [ ] 팀 공유 세션
- [ ] Phase 2 대상 워크플로우 선정
```

---

## Phase 2: 팀 확산 (30-90일)

### AI 리터러시 구축

```
Level 1: 기본 사용         Level 2: 효과적 활용        Level 3: 오케스트레이션
────────────────          ─────────────────          ──────────────────
- 코드 자동완성            - 프롬프트 엔지니어링        - SPEC 기반 개발 (SDD)
- 챗 기반 질문             - Context engineering       - Multi-agent 조율
- 단순 생성 요청           - Plan Mode 활용            - 워크플로우 설계
                          - CLAUDE.md 규칙 설정        - 품질 게이트 설계
```

### 성공 패턴 표준화

파일럿에서 효과가 검증된 패턴을 **팀 표준**으로:

```
1. 검증된 CLAUDE.md / Rules → 팀 레포에 커밋
2. 효과적인 프롬프트 패턴 → Skills로 변환
3. 반복되는 워크플로우 → Hooks / MCP로 자동화
4. 팀 온보딩 가이드에 AI 워크플로우 추가
```

### Product Management 마인드셋

```
Google의 AI 채택 원칙:
1. 고가치 기회 식별 (어디에 AI를 쓸까?)
2. AI 도구의 능력 이해 (뭘 할 수 있나?)
3. 워크플로우 재설계 (빠른 해결책이 아니라 근본 재설계)
```

---

## Phase 3: AI-First 문화 (90일-12개월)

### 워크플로우 재설계

```
기존 워크플로우:
  요구사항 → 설계 → 구현 → 테스트 → 리뷰 → 배포
                     ↑
                  인간이 전부

AI-First 워크플로우:
  요구사항(인간) → 스펙(인간+AI) → 설계(인간) →
  구현(AI) → 테스트(AI) → 리뷰(인간) → 배포(자동)
                                 ↑
                          인간은 설계+검증에 집중
```

### Shopify 모델 참고

```
Shopify AI-First 원칙:
1. 인프라가 실험을 저렴하고 안전하게 만들어야 함
2. 문화가 엔지니어에게 AI를 기본으로 사용하도록 장려
3. 가드레일이 속도를 높이면서 품질을 유지

실전:
- 시니어 엔지니어가 여러 Agent 동시 실행
- 결과를 리뷰, 안 되는 건 버리고, 되는 건 머지
- 20% 생산성 향상 달성
```

### 역할 재정의

| 기존 역할 | AI-First 역할 | 핵심 변화 |
|---------|-------------|---------|
| Junior 개발자 | AI Reliability Engineer | AI 출력 검증, 기술 스펙 작성 |
| Senior 개발자 | Agent Orchestrator | 시스템 설계, Agent 조율, 품질 평가 |
| 테크리드 | AI Strategy Lead | 워크플로우 설계, 거버넌스, ROI |
| EM | AI-Enabled EM | 팀 AI 리터러시, 채택률 추적 |

---

## ROI 측정 프레임워크

### 잘못된 지표 (사용하지 말 것)

| 지표 | 왜 잘못인가 |
|------|-----------|
| Lines of Code | AI가 부풀림, 양 ≠ 가치 |
| PR 수 / 커밋 수 | AI가 증가시키지만 가치와 무관 |
| "AI 사용률" | 사용 ≠ 효과 |

### 올바른 지표

| 카테고리 | 지표 | 측정 방법 |
|---------|------|---------|
| **속도** | Time-to-First-PR (신규 기능) | 이슈 생성 → 첫 PR 시간 |
| **속도** | MTTR (장애 복구 시간) | 알림 → 수정 배포 시간 |
| **품질** | 프로덕션 버그율 | 배포 후 7일 내 버그 수 |
| **품질** | 코드 리뷰 라운드 수 | PR당 리뷰 왕복 횟수 |
| **효율** | 개발자 체감 생산성 | 분기별 설문 (1-10) |
| **효율** | AI 채택률 | 주간 AI 도구 사용 개발자 비율 |
| **비용** | 기능당 비용 | (인건비 + AI 비용) / 기능 수 |

### 측정 타임라인

```
30일:  Before/After 베이스라인 비교
90일:  팀 단위 생산성 트렌드
6개월: 조직 단위 ROI 산출
12개월: 연간 총 비용 절감 / 가치 창출
```

### ROI 기대치 (현실적)

```
단순 자동화 (코드 제안, 테스트): 1-2년 내 ROI
워크플로우 재설계: 6-12개월 내 ROI
Agent 기반 자율 실행: 3년+ (거버넌스 비용 포함)

주의: 95%의 AI 파일럿이 ROI 달성 실패
원인: 산발적 실험 (도구만 도입, 워크플로우 미변경)
```

---

## Claude Code 운영 전략

### 프로젝트 셋업 표준

```
새 프로젝트에 Claude Code 도입 시:

1. CLAUDE.md 작성 (프로젝트 규칙, 200줄 이내)
2. .claude/rules/ 디렉토리 (코딩 컨벤션)
3. .claude/skills/ 디렉토리 (도메인 지식)
4. .claude/settings.json (hooks, MCP 서버)
5. SPEC.md 템플릿 준비

→ install.sh --plugin ai-engineering 으로 한 번에 설치
```

### 비용 관리

```
Claude Code 비용 구조:
├─ API 비용: 모델별 token 과금
├─ 에이전트 비용: 병렬 실행 시 증가
└─ 인프라 비용: MCP 서버, GPU (해당 시)

최적화:
├─ Model Routing (단순→경량, 복잡→Frontier)
├─ Plan Mode로 불필요한 구현 방지
├─ SPEC 기반으로 재작업 최소화
└─ 주간 비용 리뷰
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 도구만 도입, 워크플로우 유지 | 95% 실패 원인 | 일하는 방식 자체 재설계 |
| 모든 팀 동시 도입 | 혼란, 지원 부족 | 얼리어답터 → 점진 확산 |
| LOC/PR 수로 ROI 측정 | 의미 없는 지표 | Time-to-PR, MTTR, 체감 생산성 |
| AI에게 아키텍처 위임 | 일관성 부족 | 인간이 설계, AI가 구현 |
| CLAUDE.md 200줄 초과 | Claude가 규칙 무시 | 핵심만 CLAUDE.md, 나머지 Skills |
| 거버넌스 없이 자율 실행 | 보안/품질 리스크 | hooks + 가드레일 |

---

## 체크리스트

### Phase 1: 파일럿
- [ ] 파일럿 워크플로우 1-2개 선택
- [ ] Before 베이스라인 측정
- [ ] CLAUDE.md + Rules 작성
- [ ] 30일 후 After 측정

### Phase 2: 확산
- [ ] 성공 패턴 표준화 (CLAUDE.md, Skills)
- [ ] 팀 AI 리터러시 교육
- [ ] AI 채택률 주간 추적
- [ ] 온보딩 가이드에 AI 워크플로우 추가

### Phase 3: AI-First
- [ ] 워크플로우 재설계 (설계+검증은 인간, 구현은 AI)
- [ ] 역할 재정의 문서화
- [ ] 분기별 ROI 리포트
- [ ] 거버넌스 정책 수립

---

## 참조 스킬

- `spec-driven-development.md` — SDD 워크플로우 (Research→Spec→Plan→Execute)
- `agentic-coding.md` — Agentic Coding 4가지 모드, Agent Supervision
- `dx-ai-agents.md` — 엔터프라이즈 AI 거버넌스, RBAC
- `dx-metrics.md` — DORA, SPACE, DevEx 측정 프레임워크
- `finops-ai.md` — AI 비용 관리, Token Economics
- `engineering-strategy.md` — Tech Radar, 로드맵, 기술 부채 관리

---

## Sources

- [Shopify AI-First Playbook (Bessemer)](https://www.bvp.com/atlas/inside-shopifys-ai-first-engineering-playbook)
- [Vellum: 2026 AI Transformation Playbook](https://vellum.ai/blog/ai-transformation-playbook)
- [Google: Product Management Mindset for AI](https://blog.google/company-news/inside-google/life-at-google/strategies-to-adopt-ai-at-work/)
- [Developer Productivity Benchmarks 2026](https://larridin.com/developer-productivity-hub/developer-productivity-benchmarks-2026)
- [AI ROI Measurement (Pinnacle)](https://www.heypinnacle.com/blog/ai-roi-measurement-framework-2026)
- [AI-First Engineering Organization 2026](https://codenote.net/en/posts/ai-first-engineering-org-evolution-2026/)
