---
name: "Horse Framework"
description: "Patterns for developing REST APIs with Horse framework in Delphi"
---

# Horse Framework — Skill

Use this skill when creating REST APIs with the **Horse** framework in Delphi.

## When to Use

- When creating a new REST API project
- When adding routes and endpoints
- When implementing middleware (JWT, CORS, logging)
- When integrating Horse with FireDAC

## About Horse

Horse is a minimalist and performant REST framework for Delphi, inspired by Express.js (Node.js). It uses the middleware chain concept and is extremely simple to configure.

- **Repository:** [github.com/HashLoad/horse](https://github.com/HashLoad/horse)
- **Installation:** Boss (`boss install horse`) or manual

## Project Structure

```
src/
├── MeuApp.dpr                          ← Projeto principal
├── Controllers/
│   ├── MeuApp.Controller.Customer.pas
│   ├── MeuApp.Controller.Product.pas
│   └── MeuApp.Controller.Health.pas
├── Middleware/
│   ├── MeuApp.Middleware.Auth.pas
│   ├── MeuApp.Middleware.Logger.pas
│   └── MeuApp.Middleware.CORS.pas
├── Domain/
│   ├── MeuApp.Domain.Customer.Entity.pas
│   └── MeuApp.Domain.Customer.Repository.Intf.pas
├── Application/
│   └── MeuApp.Application.Customer.Service.pas
├── Infrastructure/
│   └── MeuApp.Infra.Customer.Repository.pas
└── Config/
    └── MeuApp.Config.Server.pas
```

## Basic Server Configuration

```pascal
program MeuApp;

{$APPTYPE CONSOLE}

uses
  Horse,
  Horse.Jhonson,       //JSON middleware
  Horse.CORS,          //CORS middleware
  Horse.HandleException,
  MeuApp.Controller.Customer,
  MeuApp.Controller.Health;

begin
  THorse.Use(Jhonson);
  THorse.Use(CORS);
  THorse.Use(HandleException);

  //Register broken
  TCustomerController.RegisterRoutes;
  THealthController.RegisterRoutes;

  THorse.Listen(9000,
    procedure
    begin
      Writeln('Server running on port 9000');
    end
  );
end.
```

## Controller Pattern

```pascal
unit MeuApp.Controller.Customer;

interface

uses
  Horse,
  System.JSON;

type
  TCustomerController = class
  public
    class procedure RegisterRoutes;
  private
    class procedure GetAll(AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
    class procedure GetById(AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
    class procedure Create(AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
    class procedure Update(AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
    class procedure Delete(AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
  end;

implementation

uses
  System.SysUtils,
  MeuApp.Application.Customer.Service.Intf;

class procedure TCustomerController.RegisterRoutes;
begin
  THorse.Get('/api/customers', GetAll);
  THorse.Get('/api/customers/:id', GetById);
  THorse.Post('/api/customers', Create);
  THorse.Put('/api/customers/:id', Update);
  THorse.Delete('/api/customers/:id', Delete);
end;

class procedure TCustomerController.GetAll(
  AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
var
  LService: ICustomerService;
  LResult: TJSONArray;
begin
  LService := TServiceFactory.CreateCustomerService;
  LResult := LService.GetAllAsJSON;
  ARes.Send<TJSONArray>(LResult).Status(THTTPStatus.OK);
end;

class procedure TCustomerController.GetById(
  AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
var
  LService: ICustomerService;
  LId: Integer;
  LResult: TJSONObject;
begin
  LId := AReq.Params['id'].ToInteger;
  LService := TServiceFactory.CreateCustomerService;

  LResult := LService.GetByIdAsJSON(LId);
  if not Assigned(LResult) then
  begin
    ARes.Send('Customer not found').Status(THTTPStatus.NotFound);
    Exit;
  end;

  ARes.Send<TJSONObject>(LResult).Status(THTTPStatus.OK);
end;

class procedure TCustomerController.Create(
  AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
var
  LService: ICustomerService;
  LBody: TJSONObject;
begin
  LBody := AReq.Body<TJSONObject>;
  LService := TServiceFactory.CreateCustomerService;

  try
    LService.CreateFromJSON(LBody);
    ARes.Send('Created').Status(THTTPStatus.Created);
  except
    on E: EValidationException do
      ARes.Send(E.Message).Status(THTTPStatus.BadRequest);
    on E: EBusinessRuleException do
      ARes.Send(E.Message).Status(THTTPStatus.Conflict);
  end;
end;
```

## Custom Middleware

```pascal
unit MeuApp.Middleware.Auth;

interface

uses
  Horse;

procedure AuthMiddleware(AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);

implementation

uses
  System.SysUtils,
  Horse.JWT;

procedure AuthMiddleware(AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
var
  LToken: string;
begin
  LToken := AReq.Headers['Authorization'];

  if LToken.IsEmpty then
  begin
    ARes.Send('Token not provided').Status(THTTPStatus.Unauthorized);
    Exit;
  end;

  //Validar token JWT
  if not ValidateJWTToken(LToken) then
  begin
    ARes.Send('Invalid token').Status(THTTPStatus.Unauthorized);
    Exit;
  end;

  ANext; //continue to the next handler
end;

end.
```

## Logger Middleware

```pascal
unit MeuApp.Middleware.Logger;

interface

uses
  Horse;

procedure LoggerMiddleware(AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);

implementation

uses
  System.SysUtils,
  System.DateUtils;

procedure LoggerMiddleware(AReq: THorseRequest; ARes: THorseResponse; ANext: TProc);
var
  LStartTime: TDateTime;
begin
  LStartTime := Now;
  Writeln(Format('[%s] %s %s',
    [FormatDateTime('hh:nn:ss', Now),
     AReq.MethodType.ToString,
     AReq.RawWebRequest.PathInfo]));

  ANext;

  Writeln(Format('[%s] Completed in %dms',
    [FormatDateTime('hh:nn:ss', Now),
     MilliSecondsBetween(Now, LStartTime)]));
end;

end.
```

## Conventions for Horse

| Appearance | Convention |
|---------|-----------|
| **URLs** | Kebab-case, plural: `/api/customers`, `/api/order-items` |
| **HTTP Methods** | GET (list/search), POST (create), PUT (update), DELETE (remove) |
| **Status** | 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal |
| **Response** | Always JSON via `Jhonson` middleware |
| **Controller** | Static class methods with `RegisterRoutes` |
| **Middleware** | Standalone procedures or class methods |
| **Parameters** | Path: `AReq.Params['id']`, Query: `AReq.Query['search']` |

## Horse Add-on Packages

| Package | Usage | Boss Installation |
|--------|-----|-----------------|
| `horse-jhonson` | JSON middleware | `boss install horse-jhonson` |
| `horse-cors` | CORS | `boss install horse-cors` |
| `horse-jwt` | JWT Authentication | `boss install horse-jwt` |
| `horse-basic-auth` | Basic Auth | `boss install horse-basic-auth` |
| `horse-handle-exception` | Error handler | `boss install horse-handle-exception` |
| `horse-octet-stream` | Upload/download | `boss install horse-octet-stream` |

## Checklist for Horse Projects

- [ ] `Jhonson` registered middleware for automatic JSON?
- [ ] `CORS` registered middleware?
- [ ] `HandleException` middleware for error handling?
- [ ] Routes follow RESTful convention (plural, kebab-case)?
- [ ] Controllers use Services (do not access direct repository)?
- [ ] Guard clauses in handlers before logic?
- [ ] Correct HTTP status in responses?
- [ ] Integration tests with `TRESTClient` simulating calls?
