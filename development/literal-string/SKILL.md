---
name: literal-string
description: "C# Literal string을 const string으로 사전 정의하여 사용하는 패턴"
---

# Literal String 처리

C# 코드에서 Literal string을 처리하는 방법에 대한 가이드입니다.

## 규칙

**Literal string에 대해서는 가급적 `const string`으로 사전에 정의하여 사용할 것**

## 예시

### 좋은 예

```csharp
// 좋은 예
const string ErrorMessage = "오류가 발생했습니다.";
// An error has occurred.

if (condition)
    throw new Exception(ErrorMessage);
```

### 나쁜 예

```csharp
// 나쁜 예
if (condition)
    throw new Exception("오류가 발생했습니다.");
```

## 이유

1. **유지보수성**: 메시지 변경 시 한 곳만 수정
2. **재사용성**: 동일한 메시지를 여러 곳에서 사용 가능
3. **타입 안전성**: 컴파일 타임에 오타 확인
4. **성능**: 문자열 리터럴 중복 제거
