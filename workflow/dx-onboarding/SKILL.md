---
name: dx-onboarding
description: "개발자 온보딩 자동화 전체 개요 — Time-to-First-Deploy 등 온보딩 메트릭 수집, 안티패턴, 체크리스트. Use when 온보딩 개선 전략을 세우고 세부 주제(환경·첫 배포·Gitpod)로 나눠 접근할 때."
---

# Developer Onboarding 자동화 가이드

개발자 온보딩 자동화, Time-to-First-Deploy 최적화, 셀프서비스 환경 구축

## Quick Reference (결정 트리)

```
온보딩 자동화 수준?
    │
    ├─ Level 1: 문서화 ─────> README, Wiki 정리
    │       │
    │       └─ 수동 설정, 1-2주 소요
    │
    ├─ Level 2: 스크립트 ───> 셋업 스크립트, dotfiles
    │       │
    │       └─ 반자동, 2-3일 소요
    │
    ├─ Level 3: 플랫폼 ────> IDP, Dev Container, Gitpod
    │       │
    │       └─ 완전 자동화, 수 시간 내
    │
    └─ Level 4: AI 어시스트 ─> AI 가이드, 컨텍스트 자동 주입
            │
            └─ 즉시 생산성, Day 1 배포 가능
```

---

## CRITICAL: 온보딩 메트릭

```
┌─────────────────────────────────────────────────────────────────┐
│                  Developer Onboarding Metrics                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Time to First Deploy (TTFD)                                    │
│  ─────────────────────────                                      │
│  입사 → 첫 프로덕션 배포까지 시간                                 │
│                                                                  │
│  Elite:    < 1 day     (Day 1 Deploy)                           │
│  Good:     < 1 week                                             │
│  Medium:   < 2 weeks                                            │
│  Poor:     > 2 weeks   ← 많은 조직이 여기                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 목표: TTFD < 1 day = 개발자 경험 & 생산성 핵심 지표       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Additional Metrics:                                             │
│  - Time to First Commit: 첫 커밋까지 시간                        │
│  - Time to First PR: 첫 PR까지 시간                              │
│  - Environment Setup Time: 로컬 환경 구축 시간                   │
│  - Onboarding Satisfaction: 온보딩 만족도 (설문)                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 온보딩 단계별 목표

| 단계 | 목표 시간 | 완료 기준 |
|------|----------|-----------|
| Day 0 | 계정/접근 권한 | 모든 시스템 접근 가능 |
| Day 0.5 | 개발 환경 | 로컬에서 앱 실행 |
| Day 1 | 첫 커밋 | 작은 변경 커밋 |
| Day 1-2 | 첫 PR | 코드 리뷰 받기 |
| Day 2-3 | 첫 배포 | 프로덕션 배포 |
| Week 1 | 독립 작업 | 티켓 혼자 처리 |

---

## 온보딩 메트릭 수집

### 자동 TTFD 측정

```yaml
# .github/workflows/onboarding-metrics.yaml
name: Onboarding Metrics

on:
  pull_request:
    types: [closed]

jobs:
  track-first-deploy:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Check First Merged PR
        uses: actions/github-script@v7
        with:
          script: |
            const author = context.payload.pull_request.user.login;

            // 이전 머지된 PR 조회
            const prs = await github.rest.pulls.list({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'closed',
              creator: author
            });

            const mergedPRs = prs.data.filter(pr => pr.merged_at);

            if (mergedPRs.length === 1) {
              // 첫 머지!
              const user = await github.rest.users.getByUsername({
                username: author
              });

              // 계정 생성일 기준 TTFD 계산 (실제로는 입사일 사용)
              const createdAt = new Date(user.data.created_at);
              const mergedAt = new Date(context.payload.pull_request.merged_at);
              const ttfdDays = (mergedAt - createdAt) / (1000 * 60 * 60 * 24);

              // 메트릭 전송
              await fetch(process.env.METRICS_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  metric: 'time_to_first_deploy',
                  developer: author,
                  ttfd_days: ttfdDays,
                  first_pr_url: context.payload.pull_request.html_url
                })
              });

              // 축하 메시지
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.payload.pull_request.number,
                body: `## 🎊 첫 프로덕션 배포 완료!

                축하합니다 @${author}! 첫 코드가 프로덕션에 배포되었습니다!

                **Time to First Deploy**: ${ttfdDays.toFixed(1)} days

                이제 팀의 정식 기여자입니다! 🚀`
              });
            }
```

### Prometheus 메트릭

```promql
# 평균 TTFD (Time to First Deploy)
avg(onboarding_ttfd_days) by (team)

# TTFD 분포
histogram_quantile(0.5, sum(rate(onboarding_ttfd_days_bucket[30d])) by (le))
histogram_quantile(0.95, sum(rate(onboarding_ttfd_days_bucket[30d])) by (le))

# 환경 설정 시간
avg(onboarding_env_setup_minutes) by (method)  # devcontainer, local, gitpod

# 온보딩 완료율
sum(onboarding_completed_total) by (team)
/
sum(onboarding_started_total) by (team)

# 온보딩 만족도
avg(onboarding_satisfaction_score) by (team, quarter)
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 문서만 던져주기 | 컨텍스트 부족 | 인터랙티브 가이드 |
| 수동 계정 설정 | 1-2일 지연 | 셀프서비스 자동화 |
| 복잡한 로컬 설정 | 환경 불일치 | Dev Container |
| 첫 과제 난이도 높음 | 좌절감 | 단순한 첫 과제 |
| 멘토 미배정 | 질문 못함 | 자동 멘토 매칭 |
| TTFD 미측정 | 개선 불가 | 자동 메트릭 수집 |

---

## 체크리스트

### 자동화
- [ ] 셀프서비스 온보딩 포털
- [ ] 계정/권한 자동 프로비저닝
- [ ] Dev Container 또는 Gitpod 설정
- [ ] 첫 과제 자동 생성

### 문서화
- [ ] 인터랙티브 온보딩 가이드
- [ ] 아키텍처 다이어그램
- [ ] FAQ 문서
- [ ] 트러블슈팅 가이드

### 메트릭
- [ ] TTFD 자동 측정
- [ ] 환경 설정 시간 추적
- [ ] 온보딩 만족도 설문
- [ ] 대시보드 구축

### 멘토링
- [ ] 멘토 자동 할당
- [ ] 첫 PR 리뷰 가이드라인
- [ ] 정기 체크인 스케줄

**관련 skill**: `/dx:dx-onboarding-environment` (개발 환경), `/dx:dx-onboarding-deploy` (첫 배포), `/dx:dx-metrics`, `/platform:platform-backstage`
