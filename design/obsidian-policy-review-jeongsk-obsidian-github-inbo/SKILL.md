---
name: obsidian-policy-review
description: |
  Obsidian 플러그인 코드가 공식 가이드라인을 준수하는지 검토하고 개선점을 제안한다.

  Use when:
  - 사용자가 Obsidian 플러그인 가이드라인 준수 여부를 확인하고 싶을 때
  - 플러그인을 커뮤니티 스토어에 제출하기 전 검토가 필요할 때
  - 코드 품질, 보안, 성능, UI/UX 검토가 필요할 때
  - "가이드라인", "정책 검토", "코드 리뷰", "policy review" 등의 키워드가 언급될 때
  - README에 필수 공개 항목을 추가해야 할 때
---

# Obsidian Plugin Policy Review

Obsidian 플러그인이 [개발자 정책](https://docs.obsidian.md/Developer+policies)과 [플러그인 가이드라인](https://docs.obsidian.md/Plugins/Releasing/Plugin+guidelines)을 준수하는지 검토한다.

## 검토 절차

### 1. 코드베이스 탐색

다음 파일들을 확인:
- `manifest.json` - 플러그인 메타데이터
- `package.json` - 의존성 패키지
- `LICENSE` - 라이센스 파일
- `README.md` - 공개 정보 명시 여부
- `styles.css` - CSS 스타일링
- `src/**/*.ts` - 소스 코드 전체

### 2. 개발 가이드라인 검토

상세 체크리스트: [references/plugin-guidelines.md](references/plugin-guidelines.md)

#### 보안 검사
```bash
grep -rn "innerHTML\s*=" src/
grep -rn "outerHTML\s*=" src/
grep -rn "insertAdjacentHTML" src/
```
**위반 시**: `createEl()`, `createDiv()`, `createSpan()` 사용 권장

#### 성능 검사
```bash
grep -rn "vault.adapter" src/
grep -rn "getFiles().forEach" src/
grep -rn "getAllFolders" src/
```
**위반 시**: Vault API 우선 사용, `getFileByPath()`, `vault.process()` 권장

#### 코드 품질 검사
```bash
grep -rn "^var\s" src/
grep -rn "window.app" src/
grep -rn "\.then\s*(" src/
```
**위반 시**: `const`/`let`, `this.app`, `async/await` 권장

#### 모바일 호환성 검사
```bash
grep -rn "require.*fs" src/
grep -rn "require.*electron" src/
grep -rn "child_process" src/
```
**위반 시**: 모바일 미지원이면 `isDesktopOnly: true` 설정

#### 스타일링 검사
```bash
grep -rn 'style="' src/
grep -rn "color:\s*#" styles.css
grep -rn "background:\s*#" styles.css
```
**위반 시**: CSS 클래스 및 Obsidian CSS 변수 사용 권장

### 3. 정책 준수 검토

상세 체크리스트: [references/policy-checklist.md](references/policy-checklist.md)

**금지 사항**:
| 항목 | 검색 패턴 |
|------|----------|
| 코드 난독화 | 빌드 설정 확인 |
| 동적 광고 | `fetch`, `XMLHttpRequest`로 광고 로드 |
| 클라이언트 텔레메트리 | analytics, tracking 관련 코드 |

**공개 필수 항목** (README 명시 필요):
| 항목 | 확인 방법 |
|------|----------|
| 원격 서비스 | 외부 API 호출 코드 존재 시 |
| 계정 필요성 | API 키나 로그인 필요 시 |
| Vault 외부 접근 | `fs`, `path` 모듈 사용 시 |
| 개인정보처리 | 서버로 데이터 전송 시 |

### 4. 검토 보고서 작성

결과를 테이블로 정리:

```markdown
## 가이드라인 검토 결과

| 카테고리 | 항목 | 상태 | 설명 |
|----------|------|------|------|
| 보안 | innerHTML 사용 금지 | ✅/❌ | ... |
| 성능 | Vault API 사용 | ✅/❌ | ... |
| 코드 품질 | const/let 사용 | ✅/❌ | ... |
| 모바일 | Node.js API 미사용 | ✅/❌ | ... |
| 스타일링 | CSS 변수 사용 | ✅/❌ | ... |

## 정책 준수 결과

| 항목 | 상태 | 설명 |
|------|------|------|
| 금지 사항 미위반 | ✅/❌ | ... |
| README 공개 항목 | ✅/❌ | ... |
```

### 5. 수정 사항 적용

README 템플릿 참고: [references/readme-template.md](references/readme-template.md)

위반 사항 발견 시:
1. 코드 수정이 필요한 경우 구체적인 수정 방법 제시
2. README 업데이트가 필요한 경우 섹션 추가

## 주의사항

- `bypassPermissions` 사용 시 반드시 경고 표시
- API 키 평문 저장 시 보안 권고사항 추가
- 디버그 모드에서 민감 정보 로깅 여부 확인
