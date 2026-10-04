---
name: enforcing-dto-record
description: Force all DTO (Data Transfer Object) types to be declared as record instead of class for immutability and value-based equality.
---

# DTO는 record로 구현 강제

## 설명

DTO(Data Transfer Object)는 읽기 전용(ReadOnly) 객체입니다. C#에서 `class`가 아닌 `record`로 구현해야 합니다.
`record`는 불변성(immutability), 값 기반 동등성(value equality), `with` 식을 기본 제공하므로 DTO에 최적입니다.

## 규칙

- 모든 DTO 클래스는 `class` 대신 `record`로 선언합니다
- 응답/요청 전용 객체, 직렬화/역직렬화 전용 객체가 대상입니다
- 엔티티(Entity)나 상태 변경이 필요한 도메인 모델은 제외합니다
- `sealed class` + `{ get; set; }` 패턴을 `record` + 위치 매개변수(positional parameter) 또는 `{ get; init; }` 패턴으로 변환합니다

## Worst Case (나쁜 예)

```csharp
// DTO를 class로 구현 - 불변성 보장 없음, 보일러플레이트 과다
private sealed class PagedResponse
{
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int TotalCount { get; set; }
    public int TotalPages { get; set; }
    public EmployeeDto[] Data { get; set; } = [];
}

private sealed class CreatedResponse
{
    public int Count { get; set; }
    public EmployeeDto[] Data { get; set; } = [];
}

private sealed class EmployeeDto
{
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
    public string Tel { get; set; } = "";
    public DateTime Joined { get; set; }
}

// JSON 역직렬화용 DTO를 class로 구현
private sealed class JsonEmployeeDto
{
    public string? Name { get; set; }
    public string? Email { get; set; }
    public string? Tel { get; set; }
    public string? Joined { get; set; }
}
```

## Best Case (좋은 예)

```csharp
// DTO를 record로 구현 - 불변성 보장, 간결한 코드
private sealed record PagedResponse(
    int Page,
    int PageSize,
    int TotalCount,
    int TotalPages,
    EmployeeDto[] Data);

private sealed record CreatedResponse(
    int Count,
    EmployeeDto[] Data);

private sealed record EmployeeDto(
    string Name,
    string Email,
    string Tel,
    DateTime Joined);

// JSON 역직렬화용 DTO도 record로 구현
private sealed record JsonEmployeeDto(
    string? Name,
    string? Email,
    string? Tel,
    string? Joined);
```

## 적용 대상

- API 응답/요청 DTO
- JSON 직렬화/역직렬화 매핑 객체
- 테스트 코드의 역직렬화 DTO
- 내부 데이터 전달용 객체
