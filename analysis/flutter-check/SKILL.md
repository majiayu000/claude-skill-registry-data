---
name: flutter-check
description: 코드 변경 후 CI와 동일하게 정적분석·테스트를 돌려 회귀를 막는다. Dart/Flutter 코드를 수정한 뒤, 커밋/PR 전, "분석 돌려줘", "테스트 실행", "CI 통과 확인" 요청 시 사용.
---

# 정적분석 & 테스트 (CI 동기화)

CI(`.github/workflows/ci.yml`)는 master 푸시·PR에서 `flutter analyze`와
`flutter test`를 돌린다. **로컬에서 미리 같은 걸 돌려** CI 실패를 막는다.

## 실행

```bash
flutter pub get       # 의존성 변경/최초 1회
flutter analyze       # 정적 분석 (lint 포함)
flutter test          # 단위 테스트
```

- CI 고정 버전: **Flutter 3.44.8 stable**. 로컬 버전이 다르면 분석 결과가
  어긋날 수 있으니 `flutter --version`으로 확인.
- lint 설정은 `analysis_options.yaml` — `prefer_const_*` 룰이 켜져 있어
  const 누락도 경고로 잡힌다. analyze 경고는 0으로 유지한다.

## 테스트 작성 규칙 (이 프로젝트 관례)

테스트는 **Firebase/네트워크/GetX 레지스트리 없이 도는 순수 로직만** 검증한다
(`test/` 기존 파일 참고).

- `GlobalController`는 `_fireStore`가 `late final`이라 **Firestore 호출 전까지
  초기화되지 않는다** → 그냥 `GlobalController()`로 생성해 RxList에 값을 주입하고
  getter(필터/정렬/페어링)만 검증한다.
- `YouTubeController`는 `GlobalController`를 생성자로 주입해 테스트한다
  (`loadVideos` 등 네트워크 경로는 호출하지 않는다).
- 모델(`LiveCheckModel` 등)의 파생 getter는 결정적이므로 직접 검증한다.

## 주의: CI Firebase 스텁

`lib/default_firebase_options.dart`는 실제 키를 담고 있어 gitignore된다. CI는
이 파일을 placeholder 스텁으로 **자동 생성**하므로, 이 파일을 커밋하거나
스텁 생성 스텝을 건드리지 않는다.
