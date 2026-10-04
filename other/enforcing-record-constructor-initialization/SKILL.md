---
name: enforcing-record-constructor-initialization
description: Force record instantiation via positional constructor with named arguments instead of property initializer syntax for stronger immutability expression.
---

# Record 생성자 초기화 강제

## 설명

`record`를 인스턴스화할 때 프로퍼티 초기화 구문(`new Record { Prop = value }`) 대신 생성자에 직접 값을 전달하는 방식(`new Record(Prop: value)`)을 사용합니다. 생성자 초기화는 컴파일 타임에 모든 필수 값의 전달을 강제하므로 더 강한 불변성을 표현하며, Named Arguments를 사용하면 가독성도 유지됩니다.

## 규칙

- `record` 인스턴스 생성 시 프로퍼티 초기화 구문(`{ get; init; }` + 객체 초기화자)을 사용하지 않습니다
- 생성자에 직접 값을 전달하는 방식을 사용합니다
- Named Arguments(`Name:`, `Email:` 등)를 사용하여 가독성을 확보합니다
- 이를 위해 `record` 정의 시 positional parameter를 사용하거나, `required` 프로퍼티 대신 생성자 매개변수를 활용합니다

## Worst Case (나쁜 예)

```csharp
// record 정의 - required + init 프로퍼티
public sealed record Employee
{
    public required string Name { get; init; }
    public required string Email { get; init; }
    public required string Tel { get; init; }
    public DateTime Joined { get; init; }
}

// 프로퍼티 초기화 구문 - 컴파일러가 누락을 잡지만 장황함
var employee = new Employee
{
    Name = "김철수",
    Email = "charles@clovf.com",
    Tel = "01075312468",
    Joined = new DateTime(2018, 3, 7)
};

// 파싱 시에도 프로퍼티 초기화
result.Add(new Employee
{
    Name = name,
    Email = email,
    Tel = tel,
    Joined = joined
});
```

## Best Case (좋은 예)

```csharp
// record 정의 - positional parameter (생성자 자동 생성)
public sealed record Employee(
    string Name,
    string Email,
    string Tel,
    DateTime Joined);

// 생성자 + Named Arguments - 간결하고 불변성이 명확
var employee = new Employee(
    Name: "김철수",
    Email: "charles@clovf.com",
    Tel: "01075312468",
    Joined: new DateTime(2018, 3, 7));

// 파싱 시에도 생성자 초기화
result.Add(new Employee(name, email, tel, joined));

// 짧은 경우 한 줄로 표현 가능
var emp = new Employee(Name: "박영희", Email: "matilda@clovf.com", Tel: "01087654321", Joined: default);
```

## 비교

| 항목 | 프로퍼티 초기화 | 생성자 초기화 |
|------|-----------------|---------------|
| 필수값 누락 방지 | `required`로 가능 | 컴파일러가 강제 |
| 불변성 표현 | 약함 (`init` 허용) | 강함 (생성자 전달) |
| 코드량 | 장황함 | 간결함 |
| 가독성 | 프로퍼티명 명시 | Named Args로 동일 |
| `with` 식 지원 | 지원 | 지원 |

## 적용 대상

- 모든 `record` 타입의 인스턴스 생성
- API 응답/요청 DTO
- 파싱 결과 객체 생성
- 테스트 데이터 생성
- Moq Setup의 반환값 생성
