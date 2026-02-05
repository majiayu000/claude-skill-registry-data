---
name: avalonia-customcontrol-architecture-design-basic
description: 'AvaloniaUI CustomControl를 활용한 AvaloniaUI Desktop Application Solution 기본 구조'
---

# 6.5 AXAML 코드 작성

- **AXAML 코드를 생성할 때는 CustomControl을 사용하여 ControlTheme을 통한 Stand-Alone Control Style 사용**
- 목적: 테마 분리 및 스타일 의존성 최소화

#### 6.5.1 AvaloniaUI Custom Control Library 프로젝트 구조

**권장 프로젝트 구조:**

```
YourAvaloniaSolution
├── YourCustomControlProject1/
│    ├── Properties/
│    │   ├── AssemblyInfo.cs            ← AssemblyInfo.cs 정의
│    ├── Themes/
│    │   ├── Generic.axaml            ← ControlTheme 정의
│    │   ├── CustomButton1.axaml       ← 개별 컨트롤 테마
│    │   └── CustomTextBox1.axaml      ← 개별 컨트롤 테마
│    ├── CustomButton1.cs
│    └── CustomTextBox1.cs
└── YourCustomControlProject2/
    ├── Properties/
    │   ├── AssemblyInfo.cs            ← AssemblyInfo.cs 정의
    ├── Themes/
    │   ├── Generic.axaml            ← ControlTheme 정의
    │   ├── CustomButton2.axaml       ← 개별 컨트롤 테마
    │   └── CustomTextBox2.axaml      ← 개별 컨트롤 테마
    ├── CustomButton2.cs
    └── CustomTextBox2.cs
```

# 6.6 ⚠️ ResourceInclude vs MergeResourceInclude 구분

- **ResourceInclude**: 일반 ResourceDictionary 파일 (Generic.axaml, Styles 등)에서 사용
- **MergeResourceInclude**: Application.Resources (App.axaml)에서만 사용

**장점:**

- ControlTheme 기반으로 테마와 로직 완전 분리
- CSS Class를 통한 유연한 스타일 변형
- Pseudo Classes (:pointerover, :pressed 등)를 통한 상태 관리
- ResourceInclude를 통한 테마 모듈화
- 팀 작업 시 파일 단위로 작업 분리 가능

#### 6.5.2 WPF vs AvaloniaUI 주요 차이점

| 항목        | WPF                                     | AvaloniaUI                           |
| ----------- | --------------------------------------- | ------------------------------------ |
| 파일 확장자 | .xaml                                   | .axaml                               |
| 스타일 정의 | Style + ControlTemplate                 | ControlTheme                         |
| 상태 관리   | Trigger, DataTrigger                    | Pseudo Classes, Style Selector       |
| CSS 지원    | ❌                                      | ✅ (Classes 속성)                    |
| 리소스 병합 | MergedDictionaries + ResourceDictionary | MergedDictionaries + ResourceInclude |
| 의존성 속성 | DependencyProperty                      | StyledProperty, DirectProperty       |
