---
name: qa-workflow-manager
description: Manage QA test case workflows, status transitions, and verification checklists. Use when working with QA status states (Reviewing, DevError, ProdError, DevDone, ProdDone, Hold, Rejected, Duplicate), progress tracking (Waiting, Checking, Working, DevDeployed, ProdDeployed), activity logging, or test case management.
---

# QA Workflow Manager

QA 테스트케이스 워크플로우, 상태 전이, 검증 체크리스트를 관리하는 전문 스킬입니다.

## Quick Reference

### 상태 (Status)
| 상태 | 한글 | 색상 |
|------|------|------|
| Reviewing | 검토중 | yellow |
| DevError | Dev 오류 | red |
| ProdError | Prod 오류 | red |
| DevDone | Dev 완료 | blue |
| ProdDone | Prod 완료 | green |
| Hold | 보류 | gray |
| Rejected | 반려 | red |
| Duplicate | 중복 | gray |

### 진행 단계 (Progress)
```
Waiting → Checking → Working → DevDeployed → ProdDeployed
```

## Contents

- [reference.md](reference.md) - 상태 머신 및 전이 규칙 상세
- [guide.md](guide.md) - 액티비티 로깅 및 검증 체크리스트 패턴
- [scripts/validate_status_transition.py](scripts/validate_status_transition.py) - 상태 전이 검증
- [scripts/generate_activity_log.py](scripts/generate_activity_log.py) - 액티비티 로그 생성

## When to Use

- QA 테스트케이스 상태 변경 로직 작성 시
- 배포 환경별(Dev/Prod) 진행 상태 추적 시
- 검증 체크리스트 구현 시
- 반려 사유 처리 로직 작성 시
- 액티비티 로그 기록 시
