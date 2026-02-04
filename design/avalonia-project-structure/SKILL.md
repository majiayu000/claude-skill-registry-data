---
name: avalonia-project-structure
description: "AvaloniaUI 솔루션 및 프로젝트 구조 설계 가이드"
---

# 6.2 AvaloniaUI 솔루션 및 프로젝트 구조

#### 6.2.1 프로젝트 명명 규칙

```
SolutionName/
├── SolutionName.Abstractions      // .NET Class Library (Interface, abstract class 등 추상 타입)
├── SolutionName.Core              // .NET Class Library (비즈니스 로직, 순수 C#)
├── SolutionName.Core.Tests        // xUnit Test Project
├── SolutionName.ViewModels        // .NET Class Library (MVVM ViewModel)
├── SolutionName.AvaloniaServices  // Avalonia Class Library (Avalonia 관련 서비스)
├── SolutionName.AvaloniaLib       // Avalonia Class Library (재사용 가능한 컴포넌트)
├── SolutionName.AvaloniaApp       // Avalonia Application Project (실행 진입점)
├── SolutionName.UI                // Avalonia Custom Control Library (커스텀 컨트롤)
└── [Solution Folders]
    ├── SolutionName/              // 주요 프로젝트 그룹
    └── Common/                    // 범용 프로젝트 그룹
```

**프로젝트 타입별 명명:**
- `.Abstractions`: .NET Class Library - Interface, abstract class 등 추상 타입 정의 (Inversion of Control)
- `.Core`: .NET Class Library - 비즈니스 로직, 데이터 모델, 서비스 (UI 프레임워크 독립)
- `.Core.Tests`: xUnit/NUnit/MSTest Test Project
- `.ViewModels`: .NET Class Library - MVVM ViewModel (UI 프레임워크 독립)
- `.AvaloniaServices`: Avalonia Class Library - Avalonia 관련 서비스 (DialogService, NavigationService 등)
- `.AvaloniaLib`: Avalonia Class Library - 재사용 가능한 UserControl, Window, Converter, Behavior, AttachedProperty
- `.AvaloniaApp`: Avalonia Application Project - 실행 진입점, App.axaml
- `.UI`: Avalonia Custom Control Library - ControlTheme 기반 커스텀 컨트롤

**프로젝트 의존성 계층:**
```
SolutionName.AvaloniaApp
    ↓ 참조
SolutionName.Abstractions (최상단 - 다른 프로젝트에 의존하지 않음)
    ↓ 참조
SolutionName.Core
```

**Abstractions 레이어의 역할:**
- 모든 Interface와 abstract class 보관
- 구체 타입을 직접 참조하지 않고 추상 타입으로 의존성 역전 (Dependency Inversion Principle)
- 런타임에 DI 컨테이너를 통해 실제 구현체 주입
- 테스트 시 Mock 객체로 교체 가능

