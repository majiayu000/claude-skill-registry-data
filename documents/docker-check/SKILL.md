---
name: docker-check
description: Docker 설정 점검. 멀티스테이지 빌드, 헬스체크, 보안, 이미지 최적화 검토
allowed-tools: Read, Grep, Glob, Bash
---

# Docker Configuration Check

## Instructions
1. 모든 Dockerfile 및 docker-compose 파일 스캔
2. 다음 항목 점검:
   - 멀티스테이지 빌드 사용
   - 헬스체크 설정
   - 비root 사용자 설정
   - 이미지 크기 최적화
   - 레이어 캐싱 효율
3. 보안 설정 검토
4. 개선 보고서 생성

## Check Items
- [ ] 멀티스테이지 빌드 적용
- [ ] HEALTHCHECK 명령어 존재
- [ ] 비root 사용자 실행
- [ ] .dockerignore 파일 존재
- [ ] 불필요한 패키지 제거
- [ ] 시크릿 빌드타임 노출 없음
- [ ] 적절한 베이스 이미지 (slim/alpine)

## Output Format
```
## Docker Health Report

### Files Analyzed
- Dockerfile
- docker-compose.yaml

### Issues Found
| File | Issue | Severity |
|------|-------|----------|
| ...  | ...   | ...      |

### Optimization Opportunities
- [최적화 기회]

### Security Recommendations
- [보안 권장사항]
```
