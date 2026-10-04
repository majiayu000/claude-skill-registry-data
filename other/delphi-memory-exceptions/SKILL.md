---
description: Good memory management practices, memory leak prevention and exception handling in Delphi
---

# 🧠 Memory and Exceptions Management in Delphi

## Contexto

Delphi has **manual memory management** for class instances (not derived from interfaces) and uses **ARC (Automatic Reference Counting)** only for interfaces (`IInterface`), Strings, Dynamic Arrays and anonymous types. Poor exception handling and forgetting to release memory result in chronic **Memory Leaks**, catastrophic production failures and systemic instability.

Like AI, you must proactively ensure that every object you create is freed regardless of error streams.

## Objectives of this Skill

- Teach how to generate safe blocks of `try..finally`.
- Prevent Memory Leaks by advising on `Free` and `FreeAndNil`.
- Promote the use of Interfaces for memory automation.
- Institute defensive and typed handling of Exceptions (`try..except`).
- Introduce custom Domain Exceptions.

---

## 🛑 Memory Management: Critical Rules

### 1. The Gold Standard: `try..finally`
Whenever an object instance is created and does not have an Owner who manages it, instantiate it in a `try..finally` block.
`try` must occur **IMMEDIATELY** on the line following creation.

```pascal
var
  LList: TStringList;
begin
  LList := TStringList.Create;
  try
    LList.Add('Item 1');
    // ...
  finally
    LList.Free;
  end;
end;
```

**Anti-Pattern (DO NOT USE):**
Code between `Create` and `try` may generate an exception, leaking the newly created object.
```pascal
  // ERRADO - vazamento em potencial!
  LList := TStringList.Create;
  LList.Add('Item 1');
  try
    // ...
```

### 2. Multiple Objects in the Same Block
When allocating multiple temporary resources in the same method, do not nest dozens of `try..finally` if it is not strictly necessary. But be careful to initialize them all with `nil` beforehand if there is a chance of leakage, or nest them prudently. The ideal pattern is guaranteed sequential release, but strict nesting is safest for chained allocations:

```pascal
var
  LStream: TMemoryStream;
  LReader: TStreamReader;
begin
  LStream := TMemoryStream.Create;
  try
    LReader := TStreamReader.Create(LStream);
    try
      // lógicas com ambos
    finally
      LReader.Free;
    end;
  finally
    LStream.Free;
  end;
end;
```

### 3. Avoid Creating Objects for Single Passage
If an API takes a class parameter, declare an interface or instantiate it before the method with `try..finally`. Never pass an inline `.Create` to a parameter in a method if you do not have an absolute guarantee that the consuming function will free the memory.

### 4. Garbage Collection via Intefaces
For Dependency Injection, Repository/Service Patterns or Temporary Functional Classes, use inheritance from `TInterfacedObject` linked to a `Interface`.
Delphi will kill the instance when the reference counter reaches zero.
```pascal
var
  LService: ICustomerService;
begin
  // Sem try..finally e sem chamadas de .Free.
  // Memória é varrida ao sair do escopo desta procedure.
  LService := TCustomerService.Create; 
  LService.ProcessDailyBatch;
end;
```

---

## 🚨 Exception Handling: The Transparent Standard

### 1. Specific, Not Generic Catches
Use `try..except` primarily to trap recoverable errors, log failures without breaking loops, or transform infrastructure exceptions into more semantic domain exceptions.
Never "Swallow" an exception without logical justification.

```pascal
try
  PerformDatabaseCommit;
except
  // Captura ESPECÍFICA de banco de data
  on E: EFDDBEngineException do
  begin
    Logger.Error('Falha no banco de dados [Cód: %d]: %s', [E.ErrorCode, E.Message]);
    raise EDatabaseConnectionException.Create('Serviço temporariamente indisponível.');
  end;
  // Captura ESPECÍFICA de validation
  on E: EValidationException do
  begin
    ShowWarning(E.Message);
  end;
end;
```

**Anti-Pattern (DO NOT USE):**
This blinds the application trace (hides `AccessViolations` and `Out of Memory`).
```pascal
try
  ProcessData;
except
  // Errado! Esconde qualquer erro do desenvolvedor durante debug!
end;
```

### 2. Creating Exceptions Based on Business Logic (DDD)
Do not use `raise Exception.Create(str)`. Declare cohesive exceptions to enable elegant interception by upper layers (REST Controllers, UI Interface).

```pascal
type
  // Domínio / Essência das Regras
  EBusinessRuleException = class(Exception);
  ECustomerLimitReachedException = class(EBusinessRuleException);
  
  // Infraestrutura
  EInfrastructureException = class(Exception);
  EDatabaseConnectionException = class(EInfrastructureException);
```

### 3. Encapsulating Errors and `Raise` without Modifying Context
If you only need to perform a one-off log but want the exception to flow naturally to the global UI, just use pure `raise;`.

```pascal
try
  SomeDangerousCall;
except
  on E: Exception do
  begin
    Logger.LogError('Critical failure', E);
    raise; // REPROJETA a exception original com a mesma stack-trace
  end;
end;
```

---

## 💡 AI Action Flow

When asked to write/refactor code:
1. Review whether each `TObject.Create` will result in a deallocation (`.Free` or Third-Party Ownership).
2. Inject `try..finally` if you notice legacy code without it.
3. If you generate Services, recommend Dependency Injection via Interfaces (`IService`) to simplify garbage scanning (GC).
4. In logic that may fail, create Typological Exceptions to validate flow and prevent error code spaghetti conditionals (`if return = -1 then`).
