---
name: monggle-smart-qa
version: 1.0.0
description: |
  Smart QA testing - Project auto-detection + platform-specific tests (monggle)
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
triggers:
  - /qa
  - /smart-qa
  - /code-qa
  - monggle qa
---

# smart-qa (monggle)

프로젝트 자동 감지 및 플랫폼별 QA 테스트

**Usage:** `/smart-qa [options] [platform]`

**자동 감지 플랫폼:**
- `--android` - Android 프로젝트 (.kt, .java, AndroidManifest.xml)
- `--ios` - iOS 프로젝트 (.swift, .m, .h, .xib)
- `--web` - Web 프론트엔드 (.ts, .tsx, .js, .css)
- `--mobile` - Mobile 전체 (Android + iOS)
- `--server` - 서버/백엔드 (.py, .go, .java)
- `--code` - 코드 전체 (모든 언어)

```bash
/smart-qa                   # 자동 감지 + 전체 테스트 + 수정
/smart-qa --android         # Android만 테스트
/smart-qa --web --report    # Web 보고서만
```

## 보고서 전용 모드 (--report)

읽기 전용 모드 - 코드 수정 없이 보고서만 생성

```bash
/smart-qa --report          # 자동 감지 + 보고서만
/smart-qa --ios --report    # iOS 보고서
```

## 옵션

| 옵션 | 설명 |
|-----|------|
| `--android` | Android 프로젝트 테스트 |
| `--ios` | iOS 프로젝트 테스트 |
| `--web` | Web 프론트엔드 테스트 |
| `--mobile` | Mobile (Android + iOS) |
| `--server` | 서버/백엔드 테스트 |
| `--code` | 코드 전체 테스트 |
| `--report` | 보고서만 생성 (smart-qa만) |
| `--quick` | 빠른 스모크 테스트 |
| `--format <fmt>` | 출력 형식: json\|text\|markdown |
| `--verbose, -v` | 상세 출력 |

## 자동 감지 규칙

| 플랫폼 | 감지 파일 |
|--------|----------|
| Android | build.gradle*, AndroidManifest.xml |
| iOS | *.xcodeproj, Podfile, Info.plist |
| Web | package.json (react, vue, angular) |
| Server | requirements.txt, go.mod, pom.xml |
| Mobile | Android + iOS 결합 |

## 테스트 항목

1. **Syntax Check** - Shell, Python, JS/TS 문법
2. **Code Quality** - TODO/FIXME 주석 확인
3. **Debug Statements** - console.log/print 문 확인
4. **Git Status** - 커밋되지 않은 파일 확인
