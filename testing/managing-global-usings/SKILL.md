---
name: managing-global-usings
description: Centralize external namespace imports (BCL, FCL, NuGet) in a GlobalUsings.cs file per project, keeping individual files clean.
---

# GlobalUsings.cs로 외부 네임스페이스 중앙 관리

## 설명

프로젝트 내에서 반복적으로 사용되는 외부 네임스페이스(`System.*`, NuGet 패키지 등)를 `GlobalUsings.cs` 파일에 `global using`으로 선언하여 개별 파일의 `using` 문을 최소화합니다.

## 규칙

- 각 프로젝트 루트에 `GlobalUsings.cs` 파일을 생성합니다
- .NET BCL/FCL 네임스페이스(`System.*`, `Microsoft.*` 등)는 `global using`으로 등록합니다
- NuGet 패키지 네임스페이스(`Bogus`, `Moq`, `Scalar.AspNetCore` 등)는 `global using`으로 등록합니다
- 솔루션 내부 프로젝트의 네임스페이스(예: `CompanyC.Api`)는 `global using`에 등록하지 않습니다
- 개별 파일에서는 `GlobalUsings.cs`에 등록된 네임스페이스의 `using` 문을 제거합니다
- 알파벳 순으로 정렬합니다

## Worst Case (나쁜 예)

```csharp
// EmployeeApiTests.cs - 모든 파일마다 동일한 using 반복
using System.Net;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc.Testing;

namespace CompanyC.Api.IntegrationTests;

public class EmployeeApiTests { ... }
```

```csharp
// EmployeeBogusTests.cs - 같은 using 또 반복
using System.Net;
using System.Text;
using System.Text.Json;
using CompanyC.Api;
using Microsoft.AspNetCore.Mvc.Testing;

namespace CompanyC.Api.IntegrationTests;

public class EmployeeBogusTests { ... }
```

## Best Case (좋은 예)

```csharp
// GlobalUsings.cs - 외부 네임스페이스를 한 곳에서 관리
global using System.Net;
global using System.Net.Http.Headers;
global using System.Text;
global using System.Text.Json;
global using Bogus;
global using Microsoft.AspNetCore.Mvc.Testing;
global using Microsoft.Extensions.DependencyInjection;
global using Moq;
```

```csharp
// EmployeeApiTests.cs - 외부 using 없이 깔끔
namespace CompanyC.Api.IntegrationTests;

public class EmployeeApiTests { ... }
```

```csharp
// EmployeeBogusTests.cs - 내부 네임스페이스만 유지
using CompanyC.Api;

namespace CompanyC.Api.IntegrationTests;

public class EmployeeBogusTests { ... }
```

## 적용 대상

- 솔루션 내 모든 프로젝트 (API, 테스트, 도구)
- .NET BCL/FCL 네임스페이스 (`System.*`, `Microsoft.*`)
- NuGet 패키지 네임스페이스
- 2개 이상의 파일에서 사용되는 외부 네임스페이스

## 제외 대상

- 솔루션 내부 프로젝트 네임스페이스 (예: `using CompanyC.Api;`)
- 단일 파일에서만 사용되는 특수 네임스페이스
