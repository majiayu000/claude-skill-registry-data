---
name: "Delphi SOLID Patterns"
description: "SOLID implementation patterns for Delphi projects — Repository, Service, Factory, Strategy with constructor injection and interfaces"
---

# Delphi SOLID Patterns — Skill

Use this skill when the user requests the creation of classes, services, repositories or any structure that follows SOLID principles in Delphi.

## When to Use

- When creating a new domain **entity**
- When creating a **repository** (data access)
- When creating a **service** (business logic)
- When implementing a **use case**
- When applying any design pattern (Factory, Strategy, Observer)

## Repository Pattern

### Repository Interface

```pascal
unit MeuApp.Domain.Customer.Repository.Intf;

interface

uses
  System.Generics.Collections,
  MeuApp.Domain.Customer.Entity;

type
  /// <summary>
  ///   Interface para operations de leitura de customers.
  /// </summary>
  ICustomerReadRepository = interface
    ['{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}']
    function FindById(AId: Integer): TCustomer;
    function FindAll: TObjectList<TCustomer>;
    function FindByCpf(const ACpf: string): TCustomer;
  end;

  /// <summary>
  ///   Interface para operations de escrita de customers.
  /// </summary>
  ICustomerWriteRepository = interface
    ['{B2C3D4E5-F6A7-8901-BCDE-F12345678901}']
    procedure Insert(ACustomer: TCustomer);
    procedure Update(ACustomer: TCustomer);
    procedure Delete(AId: Integer);
  end;

  /// <summary>
  ///   Interface completa de repository combinando leitura e escrita.
  /// </summary>
  ICustomerRepository = interface(ICustomerReadRepository)
    ['{C3D4E5F6-A7B8-9012-CDEF-123456789012}']
    procedure Insert(ACustomer: TCustomer);
    procedure Update(ACustomer: TCustomer);
    procedure Delete(AId: Integer);
  end;

implementation

end.
```

### Implementation with FireDAC

```pascal
unit MeuApp.Infra.Customer.Repository;

interface

uses
  System.SysUtils,
  System.Generics.Collections,
  FireDAC.Comp.Client,
  MeuApp.Domain.Customer.Entity,
  MeuApp.Domain.Customer.Repository.Intf;

type
  TCustomerRepository = class(TInterfacedObject, ICustomerRepository)
  private
    FConnection: TFDConnection;
  public
    constructor Create(AConnection: TFDConnection);

    { ICustomerReadRepository }
    function FindById(AId: Integer): TCustomer;
    function FindAll: TObjectList<TCustomer>;
    function FindByCpf(const ACpf: string): TCustomer;

    { ICustomerWriteRepository }
    procedure Insert(ACustomer: TCustomer);
    procedure Update(ACustomer: TCustomer);
    procedure Delete(AId: Integer);
  end;

implementation

constructor TCustomerRepository.Create(AConnection: TFDConnection);
begin
  inherited Create;
  if not Assigned(AConnection) then
    raise EArgumentNilException.Create('AConnection cannot be nil');
  FConnection := AConnection;
end;

function TCustomerRepository.FindById(AId: Integer): TCustomer;
var
  LQuery: TFDQuery;
begin
  Result := nil;
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := FConnection;
    LQuery.SQL.Text := 'SELECT * FROM customers WHERE id = :id';
    LQuery.ParamByName('id').AsInteger := AId;
    LQuery.Open;

    if not LQuery.IsEmpty then
    begin
      Result := TCustomer.Create(LQuery.FieldByName('name').AsString);
      Result.Id := LQuery.FieldByName('id').AsInteger;
    end;
  finally
    LQuery.Free;
  end;
end;

// ... demais métodos seguem o mesmo default
```

## Service Pattern

### Service Interface

```pascal
unit MeuApp.Application.Customer.Service.Intf;

interface

uses
  MeuApp.Domain.Customer.Entity;

type
  ICustomerService = interface
    ['{D4E5F6A7-B8C9-0123-DEF0-234567890123}']
    function GetById(AId: Integer): TCustomer;
    procedure CreateCustomer(const AName: string; const ACpf: string);
    procedure UpdateCustomer(ACustomer: TCustomer);
    procedure DeleteCustomer(AId: Integer);
  end;

implementation

end.
```

### Service Implementation

```pascal
unit MeuApp.Application.Customer.Service;

interface

uses
  System.SysUtils,
  MeuApp.Domain.Customer.Entity,
  MeuApp.Domain.Customer.Repository.Intf,
  MeuApp.Application.Customer.Service.Intf;

type
  /// <summary>
  ///   Service de customers com validation e orquestraction de dependências.
  /// </summary>
  TCustomerService = class(TInterfacedObject, ICustomerService)
  private
    FRepository: ICustomerRepository;
    procedure ValidateCpf(const ACpf: string);
  public
    constructor Create(ARepository: ICustomerRepository);
    function GetById(AId: Integer): TCustomer;
    procedure CreateCustomer(const AName: string; const ACpf: string);
    procedure UpdateCustomer(ACustomer: TCustomer);
    procedure DeleteCustomer(AId: Integer);
  end;

implementation

constructor TCustomerService.Create(ARepository: ICustomerRepository);
begin
  inherited Create;
  if not Assigned(ARepository) then
    raise EArgumentNilException.Create('ARepository cannot be nil');
  FRepository := ARepository;
end;

function TCustomerService.GetById(AId: Integer): TCustomer;
begin
  Result := FRepository.FindById(AId);
  if not Assigned(Result) then
    raise EEntityNotFoundException.CreateFmt('Customer not found: %d', [AId]);
end;

procedure TCustomerService.CreateCustomer(const AName: string; const ACpf: string);
var
  LCustomer: TCustomer;
  LExisting: TCustomer;
begin
  ValidateCpf(ACpf);

  LExisting := FRepository.FindByCpf(ACpf);
  if Assigned(LExisting) then
    raise EBusinessRuleException.CreateFmt('CPF already registered: %s', [ACpf]);

  LCustomer := TCustomer.Create(AName);
  try
    LCustomer.Cpf := ACpf;
    FRepository.Insert(LCustomer);
  except
    LCustomer.Free;
    raise;
  end;
end;

procedure TCustomerService.ValidateCpf(const ACpf: string);
const
  CPF_LENGTH = 11;
begin
  if ACpf.Trim.IsEmpty then
    raise EValidationException.Create('CPF cannot be empty');
  if ACpf.Length <> CPF_LENGTH then
    raise EValidationException.CreateFmt('CPF must have %d digits', [CPF_LENGTH]);
end;

// ... demais métodos
```

## Factory Pattern

```pascal
unit MeuApp.Infra.Factory;

interface

uses
  FireDAC.Comp.Client,
  MeuApp.Domain.Customer.Repository.Intf,
  MeuApp.Application.Customer.Service.Intf;

type
  /// <summary>
  ///   Factory para criar instâncias de services e repositories.
  /// </summary>
  TServiceFactory = class
  public
    class function CreateCustomerRepository(AConnection: TFDConnection): ICustomerRepository;
    class function CreateCustomerService(AConnection: TFDConnection): ICustomerService;
  end;

implementation

uses
  MeuApp.Infra.Customer.Repository,
  MeuApp.Application.Customer.Service;

class function TServiceFactory.CreateCustomerRepository(AConnection: TFDConnection): ICustomerRepository;
begin
  Result := TCustomerRepository.Create(AConnection);
end;

class function TServiceFactory.CreateCustomerService(AConnection: TFDConnection): ICustomerService;
var
  LRepo: ICustomerRepository;
begin
  LRepo := CreateCustomerRepository(AConnection);
  Result := TCustomerService.Create(LRepo);
end;
```

## Strategy Pattern

```pascal
unit MeuApp.Domain.Tax.Strategy;

interface

type
  /// <summary>
  ///   Interface para estratégias de cálculo de imposto.
  /// </summary>
  ITaxCalculator = interface
    ['{E5F6A7B8-C9D0-1234-EF01-345678901234}']
    function Calculate(ABaseValue: Currency): Currency;
    function GetDescription: string;
  end;

  TSimplesTaxCalculator = class(TInterfacedObject, ITaxCalculator)
  public
    function Calculate(ABaseValue: Currency): Currency;
    function GetDescription: string;
  end;

  TLucroPresumidoTaxCalculator = class(TInterfacedObject, ITaxCalculator)
  public
    function Calculate(ABaseValue: Currency): Currency;
    function GetDescription: string;
  end;

implementation

{ TSimplesTaxCalculator }

function TSimplesTaxCalculator.Calculate(ABaseValue: Currency): Currency;
const
  SIMPLES_RATE = 0.06;
begin
  Result := ABaseValue * SIMPLES_RATE;
end;

function TSimplesTaxCalculator.GetDescription: string;
begin
  Result := 'Simples Nacional (6%)';
end;

{ TLucroPresumidoTaxCalculator }

function TLucroPresumidoTaxCalculator.Calculate(ABaseValue: Currency): Currency;
const
  LUCRO_PRESUMIDO_RATE = 0.15;
begin
  Result := ABaseValue * LUCRO_PRESUMIDO_RATE;
end;

function TLucroPresumidoTaxCalculator.GetDescription: string;
begin
  Result := 'Lucro Presumido (15%)';
end;
```

## Checklist for New Implementations

When creating any new functionality, check:

- [ ] Interface defined in the Domain?
- [ ] Implementation in Infrastructure?
- [ ] Service in Application with constructor injection?
- [ ] Factory method updated?
- [ ] Guard clauses at the beginning of methods?
- [ ] Try/finally for temporary objects?
- [ ] Names following conventions (T, I, E, F, A, L)?
- [ ] XMLDoc in public methods?
- [ ] Methods ≤ 20 lines?
- [ ] No `with`, no global variables, no magic numbers?
