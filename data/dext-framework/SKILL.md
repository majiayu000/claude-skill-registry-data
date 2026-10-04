---
name: Dext Framework Patterns
description: Architectural patterns, Entity ORM, Minimal APIs and dependency injection for projects created with Dext Framework (cesarliws/dext).
---

# Dext Framework Patterns (Delphi)

The **Dext Framework** is a complete ecosystem for Delphi, directly inspired by **ASP.NET Core** and **Spring Boot**. It is intended for high-performance corporate development. Unlike Horse or DMVC, Dext embraces Dependency Injection, Minimal APIs with automatic model binding and has its own Entity ORM (`Dext.Entity`).

This manual provides the conventions that must be followed by the AI ​​when coding with Dext.

**Important Note:** Dext Framework is **not** short for DevExpress/DevExtreme visual components, but rather the backend project (https://github.com/cesarliws/dext).

## Core Principles

1. **Minimal Routing (Minimal APIs):** Do not use traditional MVC Controllers unless necessary. Use functional routing syntax (`MapGet`, `MapPost`).
2. **Auto Model Binding:** Get JSON body not via strings and partial conversions, but by delegating strong typing to anonymous route parameters (`function(Dto: MyDto): IResult`).
3. **Integrated DI Container:** All interface dependencies must be resolved via `App.Services` (Injection). Do not use manual factories.
4. **Smart ORM (Dext.Entity):** Never concatenate SQL.

---

## 1. WebApp Lifecycle and DI

Bootstrap of a Dext API occurs by registering services in the same route pipeline.

```pascal
program MyAPI;

uses Dext.Web, Services.Interfaces, Services.Implementations;

begin
  var App := WebApplication;
  var Builder := App.Builder;

  //1. Registration of Dependency Injection Services
  App.Services.AddSingleton<IEmailService, TEmailService>;
  App.Services.AddScoped<IOrderRepository, TOrderRepository>;

  //2. Route Mapping
  Builder.MapGet<IResult>('/health', 
    function: IResult
    begin
        Result := Results.Ok('{"status": "ok"}');
    end);

  //3. Start
  App.Run(8080);
end.
```

---

## 2. Minimal APIs & Model Binding

The preferred way to build REST APIs with Dext is using typed anonymous delegates, with DI dependencies passed in the final arguments.

### Create user (Post + DTO Body + Auth)

```pascal
type
  TCreateUserDto = record
    Name: string;
    Age: Integer;
  end;

//'Dto' is populated via JSON from the request body automatically.
//'Database' is injected via DI.
Builder.MapPost<TCreateUserDto, IDatabaseService, IResult>('/users',
  function(Dto: TCreateUserDto; Database: IDatabaseService): IResult
  begin
    if Dto.Name.IsEmpty then
        Exit(Results.BadRequest('Name is required'));

    Database.SaveUser(Dto.Name, Dto.Age);
    
    Result := Results.Created('/users/new', 'User Created');
  end);
```

### Path Params & Query

```pascal
//Typed path-based routing (Route parameter Binding)
Builder.MapGet<Integer, IResult>('/orders/{id}',
  function(Id: Integer): IResult
  begin
    var Order := FindOrder(Id);
    if Order = nil then
      Result := Results.NotFound
    else
      Result := Results.Ok(Order);
  end);
```

---

## 3. Dext.Entity (ORM & Smart Properties)

Database mapping with Dext is focused on strongly typed query building and "Code First" Classes.

### LINQ-Like Queries

Avoid using complex RTTI or native ADOTables if you are on Dext. Deliver results in typed Collections (`IList<T>`).

```pascal
uses Dext.Entity;

//P is the Smart Property representation for the context class
var Products := DbContext.Products
  .Where((P.Price > 100) and (P.Stock > 0))  //'and' bitwise/Smart property syntax
  .OrderBy(P.Name)
  .Take(10)
  .ToList;
```

### Understanding "Mass Update" via Dext.Entity

With Dext ORM, Updates can run in the database without pulling data into memory (as done in modern Entity Framework Core):

```pascal
DbContext.Orders
  .Where(O.Status = 'Pending')
  .Update
  .Execute;
```

---

## 4. Returns (IResult)

Always return `IResult`-based implementations on endpoints using the `Results` factory.

- `Results.Ok( MeuRecord )` -> Status 200 + Automatically Serializes into JSON.
- `Results.Created('/rota', 'Msg')` -> Status 201 + Header "Location".
- `Results.NotFound` -> Status 404.
- `Results.BadRequest('Msg')` -> Status 400 bad request error.

---

## 5. Dext.Net Async Tasks and Resilience (TAsyncTask)

Dext includes more modern promises/tasks primitives than the pure `TTask` originals of Delphi.

```pascal
uses Dext.Core.Tasks; //Use Task Flow from the central library

TAsyncTask.Run<TUserProfile>(
  function: TUserProfile
  begin
    Result := ExternalService.Call();
  end)
  .OnComplete( //Callback chamado no contexto Sincrono/Main thread.
    procedure(Profile: TUserProfile)
    begin
        ShowVclMessage(Profile.Name);
    end)
  .OnException(
    procedure(Ex: Exception)
    begin
       LogError(Ex.Message);
    end)
  .Start;
```

---

## Review Checklist (Dext Framework)

- **Fluent routes?** Does the application use `Builder.MapGet`/`MapPost` with implicit binding instead of manual request manipulation and pure Body parse for complex json objects?
- **Has the DI container been powered?** Are instances being passed to constructors/routers through `App.Services`?
- **No Filter Strings in Data Modules?** Did you use expressive Smart Properties (`.Where(E.Price > 100)`) instead of query concat?
- **Are returns based on records and POLD objects?** (Plain Old Delphi Objects, allowing UTF-8 Zero Allocation JSON from Dext).
