---
name: checklist
description: "C#, WPF, AvaloniaUI 코딩 전 확인 체크리스트"
---

# 9. 체크리스트

코드 작성 전 확인사항:

**일반 C# 코딩:**
- [ ] 최신 .NET 버전 사용
- [ ] Context7 MCP로 최신 C# 문법 확인
- [ ] sealed 키워드 적용 가능 여부 확인
- [ ] Primary constructor 적용 가능 여부 확인
- [ ] GlobalUsings.cs 파일 생성
- [ ] File scope namespace 사용
- [ ] Early Return 패턴 적용
- [ ] Pattern Matching 활용
- [ ] Literal string은 const로 정의
- [ ] Span<T> 사용 시 async-await 충돌 확인
- [ ] 한글 메시지와 영문 메시지 병기
- [ ] GenericHost 및 DI(Dependency Injection) 설정
- [ ] Constructor Injection 패턴 사용
- [ ] ServiceProvider 직접 사용 지양 (Service Locator 패턴 금지)

**WPF 프로젝트:**
- [ ] WPF ViewModel에 System.Windows 참조 없음 확인
- [ ] ViewModel 프로젝트에서 WindowsBase.dll 참조 제거
- [ ] ViewModel 프로젝트에서 PresentationFramework.dll 참조 제거
- [ ] ViewModel은 순수 BCL 타입만 사용 (IEnumerable, ObservableCollection 등)
- [ ] Custom Control Library에서 AssemblyInfo.cs를 Properties 폴더로 이동
- [ ] Generic.xaml은 MergedDictionaries 허브로만 사용
- [ ] 각 컨트롤 스타일을 개별 XAML 파일로 분리
- [ ] CollectionView 사용 시 Service Layer 패턴 적용
- [ ] App.xaml.cs에서 GenericHost 설정 및 DI 컨테이너 구성
- [ ] MainWindow 및 ViewModel을 DI 컨테이너에 등록
- [ ] View와 ViewModel을 Constructor Injection으로 연결

**AvaloniaUI 프로젝트:**
- [ ] AvaloniaUI ViewModel에 Avalonia 참조 없음 확인
- [ ] ViewModel 프로젝트에서 Avalonia.Base.dll, Avalonia.Controls.dll 참조 제거
- [ ] ViewModel은 순수 BCL 타입만 사용 (IEnumerable, ObservableCollection 등)
- [ ] CustomControl은 기존 Avalonia 컨트롤 상속 (예: Button, TextBox 등)
- [ ] CustomControl에서 StyledProperty 사용
- [ ] Generic.axaml은 MergedDictionaries 허브로만 사용
- [ ] 각 컨트롤 ControlTheme을 개별 AXAML 파일로 분리
- [ ] CSS Class 기반 스타일 적용 (Classes 속성)
- [ ] Pseudo Classes를 사용한 상태 관리 (:pointerover, :pressed 등)
- [ ] CollectionView 대신 DataGridCollectionView 또는 ReactiveUI 사용
- [ ] App.axaml.cs에서 GenericHost 설정 및 DI 컨테이너 구성
- [ ] MainWindow 및 ViewModel을 DI 컨테이너에 등록
- [ ] View와 ViewModel을 Constructor Injection으로 연결

---

