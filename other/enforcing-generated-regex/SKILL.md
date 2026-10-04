---
name: enforcing-generated-regex
description: Force Regex to use GeneratedRegex Source Generator attribute instead of runtime Regex construction for compile-time optimization.
---

# GeneratedRegex Source Generator 강제

## 설명

`Regex`를 런타임에 `new Regex(...)` 또는 `Regex.IsMatch(pattern)` 형태로 생성하면 매번 정규식을 해석하고 컴파일해야 합니다.
`[GeneratedRegex]` 어트리뷰트를 사용하면 Source Generator가 컴파일 타임에 정규식을 최적화된 코드로 변환하여 성능과 메모리 효율이 크게 향상됩니다.

## 규칙

- `new Regex(pattern, RegexOptions.Compiled)` 대신 `[GeneratedRegex(pattern)]` 어트리뷰트를 사용합니다
- `[GeneratedRegex]`를 사용하는 클래스는 반드시 `partial`로 선언합니다
- 메서드 시그니처는 `private static partial Regex MethodName();` 형태입니다
- 호출 시 `MethodName()` (메서드 호출)으로 사용합니다
- `RegexOptions`가 필요하면 어트리뷰트 두 번째 인자로 전달합니다

## Worst Case (나쁜 예)

```csharp
// 런타임에 Regex를 생성 - 매번 해석/컴파일 비용 발생
public sealed class Validator
{
    private static readonly Regex EmailPattern = new(@"^[\w.+-]+@[\w-]+\.[\w.]+$", RegexOptions.Compiled);
    private static readonly Regex PhonePattern = new(@"^\d{2,3}-\d{3,4}-\d{4}$", RegexOptions.Compiled);

    public bool IsValidEmail(string email) => EmailPattern.IsMatch(email);
    public bool IsValidPhone(string phone) => PhonePattern.IsMatch(phone);
}
```

## Best Case (좋은 예)

```csharp
// GeneratedRegex로 컴파일 타임 최적화 - Source Generator가 코드 생성
public sealed partial class Validator
{
    [GeneratedRegex(@"^[\w.+-]+@[\w-]+\.[\w.]+$")]
    private static partial Regex EmailPattern();

    [GeneratedRegex(@"^\d{2,3}-\d{3,4}-\d{4}$")]
    private static partial Regex PhonePattern();

    public bool IsValidEmail(string email) => EmailPattern().IsMatch(email);
    public bool IsValidPhone(string phone) => PhonePattern().IsMatch(phone);
}
```

## RegexOptions가 필요한 경우

```csharp
// Worst Case
private static readonly Regex NamePattern = new(@"^[a-z]+$", RegexOptions.IgnoreCase | RegexOptions.Compiled);

// Best Case
[GeneratedRegex(@"^[a-z]+$", RegexOptions.IgnoreCase)]
private static partial Regex NamePattern();
```

## 적용 대상

- 모든 `new Regex(...)` 인스턴스 생성
- 모든 `static readonly Regex` 필드
- `Regex.IsMatch(input, pattern)` 정적 호출 (반복 사용 시)
- 테스트 코드의 정규식 패턴 (반복 실행되는 경우)
