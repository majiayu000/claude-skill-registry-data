---
name: wpf-project-structure
description: "WPF 솔루션 및 프로젝트 구조 설계 가이드 (Abstractions, Core, ViewModels, Services)"
---

# WPF 솔루션 및 프로젝트 구조

WPF 프로젝트의 솔루션 및 프로젝트 구조 설계 가이드입니다.

## 솔루션 구조 원칙

**솔루션 이름은 애플리케이션 이름**
- 예시: `GameDataTool` 솔루션 = 실행 가능한 .NET Assembly 이름

## 프로젝트 명명 규칙

```
SolutionName/
├── SolutionName.Abstractions      // .NET Class Library (Interface, abstract class 등 추상 타입)
├── SolutionName.Core              // .NET Class Library (비즈니스 로직, 순수 C#)
├── SolutionName.Core.Tests        // xUnit Test Project
├── SolutionName.ViewModels        // .NET Class Library (MVVM ViewModel)
├── SolutionName.WpfServices       // WPF Class Library (WPF 관련 서비스)
├── SolutionName.WpfLib            // WPF Class Library (재사용 가능한 WPF 컴포넌트)
├── SolutionName.WpfApp            // WPF Application Project (실행 진입점)
├── SolutionName.UI                // WPF Custom Control Library (커스텀 컨트롤)
└── [Solution Folders]
    ├── SolutionName/              // 주요 프로젝트 그룹
    └── Common/                    // 범용 프로젝트 그룹
```

## 프로젝트 타입별 명명

- `.Abstractions`: .NET Class Library - Interface, abstract class 등 추상 타입 정의 (Inversion of Control)
- `.Core`: .NET Class Library - 비즈니스 로직, 데이터 모델, 서비스 (UI 프레임워크 독립)
- `.Core.Tests`: xUnit/NUnit/MSTest Test Project
- `.ViewModels`: .NET Class Library - MVVM ViewModel (UI 프레임워크 독립)
- `.WpfServices`: WPF Class Library - WPF 관련 서비스 (DialogService, NavigationService 등)
- `.WpfLib`: WPF Class Library - 재사용 가능한 WPF UserControl, Window, Converter, Behavior, AttachedProperty
- `.WpfApp`: WPF Application Project - 실행 진입점, App.xaml
- `.UI`: WPF Custom Control Library - ResourceDictionary 기반 커스텀 컨트롤

## 프로젝트 의존성 계층

```
SolutionName.WpfApp
    ↓ 참조
SolutionName.Core
    ↓ 참조
SolutionName.Abstractions (최상단 - 다른 프로젝트에 의존하지 않음)
```

## Abstractions 레이어의 역할

- 모든 Interface와 abstract class 보관
- 구체 타입을 직접 참조하지 않고 추상 타입으로 의존성 역전 (Dependency Inversion Principle)
- 런타임에 DI 컨테이너를 통해 실제 구현체 주입
- 테스트 시 Mock 객체로 교체 가능

## Solution Folder 활용

### 범용 기능 분리

```
Solution 'GameDataTool'
├── Solution Folder: GameDataTool
│   ├── GameDataTool.Abstractions
│   ├── GameDataTool.Core
│   ├── GameDataTool.Core.Tests
│   ├── GameDataTool.ViewModels
│   ├── GameDataTool.WpfServices
│   ├── GameDataTool.WpfLib
│   ├── GameDataTool.WpfApp
│   └── GameDataTool.UI
└── Solution Folder: Common
    ├── Common.Utilities
    ├── Common.Logging
    └── Common.Configuration
```

### 규칙

- 애플리케이션 고유 기능: `SolutionName` Solution Folder에 배치
- 범용/재사용 기능: `Common` Solution Folder에 배치
- Solution Folder는 가상 폴더 (실제 파일 시스템과 무관)

## 실제 예시

```
Solution 'GameDataTool'
├── GameDataTool (Solution Folder)
│   ├── GameDataTool.Abstractions
│   │   ├── Services/
│   │   │   ├── IUserService.cs
│   │   │   └── IDataService.cs
│   │   └── Repositories/
│   │       ├── IUserRepository.cs
│   │       └── IDataRepository.cs
│   ├── GameDataTool.Core
│   │   ├── Models/
│   │   ├── Services/
│   │   │   ├── UserService.cs
│   │   │   └── DataService.cs
│   │   └── Repositories/
│   │       ├── UserRepository.cs
│   │       └── DataRepository.cs
│   ├── GameDataTool.Core.Tests
│   │   └── Services/
│   ├── GameDataTool.ViewModels
│   │   ├── MainViewModel.cs
│   │   ├── HomeViewModel.cs
│   │   └── SettingsViewModel.cs
│   ├── GameDataTool.WpfServices
│   │   ├── DialogService.cs
│   │   ├── NavigationService.cs
│   │   └── WindowService.cs
│   ├── GameDataTool.WpfLib
│   │   ├── Controls/
│   │   ├── Converters/
│   │   ├── Behaviors/
│   │   └── AttachedProperties/
│   ├── GameDataTool.WpfApp
│   │   ├── App.xaml
│   │   └── Views/
│   └── GameDataTool.UI
│       ├── Themes/
│       └── CustomControls/
└── Common (Solution Folder)
    ├── Common.Utilities
    ├── Common.Logging
    └── Common.Configuration
```
