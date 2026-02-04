---
name: whitepaper-kr
description: 한국어 기술 백서(Whitepaper) 작성을 지원합니다. 백서, whitepaper, 기술문서, 투자자료, AI백서, SaaS, 블록체인 백서 작성 시 사용하세요.
---

# 기술 백서 작성 Skill

한국어 기술 백서 작성을 지원합니다. AI, SaaS, 블록체인 등 다양한 기술 프로젝트에 적용 가능합니다.

**핵심 철학**:
- 투자자/비개발자 대상이지만 기술적 깊이 유지
- 명확성과 간결성 (문장 평균 14단어 이하)
- 데이터와 근거로 주장 뒷받침
- 프로젝트 유형별 맞춤 구조

## Instructions

### 워크플로우: 요청 분석 및 모드 선택

#### 1. 프로젝트 유형 감지

사용자 요청에서 프로젝트 유형을 파악합니다:

| 키워드 | 프로젝트 유형 | 템플릿 |
|--------|---------------|--------|
| AI, 머신러닝, 딥러닝, LLM, GPT | AI 프로젝트 | whitepaper-ai.md |
| 블록체인, 토큰, web3, NFT, 코인 | 블록체인 프로젝트 | whitepaper-blockchain.md |
| SaaS, 플랫폼, 서비스, B2B | 일반 기술 프로젝트 | whitepaper-general.md |

#### 2. 작성 모드 선택

**전체 작성 모드** (새 백서)
- 프로젝트 유형 확인
- Phase 1-6 필수 섹션 순차 진행
- 프로젝트 유형별 선택 섹션 추가

**섹션별 작성 모드** (부분 작성)
- 키워드 매칭으로 해당 리소스만 로드
- 단일 섹션 집중 작성

**보완/갱신 모드** (기존 문서 개선)
- 기존 문서 분석
- 누락 섹션 식별
- 개선점 제안 후 수정

### 섹션별 키워드 매칭

| 키워드 | 리소스 파일 | 필수/선택 |
|--------|-------------|-----------|
| 개요, 소개, introduction, 요약 | 01-overview.md | 필수 |
| 해결책, 솔루션, solution, 제안 | 02-solution.md | 필수 |
| 아키텍처, 기술, architecture, 구조 | 03-architecture.md | 필수 |
| 차별화, 경쟁력, 장점, 특징 | 04-differentiation.md | 필수 |
| 팀, team, 조직, 멤버 | 05-team.md | 필수 |
| 로드맵, 일정, roadmap, 마일스톤 | 06-roadmap.md | 필수 |
| 비즈니스, 수익, 모델, 가격 | 07-business-model.md | 선택 (일반/AI) |
| 토큰, 토크노믹스, tokenomics | 08-tokenomics.md | 선택 (블록체인) |
| 법적, 면책, legal, 규제 | 09-legal.md | 선택 |

### 리소스 로딩 전략

**단일 섹션 요청**
```
User: "백서 로드맵 섹션 작성해줘"
→ Read resources/06-roadmap.md
→ 해당 섹션만 작성
```

**전체 백서 요청**
```
User: "AI 프로젝트 백서 전체 작성해줘"
→ Read templates/whitepaper-ai.md
→ Read resources/01-overview.md ~ 06-roadmap.md (필수)
→ Read resources/07-business-model.md (AI는 비즈니스 모델 포함)
→ Phase별 순차 작성
```

**보완 요청**
```
User: "이 백서 검토하고 보완해줘"
→ 기존 문서 분석
→ 누락 섹션 식별
→ 해당 리소스 Read 후 보완
```

### 작성 워크플로우 (전체 작성 모드)

#### Phase 1: 개요 (Introduction)
1. Read resources/01-overview.md
2. 프로젝트 소개 작성
3. 해결하려는 문제 정의
4. 시장 기회 설명

#### Phase 2: 해결책 (Solution)
1. Read resources/02-solution.md
2. 제안하는 솔루션 설명
3. 핵심 기능/특징 나열
4. 사용자 가치 제안

#### Phase 3: 기술 아키텍처 (Architecture)
1. Read resources/03-architecture.md
2. 시스템 구조도 (다이어그램 권장)
3. 기술 스택 설명
4. 데이터 흐름 설명

#### Phase 4: 차별화 (Differentiation)
1. Read resources/04-differentiation.md
2. 기존 솔루션 대비 장점
3. 핵심 기술/특허
4. 경쟁 우위 분석

#### Phase 5: 팀 (Team)
1. Read resources/05-team.md
2. 핵심 팀원 소개
3. 관련 경력/전문성
4. 자문단/파트너십

#### Phase 6: 로드맵 (Roadmap)
1. Read resources/06-roadmap.md
2. 개발 단계별 목표
3. 마일스톤 및 일정
4. 장기 비전

#### Phase 7: 선택 섹션
- **일반/AI**: Read resources/07-business-model.md → 비즈니스 모델
- **블록체인**: Read resources/08-tokenomics.md → 토크노믹스
- **필요시**: Read resources/09-legal.md → 법적 고지

## 작성 원칙

### 분량 가이드
- **전체 백서**: 4,000~6,000단어 (6~12페이지)
- **개별 섹션**: 500~1,000단어

### 문체 원칙
- 평균 문장 길이 14단어 이하
- 전문 용어는 첫 등장 시 설명
- 능동태 사용 권장
- 미사여구/감탄사 배제

### 근거 제시
- 모든 주장에 데이터/출처 명시
- 측정 가능한 수치 사용
- 제3자 검증 자료 인용

### 시각 자료
- 아키텍처 다이어그램 필수
- 데이터는 차트/그래프로 시각화
- 로드맵은 타임라인 형식 권장

## Technical Details

상세한 작성 가이드는 각 리소스 파일 참조:
- `REFERENCE.md`: 리소스 전체 개요
- `resources/01-overview.md`: 개요 섹션 작성 가이드
- `resources/02-solution.md`: 해결책 섹션 작성 가이드
- `resources/03-architecture.md`: 기술 아키텍처 작성 가이드
- `resources/04-differentiation.md`: 차별화 포인트 작성 가이드
- `resources/05-team.md`: 팀 소개 작성 가이드
- `resources/06-roadmap.md`: 로드맵 작성 가이드
- `resources/07-business-model.md`: 비즈니스 모델 작성 가이드 (선택)
- `resources/08-tokenomics.md`: 토크노믹스 작성 가이드 (블록체인)
- `resources/09-legal.md`: 법적 고지 작성 가이드 (선택)
- `templates/whitepaper-general.md`: 일반 기술 백서 템플릿
- `templates/whitepaper-ai.md`: AI 프로젝트 백서 템플릿
- `templates/whitepaper-blockchain.md`: 블록체인 프로젝트 백서 템플릿
