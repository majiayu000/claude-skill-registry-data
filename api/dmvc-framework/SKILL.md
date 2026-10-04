---
name: "DelphiMVCFramework"
description: "Patterns for development with DelphiMVCFramework (DMVC) — controllers, Active Record, JWT, Swagger"
---

# DelphiMVCFramework (DMVC) — Skill

Use this skill when creating web applications and REST APIs with **DelphiMVCFramework**.

## When to Use

- When creating REST APIs with MVC architecture
- When using Active Record for data access
- When implementing JWT authentication
- When generating Swagger/OpenAPI documentation

## About DMVC

DelphiMVCFramework is the most complete MVC framework for Delphi, created by Daniele Teti. Supports RESTful APIs, Server-Sent Events, WebSockets, Active Record, JSON/XML serialization and more.

- **Repository:** [github.com/danieleteti/delphimvcframework](https://github.com/danieleteti/delphimvcframework)
- **Installation:** Clone repository and add paths, or via Boss/Delphinus

## Project Structure

```
src/
├── MeuApp.dpr                          ← Projeto principal
├── MeuApp.WebModule.pas                ← WebModule com engine DMVC
├── Controllers/
│   ├── MeuApp.Controller.Customer.pas
│   ├── MeuApp.Controller.Product.pas
│   └── MeuApp.Controller.Base.pas
├── Models/
│   ├── MeuApp.Model.Customer.pas       ← Active Record
│   ├── MeuApp.Model.Product.pas
│   └── MeuApp.Model.Base.pas
├── Services/
│   └── MeuApp.Service.Customer.pas
├── Middleware/
│   ├── MeuApp.Middleware.Auth.pas
│   └── MeuApp.Middleware.CORS.pas
└── Config/
    └── MeuApp.Config.pas
```

## WebModule (Bootstrap)

```pascal
unit MeuApp.WebModule;

interface

uses
  System.SysUtils,
  System.Classes,
  Web.HTTPApp,
  MVCFramework,
  MVCFramework.Commons;

type
  TAppWebModule = class(TWebModule)
    procedure WebModuleCreate(Sender: TObject);
    procedure WebModuleDestroy(Sender: TObject);
  private
    FMVCEngine: TMVCEngine;
  end;

implementation

uses
  MVCFramework.Middleware.CORS,
  MVCFramework.Middleware.JWT,
  MVCFramework.Middleware.StaticFiles,
  MeuApp.Controller.Customer,
  MeuApp.Controller.Product;

procedure TAppWebModule.WebModuleCreate(Sender: TObject);
begin
  FMVCEngine := TMVCEngine.Create(Self,
    procedure(AConfig: TMVCConfig)
    begin
      AConfig[TMVCConfigKey.DocumentRoot] := 'public';
      AConfig[TMVCConfigKey.DefaultContentType] := TMVCMediaType.APPLICATION_JSON;
      AConfig[TMVCConfigKey.DefaultViewFileExtension] := 'html';
    end
  );

  // Controllers
  FMVCEngine.AddController(TCustomerController);
  FMVCEngine.AddController(TProductController);

  // Middleware
  FMVCEngine.AddMiddleware(TMVCCORSMiddleware.Create);
end;

procedure TAppWebModule.WebModuleDestroy(Sender: TObject);
begin
  FMVCEngine.Free;
end;
```

## Controller Pattern

```pascal
unit MeuApp.Controller.Customer;

interface

uses
  MVCFramework,
  MVCFramework.Commons,
  MVCFramework.Serializer.Commons;

type
  [MVCPath('/api/customers')]
  TCustomerController = class(TMVCController)
  public
    [MVCPath]
    [MVCHTTPMethod([httpGET])]
    [MVCProduces(TMVCMediaType.APPLICATION_JSON)]
    procedure GetAll;

    [MVCPath('/($id)')]
    [MVCHTTPMethod([httpGET])]
    [MVCProduces(TMVCMediaType.APPLICATION_JSON)]
    procedure GetById(const AId: Integer);

    [MVCPath]
    [MVCHTTPMethod([httpPOST])]
    [MVCConsumes(TMVCMediaType.APPLICATION_JSON)]
    [MVCProduces(TMVCMediaType.APPLICATION_JSON)]
    procedure CreateCustomer;

    [MVCPath('/($id)')]
    [MVCHTTPMethod([httpPUT])]
    [MVCConsumes(TMVCMediaType.APPLICATION_JSON)]
    procedure UpdateCustomer(const AId: Integer);

    [MVCPath('/($id)')]
    [MVCHTTPMethod([httpDELETE])]
    procedure DeleteCustomer(const AId: Integer);
  end;

implementation

uses
  System.SysUtils,
  MVCFramework.ActiveRecord,
  MeuApp.Model.Customer;

procedure TCustomerController.GetAll;
var
  LCustomers: TMVCActiveRecordList;
begin
  LCustomers := TMVCActiveRecord.SelectRQL<TCustomer>('', 100);
  Render<TCustomer>(LCustomers);
end;

procedure TCustomerController.GetById(const AId: Integer);
var
  LCustomer: TCustomer;
begin
  LCustomer := TMVCActiveRecord.GetByPK<TCustomer>(AId);
  if not Assigned(LCustomer) then
  begin
    Render(HTTP_STATUS.NotFound, 'Customer not found');
    Exit;
  end;
  Render(LCustomer);
end;

procedure TCustomerController.CreateCustomer;
var
  LCustomer: TCustomer;
begin
  LCustomer := Context.Request.BodyAs<TCustomer>;
  try
    LCustomer.Insert;
    Render201Created('/api/customers/' + LCustomer.Id.ToString);
  except
    on E: Exception do
    begin
      LCustomer.Free;
      raise;
    end;
  end;
end;

procedure TCustomerController.UpdateCustomer(const AId: Integer);
var
  LCustomer: TCustomer;
begin
  LCustomer := Context.Request.BodyAs<TCustomer>;
  try
    LCustomer.Id := AId;
    LCustomer.Update;
    Render(HTTP_STATUS.OK, 'Updated');
  except
    on E: Exception do
    begin
      LCustomer.Free;
      raise;
    end;
  end;
end;

procedure TCustomerController.DeleteCustomer(const AId: Integer);
var
  LCustomer: TCustomer;
begin
  LCustomer := TMVCActiveRecord.GetByPK<TCustomer>(AId);
  if not Assigned(LCustomer) then
  begin
    Render(HTTP_STATUS.NotFound, 'Customer not found');
    Exit;
  end;

  try
    LCustomer.Delete;
    Render(HTTP_STATUS.NoContent, '');
  finally
    LCustomer.Free;
  end;
end;
```

## Active Record (Model)

```pascal
unit MeuApp.Model.Customer;

interface

uses
  MVCFramework.ActiveRecord,
  MVCFramework.Serializer.Commons;

type
  [MVCTable('customers')]
  [MVCNameCase(ncLowerCase)]
  TCustomer = class(TMVCActiveRecord)
  private
    [MVCTableField('id', [foPrimaryKey, foAutoGenerated])]
    FId: Integer;

    [MVCTableField('name')]
    FName: string;

    [MVCTableField('cpf')]
    FCpf: string;

    [MVCTableField('email')]
    FEmail: string;

    [MVCTableField('status')]
    FStatus: Integer;

    [MVCTableField('created_at')]
    FCreatedAt: TDateTime;
  public
    property Id: Integer read FId write FId;
    property Name: string read FName write FName;
    property Cpf: string read FCpf write FCpf;
    property Email: string read FEmail write FEmail;
    property Status: Integer read FStatus write FStatus;
    property CreatedAt: TDateTime read FCreatedAt write FCreatedAt;
  end;

implementation

end.
```

## JWT Middleware

```pascal
uses
  MVCFramework.Middleware.JWT;

// No WebModule:
FMVCEngine.AddMiddleware(
  TMVCJWTAuthenticationMiddleware.Create(
    TAuthHandler.Create,   // implementa IMVCAuthenticationHandler
    'my-secret-key',
    '/api/login',          // rota pública de login
    [TJWTCheckableClaim.ExpirationTime]
  )
);
```

## RQL (Resource Query Language)

```pascal
// Filtrar via query string (DMVC interpreta RQL automaticamente)
// GET /api/customers?$filter=contains(name,'João')&$orderby=name&$top=10

LCustomers := TMVCActiveRecord.SelectRQL<TCustomer>(
  Context.Request.QueryStringParam('$filter'),
  Context.Request.QueryStringParam('$top').ToInteger
);
```

## DMVC Conventions

| Appearance | Convention |
|---------|-----------|
| **Controller** | Inherits from `TMVCController` with `[MVCPath]` attribute |
| **Models** | Inherits from `TMVCActiveRecord` with `[MVCTable]` attribute |
| **Routes** | Attributes: `[MVCPath]`, `[MVCHTTPMethod]` |
| **Serialization** | Automatic via `Render()` (JSON by default) |
| **Parameters** | Path: `($id)`, Query: `Context.Request.QueryStringParam` |
| **Body** | `Context.Request.BodyAs<T>` to deserialize JSON |
| **Status** | `Render(HTTP_STATUS.OK)`, `Render201Created` |
| **Middleware** | Inherits from `TMVCCustomMiddleware` or uses built-in |
| **Swagger** | Attributes `[MVCSwagSummary]`, `[MVCSwagParam]` |

## Checklist for DMVC Projects

- [ ] WebModule configured with `TMVCEngine`?
- [ ] Controllers registered with `AddController`?
- [ ] CORS middleware added?
- [ ] Active Record models with `[MVCTable]` and `[MVCTableField]`?
- [ ] Do routes follow the RESTful standard?
- [ ] `Render()` used for all answers?
- [ ] JWT middleware for protected routes?
- [ ] `BodyAs<T>` objects released in case of exception?
