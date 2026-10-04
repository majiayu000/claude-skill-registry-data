---
name: enforcing-json-options-predefine
description: Force JsonSerializerOptions to be declared as static readonly or readonly fields instead of creating new instances inside methods.
---

# JsonSerializerOptions 사전 정의 강제

## 설명

`JsonSerializerOptions`는 읽기 전용(ReadOnly) 객체로 설계되어야 합니다. 메서드 내부에서 매번 새로 생성하면 불필요한 메모리 할당과 성능 저하가 발생합니다.
`JsonSerializerOptions`는 내부적으로 리플렉션 캐시를 유지하므로, 재사용하면 직렬화/역직렬화 성능이 크게 향상됩니다.

## 규칙

- `JsonSerializerOptions`는 `static readonly` 필드 또는 `readonly` 인스턴스 필드로 사전 정의합니다
- 메서드 내부에서 `new JsonSerializerOptions { ... }` 를 직접 생성하지 않습니다
- 동일한 옵션 구성이 여러 곳에서 사용되면 공유 상수로 추출합니다

## Worst Case (나쁜 예)

```csharp
// 메서드 내부에서 매번 JsonSerializerOptions를 새로 생성 - 성능 저하
public string GenerateJson(int count)
{
    var data = GetData(count);

    // 매 호출마다 새 인스턴스 생성 -> 리플렉션 캐시 재생성 -> 느림
    var jsonContent = JsonSerializer.Serialize(data, new JsonSerializerOptions
    {
        WriteIndented = true,
        Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    });

    return jsonContent;
}

public async Task<T> Deserialize<T>(HttpResponseMessage response)
{
    var json = await response.Content.ReadAsStringAsync();
    // 매 호출마다 새 인스턴스 생성
    return JsonSerializer.Deserialize<T>(json, new JsonSerializerOptions
    {
        PropertyNameCaseInsensitive = true
    })!;
}
```

## Best Case (좋은 예)

```csharp
// static readonly로 사전 정의 - 리플렉션 캐시 재사용, 메모리 절약
private static readonly JsonSerializerOptions JsonWriteOptions = new()
{
    WriteIndented = true,
    Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
};

private static readonly JsonSerializerOptions JsonReadOptions = new()
{
    PropertyNameCaseInsensitive = true
};

public string GenerateJson(int count)
{
    var data = GetData(count);
    // 사전 정의된 옵션 재사용
    return JsonSerializer.Serialize(data, JsonWriteOptions);
}

public async Task<T> Deserialize<T>(HttpResponseMessage response)
{
    var json = await response.Content.ReadAsStringAsync();
    // 사전 정의된 옵션 재사용
    return JsonSerializer.Deserialize<T>(json, JsonReadOptions)!;
}
```

## 적용 대상

- 모든 `JsonSerializer.Serialize()` 호출에서 사용하는 옵션
- 모든 `JsonSerializer.Deserialize()` 호출에서 사용하는 옵션
- 테스트 코드의 JSON 직렬화/역직렬화 옵션
- 데이터 생성 도구의 JSON 출력 옵션
