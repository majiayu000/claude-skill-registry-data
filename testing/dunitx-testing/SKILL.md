---
name: "DUnitX Testing Patterns"
description: "Unit testing patterns with DUnitX for Delphi — fixtures, mocking, integration tests"
---

# DUnitX Testing Patterns — Skill

Use this skill when creating or organizing unit tests in Delphi projects.

## When to Use

- When creating tests for new features
- When applying TDD (Test-Driven Development)
- When creating database integration tests
- When refactoring existing tests

## Test Project Structure

```
tests/
├── MeuApp.Tests.dpr                 ← Projeto de testes
├── Domain/
│   ├── MeuApp.Tests.Customer.Entity.pas
│   └── MeuApp.Tests.Order.Entity.pas
├── Application/
│   ├── MeuApp.Tests.Customer.Service.pas
│   └── MeuApp.Tests.Order.Service.pas
├── Infrastructure/
│   └── MeuApp.Tests.Customer.Repository.pas
└── Helpers/
    ├── MeuApp.Tests.Helpers.Database.pas
    └── MeuApp.Tests.Helpers.Mocks.pas
```

## Basic Test Fixture

```pascal
unit MeuApp.Tests.Customer.Service;

interface

uses
  DUnitX.TestFramework,
  MeuApp.Domain.Customer.Entity,
  MeuApp.Domain.Customer.Repository.Intf,
  MeuApp.Application.Customer.Service;

type
  [TestFixture]
  TCustomerServiceTest = class
  private
    FService: TCustomerService;
    FMockRepo: ICustomerRepository;
  public
    [Setup]
    procedure Setup;

    [TearDown]
    procedure TearDown;

    [Test]
    procedure CreateCustomer_WithValidData_ShouldSucceed;

    [Test]
    procedure CreateCustomer_WithEmptyName_ShouldRaiseException;

    [Test]
    procedure CreateCustomer_WithDuplicateCpf_ShouldRaiseException;

    [Test]
    procedure GetById_WithExistingId_ShouldReturnCustomer;

    [Test]
    procedure GetById_WithInvalidId_ShouldRaiseNotFoundException;
  end;

implementation

uses
  System.SysUtils;

{ TCustomerServiceTest }

procedure TCustomerServiceTest.Setup;
begin
  FMockRepo := TMemoryCustomerRepository.Create;
  FService := TCustomerService.Create(FMockRepo);
end;

procedure TCustomerServiceTest.TearDown;
begin
  FService.Free;
  // FMockRepo é interface — liberado automaticamente
end;

[Test]
procedure TCustomerServiceTest.CreateCustomer_WithValidData_ShouldSucceed;
begin
  Assert.WillNotRaiseAny(
    procedure
    begin
      FService.CreateCustomer('João Silva', '12345678901', 'joao@email.com');
    end
  );
end;

[Test]
procedure TCustomerServiceTest.CreateCustomer_WithEmptyName_ShouldRaiseException;
begin
  Assert.WillRaise(
    procedure
    begin
      FService.CreateCustomer('', '12345678901', 'joao@email.com');
    end,
    EValidationException
  );
end;

[Test]
procedure TCustomerServiceTest.CreateCustomer_WithDuplicateCpf_ShouldRaiseException;
begin
  FService.CreateCustomer('João', '12345678901', 'joao@email.com');

  Assert.WillRaise(
    procedure
    begin
      FService.CreateCustomer('Maria', '12345678901', 'maria@email.com');
    end,
    EBusinessRuleException
  );
end;

[Test]
procedure TCustomerServiceTest.GetById_WithExistingId_ShouldReturnCustomer;
var
  LCustomer: TCustomer;
begin
  FService.CreateCustomer('João', '12345678901', 'joao@email.com');

  LCustomer := FService.GetById(1);
  try
    Assert.IsNotNull(LCustomer);
    Assert.AreEqual('João', LCustomer.Name);
  finally
    LCustomer.Free;
  end;
end;

[Test]
procedure TCustomerServiceTest.GetById_WithInvalidId_ShouldRaiseNotFoundException;
begin
  Assert.WillRaise(
    procedure
    begin
      FService.GetById(999);
    end,
    EEntityNotFoundException
  );
end;

initialization
  TDUnitX.RegisterTestFixture(TCustomerServiceTest);

end.
```

## Mock Repository (in memory)

```pascal
unit MeuApp.Tests.Helpers.Mocks;

interface

uses
  System.SysUtils,
  System.Generics.Collections,
  MeuApp.Domain.Customer.Entity,
  MeuApp.Domain.Customer.Repository.Intf;

type
  TMemoryCustomerRepository = class(TInterfacedObject, ICustomerRepository)
  private
    FItems: TObjectList<TCustomer>;
    FNextId: Integer;
  public
    constructor Create;
    destructor Destroy; override;

    function FindById(AId: Integer): TCustomer;
    function FindAll: TObjectList<TCustomer>;
    function FindByCpf(const ACpf: string): TCustomer;
    function Exists(AId: Integer): Boolean;
    procedure Insert(ACustomer: TCustomer);
    procedure Update(ACustomer: TCustomer);
    procedure Delete(AId: Integer);
  end;

implementation

constructor TMemoryCustomerRepository.Create;
begin
  inherited Create;
  FItems := TObjectList<TCustomer>.Create(False);
  FNextId := 1;
end;

destructor TMemoryCustomerRepository.Destroy;
begin
  FItems.Free;
  inherited;
end;

procedure TMemoryCustomerRepository.Insert(ACustomer: TCustomer);
begin
  ACustomer.Id := FNextId;
  Inc(FNextId);
  FItems.Add(ACustomer);
end;

// ... demais métodos seguem o mesmo default
```

## Test Naming Conventions

```
MethodName_Scenario_ExpectedBehavior
```

| Example | Meaning |
|---------|-------------|
| `CreateCustomer_WithValidData_ShouldSucceed` | Happy scenery |
| `CreateCustomer_WithEmptyName_ShouldRaiseException` | Validation |
| `GetById_WithInvalidId_ShouldRaiseNotFoundException` | Not found |
| `Delete_WhenItemHasDependencies_ShouldRaiseException` | Business rule |

## DUnitX Common Assertions

```pascal
// Igualdade
Assert.AreEqual(Expected, Actual);
Assert.AreEqual('João', LCustomer.Name);

// Nulidade
Assert.IsNotNull(LCustomer);
Assert.IsNull(LResult);

// Booleanos
Assert.IsTrue(LCustomer.IsActive);
Assert.IsFalse(LOrder.IsCancelled);

// Exceptions
Assert.WillRaise(AnonProc, EValidationException);
Assert.WillNotRaiseAny(AnonProc);

// Contagem
Assert.AreEqual(3, LList.Count);
```

## Integration Test with SQLite in Memory

```pascal
[TestFixture]
TCustomerRepositoryIntegrationTest = class
private
  FConnection: TFDConnection;
  FRepository: ICustomerRepository;
public
  [Setup]
  procedure Setup;

  [TearDown]
  procedure TearDown;
end;

procedure TCustomerRepositoryIntegrationTest.Setup;
begin
  FConnection := TFDConnection.Create(nil);
  FConnection.DriverName := 'SQLite';
  FConnection.Params.Database := ':memory:';
  FConnection.Connected := True;

  // Criar schema
  FConnection.ExecSQL(
    'CREATE TABLE customers (' +
    '  id INTEGER PRIMARY KEY AUTOINCREMENT,' +
    '  name TEXT NOT NULL,' +
    '  cpf TEXT NOT NULL,' +
    '  email TEXT,' +
    '  status INTEGER DEFAULT 0' +
    ')'
  );

  FRepository := TFireDACCustomerRepository.Create(FConnection);
end;

procedure TCustomerRepositoryIntegrationTest.TearDown;
begin
  FConnection.Free;
end;
```

## Test Checklist

- [ ] Test name follows `MethodName_Scenario_ExpectedBehavior`?
- [ ] Clean setup and TearDown without side effects?
- [ ] Test checks ONE thing?
- [ ] Objects released correctly in TearDown and in try/finally?
- [ ] Mock repository used for Service testing?
- [ ] SQLite `:memory:` used for Repository integration testing?
- [ ] Test happy scenario AND error scenarios?
