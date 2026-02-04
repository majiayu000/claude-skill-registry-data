---
name: write-code
description: |
  코드 작성, 수정, 구현. Use when (1) "코드 작성해줘", "구현해줘",
  (2) 기능 추가/수정, (3) 버그 수정.
tools: [Read, Write, Edit, Bash, Glob, Grep]
model: inherit
---

> **🔔 호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: write-code` 시스템 메시지를 첫 줄에 출력하세요.

# write-code Skill

> 코드 작성, 수정, 기능 구현 통합 스킬

## 🔴 Extension 우선 라우팅

> **Extension 패키지가 설치되어 있으면 해당 패키지의 implement 스킬이 우선 호출됩니다.**

| Extension | 패턴 | 우선도 |
|-----------|------|--------|
| `eng/nextjs` | ADD Phase 4, DDD 4-layer | 1 |
| `eng/spring` | CQRS + Reactive | 2 |
| `biz/poc` | implement-mvp (간소화) | 3 |
| (없음) | 이 스킬 (기본) | 4 |

---

## Workflow

### 1. 요구사항 분석

```text
1. 사용자 요청 파악
2. 대상 파일/영역 식별
3. 변경 범위 결정
```

### 2. 기존 코드 파악

```bash
# 관련 파일 탐색
glob: "src/**/*.{ts,tsx}"
grep: "function|class|interface"

# 의존성 분석
read: package.json, tsconfig.json
```

### 3. 코드 작성/수정

```text
- 새 파일 생성: Write
- 기존 파일 수정: Edit
- 파일 삭제 필요 시: Bash rm
```

### 4. 검증

```bash
# 린트 및 타입 체크
npm run lint
npx tsc --noEmit

# 빌드 확인 (필요 시)
npm run build
```

---

## Quality Rules

### 필수 준수 사항

| 규칙 | 설명 |
|------|------|
| **기존 스타일 준수** | 프로젝트 코딩 컨벤션 따름 |
| **타입 안전성** | TypeScript strict 모드 준수 |
| **최소 변경** | 불필요한 리팩토링 금지 |
| **테스트 연동** | 변경 시 관련 테스트 확인 |

### 금지 패턴

- `any` 타입 사용 금지 (불가피한 경우 주석으로 사유 명시)
- 하드코딩된 값 (config로 분리)
- 중복 코드 작성 (기존 유틸 활용)

---

## 복잡한 구현 시

> 단순 코드 작성이 아닌 복잡한 기능 구현 시, 아래 워크플로우 권장

### Phased Implementation (선택적)

```text
1. PLANNING
   - 구현 계획 수립
   - 파일 구조 설계

2. SCAFFOLD
   - 디렉토리/파일 생성
   - 기본 구조 작성

3. IMPLEMENT
   - 핵심 로직 구현
   - 타입 정의

4. INTEGRATE
   - 기존 코드와 연동
   - 의존성 연결

5. VERIFY
   - 린트/타입 체크
   - 테스트 실행
```

---

## 출력 형식

### 작업 시작

```markdown
[SEMO] Skill: implement

📝 **작업**: {작업 요약}
📁 **대상**: {파일 경로}
```

### 작업 완료

```markdown
[SEMO] Skill: implement → 완료

✅ 변경 사항:
- {파일1}: {변경 내용}
- {파일2}: {변경 내용}

🔍 검증: lint ✅ | typecheck ✅
```

---

## 🔴 Post-Action: 체이닝 프롬프트 (NON-NEGOTIABLE)

> **⚠️ 구현 완료 후 반드시 다음 단계를 확인합니다.**

### 체이닝 플로우

```text
skill:write-code 완료
    │
    └→ "다음 단계" 프롬프트
           │
           ├─ "테스트 작성해줘" → skill:write-test
           │       │
           │       └→ "검증해줘" → skill:quality-gate
           │               │
           │               └→ "커밋해줘" → skill:git-workflow
           │
           ├─ "검증해줘" → skill:quality-gate (테스트 건너뜀)
           │
           └─ "커밋해줘" → skill:git-workflow (검증 건너뜀)
```

### 트리거 조건

```text
구현 완료 감지:
- 파일 생성/수정 완료
- lint + typecheck 통과
- 사용자 요청 작업 완료
    ↓
자동 프롬프트 출력
```

### 완료 시 출력

```markdown
[SEMO] Skill: write-code → 완료

✅ **구현 완료**: {작업 요약}
📁 **변경 파일**: {파일 목록}
🔍 **검증**: lint ✅ | typecheck ✅

---

💡 **다음 단계**:
   - "테스트 작성해줘" → skill:write-test 호출
   - "검증해줘" → skill:quality-gate 호출
   - "커밋해줘" → skill:git-workflow 호출
   - "아니" / "계속 작업" → 추가 작업 대기
```

### 사용자 응답별 동작

| 사용자 응답 | 동작 |
|------------|------|
| "테스트 작성해줘" | `skill:write-test` 호출 |
| "검증해줘" | `skill:quality-gate` 호출 |
| "커밋해줘" | `skill:git-workflow` 호출 |
| "푸시까지 해줘" | `skill:git-workflow` 호출 (push 포함) |
| "아니", "계속" | 추가 작업 대기 |
| 무응답 | 프롬프트만 표시, 대기 |

### 프롬프트 생략 조건

사용자가 아래 키워드 사용 시 프롬프트 건너뛰기:

- "프롬프트 없이"
- "커밋 안 해도 돼"
- "계속 작업할 거야"

---

## Related Skills

| Skill | 역할 | 연결 시점 |
|-------|------|----------|
| `git-workflow` | 커밋/푸시/PR | 구현 완료 후 |
| `tester` | 테스트 작성 | 구현 전/후 |
| `project-board` | 이슈 상태 변경 | PR 생성 시 |

---

## References

- [Quality Gate](../../semo-core/principles/QUALITY_GATE.md) - 코드 품질 기준
- [tester Skill](../tester/SKILL.md) - 테스트 작성
- [git-workflow Skill](../git-workflow/SKILL.md) - Git 워크플로우
